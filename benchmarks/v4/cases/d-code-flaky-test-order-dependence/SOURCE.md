# Sources

- Martin Fowler, Eradicating Non-Determinism in Tests — https://martinfowler.com/articles/nonDeterminism.html
- Google Testing Blog, Flaky Tests at Google and How We Mitigate Them — https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- Python documentation, functools (lru_cache, cache_clear) — https://docs.python.org/3/library/functools.html

## Grader basis

- root-cause-cache: Python functools (lru_cache keeps results until cleared; cache_clear()); Fowler (lack of isolation via static data/singletons changes another test's starting state).
- order-evidence-and-repro: Fowler (ordering dependence; make failures traceable); pytest-randomly prints the seed precisely so an order can be replayed (tool behaviour shown in the log).
- rejects-reruns: Google Testing Blog (reruns/quarantine can mask real bugs; dismissed failures erode trust); Fowler (a test that passes on rerun is still a problem).
- isolation-fix: Fowler (keep tests isolated rather than forcing an order; rebuild starting state per test).

## Why a capable general model might miss it

The obvious suspect — the test mutating RATES — is already undone by monkeypatch, so a model that doesn't trace the lru_cache will give a plausible but wrong diagnosis or settle for the rerun marker.

The code and CI logs are synthetic.
