---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Please review this PR. slugify was leaving a leading or trailing hyphen when the text started or ended with punctuation or spaces ("  Hello, World! " became "-hello-world-"). This trims them.

```diff
 import re


 def slugify(text):
-    return re.sub(r"[^a-z0-9]+", "-", text.lower())
+    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


 def word_count(text):
     return len(text.split(" "))

+
+def test_slugify_trims_leading_and_trailing_separators():
+    assert slugify("  Hello, World! ") == "hello-world"
+
+
+def test_slugify_keeps_inner_separators():
+    assert slugify("a b-c") == "a-b-c"
```
