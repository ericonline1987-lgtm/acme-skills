# Forms: what each kind of writing needs, in what order, at what length

Pick the form by the reader's job, then fill it from the material. A section the
material can't fill is dropped, not padded. The budget is a ceiling: detail beyond it
goes to an appendix or a link. One page is about 400 to 500 words.

## Decide or act

**Decision brief** (one page). A first block the decider can act on alone:

```
Decision: <what>, by <whom>, by <date>
Recommendation: <option>, because <the one or two reasons that decide it>
Would change if: <the evidence that would flip it>
Ask: <exactly what they say yes or no to, and what happens next either way>
```

Then the options on identical fields in one table, each cell with its basis (a source,
or observed, inferred, unverified), the best case for each option you don't recommend,
and what can and can't be undone. "Do nothing" and "decide later" are options when they
are real; say what waiting costs. Unknown figures are shown as unknown, never filled.

**Proposal** (two pages). Problem → proposed approach → cost and timeline → risks → ask.

**Status update** (one page). Takeaway in the first two sentences → blockers and risks,
each with its owner and date → numbers with their basis → next actions with owner and
date, only those the source gives. No actions given: no actions section.

**Incident review** (one page). Impact in one line (who, how many, how long) → what
happened, with times → cause and its evidence → what was done → what remains, each with
one owner and a date. Describe what the system allowed, not who slipped.

**Meeting notes** (one screen). Decisions → actions with owner and date → open
questions. Not a transcript.

## Messages

**Email or work message.** One outcome per message: a reply, a decision, an action by a
date, or awareness.

- Subject states topic and ask: "Decision needed by Fri: Q4 vendor".
- The first two lines carry the ask or the news. Context after, only what they need.
- Phrase the ask as the small answer you want ("Can you confirm yes or no by Thursday?",
  "Which of these two dates works?"), not "could you get back to me".
- Bad news, a decline or pushback: offer two versions, say what each trades off.
- Plan the follow-up for each open item: who to chase and when.
- Nothing commits the person to something they haven't agreed. Unknowns stay as bare
  slots (`[date]`), never a guessed value.

**Notice** (one paragraph). The change, who it affects and who it doesn't, and when.

**Announcement or social post.** Written in the person's voice, with the one fact or
story only they have, in the first line. Case: a seed announcement that opened
"Big news" and listed what the money would do (grow the team, deepen the product,
reach more clinics) read like every seed announcement that week; the founder's reason
for starting the company was the post. Use the platform's conventions only as far as
the person's own past posts do. If you don't have the fact or story, ask for it.

## Pages people land on

**About page.** Who is behind it, what they actually do, and one thing a regular would
tell a friend. Specific beats warm: names, years, the item people come back for. No
"passion", "family" or "quality" as claims; show them, or leave them out.

**Product description.** What it is and the two or three facts that decide a purchase
(size, what it's made of, what it does that others don't), each from the maker's
specs. Benefits only as consequences of a stated fact. No sensory adjectives the
product team didn't supply.

**Landing or feature copy.** A headline that says what the reader gets, in their words;
one line on how; proof (a number, a customer, a screenshot); one action.

## Explain

**Explanation for a non-expert.** The question they asked, answered in the first
sentence. Then the mechanism in plain words, with one comparison to something they
know, and the literal mechanism beside it. Then what it means for them. Prose in the
order they'd ask questions, no headings under 400 words, every term defined at first
use or avoided.

**How-to or runbook** (twelve steps). When to use it → prerequisites → numbered steps,
each with the check that it worked → how to roll back → what done looks like.

**Report** (two pages and an appendix). Findings first, each with its evidence and
confidence → what they imply → appendix for method and data.

**Research answer.** The answer to the question asked, with overall confidence, in two
sentences → findings, each with its evidence and confidence (high: several independent
primary sources; medium: one primary or several secondary; low: thin, old or
conflicting) → where sources disagree, and which is stronger → gaps → sources, each
with its date. Anything that changes over time is checked against a current primary
source and dated.

## Technical documents

**Design doc or RFC** (three pages; one for an incremental change). Context and scope →
goals and non-goals → design → alternatives with trade-offs → cross-cutting concerns
(security, privacy, cost, operations) → rollout and rollback → open questions with
owners.

**README** (one screen before the first link). What it is in one line → quick start
that works when pasted → one minimal example → links.

**Release notes** (one line per change). What changed for the user, breaking changes and
upgrade steps first. Internal refactors omitted.

**Hand-off note for QA or the next owner** (one page). What changed, by behaviour → what
a user can see → how it works, enough to derive test cases → what to test, in priority
order → what is not a defect → what must be prepared → what was already verified, and
how → who still has to confirm what → what to watch at rollout.

**Agent instruction file** (CLAUDE.md, AGENTS.md). Only what changes what the agent
does: commands, important paths, boundaries, and hard rules written as their executable
part ("Run `make test` before committing", not "we value quality"). Test each line: if
deleting it wouldn't change the agent's behaviour, delete it.

**Reference or API page.** Searchable headings; per item, the signature, a parameter
table, one example and its errors. No narrative.
