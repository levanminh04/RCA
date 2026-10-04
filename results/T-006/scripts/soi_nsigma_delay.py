r"""T-006 phiên 2: soi vì sao `nsigma` (RCAEval) lệch ở DELAY so với Bảng 3 bài BARO (fse-ob 0,68 so với 0,94).

Chẩn đoán, không phải kết quả chính thức: kết quả chính thức vẫn là khối l4-nsigma-fse-*.
Dựng lại đúng tiền xử lý của chay_fse.py (= main.py) và phần chấm điểm của `nsigma` (StandardScaler trên đoạn trước
mốc tiêm, điểm = max z ở đoạn sau). Với mỗi ca delay, in: kênh đứng đầu, điểm z và độ lệch chuẩn đoạn trước của nó;
kênh tốt nhất của service gốc và hạng service gốc. Nhãn (service gốc) chỉ dùng để phân tích sau khi đã có thứ hạng.
Cũng tính lại Avg@5 cho các biến thể chẩn đoán (mỗi biến thể là một giả thuyết về chỗ bài làm khác):
  goc        : đúng như RCAEval nsigma (để kiểm script này tái tạo khối chính thức)
  rs         : RobustScaler thay StandardScaler (= RCAEval baro), để so cùng tiền xử lý
  abs        : điểm = max |z| thay vì max z
  bo_hang_so_gan : bỏ cột gần hằng số trong đoạn trước (độ lệch chuẩn < 1e-6 * (1 + |trung bình|)), giữ StandardScaler
  lat50      : giữ cột _latency-50 thay cho _latency-90
Cách dùng: <python py312-pin> soi_nsigma_delay.py fse-ob|fse-ss
"""
import glob
import json
import sys
from os.path import basename, dirname, join

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler

from RCAEval.benchmark.evaluation import Evaluator
from RCAEval.classes.graph import Node
from RCAEval.io.time_series import preprocess

ds = sys.argv[1]
root = join(r"D:\RCA-ext\data", ds)


def chuan_bi(p, lat50=False):
    d = pd.read_csv(p)
    if "time.1" in d:
        d = d.drop(columns=["time.1"])
    if lat50:
        d = d.loc[:, ~d.columns.str.endswith("_latency-90")]
        d = d.rename(columns={c: c.replace("_latency-50", "_latency") for c in d.columns if c.endswith("_latency-50")})
    else:
        d = d.loc[:, ~d.columns.str.endswith("_latency-50")]
    d = d.replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    it = int(open(join(dirname(p), "inject_time.txt")).readline().strip())
    d = pd.concat([d[d["time"] < it].tail(600), d[d["time"] >= it].head(600)], ignore_index=True)
    d = d.rename(columns={c: c.replace("_latency-90", "_latency") for c in d.columns if c.endswith("_latency-90")})
    return d, it


def diem(d, it, bien_the):
    n = preprocess(d[d["time"] < it], dataset=ds)
    a = preprocess(d[d["time"] >= it], dataset=ds)
    cols = [c for c in n.columns if c in a.columns]
    out = {}
    for c in cols:
        x, y = n[c].to_numpy(), a[c].to_numpy()
        if bien_the == "bo_hang_so_gan" and x.std() < 1e-6 * (1 + abs(x.mean())):
            continue
        sc = (RobustScaler() if bien_the == "rs" else StandardScaler()).fit(x.reshape(-1, 1))
        z = sc.transform(y.reshape(-1, 1))[:, 0]
        out[c] = float(np.max(np.abs(z)) if bien_the == "abs" else np.max(z))
    return out


def svc_rank(order):
    s = []
    for c in order:
        v = c.split("_")[0].replace("-db", "")
        if v not in s:
            s.append(v)
    return s


paths = sorted(glob.glob(join(root, "**", "simple_data.csv"), recursive=True))
ev = {b: {} for b in ("goc", "rs", "abs", "bo_hang_so_gan", "lat50")}
chi_tiet = []
for p in paths:
    svc, fault = basename(dirname(dirname(p))).split("_")
    for b in ev:
        d, it = chuan_bi(p, lat50=(b == "lat50"))
        sc = diem(d, it, "goc" if b == "lat50" else b)
        order = sorted(sc, key=lambda c: sc[c], reverse=True)  # sorted ổn định như RCAEval
        ev[b].setdefault(fault, Evaluator(max_k=5)).add_case(ranks=[Node(x, "unknown") for x in svc_rank(order)], answer=Node(svc, "unknown"))
        if b == "goc" and fault == "delay":
            n = preprocess(d[d["time"] < it], dataset=ds)
            top = order[0]
            goc = [c for c in order if c.split("_")[0] == svc]
            chi_tiet.append({"ca": f"{svc}_{fault}/{basename(dirname(p))}", "hang_service_goc": svc_rank(order).index(svc) + 1 if svc in svc_rank(order) else None,
                             "kenh_dau": top, "z_kenh_dau": round(sc[top], 1), "std_truoc_kenh_dau": float(n[top].std(ddof=0)),
                             "kenh_goc_tot_nhat": goc[0] if goc else None, "z_kenh_goc": round(sc[goc[0]], 1) if goc else None})
print(f"== {ds}: Avg@5 theo biến thể (chẩn đoán)")
for b, per in ev.items():
    print(f"  {b:15}", {f: round(e.average(5), 3) for f, e in sorted(per.items())})
print(f"== {ds}: các ca delay, biến thể goc")
for x in chi_tiet:
    print("  " + json.dumps(x, ensure_ascii=False))
