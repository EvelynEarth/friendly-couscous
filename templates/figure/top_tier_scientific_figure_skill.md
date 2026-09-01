# Top-tier Scientific Figure Skill（融合升级版）

本文件是 `modules/04_figure_evidence.md` 的高阶科研绘图执行补充，不建立第二套事实源或第二套 Evidence 权威。

Module 04 负责：
- Evidence level；
- Primary question；
- Source workbook；
- Figure Layout Gate；
- Figure Enhancement Gate；
- Figure Contract；
- 论文证据闭环。

本文件负责把这些约束落到：

```text
整篇 Figure Suite 设计
→ Claim-to-visual-task
→ 多候选 grammar
→ salience / hierarchy / geometry
→ real-data prototype
→ render-review
→ MATLAB translation
→ final-width paper QA
```

高级方法细节继续读取：
- `templates/figure/journal_figure_mastery_v2.md`
- `templates/figure/journal_palette_contract.md`
- `templates/figure/figure_suite_manifest.md`
- `templates/figure/scientific_figure_skill_landscape.md`
- `templates/figure/journal_figure_research_notes.md`
- `templates/figure/journal_figure_case_patterns.md`
- `templates/figure/anti_ai_figure_gate.md`
- `templates/figure/figure_iteration_control.md`

---

# 0. Publication-grade 的定义

```text
顶刊科研图 ≠ Nature配色
顶刊科研图 ≠ 小字体 + 大留白
顶刊科研图 ≠ 高级图型堆砌
顶刊科研图 ≠ dashboard / infographic

顶刊科研图 =
证据深度
+ 视觉任务匹配
+ 显著性与相关性一致
+ 编辑式压缩
+ 数据诚实
+ 整篇图组一致
+ 可复现与最终版面可读
+ 用户指定修改范围得到尊重
```

本项目保留 Icarus Figures 的四轴质量条，并增加三项项目级门：

```text
Depth
Elegance
Unimpeachable
Visible gap
Salience relevance
Suite coherence
Scope fidelity
```

7 项都过，才进入正式 MATLAB delivery。

---

# 1. Figure Suite First：先设计整篇图组，再设计单图

若一个问题有两张以上 Figure，或已经进入 Q1–Qn 全文绘图阶段，必须先填写：

```text
templates/figure/figure_suite_manifest.md
```

每张 Figure 先登记：
- one-sentence claim；
- Evidence level；
- hero evidence；
- visual grammar；
- 为什么该 grammar 在整篇 suite 中不可替代；
- paper-family anchor；
- 正文位置。

### Suite-level FAIL

以下任一直接触发重新架构：
- 两张图回答同一句话；
- 同一批数据只是换图型重复展示；
- 全篇几乎都是同一种 dumbbell / bar / heatmap，但没有阅读任务上的必要；
- 每张图各自重新配一套颜色和字体；
- L3/L4 图比 L1 hero 更抢眼。

同一 grammar 可以重复，但必须说明为什么该 perceptual task 相同、为什么它仍是最优选择。

---

# 2. 唯一入口：Dataset + Claim + Skeptical Reviewer Question

正式绘图前，每张 Figure 必须写：

```text
Core conclusion
Evidence level
Primary question
Audience / paper role
Source workbook + sheet + headers
Hero evidence
Required comparison / threshold
What a skeptical reviewer would ask
```

然后把 claim 翻译为视觉任务，而不是直接选 chart：

```text
claim
→ reader task
→ visual encoding
→ chart grammar
```

例如：
- “哪个方案更优” → 精确比较 → aligned position / length；
- “什么时候失效” → 找 boundary → regime / threshold；
- “哪个场景贡献最大” → 排序贡献 → sorted forest / contribution；
- “机制为什么发生” → 追踪状态/约束/流 → staged flow / mechanism object。

---

# 3. Graphical Perception Gate

优先视觉通道：

```text
aligned position
> non-aligned position
> length
> slope/direction
> angle
> area
> volume
> hue/saturation
```

因此：
- 精确比较优先 dot / interval / forest；
- 不用 pie / bubble 做精确排序；
- color 不承担主要定量比较；
- composition 只有在 composition 本身是一级问题时使用；
- 2D scatter 只有二维关系本身就是 claim 时才值得占据整张坐标系。

---

# 4. Candidate Grammar Gate（至少 3 类）

`redesign` 模式下，每个 Primary question 至少比较 3 个**不同 visual grammar**。

注意：若用户当前 feedback 的 mutation scope 已锁为 `palette_only / rendering_only / annotation_only`，则**不重新开启 grammar 候选搜索**，除非用户明确批准 redesign。

Candidate scoring：0–2 分。

| 维度 | 0 | 1 | 2 |
|---|---|---|---|
| Answerability | 看不出 | 需要解释 | 一眼回答 |
| Perceptual precision | 低 | 中 | 高 |
| Information density | 大量空白/重复 | 中 | 高密度但不拥挤 |
| Mechanism depth | 只展示结果 | 部分解释 | 阈值/原因/边界可见 |
| Salience relevance | 焦点错位 | 部分一致 | 第一眼就是关键证据 |
| Data honesty | 有伪连续/隐藏例外 | 有风险 | 直接对应 accepted data |
| Caption burden | 不看caption不懂 | 中 | caption只补口径 |
| Journal fit | PPT/dashboard | 一般 | 正文级 |
| Suite coherence | 与全文冲突 | 中性 | 强化paper family |

必须记录至少一个 rejected candidate 及原因。

### 直接淘汰

- 需要伪造连续性；
- 高级图型比基础图更慢读；
- 图例/标题比数据主体更醒目；
- supporting panel 与 hero 机械等权；
- 主要空间被不变量占据；
- 只有“换个色板”才能解释为什么高级；
- 缩小后依赖小字才能理解。

---

# 5. Claim-to-Grammar 高级索引

## 5.1 阈值 / 稳健性 / 参数空间

优先：
- actual-grid regime map；
- threshold slice；
- phase/decision region（仅有连续证据时）；
- sensitivity small multiples；
- transition forest。

禁止 sparse grid 假装 continuous phase boundary。

## 5.2 机制 / 流量 /资源响应

优先：
- real network / flow；
- staged flow；
- state strip；
- timeline + glyph；
- mechanism object；
- Sankey / alluvial（仅真实守恒流）。

若某一大分量固定不变，先执行 Invariant Subtraction Gate。

## 5.3 方案比较 / 公平性 / 替代最优

优先：
- metadata strip + aligned quantitative panels；
- forest / lollipop；
- slope / dumbbell；
- rank transition；
- parallel coordinates（维度多且语义统一才使用）。

没有变化的对象降权或正文汇总。

## 5.4 成本 / 收益 /分解

优先：
- signed contribution；
- value bridge / waterfall（严格闭合才用）；
- baseline-to-optimum slope；
- cost-benefit / risk-service trade-off；
- Pareto（真实多目标）。

若一级问题是“为什么选这个方案”，先比较候选，不要先画成本分解。

## 5.5 分布 / 不确定性 /模型合法性

优先：
- raw points；
- ECDF；
- violin / raincloud / box；
- interval；
- residual；
- calibration；
- enumeration gap / feasibility certificate。

统计样本不要再用 bar of means 隐藏分布。

---

# 6. Uncertainty Semantics Gate

必须区分：

```text
Statistical
Scenario
Parametric
Robust/Feasible
Numerical
Forecast
```

合法表达见 `journal_figure_mastery_v2.md`。

硬规则：
- deterministic optimization 不伪造 CI；
- scenario range 不叫 confidence interval；
- numerical residual 不伪装统计误差；
- 离散参数扫描不画 continuous ribbon；
- error bar 必须明确 SD / SE / CI / range / tolerance 的语义。

---

# 7. Salience–Relevance Gate

每张 Figure 必须明确：

```text
Most relevant object = ?
Most visually salient object = ?
```

二者必须一致。

每个 axes 默认只有：
- 1 个 primary salient object；
- 最多 1 个 secondary witness；
- 其它 context 降权。

### 禁止 relevance inversion

- context 背景比 hero 数据更抢眼；
- 大标题比数据更醒目；
- baseline/invariant 占最大彩色面积；
- legend 比数据重要；
- 多个高饱和对象互相竞争。

---

# 8. Hero / Witness / Drop Test

多 panel Figure 必须指定：

```text
hero_panel: one
witness_panels: zero or more
```

通常 hero 应获得约 55–75% 的视觉权重，不是机械面积。

Drop test：
- 删 witness 不影响 headline → 删除/附录；
- 删 hero headline 仍成立 → hero 选错；
- 所有 panel 同权 → 默认重新设计。

---

# 9. Invariant Subtraction Gate

如果：

```text
Total = invariant baseline + informative residual
```

则优先画 residual / delta。

不变量只作为：
- 极轻 reference；
- 一句黑色文字；
- metadata；
- caption。

禁止让固定 70–80% 的 baseline 成为最大彩色块，而真正变化只有 20–30%。

---

# 10. Complexity Decomposition Gate

当出现：
- >4 条纠缠曲线；
- 多对象尺度相差 5–10 倍；
- >3 类视觉编码；
- legend ping-pong；
- ROI 被全局尺度压平；

优先考虑：
- small multiples；
- overview + justified zoom；
- hero + witness column；
- progressive cropping；
- direct label；
- context 灰化。

复杂 overview 不是高级，能快速比较才高级。

---

# 11. Journal Geometry Gate

Nature 官方核心：neat + space-efficient，panel 尺寸由内容决定。

空间分配优先级：

```text
data body
> axis labels
> critical annotation
> panel labels
> legend
> title
```

规则：
- panel 不机械等宽；
- axis span 贴近证据域；
- whitespace 必须有结构职责；
- equal 2×2 / 1×3 是高风险，不是高级默认；
- title / legend 逼缩主体时优先删除或移入 caption。

---

# 12. Axis / Tick / Grid Gate

导航元素必须可读但不抢数据：
- axis 与 tick 可见；
- tick outward；
- units 在 axis label；
- major grid 默认关闭，只有精确读数需要时用极轻 major grid；
- minor grid 默认禁止；
- bar chart 以长度编码时从 0 起；非零基线比较改用 dot/interval；
- log axis 明确标示；
- dual axis 默认高风险，只有物理耦合且必要时准入。

---

# 13. Label / Annotation Engineering

标签本身需要对齐、重构和预算。

优先：
- refactor common text；
- 单位集中在 axis；
- direct label；
- 共享 legend；
- leader/keyline + 黑/深灰文字。

Nature-style 默认**不使用大段彩色文字**。

Callout：
- 不交叉；
- 角度/长度尽量统一；
- 不穿过主数据；
- 同一 Figure leader 风格统一。

每个 axes 通常只保留 1–4 个不可替代 annotation。

---

# 14. Symbol Hierarchy

默认：

```text
primary = filled marker + solid/strong line
secondary = open marker + thinner line
context = gray/small/thin
threshold = rule/boundary
```

不要给 5 个系列随机分配 5 个高饱和色。

必须通过 grayscale：marker fill / shape / linestyle 至少有一种冗余编码。

---

# 15. Color System

颜色由 `templates/figure/journal_palette_contract.md` 统一管理。本文件只保留上层原则：

- 先判断 categorical / ordinal / sequential / diverging / cyclic / semantic region；
- 顶刊配色不是固定“Nature蓝”，也不是默认全灰或低饱和；
- 用户要求“顶刊配色”时，必须比较 publisher guideline、journal-inspired palette、scientific colormap 三类来源；
- 大面积 fill、marker、line 的同一 Hex 视觉重量不同，必须 area-aware；
- 防止两个极端：pastel washing 与 over-dark；
- 用户确认“这套颜色还行”后建立 `palette_anchor`；
- `palette_only` 时严禁改 chart grammar / layout / axis / annotation / data；
- continuous/ordinal map 使用 perceptually uniform scientific maps，禁止 jet/rainbow/HSV；
- 不默认 quantile recoloring，除非分位等级本身是 claim。

---

# 16. Typography：Review 与 Final Paper 分离

### MATLAB Review Profile

用户直接在 MATLAB 图窗看：中文必须清楚，不以小字体制造“顶刊感”。当前 HSK baseline 可继续采用 axes≈18、legend≈16、line≈1.4。

### Final Paper Profile

accepted 后按真实论文栏宽做 reduction test：
- single-column / double-column；
- vector export；
- line / marker / label 缩小后仍清楚。

若缩小失败，优先：

```text
删冗余
→ 调 panel ratio
→ 增 figure 占版
→ 简化 legend/annotation
→ 最后才缩字体
```

### Thumbnail test

缩到页面缩略图或约 25–35%：hero 和主趋势仍需可见。

---

# 17. Dense Scatter / Large-N / Maps

大 N：
- 不机械输出数十万 vector glyph；
- alpha / hexbin / density / rasterized data layer；
- labels / axes 保持 vector；
- raw point structure 仍需诚实保留。

地图：只保留 claim 需要的边界分辨率，避免高精行政边界成为视觉噪声。

---

# 18. Mechanism / Framework Figure 分流

Data Figure：accepted data + reproducible plotting only。

Mechanism / Framework：可示意，但不能 generic boxes-and-arrows。必须嵌入真实方法对象，例如：
- decision region；
- network topology；
- real distribution；
- constraint relation；
- before/after pattern；
- optimization state。

“高级机制图”来自真实方法对象，不来自发光、科技蓝和装饰箭头。

具体工具优先级、image generation / Draw.io fallback、短文字、少图标、零交叉和图例规则服从 `mechanism_figure_contract.md`。

---

# 19. Render–Review–Iterate（硬门）

用户不是第一层 linter。

### Internal v0：body-only

先不追求最终配色，检查：
- grammar；
- hero；
- body 占版；
- panel ratio；
- invariant clutter；
- axis waste；
- complexity。

geometry 失败 → redesign，禁止只换色。

### Internal v1：hierarchy

加入：
- typography；
- direct labels；
- palette contract；
- critical annotation。

检查：
- 0.5s glance；
- 2s direction；
- 10s claim；
- grayscale / CVD；
- thumbnail；
- overlap/clipping；
- anti-AI gate。

收到用户反馈后必须先确定 `mutation_scope`。若为 `palette_only`，后续迭代跳过 grammar/geometry redesign，只做 palette benchmark 与代码安全修改。

只有通过才允许 MATLAB translation。

---

# 20. Mechanical Floor + Judgment Pass 2.0

## Mechanical floor

必须无明显 FAIL：
- units；
- source workbook；
- no solver；
- no Excel write；
- no fake interpolation；
- no illegal Unicode；
- no clipping/overlap；
- no rainbow；
- unique provisional filename；
- final vector plan；
- palette-only 修改无结构漂移；
- MATLAB static preflight 无括号/字符串/token 明显错误。

## Judgment Pass 2.0

回答七问：

1. Depth：遮住 caption，机制/阈值/结论还能读出吗？
2. Elegance：Drop test 后还有冗余吗？
3. Unimpeachable：轴、单位、误差语义、颜色、边界诚实吗？
4. Visible gap：0.5 秒像论文正文还是 PPT/dashboard/AI？
5. Salience relevance：第一眼看到的是最重要证据吗？
6. Suite coherence：它和全文 Figure 是一家人，而且不重复吗？
7. Scope fidelity：本轮是否只改了用户授权的内容？

任一明显失败，不交付 `.m`。

---

# 21. Reference Figure Reverse Engineering

用户给参考图时先拆：

```text
body bbox
row/panel density
panel ratio
gap
axis domain
tick density
typography hierarchy
primary encoding
metadata structure
legend strategy
annotation budget
color roles
reading order
caption duty
```

然后写：

```text
Must imitate
Must preserve
Do not copy
```

禁止只学色号、点、图例位置。

若用户给的是“配色参考”，必须区分：
- 颜色本身；
- 颜色面积；
- alpha；
- 背景与文字 contrast；
- primary/context 比例。

同一 Hex 离开原来的面积和背景可能完全不像原图。

---

# 22. 最终执行链

```text
Paper-level Figure Suite
→ Scope / Source / Claim lock
→ Skeptical reviewer question
→ Claim-to-visual-task
→ >=3 grammar candidates (redesign only)
→ Candidate scoring
→ Salience-relevance plan
→ Invariant subtraction
→ Hero / witness / drop test
→ Geometry sketch
→ Real-data prototype v0
→ Render review: body / complexity
→ Prototype v1
→ Palette contract / benchmark
→ Grayscale / CVD / thumbnail
→ Anti-AI gate
→ Mechanical lint
→ Judgment Pass 2.0
→ User architecture review
→ MATLAB translation
→ MATLAB screenshot fidelity review
→ Final-width embedded-paper review
→ accepted / frozen
```

这条链优先于任何“Nature风 / Science风 / Cell风”的表面模仿；用户明确锁定 mutation scope 后，必须在授权范围内迭代。
