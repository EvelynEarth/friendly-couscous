# -*- coding: utf-8 -*-
"""
2025 MathorCup 大数据竞赛 赛道B
物流理赔风险识别及服务升级问题
问题2：实际赔付金额回归预测
问题3：风险标注三分类预测（直接分类 vs 回归+规则间接法）
"""
import os, json, warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             f1_score, classification_report, confusion_matrix,
                             accuracy_score)
from sklearn.preprocessing import LabelEncoder
import lightgbm as lgb
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore")
ATT = "/home/user/.doubao/agent_mode/workspace/.sessions/38445791300602626/attachments"
OUT = "/home/user/.doubao/agent_mode/workspace/mathorcup_work"
SEED = 42
N_SPLITS = 5

CAT_COLS = ["线路类型", "异常原因", "进线渠道", "商品类型", "新旧程度",
            "寄件B/C", "进线人身份", "寄件是否内部", "是否c2c",
            "是否生鲜妥投及时", "始发城市", "目的城市"]
NUM_COLS = ["保价金额", "配送超时时长", "妥投到进线时长", "索赔金额",
            "始发网点发单量", "始发网点万单理赔率", "始发网点赔付比例",
            "目的网点发单量", "目的网点万单理赔率", "目的网点赔付比例"]
DROP_COLS = ["寄件人id", "收件人id"]


def load_data():
    train = pd.read_excel(f"{ATT}/附件1.xlsx", skiprows=[1])
    test = pd.read_excel(f"{ATT}/附件2.xlsx", skiprows=[1])
    return train.reset_index(drop=True), test.reset_index(drop=True)


def feature_engineering(df):
    df = df.copy()
    df["异常原因"] = df["异常原因"].fillna("NoException")
    df["进线渠道"] = df["进线渠道"].fillna("Unknown")
    df["保价金额"] = df["保价金额"].clip(lower=0)
    df["索赔_保价比"] = df["索赔金额"] / (df["保价金额"] + 1)
    df["索赔_log"] = np.log1p(df["索赔金额"])
    df["保价_log"] = np.log1p(df["保价金额"])
    df["超时_log"] = np.log1p(df["配送超时时长"].clip(lower=0))
    df["进线时长_log"] = np.log1p(df["妥投到进线时长"].clip(lower=0))
    df["超时为负"] = (df["配送超时时长"] < 0).astype(int)
    df["始发网点理赔压力"] = df["始发网点万单理赔率"] * df["始发网点赔付比例"]
    df["目的网点理赔压力"] = df["目的网点万单理赔率"] * df["目的网点赔付比例"]
    df["网点发单量_log_始"] = np.log1p(df["始发网点发单量"].clip(lower=0))
    df["网点发单量_log_目"] = np.log1p(df["目的网点发单量"].clip(lower=0))
    df["索赔_超时比"] = df["索赔金额"] / (df["配送超时时长"].clip(lower=0) + 1)
    return df


def get_matrices(train, test):
    feat_num = NUM_COLS + ["索赔_保价比", "索赔_log", "保价_log", "超时_log",
                           "进线时长_log", "超时为负", "始发网点理赔压力",
                           "目的网点理赔压力", "网点发单量_log_始", "网点发单量_log_目",
                           "索赔_超时比"]
    train = train.drop(columns=DROP_COLS)
    test = test.drop(columns=DROP_COLS)
    for c in CAT_COLS:
        train[c] = train[c].astype(str)
        test[c] = test[c].astype(str)
        le = LabelEncoder().fit(pd.concat([train[c], test[c]]))
        train[c] = le.transform(train[c])
        test[c] = le.transform(test[c])
    feats = feat_num + CAT_COLS
    return train, test, feats


def mape(y_true, y_pred):
    y_true = np.asarray(y_true)
    mask = y_true > 1
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def run_regression(train, test, feats):
    print("\n" + "=" * 60 + "\n问题2：实际赔付金额回归（LightGBM, 5折CV）")
    y = train["实际赔付金额"].values
    y_log = np.log1p(y)
    X, X_test = train[feats], test[feats]
    bins = pd.qcut(y, 20, labels=False, duplicates="drop")
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof = np.zeros(len(train)); pred_test = np.zeros(len(test))
    params = dict(objective="regression", metric="rmse",
                  learning_rate=0.03, num_leaves=63, max_depth=-1,
                  min_child_samples=40, subsample=0.8, subsample_freq=1,
                  colsample_bytree=0.8, reg_alpha=0.1, reg_lambda=1.0,
                  verbosity=-1, seed=SEED)
    for tr, va in skf.split(X, bins):
        dtr = lgb.Dataset(X.iloc[tr], y_log[tr], categorical_feature=CAT_COLS)
        dva = lgb.Dataset(X.iloc[va], y_log[va], categorical_feature=CAT_COLS)
        m = lgb.train(params, dtr, num_boost_round=5000, valid_sets=[dva],
                      callbacks=[lgb.early_stopping(200), lgb.log_evaluation(0)])
        oof[va] = np.expm1(m.predict(X.iloc[va], num_iteration=m.best_iteration))
        pred_test += np.expm1(m.predict(X_test, num_iteration=m.best_iteration)) / N_SPLITS
    oof = np.clip(oof, 0, None); pred_test = np.clip(pred_test, 0, None)
    metrics = {"RMSE": float(np.sqrt(mean_squared_error(y, oof))),
               "MAE": float(mean_absolute_error(y, oof)),
               "MAPE(%)": float(mape(y, oof)),
               "R2": float(r2_score(y, oof))}
    print("CV指标:", json.dumps(metrics, ensure_ascii=False, indent=2))
    fi = pd.Series(m.feature_importance(importance_type="gain"), index=feats)
    fi.sort_values(ascending=False).to_csv(f"{OUT}/feat_importance_reg.csv",
                                           header=["gain"], encoding="utf-8-sig")
    return oof, pred_test, metrics


LABELS = ["合理诉求", "诉求偏高", "严重超额"]


def make_rule_labels(train):
    df = train.copy()
    df["超额"] = df["索赔金额"] - df["实际赔付金额"]
    NB = 12
    df["箱"] = pd.qcut(df["实际赔付金额"], NB, labels=False, duplicates="drop")

    def pava(v):
        v = v.tolist(); w = [1] * len(v); i = 0
        while i < len(v) - 1:
            if v[i] <= v[i + 1] + 1e-9:
                i += 1
            else:
                mm = (v[i] * w[i] + v[i + 1] * w[i + 1]) / (w[i] + w[i + 1])
                v[i] = v[i + 1] = mm; w[i] = w[i + 1] = w[i] + w[i + 1]
                if i > 0: i -= 1
        return np.array(v)

    t1 = pava(np.array([df.loc[df["箱"] == b, "超额"].quantile(0.86)
                        for b in range(NB)]))
    t2 = pava(np.array([df.loc[df["箱"] == b, "超额"].quantile(0.972)
                        for b in range(NB)]))
    edges = df.groupby("箱")["实际赔付金额"].agg(["min", "max"]).values

    def classify(pay, claim):
        over = claim - pay
        b = np.clip(np.searchsorted(edges[:, 1], pay, side="left"), 0, NB - 1)
        if over > t2[b]: return 2
        if over > t1[b]: return 1
        return 0

    y = np.array([classify(p, c) for p, c in
                  zip(df["实际赔付金额"], df["索赔金额"])])
    return y, (edges, t1, t2), classify


def run_classifier(train, test, feats, y_cls):
    print("\n" + "=" * 60 + "\n问题3：风险标注直接分类（LightGBM加权, 5折CV）")
    X, X_test = train[feats], test[feats]
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof = np.zeros(len(train), dtype=int); pred = np.zeros((len(test), 3))
    counts = np.bincount(y_cls)
    w = len(y_cls) / (3 * counts); w[2] *= 1.3
    sw = np.array([w[v] for v in y_cls])
    params = dict(objective="multiclass", num_class=3, metric="multi_logloss",
                  learning_rate=0.03, num_leaves=63, min_child_samples=30,
                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                  reg_alpha=0.1, reg_lambda=1.0, verbosity=-1, seed=SEED)
    for tr, va in skf.split(X, y_cls):
        dtr = lgb.Dataset(X.iloc[tr], y_cls[tr], weight=sw[tr],
                          categorical_feature=CAT_COLS)
        dva = lgb.Dataset(X.iloc[va], y_cls[va], categorical_feature=CAT_COLS)
        m = lgb.train(params, dtr, num_boost_round=4000, valid_sets=[dva],
                      callbacks=[lgb.early_stopping(200), lgb.log_evaluation(0)])
        oof[va] = m.predict(X.iloc[va], num_iteration=m.best_iteration).argmax(1)
        pred += m.predict(X_test, num_iteration=m.best_iteration) / N_SPLITS
    pred_label = pred.argmax(1)
    print(classification_report(y_cls, oof, target_names=LABELS, digits=4))
    cm = confusion_matrix(y_cls, oof)
    print("混淆矩阵(行=真实,列=预测):\n", cm)
    metrics = {"accuracy": float(accuracy_score(y_cls, oof)),
               "macro_f1": float(f1_score(y_cls, oof, average="macro")),
               "weighted_f1": float(f1_score(y_cls, oof, average="weighted")),
               "per_class_f1": {LABELS[i]: float(v) for i, v in
                                enumerate(f1_score(y_cls, oof, average=None))},
               "confusion_matrix": cm.tolist(),
               "train_class_dist": {LABELS[i]: float(counts[i] / len(y_cls))
                                    for i in range(3)}}
    return oof, pred_label, metrics, m


def run_smote_baseline(train, feats, y_cls):
    X = train[feats]
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=SEED)
    oof = np.zeros(len(train), dtype=int)
    for tr, va in skf.split(X, y_cls):
        Xr, yr = SMOTE(random_state=SEED, k_neighbors=5).fit_resample(X.iloc[tr], y_cls[tr])
        dtr = lgb.Dataset(Xr, yr, categorical_feature=CAT_COLS)
        m = lgb.train(dict(objective="multiclass", num_class=3,
                           metric="multi_logloss", learning_rate=0.05,
                           num_leaves=63, verbosity=-1, seed=SEED),
                      dtr, num_boost_round=1500)
        oof[va] = m.predict(X.iloc[va]).argmax(1)
    return {"macro_f1": float(f1_score(y_cls, oof, average="macro")),
            "per_class_f1": {LABELS[i]: float(v) for i, v in
                             enumerate(f1_score(y_cls, oof, average=None))}}


def indirect_method(oof_reg, pred_reg, train, test):
    _, rule_pack, classify = make_rule_labels(train)
    oof_lab = np.array([classify(p, c) for p, c in zip(oof_reg, train["索赔金额"])])
    pred_lab = np.array([classify(p, c) for p, c in zip(pred_reg, test["索赔金额"])])
    return oof_lab, pred_lab


def main():
    train_raw, test_raw = load_data()
    train = feature_engineering(train_raw)
    test = feature_engineering(test_raw)
    train, test, feats = get_matrices(train, test)
    y_cls, rule_pack, _ = make_rule_labels(train_raw)
    print("问题1标签分布:", np.bincount(y_cls) / len(y_cls))
    oof_reg, pred_reg, reg_metrics = run_regression(train, test, feats)
    oof_cls, pred_cls, cls_metrics, last_model = run_classifier(train, test, feats, y_cls)
    oof_ind, pred_ind = indirect_method(oof_reg, pred_reg, train_raw, test_raw)
    ind_metrics = {
        "accuracy": float(accuracy_score(y_cls, oof_ind)),
        "macro_f1": float(f1_score(y_cls, oof_ind, average="macro")),
        "weighted_f1": float(f1_score(y_cls, oof_ind, average="weighted")),
        "per_class_f1": {LABELS[i]: float(v) for i, v in
                         enumerate(f1_score(y_cls, oof_ind, average=None))},
        "confusion_matrix": confusion_matrix(y_cls, oof_ind).tolist()}
    print("\n间接法(回归+规则) CV:\n",
          classification_report(y_cls, oof_ind, target_names=LABELS, digits=4))
    smote_metrics = run_smote_baseline(train, feats, y_cls)
    print("SMOTE对照:", smote_metrics)
    all_metrics = {"问题2_回归": reg_metrics,
                   "问题3_直接分类": cls_metrics,
                   "问题3_间接法_回归加规则": ind_metrics,
                   "问题3_SMOTE对照": smote_metrics}
    with open(f"{OUT}/metrics.json", "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, ensure_ascii=False, indent=2)
    result = pd.read_excel(f"{ATT}/Result.xlsx")
    ids = test_raw["运单号"].values
    assert list(result["运单号"]) == list(ids), "运单号不一致!"
    result["实际赔付金额"] = np.round(pred_reg, 2)
    result["风险标注"] = [LABELS[i] for i in pred_cls]
    result.to_excel(f"{OUT}/Result.xlsx", index=False)
    out1 = train_raw.copy()
    out1["索赔差额"] = out1["实际赔付金额"] - out1["索赔金额"]
    out1["风险标注"] = [LABELS[i] for i in y_cls]
    out1.to_excel(f"{OUT}/附件1_风险标注结果.xlsx", index=False)
    pd.DataFrame({"运单号": ids,
                  "风险标注_间接法": [LABELS[i] for i in pred_ind]
                  }).to_csv(f"{OUT}/附件2_间接法结果.csv", index=False,
                           encoding="utf-8-sig")
    print("\n全部完成，产物已保存。")


if __name__ == "__main__":
    main()
