"""T-032 TORAI B: bảng lõi severity → cụm → nhánh, từ trung gian của lượt torai-core-obs-001 (đã khớp bản đóng băng).

Chạy trên EC2, chỉ đọc. Không gọi phương pháp. Mọi dịch vụ được tính trước; nhãn root nối sau cùng.
Chuỗi tính của TORAI bản sửa (src/torai/torai_sua.py):
  mỗi nguồn (metric, log, trace_lat, trace_err): điểm cột = max|z| của A theo nền N, chia cho tổng điểm mọi cột của nguồn;
  mức dịch vụ: metric = cộng các cột, log = cột cao nhất rồi chia lại cho tổng, trace_lat = cộng, trace_err = cộng;
  m = ma trận dịch vụ × 4 nguồn (thiếu thì 0); y_train = trung bình 4 nguồn (severity);
  GaussianMixture trên m, số cụm theo BIC; điểm cụm = trung bình y_train của các dịch vụ trong cụm; cụm xếp theo điểm;
  trong cụm nhiều dịch vụ: RCD, nếu RCD không trả đủ thì xếp theo y_train (nhánh dự phòng).
Tự kiểm theo đơn vị: y_train = trung bình hàng của m; điểm cụm dựng lại = cluster_rank; thứ tự khối dựng lại từ
cluster_rank trùng khối trong bản ghi; hạng root trùng T-028.
Bản v2 = v1 + chuyển kiểu số của numpy khi ghi JSON (v1 hỏng ở bước ghi; lượt torai-severity-table-001 giữ lại, rỗng).
Dùng: python torai_severity_table_v2.py <thư mục lượt mới>
"""
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

BASE = Path("/home/ubuntu/rca/T-032")
RUN = BASE / "runs/torai-core-obs-001"
REPO = BASE / "repo"
LABELS = REPO / "results/T-028/runs/phan-hoi-review-001/ca-sai.json"
SOURCES = ("metric", "log", "trace_lat", "trace_err")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def rank_desc(values, index):
    """Hạng (min, max) của phần tử index khi xếp giảm dần, hòa theo giá trị bằng nhau."""
    x = values[index]
    return 1 + int(sum(v > x for v in values)), int(sum(v >= x for v in values))


def entity_ranks(record):
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
    labels = {r["opaque_id"]: r for r in read(LABELS)["main_rows"] if r["dataset"] == "RE2-TT" and r["method"] == "torai_B"}
    units = []
    for unit_dir in sorted((RUN / "units").iterdir()):
        unit = read(unit_dir / "unit.json")
        opaque_id, seed = unit["opaque_id"], unit["seed"]
        label = labels[opaque_id]
        base = {"opaque_id": opaque_id, "seed": seed, "root": label["root"], "fault": label["fault"], "cell": label["cell"]}
        if not (unit["sham_exact_vs_frozen"] and unit.get("obs_ket_qua_exact_vs_sham")):
            units.append({**base, "status": "INVALID", "reason": "sham hoặc nhánh quan sát không khớp"})
            continue
        state = read(unit_dir / "obs/locals.json")
        loc = state["locals"]
        record = read(RUN / unit["sham_run_dir"] / "ban-ghi-0.json")
        services = loc["service_list"]
        m = np.asarray(loc["m"]["values"], dtype=float)
        y = np.asarray(loc["y_train"], dtype=float)
        pred = np.asarray(loc["y_pred"])
        assert loc["m"]["index"] == services and loc["m"]["columns"] == list(SOURCES)
        check_y = bool(np.array_equal(m.mean(axis=1), y))
        clusters = {}
        for c in sorted(set(pred.tolist())):
            idx = np.flatnonzero(pred == c)
            clusters[int(c)] = {"members": [services[i] for i in idx], "score": float(np.mean(y[idx])), "size": int(len(idx))}
        check_cluster = all(float(score).hex() == float(clusters[int(c)]["score"]).hex() for c, score in loc["cluster_rank"])
        order = [int(c) for c, _ in loc["cluster_rank"]]
        block_members = [sorted(s for g in b["groups"] for s in g) for b in record["blocks"]]
        check_blocks = block_members == [sorted(clusters[c]["members"]) for c in order]
        # --- phần mô tả cho mọi dịch vụ, chưa dùng nhãn ---
        source_rank = {s: [rank_desc(m[:, j].tolist(), i) for i in range(len(services))] for j, s in enumerate(SOURCES)}
        y_rank = [rank_desc(y.tolist(), i) for i in range(len(services))]
        top_share = {}
        for name in ("metric_ranks", "log_ranks", "trace_lat_ranks", "trace_err_ranks"):
            rows = loc[name]
            top_share[name] = {"n_columns": len(rows), "top_column": rows[0][0] if rows else None, "top_share": float(rows[0][1]) if rows else None,
                               "top3_share": float(sum(r[1] for r in rows[:3])) if rows else None}
        # --- nối nhãn ---
        root = label["root"]
        rank = entity_ranks(record)
        item = {**base, "status": "OK", "checks": {"y_train_equals_row_mean": check_y, "cluster_score_rebuilt": check_cluster,
                                                  "blocks_equal_clusters_in_rank_order": check_blocks},
                "n_services": len(services), "n_clusters": len(clusters), "n_comp_opt": loc["n_comp_opt"],
                "cluster_sizes_in_rank_order": [clusters[c]["size"] for c in order],
                "cluster_scores_in_rank_order": [clusters[c]["score"] for c in order],
                "source_top_share": top_share, "sources_nonzero_services": {s: int((m[:, j] > 0).sum()) for j, s in enumerate(SOURCES)},
                "branches": record["extra"]["nhanh_khoi"], "rcd_returns": len(state["rcd_returns"])}
        t028 = {"status": label["status"], "rank_min": label["rank_min"], "rank_max": label["rank_max"]}
        if root in rank and root in services:
            i = services.index(root)
            c_root = int(pred[i])
            pos = order.index(c_root)
            above = sorted((e for e in rank if rank[e][1] < rank[root][0]), key=lambda e: rank[e][0])
            item.update({
                "root_rank_min": rank[root][0], "root_rank_max": rank[root][1],
                "self_check_rank_equals_t028": t028["status"] == "OK" and [rank[root][0], rank[root][1]] == [t028["rank_min"], t028["rank_max"]],
                "root_vector": {s: float(m[i, j]) for j, s in enumerate(SOURCES)}, "root_severity": float(y[i]),
                "root_severity_rank": list(y_rank[i]),
                "root_source_rank": {s: list(source_rank[s][i]) for s in SOURCES},
                "root_cluster_position": pos, "root_cluster_size": clusters[c_root]["size"], "root_cluster_score": clusters[c_root]["score"],
                "root_cluster_branch": record["extra"]["nhanh_khoi"][pos],
                "root_rank_within_cluster_by_severity": list(rank_desc(y[pred == c_root].tolist(), int(np.flatnonzero(np.flatnonzero(pred == c_root) == i)[0]))),
                "services_in_earlier_clusters": int(sum(clusters[c]["size"] for c in order[:pos])),
                "top_service_by_severity": [services[k] for k in np.argsort(-y, kind="stable")[:3]],
                "above_root": []})
            for e in above:
                k = services.index(e)
                item["above_root"].append({
                    "entity": e, "rank_min": rank[e][0], "severity": float(y[k]), "severity_minus_root": float(y[k] - y[i]),
                    "cluster_position": order.index(int(pred[k])), "same_cluster_as_root": int(pred[k]) == c_root,
                    "difference_by_source": {s: float(m[k, j] - m[i, j]) for j, s in enumerate(SOURCES)},
                    "largest_source_difference": SOURCES[int(np.argmax(m[k] - m[i]))]})
            # root mất hạng ở đâu
            if rank[root][1] == 1:
                item["where_lost"] = "không mất"
            elif y_rank[i][1] > 1 and all(a["severity"] > y[i] for a in item["above_root"]):
                item["where_lost"] = "ở bước severity: mọi thực thể đứng trên root có severity lớn hơn root"
            elif y_rank[i][1] == 1:
                item["where_lost"] = "sau bước severity: root có severity cao nhất nhưng không đứng hạng 1"
            else:
                item["where_lost"] = "hỗn hợp: có thực thể đứng trên root với severity không lớn hơn root"
            item["above_root_with_lower_or_equal_severity"] = sum(a["severity"] <= y[i] for a in item["above_root"])
        else:
            item["root_ranked"] = False
        units.append(item)
    ok = [u for u in units if u["status"] == "OK" and "root_rank_min" in u]
    # ba seed của một ca có cùng trung gian trước RCD không
    by_case = {}
    for u in ok:
        by_case.setdefault(u["opaque_id"], []).append(u)
    same_pre_rcd = sum(1 for rows in by_case.values() if len(rows) == 3 and all(
        r["root_vector"] == rows[0]["root_vector"] and r["cluster_scores_in_rank_order"] == rows[0]["cluster_scores_in_rank_order"]
        and r["cluster_sizes_in_rank_order"] == rows[0]["cluster_sizes_in_rank_order"] for r in rows))
    seed0 = [u for u in ok if u["seed"] == 0]

    def q(values):
        values = sorted(values)
        return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]} if values else {"n": 0}

    wrong = [u for u in seed0 if u["root_rank_max"] > 1]
    right = [u for u in seed0 if u["root_rank_max"] == 1]
    summary = {
        "n_units": len(units), "status_counts": dict(Counter(u["status"] for u in units)),
        "checks": {k: sum(u["status"] == "OK" and u["checks"][k] for u in units) for k in ("y_train_equals_row_mean", "cluster_score_rebuilt", "blocks_equal_clusters_in_rank_order")},
        "self_check_rank_equals_t028": sum(bool(u.get("self_check_rank_equals_t028")) for u in units),
        "cases_three_seeds_same_pre_rcd_intermediates": same_pre_rcd, "n_cases": len(by_case),
        "seed0": {
            "n": len(seed0), "hit1": len(right), "wrong_at_1": len(wrong),
            "root_severity_rank_is_1": sum(u["root_severity_rank"][1] == 1 for u in seed0),
            "root_severity_rank_is_1_among_hit1": sum(u["root_severity_rank"][1] == 1 for u in right),
            "root_severity_rank_is_1_among_wrong": sum(u["root_severity_rank"][1] == 1 for u in wrong),
            "root_severity_rank": q([u["root_severity_rank"][0] for u in seed0]),
            "root_cluster_size": dict(Counter(str(min(u["root_cluster_size"], 5)) for u in seed0)),
            "n_clusters": q([u["n_clusters"] for u in seed0]),
            "largest_cluster_size": q([max(u["cluster_sizes_in_rank_order"]) for u in seed0]),
            "root_source_rank_is_1": {s: sum(u["root_source_rank"][s][1] == 1 for u in seed0) for s in SOURCES},
            "root_source_value_is_zero": {s: sum(u["root_vector"][s] == 0 for u in seed0) for s in SOURCES},
            "trace_err_columns": q([u["source_top_share"]["trace_err_ranks"]["n_columns"] for u in seed0]),
            "trace_err_top_share_ge_0_5": sum((u["source_top_share"]["trace_err_ranks"]["top_share"] or 0) >= 0.5 for u in seed0),
            "trace_lat_top_share": q([u["source_top_share"]["trace_lat_ranks"]["top_share"] for u in seed0 if u["source_top_share"]["trace_lat_ranks"]["top_share"] is not None]),
            "where_lost": dict(Counter(u["where_lost"] for u in seed0)),
            "wrong_cases": [{k: u[k] for k in ("opaque_id", "cell", "root_rank_min", "root_rank_max", "root_severity", "root_severity_rank", "root_vector",
                                               "root_source_rank", "root_cluster_position", "root_cluster_size", "root_cluster_score",
                                               "root_cluster_branch", "root_rank_within_cluster_by_severity", "cluster_sizes_in_rank_order",
                                               "cluster_scores_in_rank_order", "where_lost", "above_root", "top_service_by_severity")} for u in wrong],
            "pairs_above_root_largest_source_difference": dict(Counter(a["largest_source_difference"] for u in wrong for a in u["above_root"])),
            "pairs_above_root": sum(len(u["above_root"]) for u in wrong),
            "pairs_above_root_same_cluster": sum(a["same_cluster_as_root"] for u in wrong for a in u["above_root"]),
            "pairs_above_root_with_lower_or_equal_severity": sum(u["above_root_with_lower_or_equal_severity"] for u in wrong)},
        "note": "Mô tả từ trung gian đã khớp bản đóng băng. Bảng seed0 dùng seed 0 vì trung gian trước RCD giống nhau giữa ba seed (xem "
                "cases_three_seeds_same_pre_rcd_intermediates). Chênh theo nguồn là phân rã cộng chính xác của severity (trung bình 4 nguồn)."}
    result = {"schema": "T032-TORAI-severity-table-v2", "run": "runs/torai-core-obs-001", "methods_executed": False,
              "labels_sha256": sha(LABELS), "this_script_sha256": sha(__file__), "summary": summary, "units": units}
    def plain(value):  # v2: số nguyên/bool của numpy sinh ra từ các phép đếm
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, np.bool_):
            return bool(value)
        raise TypeError(type(value).__name__)

    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1, default=plain) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "seed0"}, ensure_ascii=False, indent=1, default=plain))
    print(json.dumps({k: v for k, v in summary["seed0"].items() if k != "wrong_cases"}, ensure_ascii=False, indent=1, default=plain))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
