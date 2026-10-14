"""T-032 bản 009 (việc 4): tổng hợp ba nhánh shamp / mo15 / mo1p50 của lượt microrank-partition. Chạy trên laptop, chỉ đọc.

Nhãn root nối ở đây, sau khi mọi nhánh đã chạy. Quy ước như các bộ tổng hợp trước: tăng/giảm hạng theo hạng tốt nhất (rank_min),
Hit@k bi quan theo hạng xấu nhất (rank_max). Mẫu số giữ đủ 52 ca; N/A theo mốc 90% của bước đếm, ERROR và nhóm rỗng đếm riêng.
Dùng: py -3 -B -X utf8 scripts/laptop_contrast_collect_v4.py <thư mục lượt> <thư mục tổng hợp mới>
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
BRANCHES = ("mo15", "mo1p50")


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
    """Thư mục lần chạy cuối có check.json (branch, branch-lan2, ...)."""
    found = [d for d in sorted(case_dir.glob(branch + "*")) if (d / "check.json").is_file() and (d.name == branch or d.name.startswith(branch + "-lan"))]
    return found[-1] if found else None


def view(directory, root):
    check = read(directory / "check.json")
    record = read(directory / "ban-ghi-0.json")
    call = (check["info"].get("calls") or [{}])[0]
    out = {"status": record["status"], "method_status_raw": record.get("method_status_raw"), "error": (record.get("error") or "")[:160] or None,
           "exact_vs_frozen": check["exact_vs_frozen"], "call": {k: v for k, v in call.items() if not k.endswith("_by_service")}}
    for key, total in (("native_abnormal_traces_by_service", "native_abnormal"), ("new_abnormal_traces_by_service", "new_abnormal")):
        if key in call and call.get(total):
            out[key.replace("_traces_by_service", "_share_with_root")] = call[key].get(root, 0) / call[total]
    rank = ranks(record) if record["status"] == "OK" else {}
    if root in rank:
        out.update(root_ranked=True, root_rank_min=rank[root][0], root_rank_max=rank[root][1], n_entities=len(rank),
                   above=sorted(e for e in rank if e != root and rank[e][1] < rank[root][0]),
                   top=[e for e in rank if rank[e][0] == 1])
    else:
        out["root_ranked"] = False
    return out


def q(values):
    values = sorted(v for v in values if v is not None)
    if not values:
        return {"n": 0}
    return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]}


def main():
    run, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    labels = {(r["dataset"], r["opaque_id"]): r for r in read(LABELS)["main_rows"] if r["method"] == "microrank_full"}
    gate = {(c["dataset"], c["opaque_id"]): c["gate"]["pass"] for c in read(CENSUS)["cases"]}
    cases = []
    for (dataset, opaque_id), label in sorted(labels.items()):
        case_dir = run / "cases" / dataset / opaque_id
        item = {"dataset": dataset, "opaque_id": opaque_id, "root": label["root"], "fault": label["fault"], "cell": label["cell"],
                "t028": {"status": label["status"], "rank_min": label.get("rank_min"), "rank_max": label.get("rank_max")},
                "gate_pass": gate.get((dataset, opaque_id)), "branches": {}}
        sham = branch_dir(case_dir, "shamp")
        if sham is None:
            item["state"] = "CHƯA_CHẠY"
            cases.append(item)
            continue
        item["shamp"] = view(sham, label["root"])
        item["self_check_sham_exact"] = item["shamp"]["exact_vs_frozen"]
        item["self_check_sham_rank_equals_t028"] = (label["status"] != "OK") or (
            item["shamp"].get("root_ranked") and [item["shamp"]["root_rank_min"], item["shamp"]["root_rank_max"]] == [label["rank_min"], label["rank_max"]])
        for b in BRANCHES:
            d = branch_dir(case_dir, b)
            item["branches"][b] = view(d, label["root"]) if d else {"status": "CHƯA_CHẠY"}
        cases.append(item)

    def block(rows, b):
        res = {"cases": len(rows), "state": dict(Counter(
            "CHƯA_CHẠY" if "shamp" not in c or c["branches"][b].get("status") == "CHƯA_CHẠY" else
            "N/A_mốc_90" if not c["gate_pass"] else
            "nguồn_" + c["shamp"]["status"] if c["shamp"]["status"] != "OK" else
            c["branches"][b]["status"] if c["branches"][b]["status"] != "OK" else
            "OK_root_không_được_xếp" if not c["branches"][b].get("root_ranked") else "OK" for c in rows))}
        ev = [c for c in rows if "shamp" in c and c["gate_pass"] and c["shamp"]["status"] == "OK" and c["shamp"].get("root_ranked")
              and c["branches"][b].get("status") == "OK" and c["branches"][b].get("root_ranked")]
        res["evaluable"] = len(ev)
        res["method_status_raw_all"] = dict(Counter(str(c["branches"][b].get("method_status_raw")) for c in rows if "shamp" in c))
        eff = Counter("tăng hạng" if c["branches"][b]["root_rank_min"] < c["shamp"]["root_rank_min"] else
                      "giảm hạng" if c["branches"][b]["root_rank_min"] > c["shamp"]["root_rank_min"] else "không đổi" for c in ev)
        res["root_effect"] = {k: eff.get(k, 0) for k in ("tăng hạng", "không đổi", "giảm hạng")}
        res["hit1"] = {"native": sum(c["shamp"]["root_rank_max"] == 1 for c in ev), b: sum(c["branches"][b]["root_rank_max"] == 1 for c in ev)}
        res["hit5"] = {"native": sum(c["shamp"]["root_rank_max"] <= 5 for c in ev), b: sum(c["branches"][b]["root_rank_max"] <= 5 for c in ev)}
        res["hit1_all_native_ok"] = {"native": sum(c["shamp"].get("root_rank_max") == 1 for c in rows if "shamp" in c and c["shamp"]["status"] == "OK"),
                                     "note": "mẫu số là mọi ca native OK, kể cả ca N/A hoặc ERROR ở nhánh mới"}
        res["abnormal_share"] = {"native": q([c["branches"][b]["call"].get("native_abnormal_share") for c in ev]),
                                 b: q([c["branches"][b]["call"].get("new_abnormal_share") for c in ev])}
        res["abnormal_share_with_root_service"] = {"native": q([c["branches"][b].get("native_abnormal_share_with_root") for c in ev]),
                                                   b: q([c["branches"][b].get("new_abnormal_share_with_root") for c in ev])}
        res["new_abnormal_count"] = q([c["branches"][b]["call"].get("new_abnormal") for c in ev])
        pairs = [(c, e) for c in ev for e in c["shamp"]["above"]]
        res["pairs_above_root_native"] = {"n": len(pairs), "still_above": sum(e in c["branches"][b]["above"] for c, e in pairs),
                                          "gone": sum(e not in c["branches"][b]["above"] for c, e in pairs),
                                          "new_pairs": sum(e not in c["shamp"]["above"] for c in ev for e in c["branches"][b]["above"])}
        res["top_entity_when_root_not_first"] = {"native": dict(Counter(e for c in ev if c["shamp"]["root_rank_min"] > 1 for e in c["shamp"]["top"]).most_common(5)),
                                                 b: dict(Counter(e for c in ev if c["branches"][b]["root_rank_min"] > 1 for e in c["branches"][b]["top"]).most_common(5))}
        res["by_fault"] = {f: {"evaluable": len(g), "hit1_native": sum(c["shamp"]["root_rank_max"] == 1 for c in g),
                               "hit1_branch": sum(c["branches"][b]["root_rank_max"] == 1 for c in g),
                               "root_up": sum(c["branches"][b]["root_rank_min"] < c["shamp"]["root_rank_min"] for c in g),
                               "root_down": sum(c["branches"][b]["root_rank_min"] > c["shamp"]["root_rank_min"] for c in g)}
                           for f, g in ((f, [c for c in ev if c["fault"] == f]) for f in sorted({c["fault"] for c in ev}))}
        return res

    summary = {"self_check": {"cases_with_sham": sum("shamp" in c for c in cases), "sham_exact": sum(bool(c.get("self_check_sham_exact")) for c in cases),
                              "sham_rank_equals_t028": sum(bool(c.get("self_check_sham_rank_equals_t028")) for c in cases if "shamp" in c),
                              "sham_status": dict(Counter(c["shamp"]["status"] for c in cases if "shamp" in c))}}
    for dataset in ("RE2-TT", "Nezha-OB", "all"):
        rows = [c for c in cases if dataset == "all" or c["dataset"] == dataset]
        summary[dataset] = {b: block(rows, b) for b in BRANCHES}
    result = {"schema": "T032-laptop-contrast-collect-v4", "design": "results/T-032/thiet-ke-phep-doi-009.md", "run": str(run),
              "sources": {"labels_sha256": sha(LABELS), "census_sha256": sha(CENSUS)},
              "name": "công thức của bài gốc với span đầu do ta quy ước; không phải MicroRank gốc",
              "summary": summary, "cases": cases, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary["self_check"], ensure_ascii=False))
    for dataset in ("RE2-TT", "Nezha-OB", "all"):
        for b in BRANCHES:
            r = summary[dataset][b]
            print(dataset, b, r["state"], "| ev", r["evaluable"], r["root_effect"], "hit1", r["hit1"], "hit5", r["hit5"],
                  "| A share", {k: (round(v["median"], 3) if v.get("n") else None) for k, v in r["abnormal_share"].items()},
                  "| A with root", {k: (round(v["median"], 3) if v.get("n") else None) for k, v in r["abnormal_share_with_root_service"].items()},
                  "| pairs", r["pairs_above_root_native"])


if __name__ == "__main__":
    main()
