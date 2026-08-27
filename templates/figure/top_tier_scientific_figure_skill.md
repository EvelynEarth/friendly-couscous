# Top-tier Scientific Figure Skill

本文件是 `modules/04_figure_evidence.md` 的高阶科研绘图执行补充，不建立第二套 Figure 决策权威。Module 04 仍负责 Evidence level、Primary question、Layout Gate、Enhancement Gate、Source workbook 与 Figure Contract；本文件负责把已批准的 Figure Contract 落到“证据驱动选型 → 视觉原型 → render-review → MATLAB 实现 → 论文嵌入 QA”。

外部方法论研究底稿见：`templates/figure/journal_figure_research_notes.md`。

---

## 0. 适用范围与核心纠偏

适用于数学建模、优化、仿真、风险、网络、空间、时序、参数敏感性、多目标、预测与诊断结果图。默认中文论文环境。

### 顶刊科研图的正确理解

```text
顶刊科研图 ≠ 小字体 + 细线 + 大留白 + 低饱和
顶刊科研图 = 高信息效率 + 紧凑结构 + 清楚层级 + 数据诚实 + 最终版面可读
```

英文期刊只提供**视觉语法和 production QA 方法**，不得机械复制：
- 英文字体；
- 英文标签；
- 5–7 pt 最终 production 字号；
- 89 / 183 mm 版芯到 MATLAB 交互图窗；
- 某篇论文的固定色号或 panel 数量。

中文项目审图阶段优先保证实际 MATLAB 截图和 Word/PDF 页面可读，再做最终缩放测试。

---

## 1. Figure 的唯一入口：Evidence before chart

禁止先问“画什么高级图”。每张 Figure 先填写：

```text
Core conclusion
Evidence level
Primary question
Audience / paper role
Source workbook + sheet + headers
Required comparisons / thresholds
```

然后才执行：

```text
Evidence task
→ Data structure
→ Perceptual task
→ Candidate chart pool
→ Candidate scoring
→ Geometry sketch
→ Chinese review prototype
→ Render-review #1
→ Redesign if needed
→ Render-review #2
→ MATLAB implementation
→ Screenshot fidelity review
→ Embedded-paper reduction test
→ accepted / frozen
```

---

## 2. Candidate Chart Pool：先展开，再淘汰

每个 Primary question 至少比较 3 个**不同视觉语法**候选，不能只在 bar / line / heatmap / dumbbell / waterfall 中循环，也不能为了“高级感”强行用 ternary / Sankey / 3D。

### 2.1 参数空间 / 稳健性 / 阈值

候选：
- phase / regime diagram；
- decision-region map；
- overview + threshold slice；
- forest / tornado；
- small-multiple sensitivity strips；
- contour / response surface（仅真实连续响应）；
- transition path。

硬规则：
- 离散扫描默认不插值；
- 没有连续模型证据，不画假平滑边界；
- 若一个维度几乎不变，优先切片，不浪费二维画布。

### 2.2 机制 / 流量 / 资源响应

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
- ternary 只有三种组成都实际占据二维 simplex 时才有价值；若点几乎共线、某一分量近似常数或样本太少，改用更直接的 composition strip / point-range；
- 时间长度若不是主要问题，不允许“63天”把其他阶段压成两条缝。

### 2.3 方案差异 / 替代最优 / 公平性

候选：
- dumbbell；
- slopegraph；
- paired interval；
- Cleveland dot；
- rank transition；
- parallel coordinates（变量足够多且语义统一）。

硬规则：
- 没变化对象降权或文字汇总；
- 大量重合点不是“完整”，而是视觉噪声；
- 两状态比较优先位置/连接关系，不靠两种艳色解决。

### 2.4 成本 / 收益 / 目标分解

候选：
- value bridge / waterfall；
- balance ledger；
- signed contribution plot；
- decomposition strip；
- baseline-to-optimum slope；
- cost-benefit interval；
- Pareto front（仅真实多目标权衡）。

硬规则：
- Waterfall 只在增量严格可加总闭合时使用；
- 单个总量 + 若干贡献项不一定需要整张大 waterfall，signed contribution 往往更紧凑；
- “一个数字一根柱”若没有比较任务，优先正文/表格/直接 callout。

### 2.5 分布 / 不确定性 / 合法性

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
- n 很小时优先展示实际点；
- 不用单 bar 代替可见的原始样本；
- 分布图必须能说明样本量或真实统计结构。

---

## 3. Candidate Scoring Gate（强制）

生成 MATLAB 前，对每个候选图型按 0–2 分打分；总分最高者才进入原型阶段。

| 维度 | 0 分 | 1 分 | 2 分 |
|---|---|---|---|
| Answerability | 无法直接回答 Primary question | 需要大量解释 | 一眼回答主要问题 |
| Perceptual precision | 主要靠面积/颜色猜 | 可比较但搜索成本高 | 主要靠位置/长度/对齐 |
| Information density | 大量无效空白/重复对象 | 中等 | 高密度但不拥挤 |
| Data honesty | 需插值/伪连续/隐去例外 | 有风险但可说明 | 直接对应 accepted data |
| Caption burden | 图内不自解释 | 需要较长 caption | caption 只补统计口径 |
| Journal fit | 像 dashboard / PPT | 可入文但一般 | 缩小后仍像科研正文图 |

### 淘汰规则

任一候选若出现下面任一项，直接淘汰，不看总分：
- 需要伪造连续性；
- 主体超过一半区域为空但无结构意义；
- 图例比数据主体更显眼；
- 需要 3 种以上图型才能解释一个 Primary question；
- 图型“高级”但基本二维图更快读；
- 缩小后依赖小字才能看懂。

必须在 Figure Review Note 中记录至少 1 个被淘汰候选及原因，避免反复回到失败架构。

---

## 4. Journal Geometry Gate：顶刊感首先来自版式

### 4.1 数据主体优先

吸收 Nature / Science 风格的共同原则：
- 最大化有效数据区域；
- panel 紧凑排列；
- 无意义轴域、标题区、legend 区和脚注区都算版面成本；
- whitespace 只用于分组、呼吸和层级，不是越多越高级。

### 4.2 Panel 比例由信息量决定

禁止默认等宽 1×2。

若 panel A 是 8×10 参数矩阵，panel B 只有一条阈值曲线，优先 2:1 / 3:1；若两者阅读任务同等，才等宽。

`tiledlayout(...,'TileSpacing','compact','Padding','compact')` 是常用起点，但**不是必须等宽的借口**。必要时使用 tile spanning 或受控 `Position`，并在 render-review 后调整。

### 4.3 Axis bounds

- axis 不应明显超出实际数据范围，除非该空间承载真实阈值/可行域/预测区；
- 不允许通过无意义的 0 起点、超宽 xlim 或过高 ylim 制造巨大空白；
- 共享语义的 panel 统一 tick convention；
- common axis label 能共享时不要重复。

### 4.4 标题层级

Journal mode 默认：
- 不在图内放“Figure 1 / Q3 / 某某结果”式大标题；
- single figure 可无 title，由 caption 承担；
- multi-panel 用 `a / b / c` + 极短 panel subtitle；
- 数模竞赛若必须保留中文整体标题，字号不能把主体挤下去，且不得与 panel title / caption 重复三遍。

优先顺序：

```text
缩短标题 > 移到 caption > 减少重复 > 最后才缩字体
```

---

## 5. Typography：分离“审图字号”和“最终生产字号”

这是本仓库后续必须执行的纠偏。

### 5.1 MATLAB Review Profile（中文）

默认供用户在 MATLAB 图窗 / 截图直接审查：
- axes / tick / axis label：约 16–18；
- legend：约 14–16；
- panel label / subtitle：约 18–22；
- line width：约 1.2–1.6；
- marker 按对象数和图窗缩放，不低于明显可辨阈值。

当前 HSK MATLAB 模板保留 `axes=18, legend=16, LineWidth=1.4` 作为 review baseline。

### 5.2 Final Paper Profile

只在 figure 已 accepted 后做：
1. 按论文实际栏宽导出；
2. 把图嵌入 Word/LaTeX/PDF；
3. 在**整页**而非单独图片上检查；
4. 如果缩放后太小，优先增大图占版或删冗余，而不是继续压字号。

禁止把 Nature 5–7 pt 等生产范围直接写回 review profile。

---

## 6. Color Role Contract

先定义角色，再选颜色。

默认一个 Figure：
- 1 个 Primary 色；
- 1 个 adverse / risk 色；
- baseline/context 用灰或低饱和；
- 必要时第 2 个 category 色，但必须解释语义。

颜色是辅助通道，不是主要定量通道。

硬规则：
- 禁止 rainbow / jet 表连续量；
- 避免红绿直接对比；
- 不用彩色文字承担大段解释；
- 同一对象跨 Figure 颜色职责一致；
- 灰度和色觉缺陷下仍应能通过位置、线型、marker 或明度区分；
- 高饱和色只给 focal point / risk / threshold，不整张图均高饱和。

---

## 7. Legend / Label Search Cost

### 7.1 Legend Tax

legend 会侵占主体面积；必须证明它值得存在。

优先级：

```text
2–4 个对象且可直接标注 → direct label
多个 panel 共用编码 → shared compact legend
对象很多 → 分组 / facet / focus highlighting
最后才是每个 axes 一个 legend
```

### 7.2 Annotation Budget

每个 axes 默认保留 3–5 个不可替代标注：
- 基准；
- 阈值；
- 极值；
- 推荐；
- 失效；
- 关键改善。

不是每个点都贴值。大量精确数值进入表格或 caption。

---

## 8. Render–Review–Iterate Gate（硬门）

**不得在只完成绘图代码时声称 Figure 已完成。**

在生成正式 MATLAB 前，用真实 accepted data 做视觉原型，并至少执行两轮：

```text
Prototype v1
→ render PNG
→ read actual image
→ body geometry critique
→ redesign if needed
→ Prototype v2
→ hierarchy / label / color critique
→ only then MATLAB
```

### Review #1：body geometry

只看：
- 主体占版；
- panel 比例；
- 空白是否有意义；
- axis 是否浪费；
- 图型主体是否成立；
- 是否出现“大标题 + 小主体”。

若失败，禁止靠换色修复。

### Review #2：hierarchy / labels / color

再看：
- 第一眼焦点；
- 字号层级；
- label collision / clipping；
- legend search cost；
- color role；
- grayscale / color-deficiency sanity；
- 2 秒 / 10 秒阅读测试。

**2 秒测试**：能否知道比较谁、差异方向在哪里。  
**10 秒测试**：能否用一句话复述该 Figure 的主结论。

---

## 9. Prototype before MATLAB

容器无 MATLAB 时：
- Python/Matplotlib 只做视觉原型；
- 原型必须读取相同 accepted workbook；
- 不重新求解；
- 不改变证据语义；
- 可改变 chart grammar / geometry 直到通过 render-review；
- MATLAB 必须忠实翻译已通过的原型，而不是重新“设计一遍”。

如果 MATLAB 最终截图与原型差异明显，进入 **implementation fidelity review**，只修：
- 字号；
- panel spacing；
- axes extent；
- legend；
- label；
- MATLAB renderer 差异。

除非显式 reopen，不重新换图型。

---

## 10. Embedded-paper Gate

Standalone PNG 通过不等于论文图通过。

最终 accepted 前必须检查：
- 嵌入 Word/LaTeX/PDF 后是否仍可读；
- caption 是否和图争夺视觉注意；
- 页面缩放是否让字、线、marker 变小；
- 图在页面上是否过宽/过窄；
- 是否造成页底大空白；
- panel label 顺序是否符合正文引用。

若嵌入后失败，优先：

```text
调整版心占用
→ 删除重复标题/图例/标签
→ 调整 panel 比例
→ 增加 figure 高度
→ 最后才改字号
```

---

## 11. Reference Figure Reverse Engineering

用户提供顶刊参考图时，必须先拆解：

```text
1. Body bounding box / 占版率
2. Panel ratio / gap
3. Axis range / tick density
4. Typography hierarchy
5. Primary / context / risk 颜色职责
6. Point / line / fill 层级
7. Annotation density
8. Legend strategy
9. Reading order
10. 哪些内容实际放在 caption 而不在图内
```

必须写：

```text
Must imitate   = geometry / hierarchy / encoding / density
Must preserve  = 本题 accepted data / thresholds / Chinese semantics
Do not copy    = 原图对象名 / 阈值 / production font / fixed Hex / irrelevant panels
```

禁止只学到“有一个小方块、有几个点、有某个颜色”。

---

## 12. Data honesty

- 离散点不 spline；
- 独立场景点不伪造连续曲线；
- ROI 不截轴夸大；
- ternary / Sankey / alluvial 明确表示 composition、path 还是 flow；
- 阈值区间只画真实 evidence；
- 数值残差采用业务/数值容差；
- axis 与颜色不得暗示不存在的顺序、连续性或因果。

---

## 13. Anti-patterns（项目历史硬禁）

1. **Small-font fallacy**：小字体不是顶刊感。
2. **White-space fallacy**：大空白不是高级感。
3. **Equal-panel fallacy**：证据密度不同不必等宽。
4. **Novelty fallacy**：高级图只有提高信息效率才准入。
5. **Title stacking**：大标题 + panel title + annotation + caption 不得重复同一结论。
6. **Legend tax**：legend 不得逼缩主体。
7. **Axis waste**：无意义超宽 axis 视为失败。
8. **Unchanged-object clutter**：不变对象降权/汇总。
9. **Reference cosplay**：不机械模仿 Nature/Science 的表面风格。
10. **Single-preview fallacy**：至少两轮 render-review。
11. **Color-patch repair**：geometry 失败时禁止只换配色。
12. **Version churn**：连续约 3 轮未收敛，必须停止出 vN，先做 mismatch diagnosis。

---

## 14. External methodological references

方法论来源及吸收边界见 `templates/figure/journal_figure_research_notes.md`。重点包括：
- Nature Research Figure Guide；
- Nature Methods Points of View / Points of View, anew (2026)；
- PLOS Better Figures / Colorization rules；
- Science/AAAS-style author figure guidance；
- JAMA Editors Guide / Oxford；
- Brain author figure guidance；
- MATLAB `gramm`；
- `hanlulong/matlab-plot-skill` render-review workflow；
- SciencePlots / sci-figure 仅作 production/style-system 参考。

外部资料只提供方法论；项目真值、字段、阈值、结论和 Figure 职责仍以 Module 04 + accepted workbook 为准。