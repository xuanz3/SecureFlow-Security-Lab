# SecureFlow Security Lab

A local-first enterprise security engineering and assurance portfolio project covering secure application development, DevSecOps, application security testing, vulnerability management, detection engineering, governance and recovery.

**Project status:** Phase 1 — Secure application foundation completed.

## Intended workflow

**Design → Build → Test → Assess → Remediate → Detect → Assure → Recover**

## Implemented in Phase 1

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
