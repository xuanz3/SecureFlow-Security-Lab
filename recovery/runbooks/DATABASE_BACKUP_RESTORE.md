# PostgreSQL Backup and Clean Restore Runbook

## Scope

This runbook is for SecureFlow project-owned local Docker environments. It does
not operate on an existing development volume. Every exercise uses two unique
Docker Compose project names:

- source environment
- clean restore environment

The raw database archive remains in a temporary directory and is deleted at the
end. Only checksums, sizes, schema fingerprints, row counts and measured timing
are committed.

## Backup procedure

1. Build an immutable local known-good application image from the tested commit.
2. Start the isolated source database and application.
3. Wait for PostgreSQL and `/health/ready`.
4. Insert one deterministic recovery marker into `SecurityAuditEvents`.
5. Record the public-table set, row counts and schema fingerprint.
6. Run `pg_dump` in PostgreSQL custom format with `--no-owner --no-acl`.
7. Calculate SHA-256 and validate the archive with `pg_restore --list`.

## Clean restore procedure

1. Start a second Compose project with a new PostgreSQL volume.
2. Verify that the target database has zero public application tables.
3. Restore the custom-format archive using `pg_restore --exit-on-error`.
4. Start the known-good application image.
5. Wait for `/health/ready`.
6. Compare the restored table set, every table row count, schema fingerprint and
   recovery marker against the source summary.
7. Record restore duration and total measured recovery time.

## Failure handling

- If the archive cannot be listed, stop before attempting restore.
- If the target is not empty, destroy the exercise target and create a new one.
- If `pg_restore` returns non-zero, retain the temporary log for the current run,
  destroy the target volume and do not publish evidence.
- If any table count, schema fingerprint or marker differs, classify the restore
  as failed and do not merge the branch.
- If the restored application does not become ready, collect Compose logs, stop
  the exercise and do not claim successful recovery.
- A production process must add encrypted off-site storage, access control,
  retention, scheduled testing and organisation-approved RPO/RTO values.

## Evidence boundary

The measured time is valid only for this local exercise and dataset. It is not a
production recovery-time commitment.
