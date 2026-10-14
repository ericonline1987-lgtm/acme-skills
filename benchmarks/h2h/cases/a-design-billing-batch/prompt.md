---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Design how we should move our nightly billing job to something more reliable. Today it's a single cron job on one VM that runs for about 4 hours and charges roughly 40,000 customers each night.
