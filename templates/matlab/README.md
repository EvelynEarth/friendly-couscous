# HSK MATLAB 科研绘图模板（当前活动模板）

MATLAB 只读取 Python 两阶段输出的标准工作簿，不重新求解。每问唯一入口通用记为 `q{x}_plot.m`，与主求解/深化分析脚本及工作簿同处 `问题X求解/`。禁止 `q1_polt.m`、`final_plot_new.m` 等拼写变体和并行 active 入口。

本模板现在不是“另起一套顶刊风格”，而是**原 HSK 绘图规范 + 高级期刊 Figure Evidence 方法的融合实现层**。

融合关系：

```text
原 HSK / 项目规则（保留为底座）
- 中文可读性与 review 字号
- MATLAB 只绘图、不重求解
- 标准工作簿 / 真实表头 / 单位
- Figure Layout Gate
- Figure Enhancement Gate
- q{x}_plot.m 单一入口
- 模型论文框架证据闭环

        +

高级期刊 Figure 方法（吸收为上层质量门）
- Dataset + Claim
- Graphical Perception
- >=3 visual grammars + candidate scoring
- hero / witness + drop test
- Nature-style space-efficient geometry
- paper-family anchor
- Anti-AI gate
- real-data render-review
- embedded-paper QA
- state / freeze / release control

        ↓

统一执行于本 MATLAB 模板
```

因此：**高级期刊 Skill 不覆盖原 HSK 规则，而是在原规则上增加选型、版式、视觉层级、迭代收敛和论文页 QA。**

高阶科研绘图流程同时读取：
- `modules/04_figure_evidence.md`（原项目 Figure 决策权威）
- `templates/figure/top_tier_scientific_figure_skill.md`（顶刊级 Figure 方法）
- `templates/figure/figure_iteration_control.md`（scope / version / release / freeze 状态机）
- `templates/figure/anti_ai_figure_gate.md`（去 AI/PPT/dashboard 味硬门）
- `templates/figure/figure_failure_postmortem_2026-08.md`（有历史返工时强制读取）
- `templates/figure/journal_figure_research_notes.md`（外部方法论研究）
- `templates/figure/result_figure_qa.md`（最终 QA）

---

## 1. 路径与真实数据源

```matlab
scriptPath = string(mfilename("fullpath"));
resultDir = string(fileparts(scriptPath));
solutionBook = fullfile(resultDir, "问题一求解结果.xlsx");
resultAnalysisBook = fullfile(resultDir, "问题一结果深化分析.xlsx");
```

主结果图读取 `solutionBook`；稳定性、阈值、算法或结构图读取 `resultAnalysisBook`。不得跨问题读取临时 Excel、根据摘要数字反推数据或在 MATLAB 中重算核心结果。

字段定位采用精确表头唯一匹配。允许登记期望列号作为结构漂移警告，禁止模糊匹配、别名猜测、相似字段回退和自动改变语义映射。

---

## 2. 两种尺寸概念必须分开

### A. Review Profile（默认）

用于用户直接在 MATLAB 图窗和截图中审查。这里**不能机械复制 Nature 最终 5–7 pt production 字号**。

当前中文 review baseline：

```text
axes / tick / axis label ≈ 16–18
legend                  ≈ 14–16
panel label / subtitle  ≈ 18–22
line width              ≈ 1.2–1.6
```

模板辅助函数 `hsk_apply_scientific_style` 默认以此 profile 工作。

### B. Final Paper Profile

只有 Figure 已 accepted 后才进入：
1. 按论文实际栏宽导出；
2. 嵌入 Word / LaTeX / PDF；
3. 在整页尺寸检查，而不是只看 standalone PNG；
4. 若缩放后字太小，优先增加图占版、删冗余、调整 panel 比例；最后才继续减字号。

Nature / Science 等期刊的生产宽度和字号只用于 reduction test，不直接覆盖 Review Profile。

---

## 3. Figure Layout Gate

正式绘图前按 `modules/04_figure_evidence.md` 动态决定单图、1×2、2×1、1×3、2×2 或拆图。

判定顺序：

```text
单图能闭合核心结论 → 单图
否则两个证据强配对/互补 → 1×2 或 2×1
否则三个证据构成不可拆序列 → 1×3
否则四个 panel 同时满足 2×2 保留条件 → 2×2
否则 → 按 Primary question / Evidence level 拆图
```

### 顶刊几何补充

- panel 紧凑，但不机械等宽；
- panel 大小按信息密度和标签需求决定；
- `tiledlayout(...,'TileSpacing','compact','Padding','compact')` 是常用起点，不是等宽强制；
- 一个 8×10 参数矩阵和一条阈值切片可以采用 2:1 / 3:1 span；
- axis 范围不应远超数据，除非该空域承载真实阈值/可行域；
- common axis label / common legend 能共享时不重复；
- 先最大化数据主体，再决定标题、legend 和 annotation 的空间。

**禁止：**
- 大标题 + 小主体；
- 两 panel 信息量明显不同却机械 50/50；
- 为“呼吸感”保留大面积无意义白区；
- legend 放在外部导致主体被压缩到半幅。

---

## 4. Figure Enhancement Gate

基础图型和布局确定后，按 `modules/04_figure_evidence.md` 判断是否启用 Local Zoom、Small Multiples、Focus Highlighting、Semantic Background、Composite Diagnostic 或 Conditional 3D。

默认 `Enhancement=none`。只有增强后能增加可验证信息、降低搜索成本或强化关键证据时才使用。

高级图型不是加分项本身：
- ternary 若数据几乎共线或一项基本常数，降级；
- Sankey/alluvial 只有真实流量/守恒关系时使用；
- 3D 只有第三维不可替代时使用；
- 单个数字/单根柱通常进入正文或 callout，不单占 Figure。

---

## 5. 标题、panel label 与 caption 分工

### Review / competition mode

允许简洁中文整体标题，但：
- title 不得和 panel subtitle / caption 重复；
- title 的高度不能明显挤压主体；
- multi-panel 优先 `a / b / c` + 短 subtitle。

### Journal mode

优先把正式 Figure title 放 caption；图内只保留 panel label 和必要 subtitle。

调整顺序固定：

```text
缩短 title
→ 删除重复 title
→ 把解释移到 caption
→ 调整 figure height
→ 最后才减字号
```

---

## 6. 风格与颜色职责

- 白底；
- grid 默认关闭，除非网格本身有读数价值；
- `TickDir='out'` 或清晰轻轴；
- 中文坐标轴和单位完整；
- 同一对象/语义跨全文颜色一致；
- 颜色先定义职责，再选 Hex。

默认角色：

```text
Primary / recommended → 1 个主色
Risk / failure        → 1 个 adverse 色
Baseline / context    → 中性灰 / 低饱和
```

主色不是固定 Nature/Science 色板。`hsk_apply_scientific_style.m` 只提供**非霓虹、可打印的起点**，问题脚本仍按 Figure Contract 调整。

若已有用户认可的 `paper_family_anchor`，本问优先继承其：font family、stroke weight、marker scale、颜色职责、annotation density、panel gap 与 whitespace rhythm；不得重新发明一套“期刊配色”。

禁止：
- rainbow / jet；
- 红绿作为唯一差异；
- 每个指标一支艳色；
- 大段彩色文字；
- 阴影、渐变、无意义 3D；
- 全图同时高饱和。

---

## 7. Render–Review–Iterate（正式交付硬门）

绘图代码写完 ≠ Figure 完成。

在正式 `q{x}_plot.m` 生成前：

```text
scope lock
→ accepted workbook
→ Dataset + Claim
→ >=3 visual grammars + scoring
→ Python/Matplotlib 真实数据视觉原型
→ render PNG
→ body geometry review
→ redesign if needed
→ second render
→ hierarchy / labels / color review
→ Anti-AI / grayscale / clipping sanity
→ release candidate gate
→ MATLAB translation
```

用户本地 MATLAB 截图回来后：
- 先做 implementation fidelity review；
- 只修 MATLAB renderer 导致的字号、间距、legend、label、axes extent；
- 未显式 reopen 时，不重新发明图型。

连续约 3 轮仍未收敛：停止出 vN，先做 Reference / Current mismatch diagnosis。

**用户不是第一层 linter。** 未通过内部 real-data render-review 与 release gate，不向用户交付所谓“最终 `.m`”。

---

## 8. Version / Freeze / Naming

Provisional 用户交付必须使用唯一新文件名：

```text
qX_plot_vNN_<short-note>.m
```

不得覆盖上一版，不得“名字新、内容旧”。

用户明确“确定 / 通过 / 冻结”后，才生成：

```text
qX_plot.m
```

作为 canonical active entry，并记录 accepted source version、commit/hash、frozen Figure IDs 与 `paper_family_anchor`。

已 frozen Figure 如需换图型、证据职责或重新配色，必须先显式 `REOPEN reason=...`。

---

## 9. MATLAB Preflight

交付前同时过两层检查。

### Semantic preflight
- 工作簿、Sheet、Required headers 真实存在；
- 单位与比例口径正确；
- 不调用求解器；
- 不写 Excel；
- assert 只验证当前 accepted contract，不保留旧版本 stale assumption；
- 离散扫描不擅自插值/平滑。

### Lexical / compatibility preflight
- 扫描不可见 Unicode、NBSP、smart quote、smart dash；
- 禁止非法复制字符进入 MATLAB 语法位置；
- 避免中文表头点索引；
- 检查函数/变量名冲突；
- 文件名与内部版本一致。

---

## 10. 图窗与导出

默认：
- 保留可见图窗；
- 不自动关闭；
- 不自动创建图表子目录；
- 不批量导出。

论文阶段人工确认后，按需导出到项目级 `figures/`，并执行 embedded-paper reduction test。

每张图的源工作簿、工作表、真实表头、脚本、图注、Evidence level、Primary question、Layout decision、Split decision、Enhancement / rationale 和正文位置同步登记到 `模型论文框架.md`。

图表交付前执行：

```text
python scripts/sync_project.py <project_root> --write --strict --delivery-scope figures
```

同步器检查工作簿、`qX_plot.m` 的真实引用、标题和证据链；默认不要求导出图片已经存在。