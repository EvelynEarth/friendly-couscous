# Big Data Competition Skill v2.4.0

面向**未知赛题、最终以论文为核心成果**的 MathorCup 等大数据竞赛通用 Skill。主入口见仓库根目录 [SKILL.md](../../SKILL.md)；本目录为按需加载的方法、证据与辅助预检层。

它不是 Kaggle leaderboard 流程，也不是以传统数学建模固定套路选择算法。以当届题面和数据决定所需方法，先确保验证可信，再尝试复杂模型。

## 入口与功能

- [本模块 SKILL.md](SKILL.md)：按需执行与动态路由。
- [方法手册目录](playbooks/00-index.md)：已有表格、时间序列、视觉、优化等任务手册，以及大规模数据、时空/图模型补充。
- [外部 Skill 参考路由](references/external-skill-routing.md)：Probabl、K-Dense、Ultralytics、Hugging Face 的限定式参考；不强制安装。
- [比赛验收门](references/competition-validation-gates.md)：数据、泄漏、实验、论文证据与官方交付检查。
- [优秀论文复盘协议](references/award-paper-audit.md)：配合 [逐篇审查表](./templates/award-paper-audit.md)，从实际 PDF 页码提取可迁移经验。
- [标准库预检工具](tools/bigdata_preflight.py)：`assets` / `yolo` / `csv` 三种只读模式。

## 本地运行

```bash
python skills/big-data-competition-skill/tools/bigdata_preflight.py assets --root path/to/dataset --strict-lfs
python skills/big-data-competition-skill/tools/bigdata_preflight.py yolo --root path/to/yolo_dataset --split train --task detect --classes 3
python skills/big-data-competition-skill/tools/bigdata_preflight.py csv --template official.csv --candidate result.csv --id-column order_id --numeric amount --enum risk=0,1,2
python -m unittest tests/test_bigdata_preflight.py
```

以上仅检查文件级约束，不执行赛题模型、GPU 训练或证明预测效果。具体文件格式、提交方式与评价指标必须按当届官方通知核验；没有完整读取的获奖论文不得当作已分析数据。

## v2.2 新增实战质量闸门

- [历史赛题合成对抗测试和获奖论文证据审核协议](references/historical-benchmark-protocol.md)
- [16 个已确认的优秀论文 PDF 文件元数据](competition/award_papers_2024_2025.json)

```bash
python skills/big-data-competition-skill/tools/award_paper_audit.py --summary
python skills/big-data-competition-skill/tools/competition_benchmark.py
```

上述工具检查证据状态与方法计划，**不训练真实赛题模型**。

## v2.3 本地赛题数据就绪与论文数字审计

详见 [真实案例检查协议](references/real-case-replay.md)、[附件来源快照](competition/real_case_2025_profiles.json) 和 [实验证据模板](templates/accepted-evidence-record.md)。

```bash
python skills/big-data-competition-skill/tools/real_case_audit.py 2025-a --root /path/to/数据集3713
python skills/big-data-competition-skill/tools/real_case_audit.py 2025-b --root /path/to/赛道B附件目录
python skills/big-data-competition-skill/tools/paper_evidence_gate.py --record /path/to/accepted.json --artifact-root /path/to/outputs
```

## v2.4 独立质量审核与论文论证写作

- [模型与结论正确性核验](references/solution-validity.md)（无题型/算法预设）。
- [扰动稳定性与不确定性](references/stability-and-uncertainty.md)（有真实运行才汇总）。
- [论文结构、衔接与审稿逻辑](references/paper-argumentation.md)。
- [通用复核记录](templates/solution_quality_record.md)、[稳定性记录](templates/stability_record.md)、[优秀论文写作结构阅读卡](templates/award-paper-writing-review.md)。

正式论文首要回答**题意是否解决、模型/计算是否可信、结论是否成立**，不追求机械地堆叠模型数和图表数。
