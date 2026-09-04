%% q2_plot：2022A 问题二 Figure Evidence
% 只读取已经通过主结果质量门的：
%   1) 问题二求解结果.xlsx
%   2) 问题二边界稳态精修结果.xlsx
% 不重新求解 ODE，不重新优化，不插值/平滑，不依赖“问题二结果深化分析.xlsx”。
%
% Figure Q2-1：最优阻尼结构与功率增益
% Core conclusion：
%   幂律方案的比例系数最优值落在 a=100000 上边界，
%   幂指数在 n≈0.416065 形成内部稳态峰值；相较最优直线阻尼，
%   最大平均功率提升约 0.288%，提升稳定但幅度有限。
% Evidence level：L1 主结果 + L2 结构解释（同屏直接完成同一个“最优在哪里、收益多大”问题）
% Layout：1×2
% Panel (a)：固定 a=100000 的 n—稳态平均功率局部扫描与精修最优点
% Panel (b)：二维候选/边界精修相对最优直线阻尼的功率增益
%
% Figure Q2-2：最终幂律候选的数值收敛证据
% Core conclusion：
%   T/40 与 T/80 两套步长在 170T 得到一致的稳态平均功率，
%   功率窗口差和同相位状态差均降至 1e-5 阈值以下。
% Evidence level：L4 数值合法性
% Layout：1×2
% Panel (a)：两套步长的后窗口稳态功率
% Panel (b)：功率相对差/同相位状态相对差及 1e-5 阈值
%
% 默认只保留 MATLAB 图窗供 Figure QA；不自动导出图片。

clearvars;
clc;

%% 1. 路径、工作簿与必须工作表
scriptPath = string(mfilename("fullpath"));
assert(strlength(scriptPath) > 0, "请从已保存的 q2_plot.m 运行脚本");
resultDir = string(fileparts(scriptPath));

solutionBook = fullfile(resultDir, "问题二求解结果.xlsx");
refineBook = fullfile(resultDir, "问题二边界稳态精修结果.xlsx");

assert(isfile(solutionBook), "缺少工作簿: %s", solutionBook);
assert(isfile(refineBook), "缺少工作簿: %s", refineBook);

solutionSheets = string(sheetnames(solutionBook));
refineSheets = string(sheetnames(refineBook));

mustSolution = ["核心指标", "主结果质量门"];
mustRefine = ["核心结论", "局部稳态扫描", "边界对照", "收敛诊断", "主结果质量门"];
for s = mustSolution
    assert(any(solutionSheets == s), "问题二求解结果.xlsx 缺少工作表：%s", s);
end
for s = mustRefine
    assert(any(refineSheets == s), "问题二边界稳态精修结果.xlsx 缺少工作表：%s", s);
end

%% 2. 主结果与边界精修核心量
mainCore = readcell(solutionBook, "Sheet", "核心指标");
refineCore = readcell(refineBook, "Sheet", "核心结论");

cStar = metric_value(mainCore, "指标", "数值", "直线阻尼最优c");
pLinear = metric_value(mainCore, "指标", "数值", "直线阻尼最大平均功率");
nOld = metric_value(mainCore, "指标", "数值", "幂律阻尼最优幂指数n");
pOld = metric_value(mainCore, "指标", "数值", "幂律阻尼最大平均功率");

aStar = metric_value(refineCore, "指标", "数值", "固定比例系数a");
nStar = metric_value(refineCore, "指标", "数值", "边界精修最优n");
pRefine40 = metric_value(refineCore, "指标", "数值", "边界精修最大稳态平均功率(T/40)");
pRefine80 = metric_value(refineCore, "指标", "数值", "步长加密平均功率(T/80)");

assert(abs(aStar - 100000) <= 1e-9, "边界精修工作簿中的 a 不是100000");
assert(cStar >= 0 && cStar <= 100000, "直线阻尼最优 c 超出题面范围");
assert(nStar >= 0 && nStar <= 1, "边界精修 n* 超出题面范围");

gainOld = pOld - pLinear;
gainRefined = pRefine40 - pLinear;
gainPercent = gainRefined / pLinear * 100;
refineIncrement = pRefine40 - pOld;

%% 3. 读取固定 a=100000 的局部稳态扫描
scanRaw = readcell(refineBook, "Sheet", "局部稳态扫描");
scanHeaders = strtrim(string(scanRaw(1, :)));
colN = exact_header_column(scanHeaders, "n");
colPower = exact_header_column(scanHeaders, "稳态平均功率/W");
colNote = exact_header_column(scanHeaders, "备注");

nScan = cell_to_numeric(scanRaw(2:end, colN));
pScan = cell_to_numeric(scanRaw(2:end, colPower));
noteScan = strtrim(string(scanRaw(2:end, colNote)));

validScan = isfinite(nScan) & isfinite(pScan);
nScan = nScan(validScan);
pScan = pScan(validScan);
noteScan = noteScan(validScan);

[nScan, order] = sort(nScan);
pScan = pScan(order);
noteScan = noteScan(order);

assert(numel(nScan) >= 8, "局部稳态扫描有效点过少");
assert(all(diff(nScan) > 0), "局部稳态扫描 n 存在重复或非递增点");

[~, idxOldScan] = min(abs(nScan - nOld));
oldBoundaryPower = pScan(idxOldScan);

%% 4. 读取最终 T/40、T/80 收敛诊断
convRaw = readcell(refineBook, "Sheet", "收敛诊断");
convHeaders = strtrim(string(convRaw(1, :)));

colObject = exact_header_column(convHeaders, "对象");
colEndCycle = exact_header_column(convHeaders, "后窗口结束周期");
colAfterPower = exact_header_column(convHeaders, "后功率/W");
colPowerRel = exact_header_column(convHeaders, "功率相对差");
colPhaseRel = exact_header_column(convHeaders, "同相位状态相对差");

convObject = strtrim(string(convRaw(2:end, colObject)));
convCycle = cell_to_numeric(convRaw(2:end, colEndCycle));
convPower = cell_to_numeric(convRaw(2:end, colAfterPower));
convPowerRel = cell_to_numeric(convRaw(2:end, colPowerRel));
convPhaseRel = cell_to_numeric(convRaw(2:end, colPhaseRel));

mask40 = convObject == "最终T/40" & isfinite(convCycle) & isfinite(convPower);
mask80 = convObject == "最终T/80" & isfinite(convCycle) & isfinite(convPower);

cycle40 = convCycle(mask40);
power40 = convPower(mask40);
powerRel40 = convPowerRel(mask40);
phaseRel40 = convPhaseRel(mask40);

cycle80 = convCycle(mask80);
power80 = convPower(mask80);
powerRel80 = convPowerRel(mask80);
phaseRel80 = convPhaseRel(mask80);

[cycle40, idx40] = sort(cycle40);
power40 = power40(idx40);
powerRel40 = powerRel40(idx40);
phaseRel40 = phaseRel40(idx40);

[cycle80, idx80] = sort(cycle80);
power80 = power80(idx80);
powerRel80 = powerRel80(idx80);
phaseRel80 = phaseRel80(idx80);

assert(numel(cycle40) >= 5 && numel(cycle80) >= 5, "最终收敛诊断记录不足");
assert(isequal(cycle40, cycle80), "T/40 与 T/80 收敛诊断周期节点不一致");

%% 5. 科研绘图角色色与基础样式（继承 Q1 paper-family）
palette.primary = [48, 96, 130] / 255;
palette.secondary = [178, 76, 62] / 255;
palette.accent = [201, 139, 55] / 255;
palette.baseline = [116, 124, 132] / 255;
palette.ink = [38, 43, 49] / 255;
palette.light = [226, 230, 233] / 255;
palette.risk = [178, 76, 62] / 255;
fontName = select_font();

%% 6. Figure Q2-1：最优阻尼结构与功率增益
fig1 = figure("Color", "w", "Position", [90, 90, 1240, 560], ...
    "Name", "Q2-L1/L2 最优阻尼结构与功率增益");
tl1 = tiledlayout(fig1, 1, 2, "TileSpacing", "compact", "Padding", "compact");
sgtitle(tl1, "问题二：最优阻尼结构与平均输出功率增益", "FontWeight", "bold");

% (a) 固定 a=100000：n 的局部稳态响应
axA = nexttile(tl1, 1);
hold(axA, "on");

hScan = plot(axA, nScan, pScan, "-o", ...
    "Color", palette.primary, "LineWidth", 1.65, ...
    "MarkerSize", 5.3, "MarkerFaceColor", "w");

hOld = scatter(axA, nScan(idxOldScan), oldBoundaryPower, 74, ...
    "Marker", "d", "MarkerFaceColor", palette.secondary, ...
    "MarkerEdgeColor", "w", "LineWidth", 0.9);

hBest = scatter(axA, nStar, pRefine40, 98, ...
    "Marker", "p", "MarkerFaceColor", palette.accent, ...
    "MarkerEdgeColor", "w", "LineWidth", 0.9);

xline(axA, nStar, "--", "Color", palette.accent, ...
    "LineWidth", 1.05, "HandleVisibility", "off");

scanRange = max([pScan; pRefine40]) - min([pScan; pRefine40]);
if scanRange <= 0
    scanRange = 1;
end
ylim(axA, [min([pScan; pRefine40]) - 0.08 * scanRange, ...
           max([pScan; pRefine40]) + 0.10 * scanRange]);
xlim(axA, [min(nScan) - 0.004, max(nScan) + 0.004]);

xlabel(axA, "幂指数 n");
ylabel(axA, "稳态平均输出功率 / W");
title(axA, "(a) 固定 a=100000 的局部稳态功率响应", "FontWeight", "normal");
legend(axA, [hScan, hOld, hBest], ...
    ["局部稳态扫描", sprintf("二维候选 n=%.4f", nOld), sprintf("边界精修 n^*=%.4f", nStar)], ...
    "Location", "southoutside", "Orientation", "horizontal", "Box", "off");

text(axA, nStar + 0.0025, pRefine40, ...
    sprintf("P_{max}=%.6f W", pRefine40), ...
    "Color", palette.ink, "FontSize", 11, ...
    "VerticalAlignment", "bottom");

% (b) 相对最优直线阻尼的功率增益
axB = nexttile(tl1, 2);
hold(axB, "on");

gainValues = [gainOld; gainRefined];
gainLabels = ["二维幂律候选", "a=100000 边界精修"];

b = barh(axB, 1:2, gainValues, 0.62, ...
    "FaceColor", "flat", "EdgeColor", "none");
b.CData = [palette.secondary; palette.primary];

set(axB, "YTick", 1:2, "YTickLabel", gainLabels, "YDir", "reverse");
xline(axB, 0, "-", "Color", palette.baseline, "LineWidth", 0.9, "HandleVisibility", "off");

maxGain = max(gainValues);
xlim(axB, [0, maxGain * 1.22]);
xlabel(axB, "相对最优直线阻尼的平均功率增量 / W");
title(axB, "(b) 幂律方案相对直线方案的收益", "FontWeight", "normal");

for i = 1:2
    text(axB, gainValues(i) + 0.015 * maxGain, i, ...
        sprintf("+%.6f W", gainValues(i)), ...
        "VerticalAlignment", "middle", "Color", palette.ink, "FontSize", 11.5);
end

annotation(fig1, "textbox", [0.555, 0.135, 0.39, 0.08], ...
    "String", sprintf("最终幂律方案：a^*=100000, n^*=%.6f；相对提升 %.4f%%；边界精修仅再增加 %.6f W", ...
        nStar, gainPercent, refineIncrement), ...
    "EdgeColor", "none", "HorizontalAlignment", "center", ...
    "FontName", fontName, "FontSize", 10.8, "Color", palette.baseline);

apply_style(fig1, fontName, palette.ink);

%% 7. Figure Q2-2：最终候选的稳态收敛与步长一致性
fig2 = figure("Color", "w", "Position", [120, 120, 1240, 560], ...
    "Name", "Q2-L4 数值收敛证据");
tl2 = tiledlayout(fig2, 1, 2, "TileSpacing", "compact", "Padding", "compact");
sgtitle(tl2, "问题二：最终幂律候选的周期稳态收敛与步长一致性", "FontWeight", "bold");

% (a) 稳态平均功率随验证周期收敛
axC = nexttile(tl2, 1);
hold(axC, "on");

h40 = plot(axC, cycle40, power40, "-o", ...
    "Color", palette.primary, "LineWidth", 1.65, ...
    "MarkerSize", 5.2, "MarkerFaceColor", "w");
h80 = plot(axC, cycle80, power80, "--s", ...
    "Color", palette.secondary, "LineWidth", 1.55, ...
    "MarkerSize", 5.0, "MarkerFaceColor", "w");

yline(axC, pRefine80, ":", ...
    sprintf("T/80 最终 %.6f W", pRefine80), ...
    "Color", palette.baseline, "LineWidth", 1.0, ...
    "LabelHorizontalAlignment", "left", ...
    "HandleVisibility", "off");

allConvPower = [power40; power80; pRefine40; pRefine80];
convSpan = max(allConvPower) - min(allConvPower);
if convSpan <= 0
    convSpan = 1e-3;
end
ylim(axC, [min(allConvPower) - 0.08 * convSpan, max(allConvPower) + 0.10 * convSpan]);
xlim(axC, [min(cycle40) - 3, max(cycle40) + 3]);

xlabel(axC, "后窗口结束周期 / T");
ylabel(axC, "后窗口平均输出功率 / W");
title(axC, "(a) T/40 与 T/80 的稳态功率收敛", "FontWeight", "normal");
legend(axC, [h40, h80], ["max step = T/40", "max step = T/80"], ...
    "Location", "southoutside", "Orientation", "horizontal", "Box", "off");

% (b) 功率/同相位状态差与 1e-5 判据
axD = nexttile(tl2, 2);
hold(axD, "on");
set(axD, "YScale", "log");

hp40 = plot(axD, cycle40, powerRel40, "-o", ...
    "Color", palette.primary, "LineWidth", 1.55, ...
    "MarkerSize", 5.0, "MarkerFaceColor", "w");
hs40 = plot(axD, cycle40, phaseRel40, "--o", ...
    "Color", palette.primary, "LineWidth", 1.35, ...
    "MarkerSize", 4.7, "MarkerFaceColor", "w");
hp80 = plot(axD, cycle80, powerRel80, "-s", ...
    "Color", palette.secondary, "LineWidth", 1.55, ...
    "MarkerSize", 5.0, "MarkerFaceColor", "w");
hs80 = plot(axD, cycle80, phaseRel80, "--s", ...
    "Color", palette.secondary, "LineWidth", 1.35, ...
    "MarkerSize", 4.7, "MarkerFaceColor", "w");

yline(axD, 1e-5, "--", "1\times10^{-5} 判据", ...
    "Color", palette.risk, "LineWidth", 1.2, ...
    "LabelHorizontalAlignment", "left", ...
    "HandleVisibility", "off");

xlabel(axD, "后窗口结束周期 / T");
ylabel(axD, "相对差");
title(axD, "(b) 功率窗口与同相位状态收敛判据", "FontWeight", "normal");
xlim(axD, [min(cycle40) - 3, max(cycle40) + 3]);

positiveResiduals = [powerRel40; phaseRel40; powerRel80; phaseRel80];
positiveResiduals = positiveResiduals(isfinite(positiveResiduals) & positiveResiduals > 0);
assert(~isempty(positiveResiduals), "收敛诊断相对差为空或非正");
ylim(axD, [min(positiveResiduals) / 2.2, max(positiveResiduals) * 2.0]);

legend(axD, [hp40, hs40, hp80, hs80], ...
    ["T/40 功率差", "T/40 状态差", "T/80 功率差", "T/80 状态差"], ...
    "Location", "southoutside", "Orientation", "horizontal", "Box", "off");

annotation(fig2, "textbox", [0.55, 0.135, 0.39, 0.08], ...
    "String", sprintf("170T：T/40=%.9f W，T/80=%.9f W；步长加密相对差=%.3e", ...
        pRefine40, pRefine80, abs(pRefine80 - pRefine40) / (1 + abs(pRefine80))), ...
    "EdgeColor", "none", "HorizontalAlignment", "center", ...
    "FontName", fontName, "FontSize", 10.8, "Color", palette.baseline);

apply_style(fig2, fontName, palette.ink);

%% 8. 图窗保留供人工 Figure QA
% 不自动 exportgraphics。
% Figure QA 建议重点检查：
% 1) Q2-1(a) n*=0.416065 与原二维候选是否能清楚区分；
% 2) Q2-1(b) 0.6603 W / 0.2879% 的小幅收益是否表达准确且不过度夸张；
% 3) Q2-2(b) 1e-5 阈值与 170T 最终通过点是否容易辨认；
% 4) 与 Q1 的字体、线宽、主/次颜色职责是否保持 paper-family 一致。

%% ----------------------------- 局部函数 -----------------------------
function column = exact_header_column(headers, expected)
matches = find(headers == strtrim(string(expected)));
assert(numel(matches) == 1, "字段缺失或重复: %s", expected);
column = matches(1);
end

function value = metric_value(raw, keyHeader, valueHeader, keyName)
headers = strtrim(string(raw(1, :)));
keyCol = exact_header_column(headers, keyHeader);
valueCol = exact_header_column(headers, valueHeader);
keys = strtrim(string(raw(2:end, keyCol)));
values = cell_to_numeric(raw(2:end, valueCol));
match = find(keys == strtrim(string(keyName)));
assert(numel(match) == 1, "指标缺失或重复: %s", keyName);
value = values(match);
assert(isfinite(value), "指标不是有限数值: %s", keyName);
end

function values = cell_to_numeric(cells)
values = nan(size(cells));
for i = 1:numel(cells)
    item = cells{i};
    if isnumeric(item) && isscalar(item)
        values(i) = double(item);
    elseif islogical(item) && isscalar(item)
        values(i) = double(item);
    elseif isstring(item) || ischar(item)
        values(i) = str2double(string(item));
    end
end
end

function fontName = select_font()
fontName = "Microsoft YaHei";
try
    fonts = string(listfonts);
    candidates = ["Microsoft YaHei", "Microsoft YaHei UI", "SimHei", "Noto Sans CJK SC", "Arial"];
    for name = candidates
        if any(strcmpi(fonts, name))
            fontName = name;
            return;
        end
    end
catch
    fontName = "Arial";
end
end

function apply_style(fig, fontName, ink)
axesList = findall(fig, "Type", "axes");
for ax = axesList'
    set(ax, ...
        "FontName", fontName, ...
        "FontSize", 11.5, ...
        "LineWidth", 0.85, ...
        "TickDir", "out", ...
        "Box", "off", ...
        "XColor", ink, ...
        "YColor", ink);
end

textList = findall(fig, "Type", "text");
for item = textList'
    try
        item.FontName = fontName;
        item.Color = ink;
    catch
    end
end
end
