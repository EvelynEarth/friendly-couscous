"""Synthetic workflow regression tests; not scientific or real competition model tests."""
from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "skills/big-data-competition-skill/tools/competition_autopilot.py"
spec = spec_from_file_location("competition_autopilot", MODULE)
assert spec and spec.loader
auto = module_from_spec(spec)
spec.loader.exec_module(auto)


class AutopilotFixture:
    def __init__(self, root: Path):
        self.inputs = root / "official_inputs"
        self.inputs.mkdir()
        (self.inputs / "problem.txt").write_text("Official problems: Q1, Q2", encoding="utf-8")
        (self.inputs / "data.csv").write_text("x,y\n1,2\n", encoding="utf-8")
        self.workspace = root / "work"
        auto.init(self.workspace, self.inputs)

    def report(self, stage, *, decision="passed", **extra):
        (self.workspace / "reviews").mkdir(exist_ok=True)
        (self.workspace / "artifacts").mkdir(exist_ok=True)
        filename = f"artifacts/{stage}.txt"
        (self.workspace / filename).write_text(
            f"{stage}: actual synthetic verification artifact, not competition data.\n",
            encoding="utf-8",
        )
        data = {
            "stage": stage, "decision": decision, "artifacts": [filename],
            "checks": {
                name: {"status": "passed", "artifact": filename,
                       "method": f"independent synthetic check of {name}"}
                for name in auto.CHECKS[stage]
            },
        }
        data.update(extra)
        (self.workspace / "reviews" / f"{stage}.json").write_text(
            json.dumps(data, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        return data

    def start_through(self, last):
        for stage in auto.STAGES[1:auto.STAGES.index(last)+1]:
            self.report(stage)
        while True:
            result = auto.advance(self.workspace)
            if result["status"] == "awaiting_human_approval":
                auto.approve(self.workspace, result["next"], "authorized-human")
                continue
            return result


class AutopilotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.f = AutopilotFixture(Path(self.tmp.name))

    def test_init_fingerprints_inputs_and_detects_first_stage(self):
        state = auto.load(self.f.workspace)
        self.assertEqual(len(state["inputs"]), 2)
        self.assertEqual(auto.summary(self.f.workspace)["next"], "contract")
        self.assertEqual(auto.advance(self.f.workspace)["status"], "awaiting_work")

    def test_full_project_needs_explicit_approvals(self):
        f = self.f
        for stage in auto.STAGES[1:]:
            f.report(stage)
        out = auto.advance(f.workspace)
        self.assertEqual((out["status"], out["next"]), ("awaiting_human_approval", "plan"))
        auto.approve(f.workspace, "plan", "real-user-confirmed")
        out = auto.advance(f.workspace)
        self.assertEqual((out["status"], out["next"]), ("awaiting_human_approval", "delivery"))
        auto.approve(f.workspace, "delivery", "real-user-confirmed")
        out = auto.advance(f.workspace)
        self.assertEqual(out["status"], "machine_workflow_complete")
        self.assertEqual(auto.summary(f.workspace)["next"], "complete")
        self.assertIn("not scientific", out["message"].lower())

    def test_cannot_skip_upstream_contract(self):
        self.f.report("data")
        out = auto.advance(self.f.workspace)
        self.assertEqual(out["next"], "contract")

    def test_empty_evidence_file_blocks(self):
        f = self.f
        f.report("contract")
        (f.workspace / "artifacts/contract.txt").write_text("")
        out = auto.advance(f.workspace)
        self.assertEqual(out["status"], "gate_blocked")

    def test_failed_check_blocks(self):
        f = self.f
        report = f.report("contract")
        report["checks"]["all_questions_mapped"]["status"] = "failed"
        (f.workspace / "reviews/contract.json").write_text(json.dumps(report))
        out = auto.advance(f.workspace)
        self.assertEqual(out["status"], "gate_blocked")

    def test_non_waivable_check_blocks(self):
        f = self.f
        report = f.report("contract")
        report["checks"]["all_questions_mapped"] = {
            "status": "not_applicable", "reason": "There were no questions to consider"}
        (f.workspace / "reviews/contract.json").write_text(json.dumps(report))
        self.assertEqual(auto.advance(f.workspace)["status"], "gate_blocked")

    def test_unrelated_files_cannot_back_artifact(self):
        f = self.f
        report = f.report("contract")
        report["checks"]["unknowns_identified"]["artifact"] = "unrelated-file.txt"
        (f.workspace / "reviews/contract.json").write_text(json.dumps(report))
        self.assertEqual(auto.advance(f.workspace)["status"], "gate_blocked")

    def test_symlink_or_escape_blocked(self):
        f = self.f
        report = f.report("contract")
        report["artifacts"] = ["../official_inputs/problem.txt"]
        (f.workspace / "reviews/contract.json").write_text(json.dumps(report))
        self.assertEqual(auto.advance(f.workspace)["status"], "gate_blocked")

    def test_modified_accepted_artifact_invalidates_downstream(self):
        f = self.f
        out = f.start_through("baseline")
        self.assertEqual(out["next"], "solve")
        (f.workspace / "artifacts/baseline.txt").write_text("changed result")
        out = auto.advance(f.workspace)
        self.assertEqual((out["status"], out["next"]), ("awaiting_rework", "baseline"))
        self.assertNotIn("baseline", auto.load(f.workspace)["completed"])
        self.assertIn("plan", auto.load(f.workspace)["approvals"])  # earlier model approval remains valid if only baseline changes

    def test_modified_accepted_review_must_be_redone(self):
        f = self.f
        f.report("contract")
        self.assertEqual(auto.advance(f.workspace)["next"], "data")
        old = json.loads((f.workspace / "reviews/contract.json").read_text())
        old["comment"] = "changed explanation"
        (f.workspace / "reviews/contract.json").write_text(json.dumps(old))
        self.assertEqual(auto.advance(f.workspace)["next"], "data")  # changed review recertified
        self.assertIn("contract", auto.load(f.workspace)["completed"])

    def test_modified_official_input_blocks_until_explicit_sync(self):
        f = self.f
        f.report("contract")
        self.assertEqual(auto.advance(f.workspace)["next"], "data")
        (f.inputs / "problem.txt").write_text("amended official problem", encoding="utf-8")
        self.assertEqual(auto.advance(f.workspace)["status"], "inputs_changed")
        out = auto.advance(f.workspace, sync_inputs=True)
        self.assertEqual((out["status"], out["next"]), ("awaiting_rework", "contract"))

    def test_leakage_failure_rewinds_to_data_not_paper(self):
        f = self.f
        f.start_through("solve")
        f.report("verify", decision="failed", failure_class="leakage",
                 reason="Validation joined on future labels; rebuild splits and models.")
        out = auto.advance(f.workspace)
        self.assertEqual((out["status"], out["next"]), ("rewind", "data"))
        self.assertNotIn("solve", auto.load(f.workspace)["completed"])
        self.assertEqual(auto.advance(f.workspace)["status"], "awaiting_rework")

    def test_retry_budget_escalates_to_human(self):
        f = self.f
        for i in range(3):
            f.report("contract", decision="failed", failure_class="task_mismatch",
                     reason=f"Missed official task constraint iteration {i}.")
            result = auto.advance(f.workspace)
            self.assertEqual(result["attempts"], i + 1)
        self.assertEqual(result["status"], "human_escalation")
        self.assertEqual(auto.advance(f.workspace)["status"], "human_escalation")

    def test_incomplete_failure_record_cannot_trigger_rollback(self):
        f = self.f
        f.report("contract", decision="failed", failure_class="leakage", reason="bad")
        self.assertEqual(auto.advance(f.workspace)["status"], "invalid_failure")

    def test_plan_approval_requires_current_stage_and_good_evidence(self):
        f = self.f
        f.report("plan")
        with self.assertRaises(ValueError):
            auto.approve(f.workspace, "plan", "user")
        f.report("contract")
        f.report("data")
        out = auto.advance(f.workspace)
        self.assertEqual(out["next"], "plan")
        self.assertEqual(auto.approve(f.workspace, "plan", "user")["status"], "approval_recorded")

    def test_old_approval_does_not_survive_revision(self):
        f = self.f
        f.start_through("plan")
        self.assertEqual(auto.summary(f.workspace)["next"], "baseline")
        report = json.loads((f.workspace / "reviews/plan.json").read_text())
        report["revision"] = 2
        (f.workspace / "reviews/plan.json").write_text(json.dumps(report))
        self.assertEqual(auto.advance(f.workspace)["next"], "plan")
        self.assertEqual(auto.advance(f.workspace)["status"], "awaiting_human_approval")

    def test_repeated_run_is_idempotent(self):
        f = self.f
        f.report("contract")
        self.assertEqual(auto.advance(f.workspace)["next"], "data")
        a = auto.load(f.workspace)
        self.assertEqual(auto.advance(f.workspace)["next"], "data")
        b = auto.load(f.workspace)
        self.assertEqual(a["completed"], b["completed"])

    def test_initializing_existing_workspace_fails_safe(self):
        with self.assertRaises(ValueError):
            auto.init(self.f.workspace, self.f.inputs)

    def test_source_and_workspace_cannot_be_nested(self):
        with self.assertRaises(ValueError):
            auto.inputs_snapshot(self.f.inputs, self.f.inputs / "nested")

    def test_template_has_all_checks_but_none_prepassed(self):
        for stage, fields in auto.CHECKS.items():
            self.assertTrue(fields)
            self.assertTrue(all(isinstance(f, str) for f in fields))
        self.assertNotIn("delivery", auto.FAIL_BACKTRACK.values())

    def test_corrupt_json_review_does_not_crash(self):
        f = self.f
        (f.workspace / "reviews").mkdir()
        (f.workspace / "reviews/contract.json").write_text("{INVALID", encoding="utf-8")
        self.assertEqual(auto.advance(f.workspace)["status"], "invalid_review")


if __name__ == "__main__":
    unittest.main()
