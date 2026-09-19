# EKS Compute Operations Lab

An independent AWS lab comparing **EKS managed EC2 nodes and AWS Fargate** through application deployment, controlled failure exercises, access audits, and manual adoption of existing infrastructure into Terraform.

The project follows an operational workflow: build the environment, introduce a controlled fault, collect evidence, diagnose the behavior, recover, and document the result.

## Project status

The EC2 and Fargate cluster exercises are complete, and both lab clusters were removed. The lab NAT gateway and its Elastic IP were also removed.

The retained network, Terraform state bucket configuration, and network-backend IAM resources are managed through Terraform. Network and bootstrap state use separate objects in a versioned S3 bucket with state locking.

Final cost reconciliation, the recorded walkthrough, and publication materials remain outstanding.

## Architecture

### EC2 and Fargate deployment phases

The clusters were deployed sequentially. This diagram describes the historical lab deployments, including management access, internal application requests, outbound connectivity, and workload identity.

![Historical EKS deployment phases, request paths, networking, and workload identity](docs/diagrams/eks-compute-architecture.svg)

[View the full-size deployment diagram](docs/diagrams/eks-compute-architecture.svg)

### Terraform ownership and state access

This diagram describes the retained infrastructure, separate Terraform roots, and the distinction between backend credentials and provider credentials.

![Terraform roots, backend access, and retained infrastructure](docs/diagrams/terraform-state-architecture.svg)

[View the full-size Terraform diagram](docs/diagrams/terraform-state-architecture.svg)

[Diagram explanations, editable source, and regeneration instructions](docs/diagrams/README.md)

## Implementation scope

| Area | Implementation |
|---|---|
| Initial network, bucket, and IAM configuration | AWS console |
| EC2-backed and Fargate EKS clusters | eksctl |
| Application, Service, probes, and Kubernetes access controls | Kubernetes manifests |
| Fargate application adaptation | Kustomize overlay |
| Retained network and backend infrastructure | Manually written Terraform with imports |
| Verification | AWS CLI, kubectl, request observer, saved logs, and policy simulations |

The application is a small `inventory-status` HTTP workload with two replicas, health probes, and an internal ClusterIP Service. A separate observer records timestamped request successes and failures.

EKS provisioning remains represented by the eksctl configurations. Terraform adoption covered the retained network and backend resources.

## Controlled incident exercises

These were intentionally injected lab scenarios.

| Incident | Exercise | Retained evidence |
|---|---|---|
| [INC-001](docs/incidents/INC-001-readiness-probe-failure.md) | Readiness-probe failure during rollout | Kubernetes recorded an HTTP 404 readiness failure; both saved observer snapshots contained zero failed requests. |
| [INC-002](docs/incidents/INC-002-service-selector-mismatch.md) | Service selector mismatch | Saved request logs contained failures; the original selector and recovery-verification marker were retained. |
| [INC-003](docs/incidents/INC-003-node-drain-pdb.md) | Node maintenance with a PodDisruptionBudget | An eviction was temporarily rejected, the drain retried and completed, and replacement application Pods were Ready on the other worker. |
| [INC-004](docs/incidents/INC-004-fargate-profile-mismatch.md) | Fargate profile mismatch | The rollout timed out after the Pod label stopped matching the profile; the recorded observer window contained 339 successful requests and zero failures. |

Observer snapshots can overlap. Request counts are not added across overlapping files or converted directly into outage durations. Successful sampled requests do not establish an availability guarantee.

## Access and security work

The lab examined several distinct permission boundaries:

- **Human access:** namespace-scoped Kubernetes reader permissions and allowed/denied operation checks.
- **Workload access:** IRSA credentials for a synthetic S3 audit, followed by narrower object permissions and repeat access checks.
- **Worker access:** node-role policies, separate VPC CNI identity, and IMDS configuration and runtime observations.
- **Fargate identity:** separation between the Pod execution role and the workload's IRSA role.
- **Terraform state access:** a dedicated network-backend role with state and lock-object permissions, plus IAM policy simulations.

Detailed reports:

- [Kubernetes reader access](docs/audits/reader-access.md)
- [Workload S3 access](docs/audits/workload-s3-access.md)
- [Infrastructure access](docs/audits/infrastructure-access.md)
- [Fargate workload access](docs/audits/fargate-workload-access.md)
- [Terraform backend access](docs/audits/terraform-backend-access.md)
- [Terraform state protection](docs/audits/terraform-state-protection.md)

**Remaining access limitation:** the OpsBox role retains `AdministratorAccess`. Narrowing the network-backend session does not remove the OpsBox role's broader permissions or make provider operations least privilege.

## From console configuration to Terraform

Existing resources were inventoried, described manually in Terraform, and imported using reviewed plans. Subsequent plans reported no changes.

| Terraform root | Managed scope | State key |
|---|---|---|
| `terraform/network` | 14 resources: VPC, four subnets, internet gateway, three route tables, public default route, and four subnet associations | `network/terraform.tfstate` |
| `terraform/bootstrap` | Nine resources: bucket, five S3 configuration resources, backend IAM role, permissions policy, and attachment | `bootstrap/terraform.tfstate` |

The state bucket uses versioning, AES256 encryption, blocked SSE-C uploads, bucket-owner-enforced ownership, Block Public Access, and an HTTPS-only policy.

Bootstrap manages the bucket holding its own state. It is retained infrastructure and requires deliberate recovery and decommissioning procedures.

[Read the Terraform adoption and state architecture report](docs/architecture/terraform-adoption.md)

## Repository layout

```text
docs/
  architecture/       Terraform adoption and design documentation
  audits/             Access and state-protection reports
  diagrams/           SVGs, Mermaid sketches, and diagram generator
  incidents/          Controlled failure and maintenance reports
eksctl/               EC2 and Fargate cluster configurations
kubernetes/
  base/               Shared application and access manifests
  ec2/                EC2-specific maintenance configuration
  fargate/            Fargate overlay and audit workloads
terraform/
  network/            Retained network configuration and imports
  bootstrap/          State bucket and backend IAM configuration
```

Private logs, Terraform state, and saved plans are excluded from version control.

## Reproduction considerations

These configurations describe this lab environment and require adaptation before use elsewhere.

- Review account IDs, subnet IDs, IAM role ARNs, and the EKS endpoint allowlist.
- Restore the required private-subnet egress before rebuilding either cluster.
- Update cluster-specific OIDC trust relationships when recreating EKS.
- Update any EC2 observer node selector that references a previous worker hostname.
- Existing backend buckets and authorized credentials are prerequisites for initializing the committed S3 backends.
- Review Terraform plans and cleanup ownership before applying changes.

## Tradeoffs and lessons

- **Readiness and availability are different signals.** A new revision can fail readiness while existing replicas continue serving requests.
- **Healthy Pods do not guarantee a working Service.** Labels, selectors, and eligible endpoints must agree.
- **A PDB constrains voluntary disruption.** It does not guarantee resilience to node failure.
- **Two nodes or two subnets do not prove balanced replica placement.** The EC2 maintenance evidence showed replicas sharing a node.
- **Fargate shifts operational responsibility.** Profile selection and workload identity still require deliberate configuration.
- **Importing infrastructure requires configuration matching.** A no-change plan applies to the resources and attributes managed by that Terraform root.

## Cost and remaining work

The project allowance is **$20 across all sessions and rebuilds**. This is a budget target, not a verified final spend.

The deployed lab used one zonal NAT gateway as a cost and availability tradeoff. Cluster and NAT teardown does not establish that every remaining AWS resource is free; the OpsBox, retained storage, and logs must be included in the cost review.

Remaining work:

- Reconcile actual spending and document retained resources.
- Review public evidence and repository links.
- Record the architecture and incident walkthrough.
- Publish the project summary.

This repository documents independent lab experience. It does not represent operation of a production EKS environment.
