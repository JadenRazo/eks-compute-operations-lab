# Terraform backend access

**Result:** the network backend assumed a dedicated role with separate state and lock-object permissions. Policy simulations allowed the required operations and denied the tested state deletions and unrelated-object access.

## Implementation and checks

The [network backend](../../terraform/network/backend.tf) assumes `eks-lab-terraform-state`. Reconfiguration succeeded, followed by a no-change plan. The [IAM configuration](../../terraform/bootstrap/state-iam.tf) defines these object permissions:

| Resource | Simulated actions | Decision |
| --- | --- | --- |
| `network/terraform.tfstate` | `GetObject`, `PutObject` | `allowed` |
| Network state | `DeleteObject`, `DeleteObjectVersion` | `implicitDeny` |
| `network/terraform.tfstate.tflock` | `GetObject`, `PutObject`, `DeleteObject` | `allowed` |
| Unrelated object | `GetObject`, `PutObject` | `implicitDeny` |

**Screenshots:** [state-object permissions](../screenshots/31a-state-object-permissions.png) · [lock-object permissions](../screenshots/31b-state-lock-permissions.png). The unrelated-object results are retained in private terminal records under `private/terraform-iam-audit/`.

These were simulations; they did not delete or overwrite S3 objects. The live no-change plan separately checked backend use, but did not demonstrate writing updated infrastructure state.

## Remaining boundary

**The OpsBox still has `AdministratorAccess`.** The AWS provider uses that identity, and it retains direct administrative access outside the narrower backend session.

The backend role can overwrite state through `PutObject`. Versioning supports recovery, but restoration has not been tested. Policy simulation also does not cover every possible effective-access path.

## Operational lesson

Backend credentials and provider credentials are separate concerns. A future improvement is to test a scoped provisioning role against the required workflows before removing routine administrator access.
