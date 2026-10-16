---
name: Skill misfired or gave a weak result
about: A skill triggered when it shouldn't, didn't trigger when it should, or produced a poor answer
labels: eval-case
---

**Skill:** <!-- e.g. proving-outcomes -->

**What happened:** <!-- fired when it shouldn't / didn't fire / fired but the answer was wrong -->

**The prompt** (as you typed it, with anything private removed):

```
```

**What a good answer would have done** (one observable thing per line; these become eval criteria):

-
-

Fixes start by turning this into an eval case with `plugins/foundations/skills/capturing-learning/scripts/add_eval_case.py`, so the fix is measured.
