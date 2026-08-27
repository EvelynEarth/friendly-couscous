# Journal Figure Mastery v2（高级顶刊科研绘图融合层）

> 目的：在现有 HSK / Module 04 / Top-tier Figure Skill 之上，再增加一层真正接近顶刊编辑部与高级 visualization judgment 的决策规则。  
> 本文件不建立第二套事实源；数据真值、Evidence level、Primary question 仍由 `modules/04_figure_evidence.md` 与 accepted workbook 决定。

---

## 0. 顶刊 Figure 的真正问题不是“画得漂亮”，而是“让最重要的证据最容易被正确看见”

本层吸收并项目化以下思想：

- Nature Research Figure Guide：panel 要 neat、space-efficient、按内容决定尺寸；减少无意义白区；数据可读性优先；
- Nature Methods：Design of data figures / Layout / Salience / Salience to relevance / Labels and callouts / Axes, ticks and grids / Plotting symbols / Simplify to clarify / Unentangling complex plots；
- Nature 的 visual communication framework：视觉设计必须考虑 audience 和 communication context；
- Icarus Figures：Dataset + Claim、四轴质量条、mechanical floor + judgment pass、hero/drop test；
- scientific-publication-plotter：style 参数集中管理、final-width 思维、dense scatter / map 简化；
- Crameri scientific colour maps：连续色图的感知均匀性与 CVD/grayscale 可读；
- 本项目 Q1–Q3 的长期返工经验。

核心定义：

```text
Publication-grade Figure
= Evidence architecture
+ Perceptual accuracy
+ Salience relevance
+ Editorial compression
+ Reproducibility
+ Paper-family consistency
```

颜色、字体、线宽只是最后一层。

---

# 1. Figure Suite Architecture Gate（整篇论文层，而不是单图层）

过去一个重要问题是：单张图看似合理，但 Q1/Q2/Q3 放在一起会重复图型、重复证据或风格漂移。

因此正式设计单张 Figure 前，先设计整套 Figure Suite。

每个 Figure 必须登记：

```text
Figure ID
Question / subsection
Evidence level
One-sentence claim
Hero evidence
Visual grammar
Why this grammar is unique in the suite
Paper-family anchor inherited
Expected manuscript position
```

## 1.1 Suite redundancy test

若两张 Figure 满足以下任两项，应考虑合并、降级或替换：
- 回答几乎同一句话；
- 使用相同数据，只是换图型复述；
- 都是同一种 aligned dot / bar / heatmap，但没有视觉任务上的必要；
- 一张删掉后正文论证完全不受影响。

## 1.2 Suite diversity ≠ 为了多样而多样

同一图型可以重复，但必须满足：

```text
same perceptual task
+ same grammar truly remains best
+ repetition improves paper-level consistency
```

禁止为了“每张都不一样”强行使用 Sankey / ternary / 3D / radar。

---

# 2. Claim → Visual Task → Grammar：三层映射

禁止从“我会画什么图”出发。

每张 Figure 必须先把 claim 翻译为视觉任务：

| Claim 类型 | 读者真正要做的视觉任务 | 优先 grammar |
|---|---|---|
| 谁更大 / 更优 | 精确比较位置/长度 | aligned dot / interval / forest |
| 改了多少 | 读取 delta | slope / dumbbell / delta forest |
| 为什么选这个方案 | 同时比较多维 trade-off | aligned metadata + quantitative panels / Pareto |
| 何时失效 | 找 threshold / boundary | regime map / threshold slice |
| 哪个因素主导 | 比较贡献量 | sorted contribution / tornado / signed decomposition |
| 哪里不同 | 定位异常 /空间结构 | heatmap / map / residual field |
| 分布怎样 | 读取 spread / skew / overlap | raw points / ECDF / violin / raincloud |
| 机制如何发生 | 追踪状态、资源或约束转移 | staged flow / real network / mechanism schematic |
| 是否稳健 | 读取结构是否变、范围多大 | phase/regime / small multiples / transition strips |
| 模型是否可信 | 看 fit / residual / calibration / enumeration gap | diagnostic pair / certificate figure |

图型名称只是 grammar 的实现，不是设计起点。

---

# 3. Salience–Relevance Gate（显著性必须服务相关性）

Nature Methods 强调：最醒目的对象若不是最重要对象，会误导读者。

每张 Figure 必须写：

```text
Most relevant object = ?
Most visually salient object = ?
```

二者必须相同或高度一致。

## 3.1 Salience budget

每个 axes 默认：
- 1 个 primary salient object；
- 最多 1 个 secondary witness；
- 其余全部降权为 context。

显著性通道按优先级使用：
1. position / alignment；
2. marker fill / size 的有限变化；
3. line weight；
4. one accent color；
5. annotation。

禁止同时对同一对象使用：超大 marker + 鲜艳颜色 + 粗线 + 彩色文字 + 背景色块。

## 3.2 Relevance inversion FAIL

以下直接 FAIL：
- context 背景色比数据更抢眼；
- 大标题比 hero data 更醒目；
- legend 比结果本身更显眼；
- baseline/invariant 占据最大面积而真正变化被压缩；
- decorative flow arrows 比真实数值更醒目。

---

# 4. Editorial Compression Gate（像顶刊的重要来源：删掉不承担论证的东西）

顶刊 Figure 的“高级”常来自压缩，而非叠加。

每个视觉元素必须回答：

```text
如果删掉它，读者会失去哪条证据？
```

若答案是“没有，只是不那么丰富”，删掉。

优先删：
- 重复 title；
- 单系列 legend；
- 重复的 baseline block；
- 全部精确数值标签；
- 无数据语义的边框/背景；
- 重复 axis title；
- 不参与 claim 的 supporting panel。

### Figure text hierarchy

```text
数据标记 / 阈值
> axis labels
> panel label + short subtitle
> optional figure title
> decorative explanation（通常删除）
```

最终 journal mode 可完全不在图内放大标题，由 caption 承担。

---

# 5. Complexity Decomposition Gate（复杂图不要硬塞一个 overview）

吸收 Nature Methods “Unentangling complex plots” 思路：复杂数据若尺度不同、线条纠缠，经过良好设计的小 multiples 往往优于一个巨型 overview。

触发条件：
- >4 条高度重叠曲线；
- 不同对象的 y-scale 差异 >5–10 倍；
- 一个 panel 中同时出现 3 种以上视觉编码；
- 读者需要 legend ping-pong 才能追踪对象；
- ROI 差异在全局图中不可见。

候选解决：
- small multiples；
- overview + one justified zoom；
- hero + witness column；
- progressive cropping；
- direct labels；
- 对 context 灰化，只突出 claim-bearing series。

注意：small multiples 也不能机械 equal grid。每个 panel 的尺度差异必须明确、可比较。

---

# 6. Uncertainty Semantics Gate（数模论文必须区分“哪一种不确定性”）

不得把所有 uncertainty 都画成 CI band。

先分类：

| 不确定性类型 | 典型来源 | 合法视觉表达 |
|---|---|---|
| Statistical | 抽样/重复实验 | raw points, CI, distribution, bootstrap interval |
| Scenario | 离散灾害/情景 | scenario points, envelope, small multiples, weighted contribution |
| Parametric | 参数扰动 | sensitivity curve, interval, regime map, tornado |
| Robust/Feasible | 可行域/不确定集 | feasible region, robust frontier, decision region |
| Numerical | solver tolerance / residual | residual, gap, convergence, feasibility certificate |
| Forecast | 预测误差 | fan/ribbon, prediction interval, calibration |

硬规则：
- deterministic optimization 不伪造 statistical CI；
- scenario range 不叫 95% CI；
- numerical tolerance 不用“误差棒”伪装成统计不确定性；
- 参数扫描如果只是离散测试点，不画成连续置信带。

---

# 7. Invariant Subtraction Gate（不变量不能占主体）

若某一分量在所有比较对象中近似不变，先剥离：

```text
Total = invariant baseline + informative residual
```

图中优先画 informative residual。

适用：
- 固定 75% 网络覆盖；
- 所有方案共同启用的设施；
- 所有场景相同的常数成本；
- 各阶段共同基线。

不变量可用：
- 一句黑色 reference text；
- 极轻 baseline；
- metadata strip；
- caption。

禁止让不变量成为最大彩色块。

---

# 8. Axis & Navigation Ink Gate

Nature Methods 建议导航元素应清晰但不抢数据。

默认：
- tick outward；
- 轴线和 tick 可见；
- major grid 默认关闭；若读数任务真的需要，使用极轻 major grid；
- minor grid 默认禁止；
- axis span 尽量贴合证据域；
- units 永远在 axis label；
- 0 baseline 只有在语义重要时强调；
- truncated axis 必须不制造夸张差异。

### Bar / area 特别规则

bar 用长度编码并从 0 起点；若不从 0，改用 dot/interval/point-range。

---

# 9. Label Engineering Gate

吸收 Nature Methods Labels and callouts：标签不是“放上去就完了”，而是版式结构。

## 9.1 Refactor common text

若多行标签共享前缀/单位，不要重复写满：
- 把共享词放到列标题；
- row label 只留差异部分；
- 单位放 axis title；
- explanation 放 caption。

## 9.2 Direct label 策略

优先 direct label，但不默认使用彩色文字。

Nature-style 优先：
- 黑/深灰文字；
- 旁边使用对应 marker / keyline / leader；
- 只有在确实增强识别且 contrast 足够时才使用系列色文字。

## 9.3 Annotation line discipline

callout line：
- 长度和角度尽量一致；
- 不交叉；
- 文字基线对齐；
- 不穿过主数据；
- 同一 figure 中 arrowhead / leader 风格一致。

---

# 10. Plotting Symbol Hierarchy Gate

符号需要形成“自然层级”，降低 legend lookup。

优先组合：

```text
primary = filled marker + solid line
secondary = open marker + solid/thin line
context = small gray marker / thin line
threshold = rule / boundary
```

不要给 5 个系列随机分配 5 种高饱和色。

B&W 测试时，应通过 fill / marker / line style 保持可区分。

---

# 11. Continuous Color Gate

连续色图必须先确认数据语义：
- sequential；
- diverging；
- cyclic。

默认使用 perceptually uniform scientific maps（如 Crameri 系列或等效的 perceptually uniform map）。

禁止：
- jet / rainbow / HSV；
- 用离散类别 palette 表连续量；
- 无业务中心却使用 diverging map；
- 为了让分布“更丰富”随意做 quantile recoloring，若这样会破坏物理量的数值距离含义。

注意：外部 `scientific-publication-plotter` 提倡 quantile color split；本项目**不默认采纳**，因为数模图常需要保留物理/经济量的绝对间距。只有 Primary question 明确是“分位等级”时才允许 quantile transform。

---

# 12. Final-width-first + Dual-scale Review

顶刊最终版面是 89/183 mm 级别，而 MATLAB Review window 通常更大。因此必须同时检查两种尺度：

### A. Review scale
用户在 MATLAB 图窗直接审图：中文必须清楚、不能小字假顶刊。

### B. Final-width scale
accepted 后：
- 单栏 / 双栏宽度；
- 缩小后的线、marker、tick、label；
- caption 后的整页平衡；
- vector editability。

### Thumbnail test
把 Figure 缩到约 25–35% 视觉尺寸或页面缩略图：
- hero 仍然是谁？
- 主趋势/阈值仍可辨吗？
- 若只剩标题和大色块可见，则失败。

---

# 13. Dense Scatter / Large-N Gate

大 N 点图：
- 不直接把数十万点全部矢量化；
- 可用 transparency、hexbin、2D density、rasterized data layer + vector labels；
- 不因导出 PDF 而制造巨大文件；
- 如果 raw points 本身是证据，保留代表性与密度结构。

地图/边界同理：只保留能支持 claim 的空间分辨率，避免高精行政边界成为视觉噪声。

---

# 14. Mechanism / Framework Figure 与 Data Figure 分流

Data Figure：必须由 accepted data + 可复现绘图库生成。

Mechanism / Framework Figure：允许示意绘制，但必须嵌入真实方法对象，而不是 generic boxes-and-arrows：
- decision region；
- network topology；
- optimization state；
- actual distribution；
- real before/after pattern；
- equation / constraint relation。

机制图的“高级”来自方法对象本身，而不是科技发光、3D CG、装饰箭头。

---

# 15. Judgment Pass 2.0（正式 release candidate 前）

机械检查通过后，还要人工回答：

### Depth
遮住 caption，图能不能说出“为什么 / 何时 / 哪里失效”？

### Elegance
Drop test 后还有没有冗余 panel / legend / text？

### Unimpeachable
轴、单位、数据口径、不确定性语义、颜色、阈值都能否经得起质疑？

### Visible gap
0.5 秒看过去，是论文 Figure 还是 dashboard / homework / AI infographic？

### Salience relevance
第一眼看到的是不是最重要的证据？

### Suite coherence
与同一问/整篇论文其它 Figure 是否属于同一 figure family，且没有重复讲同一句话？

6 项任一明显失败，不进入 MATLAB delivery。

---

# 16. 顶刊高级 Figure 的最终执行链

```text
Paper-level Figure Suite
→ Scope / Source / Claim lock
→ Audience + reviewer question
→ Claim-to-visual-task mapping
→ >=3 grammar candidates
→ Candidate scoring
→ Salience-relevance plan
→ Invariant subtraction
→ Hero / witness / drop test
→ Geometry sketch
→ Real-data prototype v0 (body only)
→ Render review: geometry + complexity
→ Prototype v1 (hierarchy + labels + restrained color)
→ Grayscale / CVD / thumbnail review
→ Mechanical lint
→ Judgment Pass 2.0
→ User architecture review
→ MATLAB translation
→ MATLAB screenshot fidelity review
→ Final-width embedded-page review
→ accepted / frozen
```

这条链优先于任何“Nature风 / Science风 / Cell风”的表面模仿。