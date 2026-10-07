# Big Data Competition Skill Repository Index

## 主入口

1. SKILL.md：大数据挑战赛主 Skill；
2. agents/openai.yaml：主调用入口；
3. .codex-plugin/plugin.json：插件元数据；
4. skills/big-data-competition-skill/：按需加载的完整模块与参考文件。

## 默认工作流

题面审计 → Competition Contract → 数据审计 → EDA → 泄漏审计 → 任务分类 → 方法选择 → Baseline → 主模型/分析 → 验证 → 消融/稳健性 → 结果分析 → 科研图表 → Evidence Map → 竞赛论文 → 终审 → Paper Delivery。

## 主要参考模块

| 路线 | Reference |
|---|---|
| 审题 | skills/big-data-competition-skill/references/problem-framing.md |
| 任务分类 | skills/big-data-competition-skill/references/task-taxonomy.md |
| 数据审计 | skills/big-data-competition-skill/references/data-audit.md |
| 方法选择 | skills/big-data-competition-skill/references/method-selection.md |
| 验证与泄漏 | skills/big-data-competition-skill/references/evaluation-and-leakage.md |
| 实验溯源 | skills/big-data-competition-skill/references/experiment-provenance.md |
| 结果分析 | skills/big-data-competition-skill/references/result-analysis.md |
| 图表证据 | skills/big-data-competition-skill/references/figure-evidence.md |
| 论文证据 | skills/big-data-competition-skill/references/paper-evidence.md |
| 论文写作 | skills/big-data-competition-skill/references/paper-writing.md |
| 终审 | skills/big-data-competition-skill/references/final-review.md |
| 交付 | skills/big-data-competition-skill/references/paper-delivery.md |

## 边界

本 Skill 不假设 Kaggle，不假设公开 leaderboard，不假设固定赛题类型，不把历史比赛答案写成永久规则。

原有数学建模框架及历史竞赛材料保留在仓库中作为历史兼容材料，但不进入本 Skill 的默认调用链。

## 修改原则

活动 Skill 的修改仍遵循 SKILL_CHANGE_GOVERNANCE.md。