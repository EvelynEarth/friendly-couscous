%% q2_plot：2022A 问题二 Figure Evidence（深化分析闭环版）
% 只读取同目录下已验收的：
%   1) 问题二求解结果.xlsx
%   2) 问题二结果深化分析.xlsx
% 不重新求解 ODE，不重新运行 DE/Powell，不读取边界稳态精修工作簿。
%
% Figure Q2-1：参数结构与稳态功率收益
% Figure Q2-2：幂律主候选的周期稳态收敛与步长一致性
% 默认仅打开 MATLAB 图窗供 Figure QA，不自动导出。

clearvars; clc;

%% 1. 路径与工作簿
scriptPath = string(mfilename("fullpath"));
assert(strlength(scriptPath) > 0, "请从已保存的 q2_plot.m 运行脚本");
resultDir = string(fileparts(scriptPath));
solutionBook = fullfile(resultDir, "问题二求解结果.xlsx");
analysisBook = fullfile(resultDir, "问题二结果深化分析.xlsx");
assert(isfile(solutionBook), "缺少工作簿：%s", solutionBook);
assert(isfile(analysisBook), "缺少工作簿：%s", analysisBook);

mustSolution = ["运行配置","核心指标","收敛诊断","主结果质量门"];
mustAnalysis = ["运行配置","结论总览","局部敏感性","稳健性证据","深化分析质量门"];
ss = string(sheetnames(solutionBook));
as = string(sheetnames(analysisBook));
for s = mustSolution, assert(any(ss == s), "问题二求解结果.xlsx 缺少：%s", s); end
for s = mustAnalysis, assert(any(as == s), "问题二结果深化分析.xlsx 缺少：%s", s); end
assert_quality_gate(solutionBook, "主结果质量门");
assert_quality_gate(analysisBook, "深化分析质量门");

%% 2. 模型/数据闭环一致性
cfg1 = readcell(solutionBook,"Sheet","运行配置");
cfg2 = readcell(analysisBook,"Sheet","运行配置");
assert(string(config_value(cfg1,"semantic_hash")) == string(config_value(cfg2,"semantic_hash")), ...
    "主结果与深化分析 semantic_hash 不一致");
assert(string(config_value(cfg1,"data_sha256")) == string(config_value(cfg2,"data_sha256")), ...
    "主结果与深化分析 data_sha256 不一致");

%% 3. 核心量
core = readcell(solutionBook,"Sheet","核心指标");
ana = readcell(analysisBook,"Sheet","结论总览");
cStar = metric_value(core,"直线阻尼最优c");
pLinear = metric_value(core,"直线阻尼最大平均功率");
aStar = metric_value(core,"幂律阻尼最优比例系数a");
nStar = metric_value(core,"幂律阻尼最优幂指数n");
pNonlinear = metric_value(core,"幂律阻尼最大平均功率");
stopCycle = metric_value(core,"幂律候选最终验证停止周期");
gainAbs = metric_value(ana,"幂律相对直线绝对提升");
gainRel = metric_value(ana,"幂律相对直线相对提升");
aGap = metric_value(ana,"a距题面上界100000");
stepRel = metric_value(ana,"最终T/40-T/80功率相对差");
n0Rel = metric_value(ana,"n=0跨模型等价相对差");
assert(abs((pNonlinear-pLinear)-gainAbs) <= 1e-8, "收益与主结果不一致");

%% 4. 局部敏感性：只使用深化分析已经写出的 60T 搜索诊断
sens = readcell(analysisBook,"Sheet","局部敏感性");
h = strtrim(string(sens(1,:)));
colLabel = exact_header_column(h,"检查点");
colPct = exact_header_column(h,"相对当前候选差/%");
labels = strtrim(string(sens(2:end,colLabel)));
pcts = cell_to_numeric(sens(2:end,colPct));
wanted = ["u-0.01","u+0.01","n-0.01","n+0.01"];
showLabels = ["a-1000","a=100000","n-0.01","n+0.01"];
localPct = nan(4,1);
for i=1:4
    idx = find(labels == wanted(i),1);
    assert(~isempty(idx),"局部敏感性缺少：%s",wanted(i));
    localPct(i)=pcts(idx);
end

%% 5. T/40 与 T/80 收敛序列
conv = readcell(solutionBook,"Sheet","收敛诊断");
h = strtrim(string(conv(1,:)));
cObj = exact_header_column(h,"对象");
cCycle = exact_header_column(h,"后窗口结束周期");
cPower = exact_header_column(h,"后窗口功率/W");
cPR = exact_header_column(h,"功率相对差");
cSR = exact_header_column(h,"同相位状态相对差");
obj = strtrim(string(conv(2:end,cObj)));
cyc = cell_to_numeric(conv(2:end,cCycle));
pow = cell_to_numeric(conv(2:end,cPower));
pr = cell_to_numeric(conv(2:end,cPR));
sr = cell_to_numeric(conv(2:end,cSR));

mask40 = obj=="幂律候选" & isfinite(cyc) & isfinite(pow);
mask80 = obj=="幂律候选-步长加密" & isfinite(cyc) & isfinite(pow);
[cycle40,idx] = sort(cyc(mask40)); power40=pow(mask40); power40=power40(idx); pr40=pr(mask40); pr40=pr40(idx); sr40=sr(mask40); sr40=sr40(idx);
[cycle80,idx] = sort(cyc(mask80)); power80=pow(mask80); power80=power80(idx); pr80=pr(mask80); pr80=pr80(idx); sr80=sr(mask80); sr80=sr80(idx);
assert(numel(cycle40)>=6 && isequal(cycle40,cycle80),"T/40 与 T/80 收敛记录不足或周期节点不一致");

%% 6. 角色色与基础样式（继承 Q1 paper-family）
pal.primary=[48,96,130]/255; pal.secondary=[178,76,62]/255;
pal.accent=[201,139,55]/255; pal.base=[116,124,132]/255; pal.ink=[38,43,49]/255;
fontName=select_font();

%% 7. Figure Q2-1：参数结构与稳态功率收益
fig1=figure("Color","w","Position",[80,80,1260,570],"Name","Q2 参数结构与功率收益");
tl=tiledlayout(fig1,1,2,"TileSpacing","compact","Padding","compact");
sgtitle(tl,"问题二：PTO 阻尼参数结构与平均输出功率收益","FontWeight","bold");

% (a) 局部扰动
ax=nexttile(tl,1); hold(ax,"on");
y=1:4;
b=barh(ax,y,localPct,0.62,"FaceColor","flat","EdgeColor","none");
b.CData=[pal.primary;pal.primary;pal.accent;pal.accent];
xline(ax,0,"-","Color",pal.base,"LineWidth",1,"HandleVisibility","off");
set(ax,"YTick",y,"YTickLabel",showLabels,"YDir","reverse");
mn=min(localPct); mx=max(localPct); span=max(0.01,mx-mn);
xlim(ax,[mn-0.18*span,max(0.002,mx+0.18*span)]);
for i=1:4
    if localPct(i)>=0, xt=localPct(i)+0.012*span; ha="left"; else, xt=localPct(i)-0.012*span; ha="right"; end
    text(ax,xt,i,sprintf("%+.6g%%",localPct(i)),"HorizontalAlignment",ha,"VerticalAlignment","middle","Color",pal.ink,"FontSize",10.8);
end
xlabel(ax,"相对当前候选的 60T 搜索功率变化 / %");
title(ax,"(a) 局部扰动揭示的参数结构","FontWeight","normal");
text(ax,0.03,0.04,sprintf("主候选：a=%.3f（距上界 %.3f），n=%.5f\na明显趋向上边界；n±0.01 两侧均降低搜索功率",aStar,aGap,nStar), ...
    "Units","normalized","Color",pal.base,"FontSize",10.3,"VerticalAlignment","bottom");

% (b) 稳态收益
ax=nexttile(tl,2); hold(ax,"on");
xline(ax,0,"-","Color",pal.base,"LineWidth",1,"HandleVisibility","off");
scatter(ax,0,1,90,"o","MarkerFaceColor",pal.base,"MarkerEdgeColor","w","LineWidth",0.9);
barh(ax,2,gainAbs,0.58,"FaceColor",pal.primary,"EdgeColor","none");
set(ax,"YTick",[1,2],"YTickLabel",["最优直线阻尼","幂律主候选"],"YDir","reverse");
xlim(ax,[-0.08*gainAbs,1.24*gainAbs]);
xlabel(ax,"相对最优直线阻尼的稳态平均功率增量 / W");
title(ax,"(b) 幂律阻尼的正式稳态功率收益","FontWeight","normal");
text(ax,0.015*gainAbs,1,sprintf("P=%.6f W",pLinear),"VerticalAlignment","middle","Color",pal.base,"FontSize",10.8);
text(ax,gainAbs+0.02*gainAbs,2,sprintf("+%.6f W  (+%.4f%%)",gainAbs,100*gainRel),"VerticalAlignment","middle","Color",pal.ink,"FontSize",11.2);
text(ax,0.03,0.04,sprintf("c^*=%.2f N·s/m\n幂律：a=%.3f, n=%.5f, P=%.6f W\n提升稳定，但幅度有限",cStar,aStar,nStar,pNonlinear), ...
    "Units","normalized","Color",pal.base,"FontSize",10.3,"VerticalAlignment","bottom");
apply_style(fig1,fontName,pal.ink);

%% 8. Figure Q2-2：周期稳态收敛与步长一致性
fig2=figure("Color","w","Position",[110,110,1260,570],"Name","Q2 数值收敛证据");
tl=tiledlayout(fig2,1,2,"TileSpacing","compact","Padding","compact");
sgtitle(tl,"问题二：幂律主候选的周期稳态收敛与步长一致性","FontWeight","bold");

% (a) 后窗口稳态功率
ax=nexttile(tl,1); hold(ax,"on");
h40=plot(ax,cycle40,power40,"-o","Color",pal.primary,"LineWidth",1.65,"MarkerSize",5.4,"MarkerFaceColor","w");
h80=plot(ax,cycle80,power80,"--s","Color",pal.secondary,"LineWidth",1.55,"MarkerSize",5.2,"MarkerFaceColor","w");
scatter(ax,cycle40(end),power40(end),76,"o","MarkerFaceColor",pal.primary,"MarkerEdgeColor","w");
scatter(ax,cycle80(end),power80(end),76,"s","MarkerFaceColor",pal.secondary,"MarkerEdgeColor","w");
allP=[power40(:);power80(:)]; r=max(allP)-min(allP); if r<=0,r=1;end
ylim(ax,[min(allP)-0.12*r,max(allP)+0.12*r]); xlim(ax,[min(cycle40)-3,max(cycle40)+3]);
xlabel(ax,"后窗口结束周期 / T"); ylabel(ax,"后窗口平均输出功率 / W");
title(ax,"(a) T/40 与 T/80 的稳态功率收敛","FontWeight","normal");
legend(ax,[h40,h80],["max step = T/40","max step = T/80"],"Location","southoutside","Orientation","horizontal","Box","off");
text(ax,0.03,0.96,sprintf("最终在 %.0fT 通过；T/40-T/80 相对差 = %.3e",stopCycle,stepRel),"Units","normalized","VerticalAlignment","top","Color",pal.base,"FontSize",10.5);

% (b) 功率窗口与同相位状态判据
ax=nexttile(tl,2); hold(ax,"on");
hP40=semilogy(ax,cycle40,pr40,"-o","Color",pal.primary,"LineWidth",1.55,"MarkerSize",5.2,"MarkerFaceColor","w");
hS40=semilogy(ax,cycle40,sr40,"--o","Color",pal.primary,"LineWidth",1.35,"MarkerSize",5.0,"MarkerFaceColor","w");
hP80=semilogy(ax,cycle80,pr80,"-s","Color",pal.secondary,"LineWidth",1.55,"MarkerSize",5.2,"MarkerFaceColor","w");
hS80=semilogy(ax,cycle80,sr80,"--s","Color",pal.secondary,"LineWidth",1.35,"MarkerSize",5.0,"MarkerFaceColor","w");
hTol=yline(ax,1e-5,":","Color",pal.accent,"LineWidth",1.5,"Label","1e-5 判据","LabelHorizontalAlignment","left","LabelVerticalAlignment","bottom");
xlim(ax,[min(cycle40)-3,max(cycle40)+3]);
yMin=min([pr40(:);sr40(:);pr80(:);sr80(:)]); yMax=max([pr40(:);sr40(:);pr80(:);sr80(:)]);
ylim(ax,[max(1e-7,yMin/2.5),min(1,yMax*2)]);
xlabel(ax,"后窗口结束周期 / T"); ylabel(ax,"相对差（对数坐标）");
title(ax,"(b) 功率窗口与同相位状态收敛判据","FontWeight","normal");
legend(ax,[hP40,hS40,hP80,hS80,hTol],["T/40 功率差","T/40 状态差","T/80 功率差","T/80 状态差","1e-5 判据"],"Location","southoutside","NumColumns",3,"Box","off");
text(ax,0.03,0.96,sprintf("n=0 跨模型等价相对差 = %.3e",n0Rel),"Units","normalized","VerticalAlignment","top","Color",pal.base,"FontSize",10.5);
apply_style(fig2,fontName,pal.ink);

%% 9. 控制台摘要
fprintf("\nQ2 Figure Evidence 数据闭环通过。\n");
fprintf("  c* = %.10f N·s/m\n",cStar);
fprintf("  幂律主候选：a = %.10f, n = %.10f\n",aStar,nStar);
fprintf("  P_linear = %.10f W\n",pLinear);
fprintf("  P_power  = %.10f W\n",pNonlinear);
fprintf("  gain = %.10f W (%.6f%%)\n",gainAbs,100*gainRel);
fprintf("  stop cycle = %.0fT, T/40-T/80 rel diff = %.3e\n",stopCycle,stepRel);
fprintf("  默认不自动导出图片，请先完成 Figure QA。\n\n");

%% ===== 局部函数 =====
function value=config_value(raw,key)
    h=strtrim(string(raw(1,:))); ck=exact_header_column(h,"项目"); cv=exact_header_column(h,"值");
    keys=strtrim(string(raw(2:end,ck))); idx=find(keys==string(key),1); assert(~isempty(idx),"运行配置缺少：%s",key); value=raw{idx+1,cv};
end

function value=metric_value(raw,keyText)
    h=strtrim(string(raw(1,:))); ck=exact_header_column(h,"指标"); cv=exact_header_column(h,"数值");
    keys=strtrim(string(raw(2:end,ck))); idx=find(keys==string(keyText),1); assert(~isempty(idx),"未找到指标：%s",keyText);
    value=to_double(raw{idx+1,cv}); assert(isfinite(value),"指标 %s 不是有限数值",keyText);
end

function col=exact_header_column(headers,target)
    idx=find(headers==string(target),1); assert(~isempty(idx),"缺少列：%s",target); col=idx;
end

function values=cell_to_numeric(cells)
    values=nan(numel(cells),1); for i=1:numel(cells), values(i)=to_double(cells{i}); end
end

function value=to_double(x)
    if isnumeric(x)||islogical(x), if isempty(x),value=NaN;else,value=double(x(1));end; return; end
    s=strtrim(string(x)); if strlength(s)==0||ismissing(s),value=NaN;else,value=str2double(s);end
end

function assert_quality_gate(bookPath,sheetName)
    raw=readcell(bookPath,"Sheet",sheetName); h=strtrim(string(raw(1,:))); c=exact_header_column(h,"是否通过");
    r=strtrim(string(raw(2:end,c))); r=r(strlength(r)>0 & ~ismissing(r));
    assert(~isempty(r),"%s 没有质量门记录",sheetName); assert(all(r=="是"),"%s 存在未通过项",sheetName);
end

function fontName=select_font()
    preferred=["Microsoft YaHei","Microsoft YaHei UI","SimHei","Noto Sans CJK SC","Arial"];
    installed=string(listfonts); fontName="Arial";
    for f=preferred, if any(strcmpi(installed,f)),fontName=f;return;end,end
end

function apply_style(figHandle,fontName,inkColor)
    axs=findall(figHandle,"Type","axes");
    for k=1:numel(axs)
        ax=axs(k); ax.FontName=fontName; ax.FontSize=11; ax.LineWidth=0.9; ax.TickDir="out"; ax.Box="off";
        ax.XColor=inkColor; ax.YColor=inkColor; ax.Layer="top"; grid(ax,"off");
    end
    txt=findall(figHandle,"Type","text"); for k=1:numel(txt),txt(k).FontName=fontName;end
end
