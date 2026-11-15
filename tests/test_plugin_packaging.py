"""Offline packaging contracts, not live Claude Code or Codex integration tests."""
import hashlib
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = "research-humanizer"
SKILL = "research-paper-craft"
REPOSITORY = "LethimCookMyBro/research-humanizer"


class PluginPackagingTests(unittest.TestCase):
    def read_json(self, relative_path):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"Missing plugin metadata: {relative_path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIsInstance(data, dict)
        return data

    def test_claude_manifest(self):
        manifest = self.read_json(".claude-plugin/plugin.json")
        self.assertEqual(manifest["name"], PLUGIN)
        self.assertEqual(manifest["license"], "MIT")
        self.assertEqual(manifest["repository"], f"https://github.com/{REPOSITORY}")
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(manifest["skills"], "./skills/")

    def test_codex_manifest(self):
        manifest = self.read_json(".codex-plugin/plugin.json")
        self.assertEqual(manifest["name"], PLUGIN)
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertEqual(manifest["interface"]["displayName"], "Research Humanizer")
        self.assertEqual(manifest["license"], "MIT")

    def test_manifests_agree_on_shared_package(self):
        claude = self.read_json(".claude-plugin/plugin.json")
        codex = self.read_json(".codex-plugin/plugin.json")
        for field in ("name", "version", "skills", "repository", "license"):
            self.assertEqual(claude[field], codex[field], field)

    def test_claude_marketplace(self):
        catalog = self.read_json(".claude-plugin/marketplace.json")
        self.assertEqual(catalog["name"], PLUGIN)
        self.assertEqual(catalog["owner"]["name"], "LethimCookMyBro")
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        self.assertEqual(entry["name"], PLUGIN)
        self.assertEqual(entry["source"], "./")
        self.assertEqual((ROOT / entry["source"]).resolve(), ROOT)

    def test_codex_marketplace(self):
        catalog = self.read_json(".agents/plugins/marketplace.json")
        self.assertEqual(catalog["name"], PLUGIN)
        self.assertEqual(len(catalog["plugins"]), 1)
        entry = catalog["plugins"][0]
        self.assertEqual(entry["name"], PLUGIN)
        self.assertEqual(entry["source"], {"source": "local", "path": "./"})
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(entry["category"], "Productivity")

    def test_payload_remains_self_contained(self):
        for relative in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            manifest = self.read_json(relative)
            skills = (ROOT / manifest["skills"]).resolve()
            self.assertTrue(skills.is_relative_to(ROOT))
            self.assertTrue((skills / SKILL / "SKILL.md").is_file())
            self.assertTrue((skills / SKILL / "references/writing.th.md").is_file())
            self.assertTrue((skills / SKILL / "references/writing.en.md").is_file())
            self.assertTrue((skills / SKILL / "licenses/humanizer-MIT.txt").is_file())
            for key in ("hooks", "mcpServers", "apps"):
                self.assertNotIn(key, manifest, "This is a skills-only package")

    def test_both_readmes_have_native_install_commands(self):
        commands = (
            f"/plugin marketplace add {REPOSITORY}",
            f"/plugin install {PLUGIN}@{PLUGIN}",
            f"codex plugin marketplace add {REPOSITORY}",
            f"codex plugin add {PLUGIN}@{PLUGIN}",
            f"/{PLUGIN}:{SKILL}",
            "/plugins",
        )
        for filename in ("README.md", "README(TH).md"):
            content = (ROOT / filename).read_text(encoding="utf-8")
            for command in commands:
                with self.subTest(file=filename, command=command):
                    self.assertIn(command, content)

    def test_no_install_placeholders_or_invented_codex_install_verb(self):
        for filename in ("README.md", "README(TH).md", "docs/PUBLISHING.md"):
            content = (ROOT / filename).read_text(encoding="utf-8")
            self.assertNotIn("YOUR_USERNAME", content, filename)
            self.assertNotIn("codex plugin install ", content, filename)
            self.assertNotIn("/plugin add ", content, filename)

    def test_bilingual_shell_blocks_match(self):
        def blocks(filename):
            text = (ROOT / filename).read_text(encoding="utf-8")
            return re.findall(r"```(?:bash|powershell)\n(.*?)\n```", text, re.S)
        self.assertEqual(blocks("README.md"), blocks("README(TH).md"))

    def test_readme_relative_links_resolve(self):
        for filename in ("README.md", "README(TH).md"):
            content = (ROOT / filename).read_text(encoding="utf-8")
            targets = re.findall(r"\]\(([^\s)]+)\)", content)
            targets += re.findall(r'href="([^"]+)"', content)
            for target in targets:
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                with self.subTest(file=filename, link=target):
                    self.assertTrue((ROOT / unquote(urlsplit(target).path)).exists())

    def test_existing_skill_checksums(self):
        root = ROOT / "skills" / SKILL
        for line in (root / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            digest, relative = line.split(maxsplit=1)
            path = root / relative.lstrip("*")
            with self.subTest(file=relative):
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
