# Phase 4 Checkov Assessment

- Checkov image: `bridgecrew/checkov@sha256:c64ffb6d6fc8087c896341a2c697770a04a1cf558db04fa7b8129d8ca6bce336`
- Azure reference: 17 passed, 4 failed, 0 skipped
- Deliberately insecure fixture: 5 passed, 16 failed, 0 skipped

## Secure-reference triage

The reference is non-deployed example code. Any remaining Checkov results are
retained for manual triage rather than silently suppressed.

| Check | Resource |
|---|---|
| CKV_AZURE_33 — Ensure Storage logging is enabled for Queue service for read, write and delete requests | `azurerm_storage_account.evidence` |
| CKV2_AZURE_33 — Ensure storage account is configured with private endpoint | `azurerm_storage_account.evidence` |
| CKV2_AZURE_32 — Ensure private endpoint is configured to key vault | `azurerm_key_vault.reference` |
| CKV2_AZURE_1 — Ensure storage for critical data are encrypted with Customer Managed Key | `azurerm_storage_account.evidence` |

## Insecure-fixture detection

| Check | Resource |
|---|---|
| CKV_AZURE_206 — Ensure that Storage Accounts use replication | `azurerm_storage_account.fixture` |
| CKV_AZURE_190 — Ensure that Storage blobs restrict public access | `azurerm_storage_account.fixture` |
| CKV_AZURE_59 — Ensure that Storage accounts disallow public access | `azurerm_storage_account.fixture` |
| CKV_AZURE_44 — Ensure Storage Account is using the latest version of TLS encryption | `azurerm_storage_account.fixture` |
| CKV_AZURE_33 — Ensure Storage logging is enabled for Queue service for read, write and delete requests | `azurerm_storage_account.fixture` |
| CKV_AZURE_109 — Ensure that key vault allows firewall rules settings | `azurerm_key_vault.fixture` |
| CKV_AZURE_42 — Ensure the key vault is recoverable | `azurerm_key_vault.fixture` |
| CKV_AZURE_110 — Ensure that key vault enables purge protection | `azurerm_key_vault.fixture` |
| CKV_AZURE_189 — Ensure that Azure Key Vault disables public network access | `azurerm_key_vault.fixture` |
| CKV2_AZURE_33 — Ensure storage account is configured with private endpoint | `azurerm_storage_account.fixture` |
| CKV2_AZURE_47 — Ensure storage account is configured without blob anonymous access | `azurerm_storage_account.fixture` |
| CKV2_AZURE_41 — Ensure storage account is configured with SAS expiration policy | `azurerm_storage_account.fixture` |
| CKV2_AZURE_32 — Ensure private endpoint is configured to key vault | `azurerm_key_vault.fixture` |
| CKV2_AZURE_40 — Ensure storage account is not configured with Shared Key authorization | `azurerm_storage_account.fixture` |
| CKV2_AZURE_38 — Ensure soft-delete is enabled on Azure storage account | `azurerm_storage_account.fixture` |
| CKV2_AZURE_1 — Ensure storage for critical data are encrypted with Customer Managed Key | `azurerm_storage_account.fixture` |

## Interpretation

- Fixture failures are expected evidence, not unresolved application findings.
- No Azure resources were created.
- The reference and fixture remain inside the repository for repeatable review.
