"""Preflight không nhãn cho RE3-OB, khóa trước khi đọc dữ liệu (T-055, Minh duyệt 08/11/2026).

Chạy trên EC2 bằng env main. stdin: {'data_root', 'inventory', 'cases': {opaque: {'files': {...}, 't': int}}}.
Không đọc nhãn, tên ca, root hay fault. Chỉ xuất số đếm/tỷ lệ theo mã mờ, không xuất giá trị tín hiệu.

Quy tắc quyết định (áp chung cho cả dataset, không chọn theo ca):
 R1 schema: trace/log đúng tập cột của src/p3/re3.py; metric = time + <owner>_<suffix> với suffix thuộc 8 kênh.
 R2 metric.time là giây (khai của nhà phát hành). Phải nguyên, tăng ngặt, và t nằm trong [min, max].
 R3 đơn vị span.startTime và logs.timestamp: ứng viên s/ms/us/ns. Một ứng viên "khớp" ở một ca khi >= 99% bản ghi
    rơi vào [min(metric.time) − 60 s, max(metric.time) + 60 s]. Đơn vị dataset = ứng viên duy nhất khớp ở mọi ca có
    bản ghi. Không duy nhất hoặc có ca không khớp: BLOCKED.
 R4 span.duration cùng đơn vị với startTime (mô hình Jaeger). Kiểm: duration >= 0 ở 100% span; ở cặp cha–con cùng
    traceID, span con nằm trong span cha (dung sai 1 ms) ở >= 90% cặp, gộp toàn dataset. Không đạt: BLOCKED.
    Báo thêm tỷ lệ cho các đơn vị duration khác để đối chiếu.
 R5 startTimeMillis (nếu không null) khớp startTime theo đơn vị R3 trong 1 ms ở >= 99% span; không đạt: BLOCKED.
 R6 owner của metric prefix, serviceName, container_name thuộc inventory khai trước; ngoài: BLOCKED.
 R7 statusCode không null là số nguyên trong 0..16 (miền mã gRPC); ngoài: BLOCKED.
 R8 r: metric = trung vị bước thời gian (giây) chung của dataset nếu mọi ca bằng nhau, nếu không BLOCKED;
    trace = 1 µs; log = 1 s (giữ như TT/Nezha). Đây là giả định khai, ghi "chưa kiểm".
 R9 mô tả điều kiện suy biến của baseline (luật 21c): operation mới trong A, operation có 1 span bình thường,
    ca không có span/log/metric trong N hoặc A. Chỉ báo, không chặn.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

TRACE = {'time', 'traceID', 'spanID', 'serviceName', 'methodName', 'operationName',
         'parentSpanID', 'startTimeMillis', 'startTime', 'duration', 'statusCode'}
LOG = {'timestamp', 'container_name', 'message'}
CHANNELS = {'cpu', 'mem', 'diskio', 'socket', 'workload', 'error', 'latency-50', 'latency-90'}
UNITS = {'s': 10**9, 'ms': 10**6, 'us': 10**3, 'ns': 1}


def frac(mask):
    return float(np.mean(mask)) if len(mask) else None


def check_case(base, case, inventory):
    f = {k: base / v['path'] for k, v in case['files'].items()}
    m = pq.read_table(f['metrics.parquet']).to_pandas()
    tr = pq.read_table(f['traces.parquet']).to_pandas()
    lg = pq.read_table(f['logs.parquet']).to_pandas()
    t = int(case['t'])
    r = {'rows': {'metric': len(m), 'trace': len(tr), 'log': len(lg)}, 'blocked': []}
    if set(tr.columns) != TRACE:
        r['blocked'].append('R1 trace schema')
    if set(lg.columns) != LOG:
        r['blocked'].append('R1 log schema')
    cols = [c for c in m.columns if c != 'time']
    bad = [c for c in cols if '_' not in c or c.rsplit('_', 1)[1] not in CHANNELS]
    if 'time' not in m.columns or bad:
        r['blocked'].append('R1 metric schema')
    owners = {c.rsplit('_', 1)[0] for c in cols if c not in bad}
    owners |= set(tr['serviceName'].dropna()) | set(lg['container_name'].dropna())
    r['owners_outside_inventory'] = len(owners - set(inventory))
    if owners - set(inventory):
        r['blocked'].append('R6 owner outside inventory')
    mt = m['time'].to_numpy()
    if not np.issubdtype(mt.dtype, np.integer) or not (np.diff(mt) > 0).all() or not (mt.min() <= t <= mt.max()):
        r['blocked'].append('R2 metric time')
    lo, hi = (int(mt.min()) - 60) * 10**9, (int(mt.max()) + 60) * 10**9
    d = np.diff(mt)
    r['metric_step_median_s'] = float(np.median(d)) if len(d) else None
    r['units'] = {}
    for col, df in (('span_start', tr['startTime']), ('log', lg['timestamp'])):
        v = df.dropna().to_numpy(dtype=np.int64) if len(df.dropna()) else np.array([], dtype=np.int64)
        r['units'][col] = {u: (frac((v.astype(object) * k >= lo) & (v.astype(object) * k <= hi)) if len(v) else None)
                           for u, k in UNITS.items()}
    r['duration_negative'] = int((tr['duration'].dropna() < 0).sum())
    # Nesting cha–con cho từng ứng viên đơn vị (start và duration cùng đơn vị).
    p = tr[['traceID', 'spanID', 'parentSpanID', 'startTime', 'duration']].dropna(subset=['traceID', 'spanID'])
    j = p.merge(p, left_on=['traceID', 'parentSpanID'], right_on=['traceID', 'spanID'], suffixes=('', '_p'))
    r['parent_pairs'] = int(len(j))
    r['nested'] = {}
    for u, k in UNITS.items():
        if not len(j):
            r['nested'][u] = None; continue
        tol = 10**6 / k  # 1 ms tính theo đơn vị u
        s, e = j['startTime'], j['startTime'] + j['duration']
        ps, pe = j['startTime_p'], j['startTime_p'] + j['duration_p']
        r['nested'][u] = int(((s >= ps - tol) & (e <= pe + tol)).sum())
    ms = tr['startTimeMillis'].dropna()
    r['millis_nonnull'] = int(len(ms))
    r['millis_match'] = {}
    for u, k in UNITS.items():
        if not len(ms):
            r['millis_match'][u] = None; continue
        st = tr.loc[ms.index, 'startTime'].astype(object) * k
        r['millis_match'][u] = frac(abs(st - ms.astype(object) * 10**6) <= 10**6)
    sc = tr['statusCode'].dropna()
    okc = sc.apply(lambda x: float(x).is_integer() and 0 <= int(x) <= 16) if len(sc) else pd.Series([], dtype=bool)
    r['status_nonnull'] = int(len(sc))
    r['status_outside_domain'] = int((~okc).sum()) if len(sc) else 0
    r['status_nonzero'] = int((sc != 0).sum()) if len(sc) else 0
    if r['status_outside_domain']:
        r['blocked'].append('R7 statusCode domain')
    # R9 mô tả (dùng đơn vị us cho span start như ứng viên chính; chỉ đếm).
    r['degenerate'] = {}
    return r, tr, lg, m


def degenerate(r, tr, lg, m, t, unit):
    k = UNITS[unit]
    st = tr['startTime'].astype('int64') * k
    en = (tr['startTime'] + tr['duration']).astype('int64') * k
    T = t * 10**9
    sel = (st >= T - 300 * 10**9) & (en < T + 300 * 10**9)
    w = tr[sel].copy()
    before = (w['startTime'] + w['duration']).astype('int64') * k < T
    op = w['serviceName'].astype(str) + '_' + w['methodName'].fillna(w['operationName']).astype(str)
    n_ops, a_ops = set(op[before]), set(op[~before])
    counts = op[before].value_counts()
    r['degenerate'] = {'spans_N': int(before.sum()), 'spans_A': int((~before).sum()),
                       'new_ops_in_A': len(a_ops - n_ops),
                       'single_normal_span_ops': int((counts == 1).sum()),
                       'single_normal_span_ops_also_in_A': len({o for o, c in counts.items() if c == 1} & a_ops),
                       'metric_rows_N': int(((m['time'] >= t - 300) & (m['time'] < t)).sum()),
                       'metric_rows_A': int(((m['time'] >= t) & (m['time'] < t + 300)).sum())}


def main():
    req = json.loads(sys.stdin.buffer.read())
    base = Path(req['data_root'])
    per, raw = {}, {}
    for opaque, case in sorted(req['cases'].items()):
        r, tr, lg, m = check_case(base, case, req['inventory'])
        per[opaque] = r
        raw[opaque] = (tr, lg, m, int(case['t']))
    print(json.dumps({'per_case': per, 'stage': 'host'}, sort_keys=True, default=str))
    sys.stdout.flush()
    # Mô tả suy biến cần đơn vị span: tính cho mọi ứng viên khớp >=99% ở ca đó (thường một).
    deg = {}
    for opaque, (tr, lg, m, t) in raw.items():
        cand = [u for u, x in per[opaque]['units']['span_start'].items() if x is not None and x >= 0.99]
        if len(cand) == 1 and len(tr):
            degenerate(per[opaque], tr, lg, m, t, cand[0])
            deg[opaque] = dict(per[opaque]['degenerate'], unit=cand[0])
    print(json.dumps({'degenerate': deg, 'stage': 'host-degenerate'}, sort_keys=True, default=str))


def decide(per_case_all, nesting_threshold=0.90):
    """Quyết định toàn dataset theo R3–R8 từ kết quả mọi host (chạy ở laptop, cùng code đã khóa)."""
    out = {'blocked': sorted({f'{o}: {b}' for o, r in per_case_all.items() for b in r['blocked']})}
    for col in ('span_start', 'log'):
        ok = None
        for o, r in per_case_all.items():
            fr = r['units'][col]
            if all(v is None for v in fr.values()):
                continue
            good = {u for u, v in fr.items() if v is not None and v >= 0.99}
            ok = good if ok is None else ok & good
        out[col] = sorted(ok) if ok else []
        if len(out[col]) != 1:
            out['blocked'].append(f'R3 {col} unit not unique: {out[col]}')
    if len(out.get('span_start', [])) == 1:
        u = out['span_start'][0]
        pairs = sum(r['parent_pairs'] for r in per_case_all.values())
        nested = {v: sum((r['nested'][v] or 0) for r in per_case_all.values()) for v in UNITS}
        out['nesting_fraction'] = {v: (nested[v] / pairs if pairs else None) for v in UNITS}
        if not pairs or out['nesting_fraction'][u] < nesting_threshold:
            out['blocked'].append('R4 nesting below threshold')
        if any(r['duration_negative'] for r in per_case_all.values()):
            out['blocked'].append('R4 negative duration')
        mm = [r['millis_match'][u] for r in per_case_all.values() if r['millis_match'][u] is not None]
        out['millis_match_min'] = min(mm) if mm else None
        if mm and min(mm) < 0.99:
            out['blocked'].append('R5 startTimeMillis mismatch')
    steps = {r['metric_step_median_s'] for r in per_case_all.values()}
    out['metric_step_s'] = sorted(steps)
    if len(steps) != 1 or None in steps:
        out['blocked'].append('R8 metric cadence not common')
    out['PASS'] = not out['blocked']
    return out


if __name__ == '__main__':
    main()
