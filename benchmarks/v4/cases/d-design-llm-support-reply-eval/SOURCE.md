# Sources

- Hamel Husain, Your AI Product Needs Evals — https://hamel.dev/blog/posts/evals/
- Claude documentation, Define success criteria and build evaluations — https://platform.claude.com/docs/en/test-and-evaluate/develop-tests
- Shankar et al., Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences (arXiv:2404.12272) — https://arxiv.org/abs/2404.12272

## Grader basis

- stratified-set: Claude docs (task-specific evals mirroring real distribution; include edge cases); Hamel (synthetic/curated cases for scenarios production hasn't surfaced). Expected count: 0.5% × 200 = 1 abuse ticket.
- judge-validated: Hamel (iterate the judge until it matches human labels; measure precision and recall); Shankar et al. (validate the validators); Claude docs (test LLM-grader reliability first).
- specific-criteria-not-similarity: Hamel (binary pass/fail labels; look at data; track specific errors); Claude docs (detailed rubrics with automatic-fail conditions; multidimensional evaluation).
- gate-not-mean: Claude docs (multidimensional criteria each with its own threshold); Hamel (track specific error prevalence). Statistical noise at n=200 is general practice.
- online-signal: Hamel (A/B testing and production traces once the product is used by real users).

## Why a capable general model might miss it

Models critique the plan's sample size and suggest "a better rubric", but usually keep the similarity-to-reference framing and an average-score gate, and seldom insist on calibrating the judge against humans or oversampling rare high-risk categories.

The dataset description is synthetic.
