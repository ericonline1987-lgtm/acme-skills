# Voice: text that reads as a person wrote it

Read this on the voice pass, after the draft says the right things in the right order.
Each entry names a pattern, why readers take it as machine-written, and what to write
instead. The patterns come from the Wikipedia editors' field guide to AI writing and
from samples of this model's own default output; the cases quoted are real drafts.

No single pattern proves anything, and people use every one of them. What gives text
away is density and combination: three tells in a paragraph, the same construction in
every paragraph, structure that is more regular than the content. Fix the pattern, not
the word: swapping "crucial" for "vital" leaves the sentence exactly as hollow.

## 1. Content: the root problem

Most tells are symptoms of one fault: the text says what is generally true of things
like this, not what is specifically true of this one.

- **Generic sentences.** Test each sentence by swapping in a competitor's name. If it
  is still true ("we're passionate about quality", "built for everyday adventures"),
  it carries nothing. Replace it with a fact only this subject has, or delete it.
- **Invented specifics.** When facts are thin, the model fills the gap with plausible
  detail: sensory description, figures, history, quotes. Case: an About page described
  a family bakery's conchas as "soft and golden with a sweet, crackly shell", and a
  product description promised drinks "ice-cold for up to 24 hours"; neither fact was
  given, and the bottle's figures were only admitted in a note after the text. Leave a
  visible gap (`[how long it keeps drinks cold]`) and ask. A gap gets filled correctly;
  a plausible invention gets published.
- **Inflated importance.** "A pivotal moment", "a testament to", "plays a vital role",
  "leaves a lasting impact", "rich history". Say what happened and let the reader judge
  its weight. "We've baked here since 1987" beats "a rich legacy of baking excellence".
- **Significance tacked on.** A participle clause at the end of a sentence that claims
  meaning: ", highlighting the need for…", ", underscoring its commitment to…",
  ", reflecting a broader shift…". Either state the consequence as its own claim, with
  its basis, or cut it.
- **Vague authorities.** "Experts say", "studies show", "many believe", "industry
  observers". Name the source or drop the appeal.
- **Balance for its own sake.** A "Challenges" paragraph that opens "Despite its…" and
  ends in vague optimism, or a counterpoint added because a counterpoint is expected.
  Include a limitation when it is real and specific; then commit to a view.

## 2. Constructions

| Pattern | Example | Instead |
|---|---|---|
| Reflexive triads | "grow the team, deepen our product, and bring Fernhill to more clinics"; "durable, dependable, and designed to last" | Use the number of items the content has. Two is fine. One strong one is better than three soft ones. |
| Not X but Y, and its relatives | "It's not just a tool, it's a partner." "This isn't about speed. It's about trust." | State Y. The X was never claimed by anyone. |
| Whether you… or… | "Whether you stop by for a pan dulce or trust us with your wedding…" | Address the reader you actually have, once. |
| No more X, no more Y | "No more pointing, no more planning poker, no more…" | One sentence saying what stopped and why. |
| Outlines of negatives | A section of "It doesn't…" lines, or a sequence of short denials | Keep the one denial a reader would wrongly assume; fold it into the explanation. |
| Anaphora for warmth | "Thank you to… Thank you to… And thank you to…" | Thank people specifically, in one sentence each, or once. |
| Colon or dash reveal | "The result? Faster checkouts." "Here's the thing:" "One word: trust." | Say it plainly in the sentence. |
| False ranges | "from small startups to global enterprises", "from breakfast to late-night snacks" | Name who or what, or say "all sizes" if that is the claim. |
| Elegant variation | The bakery, then "the beloved establishment", then "this Tucson gem" | Repeat the plain name. Readers track identity by the word. |
| Stock closers | "…the tools vet clinics deserve", "…we'll treat you like family", "…and that makes all the difference" | End on the last fact or the ask. Endings can just stop. |

## 3. Words

Weak alone, strong in clusters. These rose sharply in text written after 2022 and read
as filler when used figuratively:

- **Verbs:** delve, underscore, highlight (as "this highlights"), showcase, foster,
  bolster, garner, leverage, elevate, empower, unlock, unleash, streamline, navigate
  (figuratively), embark, harness, spearhead, revolutionize.
- **Adjectives:** pivotal, crucial, vital, seamless, robust, cutting-edge, innovative,
  dynamic, vibrant, intricate, multifaceted, holistic, meticulous, comprehensive,
  transformative, ever-evolving, fast-paced, game-changing.
- **Nouns:** landscape, realm, tapestry, journey, testament, synergy, paradigm,
  interplay, ecosystem (outside biology and platforms), cornerstone, beacon.
- **Phrases:** "in today's [fast-paced/digital] world", "it's important to note",
  "it's worth noting", "plays a [vital/key] role", "stands as a testament", "at the
  heart of", "a wide range of", "when it comes to", "in the realm of", "nestled in".
- **Connectives used as rhythm:** Moreover, Furthermore, Additionally, Notably,
  Ultimately, In essence. In speech, people say "and", "also", "but", or nothing.

The replacement is usually a plain verb and a concrete noun: "leverage our network" is
"use our network", which raises the better question of how.

## 4. Shape and format

- **Structure heavier than the content.** Headings, bold labels and bullets on a
  piece that is one connected explanation. Case: an explanation of VPNs for a person's
  non-technical parents came back with six headings, bolded bullets and a "What a VPN
  does *not* do" section. Read aloud to the parents, it is a manual. Three short
  paragraphs, in the order they'd ask the questions, would have reached them.
- **Inline-header bullets.** "**Scrambles your traffic**: so people on the same…" for
  every item. Use plain bullets, or prose when items depend on each other.
- **Bold for emphasis everywhere.** Bold one thing a skimmer must not miss, or nothing.
- **Title Case Headings** and headings on a 200-word piece. Sentence case, and only
  when a reader needs to navigate.
- **Emoji and hashtags** outside the platforms and registers where the person's own
  posts use them. Case: a seed-round announcement opened "Big news: … 🌿" and closed
  with four hashtags; the founder's voice was gone before the second line.
- **Uniform rhythm.** Paragraphs of equal length, each opening with a topic sentence and
  closing with a restatement; sentences all 18 to 25 words. People vary: a short
  sentence after a long one, a one-line paragraph when it matters.
- **Symmetry.** Two sections with matching sub-structure, three bullets each, parallel
  openings. Real content is lumpy; let the form follow it.
- **Em dashes as the default punctuation.** Use a comma, a full stop or parentheses
  for most asides; keep the dash for a genuine break, rarely.

## 5. Framing around the text

- **Openers that announce.** "Great question!", "Certainly!", "Here's a draft:",
  "In this post, we'll explore…", "Let's dive in." Start with the content.
- **Summaries that repeat.** "In summary", "Overall", "In conclusion", or a last
  paragraph that restates the first. Cut it unless the piece is long enough to need it.
- **Offers and menus.** A closing list of alternatives ("I can also make a shorter
  version, a more casual one, or one with a personal story"). If one question would
  improve the draft, ask it in one line. Otherwise stop.
- **Hedges on everything.** "may potentially", "could help to", "it seems that". Keep
  the hedge that carries real uncertainty, once, where it applies.
- **Talking to an imagined reader.** "It's important to remember that…", safety and
  jurisdiction asides nobody asked for. Keep a caution the reader needs, stated as
  fact.
- **Notes inside the artifact.** Your reasoning, your sourcing caveats, your offers to
  revise: those go to the person in your reply, outside the text they will copy.

## 6. What human writing does instead

- Commits. It says what the writer thinks and why, and lets disagreement exist.
- Is specific. Names, numbers, places, the one detail only an insider would know.
- Chooses one example and tells it properly instead of listing three.
- Sounds like the register it's in: a founder's post sounds like that founder, a
  bakery's page like the people behind the counter, an email to a team like a manager
  who knows them.
- Uses contractions in anything conversational, and the plainest word that is exact.
- Stops when it's done.

## Rewrites

Seed announcement, opening.

> Before: Big news: Fernhill just raised a $4M seed round. 🌿 We're building
> scheduling software for veterinary clinics. Vet teams are some of the
> hardest-working people I know.

> After, with a fact the founder supplied: We raised $4M to fix scheduling for vet
> clinics. Last spring I spent a week
> at [clinic]'s front desk and watched them rebook the same dental cleaning three
> times because their calendar thinks every visit takes fifteen minutes.

The second version needs a fact the first didn't have. That is the point: ask for it,
or leave a bracket where it goes. Never write the anecdote yourself.

Product copy.

> Before: Stay hydrated in style with our stainless steel water bottle, built for
> everyday adventures. Durable, dependable, and designed to last.

> After, with the maker's specs: A 750 ml steel bottle that fits a car cup holder and
> survives a drop onto concrete. [Cold for N hours, from your test data.]

Bakery.

> Before: Whether you stop by for a pan dulce on your way to work or trust us with your
> wedding, we'll treat you like family.

> After, with two details the owners gave: Rosa still makes the conchas every morning
> at four. If you're ordering a wedding cake, come in and talk to Luis.
