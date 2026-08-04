# ADR-001: Use a Local-First Architecture

- **Status:** Accepted
- **Date:** 2026-07-29

## Context

The existing Enterprise SOC Lab already uses three Azure virtual machines. Additional Azure compute would increase cost, quota pressure and implementation risk. SecureFlow needs to expand project coverage into AppSec, DevSecOps, vulnerability management, governance and recovery without duplicating the SOC lab.

## Decision

Use Docker Compose on the developer workstation as the primary runtime. Use GitHub-hosted workflows for heavier scanning and release evidence. Terraform will be reviewed statically and will not be applied to Azure during the core project.

## Consequences

### Positive

- No additional VM cost or quota requirement
- Fast reset of application, database and assessment data
- Reproducible local security testing
- Clear separation from the Azure SOC project
- GitHub Actions becomes visible release evidence

### Negative

- No claim of production cloud operation
- KQL and Azure IaC evidence is partly portable/static
- Local resource limits require services to run only when needed

## Safeguards

- Bind only required ports.
- Keep PostgreSQL internal to the Compose network.
- Separate insecure fixtures from the secure reference configuration.
- Document which evidence was executed and which is reference-only.
