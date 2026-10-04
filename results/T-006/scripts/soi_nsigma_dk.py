r"""T-006 phiên 2, chẩn đoán (không phải kết quả chính thức): giả thuyết bài BARO chạy N-Sigma[t_inject] và
RobustScorer[t_inject] với dk_select_useful=True (tham số có sẵn của hàm; bỏ kênh main_, redis_, ... và giữ cpu/mem
có độ lệch chuẩn > 1, lat50). Tiền xử lý như chay_fse.py; gọi đúng RCAEval.e2e.nsigma / baro.
Cách dùng: <python py312-pin> soi_nsigma_dk.py fse-ob|fse-ss
"""
import glob, sys
from os.path import basename, dirname, join
import numpy as np, pandas as pd
import RCAEval.e2e as e2e
from RCAEval.benchmark.evaluation import Evaluator
from RCAEval.classes.graph import Node
ds = sys.argv[1]
for m in ("nsigma", "baro"):
    for dk in (False, True):
        per = {}
        for p in sorted(glob.glob(join(r"D:\RCA-ext\data", ds, "**", "simple_data.csv"), recursive=True)):
            svc, f = basename(dirname(dirname(p))).split("_")
            d = pd.read_csv(p)
            d = d.loc[:, ~d.columns.str.endswith("_latency-50")].replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
            it = int(open(join(dirname(p), "inject_time.txt")).readline())
            d = pd.concat([d[d.time < it].tail(600), d[d.time >= it].head(600)], ignore_index=True)
            d = d.rename(columns={c: c.replace("_latency-90", "_latency") for c in d.columns if c.endswith("_latency-90")})
            r = getattr(e2e, m)(d, it, dataset=ds, dk_select_useful=dk)["ranks"]
            s = []
            [s.append(x.split("_")[0].replace("-db", "")) for x in r if x.split("_")[0].replace("-db", "") not in s]
            per.setdefault(f, Evaluator(max_k=5)).add_case(ranks=[Node(x, "unknown") for x in s], answer=Node(svc, "unknown"))
        print(ds, m, "dk_select_useful=", dk, {f: round(e.average(5), 3) for f, e in sorted(per.items())})
