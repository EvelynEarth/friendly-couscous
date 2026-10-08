"""Focused regression tests for optional paper-first big-data preflight."""
from __future__ import annotations

from contextlib import redirect_stdout
from importlib.util import module_from_spec, spec_from_file_location
import io
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/big-data-competition-skill/tools/bigdata_preflight.py"
spec = spec_from_file_location("bigdata_preflight", SCRIPT)
preflight = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(preflight)


class AssetsTests(unittest.TestCase):
    def test_lfs_pointer_not_mistaken_for_workbook(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "附件1.xlsx").write_text(
                "version https://git-lfs.github.com/spec/v1\n"
                "oid sha256:123456\nsize 2\n", encoding="utf-8")
            record = preflight.check_assets(root)
            self.assertEqual(record["status"], "passed")
            self.assertEqual(len(record["lfs_pointers"]), 1)
            out = io.StringIO()
            with redirect_stdout(out):
                code = preflight.main(["assets", "--root", tmp, "--strict-lfs"])
            self.assertEqual(code, 2)
            self.assertEqual(json.loads(out.getvalue())["status"], "failed")


class YoloTests(unittest.TestCase):
    def make_tree(self, root: Path):
        (root / "images/train").mkdir(parents=True)
        (root / "labels/train").mkdir(parents=True)
        (root / "images/train/img1.jpg").write_bytes(b"\xff\xd8\xff")
        return root / "labels/train/img1.txt"

    def test_valid_bbox_is_not_segmentation_ground_truth(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = self.make_tree(root)
            p.write_text("2 0.5 0.5 0.2 0.2\n", encoding="utf-8")
            result = preflight.check_yolo(root, "train", "detect", 3, True)
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["bbox_annotations"], 1)
            self.assertEqual(result["polygon_annotations"], 0)
            self.assertTrue(any("segmentation" in item for item in result["warnings"]))
            wrong = preflight.check_yolo(root, "train", "segment", 3, True)
            self.assertEqual(wrong["status"], "failed")

    def test_invalid_bbox_bounds_and_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = self.make_tree(root)
            p.write_text("4 0.99 0.5 0.4 0.1\n", encoding="utf-8")
            self.assertEqual(preflight.check_yolo(root, "train", "detect", 3, True)["status"],
                             "failed")
            p.write_text("2 0.99 0.5 0.4 0.1\n", encoding="utf-8")
            self.assertEqual(preflight.check_yolo(root, "train", "detect", 3, True)["status"],
                             "failed")

    def test_polygon_and_missing_label_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = self.make_tree(root)
            p.write_text("0 0.1 0.2 0.4 0.2 0.4 0.5\n", encoding="utf-8")
            result = preflight.check_yolo(root, "train", "segment", 2, True)
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["polygon_annotations"], 1)
            p.unlink()
            self.assertEqual(preflight.check_yolo(root, "train", "detect", 2, False)["status"],
                             "passed")
            self.assertEqual(preflight.check_yolo(root, "train", "detect", 2, True)["status"],
                             "failed")


class CsvTests(unittest.TestCase):
    def make_csv(self, root, template: str, candidate: str):
        a, b = root / "official.csv", root / "result.csv"
        a.write_text(template, encoding="utf-8")
        b.write_text(candidate, encoding="utf-8")
        return a, b

    def test_preserves_template_header_id_order_and_numeric(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = self.make_csv(
                Path(tmp), "order_id,amount,risk\n001,,\n002,,\n",
                "order_id,amount,risk\n001,4.5,1\n002,0,0\n")
            valid = preflight.check_csv(a, b, "order_id", ",", "utf-8",
                                        ["amount"], ["risk=0,1,2"])
            self.assertEqual(valid["status"], "passed")
            b.write_text("order_id,amount,risk\n002,NaN,1\n001,4.5,5\n", encoding="utf-8")
            invalid = preflight.check_csv(a, b, "order_id", ",", "utf-8",
                                          ["amount"], ["risk=0,1,2"])
            self.assertEqual(invalid["status"], "failed")
            self.assertTrue(any("order" in x for x in invalid["errors"]))
            self.assertTrue(any("numeric" in x for x in invalid["errors"]))
            self.assertTrue(any("enum" in x for x in invalid["errors"]))

    def test_missing_or_extra_rows_and_header(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = self.make_csv(Path(tmp), "id,pred\n1,\n2,\n", "id,value\n1,1\n")
            result = preflight.check_csv(a, b, "id", ",", "utf-8", [], [])
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any("row count" in x for x in result["errors"]))
            self.assertTrue(any("header" in x for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
