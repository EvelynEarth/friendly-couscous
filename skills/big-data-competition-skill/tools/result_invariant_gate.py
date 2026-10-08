#!/usr/bin/env python3
"""Check user-declared numerical invariants against an actual hashed JSON result.

Domain-independent necessary conditions, NOT proof that the chosen model or
research claims are scientifically correct. No eval(), dynamic imports or code
execution. Define checks from the official problem *before* reviewing results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

OPS = {"bounds", "sum_close", "row_sum_close", "linear_le",
       "linear_ge", "monotonic", "equal_fields"}


def number(x):
    return type(x) in (int, float) and math.isfinite(x)


def vector(x):
    return isinstance(x, list) and bool(x) and all(number(y) for y in x)


def tolerance(check):
    x = check.get("tolerance", 0)
    if not number(x) or x < 0:
        raise ValueError("tolerance must be finite and nonnegative")
    return float(x)


def scalar_or_vector(x):
    if number(x):
        return [float(x)]
    if vector(x):
        return [float(y) for y in x]
    raise ValueError("expected a finite numeric scalar or nonempty vector")


def check_one(check, values):
    if not isinstance(check, dict):
        raise ValueError("check must be object")
    op = check.get("op")
    if op not in OPS:
        raise ValueError(f"unsupported invariant op: {op!r}")
    tol = tolerance(check)
    name = check.get("field")
    if not isinstance(name, str) or name not in values:
        raise ValueError("field not in result values")
    value = values[name]
    if op == "bounds":
        seq = scalar_or_vector(value)
        low, high = check.get("lower"), check.get("upper")
        if not number(low) or not number(high) or low > high:
            raise ValueError("bounds require finite lower <= upper")
        return all(low - tol <= x <= high + tol for x in seq), "value outside bounds"
    if op == "sum_close":
        seq = scalar_or_vector(value)
        target = check.get("target")
        if not number(target):
            raise ValueError("sum_close requires finite target")
        return abs(math.fsum(seq) - target) <= tol, "sum differs from target"
    if op == "row_sum_close":
        if not isinstance(value, list) or not value or not all(vector(row) for row in value):
            raise ValueError("row_sum_close requires nonempty matrix of finite vectors")
        target = check.get("target", 1)
        if not number(target):
            raise ValueError("row_sum_close target must be numeric")
        return all(abs(math.fsum(row) - target) <= tol for row in value), "at least one row sum differs"
    if op in ("linear_le", "linear_ge"):
        seq = scalar_or_vector(value)
        weights, rhs = check.get("weights"), check.get("rhs")
        if not vector(weights) or len(weights) != len(seq) or not number(rhs):
            raise ValueError("linear check requires matched finite weights and rhs")
        lhs = math.fsum(a * b for a, b in zip(seq, weights))
        valid = lhs <= rhs + tol if op == "linear_le" else lhs >= rhs - tol
        return valid, "linear constraint violated"
    if op == "monotonic":
        seq = scalar_or_vector(value)
        direction = check.get("direction")
        if direction not in ("nondecreasing", "nonincreasing"):
            raise ValueError("monotonic requires nondecreasing/nonincreasing direction")
        pairs = zip(seq, seq[1:])
        valid = all(a <= b + tol if direction == "nondecreasing"
                    else a >= b - tol for a, b in pairs)
        return valid, "sequence monotonicity violated"
    if op == "equal_fields":
        other = check.get("other_field")
        if not isinstance(other, str) or other not in values:
            raise ValueError("equal_fields requires another existing field")
        left, right = scalar_or_vector(value), scalar_or_vector(values[other])
        if len(left) != len(right):
            return False, "fields differ in length"
        return all(abs(a - b) <= tol for a, b in zip(left, right)), "fields differ"
    raise AssertionError("unreachable")


def audit(contract: object, result: object, raw_bytes: bytes) -> dict:
    problems, cases = [], []
    if not isinstance(contract, dict) or not isinstance(result, dict):
        return {"status": "blocked", "errors": ["contract and result must be JSON objects"]}
    expected = contract.get("result_sha256")
    actual = hashlib.sha256(raw_bytes).hexdigest()
    if not isinstance(expected, str) or len(expected) != 64 or expected != actual:
        problems.append("actual result file SHA-256 does not match contract")
    if not isinstance(contract.get("case_id"), str) or not contract["case_id"].strip():
        problems.append("nonempty official case_id required")
    vals = result.get("values")
    if not isinstance(vals, dict) or not vals:
        problems.append("result must contain nonempty values object")
        vals = {}
    checks = contract.get("invariants")
    if not isinstance(checks, list) or not checks:
        problems.append("nonempty invariants required")
        checks = []
    used = set()
    for i, item in enumerate(checks):
        check_id = item.get("id") if isinstance(item, dict) else None
        if not isinstance(check_id, str) or not check_id or check_id in used:
            problems.append(f"invariants[{i}] needs unique, nonempty id")
        used.add(check_id)
        try:
            valid, reason = check_one(item, vals)
            cases.append({"id": check_id, "passed": valid,
                          "reason": "satisfied" if valid else reason})
        except (ValueError, TypeError, OverflowError) as exc:
            problems.append(f"invariants[{i}]: {exc}")
    failed = [row for row in cases if not row["passed"]]
    return {
        "status": "blocked" if problems or failed else "necessary_checks_passed",
        "errors": problems, "checks": cases, "failed_invariants": len(failed),
        "meaning": "Necessary numeric conditions only; no guarantee of correct task formulation, model, data, or optimality."
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        raw = args.result.read_bytes()
        contract = json.loads(args.contract.read_text(encoding="utf-8"))
        result = json.loads(raw.decode("utf-8"))
        outcome = audit(contract, result, raw)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        outcome = {"status": "blocked", "errors": [str(exc)]}
    print(json.dumps(outcome, ensure_ascii=False, indent=2))
    return 0 if outcome["status"] == "necessary_checks_passed" else 2


if __name__ == "__main__":
    sys.exit(main())
