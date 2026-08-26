import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestFigureIterationGovernance(unittest.TestCase):
    def test_figure_pack_has_reference_decomposition_and_freeze_loop(self):
        text = (ROOT / "packs/artifact/figure.md").read_text(encoding="utf-8")
        for token in (
            "参考图先分解，后写代码",
            "Visual Contract",
            "主体 geometry",
            "局部反馈默认局部修改",
            "多轮不收敛先诊断",
            "接受即冻结",
            "canonical `问题X求解/qX_plot.m`",
            "显式 reopen",
        ):
            self.assertIn(token, text)
        self.assertIn("约 3 个 redraw round", text)
        self.assertIn("不是禁止继续修改的硬上限", text)
        self.assertIn("不建立第二套绘图 Authority", text)

    def test_figure_qa_guards_reference_scope_and_file_hygiene(self):
        text = (ROOT / "templates/figure/result_figure_qa.md").read_text(encoding="utf-8")
        for token in (
            "accepted workbooks",
            "主体 geometry",
            "反馈作用域",
            "Reference/Current mismatch diagnosis",
            "accepted/frozen",
            "canonical `qX_plot.m`",
            "重复 wrapper",
        ):
            self.assertIn(token, text)

    def test_retrospective_is_non_authoritative(self):
        text = (ROOT / "docs/figure_iteration_retrospective.md").read_text(encoding="utf-8")
        self.assertIn("不是第二套绘图权威", text)
        self.assertIn("modules/04_figure_evidence.md", text)
        self.assertIn("Figure role / 图型", text)
        self.assertIn("三轮不收敛先诊断", text)
        self.assertIn("接受后立即冻结并清理", text)


if __name__ == "__main__":
    unittest.main()
