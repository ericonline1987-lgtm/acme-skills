---
name: writing-documents
description: Draft or revise business documents — memos, reports, proposals, plans, status updates, one-pagers, how-tos — so the reader can decide or act correctly on a first read, in house style, within a page budget. Use when someone asks to write, restructure, shorten or improve a document meant for colleagues, leadership or clients.
---

# Writing documents

Follow `../../shared/style-guide.md` for voice, formatting and terminology.

A document succeeds when its reader does the right thing after reading it once. Write
for that action, then cut everything that doesn't serve it.

## Process

1. **Fix the reader and their job.** Who reads it, what they already know, and whether
   they must decide, do, look up or understand. One document, one job.
2. **Pick the skeleton and budget** from the table below, or from
   `references/skeletons.md` for design docs, READMEs, release notes, QA hand-off notes,
   agent instruction files (CLAUDE.md, AGENTS.md), notices and reference pages. The
   budget is a ceiling; detail beyond it goes to one appendix or linked page.
3. **Lead with the bottom line.** The first two sentences carry the conclusion, the ask,
   or the action. Don't describe the document or its audience.
4. **Write headings that summarise.** Read only the headings: they should tell the story.
5. **Use the right form.** A table for values compared on the same fields, a numbered
   list for steps, a diagram for flows and structures, a sentence for one fact. When the
   document has a figure, or is an HTML page or deck, read `references/figures-and-html.md`.
6. **Keep source truth.** Numbers, names, owners and dates use the source's wording;
   delivered and planned items are labelled; unknowns are TBD, never invented. Grade or
   cite load-bearing claims (see `tracing-claims` if installed).
7. **Cut to budget.** Delete every sentence whose removal loses no fact, every hedge
   that doesn't carry real uncertainty, and every summary of what was just said. Then run
   `python3 scripts/doc_check.py <file.md> --budget <words>` for the mechanical defects
   (slow opening, meta-commentary, long sentences, label headings, hedging, open
   placeholders), and report its count when you deliver.
8. **Run the fresh-reader test.** Hand the draft to someone (or a fresh agent) who
   hasn't seen your context, with only the reader's job: "decide whether to approve" or
   "follow these steps". Fix whatever they ask about or get wrong. Report that you ran it,
   or that you couldn't.

## Skeletons

| Document | Order | Budget |
|---|---|---|
| Decision memo | Recommendation and why now; options on the same fields; the ask | 1 page (use `briefing-decisions`) |
| Status update | Takeaway; blockers and risks; numbers with their basis; next actions with owner and date | 1 page |
| Proposal | Problem; proposed approach; cost and timeline; risks; ask | 2 pages |
| Report | Summary of findings; findings with evidence; implications; appendix | 2 pages + appendix |
| How-to / runbook | When to use it; prerequisites; numbered steps each with its check; rollback; done when | 12 steps |
| Incident review | Impact in one line; cause; what was done; what remains with owner and date | 1 page |
| Meeting notes | Decisions; actions with owner and date; open questions | 1 screen |
| One-pager | Bottom line; three supporting points with evidence; ask | 1 page |

One page is about 400–500 words.

## Quality bar

- The ask or conclusion is in the first two sentences.
- Every action has one owner and an absolute date.
- No section exists only to introduce another section.
