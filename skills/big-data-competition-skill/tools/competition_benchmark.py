#!/usr/bin/env python3
"""Offline task-plan adversarial checks for paper-first big-data competitions.

This validates methodological contracts, NOT model correctness or test accuracy.
Historical cases are scenario archetypes, not claims of reproduced solutions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

DEFAULT = Path(__file__).resolve().parents[1] / "benchmarks" / "mathorcup_scenarios.json"
FAMILIES = {"tabular", "temporal", "vision", "optimization", "network", "text", "simulation", "spatial", "statistical"}


def validate_plan(plan: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(plan, dict):
        return ["plan must be object"]
    family = plan.get("task_family")
    if family not in FAMILIES:
        errors.append("unknown task_family")
    if not isinstance(plan.get("baseline"), str) or not plan["baseline"].strip():
        errors.append("credible baseline required")
    if not isinstance(plan.get("metric"), str) or not plan["metric"].strip():
        errors.append("metric or explicit unknown required")
    if not isinstance(plan.get("problem_source"), str) or not plan["problem_source"].strip():
        errors.append("problem_source required")
    features = plan.get("features")
    if not isinstance(features, list):
        errors.append("features must be explicit list")
    else:
        names = set()
        for i, feature in enumerate(features):
            if not isinstance(feature, dict) or not feature.get("name"):
                errors.append(f"features[{i}] missing name")
                continue
            if feature["name"] in names:
                errors.append(f"duplicate feature name: {feature['name']}")
            names.add(feature["name"])
            if feature.get("available_at_prediction") is not True:
                errors.append(f"future/unknown feature availability: {feature['name']}")
    scheme = plan.get("validation_scheme")
    if family == "temporal" and scheme not in ("time", "group_time", "rolling_time"):
        errors.append("temporal prediction needs time-ordered validation scheme")
    if scheme in ("time", "group_time", "rolling_time") and plan.get("time_ordered") is not True:
        errors.append("time-ordered validation claimed but not verified")
    if scheme in ("group", "group_time", "spatial_group") and plan.get("group_disjoint") is not True:
        errors.append("group/entity-disjoint validation not verified")
    if family == "vision":
        if plan.get("near_duplicate_isolation") is not True:
            errors.append("visual entity/scene near-duplicate isolation is required")
        if plan.get("output_kind") == "segmentation" and plan.get("ground_truth_kind") == "bbox":
            if plan.get("weak_supervision_declared") is not True:
                errors.append("bbox cannot be treated as pixel-level segmentation ground truth")
            if plan.get("segmentation_gt_metric_claimed") is True:
                errors.append("cannot claim pixel-GT segmentation metric from bbox-only labels")
    if family == "optimization" and plan.get("feasibility_verified") is not True:
        errors.append("optimization needs explicit constraint-feasibility verification")
    result = plan.get("official_result")
    if not isinstance(result, dict) or type(result.get("required")) is not bool:
        errors.append("official_result.required must be boolean, after reading rules")
    elif result["required"] and result.get("template_checked") is not True:
        errors.append("official result template/schema not checked")
    for i, claim in enumerate(plan.get("claims", [])):
        if not isinstance(claim, dict):
            errors.append(f"claims[{i}] invalid")
        elif claim.get("numerical") is True and not claim.get("accepted_artifact"):
            errors.append(f"claims[{i}]: numeric claim without accepted evidence")
    return errors


def run_suite(suite: dict) -> dict:
    cases = suite.get("cases", [])
    if not isinstance(cases, list) or not cases:
        return {"status": "failed", "errors": ["benchmark cases missing"], "total": 0}
    actual = []
    seen = set()
    for c in cases:
        case_id = c.get("id")
        expected = c.get("expect")
        errors = validate_plan(c.get("plan"))
        if case_id in seen or not isinstance(case_id, str) or not case_id:
            errors.append("non-unique case ID")
        seen.add(case_id)
        if expected not in ("pass", "reject"):
            errors.append("invalid expected outcome")
        outcome = "reject" if errors else "pass"
        actual.append({"id": case_id, "expected": expected, "actual": outcome,
                       "matched": outcome == expected, "reasons": errors})
    passed = sum(x["matched"] for x in actual)
    return {"status": "passed" if passed == len(actual) else "failed",
            "total": len(actual), "matched": passed, "cases": actual,
            "scope": "synthetic methodological contract checks; no contest data or models run"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--suite", type=Path, default=DEFAULT)
    args = ap.parse_args(argv)
    try:
        suite = json.loads(args.suite.read_text(encoding="utf-8"))
        result = run_suite(suite)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"status": "failed", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 2


if __name__ == "__main__":
    sys.exit(main())
