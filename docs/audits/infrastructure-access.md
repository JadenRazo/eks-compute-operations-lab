# EC2 infrastructure access

**Result:** the VPC CNI used a separate IAM role from the workers. Metadata requests from two ordinary application Pods timed out under the inspected IMDS restrictions. Provisioning access remained privileged.

## Identity boundaries reviewed

| Component | Finding |
| --- | --- |
| Worker role | Trusts `ec2.amazonaws.com`; has `AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryPullOnly`, and `AmazonSSMManagedInstanceCore`. No inline policies or permissions boundary. |
| VPC CNI | `kube-system/aws-node` uses a dedicated IRSA role with `AmazonEKS_CNI_Policy`; that policy is absent from the worker role. |
| CNI trust | Restricted to the current OIDC provider, subject `system:serviceaccount:kube-system:aws-node`, and audience `sts.amazonaws.com`. |
| Reader | EKS entry maps to `ops-lab-readers`; namespace permissions come from Kubernetes RBAC, with no associated EKS access policy. |
| Worker access entry | `EC2_LINUX`, associated with `system:nodes`. |
| OpsBox | Retains `AmazonEKSClusterAdminPolicy` for provisioning, recovery, and cleanup. |

Both CNI Pods were Ready with zero restarts. The separate CNI identity was already configured; this review did not migrate its permissions. The EKS service-linked role retained its service-managed policies.

## Metadata runtime checks

Both workers had IMDS enabled, required IMDSv2 tokens, and used a token-response hop limit of `1`.

Two application Pods on different workers sent direct IMDSv2 token requests, bypassing proxies and discarding response bodies. Both returned HTTP `000`, curl exit code `28`, and zero bytes after a four-second timeout. No node-role credentials were requested.

This is consistent with the inspected restrictions for those ordinary Pods. A timeout alone does not establish its cause or prove isolation for host-network or privileged workloads.

## Evidence and remaining checks

The [EC2 configuration](../../eksctl/ec2.yaml) records the intended settings. Role inventories, access entries, metadata settings, and runtime outputs remain under `private/infrastructure-audit/`; these audit outputs have no public screenshot in the current evidence set.

Next checks: justify worker Systems Manager access, capture CNI runtime STS identity, and review the OpsBox's broader AWS administrator permissions. This was a targeted lab review, not an account-wide security assessment.
