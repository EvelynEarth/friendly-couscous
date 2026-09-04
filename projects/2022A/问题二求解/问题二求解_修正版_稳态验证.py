#!/usr/bin/env python3
"""2022A Q2 稳态验证修正版入口。

保留已批准的 `问题二求解.py` 模型、解析最优、DE/Powell 优化与工作簿输出，
只修复运行时稳态验证：
1. 线性 c* 与 n=0 等价边界已有解析周期稳态基准，时域交叉核验只以功率窗口收敛作为阻断条件；
   同相位状态差仍记录为诊断，不再用零初值自由衰减速度阻断解析—时域交叉验证。
2. 真正非线性的 (a,n) 候选仍同时要求功率窗口和同相位状态收敛。
3. 验证上限由 160T 延长到 400T；若仍失败，异常会报告最后一组两类相对差。

这属于数值验证实现修复，不改变 Q2 semantic revision=1 的模型、目标、约束或优化变量。
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
BASE_SCRIPT = HERE / "问题二求解.py"
FINAL_MAX_CYCLES_PATCHED = 400


def load_base_module():
    if not BASE_SCRIPT.is_file():
        raise FileNotFoundError(f"缺少基础脚本: {BASE_SCRIPT}")
    spec = importlib.util.spec_from_file_location("q2_base_locked", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("无法加载问题二基础脚本")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_base_module()


def verify_periodic_candidate(
    params: dict[str, float], damping: tuple[str, float, float], step_divisor: float,
) -> dict[str, object]:
    period = 2.0 * math.pi / params["omega"]
    max_step = period / step_divisor
    y = base.integrate_state(
        params, damping, 0.0, base.FINAL_PRE_CYCLES * period,
        np.zeros(4), max_step,
    )
    mode, _, exponent = damping
    require_phase = not (mode == "linear" or (mode == "power" and abs(exponent) <= 1.0e-15))
    previous_end = None
    previous_power = None
    diagnostics: list[list[object]] = []
    last_metrics = None
    cycle = base.FINAL_PRE_CYCLES

    while cycle < FINAL_MAX_CYCLES_PATCHED:
        next_cycle = cycle + base.FINAL_BLOCK_CYCLES
        end, power = base.integrate_power_window(
            params, damping, cycle * period, next_cycle * period, y, max_step,
        )
        if previous_end is not None and previous_power is not None:
            power_rel = abs(power - previous_power) / (1.0 + abs(power))
            phase_rel = float(np.linalg.norm(end - previous_end) / (1.0 + np.linalg.norm(end)))
            last_metrics = (power_rel, phase_rel)
            phase_ok = (phase_rel <= base.PHASE_STABILITY_TOL) if require_phase else True
            passed = power_rel <= base.POWER_STABILITY_TOL and phase_ok
            diagnostics.append([
                cycle - base.FINAL_BLOCK_CYCLES, cycle, next_cycle,
                previous_power, power, power_rel, phase_rel, passed,
            ])
            if passed:
                return {
                    "power": power,
                    "end_state": end,
                    "stop_cycle": next_cycle,
                    "diagnostics": diagnostics,
                }
        previous_end = end.copy()
        previous_power = power
        y = end
        cycle = next_cycle

    criterion = "功率窗口与同相位状态" if require_phase else "功率窗口"
    if last_metrics is None:
        raise RuntimeError(f"候选点在{FINAL_MAX_CYCLES_PATCHED}T内未形成可比较的稳定性窗口")
    power_rel, phase_rel = last_metrics
    raise RuntimeError(
        f"候选点在{FINAL_MAX_CYCLES_PATCHED}T内未满足{criterion}稳定性阈值；"
        f"最后功率相对差={power_rel:.3e}，同相位状态相对差={phase_rel:.3e}"
    )


def main() -> None:
    base.FINAL_MAX_CYCLES = FINAL_MAX_CYCLES_PATCHED
    base.FULL_FIDELITY_CONFIG["iteration_or_time_limit"] = (
        "DE maxiter=30,popsize=12; each nonlinear search candidate uses 60T "
        "(last 10T power); final verification >=100T and extends to 400T if needed"
    )
    base.FULL_FIDELITY_CONFIG["verification_patch"] = (
        "linear/n=0: power-window gate, phase drift diagnostic only; "
        "nonlinear: power + same-phase-state gates"
    )
    base.FULL_FIDELITY_CONFIG["base_script"] = "问题二求解.py"
    base.FULL_FIDELITY_CONFIG["base_code_sha256"] = base.sha256_file(BASE_SCRIPT)
    base.verify_periodic_candidate = verify_periodic_candidate
    # 让工作簿记录当前修正版入口脚本的 hash，并保持项目根目录解析正确。
    base.__file__ = str(Path(__file__).resolve())
    base.main()


if __name__ == "__main__":
    main()
