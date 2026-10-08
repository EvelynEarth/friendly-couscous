# External Skill Routing — 限定式复用

## 原则与接口

此清单用于**按赛题问题选择已有开源知识**，而不是安装一套外部 Agent 再替换本仓库。比赛规则、数据可用时间、评价指标和最终论文是唯一决策依据。外部 Skill 只作为方法参考；在使用之前核验源文件、许可证、工具链版本、运行环境与实际数据，严禁复制不兼容的命令或声称已运行。

1. 完成 `Competition Contract`：按子问题确定 `objective`、`structure`、可用数据、预测时点和指标。
2. 先运行最小可信 Baseline，再选择最多 **1 个主方法 + 1 个备选**；额外工具须有明确价值和算力预算。
3. 预览外部 `SKILL.md` 的前置条件。凡强绑定云平台、账号/API Key、特定框架的能力，作为**可选**适配而非默认依赖。
4. 各任务复用外部方法论时，必须产出“模型假设 → 数据协议 → 验证方式 → 计算成本 → 结果证据 → 论文位置”的本地记录。
5. 仅引用链接，不在本仓库供应第三方代码或完整 Skill；实际引入时记录 license / commit SHA / source / changes 并更新第三方声明。

## 指向性路由

| 任务触发 | 建议先参考 | 本地必须执行的门槛 |
|---|---|---|
| 表格分类/回归、数据探索、交叉验证 | [probabl-ai/skills](https://github.com/probabl-ai/skills)：`explore-ml-data`、`frame-ml-problem`、`evaluate-ml-pipeline`、`audit-ml-pipeline` | 不强装 `skore_skills`；保证预处理只在训练折拟合；记录切分与数据版本 |
| 传统统计、时序预测/异常 | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)：`statistical-analysis`、`aeon`、`timesfm-forecasting` | 严格时点分割，滞后变量禁止含未来，报告预测区间与简单基线 |
| 多目标、排程、资源配置 | 同上：`pymoo`、`simpy`、`networkx` | 记录目标/单位/约束，可行性复算，报告实际约束违反与求解状态 |
| 多 GB 表格数据 | 同上：`polars`、`dask` | 估算内存、审计类型与 join 粒度、保证确定性和数据版本 |
| 视觉分类/检测/分割 | [ultralytics/skills](https://github.com/ultralytics/skills)：`yolo-datasets`、`yolo-training`、`yolo-tuning` | 先核对 bbox vs mask 标注；防重复图像泄漏；明确 mAP/IoU 等指标 |
| 视觉迁移学习与预训练 | [huggingface/skills](https://github.com/huggingface/skills)：`huggingface-vision-trainer` | 云 GPU / 令牌 / 费用非默认；外部权重/数据合法性先核查 |
| 论文语言、图表、审稿 | K-Dense：`scientific-writing`、`scientific-visualization`、`peer-review` | 论文数字绑定已验收结果，图表有脚本，引用可核实，不得编造 |

## 明确不采用

- 不把 Kaggle leaderboard、提交 API、追榜流程作为默认比赛流程；仅根据当届官方赛题处理 `result`/预测文件。
- 不以复杂模型替代数据审计与验证，也不套用往年赛道的固定题型。
- 不将外部 Skill 文档宣称为已经在本地安装/测试。
- 不把实验记录中的“未执行/失败”升级为“passed/accepted”。

## 完成门槛

每项方法选择说明：赛题问题、数据可用时点、Baseline、替代候选、split 防泄漏说明、失败模式、算力/时间预算，以及对应论文评价段。若资料缺失，标为 `unknown`，不得推定。
