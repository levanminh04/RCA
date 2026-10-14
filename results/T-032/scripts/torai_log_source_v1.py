"""T-032 TORAI B: nguồn log tạo điểm như thế nào (bổ sung cho torai_severity_table_v3.py). Chạy trên EC2, chỉ đọc.

Dùng bảng `bang/logts.csv` mà lượt sham của torai-core-obs-001 đã tạo (lượt sham khớp bản đóng băng từng bit) và trung gian
`log_ranks` của nhánh quan sát. Không gọi phương pháp. Chỉ seed 0 (trung gian trước RCD giống nhau giữa ba seed).
Công thức của phương pháp cho một cột log: max |z| của các bin sau mốc theo mean, std của các bin trước mốc
(StandardScaler: std = 0 thì scale = 1, tức z = số đếm trừ mean), rồi chia cho tổng điểm mọi cột log.
Tự kiểm: điểm chuẩn hóa tính lại từ logts.csv phải trùng `log_ranks` (sai khác tương đối <= 1e-9) cho mọi cột.
Với mọi cột (chưa dùng nhãn): nền có std = 0 hay không, nền toàn 0 hay không. Nối nhãn sau cùng.
Dùng: python torai_log_source_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
RUN = BASE / "runs/torai-core-obs-001"
TABLE = BASE / "runs/torai-severity-table-003/summary.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    table = {(u["opaque_id"], u["seed"]): u for u in read(TABLE)["units"]}
    cases = []
    for unit_dir in sorted((RUN / "units").glob("*-s0")):
        unit = read(unit_dir / "unit.json")
        opaque_id = unit["opaque_id"]
        loc = read(unit_dir / "obs/locals.json")["locals"]
        record = read(RUN / unit["sham_run_dir"] / "ban-ghi-0.json")
        t = record["window"]["t"]
        logts = pd.read_csv(RUN / unit["sham_run_dir"] / "bang/logts.csv")
        ranks = {c: float(v) for c, v in loc["log_ranks"]}
        normal, anomal = logts[logts["time"] < t], logts[logts["time"] >= t]
        raw, flags = {}, {}
        for column in ranks:
            n, a = normal[column].to_numpy(dtype=float), anomal[column].to_numpy(dtype=float)
            mean, std = float(n.mean()), float(n.std())
            scale = std if std > 0 else 1.0
            raw[column] = float(np.max(np.abs((a - mean) / scale)))
            flags[column] = {"std_N_zero": std == 0.0, "all_zero_N": bool((n == 0).all()), "max_A": float(a.max()), "mean_N": mean, "std_N": std}
        total = sum(raw.values())
        rebuilt = {c: v / total for c, v in raw.items()} if total else {}
        worst = max((abs(rebuilt[c] - ranks[c]) / max(abs(ranks[c]), 1e-300) for c in ranks), default=0.0)
        mass_zero_std = sum(ranks[c] for c in ranks if flags[c]["std_N_zero"])
        # mức dịch vụ: cột cao nhất của mỗi dịch vụ (fine2coarse_highest), chưa dùng nhãn
        best = {}
        for column, score in sorted(ranks.items(), key=lambda x: -x[1]):
            service = column.split("_")[0]
            best.setdefault(service, column)
        service_rows = {s: {"top_column": c, "top_column_share": ranks[c], **flags[c]} for s, c in best.items()}
        order = sorted(best, key=lambda s: -ranks[best[s]])
        item = {"opaque_id": opaque_id, "n_log_columns_scored": len(ranks), "n_log_columns_in_table": int(logts.shape[1] - 1),
                "rebuild_max_relative_error": worst, "rebuild_ok": worst <= 1e-9,
                "columns_std_N_zero": sum(f["std_N_zero"] for f in flags.values()),
                "columns_all_zero_N": sum(f["all_zero_N"] for f in flags.values()),
                "log_mass_on_std_N_zero_columns": mass_zero_std,
                "top_service_by_log": order[0] if order else None,
                "top3_services_by_log": order[:3],
                "top_service_top_column_std_N_zero": service_rows[order[0]]["std_N_zero"] if order else None,
                "services_whose_top_column_has_std_N_zero": sum(r["std_N_zero"] for r in service_rows.values()),
                "n_services_with_log_score": len(service_rows)}
        # --- nối nhãn ---
        t_unit = table[(opaque_id, 0)]
        root = t_unit["root"]
        item.update({"root": root, "cell": t_unit["cell"], "root_rank_max": t_unit["root_rank_max"],
                     "root_log": service_rows.get(root), "above_root_log": [
                         {"entity": a["entity"], **(service_rows.get(a["entity"]) or {"top_column": None})} for a in t_unit["above_root"]]})
        cases.append(item)
        print(opaque_id, item["rebuild_ok"], item["top_service_by_log"], item["top_service_top_column_std_N_zero"], flush=True)
    scored = [c for c in cases if c["n_log_columns_scored"]]
    wrong = [c for c in cases if c["root_rank_max"] > 1]

    def q(values):
        values = sorted(values)
        return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]} if values else {"n": 0}

    summary = {"n_cases": len(cases), "cases_with_log_columns": len(scored), "rebuild_ok": sum(c["rebuild_ok"] for c in scored),
               "top_service_by_log": dict(Counter(c["top_service_by_log"] for c in scored).most_common()),
               "top3_membership": dict(Counter(s for c in scored for s in c["top3_services_by_log"]).most_common()),
               "top_service_is_root": sum(c["top_service_by_log"] == c["root"] for c in scored),
               "top_service_top_column_std_N_zero": sum(bool(c["top_service_top_column_std_N_zero"]) for c in scored),
               "log_mass_on_std_N_zero_columns": q([c["log_mass_on_std_N_zero_columns"] for c in scored]),
               "share_of_scored_columns_with_std_N_zero": q([c["columns_std_N_zero"] / c["n_log_columns_scored"] for c in scored]),
               "share_of_scored_columns_all_zero_N": q([c["columns_all_zero_N"] / c["n_log_columns_scored"] for c in scored]),
               "wrong_cases": {"n": len(wrong), "pairs_above_root": sum(len(c["above_root_log"]) for c in wrong),
                               "pairs_where_entity_top_log_column_has_std_N_zero": sum(bool(a.get("std_N_zero")) for c in wrong for a in c["above_root_log"]),
                               "root_top_log_column_has_std_N_zero": sum(bool((c["root_log"] or {}).get("std_N_zero")) for c in wrong)},
               "right_cases": {"n": len(cases) - len(wrong),
                               "root_top_log_column_has_std_N_zero": sum(bool((c["root_log"] or {}).get("std_N_zero")) for c in cases if c["root_rank_max"] == 1)},
               "note": "std_N_zero: cột log không đổi ở 20 bin trước mốc (thường toàn 0), nên z của nó là số đếm thô trừ mean. "
                       "Mô tả trên 30 ca dev RE2-TT, seed 0."}
    result = {"schema": "T032-TORAI-log-source-v1", "run": "runs/torai-core-obs-001", "methods_executed": False,
              "table_sha256": sha(TABLE), "this_script_sha256": sha(__file__), "summary": summary, "cases": cases}

    def plain(value):
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            return float(value)
        if isinstance(value, np.bool_):
            return bool(value)
        raise TypeError(type(value).__name__)

    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1, default=plain) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1, default=plain))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
