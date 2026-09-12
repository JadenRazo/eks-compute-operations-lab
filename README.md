# EKS Compute Operations Lab

An independent AWS lab comparing EKS managed EC2 nodes and Fargate.

The project explores application deployment, incident diagnosis and
recovery, IAM and Kubernetes access controls, and manual Terraform
recreation.

## Current status

- EC2-backed EKS cluster deployed in us-east-1.
- Two private worker nodes verified Ready.
- Supporting system pods verified healthy.
- ops-lab namespace created.
- Application deployment and security enforcement tests pending.
- Fargate comparison and Terraform recreations pending.

## Constraints

The total project allowance is $20 across all sessions and rebuilds.
The current deployment uses a dedicated lab VPC in an existing account.
One zonal NAT gateway is a deliberate cost and availability tradeoff.

## Evidence

Screenshots and sanitized results will document configuration,
controlled failures, recovery, access tests, and cleanup.
