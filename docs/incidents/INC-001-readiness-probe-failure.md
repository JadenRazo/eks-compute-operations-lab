# INC-001: Readiness failure during rollout

**Result:** the new Pod failed readiness while the existing replicas remained Ready and sampled Service requests succeeded. Rolling back restored the working revision.

## Diagnosis and recovery

| Step | Observed evidence |
| --- | --- |
| Inspect the rollout | New ReplicaSet: one Pod, zero Ready. Previous ReplicaSet: two Pods, both Ready. |
| Check warnings and traffic | HTTP 404 from the readiness probe; the observer continued recording `OK` requests. |
| Roll back | `rollout undo` succeeded; rollout completion, `/readyz`, and two Ready application Pods were verified. |

**Screenshots:** [failed readiness and continuing requests](../screenshots/09-release-diagnosis.png) · [rollback and recovery checks](../screenshots/10-release-recovered.png).

The saved known-good revision was `2`. Recovery used:

```bash
kubectl rollout undo deployment/inventory-status -n ops-lab --to-revision=2
kubectl rollout status deployment/inventory-status -n ops-lab --timeout=180s
```

## Recorded observations

The controlled exercise ran on September 12, 2026. Injection was recorded at **08:11:03 UTC** and recovery verification at **08:17:39 UTC**. That interval includes diagnosis and verification; it is not an outage measurement.

| Retained observer snapshot | OK | FAIL |
| --- | ---: | ---: |
| Before recovery | 439 | 0 |
| After recovery | 660 | 0 |

The snapshots overlap and must not be added. Full logs remain private under `private/inc-001/`. The exact faulty probe path is not retained; the event records its HTTP 404 response.

## Operational lesson

A Pod can start successfully and still be unready for traffic. Check both rollout progress and Service requests; neither alone describes the whole incident. [Kubernetes probe behavior](https://kubernetes.io/docs/concepts/workloads/pods/probes/)

For the next run, capture the fault patch and test health paths before rollout. After an emergency rollback, reconcile the declarative configuration before applying it again.
