---
name: analyzing-data
description: Always use this skill when someone wants numbers worked out from data — analyse this CSV or spreadsheet, what's the trend, compare groups, did this change work, chart it, answer a question from a table or a query — even a quick average. It checks the data before trusting it, computes rather than estimates, says what the numbers can't show and charts them honestly.
---

# Analyzing data

A number someone will act on must be computed, reproducible, and kept with its scope.

## 1. Pin the question

Write the question in one sentence, with the exact metric: its definition, unit,
period and population ("median order value in EUR, paid orders only, Q3, EU"). Ask what
decision it feeds; that decides how precise it needs to be.

## 2. Check the data before using it

- Count rows, list columns and types, the date range, missing values, duplicate keys
  and extreme values. Say what you found, even when it's nothing.
- Decide how to handle each problem and say so: duplicates removed or kept, missing
  values excluded or filled, outliers kept with a note.
- Reconcile a total against a known figure (an invoice, a dashboard, the source system)
  where one exists.
- Check row counts before and after every filter and join. A join that drops or
  duplicates rows changes every number after it, silently.

## 3. Compute, don't estimate

- Every figure comes from a calculation over the full data: code you ran where you can
  run code, otherwise arithmetic shown step by step. Never a figure read off a glance.
- Keep the script or query so someone can re-run it.
- Give counts with rates ("12 of 400, 3%"), and the size of every group. A change from
  2 to 4 is "doubled" and means nothing.
- Use the median and range for skewed data such as money and durations; a mean alone
  hides them.
- Compare like with like: the same definition, the same period length, the same season.
- When groups differ in mix (devices, regions, customer types), compare within each
  segment as well as overall. An overall difference can reverse inside every segment.

## 4. Say what the numbers can't show

- Something that happened after a change didn't necessarily happen because of it. Name
  what else changed at the same time (season, campaigns, pricing, a bug) and how one
  could separate the effect (a comparison group, more periods, a holdout).
- Name who is missing from the data: people who left, didn't respond, or whose events
  weren't logged.
- Grade each finding observed or inferred (see `tracing-claims` if installed).

## 5. Chart honestly

- Choose by question: a line for change over time, bars to compare categories, a scatter
  for a relationship, a table for exact values.
- Bars start at zero. Axes carry units. No dual axes, no 3D.
- The title states the finding ("Refunds doubled after the March change"), and the chart
  shows the comparison the title claims.

## Report

```
Answer: <the number, with its scope and n>
Method: <data and date range, filters, how problems were handled, script or query>
Findings: <finding — evidence — observed | inferred>
Can't show: <confounders, missing groups, small samples>
```
