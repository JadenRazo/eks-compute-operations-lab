# Kubernetes reader access

**Result:** a dedicated reader identity could inspect application Pods and logs in `ops-lab`, while tested secret access, cross-namespace access, and workload changes were denied.

## Access design

`IAM reader role → EKS access entry → ops-lab-readers group → namespace RoleBinding → Role`

The [RBAC manifest](../../kubernetes/base/reader-rbac.yaml) grants inspection permissions in `ops-lab`. Tests used the actual `eks-lab-reader` role through a separate kubeconfig; `auth whoami` confirmed the role and group.

## Observed checks

| Operation using the reader identity | Result |
| --- | --- |
| List application Pods | Allowed |
| Read application logs | Allowed |
| List secrets in `ops-lab` | `Forbidden` |
| List Pods in `kube-system` | `Forbidden` |
| Execute a command in an application container | `pods/exec` creation forbidden |
| Attempt scaling with server dry-run | `Forbidden` |
| Ask `auth can-i` about patching Deployments | `no` |
| Ask `auth can-i` about patching Deployment scale | `no` |

**Screenshots:** [identity, Pods, and logs](../screenshots/15-reader-allowed.png) · [secret and cross-namespace denials](../screenshots/16-reader-denied.png).

The exec, scale, and permission-query outputs are retained in private terminal records under `private/access-audit/`; they are not shown in those two screenshots. Permission queries are distinguished from attempted API operations in the table.

## Operational lesson

Test both the access an operator needs and the access they should not have. A successful login alone does not establish an appropriate permission boundary.

This was a targeted lab check of the reader identity. The provisioning identity's broader administrator access remains a separate limitation.
