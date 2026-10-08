# Experiment Provenance

每个关键实验记录：

experiment_id
question
hypothesis
data_version
feature_version
method
parameters
validation_scheme
random_seed
metrics
runtime
artifacts
decision
limitations

## Selection provenance

最终模型必须有选择理由。至少保存 baseline、候选、最终模型的可比较记录。

## Reproducibility

同一结论应能通过代码、数据版本、参数和验证方案重新得到。用户未执行的题目专属代码不能被描述为“已运行”。
## 稳定性和失败实验也是实验溯源

除最终最优运行之外，还保存独立验证、未通过的边界条件、参数/种子扰动、基线成对结果及阈值**事先确定**的依据。描述性汇总可用 [真实重复运行稳定性工具](stability-and-uncertainty.md)，但输出不能被当作置信区间。独立 Reviewer 必须根据 artifact 检验逻辑与实际结果，而不是根据记录字段的 `passed` 文字打勾。
