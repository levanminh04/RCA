"""T-018 B9: Retrieval@K của một bộ chọn NGẪU NHIÊN, mức service, trên RE1-OB và RE1-SS (không chạy phương pháp RCA).

Mục đích: đọc đúng con số "Retrieval@15 = 0,98–1,00 trên microservice" của DecompRCA (Bảng 1). Ở RCAEval, DecompRCA
lấy K metric rồi quy về service (`method/runners/compute_retrieval_recall_cumulative.py:56-74`): trúng nếu BẤT KỲ metric
nào của service gốc nằm trong K metric. Script tính xác suất trúng khi chọn K metric ngẫu nhiên đều:
    P = 1 − C(p − m, K) / C(p, K),  p = số metric của ca, m = số metric thuộc service gốc,
rồi lấy trung bình qua các ca. Đồng thời tính theo định nghĩa của RCAEval `Evaluator.retrieval_service` (K là số SERVICE
trong thứ hạng mức service): bộ ngẫu nhiên trúng với xác suất min(1, K / số service).

Tiền xử lý theo loader của DecompRCA (`method/datasets/rcaeval_dataset.py:45-74, 200-232`): ưu tiên simple_data.csv,
rồi data.csv; cửa sổ 600 dòng trước và 600 dòng từ mốc tiêm; bỏ cột time; bỏ cột hằng trong TỪNG cửa sổ; giữ giao hai
cửa sổ. Service của metric: phần trước dấu '_' đầu tiên, bỏ hậu tố '-db' (`compute_retrieval_recall_cumulative.py:56-57`).
Nhãn (tên thư mục ca) chỉ dùng để biết service gốc khi tính xác suất; không có phương pháp nào nhận nhãn.

Chạy: D:/RCA-ext/envs/py312/Scripts/python.exe retrieval_ngau_nhien.py
"""
import json
import math
import os

import numpy as np
import pandas as pd

ROOT = r"D:\RCA-ext\data"
OUT = r"D:\RCA-flashticket\results\T-018\runs\b9-retrieval-ngau-nhien.json"


def svc(m):
    return m.split("_")[0].replace("-db", "")


def tien_xu_ly(df):
    df = df.drop(columns=[c for c in ("time", "Time", "time.1") if c in df.columns])
    df = df.loc[:, (df != df.iloc[0]).any()]
    return df


def main():
    kq = {}
    for suite in ["RE1-OB", "RE1-SS"]:
        rows = []
        hop, so_cot_tho = set(), []
        for fd in sorted(os.listdir(os.path.join(ROOT, suite))):
            service, fault = fd.rsplit("_", 1)
            for inst in sorted(os.listdir(os.path.join(ROOT, suite, fd))):
                d = os.path.join(ROOT, suite, fd, inst)
                f = next((os.path.join(d, c) for c in ("simple_data.csv", "simple_metrics.csv", "data.csv")
                          if os.path.exists(os.path.join(d, c))), None)
                if f is None:
                    continue
                inj = int(open(os.path.join(d, "inject_time.txt")).read().strip())
                df = pd.read_csv(f)
                cot_tho = [c for c in df.columns if c not in ("time", "Time", "time.1")]
                hop |= set(cot_tho)
                so_cot_tho.append(len(cot_tho))
                pre = tien_xu_ly(df[df["time"] < inj].tail(600))
                post = tien_xu_ly(df[df["time"] >= inj].head(600))
                cols = [c for c in pre.columns if c in post.columns]
                p = len(cols)
                m = sum(1 for c in cols if svc(c) == service)
                n_svc = len({svc(c) for c in cols})
                row = {"ca": f"{fd}/{inst}", "p": p, "m": m, "n_service": n_svc}
                for K in (5, 10, 15):
                    # math.comb(n, k) = 0 khi k > n, nên công thức đúng cả khi p − m < K
                    row[f"P_metric_K{K}"] = (1 - math.comb(p - m, K) / math.comb(p, K)) if p >= K else float(m > 0)
                    row[f"P_service_K{K}"] = min(1.0, K / n_svc) if m > 0 else 0.0
                rows.append(row)
        df = pd.DataFrame(rows)
        kq[suite] = {"so_ca": len(df), "p_trung_vi": float(df.p.median()), "m_trung_vi": float(df.m.median()),
                     "so_service_trung_vi": float(df.n_service.median()),
                     "so_ca_service_goc_khong_con_metric": int((df.m == 0).sum()),
                     "so_cot_tho_moi_ca_min_max": [min(so_cot_tho), max(so_cot_tho)], "hop_cot_tho_cac_ca": len(hop)}
        for K in (5, 10, 15):
            kq[suite][f"ngau_nhien_K{K}_metric_quy_service"] = round(float(df[f"P_metric_K{K}"].mean()), 3)
            kq[suite][f"ngau_nhien_K{K}_theo_service"] = round(float(df[f"P_service_K{K}"].mean()), 3)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(kq, fh, ensure_ascii=False, indent=1)
    print(json.dumps(kq, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
