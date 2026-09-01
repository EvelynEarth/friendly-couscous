# Module 03B：独立结果深化分析代码

本模块只接受已验收的主工作簿。根据真实主结果选择参数敏感性、场景压力、多算法/多初值、结构稳健性、阈值、异质性、误差分解或外样本稳定性。若 current `模型论文框架.md` 已存在，制定分析计划前先读取本问当前模型、验证方案、主结果摘要、适用/失效边界和跨问依赖，再用已验收主工作簿复核具体数值；不得脱离框架按聊天印象选择分析对象。

数据事实源必须继承当前 `preprocessing_decision`，不得在深化分析阶段重新决定数据清洗口径：

- `not_needed`：可读取必要原始数据 + 已验收主工作簿；
- `question_local`：可读取必要原始数据，并仅复现本问数学层已经定义的局部变换；
- `project_level`：读取 `数据预处理/数据预处理结果.xlsx` + 已验收主工作簿，禁止再次直接读取对应共享原始数据。

本模块的跨阶段 handoff、用户返回深化结果后的合理性复核和当前问题 closure 统一服从 `core/workflow_convergence_contract.yaml`。代码身份、候选版本、接口绑定和失败恢复服从 `core/code_quality_contract.yaml`。深化分析工作簿 accepted 并不自动授权进入 MATLAB 或下一问。

## 一、执行规则

```text
主工作簿accepted
→ 主结果 post_execution_review passed
→ 冻结canonical问题X求解.py
→ 绑定accepted主工作簿identity/path/hash/sheets/headers
→ 继承preprocessing_decision与当前数据事实源
→ 建立result_analysis_plan
→ 为每项计划声明target claim与判定准则
→ 新建唯一candidate问题X结果深化分析脚本
→ 读取当前数据事实源 + 已绑定主工作簿 + 必要前问标准工作簿
→ validate_code_delivery.py静态验收analysis阶段代码与artifact identity
→ 用户本地full_fidelity运行
→ candidate对应深化工作簿
→ validate_user_execution.py验收
→ 对每项证据给出support / modify / reject
→ post_analysis_review：检查分析结论、范围、异常与对核心答案的影响
→ 用户接受后冻结canonical问题X结果深化分析.py/工作簿
→ passed 后才允许进入 Figure Evidence / question_closure_gate
→ analyzed或redo_required
```

`问题X结果深化分析.py` 是独立可复现程序，不复制主求解主链，不通过改写 `问题X求解.py` 实现深化分析。其 `FULL_FIDELITY_CONFIG.stage` 必须为 `analysis`，工作簿中的 `code_sha256` 必须对应该深化分析脚本，并记录当前数据事实源的哈希。

## 二、上游工作簿接口绑定

生成深化分析代码前必须实际打开已验收主工作簿并记录当前接口：

```text
source question/stage identity
→ accepted workbook path + hash/identity
→ actual worksheet names
→ actual required headers
→ primary keys / units / row-granularity
→ analysis consumer requirements
```

硬规则：

1. 不得凭旧版本、另一问或模板经验假设主工作簿具有某些“标准工作表”；
2. 深化分析只要求分析真正需要且已在上游核验存在的 sheet/header；
3. 如果需要的信息上游没有输出，先判断它是否可从现有已验收结果无歧义派生；若不能，则回到主求解接口设计，不得在分析脚本里伪造一套新主结果结构；
4. 运行时发现缺 sheet/header 时，错误信息应列出 `required` 与 `actual`，而不是只说“缺少标准工作表”；
5. 不使用模糊匹配把名字相近的 sheet/header 静默当成目标字段；
6. 若绑定的上游工作簿被替换或哈希/identity变化，旧 analysis candidate 立即 stale，重新核验接口后再运行。

## 三、Analysis Evidence Disposition

深化分析的每一项敏感性、鲁棒性、外样本、压力测试、多算法或多初值证据都必须说明它**作用于哪个具体主张**，并给出以下三种 disposition 之一：

- `support`：目标主张在该检验下保持，可作为正文增强证据，但不得自动扩大适用范围；
- `modify`：目标主张主体仍可使用，但区间、阈值、置信度、排序、边界或文字必须修改，并使依赖的 paper fragments 在完成同步前保持 stale；
- `reject`：目标主张不能继续原样使用。若否决的是核心答案、核心模型结构或关键可行性判断，必须 `redo_required` 并按原因回退；若只是否决一个附加的“稳定性很强”等非核心 claim，可以删除/重写该 claim，而不强迫整题重算。

每项证据至少记录：

```text
Evidence ID
→ method/source
→ target claim
→ disposition
→ key finding
→ required action
→ paper/figure anchor
```

禁止只写“通过敏感性分析验证了模型稳定性”而不说明：分析了什么、支持/修改/否决了哪个主张、变化范围多大以及正文应怎样处理。

## 四、并列最优、近并列与稳健性语义

优化/枚举类问题在深化阶段必须优先区分：

- `exact tie`：数学/离散枚举结果完全相等；
- `tolerance tie`：差异小于预先声明的数值容差；
- `small nonzero gap`：确有唯一最优，但与次优差距很小。

三者不得混写成“唯一最优”或“并列最优”。若存在多个最优策略，工作簿、正文和图表必须保留完整最优集合，除非题目额外给出明确二级排序规则。

稳健性分析优先回答“结论在什么范围内保持/何时切换”，而不是机械多跑几组扰动。对离散策略、方案选择或阈值问题，优先候选证据包括：

- 最优—次优目标 gap；
- 参数切换边界/decision region；
- stable set / admissible set；
- 多场景排名保持率；
- 结构性退化或失效条件。

若题面点处最优但非常靠近切换边界，应表述为“当前点最优但局部稳健性有限/边界附近”，不能因基准点仍最优就写成“稳健性强”。

## 五、Post-analysis Review 与跨问关闭

用户返回深化分析结果后，在规划 Figure Evidence 或下一问前必须执行 `workflow_convergence_contract.post_execution_review` 的 analysis 变体，至少回答：

1. 是否存在异常范围、符号、单位、约束或边界行为；
2. 各项 `support / modify / reject` 是否与工作簿证据一致；
3. 是否有某个 `modify/reject` 尚未同步到主张、框架、图表或正文；
4. exact tie / tolerance tie / small nonzero gap 是否被正确区分；
5. 核心答案是否仍保持；
6. 下一步允许进入 Figure Evidence、回退重算，还是当前问题已经满足 closure 条件。

只有 `post_analysis_review.status=passed` 且无未处理的核心 `reject`，当前 analysis 阶段才算闭合。若用户询问“结果是否合理”，本模块应先完成此审查，不得把问题直接推进到下一问。

## 六、候选版本与错误恢复

深化分析脚本的实质修改必须新建 candidate/version 后缀，不覆盖用户正在运行或比较的上一版；只有用户接受后才冻结为 canonical `问题X结果深化分析.py`。

发生以下错误时先诊断再改代码：

- 主工作簿找不到：重新核对实际项目树与 accepted workbook binding；
- sheet/header缺失：列出实际 sheet/header，检查是否绑定错版本/错问题；
- 输出工作簿结构不匹配：检查 analysis candidate identity 与预期输出合同；
- 同一错误重复出现：停止继续改名/猜路径，给出 root-cause diagnosis。

不得让一个 analysis candidate 同时兼容多套互相冲突的旧工作簿 schema；兼容需要明确、有限且可审计，否则应重新绑定当前 accepted artifact。

## 七、数据与模型边界

数据处理边界：

- `project_level` 项目不得重复公共去缺失、异常处理、单位换算、统一滤波、统一重采样或坐标修正；
- `question_local` 项目只能复现当前小问已有数学来源的局部变换，不得新增全局清洗；
- `not_needed` 项目不得为了深化分析方便而擅自补值、删异常、平滑或滤波。

若深化分析发现公共数据处理口径本身导致结论不稳定，且当前为 `project_level`，应回退 `data_preprocessing`；若发现 `not_needed/question_local` 的判定本身错误，则回退 `model_design` 修改 `preprocessing_decision`；若发现模型语义问题，则回退 `model_design`；若仅主求解数值质量不足，则回退 `solve_validate`。任何回退都必须按依赖传播下游 stale。

若核心结论未保持，必须回退相应阶段并标记真实依赖的下游 stale。默认不生成独立运行配置、运行说明或校验报告。
