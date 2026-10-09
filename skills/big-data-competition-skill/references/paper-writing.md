# Paper Writing

## Core rule

论文解释研究证据，不是代码注释集合。

## Default chapter logic

摘要 → 问题与研究目标 → 数据与预处理 → 方法 → 各任务结果 → 实验验证 → 敏感性与稳健性 → 讨论与局限 → 结论 → 参考文献 → 附录。

## Paragraph logic

每段尽量围绕一个 claim，优先使用：

claim → evidence → interpretation → limitation or transition

## Precision

关键结果保留能够支持评分和科学解释的精度。数字必须来自 accepted result artifact。

## Citation

外部事实、方法来源和理论背景使用可追溯文献。引用不是用来替代实验结果。
## 以论证链决定写作顺序

重点学习优秀论文如何组织目标、动机、方法选择、验证、解释与边界，而不是照搬模型。参考 [适应未知赛题的论文结构与论证](paper-argumentation.md)。应以所需答案组织章节：独立问可以逐问闭合，共享模型则先讲共同部分，递进任务突出依赖与误差传递。不要强制固定三问。

最终安排 **scientific reviewer**（对题意、模型/代码、误差、稳定性挑错）和 **editorial reviewer**（核查篇章逻辑、图表作用、段落衔接）；前者失败时不能靠文字润色宣称完成。


## v2.11 语言级拒收标准与实际终稿

必须依据 [论文视觉与学术质量硬门](paper-visual-quality-gate.md) 审核每一段话的论点、实际证据、解释与局限，不得写成程序使用指南、罗列流水账或过度称赞模型。学术写作深度不能由模板字号替代：说明为何选此模型而不选更简单方法、符号/量纲/假设、参数来源、合法回测与反例。

用户使用 Windows 11 + TeX Live 时，默认交付可编辑 `main.tex`、图表/参考文献源、成功编译的当前 PDF 和编译日志；参考 [XeLaTeX 模板入口](../templates/bigdata-paper-xelatex.md)。对缺少的原始模板或官方格式要明确报告，不得假装已读取或编译。逐页 PDF 质量仍由独立 Editorial Reviewer 实际检查。
