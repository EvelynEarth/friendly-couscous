# 2025 MathorCup 数学应用挑战赛 · 大数据竞赛 · 赛道 B

## 物流理赔风险识别及服务升级问题

本目录为赛道 B 初赛完整作品，包含三个问题的建模代码、结果文件、论文与图表。

### 目录结构

```
projects/mathorcup-2025-trackB/
├── README.md                 # 本说明
├── requirements.txt          # Python 依赖
├── 论文.md                   # 完整论文（Markdown）
├── src/
│   ├── pipeline.py           # 问题1规则 + 问题2回归 + 问题3分类 全流程
│   └── make_figures.py       # 论文图表生成 + 分段指标
├── data/
│   ├── Result.xlsx           # 【提交结果】附件2 实际赔付金额 + 风险标注
│   ├── 附件1_风险标注结果_精简.csv
│   ├── 附件2_间接法结果.csv
│   ├── metrics.json          # 全部模型评估指标
│   ├── reg_segment_metrics.csv
│   └── feat_importance_reg.csv
├── figures/                  # 论文配图（5 张）
└── assets_b64/               # 二进制文件的 base64 编码 + 解码脚本
    └── decode.py
```

> 说明：通过 API 推送时二进制文件以 base64 文本存放于 `assets_b64/`。
> 克隆后执行 `python assets_b64/decode.py` 即可还原 `data/Result.xlsx` 与 `figures/*.jpg`。

### 快速开始

```bash
pip install -r requirements.txt
python assets_b64/decode.py            # 还原二进制产物（可选）
python src/pipeline.py                 # 端到端重跑
python src/make_figures.py
```

### 方法与结果摘要

| 问题 | 方法 | 关键结果 |
| --- | --- | --- |
| 问题1 风险标注 | 分层约束式一维聚类（12 个赔付分位层 + 分位分界 + PAVA 保序校准） | 合理诉求 85.94%、诉求偏高 11.17%、严重超额 2.89% |
| 问题2 赔付金额预测 | LightGBM 回归（log1p 目标、5 折分层交叉验证） | RMSE 149.71、MAE 98.35、R² 0.718 |
| 问题3 风险三分类 | 反比类别加权 LightGBM；SMOTE 对照；回归+规则间接法对比 | 准确率 90.60%、Macro-F1 0.602；间接法准确率 91.59% |

核心结论：直接分类对高风险“严重超额”的召回更高（26.3% 对间接法 17.0%），适合作为主模型；间接法可解释、阈值可调，适合作为并行校验与人工复核依据。
