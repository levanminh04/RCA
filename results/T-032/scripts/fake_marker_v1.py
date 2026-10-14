"""T-032 bản 013 mục 1 (KT-1, KT-2): mốc giả trên bảng span RE2-TT. Chạy trên EC2, chỉ đọc. Không gọi phương pháp.

Sáu cấu hình cửa sổ (đoạn nền, đoạn xét) theo thiet-ke-phep-doi-013.md mục 1. Bước duy nhất bị đổi: vị trí và độ dài hai cửa sổ.
Luật cờ giữ nguyên: thời lượng/1000 >= round(mean/1000, 2) + 3*round(std/1000, 2) theo thao tác ở đoạn nền; trace bất thường
khi có ít nhất một span mang cờ. Mọi thao tác, mọi dịch vụ được tính trước; nhãn root nối sau cùng.
Tự kiểm (cấu hình real300): tổng cờ luật TraceRCA = H_native; số trace bất thường/bình thường và số cờ luật MicroRank = lượt chain-spanpass-001.
Dùng: python fake_marker_v1.py <thư mục lượt mới> [opaque_id để chạy thử một ca]
"""
import json
import math
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402
import root_signal_location_v1 as rsl  # noqa: E402 — baseline_flags đã khớp H_native 48/48
import chain_position_v1 as cp  # noqa: E402

SPANPASS = BASE / "runs/chain-spanpass-001"
LINK = BASE / "runs/slow-call-flag-link-001/cases.json"
INF = float("inf")
CONFIGS = {  # tên: (đầu nền, cuối nền, đầu đoạn xét, cuối đoạn xét), giây so với t; nửa mở [đầu, cuối) theo thời điểm kết thúc span
    "real300": (-INF, 0, 0, INF),
    "real150": (-150, 0, 0, 150),
    "fake150": (-INF, -150, -150, 0),
    "real100": (-100, 0, 0, 100),
    "fake100a": (-INF, -200, -200, -100),
    "fake100b": (-200, -100, -100, 0),
}
BUSY_N = 200
UNRELATED = ("chung_phia_tren", "roi")


def window(end, t_us, lo, hi):
    m = np.ones(len(end), dtype=bool)
    if lo != -INF:
        m &= end >= t_us + int(lo * 1_000_000)
    if hi != INF:
        m &= end < t_us + int(hi * 1_000_000)
    return m


def flags_microrank(duration, operation, before, after):
    """Đúng biểu thức của src/microrank/__init__.py: mean, std (ddof=1) chia 1000 rồi round(2) của pandas."""
    frame = pd.DataFrame({"operation": operation, "duration": duration})
    stats = frame[before].groupby("operation", sort=True)["duration"].agg(["mean", "std", "count"])
    m = frame["operation"].map((stats["mean"] / 1000).round(2)).to_numpy(dtype="float64")
    s = frame["operation"].map((stats["std"] / 1000).round(2)).to_numpy(dtype="float64")
    ok = after & ~np.isnan(m) & ~np.isnan(s)
    with np.errstate(invalid="ignore"):
        flag = ok & ((np.asarray(duration, dtype="float64") / 1000) >= m + 3 * s)
    return flag, ok


def predicted_share(tcode, nt, rate_of_span):
    """Trung bình trên trace của 1 - tích(1 - r) lấy trên mọi span của trace."""
    r = np.clip(rate_of_span, 0.0, 1.0)
    with np.errstate(divide="ignore"):
        log_keep = np.where(r >= 1.0, -np.inf, np.log1p(-r))
    total = np.zeros(nt)
    np.add.at(total, tcode, log_keep)
    return float(np.mean(1.0 - np.exp(total)))


def fixtures():
    end = np.array([10, 20, 30, 40]) * 1_000_000
    checks = {"cửa sổ nửa mở": window(end, 30_000_000, -20, 0).tolist() == [True, True, False, False],
              "không chặn dưới": window(end, 30_000_000, -INF, 0).tolist() == [True, True, False, False],
              "đoạn xét": window(end, 30_000_000, 0, INF).tolist() == [False, False, True, True],
              "dự đoán độc lập: hai trace, một trace hai span r=0,5 và một trace một span r=0": abs(
                  predicted_share(np.array([0, 0, 1]), 2, np.array([0.5, 0.5, 0.0])) - 0.375) < 1e-12}
    d = np.array([1000, 1000, 1200, 1000, 9000, 1100] * 1, dtype="int64")
    op = np.array(["a"] * 6, dtype=object)
    before = np.array([True, True, True, True, False, False])
    after = ~before
    flag, ok = flags_microrank(d, op, before, after)   # mean 1,05 ms; std 0,1 ms; ngưỡng 1,35 ms
    checks["cờ: 9 ms vượt, 1,1 ms không"] = flag.tolist() == [False, False, False, False, True, False] and ok.tolist() == after.tolist()
    checks = {k: bool(v) for k, v in checks.items()}
    return {"pass": all(checks.values()), "checks": checks}


def one_case(spans, t_us):
    spans = spans.reset_index(drop=True)
    spans["methodName"] = spans["methodName"].fillna(spans["operationName"])
    operation = (spans["serviceName"].astype(str) + "_" + spans["methodName"].astype(str)).to_numpy()
    service = spans["serviceName"].astype(str).to_numpy()
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    end = start + duration
    trace = spans["traceID"].astype(str).to_numpy()
    op_service = dict(pd.DataFrame({"o": operation, "s": service}).drop_duplicates().itertuples(index=False, name=None))
    out = {"spans": int(len(spans)), "earliest_end_minus_t_s": float((int(end.min()) - t_us) / 1e6),
           "latest_end_minus_t_s": float((int(end.max()) - t_us) / 1e6), "op_service": op_service, "configs": {}}
    rates = {}
    keep = {}
    for name, (blo, bhi, elo, ehi) in CONFIGS.items():
        before, after = window(end, t_us, blo, bhi), window(end, t_us, elo, ehi)
        item = {"spans_before": int(before.sum()), "spans_after": int(after.sum())}
        if not before.any() or not after.any():
            item["status"] = "thiếu span ở một cửa sổ"
            out["configs"][name] = item
            continue
        f_tr, ok_tr = rsl.baseline_flags(spans["duration"], operation, before, after)
        f_tr, ok_tr = np.asarray(f_tr, dtype=bool), np.asarray(ok_tr, dtype=bool)
        f_mr, ok_mr = flags_microrank(duration, operation, before, after)
        A = np.flatnonzero(after)
        tcode, tuniq = pd.factorize(trace[A])
        nt = len(tuniq)
        t_abn = np.zeros(nt, dtype=bool)
        t_abn[tcode[f_mr[A]]] = True
        ops = {}
        for o, n in pd.Series(operation[after & ok_tr]).value_counts().items():
            ops[o] = {"n": int(n), "a": 0, "a_mr": 0}
        for o, a in pd.Series(operation[f_tr]).value_counts().items():
            ops[o]["a"] = int(a)
        for o, a in pd.Series(operation[f_mr]).value_counts().items():
            ops[o]["a_mr"] = int(a)
        n_mr = pd.Series(operation[after & ok_mr]).value_counts()
        a_mr = pd.Series(operation[f_mr]).value_counts()
        rate = (a_mr.reindex(n_mr.index).fillna(0) / n_mr).to_dict()
        rates[name] = rate
        keep[name] = (A, tcode, nt)
        by_service = {}
        pairs = pd.DataFrame({"t": tcode, "s": service[A]}).drop_duplicates()
        pairs["abn"] = t_abn[pairs["t"].to_numpy()]
        for s, g in pairs.groupby("s", sort=True):
            by_service[s] = {"traces": int(len(g)), "abnormal": int(g["abn"].sum())}
        span_per_trace = np.bincount(tcode, minlength=nt)
        item.update({"status": "OK", "traces": int(nt), "abnormal_traces": int(t_abn.sum()),
                     "abnormal_share": float(t_abn.mean()), "flags_tracerca_rule": int(f_tr.sum()), "flags_microrank_rule": int(f_mr.sum()),
                     "flags_differ": int((f_tr != f_mr).sum()), "after_spans_without_baseline": int((after & ~ok_tr).sum()),
                     "span_flag_share": float(f_mr.sum() / max(1, int((after & ok_mr).sum()))),
                     "spans_per_trace_median": float(np.median(span_per_trace)), "spans_per_trace_max": int(span_per_trace.max()),
                     "predicted_share_independent_own_rates": predicted_share(tcode, nt, pd.Series(operation[A]).map(rate).fillna(0.0).to_numpy()),
                     "operations": ops, "traces_by_service": by_service})
        out["configs"][name] = item
    # tỷ lệ dự đoán cho đoạn xét của mốc thật nếu thao tác chỉ vượt ngưỡng như ở mốc giả cùng độ dài
    for real, fake in (("real150", "fake150"), ("real100", "fake100b"), ("real100", "fake100a")):
        if real in keep and fake in rates:
            A, tcode, nt = keep[real]
            mapped = pd.Series(operation[A]).map(rates[fake])
            out["configs"][real]["predicted_share_independent_rates_of_" + fake] = predicted_share(tcode, nt, mapped.fillna(0.0).to_numpy())
            out["configs"][real]["spans_without_rate_in_" + fake] = int(mapped.isna().sum())
    return out


def q(values):
    values = sorted(v for v in values if v is not None and not (isinstance(v, float) and math.isnan(v)))
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    (out / "cases").mkdir()
    only = sys.argv[2] if len(sys.argv) > 2 else None
    fx = fixtures()
    if not fx["pass"]:
        raise SystemExit("trường hợp tự dựng không đạt: " + json.dumps(fx, ensure_ascii=False))
    from replay_tracerca_v3 import table_columns
    td_cases = {(c["dataset"], c["opaque_id"]): c for c in td.read(BASE / "runs/tracerca-core-td-001/summary.json")["cases"]}
    labels = {(r["dataset"], r["opaque_id"]): r for r in td.read(td.LABELS)["main_rows"] if r["method"] == "tracerca"}
    link = [c for c in td.read(LINK) if c["dataset"] == "RE2-TT" and c["method"] == "tracerca" and c.get("status") == "OK" and c.get("root_ranked")]
    link = {c["opaque_id"]: c for c in link}
    cases = []
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if dataset != "RE2-TT" or (only and only != opaque_id):
            continue
        label = labels[(dataset, opaque_id)]
        base = {"dataset": dataset, "opaque_id": opaque_id, "root": label["root"], "fault": label["fault"], "cell": label["cell"]}
        if row["source_status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "nguồn TraceRCA " + row["source_status"] + ": không có bảng span đã lưu"})
            continue
        began = time.time()
        directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
        adapter = td.read(directory / "capture/calls/001-adapter.json")
        spans = pd.DataFrame(table_columns(directory / "capture", adapter["entry"]["input"]))
        computed = one_case(spans, int(adapter["entry"]["t_seconds"]) * 1_000_000)   # chưa dùng nhãn
        sp = td.read(SPANPASS / "cases" / (dataset + "-" + opaque_id + ".json"))
        r300 = computed["configs"]["real300"]
        check = {"flags_equal_H_native": r300.get("flags_tracerca_rule") == td_cases[(dataset, opaque_id)]["counts"]["H_native"],
                 "traces_A_N_flags_equal_spanpass": [r300.get("abnormal_traces"), r300.get("traces", 0) - r300.get("abnormal_traces", 0), r300.get("flags_microrank_rule")] ==
                 [sp["counts"]["traces_A"], sp["counts"]["traces_N"], sp["counts"]["flags_microrank_rule"]],
                 "operations_a_n_equal_spanpass": all(sp["operations"].get(o, {}).get("a") == v["a"] and sp["operations"][o]["n"] == v["n"]
                                                      for o, v in r300.get("operations", {}).items()) and len(sp["operations"]) == len(r300.get("operations", {}))}
        full = {**base, "status": "OK" if all(check.values()) else "CHECK_FAIL", "self_check": check, **computed}
        (out / "cases" / (opaque_id + ".json")).write_text(json.dumps(full, ensure_ascii=False) + "\n", encoding="utf-8")
        # --- từ đây nối nhãn ---
        root = label["root"]
        g = cp.Graph(sp["services"], [(e["caller"], e["callee"]) for e in sp["edges"].values()])
        cls = {s: ("root" if s == root else g.position(s, root)["class"]) for s in sp["services"]}
        item = {**base, "status": full["status"], "self_check": check, "root_in_trace": root in sp["services"], "configs": {}, "wall_s": round(time.time() - began, 1)}
        for name, c in computed["configs"].items():
            if c.get("status") != "OK":
                item["configs"][name] = {"status": c.get("status"), "spans_before": c["spans_before"], "spans_after": c["spans_after"]}
                continue
            with_root = c["traces_by_service"].get(root, {"traces": 0, "abnormal": 0})
            t_no, a_no = c["traces"] - with_root["traces"], c["abnormal_traces"] - with_root["abnormal"]
            v = {k: c[k] for k in c if k not in ("operations", "traces_by_service")}
            v.update({"traces_with_root": with_root["traces"], "abnormal_with_root": with_root["abnormal"],
                      "share_with_root": with_root["abnormal"] / with_root["traces"] if with_root["traces"] else None,
                      "traces_without_root": t_no, "abnormal_without_root": a_no, "share_without_root": a_no / t_no if t_no else None})
            item["configs"][name] = v
        # KT-2: thao tác đông span ở cả fake150 lẫn real150, không phải của root
        busy = []
        cf, cr = computed["configs"].get("fake150", {}), computed["configs"].get("real150", {})
        if cf.get("status") == "OK" and cr.get("status") == "OK":
            for o, vf in cf["operations"].items():
                vr = cr["operations"].get(o)
                s = computed["op_service"][o]
                if vr and vf["n"] >= BUSY_N and vr["n"] >= BUSY_N and s != root:
                    busy.append({"operation": o, "service": s, "class": cls.get(s), "fake_n": vf["n"], "fake_a": vf["a"], "real_n": vr["n"], "real_a": vr["a"],
                                 "fake_share": vf["a"] / vf["n"], "real_share": vr["a"] / vr["n"]})
        item["busy_operations"] = busy
        # thực thể không liên hệ đứng trên root trong bản ghi TraceRCA đã chấm
        read_pairs = []
        for e in link.get(opaque_id, {}).get("entities", []):
            if e.get("above_root") and e.get("class") in UNRELATED and "span" in e:
                o = e["operation"]
                rec = {"entity": e["entity"], "operation": o, "class": e["class"], "stored_a": e["span"]["a"], "stored_n": e["span"]["n"]}
                for name in ("real300", "real150", "fake150", "real100", "fake100a", "fake100b"):
                    v = computed["configs"].get(name, {}).get("operations", {}).get(o)
                    rec[name] = None if v is None else {"a": v["a"], "n": v["n"], "share": v["a"] / v["n"] if v["n"] else None}
                rec["real300_equals_stored"] = rec["real300"] is not None and rec["real300"]["a"] == rec["stored_a"] and rec["real300"]["n"] == rec["stored_n"]
                read_pairs.append(rec)
        item["unrelated_above_root_tracerca"] = read_pairs
        cases.append(item)
        print(opaque_id, item["status"], check, {n: round(v["abnormal_share"], 3) for n, v in item["configs"].items() if "abnormal_share" in v}, item["wall_s"], flush=True)

    ok = [c for c in cases if c["status"] == "OK"]

    def col(name, key):
        return [c["configs"][name].get(key) for c in ok if c["configs"].get(name, {}).get("status") == "OK"]

    summary = {"n_cases": len(cases), "status": dict(Counter(c["status"] for c in cases)),
               "self_check": {k: sum(bool(c["self_check"][k]) for c in cases if "self_check" in c) for k in ("flags_equal_H_native", "traces_A_N_flags_equal_spanpass", "operations_a_n_equal_spanpass")},
               "configs": {}}
    for name in CONFIGS:
        summary["configs"][name] = {"cases_ok": len(col(name, "abnormal_share")),
                                    "abnormal_share": q(col(name, "abnormal_share")), "share_without_root": q(col(name, "share_without_root")),
                                    "share_with_root": q(col(name, "share_with_root")), "span_flag_share": q(col(name, "span_flag_share")),
                                    "predicted_share_independent_own_rates": q(col(name, "predicted_share_independent_own_rates")),
                                    "traces": q(col(name, "traces")), "spans_per_trace_median": q(col(name, "spans_per_trace_median")),
                                    "flags_differ_total": sum(v or 0 for v in col(name, "flags_differ"))}
    summary["configs"]["real150"]["predicted_share_rates_of_fake150"] = q(col("real150", "predicted_share_independent_rates_of_fake150"))
    summary["configs"]["real100"]["predicted_share_rates_of_fake100b"] = q(col("real100", "predicted_share_independent_rates_of_fake100b"))
    # KT-1: mốc đọc
    both = [c for c in ok if all(c["configs"].get(n, {}).get("status") == "OK" for n in ("real150", "fake150"))]
    R = [c["configs"]["real150"]["share_without_root"] for c in both if c["configs"]["real150"]["share_without_root"] is not None]
    F = [c["configs"]["fake150"]["abnormal_share"] for c in both]
    pred = [c["configs"]["fake150"]["predicted_share_independent_own_rates"] for c in both]
    ratio_case = [c["configs"]["fake150"]["abnormal_share"] / c["configs"]["real150"]["share_without_root"] for c in both
                  if c["configs"]["real150"]["share_without_root"]]
    pos = [c for c in ok if all(c["configs"].get(n, {}).get("status") == "OK" for n in ("fake100a", "fake100b"))]
    unstable = sum(abs(c["configs"]["fake100a"]["abnormal_share"] - c["configs"]["fake100b"]["abnormal_share"]) >
                   0.5 * max(c["configs"]["fake100a"]["abnormal_share"], c["configs"]["fake100b"]["abnormal_share"]) for c in pos)
    medR, medF, medP = (statistics.median(x) if x else None for x in (R, F, pred))
    kt1 = {"n_cases": len(both), "median_R_real150_without_root": medR, "median_F_fake150": medF, "median_predicted_fake150": medP,
           "ratio_F_over_R_of_medians": medF / medR if medR else None, "ratio_F_over_R_by_case": q(ratio_case),
           "cases_F_ge_0.8R": sum(r >= 0.8 for r in ratio_case), "cases_F_le_0.5R": sum(r <= 0.5 for r in ratio_case),
           "predicted_within_20pct_of_F_by_case": sum(abs(c["configs"]["fake150"]["predicted_share_independent_own_rates"] - c["configs"]["fake150"]["abnormal_share"]) <=
                                                      0.2 * c["configs"]["fake150"]["abnormal_share"] for c in both),
           "fake_position_cases": len(pos), "fake_position_unstable_cases": int(unstable),
           "fake100a_minus_fake100b": q([c["configs"]["fake100a"]["abnormal_share"] - c["configs"]["fake100b"]["abnormal_share"] for c in pos])}
    kt1["mark_a"] = bool(medR and medF >= 0.8 * medR and medP is not None and abs(medP - medF) <= 0.2 * medF)
    kt1["mark_b"] = bool(medR and medF <= 0.5 * medR)
    kt1["mark_c"] = bool(medF is not None and medF >= 0.20 and pos and unstable >= len(pos) / 2)
    summary["kt1"] = kt1
    # KT-2
    busy = [dict(b, opaque_id=c["opaque_id"]) for c in ok for b in c["busy_operations"]]

    def kt2_block(rows):
        if not rows:
            return {"n": 0}
        fs, rs = [b["fake_share"] for b in rows], [b["real_share"] for b in rows]
        return {"n": len(rows), "fake_share": q(fs), "real_share": q(rs), "fake_ge_2pct": sum(v >= 0.02 for v in fs), "fake_lt_1pct": sum(v < 0.01 for v in fs),
                "real_ge_2pct": sum(v >= 0.02 for v in rs), "real_lt_1pct": sum(v < 0.01 for v in rs), "real_gt_fake": sum(r > f for r, f in zip(rs, fs)),
                "real_ge_2x_fake": sum(r >= 2 * f and r > 0 for r, f in zip(rs, fs)), "fake_zero": sum(v == 0 for v in fs)}

    kt2 = {"busy_n": BUSY_N, "all": kt2_block(busy), "by_class": {k: kt2_block([b for b in busy if b["class"] == k]) for k in sorted({str(b["class"]) for b in busy})},
           "by_fault": {f: kt2_block([b for c in ok if c["fault"] == f for b in c["busy_operations"]]) for f in sorted({c["fault"] for c in ok})},
           "cases_with_busy_operations": sum(bool(c["busy_operations"]) for c in ok)}
    a = kt2["all"]
    if a["n"]:
        kt2["mark_a"] = bool(a["fake_ge_2pct"] >= a["n"] / 2)
        kt2["mark_b"] = bool(a["fake_lt_1pct"] >= 0.75 * a["n"] and a["real_share"]["median"] >= 2 * a["fake_share"]["median"] and a["real_share"]["median"] > 0)
    pairs = [dict(p, opaque_id=c["opaque_id"], fault=c["fault"]) for c in ok for p in c["unrelated_above_root_tracerca"]]
    kt2["unrelated_above_root_tracerca"] = {"pairs": len(pairs), "real300_equals_stored": sum(p["real300_equals_stored"] for p in pairs),
                                             "stored_share": q([p["stored_a"] / p["stored_n"] for p in pairs if p["stored_n"]]),
                                             "real150_share": q([p["real150"]["share"] for p in pairs if p["real150"]]),
                                             "fake150_share": q([p["fake150"]["share"] for p in pairs if p["fake150"]]),
                                             "fake150_ge_2pct": sum(p["fake150"]["share"] >= 0.02 for p in pairs if p["fake150"] and p["fake150"]["share"] is not None),
                                             "fake150_lt_1pct": sum(p["fake150"]["share"] < 0.01 for p in pairs if p["fake150"] and p["fake150"]["share"] is not None),
                                             "no_fake150_baseline": sum(p["fake150"] is None for p in pairs)}
    summary["kt2"] = kt2
    result = {"schema": "T032-fake-marker-v1", "design": "results/T-032/thiet-ke-phep-doi-013.md mục 1", "configs": {k: [None if abs(x) == INF else x for x in v] for k, v in CONFIGS.items()},
              "fixtures": fx, "sources": {"plan_sha256": td.sha(td.PLAN), "labels_sha256": td.sha(td.LABELS), "spanpass_summary_sha256": td.sha(SPANPASS / "summary.json"),
                                          "link_cases_sha256": td.sha(LINK)},
              "note": "Chẩn đoán trên dev; cửa sổ ngắn hơn giao thức. Không là nhãn lan. Phép độc lập là giả định để so.",
              "methods_executed": [], "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("status", "self_check", "kt1")}, ensure_ascii=False, indent=1), flush=True)
    print(json.dumps({k: v for k, v in kt2.items() if k != "by_fault"}, ensure_ascii=False, indent=1), flush=True)
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
