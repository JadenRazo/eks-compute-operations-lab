# From console configuration to Terraform

**Result:** adopted 23 existing network and backend resources into two Terraform roots. Reviewed import plans preserved the existing resources, and subsequent plans reported no changes.

I first built the network, bucket, and IAM configuration through the AWS console. Writing the Terraform manually required matching the live configuration and deciding what each root should own. EKS cluster provisioning remained with eksctl.

## Ownership

| Root | Managed scope | State key |
| --- | --- | --- |
| [Network](../../terraform/network/) | 14 resources: VPC, four subnets, internet gateway, three route tables, public default route, four subnet associations | `network/terraform.tfstate` |
| [Bootstrap](../../terraform/bootstrap/) | Nine resources: bucket, five S3 configuration resources, backend IAM role, policy, and attachment | `bootstrap/terraform.tfstate` |

## Adoption workflow and evidence

1. Inventory existing resources and write matching resource blocks.
2. Declare imports, then review plans for zero additions, changes, or destruction.
3. Apply the reviewed import plans and check the resulting state addresses.
4. Run fresh plans to verify configuration agreement.

| Stage | Screenshot evidence |
| --- | --- |
| VPC | [Import plan](../screenshots/25-terraform-vpc-import-plan.png) · [verification](../screenshots/26-terraform-vpc-import-verified.png) |
| Subnets and routing | [Subnet verification](../screenshots/27-terraform-subnets-import-verified.png) · [all 14 network resources](../screenshots/28-terraform-routing-import-verified.png) |
| Bucket and five S3 controls | [Six-resource import plan](../screenshots/32-bootstrap-bucket-import-plan.png) · [import and no-change result](../screenshots/33-bootstrap-bucket-import-verified.png) |
| Backend IAM | [Three-resource import plan](../screenshots/34-bootstrap-iam-import-plan.png) · [import and no-change result](../screenshots/35-bootstrap-iam-import-verified.png) |
| Bootstrap state migration | [Encryption, version ID, and no-change result](../screenshots/36-bootstrap-remote-state-verified.png) |

Configuration and provider lock files are committed. State, saved plans, and raw inventories remain private.

## State and access design

Both roots use separate keys and lock objects in one versioned S3 bucket. Bucket controls include AES256 encryption, blocked SSE-C uploads, Block Public Access, bucket-owner-enforced ownership, and HTTPS-only access.

The network backend assumes a dedicated state role. Bootstrap administration and both AWS providers use the OpsBox role, which retains `AdministratorAccess`.

[Ownership diagram](../diagrams/terraform-state-architecture.svg) · [state protection](../audits/terraform-state-protection.md) · [backend permission audit](../audits/terraform-backend-access.md)

## Lifecycle and lesson

Bootstrap state started locally, then moved to S3 after a backup and resource-address comparison. Bootstrap now manages the bucket holding its own state, so cleanup and recovery require deliberate handling. `prevent_destroy` guards the configured resource; it does not restrict AWS administrator actions.

A no-change plan establishes agreement for the resources and attributes managed by that root. It does not establish account-wide Terraform coverage, least privilege, or tested state recovery. The practical lesson is to define ownership and verify each adoption step before expanding the managed scope.
