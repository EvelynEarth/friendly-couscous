# 论文语言、科研绘图与 XeLaTeX 视觉质量硬门（2026-10 实战修复）

> 这是跨题型的质量协议，不是某届获奖论文的仿制格式。最终遵从**当届官方**题面、论文格式公告与提交说明。

## 证据范围与获奖论文的用法
- 不得把已知 GitHub 路径/文件大小写成“已研读 16 篇”。每份 PDF 要实际可读取、记下**页码和具体验证点**，分别记录章节功能、方法动机、主要公式、有效图表、负面论证、视觉组织，再作为写作参考；无法获取正文时记 `unreviewed_access_blocked`，绝不假造论文规范或算法流行率。
- 优秀论文的安排只是可迁移的设计线索，不是对本届题意、科学有效性、获奖概率的证明。
- 对传统数学建模 TeX 模板，先审计 `cls/sty` 依赖、目录和摘要页、页码、匿名、参考文献、附录、图表、目录、命令编码、版权和兼容性，按大数据赛制重新配置。缺原模板时从最小 `ctexart` XeLaTeX 工作样例起步，绝不声称已经迁移原件。

## 中文论文硬门：先科学论证，再排版
- 每个实际子任务包含 **目标/输出 → 主要困难 → 数学变量及假设 → 选择该模型的理由与 baseline → 必要公式与求解 → 合法实验/反例 → 结论/适用边界**。共享方法集中叙述；禁止流水账代码说明、笼统“模型效果好”、堆模型缩写。
- 对摘要和正文每个量化主张查唯一 source metric、切分、结论范围；图表/表格必须被正文解释；失败实例不得删除。
- 中文术语统一，变量首次定义且单位明确，公式有可复算定义。引用来源可追溯，未经阅读的文献不写成论据。
- 至少一份独立学术语言审稿记录，逐段检查论证闭环、歧义、重复、过度宣称；审稿者必须记录具体页码/段落和应改句，不得单纯在 JSON 中填 passed。

## 科研图表硬门：数据证据 + 设计
每张图必须记录 `figure_id,source_data,source_sha256,script,experiment_id,scientific_question,finding,limitations,paper_section`，并实查：
1. 正确图型/刻度/坐标单位/时段/分组；禁止误导性截断坐标、隐瞒失败窗、把情景或移动平均画成已观测真值。
2. 彩色**默认优先**，采用色盲友好的少量语义色（例如蓝#0072B2、绿#009E73、橙红#D55E00、深灰#203047），好坏/基线/候选保持一致；不强制所有图有色，也不强制论文图纯黑白；官方颜色限制优先。
3. 不能单凭颜色分组：线型、marker、直接标注或图例辅助；灰度打印检查仍可判读。背景白、网格细、无无意义渐变/3D、中文字体嵌入、图中标签清楚且不与图题重复。
4. 导出 300 dpi 或可编辑矢量 PDF/SVG，以及真实论文引用的 PNG/PDF；图题与正文说明辨明历史数据、验证、预测和情景。**PDF 不会自动去色，黑白通常来自绘图脚本/转换设定**。

## 最终 TeX / PDF 硬门（Windows 11 + TeX Live）
- 交付至少 `main.tex`、真实引用的 `figures/`、所需 `cls/sty`（仅合法授权来源）、`README` 编译命令、参考文献（如用 BibTeX/biber）、重跑记录、**当前编译 PDF**。不依赖私有 Windows 盘符、在线下载字体、绝对路径、缺失图片或自定义 shell-escape。
- XeLaTeX 为中文首选；命令 `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`，或者 `xelatex` 连续两次。TeX Live 安装 `ctex`、`xeCJK`、`booktabs`、`geometry`、`graphicx` 等必需包；Windows `chcp 65001`，源文件和文件名 UTF-8。
- 实际编译必须返回 exit code 0；终审读取 .log，阻断 missing characters / undefined control sequence / unresolved references or citations / missing figures / serious overfull hbox；记录允许豁免的轻微 warning 与理由，不得删除 log 假装无警告。
- **每页渲染为图片**：逐页看公式是否截断、表格是否越界、页首尾孤行、标题/图题分离、大面积无意义留白、图内中文与色彩是否可读。记录 page_count、每页检查结论、问题所在页、修订后再渲染。PDF 存在不等于排版通过。
- 官方无格式说明时标记 unknown，不能用其他赛制常规冒充官方规则；正式 PDF 命名、目录位置、页码、匿名、页数、附录、代码、照片/签署材料以当届公告覆盖本模板。
- `paper / figures / final` 任一质量门失败时，回到相应上游更改正文、图表生成脚本或 TeX 源码，重新编译、复核与更新 Evidence Map；**不得只改 review JSON 通过机器门**。

## 2023 MathorCup 大数据竞赛真实官方格式案例（不是跨年度默认）
官方 2023 大数据竞赛格式（https://www.saikr.com/c/nd/14788 ，对应 PDF https://files.mathorcup.org/uploads/files/20231027/1698400522612279.pdf）要求：首页标题/摘要/关键词，第二页目录，正文从 1 编号、页脚居中、无页眉、匿名、中文、正文 30 页内；格式色彩不统一限制。附录写明程序，具体提交材料按官方要求。本案例的赛题结果表和论文是不同交付类，不能套普通 MathorCup 2023 数学建模竞赛另一个公告。


## v2.11.1 本次真实 PDF 反例与硬性复查

当前 2023 B 研究稿曾暴露：`\\caption{图1 ...}` 造成自动图号+手工图号双重输出；目录前独立写了“目录”又使用 `\\tableofcontents` 导致双标题；默认 Section 后首段未被明确纳入两字缩进策略；上下两级标题粗细、字距/留白接近，难以辨识；双面板图太小、图例和横轴标注压在一起；少量内容独占一页。**这些是已检查到的真实 TeX/版面错误，不是仅凭用户口味推断。**

实际修复应遵守以下可检验顺序：

1. 在需要的中文排版方案中声明 `\\setlength{\\parindent}{2\\ccwd}`、`\\setlength{\\parskip}{0pt}`、`\\usepackage{indentfirst}` 和 `\\ctexset{section/subsection={...,afterindent=true}}`；段落首行和标题后首段均抽样在最终渲染 PDF 中核查。**这是一套建议风格，而非2023大数据官方强制字号**。
2. 在标题相邻页面检查一级、二级标题的字号、对齐与段前段后；可选样式示例：一级居中黑体小三，二级左齐黑体四号，三级左齐黑体小四；每个比赛应先查本届官方模板，用户确认的风格优先。
3. 目录只用一次 `\\tableofcontents`（不要另外自己写一个“目录”标题），第一页摘要和目录不要出现正文页码，正文从1编，超链接 PDF 避免页锚点重复；图表 `\\caption{研究对象及发现}` **不手写“图1”“表2”**。
4. 用实际数据重新绘制图；当双面板缩小造成字号不足，优先改为**一图一项研究主张**。严格保持图表的事实数值、单位、误差与失败案例，彩色兼顾灰度；放入 PDF 后再次检查图例/轴标签/图题重叠、图中文字至少能在实际打印大小阅读。
5. 使用 `python skills/big-data-competition-skill/tools/latex_paper_audit.py --tex main.tex --pdf main.pdf --log main.log --profile bigdata2023` 检查具体源、图片、PDF 与日志。该工具拒绝几类确定性排版错误，返回 `preflight_passed_manual_review_required` 仍然**不能自动写 passed**；逐页看图和人审必须另做记录。对不适用此年度格式的赛题使用 `--profile generic`。

推荐示范：[修订 XeLaTeX 模板](../templates/bigdata-paper-xelatex/main.tex)。任何具体图表源码变动必须重新生成图、编译 TeX 并检查 PDF。奖项论文的 16 个元数据记录仍不是 16 篇已读正文。

 
## v2.12 本届可复核的获奖论文视觉对照证据
另见 [award-paper-empirical-layout.md](award-paper-empirical-layout.md)。原先“16篇只看文件名、大小”的说法已发生实质变化：通过 GitHub Actions 真实解析了全部16篇PDF的716页页面布局，48个页面抽样已视觉审阅；但**16篇全文学术论证审稿仍未完成**。正式作图/排版可用样本页作为具体观测，而不能据样本制定统一强制标题字号，也不能把机器布局抽取称为优秀论文写作质量认证。
