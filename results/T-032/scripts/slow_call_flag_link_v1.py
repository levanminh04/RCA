"""T-032 bản 008 mục 4 (việc 2): span làm thực thể đứng trên root có phải là span chờ root không. Chạy trên EC2, chỉ đọc.

Chỉ TraceRCA và MicroRank. Thao tác cao nhất của mỗi thực thể lấy từ bản ghi đóng băng (mục `ranking`); bảng theo thao tác
và theo trace lấy từ lượt chain-spanpass (tính trước khi nối nhãn). Không gọi phương pháp, không chấm Hit mới.
Dùng: python slow_call_flag_link_v1.py <thư mục lượt spanpass> <thư mục lượt mới>
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import chain_position_v1 as cp  # noqa: E402 — dùng nguyên Graph, ranks_of, read đã kiểm bằng trường hợp tự dựng

TD = BASE / "runs/tracerca-core-td-001/summary.json"
MR = BASE / "runs/microrank-core-aprime-c1-002/summary.json"
UP = ("goi_truc_tiep", "phia_tren_gian_tiep", "hai_chieu")
MARKS = (0.2, 0.5, 0.8)


def share(a, b):
    return (a / b) if b else None


def q(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def marks(values):
    values = [v for v in values if v is not None]
    return {"n": len(values), **{"ge_" + str(m): sum(v >= m for v in values) for m in MARKS}, "eq_0": sum(v == 0 for v in values)}


def main():
    spanpass, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    labels = cp.read(cp.LABELS)["main_rows"]
    td = {(c["dataset"], c["opaque_id"]): c for c in cp.read(TD)["cases"]}
    mr = {(c["dataset"], c["opaque_id"]): c for c in cp.read(MR)["cases"]}
    cases = []
    for row in labels:
        if row["method"] not in ("tracerca", "microrank_full"):
            continue
        method = "tracerca" if row["method"] == "tracerca" else "microrank"
        dataset, opaque_id, root = row["dataset"], row["opaque_id"], row["root"]
        base = {"dataset": dataset, "method": method, "opaque_id": opaque_id, "root": root, "fault": row["fault"], "cell": row["cell"]}
        ref = row["source"]["records"][0]
        if row["status"] != "OK":
            cases.append({**base, "status": row["status"]})
            continue
        record = cp.read(cp.REPO / ref["path"])
        rank = cp.ranks_of(record, method)
        if root not in rank:
            cases.append({**base, "status": "OK", "root_ranked": False})
            continue
        item_of = {}
        for r in record["ranking"]:
            item_of.setdefault(r["entity"], r["item"])
        sp = cp.read(spanpass / "cases" / (dataset + "-" + opaque_id + ".json"))
        g = cp.Graph(sp["services"], [(e["caller"], e["callee"]) for e in sp["edges"].values()])
        measurable_x = sorted({e["callee"] for e in sp["edges"].values() if "slow_share_after" in e})
        upstream_of_root = {s for s in sp["services"] if g.reach(s).get(root)}
        other_x = [x for x in measurable_x if x != root and x not in upstream_of_root]
        ops, tops = sp["operations"], sp["trace_operations"]

        def link(entity):
            o = item_of.get(entity)
            op, tr = ops.get(o), tops.get(o)
            res = {"entity": entity, "operation": o, "rank_min": rank[entity][0], "rank_max": rank[entity][1]}
            if entity != root:
                res.update(g.position(entity, root))
                res["above_root"] = rank[entity][1] < rank[root][0]
            if op:
                x = op["x"].get(root, {})
                a, n = op["a"], op["n"]
                res["span"] = {"a": a, "n": n, "a_below": x.get("a_below", 0), "a_slow": x.get("a_slow", 0), "a_flag_below": x.get("a_flag_below", 0),
                               "a_r50": x.get("a_r50", 0), "a_r80": x.get("a_r80", 0), "ratio_median": x.get("ratio_median"),
                               "nf": n - a, "nf_below": x.get("nf_below", 0), "nf_slow": x.get("nf_slow", 0),
                               "share_slow": share(x.get("a_slow", 0), a), "share_r50": share(x.get("a_r50", 0), a),
                               "share_flag_below": share(x.get("a_flag_below", 0), a), "share_slow_nonflag": share(x.get("nf_slow", 0), n - a),
                               "other_x_share_slow": sorted((share(op["x"].get(y, {}).get("a_slow", 0), a) or 0.0 for y in other_x), reverse=True)[:3]}
            if tr:
                x = tr["x"].get(root, {})
                A = tr["A"]
                res["trace"] = {"A": A, "N": tr["N"], "own_A": tr["own_A"], "A_has_root": x.get("A_has", 0), "A_root_own_flag": x.get("A_own_flag", 0),
                                "A_root_wait_flag": x.get("A_wait_flag", 0), "A_linked": x.get("A_linked", 0), "N_has_root": x.get("N_has", 0),
                                "share_linked": share(x.get("A_linked", 0), A), "share_has_root": share(x.get("A_has", 0), A),
                                "share_N_has_root": share(x.get("N_has", 0), tr["N"]),
                                "other_x_share_linked": sorted((share(tr["x"].get(y, {}).get("A_linked", 0), A) or 0.0 for y in other_x), reverse=True)[:3]}
            return res

        entities = [link(e) for e in rank if e != root]
        item = {**base, "status": "OK", "root_ranked": True, "root_rank": list(rank[root]), "root_link": link(root),
                "root_edge_measurable": root in measurable_x, "callers_of_root": sorted(s for s in sp["services"] if g.reach(s).get(root) == 1),
                "n_upstream_of_root": len(upstream_of_root), "entities": entities}
        # tự kiểm với lượt phiên 9
        check = {}
        if method == "tracerca":
            ref_case = td[(dataset, opaque_id)]["native"]
            mine = {e["entity"]: e for e in entities if e["above_root"]}
            check["above_set_equal"] = set(mine) == {a["entity"] for a in ref_case["above_root"]}
            check["above_operation_a_n_equal"] = all(a["entity"] in mine and mine[a["entity"]]["operation"] == a["operation"] and
                                                     mine[a["entity"]].get("span", {}).get("a") == a["a"] and mine[a["entity"]]["span"]["n"] == a["n"]
                                                     for a in ref_case["above_root"])
            check["root_operation_a_n_equal"] = (item["root_link"]["operation"] == ref_case["root"]["operation"] and
                                                 item["root_link"]["span"]["a"] == ref_case["root"]["a"] and item["root_link"]["span"]["n"] == ref_case["root"]["n"])
        else:
            ref_case = mr[(dataset, opaque_id)]["branches"]["w_native"]
            mine = {e["entity"]: e for e in entities if e["above_root"]}
            check["above_set_equal"] = set(mine) == {a["entity"] for a in ref_case["above_root"]}
            check["above_operation_coverage_equal"] = all(
                a["entity"] in mine and mine[a["entity"]]["operation"] == a["operation"] and
                mine[a["entity"]].get("trace", {}).get("own_A") == a["max_operation_own_A"] and
                mine[a["entity"]]["trace"]["A"] == a["max_operation_own_A"] + a["max_operation_context_only_A"] for a in ref_case["above_root"])
        item["self_check"] = check
        cases.append(item)

    def block(rows, method):
        ok = [c for c in rows if c.get("status") == "OK" and c.get("root_ranked")]
        key = "share_r50" if method == "tracerca" else "share_linked"
        part = "span" if method == "tracerca" else "trace"
        res = {"cases": len(rows), "status": dict(Counter(c.get("status") for c in rows)), "cases_ok_root_ranked": len(ok),
               "self_check": {k + "=" + str(v): n for (k, v), n in Counter((k, v) for c in ok for k, v in c["self_check"].items()).items()},
               "cases_root_edge_measurable": sum(c["root_edge_measurable"] for c in ok),
               "cases_root_rank1": sum(c["root_rank"][1] == 1 for c in ok)}

        def pick(case_filter, entity_filter):
            return [e for c in ok if case_filter(c) for e in c["entities"] if entity_filter(e) and part in e]

        wrong = lambda c: c["root_rank"][0] > 1 or c["root_rank"][1] > 1   # noqa: E731
        meas = lambda c: c["root_edge_measurable"]                          # noqa: E731
        above = [e for c in ok for e in c["entities"] if e["above_root"]]
        res["pairs_above"] = len(above)
        res["pairs_above_by_class"] = dict(Counter(e["class"] for e in above))
        res["pairs_above_upstream"] = sum(e["class"] in UP for e in above)
        res["pairs_above_upstream_in_measurable_cases"] = len(pick(meas, lambda e: e["above_root"] and e["class"] in UP))
        res["pairs_above_upstream_in_unmeasurable_cases"] = len(pick(lambda c: not meas(c), lambda e: e["above_root"] and e["class"] in UP))
        groups = {
            "above_upstream_measurable": pick(meas, lambda e: e["above_root"] and e["class"] in UP),
            "above_direct_caller_measurable": pick(meas, lambda e: e["above_root"] and e.get("dist_up") == 1),
            "above_not_upstream_measurable": pick(meas, lambda e: e["above_root"] and e["class"] not in UP),
            "not_above_upstream_measurable_wrong_cases": pick(lambda c: meas(c) and wrong(c), lambda e: not e["above_root"] and e["class"] in UP),
            "not_above_upstream_measurable_root_rank1_cases": pick(lambda c: meas(c) and not wrong(c), lambda e: not e["above_root"] and e["class"] in UP),
        }
        res["groups"] = {}
        for name, es in groups.items():
            g = {"n": len(es), "main_share": key, "main": marks([e[part][key] for e in es]), "main_quantiles": q([e[part][key] for e in es])}
            if method == "tracerca":
                g["share_slow"] = marks([e["span"]["share_slow"] for e in es])
                g["share_slow_quantiles"] = q([e["span"]["share_slow"] for e in es])
                g["share_slow_nonflag_quantiles"] = q([e["span"]["share_slow_nonflag"] for e in es])
                g["share_flag_below"] = marks([e["span"]["share_flag_below"] for e in es])
                g["other_x_top_share_slow_quantiles"] = q([(e["span"]["other_x_share_slow"] or [0.0])[0] for e in es])
                g["zero_flag_operations"] = sum(e["span"]["a"] == 0 for e in es)
            else:
                g["share_has_root"] = marks([e["trace"]["share_has_root"] for e in es])
                g["share_has_root_quantiles"] = q([e["trace"]["share_has_root"] for e in es])
                g["share_N_has_root_quantiles"] = q([e["trace"]["share_N_has_root"] for e in es])
                g["other_x_top_share_linked_quantiles"] = q([(e["trace"]["other_x_share_linked"] or [0.0])[0] for e in es])
                g["span_share_slow"] = marks([e["span"]["share_slow"] for e in es if "span" in e])
            res["groups"][name] = g
        # theo ca: ca sai có ít nhất một cặp phía trên được xếp "chủ yếu là chờ root"
        wrong_cases = [c for c in ok if wrong(c)]
        res["wrong_cases"] = len(wrong_cases)
        res["wrong_cases_measurable"] = sum(meas(c) for c in wrong_cases)
        res["wrong_cases_with_above_upstream"] = sum(any(e["above_root"] and e["class"] in UP for e in c["entities"]) for c in wrong_cases)
        res["wrong_cases_with_above_upstream_mostly_waiting"] = sum(
            meas(c) and any(e["above_root"] and e["class"] in UP and part in e and (e[part][key] or 0) >= 0.5 for e in c["entities"]) for c in wrong_cases)
        res["wrong_cases_all_above_mostly_waiting"] = sum(
            meas(c) and all(e["class"] in UP and part in e and (e[part][key] or 0) >= 0.5 for e in c["entities"] if e["above_root"]) for c in wrong_cases)
        res["wrong_cases_by_fault"] = {}
        for f in sorted({c["fault"] for c in wrong_cases}):
            cs = [c for c in wrong_cases if c["fault"] == f]
            res["wrong_cases_by_fault"][f] = {
                "wrong_cases": len(cs), "measurable": sum(meas(c) for c in cs),
                "with_above_upstream_mostly_waiting": sum(meas(c) and any(e["above_root"] and e["class"] in UP and part in e and (e[part][key] or 0) >= 0.5
                                                                         for e in c["entities"]) for c in cs),
                "pairs_above": sum(e["above_root"] for c in cs for e in c["entities"]),
                "pairs_above_upstream": sum(e["above_root"] and e["class"] in UP for c in cs for e in c["entities"])}
        return res

    summary = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        for method in ("tracerca", "microrank"):
            summary.setdefault(dataset, {})[method] = block([c for c in cases if c["dataset"] == dataset and c["method"] == method], method)
    result = {"schema": "T032-slow-call-flag-link-v1", "design": "results/T-032/thiet-ke-vi-tri-chuoi-goi-008.md mục 4",
              "sources": {"spanpass_summary_sha256": cp.sha(spanpass / "summary.json"), "labels_sha256": cp.sha(cp.LABELS), "td_sha256": cp.sha(TD), "mr_sha256": cp.sha(MR)},
              "marks": list(MARKS), "upstream_classes": list(UP),
              "note": "Mô tả trên dev. Không là nhãn lan; các cột có thể chồng lấn, không cộng thành tỷ lệ nguyên nhân.",
              "summary": summary, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "cases.json").write_text(json.dumps(cases, ensure_ascii=False) + "\n", encoding="utf-8")
    for dataset, b in summary.items():
        for method, r in b.items():
            print(dataset, method, "ok", r["cases_ok_root_ranked"], "selfcheck", r["self_check"], "pairs", r["pairs_above"], r["pairs_above_by_class"], flush=True)
            for name, g in r["groups"].items():
                print("   ", name, g["n"], g["main_share"], g["main"], g["main_quantiles"], flush=True)
            print("    wrong", r["wrong_cases"], "meas", r["wrong_cases_measurable"], "with_up", r["wrong_cases_with_above_upstream"],
                  "mostly_wait", r["wrong_cases_with_above_upstream_mostly_waiting"], "all_above_wait", r["wrong_cases_all_above_mostly_waiting"], flush=True)


if __name__ == "__main__":
    main()
