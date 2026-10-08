# MathorCup 2025 A/B 真实附件就绪检查与论文数字闭环（v2.3）

## 明确结论边界

本协议使用 `EvelynEarth/supreme-spoon` 的**真实 GitHub 文件清单与抽查标注**，比 v2.2 的纯合成对抗样例更进一步；但仓库连接只返回文本和元数据，**没有在 CI 中下载/训练 3,713 张真实图片，也没有解开 2025 B 的 LFS Excel 内容**。所有模型分数、训练耗时、测试结果均为**尚未执行**。

[已核对的来源快照](../competition/real_case_2025_profiles.json) 记录源仓库 `main` 文件树与抽查结果。适用于**历史 2025 赛题复盘**，不得用于规定 2026 当届任务规模或提交方式。

## 2025 A — 视觉任务

GitHub `数据集3713/` 文件树提供：`images/train` 3300 个图像文件与 `labels/train` 3300 个标签，`images/test` 413 图像文件与 `labels/test` 413 标签。类别 ID 为 Dent=0、Hole=1、Rusty=2；抽查 `labels/train/1.txt` 的 9 个框均为 ID 2，`labels/train/100.txt` 的 1 个框为 ID 0。**这些是归一化 bbox 坐标，不是像素分割 mask。**

本地将数据集解压/clone 到真实路径后：

```bash
python skills/big-data-competition-skill/tools/real_case_audit.py 2025-a --root "/path/to/数据集3713"
# 当计算资源允许时，进行跨 split 图片二进制 SHA-256 精确重复检查
python skills/big-data-competition-skill/tools/real_case_audit.py 2025-a --root "/path/to/数据集3713" --hash-images
```

检查完整性、训练标签是否越界/漏配、bbox 类别分布，并检测测试标签是否存在。**默认只读 `labels/train`**；即使仓库公开了 `labels/test`，也不可用它来构造特征、筛模型、校准阈值、调参或选论文主结果。测试标签有无只统计文件数量，不读正文。

数据就绪后还需实际训练：从 `train` 创建与实体/拍摄场景相适配的内部训练-验证切分，至少用简单图像分类/检测基准与候选模型在同一 holdout 上比较，并记录真实指标；若没有实体 ID，标注这一限制并用感知重复检查补充。**工具返回 `ready_for_baseline` 不表示任何模型已训练。**

`--hash-images` 仅识别**字节完全相同**的跨分组图片；语义近重复、同集装箱多角度及相同背景仍须单独人工/算法审计。且不同 split 出现相同文件名并不直接证明数据泄漏。

## 2025 B — 理赔风险

已查阅的仓库中 `附件1.xlsx`、`附件2.xlsx` 和 `Result.xlsx` 是 **Git LFS 指针文本**，指针各自报告原对象字节数 2、503356、33319。这不等于已拥有可读 XLSX。尤其 `附件1` 仅声明 2 字节，极可能不完整，应优先找官方原附件而不是编造字段或示例表格。

```bash
git lfs pull
python skills/big-data-competition-skill/tools/real_case_audit.py 2025-b --root "/path/to/2025年MathorCup大数据挑战赛-赛道B初赛"
```

结果 `blocked`：文件缺失、仍为指针或 XLSX 不是真正可解压的 OOXML；切勿声称已运行回归/分类。`ready_for_schema_review`：三个文件**仅通过容器完整性**，仍需核对 sheet、字段、样本行数、标签构造规则、ID 顺序与官方 `Result.xlsx` 模板。2025 B 结果为 XLSX，不能用只支持 CSV 的检查冒充校验通过。

当真实数据恢复后：明确结算赔付金额是否仅作为训练标签可用，**不得作为未来索赔预测特征**；用统一 holdout 比较金额回归+映射规则与直接分类，记录少数类别召回/F1，做阈值与稳定性敏感性分析。指标须真实跑出。

## 论文真实数值追踪（通用）

使用 [实验证据记录模板](../templates/accepted-evidence-record.md) 与可执行脚本：

```bash
python skills/big-data-competition-skill/tools/paper_evidence_gate.py --record /path/to/accepted_record.json --artifact-root /path/to/accepted_outputs
```

要核查 `run_status=accepted`、数据/代码版本、验证方案、随机种子、split 文件、实际指标、每个 artifacts 的 SHA-256，以及每条论文数字与存档指标完全一致。若用户本地还没实际执行，`run_status=planned` 必须被拒绝作为正式论文证据；文件哈希不一致时立即终止引用。

**SHA-256 一致只证明记录和文件未改变，不能独立证明结果科学正确。** 仍需模型评审、泄漏检查、官方指标实现与论文审阅才能接受该结果。不得把此 Skill 的合成单元测试当成获奖论文的复现。

## 后续阶段验收

1. **文件级**：真实附件就绪、预检无阻断、源文件版本记录。
2. **实验级**：完成真实 Baseline、切分复核、候选模型、性能/误差/消融，保留失败案例和运行日志。
3. **论文级**：运行上面的证据追踪工具，逐条核对图表、摘要、正文数字并标记局限。
4. **评委级**：检查所有子任务和当届实际提交模板；缺数据时发布阻断报告而非虚构实验。

这四个门槛不能仅靠 CI 的通过状态替代。
