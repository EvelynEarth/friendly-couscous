# 大数据竞赛论文 XeLaTeX 源码（Windows 11 / TeX Live）

该模板对应通用`paper-first`研究论文，不预设赛题数量或方法；`main.tex` 可独立编译。**2023 MathorCup 大数据竞赛**的匿名首页、第二页目录、正文编号为一个明确可选的示例配置；其他赛事要核对当届规则并修改。

编译（TeX Live 命令行，项目目录内）：

```bat
chcp 65001
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

如果没有 `latexmk`，连续运行两次 `xelatex -interaction=nonstopmode -halt-on-error main.tex`。建议 TeX Live 完整安装或至少包含 ctex、xeCJK、geometry、graphicx、booktabs、amsmath、caption、hyperref、fancyhdr、setspace。仅用 UTF-8；用相对路径 `figures/` 放置来自真实实验的图片，推荐 PNG 高分辨率以及 PDF 矢量格式；本模板不含任何捏造的实验图。

检查：每页渲染 PDF，查看公式、三线表、图题、分页、字体和颜色；注意警告、缺失字符与严重 overfull，必须修复或解释后才验收。2023 规则来源：https://www.saikr.com/c/nd/14788。

交付：`main.tex`、图片/参考文献/辅助合法文件、编译日志与真实最新 PDF；按本届官方要求提交，不把 TeX 源文件自动视为必须向赛事平台上传。


## 2026-10 本次排版修复和实测范围

本模板明确区分一级居中黑体小三、二级左齐黑体四号、正文小四和首行 2 汉字宽；这是风格范例，不是大数据赛题官方强制字号。使用 `indentfirst` 和 `afterindent=true` 处理标题后的第一自然段；仅写一次 `\tableofcontents`，不要在 `\caption` 内手动补“图1/表1”。PDF 页锚点在目录/正文编号切换时关闭/重启，避免重复 page anchor。

命令行预检：
```bat
python skills/big-data-competition-skill/tools/latex_paper_audit.py --tex main.tex --pdf main.pdf --log main.log --profile bigdata2023
```
实际模板在你自己的论文目录下执行时，请将工具路径指向仓库。非 2023 赛制改用 `--profile generic`。机器预检通过仍必须逐页渲染检查，特别关注图例与横轴标签是否相互遮挡。


## v2.13.1 中文标题编号与目录一致性修复

针对当前用户的实际论文编辑意见，默认提供可改的**中文层级编号**：一级「一、」且黑体居中；二级「（一）」且黑体左齐；三级「1．」。通过 ctex `section.name/number` 等参数生成，不在每个 `\\section` 里手敲编号；目录与正文共用 counters，章节引用可复用。

这属于当前示范写作风格，不是2023或2026大数据竞赛官方强制编号；如当届赛规要求 `1 / 1.1`，可在源文件 `\\ctexset` 改回，检查器使用 `--heading-style unspecified`。需要当前用户所要求的中文分级时，使用 `python .../latex_paper_audit.py --heading-style chinese-tiered --tex main.tex --pdf main.pdf --log main.log` 并在 PDF 实际页面核验。不得只检查源码而不检查目录与正文。

 
## v2.13.2 用户指定五层样式（覆盖上一轮的默认风格）

已由当前用户把标题层次明确为：`一、`（一级章节）→ `1.1`（二级章节）→ `1.1.1`（三级章节）→ `（1）`（四级枚举）→ 实心圆点（五级分项）。模板 `main.tex` 包含真实可编译的五层样例，三级之后使用 `enumitem` 的 `enumerate/itemize`；数字来自 LaTeX 计数器，不能在章节正文里手写编号。以当前 PDF 目录和正文实测为准。

使用：`python skills/big-data-competition-skill/tools/latex_paper_audit.py --tex main.tex --pdf main.pdf --log main.log --profile bigdata2023 --heading-style chinese-mixed-five`。旧 `chinese-tiered` 仅作为兼容选项，不再是这位用户当前论文默认配置。
