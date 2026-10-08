# 独立参考求解器 JSON 案例模板（v2.6）

> 以下全部是**人工推导的玩具数值**，不是任何真实赛题分数。正式使用时，输入必须取自已锁定的数据和求解结果，并另行验证真实标签是否可合法使用。

## A. 回归：指标重算

```json
{
  "task": "regression",
  "actual": [0, 2, 4],
  "predicted": [1, 1, 5],
  "reported": {"mae": 1, "rmse": 1}
}
```

从三个误差的绝对值均为 1 可手算：MAE=1，RMSE=1。使用时按官方指标及数据隔离要求选择验证集；未经过独立抽样、合规划分或法定结果的真实标签不得被假装成测试成绩。

## B. 分类：明确标签口径的宏平均

```json
{
  "task": "classification",
  "labels": ["A", "B"],
  "actual": ["A", "A", "B", "B"],
  "predicted": ["A", "B", "B", "B"],
  "reported": {
    "accuracy": 0.75,
    "macro_precision": 0.8333333333333334,
    "macro_recall": 0.75,
    "macro_f1": 0.7333333333333333
  }
}
```

按顺序给定全部真实类别。混淆矩阵（行=真实类，列=预测类）为 `[[1,1],[0,2]]`；A 类 F1=2/3，B 类 F1=4/5，macro-F1=11/15。零分母以 0 处理，包括整个验证集未出现但在固定类别集合中的类别。具体比赛如果使用加权 F1、micro F1 或特殊类指标，应在其他独立实现中按官方定义重新计算，而非冒充本工具支持。

## C. 小规模整数优化：独立精确枚举

```json
{
  "task": "bounded_integer_linear",
  "sense": "maximize",
  "objective": [3, 2],
  "bounds": [[0, 4], [0, 4]],
  "constraints": [
    {"op": "le", "weights": [2, 1], "rhs": 7},
    {"op": "le", "weights": [1, 2], "rhs": 7}
  ],
  "candidate": [3, 1],
  "claimed_objective": 11
}
```

模型是 max `3x+2y`，满足 `2x+y<=7`、`x+2y<=7`、`0<=x,y<=4` 且整数。枚举 25 个状态得到可行最优 `(3,1)`、值 11。若把候选改成可行但次优的 `[2,2]`、目标 10，应报告 disagreement，差距为 1；若输入更大、超过 **100,000** 状态，工具将中止，不能声称检查了真实大规模全局最优。

## 命令

```bash
python skills/big-data-competition-skill/tools/independent_oracle.py --case actual_check.json
```

这个模板覆盖的只是三种明确的可复算数值问题，不能取代模型假设审查、随机稳定性分析、因果识别或不同算法实现的真实交叉验证。详见 [验证边界和论文使用方法](../references/independent-recomputation.md)。
