"""T-032 bảng C2 (thiet-ke-bang-mo-ta-004.md mục 5b): phân rã theo từng lời gọi chậm. Chạy trên EC2, chỉ đọc.

Với mỗi cạnh (dịch vụ gọi A, dịch vụ được gọi B) của mỗi ca: ngưỡng chậm = phân vị 95 của d_p trước mốc; lời gọi chậm sau mốc
được xếp "trong span của B" nếu phần vượt của d_c không nhỏ hơn phần vượt của gap (so với trung vị trước mốc), ngược lại "ngoài".
48 ca đọc bảng span adapter TraceRCA đã lưu; 4 ca RE2 nguồn TraceRCA ERROR đọc parquet gốc qua cua_so.cat_span.
Không gọi phương pháp. Mọi cạnh được tính trước; nhãn root nối sau cùng.
Dùng: python call_slow_table_v1.py <thư mục lượt mới>
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402

MIN_CALLS = 20


def calls_of(spans, t_us):
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    end = start + duration
    service = spans["serviceName"].astype(str).to_numpy()
    ident = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(spans)), index=ident)
    position = position[~position.index.duplicated(keep=False)]
    parent = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent)
    p = np.where(has_parent, parent, 0).astype("int64")
    cross = has_parent & (service[p] != service)
    c_index, p_index = np.flatnonzero(cross), p[cross]
    calls = pd.DataFrame({"caller": service[p_index], "callee": service[c_index], "d_p": duration[p_index], "d_c": duration[c_index],
                          "after": end[p_index] >= t_us})
    calls["gap"] = calls["d_p"] - calls["d_c"]
    return calls


def edges_of(calls):
    out = {}
    for (a, b), g in calls.groupby(["caller", "callee"], sort=True):
        before, after = g[~g["after"]], g[g["after"]]
        if len(before) < MIN_CALLS or len(after) < MIN_CALLS:
            continue
        threshold = float(np.percentile(before["d_p"].to_numpy(), 95))
        med_c, med_g = float(np.median(before["d_c"].to_numpy())), float(np.median(before["gap"].to_numpy()))
        slow = after[after["d_p"] > threshold]
        inside = int(((slow["d_c"] - med_c) >= (slow["gap"] - med_g)).sum())
        out[a + "→" + b] = {"caller": a, "callee": b, "n_before": int(len(before)), "n_after": int(len(after)),
                                 "threshold_p95_d_p_us": threshold, "slow_share_before": float((before["d_p"] > threshold).mean()),
                                 "slow_share_after": float(len(slow) / len(after)), "n_slow_after": int(len(slow)),
                                 "slow_inside_callee_span": inside, "slow_outside_callee_span": int(len(slow) - inside),
                                 "median_d_p_before_us": float(np.median(before["d_p"].to_numpy())),
                                 "median_d_p_after_us": float(np.median(after["d_p"].to_numpy()))}
    return out


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "tracerca"}
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    cases = []
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        label = labels[(dataset, opaque_id)]
        if row["source_status"] == "OK":
            directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
            adapter = td.read(directory / "capture/calls/001-adapter.json")
            spans = pd.DataFrame(table_columns(directory / "capture", adapter["entry"]["input"]))
            t = int(adapter["entry"]["t_seconds"])
            source = "bảng span adapter TraceRCA đã lưu"
        else:
            entry = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == opaque_id][0]
            t = int(td.read(BASE / "repo" / entry["path"])["window"]["t"])
            files = selector.chon_ca(allow, opaque_id, Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
            spans = cua_so.cat_span(pd.read_parquet(files["traces.parquet"]), t)
            source = "parquet gốc qua cua_so.cat_span"
        edges = edges_of(calls_of(spans, t * 1_000_000))  # chưa dùng nhãn
        (out / "cases" / (dataset + "-" + opaque_id + ".json")).write_text(json.dumps({"dataset": dataset, "opaque_id": opaque_id, "edges": edges},
                                                                                     ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        root = label["root"]
        to_root = {k: v for k, v in edges.items() if v["callee"] == root}
        others = [v for v in edges.values() if v["callee"] != root and v["caller"] != root]
        from_root = [v for v in edges.values() if v["caller"] == root]
        item = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": label["fault"], "cell": label["cell"], "span_source": source,
                "n_edges": len(edges), "edges_to_root": to_root,
                "to_root_max_slow_share_after": max((v["slow_share_after"] for v in to_root.values()), default=None),
                "other_edges": {"n": len(others), "median_slow_share_after": statistics.median([v["slow_share_after"] for v in others]) if others else None,
                                "max_slow_share_after": max((v["slow_share_after"] for v in others), default=None),
                                "n_with_slow_share_after_ge_0_5": sum(v["slow_share_after"] >= 0.5 for v in others),
                                "top": sorted(((round(v["slow_share_after"], 3), v["caller"] + "→" + v["callee"]) for v in others), reverse=True)[:5]},
                "from_root_edges": {"n": len(from_root), "max_slow_share_after": max((v["slow_share_after"] for v in from_root), default=None)}}
        cases.append(item)
        print(dataset, opaque_id, len(edges), None if item["to_root_max_slow_share_after"] is None else round(item["to_root_max_slow_share_after"], 3),
              item["other_edges"]["median_slow_share_after"], flush=True)

    def summarize(rows):
        have = [c for c in rows if c["edges_to_root"]]
        edges = [(c, v) for c in have for v in c["edges_to_root"].values()]
        by_fault = {}
        for fault in sorted({c["fault"] for c in rows}):
            sub = [(c, v) for c, v in edges if c["fault"] == fault]
            slow = sum(v["n_slow_after"] for _c, v in sub)
            by_fault[fault] = {"cases_with_edge_to_root": len({c["opaque_id"] for c, _v in sub}), "edges_to_root": len(sub),
                               "median_slow_share_after": statistics.median([v["slow_share_after"] for _c, v in sub]) if sub else None,
                               "edges_slow_share_after_ge_0_5": sum(v["slow_share_after"] >= 0.5 for _c, v in sub),
                               "slow_calls_after": slow,
                               "slow_calls_inside_root_span_share": (sum(v["slow_inside_callee_span"] for _c, v in sub) / slow) if slow else None,
                               "cases_max_to_root_slow_ge_0_5": sum(1 for c in have if c["fault"] == fault and c["to_root_max_slow_share_after"] >= 0.5),
                               "cases_other_edges_median_slow_ge_0_5": sum(1 for c in rows if c["fault"] == fault and (c["other_edges"]["median_slow_share_after"] or 0) >= 0.5),
                               "median_of_other_edges_median_slow_share": statistics.median([c["other_edges"]["median_slow_share_after"] for c in rows
                                                                                              if c["fault"] == fault and c["other_edges"]["median_slow_share_after"] is not None])
                               if any(c["fault"] == fault and c["other_edges"]["median_slow_share_after"] is not None for c in rows) else None}
        return {"n_cases": len(rows), "cases_with_edge_to_root": len(have), "edges_to_root": len(edges),
                "cases_max_to_root_slow_share_after_ge_0_5": sum(c["to_root_max_slow_share_after"] >= 0.5 for c in have),
                "cases_max_to_root_slow_share_after_ge_0_2": sum(c["to_root_max_slow_share_after"] >= 0.2 for c in have),
                "cases_to_root_exceeds_every_other_edge": sum(1 for c in have if c["other_edges"]["max_slow_share_after"] is not None
                                                             and c["to_root_max_slow_share_after"] > c["other_edges"]["max_slow_share_after"]),
                "slow_share_before_median_all_root_edges": statistics.median([v["slow_share_before"] for _c, v in edges]) if edges else None,
                "by_fault": by_fault}

    summary = {ds: summarize([c for c in cases if c["dataset"] == ds]) for ds in ("RE2-TT", "Nezha-OB")}
    result = {"schema": "T032-call-slow-table-v1", "design": "results/T-032/thiet-ke-bang-mo-ta-004.md#5b", "methods_executed": False,
              "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
