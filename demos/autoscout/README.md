# AUTO-SCOUT mini demo

A clean-room, synthetic-only Python/SQLite example of manual intake, state changes, immutable audit events, idempotent imports, and checked backups. It is **not** a copy of the private AUTO-SCOUT repository.

From repository root, use Python 3.11+:

```bash
python -m demos.autoscout.cli --db /tmp/synthetic-scout.sqlite3 init
python -m demos.autoscout.cli --db /tmp/synthetic-scout.sqlite3 import --file demos/autoscout/leads.json
python -m demos.autoscout.cli --db /tmp/synthetic-scout.sqlite3 list
python -m demos.autoscout.cli --db /tmp/synthetic-scout.sqlite3 decide --id SYN-101 --state SHORTLIST --reason "Human review complete" --confirm-owner
python -m demos.autoscout.cli --db /tmp/synthetic-scout.sqlite3 audit
python -m demos.autoscout.cli --db /tmp/synthetic-scout.sqlite3 backup --out /tmp/synthetic-scout-copy.sqlite3
python -m demos.autoscout.cli --db /tmp/synthetic-scout-copy.sqlite3 verify
```

On Windows, substitute a writable directory such as `C:\\Temp` for `/tmp`. Backup names must be new: existing destinations are never overwritten. No external requests, data harvesting, real opportunities, or automatic submissions are implemented.

**Design boundaries:** invalid input rolls back atomically; exact duplicate IDs are skipped, conflicting IDs rejected; decisions require explicit `--confirm-owner`; event history records every import and decision. This demo omits authentication, authorization beyond a user-supplied CLI confirmation, encryption, and multi-user concurrency guarantees. Do not use it for business or personal data.
