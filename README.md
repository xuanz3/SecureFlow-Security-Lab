# SecureFlow Security Lab

A local-first enterprise security engineering and assurance portfolio project covering secure application development, DevSecOps, application security testing, vulnerability management, detection engineering, governance and recovery.

**Project status:** Phase 0 — Security design and repository foundation.

## Intended workflow

**Design → Build → Test → Assess → Remediate → Detect → Assure → Recover**

## Planned capabilities

- ASP.NET Core application with PostgreSQL
- Authentication, role-based access control and object-level authorisation
- Secure file upload and structured audit logging
- GitHub Actions security gates
- SAST, SCA, secret, container, IaC and DAST scanning
- Authorised Web/API security assessment
- Vulnerability register, remediation PRs and retesting
- Sigma and Microsoft Sentinel KQL examples
- NIST CSF 2.0 and Essential Eight gap assessment
- Backup, restore and application rollback exercises

## Repository map

- `docs/` — scope, architecture, threat model and decisions
- `src/` — application source code, added in Phase 1
- `tests/` — automated security and application tests
- `security-assessment/` — scope, rules of engagement, findings and retests
- `detections/` — Sigma and KQL detection content
- `infrastructure/` — Docker and Terraform reference material
- `governance/` — risk and control-assurance artefacts
- `recovery/` — backup, restore and rollback evidence
- `evidence/` — selected portfolio evidence

## Safety boundary

All testing is restricted to project-owned local containers and deliberately created test fixtures. No public or third-party systems are in scope.

## Author

Xuanze Chen
