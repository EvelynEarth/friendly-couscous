"""Cross-module adversarial regression: no independent result, no green paper gate.

All fixtures use hand-checkable synthetic data. They DO NOT reproduce contest runs.
"""
from __future__ import annotations

import hashlib
from importlib.util import module_from_spec, spec_from_file_location
import json
import math
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "skills/big-data-competition-skill/tools"
sys.path.insert(0, str(TOOLS))
spec = spec_from_file_location("project_evidence_chain", TOOLS / "project_evidence_chain.py")
assert spec is not None and spec.loader is not None
chain = module_from_spec(spec)
spec.loader.exec_module(chain)

from solution_quality_gate import GENERAL, CONDITIONAL  # noqa: E402


def sha(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


class SyntheticProject:
    def __init__(self, root: Path):
        self.root = root
        self.payloads = {
            "review-proof.txt": b"Hand-computed toy regression by independent evaluator.\n",
            "split.csv": b"id,fold\nA,train\nB,valid\n",
        }
        self.quality = self._quality()
        self.accepted = self._accepted()
        self.oracle = {
            "task": "regression", "actual": [0, 2, 4], "predicted": [1, 1, 5],
            "reported": {"mae": 1, "rmse": 1},
        }
        self.result = {"values": {"predicted": [1, 1, 5]}}
        self.invariants = {"case_id": "toy-Q1", "invariants": [
            {"id": "pred-bounds", "field": "predicted", "op": "bounds",
             "lower": 0, "upper": 6},
        ]}
        self.stability = {
            "metric": "mae", "direction": "minimize", "protocol_id": "fixed holdout",
            "data_version": "toy synthetic data", "perturbation": "seed",
            "max_range": .1, "threshold_predeclared": True,
            "claim_improvement": False,
            "runs": [
                {"run_id": "anchor", "value": 1.0},
                {"run_id": "alternate", "value": 1.02},
                {"run_id": "another", "value": .99},
            ],
        }
        self.task = {
            "id": "Q1", "paper_record": "paper.json",
            "oracle": {"engine": "independent", "case": "oracle.json"},
            "metric_map": {"mae": "recomputed.mae", "rmse": "recomputed.rmse"},
            "invariants": {
                "contract": "invariants.json", "result": "result.json",
                "result_links": {"predicted": "predicted"},
            },
            "stability": "stability.json", "stability_anchor_run_id": "anchor",
        }
        self.manifest = {
            "schema_version": 1, "project_id": "synthetic-golden",
            "official_questions": ["Q1"], "quality_record": "quality.json",
            "questions": [self.task],
        }

    def _quality(self):
        checks = {name: {"status": "passed", "method": "independent test",
                         "artifact": "review-proof.txt"}
                  for name in (*GENERAL, *CONDITIONAL["prediction"])}
        checks["independent_verification"]["independent"] = True
        return {"questions": [{
            "id": "Q1", "objective": "prediction",
            "expected_output": "numerical regression predictions in given units",
            "actual_output": "predictions in specified units",
            "model_rationale": "tiny toy baseline, cross-checked independently",
            "limitations": ["synthetic example only"],
            "checks": checks,
            "claims": [{"statement": "toy MAE equals 1", "strength": "predictive",
                        "artifact": "metrics.json", "status": "supported"}],
        }]}

    def _accepted(self):
        return {
            "experiment_id": "toy-RUN1", "run_status": "accepted",
            "data_version": "toy-v1", "code_revision": "toy-commit",
            "validation_scheme": "holdout", "split_protocol": "fixed train and valid",
            "random_seed": 42, "split_manifest": "split.csv",
            "metrics_artifact": "metrics.json",
            "metrics": {"mae": 1, "rmse": 1}, "artifacts": [],
            "claims": [
                {"claim_id": "C1", "metric": "mae", "value": 1,
                 "artifact": "metrics.json", "paper_location": "Q1 results"},
                {"claim_id": "C2", "metric": "rmse", "value": 1,
                 "artifact": "metrics.json", "paper_location": "Q1 results"},
            ],
        }

    def write(self):
        self.payloads["metrics.json"] = json.dumps(
            {"metrics": self.accepted["metrics"]}).encode()
        self.accepted["artifacts"] = [
            {"path": name, "sha256": sha(self.payloads[name])}
            for name in ("metrics.json", "split.csv")
        ]
        self.payloads["paper.json"] = json.dumps(self.accepted).encode()
        self.payloads["oracle.json"] = json.dumps(self.oracle).encode()
        self.payloads["result.json"] = json.dumps(self.result).encode()
        self.invariants["result_sha256"] = sha(self.payloads["result.json"])
        self.payloads["invariants.json"] = json.dumps(self.invariants).encode()
        self.payloads["stability.json"] = json.dumps(self.stability).encode()
        self.payloads["quality.json"] = json.dumps(self.quality).encode()
        for path, content in self.payloads.items():
            (self.root / path).write_bytes(content)
        self.manifest["files"] = [
            {"path": name, "sha256": sha(content)}
            for name, content in sorted(self.payloads.items())
        ]
        return chain.audit(self.manifest, self.root)


class EvidenceChainTests(unittest.TestCase):
    def with_project(self, fn):
        with tempfile.TemporaryDirectory() as tmp:
            sample = SyntheticProject(Path(tmp))
            sample.write()
            fn(sample)

    def test_positive_end_to_end_machine_consistency_only(self):
        def run(s):
            result = s.write()
            self.assertEqual(result["status"], "machine_evidence_consistent", result)
            self.assertEqual(result["questions_declared"], 1)
            self.assertEqual(result["questions"][0]["checks"]["independent_oracle"], "recomputed_match")
            self.assertEqual(result["scientific_approval"], "human_scientific_review_still_required")
        self.with_project(run)

    def test_no_metric_oracle_collusion(self):
        def run(s):
            s.accepted["metrics"]["mae"] = .9
            s.accepted["claims"][0]["value"] = .9
            s.oracle["reported"]["mae"] = 1  # actual is 1
            result = s.write()
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("differs from independent" in x for x in result["errors"]))
        self.with_project(run)

    def test_oracle_rejects_fake_independent_metric(self):
        def run(s):
            s.oracle["reported"]["mae"] = .9
            result = s.write()
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("independent oracle" in x for x in result["errors"]))
        self.with_project(run)

    def test_invariant_result_must_match_oracle_output(self):
        def run(s):
            s.result["values"]["predicted"] = [0, 0, 0]
            result = s.write()
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("invariant values differ" in x for x in result["errors"]))
        self.with_project(run)

    def test_invariant_failure_blocks_whole_paper(self):
        def run(s):
            s.invariants["invariants"][0]["upper"] = .5
            result = s.write()
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("violates specified invariants" in x for x in result["errors"]))
        self.with_project(run)

    def test_wrong_anchor_not_stability_evidence(self):
        def run(s):
            s.stability["runs"][0]["value"] = .4
            s.stability["max_range"] = 1
            result = s.write()
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("stability anchor run" in x for x in result["errors"]))
        self.with_project(run)

    def test_unstable_results_block_paper(self):
        def run(s):
            s.stability["runs"][1]["value"] = 3
            result = s.write()
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("declared stability study failed" in x for x in result["errors"]))
        self.with_project(run)

    def test_missing_official_subquestion_never_green(self):
        def run(s):
            s.manifest["official_questions"] = ["Q1", "Q2"]
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("question" in e for e in out["errors"]))
        self.with_project(run)

    def test_unverified_review_proof_fails(self):
        def run(s):
            s.quality["questions"][0]["checks"]["baseline_or_reference"]["artifact"] = "missing-proof.txt"
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("review evidence not SHA-verified" in e for e in out["errors"]))
        self.with_project(run)

    def test_snapshot_change_after_hashing_fails(self):
        def run(s):
            self.assertEqual(s.write()["status"], "machine_evidence_consistent")
            (s.root / "metrics.json").write_text('{"metrics":{"mae":900}}', encoding="utf-8")
            out = chain.audit(s.manifest, s.root)
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("SHA-256 differs" in e for e in out["errors"]))
        self.with_project(run)

    def test_metric_map_partial_is_blocked(self):
        def run(s):
            s.task["metric_map"] = {"mae": "recomputed.mae"}
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("ALL paper metrics" in e for e in out["errors"]))
        self.with_project(run)

    def test_unsupported_task_must_escalate_not_pass(self):
        def run(s):
            s.task["oracle"]["engine"] = "invented"
            out = s.write()
            self.assertEqual(out["status"], "blocked")
        self.with_project(run)

    def test_skipping_invariants_requires_reason(self):
        def run(s):
            del s.task["invariants"]
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            s.task["invariants_not_applicable_reason"] = (
                "The specific quantity has no numeric invariants expressible in the available DSL."
            )
            out = s.write()
            self.assertEqual(out["status"], "machine_evidence_consistent", out)
        self.with_project(run)

    def test_skipping_stability_requires_reason(self):
        def run(s):
            del s.task["stability"]
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            s.task["stability_not_applicable_reason"] = (
                "This is a deterministic mathematical oracle with no random parameter to vary."
            )
            out = s.write()
            self.assertEqual(out["status"], "machine_evidence_consistent", out)
        self.with_project(run)

    def test_oracle_input_must_be_locked_in_snapshot(self):
        def run(s):
            s.write()
            s.manifest["files"] = [f for f in s.manifest["files"] if f["path"] != "oracle.json"]
            out = chain.audit(s.manifest, s.root)
            self.assertEqual(out["status"], "blocked")
        self.with_project(run)

    def test_duplicate_subquestion_entry_is_blocked(self):
        def run(s):
            s.manifest["questions"].append(s.task)
            out = s.write()
            self.assertEqual(out["status"], "blocked")
        self.with_project(run)

    def test_quality_gate_failed_cannot_be_overridden(self):
        def run(s):
            s.quality["questions"][0]["checks"]["leakage_control"] = {"status": "failed"}
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("solution quality" in e for e in out["errors"]))
        self.with_project(run)

    def test_strict_paper_source_is_mandatory(self):
        def run(s):
            del s.accepted["metrics_artifact"]
            out = s.write()
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("strict check" in e for e in out["errors"]))
        self.with_project(run)

    def test_no_false_green_on_empty_project(self):
        self.assertEqual(chain.audit({}, Path("/tmp"))["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
