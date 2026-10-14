# Figures, HTML pages and decks

Read this when the document carries a chart, diagram, screenshot, recording or table,
or when the output is an HTML page or a deck.

## Pick the form from the content's shape

If one plain sentence carries the point, use the sentence; a figure that repeats a
sentence is the same content twice.

| The reader needs | Form |
|---|---|
| One conclusion, or one or two numbers | A sentence, or one large labelled number with its basis |
| Exact values, or the same fields across items | A table |
| Options compared on the same fields | An aligned comparison table |
| A ranking on one measure | Bars sorted by value, labelled directly |
| Named events over time | A timeline |
| A number changing over time | A line chart |
| Parties interacting over time | A sequence diagram |
| A branching process or decision path | A flowchart |
| A hierarchy | A tree (not a mind map) |
| Parts of a whole | A stacked bar |
| The spread of many values | A histogram |
| Components and their boundaries | A context or architecture diagram |
| Proof that something happened | The real screenshot, record or output |

## Rules for every figure

- Title it with its takeaway ("Scan latency blocks every upload worker"), and state its
  data source and period.
- Under it, write only what the figure can't show: the conclusion, the mechanism behind
  one arrow, or a caveat. Don't narrate the boxes in order.
- An arrow claims sequence or cause; a plus sign claims arithmetic. Draw one only when the
  data proves it. Keep metrics that can't be compared visibly separate.
- One question per diagram, at one level of detail, at most about 15 nodes. Split rather
  than crowd.
- A numbered procedure is already a sequence; don't add a flowchart that repeats it.
  Add a figure only for a branch the steps can't show, or a screenshot of a state the
  reader must recognise.
- Don't chart two or three numbers. Large labelled figures with their basis are clearer.

## Render for the medium

| Medium | Use |
|---|---|
| Markdown on a code host | Mermaid or the project's diagram format beside the text; static images; GIFs |
| HTML page | Authored SVG or HTML layout (not a pasted auto-layout render); video and click-to-open detail allowed, each with a static fallback |
| Slides | The deck tool's native shapes; one claim per slide as the headline, the proving visual beneath |

## Turning screen recordings into demo material

Trim to the moments that prove the point, speed up waiting, add a caption with the
takeaway per segment, and keep the raw recording as evidence elsewhere. A long
unedited recording is not a demo.

## HTML pages and decks: check before handing over

- Open it as the reader will (same browser class, file or URL). Check the console for
  errors.
- Body text readable at 200% zoom; no horizontal scrolling at 320px width; contrast at
  least 4.5:1 for body text and 3:1 for large text and chart marks.
- Every fixed-size frame (slide, card) at its real size: nothing overflows or is clipped.
- Projected decks: check at true full screen in the venue's aspect ratio.
- Interactive parts work by keyboard; focus is visible and never trapped.
- When the same content exists in two forms (a script and its rendered deck, a doc and
  its page), change both and confirm they still match.

Use `verifying-interfaces` (engineering-lifecycle) for the full browser check when it is
installed.
