---
name: tracing-claims
description: Keep figures, superlatives and claims traceable — attribute them, mark them observed, inferred or unverified, and never invent support. Use whenever turning notes, research or hearsay into text others will rely on — board or investor updates, reports, summaries, marketing copy — especially when numbers or "we're the best / fastest" claims appear.
---

# Tracing claims

Trust is cheaper than re-checking. A reader should be able to tell, for any sentence
that matters, where it came from and how solid it is.

## What counts as load-bearing

A claim is load-bearing if a decision, a number in another document, or someone's
action would change were it wrong. Typical forms: figures, comparisons, absolutes
("never", "guaranteed"), causal statements ("X caused Y"), and claims about what
someone said or decided.

## Process

1. **Grade each load-bearing claim** with one of:
   - **observed** — you saw it in a primary source (code, data, logs, the document
     itself, the person's own words). Say where.
   - **inferred** — reasoned from observed facts. Say from what.
   - **unverified** — reported by someone else, a search summary, another AI, or memory.
     Treat it as a lead and say so.
2. **Prefer primary sources.** A search snippet, a summary or "it's already done" is a
   lead to verify against the original, not a fact.
3. **Keep qualifiers attached.** A number keeps its scope (period, population,
   environment, sample) even when moved into a table or headline.
4. **Never fill gaps by invention.** Unknown names, owners, dates and figures are
   written TBD or left out.
5. **Cite in the reader's format**: links for web sources, file paths and line numbers
   for code, document and section for internal sources, "Sources:" list at the end
   for anything linkable.
6. **Run the checker** on Markdown output:
   `python3 scripts/claim_check.py <file.md>`. It flags figures and absolutes without
   a source or grade. Mark goals and examples `[target]` or `[example]` so they aren't
   mistaken for claims. It cannot tell whether a source supports the sentence; spot-check
   the important ones yourself.

## Quality bar

- Every figure in a headline or summary has a source or grade beside it.
- Nothing marked observed rests on a secondary summary.
- Conflicting sources are shown as a conflict, with your reading of which is stronger
  and why, rather than silently picking one.
