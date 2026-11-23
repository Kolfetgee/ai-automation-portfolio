# Maintaining the public portfolio

**Repository:** [Kolfetgee/ai-automation-portfolio](https://github.com/Kolfetgee/ai-automation-portfolio)  
**Status:** Published 20 November 2026. These notes are for future updates, not instructions for creating the repository.

## Before a public change

1. Check the changed files and Git history for secrets, personal data, customer information, local databases, private project material, and copyrighted assets.
2. Run `python -W error::ResourceWarning -m unittest discover -s tests -v` locally when code changes.
3. Verify that README claims match the current code, tests, and CI results. Do not imply a successful CI run before one is observed.
4. Keep synthetic fixtures and public demos separate from private AUTO-SCOUT, ORION, and MAI repositories.
5. Review the public diff before merging. Do not publish credentials, unreviewed archives, or private backup files.

## Evidence and licensing

The [QA record](QA_EVIDENCE.md) contains the observed test evidence; the [provenance note](PROVENANCE_AND_SAFETY.md) explains which examples are synthetic and AI-assisted.

No open-source license has been selected. Public visibility lets people inspect the code, but it does not automatically grant reuse rights. Choose and add a license only after a separate decision.
