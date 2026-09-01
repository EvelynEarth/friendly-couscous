# Figure Skill Index（科研绘图统一入口）

本目录不建立独立于 `modules/04_figure_evidence.md` 的第二套 Figure 决策权威。Module 04 仍是事实源、Evidence level、Primary question、Layout/Enhancement Gate 与论文闭环的上位规则；机制/物理图的实现路由由 `mechanism_figure_contract.md` 承担，不改变 Data Figure 的数值事实边界。

## 统一执行顺序

```text
modules/04_figure_evidence.md
→ Figure Purpose / role
→ Figure Suite Manifest（若一个问题/全文有2张以上图）
→ Figure Contract / Evidence level / Primary question
→ [mechanism/physical] templates/figure/mechanism_figure_contract.md
→ [data/result] templates/figure/top_tier_scientific_figure_skill.md
→ templates/figure/journal_figure_mastery_v2.md
→ templates/figure/journal_palette_contract.md
→ templates/figure/figure_iteration_control.md
→ templates/figure/chart_selection.md（Advanced-first, evidence-governed）
→ templates/figure/scientific_figure_skill_landscape.md（需要外部方法论时）
→ templates/figure/figure_skill_evals.md（Skill修改后做回归检查）
→ prototype / candidate
→ internal render-review：grammar / geometry / complexity / identity
→ hierarchy / labels / scientific color
→ grayscale / CVD / thumbnail test
→ templates/figure/anti_ai_figure_gate.md
→ mechanical lint + Judgment Pass 2.0
→ release candidate gate
→ [MATLAB data figure] templates/matlab/README.md
→ [mechanism] image generation / Draw.io / vector route
→ screenshot/preview fidelity review
→ templates/figure/result_figure_qa.md（数据结果图）或 mechanism closure review
→ final-width / embedded-paper QA
→ accepted / canonical / frozen
```

若同一 Figure 曾被用户退回过、用户评价“丑 / AI感 / 松散 / 没学到参考图精髓”，还必须先读：

```text
templates/figure/figure_failure_postmortem_2026-08.md
```

禁止在没有 mismatch diagnosis 的情况下继续机械递增 vN。

若用户明确只要求“改配色”，则先读 `journal_palette_contract.md` 并锁定 `mutation_scope=palette_only`；不得因为 anti-AI / journal-style 判断擅自重构图型。

---

## 当前核心文件

| 文件 | 作用 |
|---|---|
| `top_tier_scientific_figure_skill.md` | 融合后的 Data Figure 主 Skill：Figure Suite、claim→visual task、候选 grammar、salience、hero/drop、geometry、render-review、Judgment Pass 2.0 |
| `mechanism_figure_contract.md` | 机制/物理/场景图专用：是否需要画、image-generation/Draw.io/tool router、短标签、少图标、零交叉布线、图例、XML preflight、mechanism closure |
| `journal_figure_mastery_v2.md` | 高级顶刊层：整篇图组、Salience–Relevance、Editorial Compression、Uncertainty Semantics、Invariant Subtraction、Complexity Decomposition、mutation scope、thumbnail test |
| `journal_palette_contract.md` | 顶刊配色专用：palette-only 修改边界、期刊配色调研、journal-inspired palette、Crameri/ColorBrewer、pastel washing / over-dark、palette anchor、MATLAB换色安全门 |
| `figure_suite_manifest.md` | 整篇论文 Figure 架构表：防止重复 claim、重复 grammar、风格漂移，并登记 paper-family anchor |
| `figure_skill_evals.md` | 28个历史/对抗性回归测试：稀疏scatter、假CI、AI卡片、机制图文字/图标/布线、Draw.io XML、串问、advanced-chart漏用/滥用、palette-only越权、浅色AI感、MATLAB换色语法错误等 |
| `figure_iteration_control.md` | 绘图状态机与发布硬门：scope lock、真实数据 prototype、自审、用户迭代预算、MATLAB preflight、唯一命名、freeze/reopen |
| `figure_failure_postmortem_2026-08.md` | 历史绘图复盘：高频失败模式与禁止重犯规则；只抽象经验，不作为新题数据事实源 |
| `scientific_figure_skill_landscape.md` | Nature / Nature Methods / Icarus / matlab-plot-skill / scientific-plotting-skill / gramm / Crameri 等方法论与采用边界 |
| `anti_ai_figure_gate.md` | 去 AI 信息图 / dashboard / PPT 味硬门；区分 Data Figure 与 Mechanism Figure，并增加 palette-only mutation scope |
| `journal_figure_research_notes.md` | 顶刊官方规范与方法论研究底稿 |
| `journal_figure_research_notes_v2_2026-08-28.md` | 二次深挖：salience、labels、complexity、uncertainty、外部 skills 的新增吸收与拒绝边界 |
| `journal_figure_case_patterns.md` | 真实顶刊 Figure 结构模式案例库 |
| `chart_selection.md` | Advanced-first 的 Claim→Visual Task→Grammar 图型选择索引 |
| `figure_enhancement_patterns.md` | Local Zoom / Small Multiples / Focus Highlighting / Semantic Background / Composite Diagnostic / 3D |
| `result_figure_contract.md` | 单张结果图 Figure Contract |
| `result_figure_qa.md` | 从 suite / scope / truth 到 final-width / freeze 的最终 QA |

---

## 当前 Publication-grade 质量条

```text
Depth
+ Elegance
+ Unimpeachable
+ Visible gap
+ Salience relevance
+ Suite coherence
+ Scope fidelity
```

解释：
- **Depth**：图里能读出机制/阈值/为什么；
- **Elegance**：一个 claim、一个 hero、通过 drop test；
- **Unimpeachable**：数据诚实、轴诚实、不确定性语义正确、可复现；
- **Visible gap**：0.5 秒像论文正文，不像 homework/PPT/dashboard/AI；
- **Salience relevance**：第一眼看到的就是最重要证据/机制路径；
- **Suite coherence**：整篇 Figure 属于同一个 paper family，又不重复讲同一句话；
- **Scope fidelity**：本轮只修改用户明确授权的范围，`palette_only` 不偷换 grammar/layout。

---

## 必须长期记住的纠偏

```text
顶刊感 ≠ 小字体 + 大留白 + 低饱和
顶刊感 ≠ Nature配色 + 大标题 + 卡片式结论
顶刊感 ≠ 把所有颜色混入大量白色形成 pastel
顶刊感 ≠ 每张图都“高级图型”
但：重要结果图必须主动搜索高级 grammar，不能因为保守而机械退回 bar/line

用户不是第一层 linter。
结构失败时禁止靠换色续命。
但用户明确只让改配色时，也禁止越权改结构。
不变量不应占主体。
最醒目的对象必须是最重要的证据。
机制图的第一视觉对象必须是真实对象/路径，不是文字/图标。
新交付文件必须新命名。
已 frozen Figure 不得静默重构。
“顶刊配色”先做 palette benchmark，不存在唯一 Nature 官方色板。
```

---

## Advanced-first Figure Selection

Data/result Figure 默认先从读者任务出发主动搜索高级候选：forest、dumbbell、raincloud、regime map、Pareto、tornado、hexbin、waterfall、Sankey、ternary、small multiples、calibration/residual composite、spatial/vector field 等。

不是“越高级越好”，也不是“高级图谨慎少用”。规则是：

```text
advanced candidate 有清晰信息增益 → 优先使用
无增益 / 误导风险更高 → simpler fallback
```

每张重要 Figure 记录 `why advanced / simpler fallback / reviewer risk`。

---

## Mechanism / Physical Figure Router

```text
对象形态/空间/物理过程是理解重点
→ image generation first
→ 中文/箭头/逻辑/AI味/可编辑性失败 → Draw.io

规则结构/状态机/反馈回流/精确中文/需要XML
→ Draw.io first
```

MATLAB/Python 不再作为复杂机制图默认工具。机制图强制短标签、少图标、白底克制配色、主路径/异常/回流分层，并以零 connector crossing / through-text / arrow-overlap 为 review-ready 目标。

---

## Palette / Color Router

```text
用户只说“改配色”
→ mutation_scope = palette_only
→ 冻结 grammar / layout / axis / annotation / data
→ journal_palette_contract.md
→ 只改 palette token / colormap / alpha / contrast

用户说“顶刊配色，好好搜”
→ 比较 publisher guideline + journal-inspired palette + scientific colormap
→ 至少3个候选
→ 在真实 Figure 面积上审 contrast / AI risk / CVD / final-width
```

大面积色块、marker、line 的颜色不能只看 Hex；必须按 colored area 判断视觉重量。用户说“太浅像AI”时，不默认全灰，也不默认删色，而是先提高主色墨色、降低 white-mix、加深 context gray 或更换成熟 palette family。

---

## Figure Suite First

当一个问题有两张以上 Figure，或开始全文绘图时，先填写：

```text
templates/figure/figure_suite_manifest.md
```

必须检查：
- 是否两张图回答同一句话；
- 是否同一数据只是换图型复述；
- 是否无意识重复同一种 grammar；
- 是否 paper-family style 漂移；
- 是否 L3/L4 supporting figure 抢走 L1 hero 的视觉权重；
- 是否存在高级 grammar 明显更适合却未评估。

---

## Skill Regression Evals

每次对绘图 Skill 做较大修改后，检查：

```text
templates/figure/figure_skill_evals.md
```

当前包含 **28 个**对抗性案例。目标不是“文档看起来完整”，而是保证 Skill 在历史高频失败上做出正确判断。

如果任一错误架构仍能轻易被流程批准，说明 Skill 还没有修好。

---

## Paper-family anchor

当用户明确指出某张 Figure“有期刊味 / 这张可以 / 保留 / 这套颜色还行”，立即登记：

```text
paper_family_anchor
palette_anchor
```

后续 Figure 优先继承：
- font family；
- stroke weight；
- primary/secondary/risk/context 颜色职责；
- marker/node 尺度；
- annotation density；
- panel/node gap；
- whitespace rhythm；
- direct-label / legend strategy；
- sequential/diverging colormap family；
- saturation / alpha range。

继承的是视觉家族，不是机械复制图型。

---

## 正式 Data Figure 的 Prototype 规则

只允许：

```text
accepted data + reproducible plotting code
```

禁止使用 AI 文生图作为数值 Figure 实现基准。

Mechanism / framework Figure 可以采用示意设计，但必须嵌入真实方法/物理对象，不允许 generic boxes-and-arrows 充当 hero。

---

## Version / Freeze

对用户的 provisional 交付：

```text
qX_plot_vNN_<short-note>.m
mechanism_vNN_<short-note>.<drawio/xml/svg/...>
```

每次必须唯一命名，不覆盖上一版。

只有用户明确“确定 / 通过 / 冻结”后，才生成 canonical，并记录：
- accepted source version；
- commit/hash（适用时）；
- frozen Figure IDs；
- paper-family anchor；
- palette anchor；
- Figure Suite Manifest 当前状态。
