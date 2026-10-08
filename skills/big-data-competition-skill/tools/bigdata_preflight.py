#!/usr/bin/env python3
"""Read-only preflight for paper-first big-data competitions (stdlib only)."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
import math
from pathlib import Path
import sys


IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def report(kind: str, errors: list[str], warnings: list[str], **details: object) -> dict:
    return {
        "check": kind,
        "status": "failed" if errors else "passed",
        "errors": errors,
        "warnings": warnings,
        **details,
    }


def check_assets(root: Path) -> dict:
    if not root.is_dir():
        return report("assets", [f"directory not found: {root}"], [])
    counts: Counter[str] = Counter()
    pointers: list[dict] = []
    files = 0
    total_bytes = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(p in {".git", "__pycache__"} for p in path.parts):
            continue
        files += 1
        size = path.stat().st_size
        total_bytes += size
        counts[path.suffix.lower() or "<none>"] += 1
        if size <= 512:
            with path.open("rb") as fp:
                head = fp.read(128)
            if head.startswith(b"version https://git-lfs.github.com/spec/v1"):
                pointers.append({"path": str(path.relative_to(root)), "bytes_on_disk": size})
    warnings = ([f"{len(pointers)} Git LFS pointer(s), not underlying dataset bytes"]
                if pointers else [])
    return report("assets", [], warnings, files=files, total_bytes=total_bytes,
                  extensions=dict(sorted(counts.items())), lfs_pointers=pointers)


def check_yolo(root: Path, split: str, task: str, classes: int | None,
               require_labels: bool) -> dict:
    img_dir = root / "images" / split
    label_dir = root / "labels" / split
    errors: list[str] = []
    warnings: list[str] = []
    if not img_dir.is_dir() or not label_dir.is_dir():
        return report("yolo", [f"missing {img_dir} or {label_dir}"], [])
    images = [p for p in img_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXT]
    labels = [p for p in label_dir.rglob("*.txt") if p.is_file()]
    image_names = Counter(p.stem for p in images)
    label_names = Counter(p.stem for p in labels)
    for name, count in image_names.items():
        if count > 1:
            errors.append(f"duplicate image stem: {name}")
    for name, count in label_names.items():
        if count > 1:
            errors.append(f"duplicate label stem: {name}")
    extra = sorted(label_names.keys() - image_names.keys())
    missing = sorted(image_names.keys() - label_names.keys())
    if extra:
        errors.append(f"{len(extra)} orphan label(s): {extra[:5]}")
    if missing:
        note = f"{len(missing)} images without .txt annotation files: {missing[:5]}"
        (errors if require_labels else warnings).append(note)
    if not images:
        errors.append("no images found")
    boxes = masks = empty = 0
    for path in labels:
        lines = [line.strip() for line in path.read_text(encoding="utf-8-sig").splitlines()
                 if line.strip()]
        if not lines:
            empty += 1
        for lineno, line in enumerate(lines, 1):
            bits = line.split()
            position = f"{path.relative_to(root)}:{lineno}"
            if len(bits) == 5:
                kind = "detect"
            elif len(bits) >= 7 and len(bits) % 2 == 1:
                kind = "segment"
            else:
                errors.append(f"{position}: invalid YOLO label column count {len(bits)}")
                continue
            if task != "auto" and task != kind:
                errors.append(f"{position}: {kind} annotation used for {task} task")
            try:
                category = int(bits[0])
                values = [float(value) for value in bits[1:]]
                if category < 0 or (classes is not None and category >= classes):
                    raise ValueError("out-of-range class ID")
                if not all(math.isfinite(v) and 0 <= v <= 1 for v in values):
                    raise ValueError("nonfinite or out-of-range coordinate")
                if kind == "detect":
                    cx, cy, w, h = values
                    if w <= 0 or h <= 0:
                        raise ValueError("nonpositive bbox size")
                    if any(v < -1e-6 or v > 1 + 1e-6 for v in
                           (cx - w/2, cx + w/2, cy - h/2, cy + h/2)):
                        raise ValueError("bbox extends beyond image")
                else:
                    if len(values) < 6:
                        raise ValueError("polygon needs at least 3 points")
            except ValueError as exc:
                errors.append(f"{position}: {exc}")
            boxes += kind == "detect"
            masks += kind == "segment"
    if boxes and not masks:
        warnings.append("bbox-only labels do not provide pixel-level segmentation ground truth")
    return report("yolo", errors, warnings, split=split, images=len(images),
                  label_files=len(labels), empty_labels=empty,
                  bbox_annotations=boxes, polygon_annotations=masks,
                  missing_label_count=len(missing), orphan_label_count=len(extra))


def read_csv(path: Path, encoding: str, delimiter: str) -> tuple[list[str], list[dict]]:
    with path.open("r", encoding=encoding, newline="") as fp:
        reader = csv.DictReader(fp, delimiter=delimiter)
        columns = reader.fieldnames or []
        rows = list(reader)
    return columns, rows


def check_csv(template: Path, candidate: Path, id_column: str, delimiter: str,
              encoding: str, numeric: list[str], enumerations: list[str]) -> dict:
    errors: list[str] = []
    try:
        expected_columns, expected = read_csv(template, encoding, delimiter)
        columns, actual = read_csv(candidate, encoding, delimiter)
    except (OSError, UnicodeError, csv.Error) as exc:
        return report("csv", [f"cannot read CSV: {exc}"], [])
    if len(columns) != len(set(columns)) or len(expected_columns) != len(set(expected_columns)):
        errors.append("duplicate column names")
    if columns != expected_columns:
        errors.append(f"header/order mismatch: expected={expected_columns}, actual={columns}")
    if id_column not in columns or id_column not in expected_columns:
        errors.append(f"missing ID column: {id_column}")
    if len(actual) != len(expected):
        errors.append(f"row count mismatch: expected={len(expected)}, actual={len(actual)}")
    if id_column in columns and id_column in expected_columns:
        ids = [r.get(id_column) for r in actual]
        old_ids = [r.get(id_column) for r in expected]
        if ids != old_ids:
            errors.append("ID values or row order differ from official template")
        if any(not value for value in ids):
            errors.append("empty ID value")
        if len(ids) != len(set(ids)):
            errors.append("duplicate candidate IDs")
    if any(None in row or any(value is None for value in row.values()) for row in actual):
        errors.append("candidate has malformed/incomplete CSV row(s)")
    rule_map: dict[str, set[str]] = {}
    for item in enumerations:
        name, sep, options = item.partition("=")
        if not sep or not name or not options:
            errors.append(f"invalid --enum: {item} (expect COLUMN=a,b,c)")
        else:
            rule_map[name] = set(options.split(","))
    for col in [*numeric, *rule_map]:
        if col not in columns:
            errors.append(f"missing validation column: {col}")
    for idx, row in enumerate(actual, 2):
        for col in numeric:
            if col not in columns:
                continue
            try:
                value = float(row[col])
                if not math.isfinite(value):
                    raise ValueError("not finite")
            except (ValueError, TypeError):
                errors.append(f"row {idx}: invalid numeric value in {col}")
        for col, allowed in rule_map.items():
            if col in columns and row.get(col) not in allowed:
                errors.append(f"row {idx}: invalid enum in {col}")
        # Cap detail volume on large prediction files; status still signals failure.
        if len(errors) >= 30:
            errors.append("further row errors omitted")
            break
    return report("csv", errors, [], template_rows=len(expected),
                  candidate_rows=len(actual), columns=columns, id_column=id_column)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    assets = sub.add_parser("assets", help="file inventory and LFS pointer warning")
    assets.add_argument("--root", type=Path, required=True)
    assets.add_argument("--strict-lfs", action="store_true", help="fail if unresolved LFS pointers exist")
    yolo = sub.add_parser("yolo", help="validate YOLO bbox/polygon annotations")
    yolo.add_argument("--root", type=Path, required=True)
    yolo.add_argument("--split", default="train")
    yolo.add_argument("--task", choices=["auto", "detect", "segment"], default="auto")
    yolo.add_argument("--classes", type=int, default=None)
    yolo.add_argument("--require-label-files", action="store_true")
    csv_cmd = sub.add_parser("csv", help="compare prediction CSV with official CSV template")
    csv_cmd.add_argument("--template", type=Path, required=True)
    csv_cmd.add_argument("--candidate", type=Path, required=True)
    csv_cmd.add_argument("--id-column", required=True)
    csv_cmd.add_argument("--encoding", default="utf-8-sig")
    csv_cmd.add_argument("--delimiter", default=",")
    csv_cmd.add_argument("--numeric", action="append", default=[])
    csv_cmd.add_argument("--enum", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.mode == "assets":
        result = check_assets(args.root)
        if args.strict_lfs and result.get("lfs_pointers"):
            result["errors"].append("unresolved Git LFS pointers")
            result["status"] = "failed"
    elif args.mode == "yolo":
        if args.classes is not None and args.classes < 1:
            result = report("yolo", ["--classes must be positive"], [])
        else:
            result = check_yolo(args.root, args.split, args.task, args.classes,
                                args.require_label_files)
    else:
        if len(args.delimiter) != 1:
            result = report("csv", ["--delimiter must be one character"], [])
        else:
            result = check_csv(args.template, args.candidate, args.id_column,
                               args.delimiter, args.encoding, args.numeric, args.enum)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "passed" else 2


if __name__ == "__main__":
    sys.exit(main())
