# 报告指标恒等式验收输入（只核表内数值）

当论文同时报告 MAE、MSE、RMSE，且它们在**相同原子残差、相同权重、相同缩放口径**计算时，必须检查 `MSE = RMSE²` 和 `MAE ≤ RMSE`。若不能确认三个条件，标记 `not_comparable_requires_review`，不要判通过或判造假。

示意输入为真实获奖PDF 2024-04 物理第19页报告的**原文数值**，但 `comparability` 是**为演示“假设口径相同”而提供的条件**，不是已经审计该论文原始指标代码的断言：

```json
{"checks":[{"experiment_id":"award-2024-04-p19-conditional-example","metrics":{"RMSE":0.0336,"MSE":0.0071,"MAE":0.0295},"comparability":{"same_samples":true,"same_weights":true,"same_error_scale":true},"rounding_tolerance_mse":0.00015}]}
```

命令（先将 JSON 另存为 metrics_contract.json）：
```bash
python skills/big-data-competition-skill/tools/paper_metric_identity_gate.py --input metrics_contract.json --report reports/metric_arithmetic.json
```

结果不符返回状态 `blocked` 和退出码1。符合算术关系只表示 `arithmetic_consistent_only`，不能代替从实际原子预测重算、原始指标文件SHA核对、无泄漏审查。口径不明退出码2，请 Scientific Reviewer 核对实际定义。**不同预测样本/权重/尺度的指标不能强套恒等式。**
