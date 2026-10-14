"""T-032 việc 6 (gói bổ sung): bản cho TORAI nguồn A (bảng của tác giả), tạo từ torai_log_placebo_v1.py bằng phép thay chuỗi.
Khác bản gốc: đọc lượt runs/torai-a-obs-001. Nhãn root, loại lỗi lấy từ dòng torai_B của T-028 (cùng ca).
Trường so hạng với T-028 ở bản này so với hạng của TORAI B, nên KHÔNG phải tự kiểm; tự kiểm của nguồn A là lượt phát lại
khớp 90 bản ghi đóng băng từng bit.

Nguyên văn mô tả của bản gốc:
T-032 TORAI B: phép thử giả cho nguồn log và kiểm nguồn trace_err. Chạy trên EC2, chỉ đọc. Chỉ seed 0.

Định nghĩa (viết trước khi chạy, sau khi đã thấy runs/torai-log-source-001):
  Phép thử giả: mốc giả t' = t - 150 s. Chỉ dùng 20 bin trước mốc thật của `bang/logts.csv` (10 bin trước t', 10 bin từ t' tới t);
  không có lỗi nào được tiêm trong khoảng này. Bỏ cột không đổi trên 20 bin đó (như drop_constant của phương pháp áp trên bảng
  của nó), chấm mỗi cột bằng max|z| của 10 bin sau t' theo mean, std của 10 bin trước t' (std = 0 thì scale = 1), chia cho tổng,
  lên mức dịch vụ bằng cột cao nhất. So với bảng chính: dịch vụ đứng đầu theo log, tỷ lệ điểm nằm trên cột có nền không đổi.
  Dự đoán: nếu việc mẫu log "chỉ xuất hiện sau mốc" là đặc tính của log theo thời gian (không do lỗi) thì ở phép thử giả các
  dịch vụ đứng đầu và tỷ lệ điểm trên cột nền không đổi vẫn như bảng chính; nếu do lỗi thì chúng giảm rõ.
  trace_err: đếm số cột của `bang/tracets_err.csv`, số cột không đổi trên cả 40 bin, và tổng mọi ô.
Dùng: python torai_log_placebo_v1.py <thư mục lượt mới>
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
RUN = BASE / "runs/torai-a-obs-001"
MAIN = BASE / "runs/torai-log-source-a-001/summary.json"


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    main_cases = {c["opaque_id"]: c for c in read(MAIN)["cases"]}
    cases = []
    for unit_dir in sorted((RUN / "units").glob("*-s0")):
        unit = read(unit_dir / "unit.json")
        opaque_id = unit["opaque_id"]
        run_dir = RUN / unit["sham_run_dir"]
        t = read(run_dir / "ban-ghi-0.json")["window"]["t"]
        logts = pd.read_csv(run_dir / "bang/logts.csv")
        pre = logts[logts["time"] < t]
        fake = t - 150
        normal, anomal = pre[pre["time"] < fake], pre[pre["time"] >= fake]
        columns = [c for c in pre.columns if c != "time" and pre[c].nunique() > 1]
        raw, zero = {}, {}
        for column in columns:
            n, a = normal[column].to_numpy(dtype=float), anomal[column].to_numpy(dtype=float)
            mean, std = float(n.mean()), float(n.std())
            raw[column] = float(np.max(np.abs((a - mean) / (std if std > 0 else 1.0))))
            zero[column] = std == 0.0
        total = sum(raw.values())
        share = {c: v / total for c, v in raw.items()} if total else {}
        best = {}
        for column, score in sorted(share.items(), key=lambda x: -x[1]):
            best.setdefault(column.split("_")[0], column)
        order = sorted(best, key=lambda s: -share[best[s]])
        err = pd.read_csv(run_dir / "bang/tracets_err.csv")
        err_columns = [c for c in err.columns if c != "time"]
        item = {"opaque_id": opaque_id, "bins_before_fake": int(len(normal)), "bins_after_fake": int(len(anomal)),
                "n_columns_scored": len(columns), "top_service_by_log": order[0] if order else None, "top3_services_by_log": order[:3],
                "top_service_top_column_std_zero": bool(zero[best[order[0]]]) if order else None,
                "log_mass_on_std_zero_columns": sum(share[c] for c in share if zero[c]),
                "share_columns_std_zero": (sum(zero.values()) / len(columns)) if columns else None,
                "main_top_service_by_log": main_cases[opaque_id]["top_service_by_log"],
                "main_log_mass_on_std_zero_columns": main_cases[opaque_id]["log_mass_on_std_N_zero_columns"],
                "trace_err": {"n_columns": len(err_columns), "n_constant_columns": int(sum(err[c].nunique() <= 1 for c in err_columns)),
                              "sum_all_cells": float(err[err_columns].to_numpy(dtype=float).sum()) if err_columns else 0.0,
                              "n_bins": int(len(err))}}
        cases.append(item)
        print(opaque_id, item["top_service_by_log"], round(item["log_mass_on_std_zero_columns"], 3), item["trace_err"], flush=True)
    scored = [c for c in cases if c["n_columns_scored"]]

    def q(values):
        values = sorted(v for v in values if v is not None)
        return {"n": len(values), "min": values[0], "median": statistics.median(values), "max": values[-1]} if values else {"n": 0}

    summary = {"n_cases": len(cases), "cases_with_scored_columns": len(scored),
               "placebo_top_service_by_log": dict(Counter(c["top_service_by_log"] for c in scored).most_common()),
               "placebo_top3_membership": dict(Counter(s for c in scored for s in c["top3_services_by_log"]).most_common(8)),
               "placebo_top_service_equals_main_top_service": sum(c["top_service_by_log"] == c["main_top_service_by_log"] for c in scored),
               "placebo_top_service_top_column_std_zero": sum(bool(c["top_service_top_column_std_zero"]) for c in scored),
               "placebo_log_mass_on_std_zero_columns": q([c["log_mass_on_std_zero_columns"] for c in scored]),
               "main_log_mass_on_std_zero_columns": q([c["main_log_mass_on_std_zero_columns"] for c in scored]),
               "placebo_share_columns_std_zero": q([c["share_columns_std_zero"] for c in scored]),
               "trace_err": {"cases_with_zero_columns": sum(c["trace_err"]["n_columns"] == 0 for c in cases),
                             "cases_all_columns_constant": sum(c["trace_err"]["n_columns"] == c["trace_err"]["n_constant_columns"] for c in cases),
                             "cases_sum_all_cells_zero": sum(c["trace_err"]["sum_all_cells"] == 0 for c in cases),
                             "n_columns": q([c["trace_err"]["n_columns"] for c in cases])},
               "note": "Phép thử giả dùng nền 10 bin (150 s) thay vì 20 bin; so về hướng, không so từng số với bảng chính."}
    result = {"schema": "T032-TORAI-A-log-placebo-v1", "methods_executed": False, "main_sha256": hashlib.sha256(MAIN.read_bytes()).hexdigest(),
              "this_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "summary": summary, "cases": cases}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
