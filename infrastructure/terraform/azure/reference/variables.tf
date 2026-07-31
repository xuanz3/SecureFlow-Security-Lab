variable "location" {
  description = "Reference deployment region."
  type        = string
  default     = "australiaeast"
}

variable "resource_group_name" {
  description = "Reference resource group name."
  type        = string
  default     = "rg-secureflow-reference"
}

variable "storage_account_name" {
  description = "Globally unique lowercase storage account name supplied at plan time."
  type        = string
}

variable "key_vault_name" {
  description = "Globally unique Key Vault name supplied at plan time."
  type        = string
}

variable "tenant_id" {
  description = "Azure tenant identifier supplied at plan time."
  type        = string
  sensitive   = true
}
