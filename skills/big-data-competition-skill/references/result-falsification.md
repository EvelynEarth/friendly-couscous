# 真实结果的反证测试：数值不变式与论文指标文件闭环（v2.5）

**目的：从“已经填写审核记录”推进到对实际生成的结果文件运行反例/必要条件测试。** 与赛题年份和算法族无关；本届官方题意始终决定是否需要某项约束。不可先看输出再随意编造让模型通过的条件。

## 第一步：先写出能推翻求解结果的条件

根据当届题意冻结：输出数据的数学类型、单位、支持域、约束、必要守恒关系、边界值、独立复核方法和不能解释的情况。比如概率向量和为一，预测资源分配非负并不超容量，库存状态的守恒/单调性，两个独立计算式是否一致。**不要机械把所有条件强加给所有任务**：例如未归一化的回归分数不应该做“概率之和为一”检查。

在构建模型或查看最佳结果前制定 [结果不变式 JSON 契约](../templates/result-invariant-contract.md)。每条条件应与官方题意或模型定义相对应，不能拿作者自定义的松弛阈值遮掩约束违反。

## 第二步：对实际输出文件实施数值检查

提供的标准库 CLI：

```bash
python skills/big-data-competition-skill/tools/result_invariant_gate.py --result outputs/numeric_result.json --contract contract/invariants.json
```

- 输入必须为实际输出的 JSON：`{"values": {"allocation": [2, 3], "probabilities": [[0.2, 0.8], [0.7, 0.3]]}}`，并在契约中记录结果文件的**实际 SHA-256**。
- 内置不变式：`bounds`、`sum_close`、`row_sum_close`、`linear_le`、`linear_ge`、`monotonic`、`equal_fields`。不执行 eval、第三方求解器、任意表达式、网络服务或用户脚本。
- 核对真实 JSON 是否仍是原先验收的那一份、数值是否有限、表达式所需维度是否一致，并逐条报告通过或失败。
- `necessary_checks_passed` **仅代表本次声明的必要条件没有被推翻**；不能证明目标函数已经正确求解、因果关系存在、得到全局最优或预测具有外部效度。
- 某条件失败时，先排查量纲、公式、程序/求解器与边界，再决定修复模型或明确结论局限。不能仅提高 `tolerance` 使检测变绿。

其他题型可通过自写、可追溯的独立 Python 单元测试检查已知答案小样本、KKT/对偶界、数值收敛、分布统计、模拟守恒、误差传播或其他更符合该题的性质；这些检验不属于此轻量 DSL 已经覆盖的能力。

## 第三步：论文数字必须回读真实指标文件

原 `paper_evidence_gate.py` 可以对比“审核记录中的 metrics”和“论文 claims”，却未强制再次读取真实指标文件。两份人工记录一起写错时不会发现。新增严格模式：

```bash
python skills/big-data-competition-skill/tools/paper_evidence_gate.py --record outputs/accepted_record.json --artifact-root outputs --require-metric-source
```

在接受记录中增加 `"metrics_artifact": "metrics.json"`；必须是 `artifacts` 列表中的 SHA-256 已验证文件，内容为 `{"metrics":{"some_metric":0.8}}` 或直接为数值字典。工具核查实际指标文件数值、记录中的 `metrics` 和每条论文 `claims` **三方一致**。严格模式下，数值 claim 必须指向这个指标文件，不能随便引用某个无关文件就通过。`split_manifest` 也必须是实际 SHA 校验成功的文件。

为保证旧项目兼容，没有传入 `--require-metric-source` 时保留原先接受记录格式。**论文正式定稿建议始终启用严格模式**。旧格式的通过只表示弱化的溯源完整性，不能视作新强度审核通过。

## 第四步：独立科学复核仍是最终前提

三方数值一致仍可能是算法把指标算错；结果满足有限个不变式，也可能模型不符合原题。还必须检查训练/测试隔离、复现、模型假设、手算/独立重算、优化可行性与最优界、参数敏感性、反例和论文结论的适用范围。

理想的论文逻辑为：**问题 → 为什么选这套方法 → 关键公式/算法 → 结果如何独立验证 → 可靠性和稳定性 → 必要条件是否满足 → 具体能得出哪些结论 → 在哪里不成立**。学习优秀论文的是这条论证链，而不是机械复制某年的模型或三问结构。

配合 [通用求解正确性协议](solution-validity.md)、[稳定性与不确定性](stability-and-uncertainty.md) 和 [论文论证逻辑](paper-argumentation.md) 使用。
