r"""T-006 QT5: vì sao `redis_diskio` đứng đầu thứ hạng BARO ở 78/90 ca torai-OB. Chỉ đọc dữ liệu, không dùng nhãn.

Dựng lại đúng tiền xử lý của main.py (--length 10) và phần chấm điểm của `RCAEval.e2e.baro` (RobustScaler trên đoạn
trước mốc tiêm, điểm = max z ở đoạn sau), rồi in cho từng ca: điểm và IQR của redis_diskio, điểm lớn thứ hai.
Cách dùng: <python py312-pin> soi_baro_redis.py D:\RCA-ext\data\torai-OB
"""
import glob
import json
import sys
from os.path import basename, dirname, join

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

from RCAEval.io.time_series import preprocess

root = sys.argv[1]
rows = []
for p in sorted(glob.glob(join(root, "**", "simple_metrics.csv"), recursive=True)):
    d = dirname(p)
    data = pd.read_csv(p)
    data = data.loc[:, ~data.columns.str.endswith("_latency-50")]
    data = data.replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    it = int(open(join(d, "inject_time.txt")).readline().strip())
    data = pd.concat([data[data["time"] < it].tail(300), data[data["time"] >= it].head(300)], ignore_index=True)
    data = data.rename(columns={c: c.replace("_latency-90", "_latency") for c in data.columns if c.endswith("_latency-90")})
    n = preprocess(data[data["time"] < it], dataset="torai-ob")
    a = preprocess(data[data["time"] >= it], dataset="torai-ob")
    cols = [c for c in n.columns if c in a.columns]
    sc = {}
    for c in cols:
        s = RobustScaler().fit(n[c].to_numpy().reshape(-1, 1))
        sc[c] = (float(np.max(s.transform(a[c].to_numpy().reshape(-1, 1)))), float(s.scale_[0]))
    order = sorted(sc, key=lambda c: sc[c][0], reverse=True)
    r = sc.get("redis_diskio")
    rows.append({"ca": f"{basename(dirname(d))}/{basename(d)}", "dau": order[0], "diem_dau": sc[order[0]][0],
                 "redis_diskio_diem": r[0] if r else None, "redis_diskio_scale_IQR": r[1] if r else None,
                 "redis_diskio_iqr_bang_0_nen_scale_1": (r[1] == 1.0) if r else None,
                 "thu_hai": order[1], "diem_thu_hai": sc[order[1]][0]})
dau_redis = [x for x in rows if x["dau"] == "redis_diskio"]
print(f"{len(rows)} ca; redis_diskio đứng đầu {len(dau_redis)} ca")
print("trong các ca đó: scale (IQR) của redis_diskio =", sorted({round(x['redis_diskio_scale_IQR'], 3) for x in dau_redis})[:10])
print("điểm redis_diskio (min, trung vị, max):", np.min([x['redis_diskio_diem'] for x in dau_redis]),
      np.median([x['redis_diskio_diem'] for x in dau_redis]), np.max([x['redis_diskio_diem'] for x in dau_redis]))
print("điểm kênh thứ hai (trung vị):", np.median([x['diem_thu_hai'] for x in dau_redis]))
for x in rows[:6]:
    print(json.dumps(x, ensure_ascii=False))
