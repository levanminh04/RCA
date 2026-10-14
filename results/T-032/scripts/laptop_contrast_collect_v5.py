"""T-032 bản 012 (KT-3, KT-8 nửa MicroRank): tổng hợp lượt microrank-kt3. Chạy trên laptop, chỉ đọc.

Nhánh: shampc (giữ nguyên), c1h (đếm riêng, bộ chia native), mo15c1 và mo1p50c1 (bộ chia theo bài gốc + đếm riêng), dropnew.
Nhãn root nối ở đây, sau khi mọi nhánh đã chạy. Tăng/giảm hạng theo hạng tốt nhất (rank_min); Hit@k bi quan theo hạng xấu nhất (rank_max).
So sánh: c1h với nhánh M-C1 của phiên 9; nhánh ghép với nhánh chỉ thay bộ chia (runs/microrank-partition-001/collect-001).
Dùng: py -3 -B -X utf8 scripts/laptop_contrast_collect_v5.py <thư mục lượt> <thư mục tổng hợp mới>
"""
import hashlib
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path("D:/RCA-flashticket")
BASE = REPO / "results/T-032"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
CENSUS = BASE / "runs/trace-root-census-001/summary.json"
C1_P9 = BASE / "runs/microrank-core-aprime-c1-002/summary.json"
PART = BASE / "runs/microrank-partition-001/collect-001/summary.json"
PAIR = {"mo15c1": "mo15", "mo1p50c1": "mo1p50"}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ranks(record):
    out, offset, groups, order = {}, 0, defaultdict(list), []
    for row in record.get("entity_ranking") or []:
        if row["tie_group"] not in groups:
            order.append(row["tie_group"])
        groups[row["tie_group"]].append(row["entity"])
    for g in order:
        for e in groups[g]:
            out[e] = (offset + 1, offset + len(groups[g]))
        offset += len(groups[g])
    return out


def branch_dir(case_dir, branch):
    found = [d for d in sorted(case_dir.glob(branch + "*")) if (d / "check.json").is_file() and (d.name == branch or d.name.startswith(branch + "-lan"))]
    return found[-1] if found else None


def view(directory, root):
    check = read(directory / "check.json")
    record = read(directory / "ban-ghi-0.json")
    info = check["info"]
    call = (info.get("calls") or [{}])[0]
    out = {"status": record["status"], "method_status_raw": record.get("method_status_raw"), "error": (record.get("error") or "")[:160] or None,
           "exact_vs_frozen": check["exact_vs_frozen"], "call": {k: v for k, v in call.items() if not k.endswith("_by_service")},
           "count_call_anomaly": next((c for c in info.get("count_calls") or [] if c.get("is_anomaly")), None)}
    if call.get("new_abnormal") and "new_abnormal_traces_by_service" in call:
        out["new_abnormal_share_with_root"] = call["new_abnormal_traces_by_service"].get(root, 0) / call["new_abnormal"]
    rank = ranks(record) if record["status"] == "OK" else {}
    if root in rank:
        out.update(root_ranked=True, root_rank_min=rank[root][0], root_rank_max=rank[root][1], n_entities=len(rank),
                   n_tie_groups=len({v for v in rank.values()}),
                   above=sorted(e for e in rank if e != root and rank[e][1] < rank[root][0]), top=[e for e in rank if rank[e][0] == 1])
    else:
        out["root_ranked"] = False
    return out


def eff(new, old):
    return "tăng hạng" if new < old else "giảm hạng" if new > old else "không đổi"


def main():
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    labels = {(r["dataset"], r["opaque_id"]): r for r in read(LABELS)["main_rows"] if r["method"] == "microrank_full"}
    gate = {(c["dataset"], c["opaque_id"]): c["gate"]["pass"] for c in read(CENSUS)["cases"]}
    c1p9 = {(c["dataset"], c["opaque_id"]): c for c in read(C1_P9)["cases"]}
    part = {(c["dataset"], c["opaque_id"]): c for c in read(PART)["cases"]}
    cases = []
    for key, label in sorted(labels.items()):
        dataset, opaque_id = key
        case_dir = run / "cases" / dataset / opaque_id
        root = label["root"]
        item = {"dataset": dataset, "opaque_id": opaque_id, "root": root, "fault": label["fault"], "cell": label["cell"],
                "t028": {"status": label["status"], "rank_min": label.get("rank_min"), "rank_max": label.get("rank_max")}, "gate_pass": gate.get(key), "branches": {}}
        for b in ("shampc", "c1h", "mo15c1", "mo1p50c1", "dropnew"):
            d = branch_dir(case_dir, b)
            item["branches"][b] = view(d, root) if d else {"status": "CHƯA_CHẠY"}
        s = item["branches"]["shampc"]
        item["self_check_sham_exact"] = s.get("exact_vs_frozen")
        item["self_check_sham_rank_equals_t028"] = (label["status"] != "OK") or (
            s.get("root_ranked") and [s["root_rank_min"], s["root_rank_max"]] == [label["rank_min"], label["rank_max"]])
        ref = c1p9[key]
        if ref.get("status") == "OK" and item["branches"]["c1h"].get("root_ranked"):
            r9 = ref["branches"]["c1"]["root"]
            item["c1h_equals_phien9_c1"] = [item["branches"]["c1h"]["root_rank_min"], item["branches"]["c1h"]["root_rank_max"]] == [r9["rank_min"], r9["rank_max"]]
            item["c1_phien9_root_rank"] = [r9["rank_min"], r9["rank_max"]]
        item["partition_only"] = {b: {k: part[key]["branches"][b].get(k) for k in ("status", "root_ranked", "root_rank_min", "root_rank_max", "top")} for b in ("mo15", "mo1p50")}
        cases.append(item)

    def block(rows, b):
        base = PAIR[b]
        res = {"cases": len(rows), "state": dict(Counter(
            "N/A_mốc_90" if not c["gate_pass"] else
            "nguồn_" + c["branches"]["shampc"]["status"] if c["branches"]["shampc"]["status"] != "OK" else
            c["branches"][b]["status"] if c["branches"][b]["status"] != "OK" else
            "OK_root_không_được_xếp" if not c["branches"][b].get("root_ranked") else "OK" for c in rows))}
        ev = [c for c in rows if c["gate_pass"] and c["branches"]["shampc"].get("root_ranked") and c["branches"][b].get("root_ranked")
              and c["partition_only"][base].get("root_ranked")]
        res["evaluable_with_partition_only"] = len(ev)
        res["hit1"] = {"native": sum(c["branches"]["shampc"]["root_rank_max"] == 1 for c in ev),
                       base: sum(c["partition_only"][base]["root_rank_max"] == 1 for c in ev),
                       "c1h": sum(c["branches"]["c1h"].get("root_rank_max") == 1 for c in ev),
                       b: sum(c["branches"][b]["root_rank_max"] == 1 for c in ev)}
        res["hit5"] = {"native": sum(c["branches"]["shampc"]["root_rank_max"] <= 5 for c in ev),
                       base: sum(c["partition_only"][base]["root_rank_max"] <= 5 for c in ev),
                       "c1h": sum((c["branches"]["c1h"].get("root_rank_max") or 99) <= 5 for c in ev),
                       b: sum(c["branches"][b]["root_rank_max"] <= 5 for c in ev)}
        e1 = Counter(eff(c["branches"][b]["root_rank_min"], c["partition_only"][base]["root_rank_min"]) for c in ev)
        e2 = Counter(eff(c["branches"][b]["root_rank_min"], c["branches"]["shampc"]["root_rank_min"]) for c in ev)
        res["root_effect_vs_partition_only"] = {k: e1.get(k, 0) for k in ("tăng hạng", "không đổi", "giảm hạng")}
        res["root_effect_vs_native"] = {k: e2.get(k, 0) for k in ("tăng hạng", "không đổi", "giảm hạng")}
        res["wrong_under_partition_only_becomes_rank1"] = [sum(c["branches"][b]["root_rank_max"] == 1 for c in ev if c["partition_only"][base]["root_rank_max"] > 1),
                                                           sum(c["partition_only"][base]["root_rank_max"] > 1 for c in ev)]
        res["rank1_under_partition_only_lost"] = [sum(c["branches"][b]["root_rank_max"] > 1 for c in ev if c["partition_only"][base]["root_rank_max"] == 1),
                                                  sum(c["partition_only"][base]["root_rank_max"] == 1 for c in ev)]
        res["ties_root_rank_min_lt_max"] = sum(c["branches"][b]["root_rank_min"] < c["branches"][b]["root_rank_max"] for c in ev)
        res["abnormal_traces_without_flagged_span"] = {"cases_any": sum(1 for c in ev if (c["branches"][b]["count_call_anomaly"] or {}).get("group_traces", 0)
                                                                         > (c["branches"][b]["count_call_anomaly"] or {}).get("group_traces_with_flagged_span", 0))}
        res["top_entity_when_root_not_first"] = dict(Counter(e for c in ev if c["branches"][b]["root_rank_min"] > 1 for e in c["branches"][b]["top"]).most_common(6))
        return res

    ok_native = [c for c in cases if c["t028"]["status"] == "OK"]
    summary = {"self_check": {"cases": len(cases), "shampc_exact": sum(bool(c["self_check_sham_exact"]) for c in cases),
                              "shampc_rank_equals_t028": sum(bool(c["self_check_sham_rank_equals_t028"]) for c in cases),
                              "shampc_status": dict(Counter(c["branches"]["shampc"]["status"] for c in cases)),
                              "c1h_rank_equals_phien9_c1": [sum(bool(c.get("c1h_equals_phien9_c1")) for c in cases), sum("c1h_equals_phien9_c1" in c for c in cases)],
                              "dropnew_exact_where_native_ok": [sum(bool(c["branches"]["dropnew"].get("exact_vs_frozen")) for c in ok_native), len(ok_native)]},
               "c1h": {d: {"evaluable": len(r), "hit1_native": sum(c["branches"]["shampc"]["root_rank_max"] == 1 for c in r),
                           "hit1_c1h": sum(c["branches"]["c1h"]["root_rank_max"] == 1 for c in r)}
                       for d, r in ((d, [c for c in cases if (d == "all" or c["dataset"] == d) and c["branches"]["c1h"].get("root_ranked")
                                         and c["branches"]["shampc"].get("root_ranked")]) for d in ("RE2-TT", "Nezha-OB", "all"))}}
    for dataset in ("RE2-TT", "Nezha-OB", "all"):
        rows = [c for c in cases if dataset == "all" or c["dataset"] == dataset]
        summary[dataset] = {b: block(rows, b) for b in PAIR}
    summary["dropnew_error_cases"] = [{"opaque_id": c["opaque_id"], "cell": c["cell"], "status": c["branches"]["dropnew"]["status"], "error": c["branches"]["dropnew"].get("error"),
                                       "call": c["branches"]["dropnew"].get("call"), "root_ranked": c["branches"]["dropnew"].get("root_ranked"),
                                       "root_rank": [c["branches"]["dropnew"].get("root_rank_min"), c["branches"]["dropnew"].get("root_rank_max")],
                                       "n_above": len(c["branches"]["dropnew"].get("above") or []), "top": c["branches"]["dropnew"].get("top")}
                                      for c in cases if c["t028"]["status"] != "OK"]
    result = {"schema": "T032-laptop-contrast-collect-v5", "design": "results/T-032/thiet-ke-phep-doi-012.md mục 1, 2", "run": str(run),
              "sources": {"labels_sha256": sha(LABELS), "census_sha256": sha(CENSUS), "c1_phien9_sha256": sha(C1_P9), "partition_collect_sha256": sha(PART)},
              "name": "phép ghép: bộ chia theo công thức của bài gốc (span đầu do ta quy ước) + đếm riêng; không phải MicroRank gốc",
              "summary": summary, "cases": cases, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary["self_check"], ensure_ascii=False))
    print("c1h", json.dumps(summary["c1h"], ensure_ascii=False))
    for dataset in ("RE2-TT", "Nezha-OB", "all"):
        for b in PAIR:
            print(dataset, b, json.dumps(summary[dataset][b], ensure_ascii=False))
    for x in summary["dropnew_error_cases"]:
        print("dropnew", json.dumps(x, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
