# INC-004: Fargate profile mismatch

## Summary

An intentionally injected label mismatch prevented an application rollout from completing on the `eks-compute-lab-fargate` cluster.

The Deployment’s Pod template label was changed from `compute: lab` to `compute: unmatched`. The applications Fargate profile selects Pods in namespace `ops-lab` with the label `compute: lab`.

The rollout command timed out after 60 seconds. During the recorded observation window, the internal Service observer recorded **339 successful requests and 0 failed requests**.

Restoring `compute: lab` recovered the rollout.

This was a controlled lab exercise, not a production incident.

## Environment

| Component | Configuration |
|---|---|
| Cluster | `eks-compute-lab-fargate` |
| Namespace | `ops-lab` |
| Deployment | `inventory-status` |
| Desired replicas | 2 |
| Fargate profile | `applications` |
| Profile selector | Namespace `ops-lab`, label `compute: lab` |
| Rolling update settings | `maxUnavailable: 0`, `maxSurge: 1` |
| Observer | `service-observer`, requesting the internal Service’s `/readyz` endpoint |

## Fault injection

Applied the following patch:

```bash
kubectl patch deployment inventory-status -n ops-lab \
  --type=merge \
  -p '{"spec":{"template":{"metadata":{"labels":{"compute":"unmatched"}}}}}'
```

Kubernetes accepted the patch. The subsequent rollout check did not complete within its 60-second timeout:

```text
Waiting for deployment "inventory-status" rollout to finish:
1 out of 2 new replicas have been updated...
error: timed out waiting for the condition
```

This was a timeout of the rollout command’s wait period. It did not, by itself, establish a Service outage or trigger an automatic rollback.

## Retained evidence

### Fault injection and rollout

Screenshot `22-fargate-profile-mismatch.png` shows:

- The observer becoming Ready and returning an `OK` before fault injection.
- The accepted change to `compute: unmatched`.
- The rollout command timing out.

The screenshot does not show the application Pod status table or the individual readiness of the existing replicas during the fault.

### Scheduling event

A subsequent event query returned:

```text
Reason: FailedScheduling
Object: pod/inventory-status-8d85d58bc-27xpm

0/7 nodes are available: 7 node(s) had untolerated taint(s).
no new claims to deallocate, preemption: 0/7 nodes are available:
7 Preemption is not helpful for scheduling.
```

This event establishes that the named Pod could not be scheduled onto the seven nodes evaluated by the scheduler.

The message does not explicitly identify a Fargate profile mismatch. It is consistent with the scheduling problem investigated, but its exact timestamp was not retained alongside the incident timeline to conclusively correlate it with the fault window.

### Request observations

The saved observer log produced:

```text
Observed OK: 339
Observed FAIL: 0
```

No failed requests were recorded during that observation window. The sample count is not an exact duration or a production availability measurement.

## Cause and interpretation

The injected configuration error was a mismatch between the Deployment’s Pod template label and the applications Fargate profile selector:

```text
Required by profile: compute: lab
Injected Pod label:  compute: unmatched
```

New Pods carrying the modified label did not match that profile.

The configured rolling update settings were intended to preserve existing available replicas while a replacement was not ready. The successful observer requests are consistent with continued Service availability, although individual replica readiness during the fault was not retained.

The scheduling event was supporting evidence, not a direct statement of the profile configuration error.

## Recovery

Restored the expected Pod template label:

```bash
kubectl patch deployment inventory-status -n ops-lab \
  --type=merge \
  -p '{"spec":{"template":{"metadata":{"labels":{"compute":"lab"}}}}}'
```

Then checked rollout completion:

```bash
kubectl rollout status deployment/inventory-status \
  -n ops-lab --timeout=300s
```

The recovery checks were completed and captured in `23-fargate-profile-recovered.png`.

Observer logs were preserved before removing the temporary observer Pod.

## Prevention and operational improvements

- Review rendered Pod labels against the intended Fargate profile selectors before deployment.
- Add a configuration check that compares workload namespaces and labels with profile selectors; manifest validation alone does not establish scheduling eligibility.
- Monitor stalled rollouts separately from application request failures.
- Keep a documented procedure for restoring the previous Pod template.
- Capture Pod status, relevant events, and timestamps before recovery when practical.
- Export Kubernetes events when longer retention is needed for incident investigation.

## Lessons learned

A deployment can fail to progress while the existing application continues serving requests.

This exercise demonstrated the importance of checking both deployment progress and user-facing behavior. It also exposed an evidence-collection gap: the retained screenshot showed the rollout failure, but not the complete Pod scheduling state.

## Evidence files

- `22-fargate-profile-mismatch.png`
- `23-fargate-profile-recovered.png`
- Private observer log: `private/inc-004/observer-complete.log`
- Private request summary: `private/inc-004/request-summary.txt`

Raw private evidence is excluded from the public repository.
