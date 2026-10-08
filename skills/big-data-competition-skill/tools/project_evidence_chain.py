#!/usr/bin/env python3
"""Cross-module, fail-closed evidence-chain audit for paper-first competitions.

Requires actual artifact bytes, SHA-256 inventory, per-question review coverage,
independent numerical recomputation, and a strict source-file-backed paper claim.
It cannot prove a scientifically valid problem formulation or trusted data origin.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

from independent_oracle import audit as base_oracle
from extended_oracles import audit as extended_oracle
from paper_evidence_gate import audit_record as paper_audit
from result_invariant_gate import audit as invariant_audit
from solution_quality_gate import inspect as quality_audit
from stability_audit import audit as stability_audit

PASS_ORACLES = {"recomputed_match", "exact_small_case_match", "analytic_optimum_match", "precision_met"}
PASS_STATUSES = {"stable_under_tested_perturbations"}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def verified_path(root: Path, relative: object) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError("nonempty relative path required")
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"file missing or escapes evidence root: {relative}")
    return path


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def valid_number(value: object) -> bool:
    return type(value) in (float, int) and math.isfinite(value)


def numeric_fields(data: dict) -> dict[str, float]:
    """Read only the finite numeric leaf paths exposed by an oracle."""
    out = {}
    for k, v in data.items():
        if valid_number(v):
            out[k] = float(v)
        elif isinstance(v, dict):
            for nested, value in v.items():
                if valid_number(value):
                    out[f"{k}.{nested}"] = float(value)
    return out


def audit(manifest: object, root: Path) -> dict:
    errors: list[str] = []
    results: list[dict] = []
    if not isinstance(manifest, dict):
        return {"status": "blocked", "errors": ["project manifest must be a JSON object"], "questions": []}
    if manifest.get("schema_version") != 1:
        errors.append("schema_version must equal 1")
    if not isinstance(manifest.get("project_id"), str) or not manifest["project_id"].strip():
        errors.append("project_id is required")
    wanted = manifest.get("official_questions")
    if (not isinstance(wanted, list) or not wanted or
            any(not isinstance(q, str) or not q for q in wanted) or
            len(set(wanted)) != len(wanted)):
        errors.append("official_questions must be a nonempty list of unique IDs")
        wanted = []
    snapshot = manifest.get("files")
    trusted: dict[str, Path] = {}
    if not isinstance(snapshot, list) or not snapshot:
        errors.append("nonempty files SHA-256 inventory required")
        snapshot = []
    for item in snapshot:
        if not isinstance(item, dict):
            errors.append("file inventory contains non-object")
            continue
        name, digest = item.get("path"), item.get("sha256")
        if not isinstance(name, str) or name in trusted or not isinstance(digest, str):
            errors.append("file inventory requires unique path and SHA-256")
            continue
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            errors.append(f"invalid lowercase SHA-256 for {name}")
            continue
        try:
            path = verified_path(root, name)
            if sha256_bytes(path.read_bytes()) != digest:
                raise ValueError(f"SHA-256 differs from snapshot: {name}")
            trusted[name] = path
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    def required_json(path: object) -> object:
        if not isinstance(path, str) or path not in trusted:
            raise ValueError(f"missing SHA-verified JSON input: {path}")
        return read_json(trusted[path])

    try:
        quality_record = required_json(manifest.get("quality_record"))
        reviewed = quality_audit(quality_record)
        if reviewed.get("status") != "review_ready":
            errors.append("solution quality coverage is incomplete or reports failures")
        if not isinstance(quality_record, dict) or not isinstance(quality_record.get("questions"), list):
            errors.append("invalid quality review questions")
            observed = {}
        else:
            observed = {q.get("id"): q for q in quality_record["questions"] if isinstance(q, dict)}
            if set(observed) != set(wanted) or len(quality_record["questions"]) != len(wanted):
                errors.append("official question IDs do not match quality review IDs")
            for question in quality_record["questions"]:
                if not isinstance(question, dict):
                    continue
                for review in question.get("checks", {}).values():
                    if isinstance(review, dict) and review.get("status") == "passed":
                        evidence = review.get("artifact")
                        if evidence not in trusted:
                            errors.append(f"{question.get('id')}: review evidence not SHA-verified: {evidence}")
                for claim in question.get("claims", []):
                    if isinstance(claim, dict) and claim.get("artifact") not in trusted:
                        errors.append(f"{question.get('id')}: claim evidence not SHA-verified")
    except (OSError, ValueError, UnicodeError, json.JSONDecodeError, TypeError, AttributeError) as exc:
        errors.append(f"cannot verify quality record: {exc}")
    tasks = manifest.get("questions")
    if not isinstance(tasks, list) or len(tasks) != len(wanted):
        errors.append("questions must have exactly one entry per official question")
        tasks = tasks if isinstance(tasks, list) else []
    task_ids = [t.get("id") for t in tasks if isinstance(t, dict)]
    if len(task_ids) != len(tasks) or any(not isinstance(x, str) for x in task_ids) or len(set(x for x in task_ids if isinstance(x, str))) != len(task_ids) or set(x for x in task_ids if isinstance(x, str)) != set(wanted):
        errors.append("question entries missing, duplicate or not identical to official questions")
    for i, task in enumerate(tasks):
        item = {"id": task.get("id") if isinstance(task, dict) else f"invalid-{i}", "checks": {}}
        results.append(item)
        if not isinstance(task, dict):
            errors.append(f"questions[{i}]: object required")
            continue
        qid = item["id"]
        try:
            paper_record = required_json(task.get("paper_record"))
            if not isinstance(paper_record, dict):
                raise ValueError("accepted paper record must be an object")
            paper_result = paper_audit(paper_record, root, require_metric_source=True)
            item["checks"]["strict_paper_evidence"] = paper_result.get("status")
            if paper_result.get("status") != "trace_consistent" or not paper_result.get("metrics_source_verified"):
                errors.append(f"{qid}: accepted paper numerical evidence fails strict check")
            # The paper tool verifies its files against hashes in accepted_record;
            # we ALSO require those files to match the overall project snapshot.
            for artifact in paper_record.get("artifacts", []):
                if not isinstance(artifact, dict) or artifact.get("path") not in trusted:
                    errors.append(f"{qid}: paper artifact not in verified project file inventory")
                elif artifact.get("sha256") != sha256_bytes(trusted[artifact["path"]].read_bytes()):
                    errors.append(f"{qid}: paper artifact does not match project inventory")
            oracle_cfg = task.get("oracle")
            if not isinstance(oracle_cfg, dict):
                raise ValueError("every question needs a real independent oracle record; unsupported cases must escalate to human review")
            engine = oracle_cfg.get("engine")
            case = required_json(oracle_cfg.get("case"))
            if engine == "independent":
                computed = base_oracle(case)
            elif engine == "extended":
                computed = extended_oracle(case)
            else:
                raise ValueError("oracle engine must be independent or extended")
            item["checks"]["independent_oracle"] = computed.get("status")
            if computed.get("status") not in PASS_ORACLES:
                errors.append(f"{qid}: independent oracle blocked or disagrees: {computed.get('status')}")
            actual_metrics = paper_record.get("metrics")
            metric_map = task.get("metric_map")
            if not isinstance(actual_metrics, dict) or not actual_metrics:
                errors.append(f"{qid}: accepted record has no actual metrics")
            elif not isinstance(metric_map, dict) or set(metric_map) != set(actual_metrics):
                errors.append(f"{qid}: ALL paper metrics must map to independently recomputed numeric oracle outputs")
            else:
                reference = numeric_fields(computed)
                for claimed_metric, oracle_name in metric_map.items():
                    expected = reference.get(oracle_name)
                    observed_value = actual_metrics[claimed_metric]
                    if not valid_number(expected) or not valid_number(observed_value):
                        errors.append(f"{qid}: metric {claimed_metric} is not independently recomputed")
                    elif not math.isclose(expected, float(observed_value), rel_tol=1e-10, abs_tol=1e-12):
                        errors.append(f"{qid}: {claimed_metric} differs from independent {oracle_name}")
            check = task.get("invariants")
            if check is not None:
                if not isinstance(check, dict):
                    raise ValueError("invariants must be object")
                contract = required_json(check.get("contract"))
                result_name = check.get("result")
                result = required_json(result_name)
                # Bind the checked output values to the SAME atomic oracle input.
                # Otherwise a valid-looking but unrelated result can pass.
                links = check.get("result_links")
                values = result.get("values") if isinstance(result, dict) else None
                if not isinstance(links, dict) or not links or not isinstance(values, dict):
                    errors.append(f"{qid}: invariant result needs nonempty result_links to oracle atomic inputs")
                elif not isinstance(case, dict) or any(
                    not isinstance(k, str) or not isinstance(v, str) or k not in values
                    or v not in case or type(values[k]) is not type(case[v]) or values[k] != case[v]
                    for k, v in links.items()
                ):
                    errors.append(f"{qid}: invariant values differ from the independently recomputed oracle inputs")
                condition = invariant_audit(contract, result, trusted[result_name].read_bytes())
                item["checks"]["necessary_invariants"] = condition.get("status")
                if condition.get("status") != "necessary_checks_passed":
                    errors.append(f"{qid}: numeric result violates specified invariants or file snapshot")
            elif not isinstance(task.get("invariants_not_applicable_reason"), str) or len(task["invariants_not_applicable_reason"].strip()) < 20:
                errors.append(f"{qid}: invariants skipped without substantive scientific justification")
            stable = task.get("stability")
            if stable is not None:
                observation = stability_audit(required_json(stable))
                item["checks"]["stability"] = observation.get("status")
                if observation.get("status") not in PASS_STATUSES:
                    errors.append(f"{qid}: declared stability study failed or lacks data")
                stability_record = required_json(stable)
                anchor = task.get("stability_anchor_run_id")
                run_list = stability_record.get("runs") if isinstance(stability_record, dict) else None
                metric_name = stability_record.get("metric") if isinstance(stability_record, dict) else None
                matched = ([r for r in run_list if isinstance(r, dict) and r.get("run_id") == anchor]
                           if isinstance(run_list, list) and isinstance(anchor, str) else [])
                if (not isinstance(actual_metrics, dict) or metric_name not in actual_metrics
                    or len(matched) != 1 or not valid_number(matched[0].get("value"))
                    or not math.isclose(float(matched[0]["value"]), float(actual_metrics[metric_name]),
                                        rel_tol=1e-10, abs_tol=1e-12)):
                    errors.append(f"{qid}: stability anchor run and accepted metric do not match")
            elif not isinstance(task.get("stability_not_applicable_reason"), str) or len(task["stability_not_applicable_reason"].strip()) < 20:
                errors.append(f"{qid}: stability omitted without substantive scientific justification")
            # A successful machine audit DOES NOT certify mathematical assumptions,
            # independent provenance, or true scientific conclusions.
        except (OSError, ValueError, UnicodeError, json.JSONDecodeError, KeyError, TypeError, AttributeError, OverflowError) as exc:
            errors.append(f"{qid}: validation cannot complete: {exc}")
    return {
        "status": "blocked" if errors else "machine_evidence_consistent",
        "errors": errors, "questions": results,
        "questions_declared": len(wanted), "files_sha_verified": len(trusted),
        "scientific_approval": "human_scientific_review_still_required",
        "interpretation": "Cross-module consistency and necessary numerical checks only. It is NOT approval to publish or a proof of model correctness, data legality, causal inference or optimality."
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, required=True, help="JSON manifest enumerating all official questions and SHA-256-locked evidence inputs")
    p.add_argument("--artifact-root", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        result = audit(read_json(args.manifest), args.artifact_root)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "blocked", "errors": [str(exc)], "questions": []}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "machine_evidence_consistent" else 2


if __name__ == "__main__":
    sys.exit(main())
