# Figure Evidence 多轮返工复盘与防回归说明

> 本文是项目经验复盘，不是第二套绘图权威。正式绘图规则仍以 `modules/04_figure_evidence.md` 为唯一 Authority；本文只解释为什么一次 Q1 图审出现十余轮返工，以及后续执行时应如何利用现有 Figure Layout / Enhancement / QA 规则减少无效迭代。

## 1. 复盘背景

在一次供应链 Q1 Figure Evidence 图审中，主求解与结果深化分析均已验收，数据事实并不存在争议，但“结构稳健性”图仍连续经历多轮修改。问题主要不在 MATLAB 能否画出图，而在**视觉任务定义、参考图解析、反馈作用域、版本冻结与文件卫生**没有在生成代码前闭合。

这类返工会产生三个直接损失：

1. 图型、布局、配色、标注和图例同时变化，导致每轮无法判断究竟哪一个修改改善或破坏了结果；
2. 用户已经认可的部分可能被后续改动重新破坏，形成“越改越乱”；
3. 多个近似命名的 `.m` 文件并存，用户可能运行到旧版本，使图审失去共同事实基线。

## 2. 本次暴露出的主要问题

### 2.1 先追求“高级图”，后确认 Primary question

曾出现为了显得丰富而使用 1×2、Tornado、Local Zoom、inset 等表达，但其中部分并没有增加新的可判别信息。高级图型本身不是价值；只有当它降低搜索成本、揭示尺度压缩、阈值、异质性或结构关系时才有价值。

### 2.2 参考图只学了表层元素，没有先拆主体骨架

用户给出 Nature 风格哑铃图后，早期迭代先模仿了“空心点、实心点、图例”等局部元素，却没有优先识别参考图真正的视觉结构：

- 左侧名称列与窄 metadata strips 紧密对齐；
- 行距密集且统一；
- 右侧每行共享浅灰 guide；
- 灰色 transition 带为背景，空心点和实心点承担状态差异；
- 主体占据绝大多数版心，图例只在角落解释视觉编码。

因此出现“元素像了，但整体仍不像”的问题。

### 2.3 没有把“模仿风格”和“复制数据/语义”显式分开

参考图只能提供版式、视觉语法和配色启发；本题数值必须继续来自 accepted workbooks。若不在代码前明确 `imitate / preserve / do_not_copy`，很容易在布局层面过度照搬参考图中并不适用于当前数据的信息结构。

### 2.4 收到局部反馈后，修改范围过大

用户说“只改前两张”“只改结构稳健性”“主要改主体而不是图例”时，后续代码仍曾同时变化多个视觉层。局部反馈应默认只修改对应层，其他已经通过的层保持冻结。

### 2.5 没有按层级做 Figure Review

高效图审应按以下顺序推进：

```text
A. Figure role / 图型
→ B. 主体 geometry / 密度 / aspect ratio
→ C. 视觉编码（颜色、点、线、metadata）
→ D. 标注与标题
→ E. 图例
→ F. 最后润色
```

如果 B 尚未通过，就不应花大量时间修 E；否则图例修好了，主体仍会要求重画。

### 2.6 一轮同时改动太多变量

图型、panel 数、颜色、字号、图例、文件名一起变化，会让反馈失去因果性。一次反馈轮次原则上只应调整一个视觉层；若依赖关系要求联动，必须明确说明哪些元素被迫联动、哪些保持冻结。

### 2.7 没有及时冻结人工认可结果

一旦用户明确说“这张可以”“确定这个版本”“这部分不要动”，应立即记录：

- accepted/frozen 状态；
- canonical script；
- SHA-256；
- 被冻结的 Figure / panel / visual layer。

后续除非用户明确 reopen，不得再改。

### 2.8 文件命名和入口管理导致版本混淆

连续出现 `v8/v9/...`、wrapper、同名主脚本等文件，会让本地 MATLAB 路径命中旧文件。实验版本可以临时存在，但项目目录中应始终只有一个 canonical `qX_plot.m`。人工接受后立即把最终版同步为 canonical，旧实验脚本从当前项目目录清理。

### 2.9 缺少“多轮不收敛时先诊断”的升级机制

当同一 Figure 连续约 3 轮仍未收敛时，不应继续盲画下一版。应先暂停代码修改，给出 Reference / Current 的 mismatch table，指出：主体骨架、密度、比例、颜色职责、annotation、legend 哪一层不一致，再让下一轮修改只针对最高优先级 mismatch。

## 3. 后续 Figure Evidence 推荐执行法

### 3.1 参考图出现时，先写 Visual Contract

在生成 MATLAB 代码前先锁定：

```text
Primary question:
Figure role / Evidence level:
Reference purpose: layout / color / visual grammar / none
Must preserve:
Must imitate:
Do not copy:
Body geometry:
Density / aspect ratio:
Color roles:
Line / point hierarchy:
Annotation budget:
Legend placement:
Frozen existing figures / panels:
```

没有这个视觉合同，不进入参考图式重绘。

### 3.2 主体优先，图例后置

参考图对照顺序固定为：

1. 版心与 aspect ratio；
2. 行列结构与主体密度；
3. metadata 与主图区距离；
4. 点线比例、颜色职责；
5. 标注；
6. legend。

只有主体通过后才精修 legend。

### 3.3 局部反馈默认局部修改

若用户明确指出“只改 legend / 只改主体 / 只改 Figure 2”，则其余 Figure 与视觉层视为临时冻结。若必须联动，应在修改前解释依赖，不得静默扩大范围。

### 3.4 三轮不收敛先诊断

同一 Figure 约 3 个 redraw round 仍没有明显收敛时，下一步默认不是直接生成 v4，而是先输出 mismatch diagnosis。诊断通过后再继续绘图。

### 3.5 接受后立即冻结并清理

用户明确接受后：

```text
accepted Figure
→ 写入模型论文框架 / project state
→ 记录 canonical qX_plot.m + SHA-256
→ 标记 frozen visual scope
→ 删除当前项目中的实验版 .m / wrapper
→ 后续只有显式 reopen 才能修改
```

## 4. 本次最终经验

这次迭代说明，绘图质量瓶颈并不是“会不会更多高级图”，而是能否在代码前完成**证据任务定义 + 主体版式设计 + 参考图分解 + 冻结边界**。真正高级的 Figure 往往视觉语法更少，而不是更多；评委应在数秒内知道比较对象、主要差异和应该看哪里。

后续 Q2/Q3 Figure Evidence 应直接复用这套复盘结论，而不是重新从“先画一版再看”开始。