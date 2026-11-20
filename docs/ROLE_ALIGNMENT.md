# Skills-to-evidence matrix for an AI automation role

This is an interview map, not a claim of commercial implementation.

| Requirement | Demonstration | Current limit |
| --- | --- | --- |
| Define agent roles, inputs, outputs and exception rules | ORION gated workflow, MAI mock agent | Purely deterministic / synthetic |
| Python automation and data processing | AUTO-SCOUT SQLite import, validation, audit | No customer data or scheduled tasks |
| REST-like JSON interfaces | MAI mock localhost JSON API; separate FastAPI example | No external integration or OAuth |
| Auditability and quality control | Import history, checker gate, owner approval | CLI confirmation is not identity authentication |
| Reliability and backup | SQLite API backup and verification | Not a disaster-recovery-certified solution |
| Technical documentation and training | README/runbook, tests, negative examples | No validated company-wide employee training |
| ROI and rollout planning | Can explain how to define metrics and pilot criteria | **No measured ROI or business outcomes** |
| Pharma-specific data protection | Demonstrates data minimization by using synthetic fixtures | No validated regulatory control framework |

## Suggested interview narrative

1. **Identify** a narrow repetitive process and current manual error sources.
2. **Specify** inputs/outputs, exception paths, sensitive data boundaries and manual approvals.
3. **Prototype** an offline bounded integration with deterministic fixtures.
4. **Test** negative cases and separately review the output rather than trusting a model claim.
5. **Pilot** only after production security, ownership, audit and rollback gates.
6. **Measure** baseline time, exception rate, intervention rate and total cost before making ROI claims.

## Example ROI formula (framework, not actual result)

For a validated pilot: `monthly net benefit = time_saved_hours * labor_cost_per_hour - monthly_running_cost - monthly_support_cost`; compare against upfront implementation and training costs. Explicitly include evaluation, maintenance, compliance review and human-in-the-loop costs. This portfolio contains **no real company values** for that calculation.
