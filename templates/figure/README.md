# Figure Skill Index（科研绘图入口）

本目录不建立独立于 `modules/04_figure_evidence.md` 的第二套决策权威。推荐执行顺序：

```text
modules/04_figure_evidence.md
→ Figure Contract / Evidence level / Primary question
→ templates/figure/top_tier_scientific_figure_skill.md
→ templates/figure/chart_selection.md
→ visual prototype + render-review
→ templates/matlab/README.md
→ q{x}_plot.m
→ templates/figure/result_figure_qa.md
→ accepted / frozen
```

## 当前核心文件

| 文件 | 作用 |
|---|---|
| `top_tier_scientific_figure_skill.md` | 顶级科研图完整执行法：选型评分、geometry、typography、render-review、embedded-paper gate |
| `journal_figure_research_notes.md` | Nature / Nature Methods / PLOS / Science-style / JAMA / Brain / Cell / MATLAB 外部方法论研究底稿 |
| `journal_figure_case_patterns.md` | 从真实 Nature Communications 等论文 Figure 抽取的结构模式案例库 |
| `chart_selection.md` | 按证据任务选择图型的索引 |
| `figure_enhancement_patterns.md` | Local Zoom / Small Multiples / Focus Highlighting / Semantic Background / Composite Diagnostic / 3D 的实现模式 |
| `result_figure_contract.md` | 结果图 Figure Contract |
| `result_figure_qa.md` | 从数据真值到 embedded-paper 的最终 QA |

## 当前最重要的绘图纠偏

```text
顶刊感 ≠ 小字体 + 大留白 + 低饱和
顶刊感 = 高信息效率 + 紧凑版式 + 清楚层级 + 数据诚实 + 最终版面可读
```

任何“参考 Nature / Science / Cell”的请求，都必须：
1. 先查 `journal_figure_research_notes.md`；
2. 若需要实际结构案例，再查 `journal_figure_case_patterns.md`；
3. 只模仿 geometry / hierarchy / visual grammar；
4. 中文字段、真实数值、阈值和结论完全来自本项目 accepted workbook；
5. 至少两轮 render-review 后才写正式 MATLAB。
