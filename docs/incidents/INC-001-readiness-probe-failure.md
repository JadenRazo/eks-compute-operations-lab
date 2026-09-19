# INC-001: Readiness probe failure during rollout

## Summary

An intentionally injected readiness-probe fault affected a new Pod during an inventory-status rollout on the EC2-backed EKS cluster.

Kubernetes recorded an HTTP 404 readiness-probe failure. The saved observer snapshots contain no failed Service requests.

## Recorded timeline

All timestamps are UTC on September 12, 2026.

| Marker | Time |
|---|---|
| Fault injection recorded | 08:11:03 |
| Recovery verification recorded | 08:17:39 |

The interval between these markers was 6 minutes 36 seconds. This is an exercise interval, not a measured outage duration.

## Evidence

- The saved known-good Deployment revision was `2`.
- Events show creation and startup of a Pod in ReplicaSet `inventory-status-6c75c5cddd`.
- That Pod subsequently generated: `Readiness probe failed: HTTP probe failed with statuscode: 404`.

| Observer snapshot | OK | FAIL |
|---|---:|---:|
| Before recovery | 439 | 0 |
| After recovery | 660 | 0 |

These snapshots may overlap and must not be added together.

## Diagnosis

The new Pod started, but its readiness check failed. This distinguishes container startup from readiness to receive application traffic.

A failed readiness check makes a Pod unready; it does not by itself restart the container. Readiness is intended to control whether the Pod receives Service traffic. [Kubernetes probe documentation](https://kubernetes.io/docs/concepts/workloads/pods/probes/)

The successful observer requests are consistent with existing healthy replicas continuing to serve traffic while the new revision failed readiness.

## Recovery and outcome

A known-good revision was retained for recovery, and recovery verification was recorded at 08:17:39 UTC.

The retained excerpts do not contain the exact recovery command or a post-recovery Deployment status table. They support a readiness failure and no observed request failures in the saved observer snapshots, rather than an exact reconstruction of every recovery action.

## Improvements

- Test health-check paths before deploying a revision.
- Retain the fault patch, rollout status, recovery command, and final Deployment status.
- Record observer timestamps alongside injection and recovery markers.
- Validate application availability independently of rollout success.

## Evidence records

Private records are retained under `private/inc-001/`: the event snapshot, known-good revision, injection and recovery markers, and observer logs.

This was a controlled lab exercise. Successful sampled requests do not establish an availability guarantee.
