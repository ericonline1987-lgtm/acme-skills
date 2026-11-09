---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

`test_invoice_totals` fails on CI maybe 1 run in 5. Always passes locally (`pytest tests/test_invoice.py`). I'm going to slap `@pytest.mark.flaky(reruns=3)` on it unless you see something. Relevant code + last three CI runs below.

```python
# billing/tax_rates.py
from decimal import Decimal
from functools import lru_cache

RATES = {"DE": Decimal("0.19"), "FR": Decimal("0.20"), "NL": Decimal("0.21")}

@lru_cache(maxsize=None)
def rate_for(country: str) -> Decimal:
    return RATES[country]
```

```python
# billing/invoice.py
from decimal import Decimal, ROUND_HALF_UP
from billing.tax_rates import rate_for

def build_invoice(lines, country):
    net = sum(qty * price for _, qty, price in lines)
    gross = (net * (1 + rate_for(country))).quantize(Decimal("0.01"), ROUND_HALF_UP)
    return Invoice(lines=lines, net=net, total=gross)
```

```python
# tests/test_invoice.py
def test_invoice_totals():
    inv = build_invoice(lines=[("Widget", 3, Decimal("19.99"))], country="DE")
    assert inv.total == Decimal("71.36")
```

```python
# tests/test_tax.py (excerpt)
def test_rate_override(monkeypatch):
    tax_rates.rate_for.cache_clear()
    monkeypatch.setitem(tax_rates.RATES, "DE", Decimal("0.20"))
    assert tax_rates.rate_for("DE") == Decimal("0.20")
```

CI run #4471 (failed)
```
============================= test session starts ==============================
platform linux -- Python 3.12.4, pytest-8.2.2, pluggy-1.5.0
Using --randomly-seed=2841907731
rootdir: /builds/billing
plugins: randomly-3.15.0, rerunfailures-14.0, cov-5.0.0
collected 412 items

tests/test_currency.py ..............                                    [  3%]
tests/test_tax.py ........................                               [  9%]
tests/test_pdf.py .........................................              [ 19%]
tests/test_invoice.py ....F.......                                       [ 22%]
tests/test_api.py ...................................................... [ 35%]
...
=================================== FAILURES ===================================
_____________________________ test_invoice_totals ______________________________

    def test_invoice_totals():
        inv = build_invoice(lines=[("Widget", 3, Decimal("19.99"))], country="DE")
>       assert inv.total == Decimal("71.36")
E       AssertionError: assert Decimal('71.96') == Decimal('71.36')

tests/test_invoice.py:4: AssertionError
=========================== short test summary info ============================
FAILED tests/test_invoice.py::test_invoice_totals - AssertionError: assert Decimal('71.96') == Decimal('71.36')
======================== 1 failed, 411 passed in 48.12s ========================
```

CI run #4474 (passed)
```
Using --randomly-seed=1730022514
...
tests/test_api.py ...................................................... [ 13%]
tests/test_invoice.py ............                                       [ 16%]
tests/test_currency.py ..............                                    [ 19%]
tests/test_pdf.py .........................................              [ 29%]
tests/test_tax.py ........................                               [ 35%]
...
============================ 412 passed in 47.55s =============================
```

CI run #4479 (failed)
```
Using --randomly-seed=99102211
...
tests/test_tax.py ........................                               [  5%]
tests/test_api.py ...................................................... [ 18%]
tests/test_invoice.py .......F....                                       [ 21%]
...
E       AssertionError: assert Decimal('71.96') == Decimal('71.36')
======================== 1 failed, 411 passed in 49.03s ========================
```
