---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Write pytest tests for this function:

```python
import re

def parse_duration(text: str) -> int:
    """Parse '1h30m', '45m', '2h' or '90s' into seconds."""
    match = re.fullmatch(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', text.strip())
    if not match or not any(match.groups()):
        raise ValueError(f'invalid duration: {text!r}')
    h, m, s = (int(g) if g else 0 for g in match.groups())
    return h * 3600 + m * 60 + s
```
