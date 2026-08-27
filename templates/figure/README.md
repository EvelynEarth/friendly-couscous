# Figure Skill Index（科研绘图入口）

本目录不建立独立于 `modules/04_figure_evidence.md` 的第二套决策权威。推荐执行顺序：

```text
modules/04_figure_evidence.md
→ Figure Contract / Evidence level / Primary question
→ templates/figure/top_tier_scientific_figure_skill.md
→ templates/figure/chart_selection.md
→ templates/figure/scientific_figure_skill_landscape.md（需要外部方法论时）
→ real-data prototype + render-review
→ templates/figure/anti_ai_figure_gate.md
→ templates/matlab/README.md
→ q{x}_plot.m
→ templates/figure/result_figure_qa.md
→ embedded-paper QA
→ accepted / frozen
```

## 当前核心文件

| 文件 | 作用 |
|---|---|
| `top_tier_scientific_figure_skill.md` | 顶级科研图完整执行法：四轴质量条、hero/drop test、选型评分、geometry、render-review、embedded-paper gate |
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

任何“参考 Nature / Science / Cell / 顶刊”请求，都必须：
1. 先写 Dataset + Claim / Figure Contract；
2. 先查 `top_tier_scientific_figure_skill.md`；
3. 若需要外部 skill 方法，查 `scientific_figure_skill_landscape.md`；
4. 若需要实际顶刊结构案例，查 `journal_figure_case_patterns.md`；
5. 正式数据图 prototype 只使用真实 accepted data + 可复现绘图库，**不使用 AI 文生图作为实现基准**；
6. 至少两轮 render-review，并通过 `anti_ai_figure_gate.md`；
7. MATLAB 只翻译 approved prototype；
8. standalone Figure 通过后，还要在 Word/LaTeX/PDF 实际页面做 final-width reduction test。

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
