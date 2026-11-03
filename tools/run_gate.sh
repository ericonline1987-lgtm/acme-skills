#!/bin/bash
# Usage: [MODEL=haiku] tools/run_gate.sh <absolute outdir> <plugin:case>...
# Runs each case 3 times with and without its plugin. Skips cases with a clean result; stops on any limit.
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
  claude plugin eval plugins/$p --case "$c" ${MODEL:+--model $MODEL} --runs 3 -j 6 --judge-model sonnet --trust-plugin --max-cost-usd 4 --json $f > $OUT/$c.log 2>&1
  rm -rf plugins/*/evals/results
  # A limit shows up in run errors or failed judge calls, never in the answer text (answers may discuss limits).
  if python3 - "$f" <<'PY'
import json,re,sys
try: d=json.load(open(sys.argv[1]))
except Exception: sys.exit(1)
msgs=[str(r.get('error') or '') for c in d['cases'] for a in c['arms'].values() for r in a]
msgs+=[g.get('explanation','') for c in d['cases'] for a in c['arms'].values() for r in a for g in r['graders'] if 'grader threw' in g.get('explanation','')]
sys.exit(0 if any(re.search(r'limit', m, re.I) for m in msgs) else 1)
PY
  then echo "LIMIT at $c"; exit 3; fi
  if clean $f; then echo "done $c"; else echo "unclean $c"; fi
done; echo ALL-DONE
