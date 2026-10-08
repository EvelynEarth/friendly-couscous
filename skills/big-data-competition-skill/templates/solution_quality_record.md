# 通用求解质量审核记录（JSON 字段约定）

> 示例只是字段结构，不含真实通过证据。不要把 status 自动填成 passed。工具 `solution_quality_gate.py` 只验证声明与引用的完整性，不能证明模型科学正确。

每一个子问题在 `questions` 里单独记录，数量不固定。下面为字段结构提示；正式文件必须是有效 JSON：

```json
{
  "case_id": "current-official-problem-id",
  "questions": [
    {
      "id": "Q1",
      "objective": "prediction",
      "expected_output": "official objective and units",
      "actual_output": "what the model actually computes",
      "model_rationale": "why this model, its assumptions and alternative considered",
      "limitations": ["at least one concrete limitation"],
      "checks": {
        "question_answer_alignment": {"status": "pending"},
        "assumptions_and_domain": {"status": "pending"},
        "units_and_boundary_cases": {"status": "pending"},
        "independent_verification": {"status": "pending"},
        "baseline_or_reference": {"status": "pending"},
        "uncertainty_and_error": {"status": "pending"},
        "stability_and_sensitivity": {"status": "pending"},
        "claim_evidence_alignment": {"status": "pending"},
        "evaluation_design": {"status": "pending"},
        "leakage_control": {"status": "pending"}
      },
      "claims": [
        {"statement": "do not claim before checking", "strength": "qualified", "status": "pending", "artifact": ""}
      ]
    }
  ]
}
```

全部通用字段见 `solution_quality_gate.py` 常量 `GENERAL`；按 `objective` 自动要求：
- prediction：evaluation_design, leakage_control
- causal：identification_and_confounding
- optimization：constraint_feasibility, optimality_or_gap
- simulation：randomness_and_convergence
- inference：identifiability_and_uncertainty

`passed` 必须说明 `method` 和 `artifact`；独立复核还需 `independent: true`，并且实际由不同路线复算。除特别关键项以外，可在真实不适用时用 `not_applicable` 加充分的 `reason`，不能虚假免检。请同时参考 [质量审查](../references/solution-validity.md)。

正式提交前，检查每一项 `artifact` 是否为实际运行、可追溯的证据；如需要数值哈希层核验，另运行 `paper_evidence_gate.py`。这两个工具也不能取代人工独立审稿。
