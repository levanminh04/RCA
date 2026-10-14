"""T-032 phiên 10: tổng hợp các lượt của laptop_contrast_v1.py. Chỉ đọc file đã có; nhãn root nối ở đây.

  python laptop_contrast_collect_v1.py circa <thư mục lượt> <file kết quả mới>
  python laptop_contrast_collect_v1.py microrank <thư mục lượt> <file kết quả mới>

CIRCA: K-2 (thiet-ke-phep-doi-001.md mục 8, bản 003 mục 2) và các đại lượng đọc từ nhánh quan sát.
MicroRank: M-D (bản 001 mục 4, bản 003 mục 3).
Hit tính bi quan theo hòa. Số của nhánh phép đổi đo tác động của một bước, không phải thành tích của phương pháp.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
BASE = REPO / "results/T-032"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
CALLER_ROOT = BASE / "runs/caller-root-phien9-001/caller-root.json"
HUGE = 1e10


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=1, allow_nan=True)
        stream.write("\n")


def branch_dir(case_dir, branch):
    """Thư mục lần chạy có check.json của một nhánh (lần 1, hoặc lần 2, 3 nếu lần trước bị giết vì RAM)."""
    for name in (branch, branch + "-lan2", branch + "-lan3"):
        if (case_dir / name / "check.json").is_file():
            return case_dir / name
    return None


def ranks(record):
    groups = {}
    for row in record["entity_ranking"]:
        groups.setdefault(row["tie_group"], []).append(row["entity"])
    out, offset = {}, 0
    for group in sorted(groups):
        for entity in groups[group]:
            out[entity] = (offset + 1, offset + len(groups[group]))
        offset += len(groups[group])
    return out


def entity_scores(record):
    best = {}
    for row in record["ranking"]:
        best.setdefault(row["entity"], (row["item"], row["key"]))
    return best


def margin(a, b):
    return None if abs(a) + abs(b) == 0 else (a - b) / (abs(a) + abs(b))


def view(record, root, callers, callees):
    rank = ranks(record)
    best = entity_scores(record)
    if root not in rank:
        return {"root_ranked": False, "n_entities": len(rank)}
    above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
    root_score = best[root][1][0]
    return {"root_ranked": True, "n_entities": len(rank), "root_rank_min": rank[root][0], "root_rank_max": rank[root][1],
            "root_best_item": best[root][0], "root_key": best[root][1],
            "above_root": [{"entity": e, "relation": "caller_of_root" if e in callers else "callee_of_root" if e in callees else "other",
                            "rank_min": rank[e][0], "best_item": best[e][0], "key_first": best[e][1][0],
                            "key_first_huge": abs(best[e][1][0]) > HUGE, "margin_vs_root": margin(best[e][1][0], root_score)} for e in above]}


def effect(native_min, changed_min):
    return "tăng hạng" if changed_min < native_min else "giảm hạng" if changed_min > native_min else "không đổi"


def labels_for(method_name, dataset=None):
    out = {}
    for row in read(LABELS)["main_rows"]:
        if row["method"] == method_name and (dataset is None or row["dataset"] == dataset):
            out[(row["dataset"], row["opaque_id"])] = {"root": row["root"], "fault": row["fault"], "cell": row["cell"],
                                                       "t028": {"status": row["status"], "rank_min": row["rank_min"], "rank_max": row["rank_max"]}}
    return out


def pair_table(native_view, changed_record, root, callers, callees):
    """Với từng thực thể đứng trên root ở bảng native: margin ở hai nhánh và còn đứng trên root hay không."""
    changed_rank = ranks(changed_record)
    changed_best = entity_scores(changed_record)
    pairs = {}
    for item in native_view["above_root"]:
        e = item["entity"]
        row = {"relation": item["relation"], "margin_native": item["margin_vs_root"], "key_first_huge_native": item["key_first_huge"]}
        if e in changed_rank and root in changed_rank:
            row["margin_changed"] = margin(changed_best[e][1][0], changed_best[root][1][0])
            row["delta"] = None if row["margin_changed"] is None or row["margin_native"] is None else row["margin_native"] - row["margin_changed"]
            row["still_above"] = changed_rank[e][1] < changed_rank[root][0]
        else:
            row["margin_changed"], row["delta"], row["still_above"] = None, None, None
        pairs[e] = row
    return pairs


def quantiles(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def collect_circa(run, out):
    labels = labels_for("circa_ols_da", "RE2-TT")
    cases = []
    for (dataset, opaque_id), label in sorted(labels.items()):
        base = {"opaque_id": opaque_id, **label}
        case_dir = run / "cases" / dataset / opaque_id
        dirs = {b: branch_dir(case_dir, b) for b in ("sham", "obs", "k2")}
        checks = {b: (read(d / "check.json") if d else None) for b, d in dirs.items()}
        base["branch_present"] = {b: d is not None for b, d in dirs.items()}
        base["sham_exact"] = bool(checks["sham"] and checks["sham"]["exact_vs_frozen"])
        base["obs_exact"] = bool(checks["obs"] and checks["obs"]["exact_vs_frozen"])
        if not base["sham_exact"]:
            cases.append({**base, "status": "SHAM_NOT_EXACT_OR_MISSING"})
            continue
        native_da, native_rht = read(dirs["sham"] / "ban-ghi-0.json"), read(dirs["sham"] / "ban-ghi-1.json")
        root = label["root"]
        call_edges = [tuple(e) for e in native_rht["extra"]["call_edges"]]
        callers = {a for a, b in call_edges if b == root}
        callees = {b for a, b in call_edges if a == root}
        item = {**base, "status": "OK", "callers_of_root": sorted(callers), "callees_of_root": sorted(callees),
                "root_has_call_edge": bool(callers or callees)}
        native_nodes = native_rht["diagnostics"]["nodes"]
        item["has_huge_node"] = any(abs(v["rht_score"]) > HUGE for v in native_nodes.values())
        views = {"native_rht": view(native_rht, root, callers, callees), "native_da": view(native_da, root, callers, callees)}
        if views["native_da"]["root_ranked"]:
            item["self_check_da_rank_equals_t028"] = (label["t028"]["status"] == "OK" and
                [views["native_da"]["root_rank_min"], views["native_da"]["root_rank_max"]] == [label["t028"]["rank_min"], label["t028"]["rank_max"]])
        # ---------- K-2 ----------
        if dirs["k2"] is not None:
            k2_da, k2_rht = read(dirs["k2"] / "ban-ghi-0.json"), read(dirs["k2"] / "ban-ghi-1.json")
            info = checks["k2"]["info"]
            k2_nodes = k2_rht["diagnostics"]["nodes"]
            shared = sorted(set(native_nodes) & set(k2_nodes))
            regressed = [n for n in shared if native_nodes[n]["regression_route"] == "linear_regression"]
            changed = [n for n in shared if float(native_nodes[n]["rht_score"]).hex() != float(k2_nodes[n]["rht_score"]).hex()]
            item["k2"] = {
                "statuses": checks["k2"]["branch_statuses"], "nodes": info.get("nodes"), "edges_removed": info.get("edges_removed"),
                "k2_routes": dict(Counter(v["regression_route"] for v in k2_nodes.values())),
                "k2_da_entity_order_equals_k2_rht": [r["entity"] for r in k2_da["entity_ranking"]] == [r["entity"] for r in k2_rht["entity_ranking"]],
                "node_sets_equal": set(native_nodes) == set(k2_nodes),
                "node_counts": {"n": len(shared), "native_route_linear_regression": len(regressed),
                                "score_changed_without_edges": len(changed),
                                "changed_but_no_regression_natively": len(set(changed) - set(regressed)),
                                "regression_natively_but_unchanged": len(set(regressed) - set(changed)),
                                "regression_lowers_score": sum(native_nodes[n]["rht_score"] < k2_nodes[n]["rht_score"] for n in regressed),
                                "regression_raises_score": sum(native_nodes[n]["rht_score"] > k2_nodes[n]["rht_score"] for n in regressed),
                                "huge_native": sum(abs(native_nodes[n]["rht_score"]) > HUGE for n in shared),
                                "huge_k2": sum(abs(k2_nodes[n]["rht_score"]) > HUGE for n in shared)}}
            views["k2_rht"] = view(k2_rht, root, callers, callees)
            if views["native_rht"]["root_ranked"] and views["k2_rht"]["root_ranked"]:
                # hạng nhỏ hơn là tốt hơn; so native (có hồi quy theo cha) với không cạnh
                item["k2"]["removing_edges_effect_on_root"] = effect(views["native_rht"]["root_rank_min"], views["k2_rht"]["root_rank_min"])
                item["k2"]["pairs_above_root_native_rht"] = pair_table(views["native_rht"], k2_rht, root, callers, callees)
                node = views["native_rht"]["root_best_item"]
                item["k2"]["root_best_node_native"] = {"node": node, "route": native_nodes[node]["regression_route"],
                                                       "parents": native_nodes[node]["parents"], "rht_native": native_nodes[node]["rht_score"],
                                                       "rht_without_edges": k2_nodes.get(node, {}).get("rht_score")}
                root_nodes = sorted(n for n in shared if n.startswith(root + "_"))
                item["k2"]["root_nodes"] = [{"node": n, "route": native_nodes[n]["regression_route"], "n_parents": len(native_nodes[n]["parents"]),
                                             "rht_native": native_nodes[n]["rht_score"], "rht_without_edges": k2_nodes[n]["rht_score"]} for n in root_nodes]
        item["views"] = views
        if views["native_rht"]["root_ranked"] and views["native_da"]["root_ranked"]:
            item["da_effect_on_root"] = effect(views["native_rht"]["root_rank_min"], views["native_da"]["root_rank_min"])
        # ---------- nhánh quan sát ----------
        if base["obs_exact"] and (dirs["obs"] / "score-graph.json.gz").is_file():
            with gzip.open(dirs["obs"] / "score-graph.json.gz", "rt", encoding="utf-8") as stream:
                snap = json.load(stream)
            nodes, da, edges = snap["nodes"], snap["da"], [tuple(e) for e in snap["graph"]["edges"]]
            service_of = {n: n.rsplit("_", 1)[0] for n in nodes}
            for n in set(a for e in edges for a in e) - set(service_of):
                service_of[n] = n.rsplit("_", 1)[0]
            call_set = set(call_edges)
            direction = Counter()
            for a, b in edges:
                sa, sb = service_of[a], service_of[b]
                if sa == sb:
                    direction["cùng dịch vụ"] += 1
                elif (sb, sa) in call_set and (sa, sb) not in call_set:
                    direction["từ dịch vụ được gọi sang dịch vụ gọi"] += 1
                elif (sa, sb) in call_set and (sb, sa) not in call_set:
                    direction["từ dịch vụ gọi sang dịch vụ được gọi"] += 1
                elif (sa, sb) in call_set and (sb, sa) in call_set:
                    direction["hai dịch vụ gọi lẫn nhau"] += 1
                else:
                    direction["không có lời gọi trực tiếp"] += 1
            huge_nodes = []
            for n, v in nodes.items():
                if abs(v["rht_score"]) > HUGE:
                    huge_nodes.append({"node": n, "rht_score": v["rht_score"], "route": v["regression_route"], "n_parents": len(v["parents"]),
                                       "parents": v["parents"], "train_y_n_unique": v["train_y"]["n_unique"], "train_y_std": v["train_y"]["std"],
                                       "train_y_min": v["train_y"]["min"], "train_y_max": v["train_y"]["max"],
                                       "test_y_min": v["test_y"]["min"], "test_y_max": v["test_y"]["max"],
                                       "residual_scale": v["residual_scale"], "max_abs_test_residual": v["max_abs_test_residual"],
                                       "rht_without_edges": (item.get("k2") and read(dirs["k2"] / "ban-ghi-1.json")["diagnostics"]["nodes"].get(n, {}).get("rht_score"))})
            da_huge = []
            for n, v in da.items():
                if abs(v["key"][0]) > HUGE:
                    own, child = nodes[n]["rht_score"], v.get("child_score")
                    kind = "tự có" if abs(own) > HUGE else "nhận qua child_score" if child is not None and abs(child) > HUGE else "không rõ nguồn"
                    da_huge.append({"node": n, "service": service_of[n], "own_rht": own, "child_score": child, "source": kind})
            score_check = all(float(nodes[n]["rht_score"]).hex() == float(native_nodes[n]["rht_score"]).hex() for n in native_nodes)
            item["obs"] = {"score_graph_meta": {k: snap["meta"][k] for k in ("train_window", "test_window", "da_threshold", "detect_time", "current")},
                           "dag": snap["graph"]["dag"], "metric_nodes": len(snap["graph"]["nodes"]), "metric_edges": len(edges),
                           "edge_direction_vs_calls": dict(direction), "snapshot_rht_equals_record": score_check,
                           "huge_nodes": huge_nodes, "da_huge_nodes": da_huge,
                           "da_huge_by_source": dict(Counter(x["source"] for x in da_huge)),
                           "services_with_da_huge": sorted({x["service"] for x in da_huge}),
                           "root_has_da_huge_node": any(x["service"] == root for x in da_huge),
                           "root_da_huge_source": sorted({x["source"] for x in da_huge if x["service"] == root}),
                           "callers_of_root_with_da_huge": sorted({x["service"] for x in da_huge if x["service"] in callers}),
                           "route_counts": dict(Counter(v["regression_route"] for v in nodes.values()))}
        cases.append(item)
    ok = [c for c in cases if c["status"] == "OK"]
    k2_ok = [c for c in ok if "k2" in c and "removing_edges_effect_on_root" in c["k2"]]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        pairs = Counter()
        for c in rows:
            for pair in c["k2"]["pairs_above_root_native_rht"].values():
                pairs[pair["relation"] + ("|còn trên root" if pair["still_above"] else "|không còn trên root")] += 1
        return {"n": len(rows),
                "removing_edges_effect_on_root": {k: count(lambda c, k=k: c["k2"]["removing_edges_effect_on_root"] == k)
                                                  for k in ("tăng hạng", "không đổi", "giảm hạng")},
                "hit1": {v: count(lambda c, v=v: c["views"][v]["root_rank_max"] == 1) for v in ("native_rht", "k2_rht", "native_da")},
                "hit5": {v: count(lambda c, v=v: c["views"][v]["root_rank_max"] <= 5) for v in ("native_rht", "k2_rht", "native_da")},
                "pairs_above_root_native_rht_under_k2": dict(sorted(pairs.items())),
                "root_best_node_route": dict(Counter(c["k2"]["root_best_node_native"]["route"] for c in rows)),
                "root_best_node_score_changed": count(lambda c: c["k2"]["root_best_node_native"]["rht_native"] != c["k2"]["root_best_node_native"]["rht_without_edges"]),
                "node_counts_total": {k: sum(c["k2"]["node_counts"][k] for c in rows) for k in (rows[0]["k2"]["node_counts"] if rows else {})}}

    obs_ok = [c for c in ok if "obs" in c]
    huge_rows = [h for c in obs_ok for h in c["obs"]["huge_nodes"]]
    direction_total = Counter()
    for c in obs_ok:
        direction_total.update(c["obs"]["edge_direction_vs_calls"])
    summary = {
        "n_cases": len(cases), "sham_exact": sum(c["sham_exact"] for c in cases), "obs_exact": sum(c["obs_exact"] for c in cases),
        "k2_present": sum(c["branch_present"]["k2"] for c in cases), "n_k2_interpretable": len(k2_ok),
        "self_check_da_rank_equals_t028": sum(bool(c.get("self_check_da_rank_equals_t028")) for c in cases),
        "k2_all": tally(k2_ok),
        "k2_cases_with_huge_node": tally([c for c in k2_ok if c["has_huge_node"]]),
        "k2_cases_without_huge_node": tally([c for c in k2_ok if not c["has_huge_node"]]),
        "k2_da_entity_order_equals_k2_rht": sum(c["k2"]["k2_da_entity_order_equals_k2_rht"] for c in k2_ok),
        "k2_node_sets_equal": sum(c["k2"]["node_sets_equal"] for c in k2_ok),
        "da_effect_on_root": dict(Counter(c.get("da_effect_on_root") for c in ok)),
        "obs": {"n": len(obs_ok), "snapshot_rht_equals_record": sum(c["obs"]["snapshot_rht_equals_record"] for c in obs_ok),
                "cases_with_huge_node": sum(bool(c["obs"]["huge_nodes"]) for c in obs_ok),
                "huge_nodes_total": len(huge_rows), "huge_node_names": dict(Counter(h["node"] for h in huge_rows)),
                "huge_node_train_y_n_unique": dict(Counter(str(h["train_y_n_unique"]) for h in huge_rows)),
                "huge_node_train_y_std": quantiles([h["train_y_std"] for h in huge_rows]),
                "huge_node_residual_scale": quantiles([h["residual_scale"] for h in huge_rows]),
                "huge_node_max_abs_test_residual": quantiles([h["max_abs_test_residual"] for h in huge_rows]),
                "huge_node_test_shift_abs": quantiles([abs(h["test_y_max"] - h["train_y_max"]) for h in huge_rows]),
                "huge_nodes_still_huge_without_edges": sum(h["rht_without_edges"] is not None and abs(h["rht_without_edges"]) > HUGE for h in huge_rows),
                "da_huge_by_source_total": dict(sum((Counter(c["obs"]["da_huge_by_source"]) for c in obs_ok), Counter())),
                "cases_root_has_da_huge_node": sum(c["obs"]["root_has_da_huge_node"] for c in obs_ok),
                "cases_caller_of_root_has_da_huge_node": sum(bool(c["obs"]["callers_of_root_with_da_huge"]) for c in obs_ok),
                "edge_direction_vs_calls_total": dict(direction_total),
                "train_window_values": dict(Counter(str(c["obs"]["score_graph_meta"]["train_window"]) for c in obs_ok)),
                "test_window_values": dict(Counter(str(c["obs"]["score_graph_meta"]["test_window"]) for c in obs_ok))},
        "da_changed_cases_by_huge": {
            effect_name: {"n": sum(c.get("da_effect_on_root") == effect_name for c in obs_ok),
                          "root_has_da_huge_node": sum(c.get("da_effect_on_root") == effect_name and c["obs"]["root_has_da_huge_node"] for c in obs_ok),
                          "entity_above_root_under_da_is_huge": sum(c.get("da_effect_on_root") == effect_name and
                                                                    any(a["key_first_huge"] for a in c["views"]["native_da"]["above_root"]) for c in obs_ok)}
            for effect_name in ("tăng hạng", "không đổi", "giảm hạng")},
        "note": "K-2 là phép đổi chẩn đoán trên dev: bỏ mọi cạnh của đồ thị metric, giữ tập nút. Không phải phương pháp mới, không thay số P3. "
                "n_k2_interpretable là số ca sham khớp từng bit và root được xếp ở cả native_rht và k2_rht."}
    write(out, {"schema": "T032-CIRCA-laptop-K2-obs-v1",
                "design": ["results/T-032/thiet-ke-phep-doi-001.md#8", "results/T-032/thiet-ke-phep-doi-003.md#2"],
                "run": run.relative_to(BASE).as_posix(), "labels_sha256": sha(LABELS), "this_script_sha256": sha(__file__),
                "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("circa", "microrank"):
        print(__doc__)
        return 2
    run, out = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    if sys.argv[1] == "circa":
        collect_circa(run, out)
    else:
        collect_microrank(run, out)
    return 0


def collect_microrank(run, out):
    raise SystemExit("phần microrank được thêm ở bản v2 của script này")


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
