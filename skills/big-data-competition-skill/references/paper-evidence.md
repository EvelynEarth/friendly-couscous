# Competition Paper Evidence

主要结论的证据优先级：
1. 直接实验或计算
2. 数学推导
3. 可靠外部文献
4. 明确标注的解释

任务正文模板：
Objective → Data and Variables → Method → Experimental Design → Results → Interpretation → Limitations。

每个强结论都要检查：
- 什么证据支持？
- 是否可能由泄漏造成？
- 实验是否能够识别因果？
- 样本量是否足够？
- 是否超出了验证范围？
- 另一个人能否复现这个数字？

不要把相关性写成因果关系，不要把单次实验写成普遍稳定提升。
## 已执行实验的可验证产物（v2.3）

[实验证据记录模板](../templates/accepted-evidence-record.md) 与 [真实赛题复盘协议](real-case-replay.md) 要求论文数字指向实际运行的 metric、split、数据代码版本及每个产物 SHA-256。`paper_evidence_gate.py` 只验证对应完整性；指标科学正确性、无泄漏和模型优越性仍需独立评估。

## v2.5 真实指标源与论文数字双向核查

仅将 `metrics` 复制进实验记录，并不能证明指标来自实际运行：如果正文和记录同时写错，过去的“二者相同”检查可能误通过。正式论文定稿时按照 [结果反证与真实指标三方校验](result-falsification.md) 运行 `paper_evidence_gate.py --require-metric-source`，把指标 JSON 真实内容、artifact 的 SHA-256、接受记录与论文 claim 绑定核查。记录中的 `metrics_artifact` 必须是真实且已被哈希验证的源文件；独立 Reviewer 仍须重新计算必要的指标或抽样复核。
