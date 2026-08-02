# Phase 6 Governance Action Plan

| Priority | Action | Risk / framework driver | Owner | Target | Evidence of completion |
|---:|---|---|---|---|---|
| 1 | Execute PostgreSQL backup and clean restore with integrity checks and measured recovery time. | R-08; NIST Recover; Essential Eight regular backups | Project owner | Completed in Issue #32 | `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`; `docs/PHASE6_RECOVERY_VALIDATION.md` |
| 1 | Execute rollback from a deliberately changed application image to a known-good version. | R-09; NIST Recover | Project owner | Completed in Issue #32 | `recovery/PHASE6_RECOVERY_EXERCISE_REPORT.md`; `recovery/runbooks/APPLICATION_ROLLBACK.md` |
| 1 | Publish final management and technical reports with finding-to-remediation traceability. | R-10; NIST Govern | Project owner | Issue #33 | Final reports and v1.0 release |
| 2 | Add MFA or federated identity before any production deployment. | R-01; NIST Protect; Essential Eight MFA | Future deployment owner | Post-v1.0 | Authentication design and negative tests |
| 2 | Replace deterministic local upload scanning with managed antivirus or sandbox analysis. | R-03; NIST Protect/Detect | Future deployment owner | Post-v1.0 | Provider integration tests and quarantine telemetry |
| 2 | Forward audit events to a SIEM and assign alert ownership and escalation paths. | R-07; NIST Detect/Respond | Future operations owner | Post-v1.0 | Ingestion evidence, alert rules and response SLA |
| 2 | Use a managed secret store and production key-rotation process. | R-06; NIST Protect/Govern | Future deployment owner | Post-v1.0 | Secret-store integration and rotation evidence |
| 3 | Add privileged access review, JIT/PAM controls and enterprise endpoint baselines where applicable. | Essential Eight gaps | Future organisation | Outside lab | Organisation-specific assessment evidence |

## Decision rule

No action is marked complete from documentation alone. Closure requires
technical or operational evidence that is linked from the relevant Issue and
reviewed through a pull request.
