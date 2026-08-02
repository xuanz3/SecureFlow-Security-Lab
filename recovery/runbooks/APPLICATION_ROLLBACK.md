# Application Image Rollback Runbook

## Scope

The exercise tests the operational rollback path without introducing a defect
into the repository. It builds:

- a known-good image from the tested SecureFlow commit
- a controlled candidate image derived from it with a forced startup failure

The candidate is an exercise fixture, not a historical production release.

## Rollback procedure

1. Record the known-good image ID and source commit.
2. Deploy the controlled candidate image to the restored environment.
3. Confirm that the candidate exits with the expected controlled failure code
   and that the readiness endpoint is unavailable.
4. Start the rollback timer.
5. Recreate the application service using the known-good image tag.
6. Wait for `/health/ready` to return HTTP 200.
7. Verify that the running container image ID exactly equals the recorded
   known-good image ID.
8. Record elapsed rollback time and final database integrity.

## Failure handling

- If the candidate unexpectedly becomes healthy, stop; the failure fixture did
  not work and rollback evidence is invalid.
- If the known-good image ID is unavailable, stop rather than using `latest`.
- If the known-good container does not return HTTP 200, collect logs and retain
  the restored database for investigation during the current temporary run.
- If the running image ID differs from the recorded image ID, classify the
  rollback as failed.
- Production rollback should use approved immutable registry digests, change
  control, traffic management, monitoring and stakeholder communication.

## Success condition

Rollback succeeds only when the candidate fails as designed, the known-good
image is restored by exact image identity, the application becomes ready and
the restored database remains intact.
