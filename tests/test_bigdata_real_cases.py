"""2025 actual-file-informed contract checks and paper evidence integrity regression."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "skills/big-data-competition-skill/tools"
sys.path.insert(0, str(TOOLS))


def load(name, path):
    spec = spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    obj = module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


real = load("real_case_audit", TOOLS / "real_case_audit.py")
paper = load("paper_evidence_gate", TOOLS / "paper_evidence_gate.py")


class RealSourceInventoryTests(unittest.TestCase):
    def test_profile_is_grounded_and_does_not_assert_model_metrics(self):
        profile = real.load_profiles()
        a = profile["2025_A"]
        b = profile["2025_B"]
        self.assertEqual((a["train_images"], a["test_images"]), (3300, 413))
        self.assertEqual((a["train_label_files"], a["test_label_files"]), (3300, 413))
        self.assertEqual(a["class_count"], 3)
        self.assertEqual([r["all_class_id"] for r in a["source_samples"][:2]], [2, 0])
        self.assertEqual(b["lfs_reported_bytes"]["附件1.xlsx"], 2)
        self.assertNotIn("measured_accuracy", profile)


class VisionReadinessTests(unittest.TestCase):
    def setup_case(self, root: Path):
        (root / "images/train").mkdir(parents=True)
        (root / "images/test").mkdir(parents=True)
        (root / "labels/train").mkdir(parents=True)
        (root / "labels/test").mkdir(parents=True)
        (root / "classes.txt").write_text(
            "Dent（凹陷）标记为0\nHole（破洞）标记为1\nRusty（锈蚀）标记为2\n",
            encoding="utf-8")
        (root / "images/train/1.jpg").write_bytes(b"fake-jpeg-train-1")
        (root / "images/train/2.jpg").write_bytes(b"fake-jpeg-train-2")
        (root / "labels/train/1.txt").write_text(
            "2 0.474219 0.764063 0.185938 0.365625\n",
            encoding="utf-8")
        (root / "labels/train/2.txt").write_text(
            "0 0.203906 0.818750 0.329688 0.362500\n",
            encoding="utf-8")
        (root / "images/test/1.jpg").write_bytes(b"fake-jpeg-test-not-same")
        # Deliberately invalid label: a trustworthy readiness audit MUST NOT READ test GT.
        (root / "labels/test/1.txt").write_text("not a train label", encoding="utf-8")
        return {"2025_A": {"train_images": 2, "test_images": 1,
                          "test_label_files": 1, "class_count": 3}}

    def test_train_only_and_sealed_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = self.setup_case(root)
            out = real.audit_2025a(root, profile)
            self.assertEqual(out["status"], "ready_for_baseline", out)
            self.assertEqual(out["class_ids"], [0, 1, 2])
            self.assertEqual(out["train_bbox_per_class"], {"0": 1, "2": 1})
            self.assertEqual(out["train_annotations"], 2)
            self.assertFalse(out["test_labels_read_for_audit"])
            self.assertEqual(out["segmentation_ground_truth"], "not_supplied_by_train_bbox")
            self.assertEqual(out["experimental_metrics"], None)
            self.assertTrue(any("sealed" in x for x in out["warnings"]))

    def test_exact_duplicates_only_flagged_with_hashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = self.setup_case(root)
            (root / "images/test/1.jpg").write_bytes((root / "images/train/1.jpg").read_bytes())
            by_name_only = real.audit_2025a(root, profile, False)
            self.assertEqual(by_name_only["status"], "ready_for_baseline")
            self.assertEqual(by_name_only["cross_split_image_hash"], "not_checked")
            by_hash = real.audit_2025a(root, profile, True)
            self.assertEqual(by_hash["status"], "blocked")
            self.assertEqual(by_hash["cross_split_image_hash"], "checked")
            self.assertEqual(len(by_hash["cross_split_exact_duplicates"]), 1)

    def test_bad_label_and_partial_download_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            profile = self.setup_case(root)
            (root / "labels/train/2.txt").write_text(
                "9 0.5 0.5 0.2 0.2\n", encoding="utf-8")
            self.assertEqual(real.audit_2025a(root, profile)["status"], "blocked")
            (root / "images/train/2.jpg").unlink()
            self.assertEqual(real.audit_2025a(root, profile)["status"], "blocked")


class WorkbookReadinessTests(unittest.TestCase):
    def test_lfs_pointers_block_actual_xlsx_use(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = real.load_profiles()
            for name, size in data["2025_B"]["lfs_reported_bytes"].items():
                (root / name).write_text(
                    "version https://git-lfs.github.com/spec/v1\n"
                    + "oid sha256:" + "a" * 64 + f"\nsize {size}\n", encoding="utf-8")
            result = real.audit_2025b(root, data)
            self.assertEqual(result["status"], "blocked")
            self.assertEqual(len(result["errors"]), 3)
            self.assertTrue(any("2 data bytes" in x for x in result["warnings"]))
            self.assertFalse(result["official_result_template_schema_verified"])
            self.assertIsNone(result["experimental_metrics"])

    def test_real_zip_container_is_not_claimed_to_be_verified_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in real.PARTS:
                with zipfile.ZipFile(root / name, "w") as zipf:
                    zipf.writestr("[Content_Types].xml", "<Types/>")
                    zipf.writestr("xl/workbook.xml", "<workbook/>")
                    zipf.writestr("xl/worksheets/sheet1.xml", "<worksheet/>")
            result = real.audit_2025b(root, real.load_profiles())
            self.assertEqual(result["status"], "ready_for_schema_review")
            self.assertFalse(result["official_result_template_schema_verified"])
            self.assertFalse(result["workbook_rows_or_columns_verified"])

    def test_invalid_excel_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "Result.xlsx"
            f.write_text("plain text not a workbook", encoding="utf-8")
            self.assertEqual(real.inspect_xlsx(f)["status"], "invalid_xlsx_not_zip")


class PaperEvidenceGateTests(unittest.TestCase):
    def accepted_case(self, root: Path):
        data = {"split.csv": b"row,fold\n1,train\n2,valid\n",
                "metrics.json": b'{"macro_f1": 0.73}\n'}
        artifacts = []
        for file, payload in data.items():
            (root / file).write_bytes(payload)
            artifacts.append({"path": file, "sha256": hashlib.sha256(payload).hexdigest()})
        return {
            "experiment_id": "2025B-Q3-EXP001", "run_status": "accepted",
            "data_version": "SHA-data-v1", "code_revision": "commit-sha",
            "validation_scheme": "group_holdout", "split_protocol": "entity-disjoint",
            "random_seed": 42, "split_manifest": "split.csv",
            "metrics": {"macro_f1": 0.73}, "artifacts": artifacts,
            "claims": [{"claim_id": "C001", "metric": "macro_f1", "value": 0.73,
                        "artifact": "metrics.json", "paper_location": "Q3 results paragraph"}]
        }

    def test_valid_hash_bound_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            record = self.accepted_case(root)
            result = paper.audit_record(record, root)
            self.assertEqual(result["status"], "trace_consistent", result)
            self.assertEqual(result["claims_checked"], 1)

    def test_modified_artifact_blocks_paper_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rec = self.accepted_case(root)
            (root / "metrics.json").write_text('{"macro_f1":0.99}', encoding="utf-8")
            out = paper.audit_record(rec, root)
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("changed" in x for x in out["errors"]))

    def test_planned_or_fake_numerical_claim_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rec = self.accepted_case(root)
            rec["run_status"] = "planned"
            rec["claims"][0]["value"] = 0.99
            out = paper.audit_record(rec, root)
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("differs" in x for x in out["errors"]))
            self.assertTrue(any("accepted" in x for x in out["errors"]))

    def test_path_traversal_and_missing_split_proof_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rec = self.accepted_case(root)
            rec["artifacts"][0]["path"] = "../evil.csv"
            result = paper.audit_record(rec, root)
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("escapes" in x for x in result["errors"]))
            self.assertTrue(any("split_manifest" in x for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
