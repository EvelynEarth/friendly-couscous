"""Source-provenance and honest review-status contract; not paper-quality grading."""
from __future__ import annotations
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "skills/big-data-competition-skill/competition/award_papers_2024_2025.json"
GUIDE = ROOT / "skills/big-data-competition-skill/references/award-paper-empirical-layout.md"


class AwardPaperSourceEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.papers = cls.data["papers"]

    def test_sixteen_original_pdf_sources_with_hashes(self):
        self.assertEqual(len(self.papers), 16)
        ids = {p["paper_id"] for p in self.papers}
        expected = {f"{year}-{i:02d}" for year in (2024, 2025) for i in range(1, 9)}
        self.assertEqual(ids, expected)
        for p in self.papers:
            meta = p["machine_layout_evidence"]
            self.assertRegex(meta["source_pdf_sha256"], r"^[a-f0-9]{64}$")
            self.assertRegex(meta["source_git_blob"], r"^[a-f0-9]{40}$")
            self.assertGreater(meta["source_pdf_pages"], 0)
            self.assertEqual(len(meta["visual_preview_sample_pages"]), 3)
            self.assertIn(p["paper_id"]+".json", meta["per_paper_record"])
            self.assertEqual(p["review_status"], "unreviewed")
            self.assertFalse(p["pdf_content_verified"])
            self.assertEqual(meta["full_human_scientific_review"], "not_completed")

    def test_actual_machine_report_totals(self):
        meta = [p["machine_layout_evidence"] for p in self.papers]
        self.assertEqual(sum(p["source_pdf_pages"] for p in meta), 716)
        self.assertEqual(sum(p["text_extractable_pages_ge_80_chars"] for p in meta), 704)
        self.assertLessEqual(sum(p["text_extractable_pages_ge_80_chars"] for p in meta),
                             sum(p["source_pdf_pages"] for p in meta))

    def test_reference_card_has_real_page_provenance_and_clear_boundary(self):
        guide = GUIDE.read_text(encoding="utf-8")
        self.assertIn("2025-05", guide)
        self.assertIn("第11页", guide)
        self.assertIn("2025-02", guide)
        self.assertIn("第12页", guide)
        self.assertIn("尚未完成", guide)
        self.assertIn("机器解析", guide)


if __name__ == "__main__":
    unittest.main()
