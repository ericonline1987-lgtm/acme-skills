# v4 comparison

Method and decision rules: [docs/PLAN-v4.md](../../docs/PLAN-v4.md). Cases: `cases/` (pool D), split into dev and test by `split.json`.

```
# 1. Build the arms (decoys from github.com/anthropics/skills, reference from ly87ing/agent-skills)
python3 benchmarks/v4/build_arms.py --ref-skills REF/skills --decoys ANTHROPIC/skills \
    --cases benchmarks/v4/cases --out ARMS

# 2. Run each arm; --keep-temp keeps the traces the pairwise judge reads
for a in base acme ref; do
  claude plugin eval ARMS/$a --ablation none --runs 3 -j 4 --model sonnet --judge-model sonnet \
      --keep-temp --trust-plugin --no-publish --threshold 0 --json RUNS/$a.json
done

# 3. Judge pairs blind, both orders, two judges (resumable)
python3 benchmarks/v4/pairwise.py --arm base=RUNS/base.json --arm acme=RUNS/acme.json \
    --arm ref=RUNS/ref.json --cases benchmarks/v4/cases --names ARMS/skill_names.json \
    --judge opus --judge sonnet --out RUNS/pairs.jsonl

# 4. Score as pre-registered
python3 benchmarks/v4/stats.py --arm base=RUNS/base.json --arm acme=RUNS/acme.json \
    --arm ref=RUNS/ref.json --pairs RUNS/pairs.jsonl --split benchmarks/v4/split.json
```

Runs that stop at a usage limit or error are discarded and rerun before step 3.

Record the effort level with every result (`stats.py --effort`, `pairwise.py --judge-effort`): on recent models it moves quality and cost a lot (Anthropic reports Opus 5.5 at medium matching Opus 5 at high). `claude plugin eval` has no effort flag, so answers run at each model's default (medium on Opus 5.5); v4 rounds 1 to 3 all ran at the default. Spot-check a result at a higher effort before relying on it.
