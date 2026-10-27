---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Review this change. Our repo root CLAUDE.md includes the rule: "All money values are integers in cents. Never use float for currency."

```diff
 class LineItem:
-    def __init__(self, sku, unit_price_cents, qty):
-        self.unit_price_cents = unit_price_cents
+    def __init__(self, sku, unit_price, qty):
+        self.unit_price = float(unit_price)
         self.sku = sku
         self.qty = qty

     def total(self):
-        return self.unit_price_cents * self.qty
+        return self.unit_price * self.qty
```
