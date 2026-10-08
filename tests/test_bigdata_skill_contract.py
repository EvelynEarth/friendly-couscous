"""Paper-first Big Data Skill regression and authority-isolation checks."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


validator = load("validate_bigdata_skill", ROOT / "scripts/validate_bigdata_skill.py")
indexer = load("generate_bigdata_indexes", ROOT / "scripts/generate_indexes.py")


class BigDataContractTests(unittest.TestCase):
    def test_current_entrypoint_manifest_links_all_valid(self):
        self.assertEqual(validator.check(ROOT), [])

    def test_hsk_contracts_not_in_active_index(self):
        files = set(indexer.iter_files(ROOT))
        self.assertIn(Path("SKILL.md"), files)
        self.assertIn(Path("skills/big-data-competition-skill/SKILL.md"), files)
        self.assertNotIn(Path("core/bootstrap.yaml"), files)
        self.assertNotIn(Path("tests/test_v752_entrypoint_parity.py"), files)
        self.assertNotIn(Path("scripts/lint_skill.py"), files)

    def test_plugin_version_follows_bigdata_entrypoint(self):
        top = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], validator.version_from_skill(top))
        self.assertEqual(indexer.current_skill_version(ROOT), validator.version_from_skill(top))

    def test_markdown_links_detect_internal_targets(self):
        value = ("[web](https://example.com) [mail](mailto:a@b.com) "
                 "[anchor](#section) [local](./templates/file.md)")
        self.assertEqual(validator.local_targets(value), ["./templates/file.md"])

    def test_active_manifest_tracks_package_not_hsk(self):
        generated = indexer.generated_payloads(ROOT)
        manifest = generated[Path("MANIFEST.sha256")]
        self.assertIn("skills/big-data-competition-skill/SKILL.md", manifest)
        self.assertNotIn("  core/bootstrap.yaml", manifest)
        self.assertIn("当前 Skill 版本：2.1.0",
                      generated[Path("SKILL_FILE_INDEX.md")])
        self.assertTrue(manifest.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
