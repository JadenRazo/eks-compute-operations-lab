import {
  to = aws_s3_bucket.state
  id = local.state_bucket_name
}

import {
  to = aws_s3_bucket_versioning.state
  id = local.state_bucket_name
}

import {
  to = aws_s3_bucket_server_side_encryption_configuration.state
  id = local.state_bucket_name
}

import {
  to = aws_s3_bucket_public_access_block.state
  id = local.state_bucket_name
}

import {
  to = aws_s3_bucket_ownership_controls.state
  id = local.state_bucket_name
}

import {
  to = aws_s3_bucket_policy.state
  id = local.state_bucket_name
}

import {
  to = aws_iam_role.terraform_state
  id = "eks-lab-terraform-state"
}

import {
  to = aws_iam_policy.network_state
  id = "arn:aws:iam::919651863281:policy/eks-lab-terraform-network-state"
}

import {
  to = aws_iam_role_policy_attachment.network_state
  id = "eks-lab-terraform-state/arn:aws:iam::919651863281:policy/eks-lab-terraform-network-state"
}
