# INC-003: Node maintenance with a PodDisruptionBudget

## Summary

This maintenance exercise drained an EC2 worker hosting both inventory-status replicas.

During the drain, Kubernetes temporarily rejected an application Pod eviction because it would violate the PodDisruptionBudget. The drain retried and completed. A later snapshot shows two replacement application Pods Ready on the other worker.

## Recorded timeline

All timestamps are UTC on September 12, 2026.

| Marker | Time |
|---|---|
| Baseline recorded | 08:29:07 |
| Recovery verification recorded | 08:40:55 |

The interval between these markers was 11 minutes 48 seconds. It includes preparation and verification, not just the drain operation.

## Baseline

- Two inventory-status Pods were `1/1 Running` on the worker in private subnet A.
- The observer was initially on that same worker.
- The application PDB had `minAvailable: 1` and one allowed disruption.
- The observer was moved to the other worker for the maintenance exercise.

Co-locating both application replicas on one node made controlled eviction and replacement readiness especially relevant.

## Drain evidence

The saved drain log shows:

1. The target node was cordoned.
2. DaemonSet-managed Pods were ignored.
3. Application and metrics-server Pod evictions were attempted.
4. An application eviction was rejected with: `Cannot evict pod as it would violate the pod's disruption budget.`
5. The command retried, both application Pods were evicted, and the node was reported drained.

This demonstrates a temporary eviction constraint followed by successful completion. The saved log does not establish a permanently blocked drain or a need to bypass the PDB.

PDBs constrain voluntary disruptions through the eviction mechanism. They do not guarantee availability during involuntary node failures. [Kubernetes disruption documentation](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

## Outcome

The post-maintenance snapshot shows:

- Two replacement inventory-status Pods, both `1/1 Running`, on the other worker.
- A replacement metrics-server Pod running on that worker.
- The observer running on that worker.

The post-maintenance observer file contains **339 OK and 0 FAIL** entries.

The pre-move file contains **1262 OK and 91 FAIL** entries from its existing history. Those failures are not attributable to this maintenance exercise from the aggregate counts alone. The observer histories should not be combined.

## Limitations and improvements

The saved excerpts do not include a final node schedulability check, so they do not establish whether the drained node was subsequently uncordoned.

Both replacement application Pods were on one worker after maintenance. Successful draining therefore did not establish balanced placement or resilience to that worker failing.

For a future run:

- Verify spare capacity and replacement readiness before maintenance.
- Place the observer outside the node being drained.
- Capture node schedulability before and after the operation.
- Review replica placement after maintenance.
- Preserve timestamped observer logs for the exact maintenance window.

## Evidence records

Private records are retained under `private/inc-003/`: baseline and recovery markers, PDB and Pod snapshots, the completed drain log, and observer logs.
