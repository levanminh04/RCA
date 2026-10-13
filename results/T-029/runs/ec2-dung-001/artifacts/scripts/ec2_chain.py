"""Chuỗi 2a→2b→2c→2d T-029. Mọi ghi nằm T029_HOME; không chỉnh source/env/data."""
import json
import os
import sys
import time
from functools import partial
from pathlib import Path

import chung
from chung import ROOT, DATA_ROOT, ghi_json, progress, sha256_file

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
AL = chung.nap_allowlist()
BD = load(ROOT / 'inputs/bao-dong.json')['bo_phat_hien']
MO = load(ROOT / 'inputs/moc.json')
RUN = ROOT / 'runs/chuoi-001'

def stop_check():
    if (ROOT / 'STOP').exists(): raise RuntimeError('Dừng theo STOP của người làm')

def metric(oid):
    import numpy as np
    import pandas as pd
    from p3 import selector
    f = selector.chon_ca(AL, oid, DATA_ROOT, kiem_hash=True, tep=['metrics.parquet'])
    df = pd.read_parquet(f['metrics.parquet'])
    times = df['time'].to_numpy()
    assert len(times) == 1441 and np.all(np.diff(times) == 1), 'V1 lưới thời gian lệch'
    assert int(times[720]) == MO[oid], 'V1 mốc không ở720'
    return df

def wrapper(df, hazard):
    from baro._bocpd import MultivariateT, constant_hazard, online_changepoint_detection
    from p3.adapters.phat_hien import cot_bocpd, tien_xu_ly_bocpd, diem_doi_tu_R
    cols = cot_bocpd(df.columns)
    mat = tien_xu_ly_bocpd(df[cols])
    R, _ = online_changepoint_detection(mat.to_numpy(), partial(constant_hazard, hazard), MultivariateT(dims=mat.shape[1]))
    cps, m = diem_doi_tu_R(R)
    if cps is None: raise RuntimeError(f'posterior không hữu hạn cột {m}')
    return {'status': 'OK', 'chi_so': cps, 'alarms': [int(df['time'].iloc[i]) for i in cps],
            'm': [int(x) for x in m], 'input_shape': {'T': len(df), 'cot_tho': len(cols), 'cot_sau_tien_xu_ly': mat.shape[1]},
            'hazard_denominator': hazard}

def guard():
    from p3 import selector
    rows = []
    for oid in sorted(AL):
        stop_check()
        f = selector.chon_ca(AL, oid, DATA_ROOT, kiem_hash=True)
        rows.extend({'opaque_id': oid, 'file': n, 'sha256': sha256_file(p)} for n, p in f.items())
        progress(f'GUARD_SHA {oid} PASS {len(f)}')
    actual = chung.hash_p3()
    expected = load(ROOT / 'inputs/src-p3-expected.json')
    for p, h in actual['tep'].items(): assert expected['tep'][p] == h, 'V1 remote src lệch ' + p
    missing = sorted(set(expected['tep']) - set(actual['tep']))
    assert set(missing) <= {'src/p3/nezha.py', 'src/p3/nezha_worker.py', 'src/p3/adapters/nezha.py'}, missing
    out = {'V1': 'PASS', 'data_root': str(DATA_ROOT), 'cases': len(AL), 'files': len(rows), 'hashes': rows,
           'remote_src_p3': actual, 'local_additions_not_used_on_ec2': missing,
           'inputs': {p.name: sha256_file(p) for p in sorted((ROOT / 'inputs').glob('*'))},
           'scripts': {p.name: sha256_file(p) for p in sorted((ROOT / 'scripts').glob('*')) if p.is_file()}}
    ghi_json(RUN / 'guard.json', out)
    progress(f'GUARD PASS {len(AL)}ca {len(rows)}tep')

def v3():
    from p3.adapters.phat_hien import bocpd, cot_bocpd, tien_xu_ly_bocpd
    ds = []
    for oid in sorted(AL):
        stop_check()
        df = metric(oid)
        d = tien_xu_ly_bocpd(df[cot_bocpd(df.columns)]).shape[1]
        expected = BD['bocpd'][oid]['input_shape']['cot_sau_tien_xu_ly']
        ds.append({'opaque_id': oid, 'd': d, 'expected': expected})
        ghi_json(RUN / 'v3-dimensions.json', ds)
        assert d == expected, 'V3 số cột lệch ' + oid
    oid = min(ds, key=lambda x: (x['d'], x['opaque_id']))['opaque_id']
    progress('2a V3 BAT_DAU ' + oid)
    t0 = time.perf_counter()
    kq = bocpd(metric(oid))
    ghi_json(RUN / 'v3-replay.json', {'opaque_id': oid, 'result': kq, 'wall_s': time.perf_counter()-t0})
    expected = BD['bocpd'][oid]
    checks = {k: kq.get(k) == expected.get(k) for k in ('status', 'chi_so', 'alarms', 'input_shape', 'detector_columns')}
    ghi_json(RUN / 'v3-check.json', {'opaque_id': oid, 'checks': checks, 'status': 'PASS' if all(checks.values()) else 'FAIL'})
    assert all(checks.values()), 'V3 lệch điểm đổi ' + str(checks)
    progress('2a V3 PASS ' + oid)
    return oid

def i1(oid):
    from p3.adapters.phat_hien import bocpd
    progress('2b I1 WRAPPER50 BAT_DAU ' + oid)
    prefix = metric(oid).iloc[:720].copy()
    t0 = time.perf_counter()
    adapter = bocpd(prefix)
    ghi_json(RUN / 'wrapper50-adapter.json', {'opaque_id': oid, 'result': adapter, 'wall_s': time.perf_counter()-t0})
    t0 = time.perf_counter()
    wrap = wrapper(prefix, 50)
    ghi_json(RUN / 'wrapper50-custom.json', {'opaque_id': oid, 'result': wrap, 'wall_s': time.perf_counter()-t0})
    checks = {k: adapter.get(k) == wrap.get(k) for k in ('status', 'alarms', 'chi_so', 'input_shape')}
    ghi_json(RUN / 'wrapper50-check.json', {'checks': checks, 'status': 'PASS' if all(checks.values()) else 'FAIL'})
    assert all(checks.values()), 'wrapper50 lệch; dừng'
    progress('2b I1 WRAPPER50 PASS')
    folder = RUN / 'i1'
    folder.mkdir()
    for n, ca in enumerate(sorted(AL), 1):
        stop_check()
        progress(f'2b I1 [{n}/30] BAT_DAU {ca}')
        t0 = time.perf_counter()
        kq = adapter if ca == oid else bocpd(metric(ca).iloc[:720].copy())
        ghi_json(folder / (ca + '.json'), {'opaque_id': ca, 'result': kq, 'wall_s': time.perf_counter()-t0,
                                         'prefix': [0,720], 'source': 'p3.adapters.phat_hien.bocpd', 'hazard_denominator': 50})
        assert kq['status'] == 'OK', 'I1 lỗi chưa được SPEC quy định; dừng ' + ca
        progress(f'2b I1 [{n}/30] XONG {ca}')
    progress('2b I1 PASS 30/30')

def i2():
    folder = RUN / 'i2'
    folder.mkdir()
    for n, oid in enumerate(sorted(AL), 1):
        stop_check()
        progress(f'2c I2 [{n}/30] BAT_DAU {oid}')
        t0 = time.perf_counter()
        kq = wrapper(metric(oid).iloc[:720].copy(), 250)
        ghi_json(folder / (oid + '.json'), {'opaque_id': oid, 'result': kq, 'wall_s': time.perf_counter()-t0,
                                          'prefix': [0,720], 'hazard_denominator': 250})
        progress(f'2c I2 [{n}/30] XONG {oid}')
    progress('2c I2 PASS 30/30')

def records(folder):
    return [load(p) for p in sorted(folder.glob('luot/*/ban-ghi-*.json'))]

def i3():
    import rca_b
    exp = load(ROOT / 'inputs/v4-expected.json')
    oid = exp['opaque_id']
    progress('2d V4 BAT_DAU ' + oid)
    rca_b.main('v4', t_co_dinh=oid+':720', detector='nsigma')
    v4dir = sorted((ROOT / 'runs').glob('v4-*'))[-1]
    got = records(v4dir)
    key = lambda x: (x['method'], x['variant'], x['seed'])
    g = {key(x): x for x in got}
    checks = [{'method': e['method'], 'variant': e['variant'], 'seed': e['seed'],
               'status_match': key(e) in g and g[key(e)]['status'] == e['status'],
               'ranking_match': key(e) in g and g[key(e)].get('ranking_native') == e['ranking_native'],
               'source': e['source_path'], 'source_sha256': e['source_sha256']} for e in exp['records']]
    passed = len(got) == 6 and all(x['status_match'] and x['ranking_match'] for x in checks)
    ghi_json(RUN / 'v4-check.json', {'opaque_id': oid, 'checks': checks, 'status': 'PASS' if passed else 'FAIL', 'run': str(v4dir.relative_to(ROOT))})
    assert passed, 'V4 lệch thứ hạng; dừng'
    progress('2d V4 PASS')
    for det in ('bocpd', 'nsigma'):
        for n, ca in enumerate(sorted(AL), 1):
            stop_check()
            df = metric(ca)
            alarms = BD[det][ca]['alarms']
            post = [i for i, t in enumerate(df['time']) if int(t) in set(alarms) and i >= 720]
            assert post, 'I3 không có báo sau mốc, tình huống chưa quy định; dừng'
            i = min(post)
            progress(f'2d I3 {det} [{n}/30] BAT_DAU {ca} i={i}')
            rca_b.main(f'i3-{det}-{ca}', t_co_dinh=ca+':'+str(i), detector=det)
            folder = sorted((ROOT / 'runs').glob(f'i3-{det}-{ca}-*'))[-1]
            rows = records(folder)
            assert len(rows) == 6, 'I3 thiếu bản ghi; dừng'
            summary = load(folder / 'tom-tat.json')
            assert summary['so_loi_runner'] == 0, 'I3 lỗi runner; dừng'
            ghi_json(folder / 'source-tplus.json', {'opaque_id': ca, 'detector': det, 'index': i, 'time': int(df['time'].iloc[i]),
                                                   'source': 'inputs/bao-dong.json#/bo_phat_hien/'+det+'/'+ca+'/alarms',
                                                   'interpretation': 'RCA tại báo động đầu sau mốc, chọn nhờ nhãn mốc'})
            progress(f'2d I3 {det} [{n}/30] XONG {ca}')
    progress('2d I3 PASS 60/60 cặp, 360 bản ghi')

def main():
    RUN.mkdir(parents=True, exist_ok=False)
    t0 = time.perf_counter()
    try:
        progress('CHUOI BAT_DAU: GUARD→2a→2b→2c→2d')
        guard()
        oid = v3()
        i1(oid)
        i2()
        i3()
        ghi_json(RUN / 'ket-thuc.json', {'status': 'PASS', 'wall_s': time.perf_counter()-t0})
        progress('CHUOI XONG PASS')
    except BaseException as exc:
        ghi_json(RUN / 'dung.json', {'status': 'STOP', 'error': type(exc).__name__+': '+str(exc), 'wall_s': time.perf_counter()-t0})
        progress('CHUOI DUNG '+type(exc).__name__+': '+str(exc))
        raise

if __name__ == '__main__': main()
