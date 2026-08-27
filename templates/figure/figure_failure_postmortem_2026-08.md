# 科研绘图长期复盘：为什么曾经需要反复修改 20+ 版

> 目的：把本项目 Q1–Q3 的真实绘图返工原因固化成可执行经验，避免后续继续靠用户逐版指出同类问题。  
> 边界：本文件不是新的 Figure 决策权威；正式流程仍以 `modules/04_figure_evidence.md` 与 `top_tier_scientific_figure_skill.md` 为准。本文件只保存“历史上哪里反复做错、以后如何禁止重犯”。

---

## 1. 核心结论

过去绘图反复修改，并不是因为“配色还差一点”或“MATLAB 不够漂亮”，而是因为曾多次把 Figure 当成**图表美化任务**，没有稳定地把它当成**科学论证 + 版式工程 + 可复现实现**。

最典型的错误链是：

```text
先写图
→ 发现不好看
→ 换配色
→ 调字体/图例
→ 再换图型
→ 再加 panel
→ 用户指出仍然松散/AI感/没学到参考图精髓
→ 继续 vN
```

正确链必须是：

```text
Scope lock
→ Dataset + Claim
→ Primary question
→ Reference reverse engineering
→ >=3 visual grammars
→ Candidate scoring
→ Paper-family anchor
→ Real-data prototype
→ Self render-review
→ User architecture review
→ MATLAB translation
→ Screenshot fidelity review
→ accepted/frozen
```

---

## 2. 长上下文中的主要失败类型

### F01 — 修改作用域漂移

历史表现：
- 用户明确“只改前两张，不改最优物流结构图”，仍出现改错对象或把已接受 Figure 一起动掉；
- 用户明确“主要改主体区，不是图例”，却把主要精力继续放到 legend；
- 用户要求“在这个版本基础上只紧凑一点”，却发生主体结构重写。

根因：没有在每轮开始前冻结 `modify_scope / preserve_scope / frozen_scope`。

以后：每次动图前必须显式记录：

```text
modify = [figure/panel IDs]
preserve = [不可改数据语义、布局、颜色职责等]
frozen = [绝对不可动的 Figure/panel]
```

---

### F02 — 只模仿参考图表面，没有拆视觉语法

历史表现：
- 用户给 Nature 风格哑铃图后，曾只学到“小方块 + 两端点 + 青色/橙色”，没有学到它真正的 `左侧 metadata strip + 右侧 aligned quantitative comparison + 高行密度 + 极低 legend tax`；
- 用户指出“不是图例，是主体这部分”，说明 reference reverse engineering 错位；
- 参考图的紧凑行距、主体占版、对齐关系没有被当成第一优先级。

以后：任何参考图必须先写：

```text
Must imitate  = body geometry / density / alignment / visual grammar / hierarchy
Must preserve = 本题 accepted data / 中文语义 / 单位 / 阈值
Do not copy   = 原图对象名 / 原图数值 / 固定色号 / 无关 panel
```

禁止直接进入 MATLAB。

---

### F03 — 图型选择“会画什么就画什么”

历史表现：
- bar / line / dumbbell / waterfall / heatmap 在多轮中反复循环；
- 有时为了显得高级，增加 ternary / Sankey / 多 panel，但并未降低阅读成本；
- Q2 曾出现一张 Figure 塞太多子图，像 dashboard；
- Q3 F1 用 4 个点撑一整张二维散点，data-ink 过低；
- Q3 F2 重复画固定 75% 普通网络，让不变量占据最大视觉面积。

以后：图型必须由 `Primary question + data structure + perceptual task` 决定；同一问题中若重复使用同一视觉语法，必须说明为什么这种重复不可替代。高级图型只有在**更快读、更诚实、更高信息密度**时才准入。

---

### F04 — 多 panel 机械拼接，缺少 hero/witness 层级

历史表现：
- 1×2 / 2×2 默认等宽；
- 信息很少的 panel 和核心证据占相同面积；
- 标题、脚注、legend 与 data body 争抢版心；
- 用户多次评价“布局松散”“结构更松散”“一张图放那么多图很乱”。

根因：把“结果数量”误当成“panel 数量”。

以后：先做 Drop test；一个 Figure 必须有明确 hero。Supporting panel 若删掉不影响 headline，直接删除/附录化。

---

### F05 — 配色没有 paper-level single source of truth

历史表现：
- 亮蓝、亮红、亮橙、绿色在不同 Figure 中角色漂移；
- 颜色像 AI 信息图 / BI dashboard；
- 为“去 AI 味”临时调低饱和度，但主体结构仍然失败；
- 没有优先继承已经被用户认可的 Figure 风格。

以后：颜色只能在 `Primary / Risk / Baseline-Context / Secondary(optional)` 四类角色中选择；一旦出现 `paper_family_anchor`，后续 Figure 先继承 anchor，再谈新 palette。结构失败时禁止先换色。

---

### F06 — 字体、留白和“顶刊感”理解错误

历史表现：
- 曾把“顶刊”误解成小字体、细线、大留白；
- 用户明确反馈“字体很小、布局很松散，完全不像顶刊”；
- 有时又反向把所有文字加粗，层级消失。

以后：MATLAB Review Profile 与 Final Paper Profile 分离。审图阶段中文必须可读；最终嵌入论文后再做缩放检查。Negative space 必须有结构职责，否则就是浪费。

---

### F07 — Legend / annotation 搜索成本过高

历史表现：
- legend 位置多轮仍未排好；
- label 碰撞、遮挡、数字叠加；
- `sgtitle + panel title + 注释 + 脚注` 重复同一结论；
- 每个点都贴值，变成数字海报。

以后：优先 direct label；每个 axes 默认只保留不可替代的关键标注。标题是最低优先级版面元素之一，不能压缩 data body。

---

### F08 — 没有真正执行“代码前自审”，过早把半成品交给用户

历史表现：
- 多次直接给 `.m`，再让用户承担第一轮视觉 QA；
- 声称“最终版”后，实际截图仍然存在遮挡、松散、AI感；
- 同一图型连续 vN，但没有在第 2/3 次失败时停下来重新诊断。

以后：用户不应该充当第一层 linter。正式给用户的 release candidate 前，必须完成至少：
1. body geometry self-review；
2. hierarchy/label/color self-review；
3. anti-AI gate；
4. grayscale sanity；
5. static MATLAB preflight。

内部草稿不计入用户看到的版本号。

---

### F09 — 文件命名、版本与冻结管理不稳定

历史表现：
- 用户多次要求“新给我的要重新命名”，仍出现旧文件名/旧内容；
- 曾出现给出的文件并非修改后的版本；
- accepted 版本没有立即 canonicalize，导致后续继续误改。

以后：
- 每次**对用户交付**必须是新唯一文件名；禁止覆盖上一版交付物；
- provisional：`qX_plot_vNN_<short-note>.m`；
- 用户明确“确定/通过/冻结”后，才生成 canonical `qX_plot.m` + SHA-256；
- frozen Figure 不得静默改 chart grammar。

---

### F10 — MATLAB 预检不足

历史表现：
- 出现不支持/不可见字符导致 MATLAB 报“文本字符无效”；
- 出现过强、过时的 hard-coded assert，使已接受数据被脚本错误拒绝；
- 项目结构/工作簿/返回值等假设未重新读取就写代码；
- 代码正确性与视觉正确性混在一起验证。

以后：MATLAB 交付前必须分两层：

```text
Semantic preflight:
workbook / sheet / headers / units / accepted semantics / no re-solve

Lexical & implementation preflight:
UTF-8 / no invisible characters / no smart operator symbols / no stale hard-coded asserts / unique file name
```

assert 只验证当前 accepted contract；不得把旧版本结论写成永久真理。

---

### F11 — 把 AI 生成图当作正式科研图 prototype

历史表现：
- 文生图原型天然引入 pastel、卡片、信息图式层级；
- 真实数据 geometry 受不到严格控制；
- 结果“看起来像 AI”，反而偏离用户目标。

以后：正式 data Figure prototype 只允许真实 accepted data + 可复现绘图库。AI 生成图不得作为 MATLAB 实现基准。

---

### F12 — 没有利用“已经成功的图”作为论文家族锚点

历史表现：
- Q3 中用户已明确指出 R2 二维稳健性图“有点期刊论文的味道”，但其它 Figure 仍各自重新设计；
- 风格没有沿着成功样本收敛。

以后：一旦用户认可某 Figure，立即登记 `paper_family_anchor`。后续优先复用其：字体、stroke、marker scale、annotation density、panel gap、颜色职责、whitespace rhythm。

---

## 3. 根因归纳

所有返工基本可归并为 5 个根因：

1. **Evidence failure**：没有先确定 Figure 要证明什么；
2. **Grammar failure**：图型与 perceptual task 不匹配；
3. **Geometry failure**：主体占版、panel ratio、空白、标题/legend 失控；
4. **Workflow failure**：没有先内部 render-review，用户承担第一轮 QA；
5. **State/version failure**：作用域、frozen、文件名、canonical artifact 管理不严。

颜色通常只是第 6 层问题，而不是根因。

---

## 4. 后续最低执行标准

任何结果图在交给用户前必须能回答：

```text
1. 本轮到底允许改哪些 Figure/panel？
2. 这张图的一句话 claim 是什么？
3. 为什么最终图型比另外两个候选更合适？
4. reference figure 的精髓具体学了哪 3–5 个 geometry/hierarchy 特征？
5. hero data object 是什么？
6. 哪些不变量被主动剥离/降权？
7. 是否已经自看过真实 render，而不是只看代码？
8. 是否通过 anti-AI + grayscale + clipping/overlap 检查？
9. 这次交付是否为新唯一文件名？
10. 哪些 Figure 已 frozen，是否保证不动？
```

任一答不上来，不得称为 release candidate。
