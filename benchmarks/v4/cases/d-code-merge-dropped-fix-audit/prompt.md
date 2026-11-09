---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

Tomasz merged release/2.14 back into main on Friday (9f3c2e1). QA says the session-timeout fix (PRJ-1187, a41b7d0) isn't on main — sessions still never hit the 12h absolute limit on the 2.15 build. But git says the commit IS on main?? 2.14.1 ships from release/2.14 so that's fine; it's main I care about. What happened, how do I get the fix onto main properly, and did anything else get lost?

```
$ git log --oneline --graph -8 main
*   9f3c2e1 (HEAD -> main, origin/main) Merge branch 'release/2.14' into main
|\
| * c77e019 (origin/release/2.14, release/2.14) Bump version to 2.14.1
| * a41b7d0 PRJ-1187: enforce absolute expiry for idle-refreshed sessions
| * 5be0d32 PRJ-1170: fix CSV export header order
* | 3d9a8f4 PRJ-1190: refactor session middleware into SessionManager
* | 81c0e5a PRJ-1185: audit log for admin logins
|/
* 0aa41f2 (tag: v2.14.0) Release 2.14.0

$ git branch -a --contains a41b7d0
* main
  release/2.14
  remotes/origin/main
  remotes/origin/release/2.14

$ git show --stat a41b7d0
commit a41b7d0e5c1f9a7d2b8e44f0c6a3d1e9b7f2a6c4
Author: Lena Park <lena@example.com>
Date:   Tue Nov 3 10:12:44 2026 +0100

    PRJ-1187: enforce absolute expiry for idle-refreshed sessions

 app/session/middleware.py | 12 ++++++++----
 tests/test_session.py     | 31 +++++++++++++++++++++++++++++++
 2 files changed, 39 insertions(+), 4 deletions(-)

$ git show a41b7d0 -- app/session/middleware.py
@@ -9,6 +9,7 @@ from app.session.store import SessionStore
 IDLE_TIMEOUT = timedelta(minutes=30)
+ABSOLUTE_TIMEOUT = timedelta(hours=12)
 
@@ -41,10 +42,13 @@ class SessionMiddleware:
         session = self.store.load(sid)
         now = utcnow()
-        if now - session.last_seen > IDLE_TIMEOUT:
+        if (now - session.last_seen > IDLE_TIMEOUT
+                or now - session.created_at > ABSOLUTE_TIMEOUT):
             return self._expire(session)
         session.last_seen = now
-        self.store.touch(session)
+        # PRJ-1187: idle refresh must never extend past the absolute lifetime
+        self.store.touch(session, max_expiry=session.created_at + ABSOLUTE_TIMEOUT)
         return session

$ git show --stat 3d9a8f4
commit 3d9a8f4...
    PRJ-1190: refactor session middleware into SessionManager

 app/session/manager.py       | 96 ++++++++++++++++++++++++++++
 app/session/middleware.py    | 71 ++++-----------------
 tests/session/test_manager.py | 118 ++++++++++++++++++++++++++++++++++
 tests/test_session.py        | 87 --------------------------
 4 files changed, 224 insertions(+), 148 deletions(-)

$ git show 9f3c2e1
commit 9f3c2e1b77d0a4e8c25f3196de0b4a1c8e7d5f20
Merge: 3d9a8f4 c77e019
Author: Tomasz Wrona <tomasz@example.com>
Date:   Fri Nov 6 17:42:10 2026 +0100

    Merge branch 'release/2.14' into main

$ git diff --stat 3d9a8f4 9f3c2e1
 app/export/csv.py | 6 +++---
 version.txt       | 2 +-
 2 files changed, 4 insertions(+), 4 deletions(-)

$ git grep -n "ABSOLUTE_TIMEOUT" main
$
```

Tomasz says he "had a couple of conflicts in the session stuff and kept main's version since main has the refactor".
