# Module 03A：主求解代码交付

本模块在 `问题X求解/` 中生成主求解代码。助手只生成和静态检查，不运行赛题代码。

若项目根目录已有 current `模型论文框架.md`，正式生成本问代码前必须先读取“当前有效口径”、本问“当前模型口径/求解与验证方案/模型挑战与人工锁模”以及必要前问依赖，用它恢复当前模型语义；不得仅凭聊天记忆重建变量、参数、目标或约束。具体输入数值和已验收结果仍回到当前数据事实源/标准工作簿核验。

进入本模块前，当前小问必须依次通过 `scripts/validate_semantic_governance.py` 与 `scripts/validate_model_approval.py`。前者负责当前题意/语义/复杂度与 stale 一致性，后者是 Challenge/Human Approval 的唯一字段级运行门；具体批准状态、revision/hash 绑定与失效条件只服从 `core/model_approval_contract.yaml`，本模块不复制第二套检查清单。

任一 gate 未通过都不得生成正式主求解代码；Model Approval 未通过时返回 Module 02，并停在 `awaiting_model_approval`。

跨阶段 handoff、真实项目路径绑定、用户返回结果后的合理性复核以及“何时允许进入下一问”统一服从 `core/workflow_convergence_contract.yaml`。代码身份、候选版本、上游/下游接口与失败恢复统一服从 `core/code_quality_contract.yaml`。本模块只落实主求解阶段职责，不另建第二套 Question Closure 规则。

## 项目路径绑定

正式生成或重生成会读取本地附件的主求解代码前，必须根据用户真实项目树、已上传文件元数据或 current project state 建立 `project_path_contract`。路径属于实现事实，不得因为示例工程通常把附件放在项目根目录，就把未经核验的绝对路径写入代码。

至少确认：

- 项目根目录；
- 当前 `问题X求解/` 目录；
- 原始附件/预处理工作簿的真实位置或确定性相对寻址规则；
- 输出工作簿路径；
- 当前操作系统路径语义。

优先使用“项目根目录 + 已观察到的相对路径”解析。确需候选路径时，候选顺序必须显式、确定，并在失败信息中列出实际检查过的路径。用户返回 `FileNotFoundError` 后必须先重新核对项目树，不得原样再次发送使用同一错误路径假设的代码。

## 代码候选、身份与命名

主求解代码在设计/修复阶段必须区分 `candidate` 与 `canonical`：

```text
candidate_vNN_<short-note>.py
→ 用户本地运行/结果审查
→ accepted/frozen
→ canonical 问题X求解.py
```

规则：

1. 每次会改变运行行为、输入接口、输出结构或核心实现的修改都使用新的 candidate/version 后缀，不覆盖用户正在比较的上一版；
2. 用户明确接受后才同步为 canonical `问题X求解.py`；
3. 代码身份必须由内部 `question_id + stage + candidate/version fingerprint + input/output contract` 共同确认，不能只靠物理文件名；
4. 用户为了本地管理把脚本改成较短文件名时，除非官方外部协议明确要求固定文件名，否则不得仅因 `Path(__file__).name` 不等于某个期望字符串而直接 `RuntimeError`；
5. 启动时建议打印一行简短 identity banner，至少包含 question/stage/version 与解析到的数据源/输出路径，便于用户返回日志时确认运行的是哪一版；
6. 旧 candidate 在冻结后移出 active 目录或归档，不和 canonical 混在一起作为正式交付。

## 数据事实源分流

正式生成主求解代码前必须按 `preprocessing_decision` 选择唯一数据入口：

### `not_needed`

- 不生成、不要求 `数据预处理/`；
- `问题X求解.py` 允许直接读取题目原始附件；
- 仍必须保留字段、维度、单位、NaN/Inf、主键、索引等非破坏性检查；
- 不得为了形式完整而额外插值、滤波、平滑、标准化或删除异常候选。

### `question_local`

- 不生成全局 `数据预处理/`；
- 主求解允许读取原始附件；
- 仅允许执行本问数学层已经定义的局部变换，例如对数、标准化、滞后、滑动窗口或专属派生特征；
- 局部变换不得静默升级为其他小问必须复用的“统一清洗”。

### `project_level`

必须先完成项目级统一数据预处理：

- 当前模型已通过 Model Challenge 与 Human Approval；
- `数据预处理/数据预处理.py` 已生成并静态检查；
- 用户已本地 full-fidelity 运行；
- `数据预处理/数据预处理结果.xlsx` 的 `预处理质量门` 已通过；
- 本问数据依赖已统一指向该工作簿；
- 本问主求解脚本不得再次直接读取对应共享原始 CSV/XLSX/TXT 等数据源。

只有 `project_level` 状态下，上述统一工作簿是硬前置。`not_needed` 或 `question_local` 项目不得因缺少统一预处理工作簿而阻塞主求解。

任何一项真正适用的前置条件不满足，都不得生成正式主求解代码。尤其禁止出现“模型尚未闭环，先写 Python 看结果再决定题意”，也禁止在 `project_level` 已冻结后各问重新自行清洗。

```text
题意口径冻结
→ 非破坏性数据审计 + 模型路线/输入需求比较
→ preprocessing_decision
→ 题面—数学—代码语义闭环
→ 复杂度合理性复审
→ Independent Model Challenge
→ Human Model Approval（绑定 current semantic revision/hash）
→ semantic governance gate
→ model approval gate
→ project_path_contract（真实项目树绑定）
→ 按 preprocessing_decision 分流
   ├─ not_needed     → 原始数据
   ├─ question_local → 原始数据 + 本问局部变换
   └─ project_level  → Module 03P → 统一工作簿质量门
→ 生成唯一candidate主求解脚本
→ validate_code_delivery.py：执行配置 + 代码工程质量门 + artifact identity
→ 用户本地full_fidelity运行
→ candidate对应主结果工作簿
→ validate_user_execution.py验收运行配置、哈希与主结果质量门
→ post_execution_review：范围/单位/约束/跨组一致性/机制与边界合理性
→ 用户接受后冻结canonical问题X求解.py与主工作簿
→ passed 后才允许进入结果深化、Figure Evidence 或 question_closure_gate
```

脚本必须保留与当前数据事实源对应的读取与字段检查、模型与求解器、目标/约束或题型核心检查、停止条件、约束/残差/收敛或外样本证据、结果整理、中文工作簿输出和主入口。代码规模、函数规模、参数数量、复杂度、身份绑定与反模式以 `core/code_quality_contract.yaml` 为唯一事实源。

代码实现必须服从 Module 02 的三层语义闭环：核心 Python 变量、函数、目标项、约束、阈值、预处理和输出都必须能够回溯到当前数学层；不得在代码阶段静默新增模型语义。

- `project_level`：不得重复项目级去缺失、异常处理、单位换算、统一滤波、统一重采样或坐标修正；
- `question_local`：只允许当前小问有数学来源的局部变换；
- `not_needed`：默认保持原始数据，不为“规范化流程”虚构处理步骤。

若实现过程中发现必须新增核心变量、修改目标函数/约束、改变 `preprocessing_decision`、公共数据处理或算法语义，应停止代码交付，递增 `semantic_revision`，更新 `semantic_change_categories`，把旧 `model_challenge_status`、`human_model_approval_status` 和 `locked_model_spec` 标记 stale，必要时回退 Module 03P 或 Module 02，重新闭环、重新 Challenge、重新取得用户 Approval，并再次运行两个治理门。

完整运行配置嵌入 `FULL_FIDELITY_CONFIG` 并写入主工作簿，不生成独立 YAML、运行说明或校验报告。主工作簿 accepted 后不得为了结果深化分析覆盖更新 `问题X求解.py`；深化分析进入 Module 03B，并生成独立 `问题X结果深化分析.py`。若后续发现主模型必须修改，应显式回退 Module 02/本模块，先传播 stale，再重新审查、批准并验收主结果。

## 用户返回结果后的强制停点

`validate_user_execution.py` 通过只表示工作簿执行与质量门结构闭合，不自动等价于“结果在本题语境中合理”。用户返回运行输出后，助手必须按 `workflow_convergence_contract.post_execution_review` 给出 `passed / review_required / redo_required`。在该状态未明确前，不得直接以“下一步是下一问”为由跨问推进。

审查优化/枚举结果时还必须显式检查最优集合语义：若存在精确并列、声明容差内并列或非常小但非零的目标 gap，应分别报告 `exact tie / tolerance tie / small nonzero gap`，不得把并列最优任意压成“唯一最优”。若稳健性结论依赖方案切换，应在后续深化分析中优先量化切换边界、目标间隙或稳定区域。

## 运行错误恢复

出现路径、文件、工作表、字段或版本错误时，禁止“只改一个字符串再继续猜”。先完成最小 root-cause diagnosis：

1. 当前实际运行的脚本 identity/version；
2. 实际项目目录与实际读取到/未读取到的文件；
3. 上游工作簿真实 sheet/header；
4. 预期接口来自哪个已验收 artifact；
5. 是路径问题、接口漂移、版本串档还是模型语义变化。

只有定位后才生成新的 candidate。若根因不改变数学模型，只修实现；若发现上游事实源或模型语义错误，再按 stale/approval 规则回退。
