#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""2025仿真建模A题原始数据一致性检查；不执行FactorySimulation。"""
from pathlib import Path
import csv
from decimal import Decimal

DATA = Path(__file__).resolve().parent.parent / "data"


def load_csv(name):
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    ops = load_csv("operations.csv")
    orders = load_csv("orders.csv")
    assert len(ops) == 14 and [int(o["op_id"]) for o in ops] == list(range(1, 15))
    assert sum(Decimal(o["process_time_s"]) for o in ops) == Decimal("124.9")
    assert sum(int(o["workers_listed"]) for o in ops) == 33
    assert sum(int(o["move_distance_m"]) for o in ops) == 25
    assert len(orders) == 11 and len({o["order_id"] for o in orders}) == 11
    assert sum(int(o["quantity"]) for o in orders if o["emergency"] == "0") == 241
    assert sum(int(o["quantity"]) for o in orders) == 253
    assert all(int(o["quantity"]) > 0 and int(o["due_s"]) >= 0 for o in orders)
    o8 = next(o for o in orders if o["order_id"] == "O8")
    assert int(o8["due_s"]) - int(o8["release_s"]) == 68
    assert Decimal(68) < sum(Decimal(o["process_time_s"]) for o in ops)
    print("PASS: 工序14道/124.9秒/33人/25米; 原始241件+插单12件=253件")
    print("WARNING: O8交期窗仅68秒，小于串行工序标称时间124.9秒")
    print("WARNING: 1028件/小时、8线人员和设备作用域、运输时长、工序10批处理等仍待语义确认")
    print("NOTE: 静态检查通过不表示FactorySimulation模型已运行或科学模型已验证")


if __name__ == "__main__":
    main()
