output "storage_account_id" {
  description = "Reference storage account resource identifier."
  value       = azurerm_storage_account.evidence.id
}

output "key_vault_id" {
  description = "Reference Key Vault resource identifier."
  value       = azurerm_key_vault.reference.id
}
