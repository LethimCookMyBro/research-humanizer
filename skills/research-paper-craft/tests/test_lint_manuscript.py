"""Tests use invented prose fixtures, never research observations."""
from pathlib import Path
import importlib.util
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lint_manuscript.py"
if SCRIPT.exists():
    spec = importlib.util.spec_from_file_location("lint_manuscript", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
else:
    module = None

class LintTests(unittest.TestCase):
    def test_implementation_exists(self):
        self.assertTrue(SCRIPT.exists(), "Manuscript style checker has not been implemented")

    def check_codes(self, text):
        if module is None:
            self.skipTest("Implementation does not exist yet")
        return [item["rule"] for item in module.lint_text(text)]

    def test_clean_prose(self):
        self.assertEqual(self.check_codes("The estimate is not available.\n"), [])

    def test_semicolon(self):
        self.assertIn("PUNCT_SEMICOLON", self.check_codes("The model ran; its output was saved."))

    def test_colon(self):
        self.assertIn("PUNCT_COLON", self.check_codes("The outcome is clear: evaluation is pending."))

    def test_keyword_label_only(self):
        self.assertEqual(self.check_codes("Keywords: sensing, estimation"), [])
        self.assertIn("PUNCT_COLON", self.check_codes("Keywords: sensing: estimation"))

    def test_contractions_and_possessives(self):
        self.assertIn("CONTRACTION", self.check_codes("The estimate isn't available."))
        self.assertIn("CONTRACTION", self.check_codes("We’ve inspected the file."))
        self.assertEqual(self.check_codes("The author's method is defined."), [])

    def test_dashes(self):
        self.assertIn("PUNCT_LONG_DASH", self.check_codes("A method — with a constraint — is described."))
        self.assertIn("PUNCT_LONG_DASH", self.check_codes("The range is A–B."))
        self.assertIn("PUNCT_DOUBLE_HYPHEN", self.check_codes("A -- provisional -- result."))
        self.assertEqual(self.check_codes("A real-time system is described."), [])

    def test_code_and_frontmatter(self):
        sample = "---\nname: draft\n---\n```python\nx = {'a': 1}; print(x)\n```\nUse `key: value` in the file."
        self.assertEqual(self.check_codes(sample), [])

    def test_multiline_equations(self):
        sample = "$$\nf(x):=x;\n$$\n\\[\na:=b;\n\\]\nText."
        self.assertEqual(self.check_codes(sample), [])

    def test_inline_equations(self):
        self.assertEqual(self.check_codes("Use $f(x):=x$ and \\(x:=y\\)."), [])

    def test_urls_and_link_labels(self):
        self.assertEqual(self.check_codes("See https://example.org/a?x=1;y=2 and [source](https://example.org)."), [])
        self.assertIn("PUNCT_COLON", self.check_codes("[Label: outcome](https://example.org)"))

    def test_references_then_appendix(self):
        sample = "## References\nA. Title: subtitle; year.\n## Appendix\nThe estimate isn't available."
        self.assertEqual(self.check_codes(sample), ["CONTRACTION"])

    def test_thai_references(self):
        self.assertEqual(self.check_codes("## เอกสารอ้างอิง\nA. Title: subtitle; year."), [])

    def test_numbered_references(self):
        self.assertEqual(self.check_codes("## 10. References\nA. Title: subtitle; year."), [])

    def test_placeholders(self):
        self.assertIn("DRAFT_PLACEHOLDER", self.check_codes("[RESULT UNVERIFIED]"))
        self.assertIn("DRAFT_PLACEHOLDER", self.check_codes("{{RESULT}}"))

    def test_html_comment_is_reported(self):
        self.assertIn("HIDDEN_COMMENT", self.check_codes("<!-- author note -->"))

    def test_blockquote_is_manual_review(self):
        self.assertEqual(self.check_codes("> Exact text isn't rewritten: preserve it."), ["QUOTATION_REVIEW"])

    def test_line_numbers(self):
        if module is None:
            self.skipTest("Implementation does not exist yet")
        self.assertEqual(module.lint_text("Clean.\nThe value isn't verified.")[0]["line"], 2)

if __name__ == "__main__":
    unittest.main()
