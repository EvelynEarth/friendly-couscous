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
