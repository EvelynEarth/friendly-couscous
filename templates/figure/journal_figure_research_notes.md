# Journal Figure Research Notes（顶刊科研绘图外部研究底稿）

> 更新日期：2026-08-27  
> 作用：为 `top_tier_scientific_figure_skill.md`、`chart_selection.md`、MATLAB 模板和 Figure QA 提供可追溯的外部方法论依据。  
> 边界：本文件不是赛题真值源，不覆盖 `modules/04_figure_evidence.md`、accepted workbook、Figure Contract 或项目语义冻结。

## 1. 研究结论先行：所谓“顶刊风”不是小字号、细线和大留白

本轮检索后，统一采用下面的解释：

```text
顶刊科研图 ≠ 机械复制某期刊字号/色号/版芯
顶刊科研图 = 高信息效率 + 清楚层级 + 紧凑但不拥挤 + 数据诚实 + 最终版面可读
```

尤其禁止把 Nature 的最终生产字号（例如 5–7 pt）直接当成 MATLAB 交互审图字号。期刊生产规范描述的是**最终缩放后的成品**；项目绘图阶段仍以中文可读性、截图审查和论文嵌入后的 reduction test 为准。

---

## 2. Nature / Nature Methods：采用的规则

### 2.1 Nature Research Figure Guide

来源：
- https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/
- https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/

吸收规则：
- panel 要 **neat and space-efficient**，最小化无效白空间；
- panel 尺寸由内容和可读性决定，不要求机械等宽；
- 图中文字必须在最终尺寸可读；
- 避免背景网格线、阴影、装饰图标、难读背景上的文字；
- 避免彩色文字承担主要解释；
- 注意色觉缺陷，避免红绿难辨组合。

不机械复制：
- 5–7 pt 仅视为最终 production 尺度参考，不直接写进中文 MATLAB review profile；
- 89 / 183 mm 仅用于最终嵌入/缩放 QA，不作为交互图窗固定尺寸模板。

### 2.2 Nature Methods — Points of View

来源：
- Points of View, anew (2026): https://www.nature.com/articles/s41592-026-03143-5
- Design of data figures: https://www.nature.com/articles/nmeth0910-665
- Layout: https://www.nature.com/articles/nmeth.1711
- Color coding: https://www.nature.com/articles/nmeth0810-573
- Negative space: https://www.nature.com/articles/nmeth0111-5
- Plotting symbols: https://www.nature.com/articles/nmeth.2490
- Color blindness: https://www.nature.com/articles/nmeth.1618

吸收规则：
- 图是“读者解码数据”的界面，先确定 message，再选择视觉变量；
- layout 必须表达数据结构和结论结构；
- whitespace 是结构工具，不是“越多越高级”；
- 位置、长度、方向等感知任务优先于面积和颜色；
- 色彩优先表达类别/状态，不让 rainbow 承担连续定量排序；
- 符号的形状、填充、颜色应组成自然层级，降低 legend lookup cost；
- 图型选择按数据性质和阅读任务，而不是按软件默认或“高级感”。

---

## 3. PLOS：采用的规则

### 3.1 Ten Simple Rules for Better Figures

来源：https://journals.plos.org/plosone/doi?id=10.1371/journal.pcbi.1003833

吸收规则：
- 明确 audience 和 one-sentence message 后才画图；
- 图要让论文外的读者也能正确解码；
- 工具服务于表达，不要被 MATLAB 默认图型束缚；必要时可先用其他工具做原型，再翻译到 MATLAB；
- 科研图是“people ↔ data interface”，视觉选择必须围绕认知任务。

### 3.2 Ten simple rules to colorize biological data visualization

来源：https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008259

吸收规则：
- 先判断数据类型，再定义色彩职责；
- 检查颜色在上下文中的交互，而不是只看单个 Hex；
- 兼顾色觉缺陷、网页和打印；
- 必须进行 grayscale / black-and-white sanity check。

---

## 4. Science / AAAS 风格作者指南：采用的规则

来源（Science Partner Journals author figure guidance）：
- https://spj.science.org/page/research/for-authors/

吸收规则：
- **maximize the space given to presentation of the data**；避免 wasted white space 和 clutter；
- 标题职责优先放 figure legend/caption，不在数据区堆大标题；
- panel 靠近排列，共享 axis label 不重复；
- axis 不应远远超出数据范围；
- 不使用 minor ticks / background gridlines；
- symbol / line 在缩放后仍应可辨；
- key / legend 尽量简单，细节交给 caption。

项目适配：
- 数模竞赛中文论文允许简洁图题，但其视觉权重不得超过数据主体；
- 若 caption 已能承担标题职责，可在“journal mode”删除 MATLAB 大标题。

---

## 5. JAMA / Oxford Academic：采用的规则

来源：Effective Use of Figures and Graphs in Scientific Publications  
https://academic.oup.com/book/58841/chapter/489872449

吸收规则：
- 一个 multipanel Figure 的所有 panel 应围绕同一 theme / take-home message；
- figure suite 应能在只看图和图注时理解论文主要证据；
- 颜色可帮助密集数据分组，但多色且跨图语义漂移会增加认知负担；
- 复杂研究可加入真正提供 roadmap 的结构示意，而不是装饰性流程图。

---

## 6. Brain / Oxford Academic：采用的规则

来源：https://academic.oup.com/brain/pages/General_Instructions

吸收规则：
- panel 避免无效空白和 clutter；
- symbol / line 在最终尺寸可辨；
- 小样本连续数据优先展示实际数据点，而不是只画 summary bar；
- 单个 bar 或“100%的一根 bar”通常信息效率低；
- 色彩应节制，避免红绿组合、阴影和无意义 3D。

---

## 7. Cell Press：只采用与一般科研视觉一致的部分

来源：Cell Press Graphical Abstract Guidelines  
https://crosstalk.cell.com/hubfs/Files/GA_guide.pdf

注意：graphical abstract 不是普通 data figure，本仓库**不把它当数据图权威**。

仅吸收：
- single take-home message；
- 颜色帮助指向 focal point，但高饱和原色过多会分散注意；
- 一致、互补的视觉语言比“每张图一个新色板”更专业。

---

## 8. MATLAB / Agent 绘图实践：采用的规则

### 8.1 matlab-plot-skill

来源：https://github.com/hanlulong/matlab-plot-skill

关键吸收：
- 不能在“代码写完”时停止；
- 必须 `render → read → critique → revise`；
- 独立 PNG 好看不等于论文页好看，最终还要检查嵌入后的 page-scale；
- 标题过长时优先缩短标题，不先缩字体；
- legend 不应为了完整性侵占主体；
- panel gap、axis conventions、缩放后的字体/线宽必须检查。

### 8.2 gramm

来源：https://github.com/piermorel/gramm

吸收：
- Grammar of Graphics 思想：先声明数据映射、分组、统计与 facet 语义，再实现具体图形；
- 复杂科研图可借鉴 declarative grammar，但项目默认仍交付自包含 MATLAB `.m`，不强制用户安装第三方库。

### 8.3 SciencePlots / sci-figure 等开源项目

参考：
- https://github.com/garrettj403/SciencePlots
- https://github.com/xiao-yuling/sci-figure

只吸收：
- journal style 应通过统一 style system 管理；
- CJK 需要专门字体和最终缩放检查；
- editable/vector export 是论文阶段的 production concern；
- 不直接复制其固定字号、色板或英文排版到本项目。

---

## 9. 从本项目失败迭代中新增的反例规则

以下是本仓库后续 Figure Skill 的硬性 anti-pattern：

1. **Small-font fallacy**：不得把“小字体”当顶刊感；审图模式字体要足够大，最终再做缩放 QA。
2. **White-space fallacy**：不得把“大面积空白”当高级感；white space 必须承担分组、节奏或分隔职责。
3. **Equal-panel fallacy**：证据密度不同的 panel 不必等宽；panel 大小由信息量决定。
4. **Novelty fallacy**：ternary / Sankey / chord / 3D 只有在二维基础图明显损失结构时才使用。
5. **Title stacking**：禁止 `sgtitle + panel title + 大注释框 + caption` 同时重复同一结论。
6. **Legend tax**：能直接标注 2–4 个对象时优先直接标注；legend 不能逼缩主体。
7. **Axis waste**：axis 范围若显著超出数据而没有阈值/参考意义，视为布局失败。
8. **Unchanged-object clutter**：大量没有变化的对象应降权或汇总文字说明，不制造重合点。
9. **Reference cosplay**：参考顶刊图只拆解 geometry / hierarchy / encoding / density，不复制英文标签、固定色号或 production 字号。
10. **Single-preview fallacy**：至少两次 render-review；若首轮 geometry 失败，必须 redesign，禁止只换色。

---

## 10. 本仓库最终采用的 Journal Figure Synthesis

```text
Evidence Contract
→ Candidate Chart Pool
→ Perceptual / Honesty Score
→ Geometry Sketch
→ Chinese Review Prototype
→ Render Review #1（body）
→ Redesign if needed
→ Render Review #2（hierarchy + labels + color）
→ MATLAB translation
→ MATLAB screenshot fidelity review
→ Embedded-paper reduction test
→ accepted / frozen
```

这套流程优先于任何“Nature风 / Science风 / Cell风”字面模仿。