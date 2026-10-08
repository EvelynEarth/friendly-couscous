# Competition Validation Gates — 论文型数据竞赛

此文档为现有主 Skill 的**补充验收建议**，不更改仓库旧版数学建模门槛。只有当届题面与官方模板决定何种文件需要正式提交。

## G0 题意与数据资产

- 所有问题都有 objective、输入、输出、官方指标或 `unknown`、真实预测时点、约束、依赖。
- 逐个附件检查格式、大小、样本粒度、主键、重复、空值、标签与可用时间；存储在 Git LFS 的对象未拉取时标记 `unavailable`，不可将指针当作真实 Excel 数据。
- 检查官方提供的 `result` 模板、ID 顺序、测试集开放时点；禁止预设 Kaggle 文件结构。

## G1 方法前核验

- 预先锁定 train/validation/test 或时间、组别、空间 split。与目标未来有关的特征、全量目标编码、全量插补/归一化一律视为泄漏风险。
- 建立最小基线、指标计算脚本和约束/单位核查；记录完整计算预算。
- 选择适当方法家族：表格、时序、视觉、时空、图网络、NLP、优化、仿真、统计；不因为往届出现过就优先使用。

## G2 实验可信度

- 至少保留 Baseline、候选模型、主模型三者的**同一评估协议**及一致的数据范围。
- 罕见事件同时报告 PR-AUC / macro-F1 / 少数类 Recall 或与题意匹配的成本指标，不能只报 Accuracy。
- 时间预测用滚动回测/时间外验证；图像按实体/拍摄场景隔离近重复样本；优化必须验证约束可行。
- 消融、参数敏感性、随机种子、误差子群和失败案例按科学问题挑选，而非机械堆砌。

## G3 论文证据与交付

- `claim → accepted artifact → figure/table → paragraph` 必须可追溯；没有运行的模型不得提供数值成绩。
- 每张数值图附 source-data 与 generating script，正文摘要数字统一。
- 结果文件只在有官方模板时按官方定义生成，保持 ID/行数/顺序/表头/编码/取值。
- 提交前对照当届页面检查篇幅、匿名性、AI 使用、附录、源代码与打包方式，不沿袭往届经验作为规则。

## 2025 赛题的可迁移防错示例（**不是 2026 默认赛制**）

- 2025 A：图像分类 + 破损检测与分割。仓库中的部分标注为五列 `class cx cy w h`，属于**bbox**，不能直接冒充像素 mask。仅有 bbox 时需明确额外分割监督/弱监督方案与评估限制。
- 2025 B：风险标注依赖历史最终赔付额，但预测未来索赔风险时该字段未必可用；标签构造可以使用历史真实赔付，推断特征不得偷看未来赔付。比较“金额回归+规则”与“直接分类”时复用同一 holdout。
- “严重超额”比例和“合理诉求”比例为往届题面背景或约束，不能硬编码为所有数据集的通用阈值。

## 本地辅助命令

`python skills/big-data-competition-skill/tools/bigdata_preflight.py assets --root <data-dir>`

`python skills/big-data-competition-skill/tools/bigdata_preflight.py yolo --root <dataset-dir> --split train --task detect --classes 3`

`python skills/big-data-competition-skill/tools/bigdata_preflight.py csv --template <official.csv> --candidate <result.csv> --id-column <id>`

三个模式均只读取文件并输出 JSON；不训练模型、不篡改原始附件。CSV 工具不替代 XLSX 结果文件和官方人工验收。
