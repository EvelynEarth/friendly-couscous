"""Task-agnostic correctness review coverage and quantitative stability tests."""
from __future__ import annotations
from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "skills/big-data-competition-skill/tools"


def load(name: str, path: Path):
    spec = spec_from_file_location(name, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


quality = load("solution_quality_gate", TOOLS / "solution_quality_gate.py")
stability = load("stability_audit", TOOLS / "stability_audit.py")


def valid_question(objective="prediction"):
    checks = {
        name: {"status": "passed", "method": "independent reviewed test",
               "artifact": "out/verified-result.json"}
        for name in (*quality.GENERAL, *quality.CONDITIONAL.get(objective, ()))
    }
    checks["independent_verification"]["independent"] = True
    return {
        "id": "subproblem-X", "objective": objective,
        "expected_output": "task answer with units",
        "actual_output": "actual answer with units",
        "model_rationale": "compared baselines and assumptions",
        "limitations": ["training sample may not generalize"],
        "checks": checks,
        "claims": [{"statement": "only under tested setting", "artifact": "out/verified-result.json",
                    "strength": "qualified", "status": "supported"}],
    }


def repeated_metrics():
    return {
        "metric": "macro_f1", "direction": "maximize",
        "protocol_id": "fixed-group-holdout", "data_version": "sha256-locked",
        "perturbation": "training_seed", "max_range": 0.05, "threshold_predeclared": True,
        "claim_improvement": True, "min_paired_gain": 0.01,
        "runs": [
            {"run_id": "seed-11", "value": 0.81, "baseline_value": 0.70},
            {"run_id": "seed-22", "value": 0.80, "baseline_value": 0.70},
            {"run_id": "seed-33", "value": 0.82, "baseline_value": 0.71},
        ]
    }


class ValidityGateTests(unittest.TestCase):
    def test_generic_question_passes_coverage_not_scientific_proof(self):
        result = quality.inspect({"questions": [valid_question()]})
        self.assertEqual(result["status"], "review_ready")
        self.assertIn("does not establish", result["meaning"])

    def test_six_objective_families_are_not_hardcoded_years(self):
        objectives = ["prediction", "causal", "optimization", "simulation", "inference", "description"]
        for objective in objectives:
            with self.subTest(objective=objective):
                self.assertEqual(quality.inspect({"questions": [valid_question(objective)]})["status"], "review_ready")

    def test_missing_independent_reviewer_blocks(self):
        q = valid_question()
        del q["checks"]["independent_verification"]["independent"]
        issues = quality.inspect({"questions": [q]})["issues"]
        self.assertTrue(any("explicitly independent" in x["reason"] for x in issues))

    def test_unknown_or_failed_check_blocks(self):
        q = valid_question()
        q["checks"]["units_and_boundary_cases"] = {"status": "unknown"}
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")
        q["checks"]["units_and_boundary_cases"] = {"status": "failed"}
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")

    def test_evidence_missing_from_passed_check_blocks(self):
        q = valid_question()
        q["checks"]["baseline_or_reference"] = {"status": "passed", "method": "hand calculation"}
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")

    def test_cannot_waive_causal_identification_or_optimization_feasibility(self):
        for objective, name in (("causal", "identification_and_confounding"),
                                ("optimization", "constraint_feasibility")):
            q = valid_question(objective)
            q["checks"][name] = {"status": "not_applicable",
                                 "reason": "unjustified attempt to skip a scientific check"}
            self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")

    def test_unsupported_or_out_of_scope_claim_blocks(self):
        q = valid_question()
        q["claims"][0]["strength"] = "causal"
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")
        q["claims"][0]["strength"] = "qualified"
        q["claims"][0]["status"] = "pending"
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")

    def test_missing_official_answer_or_duplicate_question_blocks(self):
        q = valid_question()
        q["actual_output"] = ""
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")
        q = valid_question()
        self.assertEqual(quality.inspect({"questions": [q, deepcopy(q)]})["status"], "blocked")

    def test_inference_requires_identifiability_and_uncertainty(self):
        q = valid_question("inference")
        del q["checks"]["identifiability_and_uncertainty"]
        self.assertEqual(quality.inspect({"questions": [q]})["status"], "blocked")


class StabilityTests(unittest.TestCase):
    def test_three_runs_and_paired_gain(self):
        record = repeated_metrics()
        out = stability.audit(record)
        self.assertEqual(out["status"], "stable_under_tested_perturbations", out)
        self.assertEqual(out["n"], 3)
        self.assertAlmostEqual(out["observed_range"], 0.02)
        self.assertEqual(out["baseline_comparison"]["paired_count"], 3)
        self.assertTrue(out["baseline_comparison"]["meets_predeclared_min_gain_all_runs"])

    def test_one_run_is_not_stability(self):
        record = repeated_metrics()
        record["runs"] = record["runs"][:1]
        self.assertEqual(stability.audit(record)["status"], "blocked")

    def test_large_variation_is_unstable(self):
        record = repeated_metrics()
        record["runs"][2]["value"] = 0.70
        out = stability.audit(record)
        self.assertEqual(out["status"], "unsupported_improvement_claim")
        record["claim_improvement"] = False
        self.assertEqual(stability.audit(record)["status"], "unstable")

    def test_conservative_claim_requires_all_paired_gains(self):
        record = repeated_metrics()
        record["runs"][1]["value"] = 0.705
        record["max_range"] = 0.2
        self.assertEqual(stability.audit(record)["status"], "unsupported_improvement_claim")

    def test_wrong_metric_direction_correctly_changes_gain(self):
        record = repeated_metrics()
        record["direction"] = "minimize"
        self.assertEqual(stability.audit(record)["status"], "unsupported_improvement_claim")

    def test_missing_predeclared_threshold_blocks(self):
        record = repeated_metrics()
        record["threshold_predeclared"] = False
        self.assertEqual(stability.audit(record)["status"], "blocked")

    def test_duplicate_run_nonfinite_and_mismatched_baseline_block(self):
        record = repeated_metrics()
        record["runs"][1]["run_id"] = "seed-11"
        self.assertEqual(stability.audit(record)["status"], "blocked")
        record = repeated_metrics()
        record["runs"][0]["value"] = float("nan")
        self.assertEqual(stability.audit(record)["status"], "blocked")
        record = repeated_metrics()
        del record["runs"][0]["baseline_value"]
        self.assertEqual(stability.audit(record)["status"], "blocked")

    def test_no_baseline_stability_still_possible_without_superiority_claim(self):
        record = repeated_metrics()
        record["claim_improvement"] = False
        record["min_paired_gain"] = None
        for r in record["runs"]:
            del r["baseline_value"]
        self.assertEqual(stability.audit(record)["status"], "stable_under_tested_perturbations")


if __name__ == "__main__":
    unittest.main()
