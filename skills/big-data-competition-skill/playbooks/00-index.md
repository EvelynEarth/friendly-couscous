# 方法手册索引（Playbooks）

本目录是 `big-data-competition-skill` 的**可落地方法层**：每个手册给出任务识别、方法选择、精简可运行代码与验证要点。

## 使用规则（硬约束）

1. **手册是起步参考，不是默认答案。** 先做赛题审计与数据审计（见 `../../references/`），确认任务目标、数据结构和当届指标后，再选手册。
2. 手册不覆盖当届题面/官方通知；当届规则冲突时一律以当届为准。
3. 代码是骨架，需按当届数据调整；**未实际运行的代码不得描述为“已运行”**（见 `../../references/experiment-provenance.md`）。
4. 所有预处理/编码/特征选择必须在训练折内完成，避免泄漏（见 `../../references/evaluation-and-leakage.md`）。

## 手册清单

| 手册 | 适用任务 |
|---|---|
| [01 数据清洗与特征工程](01-data-cleaning-feature-engineering.md) | 一切表格任务的起点 |
| [02 表格预测：回归/分类](02-tabular-prediction.md) | 表格回归、分类、评分/价格预测 |
| [03 模型融合 Stacking](03-model-fusion-stacking.md) | 多模型集成、混合策略 |
| [04 不平衡数据](04-imbalanced-data.md) | 少数类识别、风险/欺诈检测 |
| [05 时间序列预测](05-time-series-forecasting.md) | 需求/货量/路径等时序预测 |
| [06 计算机视觉](06-computer-vision.md) | 图像分类/检测/分割 |
| [07 风险/伪标签标注](07-risk-pseudo-labeling.md) | 无标签下的规则/无监督标注 |
| [08 库存与优化](08-inventory-and-optimization.md) | (s,S) 补货、资源分配、多目标 |
| [09 NLP 与推荐](09-nlp-and-recommendation.md) | 文本挖掘、推荐序列评估 |
| [10 大规模数据工程](10-large-data-strategies.md) | 超大表格、分块计算、内存与时间预算 |
| [11 时空与图网络](11-spatiotemporal-network.md) | 轨迹、地理空间、动态图与网络关系 |

## 选型快表（按任务目标）

- 预测连续值（价格/金额/货量）：01 → 02（回归）→ 按需 03；是时序则用 05。
- 预测类别/评分：01 → 02（分类）；类不平衡加 04；无标签先用 07 造标签。
- 图像：06；图像中含决策/评估可回接 02/04。
- 资源配置/路径/调度：08。
- 文本/推荐序列：09；推荐排序可回接 08。
- 内存紧张、多文件：10 作为前置数据工程手册；时空轨迹/图任务：11。
- 外部工具可选参考：../references/external-skill-routing.md；验收：../references/competition-validation-gates.md。

## 证据边界

手册是可选方法骨架，不构成历年获奖算法排行榜。现有 2024/2025 共 16 份 PDF 的文件名和大小已核对，但尚未完成逐篇 PDF 方法审阅；此前“40 篇统计”不能作为本轮已核实的研究结论。详见 [可执行证据与任务对抗协议](../references/historical-benchmark-protocol.md)。

## 可执行预检（只读）

- 附件清单与 Git LFS 指针：`python skills/big-data-competition-skill/tools/bigdata_preflight.py assets --root DATA`
- YOLO 检测/分割标注核验：`python skills/big-data-competition-skill/tools/bigdata_preflight.py yolo --root DATASET --split train --task detect`
- CSV 官方模板兼容：`python skills/big-data-competition-skill/tools/bigdata_preflight.py csv --template TEMPLATE --candidate RESULT --id-column ID`

工具通过只意味着相应文件格式契约通过；不是模型精度、数据合法性或论文质量通过。未实际阅读的优秀论文不纳入“方法出现频次”的有效样本。
