"""Synthetic local opportunity intake. No scraping, messaging, or external APIs."""
from __future__ import annotations

from datetime import datetime, timezone
from contextlib import contextmanager, closing
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
from typing import Any

STATES = frozenset({"HOLD", "SHORTLIST", "SKIP"})
IDENTIFIER = re.compile(r"[A-Za-z0-9_-]{3,40}\Z")
REQUIRED_TABLES = {"leads", "audit_events"}


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def _connect(path: str | Path, *, create: bool = False):
    path = Path(path)
    if not create and not path.is_file():
        raise ValueError(f"Database does not exist: {path}")
    if not path.parent.is_dir():
        raise ValueError("Database parent directory must already exist")
    conn = sqlite3.connect(str(path), timeout=5)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def initialize(path: str | Path) -> None:
    with _connect(path, create=True) as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                amount INTEGER,
                state TEXT NOT NULL DEFAULT 'HOLD'
                    CHECK (state IN ('HOLD','SHORTLIST','SKIP')),
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_events (
                seq INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id TEXT NOT NULL REFERENCES leads(id),
                event_type TEXT NOT NULL,
                old_state TEXT,
                new_state TEXT NOT NULL,
                reason TEXT NOT NULL,
                actor TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            """
        )


def _validated(row: Any) -> dict[str, Any]:
    if not isinstance(row, dict) or set(row) != {"id", "title", "source", "amount"}:
        raise ValueError("Each lead needs only: id, title, source, amount")
    identifier = row["id"]
    if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
        raise ValueError("Invalid lead ID; use 3-40 alphanumeric/underscore/hyphen chars")
    title, source, amount = row["title"], row["source"], row["amount"]
    if not isinstance(title, str) or not (1 <= len(title.strip()) <= 120):
        raise ValueError("Title must be 1-120 characters")
    if not isinstance(source, str) or not (1 <= len(source.strip()) <= 80):
        raise ValueError("Source must be 1-80 characters")
    if amount is not None and (type(amount) is not int or amount < 0 or amount > 100_000_000):
        raise ValueError("Amount must be null or an integer from 0 to 100000000")
    return {"id": identifier, "title": title.strip(), "source": source.strip(), "amount": amount}


def import_records(path: str | Path, payload: Any) -> tuple[int, int]:
    """Atomic import; exact duplicates are idempotent, conflicting IDs fail."""
    if not isinstance(payload, list) or not (1 <= len(payload) <= 200):
        raise ValueError("Input must be a JSON list of 1-200 synthetic leads")
    rows = [_validated(item) for item in payload]
    local: dict[str, dict[str, Any]] = {}
    for row in rows:
        if row["id"] in local and local[row["id"]] != row:
            raise ValueError("Conflicting IDs inside input batch")
        local[row["id"]] = row

    created, skipped = 0, 0
    with _connect(path) as db:
        with db:
            for row in rows:
                old = db.execute(
                    "SELECT id,title,source,amount FROM leads WHERE id=?", (row["id"],)
                ).fetchone()
                if old is not None:
                    if any(old[field] != row[field] for field in row):
                        raise ValueError(f"Conflicting existing record: {row['id']}")
                    skipped += 1
                    continue
                db.execute(
                    "INSERT INTO leads(id,title,source,amount,created_at) VALUES(?,?,?,?,?)",
                    (row["id"], row["title"], row["source"], row["amount"], _timestamp()),
                )
                db.execute(
                    "INSERT INTO audit_events(lead_id,event_type,old_state,new_state,reason,actor,created_at) "
                    "VALUES(?, 'IMPORT', NULL, 'HOLD', 'manual synthetic intake', 'system', ?)",
                    (row["id"], _timestamp()),
                )
                created += 1
    return created, skipped


def read_leads(path: str | Path) -> list[dict[str, Any]]:
    with _connect(path) as db:
        return [dict(row) for row in db.execute("SELECT * FROM leads ORDER BY id")]


def read_audit(path: str | Path) -> list[dict[str, Any]]:
    with _connect(path) as db:
        return [dict(row) for row in db.execute("SELECT * FROM audit_events ORDER BY seq")]


def decide(
    path: str | Path, identifier: str, new_state: str, reason: str, *, owner_confirmed: bool = False
) -> None:
    if owner_confirmed is not True:
        raise PermissionError("Manual owner confirmation required; no autonomous decisions")
    if new_state not in STATES:
        raise ValueError("Unsupported state")
    if not isinstance(reason, str) or not 5 <= len(reason.strip()) <= 300:
        raise ValueError("Provide a reason between 5 and 300 characters")
    with _connect(path) as db:
        with db:
            row = db.execute("SELECT state FROM leads WHERE id=?", (identifier,)).fetchone()
            if row is None:
                raise ValueError("Unknown lead ID")
            if row["state"] == new_state:
                raise ValueError("Decision would not change the state")
            db.execute("UPDATE leads SET state=? WHERE id=?", (new_state, identifier))
            db.execute(
                "INSERT INTO audit_events(lead_id,event_type,old_state,new_state,reason,actor,created_at) "
                "VALUES(?, 'DECISION', ?, ?, ?, 'owner', ?)",
                (identifier, row["state"], new_state, reason.strip(), _timestamp()),
            )


def verify_database(path: str | Path) -> None:
    with _connect(path) as db:
        integrity = db.execute("PRAGMA integrity_check").fetchone()[0]
        if integrity != "ok":
            raise ValueError("SQLite integrity check failed")
        if db.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise ValueError("Foreign key violations")
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not REQUIRED_TABLES.issubset(tables):
            raise ValueError("Missing expected tables")
        if db.execute("SELECT count(*) FROM leads WHERE state NOT IN ('HOLD','SHORTLIST','SKIP')").fetchone()[0]:
            raise ValueError("Invalid states")


def make_backup(source: str | Path, destination: str | Path) -> None:
    """Backup to a checked temp file; publish without replacing existing paths."""
    source, destination = Path(source), Path(destination)
    verify_database(source)
    if source.resolve() == destination.resolve() or destination.exists() or destination.is_symlink():
        raise FileExistsError("Destination must be new and different from source")
    if not destination.parent.is_dir():
        raise ValueError("Backup parent must already exist")
    fd, temp_name = tempfile.mkstemp(prefix=".autoscout-backup-", suffix=".sqlite3", dir=destination.parent)
    os.close(fd)
    try:
        with _connect(source) as src, closing(sqlite3.connect(temp_name)) as dst:
            src.backup(dst)
        verify_database(temp_name)
        os.link(temp_name, destination)
    finally:
        Path(temp_name).unlink(missing_ok=True)


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)
