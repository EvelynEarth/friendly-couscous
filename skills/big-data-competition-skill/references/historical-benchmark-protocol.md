# 历年赛题对抗评测与获奖论文证据门

## 一、为什么加入两个校验工具

当前比赛是**未知题型、论文为核心成果**的场景。过去仅有方法手册和抽象的实验要求，容易出现：把往届题型当今年默认解；训练标签出现在预测特征中；给没有 mask 的 bbox 数据计算所谓真实分割指标；优化只报告目标值、不复核可行性；数字脱离正式结果；把“PDF 在仓库里”误当成“论文已经分析过”。

这轮增加的是**可执行的前置审核**，而不是已经复现了全部往届题目。

## 二、获奖论文清单与复盘闸门

[2024–2025 年实际文件清单](../competition/award_papers_2024_2025.json) 来自 GitHub 仓库 `EvelynEarth/supreme-spoon` 文件树：2024 和 2025 各 8 篇，共 16 个 PDF。文件名与字节大小已核对；**PDF 研究内容未逐篇检读**，初始 `review_status=unreviewed`，方法统计有效分母为 0。

推荐操作：

```bash
python skills/big-data-competition-skill/tools/award_paper_audit.py --summary
python skills/big-data-competition-skill/tools/award_paper_audit.py --inventory path/to/reviewed_inventory.json --summary
```

只有确实读取 PDF 正文并复核相关页码，才允许将对应篇目改为 `reviewed`、`pdf_content_verified=true`，每条方法发现必须有 `question`、`page`（从 1 开始）、`method_family`、`attribution`（`author_reported` / `reviewer_inference`）、`evidence_note` 和 `evidence_verified=true`。不能用推断替代作者声明；不能从关键词次数臆造“使用过的算法”次数。

方法出现频率按**已复盘论文数**作分母，按每篇论文每方法至多计一次；若分母为 0，则不生成方法频率结论。逐篇还需要按 [复盘提取表](../templates/award-paper-audit.md) 留下分析与风险说明。

## 三、四类赛题的合成对抗评测

[评测场景配置](../benchmarks/mathorcup_scenarios.json) 包含四类**由历史赛题的高层任务类型启发**的正例，以及六个含典型错误的反例。注意这些只是 synthetic plan fixtures，并非真实比赛数据、原始标签、历史优秀方案或算法实测成绩。

```bash
python skills/big-data-competition-skill/tools/competition_benchmark.py
python skills/big-data-competition-skill/tools/competition_benchmark.py --suite path/to/scenarios.json
```

覆盖面：

| 示例任务 | 必须关注的错误 |
|---|---|
| 2024 A 台风路径/时序类型 | 按事件分组与时间切分，避免随机拆散同一个轨迹 |
| 2024 B 预测与分仓规划类型 | 分配、仓容等优化决策必须可行性复核 |
| 2025 A 集装箱视觉类型 | 图像同实体/场景近重复泄漏；bbox 不等于 pixel mask |
| 2025 B 物流理赔类型 | 赔付结果可作训练标签，不可偷看为预测特征；官方结果模板与指标来源需核对 |

失败闸门还包括：缺少 Baseline、官方结果格式未经核实、数值结论没有 `accepted_artifact`。工具输出 `expected/actual/matched` 与详细理由，测试只有对正确方案放行且拒绝错误方案才算通过。

**重要：**工具的 `passed` 只表示预设的结构化方法计划符合这些规则，绝不等于跑出模型、获得特定准确率、论文已获奖或正式结果文件正确。

## 四、从测试到真实赛题

当本届正式赛题发布，先用题面、附件、官方表格填写 Competition Contract，再改写对应 `plan`。真实工程还要亲自运行并记录：数据版本、split ID、特征生成、Baseline、候选模型、正式结果、误差、消融与论文 Evidence Map。不能直接把合成测试中的 `expect=pass` 当本届正式结果。

此流程与 [Competition Validation Gates](competition-validation-gates.md) 合用；当届官方规则永远优先。