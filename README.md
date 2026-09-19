# EKS Compute Operations Lab

I built an AWS lab through the console and eksctl, ran the same Kubernetes workload on **EC2 and Fargate**, and adopted the retained infrastructure into **Terraform**. The focus was operating the environment: diagnose failures, test access boundaries, recover, and verify the result.

## What I demonstrated

| Skill | Result | Explore the evidence |
| --- | --- | --- |
| Kubernetes troubleshooting | Investigated failures and verified recovery across four controlled exercises. | [Service failure and recovery](docs/incidents/INC-002-service-selector-mismatch.md) |
| AWS and Kubernetes access control | Restricted reader access and removed an unnecessary S3 read permission while preserving the required read. | [S3 before/after audit](docs/audits/workload-s3-access.md) · [reader audit](docs/audits/reader-access.md) |
| Adopting infrastructure as code | Imported 23 existing network and backend resources; subsequent plans reported no changes. | [Terraform adoption](docs/architecture/terraform-adoption.md) · [IAM import result](docs/screenshots/35-bootstrap-iam-import-verified.png) |

**[Browse the screenshot evidence](docs/screenshots/README.md)** for deployment, incident, access, and Terraform results.

## How I built it

| Tool | Responsibility |
| --- | --- |
| AWS console | Initial network, S3, and IAM configuration |
| eksctl | Sequential EC2-backed and Fargate EKS clusters |
| Kubernetes + Kustomize | Application, health probes, access controls, observer, and Fargate overlay |
| Terraform | Adoption of the retained network, state bucket configuration, and backend IAM resources |

The `inventory-status` workload serves synthetic data through an internal ClusterIP Service. It has two replicas, pinned container images, non-root execution, health probes, and a PodDisruptionBudget. A separate observer records timestamped request results.

## EC2 and Fargate in this lab

| Area | Managed EC2 nodes | Fargate |
| --- | --- | --- |
| Compute configuration | Two `t3.medium` workers in private subnets | Profiles select system and application Pods |
| Application configuration | Shared base with a soft zone-spread preference | Overlay removes that preference and matches resource requests to limits |
| Operational exercise | Drain a worker while respecting the disruption budget | Recover a rollout whose Pod label no longer matches its profile |
| Workload identity | Dedicated IRSA role for the S3 audit | Separate IRSA role with the same restricted policy |

This comparison covers configuration and operational behavior. Performance benchmarking and a verified cost comparison were outside the completed work.

## Failure exercises

| Controlled fault | Observed result | Lesson |
| --- | --- | --- |
| [Readiness failure](docs/incidents/INC-001-readiness-probe-failure.md) | New Pod unready; rollback completed; saved observer snapshots had no failures. | Check rollout progress and request availability separately. |
| [Service selector mismatch](docs/incidents/INC-002-service-selector-mismatch.md) | Healthy Pods, empty Service endpoints, failed requests; restoring the selector recovered access. | Pod health alone does not prove a working Service. |
| [Node drain and PDB](docs/incidents/INC-003-node-drain-pdb.md) | Eviction temporarily rejected; drain completed; worker uncordoned. | Verify replacement capacity and replica placement during maintenance. |
| [Fargate profile mismatch](docs/incidents/INC-004-fargate-profile-mismatch.md) | Rollout timed out; restoring the matching label completed it. | Profile eligibility is part of deployment correctness. |

Reports distinguish screenshots, retained logs, and summaries. Sampled requests and exercise intervals are not availability guarantees or exact outage durations.

## Architecture

The clusters ran in separate phases and were later deleted. The deployment diagram shows those historical environments; the Terraform diagram shows retained infrastructure.

<details>
<summary>View the deployment diagram</summary>

![Historical EKS deployment phases, networking, and workload identity](docs/diagrams/eks-compute-architecture.svg)

</details>

<details>
<summary>View Terraform ownership and state access</summary>

![Terraform roots, backend access, and retained infrastructure](docs/diagrams/terraform-state-architecture.svg)

</details>

[Diagram explanations and editable source](docs/diagrams/README.md)

## Further access and state checks

- [EC2 infrastructure](docs/audits/infrastructure-access.md): worker permissions, VPC CNI identity, and metadata access tests.
- [Fargate workload access](docs/audits/fargate-workload-access.md): allowed reads, denied operations, and execution-role separation.
- [Terraform state protection](docs/audits/terraform-state-protection.md): S3 migration and lock contention.
- [Terraform backend access](docs/audits/terraform-backend-access.md): state and lock-object permission simulations.

## Current state and remaining work

Both lab clusters, the NAT gateway, and its Elastic IP were removed. The network, versioned S3 state bucket, and backend IAM resources remain under Terraform management.

The OpsBox provisioning role still has `AdministratorAccess`. State-version restoration remains untested, and bootstrap manages the bucket holding its own state. These are documented limits of this independent lab.

Final cost reconciliation, the recorded walkthrough, and public release remain outstanding. **$20 was the project budget target, not verified spend.** The cost review must include the OpsBox, retained storage, and logs. One zonal NAT gateway was a deliberate lab cost/availability tradeoff.

## Code and reuse

[Cluster configurations](eksctl/) · [Kubernetes manifests](kubernetes/) · [Network Terraform](terraform/network/) · [Bootstrap Terraform](terraform/bootstrap/)

These files record this lab environment and need adaptation before deployment elsewhere. Private logs, Terraform state, and saved plans are excluded from version control.

<details>
<summary>Reproduction prerequisites</summary>

- Replace account IDs, resource IDs, role ARNs, and the EKS endpoint allowlist.
- Restore private-subnet egress before rebuilding either cluster.
- Update cluster-specific OIDC trust and the maintenance observer's worker selector.
- Supply existing backend buckets and authorized credentials before initializing the committed S3 backends.
- Review Terraform plans and cleanup ownership, including the retained state bucket.

</details>
