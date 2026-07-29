# Phase 1 Validation

## Implemented

- ASP.NET Core 10 MVC application
- PostgreSQL 17 with EF Core migrations
- ASP.NET Core Identity with fictional local accounts
- `Admin` and `User` roles
- Login lockout, rate limiting and secure cookie settings
- Ticket creation and server-side ownership checks
- Administrator-only ticket view
- Protected upload storage outside the web root
- Extension, content-type and size validation
- Structured security-relevant logging
- PostgreSQL readiness health check
- Browser security headers
- Automated negative authorisation and upload tests
- Docker Compose local environment

## Verification commands

```bash
dotnet restore
dotnet build --configuration Release
dotnet test --configuration Release
docker compose --env-file .env -f infrastructure/docker/compose.yml config
docker compose --env-file .env -f infrastructure/docker/compose.yml up --build
```

## Expected manual checks

1. Alice can create and read her own ticket.
2. Alice receives a forbidden response for Bob's ticket URL.
3. A normal user cannot access `/Admin`.
4. An `.exe`, mismatched MIME type and file over 2 MB are rejected.
5. An allowed attachment is stored outside `wwwroot` and is retrievable only through an authorised action.
6. `/health/live` returns success.
7. `/health/ready` returns success when PostgreSQL is reachable.
8. Login attempts are rate-limited and repeated failures can lock the account.

## Evidence boundary

This document records implementation targets and repeatable checks. Screenshots and
measured results are added only after the commands have run on the local Mac
environment. No production deployment, external identity provider or MFA is claimed.
