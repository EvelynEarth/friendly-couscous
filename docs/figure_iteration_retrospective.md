# Figure Evidence 多轮返工复盘与防回归说明

> 本文是跨项目经验复盘，不是第二套绘图权威。正式绘图规则仍以 `modules/04_figure_evidence.md` 为唯一 Authority；本文只解释为什么 Q1/Q2 Figure Evidence 曾反复修改十余至二十余轮，以及后续执行时应如何利用现有 Figure Layout / Enhancement / QA 规则更快收敛。

## 1. 复盘背景

在供应链 Q1/Q2 Figure Evidence 图审中，主求解、深化分析与工作簿事实均已验收，但绘图仍多轮返工。真正的问题并不在 MATLAB 能否画图，而在**迭代模式、视觉任务定义、参考图解析、图型复杂度、坐标域、配色语义、反馈作用域、人工图审与版本冻结**没有在代码前闭合。

Q1 暴露的是“参考图只学表面、局部反馈被扩大、接受后未及时冻结”；Q2 又暴露了更深一层问题：

- 把“高级感”误解成 panel 越多、图型越新奇；
- 又把 `Less is more` 过度纠偏成“全部拆成普通单图”，导致结构信息和创意表达一起丢失；
- 把某套期刊色板当成固定模板，出现明显的“AI 配色感”；
- 把类别型结构编码与 0–500 的连续成本轴硬塞进同一 x 坐标域，导致主体被压缩；
- 在主体 geometry 尚未稳定时先修图例、脚注、标注，造成“细节越来越多，整体越来越乱”。

## 2. 本次暴露出的主要问题

### 2.1 没有先区分 Beautify 与 Redesign

外部科研美化规范常强调“美化不修改、类型保留”。这个约束只适用于 **Beautify 模式**：原图图型与证据职责已被接受，只调整颜色、字体、网格、标记、边距、标注和对齐。

当用户明确要求“重新选图型 / 重新设计证据组合”时，任务进入 **Redesign 模式**。此时允许重新选择图型或 panel 结构，但必须先通过 Figure Layout Gate / Chart Selection，并在用户认可后冻结架构。架构一旦 frozen，后续默认重新回到 Beautify/Polish，不得在代码迭代中悄悄换图型。

Q2 的多轮返工有相当一部分来自这两个模式不断混用。

### 2.2 先追求“高级图”，后确认 Primary question

曾出现为了“看起来高级”而使用 1×2、Tornado、Local Zoom、inset、额外 ribbon 等表达。高级图型本身没有价值；只有它能降低视觉搜索成本、揭示阈值、结构关系、尺度压缩或机制链时才有价值。

反过来，也不能把 `Less is more` 理解成“复杂结构一律删除”。如果左侧状态矩阵与右侧 forest 共同形成“谁中断 → 服务掉到多少”的一个视觉句子，或者“设施配置指纹 → cost-gap”必须同屏才能读出结构替代关系，那么保留这种联合结构比拆成两个普通图更高效。

### 2.3 “一种图型尽量只出现一次”被机械执行

去重复的目的，是避免**同一证据被不同图型反复复述**，不是禁止任何视觉语法再次出现。判断标准应是：

- 是否回答同一个 Primary question；
- 是否提供新的可验证结构信息；
- 是否降低比较成本；
- 是否只是把同一数字换一种画法。

不能为了“图型不重复”删掉必要的结构编码，也不能为了“高级感”重复画同一证据。

### 2.4 参考图只学了表层元素，没有拆主体骨架

用户提供 Nature-style 哑铃/森林参考后，早期迭代先模仿了空心点、实心点、图例等局部元素，却没有先识别真正决定观感的结构：

- 左侧名称/metadata strips 的宽度与主图区比例；
- 行距与主体密度；
- 每行浅灰 guide 的长度和明度；
- 空心点、实心点、区间带各自的视觉权重；
- 主体占版比例；
- 图例只解释编码，不抢版心。

因此出现“元素像了，但整体不像”的问题。

### 2.5 没有把“模仿风格”和“复制数据/语义”分开

参考图只能提供版式、视觉语法、密度、颜色职责和比例启发；数值、对象、阈值和结论必须继续来自 accepted workbooks。

参考图出现时，必须明确：

```text
Must imitate: geometry / density / color role / line-point hierarchy / legend footprint
Must preserve: current data / semantics / units / accepted conclusion
Do not copy: reference labels / values / thresholds / category structure not present in current data
```

### 2.6 配色被“期刊名”绑架，形成固定模板

外部科研绘图规范给出的 Nature / Lancet / Science / Cell 色板是候选起点，不是“选一个期刊就全局套色”。真正应冻结的是**颜色职责**：谁是主结果、风险、中断、基准、仓库结构、辅助背景。

Q2 中先后出现 Okabe-Ito 模板、Nature 皇家蓝+金黄模板、高饱和亮蓝+亮橙+亮红模板，都说明“先挑色板、后想语义”会产生明显 AI 感。

更可靠的顺序应是：

```text
数据/语义 → 视觉角色 → 明度/饱和度层级 → 再选具体 Hex
```

全图主色通常控制在 3–5 种；同一 panel 通常只保留一个主色、一个强调色与中性灰，但这是注意力预算，不是机械硬规则。

### 2.7 坐标域兼容性没有在代码前检查

Q2 F3 曾把设施配置 tiles 与 0–500 万元/年的 cost-gap 放在同一个 x 轴，导致配置矩阵被压缩到原点附近。这个错误本质不是“间距没调好”，而是**类别/元数据域与连续数值域不兼容**。

规则应是：若两个视觉编码共享行语义但 x 域不同，使用严格对齐的独立 axes / table+plot / metadata strip + numeric plot；不要用负坐标、极端 xlim 或同一连续轴硬塞。

### 2.8 没有按层级做 Figure Review

图审顺序必须固定为：

```text
A. Figure role / 图型与证据职责
→ B. 主体 geometry / 密度 / aspect ratio
→ C. 坐标域与 panel 对齐
→ D. 视觉编码（颜色、点、线、metadata）
→ E. annotation / 标题 / 轴标签
→ F. legend / 脚注
→ G. 最终 polish
```

B/C 尚未通过时，不应在 F 上投入大量精修。

### 2.9 收到局部反馈后，修改范围过大

用户说“只改前两张”“只改结构稳健性”“主要改主体而不是图例”时，后续代码曾同时变化多个视觉层。局部反馈应默认只修改对应层，其他已经通过的 Figure/panel/visual layer 临时冻结。

### 2.10 缺少用户看到之前的 Screenshot Preflight

代码静态通过并不等于图审通过。至少要在交付前做一次“按实际图窗尺寸阅读”的视觉预检：

- 标题、panel title、轴标题、脚注是否重叠；
- 文字是否压在线/点上；
- 主体是否过松或被压缩；
- metadata 是否离主图区太远；
- legend 是否超过必要面积；
- 16:9 / 4:3 / 3:2 等纵横比下是否仍保持层级；
- 主焦点是否能在数秒内识别。

只做代码层面的 `Position` 数值检查不够。

### 2.11 没有及时冻结人工认可结果

一旦用户明确说“这张可以”“确定这个版本”“不要再动”，应立即记录 accepted/frozen、canonical script、SHA-256、冻结范围，并清理 active 项目目录中的旧 `.m` / wrapper。后续只有显式 reopen 才允许修改。

## 3. 外部科研绘图规范如何正确吸收

外部顶刊级美化规范可抽象为十条长期有效原则：

1. Data First：数据是主角；
2. Less is More：删冗余，不删必要结构；
3. Color Restraint：主色有限、角色清楚；
4. High Contrast：主数据与背景层级明显；
5. Font Consistency：字体与字号梯度统一；
6. Pixel-Perfect Alignment：多 panel / metadata 严格对齐；
7. Annotation Hierarchy：主标题 > 轴 > 数据标签 > 脚注；
8. Aspect Ratio：比例服务阅读任务；
9. Accessibility：色盲、灰度和打印可区分；
10. Reproducibility：完整代码可复现。

其中“类型保留”应放在 Beautify 模式；若任务已经明确进入 Redesign，则图型可在冻结前调整，但数据、结论和事实来源不能漂移。

## 4. 后续 Figure Evidence 标准收敛流程

### Step 0 — Iteration Mode Gate

先写：

```text
Mode: beautify / redesign
Architecture status: proposed / approved / frozen / reopened
```

- `beautify`：不改图型、证据职责、数据系列；
- `redesign`：允许重新选图，但先审图型架构；
- `frozen`：后续默认只能 polish，除非用户显式 reopen。

### Step 1 — Evidence Architecture Freeze

每张 Figure 先锁定：Core conclusion、Evidence level、Primary question、Figure role、Chart type、panel necessity。先决定“为什么需要这张图”，再写 MATLAB。

### Step 2 — Reference Anatomy Contract

参考图存在时，记录：

```text
Canvas / aspect ratio
Body occupancy
Row/column pitch
Metadata width
Guide/background strength
Marker / line hierarchy
Color roles
Annotation budget
Legend footprint
Must imitate / Must preserve / Do not copy
```

### Step 3 — Layout & Coordinate-Domain Gate

检查每个 panel/axes 的 x/y 是否属于同一数据域。共享行语义但数值域不同的对象，优先使用 aligned axes，而不是硬塞一个坐标系。

### Step 4 — Color Role Contract

先定义角色，再选色值：

```text
Primary result:
Risk / failure:
Baseline / reference:
Structural category:
Context / inactive:
Semantic background:
```

禁止因为“Nature/Science 风格”就机械套固定 Hex。

### Step 5 — Body-first Review

按“图型 → geometry → 坐标域/对齐 → 颜色编码 → 标注 → legend → polish”逐层通过。一次 redraw 原则上只改一个主要视觉层。

### Step 6 — Screenshot Preflight

在用户看到之前，按实际图窗尺寸检查遮挡、密度、留白、阅读顺序与主焦点。若主体仍明显失衡，不交付下一版。

### Step 7 — 三轮不收敛先诊断

同一 Figure 连续约 3 个 redraw round 仍未明显收敛时，下一步默认不是继续 v4/v5/v6，而是输出 Reference/Current mismatch table，只修最高优先级 mismatch。

### Step 8 — 接受即冻结并清理

```text
accepted Figure
→ 记录 frozen scope
→ 同步 canonical 问题X求解/qX_plot.m + SHA-256
→ 清理 active 项目中的实验 .m / wrapper / 近似命名旧入口
→ 后续只有显式 reopen 才能修改
```

## 5. Q2 最终案例留下的可复用经验

- **F1 Waterfall**：一级结论本身就是加法分解，简单图最优，不为高级感强行复合。
- **F2 中断矩阵 + benchmark forest**：两者共享场景行并共同回答“谁中断 → 服务损失多少”，属于一个融合视觉句子，保留联合结构比拆成普通单图更高效。
- **F3 Panel A**：设施配置指纹与 cost-gap 强相关，但类别 metadata 与连续成本轴不可共域，应使用对齐的独立 axes。
- **F3 Panel B**：敏感性 profile 与 regime ribbon 共享同一参数轴，可形成强配对；ribbon 只汇总真实离散点，不能把离散测试点包装成整个连续区间已证明稳定。
- **配色**：真正高级不是颜色更多，而是颜色职责更少、更稳定，辅助元素退后，主焦点一眼可见。

## 6. 最终经验

绘图返工的根因不是“不会某个高级图”，而是没有在代码前冻结**迭代模式 + 证据架构 + 主体版式 + 坐标域 + 颜色职责 + 参考图视觉合同**。

真正的高级感不是 panel 数量，也不是固定 Nature 色板；它来自**结构信息密度、阅读路径、对齐、克制和可复现性**。后续 Q3 及其他赛题的 Figure Evidence 应直接从这套收敛流程开始，不再回到“先画一版再看”。
