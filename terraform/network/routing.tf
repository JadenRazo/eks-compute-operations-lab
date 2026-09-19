resource "aws_internet_gateway" "lab" {
  vpc_id = aws_vpc.lab.id

  tags = {
    Name        = "eks-compute-lab-igw"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.lab.id

  tags = {
    Name        = "eks-compute-lab-rtb-public"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_route_table" "private_a" {
  vpc_id = aws_vpc.lab.id

  tags = {
    Name        = "eks-compute-lab-rtb-private1-us-east-1a"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_route_table" "private_b" {
  vpc_id = aws_vpc.lab.id

  tags = {
    Name        = "eks-compute-lab-rtb-private2-us-east-1b"
    Environment = "lab"
    Project     = "eks-compute-lab"
  }
}

resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.lab.id
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private_a" {
  subnet_id      = aws_subnet.private_a.id
  route_table_id = aws_route_table.private_a.id
}

resource "aws_route_table_association" "private_b" {
  subnet_id      = aws_subnet.private_b.id
  route_table_id = aws_route_table.private_b.id
}

