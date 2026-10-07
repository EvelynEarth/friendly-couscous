# 03 模型融合 Stacking

> 适用：多个单模型已调优、希望进一步提升精度与稳健性；也是优秀论文高频“创新点”。
> 前提：基模型原理有差异（线性/核/树/提升），且都已显著优于随机水平。
> 覆盖口径（脚本现算，40 篇）：18 篇显式使用 Stacking/Voting/Blending（45%）；若计入一般集成学习则为 33 篇（82.5%）。

## 1. 三种融合层次

- **加权平均（回归）/软投票（分类）**：最简单，先试。
- **Blending**：用一个 holdout 集训练元模型，简单但耗数据。
- **Stacking**：用 OOF（折外）预测训练元学习器，信息利用更充分，最常用。

```python
# 加权/投票（快）
from sklearn.ensemble import VotingRegressor, VotingClassifier
ens = VotingRegressor([("xgb", xgb), ("lgbm", lgbm), ("rf", rf)])  # 可加 weights=
```

## 2. sklearn Stacking

```python
from sklearn.ensemble import StackingRegressor, StackingClassifier
from sklearn.linear_model import Ridge, LogisticRegression
estimators = [("xgb", xgb), ("lgbm", lgbm), ("cat", cat), ("svr", svr)]
stack = StackingRegressor(estimators=estimators,
                          final_estimator=Ridge(),
                          cv=5, n_jobs=-1, passthrough=False)
stack.fit(X_train, y_train)
```
分类用 `StackingClassifier` + `LogisticRegression` 元学习器；输出概率时基模型需 `predict_proba`。

## 3. 自定义 OOF Stacking（可控、可加元特征）

```python
import numpy as np
from sklearn.model_selection import KFold
from sklearn.base import clone

def oof_predict(model, X, y, X_test, cv):
    oof = np.zeros(len(X)); test = np.zeros(len(X_test))
    for tri, vai in cv.split(X):
        m = clone(model)
        m.fit(X.iloc[tri], y.iloc[tri])
        oof[vai] = m.predict(X.iloc[vai])
        test += m.predict(X_test) / cv.n_splits
    return oof, test

# 1) 各基模型生成 OOF 与 test 预测，拼成元特征
S_train = np.column_stack([oof_predict(clone(m), X, y, X_test, cv)[0] for m in base])
S_test  = np.column_stack([oof_predict(clone(m), X, y, X_test, cv)[1] for m in base])
# 2) 元学习器在 OOF 上训练
meta = Ridge().fit(S_train, y)
final = meta.predict(S_test)
```

## 4. 进阶：深度元特征（论文创新写法）

除基模型预测外，可拼接：

- 各模型的**预测置信度/概率**（分类）或预测方差（回归）；
- 少量关键原始特征（如赔付金额、索赔差额、高风险 ID 聚合），让元学习器有“上下文”；
- 模型分歧度（各基模型预测的标准差），用于识别难样本。

```python
S_train = np.column_stack([pred_oof, proba_oof, X[["amount","diff"]].values,
                           pred_oof.std(axis=1, keepdims=True)])
```
2025 B 获奖论文即采用“基模型输出 + 置信度 + 关键原始特征”的 Stacking，macro-F1 提升到 0.9664（该论文报告值）。

## 5. 验证要点

- 融合必须在同样 CV/指标下与**最佳单模型**对比，证明有增益；无增益则回退简单模型。
- OOF 构造过程不引入未来信息；元学习器不过拟合（看元层 CV）。
- 记录基模型版本、权重/元学习器参数与最终指标（见 `experiment-provenance.md`）。
- 不为“看起来高级”而堆叠过多模型；基模型相关性过高时融合收益有限。
