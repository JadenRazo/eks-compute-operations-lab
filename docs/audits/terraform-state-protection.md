# Terraform state protection

## Scope

Migrated the lab network’s Terraform state from the OpsBox’s local filesystem to a dedicated S3 backend.

The network configuration manages 14 resources: one VPC, four subnets, one internet gateway, three route tables, one public default route, and four subnet associations.

## Backend configuration

- State object: `network/terraform.tfstate`
- Encryption: SSE-S3
- Bucket versioning: enabled
- Terraform S3 locking: `use_lockfile = true`
- Public access: blocked
- Bucket policy: denies requests using insecure transport

The backend configuration contains no credentials. State files, saved plans, and raw evidence are excluded from Git.

## Migration verification

The remote state object returned `AES256` encryption and a version ID. Terraform’s subsequent plan reported no changes.

A private local backup was retained before migration.

## Lock-contention test

1. Added a temporary Terraform output.
2. Started an interactive apply and left it waiting for approval.
3. Verified that the S3 state-lock object existed.
4. Started a second plan against the same backend and workspace.
5. Confirmed that the second plan failed to acquire the state lock.
6. Cancelled the first apply without approving it.
7. Removed the temporary output and retried the plan.
8. Confirmed that the retry completed with no changes.

No AWS resource changes were applied during the test. No manual lock deletion or force-unlock was needed.

## Evidence

- `29-terraform-remote-state-verified.png`
- `30-terraform-state-locking.png`
- Private test logs under `private/state-lock-test/`

## Limitations

The initial console-based attempt did not demonstrate contention; the verified test used an apply waiting for approval.

Versioning was verified, but restoration of an earlier state version has not yet been tested.

This test demonstrates contention between cooperating Terraform processes. It does not prevent someone with sufficient S3 permissions from modifying state directly.

IAM permissions for state access require a separate review.
