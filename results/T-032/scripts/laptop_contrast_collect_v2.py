"""T-032 phiên 10: phần bổ sung cho laptop_contrast_collect_v1.py (giữ nguyên v1 và kết quả của nó).

  python laptop_contrast_collect_v2.py circa-regression <thư mục lượt CIRCA> <file kết quả mới>
  python laptop_contrast_collect_v2.py microrank <thư mục lượt M-D> <file kết quả mới>

circa-regression: phân rã đại số điểm RHT của từng nút có hồi quy, từ trung gian của nhánh quan sát (đã khớp từng bit):
  điểm native  = max |phần dư test − mean phần dư train| / scale phần dư train
  điểm không cạnh = max |y test − mean y train| / std y train          (đường no_effective_parents)
  nên tỷ số điểm = f_num / f_den, với f_num = tỷ số hai tử, f_den = scale phần dư / std y train.
  Đây là phân rã, không phải can thiệp. Trung gian chỉ lưu min/max của y test và max |phần dư test|, nên tử số dựng lại
  là xấp xỉ; mỗi nút được kiểm lại với điểm thật của hai nhánh và nút lệch quá 1e-6 tương đối bị loại khỏi bảng, có đếm.
microrank: M-D (thiet-ke-phep-doi-001.md mục 4, bản 003 mục 3). Nhãn root nối ở đây.
"""
from __future__ import annotations

import gzip
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import laptop_contrast_collect_v1 as v1  # noqa: E402

BASE = v1.BASE
MICRO_CORE = BASE / "runs/microrank-core-aprime-c1-002/summary.json"


def med(values):
    values = [v for v in values if v is not None]
    return statistics.median(values) if values else None


def circa_regression(run, out):
    labels = v1.labels_for("circa_ols_da", "RE2-TT")
    cases, pooled = [], []
    for (dataset, opaque_id), label in sorted(labels.items()):
        case_dir = run / "cases" / dataset / opaque_id
        obs, k2, sham = (v1.branch_dir(case_dir, b) for b in ("obs", "k2", "sham"))
        if not (obs and k2 and sham) or not v1.read(obs / "check.json")["exact_vs_frozen"]:
            cases.append({"opaque_id": opaque_id, "status": "N/A"})
            continue
        with gzip.open(obs / "score-graph.json.gz", "rt", encoding="utf-8") as stream:
            snap = json.load(stream)
        k2_nodes = v1.read(k2 / "ban-ghi-1.json")["diagnostics"]["nodes"]
        rows, excluded = [], Counter()
        for name, node in snap["nodes"].items():
            if node["regression_route"] != "linear_regression":
                continue
            native, without = node["rht_score"], k2_nodes[name]["rht_score"]
            if abs(native) > v1.HUGE:
                excluded["giá trị vượt 1e10"] += 1
                continue
            std_y, mean_y = node["train_y"]["std"], node["train_y"]["mean"]
            num_k2 = max(abs(node["test_y"]["max"] - mean_y), abs(node["test_y"]["min"] - mean_y))
            num_native = node["max_abs_test_residual"]
            scale = node["residual_scale"]
            if std_y == 0 or scale == 0 or num_k2 == 0 or without == 0 or native == 0:
                excluded["mẫu số hoặc tử số bằng 0"] += 1
                continue
            rebuilt_k2, rebuilt_native = num_k2 / std_y, num_native / scale
            if abs(rebuilt_k2 - without) > 1e-6 * abs(without) or abs(rebuilt_native - native) > 1e-6 * abs(native):
                excluded["dựng lại lệch điểm thật quá 1e-6 tương đối"] += 1
                continue
            rows.append({"node": name, "n_parents": len(node["parents"]), "native": native, "without_edges": without,
                         "f_num": num_native / num_k2, "f_den": scale / std_y, "raised": native > without})
        root = label["root"]
        root_rows = [r for r in rows if r["node"].startswith(root + "_")]
        cases.append({"opaque_id": opaque_id, "status": "OK", "root": root, "cell": label["cell"], "n_nodes_decomposed": len(rows),
                      "excluded": dict(excluded), "raised": sum(r["raised"] for r in rows), "lowered": sum(not r["raised"] for r in rows),
                      "median_f_num": med([r["f_num"] for r in rows]), "median_f_den": med([r["f_den"] for r in rows]),
                      "root_nodes": root_rows})
        pooled.extend({**r, "opaque_id": opaque_id, "is_root_node": r["node"].startswith(root + "_")} for r in rows)

    def block(rows):
        return {"n": len(rows), "raised": sum(r["raised"] for r in rows), "lowered": sum(not r["raised"] for r in rows),
                "median_f_num": med([r["f_num"] for r in rows]), "median_f_den": med([r["f_den"] for r in rows]),
                "f_num_ge_1": sum(r["f_num"] >= 1 for r in rows), "f_den_lt_half": sum(r["f_den"] < 0.5 for r in rows),
                "median_ratio_native_over_without": med([r["native"] / r["without_edges"] for r in rows])}

    summary = {"n_cases": sum(c["status"] == "OK" for c in cases), "all_nodes": block(pooled),
               "raised_nodes": block([r for r in pooled if r["raised"]]), "lowered_nodes": block([r for r in pooled if not r["raised"]]),
               "root_nodes": block([r for r in pooled if r["is_root_node"]]),
               "non_root_nodes": block([r for r in pooled if not r["is_root_node"]]),
               "excluded_total": dict(sum((Counter(c.get("excluded", {})) for c in cases), Counter())),
               "by_n_parents": {str(k): block([r for r in pooled if min(r["n_parents"], 8) == k]) for k in range(1, 9)},
               "note": "f_num = max|phần dư test| / max|y test − mean y train|; f_den = scale phần dư train / std y train. "
                       "Điểm tăng khi f_num > f_den. Cửa sổ train 111 điểm, test 10 điểm cuối (hồ sơ T-014)."}
    v1.write(out, {"schema": "T032-CIRCA-regression-decomposition-v1", "run": run.relative_to(BASE).as_posix(),
                   "this_script_sha256": v1.sha(__file__), "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def collect_microrank(run, out):
    labels = v1.labels_for("microrank_full")
    core = {(c["dataset"], c["opaque_id"]): c for c in v1.read(MICRO_CORE)["cases"]}
    plan = v1.read(run / "plan.json")["cases"]
    cases = []
    for entry in plan:
        key = (entry["dataset"], entry["opaque_id"])
        label = labels[key]
        base = {"dataset": key[0], "opaque_id": key[1], **label}
        case_dir = run / "cases" / key[0] / key[1]
        dirs = {b: v1.branch_dir(case_dir, b) for b in ("sham", "md")}
        checks = {b: (v1.read(d / "check.json") if d else None) for b, d in dirs.items()}
        base["sham_exact"] = bool(checks["sham"] and checks["sham"]["exact_vs_frozen"])
        base["source_status"] = checks["sham"]["frozen_statuses"][0] if checks["sham"] else None
        base["md_status"] = checks["md"]["branch_statuses"][0] if checks["md"] else None
        if not base["sham_exact"] or checks["md"] is None:
            cases.append({**base, "status": "SHAM_NOT_EXACT_OR_MISSING"})
            continue
        call = checks["md"]["info"]["calls"]
        base["md_quantity_calls"] = call
        if len(call) != 1 or "uncovered_error" in call[0]:
            cases.append({**base, "status": "MD_QUANTITY_NOT_APPLIED"})
            continue
        base["covered_share_of_total_duration"] = call[0]["total_covered_us"] / max(1, call[0]["total_duration_us"])
        native, changed = v1.read(dirs["sham"] / "ban-ghi-0.json"), v1.read(dirs["md"] / "ban-ghi-0.json")
        if native["status"] != "OK" or changed["status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "native " + native["status"] + ", md " + changed["status"],
                          "md_error": changed.get("error")})
            continue
        reference = core.get(key)
        if reference is None or reference.get("status") != "OK":
            cases.append({**base, "status": "N/A", "reason": "không có quan hệ gọi trong bảng lõi MicroRank"})
            continue
        root = label["root"]
        callers, callees = set(reference["callers_of_root"]), set(reference["callees_of_root"])
        views = {"native": v1.view(native, root, callers, callees), "md": v1.view(changed, root, callers, callees)}
        item = {**base, "status": "OK", "callers_of_root": sorted(callers), "callees_of_root": sorted(callees), "views": views,
                "counts": {"native": native["diagnostics"]["counts"], "md": changed["diagnostics"]["counts"]}}
        if views["native"]["root_ranked"]:
            item["self_check_native_rank_equals_t028"] = (label["t028"]["status"] == "OK" and
                [views["native"]["root_rank_min"], views["native"]["root_rank_max"]] == [label["t028"]["rank_min"], label["t028"]["rank_max"]])
        if views["native"]["root_ranked"] and views["md"]["root_ranked"]:
            item["md_effect_on_root"] = v1.effect(views["native"]["root_rank_min"], views["md"]["root_rank_min"])
            item["pairs_above_root_native"] = v1.pair_table(views["native"], changed, root, callers, callees)
            native_callers = {a["entity"] for a in views["native"]["above_root"] if a["relation"] == "caller_of_root"}
            md_callers = {a["entity"] for a in views["md"]["above_root"] if a["relation"] == "caller_of_root"}
            item["callers_above"] = {"native": sorted(native_callers), "md": sorted(md_callers),
                                     "no_longer_above": sorted(native_callers - md_callers), "newly_above": sorted(md_callers - native_callers)}
        cases.append(item)
    ok = [c for c in cases if c["status"] == "OK" and "md_effect_on_root" in c]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        pairs = Counter()
        for c in rows:
            for pair in c["pairs_above_root_native"].values():
                pairs[pair["relation"] + ("|còn trên root" if pair["still_above"] else "|không còn trên root")] += 1
        return {"n": len(rows),
                "md_effect_on_root": {k: count(lambda c, k=k: c["md_effect_on_root"] == k) for k in ("tăng hạng", "không đổi", "giảm hạng")},
                "hit1": {v: count(lambda c, v=v: c["views"][v]["root_rank_max"] == 1) for v in ("native", "md")},
                "hit5": {v: count(lambda c, v=v: c["views"][v]["root_rank_max"] <= 5) for v in ("native", "md")},
                "native_hit_at_1_loses": count(lambda c: c["views"]["native"]["root_rank_max"] == 1 and c["views"]["md"]["root_rank_max"] > 1),
                "cases_with_caller_above_root": {v: count(lambda c, v=v: bool(c["callers_above"][v])) for v in ("native", "md")},
                "pairs_above_root_native_under_md": dict(sorted(pairs.items())),
                "pairs_newly_above_root_under_md": sum(len({a["entity"] for a in c["views"]["md"]["above_root"]} -
                                                           {a["entity"] for a in c["views"]["native"]["above_root"]}) for c in rows),
                "abnormal_spans_ratio_md_over_native": v1.quantiles([c["counts"]["md"]["abnormal_spans"] / c["counts"]["native"]["abnormal_spans"]
                                                                     for c in rows if c["counts"]["native"]["abnormal_spans"]]),
                "share_A_native": v1.quantiles([c["counts"]["native"]["anomaly"] / c["counts"]["native"]["all"] for c in rows]),
                "share_A_md": v1.quantiles([c["counts"]["md"]["anomaly"] / c["counts"]["md"]["all"] for c in rows]),
                "covered_share_of_total_duration": v1.quantiles([c["covered_share_of_total_duration"] for c in rows])}

    summary = {"n_plan": len(cases), "status_counts": dict(Counter(c["status"] for c in cases)),
               "sham_exact": sum(c["sham_exact"] for c in cases),
               "sham_exact_by_source_status": dict(Counter(c["source_status"] for c in cases if c["sham_exact"])),
               "md_status_counts": dict(Counter(str(c["md_status"]) for c in cases)),
               "self_check_native_rank_equals_t028": sum(bool(c.get("self_check_native_rank_equals_t028")) for c in cases),
               "all": tally(ok), "RE2-TT": tally([c for c in ok if c["dataset"] == "RE2-TT"]),
               "Nezha-OB": tally([c for c in ok if c["dataset"] == "Nezha-OB"]),
               "note": "M-D đổi đại lượng cờ từ duration sang thời lượng chưa được span con trực tiếp phủ; phân hoạch A/N, đếm phủ, "
                       "trọng số chạy lại bằng mã native. Kết quả là tác động tổng, không tách riêng PageRank. Không phải phương pháp mới."}
    v1.write(out, {"schema": "T032-MicroRank-MD-v1",
                   "design": ["results/T-032/thiet-ke-phep-doi-001.md#4", "results/T-032/thiet-ke-phep-doi-003.md#3"],
                   "run": run.relative_to(BASE).as_posix(), "relation_source": MICRO_CORE.relative_to(BASE).as_posix(),
                   "relation_source_sha256": v1.sha(MICRO_CORE), "labels_sha256": v1.sha(v1.LABELS),
                   "this_script_sha256": v1.sha(__file__), "summary": summary, "cases": cases})
    print(json.dumps(summary, ensure_ascii=False, indent=1))


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("circa-regression", "microrank"):
        print(__doc__)
        return 2
    run, out = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    (circa_regression if sys.argv[1] == "circa-regression" else collect_microrank)(run, out)
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
