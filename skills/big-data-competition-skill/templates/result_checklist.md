# Result 结果文件校验清单

> 提交前逐项打勾。result 文件使用官方模板，**不得改文件名、列名、分隔符、编码，不得改变 ID 与样本对应关系、不得增减样本行**。

## 1. 格式与命名

- [ ] 文件名与官方模板完全一致（含大小写、扩展名）。
- [ ] 列名/表头、列顺序与模板一致，未增删列。
- [ ] 分隔符正确（CSV 逗号 / 部分 TXT 为制表符 `\t`）。
- [ ] 编码正确（以模板为准）；中文无乱码。可用以下方式核验：

```python
# 检查编码与分隔符（输入：result 文件路径；输出：编码、首行、列数）
import pandas as pd
raw = open(path, "rb").read(200)
print(raw[:80])                                  # 直看字节，发现乱码/BOM
df = pd.read_csv(path, sep="\t", encoding="utf-8")  # 按模板改 sep/encoding
print(df.shape, df.columns.tolist())
```

- [ ] Excel：sheet 名、单元格格式与模板一致；数值未被存成文本、日期未串行。

## 2. ID 与样本对应

- [ ] 结果行数 = 官方要求的预测样本数（不多不少）。
- [ ] ID/主键与官方预测集**逐一对应、顺序一致、无重复、无遗漏**。

```python
# 输入：官方待预测 ID 列表、result 的 ID 列；输出：缺失/多余/重复/顺序问题
assert set(pred_id) == set(result_id)
assert result_id.is_unique
assert (result_id.reset_index(drop=True) == pred_id.reset_index(drop=True)).all()
```

## 3. 取值合理性

- [ ] 预测值在业务合理范围（非负、不超上限、类别取值在允许集合内）。
- [ ] 无空值/NaN/Inf；数值精度与模板要求一致（如保留小数位）。
- [ ] 分类标签与官方编码一致（如 0/1/2，不写成中文或其他数字）。

```python
assert df[col].notna().all(); np.isfinite(df[num_col]).all()
assert df[cat_col].isin(allowed_labels).all()
```

## 4. 多文件与打包

- [ ] 多个结果文件齐全，各自通过上述检查。
- [ ] 按要求打包为指定 zip（文件名、目录结构符合要求）。

```python
import zipfile
with zipfile.ZipFile("result.zip", "w") as z:
    for f in result_files: z.write(f)            # 输入：结果文件；输出：zip
```

## 5. 最终复核

- [ ] result 中的关键数值与论文正文/摘要一致。
- [ ] 在干净环境重跑生成脚本，能复现同一 result。
- [ ] 截止时间前完成上传，并确认平台显示提交成功。
