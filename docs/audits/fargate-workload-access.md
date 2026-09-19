# Fargate workload access

**Result:** the Fargate audit Pod read the approved S3 object through its own IAM role. An unrelated read and an attempted write were denied.

## Observed checks

| Check inside `ops-lab/aws-audit` | Result |
| --- | --- |
| Caller identity | Assumed role `eks-lab-s3-audit-fargate` |
| Read `allowed/catalog.json` | Succeeded: 32 bytes |
| Read `unrelated/internal-note.txt` | `AccessDenied` |
| Write `allowed/fargate-write-test.json` | `AccessDenied` |

**Screenshots:** [identity and permitted read](../screenshots/24a-fargate-workload-identity-read.png) · [denied read and write](../screenshots/24b-fargate-workload-denied-access.png).

The negative-test helper required a failed command **and** an `AccessDenied` response. Other errors did not count as successful permission checks.

## Identity boundaries

The audit reused the policy narrowed during the [EC2 audit](workload-s3-access.md), with a separate role and the Fargate cluster's OIDC provider.

| Identity or selector | Responsibility |
| --- | --- |
| Fargate profile: `ops-lab`, `compute: lab` | Determines Pod placement eligibility |
| Workload IRSA role | Allows `s3:GetObject` under `allowed/`; trust restricts subject to `system:serviceaccount:ops-lab:aws-audit` and audience to `sts.amazonaws.com` |
| Fargate Pod execution role | Infrastructure duties; separate from the container's S3 permissions |

The execution-role review found the `eks-fargate-pods.amazonaws.com` trust principal, a source ARN restricted to the lab cluster's profiles, and only `AmazonEKSFargatePodExecutionRolePolicy` attached. No inline policies or remediation were identified in that review.

## Scope and lesson

The same intended S3 boundary held across the two compute environments. Scheduling eligibility and workload AWS permissions need separate checks.

These results cover the tested identity, objects, and actions. Raw responses and execution-role inventory remain private. The temporary audit Pod was removed after testing; its [manifests](../../kubernetes/fargate/) remain in the repository.
