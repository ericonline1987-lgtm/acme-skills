"""The repository's own docs pass the claim check CI runs, so a failure shows before a push."""
import io
import unittest
from contextlib import redirect_stdout

from helpers import ROOT, load_module

claim_check = load_module(ROOT / "plugins/foundations/skills/tracing-claims/scripts/claim_check.py", "claim_check_docs")
DOCS = ["docs/PLAN.md", "docs/PLAN-v1.1.md", "docs/RUNTIMES.md", "README.md", "benchmarks/RESULTS.md", "benchmarks/README.md"]


class DocsClaimTests(unittest.TestCase):
    def test_docs_have_no_untraced_claims(self):
        for doc in DOCS:
            with self.subTest(doc=doc):
                out = io.StringIO()
                with redirect_stdout(out):
                    code = claim_check.main([str(ROOT / doc)])
                self.assertEqual(code, 0, out.getvalue()[-1500:])


if __name__ == "__main__":
    unittest.main()
