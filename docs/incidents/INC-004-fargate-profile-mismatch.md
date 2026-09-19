# INC-004: Fargate profile mismatch

**Result:** changing the application Pod label stopped it matching the Fargate profile, and the rollout check timed out. Restoring the label completed the rollout and left two application Pods Ready.

## Fault and recovery

The `applications` profile selected namespace `ops-lab` with `compute: lab`. The injected Pod template used `compute: unmatched`.

| Evidence | Observed result |
| --- | --- |
| [Fault injection](../screenshots/22-fargate-profile-mismatch.png) | Label patch accepted; `rollout status --timeout=60s` timed out. |
| [Scheduling event](../screenshots/22b-fargate-scheduling-event.png) | `FailedScheduling`: the evaluated nodes had untolerated taints. |
| [Recovery](../screenshots/23-fargate-profile-recovered.png) | `compute: lab` restored; rollout completed; two Pods Ready; observer requests succeeded. |

The scheduling event supports a scheduling problem, but it does not name the profile mismatch. Its absolute timestamp was not retained alongside the fault window, so it is not conclusive evidence of that specific fault.

<details>
<summary>Fault and recovery commands</summary>

```bash
# Inject the mismatch in the controlled lab.
kubectl patch deployment inventory-status -n ops-lab --type=merge \
  -p '{"spec":{"template":{"metadata":{"labels":{"compute":"unmatched"}}}}}'
kubectl rollout status deployment/inventory-status -n ops-lab --timeout=60s

# Restore the label required by the profile.
kubectl patch deployment inventory-status -n ops-lab --type=merge \
  -p '{"spec":{"template":{"metadata":{"labels":{"compute":"lab"}}}}}'
kubectl rollout status deployment/inventory-status -n ops-lab --timeout=300s
```

</details>

## Request evidence and limits

The retained request summary records **339 OK and 0 FAIL**. Both observer log files in the local evidence archive are empty, so those totals cannot be independently recounted from them. The screenshots show successful requests before injection and after recovery; they do not provide a continuous traffic record during the fault.

The configured `maxUnavailable: 0` and `maxSurge: 1` were intended to preserve existing replicas during rollout. Individual replica readiness throughout the fault was not captured. The 60-second command timeout is not an outage duration or an automatic rollback.

## Operational lesson

Check that rendered workload namespaces and labels match a Fargate profile before deployment. Monitor rollout progress separately from Service requests, and capture Pod status and timestamped events before recovery.

This was a controlled lab exercise. The private summary is retained under `private/inc-004/`; no availability guarantee is inferred from it.
