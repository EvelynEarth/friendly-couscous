"""Small independent numerical oracles with handwritten golden answers.

All cases here are synthetic known-answer unit tests, not MathorCup results.
"""
from __future__ import annotations

from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "skills/big-data-competition-skill/tools/independent_oracle.py"


def load():
    spec = spec_from_file_location("independent_oracle", FILE)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


oracle = load()


def regression():
    # Actual [0,2,4], predictions [1,1,5], errors [-1,1,-1]
    # MAE = RMSE = 1 by hand.
    return {
        "task": "regression", "actual": [0, 2, 4], "predicted": [1, 1, 5],
        "reported": {"mae": 1, "rmse": 1},
    }


def classification():
    # A: precision=1, recall=1/2, F1=2/3
    # B: precision=2/3, recall=1, F1=4/5
    # Macro F1=11/15, macro precision=5/6, macro recall=3/4
    return {
        "task": "classification",
        "labels": ["A", "B"],
        "actual": ["A", "A", "B", "B"],
        "predicted": ["A", "B", "B", "B"],
        "reported": {"accuracy": .75, "macro_precision": 5 / 6,
                     "macro_recall": .75, "macro_f1": 11 / 15},
    }


def opt_max():
    # max 3x+2y, 0<=x,y<=4, 2x+y<=7, x+2y<=7
    # exhaustive optimum x=3,y=1, value=11 (by hand).
    return {
        "task": "bounded_integer_linear", "sense": "maximize",
        "objective": [3, 2], "bounds": [[0, 4], [0, 4]],
        "constraints": [
            {"op": "le", "weights": [2, 1], "rhs": 7},
            {"op": "le", "weights": [1, 2], "rhs": 7},
        ],
        "candidate": [3, 1], "claimed_objective": 11,
    }


def opt_min():
    # Min x+2y subject to x+y>=3, 0<=x,y<=3. x=3,y=0 is optimal, value 3.
    return {
        "task": "bounded_integer_linear", "sense": "minimize",
        "objective": [1, 2], "bounds": [[0, 3], [0, 3]],
        "constraints": [{"op": "ge", "weights": [1, 1], "rhs": 3}],
        "candidate": [3, 0], "claimed_objective": 3,
    }


class GoldenOracleTests(unittest.TestCase):
    def test_hand_computed_regression(self):
        out = oracle.audit(regression())
        self.assertEqual(out["status"], "recomputed_match", out)
        self.assertEqual(out["recomputed"], {"mae": 1.0, "rmse": 1.0})

    def test_hand_computed_classification(self):
        out = oracle.audit(classification())
        self.assertEqual(out["status"], "recomputed_match", out)
        self.assertEqual(out["confusion_matrix_rows_actual_cols_predicted"], [[1, 1], [0, 2]])
        self.assertAlmostEqual(out["recomputed"]["macro_f1"], 11 / 15)

    def test_hand_computed_max_optimum(self):
        out = oracle.audit(opt_max())
        self.assertEqual(out["status"], "exact_small_case_match", out)
        self.assertEqual(out["exact_optimal_objective"], 11)
        self.assertEqual(out["exact_witness"], [3, 1])
        self.assertEqual(out["states_enumerated"], 25)

    def test_hand_computed_min_optimum(self):
        out = oracle.audit(opt_min())
        self.assertEqual(out["status"], "exact_small_case_match", out)
        self.assertEqual(out["exact_optimal_objective"], 3)
        self.assertEqual(out["exact_witness"], [3, 0])

    def test_model_is_feasible_but_suboptimal(self):
        case = opt_max()
        case["candidate"] = [2, 2]
        case["claimed_objective"] = 10
        out = oracle.audit(case)
        self.assertEqual(out["status"], "disagreement")
        self.assertTrue(out["candidate_feasible"])
        self.assertEqual(out["objective_gap"], 1)

    def test_infeasible_but_high_objective_cannot_pass(self):
        case = opt_max()
        case["candidate"] = [4, 0]
        case["claimed_objective"] = 12
        out = oracle.audit(case)
        self.assertEqual(out["status"], "disagreement")
        self.assertFalse(out["candidate_feasible"])

    def test_fake_claimed_optimum_cannot_pass(self):
        case = opt_max()
        case["claimed_objective"] = 999
        out = oracle.audit(case)
        self.assertEqual(out["status"], "disagreement")
        self.assertFalse(out["reported_matches_recalculated"])

    def test_changed_classification_metric_rejected(self):
        case = classification()
        case["reported"]["macro_f1"] = .95
        out = oracle.audit(case)
        self.assertEqual(out["status"], "blocked")
        self.assertIn("macro_f1", out["errors"][0])

    def test_zero_division_and_absent_class(self):
        case = {"task": "classification", "labels": ["A", "B", "C"],
                "actual": ["A", "A"], "predicted": ["A", "A"],
                "reported": {"accuracy": 1, "macro_precision": 1 / 3,
                             "macro_recall": 1 / 3, "macro_f1": 1 / 3}}
        out = oracle.audit(case)
        self.assertEqual(out["status"], "recomputed_match", out)

    def test_nan_and_boolean_scores_rejected(self):
        case = regression()
        case["predicted"][0] = float("nan")
        self.assertEqual(oracle.audit(case)["status"], "blocked")
        case = regression()
        case["reported"]["mae"] = True
        self.assertEqual(oracle.audit(case)["status"], "blocked")

    def test_mismatched_prediction_length_and_invalid_labels(self):
        case = regression()
        case["predicted"].pop()
        self.assertEqual(oracle.audit(case)["status"], "blocked")
        case = classification()
        case["predicted"][0] = "UNSEEN"
        self.assertEqual(oracle.audit(case)["status"], "blocked")

    def test_bounded_search_rejects_giant_domain(self):
        case = opt_max()
        case["bounds"] = [[0, 1_000], [0, 1_000]]
        out = oracle.audit(case)
        self.assertEqual(out["status"], "blocked")
        self.assertIn("hard limit", out["errors"][0])

    def test_integer_model_rejects_fractional_or_empty_bounds(self):
        case = opt_max()
        case["candidate"][0] = 3.5
        self.assertEqual(oracle.audit(case)["status"], "blocked")
        case = opt_max()
        case["bounds"][0] = [5, 2]
        self.assertEqual(oracle.audit(case)["status"], "blocked")

    def test_detects_infeasible_problem_itself(self):
        case = opt_max()
        case["constraints"].append({"op": "ge", "weights": [1, 1], "rhs": 20})
        self.assertEqual(oracle.audit(case)["status"], "blocked")

    def test_regression_shift_metamorphic_property(self):
        case = regression()
        shift = 12345
        case["actual"] = [x + shift for x in case["actual"]]
        case["predicted"] = [x + shift for x in case["predicted"]]
        # A common shift of prediction and reference must not affect MAE / RMSE.
        out = oracle.audit(case)
        self.assertEqual(out["status"], "recomputed_match", out)

    def test_class_label_rename_metamorphic_property(self):
        case = classification()
        mapping = {"A": "container", "B": "parcel"}
        case["labels"] = [mapping[x] for x in case["labels"]]
        case["actual"] = [mapping[x] for x in case["actual"]]
        case["predicted"] = [mapping[x] for x in case["predicted"]]
        self.assertEqual(oracle.audit(case)["status"], "recomputed_match")

    def test_opt_redundant_constraint_metamorphic_property(self):
        case = opt_max()
        case["constraints"].append({"op": "le", "weights": [1, 1], "rhs": 100})
        self.assertEqual(oracle.audit(case)["status"], "exact_small_case_match")

    def test_minimization_incorrect_candidate_fails(self):
        case = opt_min()
        case["candidate"] = [1, 2]
        case["claimed_objective"] = 5
        out = oracle.audit(case)
        self.assertEqual(out["status"], "disagreement")
        self.assertEqual(out["objective_gap"], 2)

    def test_metrics_need_complete_named_dictionary(self):
        case = regression()
        del case["reported"]["rmse"]
        self.assertEqual(oracle.audit(case)["status"], "blocked")
        case = classification()
        case["reported"]["bogus"] = 1
        self.assertEqual(oracle.audit(case)["status"], "blocked")

    def test_bad_precision_tolerance_does_not_bypass_fraud(self):
        case = regression()
        case["absolute_tolerance"] = 1
        self.assertEqual(oracle.audit(case)["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
