# Security Requirements

## Identity and session

- SR-01: The application must authenticate every non-public business action.
- SR-02: Standard and administrator roles must be enforced by the backend.
- SR-03: Session cookies must use HttpOnly and an appropriate SameSite policy.
- SR-04: Repeated authentication attempts must be rate limited.

## Authorisation

- SR-05: A standard user may access only tickets they own.
- SR-06: Administrator-only functions must reject standard users.
- SR-07: Authorisation failures must produce an audit event.

## Input and files

- SR-08: Server-side validation must reject malformed business input.
- SR-09: Uploads must enforce an allow-list, maximum size and safe generated name.
- SR-10: Application errors must not expose stack traces or database details.

## Audit and privacy

- SR-11: Authentication, authorisation denial, upload and administrator actions must be logged.
- SR-12: Audit records must contain timestamp, event, outcome, actor and correlation ID.
- SR-13: Passwords, session cookies, tokens and file contents must not be logged.

## Delivery and supply chain

- SR-14: Pull requests must pass build and automated tests.
- SR-15: Code, dependency, secret and container scanning must run in GitHub Actions.
- SR-16: The release image must be versioned and accompanied by an SBOM.
- SR-17: Workflow permissions must default to read-only unless a job requires more.

## Recovery

- SR-18: PostgreSQL data must be restorable into a clean container.
- SR-19: A prior application image must be available for rollback.
- SR-20: Recovery evidence must record actual results and limitations.

## Minimum Phase 2 acceptance tests

1. Alice cannot retrieve Bob's ticket.
2. A standard user cannot access an administrator endpoint.
3. An unauthenticated request is denied or redirected.
4. A disallowed file type is rejected.
5. An oversized upload is rejected.
