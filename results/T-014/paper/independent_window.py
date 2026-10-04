"""Kiểm mảng snapshot từ raw metrics trên đúng ca dev đã chọn; không gọi code tác giả.

python independent_window.py --mode example-architecture --out paper/window-example
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from independent_scores import compare_numeric


def forward_fill(values):
    """Inf->NaN; lấy quan sát finite gần nhất; prefix thiếu->0 như runner đã chốt."""
    a = np.asarray(values, dtype=np.float64).copy()
    finite = np.isfinite(a)
    prior = np.maximum.accumulate(np.where(finite, np.arange(len(a)), -1))
    a[prior >= 0] = a[prior[prior >= 0]]
    a[prior < 0] = 0.0
    return a


def prepare(raw, detect_time, normal):
    time = np.asarray(raw['time'], dtype=np.float64)
    if normal:
        selection = np.flatnonzero(time < detect_time)
    else:
        before = np.flatnonzero(time < detect_time)[-300:]
        after = np.flatnonzero(time >= detect_time)[:300]
        selection = np.concatenate([before, after])
    all_cols, dropped = {}, []
    for name in raw.columns:
        if name == 'time' or name.endswith('_latency-50'):
            continue
        values = forward_fill(raw[name])[selection]
        converted = name.replace('_latency-90', '_latency') if name.endswith('_latency-90') else name
        if converted in all_cols:
            raise ValueError('Rename làm trùng metric: ' + converted)
        if np.any(values != values[0]):
            all_cols[converted] = values / 1e6 if name.endswith('_mem') else values
        else:
            dropped.append(converted)
    return time[selection], all_cols, dropped


def resample(time, values, start, end, interval=1):
    """Mean trong bin; nội suy tuyến tính theo thời gian; fill hai đầu nearest.

    Không gọi pandas.resample, interpolate hay DataLoader.preprocess.
    Bin0 có origin=start; synthetic NaN tại hai đầu chỉ tạo đủ grid.
    """
    if end < start or interval <= 0:
        raise ValueError('Boundary/interval không hợp lệ')
    mask = (time >= start) & (time <= end)
    source_time, source_value = time[mask], values[mask]
    if not len(source_time):
        return None, {'source_count': 0}
    n = int(np.floor((end - start) / interval)) + 1
    grid = start + np.arange(n, dtype=np.float64) * interval
    bins = np.floor((source_time - start) / interval).astype(int)
    finite = np.isfinite(source_value)
    counts = np.bincount(bins[finite], minlength=n)
    sums = np.bincount(bins[finite], weights=source_value[finite], minlength=n)
    sampled = np.full(n, np.nan, dtype=np.float64)
    present = counts > 0
    sampled[present] = sums[present] / counts[present]
    sampled = np.interp(grid, grid[present], sampled[present])
    return sampled, {
        'source_count': int(len(source_time)), 'grid_count': n,
        'source_first': float(source_time.min()), 'source_last': float(source_time.max()),
        'filled_bins': int((~present).sum()), 'duplicate_bins': int((counts > 1).sum()),
        'left_extrapolated_bins': int(np.count_nonzero(grid < source_time.min())),
        'right_extrapolated_bins': int(np.count_nonzero(grid > source_time.max())),
    }


def self_test():
    a = forward_fill([np.nan, 1., np.inf, 4.])
    assert a.tolist() == [0., 1., 1., 4.]
    a, report = resample(np.array([0., 0., 2.]), np.array([2., 4., 7.]), 0, 3)
    assert a.tolist() == [3., 5., 7., 7.]
    assert report['duplicate_bins'] == 1 and report['filled_bins'] == 2


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--task-root', type=Path, default=Path('results/T-014'))
    parser.add_argument('--mode', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    self_test()
    selected = json.loads((args.task_root / 'runs/selection-before-scores.json').read_text(encoding='utf-8'))['selected']
    allowed = json.loads((args.task_root / 'runs/inventory.json').read_text(encoding='utf-8'))
    allowed_cases = {r['case'] for r in allowed}
    if len(allowed_cases) != 30 or selected not in allowed_cases:
        raise ValueError('Không có đúng danh sách 30 ca dev và ca đã chọn')
    row = next(r for r in allowed if r['case'] == selected)
    raw_path = Path(row['source']).resolve()
    forbidden = any(p.lower() == 'locked' for p in raw_path.parts)
    if forbidden or raw_path.parent.name != selected or not selected.startswith('re2tt_'):
        raise ValueError('Raw source không thuộc ca dev đã chọn')
    snapshot_path = args.task_root / 'runs' / args.mode / 'snapshot.json'
    snapshot_bytes = snapshot_path.read_bytes()
    source = json.loads(snapshot_bytes.decode('utf-8'))
    raw = pd.read_parquet(raw_path)
    normal = args.mode.startswith('normal-normal')
    raw_time, prepared, constants = prepare(raw, row['inject_time'], normal)
    meta = source['meta']
    start, end = meta['detect_time'] - 120, meta['current']
    train_count, test_count = meta['train_window'], meta['test_window']
    series, pruning, resampling = {}, {}, {}
    for label in source['graph']['nodes']:
        if label not in prepared:
            pruning[label] = 'missing_from_prepared_or_constant'
            continue
        values, info = resample(raw_time, prepared[label], start, end)
        resampling[label] = info
        if values is None or len(set(values)) == 1:
            pruning[label] = 'missing_in_range_or_constant_after_resample'
        else:
            series[label] = values
    checks, parent_checks = [], []
    edges = source['graph']['edges']
    for label, node in source['nodes'].items():
        if label not in series:
            checks.append({'node': label, 'component': 'availability', 'pass': False,
                           'reason': pruning.get(label, 'missing_label')})
            continue
        parents = node['parents']
        expected_parents = {a for a, b in edges if b == label and a in series}
        parent_checks.append({'node': label, 'pass': set(parents) == expected_parents,
                              'snapshot_effective_parents': parents,
                              'graph_expected_effective_parents': sorted(expected_parents)})
        y = series[label]
        if parents:
            px = np.column_stack([series[p][:train_count] for p in parents])
            tx = np.column_stack([series[p][-test_count:] for p in parents])
        else:
            # split_data uses shape(0,0), but .tolist() serializes it as [];
            # JSON loses the second empty dimension. Compare JSON representation.
            px, tx = np.array([]), np.array([])
        for component, actual in [('train_y', y[:train_count]), ('test_y', y[-test_count:]),
                                  ('train_x', px), ('test_x', tx)]:
            check = compare_numeric(actual, node[component], 1e-7, 1e-7)
            checks.append({'node': label, 'component': component, **check})
    dropped = sorted(set(source['graph']['nodes']) - set(source['nodes']))
    expected_dropped = sorted(set(source['graph']['nodes']) - set(series))
    report = {
        'mode': args.mode, 'case': selected, 'raw_source': str(raw_path),
        'snapshot': str(snapshot_path.resolve()),
        'snapshot_sha256': hashlib.sha256(snapshot_bytes).hexdigest(),
        'raw_rows': len(raw), 'raw_columns': len(raw.columns),
        'inject_time_from_allowlisted_metadata': row['inject_time'],
        'window_start': start, 'window_end': end, 'grid_seconds': 1,
        'train_timestamps': [start + i for i in range(train_count)],
        'test_timestamps': [end - test_count + 1 + i for i in range(test_count)],
        'normal_mode': normal, 'preparation_selection_rows': len(raw_time),
        'preparation_constants': constants, 'raw_to_grid': resampling, 'pruned': pruning,
        'same_scored_nodes': set(series) == set(source['nodes']),
        'dropped_nodes': dropped, 'independent_expected_dropped_nodes': expected_dropped,
        'checks': checks, 'parent_checks': parent_checks,
        'scope_limit': 'Kiểm raw metric->preprocessing->1s arrays và parents so với snapshot graph; không xác minh trace->graph hoặc true causal graph.',
        'pass': bool(series and set(series) == set(source['nodes'])
                     and all(c['pass'] for c in checks) and all(c['pass'] for c in parent_checks)),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / 'window-comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    summary = {'pass': report['pass'], 'mode': args.mode, 'score_nodes': len(source['nodes']),
               'array_checks': len(checks), 'failed_arrays': sum(not c['pass'] for c in checks),
               'failed_parents': sum(not c['pass'] for c in parent_checks),
               'same_scored_nodes': report['same_scored_nodes'],
               'max_abs_error': max((c.get('max_abs_error', 0.) for c in checks), default=0.)}
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
