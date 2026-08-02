# Phase 6 Backup, Restore and Rollback Exercise

## Result

**PASS** — a PostgreSQL custom-format backup was validated,
restored into a clean isolated database volume, served by the
known-good application image and retained through a controlled
candidate failure and image rollback.

## Scope

- Project-owned local Docker environments only
- Two unique Compose projects and independent database volumes
- Fictional seeded identities and one deterministic audit marker
- No existing development database or volume used as a target

## Measured results

- Backup archive size: **22833 bytes**
- Backup archive entries: **57**
- Backup duration: **0.213 seconds**
- Restore duration: **0.146 seconds**
- Measured local recovery time: **5.007 seconds**
- Rollback duration: **1.473 seconds**
- Restored application readiness: **HTTP 200**

## Integrity verification

- Public tables: **11**
- Source and restored table sets: **MATCH**
- Every public-table row count: **MATCH**
- Schema fingerprint: **MATCH**
- Recovery marker: **restored exactly once**
- Database after rollback: **UNCHANGED**

## Rollback verification

- Controlled candidate state: **exited**
- Controlled candidate exit code: **42**
- Candidate readiness status: **HTTP 0 / unavailable**
- Rollback readiness status: **HTTP 200**
- Running image identity equals recorded known-good image: **YES**

## Evidence handling

- Backup SHA-256: `5553252e13a9ac5c6c617a69083c708999935859a9d8baf6b72259cc4e47a7d5`
- Raw backup archive committed: **No**
- Temporary passwords and Compose project identifiers committed: **No**
- Evidence contains summaries, timing and immutable image identities only.

## Failure handling

The committed runbooks require the exercise to stop without merge when
archive validation, clean-target checks, restore, integrity comparison,
application readiness or exact-image rollback verification fails.

## Limitations

The observed zero-second fixture RPO and measured recovery time apply
only to this local exercise. They are not production commitments.
Production use requires encrypted off-site backups, retention policy,
scheduled restore tests, monitored rollback and approved RPO/RTO.
