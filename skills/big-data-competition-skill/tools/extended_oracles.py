#!/usr/bin/env python3
"""Independent small-reference checks for time-series, paired inference,
iid Bernoulli simulation, and box-constrained separable convex optimization.

Only checks supplied atomic observations or stated mathematical problems.
No scientific claim is proved without verifying inputs, assumptions and scope.
Python standard library, deterministic, no external services.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
import math
from pathlib import Path
from statistics import NormalDist
import sys

MAX_FOLDS = 1000
MAX_PAIRS = 16
MAX_OBSERVATIONS = 200000
MAX_VARIABLES = 1000


def finite(v: object) -> bool:
    return type(v) in (int, float) and math.isfinite(v)


def nonempty_numbers(v: object, label: str) -> list[float]:
    if not isinstance(v, list) or not v or len(v) > MAX_OBSERVATIONS or any(not finite(x) for x in v):
        raise ValueError(f"{label} must be a bounded, nonempty list of finite numbers")
    return [float(x) for x in v]


def tolerance(d: dict) -> float:
    t = d.get("absolute_tolerance", 1e-9)
    if not finite(t) or not 0 <= t <= 1e-3:
        raise ValueError("absolute_tolerance must be between 0 and 1e-3")
    return float(t)


def scalar_match(reported: object, actual: float, tol: float, label: str) -> None:
    if not finite(reported) or not math.isclose(float(reported), actual, rel_tol=0, abs_tol=tol):
        raise ValueError(f"reported {label} differs from independently recomputed value")


def rolling_forecast(data: dict) -> dict:
    folds = data.get("folds")
    if not isinstance(folds, list) or not 2 <= len(folds) <= MAX_FOLDS:
        raise ValueError("rolling forecast requires 2..1000 folds")
    gap = data.get("required_gap", 0)
    if type(gap) is not int or gap < 0:
        raise ValueError("required_gap must be a nonnegative integer")
    previous: dict[str, tuple[int, int]] = {}
    absolute_errors: list[float] = []
    squared_errors: list[float] = []
    fold_results = []
    for i, fold in enumerate(folds):
        if not isinstance(fold, dict):
            raise ValueError(f"fold[{i}] must be object")
        key = fold.get("series_id")
        if not isinstance(key, str) or not key:
            raise ValueError(f"fold[{i}] requires nonempty series_id")
        bounds = [fold.get(s) for s in ("train_start", "train_end", "valid_start", "valid_end")]
        if any(type(x) is not int for x in bounds):
            raise ValueError(f"fold[{i}] time coordinates must be integers")
        a, b, c, d = bounds
        if not a <= b < c <= d or c - b - 1 < gap:
            raise ValueError(f"fold[{i}] has overlapping or improperly gapped training/validation")
        if key in previous:
            old_train_end, old_valid_end = previous[key]
            if b <= old_train_end or c <= old_valid_end:
                raise ValueError(f"fold[{i}] must have strictly advancing train and nonoverlapping validation windows")
        previous[key] = (b, d)
        y = nonempty_numbers(fold.get("actual"), f"fold[{i}].actual")
        p = nonempty_numbers(fold.get("predicted"), f"fold[{i}].predicted")
        if len(y) != len(p) or len(y) != d-c+1:
            raise ValueError(f"fold[{i}] horizon and observations differ")
        errors = [u-v for u, v in zip(y, p)]
        absolute_errors.extend(abs(e) for e in errors)
        squared_errors.extend(e*e for e in errors)
        fold_results.append({"series_id": key, "valid_start": c, "valid_end": d,
                             "mae": math.fsum(abs(e) for e in errors)/len(errors)})
    mae = math.fsum(absolute_errors)/len(absolute_errors)
    rmse = math.sqrt(math.fsum(squared_errors)/len(squared_errors))
    reported = data.get("reported")
    if not isinstance(reported, dict) or set(reported) != {"mae", "rmse"}:
        raise ValueError("reported must have exactly mae and rmse")
    tol = tolerance(data)
    scalar_match(reported["mae"], mae, tol, "MAE")
    scalar_match(reported["rmse"], rmse, tol, "RMSE")
    return {"status": "recomputed_match", "task": "rolling_forecast",
            "n_predictions": len(absolute_errors), "n_folds": len(folds),
            "required_gap": gap, "recomputed": {"mae": mae, "rmse": rmse},
            "folds": fold_results,
            "interpretation": "Checks declared integer-index fold boundaries and raw forecast errors, not feature timestamps, leakage within preprocessing, or future generalization."}


def paired_signflip(data: dict) -> dict:
    x = nonempty_numbers(data.get("treatment"), "treatment")
    y = nonempty_numbers(data.get("control"), "control")
    n = len(x)
    if n != len(y) or not 2 <= n <= MAX_PAIRS:
        raise ValueError(f"exact paired sign-flip requires 2..{MAX_PAIRS} matched pairs")
    if not isinstance(data.get("pairing_key"), str) or not data["pairing_key"].strip():
        raise ValueError("explicit pairing_key required")
    if data.get("exchangeable_signs_under_null") is not True:
        raise ValueError("assumption of sign-exchangeability under the null must be declared")
    if data.get("threshold_predeclared") is not True:
        raise ValueError("alpha must be set before looking at data (self-report must be independently checked)")
    alpha = data.get("alpha")
    if not finite(alpha) or not 0 < alpha < 1:
        raise ValueError("alpha must lie strictly between 0 and 1")
    diffs = [a-b for a, b in zip(x, y)]
    observed = abs(math.fsum(diffs))
    extremal = 0
    for signs in product((-1, 1), repeat=n):
        value = abs(math.fsum(d*s for d, s in zip(diffs, signs)))
        if value >= observed - 1e-12*max(1, observed):
            extremal += 1
    p = extremal/(2**n)
    mean = math.fsum(diffs)/n
    scalar_match(data.get("reported_p_value"), p, tolerance(data), "sign-flip p-value")
    return {"status": "recomputed_match", "task": "paired_signflip",
            "pairs": n, "mean_paired_difference": mean,
            "exact_two_sided_p": p, "alpha": float(alpha),
            "nominally_significant": p <= alpha, "enumerated_sign_patterns": 2**n,
            "interpretation": "Exact under a valid sign-exchangeability null; pairing, independence of units, multiplicity, causal identification, and predeclaration are not independently certified."}


def bernoulli_mc(data: dict) -> dict:
    observations = data.get("observations")
    if not isinstance(observations, list) or not 2 <= len(observations) <= MAX_OBSERVATIONS:
        raise ValueError("iid Bernoulli estimate requires 2..200000 atomic outcomes")
    if any(type(x) is not int or x not in (0, 1) for x in observations):
        raise ValueError("observations must be exact integer 0/1 (not booleans, weights or probabilities)")
    if data.get("sampling_scheme") != "iid_bernoulli":
        raise ValueError("sampling_scheme must declare independent identically distributed Bernoulli draws")
    confidence = data.get("confidence_level")
    if not finite(confidence) or not 0.5 < confidence < 0.99999:
        raise ValueError("confidence_level must be between 0.5 and 0.99999")
    target = data.get("max_ci_half_width")
    if not finite(target) or not 0 < target < 0.5:
        raise ValueError("max_ci_half_width must be between 0 and 0.5")
    if data.get("precision_predeclared") is not True:
        raise ValueError("required precision must be declared before seeing outcomes")
    n = len(observations)
    k = sum(observations)
    phat = k/n
    z = NormalDist().inv_cdf((1 + confidence)/2)
    den = 1 + z*z/n
    center = (phat + z*z/(2*n))/den
    half = z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))/den
    scalar_match(data.get("reported_probability"), phat, tolerance(data), "Bernoulli probability")
    satisfied = half <= target
    return {"status": "precision_met" if satisfied else "insufficient_precision",
            "task": "bernoulli_mc", "n": n, "successes": k, "probability": phat,
            "confidence_level": confidence, "wilson_interval": [max(0, center-half), min(1, center+half)],
            "wilson_half_width": half, "declared_max_half_width": target,
            "interpretation": "Wilson interval for iid Bernoulli observations; iid/source randomness, coverage under data reuse and simulation-model validity are not proven."}


def separable_convex(data: dict) -> dict:
    if data.get("sense") != "minimize":
        raise ValueError("separable convex quadratic oracle supports minimization only")
    a = nonempty_numbers(data.get("quadratic"), "quadratic")
    b = nonempty_numbers(data.get("linear"), "linear")
    x = nonempty_numbers(data.get("candidate"), "candidate")
    n = len(a)
    if n > MAX_VARIABLES or len(b) != n or len(x) != n or any(v <= 0 for v in a):
        raise ValueError("quadratic terms must be positive, with matched vector dimensions <=1000")
    bounds = data.get("bounds")
    if not isinstance(bounds, list) or len(bounds) != n:
        raise ValueError("must supply one inclusive [lower,upper] pair per variable")
    lo, hi = [], []
    for i, item in enumerate(bounds):
        if not isinstance(item, list) or len(item) != 2 or any(not finite(y) for y in item):
            raise ValueError(f"bounds[{i}] must have finite lower and upper")
        lower, upper = map(float, item)
        if lower > upper:
            raise ValueError(f"bounds[{i}] lower exceeds upper")
        lo.append(lower)
        hi.append(upper)
    constant = data.get("constant", 0)
    if not finite(constant):
        raise ValueError("finite constant required")
    optimum = [max(lower, min(upper, -lin/(2*quad)))
               for quad, lin, lower, upper in zip(a, b, lo, hi)]
    objective = lambda v: math.fsum(q*z*z + t*z for q, t, z in zip(a, b, v)) + constant
    actual = objective(x)
    reference = objective(optimum)
    tol = tolerance(data)
    scalar_match(data.get("claimed_objective"), actual, tol, "quadratic objective")
    feasible = all(lower-tol <= v <= upper+tol for v, lower, upper in zip(x, lo, hi))
    gap = actual-reference
    matched = feasible and gap <= tol and gap >= -tol
    return {
        "status": "analytic_optimum_match" if matched else "disagreement",
        "task": "separable_convex_quadratic", "dimensions": n,
        "candidate_feasible": feasible, "recomputed_candidate_objective": actual,
        "analytic_optimal_objective": reference, "analytic_witness": optimum,
        "objective_gap": gap if feasible else None,
        "interpretation": "Exact clipped-coordinate analytic optimum for stated separable positive-quadratic box model, not any general continuous nonlinear optimization."
    }


def audit(case: object) -> dict:
    if not isinstance(case, dict):
        return {"status": "blocked", "errors": ["case must be a JSON object"]}
    try:
        modes = {
            "rolling_forecast": rolling_forecast,
            "paired_signflip": paired_signflip,
            "bernoulli_mc": bernoulli_mc,
            "separable_convex_quadratic": separable_convex,
        }
        task = case.get("task")
        if task not in modes:
            raise ValueError(f"unsupported reference oracle: {task!r}")
        return modes[task](case)
    except (ValueError, TypeError, OverflowError, ZeroDivisionError) as exc:
        return {"status": "blocked", "errors": [str(exc)]}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        payload = json.loads(args.case.read_text(encoding="utf-8"))
        result = audit(payload)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "blocked", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in ("recomputed_match", "precision_met", "analytic_optimum_match") else 2


if __name__ == "__main__":
    sys.exit(main())
