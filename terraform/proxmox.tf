terraform {
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = ">=1.0.0"
    }
  }
  required_version = ">= 0.14"
}

provider "proxmox" {
  # Configuration options
}