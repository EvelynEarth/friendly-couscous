# v2.8 项目级证据链：防止跨模块“假通过”

之前的求解质量审核、独立参考计算、数值不变式、稳定性分析和论文证据追踪均能单独运行，但**单独通过不能推出整篇比赛论文可定稿**。例如，论文指标文件与正文一致，而独立复算发现计算错误；或稳定性实验是另一次无关运行；或一问缺少验收仍被忽略。

本模块增加项目级、**逐子问且失败关闭**的交叉验收。但**它的适用范围限于当前参考算法已支持、能映射全部数字型指标的任务**，不是任意未知赛题的通用终稿审批器。文本研究、非标准估计量、无法表达的优化模型和其他非数值任务，应先采用 [通用研究包审稿流程](competition-final-runbook.md)，再设计题目专属独立验证；绝不可虚构一份 oracle 让这个工具返回绿色。主要服务未知当届赛题，**不是某年赛题的模型模板**。

## 真实使用前提

- 优先完成当届官方题意拆解；列出**所有**需要回答的子问 ID，任何一问不得凭空删掉。
- 只输入实际存在的文件路径、真实原子验证数据和实际运行后的指标产物。SHA-256 说明“文件与快照一致”，不证明数据来源合法或模型有科学效度。
- 先独立审核数学公式/单位、验证集隔离、必要优化约束、统计假设和实验设计。本工具不能替代一位真正独立的科学审稿人。

## 运行

```bash
python skills/big-data-competition-skill/tools/project_evidence_chain.py \
  --manifest /path/to/project_evidence.json \
  --artifact-root /path/to/real_outputs
```

项目 manifest 必须是一个真实 JSON 文件，结构如下。示例是**字段形状**，不能直接用虚构数据当正式审核：

```json
{
  "schema_version": 1,
  "project_id": "official-competition-and-team-run",
  "official_questions": ["Q1", "Q2"],
  "quality_record": "quality.json",
  "files": [
    {"path":"quality.json","sha256":"replace-with-real-64-char-sha256"},
    {"path":"independent-q1.json","sha256":"replace-with-real-64-char-sha256"}
  ],
  "questions": [
    {
      "id": "Q1",
      "paper_record": "accepted_q1.json",
      "oracle": {"engine":"independent","case":"independent-q1.json"},
      "metric_map": {"mae":"recomputed.mae"},
      "invariants": {
        "contract":"q1_invariants.json",
        "result":"q1_numeric_output.json",
        "result_links":{"predicted":"predicted"}
      },
      "stability": "q1_stability.json",
      "stability_anchor_run_id": "accepted-seed"
    },
    {
      "id": "Q2",
      "paper_record": "accepted_q2.json",
      "oracle": {"engine":"extended","case":"independent-q2.json"},
      "metric_map": {"macro_f1":"recomputed.macro_f1"},
      "invariants_not_applicable_reason": "Explain substantively why no supported numeric invariant applies.",
      "stability_not_applicable_reason": "Explain why this particular question cannot use a repeated-run analysis."
    }
  ]
}
```

**注意**：上方 Q2 的 `engine` 与 `metric_map` 只是 schema 演示，实际 oracle 是否提供 `recomputed.macro_f1`，需由真实输入算法决定；映射到不存在的数值会阻断，不能直接把此模板当成功案例。你必须将**所有被引用**的 quality、paper、oracle、invariant、stability JSON，以及质量审核中已通过步骤的证据文件、paper 产物（如真实 metrics.json / split.csv）全部加入文件 SHA-256 清单。

## 明确的阻断条件

| 检查 | 阻断情形 |
|---|---|
| 题意子问覆盖 | 官方子问缺失、重复、多余，或质量审核记录未覆盖 |
| 项目文件快照 | 文件缺失、路径逃逸、内容与声明 SHA-256 不同 |
| 实验论文链 | 正式论文未使用 `paper_evidence_gate.py` 的严格回读模式；论文数值/指标文件/结果记录不一致 |
| 独立数值 | 参考计算器未通过，或者**部分正式指标没有独立计算结果映射** |
| 必要不变式 | 实际输出违反数学必要条件、结果文件与参考计算输入不一致 |
| 稳定性 | 波动超过预先阈值，或给出的“稳定性锚点运行”与正式采用的指标不一致 |
| 缺失验证说明 | 跳过不变式/稳定性却没有具体、充分的学术理由 |

当前支持 `engine=independent`（原子分类/回归及受限整数线性）和 `engine=extended`（时序滚动、配对符号翻转、iid 伯努利仿真、可分离严格凸盒约束二次优化）。**不属于这些数学类型的赛题，不能填虚构的 oracle 使程序变绿**，应编写项目专属可手算、交叉求解或形式化核验，并保留人工 Reviewer 的待审状态。

`invariants.result_links` 强制把 `result.json` 中待验的 `values` 与独立参考器 `case.json` 中同名/映射的原子输入逐一对应，防止拿与原结果不相干的“正常文件”冒充被检查输出。如果输入不是平铺的原子字段（例如滚动时序的嵌套多折），应使用课题专属跨文件检查，或明确说明当前 DSL 不适用，**不能声称不变式已被这项工具验证**。

`stability_anchor_run_id` 需要能在真实稳定性重复运行表中找到唯一一行，其 `value` 和本子问已接受 `metrics[stability.metric]` 完全一致。其他扰动运行也必须真实执行并保留实验来源，不能事后为漂亮结论编造数据。

### 状态解释

- `blocked`：存在缺失、错误、冲突、未通过的必要检查。解决之前不能将其当作完成的论文数值验证。
- `machine_evidence_consistent`：**工具能验证的各个数字和文件在当前快照中自洽**；附带 `scientific_approval=human_scientific_review_still_required`。这**不是**“论文可以提交”或“模型已被科学证明正确”。
- 需要由独立科学 Reviewer 核查原题建模、真实数据合法性和各统计前提，再由论文 Reviewer 核查章节逻辑、图表和结论边界。

### 合成端到端回归测试

`tests/test_bigdata_project_evidence_chain.py` 创建一份可手算的假想回归项目（MAE/RMSE 均为 1），包含质量证明、独立原子计算、不变式、稳定性、指标真实 JSON、摘要数值链与 SHA 快照。并通过**19 个正反例**测试识别数字双向篡改、跨文件结果替换、失败稳定性、漏题、无关证据、哈希不一致、部分指标缺少独立计算等错误。

这些都是工具集的**合成验收测试**，不代表已经跑过真实历史 MathorCup 数据，更不是优秀论文全文结构的复盘。今后优先使用真实任务对整条链进行独立测试。论文如何论证见 [论文研究逻辑](paper-argumentation.md) 与 [科学正确性审核](solution-validity.md)。

## v2.9 与通用竞赛验收的关系

`project_evidence_chain.py` 是**适用类型下可选的更严格数值门槛**；`competition_readiness.py` 是**任何实际题型的文件/结构覆盖检查**。两个工具均不能从报表“passed”判断真实统计或科学前提成立。若专业 Reviewer 发现题意模型错误，即使两个工具都报告数值自洽，也必须阻断真实论文终审。
