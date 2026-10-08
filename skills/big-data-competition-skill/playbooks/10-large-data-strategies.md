# 10 大规模数据工程与算力预算

适用：附件数据体积大、CSV/Parquet 多文件、宽表高基数 ID、内存受限、重复实验计算时间紧。并非只因比赛名为“大数据”就强制使用 Spark。

## 任务识别与决策

先测压缩前文件总量、列数、主键基数、join 膨胀风险、空值率、峰值内存预算、CPU/GPU 和剩余时间。

| 数据状态 | 建议工具 | 不用的情况 |
|---|---|---|
| 单机可内存处理 | pandas + Parquet/Arrow | 不需要引入分布式复杂度 |
| 内存偏紧/查询聚合重 | Polars lazy / DuckDB | 先做类型与执行计划审计 |
| 超出单机内存或分区自然 | Dask/分块/分区 Parquet | 无法承受调度与 shuffle 成本时退回流式 |
| 大量图片/视频 | manifest + batch loader + cache policy | 禁止一次性全部解码进 RAM |

## 最小流式资产统计（标准库，可直接运行）

```python
from collections import Counter
from pathlib import Path
import csv

def stream_profile(path: str, encoding: str = "utf-8-sig"):
    counts, missing, seen = Counter(), Counter(), 0
    with Path(path).open("r", newline="", encoding=encoding) as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            seen += 1
            for key, value in row.items():
                counts[key] += 1
                if value is None or not str(value).strip():
                    missing[key] += 1
    return {"rows": seen, "missing": dict(missing), "observations": dict(counts)}
```

这里统计的是非空缺失概况；不暗示已建立合理的训练集。文本编码须根据原附件核验。

## 不能忽略的审计

- ID 的前导零与长整数：避免强制转浮点；日期/时区与货币单位使用显式类型。
- join 前检查唯一性与 join 后样本数；滚动/累计统计按预测时点构造，避免泄漏。
- 抽样用于 EDA 或开发调试时必须记录抽样方法和覆盖范围；最终结论以真实全量/正式评估为准。
- 固定随机种子、库版本与数据 hash；记录单次耗时、内存峰值及硬件环境。
- 在比赛时限内优先完成 Baseline + 可信验证，再评估更重的模型。

升级路径：`01-data-cleaning-feature-engineering.md` → 本篇 → 按任务进入 `02/05/06/08`。参考外部工具路由见 `../references/external-skill-routing.md`。
