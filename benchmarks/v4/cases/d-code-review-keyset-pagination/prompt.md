---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

PR #2231 — "events API: switch to cursor pagination". Offset queries were timing out for big accounts past ~page 2000. Can you review?

Background: `events` is ~1.1B rows in Postgres 15. Rows are written by the ingest worker in batches of up to 500 per transaction with `created_at DEFAULT now()`. Existing index: `events_account_created_idx ON events (account_id, created_at)`. Public API, customers page through it with scripts.

```diff
--- a/api/events.py
+++ b/api/events.py
@@ -1,24 +1,38 @@
 from api.db import db
-from flask import request, jsonify
+from flask import request, jsonify
+from api.cursors import encode_cursor, decode_cursor
 
 
 @app.get("/v1/events")
 def list_events():
     account_id = g.account.id
-    page = int(request.args.get("page", 1))
     page_size = min(int(request.args.get("page_size", 100)), 500)
-    rows = db.fetch_all(
-        """
-        SELECT id, created_at, type, payload
-        FROM events
-        WHERE account_id = %s
-        ORDER BY created_at DESC
-        LIMIT %s OFFSET %s
-        """,
-        (account_id, page_size, (page - 1) * page_size),
-    )
-    return jsonify({"data": rows, "page": page})
+    cursor = request.args.get("cursor")
+
+    if cursor:
+        before = decode_cursor(cursor)  # -> datetime
+        rows = db.fetch_all(
+            """
+            SELECT id, created_at, type, payload
+            FROM events
+            WHERE account_id = %s AND created_at < %s
+            ORDER BY created_at DESC
+            LIMIT %s
+            """,
+            (account_id, before, page_size),
+        )
+    else:
+        rows = db.fetch_all(
+            """
+            SELECT id, created_at, type, payload
+            FROM events
+            WHERE account_id = %s
+            ORDER BY created_at DESC
+            LIMIT %s
+            """,
+            (account_id, page_size),
+        )
+
+    next_cursor = encode_cursor(rows[-1]["created_at"]) if rows else None
+    return jsonify({"data": rows, "next_cursor": next_cursor})
```

```diff
--- /dev/null
+++ b/api/cursors.py
@@ -0,0 +1,10 @@
+import base64
+from datetime import datetime
+
+
+def encode_cursor(ts: datetime) -> str:
+    return base64.urlsafe_b64encode(ts.isoformat().encode()).decode()
+
+
+def decode_cursor(cursor: str) -> datetime:
+    return datetime.fromisoformat(base64.urlsafe_b64decode(cursor).decode())
```
