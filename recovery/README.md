# SecureFlow Recovery Evidence

Phase 6 recovery demonstrates database backup, clean restore and application
image rollback inside isolated project-owned Docker environments.

- [Database backup and restore runbook](runbooks/DATABASE_BACKUP_RESTORE.md)
- [Application rollback runbook](runbooks/APPLICATION_ROLLBACK.md)
- [Measured recovery exercise report](PHASE6_RECOVERY_EXERCISE_REPORT.md)
- [Recovery validation](../docs/PHASE6_RECOVERY_VALIDATION.md)

## Evidence retained

The repository retains sanitised JSON summaries, SHA-256 checksums, database
schema and row-count comparisons, application health results and elapsed times.

The raw PostgreSQL archive, temporary credentials, Docker project names and
temporary environment files are not committed.

## Claim boundary

The exercise proves that the documented local recovery path worked for the
controlled dataset. It does not establish a production backup schedule,
off-site retention, disaster-recovery SLA or organisation-approved RPO/RTO.
