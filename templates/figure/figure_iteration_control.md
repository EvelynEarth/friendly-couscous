# Figure Iteration Control（绘图迭代控制硬门）

> 目的：把“用户至少改 20 版”的历史问题转化为状态机与发布门。  
> 适用：所有 `qX_plot.m`、`data_process.m`、结果 Figure、参考图仿写与论文 Figure 精修。  
> 若本文件与 `modules/04_figure_evidence.md` 冲突，以 Module 04 为准。

---

## 0. 核心原则

```text
用户不是第一层 linter。
代码能运行不是 Figure 完成。
每次新版本必须解决一个已诊断的问题，而不是随机继续 vN。
```

正式对用户交付之前，必须先在内部完成：

```text
scope lock
→ source lock
→ claim lock
→ chart grammar decision
→ reference reverse engineering
→ real-data render
→ self-review
→ release gate
```

---

## 1. State Machine

每张 Figure 只能处于下列一种状态：

```text
DRAFT
→ ARCHITECTURE_CANDIDATES
→ PROTOTYPE_REVIEW
→ ARCHITECTURE_APPROVED
→ MATLAB_IMPLEMENTED
→ SCREENSHOT_REVIEW
→ ACCEPTED
→ FROZEN
```

### DRAFT
仅确定事实源、claim、作用域，不写正式 MATLAB。

### ARCHITECTURE_CANDIDATES
至少 3 个不同视觉语法候选，完成 scoring + rejected reason。

### PROTOTYPE_REVIEW
使用真实 accepted data 生成可复现 prototype，并完成 self-review。

### ARCHITECTURE_APPROVED
图型、panel 职责、hero/witness、paper-family style 已冻结；MATLAB 只能翻译。

### MATLAB_IMPLEMENTED
完成 `.m`，但**不得称 final**。

### SCREENSHOT_REVIEW
用户本地 MATLAB renderer 截图回传后，只做 fidelity 修正。

### ACCEPTED
用户明确说“确定/通过/保留/就这个版本”。

### FROZEN
生成 canonical artifact + hash；后续不得静默改动。

---

## 2. Scope Lock（每轮必填）

每次开始修改前记录：

```yaml
iteration_mode: beautify | redesign | fidelity_fix
modify:
  - Figure / panel IDs
preserve:
  - data values
  - semantics
  - accepted conclusions
  - explicitly preserved geometry/style
frozen:
  - Figure / panel IDs
user_reference_focus:
  - body | legend | color | typography | layout | specific panel
```

### Beautify
只改视觉层：font / color / marker / line / margin / legend / annotation。除非用户明确允许，不改变已接受图型与证据职责。

### Redesign
允许换 visual grammar，但必须重新过 Candidate + Prototype Gate。

### Fidelity fix
只修 MATLAB renderer 与 approved prototype 的差异，禁止再换图型。

---

## 3. Source Lock / “美化不修改”

### 永远禁止
- 修改 accepted 数值；
- 改类别含义；
- 为好看删掉不利结果；
- 从聊天摘要反推底层序列；
- MATLAB 重求解；
- 擅自插值/平滑制造新拐点；
- 用 reference figure 的数值替换项目数据。

### Axis range
- `beautify`：默认保持已接受 axis semantics/range；
- `redesign`：可以为提高信息效率调整 axis，但必须诚实、保留阈值/基准上下文，不能截轴夸大结论。

---

## 4. Reference Figure Reverse Engineering Card

用户给参考图时，**禁止直接写代码**。先完成：

```yaml
body_bbox_ratio: ...
row_or_panel_density: ...
panel_ratio: ...
gap_logic: ...
axis_domain_logic: ...
tick_density: ...
typography_hierarchy: ...
primary_encoding: position | length | area | color | connection
metadata_structure: ...
legend_strategy: ...
annotation_budget: ...
color_roles: ...
reading_order: ...
caption_duties: ...
```

然后写：

```text
Must imitate   = 3–6 个结构/视觉语法特征
Must preserve  = 项目数据、中文字段、单位、阈值
Do not copy    = 原对象、原数值、无关 panel、固定色号
```

用户如果明确说“主要看主体，不是图例”，必须把 `legend_strategy` 降为次要项；不得再次把修改重心放错位置。

---

## 5. Chart Grammar Diversity Gate

### 原则
“高级”不是多用不同图，而是每个证据任务采用最匹配的 visual grammar。

### 同一问题内
若已经用某一种图型回答一个 Primary question，另一张 Figure 只有在**阅读任务相同且该语法确实最优**时才可重复。否则优先探索另一种更合适的 grammar。

### 禁止
- 为了统一而所有图都 dumbbell；
- 为了高级而所有图都复合 panel；
- 为了多样而强行 Sankey/ternary/3D；
- 相同数据换 2–3 种图重复讲同一句话。

必须记录：

```text
Why this grammar here?
Why not the grammar already used elsewhere?
```

---

## 6. Paper-family Anchor Gate

一旦用户指出某张 Figure“有期刊味 / 这张可以 / 保留”，立即登记：

```yaml
paper_family_anchor:
  figure_id: ...
  font_family: ...
  axes_weight: ...
  marker_scale: ...
  primary_role: ...
  risk_role: ...
  context_role: ...
  panel_gap: ...
  annotation_density: ...
  whitespace_rhythm: ...
```

后续 Figure 默认继承，不得每张图重新发明风格。

---

## 7. Internal Prototype Budget

用户看到 release candidate 前，至少内部完成 2 轮：

### Internal v0 — body only
只画主体，不追求最终颜色和图例。

审：
- chart grammar；
- hero；
- body占版；
- panel ratio；
- row density；
- axis waste；
- invariant clutter。

失败 → 换结构，不许靠换色。

### Internal v1 — hierarchy
加入 typography / direct labels / minimal color / annotation。

审：
- 0.5s glance；
- 2s direction test；
- 10s claim test；
- grayscale；
- clipping / overlap；
- anti-AI gate。

内部试验文件不对用户编号，也不污染项目 active entry。

---

## 8. User-facing Iteration Budget

### 第一轮用户拒绝
必须把反馈归类：

```text
grammar | geometry | hierarchy | typography | label/legend | color | implementation | scope
```

只针对根因改，不随机同时改全部层。

### 第二轮仍因同类原因被拒绝
停止继续微调，执行 mismatch diagnosis：
- reference 是否读错？
- Primary question 是否错？
- hero 是否选错？
- chart grammar 是否错？
- paper-family anchor 是否没继承？

### 第三轮仍然“丑/AI感/松散”
**禁止继续 vN。** 必须回到 `ARCHITECTURE_CANDIDATES`，重新选型。

---

## 9. Release Candidate Gate（用户看到前）

只有同时满足才允许发 `.m`：

```text
[ ] Scope lock 与用户本轮要求一致
[ ] Source workbook / sheet / headers 已真实读取
[ ] 至少 3 个候选 visual grammar 已比较
[ ] rejected candidate 已记录
[ ] paper_family_anchor 已继承或说明为何不适用
[ ] real-data prototype 已实际 render 并自看
[ ] body geometry PASS
[ ] anti-AI PASS
[ ] grayscale / CVD sanity PASS
[ ] legend/annotation search cost PASS
[ ] 没有明显 overlap / clipping
[ ] MATLAB lexical preflight PASS
[ ] 新文件名唯一，没有把旧文件冒充新版本
```

未过 gate → 不得称“最终版”“最终代码”。

---

## 10. MATLAB Preflight

### 10.1 Semantic

- 工作簿存在；
- Sheet 名真实存在；
- Required headers 唯一存在；
- 单位和比例口径正确；
- 不调用求解器；
- 不写 Excel；
- 不把旧版本 semantic assert 当永久规则；
- assert 必须来自当前 accepted Figure Contract。

### 10.2 Lexical

交付前扫描：
- 不可见 Unicode；
- NBSP；
- smart quote；
- smart dash 被误作运算符；
- 非法复制字符；
- 中文点索引；
- 同名函数冲突；
- 重复 figure handle/变量覆盖风险。

中文字符串本身可以保留；禁止的是**混入代码语法位置的不可见或不受支持字符**。

### 10.3 Visual implementation

MATLAB 不重新设计 approved prototype。若截图与 prototype 不同，只进入 fidelity fix。

---

## 11. Naming / Versioning Gate

用户历史上明确要求：**新给的文件必须重新命名。**

因此：

### Provisional delivery

```text
qX_plot_vNN_<short-note>.m
```

规则：
- 每次对用户交付的新文件名唯一；
- 不覆盖上一个已交付版本；
- 文件名与内容版本一致；
- 回复中明确指出本轮相对上一版到底变了什么。

### Accepted
用户明确通过后：

```text
qX_plot.m  ← canonical active entry
```

记录：
- accepted source version；
- commit SHA；
- file SHA-256（若本地生成）；
- frozen Figure IDs；
- paper-family anchor。

旧实验文件不再作为 active entry。

---

## 12. Freeze Gate

`FROZEN` 后默认禁止：
- 换图型；
- 换证据职责；
- 改数据源；
- 重新配一套颜色；
- 把 accepted Figure 合并进其它复合图。

需要变化时必须：

```text
REOPEN reason = ...
expected benefit = ...
which frozen constraints are released = ...
```

否则按回归错误处理。

---

## 13. Delivery Note 模板

每次正式给用户 release candidate 时，回复至少包含：

```text
文件名：...
Iteration mode：...
本轮只修改：...
保留不动：...
相对上一版解决：...
未改变的数据/结论：...
当前状态：PROTOTYPE_APPROVED / MATLAB_IMPLEMENTED / SCREENSHOT_REVIEW
下一步只允许：...
```

避免用户再次遇到“你到底改了哪一版 / 文件是不是旧的 / 为什么又动了我没让你动的图”。
