# Figure Skill Evals（科研绘图 Skill 对抗性测试集）

> 目的：不再只靠“写了规则”判断 Skill 是否变好，而用固定失败案例做回归测试。  
> 任何未来修改 `top_tier_scientific_figure_skill.md` / `chart_selection.md` / `journal_figure_mastery_v2.md` / `mechanism_figure_contract.md` / `journal_palette_contract.md` 后，应至少过一遍本页。

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
3个简单数值比较，没有连续关系、守恒流或第三维必要性。

### 错误答案
radar / chord / Sankey / 3D。

### 期望
Graphical Perception：aligned dot/interval 更准确，复杂图淘汰。

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
用户给出期刊风格 metadata strip + aligned forest 参考图。

### 错误答案
只复制配色和圆点；布局仍松散。

### 期望
Reverse Engineering：body bbox、row density、metadata width、aligned baseline、legend strategy、annotation density。

### PASS
学到 geometry / hierarchy / grammar，而非皮肤。

---

## Eval 15 — 机制图塞满长文字

### 输入
一个有对象流、反馈和决策的机制问题。

### 错误答案
每个节点写3–5行说明，底部再放“模型映射/公式来源”大段文字。

### 期望
触发 Sparse Mechanism Design：节点1–2行短标签；完整解释移 caption/正文；让对象与路径成为主体。

### PASS
0.5秒先看到机制路径，不是文本墙。

---

## Eval 16 — pastel + 多图标 AI mechanism infographic

### 输入
生产/物理机制图，真实逻辑只有少量对象和反馈。

### 错误答案
大面积浅色卡片、渐变、阴影、emoji/人物/设备贴纸、五六种图标和多色箭头。

### 期望
白底、黑/深灰主路径、至多一个风险/回流强调色；图标0–3类且只辅助识别。

### PASS
像论文机理图，不像营销信息图。

---

## Eval 17 — 机制图连线穿框/交叉

### 输入
主流程 + 异常路径 + feedback 回流。

### 错误答案
箭头穿过节点文字、多个反馈线互相交叉、箭头标签压在线头上。

### 期望
重新分层和预留 feedback corridor；Draw.io 使用 orthogonal connectors；要求 crossing/through-text/overlap = 0。

### PASS
主路径和回流都能顺着读，不需要猜箭头归属。

---

## Eval 18 — 复杂物理机理图仍用 MATLAB/Python 手算坐标

### 输入
对象形态和空间过程本身是理解模型的关键，且需要中文标注。

### 错误答案
默认用 matplotlib/MATLAB 画大量框和手工坐标，因为“会写代码”。

### 期望
Tool Router：物理/场景机制 image generation first；中文/结构/可编辑失败则 Draw.io；程序化绘图仅在坐标/场本身有数学价值时使用。

### PASS
工具服从图的语义，不服从习惯。

---

## Eval 19 — Draw.io XML 无效或只是改扩展名

### 输入
用户要求可编辑 Draw.io XML。

### 错误答案
把 `.drawio` 直接复制成 `.xml`，不核验 mxGraphModel/root/id/source/target；使用多个视觉编码却无图例。

### 期望
生成真实 uncompressed XML，结构 preflight + preview review；编码>1时给简短图例。

### PASS
XML能解析、可编辑，视觉语法也可恢复。

---

## Eval 20 — 当前问绘图静默显示另一问

### 输入
多问项目中某问有自己的结果工作簿和候选绘图脚本，系统路径上还存在上一问旧脚本。

### 错误答案
脚本运行成功但显示上一问的标题/变量/数据；只凭“脚本没报错”继续审图。

### 期望
Cross-question Figure Identity：question id + workbook identity + required sheets/headers + candidate fingerprint；冲突时 fail-fast，并检查实际路径/函数 shadowing。

### PASS
不同小问无法静默串档。

---

## Eval 21 — 明明高级图更好却机械退回普通图

### 输入
有清晰策略切换区、最优—次优间隙和二维参数交互。

### 错误答案
因为“高级图要谨慎”，只画几条普通敏感性折线或柱状图。

### 期望
Advanced-first：主动比较 regime/decision map、threshold slice、transition forest 等；如果 reader-task 增益明显，优先高级 grammar。

### PASS
“尽量用高级图”被落实为主动候选搜索，而非保守降级。

---

## Eval 22 — 高级图只因复杂而准入

### 输入
阶段关系不守恒、第三维可被二维无损表达、数据只有几个简单类别值。

### 错误答案
为了“更高级”使用 Sankey、3D surface、radar/chord。

### 期望
每个 advanced candidate 必须写 why better + simpler fallback + reviewer risk；没有信息增益就淘汰。

### PASS
Advanced-first 与 evidence-governed 同时成立。

---

## Eval 23 — 图型正确但没有最终版面可读性

### 输入
MATLAB大窗口中一个多panel高级图看起来很清楚，但放入论文双栏/单栏后文字和局部差异几乎不可读。

### 错误答案
以“大窗口看起来没问题”为理由冻结。

### 期望
final-width / thumbnail / embedded-paper QA；优先拆分、调整panel ratio、减少annotation，再考虑缩字体。

### PASS
Figure 在真实论文尺寸仍能回答 Primary question。

---

## Eval 24 — 用户只让改配色，却擅自改图型

### 输入
用户明确说“这个图型可以，只改顶刊配色，不要改结构”。

### 错误答案
为了“去 AI 味”，把填色矩阵改成 glyph matrix、删除 region fill、增删 panel 或改变 axis domain。

### 期望
触发 `Mutation Scope Gate = palette_only`：冻结 grammar/layout/geometry/annotation/data，只改 palette token、colormap、alpha 和必要的 contrast-dependent text/edge。

### PASS
用户授权边界被严格尊重；结构建议只能另行提出，不能偷偷实施。

---

## Eval 25 — 把“顶刊配色”误解成一套 Nature 浅蓝橙

### 输入
用户要求“仔细搜顶刊论文配色”，当前图有较大色块。

### 错误答案
立刻套 `#0072B2 + #E69F00`，再把所有区域混入 70–85% 白色，导致 pastel washing；或声称存在唯一“Nature官方配色”。

### 期望
执行 Journal Palette Research Gate：区分 publisher readability guideline、journal-inspired qualitative palette、scientific colormap；至少比较3个候选，并在当前真实图面积上评估 contrast / AI risk / CVD / grayscale / paper-family fit。

### PASS
不把可访问性原则误当成唯一审美色板，也不制造一整页奶油浅色。

---

## Eval 26 — 用户说“太浅像AI”，却把图全改成灰色

### 输入
用户反馈大面积浅蓝/浅橙太浅、AI味重，但没有要求黑白图。

### 错误答案
把 primary/secondary 全部去色成灰阶，或直接删除区域颜色。

### 期望
Palette-only 修复优先：提高主色墨色、减少 white-mix、加深 context gray、比较成熟 journal-inspired palette；保留原有语义和图型。

### PASS
解决“浅”而不是把“彩色科研图”误删成黑白图。

---

## Eval 27 — 连续/排名热图用普通浅蓝或定性色硬凑

### 输入
一个 rank/强度/概率热力图，需要明确的序数/连续视觉顺序。

### 错误答案
使用一组无顺序的期刊定性色，或浅蓝端接近白色导致大面积不可见，只因为“蓝色像论文”。

### 期望
先分类 sequential/diverging/cyclic；选择 Crameri/ColorBrewer/cividis 等感知顺序明确的科学色图；必要时裁剪最浅/最深端，而不是破坏数值顺序。

### PASS
colormap 同时具备科学语义和视觉可读性。

---

## Eval 28 — palette-only 自动补丁引入 MATLAB 语法错误

### 输入
已可运行的 MATLAB Figure candidate，仅需要换 RGB/colormap。

### 错误答案
使用大范围字符串/正则替换，误删 `)`、留下未定义旧 palette token，交给用户后在某行报“无效表达式”。

### 期望
Palette token 集中定义；`palette_only` 不大范围改写图型段；修改后至少做括号/方括号/花括号、字符串、旧 token、未定义 token、关键函数调用静态 preflight。若无法本地运行 MATLAB，必须明确“静态检查通过 ≠ runtime 已验证”。

### PASS
换色不会破坏原本可运行的代码，也不会把用户当第一层语法 linter。

---

# 回归测试判定

新 Skill 修改后，如果以上任一 eval 的错误答案仍可能被流程“合理批准”，说明 Skill 仍有漏洞。

至少要求：

```text
28/28 行为判断正确
```

再进入通用 synthetic regression：
- 简单数值比较；
- 高级数值 Figure；
- 普通结构机制图；
- 物理/场景机理图；
- 带反馈/回流的 Draw.io 图；
- `palette_only` MATLAB candidate；
- sequential / diverging heatmap。

测试不得使用正在求解赛题的真实数据、结果值、工作簿、代码或图片。
