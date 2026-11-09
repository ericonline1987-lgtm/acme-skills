# Sources

- Martin Fowler, SemanticConflict — https://martinfowler.com/bliki/SemanticConflict.html

## Grader basis

- keeps-main-rules: merge practice of preserving both sides' intent (tickets BILL-398 and BILL-412 describe main's intent); Fowler on assumptions each side makes.
- cap-in-same-currency: correctness of the combined rule once the feature changes units (practitioner judgment; units must match before comparison).
- semantic-conflict-callers: Fowler SemanticConflict (text merges cleanly but the program breaks; classic case is one side changing a signature while the other adds callers of the old one).
- verify-before-commit: Fowler (self-testing code catches semantic conflicts; integrate and test frequently).

## Why a capable general model might miss it

Models focus on the conflict markers they are shown, so they resolve the hunk and stop; the breaking file merged without conflict, and the discount cap's unit mismatch only appears when combining both sides' logic.

The code, tickets and git output are synthetic.
