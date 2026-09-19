# Terraform state protection

**Result:** network state moved from local storage to versioned S3. The retained evidence shows a lock-acquisition failure during contention and a successful no-change result after the test.

## State configuration

| Control | Configuration |
| --- | --- |
| State object | `network/terraform.tfstate` for 14 network resources |
| Encryption and recovery support | SSE-S3 (`AES256`) and bucket versioning |
| Concurrent access | Native S3 locking: `use_lockfile = true` |
| Bucket access | Block Public Access and an HTTPS-only policy |

A local backup was retained before migration. The [migration screenshot](../screenshots/29-terraform-remote-state-verified.png) shows encryption, a version ID, and the subsequent no-change plan result.

## Lock-contention exercise

The recorded procedure was:

1. Add a temporary output and hold an interactive apply at its approval prompt.
2. Check that the lock object exists, then start a competing plan.
3. Observe failure to acquire the state lock.
4. Cancel the held apply, remove the test output, and rerun the plan.

The [published result excerpt](../screenshots/30-terraform-state-locking.png) shows the acquisition error and the later no-change result. No infrastructure changes were approved, and no force-unlock or manual lock deletion was used.

## Evidence limits and next step

The initial attempt did not establish contention. Private records under `private/state-lock-test/` have filenames that do not consistently match their test stages; the published excerpt is a selection of results, not a complete ordered session transcript.

Locking protects cooperating Terraform operations. An identity with sufficient S3 permissions can still modify state directly. [Backend permission checks](terraform-backend-access.md) cover that separate access boundary.

Versioning was verified; restoring an earlier state version remains untested. A documented recovery rehearsal is the next step for demonstrating recoverability.
