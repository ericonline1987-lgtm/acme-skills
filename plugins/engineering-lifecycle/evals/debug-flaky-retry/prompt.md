---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, shell or web access is available. Answer by writing what was asked for, or by explaining exactly what you would do.)

This test fails about 1 run in 10 on CI but always passes on my laptop. I added a retry decorator and now CI is green. Can I merge?

```python
@retry(times=3)
def test_export_users():
    export_users()  # writes /tmp/users.csv
    rows = open('/tmp/users.csv').read().splitlines()
    assert rows[1].startswith('alice')
```
