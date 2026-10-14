"""T-032 bản 011 mục 3 (phép T-O, ngoài gói, Minh duyệt 11/10/2026): bước xếp hạng của bài TraceRCA gốc, cài theo lời văn
của bài (Mục III) trên dữ liệu của ta. KHÔNG phải mã của tác giả, không tái lập bài gốc. Chạy trên EC2, chỉ đọc.

Lời gọi = cặp span cha–con khác dịch vụ. Nền theo cặp dịch vụ trên lời gọi trước mốc. Lời gọi bất thường khi |v − mean|/std > ngưỡng.
Trace bất thường khi có lời gọi bất thường. Tập dịch vụ đạt support >= 10% trong trace bất thường; chỉ số Jaccard; giữ 100 tập đầu
(giữ cả tập hòa ở vị trí cuối). Điểm trong tập = |số trace có lời gọi bất thường đi vào − số trace có lời gọi bất thường đi ra|.
Điểm dịch vụ = max(Jaccard × điểm trong tập). Nhãn root chỉ dùng để đọc hạng ở cuối.
Dùng: python tracerca_original_ranking_v1.py <thư mục lượt mới> [dataset:opaque_id]
"""
import json
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402
import chain_position_v1 as cp  # noqa: E402

BRANCHES = {"to_p": ("d_p", 1.0), "to_c": ("d_c", 1.0), "to_p3": ("d_p", 3.0)}
MIN_SUPPORT, TOP_K, FS, MAX_SETS = Fraction(1, 10), 100, 0.10, 2_000_000


def rank_of(scores):
    out, offset = {}, 0
    for value in sorted(set(scores.values()), reverse=True):
        group = [e for e, s in scores.items() if s == value]
        for e in group:
            out[e] = (offset + 1, offset + len(group))
        offset += len(group)
    return out


def score_services(patterns, n_services):
    """patterns: Counter{(mask, in_mask, out_mask, abnormal): số trace}. Trả điểm theo chỉ số dịch vụ và thông tin kèm."""
    rows = list(patterns.items())
    mask = np.array([k[0] for k, _ in rows], dtype="int64")
    in_m = np.array([k[1] for k, _ in rows], dtype="int64")
    out_m = np.array([k[2] for k, _ in rows], dtype="int64")
    abn = np.array([k[3] for k, _ in rows], dtype=bool)
    cnt = np.array([c for _, c in rows], dtype="int64")
    Y = int(cnt[abn].sum())
    info = {"traces": int(cnt.sum()), "abnormal_traces": Y, "distinct_patterns": len(rows)}
    if Y == 0:
        return {}, {**info, "status": "NO_ABNORMAL_TRACE"}
    need = MIN_SUPPORT * Y
    sets = []   # (JI, bitmask, XY, X)
    amask, acnt = mask[abn], cnt[abn]

    def grow(current, start):
        for s in range(start, n_services):
            cand = current | (1 << s)
            xy = int(acnt[(amask & cand) == cand].sum())
            if xy >= need:
                x = int(cnt[(mask & cand) == cand].sum())
                sets.append((Fraction(xy, x + Y - xy), cand, xy, x))
                if len(sets) > MAX_SETS:
                    raise OverflowError("quá nhiều tập")
                grow(cand, s + 1)

    try:
        grow(0, 0)
    except OverflowError:
        return {}, {**info, "status": "TOO_MANY_SETS"}
    info["frequent_sets"] = len(sets)
    if not sets:
        return {}, {**info, "status": "NO_FREQUENT_SET"}
    sets.sort(key=lambda z: (-z[0], z[1]))
    cut = sets[min(TOP_K, len(sets)) - 1][0]
    top = [z for z in sets if z[0] >= cut]
    info.update(top_sets=len(top), top_ji_max=float(top[0][0]), top_ji_min=float(top[-1][0]), status="OK")
    scores, best = {}, {}
    for ji, cand, xy, x in top:
        inside = (mask & cand) == cand
        for s in range(n_services):
            if not (cand >> s) & 1:
                continue
            bit = 1 << s
            n_in = int(cnt[inside & ((in_m & bit) != 0)].sum())
            n_out = int(cnt[inside & ((out_m & bit) != 0)].sum())
            value = ji * abs(n_in - n_out)
            if s not in scores or value > scores[s]:
                scores[s] = value
                best[s] = {"set_size": bin(cand).count("1"), "ji": float(ji), "n_in": n_in, "n_out": n_out, "in_set_score": abs(n_in - n_out)}
    info["best"] = best
    return scores, info


def fixtures():
    """Hình 2 của bài: 5 trace, 3 bất thường đều đi qua A và B; A chỉ có lời gọi ra bất thường, B có cả vào lẫn ra."""
    A, B, Cc, D, E, F = (1 << i for i in range(6))
    p = Counter()
    p[(A | B | D | E, B | D | E, A | B, True)] += 1      # A→B, B→D, B→E bất thường
    p[(A | B | Cc | D, B | Cc | D, A | B, True)] += 1
    p[(A | B | Cc | E, B | Cc | E, A | B, True)] += 1
    p[(A | F, 0, 0, False)] += 1
    p[(E | A, 0, 0, False)] += 1
    scores, info = score_services(p, 6)
    b = info["best"]
    leaf = Counter({(A | B, B, A, True): 4, (A | Cc, 0, 0, False): 6})           # A gọi B, lời gọi A→B bất thường: B chỉ có lời gọi vào
    s2, i2 = score_services(leaf, 3)
    mid = Counter({(A | B | Cc, B | Cc, A | B, True): 5, (A | D, 0, 0, False): 5})   # A→B→C đều bất thường: B ở giữa
    s3, i3 = score_services(mid, 4)
    s4, i4 = score_services(Counter({(A | B, 0, 0, False): 7}), 2)
    checks = {"Hình 2: A có điểm trong tập 3 (3 ra, 0 vào)": b[0]["in_set_score"] == 3 and b[0]["n_out"] == 3 and b[0]["n_in"] == 0,
              "Hình 2: B có điểm trong tập 0 ở tập {A,B}": scores[1] == 0,
              "Hình 2: A đứng đầu": rank_of({s: scores.get(s, Fraction(0)) for s in range(6)})[0] == (1, 1),
              "lá chuỗi: A và B cùng có điểm trong tập 4, hòa": s2[0] == s2[1] and i2["best"][1]["n_in"] == 4 and i2["best"][0]["n_out"] == 4,
              "giữa chuỗi: B có điểm 0, A và C dương": s3[1] == 0 and s3[0] > 0 and s3[2] > 0,
              "không có trace bất thường": s4 == {} and i4["status"] == "NO_ABNORMAL_TRACE"}
    return {"pass": all(bool(v) for v in checks.values()), "checks": {k: bool(v) for k, v in checks.items()}}


def one_case(spans, t_us):
    spans = spans.reset_index(drop=True)
    start = spans["startTime"].to_numpy(dtype="int64")
    duration = spans["duration"].to_numpy(dtype="int64")
    end = start + duration
    service = spans["serviceName"].astype(str).to_numpy()
    tid = spans["traceID"].astype(str).to_numpy()
    services = sorted(set(service))
    sid = {s: i for i, s in enumerate(services)}
    ident = (spans["traceID"].astype(str) + "|" + spans["spanID"].astype(str)).to_numpy()
    position = pd.Series(np.arange(len(spans)), index=ident)
    position = position[~position.index.duplicated(keep=False)]
    parent = (spans["traceID"].astype(str) + "|" + spans["parentSpanID"].astype(str)).map(position).to_numpy(dtype="float64")
    has_parent = ~np.isnan(parent)
    p = np.where(has_parent, parent, 0).astype("int64")
    cross = has_parent & (service[p] != service)
    c_index, p_index = np.flatnonzero(cross), p[cross]
    inv = pd.DataFrame({"trace": tid[p_index], "src": service[p_index], "dst": service[c_index], "d_p": duration[p_index].astype("float64"),
                        "d_c": duration[c_index].astype("float64"), "after": end[p_index] >= t_us})
    inv["pair"] = inv["src"] + "→" + inv["dst"]
    callers = {}
    for src, dst in inv[["src", "dst"]].drop_duplicates().itertuples(index=False):
        callers.setdefault(dst, []).append(src)
    out = {"services": services, "callers_by_service": {k: sorted(v) for k, v in callers.items()},
           "invocations": {"before": int((~inv["after"]).sum()), "after": int(inv["after"].sum()), "pairs": int(inv["pair"].nunique())}, "branches": {}}
    for name, (column, threshold) in BRANCHES.items():
        base = inv[~inv["after"]].groupby("pair")[column].agg(["mean", "std", "count"])
        usable = base[(base["count"] >= 2) & (base["std"] > 0)]
        mean, std = inv["pair"].map(usable["mean"]), inv["pair"].map(usable["std"])
        severity = ((inv[column] - mean).abs() / std).to_numpy()
        evaluable = ~np.isnan(severity)
        after = inv["after"].to_numpy()
        sev_before = float(np.mean(severity[evaluable & ~after])) if (evaluable & ~after).any() else None
        sev_after = float(np.mean(severity[evaluable & after])) if (evaluable & after).any() else None
        useful = sev_before is not None and sev_after is not None and (sev_after - sev_before) > FS * sev_before
        abnormal = evaluable & after & (severity > threshold)
        info = {"feature": column, "threshold_sigma": threshold, "pairs_usable": int(len(usable)), "pairs_total": int(len(base)),
                "after_invocations_not_evaluable": int((after & ~evaluable).sum()), "mean_severity_before": sev_before, "mean_severity_after": sev_after,
                "feature_useful": bool(useful), "abnormal_invocations": int(abnormal.sum()),
                "abnormal_share_of_after_invocations": float(abnormal.sum() / max(1, (after & evaluable).sum())),
                "abnormal_share_before_same_rule": float((evaluable & ~after & (severity > threshold)).sum() / max(1, (evaluable & ~after).sum()))}
        if not useful:
            out["branches"][name] = {**info, "status": "NO_USEFUL_FEATURE", "scores": {}}
            continue
        a = inv[after].copy()
        a["abn"] = abnormal[after]
        a["sbit"] = a["src"].map(lambda s: 1 << sid[s])
        a["dbit"] = a["dst"].map(lambda s: 1 << sid[s])
        patterns = Counter()
        for _trace, g in a.groupby("trace", sort=False):
            mask = int(np.bitwise_or.reduce(g["sbit"].to_numpy() | g["dbit"].to_numpy()))
            ab = g[g["abn"]]
            in_mask = int(np.bitwise_or.reduce(ab["dbit"].to_numpy())) if len(ab) else 0
            out_mask = int(np.bitwise_or.reduce(ab["sbit"].to_numpy())) if len(ab) else 0
            patterns[(mask, in_mask, out_mask, bool(len(ab)))] += 1
        scores, sinfo = score_services(patterns, len(services))
        named = {services[s]: [v.numerator, v.denominator] for s, v in scores.items()}
        sinfo["best"] = {services[s]: v for s, v in sinfo.get("best", {}).items()}
        out["branches"][name] = {**info, **sinfo, "scores": named}
    return out


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    only = sys.argv[2] if len(sys.argv) > 2 else None
    fx = fixtures()
    (out / "fixtures.json").write_text(json.dumps(fx, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not fx["pass"]:
        raise SystemExit("trường hợp tự dựng không đạt: " + json.dumps(fx, ensure_ascii=False))
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    labels = {(r["dataset"], r["opaque_id"]): r for r in cp.read(cp.LABELS)["main_rows"] if r["method"] == "tracerca"}
    # cặp "chủ yếu là chờ root" của bản thư viện (ket-qua-phien-11.md mục 2.1): thực thể phía trên, đứng trên root, tỷ lệ r50 >= 0,5, ca xét được
    waiting = {}
    link_path = BASE / "runs/slow-call-flag-link-001/cases.json"
    for c in cp.read(link_path):
        if c["method"] == "tracerca" and c.get("root_ranked") and c.get("root_edge_measurable"):
            names = [e["entity"] for e in c["entities"] if e["above_root"] and e["class"] in ("goi_truc_tiep", "phia_tren_gian_tiep", "hai_chieu")
                     and "span" in e and (e["span"]["share_r50"] or 0) >= 0.5]
            if names:
                waiting[(c["dataset"], c["opaque_id"])] = names
    cases = []
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
        else:
            entry = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == opaque_id][0]
            t = int(td.read(BASE / "repo" / entry["path"])["window"]["t"])
            files = selector.chon_ca(allow, opaque_id, Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
            spans = cua_so.cat_span(pd.read_parquet(files["traces.parquet"]), t)
        computed = one_case(spans, t * 1_000_000)          # chưa dùng nhãn
        label = labels[(dataset, opaque_id)]
        root = label["root"]
        item = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": label["fault"], "cell": label["cell"], "library_status": label["status"],
                "library_rank": [label.get("rank_min"), label.get("rank_max")], "invocations": computed["invocations"], "branches": {}}
        root_callers = computed["callers_by_service"].get(root, [])
        item["root_callers"] = root_callers
        item["waiting_callers_library"] = waiting.get((dataset, opaque_id), [])
        for name, b in computed["branches"].items():
            view = {k: v for k, v in b.items() if k not in ("scores", "best")}
            if b.get("status") == "OK":
                scores = {s: Fraction(*b["scores"][s]) if s in b["scores"] else Fraction(0) for s in computed["services"]}
                rank = rank_of(scores)
                view["n_entities"] = len(rank)
                view["positive_scores"] = sum(v > 0 for v in scores.values())
                if root in rank:
                    view.update(root_in_spans=True, root_score_positive=scores[root] > 0, root_rank_min=rank[root][0], root_rank_max=rank[root][1],
                                above=sorted(e for e in rank if e != root and rank[e][1] < rank[root][0]), root_best=b["best"].get(root))
                else:
                    view["root_in_spans"] = False
                view["top"] = sorted(e for e in rank if rank[e][0] == 1)
                view["top_best"] = {e: b["best"].get(e) for e in view["top"][:3]}
                if root in rank:
                    def relation(c):
                        return "root trên" if rank[root][1] < rank[c][0] else "root dưới" if rank[c][1] < rank[root][0] else "hòa"
                    view["root_vs_direct_callers"] = {c: relation(c) for c in root_callers if c in rank}
                    view["root_vs_waiting_callers_library"] = {c: relation(c) for c in item["waiting_callers_library"] if c in rank}
            item["branches"][name] = view
        item["wall_s"] = round(time.time() - began, 1)
        cases.append(item)
        print(dataset, opaque_id, {n: (v.get("status"), v.get("root_rank_min"), v.get("root_rank_max"), v.get("abnormal_traces"), v.get("traces")) for n, v in item["branches"].items()},
              item["wall_s"], flush=True)
    (out / "cases.json").write_text(json.dumps({"schema": "T032-tracerca-original-ranking-v1", "design": "results/T-032/thiet-ke-phep-doi-011.md mục 3",
                                               "fixtures": fx, "cases": cases, "methods_executed": []}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    summary = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        rows = [c for c in cases if c["dataset"] == dataset]
        for name in BRANCHES:
            vs = [(c, c["branches"][name]) for c in rows]
            ok = [(c, v) for c, v in vs if v.get("status") == "OK" and v.get("root_in_spans")]
            pos = [(c, v) for c, v in ok if v["root_score_positive"]]
            lib_ok = [(c, v) for c, v in ok if c["library_status"] == "OK" and c["library_rank"][0] is not None]
            block = {"cases": len(rows), "status": dict(Counter(str(v.get("status")) for _c, v in vs)), "ranked_cases": len(ok),
                     "root_score_positive": len(pos), "root_score_zero_ids": [c["opaque_id"] for c, v in ok if not v["root_score_positive"]],
                     "hit1": sum(v["root_rank_max"] == 1 for _c, v in ok), "hit5": sum(v["root_rank_max"] <= 5 for _c, v in ok),
                     "root_rank_min_1": sum(v["root_rank_min"] == 1 for _c, v in ok),
                     "top_entities": dict(Counter(e for _c, v in ok for e in v["top"]).most_common(6)),
                     "abnormal_trace_share": sorted(round(v["abnormal_traces"] / v["traces"], 3) for _c, v in ok if v.get("traces"))[::max(1, len(ok) // 6)],
                     "abnormal_share_before_same_rule_median": float(np.median([v["abnormal_share_before_same_rule"] for _c, v in ok])) if ok else None,
                     "abnormal_share_after_median": float(np.median([v["abnormal_share_of_after_invocations"] for _c, v in ok])) if ok else None,
                     "direct_caller_pairs": dict(Counter(r for _c, v in ok for r in v.get("root_vs_direct_callers", {}).values())),
                     "cases_root_above_all_direct_callers": sum(bool(v.get("root_vs_direct_callers")) and all(r == "root trên" for r in v["root_vs_direct_callers"].values()) for _c, v in ok),
                     "cases_with_direct_callers": sum(bool(v.get("root_vs_direct_callers")) for _c, v in ok),
                     "waiting_caller_pairs_library": dict(Counter(r for _c, v in ok for r in v.get("root_vs_waiting_callers_library", {}).values())),
                     "waiting_cases_library": sum(bool(c["waiting_callers_library"]) for c in rows),
                     "library_comparison": {"cases_both_ranked": len(lib_ok), "hit1_library": sum(c["library_rank"][1] == 1 for c, _v in lib_ok),
                                            "hit1_branch": sum(v["root_rank_max"] == 1 for _c, v in lib_ok),
                                            "root_better_than_library": sum(v["root_rank_min"] < c["library_rank"][0] for c, v in lib_ok),
                                            "root_worse_than_library": sum(v["root_rank_min"] > c["library_rank"][0] for c, v in lib_ok)},
                     "by_fault": {f: {"n": len(g), "hit1": sum(v["root_rank_max"] == 1 for _c, v in g), "root_positive": sum(v["root_score_positive"] for _c, v in g)}
                                  for f, g in ((f, [(c, v) for c, v in ok if c["fault"] == f]) for f in sorted({c["fault"] for c, _v in ok}))}}
            summary.setdefault(dataset, {})[name] = block
    (out / "summary.json").write_text(json.dumps({"schema": "T032-tracerca-original-ranking-summary-v1", "design": "results/T-032/thiet-ke-phep-doi-011.md mục 3",
                                                 "name": "bước xếp hạng của bài TraceRCA gốc, cài theo lời văn của bài trên dữ liệu của ta; không phải mã của tác giả",
                                                 "fixtures": fx, "summary": summary, "methods_executed": []}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for dataset, b in summary.items():
        for name, r in b.items():
            print("==", dataset, name, r["status"], "ranked", r["ranked_cases"], "root>0", r["root_score_positive"], "hit1", r["hit1"], "hit5", r["hit5"], "rank_min1", r["root_rank_min_1"],
                  "| top", r["top_entities"], "| callers", r["direct_caller_pairs"], "| waiting", r["waiting_caller_pairs_library"], "| lib", r["library_comparison"],
                  "| abn share", r["abnormal_trace_share"], "before/after inv", r["abnormal_share_before_same_rule_median"], r["abnormal_share_after_median"], flush=True)
    print("XONG", len(cases), flush=True)


if __name__ == "__main__":
    main()
