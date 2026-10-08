# Changelog

## Current release: 2.1.0

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
