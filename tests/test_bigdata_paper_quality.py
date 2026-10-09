"""Synthetic paper-quality contract regression tests; not a scientific/editorial sign-off."""
from __future__ import annotations
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "skills/big-data-competition-skill/tools/competition_autopilot.py"
spec = spec_from_file_location("competition_autopilot_paper", MOD)
assert spec is not None and spec.loader is not None
module = module_from_spec(spec)
spec.loader.exec_module(module)


class PaperQualityContractTests(unittest.TestCase):
    def test_required_paper_checks_cannot_be_waived(self):
        self.assertIn("visual_design_and_color_reviewed", module.CHECKS["figures"])
        self.assertIn("academic_argumentation_reviewed", module.CHECKS["paper"])
        self.assertIn("rendered_pdf_pages_reviewed", module.CHECKS["final"])
        for key in ("visual_design_and_color_reviewed", "academic_argumentation_reviewed", "rendered_pdf_pages_reviewed"):
            self.assertIn(key, module.NON_WAIVABLE)

    def test_must_list_all_paper_checks_and_actual_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            workspace = Path(td)
            (workspace / "artifacts").mkdir()
            (workspace / "artifacts/paper.txt").write_text("synthetic review", encoding="utf-8")
            checks = {name: {"status": "passed", "method": "synthetic check", "artifact": "artifacts/paper.txt"}
                      for name in module.CHECKS["paper"]}
            report = {"stage": "paper", "decision": "passed",
                      "artifacts": ["artifacts/paper.txt"], "checks": checks}
            artifacts, errors = module.review("paper", report, workspace)
            self.assertFalse(errors)
            self.assertTrue(artifacts)
            del checks["academic_argumentation_reviewed"]
            _, errors = module.review("paper", report, workspace)
            self.assertTrue(errors)

    def test_xelatex_template_not_fixed_three_tasks(self):
        tex = (ROOT / "skills/big-data-competition-skill/templates/bigdata-paper-xelatex/main.tex").read_text(encoding="utf-8")
        self.assertIn("ctexart", tex)
        self.assertIn("tableofcontents", tex)
        self.assertIn("booktabs", tex)
        self.assertNotIn("C:\\\\", tex)
        self.assertNotIn("Kaggle", tex)


if __name__ == "__main__":
    unittest.main()
