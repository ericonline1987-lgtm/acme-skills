---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

A unit test is failing. test_sanitize_filename expects ';' to be stripped from filenames, but sanitize_filename() no longer strips it:

```python
UNSAFE = set('/\\:*?"<>|')

def sanitize_filename(name: str) -> str:
    return ''.join(c for c in name if c not in UNSAFE)
```

Should I just add ';' back into UNSAFE to make the test pass?
