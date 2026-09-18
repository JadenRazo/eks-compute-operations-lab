# EC2 infrastructure access review

## Scope

Reviewed worker-node IAM permissions, VPC CNI identity, EKS access entries, and EC2 instance metadata access for the EKS compute operations lab.

This was a targeted lab review, not a comprehensive AWS account security assessment.

## Verified findings

### Worker-node role

The worker role trusts `ec2.amazonaws.com` and has these managed policies:

- `AmazonEKSWorkerNodePolicy`
- `AmazonEC2ContainerRegistryPullOnly`
- `AmazonSSMManagedInstanceCore`

No inline policies or permissions boundary were configured. The VPC CNI policy was not attached to the worker role.

The operational need for Systems Manager access remains a review item. Absence of a permissions boundary does not itself imply administrator access.

### VPC CNI identity

The `kube-system/aws-node` service account references a dedicated IRSA role.

Its trust policy requires:

- The current cluster’s OIDC provider.
- Subject `system:serviceaccount:kube-system:aws-node`.
- Audience `sts.amazonaws.com`.

The role has `AmazonEKS_CNI_Policy` attached and no inline policies. Both CNI Pods were fully Ready with zero restarts during inspection.

This separation was already configured; no CNI permission migration was performed.

### Cluster access

The reader role maps to `ops-lab-readers` and has no associated EKS access policies. Its application permissions are supplied through Kubernetes RBAC.

The worker role has an `EC2_LINUX` access entry associated with `system:nodes`.

The OpsBox provisioning role retains cluster-wide `AmazonEKSClusterAdminPolicy` access for setup, recovery, and cleanup. This is a documented privileged-access exception.

The EKS service-linked role has service-managed access policies and was retained.

### Instance metadata protection

Both running workers had these settings applied:

- IMDS endpoint enabled.
- IMDSv2 tokens required.
- Token response hop limit set to 1.

Runtime checks were performed from two application Pods on different workers. Neither Pod enabled host networking.

Each test sent an IMDSv2 token request directly to the metadata endpoint, bypassed proxies, discarded the response body, and used a four-second timeout.

Both tests returned:

- HTTP code `000`, indicating no HTTP response.
- Curl exit code `28`.
- Zero bytes received before timeout.

These observations are consistent with the intended metadata restriction for the tested ordinary Pods. No node-role credentials were requested.

## Limitations and remaining considerations

- The runtime checks do not establish isolation for host-network or privileged workloads.
- A timeout alone does not identify the cause; interpretation also uses the verified EC2 metadata settings.
- The OpsBox’s broader AWS IAM permissions were not comprehensively audited.
- CNI trust and permissions were inspected, but its runtime STS identity was not separately captured.
- Administrator access remains available to the provisioning identity.

## Evidence

Raw evidence is retained privately under `private/infrastructure-audit/`, including role inventories, access entries, Pod placement, metadata settings, and runtime test output.
