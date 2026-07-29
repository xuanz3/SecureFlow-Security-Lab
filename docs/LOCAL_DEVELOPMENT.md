# Local Development

## Prerequisites

- .NET 10 SDK
- Docker Desktop
- Git

## Start the environment

```bash
./scripts/generate-local-secrets.sh
docker compose --env-file .env -f infrastructure/docker/compose.yml up --build
```

Open `http://localhost:8080`.

The generated identities and passwords are fictional, local-only values. `.env` and
.NET user-secrets are excluded from Git. PostgreSQL is bound only to `127.0.0.1`.

## Stop the environment

```bash
docker compose --env-file .env -f infrastructure/docker/compose.yml down
```

Add `--volumes` only when the test database and upload volume should be deleted.
