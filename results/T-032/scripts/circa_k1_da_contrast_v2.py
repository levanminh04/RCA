"""T-032 phép K-1 (thiet-ke-phep-doi-001.md mục 8): CIRCA OLS có và không có bước DA, từ bản đóng băng. Bản v2.

Khác v1: (1) cờ "huge" xét cả thành phần đầu của khóa xếp hạng (ở DA, khóa có thể thừa hưởng điểm
của hậu duệ); v1 chỉ xét điểm RHT của nút nên đếm thiếu ở nhánh DA; (2) tự kiểm hạng root của nhánh DA
với hạng đã chấm trong T-028; (3) ghi caller rời khỏi/bước vào vị trí trên root khi thêm DA.

Chỉ đọc bản ghi đã đóng của T-024 (`ols+rht` và `ols+rht_da` sinh từ cùng một lượt chấm) và nhãn dev
trong T-028. Không gọi phương pháp. Mọi đại lượng tính cho mọi thực thể trước, nhãn root nối sau.
Dùng: python circa_k1_da_contrast_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path("/home/ubuntu/rca/T-032/repo")
INDEX = "results/T-024/ban-ghi-dua-vao-cham.json"
LABELS = "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
HUGE = 1e10  # mốc báo riêng của Q-82/WHY-36, không phải ngưỡng mới


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def ranks(record):
    """entity -> (rank_min, rank_max) theo nhóm hòa đã ghi trong bản ghi."""
    groups = {}
    for position, row in enumerate(record["entity_ranking"]):
        groups.setdefault(row["tie_group"], []).append((position, row["entity"]))
    out, offset = {}, 0
    for group in sorted(groups):
        members = groups[group]
        for _position, entity in members:
            out[entity] = (offset + 1, offset + len(members))
        offset += len(members)
    return out


def best_nodes(record):
    """entity -> nút metric đứng cao nhất của entity trong danh sách đã xếp (item, key)."""
    out = {}
    for row in record["ranking"]:
        out.setdefault(row["entity"], {"item": row["item"], "key": row["key"]})
    return out


def describe(record, call_edges):
    rank = ranks(record)
    best = best_nodes(record)
    nodes = record["diagnostics"]["nodes"]
    callers = {}
    for caller, callee in call_edges:
        callers.setdefault(callee, set()).add(caller)
    entities = {}
    for row in record["entity_ranking"]:
        entity = row["entity"]
        node = nodes.get(best[entity]["item"], {})
        entities[entity] = {"rank_min": rank[entity][0], "rank_max": rank[entity][1], "key": row["key"],
                            "best_node": best[entity]["item"], "best_node_rht_score": node.get("rht_score"),
                            "best_node_route": node.get("regression_route"), "best_node_parents": node.get("parents"),
                            "best_node_huge": abs(node.get("rht_score") or 0.0) > HUGE,
                            "key_first_huge": abs(row["key"][0]) > HUGE}
    return entities, callers


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    index = read(REPO / INDEX)
    paths = {}
    for record in index["records"]:
        if record["method"] == "circa" and record.get("variant") in ("ols+rht", "ols+rht_da"):
            paths.setdefault(record["opaque_id"], {})[record["variant"]] = (record["path"], record["sha256"])
    labels = {}
    for row in read(REPO / LABELS)["main_rows"]:
        if row["dataset"] == "RE2-TT":
            labels.setdefault(row["opaque_id"], {"root": row["root"], "fault": row["fault"], "cell": row["cell"]})
            if row["method"] == "circa_ols_da":
                flags = {}
                for k in ("1", "5"):
                    assignment = ((row.get("mechanisms") or {}).get(k) or {}).get("assignment") or {}
                    flags[k] = assignment.get("multi")
                labels[row["opaque_id"]]["t028_multi_flags_circa_ols_da"] = flags
                labels[row["opaque_id"]]["t028_rank_circa_ols_da"] = [row["rank_min"], row["rank_max"], row["status"]]
    cases = []
    for opaque_id in sorted(paths):
        pair = paths[opaque_id]
        if set(pair) != {"ols+rht", "ols+rht_da"}:
            cases.append({"opaque_id": opaque_id, "status": "N/A", "reason": "thiếu một trong hai biến thể"})
            continue
        records, hash_ok = {}, True
        for variant, (path, expected) in pair.items():
            hash_ok = hash_ok and sha(REPO / path) == expected
            records[variant] = read(REPO / path)
        statuses = {variant: record["status"] for variant, record in records.items()}
        if not hash_ok or any(status != "OK" for status in statuses.values()):
            cases.append({"opaque_id": opaque_id, "status": "N/A", "hash_ok": hash_ok, "source_statuses": statuses})
            continue
        call_edges = records["ols+rht"]["extra"]["call_edges"]
        described = {variant: describe(record, call_edges) for variant, record in records.items()}
        # Từ đây mới nối nhãn root.
        label = labels[opaque_id]
        root = label["root"]
        callers_of_root = sorted(described["ols+rht"][1].get(root, set()))
        callees_of_root = sorted(callee for caller, callee in call_edges if caller == root)
        row = {"opaque_id": opaque_id, "status": "OK", "root": root, "fault": label["fault"], "cell": label["cell"],
               "t028_multi_flags_circa_ols_da": label.get("t028_multi_flags_circa_ols_da"),
               "callers_of_root": callers_of_root, "callees_of_root": callees_of_root,
               "paths": {variant: pair[variant][0] for variant in pair}, "variants": {}}
        for variant in ("ols+rht", "ols+rht_da"):
            entities = described[variant][0]
            if root not in entities:
                row["variants"][variant] = {"root_present": False, "n_entities": len(entities)}
                continue
            root_info = entities[root]
            above = [e for e, info in entities.items() if info["rank_max"] < root_info["rank_min"]]
            row["variants"][variant] = {
                "root_present": True, "n_entities": len(entities), "root": root_info,
                "above_root": [{"entity": e, "relation": "caller_of_root" if e in callers_of_root else
                                "callee_of_root" if e in callees_of_root else "other", **entities[e]} for e in above],
                "n_above": len(above), "n_callers_above": sum(e in callers_of_root for e in above),
                "callers_above": sorted(e for e in above if e in callers_of_root),
                "any_huge_above": any(entities[e]["best_node_huge"] or entities[e]["key_first_huge"] for e in above),
                "root_best_node_huge": root_info["best_node_huge"], "root_key_first_huge": root_info["key_first_huge"]}
        a, b = row["variants"]["ols+rht"], row["variants"]["ols+rht_da"]
        if a.get("root_present") and b.get("root_present"):
            before, after = a["root"]["rank_min"], b["root"]["rank_min"]
            row["root_rank_min_rht"], row["root_rank_min_da"] = before, after
            row["da_effect_on_root"] = "tăng hạng" if after < before else "giảm hạng" if after > before else "không đổi"
            row["callers_above_rht"], row["callers_above_da"] = a["n_callers_above"], b["n_callers_above"]
            row["callers_no_longer_above_with_da"] = sorted(set(a["callers_above"]) - set(b["callers_above"]))
            row["callers_newly_above_with_da"] = sorted(set(b["callers_above"]) - set(a["callers_above"]))
            t028 = label.get("t028_rank_circa_ols_da")
            row["t028_rank_circa_ols_da"] = t028
            row["self_check_da_rank_equals_t028"] = (t028 is not None and t028[2] == "OK"
                                                     and [b["root"]["rank_min"], b["root"]["rank_max"]] == t028[:2])
        cases.append(row)
    ok = [c for c in cases if c["status"] == "OK" and "da_effect_on_root" in c]
    def count(predicate):
        return sum(1 for c in ok if predicate(c))
    summary = {
        "n_cases_in_index": len(paths), "n_ok_both_variants_root_present": len(ok),
        "n_not_applicable": len(cases) - len(ok),
        "da_effect_on_root": {key: count(lambda c, key=key: c["da_effect_on_root"] == key)
                              for key in ("tăng hạng", "không đổi", "giảm hạng")},
        "hit1": {"rht": count(lambda c: c["variants"]["ols+rht"]["root"]["rank_max"] == 1),
                 "da": count(lambda c: c["variants"]["ols+rht_da"]["root"]["rank_max"] == 1)},
        "hit5": {"rht": count(lambda c: c["variants"]["ols+rht"]["root"]["rank_max"] <= 5),
                 "da": count(lambda c: c["variants"]["ols+rht_da"]["root"]["rank_max"] <= 5)},
        "cases_with_caller_above_root": {"rht": count(lambda c: c["callers_above_rht"] > 0),
                                         "da": count(lambda c: c["callers_above_da"] > 0)},
        "cases_with_huge_node_above_root": {"rht": count(lambda c: c["variants"]["ols+rht"]["any_huge_above"]),
                                            "da": count(lambda c: c["variants"]["ols+rht_da"]["any_huge_above"])},
        "cases_root_key_first_huge": {"rht": count(lambda c: c["variants"]["ols+rht"]["root_key_first_huge"]),
                                      "da": count(lambda c: c["variants"]["ols+rht_da"]["root_key_first_huge"])},
        "self_check_da_rank_equals_t028": count(lambda c: c["self_check_da_rank_equals_t028"]),
        "cases_caller_leaves_above_root_with_da": count(lambda c: c["callers_no_longer_above_with_da"]),
        "cases_caller_enters_above_root_with_da": count(lambda c: c["callers_newly_above_with_da"]),
        "by_da_effect": {key: sorted(c["opaque_id"] + " " + c["cell"] + " " + str(c["root_rank_min_rht"]) + "->" + str(c["root_rank_min_da"])
                                     for c in ok if c["da_effect_on_root"] == key) for key in ("tăng hạng", "giảm hạng")},
        "note": "Mẫu số là số ca OK có root trong cả hai bảng xếp hạng. Hit dùng rank_max (hòa tính bi quan). "
                "Đây là so hai bản ghi đóng băng của cùng lượt chấm, không phải lượt chạy mới.",
    }
    result = {"schema": "T032-CIRCA-K1-v2", "design": "results/T-032/thiet-ke-phep-doi-001.md#8",
              "sources": {INDEX: sha(REPO / INDEX), LABELS: sha(REPO / LABELS)},
              "summary": summary, "cases": cases, "methods_executed": False}
    (out / "k1.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
