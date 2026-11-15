"""Targeted audit regressions for v2.0, separate from the bundled tests.

Usage: python -B audit_regressions.py /path/to/research-paper-craft
These are synthetic text fixtures, not observations from a research study.
"""
from pathlib import Path
import importlib.util
import sys
import unittest

if len(sys.argv) != 2:
    raise SystemExit('Usage: python -B audit_regressions.py SKILL_DIRECTORY')
root = Path(sys.argv.pop()).resolve()
script = root / 'scripts' / 'lint_manuscript.py'
if not script.is_file():
    raise SystemExit(f'Missing checker: {script}')
spec = importlib.util.spec_from_file_location('audited_checker', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class AuditRegressions(unittest.TestCase):
    def codes(self, text):
        return {item['rule'] for item in module.lint_text(text)}

    def test_unambiguous_heres_contraction(self):
        self.assertIn('CONTRACTION', self.codes("Here's the result."))

    def test_unresolved_marker_inside_inline_math(self):
        self.assertIn('DRAFT_PLACEHOLDER', self.codes('Result $[RESULT UNVERIFIED]$.'))

    def test_unresolved_marker_inside_inline_code(self):
        self.assertIn('DRAFT_PLACEHOLDER', self.codes('Result `[RESULT UNVERIFIED]`.'))

    def test_unclosed_frontmatter_is_not_silently_clean(self):
        self.assertTrue(module.lint_text("---\nThe model isn't ready; its source is unknown."),
                        'Malformed protected regions should trigger review, not return a clean report.')

    def test_unclosed_display_math_is_not_silently_clean(self):
        self.assertTrue(module.lint_text("$$\nx = 1\nThe model isn't ready; its source is unknown."),
                        'Malformed protected regions should trigger review, not return a clean report.')

if __name__ == '__main__':
    unittest.main(verbosity=2)
