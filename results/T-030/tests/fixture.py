"""Fixture tổng hợp giống schema RE2-TT cho test bước 3–4. Không đọc dữ liệu thật.

Một "repo" giả trong results/T-030/work/fixture/<tên>: data/rcaeval/<ca>/{metrics,traces,logs}.parquet,
allowlist.json, nhan.json và thư mục tác giả TORAI giả. Lỗi tiêm ở ts-b-service từ mốc t (độ trễ ×4,
log ERROR, cpu tăng). Sinh tất định theo seed.
"""
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'results' / 'T-030' / 'work' / 'fixture'
T0 = 1_706_000_000
N = 1441
T_INJ = T0 + 720
SVC = ['ts-ui-dashboard', 'ts-a-service', 'ts-b-service', 'ts-c-service', 'ts-d-service']
DB = ['ts-b-mongo']
CHUOI = [  # (service, operation, duration µs bình thường)
    [('ts-ui-dashboard', 'GET', 9000), ('ts-a-service', 'POST /api/v1/aservice/do', 6000),
     ('ts-b-service', 'queryB', 3000), ('ts-b-mongo', 'find ts-b-mongo.x', 800)],
    [('ts-ui-dashboard', 'GET', 7000), ('ts-c-service', 'GET /api/v1/cservice/x/{id}', 4000),
     ('ts-d-service', 'calc_value', 1500)],
]


def metrics(rng, t_inj=T_INJ, root='ts-b-service'):
    t = np.arange(T0, T0 + N)
    df = {'time': t}
    for s in SVC + DB:
        sau = (t >= t_inj) & (s == root)
        df[f'{s}_cpu'] = rng.normal(10, 1, N) + np.where(sau, 8, 0)
        df[f'{s}_mem'] = rng.normal(100, 2, N)
        if s in SVC:
            df[f'{s}_latency-50'] = rng.normal(5, 0.3, N) + np.where(sau, 6, 0)
            df[f'{s}_latency-90'] = rng.normal(8, 0.5, N) + np.where(sau, 9, 0)
    df['ts-a-service_error'] = rng.poisson(0.2, N).astype(float)
    m = pd.DataFrame(df)
    m.loc[m.index[:3], 'ts-d-service_mem'] = np.nan  # ô trống đầu file
    return m


def traces(rng, t_inj=T_INJ, root='ts-b-service'):
    rows, k = [], 0
    for sec in range(T0, T0 + N):
        for c, chain in enumerate(CHUOI):
            for rep in range(2):
                tid = f'{sec:x}{c}{rep}'
                start = sec * 1_000_000 + rng.integers(0, 400_000)
                parent = None
                for depth, (s, op, d) in enumerate(chain):
                    k += 1
                    dur = int(max(50, rng.normal(d, d * 0.1)))
                    if sec >= t_inj and (s == root or (depth < len(chain) - 1 and any(x[0] == root for x in chain[depth:]))):
                        dur *= 4
                    sid = f'{k:016x}'
                    rows.append((tid, sid, s, None, op, parent, start // 1000, start + depth * 100, dur, None))
                    parent = sid
    df = pd.DataFrame(rows, columns=['traceID', 'spanID', 'serviceName', 'methodName', 'operationName', 'parentSpanID',
                                     'startTimeMillis', 'startTime', 'duration', 'statusCode'])
    df['time'] = '00:00'
    df['methodName'] = df['methodName'].astype('string')
    df['statusCode'] = df['statusCode'].astype('Int64')
    return df[['time', 'traceID', 'spanID', 'serviceName', 'methodName', 'operationName', 'parentSpanID',
               'startTimeMillis', 'startTime', 'duration', 'statusCode']]


def logs(rng, t_inj=T_INJ, root='ts-b-service'):
    rows = []
    for sec in range(T0, T0 + N, 2):
        for s in SVC:
            rows.append((sec, s, f'2024-01-01 INFO 1 --- handled request id={rng.integers(1, 9999)} ok'))
            if s == root and sec >= t_inj:
                rows.append((sec, s, f'2024-01-01 ERROR 1 --- timeout calling ts-b-mongo after {rng.integers(1, 99)} ms'))
    return pd.DataFrame(rows, columns=['timestamp', 'container_name', 'message'])


def tao_repo(ten, so_ca=2, seed=0, logs_cho_ca=None, sao_y_het=False):
    """Tạo repo giả. sao_y_het=True: các ca chung một nội dung (kiểm đổi locator)."""
    from p3.torai_b import BIN, theo_quy_uoc_tac_gia
    root = BASE / ten
    if root.exists():
        shutil.rmtree(root)
    cases, nhan = [], []
    for i in range(so_ca):
        rng = np.random.default_rng(seed if sao_y_het else seed + i)
        cname = f're2tt_ts-b-service_cpu_{i + 1}'
        d = root / 'data' / 'rcaeval' / cname
        d.mkdir(parents=True)
        m, tr, lg = metrics(rng), traces(rng), logs(rng)
        m.to_parquet(d / 'metrics.parquet', index=False)
        tr.to_parquet(d / 'traces.parquet', index=False)
        files = {}
        if logs_cho_ca is None or i in logs_cho_ca:
            lg.to_parquet(d / 'logs.parquet', index=False)
        from p3.selector import sha256_file
        for f in sorted(d.iterdir()):
            files[f.name] = {'path': f'data/rcaeval/{cname}/{f.name}', 'bytes': f.stat().st_size,
                             'sha256': sha256_file(f)}
        oid = 'dev-' + files['metrics.parquet']['sha256'][:10] if not sao_y_het else f'dev-{i:010x}'
        cases.append({'opaque_id': oid, 'case_dir': f'data/rcaeval/{cname}', 'files': files})
        nhan.append({'opaque_id': oid, 'case': cname, 'root': 'ts-b-service', 'fault': 'cpu',
                     'cell': 'ts-b-service|cpu', 'nhom_vi_tri_p75': 'x', 'inject_time': T_INJ})
        # thư mục tác giả TORAI giả: lưới bắt đầu ở đầu file + 10 s (như ca auth_cpu_1 thật)
        a = root / 'torai-TT' / 'ts-b-service_cpu' / str(i + 1)
        a.mkdir(parents=True)
        luoi = np.arange(T0 + 10, T0 + N, BIN)
        err, lat, _ = theo_quy_uoc_tac_gia(tr, luoi)
        err.reset_index().to_csv(a / 'tracets_err.csv', index=False)
        lat.reset_index().to_csv(a / 'tracets_lat.csv', index=False)
        # logts giả (không cần drain3): mỗi service một mẫu INFO, ts-b-service thêm mẫu ERROR
        lg2 = lg[(lg.timestamp >= luoi[0]) & (lg.timestamp < luoi[-1] + BIN)].copy()
        lg2['cot'] = lg2['container_name'] + '_' + np.where(lg2['message'].str.contains('ERROR'), '2', '1')
        lg2['bin'] = luoi[0] + ((lg2['timestamp'] - luoi[0]) // BIN) * BIN
        lt = lg2.groupby(['bin', 'cot']).size().unstack().reindex(index=luoi).fillna(0)
        lt.index.name = 'time'
        lt.reset_index().to_csv(a / 'logts.csv', index=False)
    al = {'so_ca': so_ca, 'cases': cases}
    (root / 'allowlist.json').write_text(json.dumps(al, indent=1), encoding='utf-8')
    (root / 'nhan.json').write_text(json.dumps({'so_ca': so_ca, 'cases': nhan}, indent=1), encoding='utf-8')
    return root
