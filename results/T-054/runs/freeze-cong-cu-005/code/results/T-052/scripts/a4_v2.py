"""Ghép cặp và áp dụng A4 đã duyệt. Các độ nhạy chưa khóa được đánh dấu riêng."""
from bisect import bisect_left
from collections import defaultdict
from fractions import Fraction
from math import lcm

import numpy as np

from bang_doc_lap import exact_score
from p3 import danh_gia
from thong_ke import certain, counts, e04, mcnemar

WORLDS = ('P', 'S_lo', 'S_hi')


def ob_pass(p, alpha):
    return p <= alpha


def cell_sign_exact(delta, cells):
    totals = defaultdict(Fraction)
    for oid, value in delta.items():
        totals[cells[oid]] += value
    scale = lcm(*(v.denominator for v in totals.values()))
    ints = [int(scale * totals[key]) for key in sorted(totals)]

    def signed_sums(values):
        sums = [0]
        for value in values:
            sums = [s - value for s in sums] + [s + value for s in sums]
        return sums

    half = len(ints) // 2
    right = sorted(signed_sums(ints[half:]))
    observed = sum(ints)
    exceed = sum(len(right) - bisect_left(right, observed - s) for s in signed_sums(ints[:half]))
    denominator = 2 ** len(ints)
    return {'p_exact': Fraction(exceed, denominator), 'numerator': exceed, 'denominator': denominator,
            'effective_cells': sum(bool(v) for v in ints), 'cell_totals': totals,
            'H0': 'Bất biến dấu vector tổng chênh theo ô, gồm cả ô tổng 0.'}


def _score(record, root, world=None):
    if world is not None and record['status'] == 'OK':
        record = dict(record, blocks=record['worlds'][world]['blocks'])
    if record['status'] not in {'OK', 'ERROR', 'TIMEOUT', 'NO_EVIDENCE', 'UNSUPPORTED'}:
        raise ValueError('trạng thái A4 chưa được khai')
    return exact_score(record, root)


def _pairs(left, right, labels, seeds):
    if not left or set(left) != set(right) or set(left) != set(labels):
        raise ValueError('thiếu cặp/nhãn so với tập đã khai')
    for oid, records in right.items():
        if len(records) != len(seeds) or {r.get('seed') for r in records} != set(seeds):
            raise ValueError(f'seed thiếu, trùng hoặc ngoài khai báo: {oid}')
    return {oid: labels[oid]['cell'] for oid in sorted(left)}


def case_permutation_candidate(delta, *, draws=10000, seed=20261005):
    """Ứng viên độ nhạy hai phía; đổi dấu từng ca, không điều khiển A4."""
    values = np.array([float(delta[o]) for o in sorted(delta)])
    observed = abs(values.sum())
    rng = np.random.default_rng(seed)
    signs = 2 * rng.integers(0, 2, size=(draws, len(values))) - 1
    exceed = int(np.count_nonzero(np.abs(signs @ values) >= observed - 1e-12))
    return {'p': Fraction(exceed + 1, draws + 1), 'draws': draws, 'seed': seed,
            'status': 'CANDIDATE_NOT_LOCKED', 'limit': 'Ca cùng ô có thể phụ thuộc; chỉ độ nhạy.'}


def _excluded_candidate(left, right):
    error_status = {'ERROR', 'TIMEOUT'}
    excluded = sorted(oid for oid, row in left.items() if row['status'] in error_status
                      or any(s['status'] in error_status for s in right[oid]))
    return {'kept': sorted(set(left) - set(excluded)), 'excluded': excluded,
            'status': 'CANDIDATE_NOT_LOCKED',
            'rule': 'Loại cả cặp nếu bất kỳ phương pháp hoặc seed định trước có ERROR/TIMEOUT. Giữ NO_EVIDENCE/UNSUPPORTED. Không tính lại seed trên tập con.'}


def _mean_scores(scored):
    return {k: sum(r[k] for r in scored) / len(scored)
            for k in (*danh_gia.DO_DO_BOOT, 'RR', 'Hit5_Q')}


def evaluate(tt, ob, *, torai_seeds, expected_counts=(60, 34)):
    """Dùng bản ghi đã seal và nhãn từ evaluator; nhận đúng hai cặp A4."""
    if len(torai_seeds) != 3 or len(set(torai_seeds)) != 3:
        raise ValueError('A4 cần ba seed TORAI khác nhau đã khai')
    results = {}
    for dataset, (left, right, labels), seeds, expected in (
        ('TT', tt, torai_seeds, expected_counts[0]), ('OB', ob, (None,), expected_counts[1]),
    ):
        cells = _pairs(left, right, labels, seeds)
        if len(cells) != expected:
            raise ValueError('số ca A4 khác tập đã khai')
        b_seed = {oid: [_score(r, labels[oid]['root']) for r in right[oid]] for oid in cells}
        b = {oid: _mean_scores(b_seed[oid]) for oid in cells}
        excluded = _excluded_candidate(left, right)
        worlds = {}
        for world in WORLDS:
            a = {oid: _score(left[oid], labels[oid]['root'], world) for oid in cells}
            metric = 'RR' if dataset == 'TT' else 'Hit5_Q'
            ma = {oid: a[oid][metric] for oid in cells}
            mb = {oid: b[oid][metric] for oid in cells}
            delta = {oid: ma[oid] - mb[oid] for oid in cells}
            tally = counts(delta, cells, ma, mb)
            boot = danh_gia.bootstrap({'M1': a, 'baseline': b}, cells)
            ci = boot['hieu']['M1 - baseline']['rr' if dataset == 'TT' else 'hit@5']
            result = {'delta': sum(delta.values()) / len(delta), 'CI': ci, 'counts': tally,
                      'cell_sign_at_zero': cell_sign_exact(delta, cells)}
            if dataset == 'TT':
                decision = e04(ci)
                decision['statement'] = decision.get('statement', 'CI không hợp lệ') + (
                    f'; {tally["cells_total_nonzero"]} ô tổng khác 0, {tally["cells_total_negative"]} ô M1 thua, '
                    f'{tally["both_miss"]} ca cả hai trượt')
                result['E04'] = decision
                result['case_permutation_candidate'] = case_permutation_candidate(delta)
                ca = {oid: certain(a[oid]) for oid in cells}
                for key, threshold in [('majority', 2), ('all', 3)]:
                    cb = {oid: sum(certain(s) for s in b_seed[oid]) >= threshold for oid in cells}
                    result['McNemar_' + key] = mcnemar(ca, cb)
            kept = excluded['kept']
            result['error_excluded_candidate'] = dict(excluded, delta=(
                sum(delta[o] for o in kept) / len(kept) if kept else None))
            worlds[world] = result
        results[dataset] = worlds
    alpha = Fraction(str(results['TT']['P']['E04']['transfer_OB_alpha']))
    for world, result in results['OB'].items():
        result['alpha_from_TT_P'] = alpha
        result['pass_formula'] = ob_pass(result['cell_sign_at_zero']['p_exact'], alpha)
        result['decision_world'] = world == 'P'
    return results
