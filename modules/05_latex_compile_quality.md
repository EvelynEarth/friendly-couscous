# Module 05D：LaTeX 编译质量检查

本模块只处理已经完成 AI Cleanup 的 `latex_source`。正式入口统一为 `scripts/render_paper.py`：它先执行项目级 LaTeX 审计并生成 `latex_audit_report.yaml`，审计通过后才按当前 compile profile 编译，最终输出 `compiled_pdf` 与机器生成的 v3 `compile_report.yaml`。

跨版本布局收敛、Presentation Lock 和“已接受内容不能在后续编译中悄然消失”统一服从 `core/workflow_convergence_contract.yaml` 的 `latex_expected_artifact_gate`。因此“编译通过”只是必要条件，不等价于“当前 PDF 仍是完整有效版本”。

## 工程与配置

- Windows 工程放纯英文路径，项目主文件使用 Profile 的 `project_main`；
- 图片文件名使用英文或拼音；
- 编译链、仓库模板入口和最终项目入口以 `core/compile_profiles.yaml` 为唯一机器可读配置；
- 正式项目使用 `python scripts/render_paper.py final_latex --profile <name> --clean`；不得绕过项目审计后再手工伪造 compile report；
- 正式 `latex_audit_report.yaml` 必须绑定当前 active source bundle 与项目根目录 `模型论文框架.md` 哈希；源码或框架在审计后变化，审计证明立即 stale；
- v3 `compile_report.yaml` 必须绑定：正式审计报告哈希、compile-profile fingerprint、实际引擎/文献工具/执行序列、active source bundle hash、有效编译日志与 PDF hash；
- 缺少 `.log`、存在 fatal error、未解析引用/文献、审计证明失效时，`compile_report.status` 不得为 `passed`；
- 当前 `core/compile_profiles.yaml` 对所用 profile 的定义变化后，旧 PDF 的编译证明失效，必须重新编译；不能只依据源码未变继续复用旧 PDF；
- `--template-smoke` 仅供仓库模板 CI。该模式产生的 attestation 明确标记为 `template_smoke`，不得满足用户项目的正式交付门。

CUMCM 工程若尚未包含 `cumcmthesis.cls`，`render_paper.py` 从仓库已审计的上游 class 资源自动 materialize 到当前工程，并仅执行既有的窄范围、幂等字体回退补丁；不得要求用户靠隐藏的手工复制步骤才能进入正式编译。

## Expected Artifact Manifest

若当前项目已经接受或锁定了展示结构，在首次正式成稿或每次展示变更后建立轻量 expected-artifact manifest。它不是新的数值事实源，只记录“当前 PDF 必须仍包含什么”。至少按项目实际记录：

- 摘要分页策略；
- 一级/二级标题编号与已锁定命名；
- 正文必须出现的 Figure/表格 label；
- technical roadmap 是否启用及其位置；
- 附录是否先有三线文件说明表；
- 附录应包含的 canonical 求解/绘图代码；
- 是否要求代码高亮。

纯写作或排版修改不得擅自重置该 manifest。用户显式改变其中某项时，只更新受影响字段。

## 竞赛编译链

- CUMCM：XeLaTeX → Biber → XeLaTeX → XeLaTeX，日志应显示 `This is XeTeX`；
- MCM/ICM：pdfLaTeX → BibTeX → pdfLaTeX → pdfLaTeX，除非模板明确改为其他引擎；
- 电工杯中文模板：XeLaTeX → Biber → XeLaTeX → XeLaTeX；
- 未知竞赛先读取模板所用文献宏包与字体方案，再显式选择 profile；不得默认套用 CUMCM。

## 字体回退

Times New Roman 缺失时回退 TeX Gyre Termes；SimSun 缺失时回退 FandolSong。代码字体不得强制依赖某一台机器的 CJK 等宽字体。

## 编译故障处理

主文件名、路径、编译引擎变化，或 Biber/BibTeX/书签异常时，删除 `.aux .bcf .bbl .blg .run.xml .out .toc .lof .lot .log .synctex.gz` 后按 profile 完整重编译。

- `fontspec cannot-use-pdftex`：使用了依赖 `fontspec` 的模板，却实际调用 pdfLaTeX；
- `Wide character in die` 或 `.blg Invalid argument`：中文路径、主文件名或 Biber 编码异常；
- `No file main.bbl`、`Citation undefined`：先解决首次 LaTeX 或文献工具报出的首个错误；
- `I couldn't open database file`：检查 `.bib` 文件名、路径和 `\addbibresource`/`\bibliography`；
- `File ended while scanning use of \@writefile` 或书签错误：清理辅助文件并检查标题中的 `% # _ & { }` 与复杂公式。

## 终稿检查

先做机器编译与引用检查，再做 expected-artifact 与视觉检查：

1. 无 Error、未定义引用、缺失文献、缺图、字体错误、不可接受的 Overfull box 和表格越界；
2. 目录页码正确；摘要、图表、命题和附录编号正确；
3. 对照 current Presentation Lock / expected-artifact manifest，确认锁定的一级标题、编号方式、摘要分页、路线图位置、附录表与 canonical 代码仍在；
4. 对本次修改涉及的页面必须实际渲染/逐页目视检查，不得只看 `.tex` 或编译日志；
5. 若某张此前 accepted 的 Figure 在后续 LaTeX 改版中丢失，即使 PDF 无编译错误也判为 delivery regression，修复后重新生成审计/编译证明；
6. 正式交付时以 `latex_audit_report.yaml + compile_report.yaml + 当前 PDF` 的哈希证明链为机器证据，不以“文件存在”代替当前性检查。

PDF 必须逐页检查；当论文很长时至少保证所有改动页面、图表页、摘要页、章节边界和附录入口被人工检查，并由正式 review/delivery 模块补充全篇抽查或逐页审阅。
