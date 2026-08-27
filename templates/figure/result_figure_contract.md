# 结果图 Figure Contract

| 字段 | 内容 |
|---|---|
| Figure ID | 图 X |
| Iteration mode | `beautify` / `redesign` |
| Architecture status | `proposed` / `approved` / `frozen` / `reopened` |
| Frozen visual scope | 已冻结的 Figure / panel / 图型 / geometry / color role；未冻结时写 `none` |
| Core conclusion | 一句话核心结论 |
| Evidence level | L1 / L2 / L3 / L4 |
| Primary question | 评委看完本 Figure 应回答的唯一一级问题 |
| Figure role | 趋势 / 分布 / 诊断 / 敏感性 / 鲁棒性 / Pareto / 空间 / 网络 / 构成 / 多维画像 |
| MATLAB title | 单图 `title` 或多面板 `sgtitle` 的简洁中文标题 |
| DOCX/LaTeX caption | 图下题注，补充样本、统计口径、时间范围和误差，不与 MATLAB title 逐字重复 |
| Chart type | 折线图 / 条形图 / 散点图 / 区间图 / 热力图 / Pareto / 网络图 / 其他 |
| Efficiency rationale | 相较替代图如何提高可验证信息密度；若为复合图说明为何拆分会损失证据关系 |
| Enhancement | 可选：none / Local Zoom / Small Multiples / Focus Highlighting / Semantic Background / Composite Diagnostic / Conditional 3D；可合理组合 |
| Enhancement rationale | 为什么基础布局不足，以及增强后增加了什么可验证信息或降低了什么视觉搜索成本 |
| Reference purpose | `none` / layout / density / color role / visual grammar / line-point hierarchy / legend footprint |
| Must imitate | 只写可借鉴的版式/视觉语法；无参考图写 `none` |
| Must preserve | 当前 accepted data / semantics / units / conclusion / frozen scope |
| Do not copy | 参考图中的标签、数值、阈值、对象结构等本题不存在的信息 |
| Body geometry | 纵横比、主体占版、行列密度、metadata 宽度和 panel 关系 |
| Axis-domain plan | 各 axes 的 x/y 数据域；若共享行语义但数值域不同，明确使用 aligned axes / table+plot 等方案 |
| Color role contract | Primary / risk-failure / baseline-reference / structure / context / semantic background 的角色与方向语义；先定角色后定 Hex |
| Annotation budget | 只保留不可替代的端点、基准、阈值、最差/最优等标注；说明图例与脚注预算 |
| Source workbook | `问题X求解/问题X求解结果.xlsx` 或 `问题X求解/问题X结果深化分析.xlsx` |
| Worksheet | 中文工作表名 |
| Required columns | 绘图必需真实字段、记录键、单位和排序字段 |
| Expected positions | 可选列号，仅作结构漂移警告 |
| MATLAB script | `问题X求解/qX_plot.m` |
| Panel map | a/b/c/d 或其他 axes 的证据职责；无多面板时写单图职责 |
| Statistics/error | 误差线、区间、样本量和统计口径 |
| Export files | 求解阶段留空；论文阶段人工确认后可登记项目级 `figures/qx_*.pdf`、`.png` 或 `.svg` |
| Framework registry | `模型论文框架.md` 中的对应图表登记 |
| Paper location | 正文章节 |
| Reviewer risk | 可能质疑点与处理 |

Figure Contract 默认登记在 `模型论文框架.md`，不生成独立 `figure_evidence` 文件。Enhancement 只记录决策与理由，不记录 inset 坐标、透明度等 MATLAB 实现参数。历史目录和旧工作簿名只允许出现在专用兼容说明中。

`Iteration mode` 的语义：

- `beautify`：图型、证据职责和数据系列已接受，只调整颜色、字体、网格、geometry、对齐、annotation、legend 与 polish；
- `redesign`：用户明确允许重新选择图型/面板架构，先通过 Figure Layout Gate 与 Chart Selection，再进入代码；
- `frozen`：架构或视觉层已被用户接受，后续不得静默改动，只有显式 `reopened` 才能改变对应冻结范围。
