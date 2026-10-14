"""T-032 phiên 10: tổng hợp K-2 theo loại cạnh của CIRCA (thiet-ke-phep-doi-005.md). Chỉ đọc file đã có; nhãn nối ở đây.

  python laptop_contrast_collect_v3.py <thư mục lượt k2x/k2s> <thư mục lượt có nhánh k2 (không cạnh)> <file kết quả mới>

Bốn nhánh được so trên bảng RHT (bản ghi `ols+rht`): native (sham của lượt mới), k2x (bỏ cạnh giữa hai dịch vụ),
k2s (bỏ cạnh cùng dịch vụ), k2 (không cạnh, lấy từ lượt circa-laptop-k2-001). Hit tính bi quan theo hòa.
Số của các nhánh đo tác động của một bước, không phải thành tích của một phương pháp.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import laptop_contrast_collect_v1 as v1  # noqa: E402

BRANCHES = ("native", "k2x", "k2s", "k2")


def main():
    run, run_k2, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    labels = v1.labels_for("circa_ols_da", "RE2-TT")
    cases = []
    for (dataset, opaque_id), label in sorted(labels.items()):
        base = {"opaque_id": opaque_id, **label}
        here, there = run / "cases" / dataset / opaque_id, run_k2 / "cases" / dataset / opaque_id
        dirs = {"native": v1.branch_dir(here, "sham"), "k2x": v1.branch_dir(here, "k2x"), "k2s": v1.branch_dir(here, "k2s"),
                "k2": v1.branch_dir(there, "k2")}
        if any(d is None for d in dirs.values()):
            cases.append({**base, "status": "MISSING_BRANCH", "missing": [b for b, d in dirs.items() if d is None]})
            continue
        checks = {b: v1.read(d / "check.json") for b, d in dirs.items()}
        if not checks["native"]["exact_vs_frozen"]:
            cases.append({**base, "status": "SHAM_NOT_EXACT"})
            continue
        records = {b: v1.read(d / "ban-ghi-1.json") for b, d in dirs.items()}  # ols+rht
        nodes = {b: records[b]["diagnostics"]["nodes"] for b in BRANCHES}
        root = label["root"]
        call_edges = [tuple(e) for e in records["native"]["extra"]["call_edges"]]
        callers = {a for a, b in call_edges if b == root}
        callees = {b for a, b in call_edges if a == root}
        views = {b: v1.view(records[b], root, callers, callees) for b in BRANCHES}
        shared = sorted(set.intersection(*(set(n) for n in nodes.values())))
        regressed = [n for n in shared if nodes["native"][n]["regression_route"] == "linear_regression"]
        item = {**base, "status": "OK", "has_huge_node_native": any(abs(v["rht_score"]) > v1.HUGE for v in nodes["native"].values()),
                "edges": {b: {k: checks[b]["info"].get(k) for k in ("edges_total", "edges_cross_service", "edges_same_service", "edges_removed", "edges_left")}
                          for b in ("k2x", "k2s")},
                "node_sets_equal": all(set(nodes[b]) == set(nodes["native"]) for b in BRANCHES),
                "huge_nodes": {b: sum(abs(nodes[b][n]["rht_score"]) > v1.HUGE for n in shared) for b in BRANCHES},
                "regressed_nodes_native": len(regressed),
                "regressed_nodes_still_with_parents": {b: sum(nodes[b][n]["regression_route"] == "linear_regression" for n in regressed) for b in ("k2x", "k2s")},
                "score_above_no_edges": {b: sum(nodes[b][n]["rht_score"] > nodes["k2"][n]["rht_score"] for n in regressed) for b in ("native", "k2x", "k2s")},
                "score_below_no_edges": {b: sum(nodes[b][n]["rht_score"] < nodes["k2"][n]["rht_score"] for n in regressed) for b in ("native", "k2x", "k2s")},
                "score_equals_native": {b: sum(float(nodes[b][n]["rht_score"]).hex() == float(nodes["native"][n]["rht_score"]).hex() for n in regressed)
                                        for b in ("k2x", "k2s")},
                "score_equals_no_edges": {b: sum(float(nodes[b][n]["rht_score"]).hex() == float(nodes["k2"][n]["rht_score"]).hex() for n in regressed)
                                          for b in ("k2x", "k2s")},
                "views": {b: {k: views[b].get(k) for k in ("root_ranked", "root_rank_min", "root_rank_max", "root_best_item", "n_entities")} for b in BRANCHES}}
        if all(views[b]["root_ranked"] for b in BRANCHES):
            item["effect_vs_native"] = {b: v1.effect(views["native"]["root_rank_min"], views[b]["root_rank_min"]) for b in ("k2x", "k2s", "k2")}
            item["pairs_above_root_native"] = {b: v1.pair_table(views["native"], records[b], root, callers, callees) for b in ("k2x", "k2s", "k2")}
        cases.append(item)
    ok = [c for c in cases if c["status"] == "OK" and "effect_vs_native" in c]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        result = {"n": len(rows),
                  "hit1": {b: count(lambda c, b=b: c["views"][b]["root_rank_max"] == 1) for b in BRANCHES},
                  "hit5": {b: count(lambda c, b=b: c["views"][b]["root_rank_max"] <= 5) for b in BRANCHES},
                  "effect_vs_native": {b: dict(Counter(c["effect_vs_native"][b] for c in rows)) for b in ("k2x", "k2s", "k2")},
                  "cases_with_huge_node": {b: count(lambda c, b=b: c["huge_nodes"][b] > 0) for b in BRANCHES},
                  "regressed_nodes_native": sum(c["regressed_nodes_native"] for c in rows),
                  "regressed_nodes_still_with_parents": {b: sum(c["regressed_nodes_still_with_parents"][b] for c in rows) for b in ("k2x", "k2s")},
                  "score_above_no_edges": {b: sum(c["score_above_no_edges"][b] for c in rows) for b in ("native", "k2x", "k2s")},
                  "score_below_no_edges": {b: sum(c["score_below_no_edges"][b] for c in rows) for b in ("native", "k2x", "k2s")},
                  "score_equals_native": {b: sum(c["score_equals_native"][b] for c in rows) for b in ("k2x", "k2s")},
                  "score_equals_no_edges": {b: sum(c["score_equals_no_edges"][b] for c in rows) for b in ("k2x", "k2s")},
                  "edges_removed": {b: sum(c["edges"][b]["edges_removed"] for c in rows) for b in ("k2x", "k2s")},
                  "edges_left": {b: sum(c["edges"][b]["edges_left"] for c in rows) for b in ("k2x", "k2s")}}
        pairs = {b: Counter() for b in ("k2x", "k2s", "k2")}
        for c in rows:
            for b in pairs:
                for pair in c["pairs_above_root_native"][b].values():
                    pairs[b][pair["relation"] + ("|còn trên root" if pair["still_above"] else "|không còn trên root")] += 1
        result["pairs_above_root_native"] = {b: dict(sorted(v.items())) for b, v in pairs.items()}
        return result

    summary = {"n_cases": len(cases), "status_counts": dict(Counter(c["status"] for c in cases)),
               "node_sets_equal": sum(bool(c.get("node_sets_equal")) for c in cases),
               "all": tally(ok), "cases_with_huge_node": tally([c for c in ok if c["has_huge_node_native"]]),
               "cases_without_huge_node": tally([c for c in ok if not c["has_huge_node_native"]]),
               "note": "k2x bỏ cạnh giữa hai dịch vụ; k2s bỏ cạnh cùng dịch vụ; k2 không cạnh. Phép đổi chẩn đoán trên dev, không thay số P3."}
    v1.write(out, {"schema": "T032-CIRCA-K2-edge-types-v1", "design": "results/T-032/thiet-ke-phep-doi-005.md",
                   "run": run.relative_to(v1.BASE).as_posix(), "run_k2": run_k2.relative_to(v1.BASE).as_posix(),
                   "this_script_sha256": v1.sha(__file__), "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
