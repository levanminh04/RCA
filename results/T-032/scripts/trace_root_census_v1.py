"""T-032 bản 009 mục 5 (việc 4, bước đếm): span đầu, span mất cha, trace vắt qua mốc, đẳng thức thời lượng, độ phủ mức nền.

Chạy trên EC2, chỉ đọc 52 bảng span như lượt chain-spanpass. KHÔNG chạy phương pháp, KHÔNG chia trace, KHÔNG dùng nhãn.
Span đầu: trường cha trống (RE2-TT) hoặc ghi 'root' (Nezha-OB). Span mất cha: trường cha có giá trị nhưng không thấy trong bảng.
Dùng: python trace_root_census_v1.py <thư mục lượt mới> [dataset:opaque_id]
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402

GATE = 0.90
ONE_SECOND_US = 1_000_000


def census(spans, t_us):
    spans = spans.reset_index(drop=True)
    spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
    operation = (spans["serviceName"].astype(str) + "_" + spans["methodName"].astype(str)).to_numpy()
    service = spans["serviceName"].astype(str).to_numpy()
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    end = start + duration
    after_span = end >= t_us
    par = spans["parentSpanID"]
    declared = (par.isna() | par.astype("string").fillna("").isin(["", "root"])).to_numpy(dtype=bool)
    ident = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(spans)), index=ident)
    duplicated_rows = int(position.index.duplicated(keep=False).sum())
    position = position[~position.index.duplicated(keep=False)]
    parent = (spans["traceID"].astype(str) + "|" + par.astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent) & ~declared
    p = np.where(has_parent, parent, 0).astype("int64")
    orphan = ~declared & ~has_parent
    child_sum = np.zeros(len(spans), dtype="int64")
    np.add.at(child_sum, p[has_parent], duration[has_parent])
    handling = duration - child_sum
    u, _covered, children, _resolved = td.uncovered(spans[["traceID", "spanID", "parentSpanID", "startTime", "duration"]].copy())
    u = np.asarray(u, dtype="int64")
    tcode, tuniq = pd.factorize(spans["traceID"].astype(str).to_numpy())
    df = pd.DataFrame({"t": tcode, "after": after_span, "declared": declared, "orphan": orphan, "dur": duration, "handling": handling,
                       "start": start, "end": end})
    g = df.groupby("t", sort=True).agg(n=("after", "size"), n_after=("after", "sum"), roots=("declared", "sum"), orphans=("orphan", "sum"),
                                       sum_handling=("handling", "sum"), tmin=("start", "min"), tmax=("end", "max"))
    roots = df[df["declared"]].groupby("t", sort=True).agg(root_dur=("dur", "sum"), root_start=("start", "min"), root_end=("end", "max"),
                                                           root_handling_max=("handling", "max"))
    g = g.join(roots)
    is_after = g["n_after"] > 0
    at = g[is_after]
    one = at[at["roots"] == 1]
    complete_one = one[one["orphans"] == 0]
    base = g[~is_after]
    drop_no_root = base["roots"] == 0
    drop_orphan = (base["orphans"] > 0) & ~drop_no_root
    drop_1s = ~drop_no_root & ~drop_orphan & (base["root_handling_max"] > ONE_SECOND_US)
    used = base[~drop_no_root & ~drop_orphan & ~drop_1s]
    used_codes = np.zeros(len(g), dtype=bool)
    used_codes[used.index.to_numpy()] = True
    slo_ops = set(operation[used_codes[tcode]])
    after_root_codes = np.zeros(len(g), dtype=bool)
    after_root_codes[at.index[at["roots"] >= 1].to_numpy()] = True
    in_after_root = after_root_codes[tcode]
    need_ops = set(operation[in_after_root])
    missing = sorted(need_ops - slo_ops)
    missing_mask = in_after_root & np.isin(operation, missing) if missing else np.zeros(len(spans), dtype=bool)
    traces_missing = int(len(np.unique(tcode[missing_mask])))
    native_baseline_ops = set(operation[~after_span])
    with_children = children > 0
    return {
        "spans": int(len(spans)), "traces": int(len(g)), "duplicated_identity_rows": duplicated_rows,
        "declared_root_spans": int(declared.sum()), "orphan_spans": int(orphan.sum()),
        "after_traces": {"n": int(len(at)), "roots_0": int((at["roots"] == 0).sum()), "roots_1": int(len(one)), "roots_2_plus": int((at["roots"] >= 2).sum()),
                         "with_orphan": int((at["orphans"] > 0).sum()), "straddling_t": int((at["n_after"] < at["n"]).sum()),
                         "share_exactly_one_root": float(len(one) / len(at)) if len(at) else None},
        "one_root_after_traces": {"n": int(len(one)), "root_encloses_all_spans": int(((one["root_start"] <= one["tmin"]) & (one["root_end"] >= one["tmax"])).sum()),
                                  "complete": int(len(complete_one)),
                                  "complete_with_identity_sum_handling_equals_root_duration": int((complete_one["sum_handling"] == complete_one["root_dur"]).sum())},
        "root_service_of_after_traces": {k: int(v) for k, v in pd.Series(service[declared & in_after_root]).value_counts().head(12).items()},
        "handling": {"spans_with_children": int(with_children.sum()), "sum_rule_differs_from_union_rule": int((handling != u).sum()),
                     "negative_handling_spans": int((handling < 0).sum())},
        "baseline": {"traces_entirely_before_t": int(len(base)), "dropped_no_root": int(drop_no_root.sum()), "dropped_orphan": int(drop_orphan.sum()),
                     "dropped_root_handling_gt_1s": int(drop_1s.sum()), "used": int(len(used)),
                     "operations_with_slo": len(slo_ops), "operations_in_native_baseline": len(native_baseline_ops),
                     "operations_needed_by_after_traces": len(need_ops), "operations_needed_without_slo": len(missing),
                     "operations_needed_without_slo_names": missing[:20], "after_traces_touching_missing_slo": traces_missing},
        "gate": {"threshold": GATE, "pass": bool(len(at) and len(one) / len(at) >= GATE)},
    }


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    only = sys.argv[2] if len(sys.argv) > 2 else None
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    rows = []
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if only and only != dataset + ":" + opaque_id:
            continue
        began = time.time()
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
        item = {"dataset": dataset, "opaque_id": opaque_id, "source_status": row["source_status"], "span_source": source}
        try:
            item.update(census(spans, t * 1_000_000))
            item["status"] = "OK"
        except Exception as error:
            item.update(status="TOOL_ERROR", error=type(error).__name__ + ": " + str(error)[:300])
        item["wall_s"] = round(time.time() - began, 1)
        rows.append(item)
        print(dataset, opaque_id, item["status"], item.get("after_traces", {}).get("share_exactly_one_root"), item.get("gate"), item["wall_s"], flush=True)
    summary = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        cs = [r for r in rows if r["dataset"] == dataset and r["status"] == "OK"]
        if not cs:
            continue
        shares = sorted(r["after_traces"]["share_exactly_one_root"] for r in cs)
        tot = lambda f: int(sum(f(r) for r in cs))  # noqa: E731
        one = tot(lambda r: r["one_root_after_traces"]["n"])
        comp = tot(lambda r: r["one_root_after_traces"]["complete"])
        summary[dataset] = {
            "cases": len([r for r in rows if r["dataset"] == dataset]), "cases_ok": len(cs), "cases_gate_pass": sum(r["gate"]["pass"] for r in cs),
            "share_exactly_one_root": {"min": shares[0], "median": shares[len(shares) // 2], "max": shares[-1]},
            "after_traces": tot(lambda r: r["after_traces"]["n"]), "after_traces_roots_0": tot(lambda r: r["after_traces"]["roots_0"]),
            "after_traces_roots_1": one, "after_traces_roots_2_plus": tot(lambda r: r["after_traces"]["roots_2_plus"]),
            "after_traces_with_orphan": tot(lambda r: r["after_traces"]["with_orphan"]), "after_traces_straddling_t": tot(lambda r: r["after_traces"]["straddling_t"]),
            "one_root_traces_root_encloses_all": tot(lambda r: r["one_root_after_traces"]["root_encloses_all_spans"]),
            "one_root_complete": comp, "one_root_complete_identity_holds": tot(lambda r: r["one_root_after_traces"]["complete_with_identity_sum_handling_equals_root_duration"]),
            "spans": tot(lambda r: r["spans"]), "spans_sum_rule_differs_from_union_rule": tot(lambda r: r["handling"]["sum_rule_differs_from_union_rule"]),
            "spans_negative_handling": tot(lambda r: r["handling"]["negative_handling_spans"]),
            "baseline_traces": tot(lambda r: r["baseline"]["traces_entirely_before_t"]), "baseline_used": tot(lambda r: r["baseline"]["used"]),
            "baseline_dropped_no_root": tot(lambda r: r["baseline"]["dropped_no_root"]), "baseline_dropped_orphan": tot(lambda r: r["baseline"]["dropped_orphan"]),
            "baseline_dropped_gt_1s": tot(lambda r: r["baseline"]["dropped_root_handling_gt_1s"]),
            "cases_with_needed_operation_without_slo": sum(r["baseline"]["operations_needed_without_slo"] > 0 for r in cs),
            "cases_with_fewer_than_30_baseline_traces_used": sum(r["baseline"]["used"] < 30 for r in cs),
            "baseline_used_per_case": {"min": min(r["baseline"]["used"] for r in cs), "max": max(r["baseline"]["used"] for r in cs)},
            "root_services": sorted({s for r in cs for s in r["root_service_of_after_traces"]}),
            "dataset_stop": sum(not r["gate"]["pass"] for r in cs) > len(cs) / 2}
    result = {"schema": "T032-trace-root-census-v1", "design": "results/T-032/thiet-ke-phep-doi-009.md mục 5", "summary": summary, "cases": rows, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1), flush=True)


if __name__ == "__main__":
    main()
