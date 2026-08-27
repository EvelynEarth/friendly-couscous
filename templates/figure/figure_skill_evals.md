# Figure Skill Evals（科研绘图 Skill 对抗性测试集）

> 目的：不再只靠“写了规则”判断 Skill 是否变好，而用固定失败案例做回归测试。  
> 任何未来修改 `top_tier_scientific_figure_skill.md` / `chart_selection.md` / `journal_figure_mastery_v2.md` 后，应至少过一遍本页。

---

## Eval 1 — 4个方案撑满二维 scatter

### 输入
4 个候选方案，只有“成本变化”和“服务改善”两个指标；其中 1 个方案明显优选。

### 错误答案
画一个大 scatter，4 个点散在巨大二维坐标系，再加大 callout / pastel 优选域。

### 期望 Skill 行为
先问二维关系是不是 claim。
- 若 claim 是 trade-off / Pareto → scatter/Pareto 合理；
- 若 claim 是“为什么选方案A”且类别结构也重要 → 优先 metadata + aligned cost/service panels。

### PASS
不因“二维看起来高级”浪费 axis 空间。

---

## Eval 2 — 固定75% baseline 的100% stacked bar

### 输入
三阶段中 baseline 始终 75%，剩余25%在“缓冲/缺货”之间变化。

### 错误答案
三根100% stacked bar，让固定75%成为每根最大彩色块。

### 期望 Skill 行为
触发 Invariant Subtraction：只画剩余25%的 residual decomposition；75%作为 reference text/metadata。

### PASS
变化信息成为主体。

---

## Eval 3 — equal 2×2 dashboard

### 输入
一个核心 fit panel + residual + sensitivity + 一个几乎重复的 summary。

### 错误答案
四个 panel 机械 2×2 等宽等高。

### 期望
Hero/drop test：fit 为 hero；residual/sensitivity witness；重复 summary 删除。

### PASS
非等权布局或拆图。

---

## Eval 4 — 6条纠缠曲线 + 大legend

### 输入
6条曲线，y-scale差异明显，legend 反复查找。

### 错误答案
一个 axes + 6种鲜艳色 + corner legend。

### 期望
Complexity Decomposition：small multiples / context gray + focus / direct labels；必要时 progressive crop。

### PASS
读者不需要 legend ping-pong。

---

## Eval 5 — 离散参数扫描伪装连续相图

### 输入
5×4 离散网格，无连续模型。

### 错误答案
spline / contourf 画平滑 phase boundary。

### 期望
actual-grid regime map；若阈值需精化，另用真实细网格 slice。

### PASS
无伪连续性。

---

## Eval 6 — deterministic optimization 自造“置信区间”

### 输入
只有求解器最优解、参数敏感性和数值 gap。

### 错误答案
为了“像论文”画 95% CI band。

### 期望
触发 Uncertainty Semantics：parametric sensitivity / numerical gap / scenario range 分开表达。

### PASS
不伪造统计不确定性。

---

## Eval 7 — 大标题/卡片比数据更醒目

### 输入
结果本身只有一条明确阈值曲线。

### 错误答案
大 `sgtitle` + pastel box + “推荐/提升xx%” badge。

### 期望
Salience–Relevance：阈值/数据点是最显著对象；标题缩短/移caption；无卡片。

### PASS
0.5秒先看到数据，不是UI。

---

## Eval 8 — 统计样本用bar of means

### 输入
每组有多个样本且分布偏斜/可能双峰。

### 错误答案
mean bar + SE。

### 期望
raw points / ECDF / box / violin / raincloud；mean只是附加统计。

### PASS
分布结构可见。

---

## Eval 9 — 同一论文8张图全部dumbbell

### 输入
有阈值、网络、分布、成本分解、参数区等不同任务。

### 错误答案
为了保持风格，所有 Figure 都转换成 dumbbell。

### 期望
Figure Suite Manifest：统一的是 typography/palette/annotation rhythm；grammar 随 perceptual task 变化。

### PASS
一致但不单调，且每张图职责不同。

---

## Eval 10 — 为了“多样”乱上高级图

### 输入
3个简单数值比较。

### 错误答案
radar / chord / Sankey / 3D。

### 期望
Graphical Perception：aligned dot/interval 更准确，复杂图直接淘汰。

### PASS
高级感来自判断，不来自复杂度。

---

## Eval 11 — 彩色direct label

### 输入
3条线，已经有marker/linestyle。

### 错误答案
每条线名称都用高饱和系列色大字写在图里。

### 期望
优先黑/深灰文字 + 对应 marker/keyline；只有确有必要且对比度足够时才使用系列色文字。

### PASS
label 不抢数据 salience。

---

## Eval 12 — 大N scatter 导出百万矢量点

### 输入
20万散点，核心 claim 是密度结构。

### 错误答案
每个点都输出 vector marker，PDF巨大且过绘制。

### 期望
hexbin / 2D density / alpha / rasterized data layer + vector labels。

### PASS
既保留密度证据，又保证 production 可用。

---

## Eval 13 — 两张图重复同一结论

### 输入
Figure A 是敏感性折线；Figure B 是相同数据的bar，只换形式。

### 错误答案
两张都保留正文。

### 期望
Suite Redundancy Gate：删除一张，或让另一张承担不同机制/边界证据。

### PASS
每张正文 Figure 都不可替代。

---

## Eval 14 — reference figure 只学颜色

### 输入
用户给出 Nature 风格 metadata strip + aligned forest 参考图。

### 错误答案
只复制青/橙配色和圆点；布局仍松散。

### 期望
Reverse Engineering：body bbox、row density、metadata width、aligned baseline、legend strategy、annotation density。

### PASS
学到 geometry / hierarchy / grammar，而非皮肤。

---

# 回归测试判定

新 Skill 修改后，如果以上任一 eval 的错误答案仍可能被流程“合理批准”，说明 Skill 仍有漏洞。

至少要求：

```text
14/14 行为判断正确
```

再进入实际 Q1/Q2/Q3 重绘测试。