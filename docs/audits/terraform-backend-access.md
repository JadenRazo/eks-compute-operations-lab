# Terraform backend access audit

## Scope

This audit evaluated the dedicated IAM role `eks-lab-terraform-state`, used by the Terraform network configuration to access its S3 backend.

The backend stores state at `network/terraform.tfstate` and uses `network/terraform.tfstate.tflock` for locking.

## Implementation

The S3 backend assumes the dedicated state role. Its permissions allow reading and updating the network state object and reading, creating, and deleting the corresponding lock object.

Backend reconfiguration completed successfully. A subsequent Terraform plan refreshed the managed network resources and reported no changes.

The configuration was committed in `db526d8`.

## Permission simulation results

| Resource | Action | Observed decision |
|---|---|---|
| Network state | GetObject | allowed |
| Network state | PutObject | allowed |
| Network state | DeleteObject | implicitDeny |
| Network state | DeleteObjectVersion | implicitDeny |
| Network lock | GetObject | allowed |
| Network lock | PutObject | allowed |
| Network lock | DeleteObject | allowed |
| Unrelated object | GetObject | implicitDeny |
| Unrelated object | PutObject | implicitDeny |

These were IAM policy simulations. No S3 objects were deleted or overwritten by the simulations.

## Evidence

- `31a-state-object-permissions.png`
- `31b-state-lock-permissions.png`
- Private terminal records in `private/terraform-iam-audit/`

## Interpretation and limitations

The observed simulation results match the intended object permissions. The successful live plan separately demonstrated that Terraform could use the configured backend during a no-change planning operation.

The no-change plan did not demonstrate writing updated infrastructure state. Policy simulation is not a complete test of effective access across all applicable AWS controls.

The role can overwrite the state object through PutObject. Restricting deletion does not make state immutable. Bucket versioning supports recovery, but a version-restoration exercise was not part of this check.

## Remaining administrator access

The OpsBox role still has AdministratorAccess. The AWS provider continues to use that role for infrastructure operations.

Assuming a narrower backend role scopes the backend session. It does not remove the OpsBox role’s direct administrative access to S3 or other AWS services.

A future improvement is to replace routine provisioning access with a separately scoped role, test the required workflows, and then review whether administrator access can be removed from the OpsBox without disrupting its other responsibilities.
