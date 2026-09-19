terraform {
  required_version = "~> 1.15.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>6.65.0"
    }
  }


  backend "local" {
    path = "../../private/bootstrap-state/terraform.tfstate"
  }
}


