"""T-032 phiên 13: tổng hợp KT-9 của CIRCA (thiet-ke-phep-doi-013.md mục 5). Chỉ đọc file đã có; nhãn nối ở đây.

  python laptop_contrast_collect_v6.py <thư mục lượt KT-9> <thư mục lượt có nhánh k2 native> <file kết quả mới>

Ba cấu hình cửa sổ, mỗi cấu hình một nhánh có cạnh và một nhánh không cạnh:
  native: shamw (lượt KT-9; phải khớp bản đóng băng từng bit) và k2 (lượt circa-laptop-k2-001)
  tf:     học 291 điểm;  tf và tfk2
  t0:     chấm 10 điểm ngay sau mốc;  t0 và t0k2
Tỷ số điểm của một nút = điểm RHT ở nhánh có cạnh / điểm RHT ở nhánh không cạnh, trên các nút có hồi quy theo cha ở nhánh có cạnh
và có mặt ở nhánh không cạnh. Số của các nhánh đo tác động của một bước, không phải thành tích của một phương pháp.
"""
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import laptop_contrast_collect_v1 as v1  # noqa: E402

WINDOWS = {"native": ("shamw", "k2"), "tf": ("tf", "tfk2"), "t0": ("t0", "t0k2")}
BINS = (("1", 1, 1), ("2-4", 2, 4), ("5", 5, 5), ("6", 6, 6), ("7", 7, 7), ("8+", 8, 10**9))
DESIGN_BINS = (("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), ("8+", 8, 10**9))


def q(values):
    values = sorted(values)
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def main():
    run, run_k2, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    labels = v1.labels_for("circa_ols_da", "RE2-TT")
    cases, nodes_all = [], {w: [] for w in WINDOWS}
    for (dataset, opaque_id), label in sorted(labels.items()):
        base = {"opaque_id": opaque_id, **label}
        here, there = run / "cases" / dataset / opaque_id, run_k2 / "cases" / dataset / opaque_id
        dirs = {b: v1.branch_dir(here, b) for b in ("shamw", "tf", "tfk2", "t0", "t0k2")}
        dirs["k2"] = v1.branch_dir(there, "k2")
        if any(d is None for d in dirs.values()):
            cases.append({**base, "status": "MISSING_BRANCH", "missing": [b for b, d in dirs.items() if d is None]})
            continue
        checks = {b: v1.read(d / "check.json") for b, d in dirs.items()}
        if not checks["shamw"]["exact_vs_frozen"]:
            cases.append({**base, "status": "SHAM_NOT_EXACT"})
            continue
        rht = {b: v1.read(d / "ban-ghi-1.json") for b, d in dirs.items()}   # ols+rht
        da = {b: v1.read(d / "ban-ghi-0.json") for b, d in dirs.items()}    # ols+rht_da
        root = label["root"]
        call_edges = [tuple(e) for e in rht["shamw"]["extra"]["call_edges"]]
        callers = {a for a, b in call_edges if b == root}
        callees = {b for a, b in call_edges if a == root}
        item = {**base, "status": "OK", "windows": {}, "branch_statuses": {b: checks[b]["branch_statuses"] for b in dirs},
                "hook": {b: {"case_calls": checks[b]["info"].get("case_calls"), "score_calls": checks[b]["info"].get("score_calls"),
                             "edges_left": checks[b]["info"].get("edges_left")} for b in ("shamw", "tf", "tfk2", "t0", "t0k2")}}
        for w, (eb, kb) in WINDOWS.items():
            if rht[eb]["status"] != "OK" or rht[kb]["status"] != "OK":
                item["windows"][w] = {"status": "nhánh không OK: " + rht[eb]["status"] + ", " + rht[kb]["status"]}
                continue
            en, kn = rht[eb]["diagnostics"]["nodes"], rht[kb]["diagnostics"]["nodes"]
            regressed = [n for n in en if en[n]["regression_route"] == "linear_regression"]
            shared = [n for n in regressed if n in kn]
            up = sum(en[n]["rht_score"] > kn[n]["rht_score"] for n in shared)
            down = sum(en[n]["rht_score"] < kn[n]["rht_score"] for n in shared)
            rows = []
            for n in shared:
                e, k = float(en[n]["rht_score"]), float(kn[n]["rht_score"])
                row = {"node": n, "n_parents": len(en[n]["parents"]), "edge": e, "noedge": k}
                if abs(e) <= v1.HUGE and abs(k) <= v1.HUGE and k > 0 and e > 0:
                    row["ratio"] = e / k
                rows.append(row)
            for r in rows:
                nodes_all[w].append({**r, "opaque_id": opaque_id})
            ve, vk = v1.view(rht[eb], root, callers, callees), v1.view(rht[kb], root, callers, callees)
            vda = v1.view(da[eb], root, callers, callees)
            item["windows"][w] = {
                "status": "OK", "nodes_edge": len(en), "nodes_noedge": len(kn), "nodes_only_edge": len(set(en) - set(kn)), "nodes_only_noedge": len(set(kn) - set(en)),
                "regressed": len(regressed), "regressed_shared": len(shared), "score_above_noedge": up, "score_below_noedge": down, "score_equal": len(shared) - up - down,
                "huge_nodes_edge": sum(abs(float(v["rht_score"])) > v1.HUGE for v in en.values()),
                "huge_node_names": sorted(n for n, v in en.items() if abs(float(v["rht_score"])) > v1.HUGE)[:5],
                "huge_nodes_noedge": sum(abs(float(v["rht_score"])) > v1.HUGE for v in kn.values()),
                "ratio": q([r["ratio"] for r in rows if "ratio" in r]),
                "root_rht": {k: ve.get(k) for k in ("root_ranked", "root_rank_min", "root_rank_max", "root_best_item", "n_entities")},
                "root_rht_noedge": {k: vk.get(k) for k in ("root_ranked", "root_rank_min", "root_rank_max", "root_best_item", "n_entities")},
                "root_da": {k: vda.get(k) for k in ("root_ranked", "root_rank_min", "root_rank_max", "root_best_item", "n_entities")}}
        item["has_huge_node_native"] = item["windows"].get("native", {}).get("huge_nodes_edge", 0) > 0
        cases.append(item)
    ok = [c for c in cases if c["status"] == "OK"]

    def node_block(rows):
        with_ratio = [r for r in rows if "ratio" in r]
        res = {"regressed_shared": len(rows), "score_above_noedge": sum(r["edge"] > r["noedge"] for r in rows),
               "score_below_noedge": sum(r["edge"] < r["noedge"] for r in rows), "with_ratio": len(with_ratio),
               "ratio_ge_1": sum(r["ratio"] >= 1 for r in with_ratio), "ratio": q([r["ratio"] for r in with_ratio]), "by_n_parents": {}, "by_n_parents_design_bins": {}}
        res["share_above"] = res["score_above_noedge"] / len(rows) if rows else None
        for target, bins in (("by_n_parents", BINS), ("by_n_parents_design_bins", DESIGN_BINS)):
            for name, lo, hi in bins:
                part = [r["ratio"] for r in with_ratio if lo <= r["n_parents"] <= hi]
                res[target][name] = q(part)
        return res

    def tally(rows, case_filter):
        ids = {c["opaque_id"] for c in rows}
        res = {"n_cases": len(rows)}
        for w in WINDOWS:
            usable = [c for c in rows if c["windows"].get(w, {}).get("status") == "OK"]
            block = node_block([r for r in nodes_all[w] if r["opaque_id"] in ids and case_filter(r["opaque_id"])])
            block.update({"cases_usable": len(usable), "cases_with_huge_node": sum(c["windows"][w]["huge_nodes_edge"] > 0 for c in usable),
                          "huge_nodes": sum(c["windows"][w]["huge_nodes_edge"] for c in usable),
                          "nodes_only_edge": sum(c["windows"][w]["nodes_only_edge"] for c in usable),
                          "nodes_only_noedge": sum(c["windows"][w]["nodes_only_noedge"] for c in usable),
                          "nodes_edge_total": sum(c["windows"][w]["nodes_edge"] for c in usable)})
            for key in ("root_rht", "root_rht_noedge", "root_da"):
                ranked = [c for c in usable if c["windows"][w][key]["root_ranked"]]
                block[key] = {"ranked": len(ranked), "hit1": sum(c["windows"][w][key]["root_rank_max"] == 1 for c in ranked),
                              "hit5": sum(c["windows"][w][key]["root_rank_max"] <= 5 for c in ranked)}
            res[w] = block
        return res

    groups = {"all": ok, "cases_with_huge_node_native": [c for c in ok if c["has_huge_node_native"]],
              "cases_without_huge_node_native": [c for c in ok if not c["has_huge_node_native"]]}
    summary = {"n_cases": len(cases), "status_counts": dict(Counter(c["status"] for c in cases)),
               "self_check": {"shamw_exact_vs_frozen": sum(c["status"] == "OK" for c in cases),
                              "hook_native_values": sum(c["status"] == "OK" and c["hook"]["shamw"]["case_calls"] == [{"train_window": 111, "test_window": 10, "lookup_window_points": 120}]
                                                        and all(s["current_used"] == s["current_native"] for s in c["hook"]["shamw"]["score_calls"]) for c in cases),
                              "tf_train_window_291": sum(c["status"] == "OK" and all(k["train_window"] == 291 for b in ("tf", "tfk2") for k in c["hook"][b]["case_calls"]) for c in cases),
                              "t0_current_is_t_plus_9": sum(c["status"] == "OK" and all(s["current_used"] == s["detect_time"] + 9 for b in ("t0", "t0k2") for s in c["hook"][b]["score_calls"]) for c in cases),
                              "noedge_branches_have_no_edges": sum(c["status"] == "OK" and all(c["hook"][b]["edges_left"] == 0 for b in ("tfk2", "t0k2")) for c in cases)}}
    for name, rows in groups.items():
        summary[name] = tally(rows, lambda _i: True)
    # mốc đã khai trước (thiet-ke-phep-doi-013.md mục 5), trên mọi ca
    nat, marks = summary["all"]["native"], {}
    for w in ("tf", "t0"):
        b = summary["all"][w]
        m8n, m8 = nat["by_n_parents"]["8+"].get("median"), b["by_n_parents"]["8+"].get("median")
        marks[w] = {"median_ratio_8plus_native": m8n, "median_ratio_8plus": m8, "share_above_native": nat["share_above"], "share_above": b["share_above"],
                    "ratio_8plus_below_half_of_native": bool(m8 is not None and m8n is not None and m8 < 0.5 * m8n),
                    "share_above_drops_10_points": bool(b["share_above"] is not None and nat["share_above"] - b["share_above"] >= 0.10)}
        marks[w]["mark_met"] = marks[w]["ratio_8plus_below_half_of_native"] and marks[w]["share_above_drops_10_points"]
    summary["marks"] = marks
    v1.write(out, {"schema": "T032-CIRCA-KT9-windows-v1", "design": "results/T-032/thiet-ke-phep-doi-013.md mục 5",
                   "run": run.relative_to(v1.BASE).as_posix(), "run_k2": run_k2.relative_to(v1.BASE).as_posix(),
                   "this_script_sha256": v1.sha(__file__), "note": "Nhánh chẩn đoán trên dev; không thay cửa sổ đã khóa và số đã chấm.",
                   "summary": summary, "cases": cases})
    print(json.dumps({k: summary[k] for k in ("status_counts", "self_check", "marks")}, ensure_ascii=False, indent=1))
    for g in groups:
        for w in WINDOWS:
            b = summary[g][w]
            print(g, w, "cases", b["cases_usable"], "regressed", b["regressed_shared"], "above", b["score_above_noedge"], "below", b["score_below_noedge"],
                  "share", None if b["share_above"] is None else round(b["share_above"], 3), "ratio_med", b["ratio"].get("median"),
                  "by_parents", {k: (v.get("n"), None if "median" not in v else round(v["median"], 2)) for k, v in b["by_n_parents"].items()},
                  "huge cases", b["cases_with_huge_node"], "huge nodes", b["huge_nodes"], "RHT hit1/5", b["root_rht"], "noedge", b["root_rht_noedge"], "DA", b["root_da"])
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
