# Scientific Figure Skill Landscape（顶尖科研绘图 Skill / Tool 调研）

> 更新时间：2026-08-28  
> 目标：不是找一个“最漂亮模板”照抄，而是拆出最值得吸收的执行机制。

---

## 1. 本轮最值得吸收的 6 个来源

### A. Icarus Figures — 当前最完整的“Figure judgment skill”

仓库：https://github.com/TAO-QKV/Icarus-Figures

核心价值不是 48 个 chart type，而是它把 publication-grade 定义成四轴：

```text
Depth
Elegance
Unimpeachable
Visible gap
```

以及：
- Dataset + Claim；
- Figure Contract；
- hero panel；
- drop test；
- mechanical floor + judgment pass；
- archetype 是 floor，不是 ceiling；
- 真实方法对象应嵌入 hero figure，而不是 generic boxes-and-arrows。

本项目吸收：★★★★★

需要改写：
- 它强制 N / uncertainty，更适合统计/实验论文；数学规划需替换为 threshold / scenario range / numerical tolerance / enumeration verification；
- 最终后端仍以 MATLAB 为主。

---

### B. hanlulong/matlab-plot-skill — 当前最强 MATLAB render-review workflow

仓库：https://github.com/hanlulong/matlab-plot-skill

最重要的硬规则：

```text
code written != figure done
render -> export -> read PNG -> critique -> iterate
```

同时要求：
- 先知道 final printed width；
- MATLAB `checkcode`；
- vector PDF + PNG preview；
- 读 standalone figure；
- 能编译论文时再读 embedded page；
- cramped panels 先增加 canvas / 改 geometry，不先缩字体；
- legend 不应偷走 data area；
- direct labels / marker / line style 增强 B&W 可读性。

本项目吸收：★★★★★

---

### C. PEEKPerformer/skill-publication-figures — 最强 style consistency + lint 思路

仓库：https://github.com/PEEKPerformer/skill-publication-figures

值得吸收：
- **one palette per paper**；
- style config single source of truth；
- `lint_figure()` 检查 clipping / overlap / missing panel letters；
- preview-only readback；
- PDF + PNG + SVG 多格式；
- fixed house-style 能避免半年后图风漂移。

本项目吸收：★★★★☆

不照搬：
- 固定 Arial 20/22/32 pt；
- all spines visible；
- annotation round box；
- 18×14 inch 默认 canvas。

这些是其 lab house-style，不是普适顶刊规则。

---

### D. gramm — 最适合 MATLAB 的 Grammar of Graphics 思路

仓库：https://github.com/piermorel/gramm

价值：
- declarative grammar；
- grouping / faceting / statistical summary / density / uncertainty；
- publication-quality complex data visualization；
- 图型不是“命令堆叠”，而是 data mapping + visual grammar。

本项目吸收：★★★★☆

原则：
- 默认不要求用户额外安装 gramm；
- 但 chart selection 和 panel composition 可按 grammar-of-graphics 思维组织。

---

### E. SciencePlots — 强在 journal preset，不强在 Figure judgment

仓库：https://github.com/garrettj403/SciencePlots

价值：
- publication style preset；
- journal-specific style；
- colorblind options；
- CJK 支持。

本项目吸收：★★★☆☆

限制：
- style sheet 只能解决 typography / line / canvas，不能解决 chart grammar / hero hierarchy / evidence depth；
- 不能再把“套 Nature style”误认为 Figure 已 publication-grade。

---

### F. Fabio Crameri Scientific Colour Maps + DiVA

论文：Crameri, Shephard & Heron, Nature Communications 2020  
https://www.nature.com/articles/s41467-020-19160-7

DiVA: effective design for any MatLab figure  
https://doi.org/10.5281/zenodo.3596368

核心价值：
- continuous colormap 要 perceptually uniform；
- equal data difference 应映射成 equal perceptual difference；
- CVD / grayscale 可读；
- `jet / rainbow` 会制造视觉误差；
- continuous / diverging / cyclic 必须按数据语义匹配。

本项目吸收：★★★★★（连续色图部分）

---

## 2. 学术方法论基础（比“风格模板”更重要）

### Nature Methods — Bang Wong / Martin Krzywinski / Nils Gehlenborg

重点：
- Design of data figures；
- Layout；
- Negative space；
- Simplify to clarify；
- Axes, ticks and grids；
- Plotting symbols；
- Integrating data；
- Unentangling complex plots。

核心不是“Nature配色”，而是：

```text
visual structure should match the message
```

### Cleveland & McGill graphical perception

Figure 选型应优先更精确的视觉任务：

```text
aligned position
> non-aligned position
> length
> direction / slope
> angle
> area
> volume
> hue / saturation
```

这解释了为什么：
- dot / interval / forest 常比 pie / bubble 更精确；
- 4 个方案的 exact comparison 不应靠大色块；
- color 应辅助，而不是承担主要定量比较。

---

## 3. 最终采用的组合，不选择“唯一神 Skill”

没有一个外部 Skill 可以完整覆盖本项目。

最终组合：

```text
Icarus Figures
  → 判断 Figure 是否有 Depth / Elegance / Unimpeachable / Visible gap

Nature Methods + Cleveland/McGill
  → 决定视觉编码和 layout

matlab-plot-skill
  → 强制 MATLAB render-review-iterate

skill-publication-figures
  → style consistency + lint / preview 思维

gramm
  → chart grammar / facet / statistical composition 思维

Crameri / DiVA
  → 科学连续色图 + MATLAB 设计准确性
```

本仓库 `top_tier_scientific_figure_skill.md` 是以上方法论的项目适配版。

---

## 4. 针对本项目历史失败的最重要新规则

### 4.1 不再使用 AI-generated image 做数据 Figure 原型

正式 Figure prototype 必须可复现，读取 accepted workbook。文生图只会强化：
- pastel card；
- dashboard；
- infographic；
- 不受数值约束的 geometry。

### 4.2 “像顶刊”的第一条件不是颜色，是 evidence hierarchy

```text
hero panel
+ threshold / mechanism / distribution / region
+ witnesses
```

比：

```text
蓝色 + 红色 + 大标题 + 两个等宽 panel
```

高级得多。

### 4.3 “高级图型”只在 basic grammar 损失证据时准入

- ternary：必须真正占据二维 simplex；
- Sankey：必须真实 flow；
- chord：必须关系矩阵值得比较；
- 3D：必须第三维不可替代；
- radar：默认高风险；
- pie/donut：默认低优先级。

### 4.4 一旦用户指出一张 Figure 有期刊味，它就是 figure-family anchor

后续 Figure 的：
- typography；
- stroke；
- palette roles；
- marker scale；
- annotation density；
- whitespace rhythm

优先与 anchor 对齐，而不是继续“每张图重新找风格”。

---

## 5. 后续 Q3 重绘执行顺序

```text
F3（已被用户认为最接近期刊）= paper-family anchor

F1 / F2 reopen
→ 先做 mechanism / claim diagnosis
→ 参考真实论文结构，不参考 AI mockup
→ >=3 candidates
→ four-axis quality scoring
→ real-data prototype
→ anti-AI gate
→ render review #1
→ redesign
→ render review #2
→ grayscale test
→ MATLAB translation
→ screenshot fidelity review
```

在以上步骤完成前，不再生成新的 `q3_plot_v13/v14/...`。