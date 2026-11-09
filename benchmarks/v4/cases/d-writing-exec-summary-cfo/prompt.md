---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

(Context for this exercise: no repository, files, browser or environment are available; everything you need is in this message.)

turn this into an exec summary for Gwen (CFO). ~150 words, she reads these on her phone. she has to decide by friday.

my notes:

DW renewal — notes (messy sorry)
- Snowflake contract ends Dec 31. renewal quote: 3-yr @ $1.18M/yr (we pay ~$940k/yr now). Kyle (their AE) said they "might" move on price, then didn't
- Kyle also offered 1-yr bridge at $1.02M if signed by Fri Nov 13. after that it's list
- if we sign the 3-yr we're locked in thru end of 2029
- BigQuery option: Lior's cost model says ~$760k/yr steady state. assumes ~70% of workload on committed slots (Enterprise edition), rest on-demand
- Lior built the model in March off Feb query volumes. query volume is up ~40% since then (feature store jobs + new finance dashboards)
- migration est: ~5 months, 2 data engs full time + ~$120k for a dbt partner
- dbt: 310 models, Anika thinks ~25% use Snowflake-specific SQL (QUALIFY, VARIANT, FLATTEN) -> rewrites
- InfoSec review for GCP data residency not started. 4-6 wks once kicked off
- data team really wants BQ (rest of stack is GCP / Vertex)
- Tableau licences also up for renewal, separate convo w/ IT, ignore
- Ravi out next week
- office move to 3rd floor 12/1, might disrupt data team??
- my rec: sign the 1-yr bridge. use the year to re-run Lior's model on current volumes, do the InfoSec review, pilot ~30 dbt models on BQ. decide on full migration by end of Q2.
