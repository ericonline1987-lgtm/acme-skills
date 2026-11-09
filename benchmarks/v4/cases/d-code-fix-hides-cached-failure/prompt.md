---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

We've had bursts of TypeErrors from checkout totals in prod this week. Sam opened a one-line fix (below). OK to merge?

```python
# pricing/fx.py
import logging
from functools import lru_cache

import requests

log = logging.getLogger(__name__)
FX_URL = "https://fx.internal"

@lru_cache(maxsize=256)
def get_rate(base: str, quote: str) -> float | None:
    try:
        r = requests.get(f"{FX_URL}/rates", params={"base": base, "quote": quote}, timeout=2)
        r.raise_for_status()
        return float(r.json()["rate"])
    except requests.RequestException as e:
        log.warning("fx lookup failed %s/%s: %s", base, quote, e)
        return None
```

```python
# checkout/totals.py
from pricing.fx import get_rate

def to_display_currency(amount_cents: int, base: str, quote: str) -> int:
    rate = get_rate(base, quote)
    return round(amount_cents * rate)
```

Sam's PR:
```diff
 def to_display_currency(amount_cents: int, base: str, quote: str) -> int:
-    rate = get_rate(base, quote)
+    rate = get_rate(base, quote) or 1.0
     return round(amount_cents * rate)
```

Logs (filtered to pricing.fx + checkout.totals):
```
2026-11-06T09:14:02Z pod=checkout-7c9f WARN  pricing.fx fx lookup failed USD/EUR: HTTPSConnectionPool(host='fx.internal', port=443): Read timed out. (read timeout=2)
2026-11-06T09:14:02Z pod=checkout-7c9f ERROR checkout.totals TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
2026-11-06T09:14:09Z pod=checkout-7c9f ERROR checkout.totals TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
2026-11-06T09:14:31Z pod=checkout-7c9f ERROR checkout.totals TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
... 409 more ERROR lines on checkout-7c9f, all USD/EUR carts, no further WARN lines ...
2026-11-06T11:52:40Z pod=checkout-7c9f INFO  shutdown: deploy checkout v2.31.4
2026-11-06T13:30:11Z pod=checkout-2a1d WARN  pricing.fx fx lookup failed USD/GBP: HTTPSConnectionPool(host='fx.internal', port=443): Read timed out. (read timeout=2)
2026-11-06T13:30:11Z pod=checkout-2a1d ERROR checkout.totals TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
... errors continue on checkout-2a1d for USD/GBP carts only; the other 11 pods show no errors ...
```
