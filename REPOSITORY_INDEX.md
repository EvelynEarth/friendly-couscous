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

## v2.3 真数据与论文证据

- [2025 A/B 已核实真实文件元数据](skills/big-data-competition-skill/competition/real_case_2025_profiles.json)
- [真实数据就绪检查及纸面数字哈希协议](skills/big-data-competition-skill/references/real-case-replay.md)
- [已接受实验的证据记录模板](skills/big-data-competition-skill/templates/accepted-evidence-record.md)

B 的 Git LFS 指针不是可读 Excel；当前尚无可信真实模型跑分。

## v2.4 求解科学质量与论文论证

- [通用模型、算法、结论正确性审核](skills/big-data-competition-skill/references/solution-validity.md)
- [实验扰动与稳定性边界](skills/big-data-competition-skill/references/stability-and-uncertainty.md)
- [论文结构、段落论证与审稿方式](skills/big-data-competition-skill/references/paper-argumentation.md)
- [动态论文大纲](skills/big-data-competition-skill/templates/paper_outline.md)
- [优秀论文写作结构复盘卡](skills/big-data-competition-skill/templates/award-paper-writing-review.md)

工具用于记录、发现阻断点和汇总真实结果；正确性最终仍须独立复核，不能以 CI 通过替代。

## v2.5 数值反证与原始指标链

- [通用真实结果数值必要条件与论文数字三方核验](skills/big-data-competition-skill/references/result-falsification.md)
- [数值不变式契约填写说明](skills/big-data-competition-skill/templates/result-invariant-contract.md)
- `python skills/big-data-competition-skill/tools/result_invariant_gate.py --help`
- `python skills/big-data-competition-skill/tools/paper_evidence_gate.py --help`（正式论文用 `--require-metric-source`）

以上检验均是数学正确性的**必要检查/证据完整性检查**，不能自动证明未知题型下所有结论成立。

## v2.6 独立参考计算与黄金案例

- [未知赛题参考复算、错误注入与变形性质](skills/big-data-competition-skill/references/independent-recomputation.md)
- [输入案例模板](skills/big-data-competition-skill/templates/independent-oracle-case.md)
- `python skills/big-data-competition-skill/tools/independent_oracle.py --help`

只在实际小规模模型/原始验证标签条件下使用，不假定已完成历史获奖论文全文阅读或真题精确复现。

## v2.7 时序、推断、仿真与连续凸优化的参考验算

- [扩展科学独立参考计算器与适用范围](skills/big-data-competition-skill/references/extended-oracles.md)
- [时序/配对/仿真/解析最优输入模板](skills/big-data-competition-skill/templates/extended-oracle-cases.md)
- `python skills/big-data-competition-skill/tools/extended_oracles.py --help`

四类验证均只检验输入数据下的部分数值性质，不能代替独立验证真实赛题数学定义、数据独立性与论文结论。

## v2.8 全项目科学证据链

- [项目级联动、阻断条件与官方子问完整性](skills/big-data-competition-skill/references/project-evidence-chain.md)
- `python skills/big-data-competition-skill/tools/project_evidence_chain.py --help`

该项目级审计连接正式论文数值、真实 SHA-256 文件、独立计算及稳定性锚点；不能替代独立科学 Reviewer 和论文逻辑审稿。

## v2.9 通用赛场收尾与未知题型纸面交付

- [通用比赛执行、独立科学核查与论文定稿操作](skills/big-data-competition-skill/references/competition-final-runbook.md)
- [不限定算法/题目数的研究包](skills/big-data-competition-skill/templates/competition-readiness-record.md)
- `python skills/big-data-competition-skill/tools/competition_readiness.py --help`

旧 `project_evidence_chain.py` 继续保留为**当前数学 oracle 能覆盖的特定数值任务**的严格检查，不能要求所有未知问题伪装为该输入。
