# 04 不平衡数据

> 适用：少数类识别（风险/欺诈/严重超额/缺陷检测）。**不要用准确率衡量**，多数类占优时全预测多数类也能高准确。

## 1. 先看清不平衡与正确指标

```python
y.value_counts(normalize=True)                    # 类别占比
from sklearn.metrics import (confusion_matrix, classification_report,
                             f1_score, precision_recall_curve, average_precision_score)
print(classification_report(y, pred))             # 逐类 precision/recall/f1
f1_score(y, pred, average="macro")                # 宏平均 F1（多类主指标）
average_precision_score(y, proba[:,1])            # PR-AUC（比 ROC 更能反映不平衡）
```
关键看**少数类召回**（别漏掉风险样本）与 precision（误报代价）的平衡，及混淆矩阵。

## 2. 三条处理路线（可叠加，按代价选择）

### A. 算法层（优先尝试，不改变数据）

```python
# 通用 class_weight
LogisticRegression(class_weight="balanced")
from sklearn.utils.class_weight import compute_sample_weight
w = compute_sample_weight("balanced", y_train); model.fit(X, y, sample_weight=w)
# XGB / LGBM
XGBClassifier(scale_pos_weight=neg/pos)           # 二值：负/正样本比
LGBMClassifier(class_weight="balanced")
```

### B. 数据重采样

```python
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
# 过采样少数类 / 欠采样多数类；SMOTE 造合成样本
ros = RandomOverSampler(random_state=42)
smote = SMOTE(k_neighbors=5, random_state=42)
Xr, yr = smote.fit_resample(X_train, y_train)
```
注意：**SMOTE 只能在训练折内、在切分之后做**，否则信息泄漏；类别极稀疏或特征为混合类型时，SMOTE 可能生成不合理样本，改用随机过采样或 SMOTENC/SMOTEN。

### C. 阈值调整（代价敏感决策）

```python
# 默认 0.5 阈值往往漏少数类；按 PR 曲线选阈值满足目标召回
prec, rec, thr = precision_recall_curve(y_test, proba[:,1])
# 选召回率达到目标(如 .9)对应的阈值
idx = np.argmax(rec >= .9)
threshold = thr[idx]
pred = (proba[:,1] >= threshold).astype(int)
```

## 3. 进阶：集成 + 重采样

```python
# SMOTEBAG：每个自助折内对少数类过采样（2022 B 获奖有用）
from imblearn.ensemble import BalancedBaggingClassifier, BalancedRandomForestClassifier
BalancedBaggingClassifier(base_estimator=tree, n_estimators=50, random_state=42)
# 也可对 XGB/LGBM 做 Bagging，每折独立过采样 + 投票
```

## 4. 多类不平衡（如三类风险，严重超额 <3%）

- 主指标用 **macro-F1**，同时报告少数类召回与混淆矩阵；
- 用 `class_weight="balanced"` 或按频率倒数自定义各类权重；
- 可结合分阶段：先过采样/代价敏感训练，再用 Stacking（见 `03-model-fusion-stacking.md`）。

## 5. 验证要点

- 在原始（未重采样）验证/测试分布上评估，不在重采样数据上报成绩。
- 报告 precision/recall 权衡与阈值依据，不只报一个 F1。
- 处理方式与业务代价匹配（漏检风险高 → 重召回；误报贵 → 重 precision）。
- 对比“处理 vs 不处理”，证明对少数类有效。
