# 通用论文研究包填写说明

本文介绍 `competition_readiness.py` 的审稿记录 JSON。这里的条目只是**字段结构**；没有真实审稿人的独立复核、真实运行文件与本届官方要求时，禁止凭此模板声称“论文可以提交”。

记录结构及要点：

- `schema_version: 1`、`competition_id`、`official_questions: ["Q1", ...]`：照今年题面填写，不固定三问。
- `files`：所有被引用的真实附件、实验/复核证据、论文草稿及提交规则核验产物，分别记录项目根目录内相对路径和文件内容的 SHA-256。禁止使用路径逃逸与虚构哈希。
- `questions[]`：每个官方题目恰好一个记录，包含 `id`、`objective`、`official_output`、`delivered_answer`、`model_choice_reason`、`claim_ids`。
- `questions[].reviews`：四项 `model_correctness`、`independent_verification`、`reliability`、`stability`。实际通过写 `{"status":"passed","method":"真实做了什么","artifact":"可校验文件"}`，独立复核另加 `"independent": true`。如果可靠性或稳定性**科学上确实不适用**，可填 `not_applicable` 和不少于 25 字的具体原因，模型正确性和独立复核不许跳过。
- `claims[]`：每条有 `id`、`question_id`、`statement`、`strength`、`scope_and_limitations`、`evidence` 数组及 `status:"supported"`；因果主张只在因果任务且有识别依据时使用；“全局最优”必须是优化问题且写清数学依据。
- `paper`：`manuscript` 指向完整稿；`sections[]` 不强制固定标题，但逻辑作用 `function` 必须覆盖 `problem,method,validation,results,discussion,conclusion`，并用 `argument` 说明本节为什么存在、`claim_ids` 链接结论。`conclusion_claim_ids` 应覆盖每个官方子问。
- `delivery`：`rules_from_current_competition_verified:true` 表示**已经人工核对**本届公告；`official_requirements[]` 应逐项有 `id`、`status:"checked"`、`detail` 和审核证据 `artifact`。缺失真实核查时不得填 true。

更简洁的思路：**一问一份可信解答、一结论一份实际证据、一章节一项论证作用、一交付要求一项核对记录。**

```bash
python skills/big-data-competition-skill/tools/competition_readiness.py --record ./review-package.json --artifact-root ./results
```

返回 `blocked` 时逐项解决缺失；返回 `documentation_consistent_pending_expert_review` 时只能称“资料一致并可供独立审阅”，仍需真正的 Scientific Reviewer 和 Editorial Reviewer。数值型题目如有适用的独立 oracle，再额外使用 `project_evidence_chain.py` 进行更严格的实际数字交叉核验。
