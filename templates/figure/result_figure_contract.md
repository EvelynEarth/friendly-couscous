# 结果图 Figure Contract（高级融合版）

| 字段 | 内容 |
|---|---|
| Figure ID | 图 X |
| Iteration mode | `beautify` / `redesign` / `fidelity_fix` |
| Architecture status | `proposed` / `approved` / `frozen` / `reopened` |
| Frozen visual scope | 已冻结的 Figure / panel / 图型 / geometry / color role；未冻结写 `none` |
| Suite role | 本 Figure 在整篇 Figure Suite 中的职责：L1 hero / L2 mechanism / L3 robustness / L4 legality / appendix |
| Suite uniqueness | 为什么该 Figure 不与其它 Figure 重复 claim / data / grammar |
| Paper-family anchor | 继承哪张已认可 Figure 的字体、stroke、颜色职责、annotation density、whitespace rhythm |
| Core conclusion | 一句话核心结论 |
| Evidence level | L1 / L2 / L3 / L4 |
| Primary question | 评委看完本 Figure 应回答的唯一一级问题 |
| Skeptical reviewer question | 最可能的审稿/评委反问是什么；本 Figure 如何回答 |
| Audience / paper role | 正文主结果 / 机制解释 / 稳健性 / 数值合法性 / 附录；默认技术型评委快速扫描 |
| Hero evidence | 本 Figure 最重要的数据对象/阈值/边界/关系 |
| Most relevant object | 科学上最重要的对象 |
| Most salient object | 视觉上最醒目的对象；必须与 Most relevant object 一致或高度一致 |
| Visual task | exact comparison / delta / rank / threshold / boundary / distribution / mechanism / flow / spatial / diagnostic |
| Candidate chart pool | 至少 3 个不同 visual grammar；`beautify` / `fidelity_fix` 可写 frozen |
| Candidate scoring | Answerability / Perceptual precision / Information density / Mechanism depth / Salience relevance / Data honesty / Caption burden / Journal fit / Suite coherence，0–2分 |
| Rejected candidate | 至少 1 个淘汰候选及原因 |
| Invariant component | 是否存在跨对象不变的大分量；若有，如何剥离/降权 |
| Uncertainty semantics | `none` / statistical / scenario / parametric / robust-feasible / numerical / forecast；禁止混用 |
| Statistics/error | 若有 error/range，明确 SD / SE / CI / scenario range / tolerance / residual 等口径 |
| Figure role | 趋势 / 分布 / 诊断 / 敏感性 / 鲁棒性 / Pareto / 空间 / 网络 / 构成 / 多维画像 |
| MATLAB title | 单图 `title` 或多面板 `sgtitle`；journal mode 可为 `none` |
| DOCX/LaTeX caption | 图下题注，结论导向，补充口径，不与图内标题逐字重复 |
| Chart type | 具体实现，如 forest / regime map / network / ECDF 等 |
| Efficiency rationale | 相较替代图如何提高可验证信息密度与 perceptual accuracy |
| Enhancement | none / Local Zoom / Small Multiples / Focus Highlighting / Semantic Background / Composite Diagnostic / Conditional 3D |
| Enhancement rationale | 为什么增强后增加真实信息或降低视觉搜索成本 |
| Complexity decomposition | 是否需要 small multiples / overview+zoom / hero+witness；为什么 |
| Reference purpose | `none` / layout / density / visual grammar / line-point hierarchy / legend footprint / salience |
| Must imitate | 可借鉴的 geometry / hierarchy / visual grammar |
| Must preserve | accepted data / semantics / units / conclusion / frozen scope |
| Do not copy | 参考图中的对象名、阈值、固定色号、production字号等本题不存在信息 |
| Body geometry | 纵横比、主体占版、row density、metadata宽度、panel ratio、gap |
| Hero/witness plan | 哪个 panel 是 hero；witness panel 通过何种 drop test 保留 |
| Panel density rationale | 为什么 panel 等宽/非等宽；各自信息密度与标签负担 |
| Axis-domain plan | x/y 数据域；0 baseline / log / threshold / shared scale 的语义 |
| Navigation-ink plan | axis / ticks / major grid 是否需要，如何保证不抢数据 |
| Shared-axis / shared-legend plan | 如何减少重复 |
| Typography profile | `HSK review` / `journal reduction` |
| Color role contract | Primary / Risk-Failure / Baseline-Reference / Secondary / Context；连续色图区分 sequential/diverging/cyclic |
| Symbol hierarchy | filled/open/shape/linestyle 如何建立 primary/secondary/context 层级并支持灰度 |
| Legend strategy | direct labels / keyline + black text / shared compact legend / per-panel legend |
| Annotation budget | 每 axes 只保留不可替代 annotation；通常 1–4 个 |
| Source workbook | `问题X求解/问题X求解结果.xlsx` 或 `问题X求解/问题X结果深化分析.xlsx` |
| Worksheet | 中文工作表名 |
| Required columns | 必需真实字段、记录键、单位、排序字段 |
| Expected positions | 可选列号，仅作结构漂移警告 |
| MATLAB script | provisional `qX_plot_vNN_<short-note>.m`；accepted 后 canonical `qX_plot.m` |
| Panel map | a/b/c/d 或其它 axes 的证据职责 |
| Prototype status | `not_started` / `body_v0` / `rendered_v1` / `redesigned` / `hierarchy_v1` / `approved` |
| Render Review #1 | grammar / hero / body geometry / complexity / invariant clutter / axis waste |
| Render Review #2 | salience / hierarchy / labels / color / 0.5s / 2s / 10s 测试 |
| Grayscale/CVD QA | 是否只靠颜色；B&W/CVD 下是否仍能正确解码 |
| Thumbnail QA | 缩到约25–35%或论文页面缩略图后，hero与主趋势是否仍存在 |
| Mechanical lint | units / source / no solver / no write / no fake interpolation / no illegal Unicode / no overlap |
| Judgment Pass 2.0 | Depth / Elegance / Unimpeachable / Visible gap / Salience relevance / Suite coherence |
| MATLAB fidelity review | 本地 MATLAB screenshot 与 approved prototype 的差异 |
| Embedded-paper QA | Word/LaTeX/PDF 最终宽度下的可读性、页内占版、caption竞争、vector editability |
| Export files | 求解阶段留空；论文阶段登记 PDF/PNG/SVG 等 |
| Framework registry | `模型论文框架.md` 对应登记 |
| Paper location | 正文章节 |
| Reviewer risk | 可能质疑点与处理 |

Figure Contract 默认登记在 `模型论文框架.md`，不生成独立事实源。

## Iteration mode

- `beautify`：已接受 grammar/series，不换证据职责；只调字体、颜色职责、geometry、legend、annotation、spacing；
- `redesign`：允许重新选 visual grammar，必须重新过 Suite/Claim/Candidate/Prototype Gate；
- `fidelity_fix`：只修 MATLAB renderer 与 approved prototype 的差异，禁止重新发明图型；
- `frozen`：用户已接受，只有显式 `reopened` 才能释放冻结约束。

## Release 条件

`redesign` 模式正式交付 MATLAB 前必须至少完成：

```text
Figure Suite check
→ Candidate scoring
→ real-data body prototype
→ body render-review
→ hierarchy prototype
→ salience/grayscale/thumbnail
→ anti-AI gate
→ mechanical lint
→ Judgment Pass 2.0
```

Standalone Figure 通过后，accepted 前仍需完成 final-width embedded-paper QA。