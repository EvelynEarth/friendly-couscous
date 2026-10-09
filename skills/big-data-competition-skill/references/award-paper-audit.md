# Award Paper Audit — 优秀论文证据化复盘

目的：把已有优秀论文转成**可迁移的研究方法经验**，而不是背诵模型名、复制图表或假设每年题型相同。

## 数据边界

来源优先：`EvelynEarth/supreme-spoon` 中 2024、2025 各 8 篇优秀论文 PDF 与相应赛题。**“已发现 PDF 文件”不等于“逐篇分析完成”**。论文内容未实际阅读、无法取得正文或只有封面时，记录 `unreviewed/unavailable`，不得宣称已统计方法频次、优秀率或优胜原因。

逐篇填写 `templates/award-paper-audit.md`；每一判断都记录 `paper_id`、PDF 文件/页码、摘录的极短关键词、分析人的推断及信心度。长段落和图片禁止搬运。不要用优秀论文中的结果当作本届实验结果。

## 必查八项

1. 题意与输出：每问的 prediction/inference/optimization 目的是什么？
2. 数据：样本、粒度、缺失、类别分布、实体/时间边界是否交代？
3. 方法：Baseline 是什么？为何使用复杂方法？是否解释参数？
4. 验证：训练/验证隔离、官方指标、外部数据、泄漏与可复现性如何？
5. 数学表达：决策变量、损失函数、约束和求解器是否自洽？
6. 证据：对照、消融、鲁棒性、误差与失败案例是否支持主张？
7. 图表与论文：哪些图有分析意义，哪些重复，数值是否可核？
8. 不足：哪些结论缺少证据、哪些做法不可直接迁移？

## 跨论文归纳规则

- 先创建 `paper_id × question × method_family × evidence_page` 的矩阵，再按赛题年份/赛道/任务聚合。
- 区分“作者报告的算法”和“复盘者推断的算法”，没有可定位 PDF 页码的不统计为证据。
- 频次统计必须声明样本基数和统计口径；不能把某词出现次数理解为算法实际使用次数。
- 只形成两类输出：(a) 通用可执行规则 → 本 Skill 现有 Playbook；(b) 届别特定经验 → `competition/mathorcup.md`。不能用案例覆盖当届官方规则。

## 输出与终审

建议文件：`analysis/award_paper_matrix.csv`（如已建立实际论文复盘项目）、`paper_review_notes.md`、`method_transfer_decisions.md`。优先保存分析与定位证据，不提交全文 PDF 的转载版。

## v2.2 数据与页码证据验收

使用 [2024–2025 论文元数据](../competition/award_papers_2024_2025.json) 和 [审核脚本](../tools/award_paper_audit.py)。16 个文件初始没有被逐篇检读，因此方法频率的当前有效样本分母为零。

`python skills/big-data-competition-skill/tools/award_paper_audit.py --summary`

必须先读取 PDF 正文并核验页码，才能把文章标为 reviewed，并为每条方法记录 PDF 页码、归属和核实情况；不能根据文件名或搜索片段推测获奖论文使用了某方法。

## v2.4 优先学习论文写作结构，而非算法频率

历年优秀论文的主要学习目标调整为**章节组织、问题拆解、研究叙事、模型动机、段落衔接、图表论证和结论边界**。每篇实际读完正文后填写 [写作结构复盘卡](../templates/award-paper-writing-review.md)，定位 PDF 页码，区分作者原文观点和我们对逻辑作用的独立分析。

不从文件清单推断“优秀论文常用的最优算法”“固定章节数”“固定三问框架”，且不因此保证历史获奖论文某项数学推断正确。现有方法统计模板仅作次要信息；模型选择仍应以当前赛题及独立验证为准。参阅 [论文论证架构](paper-argumentation.md)。

 
## v2.12 实际机器提取与样本视觉审核已可复查
以 [award-paper-empirical-layout.md](award-paper-empirical-layout.md) 为新增真实来源。16篇PDF全部页面机器布局统计、源SHA-256、48页视觉样本证据可由 supreme-spoon 的 award-paper-audit 查证。旧的 `review_status=unreviewed` 现在专指**全文学术审读尚未完成**，并不否定机器实际打开PDF。后续任何方法论、语言/图表优劣评价必须先补带页码的全文审读卡，不能从低级结构统计跳到科学结论。
