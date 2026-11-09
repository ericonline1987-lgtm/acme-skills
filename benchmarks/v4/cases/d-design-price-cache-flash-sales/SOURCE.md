# Sources

- AWS Builders' Library, Caching challenges and strategies — https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies
- Wikipedia, Cache stampede — https://en.wikipedia.org/wiki/Cache_stampede

## Grader basis

- key-dimensions: basic correctness check (cache key must cover every input of the computed value).
- checkout-authoritative: AWS caching (clients must tolerate eventual consistency; cached data necessarily grows inconsistent with the source) — so the charge path must not depend on it.
- flash-sale-freshness: AWS caching (TTL chosen by staleness tolerance and change rate); Wikipedia (external recomputation refreshes entries before expiry).
- stampede-protection: Wikipedia cache stampede (locking, external recomputation, probabilistic early expiration); AWS (request coalescing, soft/hard TTL, serving stale).
- cache-outage-fallback: AWS caching ("cache as a dependency": cold starts or cache fleet outage send a surge downstream; local cache fallback, load shedding, capping requests).

## Why a capable general model might miss it

"Put Redis in front with a TTL" sounds reasonable, so models tune the TTL rather than asking what breaks: wrong-price keys, stale prices at checkout, the synchronized miss at sale start, and the backend's inability to survive a cold cache.

The traffic and service figures are synthetic.
