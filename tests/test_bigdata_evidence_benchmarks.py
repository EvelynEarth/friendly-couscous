"""Evidence-based award-paper audit + four-family adversarial benchmark tests."""
from __future__ import annotations

from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "skills/big-data-competition-skill"


def load(name, path):
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    obj = module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


audit = load("award_paper_audit", BASE / "tools/award_paper_audit.py")
bench = load("competition_benchmark", BASE / "tools/competition_benchmark.py")


class AwardEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((BASE / "competition/award_papers_2024_2025.json").read_text(encoding="utf-8"))

    def test_inventory_matches_2024_2025_eight_each(self):
        self.assertEqual(audit.check_inventory(self.data), [])
        report = audit.summarize(self.data)
        self.assertEqual(report["inventory_total"], 16)
        self.assertEqual(report["reviewed_papers"], 0)
        self.assertEqual(report["method_frequency_denominator"], 0)
        self.assertEqual(report["by_year"]["2024"]["total"], 8)
        self.assertEqual(report["by_year"]["2025"]["total"], 8)
        self.assertEqual(report["method_family_paper_counts"], {})

    def test_unreviewed_cannot_claim_methods(self):
        copy = deepcopy(self.data)
        copy["papers"][0]["findings"] = [{"method_family": "LightGBM"}]
        self.assertTrue(any("unreviewed/unavailable" in x for x in audit.check_inventory(copy)))

    def test_reviewed_requires_verified_page_and_content(self):
        copy = deepcopy(self.data)
        p = copy["papers"][0]
        p["review_status"] = "reviewed"
        p["findings"] = [{
            "question": "Q1", "page": 3, "method_family": "time_series",
            "attribution": "author_reported", "evidence_note": "Method explicitly described on PDF page 3",
            "evidence_verified": True
        }]
        self.assertTrue(audit.check_inventory(copy))  # not enough: content flag required
        p["pdf_content_verified"] = True
        self.assertEqual(audit.check_inventory(copy), [])
        self.assertEqual(audit.summarize(copy)["method_frequency_denominator"], 1)
        p["findings"].append(deepcopy(p["findings"][0]))
        self.assertEqual(audit.summarize(copy)["method_family_paper_counts"], {"time_series": 1})

    def test_bad_page_and_unverified_claim_rejected(self):
        copy = deepcopy(self.data)
        p = copy["papers"][0]
        p["review_status"] = "reviewed"
        p["pdf_content_verified"] = True
        p["findings"] = [{
            "question": "Q2", "page": 0, "method_family": "vision",
            "attribution": "author_reported", "evidence_note": "X", "evidence_verified": False
        }]
        problems = audit.check_inventory(copy)
        self.assertTrue(any("PDF page" in x for x in problems))
        self.assertTrue(any("verified PDF evidence" in x for x in problems))


class CompetitionBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((BASE / "benchmarks/mathorcup_scenarios.json").read_text(encoding="utf-8"))

    def test_ten_cases_four_families_and_six_negative_guards(self):
        outcome = bench.run_suite(self.data)
        self.assertEqual(outcome["status"], "passed", outcome)
        self.assertEqual(outcome["total"], 10)
        self.assertEqual(outcome["matched"], 10)
        self.assertEqual(sum(c["expected"] == "pass" for c in outcome["cases"]), 4)
        self.assertEqual(sum(c["expected"] == "reject" for c in outcome["cases"]), 6)

    def test_future_label_feature_rejected(self):
        p = deepcopy(self.data["cases"][3]["plan"])
        p["features"].append({"name": "post-claim payout", "available_at_prediction": False})
        self.assertTrue(any("future" in x for x in bench.validate_plan(p)))

    def test_bbox_cannot_be_segmentation_gt(self):
        p = deepcopy(self.data["cases"][2]["plan"])
        p["output_kind"] = "segmentation"
        p["ground_truth_kind"] = "bbox"
        problems = bench.validate_plan(p)
        self.assertTrue(any("pixel-level" in x for x in problems))

    def test_group_time_splits_guarded(self):
        p = deepcopy(self.data["cases"][0]["plan"])
        p["group_disjoint"] = False
        self.assertTrue(any("disjoint" in x for x in bench.validate_plan(p)))
        p = deepcopy(self.data["cases"][0]["plan"])
        p["validation_scheme"] = "random"
        self.assertTrue(any("time-ordered" in x for x in bench.validate_plan(p)))

    def test_optimization_needs_feasibility(self):
        p = deepcopy(self.data["cases"][1]["plan"])
        p["feasibility_verified"] = False
        self.assertTrue(any("feasibility" in x for x in bench.validate_plan(p)))

    def test_official_results_and_numerical_evidence_guarded(self):
        p = deepcopy(self.data["cases"][3]["plan"])
        p["official_result"]["template_checked"] = False
        self.assertTrue(any("official result" in x for x in bench.validate_plan(p)))
        p = deepcopy(self.data["cases"][3]["plan"])
        p["claims"] = [{"numerical": True, "statement": "accuracy = 0.99"}]
        self.assertTrue(any("accepted evidence" in x for x in bench.validate_plan(p)))


if __name__ == "__main__":
    unittest.main()
