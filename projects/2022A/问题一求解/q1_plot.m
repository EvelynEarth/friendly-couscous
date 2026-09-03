%% q1_plot：2022A 问题一 Figure Evidence
% 只读取已验收的“问题一求解结果.xlsx”和“问题一结果深化分析.xlsx”。
% 不重新求解 ODE，不重新构造模型，不修改工作簿。
%
% Figure Q1-1 (L1 主结果证据)：
%   2×2 时程小多图，比较常阻尼与幂律阻尼下浮子/振子的位移和速度；
%   采用同一客观 ROI 的 Embedded Local Zoom，并用浅色带标出两曲线间差异。
% Figure Q1-2 (L3 稳健性证据)：
%   1×2，左图为第35-39周期重复性最大相对偏差及2%阈值，
%   右图为两种阻尼稳态指标的相对差异。
%
% 默认仅保留图窗供人工检查，不自动导出图片。

clearvars;
clc;

%% 1. 路径与工作簿
scriptPath = string(mfilename("fullpath"));
assert(strlength(scriptPath) > 0, "请从已保存的 q1_plot.m 运行脚本");
resultDir = string(fileparts(scriptPath));
solutionBook = fullfile(resultDir, "问题一求解结果.xlsx");
analysisBook = fullfile(resultDir, "问题一结果深化分析.xlsx");
assert(isfile(solutionBook), "缺少工作簿: %s", solutionBook);
assert(isfile(analysisBook), "缺少工作簿: %s", analysisBook);

solutionSheets = string(sheetnames(solutionBook));
analysisSheets = string(sheetnames(analysisBook));
assert(any(solutionSheets == "仿真明细"), "主工作簿缺少‘仿真明细’");
assert(any(solutionSheets == "核心指标"), "主工作簿缺少‘核心指标’");
assert(any(analysisSheets == "误差分解"), "深化工作簿缺少‘误差分解’");
assert(any(analysisSheets == "稳态结构差异"), "深化工作簿缺少‘稳态结构差异’");

%% 2. 读取主结果长表
mainRaw = readcell(solutionBook, "Sheet", "仿真明细");
mainHeaders = strtrim(string(mainRaw(1, :)));
colScenario = exact_header_column(mainHeaders, "场景");
colTime = exact_header_column(mainHeaders, "时刻");
colValue = exact_header_column(mainHeaders, "数值");
colState = exact_header_column(mainHeaders, "状态量");

scenarioConstant = "常阻尼c=10000";
scenarioNonlinear = "幂律阻尼a=10000,n=0.5";
stateLabels = ["浮子位移", "振子位移", "浮子速度", "振子速度"];

[tConst, yConst] = collect_state_series(mainRaw, colScenario, colTime, colValue, colState, scenarioConstant, stateLabels);
[tNonlin, yNonlin] = collect_state_series(mainRaw, colScenario, colTime, colValue, colState, scenarioNonlinear, stateLabels);
assert(isequal(tConst, tNonlin), "两种阻尼情形的时间网格不一致");
assert(numel(tConst) == 898, "仿真明细输出点数不是898");
wavePeriod = read_scalar_metric(solutionBook, "核心指标", "波浪周期T");
assert(isfinite(wavePeriod) && wavePeriod > 0, "波浪周期T异常");

%% 3. 科研绘图角色色与基础样式
palette.primary = [48, 96, 130] / 255;      % 常阻尼
palette.secondary = [178, 76, 62] / 255;   % 幂律阻尼
palette.baseline = [116, 124, 132] / 255;
palette.context = [236, 238, 240] / 255;
palette.ink = [38, 43, 49] / 255;
palette.risk = [178, 76, 62] / 255;
palette.zoomBand = [225, 229, 232] / 255;  % 主图 ROI 语义背景
palette.gapFill = [201, 139, 55] / 255;    % inset 两曲线间差异带
fontName = select_font();

%% 4. Figure Q1-1：完整时程 + 客观局部放大（L1）
% Core conclusion：两种阻尼均由初始瞬态逐步进入有界周期响应，
% 但瞬态轨迹和稳态量值并不完全相同。
%
% Local Zoom 规则：
% 1) 四个状态量先分别按自身全时域响应范围无量纲化差值；
% 2) 对四项无量纲差值取 RMS，得到共同“分离度”评分；
% 3) 自动选择评分最大的时刻，并以其为中心取 2.5 个波浪周期宽度；
% 4) 四个 panel 使用同一个 ROI，避免人为挑选对结论有利的局部。
[zoomX, zoomMask, zoomCenter] = difference_focus_window(tConst, yConst, yNonlin, wavePeriod);

fig1 = figure("Color", "w", "Position", [80, 70, 1240, 850], "Name", "Q1-L1 主结果");
tl1 = tiledlayout(fig1, 2, 2, "TileSpacing", "compact", "Padding", "compact");
sgtitle(tl1, "两种阻尼下浮子—振子垂荡响应及差异局部放大", "FontWeight", "bold");

panelTitles = ["浮子位移", "振子位移", "浮子速度", "振子速度"];
yLabels = ["位移 / m", "位移 / m", "速度 / (m·s^{-1})", "速度 / (m·s^{-1})"];
deltaUnits = ["m", "m", "m/s", "m/s"];
axesList = gobjects(4, 1);
legendHandles = gobjects(2, 1);
for k = 1:4
    ax = nexttile(tl1, k);
    axesList(k) = ax;
    hold(ax, "on");
    h1 = plot(ax, tConst, yConst(:, k), "LineWidth", 1.55, "Color", palette.primary, "LineStyle", "-");
    h2 = plot(ax, tNonlin, yNonlin(:, k), "LineWidth", 1.45, "Color", palette.secondary, "LineStyle", "--");
    yline(ax, 0, ":", "Color", palette.baseline, "LineWidth", 0.8, "HandleVisibility", "off");
    xlim(ax, [tConst(1), tConst(end)]);
    xlabel(ax, "时间 / s");
    ylabel(ax, yLabels(k));
    title(ax, panelTitles(k), "FontWeight", "normal");
    box(ax, "off");
    grid(ax, "off");
    if k == 1
        legendHandles = [h1; h2];
    end
end
legend(axesList(1), legendHandles, ["常阻尼 c=10000", "幂律阻尼 a=10000, n=0.5"], ...
    "Location", "northoutside", "Orientation", "horizontal", "Box", "off");
apply_style(fig1, fontName, palette.ink);
drawnow;

% 在四个主 panel 上标记同一 ROI，再放置嵌入式局部放大图。
for k = 1:4
    ax = axesList(k);
    yl = ylim(ax);
    roi = patch(ax, ...
        [zoomX(1), zoomX(2), zoomX(2), zoomX(1)], ...
        [yl(1), yl(1), yl(2), yl(2)], ...
        palette.zoomBand, ...
        "FaceAlpha", 0.24, "EdgeColor", palette.baseline, "LineStyle", "--", ...
        "LineWidth", 0.75, "HandleVisibility", "off");
    uistack(roi, "bottom");
    ylim(ax, yl);

    add_local_zoom(fig1, ax, tConst, yConst(:, k), yNonlin(:, k), zoomMask, zoomX, ...
        palette, fontName, deltaUnits(k), k);
end

% 只给一个轻量说明，避免四个 panel 重复标注。
annotation(fig1, "textbox", [0.62, 0.935, 0.33, 0.035], ...
    "String", sprintf("灰色带：自动最大分离区间，中心 t = %.1f s", zoomCenter), ...
    "EdgeColor", "none", "HorizontalAlignment", "right", ...
    "FontName", fontName, "FontSize", 10.5, "Color", palette.baseline);

%% 5. 读取深化分析证据
errRaw = readcell(analysisBook, "Sheet", "误差分解");
errHeaders = strtrim(string(errRaw(1, :)));
errMetricCol = exact_header_column(errHeaders, "指标");
errValueCol = exact_header_column(errHeaders, "数值");
errGroupCol = exact_header_column(errHeaders, "分组");
errMetric = strtrim(string(errRaw(2:end, errMetricCol)));
errGroup = strtrim(string(errRaw(2:end, errGroupCol)));
errValue = cell_to_numeric(errRaw(2:end, errValueCol));
validErr = strlength(errMetric) > 0 & strlength(errGroup) > 0 & isfinite(errValue);
errMetric = errMetric(validErr);
errGroup = errGroup(validErr);
errValue = errValue(validErr) * 100;  % %
assert(numel(errValue) == 8, "误差分解应包含8个末5周期重复性指标");

steadyRaw = readcell(analysisBook, "Sheet", "稳态结构差异");
steadyHeaders = strtrim(string(steadyRaw(1, :)));
steadyMetricCol = exact_header_column(steadyHeaders, "指标");
steadyDiffCol = exact_header_column(steadyHeaders, "相对差异");
steadyMetric = strtrim(string(steadyRaw(2:end, steadyMetricCol)));
steadyDiff = cell_to_numeric(steadyRaw(2:end, steadyDiffCol));
validSteady = strlength(steadyMetric) > 0 & isfinite(steadyDiff);
steadyMetric = steadyMetric(validSteady);
steadyDiff = steadyDiff(validSteady) * 100;  % %
assert(numel(steadyDiff) == 4, "稳态结构差异应包含4个指标");

%% 6. Figure Q1-2：尾段稳定性与阻尼结构差异（L3）
% Core conclusion：两种阻尼情形第35-39周期均满足预设2%重复性判据；
% 稳态结构差异最大出现在相对位移半峰峰值，约2.23%。
fig2 = figure("Color", "w", "Position", [110, 100, 1220, 560], "Name", "Q1-L3 稳健性");
tl2 = tiledlayout(fig2, 1, 2, "TileSpacing", "compact", "Padding", "compact");
sgtitle(tl2, "尾段周期稳定性与阻尼结构差异", "FontWeight", "bold");

% (a) 第35-39周期重复性最大相对偏差
axA = nexttile(tl2, 1);
hold(axA, "on");
yPos = 1:numel(errValue);
barColors = zeros(numel(errValue), 3);
for i = 1:numel(errValue)
    if errGroup(i) == scenarioConstant
        barColors(i, :) = palette.primary;
    else
        barColors(i, :) = palette.secondary;
    end
end
b = barh(axA, yPos, errValue, 0.72, "FaceColor", "flat", "EdgeColor", "none");
b.CData = barColors;
xline(axA, 2.0, "--", "2% 判据", "Color", palette.risk, "LineWidth", 1.4, ...
    "LabelOrientation", "horizontal", "LabelVerticalAlignment", "bottom");
shortMetric = replace(errMetric, ["半峰峰值", "RMS"], ["幅值", "RMS"]);
yLabelsA = strings(numel(errValue), 1);
for i = 1:numel(errValue)
    prefix = "常阻尼·";
    if errGroup(i) == scenarioNonlinear, prefix = "幂律·"; end
    yLabelsA(i) = prefix + shortMetric(i);
end
set(axA, "YTick", yPos, "YTickLabel", yLabelsA, "YDir", "reverse");
xlabel(axA, "最大相对偏差 / %");
title(axA, "(a) 末5周期重复性", "FontWeight", "normal");
xlim(axA, [0, max(2.15, 1.12 * max(errValue))]);
for i = 1:numel(errValue)
    text(axA, errValue(i) + 0.035, yPos(i), sprintf("%.2f%%", errValue(i)), ...
        "VerticalAlignment", "middle", "FontSize", 12, "Color", palette.ink);
end

% (b) 两种阻尼稳态指标相对差异
axB = nexttile(tl2, 2);
hold(axB, "on");
yPos2 = 1:numel(steadyDiff);
barh(axB, yPos2, steadyDiff, 0.68, "FaceColor", palette.primary, "EdgeColor", "none");
set(axB, "YTick", yPos2, "YTickLabel", replace(steadyMetric, "半峰峰值", "幅值"), "YDir", "reverse");
xlabel(axB, "幂律阻尼相对常阻尼差异 / %");
title(axB, "(b) 稳态结构差异", "FontWeight", "normal");
xlim(axB, [0, max(2.5, 1.18 * max(steadyDiff))]);
for i = 1:numel(steadyDiff)
    text(axB, steadyDiff(i) + 0.04, yPos2(i), sprintf("%.2f%%", steadyDiff(i)), ...
        "VerticalAlignment", "middle", "FontSize", 12, "Color", palette.ink);
end
apply_style(fig2, fontName, palette.ink);

%% 7. 图窗保留供人工检查
% 不自动 exportgraphics；待 Figure QA（缩略图、灰度、论文最终宽度）通过后再导出。

%% ----------------------------- 局部函数 -----------------------------
function column = exact_header_column(headers, expected)
matches = find(headers == strtrim(string(expected)));
assert(numel(matches) == 1, "字段缺失或重复: %s", expected);
column = matches(1);
end

function [times, matrix] = collect_state_series(raw, scenarioCol, timeCol, valueCol, stateCol, scenario, stateLabels)
bodyRows = raw(2:end, :);
scenarioValues = strtrim(string(bodyRows(:, scenarioCol)));
stateValues = strtrim(string(bodyRows(:, stateCol)));
timeValues = cell_to_numeric(bodyRows(:, timeCol));
numValues = cell_to_numeric(bodyRows(:, valueCol));

matrix = [];
times = [];
for k = 1:numel(stateLabels)
    mask = scenarioValues == scenario & stateValues == stateLabels(k) & isfinite(timeValues) & isfinite(numValues);
    t = timeValues(mask);
    y = numValues(mask);
    [t, order] = sort(t);
    y = y(order);
    assert(numel(t) == 898, "%s-%s记录数不是898", scenario, stateLabels(k));
    if isempty(times)
        times = t;
        matrix = nan(numel(t), numel(stateLabels));
    else
        assert(isequal(times, t), "%s四个状态量的时间网格不一致", scenario);
    end
    matrix(:, k) = y;
end
end

function value = read_scalar_metric(bookPath, sheetName, metricName)
raw = readcell(bookPath, "Sheet", sheetName);
headers = strtrim(string(raw(1, :)));
metricCol = exact_header_column(headers, "指标");
valueCol = exact_header_column(headers, "数值");
metricValues = strtrim(string(raw(2:end, metricCol)));
idx = find(metricValues == metricName);
assert(numel(idx) == 1, "%s 中指标 %s 缺失或重复", sheetName, metricName);
values = cell_to_numeric(raw(2:end, valueCol));
value = values(idx);
assert(isfinite(value), "%s-%s 不是有限数值", sheetName, metricName);
end

function [zoomX, zoomMask, centerTime] = difference_focus_window(times, yBase, yAlt, period)
combined = [yBase; yAlt];
responseRange = max(combined, [], 1) - min(combined, [], 1);
responseRange(responseRange < 1.0e-12) = 1.0;
normalizedDifference = abs(yAlt - yBase) ./ responseRange;
separationScore = sqrt(mean(normalizedDifference .^ 2, 2));

halfWidth = 1.25 * period;
validCenter = times >= times(1) + halfWidth & times <= times(end) - halfWidth;
assert(any(validCenter), "局部放大窗口无法在当前时域内放置");
validIdx = find(validCenter);
[~, localIndex] = max(separationScore(validCenter));
centerIndex = validIdx(localIndex);
centerTime = times(centerIndex);
zoomX = [centerTime - halfWidth, centerTime + halfWidth];
zoomMask = times >= zoomX(1) & times <= zoomX(2);
assert(nnz(zoomMask) >= 10, "局部放大窗口采样点过少");
end

function add_local_zoom(fig, mainAx, times, baseSeries, altSeries, mask, zoomX, palette, fontName, unitText, panelIndex)
% Embedded inset：位置依附对应主 axes，不改变主图尺度。
set(mainAx, "Units", "normalized");
mainPos = mainAx.Position;

% 为避免四个 inset 机械遮住相同区域，左右列采用略不同的锚点。
if mod(panelIndex, 2) == 1
    insetPos = [mainPos(1) + 0.58 * mainPos(3), mainPos(2) + 0.57 * mainPos(4), ...
        0.36 * mainPos(3), 0.34 * mainPos(4)];
else
    insetPos = [mainPos(1) + 0.57 * mainPos(3), mainPos(2) + 0.57 * mainPos(4), ...
        0.36 * mainPos(3), 0.34 * mainPos(4)];
end

axInset = axes("Parent", fig, "Units", "normalized", "Position", insetPos);
hold(axInset, "on");
localT = times(mask);
localBase = baseSeries(mask);
localAlt = altSeries(mask);

% 先画两曲线之间的真实差异带，再叠加原始曲线；不进行插值或平滑。
patch(axInset, [localT; flipud(localT)], [localBase; flipud(localAlt)], palette.gapFill, ...
    "FaceAlpha", 0.15, "EdgeColor", "none", "HandleVisibility", "off");
plot(axInset, localT, localBase, "LineWidth", 1.35, "Color", palette.primary, "LineStyle", "-");
plot(axInset, localT, localAlt, "LineWidth", 1.25, "Color", palette.secondary, "LineStyle", "--");
yline(axInset, 0, ":", "Color", palette.baseline, "LineWidth", 0.65, "HandleVisibility", "off");
xlim(axInset, zoomX);

localValues = [localBase; localAlt];
yMin = min(localValues);
yMax = max(localValues);
span = yMax - yMin;
if span < 1.0e-10
    span = max(1.0e-6, 0.1 * max(abs(localValues)));
end
padding = 0.10 * span;
ylim(axInset, [yMin - padding, yMax + padding]);

maxDelta = max(abs(localAlt - localBase));
text(axInset, 0.03, 0.96, sprintf("max |Δ| = %.3g %s", maxDelta, unitText), ...
    "Units", "normalized", "VerticalAlignment", "top", "FontName", fontName, ...
    "FontSize", 8.7, "Color", palette.ink, "BackgroundColor", "w", "Margin", 1.2);

set(axInset, "FontName", fontName, "FontSize", 8.5, "LineWidth", 0.9, ...
    "Box", "on", "Layer", "top", "TickDir", "out", "XColor", palette.ink, "YColor", palette.ink);
axInset.XTick = linspace(zoomX(1), zoomX(2), 3);
axInset.XTickLabel = compose("%.1f", axInset.XTick);
grid(axInset, "off");
end

function values = cell_to_numeric(column)
values = nan(size(column, 1), 1);
for i = 1:size(column, 1)
    item = column{i};
    if (isnumeric(item) || islogical(item)) && isscalar(item)
        values(i) = double(item);
    elseif ischar(item) || isstring(item)
        parsed = str2double(string(item));
        if isfinite(parsed), values(i) = parsed; end
    end
end
end

function apply_style(fig, fontName, ink)
set(fig, "Color", "w");
for ax = reshape(findall(fig, "Type", "axes"), 1, [])
    set(ax, "FontName", fontName, "FontSize", 15, "LineWidth", 1.2, ...
        "Box", "off", "Layer", "top", "TickDir", "out", "XColor", ink, "YColor", ink);
    grid(ax, "off");
end
for lgd = reshape(findall(fig, "Type", "legend"), 1, [])
    set(lgd, "FontName", fontName, "FontSize", 13, "Box", "off");
end
for txt = reshape(findall(fig, "Type", "text"), 1, [])
    if isprop(txt, "FontName"), set(txt, "FontName", fontName); end
end
end

function fontName = select_font()
preferred = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Arial Unicode MS", "Helvetica", "Arial"];
available = string(listfonts);
fontName = "Helvetica";
for candidate = preferred
    if any(strcmpi(available, candidate))
        fontName = candidate;
        return;
    end
end
end
