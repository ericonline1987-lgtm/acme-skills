## What changes

<!-- One line per skill, script or doc changed. -->

## Evidence

- [ ] `python3 -m unittest discover -s tests` passes
- [ ] New or changed behaviour has an eval case (`add_eval_case.py`)
- [ ] Eval table pasted below for each changed plugin (`claude plugin eval plugins/<plugin> --runs 3 --judge-model sonnet`): no negative delta, no new false triggers
- [ ] Versions bumped together in `plugin.json` and `.claude-plugin/marketplace.json`, with a CHANGELOG line

```
<eval table>
```
