---
name: writing-for-people
description: Always use this skill when writing, rewriting or editing anything a person will read — an email, post, memo, brief, status update, report, web or product copy, an explanation — or when asked to make text sound less like AI, more human or plainer, even a short one. It writes from specifics for the actual reader, strips machine-written patterns and checks facts against sources.
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

## 2. Pick the form

Choose the form from `references/forms.md` by the reader's job, with its order and
length budget. Prose when ideas depend on each other; a list only for steps or
parallel items someone will scan; a table for values compared on the same fields.
Structure follows the content's size: no headings on a 300-word piece, no bold labels
on a paragraph's worth of ideas.

## 3. Draft from specifics, and only from given ones

- Start with the fact, decision or ask. No preamble about the text itself.
- Use what only this subject has: names, numbers, the detail a regular would mention.
  Test a sentence by swapping in a competitor's name; if it stays true, cut or replace
  it.
- **Never invent specifics to make prose vivid**: no sensory details, figures, history,
  quotes or anecdotes the person didn't give. Leave a visible slot (`[how long it keeps
  drinks cold]`) and ask for it. Case: an About page described a bakery's conchas as
  "soft and golden with a sweet, crackly shell", and a product page promised "ice-cold
  for up to 24 hours"; neither was given, and the figures were only admitted in a note
  after the text.
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
`references/accessible.md`: the reader's words, terms defined at first use, subject and
verb early, most sentences under 20 words, rates with their base, headings that state
conclusions. For expert readers, the opposite risk: don't translate their daily
vocabulary into plain speech.

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
alternative versions. Nothing is sent on the person's behalf without their go-ahead.

## Quality bar

- The first two sentences carry the point.
- Every specific traces to the person's material or a cited source; the rest is a slot.
- No paragraph has more than one pattern from `references/voice.md`, and no pattern
  repeats across paragraphs.
- Read aloud, it sounds like the person it's from, talking to the person it's for.

## Not this skill

Slides, charts, page layout and checking a rendered page belong to `making-visuals`; a
design doc's technical content belongs to `shaping-designs`, and its prose to this
skill.
