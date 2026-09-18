# Fargate workload access audit

## Objective

Verify that an application running on EKS Fargate can access an approved S3 object through its own IAM role while unrelated reads and writes remain denied.

This was a controlled lab exercise using synthetic fixtures.

## Configuration

- Cluster: `eks-compute-lab-fargate`
- Namespace: `ops-lab`
- Pod: `aws-audit`
- Kubernetes ServiceAccount: `aws-audit`
- Workload IAM role: `eks-lab-s3-audit-fargate`
- Permissions policy: `eks-lab-s3-fixture-read`
- Fargate profile matching label: `compute: lab`

The role trust policy names this cluster’s OIDC provider and restricts the subject to `system:serviceaccount:ops-lab:aws-audit`, with audience `sts.amazonaws.com`.

The permissions policy allows `s3:GetObject` within the fixture bucket’s `allowed/` prefix.

## Validation results

| Check | Observed result |
|---|---|
| Query caller identity inside the Pod | Assumed role `eks-lab-s3-audit-fargate` |
| Read `allowed/catalog.json` | Succeeded; returned 32 bytes |
| Read `unrelated/internal-note.txt` | Denied with `AccessDenied` |
| Write `allowed/fargate-write-test.json` | Denied with `AccessDenied` |

The negative-test helper required both a failed command and an `AccessDenied` response before classifying a test as an expected denial. Other errors were not treated as successful security checks.

## Comparison with the EC2 audit

The earlier EC2 workload audit demonstrated excessive read access and then narrowed that access.

The Fargate audit reused the restricted policy with a separate workload role and the Fargate cluster’s OIDC provider. It verified that the same intended access boundaries worked with the new compute environment.

The Fargate profile determines where the Pod runs. The ServiceAccount’s IAM role association determines the AWS permissions available to its containers.

The Fargate Pod execution role serves infrastructure operations and is separate from this workload role.

## Evidence

- `24a-fargate-workload-identity-read.png`
- `24b-fargate-workload-denied-access.png`

Raw identity and API responses are retained privately under `private/fargate-s3-audit/` and excluded from the public repository.

## Limitations

These checks establish the observed behavior for the tested identity, objects, and actions. They are not an exhaustive audit of every AWS permission or possible access path.

No credential values or fixture contents were required in the public screenshots.

## Cleanup

The temporary audit Pod was deleted after preserving the evidence. Its manifests and the ServiceAccount configuration were retained for reproducibility.
