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
