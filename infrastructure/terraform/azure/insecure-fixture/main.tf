# Deliberately insecure, non-deployed fixture for Checkov validation only.

resource "azurerm_resource_group" "fixture" {
  name     = "rg-secureflow-insecure-fixture"
  location = "australiaeast"
}

resource "azurerm_storage_account" "fixture" {
  name                            = "secureflowfixture001"
  resource_group_name             = azurerm_resource_group.fixture.name
  location                        = azurerm_resource_group.fixture.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_0"
  allow_nested_items_to_be_public = true
  public_network_access_enabled   = true
  shared_access_key_enabled       = true
  cross_tenant_replication_enabled = true
}

resource "azurerm_key_vault" "fixture" {
  name                          = "kv-secureflow-fixture"
  location                      = azurerm_resource_group.fixture.location
  resource_group_name           = azurerm_resource_group.fixture.name
  tenant_id                     = "00000000-0000-0000-0000-000000000000"
  sku_name                      = "standard"
  enable_rbac_authorization     = false
  purge_protection_enabled      = false
  public_network_access_enabled = true

  network_acls {
    bypass         = "None"
    default_action = "Allow"
  }
}
