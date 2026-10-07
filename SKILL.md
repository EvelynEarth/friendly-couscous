---
name: big-data-competition-skill
version: 1.0.0
summary: 面向未知赛题的大数据挑战赛全流程 Skill，覆盖数据审计、统计分析、机器学习、深度学习、时序、空间网络、优化、仿真、实验验证、图表与竞赛论文。
triggers: [大数据挑战赛, 大数据竞赛, 数据分析竞赛, 数据科学竞赛, 赛题分析, 数据分析, 特征工程, 机器学习, 深度学习, 时序预测, 分类, 回归, 聚类, 异常检测, 优化, 仿真, 图网络, 模型评价, 消融实验, 论文, 竞赛论文, 结果分析, 可视化, LaTeX]
---

# 大数据挑战赛 Skill

本根入口现在只负责大数据挑战赛，不再作为数学建模 Skill 使用。

完整工作流位于 `skills/big-data-competition-skill/SKILL.md`。

按需读取：
- `references/method-selection.md`
- `references/evaluation-and-leakage.md`
- `references/paper-evidence.md`

核心工作流：

赛题审计 → Problem Contract → 数据审计 → EDA → 泄漏检查 → 任务与评价指标 → 方法族比较 → Baseline → 特征与模型 → 验证 → 消融/敏感性/稳健性 → 结果分析 → 图表证据 → 竞赛论文 → 终审 → 可复现交付。

本 Skill 不预设今年赛题的类型，也不把机器学习作为唯一方法。必须根据实际数据和任务选择统计学、机器学习、深度学习、时序、空间、网络、优化、仿真或因果方法。

论文是正式交付的一部分。模型、实验、结果、图表和论文结论必须形成可追溯证据链。

如果用户本地执行赛题代码，Skill 负责生成、静态检查、审查和解释代码，但不伪造本地运行结果。
