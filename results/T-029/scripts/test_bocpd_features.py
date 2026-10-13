"""Synthetic answers known in advance, T-029 V6 subset B1/B4."""
import json
import time
import traceback

import numpy as np
import pandas as pd

import bocpd_features as bf


def main():
    bf.audit('Lệnh có ghi: T-014-main python -B -W ignore results/T-029/scripts/test_bocpd_features.py; chỉ chuỗi tổng hợp có đáp án, không đọc telemetry/nhãn.')
    start = time.perf_counter()
    checks = []

    def check(name, ok):
        checks.append({'name': name, 'pass': bool(ok)})
        if not ok:
            raise AssertionError(name)

    frame = pd.DataFrame({'time': np.arange(1441), 'svc_latency-50': [np.nan] * 200 + [1.] * 1241,
                          'constant_error': [0.] * 1441, 'leading_error': [np.nan] * 202 + list(np.arange(1239))})
    filled, endings, raw = bf.prepare(frame)
    check('B1 native retains leading NaN, drops true constant', list(filled.columns) == ['svc_latency-50', 'leading_error'])
    check('B1 first non-NaN ends recorded', endings == {'svc_latency-50': 200, 'leading_error': 202})
    check('B1 includes both ends within +-2', bf.b1_at(endings, 200)['columns'] == ['leading_error', 'svc_latency-50'])
    check('B1 excludes end beyond +-2', bf.b1_at(endings, 197)['flag'] is False)
    check('B1 Nv boundary NA left', bf.b1_at(endings, 2)['flag'] is None)
    check('B1 Nv boundary NA right', bf.b1_at(endings, 718)['flag'] is None)
    check('B1 Nv inclusive valid edges', bf.b1_at({}, 3)['valid'] and bf.b1_at({}, 717)['valid'])
    x = np.resize(np.array([-1., 0., 1.]), 1441)
    x[300:] += 10
    data = np.column_stack([x])
    comp = bf.b4_components(data, 300, 30)
    check('B4 known MAD=1 and step=10', comp['mad'][0] == 1 and comp['jump'][0] == 10)
    check('B4 step reaches all predeclared thresholds', all(bf.summary(comp, ['step'])['flags'].values()))
    flat = np.zeros((1441, 2)); flat[300:, 0] = 10
    comp_flat = bf.b4_components(flat, 300, 30)
    summarized = bf.summary(comp_flat, ['changed', 'flat'])
    check('B4 MAD0 jump separate', summarized['constant_change_columns'] == ['changed'])
    check('B4 MAD0 jump does not make threshold flag true', not any(summarized['flags'].values()))
    check('B4 MAD0 zero step count', summarized['constant_no_change_count'] == 1)
    for w in bf.WS:
        low, high = 1 + w + 30, 720 - w
        check(f'B4 w={w} inclusive low/high', bf.b4_components(data, low, w) is not None and bf.b4_components(data, high, w) is not None)
        check(f'B4 w={w} outside low/high NA', bf.b4_components(data, low - 1, w) is None and bf.b4_components(data, high + 1, w) is None)
    check('B4 S at720 NA as flag', bf.b4_components(data, 720, 30) is None)
    he = bf.heuristic(bf.b4_components(data, 720, 30, background=False), ['step'])
    check('E heuristic uses formula but has no flags/threshold', he['valid'] and 'flags' not in he and 'flags' not in he['columns'][0])
    dest = bf.OUT / 'runs/bocpd-features-001/V6.json'
    version = 2
    while dest.exists():
        dest = bf.OUT / f'runs/bocpd-features-001/V6-{version:03d}.json'
        version += 1
    bf.write_json(dest, {'status': 'PASS', 'checks': checks, 'count': len(checks),
                         'seconds': round(time.perf_counter() - start, 3), 'script_sha256': bf.digest(__file__),
                         'implementation_sha256': bf.digest(bf.__file__), 'uses_real_data': False})
    bf.audit(f'V6 B1/B4 PASS {len(checks)}/{len(checks)} đáp án tổng hợp; không phải V6 toàn bộ N-Sigma.')
    print(json.dumps({'status': 'PASS', 'checks': len(checks)}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        path = bf.OUT / 'runs/bocpd-features-001/V6-failed.json'
        attempt = 2
        while path.exists():
            path = bf.OUT / f'runs/bocpd-features-001/V6-failed-{attempt:03d}.json'
            attempt += 1
        bf.write_json(path, {'status': 'FAILED', 'error': f'{type(error).__name__}: {error}', 'traceback': traceback.format_exc()})
        bf.audit(f'DỪNG test B1/B4: {type(error).__name__}: {error}; giữ lượt hỏng, báo root.')
        raise
