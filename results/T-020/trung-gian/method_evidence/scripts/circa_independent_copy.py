"""Tính lại OLS/RHT/DA từ snapshot; không import CIRCA, RCAEval hay sklearn.

Chạy: python independent_scores.py snapshot.json --out output-directory
Độc lập ở bước tính, KHÔNG độc lập ở khâu chuẩn bị mảng: raw resampling,
cắt cửa sổ, metric identities và effective parents phải kiểm riêng từ input.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy import linalg


def normal_parameters(values):
    """Mean và corrected two-pass population variance; rule nearconstant sklearn1.6."""
    a = np.asarray(values, dtype=np.float64)
    if a.ndim != 1 or not len(a) or not np.isfinite(a).all():
        raise ValueError('Residual train phải là vector hữu hạn không rỗng')
    n = len(a)
    mean = float(np.sum(a, dtype=np.float64) / n)
    centered = a - mean
    correction = float(np.sum(centered, dtype=np.float64))
    variance = float((np.sum(centered * centered, dtype=np.float64)
                      - correction ** 2 / n) / n)
    eps = np.finfo(np.float64).eps
    upper = float(n * eps * variance + (n * mean * eps) ** 2)
    constant = bool(variance <= upper)
    if variance < 0 and not constant:
        raise ValueError('Phương sai âm, không tự sàn')
    scale = 1.0 if constant else math.sqrt(variance)
    return {'mean': mean, 'variance': variance, 'scale': scale,
            'near_constant': constant, 'near_constant_upper_bound': upper,
            'n': n, 'ddof': 0}


def rht(node):
    train_y = np.asarray(node['train_y'], dtype=np.float64)
    test_y = np.asarray(node['test_y'], dtype=np.float64)
    # RCAEval tau=0: np.array(parent-series).T yields F memory order.
    # sklearn copy_X keeps order K. Do not try layouts against official scores.
    memory_order = node.get('x_memory_order', 'F')
    if memory_order not in ('C', 'F'):
        raise ValueError('x_memory_order phải là C hoặc F')
    train_x = np.array(node['train_x'], dtype=np.float64, order=memory_order)
    test_x = np.array(node['test_x'], dtype=np.float64, order=memory_order)
    if train_y.ndim != 1 or test_y.ndim != 1 or not len(test_y):
        raise ValueError('train_y/test_y phải là vector, test_y không rỗng')
    if not np.isfinite(train_y).all() or not np.isfinite(test_y).all():
        raise ValueError('y chứa NaN/Inf; không tự thay giá trị')
    reason, coef, intercept, singular, rank = None, [], None, [], None
    # Source rht split produces shape(0,0) for no effective parents.
    if train_x.size == 0:
        train_residual, test_residual = train_y.copy(), test_y.copy()
        reason = 'no_effective_parents'
    else:
        try:
            if (train_x.ndim != 2 or test_x.ndim != 2
                    or train_x.shape[0] != len(train_y)
                    or test_x.shape[0] != len(test_y)
                    or train_x.shape[1] != test_x.shape[1]
                    or not np.isfinite(train_x).all()
                    or not np.isfinite(test_x).all()):
                raise ValueError('X shape/finite không hợp lệ cho OLS')
            xmean = np.average(train_x, axis=0)
            ymean = float(np.average(train_y))
            xc = train_x - xmean
            yc = train_y - ymean
            cond = max(xc.shape) * np.finfo(xc.dtype).eps
            beta, _, rank, singular = linalg.lstsq(xc, yc, cond=cond)
            intercept = float(ymean - xmean @ beta)
            train_residual = train_y - (train_x @ beta + intercept)
            test_residual = test_y - (test_x @ beta + intercept)
            coef = beta.tolist()
            singular = singular.tolist()
            rank = int(rank)
        except ValueError as exc:
            train_residual, test_residual = train_y.copy(), test_y.copy()
            reason = 'ValueError: ' + str(exc)
    params = normal_parameters(train_residual)
    z = (test_residual - params['mean']) / params['scale']
    score = float(np.max(np.abs(z)))
    if not np.isfinite(score):
        raise ValueError('Điểm không hữu hạn; không tự sàn/cắt')
    confidence = math.erf(score / math.sqrt(2.0))
    return {'rht_score': score, 'confidence': confidence, 'coefficients': coef,
            'x_memory_order': memory_order,
            'x_memory_order_source': ('snapshot' if 'x_memory_order' in node
                                      else 'RCAEval tau=0 source default'),
            'intercept': intercept, 'ols_rank': rank, 'ols_singular_values': singular,
            'train_residual': train_residual.tolist(),
            'test_residual': test_residual.tolist(), 'test_z': z.tolist(),
            'normal': params, 'regression_route': reason or 'OLS',
            'regression_fallback': bool(reason and reason.startswith('ValueError')),
            'score_large_gt_1e6': bool(score > 1e6)}


def descendant_adjustment(scores, edges, groups, threshold=3.0):
    """DAG recurrence; giữ chính xác thứ tự group đã được snapshot cung cấp."""
    children = {label: set() for label in scores}
    for source, target in edges:
        if source in children:
            children[source].add(target)
    index = {}
    normalized_groups = []
    for i, group in enumerate(groups):
        normalized_groups.append([x for x in group if x in scores])
        for x in normalized_groups[-1]:
            if x in index:
                raise ValueError('Node lặp trong topological_groups: ' + x)
            index[x] = i
    if set(index) != set(scores):
        raise ValueError('topological_groups thiếu scored node')
    child_scores = {}
    unresolved = []
    for group in reversed(normalized_groups):
        for node in group:
            evidence = {}
            for child in sorted(children[node]):
                if child in scores:
                    evidence[child] = scores[child]
                    if scores[child] < threshold:
                        if child not in child_scores:
                            unresolved.append({'node': node, 'child': child,
                                               'same_group': index[node] == index[child]})
                        evidence.update(child_scores.get(child, {}))
            child_scores[node] = evidence
    result = {}
    for node, score in scores.items():
        addition = (max(child_scores[node].values())
                    if score >= threshold and child_scores[node] else 0.0)
        adjusted = score + addition
        result[node] = {'score': adjusted,
                        'key': [adjusted, -index[node], score],
                        'index': index[node], 'child_score': addition,
                        'child_evidence': child_scores[node]}
    return result, unresolved


def compare_numeric(actual, expected, atol, rtol):
    a = np.asarray(actual, dtype=np.float64)
    e = np.asarray(expected, dtype=np.float64)
    if a.shape != e.shape:
        return {'pass': False, 'reason': 'shape_mismatch',
                'actual_shape': list(a.shape), 'expected_shape': list(e.shape)}
    if not np.isfinite(a).all() or not np.isfinite(e).all():
        return {'pass': False, 'reason': 'nonfinite_value'}
    error = np.abs(a - e)
    limits = atol + rtol * np.abs(e)
    relative = np.zeros_like(error)
    nonzero = e != 0
    np.divide(error, np.abs(e), out=relative, where=nonzero)
    max_relative = float(np.max(relative)) if relative.size else 0.0
    zero_ref_errors = int(np.count_nonzero((~nonzero) & (error != 0)))
    return {'pass': bool(np.all(error <= limits)),
            'max_abs_error': float(np.max(error)) if error.size else 0.0,
            'max_relative_error_nonzero_reference': max_relative,
            'zero_reference_nonzero_error_count': zero_ref_errors,
            'failed_values': int(np.count_nonzero(error > limits)),
            'n_values': int(error.size),
            'abs_errors': error.tolist(), 'tolerance_limits': limits.tolist()}


def self_test():
    params = normal_parameters([1., 2., 3., 4.])
    assert params['mean'] == 2.5 and params['variance'] == 1.25
    assert normal_parameters([7., 7., 7.])['scale'] == 1.0
    node = {'train_x': [[0.], [1.], [2.], [3.]], 'test_x': [[4.]],
            'train_y': [1., 3., 5., 7.], 'test_y': [11.]}
    calculation = rht(node)
    assert abs(calculation['coefficients'][0] - 2.) < 1e-12
    assert abs(calculation['intercept'] - 1.) < 1e-12
    assert calculation['normal']['scale'] == 1.0
    assert abs(calculation['rht_score'] - 2.) < 1e-12
    da, unresolved = descendant_adjustment({'a': 4., 'b': 1., 'c': 9.},
                                          [('a', 'b'), ('b', 'c')],
                                          [['a'], ['b'], ['c']])
    assert da['a']['score'] == 13. and da['b']['score'] == 1.
    assert not unresolved
    # Đây là phản ví dụ code order trên SCC, không phải mẫu dữ liệu thật.
    edges = [('d', 'b'), ('a', 'b'), ('b', 'a'), ('a', 'c')]
    scores = {'d': 5., 'a': 1., 'b': 1., 'c': 10.}
    first, _ = descendant_adjustment(scores, edges, [['d'], ['a', 'b'], ['c']])
    second, _ = descendant_adjustment(scores, edges, [['d'], ['b', 'a'], ['c']])
    assert first['d']['score'] == 15. and second['d']['score'] == 6.
    print(json.dumps({'self_test': 'PASS', 'DAG_score_a': da['a']['score'],
                      'SCC_order_scores_d': [first['d']['score'], second['d']['score']]},
                     ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', nargs='?', type=Path)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--atol', type=float, default=1e-7)
    parser.add_argument('--rtol', type=float, default=1e-7)
    parser.add_argument('--compare', action='store_true', help='So luôn được chạy; cờ để tương thích lệnh SPEC')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if not args.self_test:
        assert args.snapshot.resolve()==Path('D:/RCA-flashticket/results/T-014/runs/example-architecture/snapshot.json').resolve()
        assert args.out.resolve()==Path('D:/RCA-flashticket/results/T-020/trung-gian/method_evidence/runs/circa-arithmetic-001').resolve()

    if args.self_test:
        self_test()
        return 0
    if not args.snapshot:
        parser.error('Cần snapshot hoặc --self-test')
    snapshot_bytes = args.snapshot.read_bytes()
    source = json.loads(snapshot_bytes.decode('utf-8'))
    out = args.out or args.snapshot.parent / 'independent'
    out.mkdir(parents=True, exist_ok=True)
    calculations, errors, checks, warnings = {}, {}, [], []
    for label, node in source['nodes'].items():
        try:
            result = rht(node)
            calculations[label] = result
            if result['score_large_gt_1e6']:
                warnings.append({'node': label, 'reason': 'score_gt_1e6',
                                 'score': result['rht_score'], 'normal': result['normal']})
            if (result['regression_fallback']
                    != bool(node.get('regression_fallback', False))):
                warnings.append({'node': label, 'reason': 'fallback_flag_differs',
                                 'independent_route': result['regression_route'],
                                 'snapshot_flag': node.get('regression_fallback')})
            for independent_key, official_key in [
                    ('rht_score', 'rht_score'), ('confidence', 'confidence'),
                    ('train_residual', 'official_train_residual'),
                    ('test_residual', 'official_test_residual')]:
                if official_key in node:
                    check = compare_numeric(result[independent_key], node[official_key], args.atol, args.rtol)
                    checks.append({'node': label, 'component': independent_key, **check})
        except Exception as exc:
            errors[label] = {'type': type(exc).__name__, 'message': str(exc)}
    da, unresolved = {}, []
    if source.get('da') and not errors:
        da, unresolved = descendant_adjustment(
            {label: value['rht_score'] for label, value in calculations.items()},
            source['graph']['edges'], source['graph'].get(
                'da_iteration_order', source['graph']['topological_groups']))
        for label, official in source['da'].items():
            if label not in da:
                errors[label + ':DA'] = {'type': 'MissingNode', 'message': 'DA official node thiếu ở independent'}
                continue
            for key in ['score', 'key', 'index', 'child_score']:
                if key in official:
                    expected = official[key]
                    # Code gốc không đặt child_score khi không tăng score.
                    if expected is None and key == 'child_score':
                        expected = 0.0
                    checks.append({'node': label, 'component': 'da_' + key,
                        **compare_numeric(da[label][key], expected, args.atol, args.rtol)})
    failed = [c for c in checks if not c['pass']]
    report = {'snapshot': str(args.snapshot.resolve()),
              'snapshot_sha256': hashlib.sha256(snapshot_bytes).hexdigest(),
              'meta': source.get('meta'),
              'atol': args.atol, 'rtol': args.rtol,
              'pass': bool(not failed and not errors and calculations and checks),
              'node_count': len(calculations), 'checks_count': len(checks),
              'failed_checks_count': len(failed), 'errors': errors, 'warnings': warnings,
              'DA_unresolved_child_evidence': unresolved,
              'DA_group_order_source': ('da_iteration_order captured from official DAScorer'
                  if 'da_iteration_order' in source['graph'] else 'topological_groups; actual set iteration chưa kiểm'),
              'scope_limit': 'Chấm điểm độc lập từ snapshot arrays; không kiểm raw preprocessing/resampling, selection, labels hoặc parent construction.',
              'OLS_library': 'scipy.linalg.lstsq; cond=max(shape)*float64_eps; centered X/y',
              'variance_algorithm': 'corrected two-pass population variance; StandardScaler sklearn1.6 nearconstant bound',
              'nodes': calculations, 'da': da, 'checks': checks}
    (out / 'comparison.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    fields = ['node', 'component', 'pass', 'max_abs_error', 'max_relative_error_nonzero_reference',
              'zero_reference_nonzero_error_count', 'failed_values', 'n_values', 'reason']
    with (out / 'comparison.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(checks)
    summary = {k: report[k] for k in ['pass', 'node_count', 'checks_count', 'failed_checks_count', 'errors']}
    summary['large_score_nodes'] = [w['node'] for w in warnings if w['reason'] == 'score_gt_1e6']
    summary['max_abs_error'] = max((c.get('max_abs_error', 0) for c in checks), default=0)
    summary['max_relative_error_nonzero_reference'] = max((c.get('max_relative_error_nonzero_reference', 0) for c in checks), default=0)
    print(json.dumps(summary, ensure_ascii=False, allow_nan=False))
    return 0 if report['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
