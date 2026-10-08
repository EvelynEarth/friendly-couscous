#!/usr/bin/env python3
"""Independent, bounded numerical reference checks (Python stdlib only).

Supports held-out regression/classification metric recalculation from atomic
observations, and exhaustive tiny integer-linear optimization. Does not train
models, certify the dataset, or establish large-problem global optimality.
"""
from __future__ import annotations

import argparse
from itertools import product
import json
import math
from pathlib import Path
import sys

MAX_STATES = 100_000
METRICS = {
    "regression": ("mae", "rmse"),
    "classification": ("accuracy", "macro_precision", "macro_recall", "macro_f1"),
}


def real(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def numeric_sequence(values: object, name: str) -> list[float]:
    if not isinstance(values, list) or not values:
        raise ValueError(f"{name} must be a nonempty list")
    if any(not real(v) for v in values):
        raise ValueError(f"{name} has non-finite/non-numeric observations")
    return [float(v) for v in values]


def asserted_metric(actual: dict, expected: dict, name: str, atol: float) -> None:
    reported = actual.get(name)
    if not real(reported):
        raise ValueError(f"reported.{name} must be a finite numeric value")
    if not math.isclose(float(reported), expected[name], rel_tol=0, abs_tol=atol):
        raise ValueError(f"reported.{name} differs from independently computed value")


def check_regression(case: dict, atol: float) -> dict:
    y = numeric_sequence(case.get("actual"), "actual")
    p = numeric_sequence(case.get("predicted"), "predicted")
    if len(y) != len(p):
        raise ValueError("actual/predicted lengths differ")
    errors = [a - b for a, b in zip(y, p)]
    calculated = {
        "mae": math.fsum(abs(e) for e in errors) / len(errors),
        "rmse": math.sqrt(math.fsum(e * e for e in errors) / len(errors)),
    }
    reported = case.get("reported")
    if not isinstance(reported, dict) or set(reported) != set(calculated):
        raise ValueError("reported requires exactly mae and rmse")
    for name in calculated:
        asserted_metric(reported, calculated, name, atol)
    return {"status": "recomputed_match", "task": "regression", "n": len(y),
            "recomputed": calculated,
            "meaning": "Metrics recomputed from supplied observations; independent prediction validity is not established."}


def normalized_label(value: object) -> str | int:
    if type(value) not in (str, int) or (type(value) is str and not value):
        raise ValueError("classification labels must be nonempty strings or integers, not bools")
    return value


def check_classification(case: dict, atol: float) -> dict:
    labels = case.get("labels")
    if not isinstance(labels, list) or not labels:
        raise ValueError("nonempty declared labels required")
    normalized = [normalized_label(x) for x in labels]
    if len(set(map(lambda x: (type(x).__name__, x), normalized))) != len(normalized):
        raise ValueError("labels must be unique")
    y, p = case.get("actual"), case.get("predicted")
    if not isinstance(y, list) or not y or not isinstance(p, list) or len(y) != len(p):
        raise ValueError("nonempty, equal-length actual/predicted lists required")
    if any(type(x) is not type(normalized[0]) for x in normalized):
        raise ValueError("declared label types must match")
    if any(type(x) is not type(normalized[0]) or x not in normalized for x in y + p):
        raise ValueError("observed class is not in the fixed declared label set")
    matrix = [[0] * len(normalized) for _ in normalized]
    lookup = {label: i for i, label in enumerate(normalized)}
    for target, guess in zip(y, p):
        matrix[lookup[target]][lookup[guess]] += 1
    pres, recs, f1s = [], [], []
    for i in range(len(normalized)):
        tp = matrix[i][i]
        predicted_count = sum(row[i] for row in matrix)
        actual_count = sum(matrix[i])
        precision = tp / predicted_count if predicted_count else 0.0
        recall = tp / actual_count if actual_count else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        pres.append(precision)
        recs.append(recall)
        f1s.append(f1)
    calculated = {
        "accuracy": sum(matrix[i][i] for i in range(len(normalized))) / len(y),
        "macro_precision": math.fsum(pres) / len(normalized),
        "macro_recall": math.fsum(recs) / len(normalized),
        "macro_f1": math.fsum(f1s) / len(normalized),
    }
    reported = case.get("reported")
    if not isinstance(reported, dict) or set(reported) != set(calculated):
        raise ValueError("reported requires exactly accuracy/macro_precision/macro_recall/macro_f1")
    for name in calculated:
        asserted_metric(reported, calculated, name, atol)
    return {
        "status": "recomputed_match", "task": "classification", "n": len(y),
        "labels": normalized, "confusion_matrix_rows_actual_cols_predicted": matrix,
        "recomputed": calculated, "zero_division": 0,
        "meaning": "Metrics recomputed from labels; fixed labels include absent classes, which receive zero when undefined."
    }


def integers(value: object, name: str, length: int | None = None) -> list[int]:
    if (not isinstance(value, list) or not value or
            any(type(x) is not int for x in value)):
        raise ValueError(f"{name} must be nonempty list of exact integers")
    if length is not None and len(value) != length:
        raise ValueError(f"{name} vector dimensions differ")
    return value


def dot(a: list[int], b: list[int]) -> int:
    return sum(x * y for x, y in zip(a, b))


def opt_case(case: dict) -> dict:
    sense = case.get("sense")
    if sense not in ("maximize", "minimize"):
        raise ValueError("sense must be maximize or minimize")
    weights = integers(case.get("objective"), "objective")
    n = len(weights)
    bounds = case.get("bounds")
    if not isinstance(bounds, list) or len(bounds) != n:
        raise ValueError("one inclusive [low, high] integer bound per variable required")
    ranges, states = [], 1
    for i, interval in enumerate(bounds):
        if (not isinstance(interval, list) or len(interval) != 2 or
                any(type(x) is not int for x in interval)):
            raise ValueError(f"bounds[{i}] must contain exact integers")
        low, high = interval
        if low > high:
            raise ValueError(f"bounds[{i}] empty")
        width = high - low + 1
        states *= width
        if states > MAX_STATES:
            raise ValueError(f"exact enumeration exceeds hard limit of {MAX_STATES} states")
        ranges.append(range(low, high + 1))
    constraints = case.get("constraints")
    if not isinstance(constraints, list):
        raise ValueError("constraints must be list")
    parsed = []
    for i, c in enumerate(constraints):
        if not isinstance(c, dict) or c.get("op") not in ("le", "ge", "eq"):
            raise ValueError(f"constraints[{i}]: op must be le, ge or eq")
        w = integers(c.get("weights"), f"constraints[{i}].weights", n)
        rhs = c.get("rhs")
        if type(rhs) is not int:
            raise ValueError(f"constraints[{i}].rhs must be exact integer")
        parsed.append((c["op"], w, rhs))
    candidate = integers(case.get("candidate"), "candidate", n)
    claimed = case.get("claimed_objective")
    if type(claimed) is not int:
        raise ValueError("claimed_objective must be an exact integer")
    candidate_value = dot(weights, candidate)
    in_bounds = all(low <= x <= high for x, (low, high) in zip(candidate, bounds))

    def feasible(x):
        if not all(lo <= v <= hi for v, (lo, hi) in zip(x, bounds)):
            return False
        for op, w, rhs in parsed:
            score = dot(x, w)
            if not (score <= rhs if op == "le" else score >= rhs if op == "ge" else score == rhs):
                return False
        return True

    best = None
    witness = None
    feasible_count = 0
    for point in product(*ranges):
        if not feasible(point):
            continue
        feasible_count += 1
        score = dot(weights, point)
        if best is None or (score > best if sense == "maximize" else score < best):
            best, witness = score, list(point)
    if best is None:
        raise ValueError("the bounded integer model has no feasible solution")
    is_feasible = in_bounds and feasible(candidate)
    gap = (best - candidate_value) if sense == "maximize" else (candidate_value - best)
    matched = is_feasible and claimed == candidate_value and gap == 0
    return {
        "status": "exact_small_case_match" if matched else "disagreement",
        "task": "bounded_integer_linear", "states_enumerated": states,
        "feasible_states": feasible_count, "candidate_feasible": is_feasible,
        "recomputed_candidate_objective": candidate_value,
        "exact_optimal_objective": best, "exact_witness": witness,
        "objective_gap": gap if is_feasible else None,
        "reported_matches_recalculated": claimed == candidate_value,
        "meaning": "Exact exhaustive check of this bounded *small* instance only. No guarantee for large original models."
    }


def audit(case: object) -> dict:
    if not isinstance(case, dict):
        return {"status": "blocked", "errors": ["case must be JSON object"]}
    task = case.get("task")
    atol = case.get("absolute_tolerance", 1e-9)
    if type(atol) not in (int, float) or not math.isfinite(atol) or atol < 0 or atol > 1e-3:
        return {"status": "blocked", "errors": ["absolute_tolerance must be between 0 and 1e-3"]}
    try:
        if task == "regression":
            return check_regression(case, atol)
        if task == "classification":
            return check_classification(case, atol)
        if task == "bounded_integer_linear":
            return opt_case(case)
        raise ValueError(f"unsupported task: {task!r}")
    except (ValueError, OverflowError, ZeroDivisionError) as exc:
        return {"status": "blocked", "errors": [str(exc)]}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--case", type=Path, required=True, help="JSON of actual observations and model claims")
    args = p.parse_args(argv)
    try:
        case = json.loads(args.case.read_text(encoding="utf-8"))
        result = audit(case)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "blocked", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in ("recomputed_match", "exact_small_case_match") else 2


if __name__ == "__main__":
    sys.exit(main())
