"""Synthetic falsification + source anchor coverage, not award-paper model certification."""
from __future__ import annotations
import json
import re
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
TOOL=ROOT/"skills/big-data-competition-skill/tools/paper_metric_identity_gate.py"
spec=spec_from_file_location("paper_metric_identity_gate",TOOL)
assert spec and spec.loader
metric=module_from_spec(spec)
spec.loader.exec_module(metric)

STUDY=ROOT/"skills/big-data-competition-skill/references/award-paper-deep-argumentation-16.md"
INVENTORY=ROOT/"skills/big-data-competition-skill/competition/award_papers_2024_2025.json"

class AwardDeepReviewTests(unittest.TestCase):
    def test_all_sixteen_pdf_page_anchors(self):
        s=STUDY.read_text(encoding="utf-8")
        ids=re.findall(r"(?m)^### (202[45]-\d{2}) ·",s)
        self.assertEqual(len(ids),16)
        self.assertEqual(set(ids),{f"{year}-{i:02d}" for year in (2024,2025) for i in range(1,9)})
        inventory=json.loads(INVENTORY.read_text(encoding="utf-8"))["papers"]
        by_id={p["paper_id"]:p for p in inventory}
        for id in ids:
            self.assertRegex(by_id[id]["machine_layout_evidence"]["source_pdf_sha256"],r"^[a-f0-9]{64}$")
            self.assertIn("pdf_content_verified",by_id[id])
            self.assertIn("unreviewed",by_id[id]["review_status"])
        self.assertIn("不是716页",s)
        self.assertIn("2024-04",s)
        self.assertIn("2025-05",s)

    def test_falsifies_real_paper_reported_metric_pair(self):
        payload={"checks":[{"experiment_id":"award-paper-2024-04-example",
                 "comparability":{"same_samples":True,"same_weights":True,"same_error_scale":True},
                 "metrics":{"MSE":0.0071,"RMSE":0.0336}}]}
        r=metric.audit(payload)
        self.assertEqual(r["status"],"blocked")
        self.assertAlmostEqual(r["records"][0]["implied_mse"],0.00112896,places=8)

    def test_consistent_synthetic_metrics_are_not_scientific_pass(self):
        x={"checks":[{"experiment_id":"synthetic-pass",
                     "comparability":{"same_samples":True,"same_weights":True,"same_error_scale":True},
                     "metrics":{"MSE":0.09,"RMSE":0.3,"MAE":0.25}}]}
        a=metric.audit(x)
        self.assertEqual(a["status"],"arithmetic_consistent_only")
        self.assertEqual(a["records"][0]["status"],"arithmetic_consistent_not_scientifically_verified")

    def test_missing_metric_comparability_requires_review(self):
        x={"checks":[{"experiment_id":"synthetic-unknown",
                     "comparability":{"same_samples":True,"same_weights":False},
                     "metrics":{"MSE":0.09,"RMSE":0.3}}]}
        self.assertEqual(metric.audit(x)["status"],"requires_human_comparability_review")

    def test_mae_exceeds_rmse_is_blocked(self):
        x={"checks":[{"experiment_id":"synthetic-conflict",
                     "comparability":{"same_samples":True,"same_weights":True,"same_error_scale":True},
                     "metrics":{"MSE":0.09,"RMSE":0.3,"MAE":0.45}}]}
        self.assertEqual(metric.audit(x)["status"],"blocked")

if __name__=="__main__":
    unittest.main()
