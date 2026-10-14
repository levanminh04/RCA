"""T-032: các bảng mô tả dẫn xuất của phiên 9, để mỗi số trong ket-qua-phien-9.md có con trỏ file.

Chạy trên EC2, chỉ đọc các lượt đã có. Không gọi phương pháp, không đổi phép tính, không đặt ngưỡng mới.
Nội dung:
  microrank: quan hệ và thành phần own/context của các cặp (thực thể đứng trên root, root); tỷ lệ theo ca;
  tracerca : quan hệ của các cặp và kết cục dưới T-D;
  circa    : 15 ca hạng root đổi khi thêm DA;
  baro     : loại cột thắng; median, IQR, tử số và vị trí đỉnh của cột thắng ở root và ở thực thể đứng trên root;
  simplerca: phiếu theo loại cột, số cột metric, quan hệ gọi của 64 cặp.
Dùng: python derived_tables_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

RUNS = Path("/home/ubuntu/rca/T-032/runs")
SRC = {
    "microrank": "microrank-core-aprime-c1-002/summary.json",
    "tracerca": "tracerca-core-td-001/summary.json",
    "circa": "circa-k1-002/k1.json",
    "baro_b1": "baro-b1-001/summary.json",
    "baro_chains": "execution-research-baro-006/baro-saved-chains.json",
    "simplerca": "simplerca-decomposition-002/summary.json",
}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def quantiles(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    pick = lambda q: values[min(len(values) - 1, int(q * len(values)))]
    return {"n": len(values), "min": values[0], "q25": pick(0.25), "median": statistics.median(values), "q75": pick(0.75), "max": values[-1]}


def kind(column):
    return column.rsplit("_", 1)[-1]


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    result = {"schema": "T032-derived-tables-v1", "sources": {k: {"path": v, "sha256": sha(RUNS / v)} for k, v in SRC.items()},
              "note": "Bảng mô tả. Không có ngưỡng mới. Các cột có thể chồng lấn, không cộng thành tỷ lệ nguyên nhân."}

    # ---------- MicroRank ----------
    micro = [c for c in read(RUNS / SRC["microrank"])["cases"] if c.get("status") == "OK"]
    table = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        rows = [c for c in micro if c["dataset"] == dataset]
        relation, composition = Counter(), Counter()
        still = {"w_unit": Counter(), "c1": Counter()}
        for c in rows:
            for item in c["branches"]["w_native"].get("above_root", []):
                relation[item["relation"]] += 1
                own, context = item["max_operation_own_A"], item["max_operation_context_only_A"]
                composition["own_zero" if own == 0 else "context_gt_own" if context > own else "own_ge_context"] += 1
            for branch in still:
                for pair in c.get(branch + "_pairs_above_root_native", {}).values():
                    still[branch][pair["relation"] + ("|still_above" if pair["still_above"] else "|no_longer_above")] += 1
        table[dataset] = {"cases": len(rows), "pairs_by_relation": dict(relation), "max_operation_composition": dict(composition),
                          "pairs_under_w_unit": dict(still["w_unit"]), "pairs_under_c1": dict(still["c1"]),
                          "share_of_traces_in_A": quantiles([c["counts"]["share_A"] for c in rows]),
                          "share_of_A_traces_without_root_service": quantiles([c["counts"]["A_traces_without_root_service"] / c["counts"]["A"] for c in rows]),
                          "share_of_A_traces_where_root_service_has_flagged_span": quantiles([c["counts"]["A_traces_root_service_own_abnormal"] / c["counts"]["A"] for c in rows]),
                          "root_rank_min": {b: sorted(c["branches"][b]["root"]["rank_min"] for c in rows if c["branches"][b]["root_ranked"])
                                            for b in ("w_native", "w_unit", "c1")}}
    result["microrank"] = table

    # ---------- TraceRCA ----------
    trace_cases = read(RUNS / SRC["tracerca"])["cases"]
    trace = [c for c in trace_cases if c.get("status") == "OK" and "td_effect_on_root" in c]
    relation_of = {}  # (dataset, opaque_id) -> (callers, callees) theo span toàn cửa sổ
    for c in trace_cases:
        if c.get("status") == "OK":
            relation_of[(c["dataset"], c["opaque_id"])] = (set(c["callers_of_root"]), set(c["callees_of_root"]))
    table = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        rows = [c for c in trace if c["dataset"] == dataset]
        outcome = Counter()
        for c in rows:
            for pair in c["pairs_above_root_native"].values():
                outcome[pair["relation"] + ("|still_above" if pair["still_above"] else "|no_longer_above")] += 1
        table[dataset] = {"cases": len(rows), "pairs_under_t_d": dict(outcome),
                          "covered_share_of_total_duration": quantiles([c["counts"]["covered_share_of_total_duration"] for c in rows]),
                          "flagged_spans_ratio_uncovered_over_native": quantiles([c["counts"]["H_u"] / c["counts"]["H_native"] for c in rows if c["counts"]["H_native"]]),
                          "root_rank_min": {"native": sorted(c["native"]["root"]["rank_min"] for c in rows),
                                            "t_d": sorted(c["t_d"]["root"]["rank_min"] for c in rows)}}
    result["tracerca"] = table

    # ---------- CIRCA K-1 ----------
    rows = []
    for c in read(RUNS / SRC["circa"])["cases"]:
        if c.get("status") != "OK" or c["da_effect_on_root"] == "không đổi":
            continue
        rht, da = c["variants"]["ols+rht"], c["variants"]["ols+rht_da"]
        rows.append({"opaque_id": c["opaque_id"], "cell": c["cell"], "da_effect_on_root": c["da_effect_on_root"],
                     "root_rank_min_rht": c["root_rank_min_rht"], "root_rank_min_da": c["root_rank_min_da"],
                     "root_key_da_first_huge": da["root"]["key_first_huge"], "root_key_da": da["root"]["key"], "root_key_rht": rht["root"]["key"],
                     "above_rht": [{"entity": a["entity"], "relation": a["relation"], "huge": a["key_first_huge"]} for a in rht["above_root"]],
                     "above_da": [{"entity": a["entity"], "relation": a["relation"], "huge": a["key_first_huge"]} for a in da["above_root"]],
                     "huge_involved": da["root"]["key_first_huge"] or any(a["key_first_huge"] for a in da["above_root"])
                                      or any(a["key_first_huge"] for a in rht["above_root"])})
    result["circa_k1_changed_cases"] = {
        "n": len(rows), "rows": rows,
        "improved_with_root_key_huge": sum(r["da_effect_on_root"] == "tăng hạng" and r["root_key_da_first_huge"] for r in rows),
        "worsened_with_huge_caller_above_under_da": sum(r["da_effect_on_root"] == "giảm hạng" and
                                                         any(a["huge"] and a["relation"] == "caller_of_root" for a in r["above_da"]) for r in rows),
        "changed_cases_with_huge_value_involved": sum(r["huge_involved"] for r in rows)}

    # ---------- BARO ----------
    labels = {(c["dataset"], c["opaque_id"]): c for c in read(RUNS / SRC["baro_b1"])["cases"] if c["status"] == "OK"}
    chains = read(RUNS / SRC["baro_chains"])["cases"]
    pair_rows, per_case = [], []
    for case in chains:
        key = (case["dataset"], case["opaque_id"])
        if key not in labels or not labels[key]["native"].get("root_ranked"):
            continue
        by_column = {m["column"]: m for m in case["metric_chains"]}
        native = labels[key]["native"]

        def describe(column):
            m = by_column.get(column)
            if m is None:
                return None
            median, iqr = m["median_N"], m["raw_IQR_N"]
            numerator = m["numerator_at_max"][0] if m["numerator_at_max"] else None
            return {"column": column, "kind": kind(column), "z": m["signed_max_robust_z"], "median_N": median, "IQR_N": iqr,
                    "numerator_at_max": numerator, "first_max_position_in_A": m["max_positions_A"][0] if m["max_positions_A"] else None,
                    "IQR_over_abs_median": None if not median else iqr / abs(median),
                    "numerator_over_abs_median": None if not median or numerator is None else abs(numerator) / abs(median),
                    "scale_fallback_observed": m["scale_fallback_observed"]}

        root = describe(native["root_best_column"])
        wrong = native["root_rank_max"] > 1
        per_case.append({"dataset": key[0], "opaque_id": key[1], "cell": labels[key]["cell"], "wrong_at_1": wrong, "root": root,
                         "n_above": len(native["above_root"])})
        callers, callees = relation_of.get(key, (None, None))
        for above in native["above_root"]:
            entity = describe(above["best_column"])
            pair_rows.append({"dataset": key[0], "opaque_id": key[1], "entity": above["entity"],
                              "relation": "N/A" if callers is None else "caller_of_root" if above["entity"] in callers
                                          else "callee_of_root" if above["entity"] in callees else "other",
                              "entity_best": entity, "root_best": root,
                              "entity_IQR_ratio_smaller_than_root": None if not entity or not root or entity["IQR_over_abs_median"] is None
                                  or root["IQR_over_abs_median"] is None else entity["IQR_over_abs_median"] < root["IQR_over_abs_median"],
                              "entity_relative_numerator_larger_than_root": None if not entity or not root or entity["numerator_over_abs_median"] is None
                                  or root["numerator_over_abs_median"] is None else entity["numerator_over_abs_median"] > root["numerator_over_abs_median"],
                              "entity_peak_before_root_peak": None if not entity or not root or entity["first_max_position_in_A"] is None
                                  or root["first_max_position_in_A"] is None else entity["first_max_position_in_A"] < root["first_max_position_in_A"]})
    table = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        pairs = [p for p in pair_rows if p["dataset"] == dataset]
        cases = [c for c in per_case if c["dataset"] == dataset]

        def tri(field):
            return {"true": sum(p[field] is True for p in pairs), "false": sum(p[field] is False for p in pairs),
                    "n/a": sum(p[field] is None for p in pairs)}

        table[dataset] = {
            "cases": len(cases), "wrong_at_1": sum(c["wrong_at_1"] for c in cases), "pairs_above_root": len(pairs),
            "pairs_by_relation": dict(Counter(p["relation"] for p in pairs)),
            "entity_best_column_kind": dict(Counter(p["entity_best"]["kind"] for p in pairs if p["entity_best"])),
            "root_best_column_kind": {"wrong_at_1": dict(Counter(c["root"]["kind"] for c in cases if c["wrong_at_1"] and c["root"])),
                                      "hit_at_1": dict(Counter(c["root"]["kind"] for c in cases if not c["wrong_at_1"] and c["root"]))},
            "entity_IQR_ratio_smaller_than_root": tri("entity_IQR_ratio_smaller_than_root"),
            "entity_relative_numerator_larger_than_root": tri("entity_relative_numerator_larger_than_root"),
            "entity_peak_before_root_peak": tri("entity_peak_before_root_peak"),
            "IQR_over_abs_median": {"entities_above_root": quantiles([p["entity_best"]["IQR_over_abs_median"] for p in pairs if p["entity_best"]]),
                                    "root_when_wrong": quantiles([c["root"]["IQR_over_abs_median"] for c in cases if c["wrong_at_1"] and c["root"]]),
                                    "root_when_hit": quantiles([c["root"]["IQR_over_abs_median"] for c in cases if not c["wrong_at_1"] and c["root"]])},
            "numerator_over_abs_median": {"entities_above_root": quantiles([p["entity_best"]["numerator_over_abs_median"] for p in pairs if p["entity_best"]]),
                                          "root_when_wrong": quantiles([c["root"]["numerator_over_abs_median"] for c in cases if c["wrong_at_1"] and c["root"]]),
                                          "root_when_hit": quantiles([c["root"]["numerator_over_abs_median"] for c in cases if not c["wrong_at_1"] and c["root"]])}}
    result["baro"] = {"summary": table, "pairs": pair_rows, "cases": per_case}

    # ---------- SimpleRCA ----------
    simple = [c for c in read(RUNS / SRC["simplerca"])["cases"] if c.get("status") == "OK" and c.get("root_ranked")]
    pair_rows = []
    for c in simple:
        if c["root_parts"]["rank_max"] == 1:
            continue
        callers, callees = relation_of.get((c["dataset"], c["opaque_id"]), (None, None))
        for above in c["above_root"]:
            top = above["top_metric_columns"][0] if above["top_metric_columns"] else None
            pair_rows.append({"dataset": c["dataset"], "opaque_id": c["opaque_id"], "entity": above["entity"],
                              "relation": "N/A" if callers is None else "caller_of_root" if above["entity"] in callers
                                          else "callee_of_root" if above["entity"] in callees else "other",
                              "difference_vs_root": above["difference_vs_root"],
                              "entity_metric_columns_with_votes": above["metric_columns_with_votes"],
                              "root_metric_columns_with_votes": c["root_parts"]["metric_columns_with_votes"],
                              "entity_usable_metric_columns": above["metric_columns_usable"],
                              "root_usable_metric_columns": c["root_parts"]["metric_columns_usable"],
                              "entity_top_column_kind": None if top is None else kind(top["column"]),
                              "entity_top_column_votes": None if top is None else top["vote"],
                              "entity_top_single_column_exceeds_root_total_score": top is not None and top["vote"] > c["root_parts"]["score"],
                              "root_score": c["root_parts"]["score"], "root_metric": c["root_parts"]["metric"]})
    table = {}
    for dataset in ("RE2-TT", "Nezha-OB"):
        pairs = [p for p in pair_rows if p["dataset"] == dataset]
        table[dataset] = {"pairs": len(pairs), "pairs_by_relation": dict(Counter(p["relation"] for p in pairs)),
                          "entity_top_column_kind": dict(Counter(p["entity_top_column_kind"] for p in pairs)),
                          "entity_top_single_column_exceeds_root_total_score": sum(p["entity_top_single_column_exceeds_root_total_score"] for p in pairs),
                          "entity_has_more_usable_metric_columns_than_root": sum(p["entity_usable_metric_columns"] > p["root_usable_metric_columns"] for p in pairs),
                          "entity_has_more_columns_with_votes_than_root": sum(p["entity_metric_columns_with_votes"] > p["root_metric_columns_with_votes"] for p in pairs),
                          "entity_top_column_votes": quantiles([p["entity_top_column_votes"] for p in pairs]),
                          "root_metric_votes": quantiles([p["root_metric"] for p in pairs])}
    result["simplerca"] = {"summary": table, "pairs": pair_rows}

    (out / "derived.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    slim = {"microrank": result["microrank"], "tracerca": result["tracerca"],
            "circa_k1_changed_cases": {k: v for k, v in result["circa_k1_changed_cases"].items() if k != "rows"},
            "baro": result["baro"]["summary"], "simplerca": result["simplerca"]["summary"]}
    print(json.dumps(slim, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
