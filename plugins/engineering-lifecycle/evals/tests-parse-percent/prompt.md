---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, shell or web access is available. Answer by writing what was asked for, or by explaining exactly what you would do.)

Write tests for this function:

```python
def parse_percent(s: str) -> float:
    return float(s.strip('%')) / 100
```
