---
name: writing-for-people
description: Always use this skill whenever someone needs anything a person will read — an email or reply (a decline, a chaser, bad news), a post, a memo, summary or one-pager, a recommendation written up for a boss, a status or investor update, web or product copy, an explanation — or to make any text sound like a person, not AI. It writes from specifics, checks every fact, and gets the reader to act.
---

# Writing for people

Text works when the intended reader gets it on one read, does what it needs them to do,
and never wonders whether a machine wrote it. Both failures have the same root:
sentences generally true of things like this instead of specifically true of this one.

Paths to `scripts/` and `references/` are relative to this skill's folder.

## 1. Fix the reader and the job

Decide what this reader should know, feel or do after one read; that is the bar. If
the person has written to this reader before, match their voice,
not a generic one.

## 2. Pick the form, and open its entry

Read the form's entry in `references/forms.md` before drafting. The ones that most
often go wrong must open like this:

| Form | Must |
|---|---|
| Decision brief | Open with four lines: `Decision:` (what, who decides, by when; slots if unknown), `Recommendation:` (and the one or two reasons), `Would change if:`, `Ask:` (what they say yes or no to). Then options on the same fields, with the best case for each one you don't recommend. |
| Email or message | Subject states topic and ask. The ask is phrased as the small answer you want ("Can you confirm yes or no by Thursday?"), with a reply-by date or a `[reply-by date]` slot. In your note, a follow-up for each open item ("chase finance Tuesday if they haven't answered"). Bad news: two versions, with what each trades off. |
| Chat reply (Slack, DM, text) | Readable in one glance on a phone (about 100 words), because a long reply to someone upset reads as defensive. Own the specific thing, say what you'll do and by when, end on one clear question if you need one. Apologise once. No "I hear you", "thank you for sharing" or other HR register. |
| Status update | The takeaway in two sentences; blockers with owner and date; only the actions the source gives. |
| Explanation for a non-expert | The answer in the first sentence. Then plain paragraphs in the order they'd ask: no headings, no bold, under 250 words. Explain every term at first use, everyday tech words too (phishing, provider, streaming), or leave it out. |
| Post or announcement | The news in the person's own voice in the first line; facts only they have. No "big news" formula, emoji or hashtags unless their own posts use them. |

Prose for ideas that depend on each other, a list for steps to scan, a table for values
compared on the same fields; no headings on a 300-word piece.

## 3. Draft from specifics, and only from given ones

- Use what only this subject has: names, numbers, the detail a regular would mention.
  Swap in a competitor's name: if a sentence stays true, cut or replace it.
- **Never invent specifics to make prose vivid**: no sensory details, figures, history,
  quotes or anecdotes the person didn't give. Leave a visible slot (`[how long it keeps
  drinks cold]`) and ask for it.
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
summaries, closing offers). Rewrite the sentence around a specific fact; a synonym
leaves it as hollow. Then run
`python3 scripts/ai_tells.py <file>` for the countable tells (`--allow emoji,hashtags`
only where the person's own posts use them). A clean run is necessary, not sufficient.

## 5. Make it accessible

For readers outside the field, in a second language, or skimming, apply
`references/accessible.md`. For experts, keep their daily vocabulary; translating it talks down to them.

## 6. Revise

Run the passes in `references/revision.md`: read it as the reader, a delete-only pass,
the voice pass, an accuracy pass beside the sources (`python3 scripts/claim_check.py`),
and mechanics (`python3 scripts/doc_check.py <file.md> --budget <words>`). When the
person flags one instance of a problem, fix the whole class in the document and say how
many you fixed.

## 7. Hand it over

The artifact contains only what the reader should see. Your notes to the person go
outside it, kept to what they must act on: slots to fill, facts you couldn't verify, a
decision only they can make. Deliver your best complete draft now rather than a menu of
options, and ask one question if its answer would change the draft. Nothing is sent
without their go-ahead.

Last, reread it as the reader and make the change that would make it the best version:
their next question answered in advance, the detail only they have, a sentence cut.

## Works with

`making-visuals` for slides, charts and pages; `shaping-designs` for a design's
technical content.
