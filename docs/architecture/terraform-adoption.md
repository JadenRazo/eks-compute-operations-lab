# Adopting existing AWS infrastructure into Terraform

## Objective

I first configured the lab through the AWS console and eksctl, then manually wrote Terraform to describe the retained infrastructure. This let me compare the live AWS configuration with its infrastructure-as-code representation.

The EKS clusters were deployed using eksctl. Terraform adoption covered the retained network, state-storage configuration, and dedicated network-backend IAM resources.

## Configuration boundaries

| Terraform root | Managed resources | Remote state key |
|---|---|---|
| `terraform/network` | VPC, four subnets, internet gateway, three route tables, public default route, and four subnet associations | `network/terraform.tfstate` |
| `terraform/bootstrap` | State bucket, versioning, encryption, public-access block, ownership controls, bucket policy, backend IAM role, permissions policy, and role-policy attachment | `bootstrap/terraform.tfstate` |

Both state objects reside in the same versioned S3 bucket. They use separate keys and S3 lock files.

## Adoption process

1. Read the existing AWS configuration and retain private inventory records.
2. Write resource blocks matching the observed settings.
3. Declare imports mapping existing AWS resources to Terraform addresses.
4. Review plans for imports with no resource additions, changes, or destruction.
5. Apply the reviewed import plans.
6. Run fresh plans to verify that the imported resources match the configuration.
7. Commit configuration and provider lock files while excluding state, saved plans, and private evidence.

The network root tracks 14 resources. The bootstrap root tracks nine.

## State and access controls

The state bucket has versioning enabled, AES256 default encryption, SSE-C uploads blocked, all four Block Public Access settings enabled, and bucket-owner-enforced object ownership. Its bucket policy denies insecure transport.

The network backend assumes a dedicated role with read/write access to its state object and read/write/delete access to its lock object. IAM simulations confirmed no grants for state deletion or reading and writing an unrelated object.

Bootstrap administration and AWS provider operations still use the OpsBox role, which retains AdministratorAccess. The narrower network-backend session does not remove that broader access.

## Bootstrap lifecycle

Bootstrap state was initially local, then migrated to the S3 key `bootstrap/terraform.tfstate`. A private local backup was retained, resource addresses were compared, and a subsequent plan reported no changes.

The bootstrap configuration manages the bucket holding its own state. It is retained infrastructure and requires a deliberate recovery or decommissioning process. The bucket's Terraform `prevent_destroy` setting is a configuration safeguard, not an AWS authorization boundary.

## Evidence

- Screenshots 31a and 31b: backend permission simulations.
- Screenshot 32: bucket import plan.
- Screenshot 33: bucket import verification.
- Screenshot 34: IAM import plan.
- Screenshot 35, or 35a and 35b: IAM import verification.
- Screenshot 36: bootstrap remote-state verification.

Bootstrap state migration was committed in `da70f50`.

## Scope of the result

No-change plans demonstrate agreement for the resources and attributes managed by these Terraform configurations. They do not establish that every resource in the AWS account is managed, that all access is least privilege, or that recovery from a lost state bucket has been tested.
