"""T-032 việc 6, phần phụ của gói bổ sung (phép kiểm ghi ở ket-qua-phien-10.md mục 8): sau khi bỏ cột log có nền không đổi,
vì sao điểm log của nguồn B vẫn nghiêng về vài dịch vụ. Chạy trên EC2, chỉ đọc ca dev trong allowlist.

Dựng lại bảng log đúng như p3.torai_b.dung_logts (Drain riêng từng dịch vụ, tham số mặc định của hàm đó), có giữ thêm văn bản mẫu log.
Tự kiểm: bảng dựng lại phải trùng `bang/logts.csv` của lượt torai-core-obs-001 (lượt đó khớp bản đóng băng từng bit) ở mọi ô.
Điểm cột tính như phương pháp: max |z| của 20 bin sau mốc theo mean, std (std tổng thể; std = 0 thì scale = 1) của 20 bin trước mốc.
Không gọi phương pháp. Nhãn root chỉ nối ở cuối. Không lưu dòng log; chỉ lưu mẫu của Drain (đã che tham số), cắt 160 ký tự.
Dùng: python torai_log_remaining_v1.py <thư mục lượt mới> [opaque_id]
"""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

HOME = Path.home()
T031 = HOME / "rca/T-031"
BASE = HOME / "rca/T-032"
RUN = BASE / "runs/torai-core-obs-001"
LABELS = BASE / "repo/results/T-028/runs/phan-hoi-review-001/ca-sai.json"
BIN, N_BIN = 15, 40
sys.path.insert(0, str(T031 / "repo/src"))


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def build(logs, t):
    """Chép logic của p3.torai_b.dung_logts (sim_th=0.4, depth=4) và giữ thêm mẫu của từng cột."""
    from drain3 import TemplateMiner
    from drain3.template_miner_config import TemplateMinerConfig

    def miner():
        c = TemplateMinerConfig()
        c.drain_sim_th = 0.4
        c.drain_depth = 4
        c.profiling_enabled = False
        return TemplateMiner(config=c)
    luoi = np.arange(t - 300, t - 300 + BIN * N_BIN, BIN)
    t0, t_end = int(luoi[0]), int(luoi[-1]) + BIN
    lg = logs[(logs["timestamp"] >= t0) & (logs["timestamp"] < t_end)].sort_values("timestamp", kind="stable")
    tms, map_id, dem, cot = {}, {}, 0, []
    for svc, msg in zip(lg["container_name"], lg["message"]):
        tm = tms.setdefault(svc, miner())
        cid = tm.add_log_message(str(msg))["cluster_id"]
        if (svc, cid) not in map_id:
            dem += 1
            map_id[(svc, cid)] = dem
        cot.append(f"{svc}_{map_id[(svc, cid)]}")
    lg = lg.assign(cot=cot, bin=t0 + ((lg["timestamp"] - t0) // BIN) * BIN)
    out = lg.groupby(["bin", "cot"]).size().unstack() if len(lg) else pd.DataFrame(index=luoi)
    out = out.reindex(index=luoi).fillna(0)
    templates = {}
    for (svc, cid), number in map_id.items():
        cluster = tms[svc].drain.id_to_cluster.get(cid)
        templates[f"{svc}_{number}"] = (cluster.get_template() if cluster is not None else "")[:160]
    return out, templates


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    only = sys.argv[2] if len(sys.argv) > 2 else None
    from p3 import cua_so
    labels = {r["opaque_id"]: r for r in read(LABELS)["main_rows"] if r["dataset"] == "RE2-TT" and r["method"] == "torai_B"}
    cases = []
    for unit_dir in sorted((RUN / "units").glob("*-s0")):
        unit = read(unit_dir / "unit.json")
        opaque_id = unit["opaque_id"]
        if only and only != opaque_id:
            continue
        run_dir = RUN / unit["sham_run_dir"]
        job = read(run_dir / "chuan-bi/job.json")
        t = int(job["t"])
        saved = pd.read_csv(run_dir / "bang/logts.csv")
        item = {"opaque_id": opaque_id}
        if "logs.parquet" not in job["files"]:
            item["status"] = "NO_LOG_FILE"
            cases.append(item)
            continue
        logs = cua_so.cat_log(pd.read_parquet(job["files"]["logs.parquet"]["path"]), t)
        table, templates = build(logs, t)                      # chưa dùng nhãn
        cols = [c for c in saved.columns if c != "time"]
        same_columns = set(cols) == set(table.columns)
        same_cells = same_columns and bool(np.array_equal(saved[cols].to_numpy(dtype="float64"), table[cols].to_numpy(dtype="float64")))
        item.update(status="OK" if same_cells else "REBUILD_DIFFERS", n_columns=len(cols), rebuild_equals_saved=same_cells)
        if not same_cells:
            cases.append(item)
            continue
        x = table[cols].to_numpy(dtype="float64")
        before, after = x[:20], x[20:]
        mean, std = before.mean(axis=0), before.std(axis=0)
        constant = std == 0
        z = np.abs((after - mean) / np.where(constant, 1.0, std)).max(axis=0)
        signed_after = after.mean(axis=0) - mean
        service = np.array([c.rsplit("_", 1)[0] for c in cols])

        def by_service(mask):
            total = z[mask].sum()
            best = {}
            for i in np.flatnonzero(mask):
                if service[i] not in best or z[i] > z[best[service[i]]]:
                    best[service[i]] = i
            ranked = sorted(best.items(), key=lambda kv: -z[kv[1]])
            return total, ranked
        total_all, ranked_all = by_service(np.ones(len(cols), dtype=bool))
        total_kept, ranked_kept = by_service(~constant)
        label = labels[opaque_id]
        root = label["root"]
        top3 = []
        for svc, i in ranked_kept[:3]:
            first, second = before[:10, i].mean(), before[10:, i].mean()
            top3.append({"service": svc, "column": cols[i], "template": templates.get(cols[i], ""), "share_of_kept_log_score": float(z[i] / total_kept) if total_kept else None,
                         "z": float(z[i]), "baseline_mean": float(mean[i]), "baseline_std": float(std[i]), "baseline_cv": float(std[i] / mean[i]) if mean[i] else None,
                         "baseline_first_half_mean": float(first), "baseline_second_half_mean": float(second),
                         "after_mean": float(after[:, i].mean()), "after_max": float(after[:, i].max()), "after_min": float(after[:, i].min()),
                         "direction": "tăng" if signed_after[i] > 0 else "giảm" if signed_after[i] < 0 else "bằng",
                         "baseline_nonzero_bins": int((before[:, i] > 0).sum()), "after_nonzero_bins": int((after[:, i] > 0).sum())})
        order_kept = [svc for svc, _i in ranked_kept]
        order_all = [svc for svc, _i in ranked_all]
        item.update(root=root, fault=label["fault"], cell=label["cell"], n_constant_baseline_columns=int(constant.sum()), n_kept_columns=int((~constant).sum()),
                    top_service_all_columns=order_all[0] if order_all else None, top_service_kept_columns=order_kept[0] if order_kept else None,
                    top3_services_kept=order_kept[:3], root_rank_by_log_kept=(order_kept.index(root) + 1) if root in order_kept else None,
                    root_rank_by_log_all=(order_all.index(root) + 1) if root in order_all else None, top3_kept=top3)
        cases.append(item)
        print(opaque_id, item["status"], item.get("top_service_kept_columns"), [(d["service"], d["direction"], round(d["z"], 1), d["baseline_nonzero_bins"]) for d in top3], flush=True)
    ok = [c for c in cases if c["status"] == "OK" and c.get("top3_kept")]
    tops = [d for c in ok for d in c["top3_kept"][:1]]
    all3 = [d for c in ok for d in c["top3_kept"]]

    def describe(rows):
        return {"n": len(rows), "direction": dict(Counter(d["direction"] for d in rows)),
                "baseline_nonzero_bins_le_3": sum(d["baseline_nonzero_bins"] <= 3 for d in rows),
                "baseline_nonzero_bins_median": statistics.median(d["baseline_nonzero_bins"] for d in rows) if rows else None,
                "baseline_mean_median": statistics.median(d["baseline_mean"] for d in rows) if rows else None,
                "baseline_cv_median": statistics.median(d["baseline_cv"] for d in rows if d["baseline_cv"] is not None) if rows else None,
                "share_of_kept_log_score_median": statistics.median(d["share_of_kept_log_score"] for d in rows) if rows else None,
                "templates": dict(Counter(d["service"] + " | " + d["template"][:90] for d in rows).most_common(8))}
    summary = {"cases": len(cases), "status": dict(Counter(c["status"] for c in cases)), "rebuild_equals_saved": sum(bool(c.get("rebuild_equals_saved")) for c in cases),
               "top_service_all_columns": dict(Counter(c["top_service_all_columns"] for c in ok).most_common(6)),
               "top_service_kept_columns": dict(Counter(c["top_service_kept_columns"] for c in ok).most_common(6)),
               "top3_membership_kept": dict(Counter(s for c in ok for s in c["top3_services_kept"]).most_common(8)),
               "top_service_kept_is_root": sum(c["top_service_kept_columns"] == c["root"] for c in ok),
               "top_column_of_top_service": describe(tops),
               "top_columns_of_top3_services": describe(all3),
               "top_columns_order_other_and_seat": describe([d for d in all3 if d["service"] in ("ts-order-other-service", "ts-seat-service")]),
               "note": "direction: trung bình 20 bin sau mốc so với trung bình 20 bin trước mốc của chính cột. baseline_nonzero_bins: số bin trước mốc có ít nhất một dòng log thuộc mẫu."}
    (out / "summary.json").write_text(json.dumps({"schema": "T032-torai-log-remaining-v1", "run": "runs/torai-core-obs-001", "summary": summary, "cases": cases,
                                                 "methods_executed": []}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1)[:3500], flush=True)


if __name__ == "__main__":
    main()
