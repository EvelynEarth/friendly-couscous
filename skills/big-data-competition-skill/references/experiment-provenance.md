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