from pathlib import Path
import json
import re
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
            self.assertRegex(text, r"(?m)^version: 7\.14\.0$")
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
            "latex_expected_artifact_gate:",
            "skill_repository_project_artifact_isolation:",
        ]
        for token in required:
            self.assertIn(token, text)

        self.assertIn("do not claim that a candidate was executed", text)
        self.assertIn("FileNotFoundError", text)
        self.assertIn("\\m", text)
        self.assertIn("strictly increasing", text)

    def test_stage_modules_reference_convergence_contract(self):
        solve = (ROOT / "modules" / "03_solve_validate.md").read_text(encoding="utf-8")
        analysis = (ROOT / "modules" / "03_result_analysis.md").read_text(encoding="utf-8")
        compile_quality = (ROOT / "modules" / "05_latex_compile_quality.md").read_text(encoding="utf-8")

        self.assertIn("core/workflow_convergence_contract.yaml", solve)
        self.assertIn("project_path_contract", solve)
        self.assertIn("post_execution_review", solve)
        self.assertIn("core/workflow_convergence_contract.yaml", analysis)
        self.assertIn("post_analysis_review", analysis)
        self.assertIn("latex_expected_artifact_gate", compile_quality)
        self.assertIn("Expected Artifact Manifest", compile_quality)

    def test_roadmap_and_presentation_templates_exist(self):
        roadmap = (ROOT / "templates" / "figure" / "technical_roadmap_contract.md").read_text(encoding="utf-8")
        presentation = (ROOT / "templates" / "writing" / "presentation_lock.md").read_text(encoding="utf-8")
        self.assertIn("no connector may cross a text box", roadmap)
        self.assertIn("Draw.io", roadmap)
        self.assertIn("official competition/template hard rule", presentation)
        self.assertIn("appendix", presentation)

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

    def test_no_project_specific_result_numbers_in_new_contracts(self):
        paths = [
            ROOT / "core" / "workflow_convergence_contract.yaml",
            ROOT / "templates" / "figure" / "technical_roadmap_contract.md",
            ROOT / "templates" / "writing" / "presentation_lock.md",
        ]
        text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
        # Privacy regression sentinel: contracts should contain generic rules,
        # not copied project-specific result values.
        for value in ("7.400640", "3.566807"):
            self.assertNotIn(value, text)


if __name__ == "__main__":
    unittest.main()
