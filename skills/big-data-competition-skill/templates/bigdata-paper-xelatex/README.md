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
