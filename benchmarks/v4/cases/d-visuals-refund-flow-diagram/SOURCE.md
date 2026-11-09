# Sources

- C4 model, Notation — https://c4model.com/diagrams/notation
- Mermaid documentation, Sequence diagrams — https://mermaid.js.org/syntax/sequenceDiagram.html

## Grader basis

- async-boundary: Mermaid sequence-diagram async arrows (-) / --)) and activations; diagramming practice of showing where control returns (practitioner judgment).
- all-outcomes: Mermaid alt/else/loop blocks; faithful representation of each described branch.
- webhook-reconciliation: completeness against the supplied description; C4 guidance that each relationship carries a specific label (the condition).
- labelled-and-faithful: C4 notation ("be as specific as possible with the label", avoid "Uses"; unidirectional labelled lines).
- valid-mermaid: basic correctness check against Mermaid syntax.

## Why a capable general model might miss it

Models tend to render prose flows as happy-path flowcharts, collapsing failure branches and the separate reconciliation path, and blur the asynchronous boundary that is exactly what reviewers misread.

The flow is synthetic.
