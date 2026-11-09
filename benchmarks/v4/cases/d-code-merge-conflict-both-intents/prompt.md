---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Merging main into feature/multi-currency before I open the PR and got one conflict. Can you give me the resolved file and anything else I need to do before committing the merge?

```
$ git merge main
Auto-merging billing/invoice.py
CONFLICT (content): Merge conflict in billing/invoice.py
Auto-merging reports/daily.py
Auto-merging billing/__init__.py
Automatic merge failed; fix conflicts and then commit the result.

$ git status --short
UU billing/invoice.py
A  billing/credit_notes.py
M  billing/__init__.py
M  reports/daily.py
M  tests/test_invoice.py
```

Main's side of the conflict came from two tickets: BILL-398 (tax-exempt customers pay no tax) and BILL-412 (discount can't exceed subtotal — we had negative invoices). My branch adds per-currency prices, regional tax and returns `Money`; I already updated every caller of `calculate_total` that existed when I branched.

```python
# billing/invoice.py
from billing.money import Money, convert
from billing.tax import tax_rate_for

TAX_RATE = 0.0825

<<<<<<< HEAD
def calculate_total(order, currency):
    subtotal = sum(line.price_in(currency) * line.qty for line in order.lines)
    tax = round(subtotal * tax_rate_for(order.ship_to, currency))
    discount = convert(order.discount_cents, "USD", currency)
    return Money(subtotal + tax - discount, currency)
=======
def calculate_total(order):
    subtotal = sum(line.price_cents * line.qty for line in order.lines)
    if order.customer.is_tax_exempt:
        tax = 0
    else:
        tax = round(subtotal * TAX_RATE)
    discount = min(order.discount_cents, subtotal)  # BILL-412: never exceed subtotal
    return subtotal + tax - discount
>>>>>>> main
```

The new file from main, merged cleanly:

```python
# billing/credit_notes.py  (added on main in BILL-405)
from billing.invoice import calculate_total

def credit_note_amount(order, refund_lines):
    original = calculate_total(order)
    refunded = sum(l.price_cents * l.qty for l in refund_lines)
    return max(original - refunded, 0)
```

And what main brought into reports/daily.py, also merged cleanly:

```
$ git diff HEAD -- reports/daily.py
@@ -18,6 +18,10 @@ def daily_revenue(orders):
     revenue = sum(calculate_total(o, "USD").amount for o in orders)
     return revenue
+
+
+def daily_test_order_revenue(orders):
+    return sum(calculate_total(o) for o in orders if o.is_test)
```
