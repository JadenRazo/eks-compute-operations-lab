# Screenshot evidence

Selected console views and terminal captures from the lab. Start with these three case studies:

- **Diagnose a Service failure:** [healthy Pods but no endpoints](11-service-selector-failure.png) → [restored selector and requests](12-service-selector-recovered.png). [Read the incident](../incidents/INC-002-service-selector-mismatch.md).
- **Narrow workload permissions:** [excess read access](17-workload-excess-access.png) → [required read preserved; other operations denied](18-workload-least-privilege.png). [Read the audit](../audits/workload-s3-access.md).
- **Adopt existing infrastructure:** [import plan](34-bootstrap-iam-import-plan.png) → [imports completed and no-change plan](35-bootstrap-iam-import-verified.png). [Read the Terraform case study](../architecture/terraform-adoption.md).

## Deployment baseline

| Check | Captures |
| --- | --- |
| EC2 workers and system health | [Ready workers](01-ec2-workers-healthy.png) · [system Pods and node metrics](02-system-health-baseline.png) |
| Console-built network | [VPC resource map during deployment](03-vpc-resource-map.png) |
| Namespace security | [Restricted policy labels](04-namespace-security-policy.png) · [rejected noncompliant Pod dry-run](07-policy-rejection.png) |
| Application deployment | [Rollout completion](05-application-rollout-1.png) · [Ready Pods](05-application-rollout-2.png) · [subsequent rollout](05b-application-image-pinned.png) |
| Request baseline | [HTTP responses](06-application-response.png) · [internal Service observer](06b-internal-service-baseline.png) |
| Fargate deployment | [Pod placement and provisioned capacity](21-fargate-placement.png) |

## Controlled incidents

| Report | Fault or diagnosis | Recovery |
| --- | --- | --- |
| [Readiness failure](../incidents/INC-001-readiness-probe-failure.md) | [Unready new Pod; continuing requests](09-release-diagnosis.png) | [Rollback and readiness checks](10-release-recovered.png) |
| [Service selector mismatch](../incidents/INC-002-service-selector-mismatch.md) | [Wrong selector; empty endpoints](11-service-selector-failure.png) | [Selector and endpoints restored](12-service-selector-recovered.png) |
| [Node maintenance](../incidents/INC-003-node-drain-pdb.md) | [Budget allowing zero disruptions](13-maintenance-blocked.png) | [Eviction retry, completed drain, and uncordon](14-maintenance-recovered.png) |
| [Fargate profile mismatch](../incidents/INC-004-fargate-profile-mismatch.md) | [Label change and rollout timeout](22-fargate-profile-mismatch.png) · [scheduling event](22b-fargate-scheduling-event.png) | [Matching label, Ready Pods, and requests](23-fargate-profile-recovered.png) |

## Access checks

| Report | Captures |
| --- | --- |
| [Namespace reader](../audits/reader-access.md) | [Identity and allowed inspection](15-reader-allowed.png) · [secret and cross-namespace denials](16-reader-denied.png) |
| [EC2 S3 access](../audits/workload-s3-access.md) | [Before narrowing permissions](17-workload-excess-access.png) · [after narrowing permissions](18-workload-least-privilege.png) |
| [Fargate S3 access](../audits/fargate-workload-access.md) | [Identity and permitted read](24a-fargate-workload-identity-read.png) · [denied read and write](24b-fargate-workload-denied-access.png) |

## Terraform adoption and state

| Stage | Captures |
| --- | --- |
| VPC adoption | [Import plan](25-terraform-vpc-import-plan.png) · [verification](26-terraform-vpc-import-verified.png) |
| Network adoption | [Subnets verified](27-terraform-subnets-import-verified.png) · [routing and complete managed network](28-terraform-routing-import-verified.png) |
| [Remote state and locking](../audits/terraform-state-protection.md) | [Encryption, version ID, and no-change result](29-terraform-remote-state-verified.png) · [contention and retry result excerpt](30-terraform-state-locking.png) |
| [Backend permissions](../audits/terraform-backend-access.md) | [State-object simulation](31a-state-object-permissions.png) · [lock-object simulation](31b-state-lock-permissions.png) |
| Bucket adoption | [Import plan](32-bootstrap-bucket-import-plan.png) · [six resources imported](33-bootstrap-bucket-import-verified.png) |
| Backend IAM adoption | [Import plan](34-bootstrap-iam-import-plan.png) · [three resources imported](35-bootstrap-iam-import-verified.png) |
| Bootstrap state migration | [Remote state and no-change result](36-bootstrap-remote-state-verified.png) |

## Reading the evidence

Captures document particular observations, not a live deployment or a complete session history. Reports identify private-only records, simulation results, and missing evidence. In particular, the Fargate request totals survive as a summary; the underlying observer logs are empty. Filenames alone do not establish what a capture proves.

[Back to the project overview](../../README.md)
