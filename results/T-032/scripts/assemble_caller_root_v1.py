"""T-032: bảng caller/root theo ca cho mọi phương pháp, ghép từ các lượt đã chạy trong phiên 9.

Chạy trên EC2, chỉ đọc các file tổng hợp. Không gọi phương pháp, không tính điểm mới.
Quan hệ gọi mức service lấy từ cặp span cha-con khác service của chính ca đó (bảng lõi TraceRCA, toàn cửa sổ);
CIRCA dùng `call_edges` trong bản ghi của nó. "Caller đứng trên root" là mô tả vị trí, không phải nhãn lan.
Các cột bằng chứng không loại trừ nhau và không được cộng thành tỷ lệ nguyên nhân.
Dùng: python assemble_caller_root_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

RUNS = Path("/home/ubuntu/rca/T-032/runs")
SOURCES = {
    "microrank": "microrank-core-aprime-c1-002/summary.json",
    "tracerca": "tracerca-core-td-001/summary.json",
    "simplerca": "simplerca-decomposition-002/summary.json",
    "baro": "baro-b1-001/summary.json",
    "circa": "circa-k1-002/k1.json",
    "torai": "torai-block-decomposition-001/summary.json",
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    data = {name: read(RUNS / relative) for name, relative in SOURCES.items()}
    callers = {}  # (dataset, opaque_id) -> danh sách caller của root theo span toàn cửa sổ
    for case in data["tracerca"]["cases"]:
        if case.get("status") == "OK":
            callers[(case["dataset"], case["opaque_id"])] = set(case["callers_of_root"])
    methods = {}

    # MicroRank
    rows = []
    for case in data["microrank"]["cases"]:
        key = (case["dataset"], case["opaque_id"])
        if case.get("status") != "OK":
            rows.append({"dataset": key[0], "opaque_id": key[1], "status": case.get("status"), "reason": case.get("reason")})
            continue
        native = case["branches"]["w_native"]
        item = {"dataset": key[0], "opaque_id": key[1], "status": "OK", "cell": case["cell"], "root_ranked": native["root_ranked"]}
        if native["root_ranked"]:
            pairs = []
            for entity in native["above_root"]:
                if entity["relation"] != "caller_of_root":
                    continue
                pairs.append({"caller": entity["entity"], "max_operation": entity["operation"],
                              "max_operation_own_A": entity["max_operation_own_A"],
                              "max_operation_context_only_A": entity["max_operation_context_only_A"],
                              "still_above_with_unit_weights": case["w_unit_pairs_above_root_native"][entity["entity"]]["still_above"],
                              "still_above_with_own_counts": case["c1_pairs_above_root_native"][entity["entity"]]["still_above"]})
            item.update(root_rank=[native["root"]["rank_min"], native["root"]["rank_max"]], n_above=len(native["above_root"]), caller_pairs=pairs)
        rows.append(item)
    methods["microrank"] = rows

    # TraceRCA
    rows = []
    for case in data["tracerca"]["cases"]:
        key = (case["dataset"], case["opaque_id"])
        if case.get("status") != "OK" or not case.get("sham_ji_bit_exact"):
            rows.append({"dataset": key[0], "opaque_id": key[1], "status": case.get("status"), "reason": case.get("reason")})
            continue
        native = case["native"]
        item = {"dataset": key[0], "opaque_id": key[1], "status": "OK", "cell": case["cell"], "root_ranked": native["root_ranked"]}
        if native["root_ranked"]:
            pairs = []
            for entity in native["above_root"]:
                if entity["relation"] != "caller_of_root":
                    continue
                pair = (case.get("pairs_above_root_native") or {}).get(entity["entity"], {})
                pairs.append({"caller": entity["entity"], "max_operation": entity["operation"], "a": entity["a"], "n": entity["n"],
                              "margin_native": pair.get("margin_native"), "margin_uncovered_duration": pair.get("margin_t_d"),
                              "still_above_with_uncovered_duration": pair.get("still_above")})
            item.update(root_rank=[native["root"]["rank_min"], native["root"]["rank_max"]], n_above=len(native["above_root"]),
                        caller_pairs=pairs, root_rank_uncovered_duration=(None if not case["t_d"]["root_ranked"] else
                                                                           [case["t_d"]["root"]["rank_min"], case["t_d"]["root"]["rank_max"]]))
        rows.append(item)
    methods["tracerca"] = rows

    # SimpleRCA và BARO: quan hệ gọi lấy từ bảng TraceRCA của cùng ca; thiếu thì ghi rõ.
    for name in ("simplerca", "baro"):
        rows = []
        for case in data[name]["cases"]:
            key = (case["dataset"], case["opaque_id"])
            if case.get("status") != "OK":
                rows.append({"dataset": key[0], "opaque_id": key[1], "status": case.get("status"), "reason": case.get("reason")})
                continue
            item = {"dataset": key[0], "opaque_id": key[1], "status": "OK", "cell": case["cell"]}
            if key not in callers:
                item.update(call_relation="N/A", reason="không có bảng span của ca này (TraceRCA nguồn ERROR hoặc chưa có)")
                rows.append(item)
                continue
            if name == "simplerca":
                if not case.get("root_ranked"):
                    item["root_ranked"] = False
                    rows.append(item)
                    continue
                above = case["above_root"]
                pairs = [{"caller": a["entity"], "difference_vs_root": a["difference_vs_root"],
                          "top_metric_columns": a["top_metric_columns"]} for a in above if a["entity"] in callers[key]]
                item.update(root_ranked=True, root_rank=[case["root_parts"]["rank_min"], case["root_parts"]["rank_max"]],
                            n_above=len(above), caller_pairs=pairs)
            else:
                native = case["native"]
                if not native.get("root_ranked"):
                    item["root_ranked"] = False
                    rows.append(item)
                    continue
                above = native["above_root"]
                pairs = [{"caller": a["entity"], "best_column": a["best_column"], "score": a["score"],
                          "margin_vs_root": a["margin_vs_root"]} for a in above if a["entity"] in callers[key]]
                item.update(root_ranked=True, root_rank=[native["root_rank_min"], native["root_rank_max"]], n_above=len(above),
                            caller_pairs=pairs, root_rank_without_constant_filter=[case["b1"]["root_rank_min"], case["b1"]["root_rank_max"]])
            rows.append(item)
        methods[name] = rows

    # CIRCA: quan hệ gọi theo call_edges của chính bản ghi.
    rows = []
    for case in data["circa"]["cases"]:
        if case.get("status") != "OK":
            rows.append({"dataset": "RE2-TT", "opaque_id": case["opaque_id"], "status": case.get("status")})
            continue
        da, rht = case["variants"]["ols+rht_da"], case["variants"]["ols+rht"]
        rows.append({"dataset": "RE2-TT", "opaque_id": case["opaque_id"], "status": "OK", "cell": case["cell"], "root_ranked": True,
                     "root_rank": [da["root"]["rank_min"], da["root"]["rank_max"]], "n_above": da["n_above"],
                     "caller_pairs": [{"caller": a["entity"], "key_first_huge": a["key_first_huge"],
                                       "also_above_without_da": a["entity"] in rht["callers_above"]} for a in da["above_root"]
                                      if a["relation"] == "caller_of_root"],
                     "root_rank_without_da": [rht["root"]["rank_min"], rht["root"]["rank_max"]],
                     "callers_above_without_da": rht["callers_above"]})
    methods["circa"] = rows

    def tally(rows, dataset):
        rows = [r for r in rows if r["dataset"] == dataset]
        ok = [r for r in rows if r.get("status") == "OK" and r.get("root_ranked") and "caller_pairs" in r]
        return {"cases": len(rows), "ok_root_ranked_with_call_relation": len(ok),
                "wrong_at_1": sum(r["root_rank"][1] > 1 for r in ok),
                "cases_with_caller_above_root": sum(bool(r["caller_pairs"]) for r in ok),
                "caller_pairs": sum(len(r["caller_pairs"]) for r in ok),
                "entity_pairs_above_root": sum(r["n_above"] for r in ok)}

    summary = {name: {dataset: tally(rows, dataset) for dataset in ("RE2-TT", "Nezha-OB")} for name, rows in methods.items()}
    micro = [p for r in methods["microrank"] for p in r.get("caller_pairs", [])]
    trace = [p for r in methods["tracerca"] for p in r.get("caller_pairs", [])]
    simple = [p for r in methods["simplerca"] for p in r.get("caller_pairs", [])]
    summary["evidence"] = {
        "microrank_caller_pairs": {"n": len(micro), "still_above_with_unit_weights": sum(p["still_above_with_unit_weights"] for p in micro),
                                   "still_above_with_own_counts": sum(p["still_above_with_own_counts"] for p in micro),
                                   "max_operation_has_own_flagged_traces": sum(p["max_operation_own_A"] > 0 for p in micro)},
        "tracerca_caller_pairs": {"n": len(trace), "still_above_with_uncovered_duration": sum(bool(p["still_above_with_uncovered_duration"]) for p in trace),
                                  "no_longer_above_with_uncovered_duration": sum(p["still_above_with_uncovered_duration"] is False for p in trace)},
        "simplerca_caller_pairs": {"n": len(simple), "metric_difference_positive": sum(p["difference_vs_root"]["metric"] > 0 for p in simple),
                                   "trace_difference_positive": sum(p["difference_vs_root"]["trace"] > 0 for p in simple)},
        "torai_units": data["torai"]["summary"]["wrong_at_1_units"],
        "note": "Mỗi dòng là một cột bằng chứng riêng, có thể chồng lấn; không cộng thành tỷ lệ nguyên nhân. "
                "Không có cột nào là bằng chứng chờ vật lý.",
    }
    result = {"schema": "T032-caller-root-phien9-v1", "sources": {name: {"path": relative, "sha256": sha(RUNS / relative)} for name, relative in SOURCES.items()},
              "summary": summary, "methods": methods}
    (out / "caller-root.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
