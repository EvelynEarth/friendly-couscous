# Journal Figure Case Patterns（顶刊实际论文图型案例拆解）

> 目的：不是复制论文图，而是从真实顶刊 Figure 中抽取**结构模式**。  
> 数据与结论仍以本项目 accepted workbook 为唯一真值。

## Case 1 — Nature Communications：参数相图 + 理论/仿真直接并列

来源：Community structure-regulation coupling reveals optimal information diffusion (2026)  
https://www.nature.com/articles/s41467-026-73665-1

该文 Fig. 3 / Fig. 4 的关键结构：
- 主体是参数空间 phase diagram；
- 理论近似和 simulation 使用同一视觉语法并列；
- 多 panel 的存在理由是**同一边界在不同网络混合参数/理论-仿真下直接比较**；
- caption 承担大量机制解释，图内不堆长段文字；
- 颜色映射服务于同一个状态变量，不为每 panel 换色板。

本仓库可迁移模式：

```text
参数区域 / 策略区域
+ 同尺度对照 panel
+ 基准点 / 最优点
+ 简洁共享 legend
```

适合：鲁棒性、可行域、相变、策略区域、理论 vs 仿真。

---

## Case 2 — Nature Communications：Overview + Detail 的 phase diagram

来源：Nucleation phenomena and extreme vulnerability of spatial k-core systems (2024)  
https://www.nature.com/articles/s41467-024-50273-5

该文 Fig. 4：
- panel a 用 phase diagram 给总体状态区；
- panel b 用具体 damage propagation 示例解释 phase 的物理含义；
- overview 和 example 不是重复，而是“一张定义边界，一张解释边界为何重要”。

本仓库可迁移模式：

```text
Overview parameter map
+ one representative mechanism/example panel
```

准入条件：detail panel 必须解释 overview 中看不出的机制，否则不加。

---

## Case 3 — Nature Communications：敏感性证据按阅读任务分 panel

来源：EnzymeTuning improves enzyme-constrained metabolic modeling... (2026)  
https://www.nature.com/articles/s41467-026-73744-3

Fig. 2 同时包含 workflow、CDF、Venn、box plot 等多种图型，但不是 dashboard 式乱拼：
- workflow 解释分析链；
- CDF 说明敏感性分布；
- intersection panel 说明筛选逻辑；
- box plot 比较最终性能。

关键不是“图型多”，而是 panel 按**证据职责**排列，形成同一 scientific story。

本仓库可迁移规则：
- 不执行“同一 Figure 只能一种图型”的机械禁令；
- 允许多图型，前提是每个 panel 有不可替代职责并组成一条证据链；
- 每个 panel 的面积按信息密度，不按数量平均分。

---

## Case 4 — Nature Communications：拟合 / 机制 / 敏感性三联证据

来源：Emulator-based Bayesian optimization for efficient multi-objective calibration... (2022)  
https://www.nature.com/articles/s41467-021-27486-z

Fig. 3：
- 一个 panel 回答 calibration goodness-of-fit；
- 一个 panel 展示 epidemiological relationship；
- 一个 panel 用 tile shading 展示 parameter sensitivity；
- 三者属于同一“模型校准可信度”主题，但视觉语法不同。

可迁移模式：

```text
fit evidence
+ behavior evidence
+ sensitivity evidence
```

只有这三块共同形成一个可信度结论时才合图；若只是三个独立结果，则拆开。

---

## Case 5 — Nature Communications：真正的 phase diagram 是“区域 + 边界 +代表状态”

来源：Multiple tipping points and optimal repairing in interacting networks (2016)  
https://www.nature.com/articles/ncomms10850

Figure 2 的信息结构：
- 区域颜色表示 state；
- boundary line 表示 transition；
- critical/triple points 用点强调；
- representative states / transitions 通过示意补充。

本仓库可迁移规则：
- phase diagram 只有在“区域/边界”真的有连续或足够密的证据时使用；
- 离散 sparse grid 不应冒充连续相图；
- sparse grid 应显示实际采样点/tiles，并配 threshold slice 或区间说明。

---

## Case 6 — Nature Communications：敏感性图不必追求复杂图型

来源：The role of direct air capture in achieving climate-neutral aviation (2024)  
https://www.nature.com/articles/s41467-024-55482-6

Fig. 6 使用一组直接 sensitivity panels 回答输入变化对成本差异的影响。

本仓库可迁移规则：
- 线图/点图如果已经最直接，就不要为了“高级”替换成 3D / radar / chord；
- 高级感来自：shared scale、紧凑 panel、清楚阈值、稳定颜色职责和 caption 闭环。

---

# 从真实顶刊 Figure 归纳出的 8 个高频结构规律

1. **Panel 是证据单元，不是装饰单元。**
2. **多 panel 可以多图型，但必须围绕同一 take-home message。**
3. **Panel 大小经常不等，取决于数据密度和说明难度。**
4. **同一变量跨 panel 保持同色/同 marker/同尺度语义。**
5. **图内文字短，长解释交给 caption。**
6. **Overview + detail 是高频有效结构，但 detail 必须不可替代。**
7. **phase / regime 图强调区域和边界；没有边界证据时展示真实采样，不伪造相图。**
8. **顶刊并不排斥基础图型；真正被避免的是重复、空白、混乱和无意义复杂度。**

# 本项目应用方式

当用户要求“参考顶刊重新设计”时，先从本案例库选**结构模式**，不是选外观：

```text
参数区 + 阈值切片
理论 / 仿真并列
overview + mechanism detail
fit + behavior + sensitivity
阶段机制 + outcome comparison
```

然后再用本题中文字段、真实数值、HSK review typography 和 Figure Contract 重画。