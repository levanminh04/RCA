"""T-032 bảng C (thiet-ke-bang-mo-ta-004.md mục 5): cấu tạo thời gian của lời gọi giữa hai dịch vụ, và kiểm kê tên span.

Chạy trên EC2, chỉ đọc bảng span adapter TraceRCA đã lưu của các ca phát lại khớp từng bit. Không gọi phương pháp.
Với mỗi lời gọi (span phía gọi p của dịch vụ A, span con c của dịch vụ B): pre = start_c - start_p, post = end_p - end_c,
gap = d_p - d_c. Tổng hợp theo cặp (A, B), tách trước/sau mốc theo thời điểm kết thúc của p. Nhãn root nối sau cùng.
Kèm kiểm kê (dịch vụ, tên span) theo dataset để đối chiếu với mã nguồn (gắn phiên bản).
Dùng: python call_interval_table_v1.py <thư mục lượt mới> [dataset:opaque_id]
"""
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402


def med(values):
    return float(np.median(values)) if len(values) else None


def block(frame):
    if not len(frame):
        return {"n": 0}
    pre, post, gap = frame["pre"].to_numpy(), frame["post"].to_numpy(), frame["gap"].to_numpy()
    return {"n": int(len(frame)), "nested_share": float(((pre >= 0) & (post >= 0)).mean()),
            "pre_negative_share": float((pre < 0).mean()), "post_negative_share": float((post < 0).mean()),
            "gap_negative_share": float((gap < 0).mean()),
            "median_d_p_us": med(frame["d_p"].to_numpy()), "median_d_c_us": med(frame["d_c"].to_numpy()),
            "median_pre_us": med(pre), "median_post_us": med(post), "median_gap_us": med(gap),
            "p90_gap_us": float(np.percentile(gap, 90)), "p90_d_c_us": float(np.percentile(frame["d_c"].to_numpy(), 90))}


def ratio(after, before, key):
    a, b = after.get(key), before.get(key)
    return None if a is None or b is None or b == 0 else a / b


def one_case(directory, table_columns):
    capture = directory / "capture"
    adapter = td.read(capture / "calls/001-adapter.json")
    spans = pd.DataFrame(table_columns(capture, adapter["entry"]["input"]))
    t_us = int(adapter["entry"]["t_seconds"]) * 1_000_000
    spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    end = start + duration
    service = spans["serviceName"].astype(str).to_numpy()
    name = spans["methodName"].astype(str).to_numpy()
    key = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(spans)), index=key)
    position = position[~position.index.duplicated(keep=False)]
    parent = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent)
    p = np.where(has_parent, parent, 0).astype("int64")
    cross = has_parent & (service[p] != service)
    c_index = np.flatnonzero(cross)
    p_index = p[cross]
    calls = pd.DataFrame({"caller": service[p_index], "callee": service[c_index], "caller_op": name[p_index], "callee_op": name[c_index],
                          "d_p": duration[p_index], "d_c": duration[c_index], "pre": start[c_index] - start[p_index],
                          "post": end[p_index] - end[c_index], "after": end[p_index] >= t_us})
    calls["gap"] = calls["d_p"] - calls["d_c"]
    # con khác của span phía gọi (cùng dịch vụ) và cha của span phía gọi
    children_total = np.zeros(len(spans), dtype="int64")
    np.add.at(children_total, p[has_parent], 1)
    calls["p_children_total"] = children_total[p_index]
    p_has_parent = has_parent[p_index]
    calls["p_parent_same_service"] = p_has_parent & (service[p[p_index]] == service[p_index])
    calls["c_children_total"] = children_total[c_index]
    pairs = {}
    for (a, b), g in calls.groupby(["caller", "callee"], sort=True):
        before, after = block(g[~g["after"]]), block(g[g["after"]])
        pairs[a + "→" + b] = {"caller": a, "callee": b, "before": before, "after": after,
                                   "ratio_after_over_before": {k: ratio(after, before, k) for k in ("median_d_c_us", "median_gap_us", "median_d_p_us",
                                                                                                    "p90_gap_us", "p90_d_c_us")},
                                   "caller_ops": dict(Counter(g["caller_op"]).most_common(6)), "callee_ops": dict(Counter(g["callee_op"]).most_common(6)),
                                   "p_children_total": {str(k): int(v) for k, v in g["p_children_total"].clip(upper=3).value_counts().sort_index().items()},
                                   "p_parent_same_service_share": float(g["p_parent_same_service"].mean()),
                                   "c_has_children_share": float((g["c_children_total"] > 0).mean())}
    inventory = Counter(zip(service, name))
    cross_ops = Counter(zip(calls["caller"], calls["caller_op"], calls["callee"], calls["callee_op"]))
    root_like = spans.loc[~has_parent]
    return {"t_seconds": int(adapter["entry"]["t_seconds"]), "n_spans": int(len(spans)), "n_calls": int(len(calls)),
            "all_calls": {"before": block(calls[~calls["after"]]), "after": block(calls[calls["after"]])},
            "pairs": pairs}, inventory, cross_ops, Counter(zip(root_like["serviceName"].astype(str), root_like["methodName"].astype(str)))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    only = sys.argv[2] if len(sys.argv) > 2 else None
    from replay_tracerca_v3 import table_columns
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "tracerca"}
    cases = []
    inventories = {"RE2-TT": Counter(), "Nezha-OB": Counter()}
    cross_inventories = {"RE2-TT": Counter(), "Nezha-OB": Counter()}
    entry_inventories = {"RE2-TT": Counter(), "Nezha-OB": Counter()}
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        label = labels[(dataset, opaque_id)]
        base = {"dataset": dataset, "opaque_id": opaque_id, "root": label["root"], "fault": label["fault"], "cell": label["cell"]}
        if row["source_status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "nguồn TraceRCA " + row["source_status"] + ": không có bảng span đã lưu"})
            continue
        directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
        computed, inventory, cross_ops, entries = one_case(directory, table_columns)  # chưa dùng nhãn
        inventories[dataset].update(inventory)
        cross_inventories[dataset].update(cross_ops)
        entry_inventories[dataset].update(entries)
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps({**base, **computed}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        # --- nối nhãn ---
        root = label["root"]
        incoming = {k: v for k, v in computed["pairs"].items() if v["callee"] == root}
        outgoing = {k: v for k, v in computed["pairs"].items() if v["caller"] == root}
        cases.append({**base, "status": "OK", "n_calls": computed["n_calls"], "all_calls": computed["all_calls"],
                      "n_pairs": len(computed["pairs"]), "incoming_to_root": incoming, "outgoing_from_root_pairs": sorted(outgoing)})
        print(dataset, opaque_id, computed["n_calls"], len(incoming), flush=True)

    def summarize(rows):
        ok = [c for c in rows if c["status"] == "OK"]
        base_nested = [c["all_calls"]["before"]["nested_share"] for c in ok if c["all_calls"]["before"]["n"]]
        result = {"n_cases": len(rows), "n_ok": len(ok),
                  "nested_share_before_all_calls": {"min": min(base_nested), "median": statistics.median(base_nested), "max": max(base_nested)} if base_nested else None,
                  "pre_negative_share_before": statistics.median([c["all_calls"]["before"]["pre_negative_share"] for c in ok]) if ok else None,
                  "post_negative_share_before": statistics.median([c["all_calls"]["before"]["post_negative_share"] for c in ok]) if ok else None,
                  "gap_negative_share_before": statistics.median([c["all_calls"]["before"]["gap_negative_share"] for c in ok]) if ok else None}
        edges = []
        for c in ok:
            for name, v in c["incoming_to_root"].items():
                if v["before"]["n"] >= 20 and v["after"]["n"] >= 20:
                    r = v["ratio_after_over_before"]
                    edges.append({"opaque_id": c["opaque_id"], "fault": c["fault"], "edge": name, "n_before": v["before"]["n"], "n_after": v["after"]["n"],
                                  "nested_before": v["before"]["nested_share"], "nested_after": v["after"]["nested_share"],
                                  "d_c_ratio": r["median_d_c_us"], "gap_ratio": r["median_gap_us"],
                                  "median_gap_before_us": v["before"]["median_gap_us"], "median_gap_after_us": v["after"]["median_gap_us"],
                                  "median_d_c_before_us": v["before"]["median_d_c_us"], "median_d_c_after_us": v["after"]["median_d_c_us"]})
        result["incoming_edges_to_root_with_20_calls_each_side"] = len(edges)
        result["cases_with_such_edge"] = len({e["opaque_id"] for e in edges})

        def kind(e):
            if e["d_c_ratio"] is None or e["gap_ratio"] is None:
                return "không tính được tỷ số"
            dc, gp = e["d_c_ratio"] >= 2, e["gap_ratio"] >= 2
            return "cả hai tăng" if dc and gp else "chỉ span của root dài ra" if dc else "chỉ phần ngoài span của root dài ra" if gp else "không phần nào tăng gấp đôi"
        result["incoming_edges_by_what_grew"] = dict(Counter(kind(e) for e in edges))
        by_fault = defaultdict(Counter)
        for e in edges:
            by_fault[e["fault"]][kind(e)] += 1
        result["incoming_edges_by_fault_and_what_grew"] = {f: dict(v) for f, v in sorted(by_fault.items())}
        result["edges"] = edges
        return result

    summary = {ds: summarize([c for c in cases if c["dataset"] == ds]) for ds in ("RE2-TT", "Nezha-OB")}
    inventory_out = {}
    for ds in ("RE2-TT", "Nezha-OB"):
        inventory_out[ds] = {"service_span_names": [{"service": s, "name": n, "count": int(v)} for (s, n), v in sorted(inventories[ds].items())],
                             "cross_service_calls": [{"caller": a, "caller_op": ao, "callee": b, "callee_op": bo, "count": int(v)}
                                                     for (a, ao, b, bo), v in sorted(cross_inventories[ds].items())],
                             "spans_without_resolved_parent": [{"service": s, "name": n, "count": int(v)} for (s, n), v in sorted(entry_inventories[ds].items())]}
    (out / "inventory.json").write_text(json.dumps(inventory_out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    result = {"schema": "T032-call-interval-table-v1", "design": "results/T-032/thiet-ke-bang-mo-ta-004.md#5", "methods_executed": False,
              "threshold_note": "mốc 'tăng gấp đôi' (tỷ số trung vị sau/trước >= 2) chỉ để đếm; tỷ số thô nằm trong /summary/*/edges",
              "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({ds: {k: v for k, v in summary[ds].items() if k != "edges"} for ds in summary}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
