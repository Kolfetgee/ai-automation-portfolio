"""Render a simulated workflow without calling AI models or external services."""
import argparse
import json
from .workflow import Workflow


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic offline Maker/Checker/Owner demo")
    parser.add_argument("--scenario", choices=["pass", "fail", "stop"], default="pass")
    args = parser.parse_args(argv)
    workflow = Workflow("SYN-ORION-001", "Normalize a fictional internal document title")
    workflow.submit_maker({
        "summary": "A proposed synthetic normalizer, without any data access",
        "test_claims": ["synthetic example executed by maker"],
    })
    if args.scenario == "stop":
        workflow.stop("Owner requested immediate halt")
    elif args.scenario == "fail":
        workflow.review_checker("NEEDS_FIXES", "Independent example check found missing edge cases")
    else:
        workflow.review_checker("PASS", "Synthetic checker example: input and output schema are valid")
        workflow.owner_decide(True, "Separate human approval for demo only")
    print(json.dumps(workflow.snapshot(), ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
