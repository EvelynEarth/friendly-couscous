# 真实重复运行稳定性记录

> 只在真的运行多次、锁定评价协议之后填写。此模板的数值均为占位符，**不可当作历史赛题或任何模型的实际结果**。

```json
{
  "metric": "official_or_justified_metric",
  "direction": "maximize",
  "protocol_id": "validation-protocol-and-split-version",
  "data_version": "hash-or-immutable-version",
  "perturbation": "random_seed",
  "threshold_predeclared": false,
  "max_range": null,
  "claim_improvement": false,
  "min_paired_gain": null,
  "runs": []
}
```

填写 `runs` 时，每项包含唯一 `run_id`、真实 `value`，以及在相同验证协议/拆分条件下可比较的 `baseline_value`（仅在确实做了配对基线时填写，必须每次都有）。至少三个真实值才能尝试检查本工具的样本内波动；这不是普遍适用的统计功效要求。阈值必须在看结果前定好，并通过项目实验日志证明时间顺序，不能只随意勾选布尔值。

```bash
python skills/big-data-competition-skill/tools/stability_audit.py --record /path/to/actual_runs.json
```

工具输出 `mean`、`sample_sd`、`observed_range`、成对增益摘要以及是否满足用户**预声明的**范围。只支持描述性检查；时间窗变化/群体迁移/数值逼近/参数扰动等若产生依赖数据，仍须单独设计有效的区间或比较方法。见 [稳定性与不确定性说明](../references/stability-and-uncertainty.md)。
