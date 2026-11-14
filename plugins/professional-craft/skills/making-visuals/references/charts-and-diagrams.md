# Charts and diagrams

Read this before making any chart, diagram or figure. If one plain sentence carries the
point, use the sentence: a figure that repeats a sentence is the same content twice, and
two or three numbers are clearer as large labelled figures than as a chart.

## Pick the form from the question

| The reader needs | Form |
|---|---|
| Exact values, or the same fields across items | A table |
| A ranking on one measure | Horizontal bars sorted by value, labelled directly |
| A number changing over time | A line; bars only for a few discrete periods |
| Parts of a whole | A stacked bar or a sorted bar of shares; a pie only for two or three parts |
| A relationship between two measures | A scatter |
| How values spread | A histogram or box plot |
| Many series over time | Small multiples on one shared scale, not one tangled chart |
| Named events in order | A timeline |
| Parties interacting over time | A sequence diagram |
| A process with branches | A flowchart |
| Components and their boundaries | A context or architecture diagram |
| Proof something happened | The real screenshot, record or output |

## Honest encoding

- Bars and areas start at zero; the visual length is the value. A line chart may zoom
  its axis, but label the axis and say so when the change looks larger than it is.
- One axis per chart. Two series with different units are two charts side by side.
- Use a log scale when ratios matter (growth rates, orders of magnitude), and label it.
- Compare like with like: the same period length, the same definition, the same base.
  When groups differ in mix, show them per segment too; an overall difference can
  reverse inside every segment.
- Rates carry their n. A bar for a group of four next to one for a group of four
  thousand needs the counts on it.
- When the person asks for a chart that "pops", make the point stand out honestly: a
  headline that states the change, the latest value highlighted, the comparison that
  makes it meaningful. Don't truncate or stretch the axis.

## Make it readable

- Title with the takeaway ("Refund requests doubled after the March change"), then the
  source and period in small type.
- Label series directly at the line end or on the bar; drop the legend when you can.
- Remove what carries no data: heavy gridlines, borders, backgrounds, 3D, shadows,
  redundant tick labels.
- Grey for context, one accent colour on what the title names. A palette that is
  distinguishable in greyscale and for colour-blind readers (avoid red against green as
  the only difference).
- Text in the figure at reading size for its medium; nothing smaller than the body
  text's footnotes.
- Put the figure where the text argues from it, and state its conclusion in the
  adjacent sentence. A figure no sentence refers to is decoration.

## Diagrams

- One question per diagram, at one level of detail, about 15 nodes at most. Split
  rather than crowd.
- An arrow claims sequence or cause; draw it only when that's true. Label arrows that
  carry different things (data, control, a request) or use visibly different strokes,
  with a key.
- Keep labels short. Auto-layout tools (Mermaid, Graphviz) render differently by
  environment and clip long labels.
- Lay the geometry out yourself (explicit coordinates in SVG) when elements must stay in
  place across states, when you show two states of one system, when containers nest,
  or when there are three or more kinds of connection. Auto-layout handles none of
  these reliably, and shortening labels doesn't fix it.
- A numbered procedure is already a sequence; don't add a flowchart that repeats it.
- For SVG, run `python3 scripts/validate_svg.py <file>`, then look at it: the script
  can't judge layout or legibility.

## Check it as the reader

Compare every plotted value, label and total against the source table before anything
else: a bar that doesn't match its row, a total that doesn't add up, or a period that
differs from the title is the error readers catch and remember.

Open the figure at its real viewing size and look: where the eye lands first, whether
every label is legible, whether anything overlaps or is cut, whether every colour and
line still means what the key says. Render-only defects are invisible in the source. If
you can't render it, say the figure is unchecked.
