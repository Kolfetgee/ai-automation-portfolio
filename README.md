# Python Automation Portfolio

[![Python tests](https://github.com/Kolfetgee/ai-automation-portfolio/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Kolfetgee/ai-automation-portfolio/actions/workflows/tests.yml)

**Three small, runnable Python demos about reliable automation, stateful APIs, and human review.**

I use this portfolio to explore the parts of automation that matter beyond a happy-path script: validating input, keeping an audit trail, handling failures, and making important decisions explicit. The examples are intentionally small enough to run locally and read end to end.

**Stack:** Python 3.11+ · SQLite · standard-library HTTP/JSON · `unittest` · GitHub Actions

## Explore the projects

| Project | What it demonstrates | Start here |
| --- | --- | --- |
| **AUTO-SCOUT** | Import fictional opportunities into SQLite without silently overwriting conflicting records. Record manual decisions and create a checked backup. | [Code and walkthrough](demos/autoscout/README.md) |
| **ORION** | Model a task moving through Maker → Checker → Owner. Reject invalid transitions and stop on a failed review. | [Code and walkthrough](demos/orion/README.md) |
| **MAI-inspired agent** | Expose a tiny local JSON API with bounded in-memory notes, predictable responses, escalation, and a STOP state. | [Code and walkthrough](demos/mai/README.md) |

I also have a separate [FastAPI + PostgreSQL exercise](https://github.com/Kolfetgee/compose-fastapi-postgre) for working with a web API and a database in Docker.

## Run the demos

You only need **Python 3.11 or newer**. The three demos have **no third-party dependencies**, accounts, API keys, or external network calls.

Clone the repository and run all tests:

```bash
git clone https://github.com/Kolfetgee/ai-automation-portfolio.git
cd ai-automation-portfolio
python -m unittest discover -s tests -v
```

**AUTO-SCOUT — local SQLite ledger**

```bash
python -m demos.autoscout.cli --db sample.sqlite3 init
python -m demos.autoscout.cli --db sample.sqlite3 import --file demos/autoscout/leads.json
python -m demos.autoscout.cli --db sample.sqlite3 list
python -m demos.autoscout.cli --db sample.sqlite3 audit
```

**ORION — simulated approvals**

```bash
python -m demos.orion.cli --scenario pass
python -m demos.orion.cli --scenario fail
python -m demos.orion.cli --scenario stop
```

**MAI-inspired agent — local HTTP API**

```bash
python -m demos.mai.api --port 8788
```

Then, in a second terminal:

```bash
curl http://127.0.0.1:8788/health
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"hello"}'
```

The server listens on **127.0.0.1 only**. Stop it with `Ctrl+C`. See the project walkthroughs above for more commands and expected behavior. On Windows, use the Python launcher (`py -3.13 -m ...`) if needed; for POST examples, a shell with a real `curl` executable is easiest.

## Things worth looking at in the code

- **AUTO-SCOUT:** validation before writing, atomic SQLite imports, idempotent identical records, rejection of conflicts, and the SQLite backup API.
- **ORION:** state-transition guards, a separate owner decision after checker review, and explicit STOP behavior.
- **MAI-inspired mock:** JSON request validation, bounded `deque` memory, silence/escalation outcomes, and localhost-only HTTP handling.

The examples favor clarity over frameworks. Their limitations are deliberate and visible in the tests.

## Tests and what they prove

The repository contains **43 tests** across the three demos. The [GitHub Actions run on 20 November 2026](https://github.com/Kolfetgee/ai-automation-portfolio/actions/runs/44710353523) completed successfully in all **six** Python/OS jobs: Python 3.11, 3.12, and 3.13 on Linux and Windows.

Tests cover invalid input, duplicate IDs, transaction rollback, backup checks, state-transition errors, and malformed HTTP requests. See [QA evidence](docs/QA_EVIDENCE.md) for details.

## What this portfolio is — and isn't

These are **synthetic educational demos**, not production deployments or copies of my private projects. The Maker/Checker flow is simulated; the MAI-inspired agent uses deterministic rules, **not a real LLM**. The examples do not connect to a CRM, scrape opportunities, send messages, or authenticate users.

The code and documentation were developed with AI assistance; [the provenance notes](docs/PROVENANCE_AND_SAFETY.md) explain the boundaries. The source and tests are public so reviewers can inspect the actual behavior rather than take a feature claim on trust.

**License:** No open-source license has been selected yet.
