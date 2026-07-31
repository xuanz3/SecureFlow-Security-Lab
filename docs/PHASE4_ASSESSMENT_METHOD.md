# Phase 4 Assessment Method

## Objective

Execute the authorised SecureFlow application-security test matrix against the
project-owned local Docker environment, triage validated findings and retain
repeatable evidence.

## Scope

Permitted targets:

- `http://localhost:8080`
- SecureFlow Docker Compose services
- Fictional Admin, Alice and Bob accounts
- Generated fictional tickets and attachments
- Source code, Docker configuration and Terraform fixtures in this repository

Prohibited targets and activities remain defined by
`security-assessment/RULES_OF_ENGAGEMENT.md`.

## Assessment layers

1. **Dynamic application tests**
   - authentication rate limiting
   - object-level authorisation
   - administrator role authorisation
   - anti-forgery enforcement
   - error handling
   - upload extension, MIME, size and filename controls
   - response security headers

2. **Targeted source/configuration review**
   - upload content validation and quarantine
   - rate-limiter partitioning
   - CSP policy strength
   - container runtime posture
   - base-image immutability
   - early request-size enforcement

3. **Infrastructure and network review**
   - Checkov against secure and deliberately insecure Azure Terraform examples
   - Nmap against loopback and the Mac LAN address
   - Docker runtime inspection without exporting environment secrets
   - packet capture of an unauthenticated health request only

## Finding acceptance standard

Every accepted finding includes:

- affected asset
- evidence and safe reproduction
- technical cause
- impact
- CWE and OWASP mapping
- severity rationale
- recommendation
- GitHub finding Issue
- remediation and retest status for Phase 5

## Evidence handling

- Passwords, cookies and `.env` values are never written to committed evidence.
- Packet capture is restricted to unauthenticated `/health/live` requests.
- Raw scanner results remain in `evidence/archive/artifacts/phase4/`.
- Selected screenshots are added only after final review.
