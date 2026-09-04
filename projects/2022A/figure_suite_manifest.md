# 2022A Figure Suite Manifest

> Q1 Figure Evidence 已由用户确认并作为 paper-family 风格锚点。Q2 主结果与 `问题二结果深化分析.xlsx` 已通过质量门；当前 Q2 Figure Evidence 只读取这两个 accepted 工作簿，不重新求解 ODE、不重新运行 DE/Powell，也不再强制依赖额外的边界稳态精修工作簿。

## 1. Figure Suite

| Figure ID | Question | Evidence level | One-sentence claim | Hero evidence | Visual grammar | Why unique in suite | Paper-family anchor | Manuscript position | Status |
|---|---|---|---|---|---|---|---|---|---|
| FQ1-1 | Q1 | L1 | 两种阻尼下浮子与振子均由初始瞬态进入有界周期响应，但时程轨迹与量值不同 | 0–179.4 s 四个状态量完整时程 | 2×2 time-series small multiples + difference-driven local zoom | 唯一直接展示 Q1 主状态时程，回答“发生了什么” | anchor | Q1 主结果段 | accepted |
| FQ1-2 | Q1 | L3 | 两种阻尼第35–39周期均满足2%重复性判据，稳态指标最大相对差异约2.23% | 8项重复性最大偏差 + 4项稳态相对差异 | 1×2 horizontal bars + threshold | 唯一回答“是否稳定、结构改变后是否保持”，不重复主时程 | anchor | Q1 稳定性/比较讨论 | accepted |
| FQ2-1 | Q2 | L1 + L2 paired | 主候选 a≈99999.863 明显趋向题面上边界，n≈0.413680 位于局部峰值附近；幂律稳态平均功率较最优直线阻尼仅提高约0.287% | `局部敏感性` + `结论总览` + `核心指标` | 1×2 local-delta bars + incremental gain | 同屏回答“参数结构是什么、稳态收益多大”，并严格区分60T搜索诊断与正式稳态功率 | inherit Q1 | Q2 主结果/参数讨论 | proposed / awaiting MATLAB review |
| FQ2-2 | Q2 | L4 | 幂律主候选在 T/40 与 T/80 两套步长下均于170T满足周期稳态判据，最终步长相对功率差约3.49e-9 | `收敛诊断` + `稳健性证据` | 1×2 convergence lines + log-threshold diagnostic | 唯一承担 Q2 数值合法性，不与参数结构/收益图重复 | inherit Q1 | Q2 数值验证/结果末段或附录 | proposed / awaiting MATLAB review |

## 2. Cross-Figure Grammar Registry

| Grammar | Used by | Primary task | Reuse allowed? | Reason |
|---|---|---|---|---|
| time-series small multiples | FQ1-1 | complex traces / exact temporal comparison | conditional | 仅当后续小问同样需要多状态时程直接比较且仍为最高效方案时复用 |
| difference-driven local zoom | FQ1-1 | reveal small local curve differences | yes | 只有全局尺度压缩真实差异时才启用 |
| horizontal threshold bars | FQ1-2(a) | threshold / diagnostic | yes | 阈值判断任务可复用，但阈值语义必须来自真实题设或预先分析判据 |
| horizontal delta bars | FQ1-2(b), FQ2-1 | exact small comparison / gain | yes | Q2 用相对候选/相对最优直线阻尼的差值避免绝对约229 W尺度掩盖小差异 |
| convergence dual-line | FQ2-2(a) | compare discretization-refined convergence | yes | T/40 与 T/80共享周期节点与功率单位，适合同轴直接比较 |
| log threshold diagnostic | FQ2-2(b) | show multiple residuals crossing a tolerance | yes | 相对差跨数量级，log y轴能直接展示1e-5判据 |

## 3. Suite Redundancy Gate

- FQ1-1 是 Q1 L1 主结果；FQ1-2 是 Q1 L3 稳健性，claim 与证据粒度不同。
- FQ2-1 Panel (a) 只使用深化分析已写出的局部扰动差值，支持“a明显趋向上边界、n位于局部峰值附近”；不把 60T 搜索邻域冒充最终稳态边界最优证明。
- FQ2-1 Panel (b) 只画正式稳态平均功率相对最优直线阻尼的增量，避免 229 W 绝对尺度掩盖约0.6585 W / 0.2871% 的有限收益。
- FQ2-2 只承担 L4 数值合法性：T/40/T/80 稳态功率以及功率窗口/同相位状态相对差，不重复 FQ2-1 的参数结构与收益。
- 不制造二维 `(a,n)` 稳态功率曲面：accepted 工作簿没有保存完整二维稳态曲面，MATLAB 不允许从摘要数值反推或重新跑优化。
- 不把 DE/Powell 的 `search_power` 画成最终功率结论；深化分析已明确该量只属于60T搜索诊断。

## 4. Paper-family Style Registry

当前 anchor：Q1 用户已确认的 Figure Evidence。

- 字体：优先 `Microsoft YaHei` / `Microsoft YaHei UI`，无则回退 `SimHei` / `Noto Sans CJK SC` / `Arial`。
- 主色职责：蓝色系 = 基准/主结果；红色系 = 对照/步长加密；橙色系 = 参数敏感性/阈值焦点；灰色 = 基准线、阈值说明或上下文。
- 坐标轴：`TickDir=out`、`Box=off`、不默认网格化；正文图线宽约1.4–1.7。
- 图例：优先横向放于 panel 外或不遮挡数据处。
- 默认只保留 MATLAB 图窗供人工 Figure QA，不自动批量导出。

## 5. Figure Order

正文建议顺序：

```text
FQ1-1 Q1 主时程（what）
→ FQ1-2 Q1 稳定性（does it hold）
→ FQ2-1 Q2 参数结构与收益（where/how much）
→ FQ2-2 Q2 数值合法性（can we trust it）
```

Q2 当前绘图脚本：`问题二求解/q2_plot.m`。
当前数据依赖：`问题二求解结果.xlsx + 问题二结果深化分析.xlsx`。
Figure QA 未完成前，FQ2-1/FQ2-2 不标记 accepted。
