# Scientific Figure Skill Landscape（高级顶刊科研绘图 Skill / 方法论调研）

> 更新日期：2026-08-28  
> 目标：持续吸收真正提高 publication-grade judgment 的方法，而不是寻找一个“更像 Nature 的模板”。

本文件只做外部方法论与工具吸收矩阵；项目实际执行以 `top_tier_scientific_figure_skill.md` + `journal_figure_mastery_v2.md` 为准。

---

# 1. 顶刊编辑部 / 学术方法论：优先级最高

## A. Nature Research Figure Guide

关键来源：
- Preparing figures — our specifications
- Building and exporting figure panels
- Top 10 ways to delay your paper

真正值得吸收：
- panel neat + space-efficient；
- panel 大小由内容和可读性决定，不机械等宽；
- 减少无意义白区；
- axis/tick/unit 完整；
- 避免背景 grid、drop shadow、decorative icon、overlapping text；
- 文字尽量黑/白高对比，不靠彩色文字解释；
- accessibility 与 CVD；
- vector artwork、editable text；
- final production width 约 89 / 183 mm。

本项目吸收：★★★★★

不机械复制：
- Nature 5–7 pt 属于最终 production size，不直接覆盖中文 MATLAB review profile。

---

## B. Nature Methods — Points of View / Points of Significance

重点：
- Design of data figures；
- Layout；
- Salience；
- Salience to relevance；
- Negative space；
- Simplify to clarify；
- Labels and callouts；
- Plotting symbols；
- Axes, ticks and grids；
- Unentangling complex plots；
- Bar charts and box plots；
- Error bars；
- Storytelling；
- The overview figure。

项目新增吸收：

### Salience → relevance
最醒目的对象必须就是最相关对象。避免 title / baseline / context / background 比 hero data 更抢眼。

### Labels are layout
callout / label 的长度、角度、对齐、公共文本重构，本身就是 Figure geometry 的一部分。

### Complex plots → small multiples
复杂 overview 不是高级；尺度差异、线条纠缠时，按数据缩放的 carefully designed small multiples 往往更好。

### Navigation ink
axes/ticks/grid 是导航，不应抢 primary data 的 salience。

### Distribution honesty
统计样本优先 raw points / box / distribution，而不是 bar of means。

本项目吸收：★★★★★

---

## C. Nature visual communication framework — Kelly Krause

核心思想：

```text
visual design depends on intended audience + communication context
```

同一科研内容面对：
- 专业审稿人；
- 跨学科读者；
- 竞赛评委；
- 教学展示

视觉解释深度、缩写、context 都应不同。

本项目适配：
- 数模论文默认 audience = 技术型评委 + 快速扫描；
- 图要专业但不能依赖领域隐语；
- Primary claim 要在 2–10 秒内可读。

本项目吸收：★★★★★

---

## D. Cleveland–McGill / Bertin graphical perception

视觉编码准确性优先：

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

项目影响：
- exact comparison → forest/dot/interval；
- composition → 只有真正需要 composition 时才用 stacked/pie/ternary；
- color 作为辅助，不承担精确数值比较。

吸收：★★★★★

---

## E. Crameri Scientific Colour Maps

Nature Communications 2020 指出 rainbow/red-green 等不均匀色图会扭曲数据解释。

项目吸收：
- continuous color 必须匹配 sequential / diverging / cyclic；
- perceptually uniform；
- grayscale / CVD 检查；
- jet / rainbow / HSV 禁止。

吸收：★★★★★

---

# 2. Agent / Skill / 工具：吸收执行机制，不照抄 house style

## A. Icarus Figures

仓库：`TAO-QKV/Icarus-Figures`

当前最值得吸收的 Figure judgment framework：

```text
Dataset + Claim
Depth
Elegance
Unimpeachable
Visible gap
mechanical floor + judgment pass
hero panel + drop test
```

最新进一步吸收：
- figure critique 明确区分“机器能检查的 floor”和“只有看真实 render 才能判断的 quality”；
- caption-cover test；
- generic boxes-and-arrows 不能当 hero method figure；
- grayscale / honest axes；
- legend ping-pong；
- distribution 优先于 bar of means。

本项目额外加两轴：
- Salience relevance；
- Suite coherence。

吸收：★★★★★

适配：
- Icarus 强调 N / uncertainty；本项目数学规划必须按 statistical / scenario / parametric / numerical 等语义分流，不能伪造统计不确定性。

---

## B. hanlulong/matlab-plot-skill

核心：

```text
code written != figure done
render → export/read → critique → iterate
```

吸收：
- MATLAB `checkcode` / static preflight 思维；
- standalone + embedded-page 双重检查；
- cramped geometry 先改 canvas / layout，不先缩字体；
- vector output；
- B&W 冗余 encoding。

吸收：★★★★★

---

## C. dazhiyang/scientific-plotting-skill

值得吸收：
- style 参数集中在一个 parameter block；
- final-width-first（85 / 180 mm）；
- dense scatter 不输出百万 vector glyph；
- map 边界简化；
- discrete color 与 continuous color 分开；
- no plot title 的 journal mode 思维。

本项目**不照搬**：
- Times 单字体；
- 所有文字一个字号；
- viridis-only；
- continuous color 默认 quantile splits。

为什么不默认 quantile splits：数模论文很多连续变量是成本、距离、容量等物理/经济量，quantile transform 会破坏“等数值差=等视觉差”的含义。只有 claim 本身是分位等级时才使用。

吸收：★★★★☆

---

## D. PEEKPerformer/skill-publication-figures

最强点：
- one palette per paper；
- style config single source of truth；
- lint clipping / overlap / panel letters；
- preview/readback；
- vector multi-format。

吸收：★★★★☆

不照搬具体 house style：Arial/固定大字号/all spines/round boxes。

---

## E. gramm

价值：Grammar of Graphics 思维。

吸收：
- data mapping；
- grouping；
- faceting；
- statistical layer；
- small multiples；
- 不把 Figure 设计理解成一串 plot 命令。

吸收：★★★★☆

MATLAB 项目默认不强制用户安装 gramm，但选型方法可以借鉴。

---

## F. SciencePlots

价值：
- style preset；
- journal-specific style；
- colorblind options；
- CJK 适配经验。

局限：style preset 解决不了 claim / hero / geometry / salience。

吸收：★★★☆☆

---

## G. 2023Anita/scientific-visual-skills — scientific-paper-figure

主要面向：
- mechanism figure；
- graphical abstract；
- anatomy / workflow；
- technical route。

值得吸收：
- mechanism / causal path first；
- 主体 + 局部放大；
- 输入→过程→输出等叙事结构；
- 标签短、箭头服务逻辑。

不适用于：
- accepted numerical data Figure 的自动生图。

本项目明确：Data Figure 不允许 AI-generated image 作为实现基准；Mechanism Figure 可以借鉴叙事结构，但必须真实、可追溯。

吸收：★★★☆☆（仅机制图部分）

---

# 3. 新增的高级融合结论

## 3.1 Figure Suite > 单图

以前关注“这一张好不好看”，现在增加整篇图组架构：
- 不重复 claim；
- 不无意识重复 grammar；
- 保持 paper-family style；
- L1/L2/L3/L4 有合理视觉资源分配。

见 `figure_suite_manifest.md`。

## 3.2 Salience-Relevance > 配色

颜色只是显著性的一种。真正需要控制的是：

```text
reader first sees what is scientifically most important
```

这比“选哪个蓝色更高级”重要得多。

## 3.3 Editorial compression > 加元素

顶刊感往往来自：
- 删除重复 panel；
- 删除重复 title；
- baseline residualization；
- refactor common labels；
- direct label；
- hero/witness 非等权布局。

## 3.4 Uncertainty semantics > 一律 error bar

数学建模必须区分：
- scenario；
- parameter；
- robust set；
- numerical gap；
- statistical；
- forecast。

不同不确定性对应不同 visual grammar。

## 3.5 Thumbnail test > standalone 大图好看

Figure 在大 MATLAB 窗口里好看，不代表论文里好看。

缩小后如果只剩：
- 大标题；
- 大色块；
- 夸张 callout

而真正数据趋势消失，说明 hierarchy 失败。

---

# 4. 当前融合后的最强组合

```text
Nature Research Guide
→ production + accessibility + space efficiency

Nature Methods Points of View
→ layout + salience + labels + axes + complexity decomposition

Nature visual communication framework
→ audience/context

Cleveland–McGill / Bertin
→ perceptual accuracy

Icarus Figures
→ claim + hero + four-axis + critique gate

matlab-plot-skill
→ MATLAB render-review loop

publication plotting skills
→ style single-source + final-width + dense data handling

Crameri
→ scientific continuous color

HSK project rules
→ Chinese review profile + accepted workbook + MATLAB-only-drawing + freeze/version control
```

本仓库真正的融合实现是：

```text
top_tier_scientific_figure_skill.md
+ journal_figure_mastery_v2.md
+ figure_suite_manifest.md
+ figure_iteration_control.md
+ anti_ai_figure_gate.md
+ result_figure_qa.md
```

没有任何一个外部 Skill 被原样照搬。