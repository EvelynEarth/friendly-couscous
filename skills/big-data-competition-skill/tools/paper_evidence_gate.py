#!/usr/bin/env python3
"""Verify paper claim -> metric -> hash-locked artifact trace (stdlib only).

This is an integrity gate, NOT an independent verification of model accuracy.
Do not mark an experiment accepted until its metrics/splits have actually run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

HEX64 = set("0123456789abcdef")


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as reader:
        for chunk in iter(lambda: reader.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def is_number(value: object) -> bool:
    return type(value) in (int, float) and math.isfinite(float(value))


def audit_record(record: dict, root: Path, require_metric_source: bool = False) -> dict:
    errors: list[str] = []
    if not isinstance(record, dict):
        return {"status": "blocked", "errors": ["record must be a JSON object"]}
    if record.get("run_status") != "accepted":
        errors.append("run_status must be accepted, backed by an actual executed run")
    for key in ("experiment_id", "data_version", "code_revision",
                "validation_scheme", "split_protocol"):
        val = record.get(key)
        if not isinstance(val, str) or not val.strip():
            errors.append(f"non-empty {key} required")
    if type(record.get("random_seed")) is not int:
        errors.append("integer random_seed required")
    metrics = record.get("metrics")
    if not isinstance(metrics, dict) or not metrics:
        errors.append("metrics must contain actual numeric results")
        metrics = {}
    for name, value in metrics.items():
        if not isinstance(name, str) or not name.strip() or not is_number(value):
            errors.append(f"invalid numeric metric: {name}")
    artifacts = record.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("nonempty list of SHA-256-verified artifacts required")
        artifacts = []
    seen: set[str] = set()
    verified: set[str] = set()
    root_abs = root.resolve()
    for i, item in enumerate(artifacts):
        if not isinstance(item, dict):
            errors.append(f"artifact[{i}]: object required")
            continue
        name, digest = item.get("path"), item.get("sha256")
        if not isinstance(name, str) or not name or name in seen:
            errors.append(f"artifact[{i}]: relative unique path required")
            continue
        seen.add(name)
        if not isinstance(digest, str) or len(digest) != 64 or not set(digest).issubset(HEX64):
            errors.append(f"artifact[{i}]: valid lowercase sha256 required")
            continue
        candidate = (root_abs / name).resolve()
        try:
            candidate.relative_to(root_abs)
        except ValueError:
            errors.append(f"artifact[{i}]: path escapes artifact root")
            continue
        if Path(name).is_absolute() or not candidate.is_file():
            errors.append(f"artifact[{i}]: file missing or absolute path disallowed")
            continue
        if file_hash(candidate) != digest:
            errors.append(f"artifact[{i}]: file changed since accepted run")
        else:
            verified.add(name)
    split_manifest = record.get("split_manifest")
    if not isinstance(split_manifest, str) or split_manifest not in verified:
        errors.append("split_manifest must name a verified artifact")
    # Stronger v2.5 mode: inspect the real, hash-verified metrics file, not only
    # numbers typed into this record. This still cannot prove metric computation
    # correctness; independent recomputation is a separate scientific obligation.
    source = record.get("metrics_artifact")
    source_verified = False
    if require_metric_source and (not isinstance(source, str) or not source.strip()):
        errors.append("strict mode requires metrics_artifact")
    if source is not None:
        if not isinstance(source, str) or source not in verified:
            errors.append("metrics_artifact must be a hash-verified file")
        else:
            try:
                raw_metrics = json.loads((root_abs / source).read_text(encoding="utf-8"))
                disk_metrics = (raw_metrics.get("metrics") if isinstance(raw_metrics, dict)
                                and isinstance(raw_metrics.get("metrics"), dict) else raw_metrics)
                if not isinstance(disk_metrics, dict) or not disk_metrics:
                    errors.append("metrics_artifact JSON must contain a nonempty metrics map")
                elif set(disk_metrics) != set(metrics):
                    errors.append("metrics_artifact metric names differ from accepted record")
                elif any(not is_number(x) for x in disk_metrics.values()):
                    errors.append("metrics_artifact contains non-finite/non-numeric values")
                elif any(not math.isclose(float(disk_metrics[k]), float(metrics[k]),
                                            rel_tol=1e-10, abs_tol=1e-12)
                         for k in metrics if is_number(metrics[k])):
                    errors.append("accepted metrics differ from actual metrics_artifact values")
                elif all(is_number(v) for v in metrics.values()):
                    source_verified = True
            except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
                errors.append(f"metrics_artifact is not readable metrics JSON: {exc}")
    claims = record.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("at least one evidence-bound numerical paper claim required")
        claims = []
    for i, claim in enumerate(claims):
        if not isinstance(claim, dict):
            errors.append(f"claim[{i}]: object required")
            continue
        metric, value, name = claim.get("metric"), claim.get("value"), claim.get("artifact")
        if not isinstance(claim.get("claim_id"), str) or not claim["claim_id"]:
            errors.append(f"claim[{i}]: claim_id missing")
        if not isinstance(claim.get("paper_location"), str) or not claim["paper_location"]:
            errors.append(f"claim[{i}]: paper_location missing")
        if metric not in metrics:
            errors.append(f"claim[{i}]: unsupported metric {metric}")
        if not is_number(value):
            errors.append(f"claim[{i}]: numerical value must be finite")
        elif metric in metrics and is_number(metrics[metric]):
            if not math.isclose(float(value), float(metrics[metric]), rel_tol=1e-8, abs_tol=1e-10):
                errors.append(f"claim[{i}]: reported number differs from accepted metric")
        if name not in verified:
            errors.append(f"claim[{i}]: no hash-verified artifact for claim")
        if require_metric_source and name != source:
            errors.append(f"claim[{i}]: numerical claim must reference metrics_artifact in strict mode")
    return {
        "status": "blocked" if errors else "trace_consistent",
        "errors": errors, "artifacts_checked": len(artifacts),
        "claims_checked": len(claims),
        "metrics_source_verified": source_verified,
        "strict_mode": require_metric_source,
        "interpretation": "Hash-verified metric consistency, NOT independently verified model correctness."
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record", type=Path, required=True, help="accepted experiment JSON record")
    p.add_argument("--artifact-root", type=Path, required=True)
    p.add_argument("--require-metric-source", action="store_true",
                   help="block claims until metrics_artifact JSON is read and SHA-256 verified")
    args = p.parse_args(argv)
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
        result = audit_record(record, args.artifact_root, args.require_metric_source)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        result = {"status": "blocked", "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "trace_consistent" else 2


if __name__ == "__main__":
    sys.exit(main())
