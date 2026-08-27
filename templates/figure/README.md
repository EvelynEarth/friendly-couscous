# Figure Skill Index（科研绘图统一入口）

本目录不建立独立于 `modules/04_figure_evidence.md` 的第二套 Figure 决策权威。Module 04 仍是事实源、Evidence level、Primary question、Layout/Enhancement Gate 与论文闭环的上位规则。

## 统一执行顺序

```text
modules/04_figure_evidence.md
→ Figure Suite Manifest（若一个问题/全文有2张以上图）
→ Figure Contract / Evidence level / Primary question
→ templates/figure/top_tier_scientific_figure_skill.md
→ templates/figure/journal_figure_mastery_v2.md
→ templates/figure/figure_iteration_control.md
→ templates/figure/chart_selection.md
→ templates/figure/scientific_figure_skill_landscape.md（需要外部方法论时）
→ templates/figure/figure_skill_evals.md（Skill修改后做回归检查）
→ real-data prototype v0（body only）
→ internal render-review #1：grammar / geometry / complexity
→ real-data prototype v1（hierarchy / labels / restrained color）
→ grayscale / CVD / thumbnail test
→ templates/figure/anti_ai_figure_gate.md
→ mechanical lint + Judgment Pass 2.0
→ release candidate gate
→ templates/matlab/README.md
→ q{x}_plot_vNN_<short-note>.m
→ MATLAB screenshot fidelity review
→ templates/figure/result_figure_qa.md
→ final-width / embedded-paper QA
→ accepted / canonical q{x}_plot.m / frozen
```

若同一 Figure 曾被用户退回过、用户评价“丑 / AI感 / 松散 / 没学到参考图精髓”，还必须先读：

```text
templates/figure/figure_failure_postmortem_2026-08.md
```

禁止在没有 mismatch diagnosis 的情况下继续机械递增 vN。

---

## 当前核心文件

| 文件 | 作用 |
|---|---|
| `top_tier_scientific_figure_skill.md` | 融合后的主 Skill：Figure Suite、claim→visual task、候选 grammar、salience、hero/drop、geometry、render-review、Judgment Pass 2.0 |
| `journal_figure_mastery_v2.md` | 高级顶刊层：整篇图组、Salience–Relevance、Editorial Compression、Uncertainty Semantics、Invariant Subtraction、Complexity Decomposition、thumbnail test |
| `figure_suite_manifest.md` | 整篇论文 Figure 架构表：防止重复 claim、重复 grammar、风格漂移，并登记 paper-family anchor |
| `figure_skill_evals.md` | 14个历史/对抗性回归测试：4点稀疏scatter、固定75% baseline、equal-grid、假CI、AI卡片、reference只学颜色等 |
| `figure_iteration_control.md` | 绘图状态机与发布硬门：scope lock、真实数据 prototype、自审、用户迭代预算、MATLAB preflight、唯一命名、freeze/reopen |
| `figure_failure_postmortem_2026-08.md` | Q1–Q3 长上下文复盘：为什么过去经常修改20+版，以及每类历史错误的禁止重犯规则 |
| `scientific_figure_skill_landscape.md` | Nature / Nature Methods / Icarus / matlab-plot-skill / scientific-plotting-skill / gramm / Crameri 等方法论与采用边界 |
| `anti_ai_figure_gate.md` | 去 AI 信息图 / dashboard / PPT 味硬门 |
| `journal_figure_research_notes.md` | 顶刊官方规范与方法论研究底稿 |
| `journal_figure_research_notes_v2_2026-08-28.md` | 本轮二次深挖：salience、labels、complexity、uncertainty、外部 skills 的新增吸收与拒绝边界 |
| `journal_figure_case_patterns.md` | 真实顶刊 Figure 结构模式案例库 |
| `chart_selection.md` | Claim→Visual Task→Grammar 图型选择索引 |
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
```

解释：
- **Depth**：图里能读出机制/阈值/为什么；
- **Elegance**：一个 claim、一个 hero、通过 drop test；
- **Unimpeachable**：数据诚实、轴诚实、不确定性语义正确、可复现；
- **Visible gap**：0.5 秒像论文正文，不像 homework/PPT/dashboard/AI；
- **Salience relevance**：第一眼看到的就是最重要证据；
- **Suite coherence**：整篇 Figure 属于同一个 paper family，又不重复讲同一句话。

---

## 必须长期记住的纠偏

```text
顶刊感 ≠ 小字体 + 大留白 + 低饱和
顶刊感 ≠ Nature配色 + 大标题 + 卡片式结论
顶刊感 ≠ 每张图都“高级图型”

用户不是第一层 linter。
结构失败时禁止靠换色续命。
不变量不应占主体。
最醒目的对象必须是最重要的证据。
新交付文件必须新命名。
已 frozen Figure 不得静默重构。
```

---

## Figure Suite First

当一个问题有两张以上 Figure，或开始 Q1–Qn 全文绘图时，先填写：

```text
templates/figure/figure_suite_manifest.md
```

必须检查：
- 是否两张图回答同一句话；
- 是否同一数据只是换图型复述；
- 是否无意识重复同一种 grammar；
- 是否 paper-family style 漂移；
- 是否 L3/L4 supporting figure 抢走 L1 hero 的视觉权重。

---

## Skill Regression Evals

每次对绘图 Skill 做较大修改后，先检查：

```text
templates/figure/figure_skill_evals.md
```

当前包含 14 个对抗性案例。目标不是“文档看起来完整”，而是保证 Skill 在这些历史高频失败上做出正确判断。

如果任一错误架构仍能轻易被流程批准，说明 Skill 还没有修好。

---

## Paper-family anchor

当用户明确指出某张 Figure“有期刊味 / 这张可以 / 保留”，立即登记 `paper_family_anchor`。

后续 Figure 优先继承：
- font family；
- stroke weight；
- primary/risk/context 颜色职责；
- marker 尺度；
- annotation density；
- panel gap；
- whitespace rhythm；
- direct-label / legend strategy。

继承的是视觉家族，不是机械复制图型。

---

## 正式数据 Figure 的 Prototype 规则

只允许：

```text
accepted data + reproducible plotting code
```

禁止使用 AI 文生图作为 MATLAB 实现基准。

Mechanism / framework Figure 可以采用示意设计，但必须嵌入真实方法对象，不允许 generic boxes-and-arrows 充当 hero。

---

## Version / Freeze

对用户的 provisional 交付：

```text
qX_plot_vNN_<short-note>.m
```

每次必须唯一命名，不覆盖上一版。

只有用户明确“确定 / 通过 / 冻结”后，才生成 canonical：

```text
qX_plot.m
```

并记录：
- accepted source version；
- commit/hash；
- frozen Figure IDs；
- paper-family anchor；
- Figure Suite Manifest 当前状态。