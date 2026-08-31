# 结果图型选择索引（Claim → Visual Task → Grammar）

图型不从“软件里有什么”出发，而从：

```text
Core claim
→ reader perceptual task
→ data structure
→ advanced candidate search
→ visual grammar
→ concrete chart
```

每张图先填写 `result_figure_contract.md`，并参考 `top_tier_scientific_figure_skill.md` 与 `journal_figure_mastery_v2.md`。

---

## 0. Advanced-first, evidence-governed

重要结果图默认**主动寻找高级 grammar**，而不是先画普通 bar/line 再决定要不要“升级”。这里的“高级”指：能用更高信息密度、更准确的视觉通道、更低搜索成本回答 Primary question，而不是图型更复杂。

每张正文候选至少记录：

```text
best advanced candidate
why it improves the reader task
simpler fallback
reviewer risk
```

选择原则：

- advanced candidate 对 reader task 有明显增益 → **优先采用**；
- advanced 与 simpler fallback 表达效率相当 → 选更直接、更稳健者；
- advanced 会造成伪连续、伪统计、不必要三维、遮挡或 legend tax → 淘汰；
- 不设“高级图数量配额”，也不设“高级图越少越好”的保守规则；
- 全文允许多种 grammar，只要每张图的 perceptual task 不同且 Figure Suite 风格仍一致。

因此既要避免“为了高级而复杂”，也要避免“明明 forest/regime/raincloud/Pareto 更合适却机械退回柱状/折线”。

---

## 1. 一级决策表

| 论文 claim | 读者任务 | 首选 visual grammar | 高风险替代 |
|---|---|---|---|
| 谁更优 / 排名如何 | 精确比较位置/长度 | dot / interval / forest / lollipop | pie / bubble / 3D bar |
| 改了多少 | 读取 delta | slope / dumbbell / signed delta forest | 两组并排大 bar |
| 为什么选该方案 | 同时看结构+量化代价/收益 | metadata strip + aligned panels / Pareto | 稀疏大 scatter / radar |
| 哪个因素主导 | 排序贡献量 | sorted contribution / tornado / signed decomposition | pie / donut |
| 什么时候失效 | 找 threshold / boundary | regime map / threshold slice | 平滑折线假边界 |
| 参数是否稳健 | 读取结构区域或切换距离 | actual-grid regime / small multiples / transition forest | 只画一个单点敏感性 |
| 机制如何发生 | 追踪状态/约束/流 | real network / staged flow / mechanism object | generic boxes-and-arrows |
| 分布怎样 | spread / skew / overlap | raw points / ECDF / violin / raincloud / box | bar of means |
| 预测/拟合可信吗 | fit / residual / calibration | observed-vs-predicted + residual / calibration | 只给R²数字 |
| 空间哪里异常 | 定位位置与强度 | map / field / heatmap / residual field | 表格或随机颜色块 |
| 三组成分如何变化 | composition | ternary / stacked composition | ternary（若近共线/一项近常数） |
| 流量如何转移 | conservation / flow | Sankey / alluvial / network flow | Sankey（若并非真实流） |
| 多目标怎样权衡 | frontier / dominance | Pareto front + selected point | radar / weighted score only |
| 风险来自哪里 | scenario contribution | metadata + contribution forest / weighted strip | 普通bar但丢掉概率/持续时间 |
| 样本很多且关注二维密度 | density / cluster / tail | hexbin / 2D density / rasterized scatter | 百万矢量散点 |
| 空间方向/速度如何变化 | direction + magnitude | quiver / streamline / vector field | 单纯热图丢失方向 |
| 方案顺序是否改变 | rank change | rank transition / slope / alluvial（真实流转时） | 多组柱状图 |

---

## 2. Graphical Perception 优先级

默认优先：

```text
aligned position
> non-aligned position
> length
> slope/direction
> angle
> area
> volume
> hue/saturation
```

精确量化比较尽量用 position / length；颜色主要负责类别、状态、风险角色和连续场辅助表达。

---

## 3. 参数 / 稳健性 / 阈值

### 优先候选
- actual-grid regime map；
- decision region；
- threshold slice；
- sensitivity small multiples；
- transition forest / tornado；
- contour / response surface（仅真实连续模型支持）。

### 主动高级搜索
若结果存在离散策略切换、可行/失效区域、最优—次优间隙或稳定集合，优先检查 regime / decision map、threshold slice、transition forest，而不是默认多条扰动折线。

### 禁止
- sparse grid 直接 spline 成连续相图；
- 独立离散测试点硬连成趋势；
- 只为了“高级感”做3D surface。

### 选型提示
若二维里一维几乎不影响结构，优先 1D slice；若二维交互本身就是结论，保留 actual-grid map。

---

## 4. 方案比较 / 结构差异 / 公平性

### 优先候选
- aligned forest / lollipop；
- metadata strip + quantitative panel；
- dumbbell / slope；
- rank transition；
- Pareto；
- parallel coordinates（维度较多且语义一致）。

### 高级规则
- 没变化对象降权或正文汇总；
- categorical structure + numerical outcome 同时重要时，metadata strip 往往比把类别塞进legend更高级；
- 4个点如果只为“看起来二维”，不要撑一整张scatter；
- 但若二维 trade-off / dominance 本身就是 claim，少量点也可以使用 Pareto/scatter，并用紧凑坐标域与直接标签提高密度。

---

## 5. 成本 / 收益 / 风险分解

### 优先候选
- signed contribution；
- sorted contribution forest；
- value bridge / waterfall；
- baseline-to-optimum slope；
- cost-service / risk-service trade-off；
- Pareto。

### Waterfall 准入
必须同时满足：
1. 各增量可加总闭合；
2. 分解本身就是 Primary question；
3. baseline 和 total 有明确业务语义。

否则优先 contribution / comparison，而不是 waterfall。

---

## 6. 机制 / 流量 / 网络

### 优先候选
- real network flow；
- mini-Sankey / alluvial；
- staged response strip；
- timeline + glyph；
- state-transition diagram；
- mechanism figure with real method object。

机制/物理图的具体实现工具、短标签、图标预算、Draw.io 与 image-generation 路由另见 `mechanism_figure_contract.md`。

### 准入
Sankey/alluvial 必须是真实可守恒的 flow；不是“有几阶段”就画流图。

机制图不能只是：

```text
Input → Model → Output
```

必须嵌入真实对象：网络拓扑、decision region、约束、actual distribution、before/after pattern 等。

---

## 7. 分布 / 样本 / 不确定性

### Statistical
raw points / ECDF / box / violin / raincloud / CI。

### Scenario
scenario points / weighted contribution / envelope / small multiples。

### Parametric
sensitivity curve / interval / regime / tornado。

### Numerical
residual / gap / convergence / feasibility certificate。

禁止把 scenario range、numerical tolerance 和 statistical CI 混为一谈。

若样本量和分布结构足够，优先 raincloud/violin+raw/ECDF 等能展示分布的 grammar，而不是 bar of means。

---

## 8. 复杂曲线 / 多对象

出现以下任一条件优先进入 Complexity Decomposition Gate：
- >4条高度纠缠曲线；
- y-scale差异明显；
- legend ping-pong；
- ROI被全局尺度压缩；
- 一个axes同时需要3类以上编码。

优先：
- small multiples；
- overview + justified zoom；
- hero + witness column；
- context grey + focus highlight；
- direct end labels。

---

## 9. Invariant Subtraction

如果大分量跨比较对象不变：

```text
Total = fixed baseline + changing residual
```

优先只画 residual / delta，并把 fixed baseline 放成 reference text / metadata / caption。

固定大分量不应该成为最大彩色区域。

---

## 10. Figure Enhancement 快速索引

| 当前视觉问题 | 优先增强 | 准入标准 |
|---|---|---|
| 全局尺度压缩关键差异 | Local Zoom | zoom 新增真实可验证信息 |
| 多曲线纠缠 | Small Multiples | 分面后比较更快且尺度说明清楚 |
| 对象很多但只关注少量 | Focus Highlighting | context 降权不隐去例外 |
| 有真实风险区/可行区 | Semantic Background | 背景区域来自真实阈值 |
| 主关系+误差共同构成可信度 | Composite Diagnostic | panel 是同一claim的互补证据 |
| 真实第三维不可替代 | Conditional 3D | 二维会丢失核心关系 |

---

## 11. 同一 Figure Suite 的 grammar 管理

正式全文绘图时填写 `figure_suite_manifest.md`。

同一 visual grammar 可以重复，但必须说明：
- perceptual task 相同；
- 该 grammar 仍为最高分候选；
- 重复强化 paper-family consistency，而非偷懒。

禁止：
- 全文都 dumbbell；
- 全文都 bar；
- 为了多样而乱上 ternary/Sankey/3D；
- 为了“稳妥”又把全篇高级候选都降级成普通 bar/line。

---

## 12. 最终选型判定

每个候选最终问 8 个问题：

```text
1. 一眼能回答 Primary question 吗？
2. 是否用尽可能准确的视觉通道？
3. 是否隐藏了分布/例外/边界？
4. 是否存在更有信息增益的高级 grammar？
5. 若用了高级 grammar，它是否真的比 simpler fallback 更快读？
6. 最醒目的对象是不是最重要的证据？
7. 数据语义（连续/离散/守恒/不确定性）是否诚实？
8. 它和整篇 Figure Suite 是否既一致又不重复？
```

若第4项为“有”却未评估，或其余任意2项明显回答“不”，重新选型。
