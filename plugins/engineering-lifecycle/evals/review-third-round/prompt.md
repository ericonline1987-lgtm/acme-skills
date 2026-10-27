---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

This is round three of review on my PR. In round one you flagged that get_orders built SQL with an f-string; in round two the same thing in get_invoices. Both are fixed now. Here is the diff since round two:

```diff
 def get_invoices(db, customer_id):
-    return db.execute(f"SELECT * FROM invoices WHERE customer_id = {customer_id}")
+    return db.execute("SELECT * FROM invoices WHERE customer_id = ?", (customer_id,))
+
+
+def get_refunds(db, customer_id, status):
+    return db.execute(
+        f"SELECT * FROM refunds WHERE customer_id = ? AND status = '{status}'",
+        (customer_id,),
+    )
```
