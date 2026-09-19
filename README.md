# EKS Compute Operations Lab

An independent AWS lab comparing EKS managed EC2 nodes and Fargate through application deployment, controlled failure exercises, access audits, and infrastructure adoption into Terraform.

## Work completed

- Deployed the application on EC2-backed EKS and Fargate using eksctl.
- Exercised rollout failures, Service troubleshooting, node maintenance, and Fargate profile selection.
- Tested namespace-scoped Kubernetes access.
- Demonstrated excessive workload access to synthetic S3 fixtures, narrowed permissions, and tested allowed and denied operations.
- Audited worker-node access, workload identity, and Fargate execution-role permissions.
- Manually wrote Terraform and imported the retained network, state bucket settings, and backend IAM resources.
- Configured separate network and bootstrap state objects in versioned S3 storage with state locking.

The EKS clusters were removed after the exercises. Retained infrastructure includes the Terraform-managed network and state-storage setup.

## Tool ownership

| Area | Implementation |
|---|---|
| Initial AWS configuration | AWS console |
| EC2 and Fargate clusters | eksctl |
| Application and access configuration | Kubernetes manifests |
| Retained network and backend infrastructure | Terraform |

Terraform adoption covered existing network and backend resources. EKS provisioning remains represented by the eksctl configurations.

## Documentation

- [Terraform adoption and state architecture](docs/architecture/terraform-adoption.md)
- [Kubernetes reader-access audit](docs/audits/reader-access.md)
- [Workload S3 access audit](docs/audits/workload-s3-access.md)
- [Infrastructure access audit](docs/audits/infrastructure-access.md)
- [Fargate workload access audit](docs/audits/fargate-workload-access.md)
- [Terraform backend access audit](docs/audits/terraform-backend-access.md)
- [Terraform state protection](docs/audits/terraform-state-protection.md)
- [Fargate profile-mismatch incident](docs/incidents/INC-004-fargate-profile-mismatch.md)

Earlier incident reports, architecture diagrams, and the recorded walkthrough are being prepared from retained evidence.

## Constraints and limitations

This is an independent lab, not a production deployment.

The project allowance is $20 across all sessions and rebuilds. Final actual spending has not yet been reconciled.

The deployed network used one zonal NAT gateway as a cost and availability tradeoff. The lab NAT gateway was subsequently removed.

The OpsBox role retains AdministratorAccess. A dedicated role scopes the network backend session, but does not eliminate the OpsBox role's broader access.

Private logs, Terraform state, and saved plans are excluded from version control. Public evidence should contain only the information needed to demonstrate each result.
