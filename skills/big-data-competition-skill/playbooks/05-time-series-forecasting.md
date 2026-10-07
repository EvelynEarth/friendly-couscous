# 05 时间序列预测

> 适用：需求/货量/库存、台风路径/风速/雨量等随时间预测。先锁定预测粒度、预测跨度（horizon）、历史窗口与官方指标。

## 1. 指标（以当届为准）

```python
# 供应链常用 WMAPE（加权/总量相对误差）
wmape = np.abs(y-p).sum()/np.abs(y).sum(); score = 1-wmape
# 另有 RMSE / MAE / MAPE；多序列可分层报告
```

## 2. 验证：只能按时间，不随机打乱

```python
from sklearn.model_selection import TimeSeriesSplit
# 滚动/扩展窗口；最后一段作为外样本 holdout
tscv = TimeSeriesSplit(n_splits=5)
```
验证要复现真实预测：只用预测时点之前的数据；多步预测明确递归/直接/多输出策略。

## 3. 分层方法（从简单基准开始，逐层升级）

### A. 必做基准与统计模型

```python
# 朴素/季节朴素（最小基准）
naive = y_train.shift(seasonal_period)
# ETS / 指数平滑、ARIMA/SARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
m = ExponentialSmoothing(y_train, trend="add", seasonal="add",
                         seasonal_periods=7).fit()
m = SARIMAX(y_train, order=(1,1,1), seasonal_order=(1,1,1,7)).fit()
# 小样本/少数据：灰色 GM(1,1)；规则化趋势：Prophet
```
优秀论文中 ARIMA 211、ETS 89、灰色 93、Prophet 59 次出现；2024 年 Prophet/ARIMA 高频。

### B. 机器学习（带滞后/滚动特征，常优于纯统计）

```python
# 构造滞后与滚动统计
def make_lags(s, lags, wins=(3,7,14)):
    f = pd.DataFrame({f"lag{k}": s.shift(k) for k in lags})
    for w in wins:
        f[f"roll_mean{w}"] = s.shift(1).rolling(w).mean()
        f[f"roll_std{w}"] = s.shift(1).rolling(w).std()
    return f
X = make_lags(y, lags=range(1,15))
# 用 RF / XGB / LGBM 拟合（可自然加入外生变量、促销标记、商品/仓库属性）
```

### C. 深度学习（序列长、模式复杂时）

```python
# LSTM / GRU / BiLSTM；需标准化、序列窗口化
# 注意小样本易过拟合，必须保留统计/树模型作基准
```
LSTM/GRU 在 40 篇中出现 234 次（2024 达 163）。

## 4. 三类困难场景（MathorCup 常考）

- **序列分类**：按数理统计特征（最小/最大/中位数/四分位/均值/方差/自相关）对“商家-仓库-商品”序列聚类或分类，同类用同类方法（KMeans/KMeans++、层次聚类、DBSCAN）。
- **冷启动/新维度**：历史过短的新品/新仓，用商品/商家/仓库属性找**相似序列**（同分类、同区域），借相似序列预测；无历史时用均值/灰色/同类中位数。
- **促销/结构突变**：用历史同期（如去年双十一）作参考，加促销标记与外生变量；不要把促销峰值当普通趋势外推。

## 5. 多步预测策略

```python
# 递归：用预测值再生成滞后，误差会累积
# 直接：为每个 horizon 训一个模型
# 多输出：一次输出未来 H 步（LSTM 多输出 / 多输出树）
```
与当届 horizon 一致；长 horizon 优先直接/多输出。

## 6. 验证要点

- 必须显著优于朴素/季节朴素基准，复杂模型才有理由。
- 报告尺度相关 + 尺度无关两类指标，给预测区间（覆盖率）。
- 检查残差均值/自相关、极端时段（促销）与结构突变。
- 多窗口、多种子验证稳定性；不把训练拟合误差当外样本成绩。
