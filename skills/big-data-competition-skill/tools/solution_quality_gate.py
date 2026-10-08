#!/usr/bin/env python3
"""Generic, evidence-oriented solution quality *coverage* audit.

This verifies recorded checks and their evidence pointers, not scientific truth.
Problem-specific tests still require independent human/computational verification.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

GENERAL = (
    "question_answer_alignment",
    "assumptions_and_domain",
    "units_and_boundary_cases",
    "independent_verification",
    "baseline_or_reference",
    "uncertainty_and_error",
    "stability_and_sensitivity",
    "claim_evidence_alignment",
)
CONDITIONAL = {
    "prediction": ("evaluation_design", "leakage_control"),
    "causal": ("identification_and_confounding",),
    "optimization": ("constraint_feasibility", "optimality_or_gap"),
    "simulation": ("randomness_and_convergence",),
    "inference": ("identifiability_and_uncertainty",),
}
OBJECTIVES = {"description", "prediction", "inference", "optimization",
              "simulation", "causal", "evaluation", "explanation", "mixed"}


def inspect(data: object) -> dict:
    errors: list[str] = []
    issues: list[dict] = []
    if not isinstance(data, dict):
        return {"status": "blocked", "errors": ["root must be object"], "issues": []}
    items = data.get("questions")
    if not isinstance(items, list) or not items:
        return {"status": "blocked", "errors": ["nonempty questions list required"], "issues": []}
    seen: set[str] = set()
    for index, task in enumerate(items):
        prefix = f"questions[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{prefix}: not an object")
            continue
        qid = task.get("id")
        if not isinstance(qid, str) or not qid.strip() or qid in seen:
            errors.append(f"{prefix}: missing or duplicate question id")
            continue
        seen.add(qid)
        objective = task.get("objective")
        if objective not in OBJECTIVES:
            errors.append(f"{qid}: invalid objective")
            continue
        for key in ("expected_output", "actual_output", "model_rationale"):
            if not isinstance(task.get(key), str) or not task[key].strip():
                errors.append(f"{qid}: nonempty {key} required")
        if not isinstance(task.get("limitations"), list) or not task["limitations"]:
            errors.append(f"{qid}: explicit limitations required")
        checks = task.get("checks")
        if not isinstance(checks, dict):
            errors.append(f"{qid}: checks must be an object")
            continue
        mandatory = (*GENERAL, *CONDITIONAL.get(objective, ()))
        for name in mandatory:
            item = checks.get(name)
            if not isinstance(item, dict):
                issues.append({"question": qid, "check": name, "severity": "blocking",
                               "reason": "missing review check"})
                continue
            status = item.get("status")
            if status == "passed":
                if not isinstance(item.get("method"), str) or not item["method"].strip():
                    issues.append({"question": qid, "check": name, "severity": "blocking",
                                   "reason": "passed check requires described verification method"})
                if not isinstance(item.get("artifact"), str) or not item["artifact"].strip():
                    issues.append({"question": qid, "check": name, "severity": "blocking",
                                   "reason": "passed check requires evidence artifact reference"})
                if name == "independent_verification" and item.get("independent") is not True:
                    issues.append({"question": qid, "check": name, "severity": "blocking",
                                   "reason": "independent check must be explicitly independent"})
            elif status == "not_applicable":
                # An explanation is required, and key task-specific checks cannot be waived.
                if not isinstance(item.get("reason"), str) or len(item["reason"].strip()) < 12:
                    issues.append({"question": qid, "check": name, "severity": "blocking",
                                   "reason": "not_applicable requires a substantive rationale"})
                if name in CONDITIONAL.get(objective, ()) or name in (
                    "question_answer_alignment", "independent_verification", "claim_evidence_alignment"):
                    issues.append({"question": qid, "check": name, "severity": "blocking",
                                   "reason": "this essential check cannot be waived"})
            elif status in ("failed", "pending", "unknown"):
                issues.append({"question": qid, "check": name, "severity": "blocking",
                               "reason": f"verification status is {status}"})
            else:
                issues.append({"question": qid, "check": name, "severity": "blocking",
                               "reason": "invalid verification status"})
        claims = task.get("claims")
        if not isinstance(claims, list) or not claims:
            errors.append(f"{qid}: conclusions must be recorded as claims")
            continue
        for j, claim in enumerate(claims):
            if not isinstance(claim, dict):
                errors.append(f"{qid}: claims[{j}] must be an object")
                continue
            if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
                errors.append(f"{qid}: claims[{j}] missing statement")
            if not isinstance(claim.get("artifact"), str) or not claim["artifact"].strip():
                errors.append(f"{qid}: claims[{j}] missing evidence artifact")
            if claim.get("strength") not in ("observed", "predictive", "associational",
                                             "causal", "optimal", "qualified"):
                errors.append(f"{qid}: claims[{j}] strength invalid")
            if claim.get("strength") == "causal" and objective != "causal":
                issues.append({"question": qid, "check": "claim_scope", "severity": "blocking",
                               "reason": "causal claim without causal-identification task"})
            if claim.get("strength") == "optimal" and objective != "optimization":
                issues.append({"question": qid, "check": "claim_scope", "severity": "blocking",
                               "reason": "global optimality claimed outside optimization task"})
            if claim.get("status") != "supported":
                issues.append({"question": qid, "check": "claim_evidence", "severity": "blocking",
                               "reason": "claim not supported or not yet reviewed"})
    return {
        "status": "blocked" if errors or issues else "review_ready",
        "errors": errors, "issues": issues,
        "questions_checked": len(items),
        "meaning": "Review coverage only: does not establish mathematical, statistical or scientific truth."
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        result = inspect(json.loads(args.record.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        result = {"status": "blocked", "errors": [str(exc)], "issues": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "review_ready" else 2


if __name__ == "__main__":
    sys.exit(main())
