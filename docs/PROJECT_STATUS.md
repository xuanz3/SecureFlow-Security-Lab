# Project Status

## Current phase

**Phase 4 — Authorised security assessment complete**

## Completed

- Phase 1 repository governance, architecture, threat model and security requirements
- ASP.NET Core 10 application and PostgreSQL persistence
- Fictional development identities, authentication and role model
- Ticket ownership and administrator authorisation
- Protected file uploads and downloads
- Structured audit events, rate limiting, security headers and health checks
- Negative unit tests for authorisation and upload controls
- Local Docker Compose environment and development documentation

## Phase 3 controls

- Locked NuGet restore and automated Release build/test
- Dependency review and Dependabot
- CodeQL security-extended C# analysis
- Full-history Gitleaks scanning
- Trivy container and configuration analysis
- CycloneDX SBOM generation
- Isolated OWASP ZAP baseline DAST
- Versioned GHCR publication with provenance

## Next phase

Phase 5 remediates selected findings, adds regression tests and detection
content, and records formal retest results.

## Phase 4 assessment outputs

- authorised application/API test matrix
- eight validated and Issue-linked findings
- vulnerability register
- Checkov Azure Terraform reference and insecure fixture
- Nmap loopback/LAN exposure evidence
- controlled unauthenticated packet capture
- final assessment report

## Limitations

- Local ASP.NET Core Identity is used instead of a production identity provider.
- MFA and federated SSO are not implemented in the six-phase compressed scope.
- Security testing remains restricted to project-owned local containers.
- Phase 2 validation evidence must reflect actual local results, not assumed outcomes.
