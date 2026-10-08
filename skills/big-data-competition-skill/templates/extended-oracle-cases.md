# v2.7 科学复算输入模板（以下数字只供手算验证，不是真实赛题结果）

执行：

```bash
python skills/big-data-competition-skill/tools/extended_oracles.py --case check.json
```

每次把**下方任意一个对象**保存为独立 JSON 文件。真实任务需使用未污染的真实数据或从原始代码独立生成的小规模数学子问题，核实所选的任务是否满足对应的统计/解析假设。

## 1. 时序滚动验证

```json
{
  "task": "rolling_forecast",
  "required_gap": 1,
  "folds": [
    {"series_id":"A","train_start":0,"train_end":3,"valid_start":5,"valid_end":6,"actual":[2,4],"predicted":[1,5]},
    {"series_id":"A","train_start":0,"train_end":6,"valid_start":8,"valid_end":9,"actual":[3,5],"predicted":[2,7]}
  ],
  "reported": {"mae":1.25,"rmse":1.3228756555322954}
}
```

手工复核四个误差绝对值为 1、1、1、2；MAE=5/4，RMSE=√(7/4)。整数坐标是等间距观测的索引；不表示实际自然日期，实际特征工程是否包含未来信息还必须独立检查。

## 2. 配对随机化检验

```json
{
  "task":"paired_signflip",
  "treatment":[2,2,2,2,2,2],
  "control":[1,1,1,1,1,1],
  "pairing_key":"same-entity-at-fixed-horizon",
  "exchangeable_signs_under_null":true,
  "threshold_predeclared":true,
  "alpha":0.05,
  "reported_p_value":0.03125
}
```

手算六个差值均为 1，在 64 种符号翻转中只有 2 种达到原始绝对差和 6，故双侧 p=2/64。**这不是实际研究显著性证据**；仅当零假设下符号可交换、配对独立等条件成立时才有相应推断意义。

## 3. 独立同分布伯努利仿真

```json
{
  "task":"bernoulli_mc",
  "observations":[1,0,1,0,1,0,1,0,1,0],
  "sampling_scheme":"iid_bernoulli",
  "confidence_level":0.95,
  "precision_predeclared":true,
  "max_ci_half_width":0.2,
  "reported_probability":0.5
}
```

此例 n=10，样本估计为 0.5，Wilson 95% 区间半宽大于 0.2，因此预期得到 `insufficient_precision` 且 CLI 返回非零退出码。这是刻意保留的**失败示例**，不能偷偷放宽精度目标。

## 4. 可分离严格凸二次模型

```json
{
  "task":"separable_convex_quadratic",
  "sense":"minimize",
  "quadratic":[1,2],
  "linear":[-4,-8],
  "bounds":[[0,5],[0,5]],
  "candidate":[2,2],
  "claimed_objective":-12
}
```

目标 (f(x,y)=x^2+2y^2-4x-8y)，盒约束 (0≤x,y≤5)。一阶条件给出 (x^*=(2,2))，全局最小目标 -12。严格凸性保证该**指定数学模型**的解唯一，但不能据此推断一般优化模型或比赛真题的最优性。

参阅 [方法和适用边界](../references/extended-oracles.md)。
