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

## v2.5 严格指标文件回读（推荐正式定稿使用）

在实际实验执行后，新建真实 `metrics.json`（直接映射指标名到有限数值，或根键 `"metrics"` 对应指标字典）；按实际 SHA-256 把它放入 `artifacts`，并在接受记录中添加 `"metrics_artifact": "metrics.json"`。每一条数字型 `claims[].artifact` 必须指向这份指标文件。

```bash
python skills/big-data-competition-skill/tools/paper_evidence_gate.py --record results/accepted.json --artifact-root results --require-metric-source
```

这会比较指标文件、审核记录和论文 claim 是否三方一致，并拒绝无关文件冒充数值证据。旧 CLI 不带严格开关依然可运行，以兼容已有项目，但**不能视为强制回读指标已通过**。仍需独立验证指标代码、验证划分、训练记录和模型假设；不要反向修改指标文件让它满足文字结论。

另可按 [未知题型的数值必要条件](result-invariant-contract.md) 建立真实输出的反证测试，必要条件失败时应先纠错而非润色。
