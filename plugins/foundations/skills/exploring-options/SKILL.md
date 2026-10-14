---
name: exploring-options
description: Compare two or three real alternatives on the same fields, attack the favourite, and propose a small spike before committing. Use whenever someone asks what to use, which tool or approach to pick, "should we do X or Y", or how to solve something with several possible answers — even if they only ask for a recommendation.
---

# Exploring options

With AI, a rough alternative costs minutes. Committing early to the first idea is now
the expensive habit. Explore wide, then commit hard.

## Process

1. **Collect constraints into one table** before proposing anything: constraint, source
   (the person's words, code, policy, data), and what it rules out. When a new constraint
   arrives, add it here and re-derive; don't patch the current favourite.
2. **Generate genuinely different options.** At least two, usually three, including "do
   nothing" or "smallest change" when that is real. Options that differ only in detail
   count as one.
3. **Make them concrete cheaply.** Prefer evidence over argument: a spike, a prototype, a
   draft of each version, a quick measurement, a dry run on real inputs. Time-box each.
   Say which options were built and which were only reasoned about.
4. **Compare on the same fields**: what it achieves against the outcome, cost, risk, how
   it is undone, and the evidence for each cell, graded observed, inferred or unverified.
5. **Attack the favourite.** State the strongest case for the option you'd reject, the
   likeliest way your favourite fails once built, and what evidence would overturn it.
   Rule on each objection: adopted, rejected with evidence, or open with who decides.
6. **Get an independent challenge when reversal is hard.** If undoing the choice would
   not undo its effects (data rewritten, other teams acting, money spent), give a fresh
   reviewer only the constraints, options and evidence, and ask how the choice fails. A
   reviewer who saw the whole discussion is not independent; say so if none is available.
7. **Decide, or hand the decision over.** If the choice is the person's (see
   `defining-done`), present the comparison with a recommendation and stop. Otherwise
   decide, and record it with `../../shared/templates/decision-record.md` when others
   will later wonder why.

## Output

```
Constraints: <table>
Options:     <table: option | achieves | cost | risk | undo | evidence (graded)>
Challenge:   <objection → ruling>, one per line
Decision:    <choice, who decided, first step that proves the direction>
```

## Quality bar

- At least two options were compared on identical fields.
- At least one comparison cell rests on something observed, not only reasoned.
- The rejected option's best case is stated fairly.
- The first step is small and would reveal quickly if the direction is wrong.
