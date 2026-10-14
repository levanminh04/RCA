"""T-032 bản 013 mục 2 (KT-12): chuỗi cột độ trễ của root ở ba cặp ca cùng ô. Chạy trên EC2. Không đổi bước tính nào.

Mỗi ca một tiến trình con chạy đúng đường phát lại BARO native (hàm one của contrast_baro_b1_v1.py, nhánh sham) với một lớp bọc
chỉ-đọc quanh p3.adapters.baro.chay để lưu bảng metric mà phương pháp nhận. Bản ghi phải khớp bản đóng băng từng bit, nếu không
thì ca đó không được dùng. Sau đó chỉ đọc: thống kê từng cột của root và của các dịch vụ gọi trực tiếp root, in nguyên chuỗi cột độ trễ
của root, đối chiếu với bảng lời gọi chậm (runs/call-slow-001).

Dùng:
  python root_latency_series_v1.py <thư mục lượt mới>                       (chạy 7 ca rồi tổng hợp)
  python root_latency_series_v1.py one <RE2-TT|Nezha-OB> <opaque_id> <thư mục mới>
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
PYTHON = "/home/ubuntu/rca/T-025/envs/main/bin/python"
sys.path.insert(0, str(BASE / "scripts"))
PAIRS = {
    "ts-auth-service|delay": [("RE2-TT", "dev-746fd74313"), ("RE2-TT", "dev-57546fd87b"), ("RE2-TT", "dev-f81f88234e")],
    "recommendationservice|network_delay": [("Nezha-OB", "dev-5467884de4"), ("Nezha-OB", "dev-63c30faf34")],
    "checkoutservice|network_delay": [("Nezha-OB", "dev-2bfc97b01e"), ("Nezha-OB", "dev-607751ac0a")],
}
SPANPASS = BASE / "runs/chain-spanpass-001"
CALLSLOW = BASE / "runs/call-slow-001"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def one(dataset, opaque_id, directory):
    import contrast_baro_b1_v1 as b1
    from p3.adapters import baro as adapter
    native = adapter.chay
    holder = {}

    def observed(metric_win, t):
        holder["frame"], holder["t"] = metric_win.copy(), t
        return native(metric_win, t)

    adapter.chay = observed   # lớp bọc chỉ-đọc; worker và adapter Nezha nạp tên này lúc được gọi
    code = b1.one("sham", dataset, opaque_id, directory)
    directory = Path(directory)
    if "frame" not in holder:
        raise RuntimeError("không bắt được bảng metric")
    holder["frame"].to_parquet(directory / "metric-frame.parquet")
    (directory / "capture.json").write_text(json.dumps({"t": int(holder["t"]), "rows": int(len(holder["frame"])),
                                                        "columns": int(holder["frame"].shape[1])}) + "\n", encoding="utf-8")
    return code


def column_stats(time_rel, values, before, after):
    import numpy as np
    n, a = values[before], values[after]
    fn, fa = n[np.isfinite(n)], a[np.isfinite(a)]
    out = {"n_N": int(len(n)), "n_A": int(len(a)), "missing_N": int(len(n) - len(fn)), "missing_A": int(len(a) - len(fa)),
           "distinct_N": int(len(set(fn.tolist()))), "distinct_A": int(len(set(fa.tolist()))),
           "nonzero_N": int((fn != 0).sum()), "nonzero_A": int((fa != 0).sum())}
    if len(fn) < 2 or len(fa) < 1:
        return out
    med, q25, q75 = float(np.median(fn)), float(np.percentile(fn, 25)), float(np.percentile(fn, 75))
    mean, std = float(fn.mean()), float(fn.std(ddof=0))
    out.update({"median_N": med, "iqr_N": q75 - q25, "mean_N": mean, "std_N": std, "median_A": float(np.median(fa)), "max_A": float(fa.max()),
                "robust_z_max": None if q75 == q25 else float((fa.max() - med) / (q75 - q25)),
                "z_max": None if std == 0 else float((fa.max() - mean) / std),
                "votes_A_gt_mean_3std": int((fa > mean + 3 * std).sum())})
    over = np.flatnonzero(np.isfinite(a) & (a > mean + 3 * std))
    out["first_exceed_s_after_t"] = float(time_rel[after][over[0]]) if len(over) else None
    return out


def analyse(dataset, opaque_id, directory, label):
    import numpy as np
    import pandas as pd
    import chain_position_v1 as cp
    from p3.adapters import baro as adapter
    from p3.ban_ghi import thuc_the_metric
    check = read(directory / "check.json")
    cap = read(directory / "capture.json")
    record = read(directory / "ban-ghi-0.json")
    root = label["root"]
    item = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": label["fault"], "cell": label["cell"],
            "exact_vs_frozen": check["exact_vs_frozen"], "t": cap["t"]}
    if not check["exact_vs_frozen"]:
        item["status"] = "LỆCH BẢN ĐÓNG BĂNG, không dùng"
        return item
    frame = pd.read_parquet(directory / "metric-frame.parquet")
    data = adapter.chuan_bi(frame)   # đổi tên cột như adapter; hàm thuần
    t = cap["t"]
    unit = 1e9 if t > 1e15 else 1.0
    time_rel = (data["time"].to_numpy(dtype="float64") - t) / unit
    before, after = time_rel < 0, time_rel >= 0
    scores = {r["item"]: r["key"][0] if isinstance(r.get("key"), list) else r.get("score") for r in record.get("ranking", [])}
    sp = read(SPANPASS / "cases" / (dataset + "-" + opaque_id + ".json"))
    g = cp.Graph(sp["services"], [(e["caller"], e["callee"]) for e in sp["edges"].values()])
    callers = sorted(s for s in sp["services"] if g.reach(s).get(root) == 1)
    item.update({"status": "OK", "rows": int(len(data)), "rows_N": int(before.sum()), "rows_A": int(after.sum()),
                 "time_span_s": [float(time_rel.min()), float(time_rel.max())], "callers_of_root": callers, "root_in_trace": root in sp["services"]})
    columns = {}
    for column in data.columns:
        if column == "time":
            continue
        entity = thuc_the_metric(column)
        if entity != root and entity not in callers:
            continue
        values = pd.to_numeric(data[column], errors="coerce").to_numpy(dtype="float64")
        stats = column_stats(time_rel, values, before, after)
        stats.update({"entity": entity, "is_root": entity == root, "latency": "latency" in column.lower(), "frozen_score": scores.get(column)})
        if entity == root and stats["latency"]:
            stats["series_N"] = [None if not np.isfinite(v) else float(v) for v in values[before]]
            stats["series_A"] = [None if not np.isfinite(v) else float(v) for v in values[after]]
            stats["time_A_s"] = [float(v) for v in time_rel[after]]
        columns[column] = stats
    item["columns"] = columns
    slow = read(CALLSLOW / "cases" / (dataset + "-" + opaque_id + ".json"))["edges"]
    into = {k: v for k, v in slow.items() if v["callee"] == root}
    item["calls_into_root"] = into
    nb, na, ns = (sum(v[k] for v in into.values()) for k in ("n_before", "n_after", "n_slow_after"))
    inside = sum(v.get("slow_inside_callee_span", 0) for v in into.values())
    item["calls_into_root_total"] = {"edges": len(into), "n_before": nb, "n_after": na, "n_slow_after": ns, "slow_share_after": ns / na if na else None,
                                     "slow_inside_root_span": inside, "inside_share_of_slow": inside / ns if ns else None}
    root_lat = {c: v for c, v in columns.items() if v["is_root"] and v["latency"]}
    best = max(root_lat, key=lambda c: (root_lat[c].get("robust_z_max") if root_lat[c].get("robust_z_max") is not None else float("-inf")), default=None)
    item["root_latency_columns"] = sorted(root_lat)
    item["root_best_latency_column"] = best
    item["root_best_latency_robust_z"] = root_lat[best].get("robust_z_max") if best else None
    item["root_best_column_any"] = max((c for c, v in columns.items() if v["is_root"] and v.get("robust_z_max") is not None),
                                       key=lambda c: columns[c]["robust_z_max"], default=None)
    return item


def main():
    args = sys.argv[1:]
    if len(args) == 4 and args[0] == "one":
        return one(*args[1:])
    out = Path(args[0])
    out.mkdir(parents=True, exist_ok=False)
    labels = {(r["dataset"], r["opaque_id"]): r for r in read(BASE / "repo/results/T-028/runs/phan-hoi-review-001/ca-sai.json")["main_rows"] if r["method"] == "baro"}
    env = dict(os.environ)
    cases, progress = {}, (out / "progress.jsonl").open("a", encoding="utf-8")
    for cell, members in PAIRS.items():
        for dataset, opaque_id in members:
            directory = out / "cases" / dataset / opaque_id
            directory.parent.mkdir(parents=True, exist_ok=True)
            began = time.time()
            child = subprocess.run([PYTHON, "-B", "-X", "utf8", str(Path(__file__).resolve()), "one", dataset, opaque_id, str(directory)],
                                   cwd=str(BASE), env=env, capture_output=True, text=True)
            line = {"dataset": dataset, "opaque_id": opaque_id, "exit_code": child.returncode, "wall_s": round(time.time() - began, 1)}
            if child.returncode != 0 or not (directory / "check.json").is_file():
                line["stderr_tail"] = child.stderr[-2000:]
                cases[opaque_id] = {"dataset": dataset, "opaque_id": opaque_id, "status": "TOOL_ERROR", "error": child.stderr[-500:]}
            else:
                label = labels[(dataset, opaque_id)]
                if label["cell"] != cell:
                    raise SystemExit("ô của ca khác ô đã khai: " + opaque_id + " " + label["cell"])
                cases[opaque_id] = analyse(dataset, opaque_id, directory, label)
                line["exact_vs_frozen"] = cases[opaque_id]["exact_vs_frozen"]
            progress.write(json.dumps(line, ensure_ascii=False) + "\n"); progress.flush()
            print(json.dumps(line, ensure_ascii=False), flush=True)
    pairs = {}
    for cell, members in PAIRS.items():
        rows = [cases[i] for _d, i in members if cases[i].get("status") == "OK"]
        block = {"cases": [i for _d, i in members], "usable": [c["opaque_id"] for c in rows]}
        if len(rows) >= 2:
            z = lambda c: c["root_best_latency_robust_z"] if c["root_best_latency_robust_z"] is not None else float("-inf")   # noqa: E731
            react = max(rows, key=z)
            col = react["root_best_latency_column"]
            block.update({"reacting_case": react["opaque_id"], "column": col, "comparisons": []})
            for other in rows:
                if other is react:
                    continue
                a, b = react["columns"].get(col, {}), other["columns"].get(col)
                sa, sb = react["calls_into_root_total"], other["calls_into_root_total"]
                comp = {"other_case": other["opaque_id"], "column_present_in_other": b is not None,
                        "reacting": {k: a.get(k) for k in ("robust_z_max", "z_max", "nonzero_A", "distinct_A", "n_A", "missing_A", "median_N", "median_A", "max_A", "votes_A_gt_mean_3std", "frozen_score")},
                        "other": None if b is None else {k: b.get(k) for k in ("robust_z_max", "z_max", "nonzero_A", "distinct_A", "n_A", "missing_A", "median_N", "median_A", "max_A", "votes_A_gt_mean_3std", "frozen_score")},
                        "other_best_latency_column": other["root_best_latency_column"], "other_best_latency_robust_z": other["root_best_latency_robust_z"],
                        "slow_share_reacting": sa["slow_share_after"], "slow_share_other": sb["slow_share_after"],
                        "calls_after_reacting": sa["n_after"], "calls_after_other": sb["n_after"],
                        "inside_share_reacting": sa["inside_share_of_slow"], "inside_share_other": sb["inside_share_of_slow"]}
                if b is not None:
                    comp["mark_b_few_samples"] = bool(b["nonzero_A"] < 0.5 * a["nonzero_A"] or b["distinct_A"] < 0.5 * a["distinct_A"])
                    within = lambda x, y: x is not None and y is not None and min(x, y) > 0 and max(x, y) / min(x, y) <= 1.5   # noqa: E731
                    if sa["slow_share_after"] is not None and sb["slow_share_after"] is not None:
                        comp["mark_c_intensity"] = bool(sb["slow_share_after"] < 0.5 * sa["slow_share_after"])
                        comp["mark_a_wrong_place"] = bool(within(sa["slow_share_after"], sb["slow_share_after"]) and within(a["nonzero_A"], b["nonzero_A"]) and
                                                          (sa["inside_share_of_slow"] or 0) < 0.2 and (sb["inside_share_of_slow"] or 0) < 0.2)
                    else:
                        comp["mark_c_intensity"] = comp["mark_a_wrong_place"] = None
                block["comparisons"].append(comp)
        pairs[cell] = block
    result = {"schema": "T032-root-latency-series-v1", "design": "results/T-032/thiet-ke-phep-doi-013.md mục 2",
              "self_check": {"cases": len(cases), "exact_vs_frozen": sum(bool(c.get("exact_vs_frozen")) for c in cases.values())},
              "methods_executed": ["baro (đường native, lớp bọc chỉ-đọc)"], "pairs": pairs, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"self_check": result["self_check"], "pairs": pairs}, ensure_ascii=False, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
