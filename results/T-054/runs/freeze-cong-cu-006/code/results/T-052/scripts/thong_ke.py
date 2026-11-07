"""A4 Q-246: công cụ danh nghĩa, không chứng minh hiệu chuẩn benchmark."""
import itertools
import math
import time
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_EVEN
from fractions import Fraction

from common import ROOT, RUN, dump, read, save, timing
import numpy as np
from p3 import danh_gia


def rounded(x):
    return Decimal(str(x)).quantize(Decimal('0.000000000001'), rounding=ROUND_HALF_EVEN)


def e04(ci):
    lo, hi = ci.get('lo'), ci.get('hi')
    if lo is None or hi is None or not all(math.isfinite(x) for x in (lo, hi)) or lo > hi:
        return {'valid': False, 'pass_formula': False, 'transfer_OB_alpha': 0.025}
    a, b = rounded(lo), rounded(hi)
    passed = a > Decimal('-0.05')
    degenerate = a == b
    text = ('đạt E-04 theo công thức; CI suy biến' if degenerate else 'đạt E-04 theo công thức') if passed else (
        'Không đạt E-04. Chưa chứng minh được không thua quá 0,05')
    return {'valid': True, 'raw': ci, 'lo_12': str(a), 'hi_12': str(b),
            'pass_formula': passed, 'degenerate': degenerate,
            'transfer_OB_alpha': 0.05 if passed and a < b else 0.025,
            'statement': text,
            'caveat': 'CI danh nghĩa; ít ô/rời rạc có thể undercoverage, kể cả CI không suy biến.'}


def sign_exact(delta, cells):
    totals = defaultdict(Fraction)
    for oid in sorted(delta):
        totals[cells[oid]] += delta[oid]
    values = [totals[c] for c in sorted(totals)]
    observed = sum(values)
    exceed = sum(sum(s * v for s, v in zip(signs, values)) >= observed
                 for signs in itertools.product((-1, 1), repeat=len(values)))
    denom = 2 ** len(values)
    return {'cell_totals': totals, 'statistic': observed / len(delta),
            'numerator': exceed, 'denominator': denom, 'p_exact': Fraction(exceed, denom),
            'effective_cells': sum(v != 0 for v in values),
            'H0': 'Vector tổng chênh từng ô bất biến khi đổi dấu nguyên ô; không tự là kiểm mọi trung bình<=0.'}


def counts(delta, cells, a, b):
    totals = defaultdict(Fraction)
    by = defaultdict(list)
    for oid, value in delta.items():
        totals[cells[oid]] += value
        by[cells[oid]].append(value)
    return {'n_cells': len(totals), 'cells_any_case_nonzero': sum(any(v != 0 for v in x) for x in by.values()),
            'cells_total_nonzero': sum(x != 0 for x in totals.values()),
            'cells_total_negative': sum(x < 0 for x in totals.values()),
            'cells_mixed_sign': sum(any(v < 0 for v in x) and any(v > 0 for v in x) for x in by.values()),
            'both_miss': sum(a[o] == b[o] == 0 for o in delta),
            'win': sum(x > 0 for x in delta.values()), 'tie': sum(x == 0 for x in delta.values()),
            'loss': sum(x < 0 for x in delta.values()), 'cell_totals': totals}


def certain(row):
    return row['status'] == 'OK' and row.get('rank_min') == row.get('rank_max') == 1


def mcnemar(a, b):
    left = sum(a[o] and not b[o] for o in a)
    right = sum(b[o] and not a[o] for o in a)
    n = left + right
    p = min(Fraction(1), Fraction(2 * sum(math.comb(n, i) for i in range(min(left, right) + 1)), 2 ** n)) if n else Fraction(1)
    return {'M1_only': left, 'baseline_only': right, 'p_two_sided_exact': p,
            'caveat': 'Theo ca; phụ thuộc giữa ca trong cùng ô. Không quyết A4.'}


def fixtures():
    start = time.perf_counter()
    checks = []
    def check(name, condition):
        assert condition, name
        checks.append(name)
    check('strict_boundary_equal_1', not e04({'lo': 0.9 - 0.95, 'hi': 0.1})['pass_formula'])
    check('strict_boundary_equal_2', not e04({'lo': 0.85 - 0.9, 'hi': 0.1})['pass_formula'])
    check('degenerate_pass_no_transfer', e04({'lo': 0.0, 'hi': 0.0})['pass_formula'] and e04({'lo': 0., 'hi': 0.})['transfer_OB_alpha'] == .025)
    check('valid_pass_transfer', e04({'lo': -.04, 'hi': .1})['transfer_OB_alpha'] == .05)
    check('missing_ci_no_transfer', not e04({'lo': None, 'hi': None})['valid'])
    for g in (3, 5, 6):
        d = {str(i): Fraction(1) for i in range(g)}
        check('signs_including_observed_' + str(g), sign_exact(d, {o: o for o in d})['p_exact'] == Fraction(1, 2 ** g))
    check('zero_cells_keep_denominator', sign_exact({'a': Fraction(0), 'b': Fraction(1)}, {'a': 'a', 'b': 'b'})['p_exact'] == Fraction(1, 2))
    seeds = [{'status': 'OK', 'rank_min': 1, 'rank_max': 1}, {'status': 'OK', 'rank_min': 1, 'rank_max': 2}, {'status': 'ERROR', 'rank_min': None, 'rank_max': None}]
    check('tie_and_error_not_certain', [certain(r) for r in seeds] == [True, False, False])
    check('mixed_seed_majority', sum(certain(r) for r in [seeds[0], seeds[0], seeds[2]]) >= 2)
    check('mcnemar_no_discordance', mcnemar({'a': False}, {'a': False})['p_two_sided_exact'] == 1)
    cells = {'a': 'x', 'b': 'x', 'c': 'y'}
    def row(x):
        return {k: x for k in danh_gia.DO_DO_BOOT} | {f'hit@{k}': x for k in (1, 5, 10)}
    # Ô khác cỡ: cặp cùng mẫu và thứ tự ô/ca; so phân vị với tính độc lập theo công thức lấy lại ô.
    table = {'M1': {'a': row(1), 'b': row(0), 'c': row(0)},
             'B': {o: row(0) for o in cells}}
    actual = danh_gia.bootstrap(table, cells)
    draw = np.random.default_rng(20261005).integers(0, 2, size=(10000, 2))
    cnt = (draw == 0).sum(axis=1)
    samples = cnt / (cnt * 2 + (2 - cnt))
    wanted = np.percentile(samples, [2.5, 97.5])
    ci = actual['hieu']['B - M1']['rr']
    check('paired_unequal_cells_and_orientation', np.allclose([ci['lo'], ci['hi']], [-wanted[1], -wanted[0]]))
    check('rerank_na_zero_retrieval', actual['phuong_phap']['B']['rerank@1(K=5)']['n_na'] == 10000)
    from m1_danh_gia import e7
    check('region_O_zero_is_NA', e7.mo_ta(['a'], {'a': ['a']}, 'a', 0)['R_ky_vong_tren_O'] is None)
    from m1 import chuoi
    bad = chuoi.chay([], [], [], [], {}, 0, {'config_id': 'bad-runner'})
    check('runner_configuration_error_before_score', bad['status'] == 'ERROR' and 'bat_tat' in bad['error'])
    save(RUN / 'fixture-a4-001.json', timing('fixtures', start, PASS=True, checks=checks,
        numpy=np.__version__, bootstrap='src/p3/danh_gia.py:208',
        caveat='Fixture kiểm phép tính và giao thức; không xác nhận hiệu chuẩn thống kê trên benchmark.'))


if __name__ == '__main__':
    fixtures()
