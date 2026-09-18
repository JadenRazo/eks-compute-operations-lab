Requirement: operators can inspect workloads and logs in ops-lab.

Implementation: dedicated IAM role -> EKS access entry -> ops-lab-readers group -> namespace RoleBinding and Role.

Test method: actual reader-role authentication through a separate kubeconfig.

Results: permissions and authorization appears scoped accordingly determined by testing various scenarios. 

| Test | Expected result |
|---|---|
| List application pods | Allowed |
| Read application logs | Allowed |
| List secrets | Forbidden |
| List `kube-system` pods | Forbidden |
| Execute a command in an application container | Forbidden |
| Attempt scaling using server dry-run | Forbidden; record the denied operation |
| Query permission to patch deployments | `no` |
| Query permission to patch deployment scale | `no` |

Screenshots: 15-reader-allowed && 16-reader-denied


