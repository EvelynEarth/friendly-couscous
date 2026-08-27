# 结果图 QA（高级融合版）

> 联用：`modules/04_figure_evidence.md`、`top_tier_scientific_figure_skill.md`、`journal_figure_mastery_v2.md`、`figure_iteration_control.md`。  
> 若 Figure 曾被用户退回，还必须先读 `figure_failure_postmortem_2026-08.md`。  
> 审查顺序：**suite → scope → truth → claim/grammar → salience/geometry → labels/symbol/color → prototype/release → MATLAB fidelity → final-width → freeze**。

---

## A. Figure Suite Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 若一个问题/全文有2张以上Figure，是否先填写 `figure_suite_manifest.md` |  |  |
| 每张Figure是否有唯一 one-sentence claim |  |  |
| 是否没有两张图用同一数据换图型重复同一句话 |  |  |
| 相同 visual grammar 若重复，是否说明为什么该 perceptual task 仍需重复 |  |  |
| 是否存在明确 L1 hero，而 L3/L4 没有抢走主要视觉资源 |  |  |
| 是否继承 paper-family anchor 的字体、stroke、颜色职责、annotation density、whitespace rhythm |  |  |
| suite thumbnail 并排时是否明显属于同一论文视觉家族 |  |  |

---

## B. Scope / Version / Freeze Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否先锁定 `modify / preserve / frozen` |  |  |
| 用户指定“只改主体/legend/某panel”时是否严格遵守 |  |  |
| `iteration_mode` 是否为 beautify / redesign / fidelity_fix |  |  |
| beautify 是否没有静默换 grammar / evidence role |  |  |
| fidelity_fix 是否只修 MATLAB renderer 差异 |  |  |
| frozen Figure 是否未被静默重构；如需变化是否显式 REOPEN |  |  |
| provisional 文件是否使用新唯一 `qX_plot_vNN_<short-note>.m` |  |  |
| 是否不存在“名字新、内容旧” |  |  |

---

## C. Truth / Data Honesty Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 数据是否来自 accepted 标准工作簿 |  |  |
| 是否记录真实 workbook / sheet / headers / units |  |  |
| MATLAB 是否只绘图、不重新求解 |  |  |
| 是否不写 Excel、不从聊天摘要反推底层数据 |  |  |
| 离散扫描是否没有被插值成假连续边界 |  |  |
| 独立场景是否没有被连成伪时间趋势 |  |  |
| axis / crop / log / baseline 是否没有夸大结论 |  |  |
| bar 用长度编码时是否从0起；若非0基线是否改用 dot/interval |  |  |

---

## D. Claim → Visual Task → Grammar Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否先写 Core conclusion / Primary question / Skeptical reviewer question |  |  |
| claim 是否先翻译成 visual task，再选 chart |  |  |
| redesign 是否比较至少3个不同 visual grammar |  |  |
| Candidate scoring 是否含 Answerability / Perceptual precision / Density / Mechanism depth / Salience / Honesty / Caption burden / Journal fit / Suite coherence |  |  |
| 是否记录至少1个 rejected candidate |  |  |
| 选中的高级图型是否真正更快读、更诚实或更高信息密度 |  |  |
| 是否避免“会画什么就画什么” |  |  |

---

## E. Uncertainty Semantics Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否明确 uncertainty = statistical / scenario / parametric / robust-feasible / numerical / forecast / none |  |  |
| statistical error bar 是否明确 SD / SE / CI 与 N |  |  |
| deterministic optimization 是否没有伪造 CI |  |  |
| scenario range 是否没有称作 confidence interval |  |  |
| numerical gap/residual 是否没有伪装统计误差 |  |  |
| 参数离散点是否没有画成 continuous ribbon |  |  |

---

## F. Salience–Relevance Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否写出 `Most relevant object` 与 `Most salient object` |  |  |
| 二者是否一致或高度一致 |  |  |
| 每个 axes 是否通常只有1个 primary salient object |  |  |
| context 背景/legend/title 是否没有比 hero data 更抢眼 |  |  |
| 是否没有“超大marker + 鲜艳色 + 粗线 + 彩色文字 + 大色块”叠加强调 |  |  |
| baseline/invariant 是否没有占据最大彩色面积 |  |  |

---

## G. Hero / Witness / Drop Test

| 检查项 | 状态 | 备注 |
|---|---|---|
| multipanel 是否明确 hero panel |  |  |
| witness panel 是否通过 drop test |  |  |
| supporting panel 是否没有与 hero 机械等权 |  |  |
| equal 2×2 / 1×3 是否有真正不可拆的逻辑 |  |  |
| 删除任一 panel 后若 claim 不受影响，是否已删除/移附录 |  |  |

---

## H. Invariant Subtraction / Complexity Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否识别跨对象近似不变的大分量 |  |  |
| 不变量是否被降为 reference / metadata / caption，而不是主体大色块 |  |  |
| >4纠缠曲线 / 多尺度 / legend ping-pong 时是否考虑 small multiples / hero+witness / overview+zoom |  |  |
| ROI zoom 是否真的增加可验证信息，而不是装饰性放大 |  |  |
| complex overview 是否没有为了“高级感”强行保留 |  |  |

---

## I. Journal Geometry Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| data body 是否占据可用版心的大部分 |  |  |
| panel 尺寸是否按内容/信息密度而非机械等宽 |  |  |
| whitespace 是否承担分组/层级/阅读顺序职责 |  |  |
| axis range 是否贴近证据域 |  |  |
| title / legend 是否没有逼缩主体 |  |  |
| common axis / legend 是否尽量共享 |  |  |
| reference figure 的 body bbox / row density / panel ratio 是否真正被学习 |  |  |

---

## J. Axis / Tick / Grid / Navigation Ink

| 检查项 | 状态 | 备注 |
|---|---|---|
| axis lines / tick / units 是否完整 |  |  |
| tick 是否清楚但不抢数据 |  |  |
| major grid 是否仅在读数需要时使用且足够轻 |  |  |
| minor grid 是否默认关闭 |  |  |
| dual axis 是否有明确物理关系且不可替代 |  |  |
| log axis 是否明确标示 |  |  |

---

## K. Label / Callout / Typography

| 检查项 | 状态 | 备注 |
|---|---|---|
| common text 是否被 refactor，不重复写满 |  |  |
| 单位是否集中到 axis title |  |  |
| direct label 是否优先于 legend ping-pong |  |  |
| direct label 是否优先黑/深灰文字 + marker/keyline，而非大段彩色文字 |  |  |
| callout line 是否不交叉、不穿数据、角度/长度风格一致 |  |  |
| annotation 是否通常控制在每 axes 1–4 个不可替代信息 |  |  |
| 是否避免全图都 bold |  |  |
| MATLAB Review Profile 与 Final Paper Profile 是否分离 |  |  |

---

## L. Symbol / Color / Accessibility

| 检查项 | 状态 | 备注 |
|---|---|---|
| primary / secondary / context / threshold 是否有自然 symbol hierarchy |  |  |
| 是否不是仅靠颜色区分系列 |  |  |
| discrete color 是否按语义角色而非随机多色 |  |  |
| continuous color 是否先判断 sequential / diverging / cyclic |  |  |
| continuous map 是否 perceptually uniform |  |  |
| 是否禁止 jet / rainbow / HSV |  |  |
| grayscale / CVD 下是否仍能正确解码 |  |  |
| 是否没有无意义 drop shadow / gradient / glow / decorative icon |  |  |
| 是否没有把 quantile recoloring 默认用于保留绝对物理距离的连续量 |  |  |

---

## M. Prototype / Render Review Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 正式 MATLAB 前是否使用 accepted data 生成可复现 prototype |  |  |
| 是否禁止 AI 文生图作为 data Figure 实现基准 |  |  |
| Internal v0 是否只审 grammar / hero / geometry / axis waste / invariant clutter |  |  |
| geometry 失败是否 redesign，而不是先换色 |  |  |
| Internal v1 是否审 hierarchy / labels / restrained color / salience |  |  |
| 是否通过 0.5s glance test |  |  |
| 是否通过 2s direction test |  |  |
| 是否通过 10s claim test |  |  |
| 是否通过 thumbnail test（约25–35%） |  |  |
| 用户是否没有被迫承担第一层 linter |  |  |

---

## N. Mechanical Floor + Judgment Pass 2.0

| 检查项 | 状态 | 备注 |
|---|---|---|
| units / source / no solver / no write / no fake interpolation 是否 PASS |  |  |
| 是否扫描 illegal Unicode / NBSP / smart quote / MATLAB 兼容风险 |  |  |
| 是否无明显 clipping / overlap |  |  |
| Depth 是否 PASS |  |  |
| Elegance 是否 PASS |  |  |
| Unimpeachable 是否 PASS |  |  |
| Visible gap 是否 PASS |  |  |
| Salience relevance 是否 PASS |  |  |
| Suite coherence 是否 PASS |  |  |

---

## O. MATLAB Fidelity / Final-width / Embedded-paper

| 检查项 | 状态 | 备注 |
|---|---|---|
| MATLAB 是否只翻译 approved prototype，而不是重新设计 |  |  |
| 本地截图是否做 renderer fidelity review |  |  |
| accepted 后是否按真实单栏/双栏宽度缩放 |  |  |
| 缩小后 line / marker / text 是否仍清楚 |  |  |
| standalone 好看后是否实际放进 Word/LaTeX/PDF 整页检查 |  |  |
| caption 是否没有和 Figure 争夺注意力 |  |  |
| vector export / editable text 是否有计划 |  |  |

---

## P. Freeze / Paper Closure

| 检查项 | 状态 | 备注 |
|---|---|---|
| 用户明确通过后是否记录 accepted / frozen |  |  |
| 是否生成 canonical `qX_plot.m`，并记录来源版本 / commit / hash |  |  |
| 是否记录 frozen Figure IDs 与 paper-family anchor |  |  |
| 是否同步 `模型论文框架.md` 与 Figure Suite Manifest |  |  |
| 旧实验 `.m` 是否不再作为 active entry |  |  |
| frozen 后如需换 grammar / evidence role，是否显式 REOPEN |  |  |
