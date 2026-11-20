"""Local, offline, synthetic-only AUTO-SCOUT demonstration."""
import argparse
import json
from .core import decide, import_records, initialize, load_json, make_backup, read_audit, read_leads, verify_database


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="AUTO-SCOUT: local synthetic opportunity ledger")
    parser.add_argument("--db", required=True, help="path to SQLite database")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    intake = commands.add_parser("import")
    intake.add_argument("--file", required=True)
    commands.add_parser("list")
    commands.add_parser("audit")
    commands.add_parser("verify")
    decision = commands.add_parser("decide")
    decision.add_argument("--id", required=True)
    decision.add_argument("--state", choices=["HOLD", "SHORTLIST", "SKIP"], required=True)
    decision.add_argument("--reason", required=True)
    decision.add_argument("--confirm-owner", action="store_true")
    backup = commands.add_parser("backup")
    backup.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            initialize(args.db)
            result = {"initialized": args.db}
        elif args.command == "import":
            created, skipped = import_records(args.db, load_json(args.file))
            result = {"created": created, "identical_duplicates": skipped}
        elif args.command == "list":
            result = {"leads": read_leads(args.db)}
        elif args.command == "audit":
            result = {"events": read_audit(args.db)}
        elif args.command == "decide":
            decide(args.db, args.id, args.state, args.reason, owner_confirmed=args.confirm_owner)
            result = {"changed": args.id, "state": args.state}
        elif args.command == "backup":
            make_backup(args.db, args.out)
            result = {"backup_created": args.out}
        else:
            verify_database(args.db)
            result = {"database_valid": True}
        print(json.dumps(result, ensure_ascii=True, indent=2))
        return 0
    except (ValueError, PermissionError, OSError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
