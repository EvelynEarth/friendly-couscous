# 16篇MathorCup大数据优秀论文：基于原PDF正文的论证复盘（v2.13）
 
**研究范围与可核验边界**：来自 EvelynEarth/supreme-spoon main 的16份真实原始PDF，合计716页；本轮已获取字节并逐一比对SHA-256。716页可全文检索；人工分析覆盖**每篇摘要、目录、选定模型、实验/结果及局限的核心页面**，每篇证据页见下表；另对8张具体学术图表/公式/表格页面做了实际渲染核查。**未逐字人工阅读716页，也未重跑获奖作者实验**，因此不得说“16篇全部模型已验证”。PDF页码均为PDF物理页，非印刷页。

此研究的结论被区分为三类：**原文事实**（PDF某页确实这样写）、**独立审稿质疑**（可能存在错误或尚无足够证据）、**新Skill建议**（适用于当前赛题时才启用）。优秀论文并非官方模板，更不是科学结论的自动认证。

资料： [源PDF列表与SHA](https://github.com/EvelynEarth/supreme-spoon/blob/main/award-paper-audit/reports/INDEX.md) · [16篇PDF版面样本](https://github.com/EvelynEarth/supreme-spoon/blob/main/award-paper-audit/VISUAL_SAMPLE_AUDIT.md)。

## 逐篇正文论证卡
### 2024-01 · 台风｜多源时空观测→分类→路径/衰减预测

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=1)、[p6](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=6)、[p18](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=18)、[p37](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=37)。

- **原文事实与论证链**：第6页说明台风生命期长度不同导致特征维度不统一；第18页将聚类类型做成具象路径定义；第37页承认突变转向、风雨激变下存在较大误差。
- **值得迁移的写法**：以任务的数据结构困难作为方法选择依据，并回到失败阶段解释结果。
- **独立审稿风险（不等于已定性违规）**：不能用路径聚类的关联结果直接证明气候因果；需滚动验证和异常轨迹对照。

### 2024-02 · 台风｜K-means聚类→LSTM路径→降水衰减

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=1)、[p16](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=16)、[p19](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=19)、[p25](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=25)。

- **原文事实与论证链**：摘要列明三问算法及MAE/RMSE/DTW；第16页为统一采样间隔丢弃非6小时记录；第25页公开承认降水量模型拟合不足。
- **值得迁移的写法**：结果段落保留弱效果、解释潜在遗漏变量，是可迁移的诚实论证。
- **独立审稿风险（不等于已定性违规）**：删除观测会引入采样偏差，DTW并非独立地理误差；用样本保留率和验证窗交代。

### 2024-03 · 台风｜LOF改进聚类→神经网络分类→时序预测

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=1)、[p6](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=6)、[p16](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=16)、[p30](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=30)。

- **原文事实与论证链**：第6页以聚类噪点为理由引入LOF与初始中心改进；第16页说明高维非线性与神经网络匹配；第30页对模型逐问评价。
- **值得迁移的写法**：新增模块的科学动机应由已有算法不足触发，而非算法越多越好。
- **独立审稿风险（不等于已定性违规）**：必须设计去除模块的消融与随机种子重复，才能证明改进必要性。

### 2024-04 · 台风｜DBSCAN/多预测器对比→模型评价

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=1)、[p19](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=19)、[p27](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=27)。

- **原文事实与论证链**：第19页表7直列RF、XGBoost、CNN-LSTM的RMSE、MAE、MSE；CNN-LSTM的RMSE=0.0336而MSE=0.0071；第27页说明DBSCAN超参数敏感。
- **值得迁移的写法**：多模型共窗指标表+独立模型不足讨论值得借鉴。
- **独立审稿风险（不等于已定性违规）**：【实证数值冲突】同一误差集合应MSE=RMSE²，0.0336²约0.00113，与0.0071不一致；不知道哪个数字正确，不能自行改值。

### 2024-05 · 电商｜预测→一品一仓规划→多目标退火

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=1)、[p14](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=14)、[p15](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=15)、[p27](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=27)。

- **原文事实与论证链**：首页摘要把库存/销量模型输出连接到仓库分配；第14页解释分品类时序预测；第27页同时讨论业务收益、成本和权重依赖。
- **值得迁移的写法**：论文按数据—预测—业务优化串联，而非机械重复三问。
- **独立审稿风险（不等于已定性违规）**：摘要所称部分随机森林R²=1/误差近0须先做泄漏审计；启发式解不可直接称全局最优。

### 2024-06 · 电商｜指数平滑/ARIMA/机器学习预测→NSGA-III约束优化

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=1)、[p15](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=15)、[p21](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=21)、[p34](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=34)、[p43](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=43)。

- **原文事实与论证链**：第34页明确多仓库存与仓容等约束，第43页对销量/仓容增加5%做扰动分析并观察成本/关联度变化。
- **值得迁移的写法**：把上游预测、下游决策变量、约束与鲁棒场景写成因果依赖清楚的研究链。
- **独立审稿风险（不等于已定性违规）**：稳定迭代不等于最优性；需要真实可行性、约束余量和多次独立运行。

### 2024-07 · 电商｜序列分型预测→MOPSO仓储多目标

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=1)、[p8](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=8)、[p19](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=19)、[p20](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=20)、[p37](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=37)。

- **原文事实与论证链**：首页摘要按季节、突变和缺失模式挑选方法；第19页为销量模型描述了随机5折验证；第37页承认求解不能保证最优。
- **值得迁移的写法**：按异质性选模型，并如实描述启发式算法的最优性边界。
- **独立审稿风险（不等于已定性违规）**：对未来时点预测若随机拆分历史序列则有泄漏风险：须确认切分与特征生成顺序，尚不能断言已泄漏。

### 2024-08 · 电商｜多模型销量/库存对比→整数/多目标分仓

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=1)、[p20](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=20)、[p35](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=35)、[p42](https://github.com/EvelynEarth/supreme-spoon/blob/main/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2024%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=42)。

- **原文事实与论证链**：第20页用五模型MAPE图支持模型筛选；第35页呈现分仓变量与数学约束；第42页将详细程序移至附录。
- **值得迁移的写法**：指标图、约束公式、程序附录分工清晰，适合长篇复杂研究。
- **独立审稿风险（不等于已定性违规）**：80/20训练测试未自动证明时间可得性正确；必须独立复核预测→仓储约束接口。

### 2025-01 · 视觉｜CABNet分类→YOLOv11检测→健康指数

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=1)、[p9](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=9)、[p13](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=13)、[p24](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=24)、[p28](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-1.pdf#page=28)。

- **原文事实与论证链**：第9页解释双注意力抑制背景；第24页按缺陷类别给出Precision/Recall/F1，其中Hole召回约0.291；第28页逐问题总结。
- **值得迁移的写法**：整体指标须由小类与失败样本证据补充；类别粒度的错误分析很重要。
- **独立审稿风险（不等于已定性违规）**：健康指数是按权重构造的业务量，未经标定不能宣称真实结构安全概率。

### 2025-02 · 视觉｜迁移学习二分类→检测/分割→多维评价

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=1)、[p10](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=10)、[p12](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=12)、[p18](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-2.pdf#page=18)。

- **原文事实与论证链**：第10页先审标注完整度、缺陷分布与bbox大小；第12页说明迁移学习/增强的理由；第18页明确NMS与掩码的输出衔接。
- **值得迁移的写法**：先核查标签，分别定义分类、检测、分割产物及验证方法。
- **独立审稿风险（不等于已定性违规）**：数据增强不能代替未见场景评估；检查同源图像与mask标注的一致性。

### 2025-03 · 视觉｜增广→ResNet50-FPN-CA→YOLOv8与三维评估

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=1)、[p11](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=11)、[p14](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=14)、[p15](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-3.pdf#page=15)。

- **原文事实与论证链**：摘要说明从有残损图裁剪无残损区域扩样；第11页事先列准确、鲁棒、效率指标；第14–15页对齐主干/注意力/融合/分类与实验。
- **值得迁移的写法**：提出新模块之前就先声明实验验收维度；模块图要与消融数据对应。
- **独立审稿风险（不等于已定性违规）**：同一原图裁剪后跨折共享背景会产生风险；必须先按源图划分，再增广。

### 2025-04 · 视觉｜MobileNet快速筛选→YOLOv11检测与分割

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=1)、[p8](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=8)、[p13](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=13)、[p22](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-4.pdf#page=22)。

- **原文事实与论证链**：第8页以FLOPs讨论轻量化；第13页展示检测/分割联合损失；第22页给出F1、mAP、FPS等多维结果。
- **值得迁移的写法**：速度与准确度应围绕部署约束协同说明。
- **独立审稿风险（不等于已定性违规）**：FLOPs不等于设备真实FPS；时延证据须有硬件、batch与图像尺度。

### 2025-05 · 物流｜分位数分层双阈值→XGBoost金额/风险预测

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=1)、[p5](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=5)、[p11](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=11)、[p13](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=13)、[p19](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-5.pdf#page=19)。

- **原文事实与论证链**：第11页用绿黄红风险分区图衔接分类结果表，表内能看到原规则与拟合规则不一致实例；第13页进一步介绍回归特征。
- **值得迁移的写法**：图→解释→对照表能让规则边界具体化而不是停留在公式。
- **独立审稿风险（不等于已定性违规）**：自建风险标签不等于外部真值；推理时若无实际赔付金额不能将其当作预测输入。

### 2025-06 · 物流｜模糊区两阶段标签→树模型金额回归→不平衡

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=1)、[p7](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=7)、[p23](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=23)、[p29](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-6.pdf#page=29)。

- **原文事实与论证链**：第7页记录按规则删除2482条记录；第23页保留MAPE=86.68%的不利成绩并说明小额分母问题；第29页讨论目标编码泄漏并给有序编码思路。
- **值得迁移的写法**：失败指标与数据清洗过程不应隐藏，泄漏防范写成可执行操作。
- **独立审稿风险（不等于已定性违规）**：零额MAPE需事先定义；目标编码是否在每折训练内拟合，须审查实际代码。

### 2025-07 · 物流｜单调分位边界MQBL→Stacking→SMOTE

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=1)、[p17](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=17)、[p21](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=21)、[p30](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-7.pdf#page=30)。

- **原文事实与论证链**：第17页基于高维和效率需求阐述LightGBM；第30页比较原始基线全局误差与少数类识别改善之间的取舍。
- **值得迁移的写法**：不要把单一分数写成全局最佳，先交代小类成本与整体误差取舍。
- **独立审稿风险（不等于已定性违规）**：Stacking须OOF，SMOTE/目标编码只在训练折执行，弱标签阈值冻结需验证。

### 2025-08 · 物流｜无真值风险规则→赔付回归→统计诊断

原文：[p1](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=1)、[p6](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=6)、[p20](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=20)、[p32](https://github.com/EvelynEarth/supreme-spoon/blob/main/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87/2025%E5%B9%B4MathorCup%E5%A4%A7%E6%95%B0%E6%8D%AE%E7%AB%9E%E8%B5%9B%E4%BC%98%E7%A7%80%E8%AE%BA%E6%96%87-8.pdf#page=32)。

- **原文事实与论证链**：第6页说明数据本身无风险标签，先建立可复现动态阈值；第20页用小提琴图论证类内密度；第32页用残差/QQ图讨论预测分布。
- **值得迁移的写法**：先阐明标签从何而来，再解释分布图与规则一致性的联系。
- **独立审稿风险（不等于已定性违规）**：残差大致正态不证明无偏或外推能力；需要独立样本与子群体验证。

## 跨赛道的可迁移设计：先定证据类型，再选章节

| 真实研究依赖 | 与16篇原文对照的参考页 | 论文可复用组织策略 | 审稿红旗 |
|---|---|---|---|
| 多源时空观测→分类→预测/机理 | 2024-01 p6、p37；2024-02 p16、p25 | 数据粒度统一、模型必要性、真实时点和异常路径在正文闭环 | 数据删除偏差、预测地理误差未核、相关误当因果 |
| 需求预测→资源优化 | 2024-05 p15、p27；2024-06 p34、p43；2024-07 p19、p37 | 预测误差向下游约束/成本传播；报告可行性、权重、敏感性 | 时序随机分折、最优性宣称过度、R²异常完美 |
| 分类→检测/分割→业务评分 | 2025-01 p9、p24；2025-02 p10；2025-03 p11、p14 | 标签审计在前；总体与小类错误并重；图表回应鲁棒和效率 | 源图拆分泄漏、仅用Accuracy、把健康权重说成安全真值 |
| 无真值风险标注→回归→不平衡 | 2025-05 p11；2025-06 p23、p29；2025-07 p30；2025-08 p6、p32 | 区分规则标签、真实标签和预测；展示小类、零值误差与损失权衡 | 目标编码/SMOTE泄漏、伪标签当真值、正态残差推成无偏 |

## 论文科学审稿新增五道硬门

1. **先核数值恒等式**：指标都来自同一原子误差时，必须复核 `MSE ≈ RMSE²`；2024-04 p19的CNN-LSTM列为0.0336和0.0071，按相同定义不自洽。不同样本、单位或加权口径不能直接套用恒等式，必须先确认口径。**不得自行改获奖论文数字**。
2. **模型选择的理由和失败对照**：先明确数据结构限制、简单Baseline、加入复杂模块的必要性；每个改善主张需消融、对照窗、随机性或稳健性证据。
3. **训练/测试的可用时点**：有序数据滚动回测；视觉以原图分组拆分，增强在split之后；目标编码、Stacking、SMOTE应只在训练折内部学习。
4. **真实实验的图—表—文字三者闭合**：一个图回答明确问题、一张表呈现单位清晰的实际数字，正文解释差异、失败窗口与证据边界，避免装饰性配图。
5. **结论与官方任务严格匹配**：预测值、分数、伪标签、业务安全评分和优化情景都是不同证据类别；无独立验证时不能直接将条件性推断写成真实结论。

## 注意：只取可证实的论文写作原则

- 选中的获奖论文仍可能含数值矛盾、潜在泄漏风险或排版不足；本研究只把它们作为**有页码的研究与审稿案例**。
- 文中引用的原模型数值尚未取得各论文完整原子结果与代码执行证据，**从未通过外部复现**。
- 原16篇全文属于原仓库作者，本文仅用少量事实概述和链接，不复制作者原文段落或整幅图片。
- 用户本地Windows11+TeX Live模板仍需当届官方格式优先，不用这些不同年份优秀论文统一限制标题字号、缩进、绘图颜色或问题数量。
