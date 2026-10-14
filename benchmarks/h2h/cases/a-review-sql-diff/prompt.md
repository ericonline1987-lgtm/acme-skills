---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Please review this pull request. It's meant to let admins look up orders by customer email.

```diff
+@app.get('/admin/orders')
+def orders_by_email(request):
+    email = request.args.get('email')
+    rows = db.execute(f"SELECT * FROM orders WHERE email = '{email}'")
+    return jsonify([dict(r) for r in rows])
```
