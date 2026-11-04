---
name: writing-for-people
description: Always use this skill when writing or rewriting anything a person will read — an email, post, memo, brief, status update, report, web or product copy, an explanation — or when asked to make text sound less like AI, more human or plainer, even a short one. Not for a one-line grammar fix or a translation. It writes from specifics, strips machine-written patterns and checks facts.
---

# Writing for people

Text works when the intended reader gets it on one read and doesn't wonder whether a
machine wrote it. Both failures have the same root: sentences that are generally true
of things like this instead of specifically true of this one.

## 1. Fix the reader and the job

Name who reads it, what they already know, and what they'll do after: decide, act,
look something up, understand, or simply hear the news. Note the register the
relationship calls for (a founder's post, a manager to their team, a bakery to its
neighbours) and, if the person has written in it before, match their voice, not a
generic one. One piece of writing has one job.

## 2. Pick the form, and open its entry

Find the form in `references/forms.md` and read its entry before drafting; it sets the
order and length budget. The ones that most often go wrong must open like this:

| Form | Must |
|---|---|
| Decision brief | Open with four lines: `Decision:` (what, who decides, by when; slots if unknown), `Recommendation:` (and the one or two reasons), `Would change if:`, `Ask:` (what they say yes or no to). Then options on the same fields, with the best case for each one you don't recommend. |
| Email or message | Subject states topic and ask. The ask is phrased as the small answer you want ("Can you confirm yes or no by Thursday?"), with a reply-by date or a `[reply-by date]` slot. In your note, a follow-up for each open item ("chase finance Tuesday if they haven't answered"). Bad news: two versions, with what each trades off. |
| Status update | The takeaway in two sentences; blockers with owner and date; only the actions the source gives. |
| Explanation for a non-expert | The answer in the first sentence. Then plain paragraphs in the order they'd ask: no headings, no bold, under 250 words. Explain every term at first use, everyday tech words too (phishing, provider, streaming), or leave it out. |
| Post or announcement | The news in the person's own voice in the first line; facts only they have. No "big news" formula, emoji or hashtags unless their own posts use them. |

Prose when ideas depend on each other; a list for steps or items someone will scan; a
table for values compared on the same fields. No headings on a 300-word piece.

## 3. Draft from specifics, and only from given ones

- Start with the fact, decision or ask. No preamble.
- Use what only this subject has: names, numbers, the detail a regular would mention.
  Test a sentence by swapping in a competitor's name; if it stays true, cut or replace
  it.
- **Never invent specifics to make prose vivid**: no sensory details, figures, history,
  quotes or anecdotes the person didn't give. Leave a visible slot (`[how long it keeps
  drinks cold]`) and ask for it. Case: plain drafts gave a bakery's conchas a "crackly
  shell" and a bottle "24 hours" of cold, neither of them given.
- A claim keeps its strength in every version you offer: "fell after" never becomes
  "cut" or "caused".
- Numbers, names, owners and dates keep the source's wording and scope. Don't add a
  year, a cause, a dependency or an action the source didn't state; a figure you work
  out (a difference, a total) is new and is labelled as yours. Unknowns are TBD.
- Grade load-bearing claims that aren't the person's own facts: cite the source, or mark
  them inferred or unverified. Anything that changes over time (prices, people, rules)
  is checked against a current primary source and dated.

## 4. Voice pass

Walk `references/voice.md` against the draft: generic and inflated content first, then
constructions (reflexive triads, "not X but Y", "Whether you… or…"), tell-words in
clusters, structure heavier than the content, and framing (announcing openers,
summaries, closing offers). Rewrite the sentence around a specific fact; swapping one
tell-word for a synonym leaves it as hollow. Then run
`python3 scripts/ai_tells.py <file>` for the countable tells (`--allow emoji,hashtags`
only where the person's own posts use them). A clean run is necessary, not sufficient.

## 5. Make it accessible

For readers outside the field, in a second language, or skimming, apply
`references/accessible.md`. For experts, don't translate their daily vocabulary.

## 6. Revise

Run the passes in `references/revision.md`: read it as the reader, a delete-only pass,
the voice pass, an accuracy pass beside the sources (`python3 scripts/claim_check.py`),
and mechanics (`python3 scripts/doc_check.py <file.md> --budget <words>`). When the
person flags one instance of a problem, fix the whole class in the document and say how
many you fixed.

## 7. Hand it over

The artifact contains only what the reader should see. Your notes to the person go
outside it, kept to what they must act on: slots to fill, facts you couldn't verify, a
decision only they can make. One question if it would change the draft; no menu of
alternatives beyond what the form calls for. Nothing is sent without their go-ahead.

## Quality bar

- The first two sentences carry the point.
- Every specific traces to the person's material or a cited source; the rest is a slot.
- No pattern from `references/voice.md` repeats across paragraphs.

## Not this skill

Slides, charts and pages: `making-visuals`. A design's technical content: `shaping-designs`.
