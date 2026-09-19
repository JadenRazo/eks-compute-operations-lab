import {
  to = aws_vpc.lab
  id = "vpc-0cc13129c2e0c7337"
}

import {
  to = aws_subnet.public_a
  id = "subnet-0f227d028bf0cbf3f"
}

import {
  to = aws_subnet.public_b
  id = "subnet-024db7d8c0e61639e"
}

import {
  to = aws_subnet.private_a
  id = "subnet-0426017a260f857cf"
}

import {
  to = aws_subnet.private_b
  id = "subnet-09ed91cd610169615"
}

import {
  to = aws_internet_gateway.lab
  id = "igw-03622dcc3991f09e4"
}

import {
  to = aws_route_table.public
  id = "rtb-009dbfac70d814848"
}

import {
  to = aws_route_table.private_a
  id = "rtb-03586c53e86c4908f"
}

import {
  to = aws_route_table.private_b
  id = "rtb-0c015ca22a0db2445"
}

import {
  to = aws_route.public_internet
  id = "rtb-009dbfac70d814848_0.0.0.0/0"
}

import {
  to = aws_route_table_association.public_a
  id = "subnet-0f227d028bf0cbf3f/rtb-009dbfac70d814848"
}

import {
  to = aws_route_table_association.public_b
  id = "subnet-024db7d8c0e61639e/rtb-009dbfac70d814848"
}

import {
  to = aws_route_table_association.private_a
  id = "subnet-0426017a260f857cf/rtb-03586c53e86c4908f"
}

import {
  to = aws_route_table_association.private_b
  id = "subnet-09ed91cd610169615/rtb-0c015ca22a0db2445"
}
