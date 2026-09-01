# Journal Palette Contract（顶刊科研图配色合同）

> 目的：把“配色审美”从临场挑色升级为可复用的科研视觉决策。  
> 本合同只负责 **palette / color role / contrast / colormap / palette-only iteration**；图型、版式、证据层级和数据事实源仍由 `modules/04_figure_evidence.md`、`top_tier_scientific_figure_skill.md` 与 Figure Contract 决定。

---

## 0. 核心原则：顶刊配色不是某一组 Hex

```text
顶刊配色 ≠ Nature 蓝
顶刊配色 ≠ 全灰
顶刊配色 ≠ 低饱和莫兰迪
顶刊配色 ≠ 大面积 pastel
顶刊配色 ≠ 高饱和越醒目越好

顶刊配色 =
语义角色稳定
+ 对比度足够
+ 显著性与科学重要性一致
+ CVD / grayscale 可辨
+ 与图型、面积和最终版面匹配
+ 整篇 Figure Suite 一致
```

“Nature / Science / Cell / JAMA 风”只能作为 **paper-family reference**，不能把一个品牌名当成唯一色板。出版社规范通常更关注可读性、色觉缺陷、印刷和数据诚实；很多网上所谓“期刊色板”只是 **inspired palette**，不得冒充官方强制色号。

---

# 1. Mutation Scope Lock：用户说改配色，就只改配色

每次用户反馈先分类：

```text
palette_only
rendering_only
annotation_only
geometry_only
grammar_redesign
full_redesign
```

若用户明确说：
- “只改颜色”；
- “这个图型可以，配色不行”；
- “布局别动”；
- “不要改蓝色那张图，只改配色”；

则锁定：

```text
chart grammar      = frozen
panel count        = frozen
layout / geometry  = frozen
axis domain        = frozen
annotation content = frozen
source data        = frozen
```

允许改动仅限：
- palette tokens；
- colormap；
- alpha；
- 因背景明暗变化而必须调整的文字/marker edge 对比色；
- legend 中对应色块。

**禁止**借“去 AI 味 / 顶刊化”擅自把 heatmap 改 glyph matrix、把 region fill 删除、增删 panel、改图型或改数据编码。若判断结构本身也有问题，只能单独提出建议并等待用户批准 `grammar_redesign`。

---

# 2. Palette Purpose Gate：先判断颜色在图里承担什么任务

配色前先登记：

```text
Color task = categorical | ordinal | sequential | diverging | cyclic | semantic region | focus-context
Number of semantic roles = ?
Largest colored area = ?
Primary salient object = ?
Paper-family anchor = ?
```

## 2.1 Categorical / discrete

适合：方案、情形、类别、执行/不执行、模型族。

优先：
- 2–4 个关键类别：高可分辨、偏中深色的定性色；
- 大量类别：优先 shape / line style / small multiples / direct label，不能仅靠 8–12 个 hue 硬分。

颜色不是数量通道。

## 2.2 Ordinal / sequential

适合：排名、概率、密度、误差大小、强度。

必须使用**单调感知顺序**的 colormap：
- Crameri scientific colour maps；
- ColorBrewer sequential；
- viridis-family 或其它经过验证的 perceptually uniform map。

不得用 qualitative palette 表示 rank/连续量。

## 2.3 Diverging

只有存在有科学意义的中心值时使用，例如：
- 0；
- baseline；
- 正负误差；
- 收益/损失分界。

无真实中心时禁止为了“丰富”使用 diverging palette。

## 2.4 Semantic region / decision region

区域色必须同时满足：
- 两区/多区肉眼快速区分；
- 边界线仍是最清楚的数学对象；
- 区域文字可读；
- 大面积色块不产生 pastel washing 或 dashboard 感。

不要机械把所有区域都混入 70–85% 白色。alpha / white-mix 必须根据面积、contrast 与 screenshot review 动态选择。

---

# 3. Journal Palette Research Gate：用户要求“顶刊配色”时必须先比较

当用户明确要求：
- 顶刊论文配色；
- Nature/Science/Cell/JAMA 风；
- “好好搜配色”；
- “积累审美”；

不得立即拿一套常用蓝橙结束。先做小型 palette benchmark。

至少比较 3 类来源：

### A. 出版社 / 顶刊视觉规范
用于学习：
- contrast；
- CVD；
- grayscale；
- typography 与 color salience；
- 对 rainbow / red-green / colored text 的限制。

### B. Journal-inspired qualitative palettes
可参考 ggsci 等成熟实现中的：
- NPG-inspired；
- AAAS-inspired；
- JAMA-inspired；
- NEJM-inspired；
- Lancet-inspired。

必须标注为 **inspired palette**，除非有出版社官方色号证据。

### C. Scientific colormaps
连续/序数图优先：
- Fabio Crameri scientific colour maps；
- ColorBrewer；
- viridis-family / cividis 等经过验证的感知均匀色图。

### Benchmark 输出

```text
candidate palette A
candidate palette B
candidate palette C

for each:
- contrast
- AI/pastel risk
- CVD / grayscale robustness
- fit to current colored area
- fit to paper-family anchor
- final-width readability
```

若用户已经给出截图，应把候选颜色映射到**当前实际图**评估，不能只看色卡。

---

# 4. Aesthetic Density Gate：防止“太浅 AI 味”与“太黑压图”两个极端

## 4.1 Pastel washing FAIL

以下组合高风险：
- 20–40% alpha 的浅蓝/浅橙铺满大面积矩阵；
- 多个区域都混入 70–85% 白色；
- context、primary、secondary 都是浅色；
- 文字与背景 contrast 不足；
- 0.5 秒只看到“柔和配色”，看不到证据。

用户明确评价“太浅、像 AI”时，默认优先：
1. 提高 chroma / 降低 white-mix；
2. 加深 context gray；
3. 保留白底但提高数据对象的墨色；
4. 再比较另一套 journal-inspired palette。

不得直接把所有颜色删成全灰，除非用户批准。

## 4.2 Over-dark FAIL

若：
- 大面积深色导致文字反色过多；
- 黑块比数据结构更醒目；
- 彩色区域压过边界/误差线；
- 打印后层次糊成一片；

则降低 fill opacity/chroma，但保留数据对象 contrast。

目标是 **ink-like, not washed-out; clear, not neon**。

---

# 5. 推荐 Palette Families（参考库，不是硬模板）

## 5.1 两级/三级重点比较

### JAMA-inspired family
适合：经济、决策、管理、医学统计风格的中深色正文 Figure。

常用角色候选：
- deep blue-gray `#374E55`
- warm orange `#DF8F44`
- cyan `#00A1D5`
- brick `#B24745`
- muted green `#79AF97`
- purple `#6A6599`
- brown-gray `#80796B`

优势：比高亮科技蓝/鲜红更成熟；比大量 pastel 更有“墨色”。

### Okabe–Ito / Wong family
适合：少类别、高可访问性、色觉缺陷友好。

常用角色候选：
- blue `#0072B2`
- vermillion `#D55E00`
- orange `#E69F00`
- bluish green `#009E73`
- sky blue `#56B4E9`
- reddish purple `#CC79A7`

优势：类别可分辨性强；缺点：直接大面积铺色时可能显得过亮，应结合面积控制。

### Paul Tol muted / bright 等成熟 CVD palette
可作为定性候选，但仍需在当前图中测试，不得机械套用。

## 5.2 Sequential / ordinal

优先从 Crameri / ColorBrewer / cividis 中按语义选择。

必须检查：
- luminance monotonicity；
- 最浅端是否在白底上消失；
- 最深端是否压掉文字；
- colorbar 在最终宽度是否仍能读出顺序。

若最浅端近白导致“奶油浅色/AI感”，可以**裁剪 colormap 的端点范围**，而不是换成无序多色。

## 5.3 Diverging

优先使用有中性色中心的 CVD-friendly diverging map，如 Crameri `vik/broc` 或等价色图；必须有真实 center。

---

# 6. Area-aware Color Rule：同一个 Hex 在不同面积上不是同一种视觉重量

同一颜色用于：
- 一个 7 pt marker；
- 一条 1.5 pt line；
- 30% panel 的 fill；

视觉重量完全不同。

所以配色合同必须记录：

```text
role
hex / RGB
object type
approximate colored area
alpha
text contrast
```

规则：
- marker/line 可使用更纯、更深的主色；
- 大面积 fill 通常降低 chroma 或 alpha，但不能自动淡到不可辨；
- context gray 必须足够深，不能所有 context 都变成“几乎看不见的浅灰”；
- region map 的数学边界通常用黑/深灰保持权威性。

---

# 7. Paper-family Palette Anchor

一旦用户明确表示：
- “这套颜色还行”；
- “这个配色保留”；
- “这张最像论文”；

登记为 `palette_anchor`。

后续 Figure 继承：
- primary color；
- secondary/risk color；
- context gray；
- sequential/diverging colormap family；
- saturation level；
- fill alpha range。

允许不同 grammar 使用不同面积/alpha，但同一语义不应随图重新换色。

用户只否定某一张图的颜色时，默认先做该图局部 palette iteration，不推翻全篇 anchor。

---

# 8. Palette Screenshot Review

正式冻结前至少过：

### Review scale
- 文字与 fill contrast 足够；
- primary / secondary / context 一眼可分；
- 颜色不比数据结构更抢眼；
- 不出现“浅色洗白”或“整块荧光”。

### Thumbnail / final width
- 25–35% 缩略后 primary 仍可见；
- context 不消失；
- heatmap/region 的类别或顺序仍可辨；
- legend swatch 不成为主要视觉对象。

### Grayscale / CVD
- 主要结论不能只靠 hue；
- 关键类别应有 marker/fill/line style 冗余；
- sequential map 灰度仍有大致顺序。

---

# 9. MATLAB Palette Implementation Rules

颜色 token 集中定义，不在绘图段散落魔法 RGB：

```matlab
cPrimary = [...];
cSecondary = [...];
cContext = [...];
cBoundary = [...];
```

`palette_only` iteration 时：
- 只替换 token / colormap / alpha；
- 不使用字符串/正则大范围改写图型代码；
- 若必须改变反色文字，只改 contrast-dependent text color；
- 修改后做括号、字符串、变量名和未定义 palette token 静态检查；
- 不因换色造成新的 MATLAB 语法错误。

---

# 10. Palette Contract 最小记录

```text
Palette mode: categorical / sequential / diverging / semantic-region
Mutation scope: palette_only / full_redesign
Paper-family anchor:
Primary:
Secondary:
Context gray:
Region colors:
Colormap:
Alpha range:
Color-area notes:
CVD fallback:
Grayscale fallback:
Reference provenance: official guideline / inspired palette / scientific colormap
Screenshot review status:
Final-width status:
```

没有这些记录时，不把“顶刊配色”当作已完成判断。
