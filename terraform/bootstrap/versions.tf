terraform {
  required_version = "~> 1.15.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>6.65.0"
    }
  }


  backend "s3" {
    bucket              = "eks-compute-lab-tfstate-919651863281-us-east-1"
    key                 = "bootstrap/terraform.tfstate"
    region              = "us-east-1"
    encrypt             = true
    use_lockfile        = true
    allowed_account_ids = ["919651863281"]
  }
}


