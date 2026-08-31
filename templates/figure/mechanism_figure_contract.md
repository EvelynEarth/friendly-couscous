# Mechanism / Physical Figure Contract

本合同只负责**机制图、机理图、场景结构图**的工具选择、稀疏表达与图面 QA；数值 Data Figure 的事实源、Evidence level、Layout/Enhancement、MATLAB 读取规则仍由 `modules/04_figure_evidence.md` 管理。

## 1. 先判断“该不该画”

机制图不是每问必需。只有满足至少一项时才画：

- 真实对象/空间关系仅靠正文难以快速恢复；
- 核心公式或约束来自一个可视化的物理/统计机制；
- 存在反馈、回流、状态转换、边界、受力、传播、几何或因果路径；
- 评委若看不到对象流/作用路径，会难以理解为什么建立当前模型。

若图只是把正文标题改成方框并连接 `输入 → 模型 → 输出`，判定 `not_needed`。

## 2. Tool Router

```text
mechanism / physical / scene figure
├─ 对象形态、空间关系、物理过程本身是理解重点
│  → image generation first
│  → 若中文/箭头/结构/AI味失败 → Draw.io
├─ 规则网络、状态机、流程/回流、需要精确中文与后续可编辑
│  → Draw.io first
└─ 纯数学几何且公式坐标控制比视觉叙事更重要
   → SVG/TikZ/GeoGebra/程序化矢量，按任务择优
```

MATLAB/Python **不是复杂机制图默认工具**。只有图本身就是坐标/几何/场数据或程序化矢量能明显提高准确性时使用。

## 3. Image Generation Gate

适合：物理机理、场景关系、设备/对象形态、空间传播、受力/运动等“看对象就能更快理解”的图。

默认 prompt 约束：

```text
plain white background
restrained scientific line-art
Chinese labels only when essential
sparse text
no marketing infographic
no pastel cards
no gradients
no shadows
no decorative UI
few or no icons
clear physical arrows
```

Image candidate 任一项失败，停止“继续换色/继续加提示词”，转 Draw.io 或矢量实现：

- 中文文字错误/乱码/漏字；
- 关键物理/因果路径缺失；
- 箭头方向错误；
- 长文字成为画面主体；
- 图标/装饰过多；
- 大面积 pastel、卡片化、AI infographic 味；
- 线、箭头与文字严重重叠；
- 用户需要精确可编辑结构。

Image generation 只能用于示意/机制，不得替代 accepted numerical data figure。

## 4. Draw.io Gate

适合：规则结构、决策门、反馈/回流、状态转换、技术路线、需要中文精确和 editable source 的图。

默认交付：

- editable `.drawio`；
- uncompressed XML：standalone `<mxGraphModel>` 或 `compressed="false"` wrapper；
- rendered preview（工具链允许时）。

XML preflight：

- root cells `id=0` / `id=1,parent=0` 完整；
- `mxCell` id 唯一；
- edge source/target 均存在；
- vertex/edge geometry 可解析；
- 不允许把 `.drawio` 只改扩展名冒充 XML；
- 中文字体显式优先本机可用 CJK 字体，如 Microsoft YaHei / SimSun；
- 结构验证通过不等于视觉通过，必须继续 preview/screenshot review。

## 5. Sparse Mechanism Design

### 5.1 文本预算

- 每节点原则上 1–2 行短标签；
- 节点写对象名/动作名/决策名，不写完整解释段落；
- 完整推导、长公式、参数清单、`模型映射`式大段说明移到 caption/正文；
- 删除一半文字仍不损失路径理解时，应删。

### 5.2 图标预算

- 默认 0–3 类少量语义图标；
- 图标只帮助识别对象，不能承担核心机制；
- 若删掉全部图标仍能完整读图，说明图标使用是健康的；
- 禁止 icon wall、emoji、装饰性人物/设备贴纸和营销信息图式图标堆叠。

### 5.3 配色

默认：

```text
background = white
main path = black / dark gray
context = gray
risk / return / adverse = at most one accent color
```

颜色只承担角色，不承担长文字解释。机制图默认比数值结果图更克制；不使用渐变、阴影、发光和大面积浅色卡片。

## 6. Layout Hard Gate

进入 review 前目标必须满足：

```text
connector crossing = 0
connector-through-node = 0
connector-through-text = 0
arrow overlap = 0
ambiguous reading order = 0
```

布线优先：

- 主流程走一条清晰主通道；
- 异常/不合格/反馈路径放独立 lane；
- feedback 预留外围或下方 corridor；
- Draw.io 优先 orthogonal connectors；
- 先移动节点/改变层级解决交叉，不靠缩小字体或加更多弯折“绕过去”；
- 箭头标签放在空白段，不压节点边界、箭头头部或其他标签。

若仍有交叉，candidate 不得称为 review-ready。

## 7. Legend Gate

当图中使用 **两种以上** 下列视觉编码表达不同语义时，必须有简短图例：

- 线型；
- 线色；
- 节点形状；
- 填充色；
- 特殊箭头类型。

图例只解释视觉语法，例如：

```text
矩形：对象/过程
菱形：决策
实线：主路径
虚线：异常路径
强调线：回流/反馈
```

图例不重复正文结论，不放长解释。

## 8. Mechanism Closure Review

最终检查：

1. 每条箭头都对应真实物理/统计/决策含义吗？
2. 模型依赖的输入、输出、反馈、出射、回流、观察路径是否实际画出？
3. 图能否解释“为什么建立这个模型/约束”，而不只是“模型有哪些模块”？
4. 0.5 秒是否先看到机制路径，而不是颜色、标题或文字块？
5. 删除 caption 后，读者能否恢复主要对象与因果/状态顺序？
6. 缩到论文插入宽度后，短标签仍可读吗？

任一核心机制只能靠图外大段文字补全时，说明图尚未闭合。

## 9. Candidate / Freeze

机制图同样服从：

```text
candidate → user visual review → accepted/frozen → canonical
```

每次结构性修改使用新 candidate/version，不覆盖上一版。用户明确接受后才冻结；纯字体/线宽小修若不改变 accepted 机制语义，可披露后修复 canonical。
