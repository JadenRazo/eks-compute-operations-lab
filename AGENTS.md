# Working on EKS Compute Operations Lab

Preserve and explain Kubernetes operations and Terraform adoption through
inspectable configuration and retained evidence. This independent lab records
sequential EC2 and Fargate exercises; both clusters, the NAT gateway and Elastic
IP were deleted. Documentation maintenance must not recreate them.

Read `README.md` for lifecycle and limits, then the relevant `docs/incidents/`
or `docs/audits/` report and its screenshot references. Infrastructure ownership
is in `docs/architecture/terraform-adoption.md`: `terraform/network/` and
`terraform/bootstrap/` own separate resources and state keys; eksctl owns cluster
provisioning. Kubernetes changes route through `kubernetes/base/`,
`kubernetes/fargate/` and the EC2 maintenance observer as applicable.

- Treat retained network/backend ownership as the documented baseline, not a
  newly verified AWS inventory. Recheck account, region, resource IDs and state
  ownership before any explicitly authorized reproduction or live change.
- Preserve separate network/bootstrap state and lock objects. The network
  backend's assumed role differs from bootstrap/provider authority. Bootstrap
  manages the bucket holding its own state; never destroy or migrate it as
  routine cleanup. Keep state, saved plans and raw inventories private.
- Preserve the limits: the provisioning role retained administrator access,
  state-version restoration was untested, and a no-change import plan proved
  only that root's managed attributes. Do not imply least privilege or tested
  recovery from those plans.
- Keep image pins, restricted workload identities, reader RBAC, health probes
  and disruption constraints meaningful. Rendering manifests does not prove
  scheduling, IAM denial or runtime recovery. Retain failure and recovery evidence.
- Cost targets were not measured spend; no performance or actual-cost comparison
  was completed. A new lab run needs an explicit budget, owned cleanup and
  preserved state/data boundaries. Do not replay incident commands for a doc edit.

Use `.github/workflows/validate.yml` for versions. In a complete checkout with
tools available, local validation is credential-free:

```sh
terraform fmt -check -recursive terraform
for root in terraform/network terraform/bootstrap; do
  terraform -chdir="$root" init -backend=false -input=false -lockfile=readonly
  terraform -chdir="$root" validate -no-color
done
kubectl kustomize kubernetes/base > /dev/null
kubectl kustomize kubernetes/fargate > /dev/null
```

Initialization may download providers. PR/push CI validates configuration only;
it does not deploy. For prose changes, review source links and evidence scope.
Use `docs/diagrams/README.md` before changing diagram sources or generated assets.

Lead docs and PRs with the observed result, cause and practical limit. Distinguish
screenshots, retained logs and summaries; sampled requests are not availability
guarantees. Link evidence rather than restating it. Use focused commits following
history, otherwise `type: concrete change` (preferably under 72 characters).
Report checks actually run, missing evidence, and actual push/PR effects.
