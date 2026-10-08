#!/usr/bin/env python3
"""Evidence-first audit of MathorCup awarded-paper inventory (stdlib only).

Do not infer reading or methods from PDF filenames. The inventory is provenance,
not a substitute for a PDF review. Non-reviewed records cannot contain claims.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

DEFAULT = Path(__file__).resolve().parents[1] / "competition" / "award_papers_2024_2025.json"
STATUS = {"unreviewed", "reviewed", "unavailable"}
ATTRIBUTION = {"author_reported", "reviewer_inference"}


def check_inventory(data: dict) -> list[str]:
    problems: list[str] = []
    papers = data.get("papers")
    if data.get("source_repo") != "EvelynEarth/supreme-spoon":
        problems.append("source_repo must identify the evidence repository")
    if not isinstance(papers, list) or not papers:
        return problems + ["papers must be nonempty list"]
    seen = set()
    for idx, p in enumerate(papers):
        pos = f"papers[{idx}]"
        if not isinstance(p, dict):
            problems.append(f"{pos}: not an object")
            continue
        pid = p.get("paper_id")
        if not isinstance(pid, str) or not pid:
            problems.append(f"{pos}: paper_id missing")
        elif pid in seen:
            problems.append(f"{pos}: duplicate paper_id")
        seen.add(pid)
        year, number = p.get("year"), p.get("number")
        if type(year) is not int or year not in (2024, 2025) or type(number) is not int or not 1 <= number <= 8:
            problems.append(f"{pos}: unsupported year/number")
        elif pid != f"{year}-{number:02d}":
            problems.append(f"{pos}: paper_id does not match year/index")
        path = p.get("source_path", "")
        if not isinstance(path, str) or not path.endswith(f"优秀论文-{number}.pdf"):
            problems.append(f"{pos}: wrong source PDF path")
        if type(p.get("size_bytes")) is not int or p["size_bytes"] <= 0:
            problems.append(f"{pos}: missing source byte size")
        state = p.get("review_status")
        if state not in STATUS:
            problems.append(f"{pos}: invalid review_status")
        findings = p.get("findings")
        if not isinstance(findings, list):
            problems.append(f"{pos}: findings must be array")
            continue
        if state != "reviewed" and findings:
            problems.append(f"{pos}: unreviewed/unavailable paper must not carry method findings")
        if state == "reviewed" and not findings:
            problems.append(f"{pos}: reviewed paper must carry page-verified findings")
        if state == "reviewed" and not p.get("pdf_content_verified", False):
            problems.append(f"{pos}: reviewed requires pdf_content_verified=true")
        if state != "reviewed" and p.get("pdf_content_verified", False):
            problems.append(f"{pos}: non-reviewed paper cannot assert content verified")
        for j, claim in enumerate(findings):
            label = f"{pos}.findings[{j}]"
            if not isinstance(claim, dict):
                problems.append(f"{label}: not an object")
                continue
            if type(claim.get("page")) is not int or claim["page"] < 1:
                problems.append(f"{label}: PDF page must be positive integer")
            for key in ("question", "method_family", "evidence_note"):
                if not isinstance(claim.get(key), str) or not claim[key].strip():
                    problems.append(f"{label}: {key} required")
            if claim.get("attribution") not in ATTRIBUTION:
                problems.append(f"{label}: separate author_reported from reviewer_inference")
            if claim.get("evidence_verified") is not True:
                problems.append(f"{label}: finding requires verified PDF evidence")
    return problems


def summarize(data: dict) -> dict:
    papers = data["papers"]
    reviewed = [p for p in papers if p["review_status"] == "reviewed"]
    counts = Counter(p["review_status"] for p in papers)
    by_year = {str(y): {"total": sum(p["year"] == y for p in papers),
                        "reviewed": sum(p["year"] == y for p in reviewed)} for y in (2024, 2025)}
    # A paper contributes at most once per method family, not once per keyword mention.
    families = Counter()
    for p in reviewed:
        families.update({c["method_family"] for c in p["findings"]})
    return {
        "status": "passed",
        "inventory_total": len(papers),
        "reviewed_papers": len(reviewed),
        "status_counts": dict(sorted(counts.items())),
        "by_year": by_year,
        "method_family_paper_counts": dict(sorted(families.items())),
        "method_frequency_denominator": len(reviewed),
        "interpretation": "Metadata inventory only; method frequencies exclude unreviewed papers."
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inventory", type=Path, default=DEFAULT)
    ap.add_argument("--summary", action="store_true")
    args = ap.parse_args(argv)
    try:
        with args.inventory.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        errors = check_inventory(data)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        data = {}
    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(summarize(data) if args.summary else
                     {"status": "passed", "count": len(data["papers"])},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
