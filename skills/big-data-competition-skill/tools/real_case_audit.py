#!/usr/bin/env python3
"""Read-only authentic MathorCup 2025 A/B dataset readiness gates.

2025 A: inventory + TRAIN-only YOLO label audit, sealed TEST policy.
2025 B: distinguish actual OOXML workbooks from Git LFS pointer text.
Requires only the Python standard library. Does NOT train or evaluate models.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

from bigdata_preflight import IMAGE_EXT, check_yolo

BASE = Path(__file__).resolve().parents[1]
PROFILE = BASE / "competition/real_case_2025_profiles.json"
LFS_MARKER = b"version https://git-lfs.github.com/spec/v1"
PARTS = ("附件1.xlsx", "附件2.xlsx", "Result.xlsx")


def load_profiles(path: Path = PROFILE) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scanned_images(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXT)


def class_ids(path: Path) -> list[int]:
    ids = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        m = re.search(r"([0-9]+)\s*$", line)
        if not m:
            raise ValueError("cannot identify numeric class ID in classes.txt")
        ids.append(int(m.group(1)))
    if not ids or sorted(set(ids)) != list(range(len(ids))) or len(ids) != len(set(ids)):
        raise ValueError("class IDs must be unique and consecutive from 0")
    return ids


def image_fingerprint(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit_2025a(root: Path, profile: dict, hash_images: bool = False) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    train = scanned_images(root / "images/train")
    test = scanned_images(root / "images/test")
    labels_train = root / "labels/train"
    labels_test = root / "labels/test"
    expected = profile["2025_A"]
    if not (root / "classes.txt").is_file():
        errors.append("missing classes.txt")
        classes = []
    else:
        try:
            classes = class_ids(root / "classes.txt")
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"invalid classes.txt: {exc}")
            classes = []
    if len(train) != expected["train_images"]:
        errors.append(f"training image count {len(train)} != source inventory {expected['train_images']}")
    if len(test) != expected["test_images"]:
        errors.append(f"test image count {len(test)} != source inventory {expected['test_images']}")
    if len(classes) != expected["class_count"]:
        errors.append(f"classes count {len(classes)} != verified {expected['class_count']}")
    training = check_yolo(root, "train", "detect",
                          len(classes) if classes else expected["class_count"], True)
    errors.extend(f"train: {err}" for err in training["errors"])
    warnings.extend(f"train: {err}" for err in training["warnings"])
    # DO NOT read label/test contents: this split is sealed for model selection.
    test_annotation_files = (sum(1 for x in labels_test.rglob("*.txt") if x.is_file())
                             if labels_test.is_dir() else 0)
    if test_annotation_files:
        warnings.append("labels/test is present; keep its contents sealed during training, feature selection and tuning")
    if test_annotation_files != expected["test_label_files"]:
        warnings.append("test annotation count differs from historical source metadata; never use for tuning")
    distribution: Counter[str] = Counter()
    # Only training labels are inspected; this cannot leak test annotations.
    if labels_train.is_dir():
        for p in sorted(labels_train.rglob("*.txt")):
            for line in p.read_text(encoding="utf-8-sig").splitlines():
                parts = line.split()
                if len(parts) == 5:
                    try:
                        distribution[str(int(parts[0]))] += 1
                    except ValueError:
                        pass
    duplicates = []
    fingerprint_status = "not_checked"
    if hash_images and train and test:
        fingerprint_status = "checked"
        by_digest: dict[str, str] = {}
        for p in train:
            by_digest.setdefault(image_fingerprint(p), p.name)
        for p in test:
            original = by_digest.get(image_fingerprint(p))
            if original is not None:
                duplicates.append({"train_name": original, "test_name": p.name})
        if duplicates:
            errors.append(f"{len(duplicates)} exact image-duplicate(s) across train/test")
    if len({p.stem for p in train} & {p.stem for p in test}):
        warnings.append("image name stems overlap across splits; filenames alone do not establish content leakage")
    return {
        "case": "2025_A", "status": "blocked" if errors else "ready_for_baseline",
        "errors": errors, "warnings": warnings,
        "train_images": len(train), "test_images": len(test),
        "test_annotation_files_present": test_annotation_files,
        "test_labels_read_for_audit": False,
        "class_ids": classes, "train_bbox_per_class": dict(sorted(distribution.items())),
        "train_annotations": training["bbox_annotations"],
        "segmentation_ground_truth": "not_supplied_by_train_bbox",
        "cross_split_exact_duplicates": duplicates,
        "cross_split_image_hash": fingerprint_status,
        "model_run": "not_run", "experimental_metrics": None
    }


def inspect_xlsx(path: Path) -> dict:
    if not path.is_file():
        return {"status": "missing"}
    try:
        with path.open("rb") as stream:
            head = stream.read(128)
        if head.startswith(LFS_MARKER):
            pointer = path.read_text(encoding="utf-8")
            size = re.search(r"(?m)^size\s+(\d+)\s*$", pointer)
            return {"status": "unresolved_lfs_pointer", "reported_size": int(size.group(1)) if size else None}
        if not zipfile.is_zipfile(path):
            return {"status": "invalid_xlsx_not_zip"}
        with zipfile.ZipFile(path) as archive:
            members = set(archive.namelist())
            if not {"[Content_Types].xml", "xl/workbook.xml"}.issubset(members):
                return {"status": "invalid_xlsx_missing_workbook"}
            if not any(name.startswith("xl/worksheets/") and name.endswith(".xml") for name in members):
                return {"status": "invalid_xlsx_missing_sheets"}
            bad = archive.testzip()
            if bad:
                return {"status": "xlsx_corrupt_zip_member", "member": bad}
        return {"status": "valid_ooxml_container"}
    except (OSError, UnicodeError, zipfile.BadZipFile, ValueError) as exc:
        return {"status": "unreadable", "reason": str(exc)}


def audit_2025b(root: Path, profile: dict) -> dict:
    files = {name: inspect_xlsx(root / name) for name in PARTS}
    errors = []
    warnings = []
    reference = profile["2025_B"]["lfs_reported_bytes"]
    for name, state in files.items():
        if state["status"] != "valid_ooxml_container":
            errors.append(f"{name}: {state['status']} (cannot use as an Excel workbook)")
        if state["status"] == "unresolved_lfs_pointer":
            if state.get("reported_size") != reference[name]:
                warnings.append(f"{name}: LFS metadata changed from inspected source snapshot")
            if state.get("reported_size") == 2:
                warnings.append(f"{name}: LFS pointer reports only 2 data bytes; verify source completeness")
    return {
        "case": "2025_B", "status": "blocked" if errors else "ready_for_schema_review",
        "files": files, "errors": errors, "warnings": warnings,
        "workbook_rows_or_columns_verified": False,
        "official_result_template_schema_verified": False,
        "model_run": "not_run", "experimental_metrics": None
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=["2025-a", "2025-b"])
    parser.add_argument("--root", type=Path, required=True, help="unpacked, locally available case data directory")
    parser.add_argument("--profile", type=Path, default=PROFILE)
    parser.add_argument("--hash-images", action="store_true",
                        help="2025-A only: compute SHA-256 of each train and test image to find exact duplicates")
    args = parser.parse_args(argv)
    try:
        profile = load_profiles(args.profile)
        result = (audit_2025a(args.root, profile, args.hash_images)
                  if args.case == "2025-a" else audit_2025b(args.root, profile))
    except (OSError, UnicodeError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result = {"case": args.case, "status": "blocked", "errors": [str(exc)],
                  "model_run": "not_run"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"ready_for_baseline", "ready_for_schema_review"} else 2


if __name__ == "__main__":
    sys.exit(main())
