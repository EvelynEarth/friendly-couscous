# Figure Evidence

每张正式图必须可追溯到真实数据或真实模型结果。

记录：
figure_id
source_data
script
analysis_question
finding
paper_location

## Preferred figure classes

- distributions
- relationships
- temporal trends
- spatial patterns
- model comparison
- ablation
- sensitivity
- error diagnostics
- prediction versus observation
- feature or variable interpretation

图表不要使用装饰性 3D、过度渐变、伪造平滑趋势或视觉重复。若离散数据没有连续观测，不得仅为好看而插值制造新结构。

## v2.11 从证据图到可发表视觉图

必须追加 [论文视觉与学术质量硬门](paper-visual-quality-gate.md)。除了证据来源真实，还要核对图种/轴/单位/时间、图中的研究问题、可读中文字体、正文实质解读、失败/反例是否被清楚呈现。默认允许并鼓励**审慎彩色科研图**：同一变量/方法跨图保持语义色，推荐蓝色基线、绿色经验证改善、橙色失败/风险，配合 marker/线型以便灰度打印。不得擅自把有色图全改灰；也不要把美观配色视为数据结论证据。科研绘图产物优先给 PNG(300dpi 或以上)、可编辑 SVG/PDF 与复现脚本，正式论文必须逐页核实引用结果。


### v2.11.1 在最终论文实际大小复核图例

图不只是单独 PNG 好看：实际 A4 页面缩放后审阅；图内若出现横轴标题与图例重合、彩色曲线缩到分辨不清、因双面板而字体过小，必须回到 Matplotlib/绘图脚本改变布局再导出，禁止靠 `\\includegraphics[width=...]` 无限制缩小来掩盖。源图中不另放“图3”标题，正文 caption 自动编号。推荐每图聚焦一条可证伪研究主张，失败窗口必须显示；同一张表和图若完全重复且不能提供独立理解则择其一。图像字体颜色与列宽是一组参数，应在实际 PDF 而不只源 PNG 中验证。

 
## v2.12 用实际论文样本反证“必须黑白”
[获奖PDF实证样本](award-paper-empirical-layout.md)已在2025-05第11页、2025-02第12页、2024-08第35页观察彩色散点图/蓝色模块/彩色机制图。说明**彩色完全可以是大数据竞赛论文的学术表达**，不表示有色必然美观或任何官方规范要求配色。设计自己的图要从实际数据与图示目的决定颜色、线型、尺度、信息密度，并在A4实际大小逐页核实。不能直接复制获奖原图、过度渐变或借奖项授权造假。
