---
name: big-data-competition-skill
version: 2.0.0
summary: 面向未知赛题、最终以论文为核心成果的大数据挑战赛全流程 Skill。动态覆盖统计分析、机器学习、深度学习、时序、空间、图网络、优化、仿真与因果分析，并建立从数据证据到论文结论的可追溯闭环。
triggers: [大数据挑战赛, 大数据竞赛, 数据分析竞赛, 数据科学竞赛, 大数据赛题, 赛题分析, 数据审计, EDA, 特征工程, 机器学习, 深度学习, 时序预测, 分类, 回归, 聚类, 异常检测, 优化, 仿真, 图网络, 实验设计, 模型评价, 消融实验, 稳健性分析, 结果分析, 科研绘图, 竞赛论文, 论文写作, LaTeX, 终审]
---

# Big Data Competition Skill v2.0

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

问题理解正确 > 数据可信 > 验证可信 > 方法匹配 > 实验充分 > 结果可复现 > 图表清晰 > 论文表达 > 形式创新。

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
- 终审 → final-review.md
- 交付 → paper-delivery.md

不要一次性读取整个仓库。