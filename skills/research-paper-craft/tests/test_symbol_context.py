"""Heuristic context checks. Numerical and mathematical source stays protected."""
from pathlib import Path
import importlib.util
import unittest
p=Path(__file__).resolve().parents[1]/'scripts/lint_manuscript.py'
s=importlib.util.spec_from_file_location('symbol_lint',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class SymbolContextTests(unittest.TestCase):
    def codes(self,text): return {x['rule'] for x in m.lint_text(text)}
    def test_greek_prose_is_reviewed(self):
        self.assertIn('SYMBOL_CONTEXT_REVIEW',self.codes('The β controls the response.'))
    def test_numeric_and_math_protected(self):
        for text in ('The value is 25 °C.', 'Use $\\beta$ in the equation.', '| β | Value |', 'The threshold is ≤ 5.'):
            self.assertNotIn('SYMBOL_CONTEXT_REVIEW',self.codes(text))
    def test_contribution_result_flagged(self):
        self.assertIn('CONTRIBUTION_RESULT',self.codes('## Contributions\n- The model achieves 95% accuracy.'))
    def test_structural_number_allowed(self):
        self.assertNotIn('CONTRIBUTION_RESULT',self.codes('## Contributions\n- We define 2 tasks.'))
    def test_contribution_section_ends(self):
        self.assertNotIn('CONTRIBUTION_RESULT',self.codes('## Contributions\n- A task model.\n## Results\nAccuracy was 95%.'))
if __name__=='__main__': unittest.main()
