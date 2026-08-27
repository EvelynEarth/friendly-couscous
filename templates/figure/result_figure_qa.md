# 结果图 QA

> 本 QA 与 `modules/04_figure_evidence.md`、`top_tier_scientific_figure_skill.md` 联用。  
> 审查顺序固定：**truth → chart/geometry → hierarchy → labels/legend → color → MATLAB fidelity → embedded-paper**。

| 检查项 | 状态 | 备注 |
|---|---|---|
| 数据是否来自每问两类标准工作簿 |  |  |
| 是否记录源工作表、真实表头和固定列位置 |  |  |
| MATLAB 是否只绘图、不重算核心结果 |  |  |
| 图窗是否默认可见并保留 |  |  |
| 是否避免默认自动导出和关闭 |  |  |
| 是否在写代码前明确 `Iteration mode = beautify / redesign` 与 `Architecture status` |  |  |
| `beautify` 模式是否保持已接受图型、证据职责和数据系列，仅调整视觉层 |  |  |
| `redesign` 模式是否先通过 Figure Layout Gate / Chart Selection 并在编码前冻结候选架构 |  |  |
| 用户已将 Figure / panel / 图型标为 `frozen` 后，是否避免静默换图型或改证据职责；需要变化时是否先显式 reopen |  |  |

## A. Chart Selection / Evidence Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否先写 Core conclusion / Evidence level / Primary question，再选图型 |  |  |
| 每个 Primary question 是否实际比较至少 3 类候选视觉语法，而不是 bar/line/heatmap/dumbbell/waterfall 内循环 |  |  |
| 是否按 Answerability / Perceptual precision / Information density / Data honesty / Caption burden / Journal fit 做候选评分 |  |  |
| 是否记录至少一个被淘汰候选及淘汰原因 |  |  |
| 高级图型是否提供不可替代信息，而不是为了“顶刊感/高级感” |  |  |
| ternary 是否真正利用二维 simplex；若数据近共线/一项近常数是否已降级 |  |  |
| Sankey/alluvial 是否对应真实流/守恒量，而非把阶段状态假装成流量 |  |  |
| Waterfall 是否严格增量可加总闭合 |  |  |
| 小样本连续数据是否优先展示原始点，而非只画 summary bar |  |  |
| 大量无变化对象是否降权/汇总，而不是制造重合点和空行 |  |  |

## B. Journal Geometry Gate（body-first）

| 检查项 | 状态 | 备注 |
|---|---|---|
| 数据主体是否占据可用版心的大部分，而不是“大标题 + 小主体” |  |  |
| panel 是否紧凑排列，gap 只承担分隔职责而非制造空洞 |  |  |
| panel 宽高是否按信息密度决定，而不是机械等宽/等高 |  |  |
| 一个 dense matrix + 一个 threshold slice 等非对称证据是否采用合理非等宽布局 |  |  |
| axis 范围是否贴合数据；超出范围是否有阈值/可行域等真实理由 |  |  |
| 是否存在大面积无效白区；若有，是否能解释其结构作用 |  |  |
| common axis label / common legend 是否避免重复 |  |  |
| panel 阅读顺序是否自然（左→右、上→下）且与 caption 一致 |  |  |
| 复合 Figure 是否仍只有一个一级 Primary question |  |  |
| 2×2 / 1×3 是否真正不可拆，而非因为“结果多” |  |  |

## C. Typography / Hierarchy Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 是否明确区分 MATLAB Review Profile 与 Final Paper Profile |  |  |
| Review Profile 是否保持中文可读性（HSK baseline：axes≈18、legend≈16、line≈1.4） |  |  |
| 是否避免把 Nature 5–7 pt production 字号直接写进 MATLAB 交互图窗 |  |  |
| 标题过长时是否优先缩短/移入 caption，而不是先缩字体 |  |  |
| 是否避免 `sgtitle + panel title + 大注释框 + caption` 重复同一结论 |  |  |
| panel label / subtitle / axis label / tick label 是否形成清楚层级 |  |  |
| 是否避免彩色正文式解释抢占数据注意力 |  |  |

## D. Legend / Annotation Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| legend 是否真的必要；2–4对象能 direct label 时是否优先直接标注 |  |  |
| shared encoding 是否使用 shared compact legend 而非每个 axes 重复 legend |  |  |
| legend 是否没有逼缩主体、制造大块空白或遮挡数据 |  |  |
| 每个 axes 的不可替代 annotation 是否大致控制在 3–5 个 |  |  |
| 大量精确数字是否移入表格/caption，而不是全部贴在点旁 |  |  |
| 标注是否无碰撞、无 clipping、无覆盖数据主体 |  |  |

## E. Color / Accessibility Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 配色是否先定义 Primary / risk-failure / baseline-context 等职责，再选 Hex |  |  |
| 全图是否通常只保留 1 个主色 + 1 个 adverse 色 + context 灰 |  |  |
| 同一对象/语义跨 Figure 是否保持一致颜色职责 |  |  |
| 是否避免 rainbow/jet 与无序多色轮换 |  |  |
| 是否避免红绿作为唯一差异通道 |  |  |
| 颜色是否不是主要定量编码；位置/长度/连接关系是否承担主要比较 |  |  |
| grayscale / color-deficiency sanity check 是否仍能辨认关键对象 |  |  |
| 是否避免阴影、无意义渐变、无意义3D和 dashboard 风格卡片 |  |  |

## F. Reference Figure Reverse Engineering

| 检查项 | 状态 | 备注 |
|---|---|---|
| 若用户给参考图，是否先拆 body bounding box / panel ratio / gap / axis / typography / color role / annotation / legend |  |  |
| 是否明确 `Must imitate / Must preserve / Do not copy` |  |  |
| 是否只模仿 geometry / hierarchy / visual grammar，而不复制参考图对象名、阈值、固定色号 |  |  |
| 是否把用户指出的“只改主体/legend/某张图”限制为本轮修改作用域 |  |  |

## G. Render–Review–Iterate Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 正式 MATLAB 前是否用 accepted data 做真实视觉原型 |  |  |
| 是否至少完成 Render Review #1：body geometry |  |  |
| 若 geometry 失败，是否 redesign，而不是只换色 |  |  |
| 是否至少完成 Render Review #2：hierarchy / labels / color |  |  |
| 是否通过 2 秒测试：立即知道比较对象和差异方向 |  |  |
| 是否通过 10 秒测试：能用一句话复述 Figure 主结论 |  |  |
| MATLAB 实现是否忠实还原通过审查的视觉原型 |  |  |
| MATLAB screenshot 是否做 implementation fidelity review |  |  |
| 同一 Figure 连续约 3 轮仍未收敛时，是否停止 vN 并做 mismatch diagnosis |  |  |

## H. MATLAB / Data Honesty Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| 中文坐标轴、单位、图例是否完整 |  |  |
| 是否避免为美观对离散点擅自平滑并制造新峰谷/拐点 |  |  |
| 独立场景点是否避免伪造连续曲线 |  |  |
| ROI 是否保留全局上下文且未截轴夸大 |  |  |
| Semantic Background 是否对应真实阈值/状态 |  |  |
| 数值残差是否使用业务/求解容差，不把 solver noise 画成实质差异 |  |  |
| ternary / Sankey / alluvial 是否在 caption 明确 composition/path/flow 语义 |  |  |

## I. Embedded-paper Gate

| 检查项 | 状态 | 备注 |
|---|---|---|
| standalone PNG 通过后，是否实际嵌入 Word/LaTeX/PDF 整页检查 |  |  |
| 缩放后 axes/legend/marker/line 是否仍可读 |  |  |
| caption 是否和图争夺视觉注意 |  |  |
| 图是否造成页面异常空白或版心失衡 |  |  |
| 若缩放失败，是否优先调整图占版/删冗余/调整 panel 比例，而非直接缩字体 |  |  |
| 若正式导出，文字是否保持可编辑/矢量或达到项目规定分辨率 |  |  |

## J. Freeze / Paper Closure

| 检查项 | 状态 | 备注 |
|---|---|---|
| 标题—图注—工作簿—脚本—结论是否已同步到 `模型论文框架.md` |  |  |
| 是否能绑定正文结论 |  |  |
| 用户明确“通过/确定这一版/保留”后，是否立即记录 accepted/frozen、canonical `qX_plot.m` 与 SHA-256 |  |  |
| 当前问题目录是否只保留 canonical `qX_plot.m` 作为 active 绘图入口 |  |  |
| 是否已清理实验版 `.m`、重复 wrapper 和近似命名旧入口 |  |  |
