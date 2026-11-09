# Sources

- Python documentation, functools (lru_cache) — https://docs.python.org/3/library/functools.html
- AWS Builders' Library, Caching challenges and strategies (negative caching with a separate TTL; TTLs by staleness tolerance) — https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies

## Grader basis

- cached-none: Python functools (lru_cache stores results by arguments until they age out or the cache is cleared; a returned None is a result).
- rejects-default-rate: root-cause debugging practice — a fallback that changes money amounts silently converts a visible failure into a correctness bug (practitioner judgment).
- dont-cache-failures: Python functools (only returned values are stored; an exception propagates before anything is cached); AWS caching (cache error responses only with a separate, short TTL).
- successes-never-expire: AWS caching (cached data grows inconsistent with the source; choose TTL by change rate and staleness tolerance); lru_cache has no time-based expiry.

## Why a capable general model might miss it

The TypeError points straight at the multiplication, and the one-line None guard looks like a sensible defensive fix; seeing the memoised failure requires reading the decorator together with the log's one-warning-then-silence pattern.

The code and logs are synthetic.
