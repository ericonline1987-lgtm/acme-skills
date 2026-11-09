# Sources

- Google SRE Workbook, Canarying Releases — https://sre.google/workbook/canarying-releases/
- Martin Fowler, ParallelChange — https://martinfowler.com/bliki/ParallelChange.html

## Grader basis

- validators-before-issuers: Fowler ParallelChange (expand: support old and new side by side before clients move; migrate; contract).
- rollback-after-issuance: ParallelChange (contract only once nothing uses the old version); SRE workbook (feature flags decouple feature launches from binary releases so a feature can be disabled without a new build).
- unbundle-changes: SRE workbook (components change at different rates; metrics must be attributable to the change; one canary at a time to avoid contamination; small self-contained artifacts make rollback cheaper).
- predefined-abort-criteria: SRE workbook (compare canary against control; SLI-based metrics; evaluation thresholds decided in advance; aggregate metrics hide canary problems).
- rate-limiter-shadow: SRE workbook (gradual stages, start with clear signals) applied to an enforcement feature; dark-launch/shadow practice (practitioner judgment).

## Why a capable general model might miss it

Generic rollout plans assume "rollback = redeploy previous version", which is unsafe once a new data format has been written to clients, and they rarely order deployments by consumer-before-producer across services.

The release contents and setup are synthetic.
