# 08 库存与优化

> 适用：补货计划、资源/订单/仓库分配、路径、调度与多目标权衡（2022 A、2023 B、2024 B）。先识别决策主体、决策时点、决策变量、可行域、目标。

## 1. 库存：周期性盘点 (s,S)

```python
# NRT=盘点周期，LT=提前期，期初库存给定；盘点时若库存 T<s 则补到 S，补货量 Q=S-T
# 依据预测需求 + 提前期需求 + 安全库存定 s；S=s+周期需求（结合成本）
# 逐日：期初+补货-需求=期末；目标：降低持有/缺货成本、提高服务水平、降低周转天数
```

```python
# 最小仿真（逐日滚动）
inv = init
for d in dates:
    if d % NRT == 0 and inv < s[d]:
        Q = S[d]-inv; arrive[d+LT] += Q
    inv += arrive[d]-forecast[d]
    hold += max(inv,0)*h; short += max(-inv,0)*p   # h 持有、p 缺货成本
```
成本与商品价格正相关时，明确假设并给出 h/p 取值依据。

## 2. 数学规划（优先，可解释且可证最优）

```python
# 线性/整数规划：订单分配、一品一仓/多仓、0-1 选择
import pulp
prob = pulp.LpProblem("alloc", pulp.LpMaximize)
x = pulp.LpVariable.dicts("x", idx, lowBound=0, cat="Binary")  # 或 Integer/Continuous
prob += pulp.lpSum(obj[i]*x[i] for i in idx)                  # 目标
for k in constraints: prob += pulp.lpSum(A[k][i]*x[i] for i in idx) <= b[k]
prob.solve(pulp.PULP_CBC_CMD(msg=0)); pulp.LpStatus[prob.status]
```
按结构选 LP / MILP / QP / SOCP / NLP；报告求解器状态、约束最大违反量、目标值、对偶/间隙。

## 3. 多目标：不直接把异质目标相加

- 量纲不同先归一化；权重需有来源（题给/熵权/CRITIC），或用 Pareto。
- 题给加权（如 2022 A：αA-βB-γC，α=.78 β=.025 γ=.195）则严格按题给口径。

```python
# NSGA-II（Pareto 前沿）或 MOPSO；2024 B 高频（NSGA 30、MOPSO 45 次）
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
# res.F 为 Pareto 目标；再按偏好/权重从前沿选方案
```

## 4. 启发式（规模大/非凸、精确法不足时）

```python
# 贪心（2022 A 订单分配）：按规则排序后逐单分配给当前最优可行对象
# 遗传/粒子群/模拟退火：多初值 + 局部精修；必须有可解释基准对照
```
贪心 34、PSO 45、模拟退火 39、遗传 12 次出现。启发式需报告重复运行、解质量与时间复杂度，**不宣称无证明的全局最优**。

## 5. 约束闭环

- 每条约束对应现实机制与代码检查；硬约束不能用惩罚项代替。
- 输出可行性校验：全分配、容量上限、时间窗/到达提前量、变量取值域。

## 6. 验证要点

- 与基准（松弛解/贪心/已知可行解）对比，报告最优性证据或间隙。
- 精确问题报告 KKT/对偶；非凸问题多初值 + 上下界。
- 参数扰动（如不同压单阈值/权重）做敏感性，给建议取值。
- 推荐方案、变量明细、约束检查可追溯（见 `experiment-provenance.md`）。
