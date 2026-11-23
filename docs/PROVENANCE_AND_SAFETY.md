# Provenance, boundaries and responsible presentation

## What was built for this public portfolio

The `demos/` files are independent clean-room example implementations prepared specifically as synthetic technical demonstrations. They do not transfer source code, Git history, security findings, customer data, schemas, archived prompts or confidential material from any private project.

The code and documentation were created with AI assistance and iterated against local Python tests. These demos should not be portrayed as entirely human-written independent software, as paid consulting work or as production deployments.

## Relation to original research

- **AUTO-SCOUT:** privately developed personal lead-tracking utility; its primary development and review gates remain separate from this mini demo.
- **ORION:** private experimental project-control and AI orchestration work. The prototype has unresolved findings; this mini demo does not hide or fix those original findings.
- **MAI:** research involving long-lived agents, memory and behavior. This demo contains only a generic rules/state mock, **no licensed fictional characters or original game assets**.
- **FastAPI + PostgreSQL:** a separate already-public learning project, linked for straightforward source verification.

## Safety properties in these demos

- All fixtures use `SYN-*` identifiers and invented task titles.
- No real LLM is invoked. No API keys, OAuth tokens, CRM access or mail operations exist.
- No HTTP client fetches outside localhost are implemented in the demos.
- The optional mock agent API accepts bounded JSON payloads and binds to loopback.
- The AUTO-SCOUT mini imports only explicit local JSON, defaults to HOLD and needs explicit manual owner confirmation for decisions.
- The ORION mini never executes tasks or grants automatic authority based on a Maker claim.
- There is no external user authentication; these examples must not be exposed to untrusted networks.

## Important limitations

- Synthetic unit tests are not independent security audits.
- A hardcoded checker verdict in an example is **not** a real independent review.
- A CLI `--confirm-owner` flag demonstrates a workflow gate, not proof of identity.
- No continuous uptime, backup durability under power failure, security compliance, user training or business ROI is claimed.
- The code cannot be assumed safe for real personal, medical, pharmaceutical, corporate or financial data.

## Keeping the public repository separate

This portfolio was published as a new, synthetic-only repository on 20 November 2026. Keep future changes independent: do not mirror private repositories, copy their branches, import private ZIP archives, or migrate their Git histories here.
