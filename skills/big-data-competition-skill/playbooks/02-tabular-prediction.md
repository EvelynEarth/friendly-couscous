# 02 表格预测：回归 / 分类

> 适用：表格数据的价格/金额/货量回归，或类别/评分/满意度分类。先锁定当届**官方指标**。

## 1. 指标（以当届题面为准）

```python
from sklearn import metrics
# 回归
metrics.mean_absolute_error(y, p)                 # MAE
np.sqrt(metrics.mean_squared_error(y, p))        # RMSE
metrics.r2_score(y, p)                           # R2
# 价格类常用 MAPE / Accuracy-k（相对误差在 k% 内占比）
mape = np.mean(np.abs((y-p)/np.where(y==0,1,y)))
acc5 = np.mean(np.abs((y-p)/np.where(y==0,1,y)) <= .05)
# 分类
metrics.accuracy_score(y, p)
metrics.f1_score(y, p, average="macro")          # 多类/不平衡看 macro-F1
metrics.recall_score(y, p, average=None)         # 各类召回
metrics.roc_auc_score(y, proba, multi_class="ovr")
```

## 2. 验证切分

- 普通表格：分层 K 折（分类按标签、回归按目标分箱分层）。
- 时间/业务有先后：按时间切分或滚动验证，不随机打乱。
- 同一实体（用户/车辆）不应跨验证集：用 GroupKFold。

```python
from sklearn.model_selection import KFold, StratifiedKFold, GroupKFold, cross_val_score
cv = StratifiedKFold(5, shuffle=True, random_state=42)
```

## 3. Baseline → 主力（先简单后复杂）

```python
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
# 必做 baseline：均值/线性 + 随机森林
```

优秀论文中表格主力为 **RandomForest / XGBoost / LightGBM / CatBoost**（40 篇中 RF 535、XGB 426、LGBM 271 次出现）。

```python
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
models = {
  "ridge": Ridge(),
  "rf": RandomForestRegressor(n_estimators=500, n_jobs=-1, random_state=42),
  "xgb": XGBRegressor(n_estimators=800, learning_rate=.05, max_depth=6,
                      subsample=.8, colsample_bytree=.8, n_jobs=-1),
  "lgbm": LGBMRegressor(n_estimators=1000, learning_rate=.03, num_leaves=31,
                        subsample=.8, colsample_bytree=.8, verbose=-1),
  "cat": CatBoostRegressor(iterations=1500, learning_rate=.03, depth=6, verbose=0),
}
```
CatBoost 对高基数类别特征友好（可传 `cat_features`）。

## 4. 统一对比（含预处理 Pipeline）

```python
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
res = {}
for name, m in models.items():
    pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), m)
    res[name] = cross_val_score(pipe, X, y, cv=cv, scoring="neg_mean_absolute_error")
    print(name, -res[name].mean(), res[name].std())
```
树模型通常不需标准化；线性/ SVM / KNN / 神经网络需要。

## 5. Optuna 调参（在训练集 + CV 内）

```python
import optuna
from sklearn.model_selection import cross_val_score
def objective(trial):
    params = dict(
        n_estimators=trial.suggest_int("n_estimators", 300, 1500),
        max_depth=trial.suggest_int("max_depth", 3, 9),
        learning_rate=trial.suggest_float("learning_rate", 1e-2, .2, log=True),
        subsample=trial.suggest_float("subsample", .6, 1.0),
        colsample_bytree=trial.suggest_float("colsample_bytree", .6, 1.0),
        reg_lambda=trial.suggest_float("reg_lambda", 1e-3, 10, log=True),
    )
    m = XGBRegressor(**params, n_jobs=-1, random_state=42)
    s = cross_val_score(m, X_train, y_train, cv=cv, scoring="neg_mean_absolute_error")
    return s.mean()
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
print(study.best_params)
```
调参只在训练/验证折进行，**测试集不参与**。

## 6. 诊断（论文加分项）

```python
# 特征重要性
pd.Series(best.feature_importances_, index=X.columns).sort_values()[-20:].plot.barh()
# 学习曲线：判断过/欠拟合与数据是否充足
from sklearn.model_selection import learning_curve
# 残差分析：预测-实际散点、残差直方图、Q-Q 图
```
回归报告：预测 vs 实际一致性图、残差图、Q-Q 图；分类报告：混淆矩阵、ROC/PR 曲线、校准曲线。

## 7. 验证要点

- 至少保留 baseline、候选、最终模型的可比较记录（见 `experiment-provenance.md`）。
- 关键结论用多指标 + 多种子，不引用单次偶然结果。
- 复杂模型必须显著优于简单 baseline 才有充分理由。
