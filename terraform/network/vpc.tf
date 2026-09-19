resource "aws_vpc" "lab" {
  cidr_block           = "10.80.0.0/16"
  instance_tenancy     = "default"
  enable_dns_support   = true
  enable_dns_hostnames = true


  tags = {
    Name        = "eks-compute-lab-vpc"
    Environment = "lab"
    Project     = "eks-compute-lab"

  }
}
