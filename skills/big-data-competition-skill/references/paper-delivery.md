# Paper Delivery

本比赛 Skill 的最终成果是论文型项目交付。

## Delivery classes

### PDF-only

官方只要求论文 PDF 时，最终交付以当前编译 PDF 为准。

### Paper + source

若官方要求可编辑源文件，同时交付当前 source bundle 与 PDF。

### Paper + reproducibility

若官方要求代码、结果或复现材料，按官方通知构建对应目录，并校验版本一致性。

## Gate

正式交付前检查：

- current paper source
- compiled PDF
- accepted result artifacts
- figure and table provenance
- references
- no stale upstream dependency
- official format and rule evidence

不得根据 Kaggle 或其他平台经验自动扩展提交文件。

## v2.11 默认可编辑 LaTeX + 当前可视 PDF

若用户要求可编辑论文或未另作排他格式规定，在内部研究交付包提供 `main.tex`、真实图表/参考文献/必要授权样式文件、完整编译说明与日志、与源码一致的当前 PDF；Windows 11 + TeX Live 默认使用 `latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex`。这是内部可复现交付，不代表赛事平台必须上传 .tex。参阅 [模板](../templates/bigdata-paper-xelatex.md) 与 [质量硬门](paper-visual-quality-gate.md)。不能交付只有 PDF、没有源文件的所谓“可编译论文”。无当前编译验证时标记 `not_verified`，不得视为 delivered。官方规范与正式参赛提交永远优先。
