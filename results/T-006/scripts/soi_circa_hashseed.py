r"""T-006 phiên 2: vì sao CIRCA chạy lại cùng đầu vào, cùng bộ thư viện chỉ ra thứ hạng giống hệt ở 75/90 ca torai-OB.

Giả thuyết: thứ tự duyệt set()/dict theo hash chuỗi của Python (đổi mỗi tiến trình nếu PYTHONHASHSEED không cố định)
làm thứ tự nút khác nhau, nên các nút bằng điểm được xếp khác nhau. rht.py dùng list(set(...)) cho services, metrics;
đồ thị networkx dựng từ Node (hash theo chuỗi).
Cách làm: với các ca có thứ hạng khác nhau giữa x1-py312pin-circa-torai-ob và l4-circa-torai-ob-lan2, chạy lại
RCAEval.e2e.circa (tiền xử lý đúng như main.py --length 10) trong tiến trình con với PYTHONHASHSEED=0 (2 lần) và =1.
Cách dùng: <python py312> soi_circa_hashseed.py   (tự gọi python của py312-pin cho tiến trình con)
"""
import json
import os
import subprocess
import sys
from pathlib import Path

WORK = Path(r"D:\RCA-ext\work\T-006")
PIN = r"D:\RCA-ext\envs\py312-pin\Scripts\python.exe"

CON = r'''
import json, sys, numpy as np, pandas as pd
from RCAEval.e2e import circa
out = {}
for case in sys.argv[1:]:
    svc_fault, lan = case.rsplit("_", 1)
    base = f"D:/RCA-ext/data/torai-OB/{svc_fault}/{lan}"
    d = pd.read_csv(f"{base}/simple_metrics.csv")
    d = d.loc[:, ~d.columns.str.endswith("_latency-50")].replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    it = int(open(f"{base}/inject_time.txt").readline())
    d = pd.concat([d[d.time < it].tail(300), d[d.time >= it].head(300)], ignore_index=True)
    d = d.rename(columns={c: c.replace("_latency-90", "_latency") for c in d.columns if c.endswith("_latency-90")})
    out[case] = circa(d, it, dataset="torai-ob", dk_select_useful=False)["ranks"]
print(json.dumps(out))
'''

a = WORK / "x1-py312pin-circa-torai-ob" / "output" / "results"
b = WORK / "l4-circa-torai-ob-lan2" / "output" / "results"
khac = [f.stem for f in sorted(a.glob("*.json")) if json.loads(f.read_text()) != json.loads((b / f.name).read_text())]
print(f"ca khác nhau giữa hai lần chạy chính thức: {len(khac)}: {khac}")
chon = khac[:4]
kq = {}
for nhan, seed in (("seed0_lan1", "0"), ("seed0_lan2", "0"), ("seed1", "1")):
    env = dict(os.environ, PYTHONHASHSEED=seed, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    r = subprocess.run([PIN, "-c", CON] + chon, capture_output=True, text=True, env=env)
    kq[nhan] = json.loads(r.stdout.strip().splitlines()[-1])
for c in chon:
    s0a, s0b, s1 = kq["seed0_lan1"][c], kq["seed0_lan2"][c], kq["seed1"][c]
    chinh_thuc = [json.loads((x / f"{c}.json").read_text())["0"] for x in (a, b)]
    # khác nhau chỉ ở thứ tự hay cả tập phần tử?
    print(f"{c}: seed0 lần1 == lần2: {s0a == s0b}; seed0 == seed1: {s0a == s1}; "
          f"cùng tập phần tử: {set(s0a) == set(s1)}; vị trí đầu tiên khác (seed0 vs seed1): "
          f"{next((i for i, (x, y) in enumerate(zip(s0a, s1)) if x != y), None)}; "
          f"hai lần chính thức cùng tập: {set(chinh_thuc[0]) == set(chinh_thuc[1])}")

# Phần 2: thêm seed 2..5 cho cùng 4 ca, đếm số thứ hạng khác nhau và vị trí khác đầu tiên so với seed 0.
them = {}
for seed in ("2", "3", "4", "5"):
    env = dict(os.environ, PYTHONHASHSEED=seed, OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")
    r = subprocess.run([PIN, "-c", CON] + chon, capture_output=True, text=True, env=env)
    them[seed] = json.loads(r.stdout.strip().splitlines()[-1])
for c in chon:
    tat_ca = [kq["seed0_lan1"][c], kq["seed1"][c]] + [them[s][c] for s in them]
    khac_nhau = len({json.dumps(x) for x in tat_ca})
    vt = [next((i for i, (x, y) in enumerate(zip(kq["seed0_lan1"][c], t)) if x != y), None) for t in tat_ca[1:]]
    top5 = len({json.dumps(t[:5]) for t in tat_ca})
    print(f"{c}: 6 seed (0..5) cho {khac_nhau} thứ hạng khác nhau; vị trí khác đầu tiên so với seed 0: {vt}; số top-5 khác nhau: {top5}")
