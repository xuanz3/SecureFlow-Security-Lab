# Project Status

## Current phase

**Phase 2 — DevSecOps security gates complete**

## Completed

- Phase 0 repository governance, architecture, threat model and security requirements
- ASP.NET Core 10 application and PostgreSQL persistence
- Fictional development identities, authentication and role model
- Ticket ownership and administrator authorisation
- Protected file uploads and downloads
- Structured audit events, rate limiting, security headers and health checks
- Negative unit tests for authorisation and upload controls
- Local Docker Compose environment and development documentation

## Phase 2 controls

- Locked NuGet restore and automated Release build/test
- Dependency review and Dependabot
- CodeQL security-extended C# analysis
- Full-history Gitleaks scanning
- Trivy container and configuration analysis
- CycloneDX SBOM generation
- Isolated OWASP ZAP baseline DAST
- Versioned GHCR publication with provenance

## Next phase

Phase 3 executes the authorised application-security assessment, vulnerability
register, manual authorisation tests, IaC review and network exposure analysis.

## Limitations

- Local ASP.NET Core Identity is used instead of a production identity provider.
- MFA and federated SSO are not implemented in the six-day compressed scope.
- Security testing remains restricted to project-owned local containers.
- Phase 1 validation evidence must reflect actual local results, not assumed outcomes.
