# Project Status

## Current phase

**Phase 1 — Secure application foundation complete**

## Completed

- Phase 0 repository governance, architecture, threat model and security requirements
- ASP.NET Core 10 application and PostgreSQL persistence
- Fictional development identities, authentication and role model
- Ticket ownership and administrator authorisation
- Protected file uploads and downloads
- Structured audit events, rate limiting, security headers and health checks
- Negative unit tests for authorisation and upload controls
- Local Docker Compose environment and development documentation

## Next phase

Phase 2 adds GitHub Actions build/test gates, CodeQL, Gitleaks, dependency checks,
Trivy, SBOM generation, OWASP ZAP and GHCR publishing.

## Limitations

- Local ASP.NET Core Identity is used instead of a production identity provider.
- MFA and federated SSO are not implemented in the six-day compressed scope.
- Security testing remains restricted to project-owned local containers.
- Phase 1 validation evidence must reflect actual local results, not assumed outcomes.
