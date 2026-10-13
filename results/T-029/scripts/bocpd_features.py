"""T-029 B1/B4/B5: label-free features; no detector or source modification.

Run only after V6, EC2 step2a V3 and laptop step3 V2 pass. Output paths are
restricted to runs/bocpd-features-001 and features-no-label/bocpd.
"""
import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-029'
LOG = ROOT / 'tasks/T-029-p4-han-che-phat-hien/LOG.md'
sys.path.insert(0, str(ROOT / 'src'))
from p3.adapters import phat_hien

S0 = 1
CUT = 720
WS = (15, 30, 60)
THRESHOLDS = (2, 3, 5)


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')


def audit(message):
    with LOG.open('a', encoding='utf-8') as handle:
        handle.write(f'\n- {now()} — Hỗ trợ B1/B4/P1: {message}\n')


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            sha.update(block)
    return sha.hexdigest()


def write_json(path, value):
    path = Path(path)
    if path.exists():
        raise RuntimeError(f'Không ghi đè output đã có: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=1, allow_nan=False), encoding='utf-8')
    audit(f'Ghi {path.relative_to(ROOT).as_posix()}; SHA lưu trong manifest của lượt.')


def prepare(metrics):
    """Native drop_constant -> ffill -> fillna(0), before native min-max."""
    from baro.utility import drop_constant
    columns = phat_hien.cot_bocpd(metrics.columns)
    retained = drop_constant(metrics[columns])
    leading_end = {}
    for col in retained:
        present = np.flatnonzero(retained[col].notna().to_numpy())
        if len(present) and int(present[0]) > 0:
            leading_end[col] = int(present[0])
    filled = retained.ffill().fillna(0)
    return filled, leading_end, columns


def b1_at(leading_end, index, s0=S0):
    if index is None or index - 2 < s0 or index + 2 > CUT - 1:
        return {'valid': False, 'flag': None, 'columns': [], 'reason': 'Ngoài miền [i-2,i+2] thuộc Nv'}
    columns = sorted(c for c, end in leading_end.items() if index - 2 <= end <= index + 2)
    return {'valid': True, 'flag': bool(columns), 'columns': columns}


def b4_components(data, index, w, s0=S0, background=True):
    """Same jump formula; background=True enforces C/V7. False is E heuristic only."""
    valid = index is not None and index - w - s0 >= 30 and index - w >= 0 and index + w <= len(data)
    if background:
        valid = valid and index < CUT and index + w <= CUT
    if not valid:
        return None
    x = np.asarray(data, dtype=float)
    before = np.median(x[index - w:index], axis=0)
    after = np.median(x[index:index + w], axis=0)
    baseline = x[s0:index - w]
    center = np.median(baseline, axis=0)
    mad = np.median(np.abs(baseline - center), axis=0)
    jump = np.abs(after - before)
    if not (np.isfinite(before).all() and np.isfinite(after).all() and np.isfinite(mad).all()):
        raise ValueError('B4 gặp median/MAD không hữu hạn; SPEC chưa quy định')
    regular = mad > 0
    ratio = np.zeros_like(jump)
    np.divide(jump, 1.4826 * mad, out=ratio, where=regular)
    constant_change = (~regular) & (jump != 0)
    return {'before': before, 'after': after, 'mad': mad, 'jump': jump,
            'ratio': ratio, 'regular': regular, 'constant_change': constant_change}


def summary(comp, columns, flags=True):
    if comp is None:
        return {'valid': False, 'flags': {str(k): None for k in THRESHOLDS}, 'reason': 'Ngoài miền hợp lệ'}
    regular = comp['regular']
    val = comp['ratio'][regular]
    maximum = float(np.max(val)) if len(val) else None
    value = {'valid': True, 'max_ratio_positive_mad': maximum,
             'constant_change_columns': [c for c, hit in zip(columns, comp['constant_change']) if hit],
             'constant_no_change_count': int(np.sum((~regular) & (comp['jump'] == 0)))}
    if flags:
        value['flags'] = {str(k): maximum is not None and maximum >= k for k in THRESHOLDS}
        value['columns_at_threshold'] = {str(k): [c for c, r, ok in zip(columns, comp['ratio'], regular) if ok and r >= k]
                                         for k in THRESHOLDS}
    return value


def heuristic(comp, columns):
    """No B4 True/False or thresholds here; tied ratios retain equal position."""
    if comp is None:
        return {'valid': False, 'reason': 'Thiếu cửa sổ hoặc đoạn MAD dưới 30 điểm', 'columns': []}
    rows = []
    for k, col in enumerate(columns):
        rows.append({'column': col, 'median_before': float(comp['before'][k]),
                     'median_after': float(comp['after'][k]), 'mad': float(comp['mad'][k]),
                     'jump': float(comp['jump'][k]),
                     'normalized_jump': float(comp['ratio'][k]) if comp['regular'][k] else None,
                     'constant_change': bool(comp['constant_change'][k])})
    rows.sort(key=lambda row: (row['normalized_jump'] is None, -(row['normalized_jump'] or 0), row['column']))
    return {'valid': True, 'interpretation': 'Heuristic phân tích §E, không là đầu ra BOCPD hoặc cờ B4/V7', 'columns': rows}


def main(args):
    audit(f'Lệnh có ghi: T-014-main python -B -W ignore bocpd_features.py {" ".join(sys.argv[1:])}; kiểm phụ thuộc trước đọc telemetry.')
    if not (args.v3_pass and args.v2_pass):
        raise RuntimeError('Chưa có xác nhận root V3 và N-Sigma V2 PASS')
    run = OUT / 'runs/bocpd-features-001'
    target = OUT / 'features-no-label/bocpd'
    tests = [json.loads(p.read_text(encoding='utf-8')) for p in run.glob('V6*.json')]
    if not any(doc['status'] == 'PASS' and doc.get('implementation_sha256') == digest(__file__) for doc in tests):
        raise RuntimeError('V6 B1/B4 chưa PASS')
    al_path = ROOT / 'results/T-022/allowlist-dev.json'
    alarm_path = ROOT / 'results/T-025/bao-dong.json'
    allow = json.loads(al_path.read_text(encoding='utf-8'))['cases']
    alarms = json.loads(alarm_path.read_text(encoding='utf-8'))['bo_phat_hien']['bocpd']
    audit('Đọc allowlist dev và bao-dong T-025 (không đọc nhãn) cho B1/B4/B5; chuẩn bị guard SHA metrics từng ca trước đọc.')
    rows, checks, output_files = {}, [], {}
    start = time.perf_counter()
    started_at = now()
    for item in sorted(allow, key=lambda x: x['opaque_id']):
        t0 = time.perf_counter()
        oid = item['opaque_id']
        meta = item['files']['metrics.parquet']
        path = ROOT / meta['path']
        got = digest(path)
        if got != meta['sha256']:
            audit(f'DỪNG V1 metrics guard lệch {oid}; chưa đọc parquet.')
            raise RuntimeError(f'V1 lệch {oid}')
        metrics = pd.read_parquet(path)
        times = metrics['time'].to_numpy()
        if len(times) != 1441 or not np.all(np.diff(times) == 1):
            audit(f'DỪNG lưới thời gian chưa theo SPEC: {oid}.')
            raise RuntimeError('Lưới thời gian lệch')
        data, leading_end, raw_columns = prepare(metrics)
        native = phat_hien.tien_xu_ly_bocpd(metrics[raw_columns])
        expected = alarms[oid]['input_shape']['cot_sau_tien_xu_ly']
        same = len(data.columns) == native.shape[1] == expected and list(data.columns) == list(native.columns)
        checks.append({'opaque_id': oid, 'actual_d': len(data.columns), 'native_d': native.shape[1], 'expected_d': expected, 'pass': same})
        if not same:
            write_json(run / 'V3-dimension-failed.json', checks)
            audit(f'DỪNG V3 số cột lệch {oid}; không dùng features đã tính trước đó.')
            raise RuntimeError(f'V3 dimension lệch {oid}')
        columns = list(data.columns)
        alarm_indices = [int(v - times[0]) for v in alarms[oid]['alarms']]
        if alarm_indices != alarms[oid]['chi_so']:
            audit(f'DỪNG indices báo động khác chi_so T-025 ở {oid}.')
            raise RuntimeError('Ánh xạ thời gian báo động lệch')
        th = min(alarm_indices) if alarm_indices else None
        later = [i for i in alarm_indices if i >= CUT]
        plus = min(later) if later else None
        all_nv = {}
        for w in WS:
            by_index = {}
            for index in range(S0, CUT):
                by_index[str(index)] = summary(b4_components(data, index, w), columns)
            all_nv[str(w)] = by_index
        at = {str(w): summary(b4_components(data, th, w), columns) for w in WS}
        at_plus = {str(w): heuristic(b4_components(data, plus, w, background=False), columns) for w in WS}
        if plus is not None and any(not v['valid'] for v in at_plus.values()):
            audit(f'DỪNG heuristic t_hat_plus thiếu cửa sổ/MADmin30 tại {oid}; SPEC chưa quy định cách xếp cột.')
            write_json(run / 'heuristic-window-failed.json', {'opaque_id': oid, 'index': plus, 'by_w': at_plus})
            raise RuntimeError('Heuristic t_hat_plus ngoài dữ liệu')
        record = {'opaque_id': oid, 'columns': columns, 'd': len(columns), 'raw_d': len(raw_columns),
                  'source': {'metrics': meta['path'], 'metrics_sha256': got, 'alarm': str(alarm_path.relative_to(ROOT)),
                             'alarm_pointer': f'/bo_phat_hien/bocpd/{oid}'},
                  't_hat_index': th, 't_hat_plus_index': plus, 'alarms_indices': alarm_indices,
                  'B1_leading_nan_end': leading_end, 'B1_t_hat': b1_at(leading_end, th),
                  'B1_all_Nv': {str(i): b1_at(leading_end, i) for i in range(S0, CUT)},
                  'B4_t_hat': at, 'B4_all_Nv': all_nv, 'B4_t_hat_plus_heuristic': at_plus,
                  'B5': {'d': len(columns), 'cp_count_Nv': sum(S0 <= i < CUT for i in alarm_indices)}}
        dest = target / f'{oid}.json'
        write_json(dest, record)
        output_files[str(dest.relative_to(ROOT))] = digest(dest)
        rows[oid] = {'d': len(columns), 't_hat_index': th, 't_hat_plus_index': plus,
                     'seconds': round(time.perf_counter() - t0, 3)}
        audit(f'Đọc metrics dev guard PASS, tính B1/B4/B5 không nhãn {oid}, d khớp T-025; thời gian {rows[oid]["seconds"]} s.')
    write_json(run / 'V3-dimensions.json', {'status': 'PASS', 'cases': len(checks), 'checks': checks})
    output_files[str((run / 'V3-dimensions.json').relative_to(ROOT))] = digest(run / 'V3-dimensions.json')
    write_json(run / 'manifest.json', {'status': 'PASS', 'started_at': started_at, 'completed_at': now(), 'total_seconds': round(time.perf_counter() - start, 3),
                                     'script_sha256': digest(__file__), 'allowlist_sha256': digest(al_path),
                                     'alarms_sha256': digest(alarm_path), 'cases': rows, 'outputs': output_files,
                                     'no_labels_read': True, 's0': S0, 'w': WS, 'thresholds': THRESHOLDS,
                                     'B4_constant_change_separate': True,
                                     'heuristic': '§E formula only; no threshold, B4 flag, or V7 at t_hat_plus'})
    print(json.dumps({'status': 'PASS', 'cases': len(rows), 'seconds': round(time.perf_counter() - start, 3)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--v3-pass', action='store_true')
    parser.add_argument('--v2-pass', action='store_true')
    arguments = parser.parse_args()
    try:
        main(arguments)
    except Exception as error:
        audit(f'DỪNG bocpd_features.py: {type(error).__name__}: {error}. Giữ mọi output/lượt, báo root; không tự xử lý.')
        raise
