# Delivery Phase Numbering

SecureFlow uses phase-based delivery terminology. Calendar days are not used as
project stages because implementation and validation may span different dates.

| Phase | Scope |
|---|---|
| Phase 1 | Security design, architecture, threat model and repository governance |
| Phase 2 | ASP.NET Core application, PostgreSQL, identity, RBAC, tickets, uploads and audit events |
| Phase 3 | CI, dependency governance, CodeQL, Gitleaks, Trivy, SBOM, ZAP and GHCR |
| Phase 4 | Authorised application-security assessment, vulnerability register, IaC and network review |
| Phase 5 | Vulnerability remediation, retesting, detection engineering and incident analysis |
| Phase 6 | Risk assurance, control mapping, backup/restore exercises and final reporting |

Future work continues with Phase 7, Phase 8 and subsequent sequential numbers.

## Naming rules

- Use `Phase N` in prose and titles.
- Use `phase-N` in branch names and labels.
- Use `phaseN` for evidence directories.
- Use `PN-XX` for screenshot evidence identifiers.
- Use only sequential phase labels for delivery stages.
