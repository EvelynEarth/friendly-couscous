# 已执行实验与论文数字证据记录模板

> 复制为实际 JSON 文件。**默认标为 planned，不能用作正式论文数值证据**。只有你或受权环境真正运行模型、复核训练/验证边界并保存产物后，才能将状态改为 accepted。

JSON 字段示例（不是成绩，不可直接执行验收）：

```json
{
  "experiment_id": "EXP-real-run-id",
  "run_status": "planned",
  "data_version": "",
  "code_revision": "",
  "validation_scheme": "",
  "split_protocol": "",
  "random_seed": null,
  "split_manifest": "",
  "metrics": {},
  "artifacts": [],
  "claims": []
}
```

完成真实实验后：

1. 保存真正执行时的**数据/代码版本、切分说明、实际随机种子**，以及分组/时间隔离的证明材料。
2. 将真实验证指标写入 `metrics`，而不是根据论文表述反向填写。全部指标必须有限数值（不是 NaN/Inf）。
3. 将用于实验的 `split_manifest`、结果表、指标 JSON、论文图表源数据都放入 `artifacts`；每项记录相对于 `--artifact-root` 的路径与**文件实际 SHA-256**（64 位小写十六进制）。
4. 对每项论文数字添加 `claim_id`、`metric`、`value`、`artifact`（能定位正式结果的产物路径）、`paper_location`。
5. 复审确认是实际运行而不是纯方案后，才把 `run_status` 改成 `accepted`，运行 `paper_evidence_gate.py`。若字段缺失、指标不一致、实验文件被改动或存在逃逸路径，必须拒绝。
6. 文件哈希只能证明同一份文件未变，不能证明指标计算正确；需要额外进行算法/验证/统计复核。

哈希可用标准库计算：

```python
from hashlib import sha256
from pathlib import Path
print(sha256(Path("path/to/artifact").read_bytes()).hexdigest())
```

对超大数据文件应改用分块 SHA-256，避免将整个文件读入内存。
