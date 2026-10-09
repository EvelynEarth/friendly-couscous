#!/usr/bin/env python3
"""Check same-sample metric identities; this is not independent model evaluation."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Any

def check_record(item: dict[str, Any]) -> dict[str, Any]:
    key = str(item.get("experiment_id", "unknown"))
    proof = item.get("comparability", {})
    mandatory = ("same_samples", "same_weights", "same_error_scale")
    absent = [x for x in mandatory if proof.get(x) is not True]
    if absent:
        return {"experiment_id":key,"status":"not_comparable_requires_review",
                "reason":"Metric comparability has not been evidenced: "+", ".join(absent)}
    metrics = item.get("metrics", {})
    if any(k not in metrics for k in ("MSE", "RMSE")):
        return {"experiment_id":key,"status":"not_comparable_requires_review",
                "reason":"Both MSE and RMSE are needed for the identity."}
    try:
        mse, rmse = float(metrics["MSE"]), float(metrics["RMSE"])
        mae = float(metrics["MAE"]) if "MAE" in metrics else None
    except (ValueError, TypeError):
        return {"experiment_id":key,"status":"blocked","reason":"Non-numeric metric values."}
    if not all(math.isfinite(x) and x >= 0 for x in [mse, rmse]+([] if mae is None else [mae])):
        return {"experiment_id":key,"status":"blocked","reason":"Non-finite or negative error metric."}
    # Rounding to 4 decimals can induce 1e-4-level discrepancy in squared RMSE.
    tolerance = float(item.get("rounding_tolerance_mse", 0.00015))
    if not math.isfinite(tolerance) or tolerance < 0 or tolerance > 0.01:
        return {"experiment_id":key,"status":"blocked","reason":"Unreasonable or invalid rounding tolerance."}
    implied = rmse**2
    discrepancies=[]
    if abs(mse-implied) > tolerance:
        discrepancies.append(f"MSE={mse:g} but RMSE^2={implied:.8g} exceeds allowed absolute MSE difference {tolerance:g}")
    if mae is not None and mae > rmse+tolerance:
        discrepancies.append(f"MAE={mae:g} exceeds RMSE={rmse:g} for claimed same sample/weight/scale")
    return {"experiment_id":key, "status":"blocked" if discrepancies else "arithmetic_consistent_not_scientifically_verified",
            "mse":mse,"rmse":rmse,"mae":mae,"implied_mse":round(implied,12),
            "rounding_tolerance_mse":tolerance,"issues":discrepancies}

def audit(payload: dict[str,Any]) -> dict[str,Any]:
    items = payload.get("checks")
    if not isinstance(items,list) or not items:
        return {"status":"blocked","reason":"Supply nonempty checks list with experiment data.","records":[]}
    rows=[check_record(x) for x in items]
    blocked=any(x["status"]=="blocked" for x in rows)
    pending=any(x["status"]=="not_comparable_requires_review" for x in rows)
    return {"status":"blocked" if blocked else ("requires_human_comparability_review" if pending else "arithmetic_consistent_only"),
            "records":rows,"scope":"Checks declared same-sample reported values only, not source predictions, experiment reproducibility or genuine mathematical correctness."}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--report",type=Path)
    args=p.parse_args()
    ans=audit(json.loads(args.input.read_text(encoding="utf-8")))
    print(json.dumps(ans,ensure_ascii=False,indent=2))
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(ans,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return 1 if ans["status"]=="blocked" else (2 if ans["status"]=="requires_human_comparability_review" else 0)

if __name__=="__main__":
    raise SystemExit(main())
