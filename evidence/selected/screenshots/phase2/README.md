# Phase 2 Screenshot Evidence Index

These screenshots record the verified Phase 2 secure application foundation. All
data is fictional and the environment is restricted to project-owned local
containers.

| ID | Evidence | Demonstrated capability |
|---|---|---|
| P2-01 | `P2-01_automated-tests-pass.png` | Release test execution with 12 passing tests and no failures |
| P2-02 | `P2-02_docker-health-validation.png` | Running application and PostgreSQL containers, HTTP 200 liveness/readiness, and security response headers |
| P2-03 | `P2-03_user-owned-ticket.png` | Authenticated normal user creating and viewing an owned ticket |
| P2-04 | `P2-04_cross-user-access-denied.png` | Server-side object-level authorisation blocking cross-user direct URL access |
| P2-05 | `P2-05_admin-rbac-view.png` | Administrator role viewing tickets owned by multiple fictional users |

## Auxiliary evidence

`../../archive/screenshots/phase2/P2-A01_pr38_build-remediation.png` records merged
PR #38, including the Docker build incident, remediation, validation results and
linked closed Issues.

## Privacy and safety review

- No passwords or `.env` values are visible.
- No real customer or employee information is present.
- User and ticket identifiers are generated fictional values.
- All URLs refer to `localhost` or the public project repository.
