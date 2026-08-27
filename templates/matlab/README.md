# HSK MATLAB 科研绘图模板（高级融合实现层）

MATLAB 只读取 Python 两阶段输出的 accepted 标准工作簿，不重新求解。每问 accepted 后唯一 active 入口为：

```text
问题X求解/qX_plot.m
```

provisional 交付使用：

```text
qX_plot_vNN_<short-note>.m
```

不得覆盖上一版；禁止 `q1_polt.m`、`final_plot_new.m` 等并行 active 入口。

---

# 0. 上位规则

MATLAB 实现前必须已经通过：

```text
modules/04_figure_evidence.md
→ figure_suite_manifest.md（若图>=2）
→ result_figure_contract.md
→ top_tier_scientific_figure_skill.md
→ journal_figure_mastery_v2.md
→ figure_iteration_control.md
→ chart_selection.md
→ real-data prototype / render review
→ anti_ai_figure_gate.md
→ release candidate gate
```

MATLAB **不是重新设计 Figure 的地方**，只负责忠实翻译 approved prototype。

---

# 1. 数据源与路径

```matlab
scriptPath = string(mfilename("fullpath"));
resultDir = string(fileparts(scriptPath));
solutionBook = fullfile(resultDir, "问题一求解结果.xlsx");
analysisBook = fullfile(resultDir, "问题一结果深化分析.xlsx");
```

主结果读 `solutionBook`；参数、阈值、结构、稳定性、场景等读 `analysisBook`。

硬规则：
- 不跨问题读取临时 Excel；
- 不从聊天摘要反推序列；
- 不在 MATLAB 中重新求解；
- 不写 Excel；
- 不进行未经 accepted contract 允许的插值/平滑；
- 中文表头使用精确唯一匹配 helper，不使用中文点索引。

---

# 2. Style Parameter Block（单一视觉参数源）

吸收 publication plotting skill 的“参数集中管理”思想，但不照搬其固定 Times/字号/viridis-only。

每个 `qX_plot_vNN_*.m` 顶部应集中定义：

```matlab
FONT = selectFont();
AXFS = 18;
PANELFS = 20;
TITLEFS = 22;      % review mode；journal mode可无整体title
LEGFS = 15;
DATAFS = 15;
LW = 1.4;

P = paperPalette();
```

同一视觉角色的 size / linewidth / color 不应散落成大量重复 numeric literals。

---

# 3. 两种尺寸概念

## A. MATLAB Review Profile

用于用户直接看图窗 / 截图：

```text
axes/ticks/axis label ≈ 16–18
legend                 ≈ 14–16
panel label/subtitle   ≈ 18–22
line width             ≈ 1.2–1.6
```

不能为了“顶刊感”直接把字号压成 Nature production 5–7 pt。

## B. Final Paper Profile

Figure accepted 后才做：
- 实际单栏 / 双栏宽度；
- Word/LaTeX/PDF 页面缩放；
- vector export；
- editable text；
- thumbnail test。

缩小失败时优先：

```text
删冗余
→ 调 panel ratio
→ 增 figure 占版
→ 简化 legend/annotation
→ 最后才缩字体
```

---

# 4. Figure Suite / Paper-family Hook

若一个问题/全文有多张 Figure，MATLAB 必须读取已经冻结的：

```text
paper_family_anchor
visual grammar registry
color role contract
```

后续脚本优先继承：
- font；
- axes weight；
- primary/risk/context 颜色职责；
- marker scale；
- annotation density；
- panel gap；
- whitespace rhythm。

继承视觉家族，不机械复制图型。

---

# 5. Salience–Relevance Implementation

每个 axes 的 approved contract 中已经指定：

```text
Most relevant object
Most salient object
```

MATLAB 实现必须保证二者一致。

默认显著性层级：

```text
primary = filled / stronger line / one accent
secondary = open / thinner
context = gray / small / thin
threshold = rule / boundary
```

禁止叠加：
- 超大 marker；
- 鲜艳色；
- 粗线；
- 彩色粗体文字；
- 大面积背景；

来同时强调同一对象。

---

# 6. Journal Geometry

正式 figure geometry 必须来自 approved prototype。

规则：
- panel 不机械等宽；
- data body 优先于 title / legend；
- `tiledlayout(...,'TileSpacing','compact','Padding','compact')` 只是起点；
- hero/witness 可用 tile span / Position 实现非等权布局；
- axis span 贴近 evidence domain；
- whitespace 必须有结构职责；
- common axis / legend 能共享就共享。

禁止：
- 大标题 + 小主体；
- equal 2×2 作为默认高级布局；
- legend 在外部把主体压成半幅；
- 为“呼吸感”留大面积空区。

---

# 7. Axis / Tick / Grid

默认：

```matlab
set(ax,'TickDir','out','Box','off','Layer','top');
grid(ax,'off');
```

但不是机械禁网格：只有精确读数任务需要时，允许极轻 major grid；minor grid 默认关闭。

必须：
- axis lines/ticks 可见；
- unit 在 axis label；
- log axis 明确；
- bar 从0起；非0基线比较改用 dot / interval；
- dual axis 默认禁止，除非 approved contract 明确物理耦合与必要性。

---

# 8. Labels / Callouts

优先：
- refactor common text；
- 单位放 axis；
- direct label；
- shared compact legend；
- black/dark-gray text + marker/keyline。

Nature-style 默认避免大段彩色文字。

Callout：
- 不交叉；
- 不穿过主数据；
- leader 风格一致；
- 角度/长度尽量一致；
- 每 axes 通常 1–4 个不可替代 annotation。

---

# 9. Color

## Discrete semantic roles

```text
Primary
Risk/Failure
Baseline/Reference
Secondary(optional)
Context
```

先定角色，再定 Hex。

## Continuous

先判断：
- sequential；
- diverging；
- cyclic。

使用 perceptually uniform map；禁止 jet/rainbow/HSV。

不默认 quantile recoloring；只有 Primary question 就是“分位等级”才允许。

---

# 10. Invariant Subtraction

若 approved contract 指出：

```text
Total = invariant + residual
```

MATLAB 主体优先画 residual/delta；invariant 仅作为 reference/metadata/caption。

固定大分量禁止成为最大彩色块。

---

# 11. Complexity Decomposition

若 approved prototype 使用：
- small multiples；
- overview + zoom；
- hero + witness；
- progressive crop；

MATLAB 不得为了代码方便重新合并为 giant overview。

Local Zoom 必须保留 ROI 对应关系，且新增真实信息，不是装饰。

---

# 12. Uncertainty Semantics

MATLAB 只实现 Figure Contract 指定的 uncertainty 类型：

```text
statistical
scenario
parametric
robust-feasible
numerical
forecast
none
```

禁止：
- deterministic optimization 自造 CI；
- scenario range 标成 CI；
- numerical residual 画成统计 error bar；
- 离散参数点画 continuous band。

---

# 13. Dense Scatter / Large-N / Maps

大 N 数据：
- 避免数十万 vector marker；
- 允许 alpha / bin / density / rasterized data layer；
- labels / axes 保持 vector；
- 不能因为性能而隐藏数据结构。

地图：边界只保留 claim 所需分辨率。

---

# 14. Titles / Caption

## Review mode
允许简洁中文 title，但不与 panel subtitle / caption 重复。

## Journal mode
优先：
- 图内无大标题；
- panel `a/b/c` + 短 subtitle；
- 正式 Figure title 与结论放 caption。

优先级：

```text
删重复title
→ 缩短title
→ 移入caption
→ 调canvas
→ 最后才缩字
```

---

# 15. MATLAB Preflight

## Semantic
- workbook exists；
- Sheet exists；
- Required headers unique；
- units / ratio correct；
- no solver；
- no Excel write；
- assert 只来自当前 accepted contract，不使用 stale assumption。

## Lexical
扫描：
- invisible Unicode；
- NBSP；
- smart quote；
- smart dash 进入运算符位置；
- 中文点索引；
- 函数/变量冲突；
- 旧版本错误复制。

## Visual source
MATLAB 只翻译 approved prototype，不在代码阶段重新设计。

---

# 16. Screenshot Fidelity Review

本地 MATLAB 截图回来后，状态进入：

```text
SCREENSHOT_REVIEW
```

只修：
- font extent；
- axes Position；
- tick density；
- legend footprint；
- label collision；
- renderer spacing；
- canvas ratio。

未显式 REOPEN 不换 visual grammar。

---

# 17. Release / Freeze

用户明确“通过 / 确定 / 保留”后：
- 生成 canonical `qX_plot.m`；
- 记录 accepted source version；
- commit/hash；
- frozen Figure IDs；
- paper-family anchor；
- Figure Suite Manifest 状态。

之后如需换 grammar / evidence role，必须显式：

```text
REOPEN reason = ...
```

---

# 18. 最终 Figure QA

MATLAB delivery 前后统一执行：

```text
templates/figure/result_figure_qa.md
```

特别检查：
- Suite coherence；
- Salience relevance；
- Invariant subtraction；
- Grayscale/CVD；
- Thumbnail；
- Mechanical floor；
- Judgment Pass 2.0；
- Final-width embedded-paper。

代码写完不是 Figure 完成。