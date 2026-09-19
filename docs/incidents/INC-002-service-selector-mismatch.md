# INC-002: Service selector mismatch

## Summary

This controlled exercise changed the inventory-status Service selector so that it no longer matched the intended application Pods.

The saved observer logs contain failed requests, demonstrating an application access problem during the exercise. Recovery verification was subsequently recorded.

## Recorded timeline

All timestamps are UTC on September 12, 2026.

| Marker | Time |
|---|---|
| Fault injection recorded | 08:21:29 |
| Recovery verification recorded | 08:25:23 |

The interval between these markers was 3 minutes 54 seconds. It includes the exercise and verification work; it is not a measured outage duration.

## Evidence

The saved original Service configuration contains:

- Type: `ClusterIP`
- Selector: `app: inventory-status`
- Target port: `http`

| Observer snapshot | OK | FAIL |
|---|---:|---:|
| Before recovery | 889 | 89 |
| After recovery | 933 | 91 |

These are whole-file counts. The snapshots may overlap and must not be summed. Failed-request counts cannot be converted directly into outage seconds.

## Diagnosis

A selector-based Service identifies its backend Pods through matching labels. An incorrect selector can break access through the Service even when application containers remain operational. [Kubernetes Service documentation](https://kubernetes.io/docs/concepts/services-networking/service/)

The baseline configuration identifies the intended selector. The retained excerpts do not include the faulty selector value or an EndpointSlice snapshot from the failure period.

## Recovery and verification

The recovery approach for this injected fault was to restore the intended Service selector and verify application access. A recovery-verification marker was recorded at 08:25:23 UTC.

The after-recovery file still contains failure entries. Since this is a saved log snapshot, those entries alone do not establish that failures continued after recovery. Timestamped request records are needed to identify the precise failure interval and last failed request.

## Improvements

- Review Service selectors and Pod labels together.
- Include an EndpointSlice check in the troubleshooting runbook.
- Test through the Service as well as checking Pod health.
- Retain the faulty configuration and the corrected configuration.
- Capture a bounded observation window with timestamps around recovery.

## Evidence records

Private records are retained under `private/inc-002/`: the original Service YAML, injection and recovery markers, and observer logs.

This report documents a controlled lab fault. It does not claim a precisely measured outage duration or production incident impact.
