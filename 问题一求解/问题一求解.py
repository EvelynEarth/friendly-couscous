from __future__ import annotations

import hashlib
import itertools
import json
import platform
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import scipy
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

FULL_FIDELITY_CONFIG = {
    "execution_owner": "user",
    "execution_profile": "full_fidelity",
    "stage": "primary",
    "problem_name": "问题一",
    "data_paths": ["A题题面参数.json"],
    "data_sha256": "0ea62664cd82b46739c68f731072b3203f7b7a8298c27dfa01671bad68f5bd7e",
    "solver": "scipy.optimize.milp (HiGHS)",
    "solver_version": "runtime-detected",
    "random_seed": 2026,
    "tolerance": 1.0e-8,
    "iteration_or_time_limit": "300 seconds",
    "expected_workbook": "问题一求解/问题一求解结果.xlsx",
    "allow_reduced_data": False,
    "allow_coarser_grid": False,
    "allow_shorter_horizon": False,
    "allow_fewer_repetitions": False,
    "allow_relaxed_tolerance": False,
    "allow_silent_solver_fallback": False,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_root(script_path: Path) -> Path:
    return script_path.resolve().parents[1]


def load_data(root: Path) -> dict[str, Any]:
    path = root / FULL_FIDELITY_CONFIG["data_paths"][0]
    if not path.is_file():
        raise FileNotFoundError(f"缺少题面参数文件: {path}")
    actual_hash = sha256_file(path)
    if actual_hash != FULL_FIDELITY_CONFIG["data_sha256"]:
        raise ValueError(
            "题面参数文件哈希与交付时锁定值不一致；请勿修改参数后继续运行。"
        )
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    validate_data(data)
    return data


def validate_data(data: dict[str, Any]) -> None:
    required = {
        "markets",
        "factories",
        "warehouses",
        "cost_factory_warehouse",
        "cost_warehouse_market",
        "cost_factory_market",
    }
    missing = sorted(required - set(data))
    if missing:
        raise ValueError(f"题面参数缺少字段: {missing}")
    markets = list(data["markets"])
    factories = list(data["factories"])
    warehouses = list(data["warehouses"])
    if (len(markets), len(factories), len(warehouses)) != (5, 4, 3):
        raise ValueError("市场/工厂/仓库数量与冻结题面口径不一致")
    if any(float(value) < 0 for value in data["markets"].values()):
        raise ValueError("市场需求不得为负")
    for factory in factories:
        row = data["factories"][factory]
        if min(float(row[key]) for key in ("capacity", "fixed_cost", "production_cost")) < 0:
            raise ValueError(f"工厂参数不得为负: {factory}")
        if set(data["cost_factory_warehouse"][factory]) != set(warehouses):
            raise ValueError(f"工厂到仓库成本矩阵列不完整: {factory}")
        if set(data["cost_factory_market"][factory]) != set(markets):
            raise ValueError(f"工厂直运成本矩阵列不完整: {factory}")
    for warehouse in warehouses:
        row = data["warehouses"][warehouse]
        if min(float(row[key]) for key in ("capacity", "fixed_cost", "handling_cost")) < 0:
            raise ValueError(f"仓库参数不得为负: {warehouse}")
        if set(data["cost_warehouse_market"][warehouse]) != set(markets):
            raise ValueError(f"仓库到市场成本矩阵列不完整: {warehouse}")


def build_index(data: dict[str, Any]) -> dict[str, Any]:
    factories = list(data["factories"])
    warehouses = list(data["warehouses"])
    markets = list(data["markets"])
    names: list[tuple[Any, ...]] = []
    names.extend(("y", factory) for factory in factories)
    names.extend(("z", warehouse) for warehouse in warehouses)
    names.extend(("xD", factory, market) for factory in factories for market in markets)
    names.extend(("xF", factory, warehouse) for factory in factories for warehouse in warehouses)
    names.extend(("xW", warehouse, market) for warehouse in warehouses for market in markets)
    return {
        "factories": factories,
        "warehouses": warehouses,
        "markets": markets,
        "names": names,
        "pos": {name: idx for idx, name in enumerate(names)},
    }


def objective_vector(data: dict[str, Any], idx: dict[str, Any]) -> np.ndarray:
    c = np.zeros(len(idx["names"]), dtype=float)
    pos = idx["pos"]
    for factory in idx["factories"]:
        f = data["factories"][factory]
        c[pos[("y", factory)]] = float(f["fixed_cost"])
        for market in idx["markets"]:
            c[pos[("xD", factory, market)]] = (
                float(f["production_cost"])
                + float(data["cost_factory_market"][factory][market])
            )
        for warehouse in idx["warehouses"]:
            c[pos[("xF", factory, warehouse)]] = (
                float(f["production_cost"])
                + float(data["cost_factory_warehouse"][factory][warehouse])
            )
    for warehouse in idx["warehouses"]:
        w = data["warehouses"][warehouse]
        c[pos[("z", warehouse)]] = float(w["fixed_cost"])
        for market in idx["markets"]:
            c[pos[("xW", warehouse, market)]] = (
                float(data["cost_warehouse_market"][warehouse][market])
                + float(w["handling_cost"])
            )
    return c


def build_constraints(data: dict[str, Any], idx: dict[str, Any]) -> LinearConstraint:
    pos = idx["pos"]
    rows: list[np.ndarray] = []
    lower: list[float] = []
    upper: list[float] = []
    n = len(idx["names"])
    for factory in idx["factories"]:
        row = np.zeros(n)
        for market in idx["markets"]:
            row[pos[("xD", factory, market)]] = 1.0
        for warehouse in idx["warehouses"]:
            row[pos[("xF", factory, warehouse)]] = 1.0
        row[pos[("y", factory)]] = -float(data["factories"][factory]["capacity"])
        rows.append(row)
        lower.append(-np.inf)
        upper.append(0.0)
    for warehouse in idx["warehouses"]:
        row = np.zeros(n)
        for factory in idx["factories"]:
            row[pos[("xF", factory, warehouse)]] = 1.0
        for market in idx["markets"]:
            row[pos[("xW", warehouse, market)]] -= 1.0
        rows.append(row)
        lower.append(0.0)
        upper.append(0.0)
    for warehouse in idx["warehouses"]:
        row = np.zeros(n)
        for market in idx["markets"]:
            row[pos[("xW", warehouse, market)]] = 1.0
        row[pos[("z", warehouse)]] = -float(data["warehouses"][warehouse]["capacity"])
        rows.append(row)
        lower.append(-np.inf)
        upper.append(0.0)
    for market in idx["markets"]:
        row = np.zeros(n)
        for factory in idx["factories"]:
            row[pos[("xD", factory, market)]] = 1.0
        for warehouse in idx["warehouses"]:
            row[pos[("xW", warehouse, market)]] = 1.0
        demand = float(data["markets"][market])
        rows.append(row)
        lower.append(demand)
        upper.append(demand)
    return LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper))


def solve_milp(data: dict[str, Any], idx: dict[str, Any]) -> Any:
    c = objective_vector(data, idx)
    n = len(c)
    lower = np.zeros(n)
    upper = np.full(n, np.inf)
    integrality = np.zeros(n, dtype=int)
    for factory in idx["factories"]:
        j = idx["pos"][("y", factory)]
        upper[j] = 1.0
        integrality[j] = 1
    for warehouse in idx["warehouses"]:
        j = idx["pos"][("z", warehouse)]
        upper[j] = 1.0
        integrality[j] = 1
    result = milp(
        c=c,
        integrality=integrality,
        bounds=Bounds(lower, upper),
        constraints=build_constraints(data, idx),
        options={"time_limit": 300.0, "mip_rel_gap": 1.0e-9},
    )
    if not result.success or result.x is None:
        raise RuntimeError(f"MILP未得到可接受解: {result.message}")
    return result


def flow_lp_for_layout(
    data: dict[str, Any], idx: dict[str, Any], y: dict[str, int], z: dict[str, int]
) -> tuple[bool, float]:
    flow_names = [name for name in idx["names"] if name[0] in {"xD", "xF", "xW"}]
    fpos = {name: j for j, name in enumerate(flow_names)}
    c_full = objective_vector(data, idx)
    c = np.array([c_full[idx["pos"][name]] for name in flow_names])
    a_ub: list[np.ndarray] = []
    b_ub: list[float] = []
    a_eq: list[np.ndarray] = []
    b_eq: list[float] = []
    for factory in idx["factories"]:
        row = np.zeros(len(flow_names))
        for market in idx["markets"]:
            row[fpos[("xD", factory, market)]] = 1.0
        for warehouse in idx["warehouses"]:
            row[fpos[("xF", factory, warehouse)]] = 1.0
        a_ub.append(row)
        b_ub.append(float(data["factories"][factory]["capacity"]) * y[factory])
    for warehouse in idx["warehouses"]:
        row = np.zeros(len(flow_names))
        for factory in idx["factories"]:
            row[fpos[("xF", factory, warehouse)]] = 1.0
        for market in idx["markets"]:
            row[fpos[("xW", warehouse, market)]] -= 1.0
        a_eq.append(row)
        b_eq.append(0.0)
        cap_row = np.zeros(len(flow_names))
        for market in idx["markets"]:
            cap_row[fpos[("xW", warehouse, market)]] = 1.0
        a_ub.append(cap_row)
        b_ub.append(float(data["warehouses"][warehouse]["capacity"]) * z[warehouse])
    for market in idx["markets"]:
        row = np.zeros(len(flow_names))
        for factory in idx["factories"]:
            row[fpos[("xD", factory, market)]] = 1.0
        for warehouse in idx["warehouses"]:
            row[fpos[("xW", warehouse, market)]] = 1.0
        a_eq.append(row)
        b_eq.append(float(data["markets"][market]))
    result = linprog(
        c,
        A_ub=np.vstack(a_ub),
        b_ub=np.array(b_ub),
        A_eq=np.vstack(a_eq),
        b_eq=np.array(b_eq),
        bounds=(0.0, None),
        method="highs",
    )
    if not result.success:
        return False, np.inf
    fixed = sum(float(data["factories"][i]["fixed_cost"]) * y[i] for i in idx["factories"])
    fixed += sum(float(data["warehouses"][w]["fixed_cost"]) * z[w] for w in idx["warehouses"])
    return True, float(result.fun + fixed)


def enumerate_layouts(data: dict[str, Any], idx: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    facilities = idx["factories"] + idx["warehouses"]
    for bits in itertools.product((0, 1), repeat=len(facilities)):
        chosen = dict(zip(facilities, bits))
        y = {i: chosen[i] for i in idx["factories"]}
        z = {w: chosen[w] for w in idx["warehouses"]}
        total_factory_capacity = sum(
            float(data["factories"][i]["capacity"]) * y[i] for i in idx["factories"]
        )
        if total_factory_capacity + 1e-12 < sum(float(v) for v in data["markets"].values()):
            feasible, objective = False, np.inf
        else:
            feasible, objective = flow_lp_for_layout(data, idx, y, z)
        rows.append(
            {
                "工厂组合": ",".join(i for i in idx["factories"] if y[i]) or "无",
                "仓库组合": ",".join(w for w in idx["warehouses"] if z[w]) or "无",
                "可行性": bool(feasible),
                "目标值": objective if feasible else np.nan,
            }
        )
    frame = pd.DataFrame(rows)
    return frame.sort_values(["可行性", "目标值"], ascending=[False, True], na_position="last")


def unpack_solution(result: Any, idx: dict[str, Any]) -> dict[tuple[Any, ...], float]:
    values = {name: float(result.x[j]) for j, name in enumerate(idx["names"])}
    for name in list(values):
        if name[0] in {"y", "z"}:
            values[name] = float(round(values[name]))
    return values


def cost_breakdown(data: dict[str, Any], idx: dict[str, Any], v: dict[tuple[Any, ...], float]) -> dict[str, float]:
    fixed = sum(float(data["factories"][i]["fixed_cost"]) * v[("y", i)] for i in idx["factories"])
    fixed += sum(float(data["warehouses"][w]["fixed_cost"]) * v[("z", w)] for w in idx["warehouses"])
    production = 0.0
    transport = 0.0
    handling = 0.0
    for i in idx["factories"]:
        produced = sum(v[("xD", i, m)] for m in idx["markets"])
        produced += sum(v[("xF", i, w)] for w in idx["warehouses"])
        production += float(data["factories"][i]["production_cost"]) * produced
        transport += sum(
            float(data["cost_factory_market"][i][m]) * v[("xD", i, m)] for m in idx["markets"]
        )
        transport += sum(
            float(data["cost_factory_warehouse"][i][w]) * v[("xF", i, w)] for w in idx["warehouses"]
        )
    for w in idx["warehouses"]:
        shipped = sum(v[("xW", w, m)] for m in idx["markets"])
        handling += float(data["warehouses"][w]["handling_cost"]) * shipped
        transport += sum(
            float(data["cost_warehouse_market"][w][m]) * v[("xW", w, m)] for m in idx["markets"]
        )
    return {
        "固定设施成本": fixed,
        "生产成本": production,
        "运输成本": transport,
        "仓库中转成本": handling,
        "总成本": fixed + production + transport + handling,
    }


def constraint_frames(
    data: dict[str, Any], idx: dict[str, Any], v: dict[tuple[Any, ...], float]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    tol = float(FULL_FIDELITY_CONFIG["tolerance"])
    checks: list[dict[str, Any]] = []
    conservation: list[dict[str, Any]] = []
    for i in idx["factories"]:
        used = sum(v[("xD", i, m)] for m in idx["markets"])
        used += sum(v[("xF", i, w)] for w in idx["warehouses"])
        bound = float(data["factories"][i]["capacity"]) * v[("y", i)]
        violation = max(0.0, used - bound)
        checks.append({"约束编号": f"FC-{i}", "约束含义": "工厂产能", "违反量": violation, "容差": tol, "是否满足": violation <= tol, "左端值": used, "右端值或界": bound})
    for w in idx["warehouses"]:
        inflow = sum(v[("xF", i, w)] for i in idx["factories"])
        outflow = sum(v[("xW", w, m)] for m in idx["markets"])
        residual = inflow - outflow
        conservation.append({"守恒量": f"仓库{w}流量", "残差": residual, "容差": tol, "是否满足": abs(residual) <= tol})
        checks.append({"约束编号": f"WB-{w}", "约束含义": "仓库流量守恒", "违反量": abs(residual), "容差": tol, "是否满足": abs(residual) <= tol, "左端值": inflow, "右端值或界": outflow})
        bound = float(data["warehouses"][w]["capacity"]) * v[("z", w)]
        violation = max(0.0, outflow - bound)
        checks.append({"约束编号": f"WC-{w}", "约束含义": "仓库容量", "违反量": violation, "容差": tol, "是否满足": violation <= tol, "左端值": outflow, "右端值或界": bound})
    for m in idx["markets"]:
        delivered = sum(v[("xD", i, m)] for i in idx["factories"])
        delivered += sum(v[("xW", w, m)] for w in idx["warehouses"])
        demand = float(data["markets"][m])
        residual = delivered - demand
        conservation.append({"守恒量": f"市场{m}需求平衡", "残差": residual, "容差": tol, "是否满足": abs(residual) <= tol})
        checks.append({"约束编号": f"MD-{m}", "约束含义": "市场需求满足", "违反量": abs(residual), "容差": tol, "是否满足": abs(residual) <= tol, "左端值": delivered, "右端值或界": demand})
    return pd.DataFrame(checks), pd.DataFrame(conservation)


def result_tables(
    data: dict[str, Any], idx: dict[str, Any], v: dict[tuple[Any, ...], float]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    decision_rows: list[dict[str, Any]] = []
    path_rows: list[dict[str, Any]] = []
    node_rows: list[dict[str, Any]] = []
    for name, value in v.items():
        unit = "0/1" if name[0] in {"y", "z"} else "千件/年"
        decision_rows.append({"变量": ":".join(map(str, name)), "取值": value, "单位": unit})
    for i in idx["factories"]:
        used = sum(v[("xD", i, m)] for m in idx["markets"])
        used += sum(v[("xF", i, w)] for w in idx["warehouses"])
        cap = float(data["factories"][i]["capacity"])
        node_rows.append({"节点": i, "数值": used / cap if cap else 0.0, "类别": "工厂产能利用率", "单位": "比例"})
        for m in idx["markets"]:
            value = v[("xD", i, m)]
            path_rows.append({"路径或流": f"{i}->{m}", "起点": i, "终点": m, "数值": value, "成本": float(data["cost_factory_market"][i][m]), "单位": "千件/年", "类型": "直运"})
        for w in idx["warehouses"]:
            value = v[("xF", i, w)]
            path_rows.append({"路径或流": f"{i}->{w}", "起点": i, "终点": w, "数值": value, "成本": float(data["cost_factory_warehouse"][i][w]), "单位": "千件/年", "类型": "工厂至仓库"})
    for w in idx["warehouses"]:
        outflow = sum(v[("xW", w, m)] for m in idx["markets"])
        cap = float(data["warehouses"][w]["capacity"])
        node_rows.append({"节点": w, "数值": outflow / cap if cap else 0.0, "类别": "仓库容量利用率", "单位": "比例"})
        for m in idx["markets"]:
            value = v[("xW", w, m)]
            path_rows.append({"路径或流": f"{w}->{m}", "起点": w, "终点": m, "数值": value, "成本": float(data["cost_warehouse_market"][w][m]) + float(data["warehouses"][w]["handling_cost"]), "单位": "千件/年", "类型": "仓库至市场含中转"})
    return pd.DataFrame(decision_rows), pd.DataFrame(path_rows), pd.DataFrame(node_rows)


def data_audit_frame(data: dict[str, Any]) -> pd.DataFrame:
    demand = sum(float(v) for v in data["markets"].values())
    capacity = sum(float(v["capacity"]) for v in data["factories"].values())
    return pd.DataFrame(
        [
            {"等级": "Info", "检查项": "市场数量", "信息": len(data["markets"]), "处理方式": "原样使用"},
            {"等级": "Info", "检查项": "工厂数量", "信息": len(data["factories"]), "处理方式": "原样使用"},
            {"等级": "Info", "检查项": "仓库数量", "信息": len(data["warehouses"]), "处理方式": "原样使用"},
            {"等级": "Info", "检查项": "年度总需求", "信息": demand, "处理方式": "原样使用，单位千件/年"},
            {"等级": "Info", "检查项": "候选工厂总产能", "信息": capacity, "处理方式": "原样使用，单位千件/年"},
            {"等级": "Pass", "检查项": "全开产能可行性", "信息": capacity >= demand, "处理方式": "通过"},
            {"等级": "Pass", "检查项": "数据哈希", "信息": FULL_FIDELITY_CONFIG["data_sha256"], "处理方式": "与交付锁定哈希一致"},
            {"等级": "Pass", "检查项": "预处理决策", "信息": "not_needed", "处理方式": "不执行插值、标准化、异常删除等变换"},
        ]
    )


def quality_frame(result: Any, objective: float, enum_best: float, checks: pd.DataFrame) -> pd.DataFrame:
    tol = float(FULL_FIDELITY_CONFIG["tolerance"])
    max_violation = float(checks["违反量"].max())
    mip_gap = float(getattr(result, "mip_gap", np.nan))
    enum_gap = abs(objective - enum_best)
    items = [
        ("求解器成功终止", bool(result.success), str(result.message)),
        ("最大约束违反量", max_violation <= tol, f"max={max_violation:.3e}, tol={tol:.1e}"),
        ("MILP最优间隙", np.isfinite(mip_gap) and mip_gap <= 1.0e-8, f"mip_gap={mip_gap:.3e}"),
        ("枚举+LP精确交叉验证", enum_gap <= 1.0e-6, f"|MILP-enum|={enum_gap:.3e}"),
    ]
    return pd.DataFrame([{"检查项": name, "是否通过": passed, "证据": evidence} for name, passed, evidence in items])


def runtime_config_frame(script: Path, result: Any) -> pd.DataFrame:
    rows = {
        "execution_owner": "user",
        "execution_profile": "full_fidelity",
        "stage": "primary",
        "problem_name": "问题一",
        "code_sha256": sha256_file(script),
        "data_sha256": FULL_FIDELITY_CONFIG["data_sha256"],
        "solver": FULL_FIDELITY_CONFIG["solver"],
        "solver_version": scipy.__version__,
        "tolerance": FULL_FIDELITY_CONFIG["tolerance"],
        "iteration_or_time_limit": FULL_FIDELITY_CONFIG["iteration_or_time_limit"],
        "actual_stop_reason": str(result.message),
        "random_seed": FULL_FIDELITY_CONFIG["random_seed"],
        "repetitions_or_scenarios": "deterministic MILP + 128 facility-layout LP cross-check",
        "grid_or_time_range": "annual static network",
        "fallback_used": False,
        "platform": platform.platform(),
        "allow_reduced_data": False,
        "allow_coarser_grid": False,
        "allow_shorter_horizon": False,
        "allow_fewer_repetitions": False,
        "allow_relaxed_tolerance": False,
        "allow_silent_solver_fallback": False,
    }
    return pd.DataFrame({"项目": list(rows), "值": [rows[key] for key in rows]})


def write_workbook(
    script: Path,
    data: dict[str, Any],
    idx: dict[str, Any],
    result: Any,
    values: dict[tuple[Any, ...], float],
    enumeration: pd.DataFrame,
) -> Path:
    root = project_root(script)
    out = root / FULL_FIDELITY_CONFIG["expected_workbook"]
    out.parent.mkdir(parents=True, exist_ok=True)
    costs = cost_breakdown(data, idx, values)
    checks, conservation = constraint_frames(data, idx, values)
    decisions, paths, nodes = result_tables(data, idx, values)
    enum_best = float(enumeration.loc[enumeration["可行性"], "目标值"].min())
    quality = quality_frame(result, costs["总成本"], enum_best, checks)
    opened_factories = ",".join(i for i in idx["factories"] if values[("y", i)] > 0.5) or "无"
    opened_warehouses = ",".join(w for w in idx["warehouses"] if values[("z", w)] > 0.5) or "无"
    recommendation = pd.DataFrame(
        [{"方案": f"工厂[{opened_factories}]；仓库[{opened_warehouses}]", "目标值": costs["总成本"], "单位": "万元/年", "排名": 1, "选择理由": "MILP最优且与128组合枚举+LP交叉验证一致"}]
    )
    core = pd.DataFrame(
        [
            {"指标": "最低年度总成本", "数值": costs["总成本"], "单位": "万元/年", "统计口径": "确定性年度最优"},
            {"指标": "固定设施成本", "数值": costs["固定设施成本"], "单位": "万元/年", "统计口径": "启用设施年化固定成本"},
            {"指标": "生产成本", "数值": costs["生产成本"], "单位": "万元/年", "统计口径": "单位生产成本×产量"},
            {"指标": "运输成本", "数值": costs["运输成本"], "单位": "万元/年", "统计口径": "全部运输边成本"},
            {"指标": "仓库中转成本", "数值": costs["仓库中转成本"], "单位": "万元/年", "统计口径": "仓库出库量×中转费"},
            {"指标": "最大约束违反量", "数值": float(checks["违反量"].max()), "单位": "千件/年", "统计口径": "全部硬约束"},
            {"指标": "MIP gap", "数值": float(getattr(result, "mip_gap", np.nan)), "单位": "比例", "统计口径": "HiGHS终止值"},
            {"指标": "枚举交叉验证差", "数值": abs(costs["总成本"] - enum_best), "单位": "万元/年", "统计口径": "MILP与128组合最优值之差"},
        ]
    )
    cost_df = pd.DataFrame({"成本项": list(costs), "数值": list(costs.values()), "单位": "万元/年"})
    with pd.ExcelWriter(out, engine="openpyxl") as writer:
        runtime_config_frame(script, result).to_excel(writer, sheet_name="运行配置", index=False)
        core.to_excel(writer, sheet_name="核心指标", index=False)
        data_audit_frame(data).to_excel(writer, sheet_name="数据审计", index=False)
        quality.to_excel(writer, sheet_name="主结果质量门", index=False)
        recommendation.to_excel(writer, sheet_name="推荐方案", index=False)
        decisions.to_excel(writer, sheet_name="决策变量明细", index=False)
        paths.to_excel(writer, sheet_name="路径或流结果", index=False)
        nodes.to_excel(writer, sheet_name="节点结果", index=False)
        checks.to_excel(writer, sheet_name="约束违反检查", index=False)
        conservation.to_excel(writer, sheet_name="守恒残差", index=False)
        cost_df.to_excel(writer, sheet_name="成本分解", index=False)
        enumeration.to_excel(writer, sheet_name="枚举验证", index=False)
    return out


def main() -> None:
    np.random.seed(FULL_FIDELITY_CONFIG["random_seed"])
    script = Path(__file__).resolve()
    data = load_data(project_root(script))
    idx = build_index(data)
    result = solve_milp(data, idx)
    values = unpack_solution(result, idx)
    enumeration = enumerate_layouts(data, idx)
    write_workbook(script, data, idx, result, values, enumeration)


if __name__ == "__main__":
    main()
