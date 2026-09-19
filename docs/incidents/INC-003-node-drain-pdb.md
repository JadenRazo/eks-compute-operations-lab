# INC-003: Node maintenance with a PodDisruptionBudget

**Result:** a PodDisruptionBudget temporarily rejected an eviction during a worker drain. The drain retried and completed; two replacement application Pods became Ready on the other worker, and the drained worker was uncordoned.

## What was checked

Both application replicas initially shared one worker. The observer was moved to the other worker before maintenance so it could continue checking the Service.

| Evidence | What it shows |
| --- | --- |
| [Budget inspection](../screenshots/13-maintenance-blocked.png) | A temporary `minAvailable: 2` setting allowed zero disruptions; requests were succeeding. |
| [Drain and recovery](../screenshots/14-maintenance-recovered.png) | An eviction was rejected, retried, then completed. Replacement Pods were Ready, the worker was uncordoned, and both nodes were Ready. |
| Final budget in the recovery screenshot | `minAvailable: 1` with one allowed disruption, matching the committed manifest. |

The screenshots do not show the command that changed the budget back to `1`. The completed drain demonstrates a temporary eviction constraint, not a permanently blocked operation or a PDB bypass.

## Recorded observations

The September 12, 2026 exercise has a baseline marker at **08:29:07 UTC** and recovery verification at **08:40:55 UTC**. That interval includes preparation and verification.

The observer log after relocation contains **339 OK and 0 FAIL** entries. Its previous history contains 91 failures from earlier observations; those cannot be attributed to maintenance from aggregate counts. Private records remain under `private/inc-003/`.

## Operational lesson

A PDB constrains voluntary eviction; it does not protect against every node failure. [Kubernetes disruption behavior](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

Both replacement replicas landed on the same worker. For future maintenance, verify spare capacity, replacement readiness, final node schedulability, and replica placement. A completed drain alone does not prove balanced placement or resilience to the remaining worker failing.
