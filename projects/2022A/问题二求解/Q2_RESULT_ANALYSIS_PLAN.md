# Q2 Result Analysis Plan

前置状态：Q2 主结果与 `a=100000` 周期稳态边界精修已通过数值质量门，进入 `modules/03_result_analysis.md`。

## Evidence A — 线性与幂律最优方案的收益差

- target claim：幂律阻尼相对最优直线阻尼可带来稳定但幅度较小的平均功率提升。
- source：`问题二求解结果.xlsx` + `问题二边界稳态精修结果.xlsx`。
- method：比较 `P_linear` 与边界精修 `P_powerlaw`，给出绝对增量、相对增量。
- disposition criterion：若增量为正且大于步长/收敛数值误差多个数量级，则 support；否则 modify/reject。

## Evidence B — a 上边界结构与 n 局部敏感性

- target claim：幂律最优点位于 `a=100000` 上边界，且 `n≈0.416` 为内部局部最优。
- source：主工作簿 `边界邻域检查` + 边界精修工作簿 `局部稳态扫描/一维精修/边界对照`。
- method：计算 `a` 近边界变化的功率差；围绕 `n*` 计算功率损失曲线、近优区间和局部平坦度。
- disposition criterion：若边界点不低于近邻且 `n*` 左右均降功率，则 support。

## Evidence C — 数值稳定性余量

- target claim：最终最优功率不依赖单一时间步长或未收敛瞬态。
- source：两工作簿 `收敛诊断` 与边界精修 `T/40/T/80` 结果。
- method：汇总最终窗口功率相对差、同相位状态相对差、步长加密差，并与阈值比较。
- disposition criterion：全部低于门限则 support；接近门限则 modify；超过则 reject/redo。

## Evidence D — 优化器增益与结果可解释性

- target claim：二维 DE 提供全域候选，Powell 只做局部微调；最终边界稳态精修对结果仅做小幅修正，不改变结构结论。
- source：主工作簿 `优化诊断` + 边界精修 `核心结论`。
- method：比较 DE、Powell、边界精修各阶段功率与参数变化。
- disposition criterion：若后续修正远小于主方案收益且参数结构一致，则 support。

## 输出

生成 `问题二求解/问题二结果深化分析.py`，用户本地运行后输出 `问题二求解/问题二结果深化分析.xlsx`。分析脚本只读取已验收结果工作簿，不重复二维 DE 或主 ODE 求解链。
