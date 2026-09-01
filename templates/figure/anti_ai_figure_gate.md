# Anti-AI Scientific Figure Gate（去 AI 味科研图硬门）

> 目的：专门拦截“看起来整洁，但像 AI 信息图 / 咨询 dashboard / PPT”的 Figure。  
> 适用：准备进入数学建模论文正文的 **Data Figure 与 Mechanism Figure**；二者允许的视觉元素不同，但都必须让科学对象/证据而不是装饰成为主体。

---

## 1. 为什么需要这道门

很多自动生成图会呈现下列共同特征：
- 大面积柔和 pastel 背景；
- 大标题 + 卡片 + 胶囊标签；
- 每个结论都用彩色文字喊出来；
- 四处强调、没有视觉主次；
- panel 机械等宽；
- 图看起来“精致”，但数据/机制主体反而小；
- 配色像产品 dashboard，而不是论文 Figure。

这些设计在演示稿/信息图中可能成立，但在科研正文中通常降低可信度、信息密度和可复现感。

---

## 2. AI Infographic Failure Signatures

任一项明显存在，默认 FAIL：

### 2.1 卡片化
- 圆角矩形包住结论；
- KPI 卡；
- “推荐 / 最优 / 改善”写成 badge / pill；
- 多个 annotation box 排成 dashboard。

### 2.2 Pastel washing
- 大面积浅蓝 / 浅紫 / 浅粉背景；
- 全图用 20–40% alpha 的大色块铺底；
- 背景色比数据/机制本身更有存在感；
- primary、secondary、context 同时被掺白到相近明度，导致整图“奶油化”；
- 为了“Nature 风”机械把所有颜色混入 70–85% 白色。

注意：**pastel washing 的修复不等于删掉颜色。** 若用户只反馈“颜色太浅 / 太 AI”，优先提高主色墨色、降低 white-mix、加深 context gray 或更换成熟 journal-inspired palette；不要擅自改 chart grammar。

### 2.3 Neon role drift
- 亮蓝 + 亮红 + 亮绿 + 亮橙同时出现；
- 同一语义跨 Figure 换色；
- 颜色只为“丰富”，没有数据/机制角色。

### 2.4 Title-heavy
- 顶部标题占据明显大块版心；
- `sgtitle + panel title + subtitle + annotation box` 同时存在；
- 标题字号远大于数据/对象，第一眼先读标题而不是证据。

### 2.5 Equal-grid template look
- 1×2 / 2×2 panel 机械等宽；
- supporting panel 明显数据更少却占同面积；
- panel 间 gap 过大，像网页卡片。

### 2.6 Text-as-data / text-as-mechanism
- 用大段文字解释本应由图直接显示的趋势或机制；
- 彩色文字代替 threshold / region / point / line / physical path；
- 每个点/柱都打数值标签，视觉变成“数字海报”；
- 机制图把“模型映射/公式解释/长段落”塞进大框，而真实对象流和反馈路径反而不清楚。

### 2.7 Decorative UI cues
Data Figure 默认禁止：
- 阴影；
- 发光；
- 渐变；
- emoji；
- ribbon header；
- dashboard 分隔卡；
- progress-bar 风格但没有真正比例语义。

Mechanism Figure **允许少量语义图标**，但必须满足：
- 图标直接对应真实对象/动作；
- 删除图标仍能完整读懂机制；
- 图标数量很少、风格统一、尺寸从属于节点与箭头；
- 不出现 icon wall、人物贴纸、营销插画堆叠。

图标一旦比路径/对象更抢眼，默认 FAIL。

---

## 3. Journal Replacement Patterns

遇到上面问题时，先判断当前 mutation scope，再选择修复：

| AI/PPT 症状 | Journal replacement |
|---|---|
| KPI 卡 | baseline line + direct annotation |
| pastel highlight card | 若允许 redesign：thin reference line / small region shading；若 `palette_only`：先提高 fill contrast/chroma |
| huge title | caption + short panel subtitle |
| multi-color dashboard | one primary + one secondary/adverse + context gray |
| equal 2×2 | hero + witnesses / asymmetric grid |
| every value labelled | only key extrema / threshold / optimum labelled |
| colored explanation text | encode with position / shape / region |
| infographic arrows | real mechanism path / flow / threshold / trajectory |
| long mechanism text boxes | short object/action labels + caption explanation |
| icon-rich mechanism | real objects + sparse labels + few semantic icons |
| big empty panel | reduce axis domain / combine with aligned metadata |

---

## 4. Data Figure vs Mechanism Figure

### Data Figure
第一视觉对象应是：数据模式、比较、边界、区间、残差或空间场。

允许较强的科研主色，只要颜色有稳定数据角色；高级 chart grammar 可以积极使用，但不能靠 UI 装饰制造“高级感”。

### Mechanism / Physical Figure
第一视觉对象应是：真实对象、作用方向、因果/状态路径、反馈、边界或物理关系。

默认更朴素：白底、黑/深灰主路径、至多一个风险/回流强调色；少字、少图标。具体工具/布局规则见 `mechanism_figure_contract.md`。

---

## 5. Paper-family Anchor Rule

如果用户明确指出某张图“有期刊味 / 这张可以 / 保留 / 这套颜色还行”，立即登记：

```text
paper_family_anchor
palette_anchor
```

后续 Figure 必须优先继承 anchor 的：
- font family；
- axis / connector weight；
- marker / node scale；
- primary / secondary / risk / context 颜色角色；
- sequential/diverging colormap family；
- panel/node gap；
- title weight；
- annotation density；
- whitespace rhythm；
- legend strategy。

**不得**每张 Figure 重新选择一套“Nature风 / Science风 / AI风”。继承的是视觉家族，不是把所有图都画成同一种 grammar。

用户只否定某一张图或某一种颜色时，默认局部迭代；不要无授权推翻整篇 palette anchor。

---

## 6. Mutation Scope Gate：先确认用户到底让你改什么

用户截图反馈后，先分类：

```text
palette_only
rendering_only
annotation_only
geometry_only
grammar_redesign
full_redesign
```

### `palette_only` 硬规则

若用户明确说：
- “只改配色”；
- “图不要动”；
- “这个图型还行，颜色不行”；
- “谁让你改这张图了，我只让你改颜色”；

则必须冻结：
- chart grammar；
- panel 数量；
- panel ratio；
- axis domain；
- 数据编码方式；
- annotation 内容；
- source data。

只允许修改：
- palette tokens；
- colormap；
- alpha；
- 因背景变化而必要的 text/marker-edge contrast；
- legend swatches。

若观察到结构问题，只能说明“另有结构建议”，不得在同一修改中偷偷实施。

详细规则见 `journal_palette_contract.md`。

---

## 7. 0.5 秒视觉分类测试

把 Figure 缩小到论文页大致尺寸，看 0.5 秒：

### PASS — Data Figure
- 第一眼先看到数据模式；
- 能判断 hero panel；
- 页面密度像论文；
- 没有 UI 卡片感；
- 配色稳定且克制，但不是被洗成一片浅色；
- 文字从属于数据。

### PASS — Mechanism Figure
- 第一眼先看到对象与路径；
- 主流/反馈/异常路径可区分；
- 没有大段文字和图标墙；
- 线条不穿框、不压字、不交叉；
- 图例（需要时）很短。

### FAIL — AI infographic
- 第一眼先看到颜色块 / 卡片 / 图标 / 标题；
- 看不出哪一个数据对象或机制路径最重要；
- 像咨询报告 / BI dashboard / 营销信息图；
- 看起来“漂亮”，但无法快速说出证据/机制是什么。

### FAIL — homework
- MATLAB 默认感；
- 图例 ping-pong；
- 粗糙 tick / title / spacing；
- 默认彩色折线；
- axes / legend / title 比例失调。

---

## 8. Color Restraint Test

把整图转灰度：
- 若主要结论消失 → FAIL；
- 若 primary 与 secondary 只能靠 hue 区分 → FAIL；
- 若风险/失效只靠红色文字表达 → FAIL。

类别图：color + marker / fill / line style 至少两种通道。  
连续图：使用 perceptually uniform colormap；不能用 qualitative palette 冒充连续梯度。  
机制图：主路径/异常/回流若使用颜色区分，线型/位置/图例至少再提供一种冗余语义。

此外还要检查**颜色面积**：同一 Hex 用在 marker、line、30% panel fill 上不是同一视觉重量。大面积 fill 需要单独审 saturation/alpha，但不得自动淡化到失去 contrast。

---

## 9. Annotation / Text Restraint Test

Data axes 统计：text objects、arrows、boxes、direct value labels。

一般情况下：
- 1–4 个 key annotations 合理；
- >6 个需要解释；
- >10 个默认 FAIL，除非本身就是 annotated matrix / forest label table。

Mechanism Figure 统计节点文本：
- 节点原则上 1–2 行短标签；
- 若长句/解释段落占据主体，FAIL；
- 完整推导与“模型映射”类说明优先移到 caption/正文。

若删除 50% annotation/text 仍不损失一级结论，应删。

---

## 10. Geometry Test

Data Figure 计算/目测：

```text
data body area / figure usable area
```

不是硬阈值，但：
- data body 明显 < 50% → 高风险；
- title + legend + note + white space 合计 > data body → FAIL；
- support panel 大面积为空 → 调整 panel ratio 或删除。

Mechanism Figure：
- connector crossing > 0 → FAIL；
- connector-through-node/text > 0 → FAIL；
- arrow overlap / ambiguous path > 0 → FAIL；
- 先改节点层级/路径 corridor，再考虑缩字体。

---

## 11. 禁止“靠风格救结构”，但也禁止越权重构

若用户只说：
- “丑”；
- “AI感”；
- “松散”；
- “不像期刊”；

而**没有指定修改范围**，先诊断：
1. chart/mechanism grammar；
2. hero / main-path hierarchy；
3. panel/node ratio；
4. axis domain / connector routing；
5. annotation/text burden；
6. legend tax；
7. typography；
8. color。

这时不能只靠换 palette 掩盖结构问题。

但若用户明确说“只改配色”，则 `Mutation Scope Gate` 优先：**不得以“结构也有问题”为理由擅自换图型。**

---

## 12. 最终交付声明

正式交付 Figure 时必须能回答：

```text
这张图为什么不像 AI 信息图？
- hero data object / main mechanism path 是什么？
- 哪些颜色有科学职责？
- 是否尊重本轮 mutation scope？
- palette provenance 是 official guideline / journal-inspired / scientific colormap 中哪一类？
- 是否存在 pastel washing / over-dark？
- 哪些 annotation/text/icon 被主动删掉？
- 是否通过灰度测试？
- 是否通过 drop test / mechanism closure？
- 是否在论文页尺度看过？
- 是否有任何线条穿框、压字或交叉？
```

答不上来 → 不得称为“最终科研图”。
