"""T-032 bảng A (thiet-ke-bang-mo-ta-004.md mục 2): tín hiệu của root nằm ở đâu trong trace.

Chạy trên EC2, chỉ đọc bảng span adapter TraceRCA đã lưu của các ca phát lại khớp từng bit. Không gọi phương pháp,
không đổi phép tính, không chấm Hit. Mọi dịch vụ được tính ở năm vị trí trước; nhãn root và loại lỗi nối sau cùng.
Tự kiểm theo ca: tổng cờ own_d và own_u phải bằng H_native và H_u của lượt tracerca-core-td-001.
Dùng: python root_signal_location_v4.py <thư mục lượt mới> [dataset:opaque_id để chạy thử một ca] [--placebo-shift=-150]

Bản v4 = v3 + tùy chọn --placebo-midpoint (mục 4b) và ghi khoảng thời gian có span. Bản v3 = v2 + sửa lỗi cộng None ở phần tổng hợp khi chạy phép thử giả (v2 hỏng ở bước ghi summary; lượt root-signal-placebo-001 giữ lại). Bản v2 = v1 + phép thử giả (thiet-ke-bang-mo-ta-004.md mục 4): với --placebo-shift=-150, mốc giả là t-150 s;
nền là span kết thúc trước mốc giả, "sau mốc" là span kết thúc trong [t-150, t); span kết thúc từ t trở đi bị bỏ khỏi cờ.
Không có lỗi nào được tiêm trong khoảng đó, nên root không được đứng đầu thường xuyên hơn mức ngẫu nhiên.
Khi có phép thử giả, tự kiểm với H_native/H_u không áp dụng. Mọi phép tính khác y như v1.
"""
SHIFT_S = 0
MIDPOINT = False  # v4: mốc giả ở điểm giữa đoạn nền có span (thiet-ke-bang-mo-ta-004.md mục 4b)
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402 — dùng nguyên hàm uncovered, read, sha và các đường dẫn đã kiểm

TD_SUMMARY = BASE / "runs/tracerca-core-td-001/summary.json"
BARO = BASE / "runs/baro-b1-001/summary.json"
SIMPLE = BASE / "runs/simplerca-decomposition-002/summary.json"
POSITIONS = ("own_d", "own_u", "in_d", "in_u", "in_d_edge")


def baseline_flags(quantity_us, group, before, after):
    """Cờ theo đúng biểu thức native: q/1000 >= round(mean/1000,2) + 3*round(std/1000,2); std của pandas (ddof=1).

    Trả (flag, evaluable): evaluable sai khi nhóm không có đủ 2 span trước mốc (std không xác định) hoặc không có nền.
    """
    frame = pd.DataFrame({"q": pd.Series(quantity_us).reset_index(drop=True), "g": np.asarray(group, dtype=object)})
    stats = frame[before].groupby("g", sort=False)["q"].agg(["mean", "std", "count"])
    # round() của Python như RCAEval e2e/tracerca.py; giữ kiểu dữ liệu gốc của cột khi lấy mean, std
    mean_ms = stats["mean"].map(lambda v: round(float(v) / 1_000, 2) if pd.notna(v) else float("nan"))
    std_ms = stats["std"].map(lambda v: round(float(v) / 1_000, 2) if pd.notna(v) else float("nan"))
    m = frame["g"].map(mean_ms).to_numpy(dtype="float64")
    s = frame["g"].map(std_ms).to_numpy(dtype="float64")
    evaluable = after & ~np.isnan(m) & ~np.isnan(s)
    flag = evaluable & ((frame["q"] / 1_000).to_numpy(dtype="float64") >= m + 3 * s)
    return flag, evaluable


def rank_of(shares):
    """shares: {service: a/n}. Hạng theo tỷ lệ giảm dần; hòa ghi rank_min, rank_max."""
    out = {}
    values = list(shares.values())
    for service, x in shares.items():
        out[service] = (1 + sum(v > x for v in values), sum(v >= x for v in values))
    return out


def one_case(directory, table_columns):
    capture = directory / "capture"
    adapter = td.read(capture / "calls/001-adapter.json")
    spans = pd.DataFrame(table_columns(capture, adapter["entry"]["input"]))
    t_us = int(adapter["entry"]["t_seconds"]) * 1_000_000
    spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
    spans["operation"] = spans["serviceName"] + "_" + spans["methodName"]
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    if MIDPOINT:
        fake = t_us - (t_us - int(start.min())) // 2
        after = (start + duration >= fake) & (start + duration < t_us)
        before = start + duration < fake
    elif SHIFT_S:
        fake = t_us + SHIFT_S * 1_000_000
        after = (start + duration >= fake) & (start + duration < t_us)
        before = start + duration < fake
    else:
        after = start + duration >= t_us
        before = ~after
    u, covered, children, _resolved = td.uncovered(spans[["traceID", "spanID", "parentSpanID", "startTime", "duration"]].copy())
    service = spans["serviceName"].astype(str).to_numpy()
    operation = spans["operation"].astype(str).to_numpy()
    own_d, own_d_ok = baseline_flags(spans["duration"], operation, before, after)
    own_u, own_u_ok = baseline_flags(pd.array(u, dtype="Int64"), operation, before, after)  # kiểu như lượt T-D
    # cha theo vị trí dòng; định danh lặp không dùng làm cha (như uncovered)
    key = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(spans)), index=key)
    position = position[~position.index.duplicated(keep=False)]
    parent = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent)
    parent_index = np.where(has_parent, parent, 0).astype("int64")
    parent_service = np.where(has_parent, service[parent_index], None)
    cross = has_parent & (parent_service != service)
    calls = pd.DataFrame({"p": parent_index[cross], "callee": service[cross]}).drop_duplicates().reset_index(drop=True)
    p = calls["p"].to_numpy()
    calls["caller"] = service[p]
    edge_group = np.array([operation[i] + "→" + s for i, s in zip(p, calls["callee"])], dtype=object)
    edge_flag, edge_ok = baseline_flags(duration[p], edge_group, before[p], after[p])
    calls["after"] = after[p]
    calls["in_d"], calls["in_d_ok"] = own_d[p], own_d_ok[p]
    calls["in_u"], calls["in_u_ok"] = own_u[p], own_u_ok[p]
    calls["in_d_edge"], calls["in_d_edge_ok"] = edge_flag, edge_ok
    cross_children = np.zeros(len(spans), dtype="int64")
    np.add.at(cross_children, parent_index[cross], 1)
    entry = ~has_parent | cross
    services = sorted(set(service))
    table = {s: {} for s in services}
    own = pd.DataFrame({"s": service, "after": after, "own_d": own_d, "own_d_ok": own_d_ok, "own_u": own_u, "own_u_ok": own_u_ok,
                        "entry": entry, "caller_side": cross_children > 0})
    own_after = own[own["after"]]
    for s, g in own_after.groupby("s", sort=True):
        table[s]["own_d"] = {"n": int(g["own_d_ok"].sum()), "a": int(g["own_d"].sum()), "n_no_baseline": int((~g["own_d_ok"]).sum())}
        table[s]["own_u"] = {"n": int(g["own_u_ok"].sum()), "a": int(g["own_u"].sum()), "n_no_baseline": int((~g["own_u_ok"]).sum())}
        parts = {}
        for name, mask in (("entry", g["entry"]), ("internal", ~g["entry"]), ("caller_side", g["caller_side"])):
            h = g[mask]
            parts[name] = {"n": int(h["own_d_ok"].sum()), "a_d": int(h["own_d"].sum()), "a_u": int(h["own_u"].sum())}
        table[s]["own_split"] = parts
    calls_after = calls[calls["after"]]
    for s, g in calls_after.groupby("callee", sort=True):
        for name in ("in_d", "in_u", "in_d_edge"):
            table[s][name] = {"n": int(g[name + "_ok"].sum()), "a": int(g[name].sum()), "n_no_baseline": int((~g[name + "_ok"]).sum())}
        table[s]["callers"] = sorted(set(g["caller"]))
    for s in services:
        for name in POSITIONS:
            table[s].setdefault(name, {"n": 0, "a": 0, "n_no_baseline": 0})
    for name in POSITIONS:
        shares = {s: table[s][name]["a"] / table[s][name]["n"] for s in services if table[s][name]["n"] > 0}
        ranks = rank_of(shares)
        for s in services:
            item = table[s][name]
            item["share"] = shares.get(s)
            item["rank_min"], item["rank_max"] = ranks.get(s, (None, None))
            item["n_services_ranked"] = len(shares)
    structure = {"spans": int(len(spans)), "spans_after": int(after.sum()), "spans_before": int(before.sum()),
                 "earliest_start_minus_t_s": float((int(start.min()) - t_us) / 1e6), "latest_end_minus_t_s": float((int((start + duration).max()) - t_us) / 1e6),
                 "parent_resolved": int(has_parent.sum()),
                 "cross_service_child_spans": int(cross.sum()), "caller_side_spans": int((cross_children > 0).sum()),
                 "caller_side_spans_by_cross_children": {str(k): int(v) for k, v in
                                                         pd.Series(np.minimum(cross_children[cross_children > 0], 3)).value_counts().sort_index().items()},
                 "calls": int(len(calls)), "calls_after": int(calls["after"].sum()),
                 "total_own_d_flags": int(own_d.sum()), "total_own_u_flags": int(own_u.sum()),
                 "after_spans_without_baseline": int((after & ~own_d_ok).sum()),
                 "caller_side_operations_after": int(pd.Series(operation[p][after[p]]).nunique()) if len(p) else 0,
                 "edge_groups_after": int(pd.Series(edge_group[after[p]]).nunique()) if len(p) else 0}
    return {"t_seconds": int(adapter["entry"]["t_seconds"]), "structure": structure, "services": table}


def quantiles(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    global SHIFT_S, MIDPOINT
    MIDPOINT = "--placebo-midpoint" in sys.argv[2:]
    arguments = [a for a in sys.argv[2:] if not a.startswith("--placebo-")]
    for a in sys.argv[2:]:
        if a.startswith("--placebo-shift="):
            SHIFT_S = int(a.split("=", 1)[1])
            if SHIFT_S >= 0 or SHIFT_S <= -300:
                raise SystemExit("mốc giả phải nằm trong đoạn nền")
    only = arguments[0] if arguments else None
    fixtures = td.interval_fixtures()
    if not fixtures["pass"]:
        raise SystemExit("8 trường hợp khoảng tự dựng không đạt")
    from replay_tracerca_v3 import table_columns
    td_cases = {(c["dataset"], c["opaque_id"]): c for c in td.read(TD_SUMMARY)["cases"]}
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "tracerca"}
    baro = {(c["dataset"], c["opaque_id"]): c for c in td.read(BARO)["cases"]}
    simple = {(c["dataset"], c["opaque_id"]): c for c in td.read(SIMPLE)["cases"]}
    cases = []
    (out / "cases").mkdir()
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        key = (dataset, opaque_id)
        label = labels[key]
        base = {"dataset": dataset, "opaque_id": opaque_id, "root": label["root"], "fault": label["fault"], "cell": label["cell"]}
        if row["source_status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "nguồn TraceRCA " + row["source_status"] + ": không có bảng span đã lưu"})
            continue
        directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
        check = directory / "check.json"
        if not check.is_file() or td.read(check).get("status") != "PASS":
            cases.append({**base, "status": "N/A", "reason": "chưa có lượt phát lại khớp tuyệt đối"})
            continue
        try:
            computed = one_case(directory, table_columns)  # chưa dùng nhãn
        except Exception as error:
            cases.append({**base, "status": "TOOL_ERROR", "error": type(error).__name__ + ": " + str(error)[:300]})
            print(dataset, opaque_id, "TOOL_ERROR", error, flush=True)
            continue
        reference = td_cases[key]["counts"]
        if SHIFT_S or MIDPOINT:
            self_check = {"own_d_total_equals_H_native": None, "own_u_total_equals_H_u": None, "placebo_shift_s": SHIFT_S,
                          "placebo_midpoint": MIDPOINT}
        else:
            self_check = {"own_d_total_equals_H_native": computed["structure"]["total_own_d_flags"] == reference["H_native"],
                          "own_u_total_equals_H_u": computed["structure"]["total_own_u_flags"] == reference["H_u"],
                          "H_native": reference["H_native"], "H_u": reference["H_u"]}
        full = {**base, "status": "OK", "self_check": self_check, **computed, "check_sha256": td.sha(check)}
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps(full, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        # --- từ đây nối nhãn ---
        root = label["root"]
        services = computed["services"]
        item = {**base, "status": "OK", "self_check": self_check, "structure": computed["structure"],
                "n_services": len(services), "root_in_trace": root in services}
        if root in services:
            r = services[root]
            item["root"] = root
            item["root_positions"] = {name: r[name] for name in POSITIONS}
            item["root_own_split"] = r.get("own_split")
            item["root_callers"] = r.get("callers", [])
            item["root_first_positions"] = [n for n in POSITIONS if r[n]["rank_max"] == 1]
            item["root_top3_positions"] = [n for n in POSITIONS if r[n]["rank_max"] is not None and r[n]["rank_max"] <= 3]
            item["root_flagged_positions"] = [n for n in POSITIONS if r[n]["a"] > 0]
            item["top_service_by_position"] = {n: sorted((s for s in services if services[s][n]["rank_min"] == 1)) for n in POSITIONS}
        b, s = baro.get(key), simple.get(key)
        if b and b.get("status") == "OK" and b["native"].get("root_ranked"):
            item["baro"] = {k: b["native"][k] for k in ("root_rank_min", "root_rank_max", "root_score", "root_best_column", "n_entities")}
        if s and s.get("status") == "OK" and s.get("root_ranked"):
            item["simplerca"] = {k: s["root_parts"][k] for k in ("rank_min", "rank_max", "metric", "trace", "log", "score")}
        t028 = td_cases[key].get("t028") or {}
        item["tracerca_t028"] = {k: t028.get(k) for k in ("status", "rank_min", "rank_max")}
        cases.append(item)
        print(dataset, opaque_id, "OK", self_check["own_d_total_equals_H_native"], self_check["own_u_total_equals_H_u"],
              item.get("root_first_positions"), flush=True)

    def tally(rows):
        ok = [c for c in rows if c["status"] == "OK" and c.get("root_in_trace")]
        result = {"n_cases": len(rows), "n_with_span_table_and_root_in_trace": len(ok),
                  "n_na": sum(c["status"] == "N/A" for c in rows), "n_tool_error": sum(c["status"] == "TOOL_ERROR" for c in rows),
                  "n_root_not_in_trace": sum(c["status"] == "OK" and not c.get("root_in_trace") for c in rows), "positions": {}}
        for name in POSITIONS:
            have = [c for c in ok if c["root_positions"][name]["n"] > 0]
            result["positions"][name] = {
                "n_root_has_spans": len(have),
                "root_has_flag": sum(c["root_positions"][name]["a"] > 0 for c in have),
                "root_first": sum(c["root_positions"][name]["rank_max"] == 1 for c in have),
                "root_first_or_tied_first": sum(c["root_positions"][name]["rank_min"] == 1 for c in have),
                "root_top3": sum(c["root_positions"][name]["rank_max"] <= 3 for c in have),
                "share": quantiles([c["root_positions"][name]["share"] for c in have])}
        combos = {}
        for c in ok:
            combo = "+".join(c["root_first_positions"]) or "không vị trí nào"
            combos[combo] = combos.get(combo, 0) + 1
        result["root_first_position_combinations"] = dict(sorted(combos.items()))
        own_first = lambda c: "own_d" in c["root_first_positions"]
        in_first = lambda c: any(n in c["root_first_positions"] for n in ("in_d", "in_u", "in_d_edge"))
        result["cross"] = {"own_d_first_and_incoming_first": sum(own_first(c) and in_first(c) for c in ok),
                           "own_d_first_only": sum(own_first(c) and not in_first(c) for c in ok),
                           "incoming_first_only": sum(in_first(c) and not own_first(c) for c in ok),
                           "neither": sum(not own_first(c) and not in_first(c) for c in ok),
                           "no_flag_at_any_position": sum(not c["root_flagged_positions"] for c in ok)}
        return result

    summary = {"all": tally(cases), "by_dataset": {}, "by_dataset_fault": {},
               "self_check": {"cases_ok": sum(c["status"] == "OK" for c in cases),
                              "own_d_total_equals_H_native": sum(c["status"] == "OK" and bool(c["self_check"]["own_d_total_equals_H_native"]) for c in cases),
                              "own_u_total_equals_H_u": sum(c["status"] == "OK" and bool(c["self_check"]["own_u_total_equals_H_u"]) for c in cases)}}
    for dataset in ("RE2-TT", "Nezha-OB"):
        rows = [c for c in cases if c["dataset"] == dataset]
        summary["by_dataset"][dataset] = tally(rows)
        for fault in sorted({c["fault"] for c in rows}):
            summary["by_dataset_fault"][dataset + "|" + fault] = tally([c for c in rows if c["fault"] == fault])
    result = {"schema": "T032-root-signal-location-v4", "design": "results/T-032/thiet-ke-bang-mo-ta-004.md#2 và #4",
              "placebo_shift_s": SHIFT_S, "placebo_midpoint": MIDPOINT,
              "interval_fixtures": fixtures, "positions": list(POSITIONS), "methods_executed": False,
              "sources": {"td_summary_sha256": td.sha(TD_SUMMARY), "baro_sha256": td.sha(BARO), "simplerca_sha256": td.sha(SIMPLE),
                          "plan_sha256": td.sha(td.PLAN), "labels_sha256": td.sha(td.LABELS)},
              "note": "Bảng mô tả nơi có tín hiệu trên dev. 'root đứng đầu theo một vị trí' không phải Hit của một phương pháp. "
                      "Các vị trí chồng lấn, không cộng thành tỷ lệ nguyên nhân.",
              "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary["self_check"], ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
