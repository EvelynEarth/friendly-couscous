# -*- coding: utf-8 -*-
"""生成论文用图表，并补算分段MAPE、保存回归OOF"""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import lightgbm as lgb
import pipeline as P

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
plt.rcParams["font.family"] = "Noto Sans CJK SC"
plt.rcParams["axes.unicode_minus"] = False

OUT = P.OUT
train_raw, test_raw = P.load_data()
train = P.feature_engineering(train_raw)
test = P.feature_engineering(test_raw)
train, test, feats = P.get_matrices(train, test)
y_cls, rule_pack, classify = P.make_rule_labels(train_raw)
edges, t1, t2 = rule_pack

pay = np.linspace(1, train_raw["实际赔付金额"].max(), 300)
def th(payv, tv):
    b = np.clip(np.searchsorted(edges[:, 1], payv, side="left"), 0, 11)
    return tv[b]
fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
colors = {0: "#4C9BE8", 1: "#F5A623", 2: "#E5484D"}
names = {0: "合理诉求", 1: "诉求偏高", 2: "严重超额"}
over_all = (train_raw["索赔金额"] - train_raw["实际赔付金额"]).values
samp = np.random.RandomState(0).choice(len(train), 6000, replace=False)
for c in [0, 1, 2]:
    m = (y_cls == c)
    m2 = m & np.isin(np.arange(len(m)), samp)
    ax.scatter(train_raw["实际赔付金额"][m2], over_all[m2], s=6,
               c=colors[c], label=f"{names[c]} ({m.mean()*100:.1f}%)", alpha=0.55)
ax.plot(pay, th(pay, t1), c="black", lw=1.8, label="标注阈值")
ax.plot(pay, th(pay, t2), c="black", lw=1.8)
ax.set_xlabel("实际赔付金额（元）"); ax.set_ylabel("索赔超额 = 索赔金额 − 实际赔付金额（元）")
ax.set_title("问题1  风险标注结果与分层阈值")
ax.legend(); ax.set_ylim(0, 4600)
plt.tight_layout(); plt.savefig(f"{OUT}/fig1_risk_labels.png"); plt.close()

y = train["实际赔付金额"].values
y_log = np.log1p(y)
X, X_test = train[feats], test[feats]
bins = pd.qcut(y, 20, labels=False, duplicates="drop")
skf = StratifiedKFold(5, shuffle=True, random_state=42)
oof = np.zeros(len(train)); pred_test = np.zeros(len(test))
params = dict(objective="regression", metric="rmse", learning_rate=0.03,
              num_leaves=63, min_child_samples=40, subsample=0.8,
              subsample_freq=1, colsample_bytree=0.8, reg_alpha=0.1,
              reg_lambda=1.0, verbosity=-1, seed=42)
for tr, va in skf.split(X, bins):
    dtr = lgb.Dataset(X.iloc[tr], y_log[tr], categorical_feature=P.CAT_COLS)
    dva = lgb.Dataset(X.iloc[va], y_log[va], categorical_feature=P.CAT_COLS)
    m = lgb.train(params, dtr, 5000, valid_sets=[dva],
                  callbacks=[lgb.early_stopping(200), lgb.log_evaluation(0)])
    oof[va] = np.expm1(m.predict(X.iloc[va], num_iteration=m.best_iteration))
    pred_test += np.expm1(m.predict(X_test, num_iteration=m.best_iteration)) / 5
oof = np.clip(oof, 0, None)

seg = []
for lo, hi, nm in [(0, 50, "0–50"), (50, 200, "50–200"), (200, 500, "200–500"),
                   (500, 1e9, "≥500")]:
    msk = (y >= lo) & (y < hi)
    ape = np.abs((y[msk] - oof[msk]) / np.maximum(y[msk], 1e-6)) * 100
    seg.append([nm, int(msk.sum()),
                round(np.sqrt(mean_squared_error(y[msk], oof[msk])), 2),
                round(mean_absolute_error(y[msk], oof[msk]), 2),
                round(ape.mean(), 1), round(r2_score(y[msk], oof[msk]), 3)])
segdf = pd.DataFrame(seg, columns=["实际赔付区间(元)", "样本数", "RMSE", "MAE",
                                   "MAPE(%)", "R2"])
print(segdf.to_string(index=False))
segdf.to_csv(f"{OUT}/reg_segment_metrics.csv", index=False, encoding="utf-8-sig")

fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=150)
ax = axes[0]
ax.scatter(y, oof, s=5, alpha=0.35, c="#4C9BE8")
lim = [0, max(y.max(), oof.max())]
ax.plot(lim, lim, "r--", lw=1.5)
ax.set_xlabel("真实实际赔付金额"); ax.set_ylabel("OOF预测值")
ax.set_title("问题2  预测值 vs 真实值（5折OOF）")
ax = axes[1]
ax.hist(y, bins=60, alpha=0.6, label="真实", color="#4C9BE8")
ax.hist(oof, bins=60, alpha=0.5, label="预测", color="#F5A623")
ax.set_xlabel("实际赔付金额"); ax.set_ylabel("频数"); ax.legend()
ax.set_title("真实与预测赔付金额分布对比")
plt.tight_layout(); plt.savefig(f"{OUT}/fig2_regression.png"); plt.close()

fi = pd.read_csv(f"{OUT}/feat_importance_reg.csv", index_col=0)["gain"]
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
top = fi.sort_values().tail(15)
ax.barh(top.index, top.values, color="#4C9BE8")
ax.set_xlabel("LightGBM 增益重要性（gain）")
ax.set_title("问题2  Top15 特征重要性")
plt.tight_layout(); plt.savefig(f"{OUT}/fig3_feature_importance.png"); plt.close()

met = json.load(open(f"{OUT}/metrics.json", encoding="utf-8"))
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), dpi=150)
for ax, key, title in [(axes[0], "问题3_直接分类", "直接分类法（加权LightGBM）"),
                       (axes[1], "问题3_间接法_回归加规则", "间接法（回归预测+问题1规则）")]:
    cm = np.array(met[key]["confusion_matrix"], dtype=float)
    cmn = cm / cm.sum(1, keepdims=True)
    im = ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{cm[i,j]:.0f}\n({cmn[i,j]*100:.0f}%)",
                    ha="center", va="center", fontsize=10,
                    color="white" if cmn[i, j] > 0.5 else "black")
    ax.set_xticks(range(3), P.LABELS); ax.set_yticks(range(3), P.LABELS)
    ax.set_xlabel("预测类别"); ax.set_ylabel("真实类别"); ax.set_title(title)
fig.colorbar(im, ax=axes, fraction=0.025)
plt.savefig(f"{OUT}/fig4_confusion.png", bbox_inches="tight"); plt.close()

fig, ax = plt.subplots(figsize=(8, 4.8), dpi=150)
methods = ["类别加权(本文)", "SMOTE过采样", "间接法(回归+规则)"]
macro = [met["问题3_直接分类"]["macro_f1"], met["问题3_SMOTE对照"]["macro_f1"],
         met["问题3_间接法_回归加规则"]["macro_f1"]]
sevf1 = [met["问题3_直接分类"]["per_class_f1"]["严重超额"],
         met["问题3_SMOTE对照"]["per_class_f1"]["严重超额"],
         met["问题3_间接法_回归加规则"]["per_class_f1"]["严重超额"]]
x = np.arange(len(methods)); w = 0.35
ax.bar(x - w/2, macro, w, label="Macro-F1", color="#4C9BE8")
ax.bar(x + w/2, sevf1, w, label="严重超额 F1", color="#E5484D")
ax.set_xticks(x, methods); ax.set_ylim(0, 0.8); ax.set_ylabel("F1 分数")
ax.set_title("问题3  类别不平衡处理方法对比"); ax.legend()
plt.tight_layout(); plt.savefig(f"{OUT}/fig5_imbalance.png"); plt.close()
print("图表生成完成")
