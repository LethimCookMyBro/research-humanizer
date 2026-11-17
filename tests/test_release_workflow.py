"""Release configuration contracts, not a claimed live publication."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReleaseWorkflowContracts(unittest.TestCase):
    def text(self):
        path = ROOT / '.github/workflows/release.yml'
        self.assertTrue(path.exists(), 'Release workflow has not been implemented')
        return path.read_text(encoding='utf-8')

    def test_main_only_and_no_pr_publishing(self):
        text = self.text()
        self.assertIn("github.ref == 'refs/heads/main'", text)
        self.assertIn("github.repository == 'LethimCookMyBro/research-humanizer'", text)
        self.assertNotIn('pull_request_target', text)
        self.assertIn('- VERSION', text)

    def test_tests_precede_release(self):
        text = self.text()
        for command in ('unittest discover -s tests', 'unittest discover -s skills/research-paper-craft/tests', 'audit_regressions.py'):
            self.assertLess(text.index(command), text.index('gh release create'))
        self.assertIn('contents: write', text)
        self.assertIn('persist-credentials: false', text)

    def test_preview_and_immutable_version(self):
        text = self.text()
        self.assertIn('--prerelease', text)
        self.assertIn('--target "$GITHUB_SHA"', text)
        self.assertIn('git archive', text)
        self.assertIn('sha256sum', text)
        self.assertNotIn('--clobber', text)
        self.assertIn('Existing tag does not match this commit', text)

    def test_notes_mark_runtime_limits(self):
        version = (ROOT / 'VERSION').read_text().strip()
        path = ROOT / f'docs/releases/v{version}.md'
        self.assertTrue(path.exists())
        text = path.read_text(encoding='utf-8')
        for term in ('Preview', 'ARS', 'CC BY-NC', 'not', 'Word', '2.3.0'):
            self.assertIn(term, text)

if __name__ == '__main__':
    unittest.main()
