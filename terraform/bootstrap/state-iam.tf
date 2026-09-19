resource "aws_iam_role" "terraform_state" {
  name                 = "eks-lab-terraform-state"
  path                 = "/"
  description          = ""
  max_session_duration = 3600

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Effect = "Allow"

        Principal = {
          AWS = "arn:aws:iam::919651863281:role/raizhost-opsbox-919"
        }

        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Project     = "eks-compute-lab"
    Environment = "lab"
  }
}

resource "aws_iam_policy" "network_state" {
  name = "eks-lab-terraform-network-state"
  path = "/"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid      = "ListStateBucket"
        Effect   = "Allow"
        Action   = "s3:ListBucket"
        Resource = aws_s3_bucket.state.arn
      },
      {
        Sid    = "ReadWriteNetworkState"
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]

        Resource = "${aws_s3_bucket.state.arn}/network/terraform.tfstate"
      },
      {
        Sid    = "ManageNetworkStateLock"
        Effect = "Allow"

        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]

        Resource = "${aws_s3_bucket.state.arn}/network/terraform.tfstate.tflock"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "network_state" {
  role       = aws_iam_role.terraform_state.name
  policy_arn = aws_iam_policy.network_state.arn
}

