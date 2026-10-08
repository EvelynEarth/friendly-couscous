# 通用数值必要条件契约（填写后以 JSON 保存）

此模板适合任意任务，但**各项检查仅在官方题意/所选模型数学定义确实要求时添加**。不要把以下条件一股脑当作所有比赛任务的默认约束。

首先从**实际求解**导出 JSON 文件，例如：
```json
{
  "values": {
    "probabilities": [[0.25, 0.75], [0.1, 0.9]],
    "allocation": [2, 3],
    "inventory": [0, 1, 3]
  }
}
```

然后在独立的 `invariants.json` 中填写：
```json
{
  "case_id": "official-task-or-subquestion",
  "result_sha256": "填入实际结果文件的64位小写SHA256",
  "invariants": [
    {"id": "P1", "field": "probabilities", "op": "row_sum_close", "target": 1, "tolerance": 1e-10},
    {"id": "B1", "field": "allocation", "op": "bounds", "lower": 0, "upper": 10},
    {"id": "C1", "field": "allocation", "op": "linear_le", "weights": [2, 1], "rhs": 7},
    {"id": "M1", "field": "inventory", "op": "monotonic", "direction": "nondecreasing"}
  ]
}
```

**上面的 2、3、0.25 等只是语法示例，绝对不是实际赛题计算结果。** 每个 `id` 应唯一。`tolerance` 默认零，必须根据单位/理论与数值求解误差事先制定。支持的操作及语义见 [反证检查协议](../references/result-falsification.md)。比较的矩阵只检查每行和，不会自动检测概率非负；若需同时确保每个概率在 [0,1]，应使用其他独立测试或按列/输出结构补充验证。可复用工具不可能覆盖所有科学必要条件。

```bash
python skills/big-data-competition-skill/tools/result_invariant_gate.py --contract contract/invariants.json --result outputs/numeric_result.json
```

成功只表示输入契约中**已经定义的**条件逐条满足。要检验其他条件，应该在真正的求解代码中写项目专属的单元测试、比较独立求解器或做手算边界检查；不要把这个工具成功输出当作“论文和数学模型正确”。
