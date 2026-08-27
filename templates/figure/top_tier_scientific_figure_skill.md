# Top-tier Scientific Figure Skill

本文件是 `modules/04_figure_evidence.md` 的高阶科研绘图执行补充，不建立第二套 Figure 决策权威。Module 04 仍负责 Evidence level、Primary question、Layout Gate、Enhancement Gate、Source workbook 与 Figure Contract；本文件负责把已批准的 Figure Contract 落到“证据驱动选型 → 真实数据原型 → render-review → MATLAB 实现 → 论文嵌入 QA”。

外部方法论研究底稿：
- `templates/figure/journal_figure_research_notes.md`
- `templates/figure/journal_figure_case_patterns.md`
- `templates/figure/anti_ai_figure_gate.md`

---

## 0. 顶刊科研图的真正质量门槛

### 0.1 核心纠偏

```text
顶刊科研图 ≠ 小字体 + 细线 + 大留白 + 低饱和
顶刊科研图 ≠ “Nature配色” + 卡片式注释 + 高级图型堆砌
顶刊科研图 = 证据深度 + 视觉优雅 + 无可挑剔 + 一眼有期刊差距
```

本项目采用四轴质量条（借鉴 Icarus Figures 的 publication-grade quality bar，并按数学建模场景改写）：

### Axis 1 — Depth（深度）

Figure 不只回答“是什么”，还应尽可能回答“为什么 / 所以怎样”。

可视化优先展示：
- 阈值 / 临界点；
- 失效区 / 推荐区；
- 机制分解；
- 分布形状 / 不确定性；
- 约束为何成为瓶颈；
- 方案结构变化为何发生。

**Caption-cover test**：遮住图注，读者是否仍能从图中复述主要结论？若不能，图只是展示数据，还没有形成证据。

> 数学规划的确定性结果不强行画 CI / N。若没有统计不确定性，应改为展示数值容差、阈值区间、枚举验证、结构边界、scenario range 或 sensitivity evidence；禁止伪造统计信息。

### Axis 2 — Elegance（优雅）

一个 Figure 只服务一个一级结论。多 panel 时必须存在清楚的视觉主次。

**Drop test**：逐个删除 panel；若一级结论几乎不变，则该 panel 应删除或移入附录。

默认：
- 一个 hero panel 承担主要结论；
- supporting panels 缩小为 witness / context；
- equal 2×2 / equal 1×3 不是默认安全布局，而是高风险布局；
- data-ink 最大化，但不是把所有数值写满。

### Axis 3 — Unimpeachable（无可挑剔）

Figure 必须经得起评委/审稿人的反问：
- 轴是否诚实？
- 是否伪造连续性？
- 颜色是否扭曲数值？
- 是否在黑白打印下失效？
- 不确定性 / 数值容差 / scenario range 是否交代清楚？
- 单位、口径、基准是否明确？
- 是否可由脚本 + accepted workbook 重现？

### Axis 4 — Visible gap（第一眼就像论文，而不是作业/PPT/AI信息图）

0.5 秒 glance test：

```text
像期刊正文 Figure  → PASS
像课程作业默认图    → FAIL
像咨询仪表板 / PPT  → FAIL
像 AI 信息图        → FAIL
```

Visible gap 来自：
- panel 比例；
- 对齐；
- 有节制的 typography hierarchy；
- 稳定的颜色职责；
- 数据主体占版；
- 少而有效的 annotation；
- consistent figure family。

不是来自：圆角卡片、渐变背景、发光点、彩色 badges、大色块、装饰性图标或“高级图型”本身。

---

## 1. Figure 的唯一入口：Dataset + Claim

正式绘图前必须填写：

```text
Core conclusion
Evidence level
Primary question
Audience / paper role
Source workbook + sheet + headers
Required comparisons / thresholds
Hero evidence
What a skeptical reviewer would ask
```

然后执行：

```text
Accepted data + one claim
→ Perceptual task
→ Candidate chart pool (>=3 visual grammars)
→ Candidate scoring
→ Journal reference matching (actual published figures, not AI mockups)
→ Geometry sketch
→ Real-data prototype v1
→ Render Review #1: body geometry
→ Redesign if needed
→ Real-data prototype v2
→ Render Review #2: hierarchy / labels / color
→ Mechanical lint / sanity checks
→ MATLAB translation
→ MATLAB screenshot fidelity review
→ Final-width / embedded-paper review
→ accepted / frozen
```

### 禁止 AI 图像作为正式 Figure 原型

正式数据 Figure 的 prototype 必须由 accepted data + 可复现绘图库生成。不得再用文生图工具生成所谓“顶刊风格示意图”作为实现基准，因为它：
- 不可复现；
- 数值和 geometry 不受约束；
- 容易引入 dashboard / infographic 视觉语言；
- 会把“风格感”置于证据结构之前。

参考图只能来自：
- 用户提供的论文 Figure；
- 真实公开论文 Figure；
- 可复现绘图库的示例。

---

## 2. Graphical Perception Gate：优先使用更准确的视觉任务

吸收 Cleveland–McGill / Nature Methods 的 graphical perception 思路：若结论可用高精度视觉通道表达，不降级到低精度通道。

默认优先级：

```text
同一基线位置
> 非同一基线位置
> 长度
> 方向 / 斜率
> 角度
> 面积
> 体积
> 色相 / 饱和度
```

因此：
- 比较精确大小 → dot / interval / aligned lollipop 往往优于 pie / bubble；
- 排名 → position/length 优先；
- 二维参数区域 → position + region；
- 连续强度 → perceptually uniform colormap，颜色不能替代坐标；
- 2 状态变化 → slope / dumbbell，但只有变化对象值得画；
- 组成 → 只有 composition 真的是一级问题时才用 stacked / ternary / alluvial。

---

## 3. Candidate Chart Pool：先展开，再淘汰

每个 Primary question 至少比较 3 个**不同视觉语法**候选，不能只在 bar / line / heatmap / dumbbell / waterfall 中循环，也不能为了高级感强行使用 ternary / Sankey / chord / 3D。

### 3.1 参数空间 / 稳健性 / 阈值

候选：
- phase / regime diagram；
- decision-region map；
- actual-grid tile map；
- overview + threshold slice；
- forest / tornado；
- small-multiple sensitivity strips；
- contour / response surface（仅真实连续响应）；
- transition path。

硬规则：
- sparse grid 不冒充 continuous phase map；
- 没有连续证据不插值；
- 若二维中一维几乎不变，优先 1D slice；
- 如果单张 actual-grid map 已闭合结论，不因“高级”额外增加 threshold panel。

### 3.2 机制 / 流量 / 资源响应

候选：
- Sankey / alluvial；
- staged flow；
- response-state strip；
- network flow；
- timeline + glyph；
- ternary composition trajectory；
- stage composition strips；
- stepwise allocation diagram。

硬规则：
- Sankey/alluvial 只表示真实流或守恒量；
- ternary 只有数据真正占据二维 simplex 才使用；若点近共线、一项近常数或样本太少，直接淘汰；
- 时间长度若不是 primary question，不让最长阶段压缩其它阶段；
- 固定不变的大分量不得占据大部分视觉面积；应剥离成 baseline/context，只画 residual / delta。

### 3.3 方案差异 / 替代最优 / 公平性

候选：
- dumbbell；
- slopegraph；
- paired interval；
- Cleveland dot；
- aligned forest / lollipop；
- metadata strip + quantitative aligned panel；
- rank transition；
- parallel coordinates（变量足够多且语义一致）。

硬规则：
- 没变化对象降权或文字汇总；
- 若对象类别结构与指标比较同时重要，优先 metadata strip + aligned quantitative plot；
- 两状态比较不靠大面积双色块；
- 不为 4 个点撑一整张空旷二维 scatter，除非二维关系本身就是结论。

### 3.4 成本 / 收益 / 目标分解

候选：
- value bridge / waterfall；
- balance ledger；
- signed contribution plot；
- decomposition strip；
- baseline-to-optimum slope；
- cost-benefit interval；
- cost-service / risk-service dominance map；
- Pareto front（仅真实多目标权衡）。

硬规则：
- Waterfall 只在增量严格闭合且“分解本身”就是一级结论时使用；
- 若一级问题是“为什么选这个方案”，比较候选方案通常优先于分解总成本；
- 单数字不单占 Figure。

### 3.5 分布 / 不确定性 / 合法性

候选：
- ECDF；
- raw points + interval；
- box / violin / raincloud / boxen；
- fan / ribbon；
- residual；
- observed-vs-predicted；
- calibration；
- Pareto + violation。

硬规则：
- n 很小时展示真实点；
- 不用 mean bar 隐藏分布；
- 对确定性优化问题不要假装存在抽样分布。

---

## 4. Candidate Scoring Gate（强制）

每个候选按 0–2 分：

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| Answerability | 无法直接回答 | 需大量解释 | 一眼回答 |
| Perceptual precision | 主要靠面积/颜色 | 比较成本中等 | 主要靠位置/长度/对齐 |
| Information density | 空白/重复严重 | 中等 | 高密度但不拥挤 |
| Mechanism depth | 只显示结果 | 有部分机制 | 阈值/边界/原因直接可见 |
| Data honesty | 插值/伪连续/隐去例外 | 有风险 | 直接对应 accepted data |
| Caption burden | 不看图注看不懂 | 中等 | caption 只补口径 |
| Journal fit | PPT/dashboard/AI | 可入文 | 缩小后仍像正文图 |

### 直接淘汰

- 需要伪造连续性；
- 主体超过一半区域为空且无结构意义；
- equal grid 让 supporting panel 与 hero panel 同权；
- legend 比数据主体更显眼；
- 高级图型比基础图型更慢读；
- 只有换配色才能解释为什么“高级”；
- AI 信息图视觉语言明显；
- 缩小后依赖小字才能看懂。

必须记录至少一个 rejected candidate + 原因。

---

## 5. Hero Panel / Drop Test

多 panel Figure 必须指定：

```text
hero_panel: one
witness_panels: zero or more
```

通常 hero panel 应占约 55–75% 的视觉权重（不是机械面积比例）。

Drop test：
- 删除 witness panel，若 headline 基本不变 → 删除；
- 删除 hero panel，若 headline 仍成立 → hero 选错；
- 所有 panel 同权 → 默认失败，除非 Primary question 确实是多项并列比较。

---

## 6. Journal Geometry Gate

Nature Research Figure Guide 的核心不是“留白多”，而是 neat + space-efficient。

### 6.1 主体优先

先给 data body 空间，再给：
1. axis labels；
2. critical annotation；
3. panel labels；
4. legend；
5. title。

若 title / legend 逼缩 data body，优先删 title / direct-label / shared legend。

### 6.2 Panel 比例

panel 不机械等宽。按：
- 数据密度；
- 标签负担；
- 视觉任务；
- hero/witness 关系
分配空间。

`tiledlayout(...,'TileSpacing','compact','Padding','compact')` 只是起点，不是终点。

### 6.3 Axis waste

axis 范围应贴合证据域。超出范围必须有真实理由（阈值、预测区、可行域）。

### 6.4 Negative space

negative space 必须承担：
- 分组；
- 阅读顺序；
- 层级；
- 呼吸。

如果只是“空”，就是浪费。

---

## 7. Typography：Review Profile 与 Final Paper Profile 分离

### 7.1 MATLAB Review Profile（中文）

用于用户直接在 MATLAB 图窗 / 截图审查：
- axes / tick / axis label：16–18；
- legend：14–16；
- panel label / subtitle：18–22；
- line width：1.2–1.6；
- marker 在 screenshot scale 明显可辨。

### 7.2 Final Paper Profile

accepted 后：
1. 确认论文实际列宽 / 页面宽；
2. 按最终显示尺寸导出，尽量不让 Word/LaTeX 再大比例缩放；
3. 嵌入整页检查；
4. 若字小，优先删冗余、增加图高度/占版、调整 panel 比例，最后才减字号。

Nature 5–7 pt 是最终 production 范围，不直接覆盖 review profile。

### 7.3 字体层级不是“全部加粗”

默认：
- panel letter 可粗；
- subplot subtitle 可 normal/semibold；
- axis label 不必全部 heavy bold；
- tick label regular；
- annotation 仅关键数字/关键词加粗。

如果全图都 bold，层级等于没有层级。

---

## 8. Color System：连续量与类别量分开

### 8.1 Categorical

优先：Okabe–Ito、Paul Tol 或经验证的 colorblind-safe palette。

但 Figure 仍采用 role contract：
- Primary；
- Risk / failure；
- Baseline / context；
- Secondary only when necessary。

同一 paper 维持一个主 palette family，不每张图换一套风格。

### 8.2 Continuous

连续量必须采用 perceptually uniform、ordered、CVD-friendly colormap，如：
- viridis / cividis；
- Crameri Scientific Colour Maps（batlow / vik / roma 等按数据类型选择）；
- parula（若符合项目环境）。

禁止：jet / rainbow / hsv。

### 8.3 颜色不是主要定量编码

关键比较仍需位置 / 长度 / marker / line style 冗余表达。

---

## 9. Anti-AI Figure Gate（硬门）

详见 `anti_ai_figure_gate.md`。任何 data Figure 若出现下列视觉语言，应默认判定 FAIL，除非有明确科学编码意义：

- 圆角卡片；
- 胶囊 badge；
- 渐变背景；
- 发光/阴影；
- 大面积淡蓝/淡紫信息块；
- 亮蓝+亮红+亮绿同时高饱和；
- dashboard KPI 卡；
- 大标题占据顶部大量空间；
- 彩色文字说明代替真正 annotation；
- 每个值都打标签；
- 不必要图标/emoji；
- 过度对称且等宽的“AI 模板式”panel；
- infographic 式解释框比数据本身更抢眼。

---

## 10. Legend / Direct-label Gate

legend 会产生 lookup tax。

优先级：

```text
2–4 个对象 → direct label
多 panel 共用语义 → shared compact legend
对象较多 → facet / focus + context gray
最后才是每个 axes 各自 legend
```

如果 legend 迫使 axes 缩小，优先重构 legend，而不是缩字。

---

## 11. Annotation Budget

每个 axes 默认 1–4 个关键 annotation：
- baseline；
- threshold；
- optimum；
- failure；
- key improvement。

“全部标数值”默认失败。

---

## 12. Render–Review–Iterate Gate（硬门）

代码正确 ≠ Figure 正确。

正式 MATLAB 前必须使用真实 accepted data 完成至少两轮可复现原型：

```text
Prototype v1
→ render PNG
→ read PNG
→ Review #1: body geometry
→ redesign
→ Prototype v2
→ read PNG
→ Review #2: hierarchy / label / color
→ mechanical lint
→ MATLAB
```

### Review #1 — Body Geometry

只看：
- hero 是否明确；
- 主体占版；
- panel ratio；
- whitespace；
- axis waste；
- chart grammar 是否成立；
- 是否像 dashboard / PPT / AI infographic。

若 geometry 失败，禁止靠配色修复。

### Review #2 — Judgment Pass

四问：
1. Depth：遮住 caption，claim 还能读出来吗？
2. Elegance：drop test 通过吗？
3. Unimpeachable：黑白/色弱/轴/容差/证据口径可靠吗？
4. Visible gap：0.5 秒看起来像期刊正文 Figure 吗？

### Mechanical floor

可自动/静态检查：
- 数据源；
- 单位；
- expected columns；
- 禁止求解器；
- 禁止 Excel write；
- 禁止非法 interpolation；
- panel letter；
- clipping / overlap（若原型工具可检测）；
- vector + preview export（论文阶段）；
- palette consistency；
- figure count；
- script reproducibility。

机械 PASS 只是 floor，不代表视觉通过。

---

## 13. MATLAB Implementation Fidelity

MATLAB 只是翻译 approved prototype，不重新设计。

本地截图回来后只修：
- figure aspect ratio；
- panel spacing；
- font metrics；
- legend extent；
- label clipping；
- marker / line weight；
- renderer-specific difference。

若要换 chart grammar，必须显式 reopen Figure Contract。

---

## 14. Embedded-paper Gate

Standalone PNG 通过不等于论文图通过。

最终 accepted 前检查：
- Word/LaTeX/PDF 页面实际占版；
- caption 与 Figure 是否争夺视觉注意；
- 字/marker/line 是否缩小失真；
- 页面是否出现异常空白；
- panel letter 与正文引用顺序一致；
- PDF/SVG 文字是否保持可编辑（若正式导出）。

---

## 15. 顶刊参考图 Reverse Engineering

参考真实论文 Figure 时先拆：

```text
1. core claim
2. hero panel
3. witness panels
4. body bounding box
5. panel ratio / gap
6. axis range / tick density
7. font hierarchy
8. marker / line / fill hierarchy
9. color role
10. direct labels / legend strategy
11. annotation density
12. what is deliberately left to caption
```

写清：

```text
Must imitate  = geometry / hierarchy / visual grammar / density
Must preserve = accepted data / semantics / units / threshold
Do not copy   = original labels / numbers / English production font / fixed colors / irrelevant panels
```

禁止只学到“低饱和、几个点、一个小方块”。

---

## 16. 三类外部 Skill 的吸收边界

### Icarus Figures

吸收：
- Dataset + Claim；
- Depth / Elegance / Unimpeachable / Visible-gap 四轴；
- hero panel；
- drop test；
- mechanical floor + judgment pass；
- archetypes 只是 floor，不是 ceiling。

不机械照搬：
- 强制 N/CI（数学规划不一定适用）；
- Python/TikZ 作为最终后端（本项目正式后端仍 MATLAB）。

### matlab-plot-skill

吸收：
- render → read → critique → iterate；
- final printed width first；
- vector PDF + PNG preview；
- embedded page review；
- prefer taller canvas over tiny fonts；
- shared legend / direct label；
- MATLAB checkcode / export QA。

### skill-publication-figures

吸收：
- paper-level palette consistency；
- pre-export lint；
- automatic overlap / clipping checks；
- preview-only readback；
- style system 单一来源。

不机械照搬：
- 固定 20/22/32 pt 英文字号；
- 所有 spines visible；
- 固定 annotation round boxes。

---

## 17. 收敛规则

同一 Figure：
- 连续 2 轮 geometry 失败 → 重新选候选图型；
- 连续 3 轮用户认为“还是很丑/AI感/松散” → 停止 vN，执行 mismatch diagnosis；
- 已明确哪一张图“有期刊味” → 把它作为 **paper family anchor**，其它 Figure 要学习它的 typography、密度、色彩职责、线宽和留白，而不是各自重新发明风格。

只有用户明确 `accepted/frozen` 后，才进入论文排版和最终导出。