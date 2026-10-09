# Big Data Competition Skill v2.11.0

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

- 主 Skill：[SKILL.md](SKILL.md)（v2.11.0）。
- 实用手册：[skills/big-data-competition-skill/](skills/big-data-competition-skill/)。
- GitHub CI：验证当前大数据 Skill 的元数据、模块清单、文档链接、论文证据流程、独立工具单元测试和生成索引。
- 历史 HSK v7.13.0 的 core/modules/ 等文件仍保留在仓库中供旧项目参考，但**不是当前 Skill 的主执行入口或 CI 验收依据**。
- 修复记录见 [CHANGELOG.md](CHANGELOG.md)，维护规范见 [SKILL_CHANGE_GOVERNANCE.md](SKILL_CHANGE_GOVERNANCE.md)。

本 Skill 保留对各种可能赛题（表格、时序、视觉、时空、网络、文本、优化、仿真等）的按需选择能力；不会根据往届题目硬编码今年的赛题或算法。

## v2.2 新增可执行证据验证

- [16 篇优秀论文 PDF 文件清单](skills/big-data-competition-skill/competition/award_papers_2024_2025.json)：只是文件元数据，初始未复盘。
- [2024/2025 四类赛题的合成对抗评测](skills/big-data-competition-skill/references/historical-benchmark-protocol.md)：包含合理方案及泄漏、标注、约束、证据反例。
- `python skills/big-data-competition-skill/tools/award_paper_audit.py --summary`；`python skills/big-data-competition-skill/tools/competition_benchmark.py`。

## v2.11.0 真实赛题就绪检查与论文证据追踪

- [2025 A/B 已核实的真附件元数据](skills/big-data-competition-skill/competition/real_case_2025_profiles.json)：A 有 3300/413 张图像及 bbox 标注，B Excel 当前为 Git LFS 指针。
- [实证就绪、阻断条件与使用说明](skills/big-data-competition-skill/references/real-case-replay.md)
- [正式实验数值追踪模板](skills/big-data-competition-skill/templates/accepted-evidence-record.md)

本次不代表已经下载完整图像、执行模型训练或核实官方 Excel 模板的 sheet 及字段。

## v2.11.0：先检验正确性，再打磨论文逻辑

**新增核心**：[通用解答正确性审核](skills/big-data-competition-skill/references/solution-validity.md) 及 [可靠性与稳定性分析](skills/big-data-competition-skill/references/stability-and-uncertainty.md)；基于真实重复实验而非模拟表演统计稳定性。[论文论证写作](skills/big-data-competition-skill/references/paper-argumentation.md) 与 [可变结构论文大纲](skills/big-data-competition-skill/templates/paper_outline.md) 不预设赛题数量和模型。

优秀论文仅作为**写作结构、章节衔接、图表论证、推理逻辑**的学习来源，模型正确性必须独立验证。已发现的 PDF 文件尚未逐篇完成正文阅读，不把目录当作已提炼的写作规律。

## v2.11.0：真实结果反证，而非只检查自报的审核记录

- [通用数值不变式](skills/big-data-competition-skill/references/result-falsification.md)：对实际 JSON 结果进行边界、概率/守恒、线性资源约束等必要条件审计，契约绑定文件 SHA-256。
- [结果反证契约模板](skills/big-data-competition-skill/templates/result-invariant-contract.md)。
- 论文指标进入正式定稿时，推荐 `paper_evidence_gate.py --require-metric-source`，读取真实指标 JSON 并与论文主张作三方校对。

不能把工具的绿色结果说成数学正确性/全局最优/真实性能的证明；仍需独立计算或审稿人验证。

## v2.11.0 独立数值参考求解器

- [独立复算、手算黄金样例、错误注入与变形测试协议](skills/big-data-competition-skill/references/independent-recomputation.md)
- [回归、分类和小规模整数优化数据格式](skills/big-data-competition-skill/templates/independent-oracle-case.md)
- `python skills/big-data-competition-skill/tools/independent_oracle.py --case check.json`

20 个人工可推导的样例和错误反例用于验证检查工具，**不是**完成真实比赛模型的训练或最优性证明。

## v2.11.0：扩展科学正确性核验，避免算法类型盲区

- [四类独立科学参考计算器及统计假设](skills/big-data-competition-skill/references/extended-oracles.md)
- [实际 JSON 输入示例、正确答案与失败案例](skills/big-data-competition-skill/templates/extended-oracle-cases.md)
- `python skills/big-data-competition-skill/tools/extended_oracles.py --case actual_review.json`

涵盖时序滚动起点、配对随机化检验、独立伯努利仿真区间和盒约束严格凸二次优化。28 个合成正反例验证工具行为，**不代表真实 MathorCup 赛题已完整复现**。

## v2.11.0：独立数值—稳定性—论文结论的跨模块联动

新增 [项目级科学证据链协议](skills/big-data-competition-skill/references/project-evidence-chain.md) 和 `tools/project_evidence_chain.py`，在所有官方子问题范围内交叉检查 SHA-256 验证的真实来源、独立参考指标、结果约束、稳定性锚点和论文指标文件；遗漏某一正式子问、任何关键检查失败均不能标记项目为通过。合成正反例检验工具的防错能力，**不是实际赛题的模型成绩或对优秀论文的全文解读**。

## v2.11.0：未知赛题通用工作流已统一

- [参赛执行与论文终稿操作手册](skills/big-data-competition-skill/references/competition-final-runbook.md)
- [通用研究包记录字段](skills/big-data-competition-skill/templates/competition-readiness-record.md)
- `python skills/big-data-competition-skill/tools/competition_readiness.py --help`：面向分类、预测、推断、优化、视觉、语言和混合研究的**通用审稿资料完备性检查**
- 现有 `project_evidence_chain.py` 继续作为**适用数学类型下**的更严格数值核对，不适用时必须设计题型专属独立验证，不能虚构结果。

这次收敛的是工程工作流，不是宣称真实赛题全部求解、论文 PDF 全部完成逐篇审读。测试只验证工具行为，科学正确性仍要审查真实数据和具体结论。

## v2.11.0 自动代理模式：赛题附件 → 进度识别 → 纠错回退 → 论文终审

- [自动赛题流程、状态恢复及失败回滚操作说明](skills/big-data-competition-skill/references/automatic-competition-workflow.md)
- [ChatGPT Project 项目级自动代理指令（复制一次）](skills/big-data-competition-skill/templates/automatic-project-instructions.md)
- 状态工具：`python skills/big-data-competition-skill/tools/competition_autopilot.py --help`

有执行权限的代理可连续推进、检查、保存状态、回退并重算；不存在运行环境时，工具只能提供可执行步骤和提示，不得凭上传文件声称后台自动运行。关键建模方案与最终论文交付需要用户确认，工具通过不等于科学正确性。


### v2.11 论文语言与 LaTeX 可编译交付

新增 [论文视觉、学术语言与 TeX Live 质量门](skills/big-data-competition-skill/references/paper-visual-quality-gate.md)，以及 [XeLaTeX 源码入口](skills/big-data-competition-skill/templates/bigdata-paper-xelatex.md)。真实科研图默认允许具有语义的彩色，不再人为统一灰度；每页编译渲染与科学/编辑复核缺一不可。16 篇优秀论文清单仍然只是待逐篇 PDF 正文核对的元数据。
