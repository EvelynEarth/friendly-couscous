# Changelog

## Current release: 2.3.0

- 从真实 supreme-spoon GitHub 文件树确认历史 2025 A 3300/413 的图像及 bbox 标注，2025 B 三个 XLSX 通过连接返回 LFS 指针（附件1 指针报告 2 字节）。
- 新增 `real_case_audit.py`：训练 YOLO 标注校验、test 标签封存提醒、可选跨拆分图像 SHA-256 精确重复检查；B 的 LFS/OOXML 容器就绪检查。
- 新增 `paper_evidence_gate.py`：正式论文指标与实际实验产物、split 记录、哈希和数值一致性检查；不把哈希当成模型准确性证明。
- 配套回归测试、实证使用协议、记录模板，明确当前没有完成 2025 赛题模型实测。
- 不改变 Kaggle 禁用约束和历史 HSK 独立的代码/工作流。

## Previous release: 2.2.0

- 已核实 supreme-spoon 2024/2025 共 16 份优秀论文 PDF 的目录元数据；未读 PDF 不计入方法统计。
- 新增优秀论文带页码的证据校验工具，未核实结论、未审阅资料不能作为模型选择依据。
- 新增四类比赛任务的十组合成方案对抗测试，识别未来信息泄漏、时序切分、bbox 分割真值混淆、优化可行性、结果模板与数值证据问题。
- 补充可复现单元测试与按需执行协议；未声称真实赛题已经建模复现。
- 删除缺乏可核查样本依据的“40 篇论文统计”等过度确定表述。

## Previous release: 2.1.0

- 增加 MathorCup 竞赛画像和任务方法手册，并保持对未知赛题的通用路由。
- 修复大数据 v2.1 主入口与 plugin/README/Changelog 的版本漂移。
- 改造仓库 CI：只对当前论文型大数据 Skill 运行有效的契约、索引和 Python 回归测试。
- 保存原有 HSK 数学建模历史代码和测试，不再把数学建模 v7.13.0 当成根 Skill 的通过条件。
- 自动索引/哈希清单以根 SKILL.md 的 v2.1.0 为单一版本来源，仅统计当前大数据 Skill 活动文件。

## Previous release: 2.0.0

- 将仓库主 Skill 从数学建模工作流正式转换为论文型大数据挑战赛工作流。
- 根目录 SKILL.md 成为当前主入口，覆盖未知赛题、数据审计、EDA、任务分类、方法选择、Baseline、泄漏审查、验证、实验溯源、结果深化、科研图表、Evidence Map、竞赛论文、终审与 Paper Delivery。
- 明确取消 Kaggle leaderboard、Kaggle submission、平台 API 和固定在线榜单作为默认工作流。
- 论文成为正式成果核心，要求数据、实验、结果、图表和论文 claim 形成可追溯证据链。
- 保留历史数学建模框架和历史竞赛材料作为兼容参考，不进入当前大数据挑战赛默认调用链。
- 增加按需 references，使不同赛题可以根据真实 objective、structure 和验证需求选择方法，而不是预设固定模型路线。

## Previous release: 7.13.0

7.13.0 为历史数学建模框架版本。其 core、module、pack 和 legacy 资料继续保留，用于历史项目兼容与仓库迁移参考，不作为当前大数据挑战赛主 Skill 的默认入口。
