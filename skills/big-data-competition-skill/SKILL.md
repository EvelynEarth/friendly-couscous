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

## 增量实战扩展（v2.1 兼容，不改变根入口）

遇到大数据比赛需求，根 `SKILL.md` 继续负责 Competition Contract、阶段治理和论文证据链；本模块只提供细化执行说明与**可选**辅助工具，不引入外部框架硬依赖。

- 不知道选什么外部工具：读取 [外部 Skill 限定路由](references/external-skill-routing.md)，基于实际任务结构只加载一到两个候选。
- 数据规模大或存在多文件：先运行 `tools/bigdata_preflight.py assets`，再按需读取 [大规模数据](playbooks/10-large-data-strategies.md)。
- 存在轨迹、空间/时间序列或图关系：读取 [时空与图网络](playbooks/11-spatiotemporal-network.md)。
- 视觉检测/分割：先运行 `tools/bigdata_preflight.py yolo` 识别标注类型，再进入 [计算机视觉](playbooks/06-computer-vision.md)；不能把 bbox 标注视为真值分割 mask。
- 需要输出官方 CSV 预测文件：按当届模板，使用 `tools/bigdata_preflight.py csv` 审计 ID、字段和取值。XLSX 等其他格式另依官方模板验证。
- 实验可信度复审：按 [论文型比赛验收门](references/competition-validation-gates.md) 完成 G0–G3；工具自检不等于模型结果验收。
- 分析历年获奖论文：先按 [优秀论文复盘协议](references/award-paper-audit.md) 逐篇读取并记录页码，使用 [证据表](templates/award-paper-audit.md)，不以 PDF 文件存在推定论文已审阅。

所有新增模块保留原有调用接口与历史模板；不改变当届题面优先权，不假设 Kaggle 榜单，也不将外部 Skill 的云训练费用或 API 凭证设为必需。
