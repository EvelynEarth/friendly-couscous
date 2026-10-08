#!/usr/bin/env python3
"""Calculate actual repeated-run stability without fabricating significance.

Use real runs obtained with a locked evaluation protocol. Thresholds must be
defined *before* inspecting results. Descriptive statistics are NOT CIs.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics
import sys


def finite(x: object) -> bool:
    return type(x) in (int, float) and math.isfinite(float(x))


def audit(payload: object) -> dict:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return {"status": "blocked", "errors": ["root must be an object"]}
    for key in ("metric", "protocol_id", "data_version", "perturbation"):
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            errors.append(f"{key} is required")
    if payload.get("direction") not in ("maximize", "minimize"):
        errors.append("direction must be maximize or minimize")
    threshold = payload.get("max_range")
    if not finite(threshold) or (finite(threshold) and threshold < 0):
        errors.append("nonnegative predeclared max_range required")
    if payload.get("threshold_predeclared") is not True:
        errors.append("threshold_predeclared must be true (verify it was set before seeing results)")
    runs = payload.get("runs")
    if not isinstance(runs, list) or len(runs) < 3:
        errors.append("at least three real repeated measurements required")
        runs = runs if isinstance(runs, list) else []
    values, baseline, ids = [], [], set()
    baseline_present = any(isinstance(r, dict) and "baseline_value" in r for r in runs)
    for i, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"runs[{i}] must be object")
            continue
        run_id = run.get("run_id")
        if not isinstance(run_id, str) or not run_id.strip() or run_id in ids:
            errors.append(f"runs[{i}] requires unique run_id")
        ids.add(run_id)
        if not finite(run.get("value")):
            errors.append(f"runs[{i}] value must be finite")
        else:
            values.append(float(run["value"]))
        if baseline_present:
            if not finite(run.get("baseline_value")):
                errors.append(f"runs[{i}] needs paired, finite baseline_value")
            else:
                baseline.append(float(run["baseline_value"]))
    if payload.get("claim_improvement") is True and not baseline_present:
        errors.append("improvement claim requires paired baseline measurements")
    min_gain = payload.get("min_paired_gain")
    if min_gain is not None and (not finite(min_gain) or min_gain < 0):
        errors.append("min_paired_gain must be finite and nonnegative")
    if payload.get("claim_improvement") is True and min_gain is None:
        errors.append("improvement claim requires predeclared min_paired_gain")
    if errors:
        return {"status": "blocked", "errors": errors,
                "meaning": "No numerical stability claim is allowed."}
    lo, hi = min(values), max(values)
    span = hi - lo
    std = statistics.stdev(values)
    mean = statistics.mean(values)
    result = {
        "status": "stable_under_tested_perturbations" if span <= threshold else "unstable",
        "metric": payload["metric"], "n": len(values), "mean": mean,
        "sample_sd": std, "minimum": lo, "maximum": hi, "observed_range": span,
        "allowed_range": threshold, "perturbation": payload["perturbation"],
        "baseline_comparison": "not_requested",
        "meaning": "Descriptive repeated-run stability only; not a confidence interval, proof of global stability, or accuracy validation."
    }
    if baseline_present:
        sign = 1 if payload.get("direction") == "maximize" else -1
        differences = [(a-b)*sign for a, b in zip(values, baseline)]
        result["baseline_comparison"] = {
            "paired_count": len(differences),
            "mean_gain": statistics.mean(differences),
            "min_gain": min(differences),
            "win_fraction": sum(x > 0 for x in differences) / len(differences),
            "interpretation": "Paired differences are descriptive, not a significance test."
        }
        if payload.get("claim_improvement") is True:
            supports = min(differences) >= min_gain
            result["baseline_comparison"]["meets_predeclared_min_gain_all_runs"] = supports
            if not supports:
                result["status"] = "unsupported_improvement_claim"
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        result = audit(json.loads(args.record.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "blocked", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "stable_under_tested_perturbations" else 2


if __name__ == "__main__":
    sys.exit(main())
