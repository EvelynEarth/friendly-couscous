"""Independent scientific oracles: hand-checkable golden and adversarial cases.

These are synthetic checks of the VERIFIERS, not past MathorCup model runs.
"""
from __future__ import annotations

from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
import math
from pathlib import Path
import unittest

FILE = (Path(__file__).resolve().parents[1] /
        "skills/big-data-competition-skill/tools/extended_oracles.py")
spec = spec_from_file_location("extended_oracles", FILE)
assert spec is not None and spec.loader is not None
oracle = module_from_spec(spec)
spec.loader.exec_module(oracle)


def rolling():
    # Errors: [1,-1,1,-2]; absolute mean 5/4, squared mean 7/4.
    return {
        "task": "rolling_forecast", "required_gap": 1,
        "folds": [
            {"series_id": "A", "train_start": 0, "train_end": 3,
             "valid_start": 5, "valid_end": 6, "actual": [2, 4], "predicted": [1, 5]},
            {"series_id": "A", "train_start": 0, "train_end": 6,
             "valid_start": 8, "valid_end": 9, "actual": [3, 5], "predicted": [2, 7]},
        ],
        "reported": {"mae": 1.25, "rmse": math.sqrt(7/4)},
    }


def paired():
    # Six strictly positive paired differences. Only the two uniform sign
    # assignments attain abs(sum)>=6, so exact two-sided p = 2 / 64.
    return {
        "task": "paired_signflip", "treatment": [2]*6, "control": [1]*6,
        "pairing_key": "same-entity-and-horizon",
        "exchangeable_signs_under_null": True,
        "threshold_predeclared": True, "alpha": .05,
        "reported_p_value": 1/32,
    }


def mc():
    return {
        "task": "bernoulli_mc", "observations": [1]*50 + [0]*50,
        "sampling_scheme": "iid_bernoulli", "confidence_level": .95,
        "precision_predeclared": True, "max_ci_half_width": .12,
        "reported_probability": .5,
    }


def convex():
    # f(x,y) = x^2 + 2y^2 - 4x - 8y, box [0,5]^2.
    # Separate exact unconstrained minimum: (2,2) and f=-12.
    return {
        "task": "separable_convex_quadratic", "sense": "minimize",
        "quadratic": [1, 2], "linear": [-4, -8],
        "bounds": [[0, 5], [0, 5]],
        "candidate": [2, 2], "claimed_objective": -12,
    }


class RollingTimeTests(unittest.TestCase):
    def test_golden_fold_metrics(self):
        r = oracle.audit(rolling())
        self.assertEqual(r["status"], "recomputed_match", r)
        self.assertEqual((r["n_folds"], r["n_predictions"]), (2, 4))
        self.assertAlmostEqual(r["recomputed"]["rmse"], math.sqrt(7/4))

    def test_rejects_temporal_leakage(self):
        c = rolling()
        c["folds"][0]["train_end"] = 5
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_missing_required_gap(self):
        c = rolling()
        c["required_gap"] = 2
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_repeated_validation_horizon(self):
        c = rolling()
        c["folds"][1]["valid_start"] = 6
        c["folds"][1]["train_end"] = 4
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_incorrect_metric(self):
        c = rolling()
        c["reported"]["rmse"] = 1.25
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_wrong_horizon_count(self):
        c = rolling()
        c["folds"][1]["actual"] = [3]
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_shift_invariant_errors(self):
        c = rolling()
        for f in c["folds"]:
            f["actual"] = [x+500 for x in f["actual"]]
            f["predicted"] = [x+500 for x in f["predicted"]]
        self.assertEqual(oracle.audit(c)["status"], "recomputed_match")

    def test_series_are_scoped_independently(self):
        c = rolling()
        c["folds"][1]["series_id"] = "B"
        c["folds"][1]["train_end"] = 3
        c["folds"][1]["valid_start"] = 8
        self.assertEqual(oracle.audit(c)["status"], "recomputed_match")


class PairedInferenceTests(unittest.TestCase):
    def test_exact_golden_signflip(self):
        r = oracle.audit(paired())
        self.assertEqual(r["status"], "recomputed_match", r)
        self.assertEqual(r["enumerated_sign_patterns"], 64)
        self.assertAlmostEqual(r["exact_two_sided_p"], 1/32)
        self.assertTrue(r["nominally_significant"])

    def test_rejects_fake_p_value(self):
        c = paired()
        c["reported_p_value"] = .000001
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_unverified_exchangeability(self):
        c = paired()
        c["exchangeable_signs_under_null"] = False
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_no_effect_p_equals_one(self):
        c = paired()
        c["treatment"] = c["control"].copy()
        c["reported_p_value"] = 1
        r = oracle.audit(c)
        self.assertEqual(r["status"], "recomputed_match", r)
        self.assertFalse(r["nominally_significant"])

    def test_rejects_unpaired_or_oversized_sample(self):
        c = paired()
        c["control"].pop()
        self.assertEqual(oracle.audit(c)["status"], "blocked")
        c = paired()
        c["treatment"] = [2]*17
        c["control"] = [1]*17
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_unrecorded_threshold(self):
        c = paired()
        c["threshold_predeclared"] = False
        self.assertEqual(oracle.audit(c)["status"], "blocked")


class BernoulliSimulationTests(unittest.TestCase):
    def test_half_success_golden_wilson(self):
        r = oracle.audit(mc())
        self.assertEqual(r["status"], "precision_met", r)
        self.assertEqual((r["n"], r["successes"], r["probability"]), (100, 50, .5))
        self.assertAlmostEqual(sum(r["wilson_interval"])/2, .5)
        self.assertGreater(r["wilson_half_width"], .09)

    def test_precision_failure_without_fake_confidence(self):
        c = mc()
        c["max_ci_half_width"] = .05
        self.assertEqual(oracle.audit(c)["status"], "insufficient_precision")

    def test_non_iid_scheme_or_outcomes_blocked(self):
        c = mc()
        c["sampling_scheme"] = "dependent_markov_samples"
        self.assertEqual(oracle.audit(c)["status"], "blocked")
        c = mc()
        c["observations"][0] = .9
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_rejects_wrong_reported_probability(self):
        c = mc()
        c["reported_probability"] = .8
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_all_successes_interval_not_equal_one(self):
        c = mc()
        c["observations"] = [1]*100
        c["reported_probability"] = 1
        r = oracle.audit(c)
        self.assertEqual(r["status"], "precision_met")
        self.assertLess(r["wilson_interval"][0], 1)

    def test_missing_predeclaration_blocks(self):
        c = mc()
        c["precision_predeclared"] = False
        self.assertEqual(oracle.audit(c)["status"], "blocked")


class ConvexReferenceTests(unittest.TestCase):
    def test_hand_computed_optimum(self):
        r = oracle.audit(convex())
        self.assertEqual(r["status"], "analytic_optimum_match", r)
        self.assertEqual(r["analytic_witness"], [2, 2])
        self.assertEqual(r["analytic_optimal_objective"], -12)

    def test_feasible_suboptimal_candidate_is_detected(self):
        c = convex()
        c["candidate"] = [2, 3]
        c["claimed_objective"] = -10
        r = oracle.audit(c)
        self.assertEqual(r["status"], "disagreement", r)
        self.assertTrue(r["candidate_feasible"])
        self.assertAlmostEqual(r["objective_gap"], 2)

    def test_infeasible_candidate_is_detected(self):
        c = convex()
        c["candidate"] = [6, 2]
        c["claimed_objective"] = 4
        r = oracle.audit(c)
        self.assertEqual(r["status"], "disagreement")
        self.assertFalse(r["candidate_feasible"])

    def test_wrong_claimed_objective_blocked(self):
        c = convex()
        c["claimed_objective"] = 99
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_boundary_optimum(self):
        c = {"task": "separable_convex_quadratic", "sense": "minimize",
             "quadratic": [1], "linear": [-10], "bounds": [[0, 2]],
             "candidate": [2], "claimed_objective": -16}
        r = oracle.audit(c)
        self.assertEqual(r["status"], "analytic_optimum_match", r)
        self.assertEqual(r["analytic_witness"], [2])

    def test_invalid_nonconvex_quadratic_rejected(self):
        c = convex()
        c["quadratic"][0] = -1
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_wrong_dimensions_and_nan_rejected(self):
        c = convex()
        c["bounds"].pop()
        self.assertEqual(oracle.audit(c)["status"], "blocked")
        c = convex()
        c["candidate"][1] = float("nan")
        self.assertEqual(oracle.audit(c)["status"], "blocked")

    def test_common_constant_shift_metamorphic(self):
        c = convex()
        c["constant"] = 1234
        c["claimed_objective"] += 1234
        self.assertEqual(oracle.audit(c)["status"], "analytic_optimum_match")


if __name__ == "__main__":
    unittest.main()
