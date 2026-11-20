# AI Automation Portfolio

**Python | Local automation | AI agent architecture | Quality gates | SQLite | HTTP/JSON**

A public, **synthetic-only** demonstration portfolio for technical interviews in AI automation, process improvement, and Python integration roles.

**Author and project owner:** [Kolfetgee](https://github.com/Kolfetgee)  
**Original private R&D themes:** AUTO-SCOUT, ORION, MAI  
**Public portfolio code:** newly written independent mini demos, not copies of private repositories.

> **Evidence boundary.** These examples are runnable educational demos with deterministic inputs. They are **not** commercial customer implementations, real LLMs, CRM integrations, production systems, deployed services, or evidence of measured ROI. Some original project engineering work was AI-assisted; the public examples were assembled with AI assistance and reviewed through local tests. See [provenance](docs/PROVENANCE_AND_SAFETY.md).

## Project map

| Demo | Business-process concept | Technologies and evidence | Open |
| --- | --- | --- | --- |
| **AUTO-SCOUT mini** | Manual opportunity intake, rules, decision trail, backup | Python standard library, SQLite, JSON, validation, test cases | [Source + runbook](demos/autoscout/README.md) |
| **ORION mini** | Maker / Checker / Owner workflow and explicit approval | Python state machine, event log, negative-case testing | [Source + runbook](demos/orion/README.md) |
| **MAI-inspired agent mock** | Stateful agent, bounded memory, human escalation, local JSON API | Python HTTP server, input validation, in-memory rules, test cases | [Source + runbook](demos/mai/README.md) |
| **FastAPI + PostgreSQL** | Web API and container-to-database communication | FastAPI, psycopg, PostgreSQL, Docker Compose | [Separate public teaching repo](https://github.com/Kolfetgee/compose-fastapi-postgre) |

## Quick start

**Requirements:** Python 3.11 or newer. No pip install, external accounts, real data, secrets, or cloud services needed for the three local demos.

From the repository root:

```bash
python -m unittest discover -s tests -v

# ORION: scripted example of a gated decision
python -m demos.orion.cli --scenario pass
python -m demos.orion.cli --scenario fail
python -m demos.orion.cli --scenario stop

# AUTO-SCOUT: synthetic local ledger
python -m demos.autoscout.cli --db sample.sqlite3 init
python -m demos.autoscout.cli --db sample.sqlite3 import --file demos/autoscout/leads.json
python -m demos.autoscout.cli --db sample.sqlite3 list
python -m demos.autoscout.cli --db sample.sqlite3 decide --id SYN-101 --state SHORTLIST --reason "Manual sample review complete" --confirm-owner
python -m demos.autoscout.cli --db sample.sqlite3 audit

# MAI-inspired: start an optional localhost-only JSON endpoint
python -m demos.mai.api --port 8788
```

In a second terminal, try the API:

```bash
curl http://127.0.0.1:8788/health
curl -X POST http://127.0.0.1:8788/turn -H "Content-Type: application/json" -d '{"message":"hello"}'
```

For Windows PowerShell use `py -3.13 -m ...` if available. The API listens on `127.0.0.1` only; stop it with `Ctrl+C`. The generated `sample.sqlite3` is ignored by Git. Do not enter personal, customer, pharmaceutical, or medical data into the demos.

## Architecture at a glance

```text
AUTOSCOUT                   ORION                       MAI MOCK

manual synthetic JSON       synthetic task              local HTTP/JSON
      |                          |                            |
validate / normalize      Maker candidate              validate input
      |                          |                            |
SQLite + audit           Checker verdict              bounded state/memory
      |                          |                            |
manual owner choice      Owner decision            reply / silence / escalate
      |                          |                            |
backup / verify         STOP / no execution          no model / no external API
```

## Test and implementation evidence

- **43 automated unit/integration checks** passed locally in a Linux container with **Python 3.13.5** on 2026-11-20; see [QA evidence](docs/QA_EVIDENCE.md).
- CI configuration is included for Python 3.11-3.13 on Linux and Windows; the **remote GitHub Actions run is not yet verified**.
- Negative tests cover invalid formats, state-transition violations, duplicate-ID conflicts, unauthorized transitions, JSON API error handling and backup overwrite attempts.
- Tests establish behavior of these mini demos only, **not independent acceptance or security approval** for private AUTO-SCOUT / ORION / MAI systems.

## How this maps to an AI automation role

See [skills-to-evidence matrix](docs/ROLE_ALIGNMENT.md). The demos help explain scoped workflow design, Python/JSON interfaces, local data handling, review gates, exception handling and technical documentation.

**Not demonstrated:** production integrations with corporate email/CRM, OAuth 2.0 authorization flows, paid RPA deployments, company onboarding/training, regulatory compliance, pharmaceutical data handling, business ROI measurement, production readiness or direct model inference inside these mini demos.

## Publication and privacy

All fixture content is invented. The repository does **not** include the history, databases, backups, secrets, documents, private prompts, personal correspondence or copyrighted game assets from the original projects. No automatic data collection, email dispatch, account access or agent execution is implemented.

Before uploading: read [publication checklist](docs/PUBLICATION_CHECKLIST.md) and [provenance/safety note](docs/PROVENANCE_AND_SAFETY.md).

**License status:** No open-source license selected. Do not assume the code grants third-party reuse rights. Select a license separately if desired.
