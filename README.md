# SecureFlow Security Lab

A local-first enterprise security engineering and assurance portfolio project covering secure application development, DevSecOps, application security testing, vulnerability management, detection engineering, governance and recovery.

**Project status:** Phase 3 — DevSecOps security gates implemented.

## Intended workflow

**Design → Build → Test → Assess → Remediate → Detect → Assure → Recover**

## Implemented in Phase 2

- ASP.NET Core 10 MVC application
- PostgreSQL 17 and EF Core migrations
- ASP.NET Core Identity with fictional local accounts
- `Admin` and `User` role boundaries
- Server-side ticket ownership authorisation
- Protected file storage outside the web root
- File extension, MIME and size validation
- Structured security audit events and correlation identifiers
- Login lockout, rate limiting and secure cookie configuration
- Security response headers
- Liveness and PostgreSQL readiness health checks
- Automated negative authorisation and upload tests
- Reproducible Docker Compose environment

## DevSecOps automation

Pull requests run locked dependency restore, Release build and tests, Docker build,
dependency review, CodeQL, Gitleaks, Trivy container/configuration scanning and an
isolated OWASP ZAP baseline scan. Published releases produce versioned GHCR images,
CycloneDX SBOM evidence and provenance attestations.

## Delivery phases

| Phase | Focus |
|---|---|
| Phase 1 | Security design and repository governance |
| Phase 2 | Secure application foundation |
| Phase 3 | DevSecOps automation and supply-chain assurance |
| Phase 4 | Authorised security assessment |
| Phase 5 | Remediation and detection engineering |
| Phase 6 | Governance, recovery and final reporting |

Detailed naming rules are recorded in `docs/PHASE_NUMBERING.md`.

## Local start

```bash
./scripts/generate-local-secrets.sh
docker compose --env-file .env -f infrastructure/docker/compose.yml up --build
```

Open `http://localhost:8080`.

The setup generates local-only credentials for:

- `admin@example.test`
- `alice@example.test`
- `bob@example.test`

No passwords are committed.

## Repository map

- `src/` — ASP.NET Core application
- `tests/` — automated security and application tests
- `docs/` — scope, architecture, threat model, decisions and validation
- `security-assessment/` — authorised test rules, findings and retests
- `detections/` — Sigma and KQL detection content
- `infrastructure/` — Docker and Terraform reference material
- `governance/` — risk and control-assurance artefacts
- `recovery/` — backup, restore and rollback evidence
- `evidence/` — selected portfolio evidence

## Safety boundary

All testing is restricted to project-owned local containers and deliberately created fictional data. No public or third-party systems are in scope.

## Known limitations

The compressed implementation uses local ASP.NET Core Identity. MFA, federation,
automated access reviews and production cloud deployment are not claimed.

## Author

Xuanze Chen
