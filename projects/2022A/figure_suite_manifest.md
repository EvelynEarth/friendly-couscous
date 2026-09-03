# 2022A Figure Suite Manifest

> 当前只登记已经完成数值验收的 Q1。Q2-Q4 尚未进入 Figure Evidence，不预先虚构图表。

## 1. Figure Suite

| Figure ID | Question | Evidence level | One-sentence claim | Hero evidence | Visual grammar | Why unique in suite | Paper-family anchor | Manuscript position | Status |
|---|---|---|---|---|---|---|---|---|---|
| FQ1-1 | Q1 | L1 | 两种阻尼下浮子与振子均由初始瞬态进入有界周期响应，但时程轨迹与量值不同 | 0–179.4 s 四个状态量完整时程 | 2×2 time-series small multiples | 唯一直接展示 Q1 主状态时程，回答“发生了什么” | pending screenshot review | Q1 主结果段 | proposed |
| FQ1-2 | Q1 | L3 | 两种阻尼第35–39周期均满足2%重复性判据，稳态指标最大相对差异约2.23% | 8项重复性最大偏差 + 4项稳态相对差异 | 1×2 horizontal bars + threshold | 唯一回答“是否稳定、结构改变后是否保持”，不重复主时程 | pending screenshot review | Q1 稳定性/比较讨论 | proposed |

## 2. Cross-Figure Grammar Registry

| Grammar | Used by | Primary task | Reuse allowed? | Reason |
|---|---|---|---|---|
| time-series small multiples | FQ1-1 | complex traces / exact temporal comparison | conditional | 仅当后续小问同样需要多状态时程直接比较且仍为最高效方案时复用 |
| horizontal threshold bars | FQ1-2(a) | threshold / diagnostic | yes | 阈值判断任务可复用，但阈值语义必须来自真实题设或预先分析判据 |
| horizontal delta bars | FQ1-2(b) | delta / exact comparison | yes | 适用于少量明确相对差异，不用于连续趋势 |

## 3. Suite Redundancy Gate

- FQ1-1 是 L1 主结果，使用主工作簿 `仿真明细` 的完整时序；FQ1-2 是 L3 稳健性，使用深化工作簿的周期重复性和结构差异指标，claim、数据粒度和 visual task 均不同。
- 不新增单独的“指定时刻结果图”，因为其信息已被时程图覆盖，表格更适合精确报告 10/20/40/60/100 s 数值。
- 不把数值收敛误差单独放入正文 Figure；Case1/Case2 数值合法性属于 L4，当前以工作簿质量门和正文/附录表述承担，避免抢占 Q1 主结果视觉资源。

## 4. Paper-family Style Registry

当前状态：`pending`。在用户返回 MATLAB 图窗并明确认可后，以首先通过 Figure QA 的 Q1 Figure 作为 paper-family anchor，再冻结字体、轴线权重、主/次颜色职责、legend strategy、panel gap 与 annotation density。

## 5. Figure Order

正文顺序固定为：

```text
FQ1-1 主结果（what）
→ FQ1-2 稳健性/边界（when/does it hold）
```

L4 数值合法性证据不前置于主结果。
