# ORION mini demo

A pure-Python, deterministic state machine showing **Maker -> Checker -> Owner** gates. It does **not** run AI models, authenticate actors, perform real independent review, or execute approved tasks. The Maker/Checker verdicts in the CLI are hardcoded synthetic examples.

```bash
python -m demos.orion.cli --scenario pass
python -m demos.orion.cli --scenario fail
python -m demos.orion.cli --scenario stop
```

The `PASS` scenario still requires explicit separate `owner_decide(True, ...)` before the state becomes `APPROVED`. A failed review cannot be bypassed. `STOP` disallows further transitions. An append-only event list records decisions. The code intentionally excludes deployments, network access, secret handling, and agent orchestration credentials.

This clean-room demonstration illustrates workflow logic from project-management research; it is **not** the private ORION codebase, and it is not production-ready.
