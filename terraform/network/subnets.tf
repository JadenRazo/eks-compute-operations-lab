resource "aws_subnet" "public_a" {
  vpc_id                          = aws_vpc.lab.id
  cidr_block                      = "10.80.0.0/24"
  availability_zone               = "us-east-1a"
  map_public_ip_on_launch         = false
  assign_ipv6_address_on_creation = false

  tags = {
    Name        = "eks-compute-lab-subnet-public1-us-east-1a"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                          = aws_vpc.lab.id
  cidr_block                      = "10.80.1.0/24"
  availability_zone               = "us-east-1b"
  map_public_ip_on_launch         = false
  assign_ipv6_address_on_creation = false

  tags = {
    Name        = "eks-compute-lab-subnet-public2-us-east-1b"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_subnet" "private_a" {
  vpc_id                          = aws_vpc.lab.id
  cidr_block                      = "10.80.10.0/24"
  availability_zone               = "us-east-1a"
  map_public_ip_on_launch         = false
  assign_ipv6_address_on_creation = false

  tags = {
    Name        = "eks-compute-lab-subnet-private1-us-east-1a"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id                          = aws_vpc.lab.id
  cidr_block                      = "10.80.11.0/24"
  availability_zone               = "us-east-1b"
  map_public_ip_on_launch         = false
  assign_ipv6_address_on_creation = false

  tags = {
    Name        = "eks-compute-lab-subnet-private2-us-east-1b"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}
