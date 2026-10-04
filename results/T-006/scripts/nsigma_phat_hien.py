r"""T-006 L4 ⑤ (loại B): N-Sigma phát hiện bất thường trên fse-ob, fse-ss; mốc Bảng 2 bài BARO (Precision, Recall, F1).

Bộ phát hiện: `baro.anomaly_detection.nsigma(data, k=3, startsfrom=100)` (repo BARO e35f4ec, mặc định của hàm).
Chuẩn bị dữ liệu và cách chấm chép từ `baro.reproducibility.reproduce_bocpd`:
  chọn cột chứa "latency-50" hoặc "_error" (bỏ queue-master, rabbitmq_); drop_constant; ffill; fillna(0); min-max;
  TP nếu có ít nhất một điểm phát hiện, FN nếu không; FP nếu điểm phát hiện đầu tiên nằm trước mốc tiêm, TN nếu không.
`nsigma` cần cột `time`; ở đây `time` = chỉ số dòng 0..n-1, để điểm phát hiện là chỉ số dòng như đầu ra BOCPD.
Hai biến thể cửa sổ (bài không ghi cửa sổ dùng cho N-Sigma):
  w300: 300 dòng trước + 300 dòng sau mốc tiêm, đúng như reproduce_bocpd; mốc tiêm ở chỉ số 300.
  full: cả ca (fse: 360 + 361 dòng); mốc tiêm ở chỉ số = số dòng trước mốc tiêm.
So thêm với `nsigma.json` tác giả lưu trong từng ca: điểm đầu tiên có trùng không, cả danh sách có trùng không.
Mốc tiêm dùng để cắt cửa sổ và để chấm. Đây là cách chạy tái lập, không phải chế độ tự phát hiện của P3 (luật cứng 6).
Cách dùng (thư mục làm việc có data/<dataset>): python nsigma_phat_hien.py --dataset fse-ob
"""
import argparse
import glob
import json
import os
import sys
import time
from os.path import basename, dirname, join

import numpy as np
import pandas as pd

sys.path.insert(0, r"D:\RCA-ext\src\baro")
from baro.anomaly_detection import nsigma  # noqa: E402
from baro.utility import drop_constant  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--dataset", choices=["fse-ob", "fse-ss"], required=True)
args = ap.parse_args()

os.makedirs(join("output", "results"), exist_ok=True)
paths = sorted(glob.glob(join("data", args.dataset, "**", "simple_data.csv"), recursive=True))
tong = {}
for bien_the in ("w300", "full"):
    tong[bien_the] = {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "trung_diem_dau_nsigma_json": 0, "trung_ca_danh_sach": 0, "n": 0}
for p in paths:
    d = dirname(p)
    ca = f"{basename(dirname(d))}_{basename(d)}"
    raw = pd.read_csv(p)
    with open(join(d, "inject_time.txt")) as f:
        inject_time = int(f.readlines()[0].strip())
    saved = json.load(open(join(d, "nsigma.json")))
    for bien_the in ("w300", "full"):
        t0 = time.time()
        if bien_the == "w300":
            normal_df = raw[raw["time"] < inject_time].tail(300)
            anomal_df = raw[raw["time"] >= inject_time].head(300)
        else:
            normal_df = raw[raw["time"] < inject_time]
            anomal_df = raw[raw["time"] >= inject_time]
        inject_idx = len(normal_df)
        data = pd.concat([normal_df, anomal_df], ignore_index=True)
        cols = [c for c in data.columns if not ("queue-master" in c or "rabbitmq_" in c) and ("latency-50" in c or "_error" in c)]
        data = data[cols]
        data = drop_constant(data)
        data = data.ffill().fillna(0)
        for c in data.columns:
            data[c] = (data[c] - np.min(data[c])) / (np.max(data[c]) - np.min(data[c]))
        data = data.ffill().fillna(0)
        data.insert(0, "time", np.arange(len(data)))
        anomalies = sorted(set(int(x) for x in nsigma(data, k=3, startsfrom=100)))
        first = anomalies[0] if anomalies else None
        t = tong[bien_the]
        t["n"] += 1
        t["tp" if anomalies else "fn"] += 1
        t["fp" if (first is not None and first < inject_idx) else "tn"] += 1
        t["trung_diem_dau_nsigma_json"] += bool(saved) and first == saved[0]
        t["trung_ca_danh_sach"] += anomalies == saved
        rec = {"ca": ca, "bien_the": bien_the, "inject_idx": inject_idx, "so_cot": len(cols), "so_diem": len(anomalies),
               "diem_dau": first, "nsigma_json_diem_dau": saved[0] if saved else None, "giay": round(time.time() - t0, 2)}
        with open(join("output", "results", f"{ca}_{bien_the}.json"), "w") as f:
            json.dump({**rec, "anomalies": anomalies}, f)
        print(json.dumps(rec, ensure_ascii=False), flush=True)

for bien_the, t in tong.items():
    P = t["tp"] / (t["tp"] + t["fp"]) if t["tp"] + t["fp"] else float("nan")
    R = t["tp"] / (t["tp"] + t["fn"]) if t["tp"] + t["fn"] else float("nan")
    F = 2 * P * R / (P + R) if P + R else float("nan")
    t.update({"precision": round(P, 4), "recall": round(R, 4), "f1": round(F, 4)})
    print(f"TONG {args.dataset} {bien_the}: P={P:.2f} R={R:.2f} F1={F:.2f} {json.dumps(t)}")
json.dump(tong, open(join("output", "tong.json"), "w"), indent=1)
