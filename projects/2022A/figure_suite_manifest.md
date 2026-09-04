# 2022A Figure Suite Manifest

> Q1 Figure Evidence 已由用户确认并作为 paper-family 风格锚点。Q2 主结果与边界稳态精修均已通过质量门；用户明确要求先直接进入 Q2 绘图，因此本次 Q2 Figure 只读取已验收的 `问题二求解结果.xlsx` 与 `问题二边界稳态精修结果.xlsx`，不等待尚未本地运行的 `问题二结果深化分析.xlsx`，也不在 MATLAB 中重新求解或优化。

## 1. Figure Suite

| Figure ID | Question | Evidence level | One-sentence claim | Hero evidence | Visual grammar | Why unique in suite | Paper-family anchor | Manuscript position | Status |
|---|---|---|---|---|---|---|---|---|---|
| FQ1-1 | Q1 | L1 | 两种阻尼下浮子与振子均由初始瞬态进入有界周期响应，但时程轨迹与量值不同 | 0–179.4 s 四个状态量完整时程 | 2×2 time-series small multiples + difference-driven local zoom | 唯一直接展示 Q1 主状态时程，回答“发生了什么” | anchor | Q1 主结果段 | accepted |
| FQ1-2 | Q1 | L3 | 两种阻尼第35–39周期均满足2%重复性判据，稳态指标最大相对差异约2.23% | 8项重复性最大偏差 + 4项稳态相对差异 | 1×2 horizontal bars + threshold | 唯一回答“是否稳定、结构改变后是否保持”，不重复主时程 | anchor | Q1 稳定性/比较讨论 | accepted |
| FQ2-1 | Q2 | L1 + L2 paired | 幂律最优比例系数落在 a=100000 上边界，n≈0.416065 形成内部稳态峰值；相较最优直线阻尼平均功率仅提高约0.288% | `局部稳态扫描` + 直线/二维候选/边界精修最终功率 | 1×2 local response curve + incremental horizontal bars | 同屏回答“最优在哪里、比线性好多少”，不把微小收益埋在绝对功率尺度里 | inherit Q1 | Q2 主结果/优化结构段 | proposed / awaiting MATLAB review |
| FQ2-2 | Q2 | L4 | 最终幂律候选在 T/40 与 T/80 两套步长下均于170T达到周期稳态，最终功率差仅约4.26e-9（相对） | `收敛诊断` 的后窗口功率、功率相对差、同相位状态相对差 | 1×2 convergence lines + log-threshold diagnostic | 唯一承担 Q2 数值合法性，不与主结果图重复 | inherit Q1 | Q2 数值验证/附录或结果末段 | proposed / awaiting MATLAB review |

## 2. Cross-Figure Grammar Registry

| Grammar | Used by | Primary task | Reuse allowed? | Reason |
|---|---|---|---|---|
| time-series small multiples | FQ1-1 | complex traces / exact temporal comparison | conditional | 仅当后续小问同样需要多状态时程直接比较且仍为最高效方案时复用 |
| difference-driven local zoom | FQ1-1 | reveal small local curve differences | yes | 只有全局尺度压缩真实差异时才启用 |
| horizontal threshold bars | FQ1-2(a) | threshold / diagnostic | yes | 阈值判断任务可复用，但阈值语义必须来自真实题设或预先分析判据 |
| horizontal delta bars | FQ1-2(b), FQ2-1(b) | exact small comparison / gain | yes | Q2 用“相对最优直线阻尼增量”避免绝对229 W尺度掩盖0.66 W收益 |
| local response curve | FQ2-1(a) | locate an interior optimum on a validated boundary | yes | 只连接工作簿已有稳态扫描点，不在 MATLAB 内插值或重求目标函数 |
| convergence dual-line | FQ2-2(a) | compare discretization-refined convergence | yes | T/40 与 T/80共享周期节点与功率单位，适合同轴直接比较 |
| log threshold diagnostic | FQ2-2(b) | show multiple residuals crossing a tolerance | yes | 相对差跨数量级，log y轴比线性轴更能展示1e-5判据 |

## 3. Suite Redundancy Gate

- FQ1-1 是 Q1 L1 主结果；FQ1-2 是 Q1 L3 稳健性，claim 与证据粒度不同。
- FQ2-1 只回答 Q2 的优化位置与收益：Panel (a) 直接使用边界精修工作簿的 `局部稳态扫描`，Panel (b) 只画相对最优直线阻尼的功率增量，因此不会因两种方案都约229 W而视觉重叠。
- FQ2-2 只承担 L4 数值合法性：T/40/T/80 稳态功率与功率/同相位状态相对差，不重复 FQ2-1 的参数最优性。
- 不额外制造 Q2 二维 `(a,n)` 功率曲面：当前 accepted 工作簿没有保存完整二维稳态曲面，MATLAB 不允许从摘要数值反推或重新跑优化，因此该图证据目前不成立。
- 不单独画“DE/Powell 迭代次数”图；它属于搜索诊断，且最终答案已被上边界真正稳态精修替代。

## 4. Paper-family Style Registry

当前 anchor：Q1 用户已确认的 Figure Evidence。

- 字体：优先 `Microsoft YaHei` / `Microsoft YaHei UI`，无则回退 `SimHei` / `Noto Sans CJK SC` / `Arial`。
- 主色职责：蓝色系 = 基准/主结果；红色系 = 对照/原候选；橙色系 = 最终精修/关键焦点；灰色 = 基准线、阈值说明或上下文。
- 坐标轴：`TickDir=out`、`Box=off`、不默认网格化；正文图线宽约1.4–1.7。
- 图例：优先横向放于 panel 外或不遮挡数据处。
- 默认只保留 MATLAB 图窗供人工 Figure QA，不自动批量导出。

## 5. Figure Order

正文建议顺序：

```text
FQ1-1 Q1 主时程（what）
→ FQ1-2 Q1 稳定性（does it hold）
→ FQ2-1 Q2 最优在哪里、收益多大（where/how much）
→ FQ2-2 Q2 数值合法性（can we trust it，必要时正文末段或附录）
```

Q2 当前绘图脚本：`问题二求解/q2_plot.m`。Figure QA 未完成前，FQ2-1/FQ2-2 不标记 accepted。
