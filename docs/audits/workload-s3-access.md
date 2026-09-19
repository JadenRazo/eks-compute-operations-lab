# EC2 workload S3 access

**Result:** removed an unnecessary object-read permission from the workload's IAM policy. The required read still succeeded; the unrelated read and an attempted write returned `AccessDenied`.

## Finding and change

The `aws-audit` Pod used the IRSA role `eks-lab-s3-audit-ec2`. Its intended access was `s3:GetObject` under the synthetic fixture bucket's `allowed/` prefix.

The initial policy also permitted a read from `unrelated/`. I removed the unnecessary resource ARN and repeated the checks using the workload identity.

| Check | Before policy change | After policy change |
| --- | --- | --- |
| Read `allowed/catalog.json` | Succeeded: 32 bytes | Succeeded: 32 bytes |
| Read `unrelated/internal-note.txt` | Succeeded: 54 bytes | `AccessDenied` |
| Write `allowed/write-test.json` | Not recorded | `AccessDenied` |

**Screenshots:** [excess read access](../screenshots/17-workload-excess-access.png) · [required read preserved; unrelated read and write denied](../screenshots/18-workload-least-privilege.png).

## Operational lesson

Verify the caller identity, test the required operation, then test operations outside that requirement. Retest the required read after narrowing permissions so that a denial is not mistaken for a broken workload.

The [Fargate audit](fargate-workload-access.md) repeated these boundaries with a separate role and cluster OIDC provider.

## Scope

This exercise used synthetic data and tested specific objects and actions. It does not establish least privilege for every AWS identity or permission path. Raw identity and API output remain under `private/s3-audit/` and are excluded from Git.
