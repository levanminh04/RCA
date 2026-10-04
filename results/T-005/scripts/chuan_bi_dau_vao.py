"""T-005: chuẩn bị đầu vào cho lượt đo. Chạy bằng môi trường py312.

Ghi ra D:/RCA-ext/work/T-005/ (ngoài repo, vì là dữ liệu ca). Không in giá trị dữ liệu, chỉ in kích thước.

Cách cắt cửa sổ chép theo RCAEval main.py (revision 259ea41), dòng 300-337 và 366-388:
- bỏ cột `_latency-50`; thay inf bằng NaN; ffill; fillna(0);
- cửa sổ "win" = cấu hình --length 10 (lệnh trong docs/TORAI.md; mặc định của main.py là --length 20):
  300 dòng trước mốc + 300 dòng sau mốc (metric),
  20 dòng trước + 20 dòng sau (logts, tracets);
- đổi `_latency-90` thành `_latency`.
"full" = toàn ca, cùng các bước làm sạch, không cắt.
Cửa sổ trace (span có startTime trong 300 s trước/sau mốc) KHÔNG chép từ main.py: main.py không có
nhánh đọc trace; đây là lựa chọn của người làm, cùng độ dài với cửa sổ metric.

Mốc tiêm chỉ dùng để cắt cửa sổ và lấy đoạn bình thường cho GDN (SPEC T-005, mục Đầu vào).
"""
import json
import os

import numpy as np
import pandas as pd

REPO = r"D:\RCA-flashticket"
CASE = "re2tt_ts-route-service_socket_1"
GDN_TRAIN = [
    "re2tt_ts-order-service_loss_1",
    "re2tt_ts-travel-service_loss_2",
    "re2tt_ts-auth-service_cpu_1",
    "re2tt_ts-auth-service_delay_1",
    "re2tt_ts-order-service_disk_1",
]
DATA = os.path.join(REPO, "data", "rcaeval")
INJ = r"D:\RCA-ext\dl\rcaeval-inject"
TORAI = r"D:\RCA-ext\data\torai-TT\ts-route-service_socket\1"
WORK = r"D:\RCA-ext\work\T-005"
INP = os.path.join(WORK, "inputs")
GDN_DIR = os.path.join(WORK, "gdn", "data", "re2tt5")

LENGTH = 10                    # phút, như docs/TORAI.md (mặc định của main.py là 20)
HALF = LENGTH * 60 // 2        # 300 dòng metric mỗi phía
LOG_HALF = LENGTH * 4 // 2     # 20 dòng logts/tracets mỗi phía


def read_inject(case):
    with open(os.path.join(INJ, case, "inject_time.txt")) as f:
        return int(f.readlines()[0].strip())


def clean_metrics(df, ts_only=False):
    if "time.1" in df:
        df = df.drop(columns=["time.1"])
    df = df.loc[:, ~df.columns.str.endswith("_latency-50")]
    if ts_only:  # nhánh "torai-TT" của main.py
        time_col = df["time"]
        df = df.loc[:, df.columns.str.startswith("ts-")]
        df["time"] = time_col
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.ffill()
    df = df.fillna(0)
    return df


def window(df, inject, half):
    a = df[df["time"] < inject].tail(half)
    b = df[df["time"] >= inject].head(half)
    return pd.concat([a, b], ignore_index=True)


def rename_lat(df):
    return df.rename(columns={c: c.replace("_latency-90", "_latency") for c in df.columns if c.endswith("_latency-90")})


def main():
    os.makedirs(INP, exist_ok=True)
    os.makedirs(GDN_DIR, exist_ok=True)
    meta = {}
    inj = read_inject(CASE)

    # == metric từ parquet RCAEval: BARO, N-Sigma, CIRCA-PC, RCD ==
    raw = pd.read_parquet(os.path.join(DATA, CASE, "metrics.parquet"))
    meta["metrics_raw"] = list(raw.shape)
    raw.to_csv(os.path.join(INP, "metrics_raw_full.csv"), index=False)  # cho bộ phát hiện
    m = clean_metrics(raw)
    for name, df in [("win", window(m, inj, HALF)), ("full", m)]:
        df = rename_lat(df)
        df.to_csv(os.path.join(INP, f"metrics_{name}.csv"), index=False)
        meta[f"metrics_{name}"] = list(df.shape)

    # == trace: MicroRank, TraceRCA. startTime và duration tính bằng micro giây ==
    cols = ["traceID", "spanID", "parentSpanID", "serviceName", "methodName",
            "operationName", "startTime", "duration"]
    tr = pd.read_parquet(os.path.join(DATA, CASE, "traces.parquet"), columns=cols)
    inj_us = inj * 1_000_000
    tw = tr[(tr["startTime"] >= inj_us - HALF * 1_000_000) & (tr["startTime"] < inj_us + HALF * 1_000_000)]
    for name, df in [("win", tw), ("full", tr)]:
        df.reset_index(drop=True).to_parquet(os.path.join(INP, f"traces_{name}.parquet"), index=False)
        meta[f"traces_{name}"] = list(df.shape)

    # == TORAI: chuỗi đã xử lý trong zip Figshare ==
    with open(os.path.join(TORAI, "inject_time.txt")) as f:
        inj_t = int(f.readlines()[0].strip())
    assert inj_t == inj, "mốc tiêm TORAI khác mốc RCAEval"
    tm = clean_metrics(pd.read_csv(os.path.join(TORAI, "simple_metrics.csv")), ts_only=True)
    others = {k: pd.read_csv(os.path.join(TORAI, f"{k}.csv")) for k in ["logts", "tracets_err", "tracets_lat"]}
    for name in ["win", "full"]:
        df = window(tm, inj, HALF) if name == "win" else tm
        df = rename_lat(df)
        df.to_csv(os.path.join(INP, f"torai_metric_{name}.csv"), index=False)
        meta[f"torai_metric_{name}"] = list(df.shape)
        for k, v in others.items():
            o = window(v, inj, LOG_HALF) if name == "win" else v
            o.to_csv(os.path.join(INP, f"torai_{k}_{name}.csv"), index=False)
            meta[f"torai_{k}_{name}"] = list(o.shape)

    # == GDN: học trên đoạn trước mốc của 5 ca, suy luận trên toàn ca đo ==
    # Chuẩn hóa min-max học trên tập học, như GDN/scripts/process_swat.py (hàm norm).
    trains = []
    for c in GDN_TRAIN:
        d = rename_lat(clean_metrics(pd.read_parquet(os.path.join(DATA, c, "metrics.parquet"))))
        trains.append(d[d["time"] < read_inject(c)])
    test = rename_lat(m)
    feats = [c for c in test.columns if c != "time" and all(c in t.columns for t in trains)]
    train = pd.concat([t[feats] for t in trains], ignore_index=True)
    test_x = test[feats].reset_index(drop=True)
    lo, hi = train.min(), train.max()
    rng = (hi - lo).replace(0, 1)
    train = (train - lo) / rng
    test_x = (test_x - lo) / rng
    test_x["attack"] = 0  # code GDN bắt buộc có cột này; không phải nhãn, không tính F1
    train.to_csv(os.path.join(GDN_DIR, "train.csv"))
    test_x.to_csv(os.path.join(GDN_DIR, "test.csv"))
    with open(os.path.join(GDN_DIR, "list.txt"), "w") as f:
        f.write("\n".join(feats) + "\n")
    meta["gdn_train"] = list(train.shape)
    meta["gdn_train_rows_per_case"] = [len(t) for t in trains]
    meta["gdn_test"] = list(test_x.shape)
    meta["gdn_features"] = len(feats)

    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
