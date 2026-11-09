# Sources

- AWS Builders' Library, Timeouts, retries and backoff with jitter — https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
- Stripe API reference, Idempotent requests — https://docs.stripe.com/api/idempotent_requests

## Grader basis

- duplicate-charge: AWS (a timeout doesn't mean the operation failed; retry side-effecting calls only if the API is idempotent); Stripe (idempotency keys make retries safe after connection errors).
- stable-key: Stripe (the server uses the key to recognise subsequent retries of the same request; saved result returned for retries with the same key).
- retry-only-transient: AWS retry guidance (retrying non-transient failures adds load without benefit) and standard payments practice that declines are final (practitioner knowledge).
- timing-budget: AWS (exponential backoff, cap, jitter; limit attempts; timeouts sized against caller budgets; retry amplification across layers).

## Why a capable general model might miss it

The PR looks like routine resilience work; models often approve it with "add backoff" and miss that the key must be stable across attempts, or that the total retry time outlasts the caller's own timeout.

The code and provider are synthetic.
