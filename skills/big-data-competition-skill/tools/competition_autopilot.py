#!/usr/bin/env python3
"""Persistent, fail-closed stage router for paper-first competition agents.

This is a local workflow controller, NOT an unattended LLM or training service.
It reads agent-produced review reports and real file hashes, then routes/retries.
Scientific validity and real approvals are outside the mechanical controller.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

STAGES = (
    "intake", "contract", "data", "plan", "baseline", "solve",
    "verify", "robustness", "figures", "paper", "final", "delivery",
)
CHECKS = {
    "contract": ("all_questions_mapped", "outputs_and_rules_mapped", "unknowns_identified"),
    "data": ("files_readable", "data_dictionary_checked", "leakage_risks_reviewed"),
    "plan": ("method_matches_problem", "assumptions_reviewed", "baseline_defined"),
    "baseline": ("baseline_actually_executed", "baseline_result_traced"),
    "solve": ("implementation_matches_math", "actual_execution_recorded", "outputs_match_task"),
    "verify": ("independent_check_performed", "information_availability_reviewed", "constraints_or_invariants_checked"),
    "robustness": ("uncertainty_assessed", "perturbations_or_limitations_recorded"),
    "figures": ("figures_derived_from_actual_data", "figure_claims_checked"),
    "paper": ("all_questions_answered", "claim_evidence_chain_checked", "numerical_provenance_checked"),
    "final": ("scientific_review_completed", "editorial_review_completed", "official_format_reviewed"),
    "delivery": ("official_deliverables_verified", "output_files_verified"),
}
NON_WAIVABLE = {
    "all_questions_mapped", "outputs_and_rules_mapped", "method_matches_problem",
    "baseline_actually_executed", "actual_execution_recorded", "outputs_match_task",
    "independent_check_performed", "all_questions_answered", "claim_evidence_chain_checked",
    "scientific_review_completed", "official_deliverables_verified",
}
DOCS = {
    "contract": "references/problem-framing.md",
    "data": "references/data-audit.md",
    "plan": "references/method-selection.md",
    "baseline": "references/method-selection.md",
    "solve": "references/solution-validity.md",
    "verify": "references/independent-recomputation.md",
    "robustness": "references/stability-and-uncertainty.md",
    "figures": "references/figure-evidence.md",
    "paper": "references/paper-argumentation.md",
    "final": "references/final-review.md",
    "delivery": "references/competition-final-runbook.md",
}
FAIL_BACKTRACK = {
    "task_mismatch": "contract",
    "data_quality": "data",
    "leakage": "data",
    "model_invalid": "plan",
    "implementation": "solve",
    "unstable": "solve",
    "evidence_missing": "verify",
    "plot_mismatch": "figures",
    "paper_mismatch": "paper",
    "delivery_noncompliance": "final",
}
HUMAN_GATE = {"plan", "delivery"}
STATE_FILE = "autopilot-state.json"
MAX_INPUT_FILES = 50000
DEFAULT_RETRY_BUDGET = 3


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def valid_rel(root: Path, name: object, *, must_exist: bool = True) -> Path:
    if not isinstance(name, str) or not name.strip() or Path(name).is_absolute():
        raise ValueError("expected nonempty relative artifact path")
    root = root.resolve()
    candidate = root / name
    if candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
        raise ValueError(f"unsafe artifact path: {name}")
    if must_exist and (not candidate.is_file() or candidate.stat().st_size == 0):
        raise ValueError(f"missing or empty evidence artifact: {name}")
    return candidate


def inputs_snapshot(folder: Path, workspace: Path) -> dict[str, str]:
    folder, workspace = folder.resolve(), workspace.resolve()
    if not folder.is_dir() or workspace == folder or workspace.is_relative_to(folder):
        raise ValueError("inputs must be an existing folder outside the workspace")
    files = sorted(p for p in folder.rglob("*") if p.is_file() or p.is_symlink())
    if not files or len(files) > MAX_INPUT_FILES:
        raise ValueError("input folder must contain 1..50000 files; batch larger datasets explicitly")
    snapshot = {}
    for file in files:
        if file.is_symlink() or not file.resolve().is_relative_to(folder):
            raise ValueError(f"unsafe input symlink: {file}")
        snapshot[file.relative_to(folder).as_posix()] = digest(file)
    return snapshot


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save(workspace: Path, state: dict) -> None:
    workspace.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".autopilot-", suffix=".tmp", dir=workspace)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(tmp, workspace / STATE_FILE)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def load(workspace: Path) -> dict:
    path = workspace / STATE_FILE
    state = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise ValueError("unsupported autopilot state")
    return state


def event(state: dict, name: str, message: str) -> None:
    state["history"].append({"at": now(), "type": name, "message": message})


def init(workspace: Path, input_folder: Path, retry_budget: int = DEFAULT_RETRY_BUDGET) -> dict:
    if (workspace / STATE_FILE).exists():
        raise ValueError("existing project state: use run/status/sync-inputs, not init")
    if not 1 <= retry_budget <= 10:
        raise ValueError("retry budget must be 1..10")
    files = inputs_snapshot(input_folder, workspace)
    state = {
        "schema_version": 1, "inputs_directory": str(input_folder.resolve()),
        "inputs": files, "retry_budget": retry_budget, "attempts": {},
        "completed": {"intake": {"input_files": len(files)}},
        "approvals": {}, "stale": {}, "history": [], "escalation": None,
    }
    event(state, "init", f"hashed {len(files)} submitted file(s), intake recorded")
    save(workspace, state)
    return state


def reset_from(state: dict, stage: str, reason: str) -> None:
    target = STAGES.index(stage)
    for completed, record in list(state["completed"].items()):
        if STAGES.index(completed) >= target:
            if isinstance(record, dict) and record.get("report_hash"):
                state["stale"][completed] = record["report_hash"]
            del state["completed"][completed]
    for name in list(state["approvals"]):
        if STAGES.index(name) >= target:
            del state["approvals"][name]
    event(state, "invalidate", f"from {stage}: {reason}")


def report_path(workspace: Path, stage: str) -> Path:
    return workspace / "reviews" / (stage + ".json")


def review(stage: str, report: object, workspace: Path) -> tuple[dict[str, str], list[str]]:
    errors = []
    if not isinstance(report, dict) or report.get("stage") != stage:
        return {}, ["review stage mismatch or non-object"]
    if report.get("decision") != "passed":
        return {}, ["review not marked passed"]
    checks = report.get("checks")
    if not isinstance(checks, dict) or set(checks) != set(CHECKS[stage]):
        return {}, ["review checks must exactly match stage requirements"]
    artifacts = report.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts or len(set(map(str, artifacts))) != len(artifacts):
        return {}, ["nonempty unique evidence artifact list required"]
    hashes = {}
    for path in artifacts:
        try:
            file = valid_rel(workspace, path)
            hashes[path] = digest(file)
        except (ValueError, OSError) as exc:
            errors.append(str(exc))
    for key in CHECKS[stage]:
        check = checks[key]
        if not isinstance(check, dict):
            errors.append(f"{key}: invalid check record")
            continue
        status = check.get("status")
        if status == "passed":
            target = check.get("artifact")
            if not isinstance(target, str) or target not in hashes or not isinstance(check.get("method"), str) or not check["method"].strip():
                errors.append(f"{key}: passed requires method and listed real evidence artifact")
        elif status == "not_applicable":
            reason = check.get("reason")
            if key in NON_WAIVABLE or not isinstance(reason, str) or len(reason.strip()) < 15:
                errors.append(f"{key}: cannot waive or insufficient rationale")
        else:
            errors.append(f"{key}: failed, unknown or invalid status")
    return hashes, errors


def stage_status(state: dict) -> str:
    for stage in STAGES:
        if stage not in state["completed"]:
            return stage
    return "complete"


def check_completed(state: dict, workspace: Path) -> None:
    for stage in STAGES[1:]:
        accepted = state["completed"].get(stage)
        if not accepted:
            continue
        p = report_path(workspace, stage)
        try:
            actual = digest(p)
            if actual != accepted["report_hash"]:
                reset_from(state, stage, "accepted review file changed")
                return
            for name, expected in accepted["artifacts"].items():
                if digest(valid_rel(workspace, name)) != expected:
                    reset_from(state, stage, f"accepted artifact changed: {name}")
                    return
        except (ValueError, OSError, KeyError):
            reset_from(state, stage, "accepted evidence missing")
            return


def advance(workspace: Path, *, sync_inputs: bool = False) -> dict:
    state = load(workspace)
    inputs = inputs_snapshot(Path(state["inputs_directory"]), workspace)
    if inputs != state["inputs"]:
        if not sync_inputs:
            return {"status": "inputs_changed", "next": "sync-inputs",
                    "message": "Original inputs changed. Explicitly sync and invalidate all dependent work."}
        state["inputs"] = inputs
        reset_from(state, "contract", "official inputs changed; re-evaluate all derived work")
        state["stale"].update({
            stage: digest(report_path(workspace, stage))
            for stage in STAGES[1:] if report_path(workspace, stage).is_file()
        })
        event(state, "sync_inputs", f"new input snapshot includes {len(inputs)} files")
        state["escalation"] = None
        save(workspace, state)
    check_completed(state, workspace)
    if state["escalation"]:
        save(workspace, state)
        return {"status": "human_escalation", "next": stage_status(state),
                "reason": state["escalation"]}
    for stage in STAGES[1:]:
        if stage in state["completed"]:
            continue
        p = report_path(workspace, stage)
        if not p.is_file():
            save(workspace, state)
            return {"status": "awaiting_work", "next": stage, "guide": DOCS.get(stage),
                    "message": "Create real artifacts and a review report; the agent should do work, not mark checks passed speculatively."}
        try:
            report_hash = digest(p)
            if state["stale"].get(stage) == report_hash:
                save(workspace, state)
                return {"status": "awaiting_rework", "next": stage,
                        "message": "Old review invalidated; rebuild evidence and update this report."}
            record = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError, json.JSONDecodeError) as exc:
            save(workspace, state)
            return {"status": "invalid_review", "next": stage, "message": str(exc)}
        if not isinstance(record, dict):
            save(workspace, state)
            return {"status": "invalid_review", "next": stage}
        if record.get("decision") == "failed":
            reason = record.get("reason")
            category = record.get("failure_class")
            if not isinstance(reason, str) or len(reason.strip()) < 15 or category not in FAIL_BACKTRACK:
                save(workspace, state)
                return {"status": "invalid_failure", "next": stage,
                        "message": "A failed review needs a failure_class and actionable reason."}
            target = FAIL_BACKTRACK[category]
            if STAGES.index(target) > STAGES.index(stage):
                target = stage
            state["attempts"][stage] = state["attempts"].get(stage, 0) + 1
            reset_from(state, target, f"{stage} failed ({category}): {reason}")
            state["stale"][stage] = report_hash
            if state["attempts"][stage] >= state["retry_budget"]:
                state["escalation"] = f"{stage}: retry budget exhausted; explicit human decision needed"
            save(workspace, state)
            return {"status": "human_escalation" if state["escalation"] else "rewind",
                    "next": target, "reason": reason, "attempts": state["attempts"][stage]}
        hashes, problems = review(stage, record, workspace)
        if problems:
            save(workspace, state)
            return {"status": "gate_blocked", "next": stage, "errors": problems}
        if stage in HUMAN_GATE:
            approval = state["approvals"].get(stage)
            if not isinstance(approval, dict) or approval.get("report_hash") != report_hash:
                save(workspace, state)
                return {"status": "awaiting_human_approval", "next": stage,
                        "message": "A human must explicitly approve this evidence snapshot."}
        state["completed"][stage] = {"report_hash": report_hash, "artifacts": hashes}
        state["stale"].pop(stage, None)
        event(state, "accepted", f"{stage}: evidence hash verified and declared checks present")
    save(workspace, state)
    return {"status": "machine_workflow_complete", "next": "none",
            "message": "Documentation and artifacts checked. This is not scientific truth or automatic submission."}


def approve(workspace: Path, stage: str, actor: str) -> dict:
    if stage not in HUMAN_GATE:
        raise ValueError(f"human approval only supported at: {', '.join(sorted(HUMAN_GATE))}")
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError("actor identity is required")
    state = load(workspace)
    if stage != stage_status(state):
        raise ValueError("only the current pending stage can be approved")
    p = report_path(workspace, stage)
    record = json.loads(p.read_text(encoding="utf-8"))
    _, problems = review(stage, record, workspace)
    if problems:
        raise ValueError("cannot approve failed or incomplete review: " + "; ".join(problems))
    current = digest(p)
    if state["stale"].get(stage) == current:
        raise ValueError("cannot approve an invalidated unchanged review")
    state["approvals"][stage] = {"report_hash": current, "actor": actor.strip(), "at": now()}
    event(state, "human_approved", f"{stage} acknowledged by {actor.strip()}")
    save(workspace, state)
    return {"status": "approval_recorded", "stage": stage,
            "warning": "The controller records an acknowledgement; it cannot authenticate who typed it."}


def summary(workspace: Path) -> dict:
    state = load(workspace)
    return {
        "next": stage_status(state), "completed": list(state["completed"]),
        "attempts": state["attempts"], "escalation": state["escalation"],
        "inputs_count": len(state["inputs"]), "history_events": len(state["history"]),
        "guide": DOCS.get(stage_status(state)), "approval_needed": stage_status(state) in HUMAN_GATE,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for action in ("init", "run", "status", "approve", "sync-inputs", "template"):
        p = sub.add_parser(action)
        if action != "template":
            p.add_argument("--workspace", type=Path, required=True)
        if action == "init":
            p.add_argument("--inputs", type=Path, required=True)
            p.add_argument("--retry-budget", type=int, default=DEFAULT_RETRY_BUDGET)
        if action == "approve":
            p.add_argument("--stage", required=True, choices=sorted(HUMAN_GATE))
            p.add_argument("--actor", required=True)
        if action == "template":
            p.add_argument("--stage", required=True, choices=list(CHECKS))
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            out = {"status": "initialized", "next": "contract",
                   "input_count": len(init(args.workspace, args.inputs, args.retry_budget)["inputs"])}
        elif args.command == "run":
            out = advance(args.workspace)
        elif args.command == "sync-inputs":
            out = advance(args.workspace, sync_inputs=True)
        elif args.command == "status":
            out = summary(args.workspace)
        elif args.command == "approve":
            out = approve(args.workspace, args.stage, args.actor)
        else:
            out = {"stage": args.stage, "decision": "pending",
                   "artifacts": ["artifacts/actual-output.json"],
                   "checks": {name: {"status": "pending"} for name in CHECKS[args.stage]}}
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 2 if out.get("status") in ("human_escalation", "inputs_changed", "gate_blocked", "invalid_review", "invalid_failure") else 0
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError, KeyError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
