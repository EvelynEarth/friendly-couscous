---
name: big-data-competition-skill
version: 2.1.0
summary: 论文型大数据挑战赛全流程 Skill。
---

# Big Data Competition Skill v2.1

这是主 Skill 的完整工作流已经迁移到仓库根目录 SKILL.md。

本文件作为按需模块入口，与根目录主 Skill 保持同一能力边界：

赛题审计 → 数据审计 → EDA → 任务分类 → 方法选择 → Baseline → Leakage-resistant Validation → 实验溯源 → 结果分析 → 科研图表 → Evidence Map → 竞赛论文 → 终审 → Paper Delivery。

本 Skill 不预设赛题类型，不默认 Kaggle，不默认数学建模，也不把历史比赛经验当作当前赛事规则。

## 竞赛画像（competition/）

具体赛事的赛制、赛道、提交物与格式画像，用于快速建立心智模型；**历史规律不代表当届规则**，当届要求以题面/官方通知为准。

- [MathorCup 大数据竞赛](competition/mathorcup.md)

## 方法手册（playbooks/）

可落地的任务级方法手册（任务识别、方法选择、精简可运行代码、验证要点）。手册是起步参考，不是默认答案；代码需按当届数据实际运行后再引用。

- [手册索引](playbooks/00-index.md)
- 01 数据清洗与特征工程
- 02 表格预测：回归/分类
- 03 模型融合 Stacking
- 04 不平衡数据
- 05 时间序列预测
- 06 计算机视觉
- 07 风险/伪标签标注
- 08 库存与优化
- 09 NLP 与推荐

## 参考与模板

参考模块见 references/，模板见 templates/（含[论文大纲](templates/paper_outline.md)与 [result 校验清单](templates/result_checklist.md)）。
