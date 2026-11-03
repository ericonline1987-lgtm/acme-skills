#!/bin/bash
# Usage: tools/run_gate.sh <absolute outdir> <plugin:case>...   Skips cases with a clean result; stops on any limit.
OUT=$1; shift; mkdir -p $OUT; cd "$(dirname "$0")/.."
clean() { python3 - "$1" <<'PY'
import json,sys
try: d=json.load(open(sys.argv[1]))
except Exception: sys.exit(1)
bad=any(r.get('error') or any('grader threw' in g.get('explanation','') for g in r['graders']) for c in d['cases'] for a in c['arms'].values() for r in a)
sys.exit(1 if bad or not d['cases'] else 0)
PY
}
for pc in "$@"; do p=${pc%%:*}; c=${pc#*:}; f=$OUT/$c.json
  if clean $f; then echo "skip $c"; continue; fi
  claude plugin eval plugins/$p --case "$c" --runs 3 -j 6 --judge-model sonnet --trust-plugin --max-cost-usd 4 --json $f > $OUT/$c.log 2>&1
  rm -rf plugins/*/evals/results
  if grep -qiE "hit your .{0,20}limit|usage limit|rate limit" $f $OUT/$c.log 2>/dev/null; then echo "LIMIT at $c"; exit 3; fi
  if clean $f; then echo "done $c"; else echo "unclean $c"; fi
done; echo ALL-DONE
