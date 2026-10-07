# 01 数据清洗与特征工程

> 适用：一切表格任务的起点。原则：**先审计、后处理；保留原始数据；处理可复现、在训练折内完成。**

## 1. 加载（按当届格式）

```python
import pandas as pd
# 制表符分隔、无表头（如 2021 二手车）
df = pd.read_csv("附件1.txt", sep="\t", header=None)
# Excel 多 sheet（如 2022 满意度）
df = pd.read_excel("附件1.xlsx", sheet_name=0)
```

先读“字段说明/数据描述”，核对列含义、单位、主键、时间列，再动手。

## 2. 审计清单

```python
df.shape; df.dtypes; df.head()
df.isna().mean().sort_values(ascending=False)   # 缺失率
df.nunique()                                     # 基数/常量列
df.duplicated().sum()                            # 重复
df.describe(include="all").T                      # 分布/异常
```

记录：缺失、重复、常量列、高基数 ID、异常值、时间覆盖、跨表键。

## 3. 缺失处理（按机制，不统一填 0）

- 缺失率过高（如 >70%）且无业务价值：删列并记录。
- 类别型：众数/单独 “Unknown” 类别。
- 数值型：中位数（鲁棒）；信息丰富时 KNN/迭代插补（**必须在训练折内 fit**）。

```python
from sklearn.impute import SimpleImputer, KNNImputer
cat_cols.fillna(cat_cols.mode().iloc[0], inplace=True)
num_imp = SimpleImputer(strategy="median")   # 放进 Pipeline，避免泄漏
```

## 4. 异常值：不默认删除

先判断是“数据错误”还是“真实但稀有”（如严重超额、大额理赔本身是目标信号）。

```python
# 仅对明确错误做处理；需要保留分布时用 Winsorize 截尾
q1, q3 = s.quantile(.25), s.quantile(.75)
hi = q3 + 3*(q3-q1)          # 3 倍 IQR，避免误删
s.clip(upper=hi, inplace=True)
```
记录“问题 → 影响 → 处理 → 验证”。

## 5. 编码

```python
# 低基数类别：One-Hot
df = pd.get_dummies(df, columns=low_card_cols, drop_first=True)
# 有序/二值：映射或 Label
# 高基数 ID（用户/网点/商品/城市）：不要 One-Hot
```
高基数 ID 处理（三选一，按效果）：

```python
# a) 计数/频率编码
freq = df[col].value_counts(normalize=True)
df[col+"_freq"] = df[col].map(freq)
# b) 类别编码（树模型可直接用）
df[col] = df[col].astype("category").cat.codes
# c) 目标编码（严格 K 折、在训练集内，防泄漏）
from sklearn.model_selection import KFold
# 对 train 做 OOF 目标编码，test 用全 train 均值映射
```

## 6. 特征工程（结合业务）

- 时间列：年/月/日/星期/是否周末/时间差（如 上牌年限 = 交易年-上牌年）。
- 价格/金额：右偏分布做 `log1p`；比率/差值特征（如 索赔差额 = 实际赔付 - 索赔金额）。
- 连续变量分箱、历史聚合（某用户/网点的次数、均值、高风险占比）。
- 匿名特征：先看分布与相关性，再决定保留/变换，不臆测含义。

```python
import numpy as np
df["price_log"] = np.log1p(df["price"])
df["car_age"] = df["tradeTime"].dt.year - df["licenseDate"].dt.year
```

## 7. 防泄漏：放进折内 Pipeline

标准化、插补、编码、特征选择都在训练折 fit，再 transform 验证/测试折；时间数据按时间切分。

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
pipe = Pipeline([("imp", SimpleImputer(strategy="median")),
                 ("sc", StandardScaler()),
                 ("model", model)])
```

## 8. 验证要点

- 原始数据只读不改；所有处理可由脚本重跑。
- 处理前后样本量、主键唯一性、目标分布可对照。
- 每个处理决定有记录，能回答“为什么这样做”。
