# Release gate results

`tools/run_gate.sh` runs every eval case three times with and without its plugin and writes one raw JSON per case to a folder you name (raw runs are not committed: they hold full answers). The summaries kept here are what RESULTS.md cites.

| File | What it is |
|---|---|
| `2026-11-02-summary.json` | v2.0 gate: per-case scores with and without the plugin for all 69 cases, which skill each case tests, and the Haiku re-runs |
| `2026-11-02-pass1.json` | The first pass of that gate, before fixes: per-criterion pass counts, kept as the record of what the fixes changed |

Re-run the whole gate, or a few cases:

```
tools/run_gate.sh "$PWD/benchmarks/gate/runs" foundations:plan-launch-order engineering-lifecycle:debug-checkout-500s
MODEL=haiku tools/run_gate.sh "$PWD/benchmarks/gate/runs-haiku" professional-craft:email-vendor-chaser
```

A case with a clean result in the folder is skipped, and the run stops at the first usage limit (read from run errors and judge errors, never from answer text), so the same command resumes after a reset.
