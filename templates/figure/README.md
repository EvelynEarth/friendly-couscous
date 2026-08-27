# Figure Skill Index（科研绘图入口）

本目录不建立独立于 `modules/04_figure_evidence.md` 的第二套决策权威。推荐执行顺序：

```text
modules/04_figure_evidence.md
→ Figure Contract / Evidence level / Primary question
→ templates/figure/top_tier_scientific_figure_skill.md
→ templates/figure/figure_iteration_control.md
→ templates/figure/chart_selection.md
→ templates/figure/scientific_figure_skill_landscape.md（需要外部方法论时）
→ real-data prototype + internal render-review
→ templates/figure/anti_ai_figure_gate.md
→ release candidate gate
→ templates/matlab/README.md
→ q{x}_plot_vNN_<short-note>.m
→ MATLAB screenshot fidelity review
→ templates/figure/result_figure_qa.md
→ embedded-paper QA
→ accepted / canonical q{x}_plot.m / frozen
```

若同一 Figure 曾被用户退回过、用户评价“丑 / AI感 / 松散 / 没学到参考图精髓”，还必须先读：

```text
templates/figure/figure_failure_postmortem_2026-08.md
```

禁止在没有做 mismatch diagnosis 的情况下继续机械递增 vN。

## 当前核心文件

| 文件 | 作用 |
|---|---|
| `top_tier_scientific_figure_skill.md` | 顶级科研图完整执行法：四轴质量条、hero/drop test、选型评分、geometry、render-review、embedded-paper gate |
| `figure_iteration_control.md` | 绘图状态机与发布硬门：scope lock、真实数据 prototype、自审、用户迭代预算、MATLAB preflight、唯一命名、freeze/reopen |
| `figure_failure_postmortem_2026-08.md` | Q1–Q3 长上下文复盘：为什么过去经常修改 20+ 版，以及每类历史错误的禁止重犯规则 |
| `scientific_figure_skill_landscape.md` | Icarus Figures / matlab-plot-skill / skill-publication-figures / gramm / SciencePlots / Crameri-DiVA 的调研与吸收矩阵 |
| `anti_ai_figure_gate.md` | 去 AI 信息图 / dashboard / PPT 味的硬门：卡片、pastel washing、title-heavy、equal-grid、annotation overload 等 |
| `journal_figure_research_notes.md` | Nature / Nature Methods / PLOS / Science-style / JAMA / Brain / Cell / MATLAB 外部方法论研究底稿 |
| `journal_figure_case_patterns.md` | 从真实 Nature Communications 等论文 Figure 抽取的结构模式案例库 |
| `chart_selection.md` | 按证据任务选择图型的索引 |
| `figure_enhancement_patterns.md` | Local Zoom / Small Multiples / Focus Highlighting / Semantic Background / Composite Diagnostic / 3D 的实现模式 |
| `result_figure_contract.md` | 结果图 Figure Contract |
| `result_figure_qa.md` | 从数据真值到 embedded-paper 的最终 QA |

## 当前最重要的绘图纠偏

```text
顶刊感 ≠ 小字体 + 大留白 + 低饱和
顶刊感 ≠ Nature 配色 + 大标题 + 卡片式结论

顶刊感 =
Depth（图里能读出机制/阈值/为什么）
+ Elegance（一个claim，一个hero，drop test）
+ Unimpeachable（诚实、可复现、灰度/CVD可读）
+ Visible gap（0.5秒看起来就是论文Figure）
```

同时必须记住：

```text
用户不是第一层 linter。
新交付文件必须新命名。
已 frozen Figure 不得静默重构。
结构失败时禁止靠换色继续续命。
```

任何“参考 Nature / Science / Cell / 顶刊”请求，都必须：
1. 先写 Dataset + Claim / Figure Contract；
2. 先查 `top_tier_scientific_figure_skill.md`；
3. 读取 `figure_iteration_control.md` 并完成 scope/source/claim lock；
4. 若该 Figure 有历史返工，先查 `figure_failure_postmortem_2026-08.md`；
5. 若需要外部 skill 方法，查 `scientific_figure_skill_landscape.md`；
6. 若需要实际顶刊结构案例，查 `journal_figure_case_patterns.md`；
7. 正式数据图 prototype 只使用真实 accepted data + 可复现绘图库，**不使用 AI 文生图作为实现基准**；
8. 至少两轮内部 render-review，并通过 `anti_ai_figure_gate.md`；
9. 只有通过 release candidate gate 后才给用户 `.m`；
10. MATLAB 只翻译 approved prototype；
11. standalone Figure 通过后，还要在 Word/LaTeX/PDF 实际页面做 final-width reduction test。

## Paper-family anchor

当用户明确指出某张 Figure“有期刊味 / 这张可以”，立即把它登记为 `paper_family_anchor`。后续 Figure 优先继承其：
- font family；
- stroke weight；
- primary/risk/context 颜色职责；
- marker 尺度；
- annotation density；
- panel gap；
- whitespace rhythm。

不得每张 Figure 各自重新发明一套“期刊风”。

## Version / Freeze 约定

对用户的 provisional 交付：

```text
qX_plot_vNN_<short-note>.m
```

每次必须唯一命名，不覆盖上一版。只有用户明确“确定 / 通过 / 冻结”后，才生成 canonical：

```text
qX_plot.m
```

并记录 accepted source version、commit/hash、frozen Figure IDs 与 paper-family anchor。