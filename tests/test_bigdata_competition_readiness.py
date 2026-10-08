"""Task-agnostic review package tests: multiple non-numeric unknown contest tasks.

Synthetic fixtures verify the gate, NOT model correctness or award-paper content.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "skills/big-data-competition-skill/tools/competition_readiness.py"
spec = importlib.util.spec_from_file_location("competition_readiness", TOOL)
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class Sample:
    def __init__(self, root):
        self.root = root
        self.content = {
            "review.txt": b"Independent counterexample checks for toy problems.\n",
            "paper.md": b"# Synthetic contest manuscript\nToy examples, not a real competition result.\n",
            "values.csv": b"x,answer\n1,2\n",
            "rules.txt": b"Synthetic official-format requirements, not current contest rules.\n",
        }
        self.claims = [
            {"id": "C1", "question_id": "Q1", "statement": "Toy predicted values were checked",
             "strength": "predictive", "scope_and_limitations": "Synthetic numeric toy only, not test accuracy.",
             "evidence": ["values.csv"], "status": "supported"},
            {"id": "C2", "question_id": "Q2", "statement": "Toy descriptive interpretation evaluated",
             "strength": "qualified", "scope_and_limitations": "Synthetic qualitative text, no external inference.",
             "evidence": ["review.txt"], "status": "supported"},
        ]
        def checks():
            return {
                k: {"status": "passed", "method": "Independent examiner checks example outputs",
                    "artifact": "review.txt", **({"independent": True} if k == "independent_verification" else {})}
                for k in gate.REVIEW_KEYS
            }
        self.questions = [
            {"id": "Q1", "objective": "prediction", "official_output": "Predict synthetic target in units",
             "delivered_answer": "Predicted numerical result for toy problem",
             "model_choice_reason": "Simple baseline with independent check on toy",
             "claim_ids": ["C1"], "reviews": checks()},
            {"id": "Q2", "objective": "other", "official_output": "Interpret described synthetic pattern",
             "delivered_answer": "Interpretation and limitations of toy pattern",
             "model_choice_reason": "Direct qualitative reasoning with counterexamples",
             "claim_ids": ["C2"], "reviews": checks()},
        ]
        self.doc = {
            "schema_version": 1, "competition_id": "toy-not-official",
            "official_questions": ["Q1", "Q2"], "questions": self.questions,
            "claims": self.claims,
            "paper": {
                "manuscript": "paper.md",
                "sections": [
                    {"function": k, "argument": f"Function of {k} in supporting study",
                     "claim_ids": ["C1", "C2"] if k == "results" else []}
                    for k in ("problem", "method", "validation", "results", "discussion", "conclusion")
                ],
                "conclusion_claim_ids": ["C1", "C2"],
            },
            "delivery": {
                "rules_from_current_competition_verified": True,
                "official_requirements": [
                    {"id": "paper_pdf", "status": "checked",
                     "detail": "Synthetic placeholder for official checked rule",
                     "artifact": "rules.txt"},
                ],
            },
        }

    def audit(self):
        for name, data in self.content.items():
            (self.root/name).write_bytes(data)
        self.doc["files"] = [
            {"path": k, "sha256": hashlib.sha256(v).hexdigest()}
            for k, v in self.content.items()
        ]
        return gate.audit(self.doc, self.root)


class CompetitionReadinessTests(unittest.TestCase):
    def with_sample(self, mutation=None):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Sample(Path(temp))
            if mutation:
                mutation(fixture)
            return fixture.audit()

    def test_task_families_not_locked_to_builtin_oracles(self):
        result = self.with_sample()
        self.assertEqual(result["status"], "documentation_consistent_pending_expert_review", result)
        self.assertEqual(result["official_questions"], 2)
        self.assertEqual(result["scientific_approval"], "not_granted_by_automation")

    def test_missing_question_blocks(self):
        out = self.with_sample(lambda s: s.doc["official_questions"].append("Q3"))
        self.assertEqual(out["status"], "blocked")
        self.assertTrue(any("EVERY" in e for e in out["issues"]))

    def test_missing_independent_verification_blocks(self):
        out = self.with_sample(lambda s: s.questions[0]["reviews"]["independent_verification"].update(status="pending"))
        self.assertEqual(out["status"], "blocked")

    def test_status_alone_is_not_evidence(self):
        out = self.with_sample(lambda s: s.questions[0]["reviews"]["model_correctness"].update(artifact="not-found.txt"))
        self.assertEqual(out["status"], "blocked")

    def test_stability_waiver_with_specific_reason(self):
        def modify(s):
            s.questions[1]["reviews"]["stability"] = {
                "status": "not_applicable",
                "reason": "A purely static descriptive identity has no perturbation parameter."
            }
        self.assertEqual(self.with_sample(modify)["status"], "documentation_consistent_pending_expert_review")

    def test_stability_waiver_without_reason_blocks(self):
        out = self.with_sample(lambda s: s.questions[1]["reviews"].update(stability={"status":"not_applicable"}))
        self.assertEqual(out["status"], "blocked")

    def test_numeric_claim_not_in_manuscript_blocks(self):
        def modify(s):
            for sec in s.doc["paper"]["sections"]:
                sec["claim_ids"] = ["C2"] if sec["function"] == "results" else []
        self.assertEqual(self.with_sample(modify)["status"], "blocked")

    def test_missing_official_answer_in_conclusion_blocks(self):
        out = self.with_sample(lambda s: s.doc["paper"].update(conclusion_claim_ids=["C1"]))
        self.assertEqual(out["status"], "blocked")

    def test_no_final_manuscript_blocks(self):
        out = self.with_sample(lambda s: s.doc["paper"].update(manuscript="missing.md"))
        self.assertEqual(out["status"], "blocked")

    def test_wrong_file_hash_blocks(self):
        def modify(s):
            s.content["paper.md"] = b"new manuscript\n"
            s.doc["files"] = [{"path":"paper.md", "sha256": "0"*64}]
        # Fixture computes own hashes: test corruption after snapshot manually.
        with tempfile.TemporaryDirectory() as temp:
            fixture = Sample(Path(temp))
            self.assertEqual(fixture.audit()["status"], "documentation_consistent_pending_expert_review")
            (fixture.root/"paper.md").write_bytes(b"changed\n")
            self.assertEqual(gate.audit(fixture.doc, fixture.root)["status"], "blocked")

    def test_path_traversal_blocks(self):
        def modify(s):
            s.content["../outside.txt"] = b"unsafe"
        # Avoid writing traversal outside temp: manipulate validated snapshot only.
        with tempfile.TemporaryDirectory() as temp:
            fixture = Sample(Path(temp))
            fixture.audit()
            fixture.doc["files"].append({"path":"../outside.txt", "sha256":"0"*64})
            self.assertEqual(gate.audit(fixture.doc, fixture.root)["status"], "blocked")

    def test_missing_claim_source_blocks(self):
        out = self.with_sample(lambda s: s.claims[0].update(evidence=["unverified.csv"]))
        self.assertEqual(out["status"], "blocked")

    def test_unsupported_causal_statement_without_causal_task_blocks(self):
        out = self.with_sample(lambda s: s.claims[1].update(strength="causal"))
        self.assertEqual(out["status"], "blocked")

    def test_optimality_needs_rationale_even_if_task_is_optimization(self):
        def modify(s):
            s.questions[0]["objective"] = "optimization"
            s.claims[0]["strength"] = "optimal"
        self.assertEqual(self.with_sample(modify)["status"], "blocked")

    def test_paper_missing_validation_logic_blocks(self):
        def modify(s):
            s.doc["paper"]["sections"] = [
                x for x in s.doc["paper"]["sections"] if x["function"] != "validation"
            ]
        self.assertEqual(self.with_sample(modify)["status"], "blocked")

    def test_official_delivery_checklist_is_mandatory(self):
        out = self.with_sample(lambda s: s.doc["delivery"].update(official_requirements=[]))
        self.assertEqual(out["status"], "blocked")

    def test_new_official_rules_not_verified_blocks(self):
        out = self.with_sample(lambda s: s.doc["delivery"].update(rules_from_current_competition_verified=False))
        self.assertEqual(out["status"], "blocked")

    def test_missing_all_claims_blocks(self):
        out = self.with_sample(lambda s: s.doc.update(claims=[]))
        self.assertEqual(out["status"], "blocked")

    def test_every_question_requires_all_its_claim_ids(self):
        out = self.with_sample(lambda s: s.questions[0].update(claim_ids=[]))
        self.assertEqual(out["status"], "blocked")

    def test_malformed_nested_unhashable_input_blocks_without_crashing(self):
        out = self.with_sample(lambda s: s.questions[0].update(objective=["not-a-string"]))
        self.assertEqual(out["status"], "blocked")
        out = self.with_sample(lambda s: s.questions[0].update(claim_ids=[{"bad": "value"}]))
        self.assertEqual(out["status"], "blocked")

    def test_malformed_paper_role_is_blocked(self):
        def modify(s):
            s.doc["paper"]["sections"][0]["function"] = {"unhashable": True}
        self.assertEqual(self.with_sample(modify)["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
