# 自动比赛代理：分阶段识别、纠错回退与论文终审（v2.10）

目标：用户提供赛题和数据后，代理读取主 Skill 并结合**持久的状态文件**自动识别做到哪一步，逐阶段分析、建模、运行、验证与写论文。每次出现验证失败，优先修复上游原因，而不是涂改论文结论。

## 使用边界

GitHub 上的 Skill **不能自动提升为平台 system prompt**，聊天仅上传附件也不能直接启动本地 Python。代理只有在当前聊天/Project/Work/Codex **实际加载入口并拥有文件读写和执行权限时**，才能自动执行后续程序。没有持久工作区时，不能保证跨聊天续接。控制器不是 LLM、不会自行训练模型或在聊天结束后后台运行。

## 一次性代理入口指令

将下段文字放在 ChatGPT Project 项目说明中，或在比赛第一次对话发出：

> 收到赛题/数据后，读取 GitHub EvelynEarth/friendly-couscous 最新 main 的 SKILL.md、AGENTS.md 和 skills/big-data-competition-skill/references/automatic-competition-workflow.md。若项目存在 autopilot-state.json，恢复进度；否则对正式附件建立输入快照。每轮读取当前阶段和对应参考，实际完成研究、编程、实验、独立审核、绘图和论文，并记录真实证据。发现失败要诊断并回到上游修正，自动尝试最多三轮；关键建模方案与正式交付必须明确征得我同意。任何没有真实结果的步骤不许填 passed；没有运行权限时给我可以执行的代码，不许假装完成。

## 自动阶段路由

| 阶段 | 必须做的事 | 关键停点 |
|---|---|---|
| intake | 盘点真实文件并计算 SHA-256 | 只说明文件存在，不代表读懂赛题 |
| contract | 对照官方逐问建立任务、指标、交付契约 | 题目不完整则阻断 |
| data | 检查数据可读性、字段、分组/时间信息和泄漏 | 不允许测试集调参 |
| plan | 候选模型、简单基准、假设和依据 | **用户批准方案** |
| baseline | 真实运行可比较的基准 | 没执行不许通过 |
| solve | 完成数学建模与可运行的主求解程序 | 不得伪造数值 |
| verify | 复核公式/算法、结果、合法数据及约束 | 失败时回退数据/方案/代码 |
| robustness | 扰动/不确定性/失败情况分析 | 不承诺普遍稳定性 |
| figures | 用真实结果绘制科研图表 | 图表需可追溯 |
| paper | 论证链、正文数字和结论 | 数字不能超出证据 |
| final | 科学 Reviewer + 论文逻辑 Reviewer | 任一关键错误阻断 |
| delivery | 对照官方规则打包与审阅 | **用户最终批准；不自动上传** |

阶段适用于未知题型，专项检查由主 Skill 按题目自适应选择；不要机械把不适用的因果/优化/分类检测强加给当前模型。

## 工作区启动和恢复

项目应有两套目录：`official_inputs/`（原始赛题、数据）和 `competition_workspace/`（生成的报告、真实程序及输出）；二者不能嵌套。启动：

```bash
python skills/big-data-competition-skill/tools/competition_autopilot.py init --inputs /path/to/official_inputs --workspace /path/to/competition_workspace
python skills/big-data-competition-skill/tools/competition_autopilot.py run --workspace /path/to/competition_workspace
```

初始化会计算输入文件 SHA-256，创建 `autopilot-state.json` 和历史事件。此控制器不会修改原始输入。超过 50,000 个文件时要求先分批建立受控资产清单，不得偷偷删样本。大型附件的全量哈希可能耗时。

`run` 会输出 `awaiting_work` + `next` 阶段，或 `awaiting_human_approval`、`awaiting_rework`、`gate_blocked`、`rewind`、`human_escalation`、`machine_workflow_complete`。代理应依照状态继续做真正的工作，不应把 `awaiting_work` 当作 AI 已执行了任务。

## 阶段证据如何记录

每个阶段，代理先生成真实非空 `competition_workspace/artifacts/...` 文件，再创建 `competition_workspace/reviews/<stage>.json`。字段结构可以查询：

```bash
python skills/big-data-competition-skill/tools/competition_autopilot.py template --stage contract
```

示例是**结构示意，并不是真实审题已经通过**：

```json
{
  "stage": "contract",
  "decision": "passed",
  "artifacts": ["artifacts/competition_contract.md"],
  "checks": {
    "all_questions_mapped": {"status": "passed", "method": "独立核对每一个官方子问", "artifact": "artifacts/competition_contract.md"},
    "outputs_and_rules_mapped": {"status": "passed", "method": "逐条核对提交输出与限制", "artifact": "artifacts/competition_contract.md"},
    "unknowns_identified": {"status": "passed", "method": "记录官方未明确事项", "artifact": "artifacts/competition_contract.md"}
  }
}
```

工具会校验所有必要检查项是否具有报告方法、**实际存在的非空证据**，并计算报告及文件 SHA-256。通过仅代表机器审核覆盖完整，不能代替独立数学复核。真实模型应再调用 `competition_readiness.py`、`independent_oracle.py`、`project_evidence_chain.py` 等适用的证据工具。

完成阶段后再次运行 `run`，代理即可自动推进已有合格证据的下一个阶段。项目中断后使用 `status --workspace ...` 查看当前阶段；有持久状态文件时可跨会话恢复。

## 自动诊断和回退

如果 `verify` 检出数据泄漏，代理应把该阶段 review 写为：

```json
{"stage":"verify","decision":"failed","failure_class":"leakage","reason":"验证特征含有预测时点之后的记录，需要重建时序切分、特征与模型。"}
```

再次执行 `run`，控制器会从 `verify` 自动退到 `data`，使涉及的原始检查与结果失效，拒绝用旧报告直接通过。其他归因路由包括 `model_invalid→plan`、`implementation→solve`、`unstable→solve`、`paper_mismatch→paper`、`task_mismatch→contract`。代理必须实际改变模型/代码/证据并重新验证，而非只改 JSON 状态。

已被验收的报告或产物一旦发生变化，状态自动撤销受影响阶段的通过；原始赛题或附件发生变化，默认输出 `inputs_changed`，必须确认变化后显式运行：

```bash
python skills/big-data-competition-skill/tools/competition_autopilot.py sync-inputs --workspace /path/to/competition_workspace
```

默认每个失败阶段自动尝试 **3 次**，达到上限进入 `human_escalation`，不能无限循环伪优化。

## 人工批准和外部执行边界

在 `plan` 和 `delivery` 阶段必须明确获得用户确认。控制器提供：

```bash
python skills/big-data-competition-skill/tools/competition_autopilot.py approve --workspace /path/to/competition_workspace --stage plan --actor confirmed-user
```

**必须先有真实用户批准，代理不得私自替用户运行 approve。** 字段 `actor` 只是本地审计信息，不具备身份认证。`delivery` 通过也只是生成可交付材料，绝不能擅自上传论文或消费未授权计算资源。

没有可执行环境或无法访问完整数据时，停止并说明具体缺口；不能捏造运行时间、论文数字和成功状态。GitHub CI 只验证状态机和合成测试，不证明未知赛题解答正确。

## 每次续接时的代理算法

1. 加载主 `SKILL.md`，查 `autopilot-state.json`，运行 `run` 并读取 `next`/`status`。
2. 只加载当前阶段需要的 references/playbooks；对正式题目实施具体研究或模型求解。
3. 保存实际程序、日志、表图、独立核验等产物，记录 stage review。
4. 运行 `run` 校验。如有 blocker / failure，先定位原因、回退并修复。
5. 若需要人工批准、运行权限或异常科学判断，明确暂停并提出集中问题。
6. 完成终稿时输出研究结论、证据位置、未解决风险及官方交付清单；严禁越权提交。

参见 [完整赛场执行手册](competition-final-runbook.md) 和 [模型正确性核验](solution-validity.md)。


## v2.11 失败自动回退的论文质量检查

执行 `figures` 必须按 [论文视觉与学术质量硬门](paper-visual-quality-gate.md) 保存可追溯图表生成代码、色彩及线型含义、PDF 中实际可读的图例/标签、灰度可辨识检查。执行 `paper` 必须审查学术论证、真实引用、段落证据链，生成可编辑 XeLaTeX 文件（用户使用 TeX Live 时）和当前 PDF；编译错误/缺少图片或论文句子不成立直接重做源码。执行 `final` 必须保存逐页渲染审核结论和真实编译日志，不得只检查文件存在、图表哈希或随意写 passed。缺原模板时标记缺口，不应据此阻塞建立可独立编译的通用 TeX 草稿。

失败时使用 `plot_mismatch→figures`、`paper_mismatch→paper` 等已有回退路径，修正实质问题并重新验收。2023 MathorCup 大数据赛论文的标题/摘要首页、第二页目录、正文页码、匿名等规则来源需明确区分传统 MathorCup 数模竞赛公告，不得擅自混用。人工最终批准仍不可绕过。
