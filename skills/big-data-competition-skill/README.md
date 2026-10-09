# Big Data Competition Skill v2.12.0

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

## v2.5 真实结果反证与论文证据严格模式

[数值不变式协议](references/result-falsification.md) 允许依据未知新赛题的数学条件检查实际结果；[填写模板](templates/result-invariant-contract.md) 仅用于定义必要条件。定稿前，`paper_evidence_gate.py --require-metric-source` 额外回读并绑定真实 metrics 文件。检查通过**不等于已证明模型科学正确性**。

## v2.6 独立重算

[独立复算协议](references/independent-recomputation.md) 与 [输入例子](templates/independent-oracle-case.md) 展示如何由实际预测重算模型指标，以及对小规模整数线性子问题进行精确枚举检查。该工具有 20 个手算/反例测试，但不能保证任意赛题或大规模求解正确。

## v2.7 扩展科学独立复算

- [适用条件与独立验证流程](references/extended-oracles.md)
- [JSON 正确答案与故意失败的示例](templates/extended-oracle-cases.md)
- `python skills/big-data-competition-skill/tools/extended_oracles.py --case check.json`

本模块需要真实数据和适用的模型假设；配套 28 个测试均为合成工具测试，不是历史比赛模型成绩。

## v2.8 端到端数值证据闭环

项目级机器复审：[使用协议](references/project-evidence-chain.md)；工具 `tools/project_evidence_chain.py --manifest project.json --artifact-root real_outputs/`。需要完整官方子问、真实不可随意替换的实验数据/论文来源、独立重算与稳定性锚点。此工具的成功只表示机器能检查的证据未发现冲突，不等于科学审稿通过。

## v2.9 赛场通用终稿操作

[通用研究解题/交付流程](references/competition-final-runbook.md)、[审核 JSON 格式](templates/competition-readiness-record.md) 和 `tools/competition_readiness.py` 面向未知数学/数据任务，确保每一官方问题有明确证据和论文逻辑。返回“documentation_consistent_pending_expert_review”**并不代表科学批准**；需要研究者独立审核真正的数据、公式、结论和本届交付要求。

## v2.10 代理自动驾驶（需授权执行环境）

[自动比赛执行、续接、失败回退和人工审批手册](references/automatic-competition-workflow.md) 提供可复用阶段管理；[ChatGPT Project 复制指令](templates/automatic-project-instructions.md) 用于一次性设置。工具 `tools/competition_autopilot.py` 管理本地状态文件，不在后台独立调用模型；真实模型性能和 SCI 论文科学性仍需实际复核。


v2.11 论文图表与 XeLaTeX：参见 [paper-visual-quality-gate](references/paper-visual-quality-gate.md) 和 [XeLaTeX 论文模板](templates/bigdata-paper-xelatex.md)。所有结论与视觉输出必须由真实实验支撑、逐页复核，且依当届论文规定，不预设传统数学建模格式。


v2.12.0: [XeLaTeX 骨架](templates/bigdata-paper-xelatex/main.tex) 已重构章节字号、首行缩进、单目录与 caption 自动编号；运行 [latex_paper_audit.py](tools/latex_paper_audit.py) 静态/编译预检后仍须逐页检查图例、坐标标签、表格和段落。

 
v2.12：新增 [优秀论文实证排版/彩色图/篇章样本对照](references/award-paper-empirical-layout.md)，链接 supreme-spoon 16篇全部716页机器抽取结果及48页视觉抽查卡；全文学术论证依然需要带页码的独立审读，严禁宣称已完成。
