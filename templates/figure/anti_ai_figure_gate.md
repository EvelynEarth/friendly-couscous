# Anti-AI Scientific Figure Gate（去 AI 味科研图硬门）

> 目的：专门拦截“看起来整洁，但像 AI 信息图 / 咨询 dashboard / PPT”的 Figure。  
> 适用：所有准备进入数学建模论文正文的结果图。

---

## 1. 为什么需要这道门

很多自动生成图会呈现下列共同特征：
- 大面积柔和 pastel 背景；
- 大标题 + 卡片 + 胶囊标签；
- 每个结论都用彩色文字喊出来；
- 四处强调、没有视觉主次；
- panel 机械等宽；
- 图看起来“精致”，但数据主体反而小；
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
- 背景色比数据本身更有存在感。

### 2.3 Neon role drift
- 亮蓝 + 亮红 + 亮绿 + 亮橙同时出现；
- 同一语义跨 Figure 换色；
- 颜色只为“丰富”，没有数据角色。

### 2.4 Title-heavy
- 顶部标题占据明显大块版心；
- `sgtitle + panel title + subtitle + annotation box` 同时存在；
- 标题字号远大于数据，第一眼先读标题而不是数据。

### 2.5 Equal-grid template look
- 1×2 / 2×2 panel 机械等宽；
- supporting panel 明显数据更少却占同面积；
- panel 间 gap 过大，像网页卡片。

### 2.6 Text-as-data
- 用大段文字解释本应由图直接显示的趋势；
- 彩色文字代替 threshold / region / point / line；
- 每个点/柱都打数值标签，视觉变成“数字海报”。

### 2.7 Decorative UI cues
- 阴影；
- 发光；
- 渐变；
- 图标；
- emoji；
- ribbon header；
- dashboard 分隔卡；
- progress-bar 风格但没有真正比例语义。

---

## 3. Journal Replacement Patterns

遇到上面问题时，不“微调颜色”，直接换成科研视觉语法：

| AI/PPT 症状 | Journal replacement |
|---|---|
| KPI 卡 | baseline line + direct annotation |
| pastel highlight card | thin reference line / small region shading |
| huge title | caption + short panel subtitle |
| multi-color dashboard | one primary + one adverse + context gray |
| equal 2×2 | hero + witnesses / asymmetric grid |
| every value labelled | only key extrema / threshold / optimum labelled |
| colored explanation text | encode with position / shape / region |
| infographic arrows | real mechanism path / flow / threshold / trajectory |
| big empty panel | reduce axis domain / combine with aligned metadata |

---

## 4. Paper-family Anchor Rule

如果用户明确指出某张图“有期刊味”，立即将其登记为 `paper_family_anchor`。

后续 Figure 必须优先继承 anchor 的：
- font family；
- axis weight；
- marker scale；
- primary / risk / context 颜色角色；
- panel gap；
- title weight；
- annotation density；
- whitespace rhythm。

**不得**每张 Figure 重新选择一套“Nature风 / Science风 / AI风”。

---

## 5. 0.5 秒视觉分类测试

把 Figure 缩小到论文页大致尺寸，看 0.5 秒：

### PASS
- 第一眼先看到数据模式；
- 能判断 hero panel；
- 页面密度像论文；
- 没有 UI 卡片感；
- 配色稳定且克制；
- 文字从属于数据。

### FAIL — AI infographic
- 第一眼先看到颜色块 / 卡片 / 标题；
- 看不出哪一个数据对象最重要；
- 像咨询报告 / BI dashboard；
- 看起来“漂亮”，但无法快速说出证据是什么。

### FAIL — homework
- MATLAB 默认感；
- 图例 ping-pong；
- 粗糙 tick / title / spacing；
- 默认彩色折线；
- axes / legend / title 比例失调。

---

## 6. Color Restraint Test

把整图转灰度：
- 若主要结论消失 → FAIL；
- 若 primary 与 secondary 只能靠 hue 区分 → FAIL；
- 若风险/失效只靠红色文字表达 → FAIL。

类别图：color + marker / fill / line style 至少两种通道。  
连续图：使用 perceptually uniform colormap；不能用 qualitative palette 冒充连续梯度。

---

## 7. Annotation Restraint Test

每个 axes 统计：
- text objects；
- arrows；
- boxes；
- direct value labels。

一般情况下：
- 1–4 个 key annotations 合理；
- >6 个需要解释；
- >10 个默认 FAIL，除非本身就是 annotated matrix / forest label table。

若删除 50% annotation 仍不损失一级结论，应删。

---

## 8. Geometry Test

计算/目测：

```text
data body area / figure usable area
```

不是硬阈值，但：
- data body 明显 < 50% → 高风险；
- title + legend + note + white space 合计 > data body → FAIL；
- support panel 大面积为空 → 调整 panel ratio 或删除。

---

## 9. 禁止“靠风格救结构”

如果用户评价：
- 丑；
- AI感；
- 松散；
- 不像期刊；

首先诊断：
1. chart grammar；
2. hero/witness hierarchy；
3. panel ratio；
4. axis domain；
5. annotation burden；
6. legend tax；
7. typography；
8. 最后才是 color。

禁止先换 palette。

---

## 10. 最终交付声明

正式交付 Figure 时必须能回答：

```text
这张图为什么不像 AI 信息图？
- hero data object 是什么？
- 哪些颜色有科学职责？
- 哪些 annotation 被主动删掉？
- 是否通过灰度测试？
- 是否通过 drop test？
- 是否在论文页尺度看过？
```

答不上来 → 不得称为“最终科研图”。