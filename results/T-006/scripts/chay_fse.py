r"""T-006 L4 ④ (loại B): chạy `baro`, `nsigma`, `circa` của RCAEval khi biết mốc tiêm, trên dữ liệu bài BARO (fse-ob, fse-ss).

`main.py` của RCAEval không nhận dataset fse-* (không có trong `choices`), nên script này dựng lại đúng `process()` của
`main.py` (RCAEval 259ea41, dòng 216-372), chỉ khác ba chỗ, đều ghi lý do:
1. Đầu vào là `simple_data.csv` (định dạng giống `data.csv` của RE1; là file code BARO dùng). `main.py` sẽ chọn
   `data.csv` thô 416-439 cột nếu chạy trên thư mục fse (xem LOG bước 0.4).
2. `sli=None` thay cho SLI suy từ tên service gốc. Bước 0.2 đã kiểm ba hàm này không đọc `sli`, nên kết quả không đổi;
   làm vậy để không có đường nhãn nào vào phương pháp (luật cứng 6).
3. `dataset=<fse-ob|fse-ss>`: `preprocess` chỉ phân nhánh theo `dataset is None` và `"causalrca-sock-shop"`.
Giữ nguyên: bỏ cột `time.1`, bỏ `_latency-50`, thay inf, ffill, fillna(0), cắt `--length` (mặc định 20, tức 600 + 600
dòng; mỗi ca fse chỉ có 360 + 360 nên là cả ca), đổi `_latency-90` -> `_latency`, các tham số gọi hàm, thứ tự ca sắp xếp.
Kết quả ghi như `main.py`: output/results/<service>_<lỗi>_<lần>.json = {"0": ranks}. Tên service, lỗi lấy từ đường dẫn
chỉ để đặt tên file (dùng khi chấm), không vào phương pháp.
Cách dùng (trong thư mục làm việc có data/<dataset>): python chay_fse.py --method baro --dataset fse-ob [--length 20]
"""
import argparse
import glob
import json
import os
import warnings
from os.path import basename, dirname, join

warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from tqdm import tqdm

import RCAEval.e2e as e2e

ap = argparse.ArgumentParser()
ap.add_argument("--method", choices=["baro", "nsigma", "circa"], required=True)
ap.add_argument("--dataset", choices=["fse-ob", "fse-ss"], required=True)
ap.add_argument("--length", type=int, default=20)
args = ap.parse_args()

func = getattr(e2e, args.method)
result_path = join("output", "results")
os.makedirs(result_path, exist_ok=True)
data_paths = sorted(glob.glob(join("data", args.dataset, "**", "simple_data.csv"), recursive=True))

for data_path in tqdm(data_paths):
    data_dir = dirname(data_path)
    service, metric = basename(dirname(dirname(data_path))).split("_")
    case = basename(dirname(data_path))
    rp = join(result_path, f"{service}_{metric}_{case}.json")

    data = pd.read_csv(data_path)
    if "time.1" in data:
        data = data.drop(columns=["time.1"])
    data = data.loc[:, ~data.columns.str.endswith("_latency-50")]
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.ffill()
    data = data.fillna(0)
    with open(join(data_dir, "inject_time.txt")) as f:
        inject_time = int(f.readlines()[0].strip())
    normal_df = data[data["time"] < inject_time].tail(args.length * 60 // 2)
    anomal_df = data[data["time"] >= inject_time].head(args.length * 60 // 2)
    data = pd.concat([normal_df, anomal_df], ignore_index=True)
    num_node = len(data.columns) - 1
    data = data.rename(columns={c: c.replace("_latency-90", "_latency") for c in data.columns if c.endswith("_latency-90")})

    out = func(data, inject_time, dataset=args.dataset, anomalies=None, dk_select_useful=False, sli=None,
               verbose=False, n_iter=num_node, args=None)
    with open(rp, "w") as f:
        json.dump({0: out.get("ranks")}, f)
