r"""T-006 phiên 2, chẩn đoán (không phải kết quả chính thức): giả thuyết bài BARO dùng N-Sigma kiểu repo CIRCA gốc
(NetManAIOps/CIRCA 0215e18, circa/alg/common.py: NSigmaScorer = max |z|, z theo StandardScaler của đoạn huấn luyện).
Cửa sổ lấy đúng mặc định của RCAEval.classes.data.CaseData (lookup_window=120, detect_window=10, interval 1 s, nên
huấn luyện = 111 điểm đầu, kiểm = 10 điểm cuối) và current = mốc tiêm + 300 như RCAEval/graph_heads/rht.py gọi.
Tức: huấn luyện = [t-120, t-10], kiểm = [t+291, t+300] (t = mốc tiêm). Dữ liệu tiền xử lý như chay_fse.py.
Chỉ thử đúng một cấu hình này, lấy từ mặc định có sẵn trong code; không dò tham số.
Cách dùng: <python py312-pin> soi_nsigma_circa_style.py fse-ob|fse-ss
"""
import glob, sys
from os.path import basename, dirname, join
import numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from RCAEval.benchmark.evaluation import Evaluator
from RCAEval.classes.graph import Node
from RCAEval.io.time_series import preprocess
ds = sys.argv[1]
per = {}
bo = []
for p in sorted(glob.glob(join(r"D:\RCA-ext\data", ds, "**", "simple_data.csv"), recursive=True)):
    svc, f = basename(dirname(dirname(p))).split("_")
    d = pd.read_csv(p)
    d = d.loc[:, ~d.columns.str.endswith("_latency-50")].replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    it = int(open(join(dirname(p), "inject_time.txt")).readline())
    d = d.rename(columns={c: c.replace("_latency-90", "_latency") for c in d.columns if c.endswith("_latency-90")})
    x = preprocess(d, dataset=ds)
    t = d["time"].to_numpy()
    tr = (t >= it - 120) & (t <= it - 10)
    te = (t >= it + 291) & (t <= it + 300)
    if tr.sum() == 0 or te.sum() == 0:  # ví dụ fse-ss user_mem/1: time rỗng từ 246 s sau mốc tiêm
        bo.append(f"{svc}_{f}/{basename(dirname(p))}")
        continue
    sc = {}
    for c in x.columns:
        a, b = x[c].to_numpy()[tr], x[c].to_numpy()[te]
        if len(set(np.concatenate([a, b]))) <= 1:   # CaseData(prune=True) bỏ chuỗi hằng
            continue
        z = StandardScaler().fit(a.reshape(-1, 1)).transform(b.reshape(-1, 1))[:, 0]
        sc[c] = float(np.max(np.abs(z)))
    order = sorted(sc, key=lambda c: sc[c], reverse=True)
    s = []
    [s.append(c.split("_")[0].replace("-db", "")) for c in order if c.split("_")[0].replace("-db", "") not in s]
    per.setdefault(f, Evaluator(max_k=5)).add_case(ranks=[Node(v, "unknown") for v in s], answer=Node(svc, "unknown"))
print(ds, "N-Sigma kiểu CIRCA, Avg@5:", {f: round(e.average(5), 3) for f, e in sorted(per.items())},
      "trung bình", round(np.mean([e.average(5) for e in per.values()]), 3), "| bỏ ca thiếu cửa sổ:", bo)
