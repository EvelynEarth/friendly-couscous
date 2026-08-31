from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowConvergenceV714Tests(unittest.TestCase):
    def test_version_sources_are_v714(self):
        bootstrap = (ROOT / "core" / "bootstrap.yaml").read_text(encoding="utf-8")
        self.assertIn("skill_version: 7.14.0", bootstrap)

        plugin = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(plugin["version"], "7.14.0")

        for path in [ROOT / "SKILL.md", ROOT / "skills" / "mathmodel-skill" / "SKILL.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertRegex(text, r"(?m)^version: 7\.14.0$")
            self.assertIn("HSK 数学建模模块化工作流 v7.14.0", text)

    def test_bootstrap_points_to_convergence_authority(self):
        bootstrap = (ROOT / "core" / "bootstrap.yaml").read_text(encoding="utf-8")
        self.assertIn("workflow_convergence: core/workflow_convergence_contract.yaml", bootstrap)
        self.assertIn("project_artifact_isolation: core/workflow_convergence_contract.yaml", bootstrap)
        self.assertIn("Cross-stage question closure", bootstrap)

    def test_convergence_contract_closes_observed_failure_modes(self):
        text = (ROOT / "core" / "workflow_convergence_contract.yaml").read_text(encoding="utf-8")
        required = [
            "question_closure_gate:",
            "post_execution_review:",
            "project_path_contract:",
            "figure_purpose_gate:",
            "mechanism_figure_closure:",
            "figure_candidate_governance:",
            "matlab_figure_static_gate:",
            "technical_roadmap_contract:",
            "presentation_lock:",
            "benchmark_calibration_boundary:",
            "competition_paper_calibration_gate:",
            "reader_recovery_test:",
            "evidence_density_and_carrier_gate:",
            "paper_prose_register_gate:",
            "title_abstract_calibration_gate:",
            "citation_source_integrity_gate:",
            "appendix_allocation_gate:",
            "final_pdf_readability_gate:",
            "latex_expected_artifact_gate:",
            "skill_repository_project_artifact_isolation:",
        ]
        for token in required:
            self.assertIn(token, text)

        self.assertIn("do not claim that a candidate was executed", text)
        self.assertIn("FileNotFoundError", text)
        self.assertIn("\\m", text)
        self.assertIn("strictly increasing", text)

    def test_paper_calibration_is_non_imitation_and_non_quota(self):
        text = (ROOT / "core" / "workflow_convergence_contract.yaml").read_text(encoding="utf-8")
        self.assertIn("benchmark papers are diagnostic references, not templates to imitate", text)
        self.assertIn("no universal page-count, figure-count, formula-count", text)
        self.assertIn("competition judge", text)
        self.assertIn("internal workflow jargon", text)
        self.assertIn("AI assistant", text)
        self.assertIn("final insertion size", text)
        self.assertIn("canonical, current code", text)

    def test_stage_modules_reference_convergence_and_identity_contracts(self):
        solve = (ROOT / "modules" / "03_solve_validate.md").read_text(encoding="utf-8")
        analysis = (ROOT / "modules" / "03_result_analysis.md").read_text(encoding="utf-8")
        figure = (ROOT / "modules" / "04_figure_evidence.md").read_text(encoding="utf-8")
        compile_quality = (ROOT / "modules" / "05_latex_compile_quality.md").read_text(encoding="utf-8")
        code_quality = (ROOT / "core" / "code_quality_contract.yaml").read_text(encoding="utf-8")

        self.assertIn("core/workflow_convergence_contract.yaml", solve)
        self.assertIn("project_path_contract", solve)
        self.assertIn("post_execution_review", solve)
        self.assertIn("candidate_vNN", solve)
        self.assertIn("不得仅因 `Path(__file__).name`", solve)
        self.assertIn("root-cause diagnosis", solve)

        self.assertIn("core/workflow_convergence_contract.yaml", analysis)
        self.assertIn("post_analysis_review", analysis)
        self.assertIn("actual worksheet names", analysis)
        self.assertIn("exact tie", analysis)
        self.assertIn("small nonzero gap", analysis)

        self.assertIn("core/workflow_convergence_contract.yaml", figure)
        self.assertIn("Figure Purpose Gate", figure)
        self.assertIn("latex_expected_artifact_gate", compile_quality)
        self.assertIn("Expected Artifact Manifest", compile_quality)

        self.assertIn("artifact_identity_contract:", code_quality)
        self.assertIn("filename_policy:", code_quality)
        self.assertIn("consumer_binding:", code_quality)
        self.assertIn("result_semantics_contract:", code_quality)
        self.assertIn("不得仅因用户本地重命名脚本而RuntimeError", code_quality)

    def test_mechanism_router_and_sparse_contract_exist(self):
        mechanism = (ROOT / "templates" / "figure" / "mechanism_figure_contract.md").read_text(encoding="utf-8")
        anti_ai = (ROOT / "templates" / "figure" / "anti_ai_figure_gate.md").read_text(encoding="utf-8")
        figure_index = (ROOT / "templates" / "figure" / "README.md").read_text(encoding="utf-8")

        self.assertIn("image generation first", mechanism)
        self.assertIn("Draw.io first", mechanism)
        self.assertIn("MATLAB/Python **不是复杂机制图默认工具**", mechanism)
        self.assertIn("每节点原则上 1–2 行短标签", mechanism)
        self.assertIn("connector crossing = 0", mechanism)
        self.assertIn("connector-through-text = 0", mechanism)
        self.assertIn("Legend Gate", mechanism)
        self.assertIn("uncompressed XML", mechanism)

        self.assertIn("Mechanism Figure **允许少量语义图标**", anti_ai)
        self.assertIn("connector crossing > 0 → FAIL", anti_ai)
        self.assertIn("mechanism_figure_contract.md", figure_index)

    def test_advanced_chart_search_is_proactive_but_evidence_governed(self):
        chart = (ROOT / "templates" / "figure" / "chart_selection.md").read_text(encoding="utf-8")
        evals = (ROOT / "templates" / "figure" / "figure_skill_evals.md").read_text(encoding="utf-8")

        self.assertIn("Advanced-first, evidence-governed", chart)
        self.assertIn("best advanced candidate", chart)
        self.assertIn("simpler fallback", chart)
        self.assertIn("reviewer risk", chart)
        self.assertIn("明明 forest/regime/raincloud/Pareto 更合适", chart)
        for grammar in [
            "forest", "raincloud", "hexbin", "regime", "Pareto", "tornado",
            "waterfall", "Sankey", "ternary", "quiver", "streamline",
        ]:
            self.assertIn(grammar, chart)

        self.assertIn("Eval 21", evals)
        self.assertIn("明明高级图更好却机械退回普通图", evals)
        self.assertIn("Eval 22", evals)
        self.assertIn("高级图只因复杂而准入", evals)
        self.assertIn("23/23", evals)

    def test_roadmap_presentation_and_reference_integrity_templates_exist(self):
        roadmap = (ROOT / "templates" / "figure" / "technical_roadmap_contract.md").read_text(encoding="utf-8")
        presentation = (ROOT / "templates" / "writing" / "presentation_lock.md").read_text(encoding="utf-8")
        references = (ROOT / "templates" / "writing" / "reference_integrity_check.md").read_text(encoding="utf-8")
        router = (ROOT / "core" / "workflow_router.yaml").read_text(encoding="utf-8")

        self.assertIn("no connector may cross a text box", roadmap)
        self.assertIn("Draw.io", roadmap)
        self.assertIn("official competition/template hard rule", presentation)
        self.assertIn("appendix", presentation)
        self.assertIn("reference_style:", presentation)
        self.assertIn("book_page_locator_required", presentation)
        self.assertIn("web_access_date_required", presentation)
        self.assertIn("reference_integrity_check.md", presentation)

        self.assertIn("Source existence gate", references)
        self.assertIn("Claim-support gate", references)
        self.assertIn("two-way audit", references)
        self.assertIn("Page locator / access-date semantics", references)
        self.assertIn("AI 助手、搜索结果页和聚合摘要不能作为", references)

        self.assertIn("templates/figure/mechanism_figure_contract.md", router)
        self.assertIn("templates/figure/anti_ai_figure_gate.md", router)
        self.assertIn("templates/writing/reference_integrity_check.md", router)

    def test_skill_repository_has_no_root_project_artifacts(self):
        # Reusable Skill repository roots must not accidentally absorb a user's
        # competition project. Templates/fixtures elsewhere are not blocked.
        forbidden_exact = [
            ROOT / "模型论文框架.md",
            ROOT / "state" / "project_state.yaml",
            ROOT / "数据预处理",
        ]
        for path in forbidden_exact:
            self.assertFalse(path.exists(), f"project artifact leaked into Skill repo: {path}")

        leaked_question_dirs = [p for p in ROOT.glob("问题*求解") if p.is_dir()]
        self.assertEqual(leaked_question_dirs, [], f"task-specific question dirs leaked: {leaked_question_dirs}")

        top_level_binary_data = []
        for suffix in ("*.xlsx", "*.xls", "*.csv", "*.mat"):
            top_level_binary_data.extend(ROOT.glob(suffix))
        self.assertEqual(top_level_binary_data, [], f"competition data leaked at repo root: {top_level_binary_data}")

    def test_new_contracts_remain_generic(self):
        paths = [
            ROOT / "core" / "workflow_convergence_contract.yaml",
            ROOT / "core" / "code_quality_contract.yaml",
            ROOT / "templates" / "figure" / "technical_roadmap_contract.md",
            ROOT / "templates" / "figure" / "mechanism_figure_contract.md",
            ROOT / "templates" / "writing" / "presentation_lock.md",
            ROOT / "templates" / "writing" / "reference_integrity_check.md",
        ]
        text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
        # Contracts may describe generic project patterns but must not contain
        # copied project result workbooks, benchmark identifiers or literal task-output directories.
        self.assertNotIn("问题一求解结果.xlsx", text)
        self.assertNotIn("问题二求解结果.xlsx", text)
        self.assertNotIn("问题三求解结果.xlsx", text)
        self.assertNotIn("2025B157", text)
        self.assertNotIn("paper_complete.pdf", text)
        self.assertNotIn("碳化硅", text)


if __name__ == "__main__":
    unittest.main()
