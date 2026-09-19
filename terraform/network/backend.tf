terraform {
  backend "s3" {
    bucket       = "eks-compute-lab-tfstate-919651863281-us-east-1"
    key          = "network/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
