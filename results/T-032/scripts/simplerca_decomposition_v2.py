"""T-032 SimpleRCA: phân rã cộng chính xác của điểm (thiet-ke-phep-doi-001.md mục 7). Không can thiệp. Bản v2.

Chạy trên EC2, chỉ đọc capture của 52 lượt phát lại đã khớp tuyệt đối. Điểm = phiếu metric + phiếu trace + phiếu log.
Kiểm bằng số: tổng ba kênh bằng điểm; phiếu metric của service bằng tổng phiếu các cột của service; điểm trong
bản ghi trùng điểm trong kết quả native. Tính cho mọi service trước, nối nhãn root sau cùng.
Dùng: python simplerca_decomposition_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path("/home/ubuntu/rca/T-032")
LABELS = BASE / "repo/results/T-028/runs/phan-hoi-review-001/ca-sai.json"
ROOTS = ["runs/simplerca-re2-first-001", "runs/simplerca-nezha-first-001", "runs/simplerca-batch-001/cases"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


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


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    labels = {}
    for row in read(LABELS)["main_rows"]:
        if row["method"] == "simplerca":
            flags = {k: (((row.get("mechanisms") or {}).get(k) or {}).get("assignment") or {}).get("multi") for k in ("1", "5")}
            labels[(row["dataset"], row["opaque_id"])] = {"root": row["root"], "fault": row["fault"], "cell": row["cell"],
                "t028": {"status": row["status"], "rank_min": row["rank_min"], "rank_max": row["rank_max"], "multi_flags": flags}}
    directories = {}
    for root in ROOTS:
        for check in sorted((BASE / root).rglob("check.json")):
            if (check.parent / "capture/native-result.json").is_file():
                value = read(check)
                directories[(value["dataset"], value["opaque_id"])] = (check.parent, value)
    # Bản v2: một ca có lượt phát lại đầu bị bộ kiểm cũ ghi FAIL do lỗi công cụ, sau đó được kiểm hồi cứu PASS
    # (check có `original_run`, `record_exact`). Khi đó dùng capture của lượt gốc với phán quyết của lượt kiểm hồi cứu.
    for check in sorted((BASE / "runs").glob("simplerca-*/check.json")):
        value = read(check)
        if value.get("original_run") and value.get("status") == "PASS" and value.get("record_exact") is True:
            original = Path(value["original_run"])
            if (original / "capture/native-result.json").is_file():
                directories[(value["dataset"], value["opaque_id"])] = (original, {**value, "posthoc_audit": str(check)})
    cases = []
    for key, label in sorted(labels.items()):
        dataset, opaque_id = key
        base = {"dataset": dataset, "opaque_id": opaque_id, **label}
        if key not in directories:
            cases.append({**base, "status": "N/A", "reason": "không tìm thấy lượt phát lại"})
            continue
        directory, check = directories[key]
        if check.get("status") != "PASS" or check.get("differences") != []:
            cases.append({**base, "status": "INVALID", "reason": "lượt phát lại không PASS"})
            continue
        record, native = read(directory / "ban-ghi-0.json"), read(directory / "capture/native-result.json")
        if record["status"] != "OK":
            cases.append({**base, "status": "N/A", "reason": "trạng thái " + record["status"]})
            continue
        scores, metrics = native["scores"], native["metrics"]
        columns = {}
        for column, row in metrics.items():
            columns.setdefault(row["service"], []).append({"column": column, "vote": row["vote"], "status": row["status"],
                                                             "count": row.get("count"), "n_incident": row["n_incident"]})
        additive = all(s["score"] == s["metric"] + s["trace"] + s["log"] for s in scores.values())
        metric_sum = all(scores[service]["metric"] == sum(c["vote"] for c in columns.get(service, [])) for service in scores)
        record_matches = all(float(scores[row["item"]]["score"]) == row["key"][0] for row in record["ranking"])
        item_of = {}
        for row in record["ranking"]:
            item_of.setdefault(row["entity"], []).append(row["item"])
        rank = ranks(record)

        def parts(entity):
            best = item_of[entity][0]  # item đứng cao nhất của thực thể trong danh sách đã xếp
            cols = sorted(columns.get(best, []), key=lambda c: -c["vote"])
            return {"entity": entity, "item": best, "rank_min": rank[entity][0], "rank_max": rank[entity][1], **scores[best],
                    "metric_columns": len(cols), "metric_columns_usable": sum(c["status"] == "ok" for c in cols),
                    "metric_columns_with_votes": sum(c["vote"] > 0 for c in cols),
                    "top_metric_columns": [{"column": c["column"], "vote": c["vote"]} for c in cols[:3] if c["vote"] > 0],
                    "trace_status": (native["traces"].get(best) or {}).get("status", "absent"),
                    "log_status": (native["logs"].get(best) or {}).get("status", "absent")}

        # Từ đây mới nối nhãn.
        root = label["root"]
        item = {**base, "status": "OK", "additive_identity": bool(additive), "metric_votes_equal_column_sum": bool(metric_sum),
                "record_scores_equal_native": bool(record_matches), "n_entities": len(rank), "check_sha256": sha(directory / "check.json"),
                "posthoc_audit": check.get("posthoc_audit")}
        if root not in rank:
            item["root_ranked"] = False
            cases.append(item)
            continue
        root_parts = parts(root)
        above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
        item.update(root_ranked=True, root_parts=root_parts,
                    self_check_rank_equals_t028=(label["t028"]["status"] == "OK" and
                                                 [rank[root][0], rank[root][1]] == [label["t028"]["rank_min"], label["t028"]["rank_max"]]),
                    above_root=[])
        for entity in above:
            p = parts(entity)
            p["difference_vs_root"] = {channel: p[channel] - root_parts[channel] for channel in ("metric", "trace", "log", "score")}
            item["above_root"].append(p)
        item["n_above"] = len(above)
        item["above_decided_by_metric_alone"] = sum(a["difference_vs_root"]["metric"] > 0 and
                                                    a["difference_vs_root"]["trace"] + a["difference_vs_root"]["log"] <= 0 for a in item["above_root"])
        item["above_where_metric_difference_not_positive"] = sum(a["difference_vs_root"]["metric"] <= 0 for a in item["above_root"])
        cases.append(item)
    ok = [c for c in cases if c["status"] == "OK" and c.get("root_ranked")]

    def tally(rows):
        def count(predicate):
            return sum(1 for c in rows if predicate(c))
        wrong = [c for c in rows if c["root_parts"]["rank_max"] > 1]
        return {"n": len(rows), "hit1": count(lambda c: c["root_parts"]["rank_max"] == 1), "hit5": count(lambda c: c["root_parts"]["rank_max"] <= 5),
                "root_score_zero": count(lambda c: c["root_parts"]["score"] == 0),
                "root_metric_votes_zero": count(lambda c: c["root_parts"]["metric"] == 0),
                "root_trace_vote_one": count(lambda c: c["root_parts"]["trace"] == 1),
                "root_log_vote_one": count(lambda c: c["root_parts"]["log"] == 1),
                "wrong_at_1": {"n": len(wrong),
                               "entity_pairs_above_root": sum(c["n_above"] for c in wrong),
                               "pairs_decided_by_metric_alone": sum(c["above_decided_by_metric_alone"] for c in wrong),
                               "pairs_where_metric_difference_not_positive": sum(c["above_where_metric_difference_not_positive"] for c in wrong),
                               "cases_all_above_decided_by_metric_alone": sum(c["above_decided_by_metric_alone"] == c["n_above"] for c in wrong)}}

    summary = {"n_cases": len(cases), "status_counts": {s: sum(c["status"] == s for c in cases) for s in ("OK", "N/A", "INVALID")},
               "additive_identity": sum(bool(c.get("additive_identity")) for c in cases),
               "metric_votes_equal_column_sum": sum(bool(c.get("metric_votes_equal_column_sum")) for c in cases),
               "record_scores_equal_native": sum(bool(c.get("record_scores_equal_native")) for c in cases),
               "self_check_rank_equals_t028": sum(bool(c.get("self_check_rank_equals_t028")) for c in cases),
               "all": tally(ok), "by_dataset": {d: tally([c for c in ok if c["dataset"] == d]) for d in ("RE2-TT", "Nezha-OB")},
               "note": "Phân rã đại số chính xác của điểm, không phải thí nghiệm can thiệp. Hit tính bi quan theo hòa. "
                       "Phiếu metric là số mẫu sau mốc vượt ngưỡng, cộng qua các cột của service; phiếu trace và log là 0 hoặc 1."}
    (out / "summary.json").write_text(json.dumps({"schema": "T032-simplerca-decomposition-v2",
        "design": "results/T-032/thiet-ke-phep-doi-001.md#7", "summary": summary, "cases": cases, "methods_executed": False},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
