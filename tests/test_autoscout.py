import json
from pathlib import Path
import sqlite3
from contextlib import closing
import tempfile
import unittest

from demos.autoscout.core import (
    decide, import_records, initialize, load_json, make_backup,
    read_audit, read_leads, verify_database,
)


class AutoScoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "scout.sqlite3"
        initialize(self.db)
        self.fixture = load_json("demos/autoscout/leads.json")

    def test_database_initially_empty_and_valid(self):
        verify_database(self.db)
        self.assertEqual(read_leads(self.db), [])

    def test_import_creates_hold_records_and_audit(self):
        self.assertEqual(import_records(self.db, self.fixture), (3, 0))
        self.assertEqual(len(read_leads(self.db)), 3)
        self.assertEqual([x["state"] for x in read_leads(self.db)], ["HOLD"] * 3)
        self.assertEqual([a["event_type"] for a in read_audit(self.db)], ["IMPORT"] * 3)

    def test_exact_duplicates_do_not_change_history(self):
        import_records(self.db, self.fixture)
        self.assertEqual(import_records(self.db, self.fixture), (0, 3))
        self.assertEqual(len(read_audit(self.db)), 3)

    def test_conflicting_existing_id_rolls_back_whole_batch(self):
        import_records(self.db, self.fixture[:1])
        altered = dict(self.fixture[0], title="Conflicting new title")
        with self.assertRaises(ValueError):
            import_records(self.db, [self.fixture[1], altered])
        self.assertEqual([x["id"] for x in read_leads(self.db)], ["SYN-101"])

    def test_conflicting_ids_inside_batch_fail(self):
        with self.assertRaises(ValueError):
            import_records(self.db, [self.fixture[0], dict(self.fixture[0], amount=3)])
        self.assertEqual(read_leads(self.db), [])

    def test_invalid_amount_bool_and_negative_rejected(self):
        for amount in [True, -1, 100_000_001, 1.5, "500"]:
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                import_records(self.db, [dict(self.fixture[0], amount=amount)])
        self.assertEqual(read_leads(self.db), [])

    def test_unexpected_fields_rejected(self):
        with self.assertRaises(ValueError):
            import_records(self.db, [dict(self.fixture[0], email="synthetic-placeholder")])

    def test_empty_and_oversized_batch_rejected(self):
        with self.assertRaises(ValueError):
            import_records(self.db, [])
        with self.assertRaises(ValueError):
            import_records(self.db, self.fixture[:1] * 201)

    def test_owner_confirmation_required(self):
        import_records(self.db, self.fixture[:1])
        with self.assertRaises(PermissionError):
            decide(self.db, "SYN-101", "SHORTLIST", "Reviewed candidate")
        self.assertEqual(read_leads(self.db)[0]["state"], "HOLD")

    def test_decision_creates_owner_audit(self):
        import_records(self.db, self.fixture[:1])
        decide(self.db, "SYN-101", "SHORTLIST", "Reviewed candidate", owner_confirmed=True)
        self.assertEqual(read_leads(self.db)[0]["state"], "SHORTLIST")
        self.assertEqual(read_audit(self.db)[-1]["actor"], "owner")

    def test_same_state_and_short_reason_rejected(self):
        import_records(self.db, self.fixture[:1])
        with self.assertRaises(ValueError):
            decide(self.db, "SYN-101", "HOLD", "long enough", owner_confirmed=True)
        with self.assertRaises(ValueError):
            decide(self.db, "SYN-101", "SKIP", "no", owner_confirmed=True)

    def test_backup_is_verified_and_recoverable(self):
        import_records(self.db, self.fixture)
        backup = Path(self.temp.name) / "backup.sqlite3"
        make_backup(self.db, backup)
        verify_database(backup)
        self.assertEqual(read_leads(backup), read_leads(self.db))
        self.assertEqual(read_audit(backup), read_audit(self.db))

    def test_backup_never_overwrites(self):
        backup = Path(self.temp.name) / "backup.sqlite3"
        backup.write_text("keep me", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            make_backup(self.db, backup)
        self.assertEqual(backup.read_text(encoding="utf-8"), "keep me")

    def test_cannot_backup_into_original(self):
        with self.assertRaises(FileExistsError):
            make_backup(self.db, self.db)

    def test_invalid_database_is_not_accepted(self):
        bad = Path(self.temp.name) / "bad.sqlite3"
        with closing(sqlite3.connect(bad)) as db:
            db.execute("CREATE TABLE unrelated(x INT)")
        with self.assertRaises(ValueError):
            verify_database(bad)


if __name__ == "__main__":
    unittest.main()
