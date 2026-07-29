# Day 2 Validation Evidence

- Validation date: 2026-07-29T12:17:22Z
- .NET SDK: 10.0.302
- Docker: Docker version 28.4.0, build d8eb465
- Release build: PASS
- Tests: Passed!  - Failed:     0, Passed:    12, Skipped:     0, Total:    12, Duration: 25 ms - SecureFlow.Tests.dll (net10.0)
- Docker image build after remediation: PASS
- Liveness endpoint: HTTP 200
- PostgreSQL readiness endpoint: HTTP 200
- Unauthenticated `/Tickets` response: HTTP 302
- Unauthenticated `/Admin` response: HTTP 302

## Commands executed

```bash
dotnet restore SecureFlow.sln
dotnet build SecureFlow.sln --configuration Release --no-restore
dotnet test SecureFlow.sln --configuration Release --no-build
docker compose --env-file .env -f infrastructure/docker/compose.yml build --no-cache app
docker compose --env-file .env -f infrastructure/docker/compose.yml up -d
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready
```

## Resolved build incident

The original container build failed because host-generated `obj/` files overwrote
the dependency graph created by the Linux container restore. The committed
`.dockerignore` prevents this cross-environment contamination.

All identities and records are fictional. Local passwords remain outside Git.
