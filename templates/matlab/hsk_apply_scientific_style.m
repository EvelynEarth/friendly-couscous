function palette = hsk_apply_scientific_style(fig)
% HSK 中文科研图 Review Profile。
%
% 目标：
% - 供 MATLAB 图窗 / 截图直接审查，不机械复制期刊最终 5–7 pt production 字号；
% - 默认 axes=18, legend=16, linewidth=1.4；
% - grid 关闭、tick outward、无装饰阴影；
% - 返回 role-based、非霓虹的科研配色起点。
%
% 注意：
% - 本函数只负责基础 style，不负责 panel geometry、chart selection 或数据语义；
% - 最终论文尺寸需在 figure accepted 后单独做 embedded-paper reduction test。

arguments
    fig (1,1) matlab.ui.Figure = gcf
end

fontName = hsk_select_font();
set(fig, "Color", "w");

axesList = findall(fig, "Type", "axes");
for ax = reshape(axesList, 1, [])
    set(ax, ...
        "FontName", fontName, ...
        "FontSize", 18, ...
        "LineWidth", 1.4, ...
        "Box", "off", ...
        "Layer", "top", ...
        "TickDir", "out");
    grid(ax, "off");

    if isprop(ax, "Title") && isgraphics(ax.Title)
        set(ax.Title, ...
            "FontName", fontName, ...
            "FontSize", 20, ...
            "FontWeight", "bold", ...
            "Color", [38, 43, 49] / 255);
    end

    if isprop(ax, "XAxis") && isgraphics(ax.XAxis)
        set(ax.XAxis, "FontName", fontName);
    end
    if isprop(ax, "YAxis") && isgraphics(ax.YAxis)
        set(ax.YAxis, "FontName", fontName);
    end
end

% tiledlayout 的 sgtitle / panel text 只统一字体，不擅自改变内容或位置。
textList = findall(fig, "Type", "text");
for txt = reshape(textList, 1, [])
    if isprop(txt, "FontName")
        set(txt, "FontName", fontName);
    end
end

legendList = findall(fig, "Type", "legend");
for lgd = reshape(legendList, 1, [])
    set(lgd, ...
        "FontName", fontName, ...
        "FontSize", 16, ...
        "Box", "off");
end

colorbarList = findall(fig, "Type", "colorbar");
for cb = reshape(colorbarList, 1, [])
    set(cb, ...
        "FontName", fontName, ...
        "FontSize", 16, ...
        "LineWidth", 1.2, ...
        "Color", [74, 81, 89] / 255);
end

% -------------------------------------------------------------------------
% Role-based palette：不是固定 Nature/Science 色板。
% 颜色只作为项目脚本的“语义起点”；若 Figure Contract 有更合适的职责映射，脚本可覆盖。
% -------------------------------------------------------------------------
palette.primary = [48, 96, 130] / 255;       % #306082, 主结果/推荐方案
palette.secondary = [74, 126, 119] / 255;    % #4A7E77, 第二结构色
palette.risk = [178, 76, 62] / 255;           % #B24C3E, 风险/失效/阈值
palette.warning = [201, 139, 55] / 255;       % #C98B37, 必要的警示/边界
palette.baseline = [116, 124, 132] / 255;     % #747C84, 基准/上下文
palette.context = [216, 220, 223] / 255;      % #D8DCDF, 降权背景
palette.ink = [38, 43, 49] / 255;             % #262B31, 文字/主轴
palette.lightGray = [236, 238, 240] / 255;    % #ECEEF0
palette.fontName = fontName;

% 可访问性建议：
% - 不默认给出 red/green 对照；
% - Primary / risk 应同时通过位置、线型、marker 或填充区分；
% - 连续值不要直接使用这些离散语义色，另选单调 sequential / diverging map。

% 兼容旧脚本字段名，但映射到当前非霓虹 role palette。
palette.brightBlue = palette.primary;
palette.vividRed = palette.risk;
palette.brightGreen = palette.secondary;
palette.brightOrange = palette.warning;
palette.brightPurple = [110, 92, 143] / 255;
palette.darkGray = palette.ink;

palette.deepBlue = palette.primary;
palette.midBlue = palette.primary;
palette.teal = palette.secondary;
palette.darkRed = palette.risk;
palette.purple = palette.brightPurple;
palette.beige = palette.lightGray;
end

function fontName = hsk_select_font()
preferred = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", ...
    "Arial Unicode MS", "Helvetica", "Arial"];
available = string(listfonts);
fontName = "Helvetica";
for candidate = preferred
    if any(strcmpi(available, candidate))
        fontName = candidate;
        return;
    end
end
end
