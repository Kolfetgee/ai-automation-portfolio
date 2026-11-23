# Test evidence

## Verified baseline — 20 November 2026

**Local:** CPython 3.13.5 in a Linux container; `python -W error::ResourceWarning -m unittest discover -s tests -q` — **43 passed**.

**GitHub Actions:** [run #44710353523](https://github.com/Kolfetgee/ai-automation-portfolio/actions/runs/44710353523) for commit `d595f452d0880fe382ebd636042054c868477983` — **6/6 jobs passed**, covering:

| Operating system | Python versions |
| --- | --- |
| Ubuntu | 3.11, 3.12, 3.13 |
| Windows | 3.11, 3.12, 3.13 |

This is the verified baseline for the initial published code, not a claim about any later change or an independent security audit.

## What is tested

- **AUTO-SCOUT (15):** database setup, atomic import, duplicate/conflict handling, validation, manual decisions, audit events, integrity checks, and backup safety.
- **ORION (14):** valid and invalid Maker/Checker/Owner transitions, failed reviews, event history, and STOP.
- **MAI mock (14):** memory limits, response modes, STOP/resume, HTTP routes, JSON validation, and oversized requests.

During initial assembly, the empty `remember:` case was fixed to reject invalid notes, and SQLite connections were explicitly closed to avoid resource warnings.

## Outside this evidence

The tests do **not** establish real LLM behavior, independent Maker/Checker identity, authentication, production deployment, high-concurrency safety, privacy compliance, real CRM integration, or business ROI. They cover only the synthetic implementations in this repository.

When code changes, use the new commit's tests and GitHub Actions run as the new evidence; do not assume this historical run covers it.
