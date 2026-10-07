"""T-030: đo thô chi phí BOCPD (BARO e35f4ec, hazard 50, MultivariateT) trên dữ liệu TỔNG HỢP, không phải ca thật.
Mục đích: kiểm giả định chi phí ∝ T²d³ dùng trong ước lượng SPEC T-031. Máy có việc khác chạy (agent viết mã): số thô.
"""
import json, sys, time
from functools import partial
import numpy as np
sys.path.insert(0, 'D:/RCA-ext/src/baro')
from baro._bocpd import MultivariateT, constant_hazard, online_changepoint_detection
out = []
for T, d in [(150, 6), (300, 6), (300, 25), (300, 48)]:
    rng = np.random.default_rng(0)
    x = rng.random((T, d)); x[T // 2:] += 0.5
    t0 = time.perf_counter()
    online_changepoint_detection(x, partial(constant_hazard, 50), MultivariateT(dims=d))
    s = time.perf_counter() - t0
    calls = T * (T + 1) // 2
    out.append({'T': T, 'd': d, 'giay': round(s, 2), 'so_lan_pdf': calls, 'ms_moi_lan': round(1000 * s / calls, 4)})
    print(out[-1], flush=True)
json.dump(out, open('results/T-030/runs/bocpd-tong-hop-001/ket-qua.json', 'w'), indent=1)
