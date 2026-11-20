# Architecture choices

## Why the demos have zero dependencies

The three new mini demos intentionally use Python standard-library modules only. That keeps review and execution cheap and allows the interviewer to inspect validation, persistence and HTTP behavior directly. It does not imply that standard-library-only is always suitable for production.

## AUTO-SCOUT

Boundary: **read local synthetic JSON -> validate -> SQLite -> append-only audit**. A user must supply `owner_confirmed=True` to change the status. IDs are stable. Conflicting duplicates are rejected; identical imports are idempotent. The backup uses the SQLite backup API and checks the copy before linking it into place without overwrite.

Production gaps: authentication, migrations/versioning, rate limits, real-source terms, encryption, secure backup storage, recovery drills and concurrent multi-user writes.

## ORION

Boundary: **task -> maker artifact -> checker verdict/evidence -> owner decision**. The protocol disallows out-of-order transitions and stops on a blocker. Events are in process memory only. It never sends tasks to an actual agent, so there are no hidden network or account side effects.

Production gaps: independently verified evidence, real identity and authorization, durable audit log, idempotent task processing, timeout management, trust separation and governance of tools.

## MAI-inspired mock

Boundary: **HTTP -> validated JSON -> local deterministic state machine -> JSON action**. Bounded local memory is lost on process exit. Unknown intents yield `escalate`; STOP yields `silence`. No model call occurs.

Production gaps: LLM adapter, prompt injection defenses, real authorization, secrets, retention policy, personal-data controls, evaluation set, per-session isolation, observability and deployment hardening.
