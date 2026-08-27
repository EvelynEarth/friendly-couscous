# Figure Suite Manifest（整篇论文图组架构表）

> 目的：在单图设计之前，先保证整篇论文的 Figure 不重复、不漂移、不变成“每张图各画各的”。  
> 适用：一个问题有 2 张以上 Figure，或整个论文进入 Figure Evidence 阶段时。

---

## 1. Figure Suite 表

| Figure ID | Question | Evidence level | One-sentence claim | Hero evidence | Visual grammar | Why unique in suite | Paper-family anchor | Manuscript position | Status |
|---|---|---|---|---|---|---|---|---|---|
| F1 |  |  |  |  |  |  |  |  | proposed |
| F2 |  |  |  |  |  |  |  |  | proposed |

---

## 2. Cross-Figure Grammar Registry

记录整篇论文已经使用的主视觉语法，避免无意识重复：

| Grammar | Used by | Primary task | Reuse allowed? | Reason |
|---|---|---|---|---|
| aligned forest |  | exact comparison | yes/no |  |
| regime map |  | threshold/boundary | yes/no |  |
| small multiples |  | complex traces | yes/no |  |
| network / flow |  | mechanism/flow | yes/no |  |
| distribution |  | uncertainty/spread | yes/no |  |

### 复用判定

允许复用同一 grammar，仅当：
1. visual task 相同；
2. 该 grammar 仍是最高效方案；
3. repetition 能强化 paper-family consistency；
4. 没有造成“整篇论文都是同一种图”的单调。

否则重新进入 Candidate Chart Pool。

---

## 3. Paper-family Style Registry

一旦某张 Figure 被用户明确认可为“有期刊味 / 这张可以 / 保留”，登记为 anchor：

```yaml
anchor_figure: ...
font_family: ...
review_font_scale: ...
axis_weight: ...
primary_marker: ...
primary_color_role: ...
risk_color_role: ...
context_gray: ...
panel_gap: ...
annotation_density: ...
legend_strategy: ...
whitespace_rhythm: ...
```

后续 Figure 默认继承这些“视觉职责”，不是机械复制图型。

---

## 4. Suite Redundancy Gate

两张 Figure 若出现以下情况，应合并/删减/换职责：
- 两张图的 claim 几乎一样；
- 数据相同，只换一种图型复述；
- supporting Figure 删除后正文没有任何损失；
- 两张图只是不同颜色或不同排序；
- L3/L4 证据抢走 L1/L2 正文视觉资源。

### 建议角色数量

正文一个问题常见：
- 1 个 L1 hero；
- 0–2 个 L2 mechanism/context；
- 0–1 个 L3 robustness；
- L4 numerical legality 优先附录，除非是结论可信度的核心。

不是硬限制，但超出时必须解释。

---

## 5. Figure Order Gate

正文 Figure 顺序优先形成：

```text
主结果（what）
→ 机制/解释（why）
→ 边界/稳健性（when/where it fails）
→ 数值合法性（why trust it，必要时附录）
```

禁止把稳定性、算法收敛图放在主结果之前，除非论文 Primary claim 本身就是方法学。

---

## 6. Suite-level Thumbnail Test

把所有正文 Figure 缩成同一页面的小缩略图并排：
- 是否明显属于同一个 paper family？
- 是否每张都有不同的证据职责？
- 是否某一张突然像 PPT / dashboard / AI 信息图？
- 是否某一张饱和度、标题、marker 大小明显失控？
- 是否一半 Figure 都是同一种 chart grammar？

任何一项失败，先在 suite 层调整，再继续单图微调。
