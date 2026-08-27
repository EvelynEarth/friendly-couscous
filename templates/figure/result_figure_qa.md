# 结果图 QA

| 检查项 | 状态 | 备注 |
|---|---|---|
| 数据是否来自每问两类标准工作簿 |  |  |
| 是否记录源工作表、真实表头和固定列位置 |  |  |
| MATLAB 是否只绘图、不重算核心结果 |  |  |
| 图窗是否默认可见并保留 |  |  |
| 是否避免默认自动导出和关闭 |  |  |
| 是否在写代码前明确 `Iteration mode = beautify / redesign` 与 `Architecture status` |  |  |
| `beautify` 模式是否保持已接受图型、证据职责和数据系列，仅调整视觉层 |  |  |
| `redesign` 模式是否先通过 Figure Layout Gate / Chart Selection 并在编码前冻结候选架构 |  |  |
| 用户已将 Figure / panel / 图型标为 `frozen` 后，是否避免静默换图型或改证据职责；需要变化时是否先显式 reopen |  |  |
| 单图是否有简洁 `title`，多面板是否有整体 `sgtitle` |  |  |
| 标题是否只说明研究对象、指标关系和必要方法信息 |  |  |
| DOCX/LaTeX 图注是否补充统计口径且未与 MATLAB 标题逐字重复 |  |  |
| 中文坐标轴、单位、图例是否完整 |  |  |
| 字号、线宽、配色和边框是否符合规范 |  |  |
| 配色是否先定义 Primary / risk-failure / baseline / structure / context 等颜色职责，再选择具体 Hex，而非机械套 Nature/Science/Okabe-Ito 固定模板 |  |  |
| 全图是否控制主色数量并保证高对比、色盲/灰度可区分；辅助对象是否明显降权 |  |  |
| 若用户给出参考图，是否明确区分“模仿版式/配色职责/视觉语法”与“本题数据/语义”，且数据仍来自 accepted workbooks |  |  |
| 若用户给出参考图，是否在写代码前拆解主体 geometry、metadata、密度/纵横比、颜色职责、点线层级、annotation 与 legend，而非只复制表面图型元素 |  |  |
| 是否写明 `Must imitate / Must preserve / Do not copy`，避免把参考图中的标签、阈值和对象结构复制进本题 |  |  |
| 是否先完成 Figure role/图型 → 主体 geometry/密度 → 坐标域/对齐 → 视觉编码 → annotation → legend → polish 的分层图审 |  |  |
| 若类别 metadata、结构 tiles 与连续数值图共享行语义但 x 域不兼容，是否拆为严格对齐的独立 axes，而非负坐标/极端 xlim/同轴硬塞 |  |  |
| 复合 Figure 是否仍只有一个一级 Primary question；高级结构是否提供不可替代的信息，而非为了 panel 数或“高级感”堆图 |  |  |
| “同一种图型尽量一次”是否用于删除证据重复，而非机械禁止必要的结构编码或强配对联合诊断 |  |  |
| 用户明确“只改某张图/某个主体/legend/不要动某部分”后，是否只修改反馈作用域；若必须联动是否已解释依赖 |  |  |
| 单轮 redraw 是否避免同时大改图型、panel、配色、标注、legend 与入口文件，确保反馈因果可追踪 |  |  |
| 同一 Figure 连续约 3 轮仍未收敛时，是否先做 Reference/Current mismatch diagnosis 再继续出下一版 |  |  |
| 交付用户前是否按实际图窗尺寸做 Screenshot Preflight，检查标题/轴/脚注/legend/数据标签遮挡、主体过松/过密与主焦点 |  |  |
| 用户明确“通过/确定这一版/保留”后，是否立即记录 accepted/frozen、canonical `qX_plot.m` 与 SHA-256，后续仅在显式 reopen 时修改 |  |  |
| 当前问题目录是否只保留 canonical `qX_plot.m` 作为 active 绘图入口，并已清理实验版 `.m`、重复 wrapper 和近似命名旧入口 |  |  |
| 若使用 Local Zoom，是否确有局部判别价值且 ROI 与主图对应清楚 |  |  |
| 若使用 Small Multiples，跨面板比较所需坐标尺度是否一致或已明确说明差异 |  |  |
| 若使用 Focus Highlighting，是否保留必要上下文而未选择性隐藏不利对象 |  |  |
| 若使用 Semantic Background，背景是否对应真实阈值、状态或阶段而非装饰 |  |  |
| 若使用 Composite Diagnostic / 3D，是否仍只有一个一级阅读任务且高级形式确实提高信息效率 |  |  |
| 是否避免为美观对离散点擅自平滑并制造新峰谷/拐点 |  |  |
| 标题—图注—工作簿—脚本—结论是否已同步到 `模型论文框架.md` |  |  |
| 是否能绑定正文结论 |  |  |
