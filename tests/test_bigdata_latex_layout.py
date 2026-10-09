"""Synthetic layout-failure regression tests, not artistic or scientific certification."""
from __future__ import annotations
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/big-data-competition-skill/tools/latex_paper_audit.py"
spec = spec_from_file_location("latex_paper_audit_test", SOURCE)
assert spec and spec.loader
audit = module_from_spec(spec)
spec.loader.exec_module(audit)

GOOD = r"\setlength{\parindent}{2\ccwd}" + "\n" + (
    r"\ctexset{section={afterindent=true}}" + "\n" +
    r"\tableofcontents" + "\n" + r"\setcounter{page}{1}"
)


class LatexLayoutAuditTests(unittest.TestCase):
    def test_template_and_profile(self):
        template = ROOT / "skills/big-data-competition-skill/templates/bigdata-paper-xelatex/main.tex"
        result = audit.check(template, profile="bigdata2023")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["editorial_page_review"], "required")
        src = template.read_text(encoding="utf-8")
        self.assertIn(r"\setlength{\parindent}{2\ccwd}", src)
        self.assertIn("afterindent=true", src)
        self.assertIn(r"\caption{", src)
        self.assertEqual(audit.active_tex(src).count(r"\tableofcontents"), 1)

    def make(self, tmp, content):
        p = Path(tmp) / "main.tex"
        p.write_text(content, encoding="utf-8")
        return p

    def test_reject_manual_figure_number(self):
        with tempfile.TemporaryDirectory() as td:
            r = audit.check(self.make(td, GOOD + "\n" + r"\caption{图1 结果}"))
            self.assertEqual(r["machine_status"], "blocked")

    def test_reject_duplicate_toc(self):
        with tempfile.TemporaryDirectory() as td:
            r = audit.check(self.make(td, GOOD + "\n" + r"\tableofcontents"))
            self.assertTrue(any("tableofcontents" in e for e in r["errors"]))

    def test_reject_missing_figure(self):
        with tempfile.TemporaryDirectory() as td:
            r = audit.check(self.make(td, GOOD + "\n" + r"\includegraphics{figures/missing.png}"))
            self.assertTrue(any("graphic" in e for e in r["errors"]))

    def test_reject_missing_indentation(self):
        with tempfile.TemporaryDirectory() as td:
            r = audit.check(self.make(td, GOOD.replace("2\\ccwd", "0pt")), profile="bigdata2023")
            self.assertTrue(any("indentation" in e for e in r["errors"]))

    def test_reject_compiler_overfull(self):
        with tempfile.TemporaryDirectory() as td:
            p = self.make(td, GOOD)
            log = Path(td) / "main.log"
            log.write_text("Overfull \\hbox (10.1pt too wide)\n", encoding="utf-8")
            r = audit.check(p, log=log)
            self.assertTrue(any("Build log" in e for e in r["errors"]))

    def test_clean_synthetic_cannot_mean_editorial_approval(self):
        with tempfile.TemporaryDirectory() as td:
            r = audit.check(self.make(td, GOOD), profile="bigdata2023")
            self.assertEqual(r["machine_status"], "preflight_passed_manual_review_required")
            self.assertEqual(r["editorial_page_review"], "required")


if __name__ == "__main__":
    unittest.main()
