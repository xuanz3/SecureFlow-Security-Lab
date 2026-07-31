# Phase 4 IaC and Network Scope

## Azure Terraform

The Terraform configuration is reference-only and is not deployed. It provides:

- a hardened Azure Storage Account reference
- a hardened Azure Key Vault reference
- a deliberately insecure fixture for Checkov validation

Checkov results are retained in JSON and Markdown. Expected fixture failures are
kept separate from application vulnerability findings.

## Network exposure

The network assessment checks only:

- `127.0.0.1`
- the Mac's active LAN IPv4 address, when available
- TCP ports 5432 and 8080
- Docker runtime metadata that excludes environment values

No network range or third-party host is scanned.

## Packet capture

The packet capture records only unauthenticated `/health/live` traffic in the
application container's network namespace. It does not capture login, ticket,
attachment or credential traffic.

## Deliberate-fixture scanner isolation

`infrastructure/terraform/azure/insecure-fixture/` intentionally contains
misconfigurations for controlled scanner validation. It is excluded only from
the general Trivy repository SARIF baseline so those known training findings do
not appear as newly introduced production-code alerts.

The fixture remains covered by the dedicated Checkov workflow and its original
JSON evidence. The Azure reference configuration, Docker configuration and all
other repository configuration remain inside the general Trivy scan boundary.
