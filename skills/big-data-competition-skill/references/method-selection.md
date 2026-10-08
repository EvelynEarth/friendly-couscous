# Method Selection

选择顺序：任务目标 → 数据结构 → 约束 → Baseline → 候选方法 → 验证 → 复杂度升级。

数据结构包括 tabular、temporal、spatial、network、text、image 和 mixed。

方法族：
- Statistics：描述、推断、不确定性和假设检验
- Machine Learning：结构化预测、分类、回归、排序
- Deep Learning：规模大、表示复杂或多模态数据
- Time Series：时间顺序、滞后和滚动预测
- Spatial / Network：空间邻接、拓扑和图结构
- Optimization：决策、资源配置、路径和调度
- Simulation：随机过程和系统动态
- Causal Analysis：具有明确识别策略的因果问题

复杂模型只有在官方指标提升、捕获简单模型无法表达的结构、显著提升稳健性或提供任务必需能力时才有充分理由。
## 正确性在模型选型之前

候选方法先做适用性与假设审计：任务输出是否匹配、数学变量与单位是否自洽、标签/特征时点是否成立、优化约束是否完整、因果识别是否可能。运行一个已知答案的玩具例子或者独立复算，再谈提升指标。优先按 [科学正确性审核](solution-validity.md) 做 Q0–Q3，而不是先从某届获奖论文挑一个模型名称。高分不能修复题意不一致的答案。
