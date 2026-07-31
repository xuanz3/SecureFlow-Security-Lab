resource "azurerm_resource_group" "reference" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    project     = "secureflow"
    environment = "reference-only"
    managed_by  = "terraform"
  }
}

resource "azurerm_storage_account" "evidence" {
  name                            = var.storage_account_name
  resource_group_name             = azurerm_resource_group.reference.name
  location                        = azurerm_resource_group.reference.location
  account_tier                    = "Standard"
  account_replication_type        = "GRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  public_network_access_enabled   = false
  shared_access_key_enabled       = false
  infrastructure_encryption_enabled = true
  cross_tenant_replication_enabled  = false
  local_user_enabled                = false

  blob_properties {
    versioning_enabled = true

    delete_retention_policy {
      days = 30
    }

    container_delete_retention_policy {
      days = 30
    }
  }

  network_rules {
    default_action = "Deny"
    bypass         = ["AzureServices"]
  }

  tags = azurerm_resource_group.reference.tags
}

resource "azurerm_key_vault" "reference" {
  name                          = var.key_vault_name
  location                      = azurerm_resource_group.reference.location
  resource_group_name           = azurerm_resource_group.reference.name
  tenant_id                     = var.tenant_id
  sku_name                      = "standard"
  enable_rbac_authorization     = true
  purge_protection_enabled      = true
  soft_delete_retention_days    = 90
  public_network_access_enabled = false

  network_acls {
    bypass         = "AzureServices"
    default_action = "Deny"
  }

  tags = azurerm_resource_group.reference.tags
}
