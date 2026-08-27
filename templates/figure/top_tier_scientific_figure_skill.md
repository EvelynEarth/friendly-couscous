# Top-tier Scientific Figure Skill

本文件是 `modules/04_figure_evidence.md` 的高阶科研绘图执行补充，不建立第二套 Figure 决策权威。Module 04 仍负责 Evidence level、Primary question、Layout Gate、Enhancement Gate、Source workbook 与 Figure Contract；本文件负责把已批准的 Figure Contract 落到“论文级视觉原型 → render-review → MATLAB 实现”。

## 0. 适用范围

适用于数学建模、优化、仿真、风险、网络、空间、时序、参数敏感性与多目标结果图。默认中文论文环境；英文期刊风格只能借鉴信息组织与视觉语法，不得机械复制英文字体、英文标签或期刊截图。

## 1. 核心原则：Evidence before chart

禁止先问“画什么高级图”。必须先完成：

```text
Core conclusion
→ Evidence task
→ Data structure
→ Perceptual task
→ Candidate chart grammar
→ Paper-size geometry
→ Prototype render
→ Visual review
→ MATLAB implementation
```

图型选择优先级遵守视觉感知效率：

```text
位置 / 对齐
> 长度 / 方向
> 形状 / 连续轨迹
> 面积
> 色相 / 饱和度
> 装饰性效果
```

能用位置、长度、排序或连接关系表达定量差异时，不让颜色承担主要定量任务。

## 2. Candidate chart grammar：先展开图型池，再淘汰

每个 Primary question 至少考虑 3 类候选，不能只在 bar / line / heatmap / dumbbell / waterfall 中循环。

### 2.1 参数空间与稳健性

候选：
- phase / regime diagram；
- decision-region map；
- threshold slice + overview；
- contour / response surface（仅连续真实响应）；
- forest / tornado；
- small-multiple sensitivity strips；
- transition / regime path。

离散扫描默认不插值；若真正连续边界不存在解析/连续模型证据，使用离散矩阵、切片或区间，不伪造平滑边界。

### 2.2 机制、流量与资源响应

候选：
- Sankey / alluvial；
- staged flow / response-state strip；
- network flow；
- timeline + quantitative glyph；
- ternary composition trajectory；
- stepwise allocation diagram；
- small-multiple composition strips。

只有存在真实“流”或守恒量时使用 Sankey/alluvial；阶段构成变化但不是跨阶段货物流转时，优先 ternary / composition trajectory / stage strips，并明确语义。

### 2.3 方案差异、替代最优与公平性

候选：
- dumbbell / slopegraph；
- paired interval；
- Cleveland / lollipop；
- rank transition；
- alluvial transition；
- parallel coordinates（变量足够多且共享尺度含义）。

没有变化的对象应作为上下文降权或文字汇总，不为了“完整”制造大量重合点。

### 2.4 成本、收益与目标分解

候选：
- value bridge / waterfall；
- balance ledger；
- paired baseline-to-optimum slope；
- decomposition strip；
- cost-benefit interval / bullet；
- Pareto front（只有多目标权衡时）。

Waterfall 只在增量可加总且闭合时使用；否则不要为视觉效果强行做桥接。

### 2.5 分布、不确定性与模型合法性

候选：
- ECDF；
- raincloud / violin / boxen；
- raw points + interval；
- fan / ribbon；
- residual diagnostic；
- calibration / observed-vs-predicted；
- Pareto + constraint violation。

## 3. Paper-size first

不要以 MATLAB 最大化窗口作为审美标准。先确定论文中的目标物理宽度，再决定字体、线宽、marker 和 annotation 密度。

建议：
- 单栏图：约 80–90 mm；
- 双栏图：约 165–180 mm；
- 复杂双 panel 默认双栏；
- 先按最终尺寸检查可读性，再允许更大窗口展示。

任何在缩小到论文尺寸后无法读取的标签，都视为失败。

## 4. Color Role Contract

先定义角色，再选颜色；禁止先挑色板。

默认最多：
- 1 个主方案色；
- 1 个 adverse / risk 色；
- 灰阶上下文。

同一 Figure 通常不超过 2 个有语义的强调色。辅助对象通过低饱和度、透明度、线宽和灰度降权，而不是继续新增颜色。

禁止：
- rainbow / jet 用于定量连续值；
- 无业务语义的大面积背景色；
- 每个指标一支颜色；
- 彩色文字承担大量解释；
- 颜色重复编码已经由位置/长度清楚表达的数值。

## 5. Annotation Budget

默认每个 axes 只保留 3–5 个不可替代标注：阈值、极值、基准、推荐点、失效点、关键改善。

不为每个数据点贴数字。大量精确数字进入表格或正文。

## 6. Render–Review–Iterate Gate（硬门）

这是本补充最重要的执行规则。

**不得在只完成绘图代码时声称 Figure 已完成。**

生成最终 MATLAB 文件前，必须先对真实 accepted 数据制作可渲染视觉原型，并执行至少一轮：

```text
render PNG
→ read rendered image
→ critique body geometry
→ revise
→ render again
```

审查顺序固定：

1. body geometry：版心占用、比例、panel balance、留白；
2. visual hierarchy：第一眼焦点是否等于 Core conclusion；
3. perceptual efficiency：是否用最直接的视觉变量表达差异；
4. label collision / clipping；
5. legend search cost；
6. color role consistency；
7. 缩小到论文尺寸后的可读性；
8. 最后才做装饰性 polish。

若 body geometry 未通过，禁止只靠换色修图。

## 7. Prototype before MATLAB

当容器无 MATLAB 时：
- 可使用 Python/Matplotlib 仅制作“视觉原型”；
- 原型必须读取同一 accepted workbook 的真实数据；
- 原型不得重新求解；
- 原型可用于图型、布局、标注密度与配色审查；
- 通过审查后再将视觉语法翻译成 MATLAB。

MATLAB 版本必须保持数据映射、图型职责、panel 语义和主要视觉层级与通过审查的原型一致。

## 8. Body-first Review

用户提供 MATLAB 截图后，先判断：
- 主体图型是否成立；
- 数据是否被错误压缩或拉伸；
- panel 是否必要；
- 是否存在大面积无效空白；
- 重点是否被图例/标题/注释抢走。

若失败，允许 partial reopen geometry / chart type；不要在失败架构上无限 vN 调色。

## 9. Data honesty

- 离散点不 spline；
- 独立场景点不伪造连续曲线；
- ROI 不截轴夸大；
- ternary / Sankey / alluvial 必须明确是否表示组成、路径还是货物流；
- 颜色区间只表示真实状态/阈值；
- 替代最优与数值残差必须采用业务/数值容差，不能把求解器残差画成实质差异。

## 10. External methodological references

本 Skill 吸收以下公开方法论，不复制具体图稿：
- Nature Methods, Points of View series / Points of View, anew (2026)
- Bang Wong / Martin Krzywinski / Nils Gehlenborg: scientific visualization advice on design, layout, color and symbols
- PLOS Computational Biology visualization / figure communication guidance
- `gramm`: Grammar of Graphics for MATLAB
- `hanlulong/matlab-plot-skill`: render-review-iterate workflow for scientific MATLAB figures

外部资料只提供方法论；项目真值、字段、阈值、结论和视觉职责仍以本仓库 Module 04 + accepted workbook 为准。
