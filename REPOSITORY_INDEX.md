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

原有数学建模框架及历史竞赛材料保留在仓库中作为历史兼容材料，但不进入本 Skill 的默认调用链。GitHub CI 和活动索引只检查 paper-first 大数据 Skill；旧 HSK 测试不会被误报为大数据 Skill 失败。

## 修改原则

活动 Skill 的修改仍遵循 SKILL_CHANGE_GOVERNANCE.md。
## 开发与验证

当前正式验证：

- `python scripts/validate_bigdata_skill.py`
- `python -m unittest discover -s tests -p "test_bigdata_*.py"`
- `python scripts/generate_indexes.py --check`

索引生成：`python scripts/generate_indexes.py`。历史 HSK 全量测试不作为当前大数据入口的验收条件，但保留源码及测试供另行迁移。

## v2.2 历史证据与任务压力测试

- [赛题对抗测试协议](skills/big-data-competition-skill/references/historical-benchmark-protocol.md)
- [16 份已确认但未复盘 PDF 的元数据清单](skills/big-data-competition-skill/competition/award_papers_2024_2025.json)

只读元数据不等于研究论文已阅读；合成方法协议通过不等于模型实测完成。
