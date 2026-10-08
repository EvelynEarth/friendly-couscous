"""Actual-result falsification checks and strong metric-file binding (stdlib)."""
from __future__ import annotations

from copy import deepcopy
import hashlib
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "skills/big-data-competition-skill/tools"


def load(name, path):
    spec = spec_from_file_location(name, path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


invariants = load("result_invariant_gate", TOOLS / "result_invariant_gate.py")
evidence = load("paper_evidence_gate_v25", TOOLS / "paper_evidence_gate.py")


def invariant_case():
    values = {
        "probability": [[0.25, 0.75], [0.1, 0.9]],
        "decision": [2, 3],
        "inventory": [0, 2, 4],
        "inventory_copy": [0, 2, 4],
    }
    raw = json.dumps({"values": values}).encode("utf-8")
    contract = {
        "case_id": "unknown-future-problem-QX",
        "result_sha256": hashlib.sha256(raw).hexdigest(),
        "invariants": [
            {"id": "prob_sum", "field": "probability", "op": "row_sum_close",
             "target": 1, "tolerance": 1e-12},
            {"id": "nonnegative", "field": "decision", "op": "bounds",
             "lower": 0, "upper": 10},
            {"id": "capacity", "field": "decision", "op": "linear_le",
             "weights": [2, 1], "rhs": 7},
            {"id": "minimum_throughput", "field": "decision", "op": "linear_ge",
             "weights": [1, 1], "rhs": 5},
            {"id": "inventory_order", "field": "inventory", "op": "monotonic",
             "direction": "nondecreasing"},
            {"id": "inventory_accounting", "field": "inventory",
             "op": "equal_fields", "other_field": "inventory_copy"},
            {"id": "sum_of_allocations", "field": "decision", "op": "sum_close",
             "target": 5},
        ],
    }
    return contract, {"values": values}, raw


def accepted(root):
    parts = {"split.csv": b"id,fold\n1,train\n2,valid\n",
             "metrics.json": b'{"metrics":{"f1":0.73}}\n'}
    artifacts = []
    for path, content in parts.items():
        (root / path).write_bytes(content)
        artifacts.append({"path": path, "sha256": hashlib.sha256(content).hexdigest()})
    return {
        "experiment_id": "real-experiment-001", "run_status": "accepted",
        "data_version": "recorded-data-hash", "code_revision": "recorded-code-revision",
        "validation_scheme": "group-holdout", "split_protocol": "entities-isolated",
        "random_seed": 42, "split_manifest": "split.csv",
        "metrics_artifact": "metrics.json", "metrics": {"f1": 0.73},
        "artifacts": artifacts,
        "claims": [{"claim_id": "CLAIM1", "metric": "f1", "value": 0.73,
                    "artifact": "metrics.json", "paper_location": "results section"}],
    }


class InvariantTests(unittest.TestCase):
    def test_valid_numerical_conditions(self):
        c, data, raw = invariant_case()
        output = invariants.audit(c, data, raw)
        self.assertEqual(output["status"], "necessary_checks_passed", output)
        self.assertEqual(len(output["checks"]), 7)

    def test_failing_probability_row(self):
        c, data, raw = invariant_case()
        data["values"]["probability"][1] = [0.8, 0.8]
        self.assertEqual(invariants.audit(c, data, raw)["status"], "blocked")
        c["result_sha256"] = hashlib.sha256(json.dumps(data).encode()).hexdigest()
        out = invariants.audit(c, data, json.dumps(data).encode())
        self.assertEqual(out["failed_invariants"], 1)
        self.assertEqual(out["checks"][0]["id"], "prob_sum")

    def test_capacity_and_bounds_detect_violations(self):
        c, data, raw = invariant_case()
        data["values"]["decision"] = [-2, 20]
        raw = json.dumps(data).encode()
        c["result_sha256"] = hashlib.sha256(raw).hexdigest()
        out = invariants.audit(c, data, raw)
        self.assertEqual(out["status"], "blocked")
        self.assertTrue(any(x["id"] == "nonnegative" and not x["passed"]
                            for x in out["checks"]))

    def test_mass_conservation_and_order_rejected(self):
        c, data, raw = invariant_case()
        data["values"]["inventory"][2] = 1
        raw = json.dumps(data).encode()
        c["result_sha256"] = hashlib.sha256(raw).hexdigest()
        out = invariants.audit(c, data, raw)
        self.assertGreaterEqual(out["failed_invariants"], 2)

    def test_old_sha_never_silently_passes_new_result(self):
        c, data, raw = invariant_case()
        self.assertEqual(invariants.audit(c, data, raw)["status"], "necessary_checks_passed")
        newer = raw + b" "
        self.assertEqual(invariants.audit(c, data, newer)["status"], "blocked")

    def test_bad_contract_missing_or_unsupported_invariant(self):
        c, data, raw = invariant_case()
        c["invariants"].append({"id": "evil", "field": "decision", "op": "exec"})
        self.assertEqual(invariants.audit(c, data, raw)["status"], "blocked")
        c["invariants"] = []
        self.assertEqual(invariants.audit(c, data, raw)["status"], "blocked")

    def test_nonfinite_and_mismatched_weights_rejected(self):
        c, data, raw = invariant_case()
        c["invariants"][2]["weights"] = [1]
        self.assertEqual(invariants.audit(c, data, raw)["status"], "blocked")
        c, data, raw = invariant_case()
        data["values"]["decision"][0] = float("nan")
        raw = json.dumps(data).encode()
        c["result_sha256"] = hashlib.sha256(raw).hexdigest()
        self.assertEqual(invariants.audit(c, data, raw)["status"], "blocked")

    def test_hash_bound_is_not_model_correctness(self):
        c, data, raw = invariant_case()
        out = invariants.audit(c, data, raw)
        self.assertIn("no guarantee", out["meaning"])


class MetricSourceTests(unittest.TestCase):
    def test_strict_hash_bound_metrics_file_passes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = accepted(root)
            result = evidence.audit_record(doc, root, require_metric_source=True)
            self.assertEqual(result["status"], "trace_consistent", result)
            self.assertTrue(result["metrics_source_verified"])
            self.assertTrue(result["strict_mode"])

    def test_legacy_record_blocked_in_strict_mode(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = accepted(root)
            del doc["metrics_artifact"]
            self.assertEqual(evidence.audit_record(doc, root, True)["status"], "blocked")
            self.assertEqual(evidence.audit_record(doc, root)["status"], "trace_consistent")

    def test_record_and_claim_collusion_fails_against_real_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = accepted(root)
            doc["metrics"]["f1"] = 0.99
            doc["claims"][0]["value"] = 0.99
            res = evidence.audit_record(doc, root, True)
            self.assertEqual(res["status"], "blocked")
            self.assertTrue(any("actual metrics_artifact" in x for x in res["errors"]))

    def test_claim_cannot_point_to_arbitrary_verified_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = accepted(root)
            doc["claims"][0]["artifact"] = "split.csv"
            out = evidence.audit_record(doc, root, True)
            self.assertEqual(out["status"], "blocked")
            self.assertTrue(any("must reference metrics_artifact" in x for x in out["errors"]))

    def test_changed_metrics_artifact_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = accepted(root)
            (root / "metrics.json").write_text('{"metrics":{"f1":0.99}}\n', encoding="utf-8")
            self.assertEqual(evidence.audit_record(doc, root, True)["status"], "blocked")

    def test_non_numeric_metrics_file_rejected_even_if_hash_valid(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            doc = accepted(root)
            data = b'{"metrics":{"f1":"0.73"}}\n'
            (root / "metrics.json").write_bytes(data)
            doc["artifacts"][1]["sha256"] = hashlib.sha256(data).hexdigest()
            self.assertEqual(evidence.audit_record(doc, root, True)["status"], "blocked")

    def test_strict_cli_accepts_supported_parameter(self):
        # Invocation from CI must use --require-metric-source; signature stays backward compatible.
        self.assertIn("require_metric_source", evidence.audit_record.__code__.co_varnames)


if __name__ == "__main__":
    unittest.main()
