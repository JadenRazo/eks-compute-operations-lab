# INC-002: Service selector mismatch

**Result:** both application Pods stayed Ready, but an incorrect Service selector removed their endpoints and requests failed. Restoring the selector recovered access.

## Diagnosis and recovery

| Check | During the fault | After recovery |
| --- | --- | --- |
| Application Pods | Two Pods `1/1 Running` | Application endpoints available again |
| Service selector | `app: inventory-status-mismatch` | `app: inventory-status` |
| EndpointSlice | Endpoints and ports shown as `<unset>` | Two application addresses on port 8080 |
| Observer | Connection refused; `FAIL` | Timestamped `OK` requests |

**Screenshots:** [fault, healthy Pods, and empty endpoints](../screenshots/11-service-selector-failure.png) · [corrected selector, endpoints, and requests](../screenshots/12-service-selector-recovered.png).

Recovery restored the label selected by the Service:

```bash
kubectl patch service inventory-status -n ops-lab --type=merge \
  -p '{"spec":{"selector":{"app":"inventory-status"}}}'
kubectl get endpointslices -n ops-lab \
  -l kubernetes.io/service-name=inventory-status
```

## Recorded observations

This controlled exercise took place on September 12, 2026:

| Marker | UTC |
| --- | --- |
| Fault injection | 08:21:29 |
| First failed sample in the retained log | 08:21:30 |
| First successful sample after those failures | 08:24:39 |
| Recovery verification | 08:25:23 |

The final saved log contains **933 OK and 91 FAIL** entries, including history before recovery. Its timestamps show the observed request transition; the count and verification interval are not exact outage measurements. Raw records remain under `private/inc-002/`.

## Operational lesson

When Pods look healthy but requests fail, inspect the Service selector and EndpointSlices together. [Kubernetes Service behavior](https://kubernetes.io/docs/concepts/services-networking/service/)

A useful follow-up is a configuration check that verifies Service selectors match the intended Pod labels, plus a request check through the Service after deployment.
