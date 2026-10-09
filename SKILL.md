---
name: big-data-competition-skill
version: 2.13.2
summary: 面向未知赛题、最终以论文为核心成果的大数据挑战赛全流程 Skill。动态覆盖统计分析、机器学习、深度学习、时序、空间、图网络、优化、仿真与因果分析，并建立从数据证据到论文结论的可追溯闭环。
triggers: [自动做题, 自动求解, 上传赛题, 继续比赛, 自动验收, 自主纠错, 大数据挑战赛, 大数据竞赛, 数据分析竞赛, 数据科学竞赛, 大数据赛题, 赛题分析, 数据审计, EDA, 特征工程, 机器学习, 深度学习, 时序预测, 分类, 回归, 聚类, 异常检测, 优化, 仿真, 图网络, 实验设计, 模型评价, 消融实验, 稳健性分析, 结果分析, 科研绘图, 竞赛论文, 论文写作, LaTeX, 终审]
---

# Big Data Competition Skill v2.13.2

## 1. 定位

这是仓库的主 Skill。它专门服务于未知赛题、方法未知、最终需要提交论文的大数据挑战赛。

它不是 Kaggle Skill，也不是传统数学建模 Skill。不得默认比赛存在公开排行榜，不得默认生成 Kaggle submission，不得把某一年度题型、数据类型、模型或评价指标写成固定规则。

可动态覆盖：

- 统计分析与统计推断
- 回归、分类、排序、推荐
- 聚类、异常检测
- 时间序列与时空分析
- 传统机器学习、集成学习、深度学习
- NLP、视觉、音频、多模态
- 空间分析、图网络
- 运筹优化、调度、路径和资源配置
- 仿真、蒙特卡洛和风险分析
- 因果分析
- 多方法融合

最终成果以论文、可信实验结果、科研图表和可复现证据为核心。

## 2. 核心优先级

题意与结论正确 > 方法、算法和计算正确 > 可靠性、稳定性 > 数据与验证可信 > 方法匹配 > 可复现 > 论文逻辑与表达 > 形式创新。

禁止以模型更复杂、分数更高、图更漂亮或代码成功运行替代方法正确性和证据质量。

## 3. 标准工作流

题面与附件审计
→ Competition Contract
→ 子任务拆解
→ 数据资产盘点
→ 数据质量与泄漏审计
→ EDA
→ 研究问题与评价指标
→ 候选方法族比较
→ Baseline
→ 特征与变量构造
→ 主模型或主分析
→ 验证设计
→ 对照实验
→ 消融、敏感性、稳健性
→ 结果深化
→ 科研图表
→ Evidence Map
→ 竞赛论文
→ 评委式终审
→ Paper Delivery

发现上游事实变化时必须回退受影响阶段，不能只修改正文措辞掩盖变化。

## 4. Competition Contract

正式研究前冻结：

- 赛题目标和所有子任务
- 数据文件、数据说明和字段含义
- 输入输出关系
- 官方评价指标
- 样本和实体粒度
- 时间范围与信息可得时点
- 空间、网络或分组结构
- 子任务间依赖
- 外部数据规则
- 计算资源约束
- 论文格式要求
- 未确认口径

题面没有给出的事项标记为 unknown。禁止使用历史比赛经验伪造本届规则。

## 5. Task Taxonomy

每个子任务独立判断 objective 与 structure。

objective：
description / inference / prediction / evaluation / optimization / simulation / causal

structure：
static_tabular / temporal / spatial / network / scheduling / stochastic / text / image / audio / multimodal / mixed

能力标记可包括：
requires_out_of_sample_validation / requires_leakage_check / requires_uncertainty_quantification / requires_feasibility_check / requires_convergence_diagnostic / requires_discretization_check / requires_calibration_check / requires_identifiability_check

分类只用于选择工作流，不限制方法。

## 6. 数据治理

所有数据先进行非破坏性审计。

至少检查文件、表、字段、类型、单位、规模、主键、实体重复、缺失、异常、极端值、类别长尾、时间覆盖、训练验证测试边界、标签定义、标签延迟、跨表连接、分布变化和潜在信息泄漏。

数据处理只允许进入：

- not_needed
- question_local
- project_level

任何改变正式输入的数据处理必须形成：

数据问题
→ 处理必要性
→ 处理规则
→ 验证证据

不得为了提高结果而静默删除样本、修改标签、使用未来信息、对验证集单独调优或把全量数据统计量泄漏到训练阶段。

## 7. 方法选择

选择顺序：

任务目标 → 数据结构 → 官方指标 → 约束 → Baseline → 候选方法 → 验证。

候选方案比较：

- 任务匹配度
- 数据需求
- 可解释性
- 计算成本
- 验证难度
- 稳健性
- 论文表达难度

复杂模型只有在以下至少一项成立时才有充分理由：

- 官方指标有实质提升
- 捕获简单方法无法表达的重要结构
- 显著改善稳健性或不确定性
- 是完成任务的必要能力
- 提供可验证、可解释的新信息

## 8. Baseline

复杂方案之前必须建立可信 Baseline。

Baseline 可以是历史均值、简单规则、线性模型、简单树模型、简单时序模型或官方基准。

最终必须能比较 Baseline、主要候选和最终方案，不能只展示最终最优结果。

## 9. 验证与 Leakage Adversary

验证必须模拟真实信息可得性。

时间任务保持时间顺序，分组任务防止实体重叠，空间任务防止空间泄漏，排序任务采用匹配排序目标的指标，不平衡任务采用合适的分层指标，仿真任务进行重复实验和收敛诊断。

主动检查：

- target leakage
- temporal leakage
- group leakage
- join leakage
- duplicate / near-duplicate contamination
- preprocessing leakage
- test-set tuning
- 外部数据时间泄漏

异常高分时先检查验证设计，再讨论模型提升。

## 10. 实验治理

每个关键实验至少记录：

experiment_id
question
hypothesis
data_version
feature_version
method
parameters
validation_scheme
random_seed
metrics
runtime
artifacts
decision
limitations

模型选择必须能回答为什么选它。必须保存失败实验的原因，不能只保存最优结果。

主结果和结果深化分析分离。结果分析不得暗改主求解逻辑。

## 11. 消融与稳健性

根据研究问题选择：

- 特征或模块消融
- 参数敏感性
- 时间窗口变化
- 空间区域变化
- 随机种子重复
- Bootstrap / 置信区间
- 外部或留出验证
- 极端场景
- 误差分解
- 子群体分析
- 失败案例分析

每项实验必须回答一个明确问题。

## 12. 结果与数字治理

正文关键数字必须有唯一事实来源：

data
→ experiment
→ accepted result
→ analysis
→ figure or table
→ paper claim

禁止捏造运行时间、准确率、误差、置信区间、显著性、最优参数或实验结果。

上游数据、参数或模型变化后，相关图、表、摘要、正文和结论必须重新检查。

## 13. 科研图表

正式图必须来自真实数据或真实模型结果。

每张图建立：

figure_id
→ source_data
→ generating_script
→ analysis_question
→ finding
→ paper_location

图表优先服务研究问题，例如分布、关系、时间趋势、空间结构、模型对比、消融、敏感性、误差诊断、预测与真实值、特征解释或机制流程。

不得使用装饰性 AI 图片替代数据图，不得通过插值或平滑制造不存在的新峰谷。

## 14. 论文证据链

论文不是代码翻译。

核心闭环：

题意
→ 研究问题
→ 数据
→ 方法
→ 验证
→ 结果
→ 解释
→ 结论

主要 claim 的证据优先级：

1. 直接实验或计算
2. 数学推导
3. 可靠外部文献
4. 明确标注的解释

严禁把相关性写成因果，把一次实验写成普遍稳定提升，把一个数据集写成普适规律。

## 15. 论文结构

结构根据赛题调整，通常包括：

摘要
问题重述与研究目标
数据来源与数据质量
方法与模型
各子任务结果
模型比较与实验验证
敏感性与稳健性
讨论与局限
结论
参考文献
附录

每个主要任务尽量闭合：

任务目标
→ 数据与变量
→ 方法选择理由
→ 模型或算法
→ 参数与验证
→ 结果
→ 解释
→ 小结

## 16. 论文写作治理

正文解释为什么这样定义问题、为什么选这种方法、变量代表什么、核心公式或算法怎样得到、参数怎样获得、如何验证、结果说明什么以及哪些结论不能推出。

DataFrame 操作、文件路径、日志、异常栈和无关工程细节不直接进入正文。

数学公式、伪代码和流程图只有在承担定义、推导或恢复核心逻辑时才使用。

## 17. Evidence Map

每个重要结论建立：

claim_id
claim_text
evidence_type
source_artifact
source_location
figure_or_table
validation_status
paper_location
limitations

论文、图表和结果发生变化时同步更新 Evidence Map。

## 18. 可复现交付

至少绑定：

题目版本
→ 数据版本
→ 数据处理版本
→ 代码版本
→ 参数
→ 随机种子
→ 验证方案
→ 结果
→ 图表
→ 论文

用户本地执行题目代码时，Skill 只负责生成、静态检查、审查和解释代码，不能伪造本地执行结果。

## 19. Final Review

提交论文前进行评委式终审：

- 是否完整回答所有子任务
- 数据处理是否有依据
- 验证是否可信
- 是否存在泄漏
- Baseline 是否合理
- 最终方案是否真正优于合理基准
- 关键 claim 是否有证据
- 图、表、正文、摘要数字是否一致
- 引用是否可追溯
- 是否存在过度因果或普适化表述
- 当前代码、结果和论文是否一致
- 是否符合当届官方论文格式和提交要求

## 20. Paper Delivery Gate

最终交付是论文型成果，而不是 Kaggle leaderboard submission。

若官方要求 PDF，则交付当前正式 PDF。

若官方要求源码、数据、结果或说明，则只按当届官方通知提供对应材料。

不得根据 Kaggle 或其他平台经验自动增加提交文件。

正式交付前至少检查：

paper source
compiled PDF
accepted results
figures and tables
references
reproducibility evidence
official rule evidence

## 21. Routing

按需加载：

- 审题 → skills/big-data-competition-skill/references/problem-framing.md
- 任务分类 → task-taxonomy.md
- 数据审计 → data-audit.md
- 方法选择 → method-selection.md
- 验证 → evaluation-and-leakage.md
- 实验 → experiment-provenance.md
- 结果 → result-analysis.md
- 图表 → figure-evidence.md
- 论文证据 → paper-evidence.md
- 论文表达 → paper-writing.md
- 论文语言、彩色科研绘图与 LaTeX 终稿 → paper-visual-quality-gate.md
- 终审 → final-review.md
- 交付 → paper-delivery.md

不要一次性读取整个仓库。

## 22. 竞赛画像与方法手册

- 具体赛事画像（赛制/赛道/提交物/格式）：skills/big-data-competition-skill/competition/，当前含 MathorCup（mathorcup.md）。
- 可落地任务方法手册：skills/big-data-competition-skill/playbooks/，从 00-index.md 进入，覆盖清洗特征、表格预测、融合、不平衡、时序、视觉、伪标签、优化、NLP 与推荐。

画像与手册仅为起步参考：历史规律不覆盖当届题面，代码需按当届数据实际运行后再引用。

## 23. 历史赛题对抗评测与论文证据门（v2.2）

在实际求解前参阅 [赛题对抗评测与论文复盘协议](skills/big-data-competition-skill/references/historical-benchmark-protocol.md)，核查验证切分、预测时点、可用特征、标注真值、优化可行性和论文数值证据。合成对抗测试不是比赛成绩。

[2024–2025 获奖 PDF 文件清单](skills/big-data-competition-skill/competition/award_papers_2024_2025.json) 含 16 篇已发现的文件，但初始均为未审阅，不得据此宣称获奖论文的方法频率。只有实际读取、核对 PDF 页码并完成审查后才计入归纳。

## 24. 真实赛题附件就绪与论文数值哈希验证（v2.3）

遇到实际赛题数据，按需加载 [MathorCup 2025 A/B 真附件就绪检查](skills/big-data-competition-skill/references/real-case-replay.md)，先判断数据是否真正可读取、哪些标签/特征在预测时不可用；不要把公开 test labels 当作训练/调参数据。对于 Git LFS 指针，未获取实际文件字节前报告阻断。

论文成稿前，对已执行且复核过的关键实验使用 [实验证据记录模板](skills/big-data-competition-skill/templates/accepted-evidence-record.md) 和 `tools/paper_evidence_gate.py` 检查数值、split、产物哈希与正文主张一致。哈希一致不等于模型指标科学正确，CI 通过也不等于赛题模型运行成功。

## 25. v2.4 核心升级：独立科学复核与论文论证质量（通用，不限定赛题）

**先核对题目到底问了什么，再核对模型为何成立，最后核对结论在何种条件下成立。** 在每个子问题进入写作之前，按 [通用求解正确性与可靠性协议](skills/big-data-competition-skill/references/solution-validity.md) 完成 Q0–Q5：
题意匹配 → 模型假设/公式/量纲 → 算法/约束及独立复算 → 任务适配验证 → 稳定性/反例 → 结论边界。至少安排一次独立 Reviewer 的反例与复核。错误、未验证或失败不能靠论文润色替代。

按需使用 `solution_quality_gate.py` 记录**审核覆盖情况**，以及 `stability_audit.py` 统计真实扰动运行的样本内波动。二者不能在没有实际证据时宣称数学正确、模型可靠或普遍稳定。

优秀论文优先学习 [研究叙事结构与论证逻辑](skills/big-data-competition-skill/references/paper-argumentation.md)：目标→困难→方法依据→独立验证→证据→解释与局限。严格区分实际阅读 PDF 和只核实文件名；不再使用“获奖论文的算法频次”替代论证本届模型为何正确。论文结构按真实问题数量与相互依赖变化，不能套用固定三问大纲。

## 26. v2.5 真实输出反证与论文数字回读

模型代码运行成功、核对表打勾以及论文记录与正文数字一致，**都不能单独保证求解正确**。对每个真实子问题，先依据原题及数学假设确定**可以证伪答案的必要条件**：概率归一化、取值界、资源容量、守恒、目标约束、独立计算值或其他必要性质。需要时使用 [数值不变式与结果反证协议](skills/big-data-competition-skill/references/result-falsification.md) 和 `tools/result_invariant_gate.py` 对*实际结果文件*验算，保留阻断信息。不变式满足仅是必要而非充分条件，还需真实数据、独立复算和任务匹配的统计验证。

论文数字在定稿前使用 `paper_evidence_gate.py --require-metric-source` 严格模式：绑定并回读 SHA-256 验证的实际 `metrics.json`，核查实际指标文件、实验记录、论文 claim 三方一致，防止两份手工记录一起写错。无需引入任何赛题专用算法或 Kaggle 提交流程。

## 27. v2.6 独立复算与黄金答案反例

未知赛题的关键模型/结论在 [独立参考求解与验证协议](skills/big-data-competition-skill/references/independent-recomputation.md) 下，尽可能用不共享主程序核心实现的参考计算核对：从真实合法标签重算分类/回归指标，并对小规模整数线性子实例通过穷举精确验证可行性及最优性。使用 [案例格式](skills/big-data-competition-skill/templates/independent-oracle-case.md) 与 `tools/independent_oracle.py --case record.json`。已知答案、错误注入和变形关系测试不等于完成真实历史赛题模型。

评审顺序：核对题意与数学建模 → 锁定独立合法验证数据 → 参考实现交叉计算/小规模精确复核 → 边界和反例 → 可靠性、稳定性及证据链 → 论文写作。小实例的精确性不意味着大规模求解全局最优，数字一致也不等于结论科学正确。

## 28. v2.7 四类扩展独立科学验算

在未知赛题经真实任务分类之后按需加载 [时序、配对推断、随机仿真、连续凸优化的独立验算协议](skills/big-data-competition-skill/references/extended-oracles.md)，并选择符合题目实际数学条件的参考算法。配套 `tools/extended_oracles.py --case actual_review.json` 可以从时序折内原子预测重算滚动指标，精确枚举少量配对符号翻转得到双侧 p 值，计算 iid 伯努利模拟的 Wilson 精度区间，以及用逐维解析解核查盒约束可分严格凸二次问题的最优性。参见 [实际输入规范](skills/big-data-competition-skill/templates/extended-oracle-cases.md)。

**科研边界必须严格执行**：自报的 time split 并不能证明特征处理没有未来泄漏；配对 sign-flip 必须满足零假设下符号可交换等条件；Wilson 区间不适用于相关或加权样本；可分离凸目标的闭式最优不证明一般连续非凸或混合整数模型正确。即使参考验算通过，仍要实际证据、独立审稿、误差与稳定性分析，以及符合题意的论文论证。

## 29. v2.8 跨模块项目级科学证据闭环

此前每个工具单独“通过”**不能**说明整篇竞赛论文数值链可靠。项目复审时按 [跨模块项目证据链与失败关闭协议](skills/big-data-competition-skill/references/project-evidence-chain.md) 把所有**当届官方子问**、原始证据 SHA-256 清单、质量复核、独立参考计算、数值不变式、稳定性及真实论文指标回读联系起来。可执行 `tools/project_evidence_chain.py --manifest project.json --artifact-root real_outputs/`，任何关键失败直接阻断项目级机器验收。

**新增的实际联系**：每个正式论文指标必须映射到独立数值参考结果；不变式文件必须绑定参考算法核对的原子结果；稳定性实验须用锚点运行指向正式结果数值。跨模块成功的状态仅是 `machine_evidence_consistent`，科学/论文审稿仍要求由独立 Reviewer 真实检查。未知题型若现有 oracle 不适用，设计新题专属参考验算，不能编造“已通过”。

## 30. v2.9 最终统一赛场工作流：未知题型与论文研究包

**赛题未知不应被有限的数值 oracle 卡死。** 正式比赛先按照 [通用赛场执行与终稿验收](skills/big-data-competition-skill/references/competition-final-runbook.md) 完成：题意/数据契约 → 方法适配 → 已知答案/独立复核 → 可靠性与稳定性 → 真实证据 → 论文逻辑与限度 → 当届官方交付要求。

任何研究任务均可在 [通用论文研究包验收](skills/big-data-competition-skill/templates/competition-readiness-record.md) 中记录官方子问、方法/独立检查、结论支持与论文结构，运行 `tools/competition_readiness.py` 检查完整性。其 `documentation_consistent_pending_expert_review` 只表示**文档可审阅**，绝不自动等于论文可交付或模型正确。已有 `project_evidence_chain.py` 仅当选定的数学类型确实适用时作为**更严格的数字交叉验收**；不支持的题型必须另做独立科学核验，不能伪造 oracle 或放弃审核。

优秀论文重点是阅读正文后理解**问题组织、论证过渡、图表证据作用和结论边界**，而非照搬获奖模型。未经逐篇阅读的 PDF 不得称为已验证写作规律。当前 v2.9 为可使用的工程版，今后改动应由真实任务实测发现的问题驱动，而不是连续机械升级版本号。

## 31. v2.10 自动比赛代理与跨会话进度恢复

**默认优先启用有状态的自动代理工作流**。用户提交正式赛题、数据与规则，且代理具有可读写、可运行的项目目录时，读取 [自动比赛代理运行协议](skills/big-data-competition-skill/references/automatic-competition-workflow.md)，优先恢复 `autopilot-state.json`；若无状态则仅在可确认真实输入目录后初始化。自动识别阶段、按需加载 reference/playbook、执行真实分析/计算、保存可验证成果、分阶段审核，不合格时定位上游缺陷并回退修改，默认单阶段最多三轮，超限交由用户判断。推荐将 [自动项目指令](skills/big-data-competition-skill/templates/automatic-project-instructions.md) 放入 ChatGPT Project 项目说明。

状态控制器：`python skills/big-data-competition-skill/tools/competition_autopilot.py --help`（子命令 `init/run/status/sync-inputs/template/approve`）。**流程状态与文件哈希一致不等于模型科学正确**：还要使用本 Skill 的独立验算、论文数字三方回读及科学/编辑终审。关键模型路线和正式论文交付必须征得用户明确批准；不得自动用现有 GitHub 权限当成赛事平台提交权限。

GitHub 中的 SKILL.md **不会自动成为 ChatGPT 系统提示词**；仅上传附件也不意味着本地服务已启动。只有在当前会话或 Project 指令实际加载本规则、且具备文件和代码执行能力时才能持续推进。没有这些能力时要说明阻断，不能声称做完、在后台运转或跨聊天持久化。该运行协议不启动定时自动任务。

## 32. v2.11 论文语言、色彩图表与 Windows XeLaTeX 科研终稿硬门

在进入 `figures`、`paper`、`final` 及 `delivery` 阶段前，按 [论文视觉与学术质量硬门](skills/big-data-competition-skill/references/paper-visual-quality-gate.md) 对图表设计、论证语言、逐页排版和当前编译证据进行实查。

**默认提供可编辑且可编译的 LaTeX 源文件**（尤其当用户已说明 Windows 11 + TeX Live），与真实实验图表及当前 PDF 一并交付。使用 [XeLaTeX 通用论文模板](skills/big-data-competition-skill/templates/bigdata-paper-xelatex.md)，按当届官方规则调整，不照搬传统数模竞赛首页/页码/匿名与固定三问。用户提供既有 TeX 模板时，应先审核代码与许可，再针对比赛调整；缺失时须说明，不可声称已经迁移。

颜色不是缺陷：科研图默认采用有意义且色盲友好的**有限彩色语义**，并保留灰度可辨识性，避免黑白一刀切。每张图同时通过事实追溯、图型与轴、叙事价值、图中文字及 PDF 中真实显示的检查，且无法由漂亮外观取代准确性。

本届优秀论文尚有未实际打开正文的 PDF：不能仅从 16 个文件名/大小宣称完成逐篇学习。实际可读后按论文页码记录结构、图表功能与可迁移原理；无法阅读时如实标记缺口。机器完成的文件/哈希检查绝不自动等于审稿通过。



### v2.11.1 LaTeX 版式质量纠错

论文写作不止要求一个可编译的 PDF，还必须复查**标题级差、标题后首段缩进、全部自然段段落缩进、目录仅一份、图题不重复编号、图例与坐标轴不冲突**。参考 [排版与图形实际纠错协议](skills/big-data-competition-skill/references/paper-visual-quality-gate.md) 和 XeLaTeX 模板。

本版新增 `tools/latex_paper_audit.py`：检测手工图/表号重复、重复目录、缺少实图、声明格式下正文缩进与编译日志错误。输出仅为 `preflight_passed_manual_review_required`，仍须逐页渲染审核与人工审定，不能把 CLI 结果写为论文优秀。官方未规定具体标题字号时，实际设计参数仅为可改的视觉风格，不能误称官方强制规范。**从具体源文件修错后重新编译**，不得只修改审核状态。

 
## 33. v2.12 基于真实优秀 PDF 的论文风格证据，而非主观套模板

2024/2025 MathorCup 大数据**16篇原始获奖 PDF 已由 GitHub Actions 打开并机器解析全部716页**；其中704页达到至少80个字符的文字提取门槛。对每篇第1、2页及一页中段做了**48页抽样视觉检查**，有带PDF页码的真实记录。全文科学论证尚未完成逐篇深入阅读，禁止把机器解析/抽样审阅说成“全部16篇学术阅读全文”。

具体证据及可迁移边界参阅 [优秀论文实证排版观察](skills/big-data-competition-skill/references/award-paper-empirical-layout.md)，原始机器记录可从仓库 `EvelynEarth/supreme-spoon/award-paper-audit/reports/` 追溯。研究证据优先级：**当届官方格式和题意 > 当前论文的研究需要 > 可页码复查的获奖论文样本 > 通用美学建议**。

这些论文的 PDF 二级标题候选字号**并非完全统一**（例如2025-01 PDF第3页约12pt，2025-02第4页约14pt，2025-06第4页约15pt），不能给未知赛题强套相同字号/模型章节。2025-05第11页、2025-02第12页、2024-08第35页均实际呈现彩色研究图或机制图，因此不得再把“全部黑白”当作获奖风格。

**新增应用纪律：** 每次论文排版前检索“当届官方赛规”；选择两三种候选标题层次/段落缩进/图表配色时，形成“哪份PDF哪页提供的证据、为什么适用于本届”的对照卡；真实编译后对照 PDF 样本逐页看；发现重复图号、标题后首段缩进不对、图中文字拥挤或图表不支撑论点，先改源代码，不得只用审核勾选转绿。赛题的研究论证科学质量仍需全文阅读与独立复核。

 
## 34. v2.13 实读优秀论文正文：写作论证链与独立反证

已通过GitHub Actions实际取得 `EvelynEarth/supreme-spoon` 原始16篇MathorCup大数据获奖PDF并逐份核对SHA-256、页数。对716页生成可检索正文，**逐篇阅读所列核心摘要、方法、评价和局限的重点页面（55个原文页码关键词锚点）**，并渲染重要图表/公式页；详见 [16篇研究论证逐篇复盘](skills/big-data-competition-skill/references/award-paper-deep-argumentation-16.md)。**非716页逐字人工通读，未独立复现作者全部实验。**

论文适配原则：当届官方赛制优先，研究目标决定叙事组织；区别时空预测、预测驱动优化、视觉任务、弱标签风险建模的“模型必要性—数学/算法—实验—证据—反例”路径。禁止套固定题目数、指定模型族、纯黑白科研图或传统数模标题体系。

**从获奖论文反证出的新增科学红旗：** `2024-04` 原PDF物理第19页表7给出CNN-LSTM的RMSE=0.0336、MSE=0.0071；**仅当计算口径相同**，RMSE平方约0.00113，二者无法同时成立。必须核查同一指标来源/样本、单位与公式，不凭获奖或漂亮PDF自动通过。按需运行 `tools/paper_metric_identity_gate.py`（契约见 [指标恒等式模板](skills/big-data-competition-skill/templates/paper-metric-identity-contract.md)），仅是表内算术门，不代替原子数据独立复算。

论文/图表终审继续强制抓住：合法时序切分与派生图像分组、防止SMOTE/目标编码/Stacking折间泄漏、预测误差向约束传播、小类召回和零值百分比误差、伪标签非真值、推断不超过证据。任何实质失败均回退上游代码/模型/图表/TeX并重新评测，不允许只勾改Review JSON。


## v2.13.1 论文编号缺陷纠正（真实2023 B稿回归）

本版明确修复论文默认 XeLaTeX 样式中“用户要求中文大标题而 `\\section` 仍显示阿拉伯编号”的缺陷。通用模板默认中文三层层级（「一、」/「（一）」/「1．」）并把实际编号结果放入排版预检范围；**可由当届官方论文样式覆盖**，不能把中文三级体系冒称所有比赛的硬性规范。必须重新编译当前论文并检查目录、正文、交叉引用，而非只修改模板文档。参见 [PDF排版质量硬门](skills/big-data-competition-skill/references/paper-visual-quality-gate.md) 和 [TeX 模板](skills/big-data-competition-skill/templates/bigdata-paper-xelatex.md)。

 
## v2.13.2 论文五层编号纠正（用户当前指定格式）

前版「一、／（一）／1．」与当前用户指定层级不一致，现将**通用XeLaTeX模板默认**改为：「一、」一级、 「1.1」二级、 「1.1.1」三级、 「（1）」四级枚举、 「•」五级实心点。前三层由 `ctex` 的自动编号实现；四、五层是嵌套 `enumerate/itemize` 列表，而不是要求每篇论文一定有五层正式章节。用实际 PDF 验证目录和正文显示，不能只在配置文件填字段。新增可选 `latex_paper_audit.py --heading-style chinese-mixed-five`；旧的 `chinese-tiered` 兼容保留，仅在明确需要旧样式时启用。**此为当前用户版式，不是官方固定要求**；当届官方格式优先，其他比赛按需选择。
