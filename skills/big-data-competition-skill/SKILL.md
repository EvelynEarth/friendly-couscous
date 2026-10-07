---
name: big-data-competition-skill
version: 2.0.0
summary: 面向未知赛题、最终以论文为核心成果的大数据挑战赛全流程 Skill。动态覆盖统计分析、机器学习、深度学习、时序、空间、图网络、优化、仿真与因果分析，并建立从数据证据到论文结论的可追溯闭环。
triggers: [大数据挑战赛, 大数据竞赛, 数据分析竞赛, 数据科学竞赛, 大数据赛题, 赛题分析, 数据审计, EDA, 特征工程, 机器学习, 深度学习, 时序预测, 分类, 回归, 聚类, 异常检测, 优化, 仿真, 图网络, 实验设计, 模型评价, 消融实验, 稳健性分析, 结果分析, 科研绘图, 竞赛论文, 论文写作, LaTeX, 终审]
---

# Big Data Competition Skill v2.0

## 定位与边界

这是一个论文型大数据挑战赛 Skill，不是 Kaggle Skill，也不是传统数学建模 Skill。

它服务于赛题尚未知晓、数据形态和方法路线可能完全变化、最终成果以竞赛论文及其可信实验结果为核心的比赛。不得预设比赛一定是预测题、机器学习题或优化题。

允许的方法族包括描述统计、统计推断、回归、假设检验、不确定性分析、传统机器学习、深度学习、时间序列、时空建模、空间统计、图算法、图神经网络、运筹优化、仿真、风险分析、因果分析和多方法融合。

本 Skill 不使用 Kaggle leaderboard、Kaggle submission、平台 API、固定在线提交文件格式或榜单追分作为工作流前提。

比赛当届规则只从用户提供的正式通知、题面、赛方文件或经核验的官方来源读取。

## 总原则

优先级：

题意与任务正确 > 数据可信 > 验证可信 > 方法匹配 > 实验充分 > 结果可复现 > 图表清晰 > 论文表达 > 形式创新。

复杂模型不能因为先进而自动优于简单模型。高分不能代替可信验证。漂亮图不能代替真实数据。代码成功运行不能代替方法正确。论文结论不能超过证据边界。

## 默认主链

题面与附件审计
→ Competition Contract
→ 子任务拆解
→ 数据资产盘点
→ 数据质量与泄漏审计
→ EDA 与研究问题发现
→ 目标、输出、评价指标冻结
→ 候选方法族比较
→ 可信 Baseline
→ 特征与变量构造
→ 主模型或主分析
→ 正确验证设计
→ 对照实验
→ 消融、敏感性、稳健性
→ 结果深化
→ 数据证据图表
→ Evidence Map
→ 竞赛论文
→ 论文与结果一致性终审
→ Paper Delivery Gate

发现上游事实变化后，必须回退到受影响阶段，不得只修改论文措辞掩盖模型或数据变化。

## Competition Contract

正式求解前建立比赛合同：

- 赛题目标
- 子任务清单
- 输入数据与说明文件
- 输出要求
- 官方评价指标
- 数据粒度和观察单位
- 时间范围及信息可得时点
- 任务之间的依赖关系
- 可用外部信息
- 明确限制
- 尚未确认的口径
- 最终论文要求与格式要求

题面没有给出的规则标记为 unknown，不得用历届经验冒充当前赛事规则。

## Task Taxonomy

每个子任务独立判断 objective 与 structure，不强迫所有任务使用相同方法。

objective 可为 description、inference、prediction、evaluation、optimization、simulation、causal。

structure 可为 static_tabular、temporal、spatial、network、scheduling、stochastic、text、image、multimodal、mixed。

能力约束可包括 requires_out_of_sample_validation、requires_leakage_check、requires_uncertainty_quantification、requires_feasibility_check、requires_convergence_diagnostic、requires_discretization_check、requires_calibration_check、requires_identifiability_check。

## 数据治理

所有数据先做非破坏性审计，但不是所有数据都需要清洗。

检查文件、表、字段、类型、单位、样本量、主键、实体重复、缺失、异常、类别长尾、时间覆盖、训练测试边界、标签定义、标签延迟、跨表连接、样本覆盖、分布变化和潜在信息泄漏。

数据处理只允许进入三类之一：

- not_needed
- question_local
- project_level

任何会改变正式输入的数据处理都必须形成数据问题 → 处理必要性 → 处理规则 → 验证证据的闭环。

不得为了提高分数而静默删除样本、修改标签、提前使用未来数据、对验证集单独调优或把全量数据统计量泄漏到训练阶段。

## 方法选择

方法选择遵循：

任务目标 → 数据结构 → 官方指标 → 约束 → Baseline → 候选方法 → 验证。

至少比较任务匹配度、数据需求、可解释性、计算成本、验证难度、稳健性和论文表达难度。

复杂度升级必须有证据。理由包括官方指标有实质提升、捕获重要结构、改善稳健性或不确定性、或属于完成任务的必要能力。

## Baseline

任何复杂方案之前建立可信 Baseline。

Baseline 可以是历史均值、简单规则、线性模型、简单树模型、官方基准或简单时序模型。

最终结果至少保留 Baseline、主要候选和最终方案的可比较记录。

## 验证与 Adversarial Review

验证必须模拟比赛预测或研究结论形成时真正可获得的信息。

随机任务使用合理交叉验证或独立测试集。时间任务使用时间切分、滚动验证或回测。分组任务使用 Group-aware split。空间任务避免邻近空间泄漏。排序任务使用与排序目标一致的指标。仿真任务进行重复实验、误差和收敛检查。因果任务先固定识别假设。

同时主动攻击 target leakage、temporal leakage、group leakage、join leakage、duplicate contamination、preprocessing leakage、test-set tuning。

异常高分时优先审查验证设计。

## 实验治理

每个关键实验保留：

experiment_id、question、hypothesis、data_version、feature_version、method、parameters、validation_scheme、random_seed、metrics、runtime、artifacts、decision、limitations。

模型改进必须可追溯到实验差异。主结果与结果深化分析分离，结果分析不能反向偷偷修改正式主求解逻辑。

## 消融、敏感性、稳健性

按研究问题选择最小必要验证，包括特征消融、模块消融、参数敏感性、时间窗口变化、空间区域变化、随机种子重复、Bootstrap、外部验证、极端场景、误差分解和子群体分析。

每项实验都必须对应明确问题，不得为了增加表格数量而堆实验。

## 结果与数字治理

所有正文关键数字必须有唯一事实来源。

raw 或 processed data
→ experiment script
→ accepted result artifact
→ analysis result
→ figure or table
→ paper claim

修改上游结果后，相关图、表、摘要、正文和结论必须重新检查。

不得捏造运行时间、准确率、误差、置信区间、显著性或最优参数。

## 图表证据

正式图必须来自真实数据或真实模型结果。

每张论文图建立 figure_id、source_data、generating_script、analysis_question、key_finding、paper_location。

图表优先回答数据分布、关系与相关、时间趋势、空间结构、网络结构、模型对比、消融、敏感性、误差诊断、预测与真实、特征解释或机制流程。

装饰性 AI 图片不能替代数据图。不得通过平滑或插值制造原始数据不存在的新峰谷。

## 论文证据链

论文不是代码翻译，而是研究证据的压缩表示。

题意
→ 研究问题
→ 数据
→ 方法
→ 验证
→ 结果
→ 解释
→ 结论

关键 claim 的证据优先级：

1. 直接实验或计算
2. 数学推导
3. 可靠外部文献
4. 明确标注的解释

严禁把相关性写成因果，把一次实验写成普遍稳定提升，把一个数据集写成普适规律，用论文措辞掩盖不确定性。

## 论文组织

结构必须根据赛题调整，但通常包括摘要、问题重述与研究目标、数据来源与数据质量、方法、各子任务结果、模型比较或实验验证、敏感性与稳健性、讨论与局限、结论、参考文献和附录。

每个主要子任务尽量形成：

任务目标
→ 数据与变量
→ 方法选择理由
→ 模型或算法
→ 参数与验证
→ 结果
→ 解释
→ 小结

## 论文写作治理

正文应解释为什么这样定义问题、为什么选择方法、变量代表什么、关键数学关系或算法逻辑如何得到、参数如何获得、如何验证、结果意味着什么以及哪些结论不应推出。

DataFrame 操作、路径、日志、异常栈和无关工程细节不直接进入正文。

数学公式、伪代码和流程图只有在承担定义、推导或恢复核心逻辑时才出现。

## 可复现性

正式项目至少绑定：

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

用户本地运行题目代码时，本 Skill 生成、静态检查、审查和解释代码，但不伪造本地执行结果。

## Final Review

提交论文前进行评委式终审：

- 是否回答全部子任务
- 数据处理是否有依据
- 验证方案是否真实
- 是否存在泄漏
- Baseline 是否合理
- 最终方法是否真正优于基准
- 关键结论是否有证据
- 图、表、正文和摘要是否一致
- 数值是否一致
- 引用是否可追溯
- 是否存在过度因果或普适化表述
- 代码、结果和论文是否对应当前版本
- 论文是否满足当届官方格式要求

## Paper Delivery Gate

本 Skill 的最终交付是论文型成果，而不是平台 leaderboard submission。

Paper Delivery Gate 至少检查 paper source、compiled PDF、accepted results、figures and tables、references 和 reproducibility evidence。

若比赛官方只要求 PDF，则只按官方规则交付 PDF。若官方要求源文件、代码、数据或说明，则以当届官方通知为准。

不得根据 Kaggle 或其他平台经验自动扩展提交文件。

## 输出合同

阶段性决策默认输出：

Problem、Inputs、Checks performed、Findings、Decision、Risks、Next actions、Artifacts。

复杂项目内部可以维护更完整状态，但对用户展示时优先提供与当前决策直接相关的信息。

## Routing Rule

审题与任务拆解 → problem-framing + task-taxonomy
数据审计与 EDA → data-audit
方法选择 → method-selection
验证与模型比较 → evaluation-and-leakage + experiment-provenance
结果解释 → result-analysis
图表 → figure-evidence
论文 → paper-evidence + paper-writing
终审 → final-review
论文交付 → paper-delivery

不要一次性读取整个仓库。
