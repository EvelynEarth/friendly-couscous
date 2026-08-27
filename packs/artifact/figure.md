# Artifact Pack：图表

## 进入条件

用户要求结果图、敏感性图、鲁棒性图、多算法图、机理图或 MATLAB 代码时加载。图表必须服务明确结论，不以复杂图型、固定版式或面板数量替代证据。

本 Pack 只做阶段摘要，不重新定义 Figure Evidence 规则。布局、证据层级、数据事实源、Figure Enhancement Gate、配色和 Figure Contract 的唯一权威为 `modules/04_figure_evidence.md`；若本文件与该模块不一致，以后者为准。高级增强的实现模式集中在 `templates/figure/figure_enhancement_patterns.md`，该模板只提供实现参考，不拥有独立决策权。

## 图审迭代执行约定

本节只把 Module 04 已有的 Primary question、Layout Gate、Enhancement Gate 与视觉注意力预算转成可执行的图审顺序，不建立第二套绘图 Authority。

### 0. 先选择迭代模式：Beautify / Redesign

在生成任何新 MATLAB 版本前，先明确当前任务属于哪一种：

```text
Iteration mode: beautify / redesign
Architecture status: proposed / approved / frozen / reopened
```

- **Beautify**：图型、证据职责和数据系列已经被接受，只优化主体 geometry、颜色、字体、网格、点线、边距、标注、legend 和 polish；不得静默换图型或增删证据系列。
- **Redesign**：用户明确要求重新选图型、重新组织 panel 或重新设计证据结构；先通过 Figure Layout Gate / `chart_selection.md`，得到候选架构并人工审核，再进入代码。
- **Frozen**：用户已经说“确定这个版本 / 保留 / 不要再动”，后续默认重新回到 Beautify/Polish；若要改图型、Evidence role 或 panel 架构，必须先显式 reopen。

外部科研美化规范中的“类型保留 / 美化不修改”默认适用于 Beautify；不能把它机械扩展到用户已经明确授权的 Redesign，也不能在架构 frozen 后继续用 Redesign 名义漂移。

### 1. 参考图先分解，后写代码

当用户提供 Nature/SCI/论文截图作为视觉参考时，默认只借鉴**版式、配色职责和视觉语法**；本题数据、阈值、对象和结论仍必须来自当前 accepted workbooks。生成 MATLAB 前先记录一个轻量 Visual Contract：

```text
Primary question / Evidence level
Reference purpose: layout / color role / visual grammar / none
Must preserve
Must imitate
Do not copy
Body geometry / density / aspect ratio
Metadata / color roles / line-point hierarchy
Annotation budget / legend placement
Frozen existing figures or panels
```

必须把参考图拆成“主体 geometry → metadata → 视觉编码 → 标注 → legend”几个层次，不能只因为看到了 inset、legend、Sankey、Tornado 等表面元素就机械复制。

参考图的拆解优先量化这些关系，而不是先抄颜色 Hex：

- canvas / aspect ratio；
- 主体占版比例；
- 行列 pitch 与密度；
- metadata strip 宽度及其与主图区的距离；
- guide / background 的强弱；
- marker / line / band 的层级；
- annotation 数量与位置；
- legend footprint。

### 2. Figure Review 采用 body-first 顺序

人工图审默认按以下顺序推进：

```text
A. Figure role / 图型与证据职责
→ B. 主体 geometry、密度、纵横比
→ C. 坐标域兼容性与 panel/axes 对齐
→ D. 视觉编码：颜色、点、线、metadata
→ E. 标注、标题与轴标签
→ F. legend / 脚注
→ G. 最终润色
```

前一层未通过时，不应在后一层投入大量精修。特别是参考图模仿场景，主体版式未通过时不得把“修图例”当作主要优化。

### 3. 坐标域兼容性先检查，避免“同轴硬塞”

若两个视觉单元共享同一行/类别语义，但 x/y 属于不同数据域，例如：

- 左侧设施配置 tiles / metadata strips；
- 右侧 0–500 万元/年的连续 cost-gap；

不得通过负坐标、极端 `xlim` 或把类别 glyph 放到连续数值轴上硬拼。应使用**严格对齐的独立 axes、table+plot、metadata strip + numeric plot** 等方式，保持共享行语义，同时让每个坐标域使用自己的尺度。

这类问题应在写代码前通过 Figure Contract 的 `Axis-domain plan` 识别；不能等用户截图后再把它当作“间距问题”修补。

### 4. 复杂度预算：删重复，不删必要结构

`Less is more` 的含义是删除冗余视觉和重复证据，而不是把所有联合结构拆成普通单图。

- 单图已经闭合 Primary question 时优先单图；
- 两个证据单元强配对、共享行/轴语义、拆开会损失“结构 → 结果”的直接阅读关系时，可以保留 1×2、Composite Diagnostic 或一体化行式结构；
- “同一种图型尽量只出现一次”用于删除**同一证据的重复复述**，不是禁止必要 metadata/matrix/forest 再次出现；
- 高级图型必须提供不可替代的信息增益，不能只为了“高级感”增加 panel 数或视觉负担。

真正的“创意”来自信息结构，而不是图型名字的新奇度。

### 5. 颜色先冻结职责，再选择 Hex

不得因为用户提到 Nature / Science / Lancet / Cell，就机械套固定期刊色板。期刊色板、Set1/Dark2/viridis 等只作为候选起点。

先定义 Color Role Contract：

```text
Primary result / main trend
Risk / failure / interruption
Baseline / reference
Structural category
Context / inactive
Semantic background
```

再根据数据类型、方向语义、色盲/灰度可读性与已有 Figure 风格选择具体 Hex。一般遵守：

- 全图主色通常 3–5 种以内；
- 同一 panel 通常只保留一个主色、一个强调色和中性灰，但不是机械硬上限；
- 主数据与背景必须有明显明度差；
- 辅助对象、guide、背景、置信区间必须降权；
- 同一对象与方向性语义在全文保持同色；
- 禁止彩虹色和无序多色轮换。

### 6. 局部反馈默认局部修改

用户明确提出“只改某张 Figure / 只改主体 / 只改 legend / 这一张不要动”时，其他 Figure、panel 和已通过视觉层默认冻结。若修复当前问题必然联动其他层，必须在修改前说明依赖范围，不得静默扩大改动。

单轮 redraw 原则上只调整一个主要视觉层；避免同时更换图型、panel 数、配色、annotation、legend 与文件入口，否则下一轮无法判断改善来源。

### 7. 交付前做 Screenshot Preflight

代码静态通过不等于图审通过。每个候选版本交给用户前，必须按实际图窗尺寸做一次视觉预检，至少检查：

- 标题、panel title、坐标轴标题、脚注、legend 是否重叠；
- 数据标签是否压在线、点、空心圈或其他 glyph 上；
- 主体是否被压缩到局部、过松或密度失衡；
- metadata 与主图区是否距离过大；
- 4:3 / 3:2 / 16:9 等实际纵横比下阅读顺序是否稳定；
- 评委是否能在数秒内识别比较对象、主要差异与下一步该看哪里。

若 Screenshot Preflight 已明显失败，不应把该版本作为正式候选交给用户继续人工找错。

### 8. 多轮不收敛先诊断

同一 Figure 连续约 3 个 redraw round 仍未明显收敛时，下一步默认先停止继续编号出图，给出 Reference / Current mismatch diagnosis，至少检查：

- 主体骨架与纵横比；
- 信息密度与行/列间距；
- metadata 与主图区关系；
- 坐标域是否冲突；
- 颜色职责与视觉焦点；
- 点、线、带区间的比例；
- annotation 与 legend 是否抢占版心。

完成诊断后再只修最高优先级 mismatch。这里的“3轮”是升级诊断触发点，不是禁止继续修改的硬上限。

### 9. 接受即冻结，项目只保留 canonical 入口

用户明确说“通过 / 确定这一版 / 保留这个版本 / 不要再动”后，应立即：

1. 将对应 Figure / panel / visual layer 标为 accepted/frozen；
2. 把最终实现同步到项目唯一 canonical `问题X求解/qX_plot.m`；
3. 在 `模型论文框架.md` 或 project state 中记录接受状态、脚本路径和 SHA-256；
4. 从当前项目目录移除实验版 `.m`、重复 wrapper 和近似命名旧入口；实验历史若确有保留价值，只能放临时/归档位置，不得继续作为 active entry；
5. 后续只有用户显式 reopen 才允许修改被冻结内容。

## 数据前置条件

正式结果图优先读取本问 `问题X求解/` 中两个标准工作簿：

- `问题X求解结果.xlsx`：主结果、题型专项结果和主结果质量门；
- `问题X结果深化分析.xlsx`：分析设计、实际深化数据和结论稳定性汇总。

只有图本身确实需要底层事实源时，才继承当前 `preprocessing_decision` 追加数据：

- `not_needed`：允许读取必要原始数据；
- `question_local`：允许读取必要原始数据，但 MATLAB 不得重新构造局部模型变换；该变换若需图证据，必须由 Python 先把处理前后底层数据写入本问工作簿；
- `project_level`：需要公共底层数据时读取 `数据预处理结果.xlsx`，禁止绕回对应共享原始附件。

深化分析方法必须根据具体风险选择，可包括参数敏感性、阈值与失效边界、场景压力测试、多算法一致性、结构稳健性、异质性和误差分解。未执行某类分析时不得生成对应占位图；深化分析要求回退重算时不得继续绘图。

## MATLAB 规则

- 每问入口统一为 `问题X求解/qX_plot.m`；通用模板记为 `q{x}_plot.m`；
- 生成代码前确认真实工作簿名、工作表、表头、单位和数据类型；
- 字段定位采用精确表头唯一匹配，列号只作结构漂移警告；
- 禁止模糊匹配、别名猜测、自动回退和在 MATLAB 中重新求解；
- 布局必须通过 `modules/04_figure_evidence.md` 的 Figure Layout Gate 动态选择单图、1×2、2×1、1×3、2×2或拆图，不存在固定默认版式；
- 基础布局后按 Figure Enhancement Gate 判断是否需要 Local Zoom、Small Multiples、Focus Highlighting、Semantic Background、Composite Diagnostic 或 Conditional 3D；默认不增强；
- 一张 Figure 原则上只承担一个一级 Core conclusion / 一级阅读任务；不同 Evidence level 默认不混装，联合诊断等必要例外仍须共享同一 Primary question；
- 主比较允许中高饱和、高对比颜色，但必须服从当前 Figure 的 Color Role Contract；辅助对象、置信区间、背景和参考元素降饱和或降低透明度；
- 同一对象和方向性语义在全文保持同色；禁止彩虹色和无序多色轮换；
- 默认白底、清晰细轴、字号 18，网格关闭或极浅；
- 单图使用简洁 `title`，多面板使用一个整体 `sgtitle`；
- 默认只保留图窗，不创建图表子目录，不自动批量导出。

进入论文阶段后，人工确认并按需导出的正式图片放在项目级 `figures/`。每张图的结论、Evidence level、Primary question、布局判定、Enhancement 及理由、源工作簿、工作表、真实表头、脚本、图注和正文位置登记在 `模型论文框架.md`，不额外生成证据 YAML。

## 信息效率与删除规则

优先使用直接、低维和可比较的二维图。局部放大、分面、联合诊断和 3D 等增强只有在增加可验证信息、降低视觉搜索成本或强化关键证据时才保留。饼图、雷达图、3D 曲面和复杂网络图必须通过高级图表准入检查，并提供额外可验证信息，否则降级或删除。统一扰动模板、无通过标准、只说明“变化不大”、从摘要手工录入数据或无法支持正文判断的图全部删除。

## 机理图

机理图服务公式来源、约束来源、对象关系、临界状态和策略机制。图中只保留对象、变量、方向、边界、距离、角度和临界状态，完整解释放正文。禁止通用“输入—模型—输出”流程图替代题目专属图。
