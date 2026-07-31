# Deliberately Insecure Terraform Fixture

This directory is never deployed. It exists only to prove that Checkov detects
controlled Azure Terraform misconfigurations.

The fixture intentionally includes:

- TLS 1.0
- public network access
- public nested storage items
- shared access keys
- cross-tenant replication
- Key Vault without RBAC or purge protection
- allow-by-default network ACLs

Do not apply this configuration.
