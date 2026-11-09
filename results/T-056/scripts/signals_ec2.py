"""T-056, chạy trên EC2 (env main). stdin: yêu cầu từ build_requests.py. Không nhãn; xuất số đếm theo mã mờ.

- RE3-OB: span status != 0 theo service ở N/A (span end < t là N; trong [t-300, t+300)); "lỗi riêng" = span lỗi
  không có span con lỗi; dòng log có từ khóa theo container ở N/A.
- Mọi bộ: với từng cột metric M1 đã cờ: trung vị/IQR của N, max/min của A, IQR < 10*eps (nhánh c=1 src/m1/e4.py),
  và z tính lại theo đúng công thức để đối chiếu với s của M1.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

EPS = np.finfo(np.float64).eps
req = json.loads(sys.stdin.buffer.read())
out = {}
for oid, c in sorted(req['cases'].items()):
    base = Path(c['data_root'])
    t = int(c['t'])
    r = {'dataset': c['dataset']}
    m = pq.read_table(base / c['files']['metrics.parquet']).to_pandas()
    tm = m['time'].to_numpy()
    nmask, amask = (tm >= t - 300) & (tm < t), (tm >= t) & (tm < t + 300)
    mets = {}
    for col in c['metric_cols']:
        if col not in m.columns:
            mets[col] = {'missing': True}; continue
        N = m.loc[nmask, col].to_numpy(dtype=float); A = m.loc[amask, col].to_numpy(dtype=float)
        N, A = N[np.isfinite(N)], A[np.isfinite(A)]
        if not len(N) or not len(A):
            mets[col] = {'empty': True}; continue
        med = float(np.median(N)); iqr = float(np.percentile(N, 75) - np.percentile(N, 25))
        cc = iqr if iqr >= 10 * EPS else 1.0
        mets[col] = {'med_N': med, 'iqr_N': iqr, 'c_is_1': bool(iqr < 10 * EPS), 'max_A': float(A.max()), 'min_A': float(A.min()),
                     'z_len': float((A.max() - med) / cc), 'z_xuong': float((med - A.min()) / cc),
                     'n_unique_N': int(len(np.unique(N))), 'n_N': int(len(N)), 'n_A': int(len(A))}
    r['metrics'] = mets
    if c['dataset'] == 'RE3-OB':
        tr = pq.read_table(base / c['files']['traces.parquet'],
                           columns=['traceID', 'spanID', 'parentSpanID', 'serviceName', 'startTime', 'duration', 'statusCode']).to_pandas()
        st = tr['startTime'].astype('int64'); en = st + tr['duration'].astype('int64')
        sel = (st >= (t - 300) * 10**6) & (en < (t + 300) * 10**6)
        w = tr[sel].copy(); w['N'] = (en[sel] < t * 10**6).to_numpy()
        w['err'] = w['statusCode'].fillna(0).astype('int64') != 0
        child_err = set(zip(w.loc[w['err'], 'traceID'], w.loc[w['err'], 'parentSpanID'].fillna('')))
        w['own'] = w['err'] & ~np.array([(a, b) in child_err for a, b in zip(w['traceID'], w['spanID'])])
        svc = {}
        for name, g in w.groupby('serviceName'):
            svc[name] = {'spans_N': int(g['N'].sum()), 'spans_A': int((~g['N']).sum()),
                         'err_N': int((g['err'] & g['N']).sum()), 'err_A': int((g['err'] & ~g['N']).sum()),
                         'own_N': int((g['own'] & g['N']).sum()), 'own_A': int((g['own'] & ~g['N']).sum())}
        r['spans'] = svc
        lg = pq.read_table(base / c['files']['logs.parquet']).to_pandas()
        ts = lg['timestamp'].astype('int64')
        lsel = (ts >= t - 300) & (ts < t + 300)
        l = lg[lsel].copy(); l['N'] = (ts[lsel] < t).to_numpy()
        pat = '|'.join(req['keywords'])
        l['kw'] = l['message'].fillna('').str.upper().str.contains(pat, regex=True)
        logs = {}
        for name, g in l.groupby('container_name'):
            logs[name] = {'lines_N': int(g['N'].sum()), 'lines_A': int((~g['N']).sum()),
                          'err_N': int((g['kw'] & g['N']).sum()), 'err_A': int((g['kw'] & ~g['N']).sum())}
        r['logs'] = logs
    out[oid] = r
print(json.dumps(out, sort_keys=True))
