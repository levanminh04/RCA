"""T-032 TORAI B: phân rã hạng root theo khối (cụm) và nhánh trong khối, từ bản ghi đóng băng. Không can thiệp.

Chạy trên EC2, chỉ đọc 90 bản ghi TORAI B của T-024 (30 ca RE2-TT x 3 seed). Bản ghi đã lưu: các khối theo thứ tự
điểm cụm, nhóm trong khối, và nhánh tạo thứ tự trong khối (don = cụm một service, rcd, du_phong).
Hạng của root = số thực thể ở các khối đứng trước + số thực thể ở các nhóm đứng trước trong cùng khối + 1.
Mỗi seed giữ riêng, không gộp. Tính cho mọi thực thể trước, nối nhãn root sau cùng.
Dùng: python torai_block_decomposition_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import sys
from pathlib import Path

REPO = Path("/home/ubuntu/rca/T-032/repo")
INDEX = REPO / "results/T-024/ban-ghi-dua-vao-cham.json"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    labels = {}
    for row in read(LABELS)["main_rows"]:
        if row["dataset"] == "RE2-TT":
            labels.setdefault(row["opaque_id"], {"root": row["root"], "fault": row["fault"], "cell": row["cell"]})
            if row["method"] == "torai_B":
                labels[row["opaque_id"]]["t028_seed_metrics"] = {seed: {"rank_min": m.get("rank_min"), "rank_max": m.get("rank_max")}
                                                                 for seed, m in (row.get("seed_metrics") or {}).items()}
    units = []
    for entry in read(INDEX)["records"]:
        if entry["method"] != "torai" or entry.get("variant") != "B":
            continue
        path = REPO / entry["path"]
        base = {"opaque_id": entry["opaque_id"], "seed": entry["seed"], "path": entry["path"]}
        if sha(path) != entry["sha256"]:
            units.append({**base, "status": "INVALID", "reason": "bản đóng băng khác hash chỉ mục"})
            continue
        record = read(path)
        if record["status"] != "OK":
            units.append({**base, "status": "N/A", "source_status": record["status"]})
            continue
        blocks, branches = record["blocks"], record["extra"]["nhanh_khoi"]
        layout = []
        for index, block in enumerate(blocks):
            for position, group in enumerate(block["groups"]):
                for entity in group:
                    layout.append({"entity": entity, "block": index, "group": position, "group_size": len(group),
                                   "block_size": sum(len(g) for g in block["groups"]), "branch": branches[index], "block_key": block["key"][0]})
        order_ok = [row["entity"] for row in layout] == [row["entity"] for row in record["entity_ranking"]]
        # Từ đây mới nối nhãn.
        label = labels[entry["opaque_id"]]
        root = label["root"]
        unit = {**base, "status": "OK", "root": root, "fault": label["fault"], "cell": label["cell"],
                "blocks": len(blocks), "blocks_multi_service": record["diagnostics"]["cum_nhieu_service"],
                "blocks_fallback": record["diagnostics"]["cum_du_phong"], "branches": branches,
                "layout_order_equals_entity_ranking": order_ok}
        mine = [row for row in layout if row["entity"] == root]
        if not mine:
            unit["root_ranked"] = False
            units.append(unit)
            continue
        mine = mine[0]
        ahead_blocks = sum(row["block"] < mine["block"] for row in layout)
        ahead_groups = sum(row["block"] == mine["block"] and row["group"] < mine["group"] for row in layout)
        rank_min, rank_max = ahead_blocks + ahead_groups + 1, ahead_blocks + ahead_groups + mine["group_size"]
        t028 = (label.get("t028_seed_metrics") or {}).get(str(entry["seed"]))
        unit.update(root_ranked=True, root_block=mine["block"], root_group=mine["group"], root_group_size=mine["group_size"],
                    root_block_size=mine["block_size"], root_block_branch=mine["branch"], root_block_key=mine["block_key"],
                    entities_in_earlier_blocks=ahead_blocks, entities_in_earlier_groups_same_block=ahead_groups,
                    rank_min=rank_min, rank_max=rank_max,
                    self_check_rank_equals_t028=t028 is not None and [rank_min, rank_max] == [t028["rank_min"], t028["rank_max"]],
                    where_root_is_lost=("không mất" if rank_max == 1 else
                                        "khối của root không đứng đầu" if ahead_blocks else
                                        "trong khối đầu, nhóm khác đứng trước" if ahead_groups else "hòa trong nhóm đầu"))
        units.append(unit)
    ok = [u for u in units if u["status"] == "OK" and u.get("root_ranked")]

    def count(rows, predicate):
        return sum(1 for u in rows if predicate(u))

    wrong = [u for u in ok if u["rank_max"] > 1]
    by_case = {}
    for u in ok:
        by_case.setdefault(u["opaque_id"], []).append(u)
    summary = {
        "n_units": len(units), "status_counts": {s: sum(u["status"] == s for u in units) for s in ("OK", "N/A", "INVALID")},
        "n_ok_root_ranked": len(ok), "layout_order_equals_entity_ranking": count(ok, lambda u: u["layout_order_equals_entity_ranking"]),
        "self_check_rank_equals_t028": count(ok, lambda u: u["self_check_rank_equals_t028"]),
        "hit1_units": count(ok, lambda u: u["rank_max"] == 1), "hit5_units": count(ok, lambda u: u["rank_max"] <= 5),
        "wrong_at_1_units": {"n": len(wrong),
                             "where_root_is_lost": {k: count(wrong, lambda u, k=k: u["where_root_is_lost"] == k)
                                                    for k in ("khối của root không đứng đầu", "trong khối đầu, nhóm khác đứng trước", "hòa trong nhóm đầu")},
                             "root_block_branch": {k: count(wrong, lambda u, k=k: u["root_block_branch"] == k) for k in ("don", "rcd", "du_phong")}},
        "all_units_root_block_branch": {k: count(ok, lambda u, k=k: u["root_block_branch"] == k) for k in ("don", "rcd", "du_phong")},
        "blocks_total": {"multi_service": sum(u["blocks_multi_service"] for u in ok), "fallback": sum(u["blocks_fallback"] for u in ok)},
        "cases": {"n": len(by_case),
                  "three_seeds_same_rank": sum(len({(u["rank_min"], u["rank_max"]) for u in rows}) == 1 for rows in by_case.values()),
                  "three_seeds_same_root_block_and_branch": sum(len({(u["root_block"], u["root_block_branch"]) for u in rows}) == 1 for rows in by_case.values())},
        "note": "Đơn vị là ca x seed, không gộp seed. Hit tính bi quan theo hòa. Điểm severity từng service không có trong bản ghi; "
                "muốn lần tiếp vì sao cụm của root có điểm thấp thì cần trung gian của bước severity và phân cụm.",
    }
    (out / "summary.json").write_text(json.dumps({"schema": "T032-torai-block-decomposition-v1", "summary": summary, "units": units,
                                                  "methods_executed": False}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
