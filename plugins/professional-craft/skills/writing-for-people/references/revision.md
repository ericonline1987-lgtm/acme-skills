# Revision: the pass before you hand it over

Run this once a full draft exists. None of it applies while drafting.

## Passes, in order

1. **Read it as the reader**, at the speed they will, ideally aloud. Mark every place
   you stumble, re-read, or think "so what?".
2. **Delete-only pass.** Change nothing; only remove. Sentences that restate a
   neighbour, openers that announce, transitions that only signal structure,
   summaries of what was just said, hedges that carry no real doubt, and every line
   that serves the writer rather than the reader (disclaimers about how you're
   talking, boasts about your own restraint, housekeeping). A first draft usually
   loses a fifth to a third with nothing missed.
3. **Voice pass.** Walk `voice.md` and run `python3 scripts/ai_tells.py <file>`.
   Fix by rewriting the sentence around a specific fact, not by swapping words.
4. **Accuracy pass.** Put every number, name, date and quote beside its source and
   check it still says what the source said, with its scope. A check that each number
   still appears proves presence, not that it still describes the right thing.
   Run `python3 scripts/claim_check.py <file.md>` for figures and absolutes left
   without a source or grade.
5. **Mechanics.** `python3 scripts/doc_check.py <file.md> --budget <words>` for slow
   openings, label headings, long sentences, open placeholders and length.

## Reader tests

- **First screen.** Hide everything after the opening. Can the reader state the
  conclusion, the current state or the first safe action, and say where the detail is?
- **Lookup.** Ask one real question the document exists to answer. Can a reader reach
  it through headings and labels without reading every paragraph?
- **Doing.** For instructions: can the reader tell when to start, what to do, how to
  know it worked, how to recover, and when it's done?
- **Fresh reader.** When the stakes justify it, give the draft to someone (or a fresh
  agent) with only the reader's job, and fix what they ask or get wrong. Say whether
  you ran it. An author re-reading their own draft is not this test.

## Sweeps after any change

- **A flagged defect is a class.** When the person points at one hedge, one invented
  detail, one repeated number, find every instance in the document, fix them all, and
  say how many you fixed. Fixing only the cited one makes the reader your proofreader.
- **A repeated correction is a missing check.** The second time the person corrects the
  same kind of thing, add it to your own checklist for the rest of the work and report
  on it each round.
- **Recurring values.** Change a name, number, date or owner, then search for every
  other occurrence, and for counts and pointers that depended on it ("the three
  options", "see above").
- **Deleted antecedents.** Remove or rename something, then find the lines that
  referred to it; they now point at nothing.
- **Mirrors.** When the same content lives in two places (the draft and the email
  that sends it, an outline and its deck), change both in one pass.
- **Positional references.** Refer to sections by name ("see Costs"), not position
  ("the previous section"), while the structure can still move.

## When the feedback is about the whole thing

"It doesn't flow", "no focus", "reads like a list of points": stop patching the spots
cited. Read it front to back as a reader new to the subject, write down where they stall,
and re-outline from that list. Carry forward everything the person liked, unless you
replace it on purpose and say so.
