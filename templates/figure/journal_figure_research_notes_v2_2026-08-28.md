# Journal Figure Research Notes v2 — 2026-08-28

> 本轮目标：针对“当前绘图 Skill 仍然容易产出普通、松散、AI感图”的问题，再次搜集更高阶的顶刊方法与 agent skill，并明确吸收/拒绝边界。

---

## 1. Nature Research Figure Guide

来源：
- https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/
- https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/
- https://research-figure-guide.nature.com/figures/top-10-ways-to-delay-your-paper/

### 新确认的关键点
- panel 要 neat and space-efficient；
- panel 大小由内容与 legibility 决定；
- avoid background gridlines / drop shadows / decorative icons / overlapping text / coloured text；
- axis lines、ticks、units 必须完整；
- 颜色考虑 CVD；
- text 可编辑；
- 89 / 183 mm 是 final production width；
- line/stroke 在最终尺寸仍必须可读。

### 对本项目的直接影响
- “无网格”不是审美偏好，而是 data salience 管理；
- title / legend / annotation 如果逼缩主体，优先删；
- direct label 优先黑/深灰文字 + marker/keyline，而不是彩色大字；
- final-width 与 MATLAB review 必须分开。

---

## 2. Nature Methods — Salience / Salience to relevance

来源：
- https://www.nature.com/articles/nmeth1010-773
- https://www.nature.com/articles/nmeth.1762

### 核心
人眼先被“最显著”对象吸引；如果最显著与最相关不一致，理解会被误导。

### 新增规则
每张 Figure 必须写：

```text
Most relevant object = ?
Most salient object = ?
```

二者必须一致。

这解决了历史问题：
- 浅蓝大背景比数据抢眼；
- 大标题抢过 hero data；
- fixed baseline 占据最大彩色面积；
- legend / KPI callout 成为第一视觉焦点。

---

## 3. Nature Methods — Labels and callouts

来源：https://www.nature.com/articles/nmeth.2405

### 核心
label 本身是 layout，需要一致的 spacing、alignment、leader geometry；公共文本应 refactor。

### 新增规则
- common prefix / unit 提取到 header / axis；
- labels 对齐；
- leader 不交叉；
- callout line 长度/角度尽量一致；
- 一行 row label 只保留差异字段；
- 不让重复文本把图撑宽。

---

## 4. Nature Methods — Axes, ticks and grids

来源：https://www.nature.com/articles/nmeth.2337

### 核心
导航元素需要可辨，但不能抢主数据 salience。

### 新增规则
- tick outward；
- major grid 默认关闭；
- 若精确读数必须 grid，只能极轻；
- minor grid 默认禁止；
- 轴范围服从 evidence domain；
- navigation ink 与 primary data 必须有层级差。

---

## 5. Nature Methods — Unentangling complex plots

来源：https://www.nature.com/articles/nmeth.3451

### 核心
仔细设计、按数据尺度缩放的小 multiples，常比一个纠缠 overview 更有效。

### 新增 Complexity Decomposition Gate
触发：
- >4纠缠曲线；
- 多尺度；
- legend ping-pong；
- ROI 被压平；
- 一个 axes >3 类编码。

优先 small multiples / overview+zoom / hero+witness / progressive cropping。

---

## 6. Nature Methods — Plotting symbols

来源：https://www.nature.com/articles/nmeth.2490

### 核心
shape / fill / color 可以建立自然层级，降低 legend lookup。

### 项目适配

```text
primary = filled
secondary = open
context = gray/small
threshold = rule
```

不再给多个系列随机分配多个高饱和色。

---

## 7. Nature Methods — Simplify to clarify / Elements of visual style

来源：
- https://www.nature.com/articles/nmeth.1660
- https://www.nature.com/articles/nmeth.2444

### 核心
删掉不承担信息的元素；过量重复会让意义衰减。

### 新增 Editorial Compression Gate
每个元素问：

```text
删掉它，会失去哪条证据？
```

没有证据损失 → 删除。

---

## 8. Nature Methods — Bar charts and box plots / Kick the bar chart habit

来源：
- https://www.nature.com/articles/nmeth.2807
- https://www.nature.com/articles/nmeth.2837

### 核心
统计样本不能用 bar of means 隐藏分布；点/box/distribution 更诚实。

### 数模适配
数学规划的确定性结果仍可用 bar 表示真实总量；但“sample distribution”绝不能只剩 bar。

---

## 9. Nature Methods — Error bars

来源：https://www.nature.com/articles/nmeth.2659

### 核心
error bar 必须明确语义，不能仅写“variability”。

### 本项目升级
建立 Uncertainty Semantics：
- statistical；
- scenario；
- parametric；
- robust/feasible；
- numerical；
- forecast。

不同类型不共用同一“误差棒语言”。

---

## 10. Nature visual communication framework — Kelly Krause

来源：
- https://pubmed.ncbi.nlm.nih.gov/27117485/
- https://journals.sagepub.com/doi/10.1177/0963662516640966

### 核心
视觉设计必须针对 audience + communication context。

### 项目适配
数学建模竞赛默认：
- audience = 技术评委，但阅读速度快；
- 图应保留专业性，同时减少隐语与 legend search；
- claim 在 2–10 秒内能复述。

---

## 11. Icarus Figures critique skill（再次深挖）

仓库：`TAO-QKV/Icarus-Figures`

重点读取：
- `.claude/skills/icarus-figures/SKILL.md`
- `references/figure-critique.md`

### 新吸收
- mechanical floor 与 judgment pass 明确分层；
- most figures 能过机械层却仍是 shallow figure；
- caption-cover test；
- generic method flowchart FAIL；
- legend ping-pong；
- grayscale skeptic test；
- bar-of-means → distribution；
- hero/witness 非等权构图。

### 项目升级
在四轴上新增：
- Salience relevance；
- Suite coherence。

形成 Judgment Pass 2.0 六问。

---

## 12. dazhiyang/scientific-plotting-skill

仓库：`dazhiyang/scientific-plotting-skill`

### 吸收
- parameter block single source；
- final-width-first；
- dense scatter / map simplification；
- discrete vs continuous color 明确分流；
- no-title journal mode。

### 明确不吸收
- Times 作为唯一字体；
- 所有文字一个字号；
- viridis-only；
- continuous 默认 quantile split。

原因：quantile recoloring 可能破坏成本、距离、容量等绝对数值间距。

---

## 13. 2023Anita/scientific-visual-skills

仓库：`2023Anita/scientific-visual-skills`

### 适用
mechanism / graphical abstract / anatomy / workflow。

### 吸收
- 科学结构和因果路径优先；
- 主体 + 局部放大；
- 输入→过程→输出；
- 标签短；
- 箭头只服务逻辑。

### 不用于
accepted numerical Data Figure 的生图实现。

---

# 14. 本轮新增到仓库的高级能力

1. `journal_figure_mastery_v2.md`
   - Figure Suite Architecture
   - Salience–Relevance
   - Editorial Compression
   - Complexity Decomposition
   - Uncertainty Semantics
   - Invariant Subtraction
   - Navigation Ink
   - Label Engineering
   - Symbol Hierarchy
   - Thumbnail Test

2. `figure_suite_manifest.md`
   - 全篇图组去重
   - grammar registry
   - paper-family anchor
   - suite thumbnail review

3. `top_tier_scientific_figure_skill.md`
   - 四轴扩展为六轴
   - claim→visual task
   - Judgment Pass 2.0

4. `chart_selection.md`
   - 从“图型菜单”升级为 claim/task/grammar 索引

5. `result_figure_contract.md` / `result_figure_qa.md`
   - 增加 suite / salience / uncertainty / thumbnail / mechanical+jdugment gates。

---

# 15. 最重要的新认识

```text
真正的顶刊感不是“选一种高级图”
而是：

整篇 Figure 有逻辑
+ 最重要的数据最显眼
+ 不变量被压缩
+ 复杂性被拆解
+ uncertainty 语义正确
+ label / axis / panel 都经过编辑式压缩
+ 缩小到论文页面仍然成立
```

后续若仍出现“丑 / 松散 / AI感”，优先检查 salience / suite / geometry / invariant / label engineering，而不是先改 palette。