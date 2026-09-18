# INC-004: Fargate profile mismatch

## Scenario

A deployment changed its Pod template label from `compute: lab`
to `compute: unmatched`. The applications Fargate profile selects
Pods in namespace `ops-lab` with `compute: lab`.

This was an intentionally injected lab fault.

## Evidence

- Kubernetes accepted the Deployment patch.
- The rollout did not complete within the 60-second command timeout.
- New Pod status: [enter observed status].
- Existing replicas: [enter observed readiness].
- Scheduling event: [paste the relevant message, if emitted].
- Observer results: [OK count] successful requests and
  [FAIL count] failed requests during the recorded observation window.

Screenshots:
- 22-fargate-profile-mismatch.png
- 23-fargate-profile-recovered.png

## Cause

The modified Pod label did not match the applications Fargate
profile selector.

## Recovery

Restored `compute: lab` on the Deployment Pod template and verified
that the rollout completed and both application replicas were ready.

## Availability analysis

The Deployment used `maxUnavailable: 0` and `maxSurge: 1`.
These settings allowed the existing replicas to remain available
while the replacement could not become ready.

The request counts above describe the measured outcome.
The rollout command timeout itself did not indicate a Service outage.

## Prevention

- Review workload labels alongside Fargate profile selectors.
- Validate environment-specific rendered manifests before deployment.
- Check rollout completion and alert on stalled deployments.
- Retain a tested rollback procedure.

## Limitation

The observer sampled an internal Service endpoint. This exercise
did not measure external client availability or every possible request.
