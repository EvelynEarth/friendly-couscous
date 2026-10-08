# Big Data Competition Skill v2.3.0

这是 friendly-couscous 的主 Skill，专门用于**未知赛题、最终提交论文的大数据挑战赛**。

它不是 Kaggle 工作流，也不是传统数学建模 Skill。

核心原则：

**先理解赛题和数据，再决定方法。先建立可信 Baseline，再追求复杂模型。先锁定验证，再做调参和实验。最终把数据、实验、结果、图表和论文结论连成证据链。**

## 核心流程

赛题审计 → Competition Contract → 数据审计 → EDA → Leakage Audit → Task Taxonomy → Method Selection → Baseline → Modeling / Analysis → Validation → Ablation / Robustness → Result Analysis → Scientific Figures → Evidence Map → Competition Paper → Final Review → Paper Delivery

## 覆盖范围

统计分析、机器学习、深度学习、时间序列、空间分析、图网络、NLP、视觉、音频、多模态、优化、仿真、因果分析以及混合方法。

## 论文优先

最终成果围绕竞赛论文组织。关键数字必须来自 accepted result artifact。每个重要 claim 应能追溯到实验、数学推导、文献或明确标注的解释。

## 不预设比赛

不假设今年赛题属于任何固定模型或固定数据类型，也不把历史比赛经验变成全局规则。

## 不使用 Kaggle 提交流程

不以 leaderboard、submission.csv、平台 API 或榜单追分作为默认工作流。官方提交物只按当届比赛的正式通知确定。

主入口：SKILL.md
详细模块：skills/big-data-competition-skill/

## 当前仓库权威入口

- 主 Skill：[SKILL.md](SKILL.md)（v2.3.0）。
- 实用手册：[skills/big-data-competition-skill/](skills/big-data-competition-skill/)。
- GitHub CI：验证当前大数据 Skill 的元数据、模块清单、文档链接、论文证据流程、独立工具单元测试和生成索引。
- 历史 HSK v7.13.0 的 core/modules/ 等文件仍保留在仓库中供旧项目参考，但**不是当前 Skill 的主执行入口或 CI 验收依据**。
- 修复记录见 [CHANGELOG.md](CHANGELOG.md)，维护规范见 [SKILL_CHANGE_GOVERNANCE.md](SKILL_CHANGE_GOVERNANCE.md)。

本 Skill 保留对各种可能赛题（表格、时序、视觉、时空、网络、文本、优化、仿真等）的按需选择能力；不会根据往届题目硬编码今年的赛题或算法。

## v2.2 新增可执行证据验证

- [16 篇优秀论文 PDF 文件清单](skills/big-data-competition-skill/competition/award_papers_2024_2025.json)：只是文件元数据，初始未复盘。
- [2024/2025 四类赛题的合成对抗评测](skills/big-data-competition-skill/references/historical-benchmark-protocol.md)：包含合理方案及泄漏、标注、约束、证据反例。
- `python skills/big-data-competition-skill/tools/award_paper_audit.py --summary`；`python skills/big-data-competition-skill/tools/competition_benchmark.py`。

## v2.3.0 真实赛题就绪检查与论文证据追踪

- [2025 A/B 已核实的真附件元数据](skills/big-data-competition-skill/competition/real_case_2025_profiles.json)：A 有 3300/413 张图像及 bbox 标注，B Excel 当前为 Git LFS 指针。
- [实证就绪、阻断条件与使用说明](skills/big-data-competition-skill/references/real-case-replay.md)
- [正式实验数值追踪模板](skills/big-data-competition-skill/templates/accepted-evidence-record.md)

本次不代表已经下载完整图像、执行模型训练或核实官方 Excel 模板的 sheet 及字段。
