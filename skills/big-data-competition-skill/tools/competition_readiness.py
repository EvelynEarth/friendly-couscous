#!/usr/bin/env python3
"""Task-agnostic paper-first competition review-package integrity gate.

Confirms coverage, cross-references and SHA-256-locked evidence for ANY problem
family. It does not establish truth, independent reviewer identity or readiness
to submit without real human scientific/editorial review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ALLOWED_OBJECTIVES = {
    "prediction", "optimization", "inference", "simulation", "causal",
    "description", "vision", "nlp", "recommendation", "explanation",
    "evaluation", "mixed", "other",
}
STRENGTHS = {"observed", "predictive", "associational", "causal", "optimal", "qualified"}
FUNCTIONS = {"problem", "method", "validation", "results", "discussion", "conclusion"}
REVIEW_KEYS = ("model_correctness", "independent_verification", "reliability", "stability")


def filled(value: object, n: int = 1) -> bool:
    return isinstance(value, str) and len(value.strip()) >= n


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _audit_unchecked(record: object, root: Path) -> dict:
    issues: list[str] = []
    if not isinstance(record, dict):
        return {"status": "blocked", "issues": ["JSON root must be object"]}
    if record.get("schema_version") != 1:
        issues.append("schema_version must equal 1")
    if not filled(record.get("competition_id")):
        issues.append("competition_id required")
    questions = record.get("official_questions")
    if (not isinstance(questions, list) or not questions or
        any(not filled(q) for q in questions) or len(set(map(str, questions))) != len(questions)):
        issues.append("official_questions must be a nonempty unique list of IDs")
        questions = []
    qset = set(questions)
    snapshot = record.get("files")
    trusted = set()
    if not isinstance(snapshot, list) or not snapshot:
        issues.append("nonempty SHA-256 file snapshot required")
        snapshot = []
    for i, entry in enumerate(snapshot):
        if not isinstance(entry, dict):
            issues.append(f"files[{i}] is not an object")
            continue
        name, expected = entry.get("path"), entry.get("sha256")
        if not filled(name) or name in trusted:
            issues.append(f"files[{i}] missing/duplicate path")
            continue
        if (not isinstance(expected, str) or len(expected) != 64
            or any(c not in "0123456789abcdef" for c in expected)):
            issues.append(f"files[{i}] invalid lowercase sha256")
            continue
        candidate = (root / name).resolve()
        if (Path(name).is_absolute() or not candidate.is_relative_to(root.resolve())
            or not candidate.is_file()):
            issues.append(f"files[{i}] missing or outside artifact root: {name}")
            continue
        try:
            if file_sha256(candidate) != expected:
                issues.append(f"files[{i}] SHA-256 changed: {name}")
                continue
        except OSError as exc:
            issues.append(f"files[{i}] unreadable: {exc}")
            continue
        trusted.add(name)

    def evidence(path: object, subject: str) -> None:
        if not filled(path) or path not in trusted:
            issues.append(f"{subject}: missing SHA-verified evidence file: {path}")

    entries = record.get("questions")
    if not isinstance(entries, list):
        entries = []
        issues.append("questions must be list")
    qids = [e.get("id") for e in entries if isinstance(e, dict)]
    if (len(qids) != len(entries) or any(not filled(q) for q in qids) or
        len(set(qids)) != len(qids) or set(qids) != qset):
        issues.append("question records must match EVERY official question exactly once")

    claim_ids = set()
    claims_by_question = {q: set() for q in qset}
    claims = record.get("claims")
    if not isinstance(claims, list) or not claims:
        issues.append("at least one evidence-backed claim required")
        claims = []
    for i, c in enumerate(claims):
        if not isinstance(c, dict):
            issues.append(f"claims[{i}] must be object")
            continue
        ident, qid = c.get("id"), c.get("question_id")
        if not filled(ident) or ident in claim_ids:
            issues.append(f"claims[{i}] missing/duplicate id")
            continue
        claim_ids.add(ident)
        if qid not in qset:
            issues.append(f"claims[{i}] outside official questions")
        else:
            claims_by_question[qid].add(ident)
        if not filled(c.get("statement"), 10) or c.get("strength") not in STRENGTHS:
            issues.append(f"{ident}: claim statement and strength required")
        if not filled(c.get("scope_and_limitations"), 15):
            issues.append(f"{ident}: limitation and scope needed")
        paths = c.get("evidence")
        if not isinstance(paths, list) or not paths:
            issues.append(f"{ident}: nonempty evidence list required")
        else:
            for path in paths:
                evidence(path, ident)
        if c.get("status") != "supported":
            issues.append(f"{ident}: unverified or contradicted claim")
    for qid in qset:
        if not claims_by_question[qid]:
            issues.append(f"{qid}: no evidence-backed claim answers this question")

    for i, item in enumerate(entries):
        if not isinstance(item, dict):
            issues.append(f"questions[{i}]: not object")
            continue
        qid = item.get("id")
        kind = item.get("objective")
        if kind not in ALLOWED_OBJECTIVES:
            issues.append(f"{qid}: objective must be an allowed family")
        for key in ("official_output", "delivered_answer", "model_choice_reason"):
            if not filled(item.get(key), 10):
                issues.append(f"{qid}: {key} must describe the actual scientific task")
        for x in item.get("claim_ids", []):
            if x not in claims_by_question.get(qid, set()):
                issues.append(f"{qid}: claim_ids references foreign or nonexistent claim: {x}")
        if not isinstance(item.get("claim_ids"), list) or set(item["claim_ids"]) != claims_by_question.get(qid, set()):
            issues.append(f"{qid}: explicit claim_ids must account for all of this question's claims")
        reviews = item.get("reviews")
        if not isinstance(reviews, dict):
            issues.append(f"{qid}: reviews must cover independent scientific checks")
            continue
        for key in REVIEW_KEYS:
            item_review = reviews.get(key)
            if not isinstance(item_review, dict):
                issues.append(f"{qid}: missing {key} review")
                continue
            status = item_review.get("status")
            if status == "passed":
                if not filled(item_review.get("method"), 15):
                    issues.append(f"{qid}: passed {key} needs an actual verification method")
                evidence(item_review.get("artifact"), f"{qid}/{key}")
                if key == "independent_verification" and item_review.get("independent") is not True:
                    issues.append(f"{qid}: independent verification not acknowledged")
            elif status == "not_applicable" and key in ("reliability", "stability"):
                if not filled(item_review.get("reason"), 25):
                    issues.append(f"{qid}: waiver of {key} needs case-specific substantive reason")
            else:
                issues.append(f"{qid}: {key} not passed or legitimately exempt")
        for c in claims:
            if not isinstance(c, dict) or c.get("question_id") != qid:
                continue
            if c.get("strength") == "causal" and kind != "causal":
                issues.append(f"{qid}: causal claim needs explicit causal task")
            if c.get("strength") == "optimal" and kind != "optimization":
                issues.append(f"{qid}: optimal claim outside optimization task")
            if c.get("strength") in ("causal", "optimal"):
                proof = item.get("claim_strength_justification")
                if not filled(proof, 25):
                    issues.append(f"{qid}: strong claim needs explicit identification/optimality rationale")

    paper = record.get("paper")
    if not isinstance(paper, dict):
        issues.append("paper must be structured manuscript plan")
        paper = {}
    evidence(paper.get("manuscript"), "paper/manuscript")
    sections = paper.get("sections")
    functions = set()
    referenced_claims = set()
    if not isinstance(sections, list) or not sections:
        issues.append("paper must provide sections")
        sections = []
    for i, section in enumerate(sections):
        if not isinstance(section, dict):
            issues.append(f"paper.sections[{i}]: invalid")
            continue
        role = section.get("function")
        if role not in FUNCTIONS:
            issues.append(f"paper.sections[{i}]: unknown logical function")
        else:
            functions.add(role)
        if not filled(section.get("argument"), 15):
            issues.append(f"paper.sections[{i}]: missing logical purpose")
        supports = section.get("claim_ids", [])
        if not isinstance(supports, list):
            issues.append(f"paper.sections[{i}]: claim_ids must be list")
        else:
            for cid in supports:
                if cid not in claim_ids:
                    issues.append(f"paper section cites unknown claim: {cid}")
                else:
                    referenced_claims.add(cid)
    for role in FUNCTIONS:
        if role not in functions:
            issues.append(f"paper structure missing logical function: {role}")
    if not claim_ids.issubset(referenced_claims):
        issues.append("one or more scientific claims have no location in paper argument")
    conclusion = paper.get("conclusion_claim_ids")
    if (not isinstance(conclusion, list) or not set(conclusion).issubset(claim_ids) or
        not all(claims_by_question[q].intersection(conclusion) for q in qset)):
        issues.append("conclusions must answer every official question with valid claim IDs")

    submission = record.get("delivery")
    if not isinstance(submission, dict):
        issues.append("delivery checklist required")
    else:
        official = submission.get("official_requirements")
        if not isinstance(official, list) or not official:
            issues.append("delivery must enumerate current official requirements")
        else:
            seen = set()
            for item in official:
                if not isinstance(item, dict) or not filled(item.get("id")) or item["id"] in seen:
                    issues.append("delivery requirement missing/duplicate id")
                    continue
                seen.add(item["id"])
                if item.get("status") != "checked" or not filled(item.get("detail"), 12):
                    issues.append(f"delivery requirement unchecked: {item['id']}")
                evidence(item.get("artifact"), f"delivery/{item['id']}")
        if submission.get("rules_from_current_competition_verified") is not True:
            issues.append("delivery rules must be checked against this year's official competition")
    return {
        "status": "blocked" if issues else "documentation_consistent_pending_expert_review",
        "issues": issues,
        "official_questions": len(qset), "claims": len(claim_ids),
        "sha_verified_files": len(trusted),
        "scientific_approval": "not_granted_by_automation",
        "interpretation": "Document and artifact coverage only. This tool cannot authenticate reviewers, establish scientific truth, verify official rules externally or authorize submission."
    }


def audit(record: object, root: Path) -> dict:
    """Malformed/unhashable user input must BLOCK, never crash or return a false pass."""
    try:
        return _audit_unchecked(record, root)
    except (TypeError, ValueError, KeyError, AttributeError) as exc:
        return {"status": "blocked", "issues": [f"invalid record structure: {exc}"],
                "scientific_approval": "not_granted_by_automation"}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record", type=Path, required=True)
    p.add_argument("--artifact-root", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        result = audit(json.loads(args.record.read_text(encoding="utf-8")), args.artifact_root)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "blocked", "issues": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "documentation_consistent_pending_expert_review" else 2


if __name__ == "__main__":
    sys.exit(main())
