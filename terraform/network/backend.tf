terraform {
  backend "s3" {
    bucket       = "eks-compute-lab-tfstate-919651863281-us-east-1"
    key          = "network/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true

    assume_role = {
      role_arn     = "arn:aws:iam::919651863281:role/eks-lab-terraform-state"
      session_name = "terraform-network-state"
    }
  }
}
