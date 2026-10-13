"""T-026: kiểm evaluator bằng nhãn giả; không đọc nhãn thật hoặc chạy phương pháp.

--manifest nhận manifest nháp hoàn chỉnh sau các lượt để kiểm bốn bảng bằng
nhãn giả trước chốt. Không tạo manifest, thay bản ghi hoặc chọn theo điểm thật.
"""
import argparse
from collections import Counter
import copy
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evaluate as ev
from p3 import ban_ghi, danh_gia as dg


def fake_record(root, items, status='OK'):
    ranked = [(name, name, key) for name, key in items]
    kq = {'status': status, 'variant': 'M4', 'items': ranked if status == 'OK' else [],
          'ranking_native': [x[0] for x in items] if status == 'OK' else [],
          'observed_entities': [x[0] for x in items]}
    return ban_ghi.tao('simplerca', 'synthetic only', 'M4', 'a', kq, {}, 'synthetic', [])


def synthetic():
    cases = [
        ('first', 'A', [('A', 3), ('B', 2), ('C', 1)], 1, 1, 1.0, 1.0),
        ('top_tie', 'A', [('A', 3), ('B', 3), ('C', 1)], 1, 2, 0.5, 0.75),
        ('deep_tie', 'A', [('B', 4), ('C', 4), ('A', 2), ('D', 2), ('E', 1)], 3, 4, 0.0, 7/24),
        ('root_absent', 'Z', [('A', 3), ('B', 2)], None, None, 0.0, 0.0),
        ('short', 'B', [('A', 2), ('B', 1)], 2, 2, 0.0, 0.5),
        ('all_tied', 'A', [('A', 1), ('B', 1), ('C', 1)], 1, 3, 1/3, 11/18),
    ]
    checks = []
    for name, root, items, rmin, rmax, hit1, rr in cases:
        rec = fake_record(root, items)
        got = dg.cham_ca(rec, root)
        ev.check_case(rec, root, got)
        assert (got['rank_min'], got['rank_max']) == (rmin, rmax)
        assert math.isclose(got['hit@1'], hit1, abs_tol=1e-12)
        assert math.isclose(got['rr'], rr, abs_tol=1e-12)
        checks.append({'name': name, 'pass': True})
    failed = {}
    for status in ev.STATES[1:]:
        rec = fake_record('A', [('A', 1)], status)
        got = dg.cham_ca(rec, 'A')
        ev.check_case(rec, 'A', got)
        assert all(got[k] == 0 for k in ev.METRICS)
        failed[status] = got
        checks.append({'name': status + '_zero', 'pass': True})
    summary = dg.tong_hop(failed)
    assert summary['n'] == 4 and sum(summary['trang_thai'].values()) == 4
    assert summary['rerank@1(K=5)'] is None
    # Mẫu ô không đều phải mang toàn bộ ca, không bình quân mỗi ô như nhau.
    cells = {f'o{i}': f'cell{i//2}' if i < 18 else f'cell{i-9}' for i in range(22)}
    assert len(set(cells.values())) == 13
    assert Counter(Counter(cells.values()).values()) == {2: 9, 1: 4}
    good = dg.cham_ca(fake_record('A', [('A', 2), ('B', 1)]), 'A')
    bad = failed['NO_EVIDENCE']
    bang = {'good': {o: copy.deepcopy(good) for o in cells},
            'empty': {o: copy.deepcopy(bad) for o in cells}}
    boot = dg.bootstrap(bang, cells, B=10_000, seed=20261005)
    assert boot['n_o'] == 13
    assert boot['phuong_phap']['good']['hit@1'] == {'lo': 1.0, 'hi': 1.0, 'n_na': 0}
    assert boot['phuong_phap']['empty']['rerank@1(K=5)'] == {'lo': None, 'hi': None, 'n_na': 10_000}
    assert boot['hieu']['empty - good']['hit@1'] == {'lo': -1.0, 'hi': -1.0, 'n_na': 0}
    assert dg.bootstrap(bang, cells, B=10_000, seed=20261005) == boot
    # Kiểm số độc lập ở ô không đều: 18 ca thuộc 9 ô đôi là 1,
    # 4 ca thuộc 4 ô đơn là 0. Lấy lại ô rồi tính trên mọi ca trong mẫu.
    import numpy as np
    mixed = {o: copy.deepcopy(good if int(o[1:]) < 18 else bad) for o in cells}
    other = {o: copy.deepcopy(bad if int(o[1:]) < 18 else good) for o in cells}
    mixed_boot = dg.bootstrap({'a': mixed, 'b': other}, cells, B=10_000, seed=20261005)
    ordered_cells = sorted(set(cells.values()))
    draws = np.random.default_rng(20261005).integers(0, 13, size=(10_000, 13))
    members = [[o for o in sorted(cells) if cells[o] == c] for c in ordered_cells]
    independent_samples = []
    for draw in draws:
        sample = [o for i in draw for o in members[i]]
        independent_samples.append(sum(mixed[o]['hit@1'] for o in sample) / len(sample))
    lo, hi = np.percentile(independent_samples, [2.5, 97.5])
    pair_lo, pair_hi = np.percentile(2 * np.asarray(independent_samples) - 1, [2.5, 97.5])
    assert math.isclose(mixed_boot['phuong_phap']['a']['hit@1']['lo'], float(lo), abs_tol=1e-12)
    assert math.isclose(mixed_boot['phuong_phap']['a']['hit@1']['hi'], float(hi), abs_tol=1e-12)
    assert math.isclose(mixed_boot['hieu']['a - b']['hit@1']['lo'], float(pair_lo), abs_tol=1e-12)
    assert math.isclose(mixed_boot['hieu']['a - b']['hit@1']['hi'], float(pair_hi), abs_tol=1e-12)
    checks.append({'name': 'bootstrap13_unequal_cells_paired_NA', 'pass': True})
    # RCAEval đối chiếu mọi trạng thái và bảng không hòa, không dùng labels thật.
    rr = {'a': fake_record('A', [('A', 3), ('B', 2)]),
          'b': fake_record('B', [('A', 3), ('B', 2)]),
          **{s: fake_record('A', [('A', 1)], s) for s in ev.STATES[1:]}}
    lab = {o: {'root': 'B' if o == 'b' else 'A'} for o in rr}
    native = ev.native_summary({o: ev.native_metrics(r, lab[o]['root']) for o, r in rr.items()})
    assert dg.bang_rcaeval(rr, lab) == native
    checks.append({'name': 'rcaeval_all_states_native_parity', 'pass': True})
    # Bốn tập và mức ngẫu nhiên khi root ngoài O, có ứng viên ngoài U.
    rec = fake_record('C', [('A', 3), ('OUT', 2)])
    four = dg.bon_tap(rec, ['A', 'B', 'C'])
    assert four == {'inventory': 3, 'quan_sat': 2, 'quan_sat_ngoai_U': ['OUT'],
                    'cham': 3, 'tra_ve': 2, 'tra_ve_ngoai_U': ['OUT']}
    chance = dg.muc_ngau_nhien(rec, 'C', ['A', 'B', 'C'])
    assert chance['O_hit@1'] == 0 and chance['U_hit@1'] == 1/3
    checks.append({'name': 'four_sets_random_absent_root_outside_U', 'pass': True})
    # MicroRank top11 lấy đúng operation gốc, không điền service vắng.
    kq = {'status': 'OK', 'items': [('A_op', 'A', 3), ('B_op', 'B', 2), ('C_op', 'C', 1)],
          'ranking_native': ['A_op', 'B_op', 'C_op'], 'observed_entities': ['A', 'B', 'C'],
          'extra': {'top11_ranks': ['A_op', 'B_op'], 'service_ranks_top11': ['A', 'B']}}
    full = ban_ghi.tao('microrank', 'synthetic', 'full', 'a', kq, {}, 'synthetic', [])
    top = ev.top11_record(full)
    assert top['sets']['observed'] == 3 and top['sets']['returned'] == 2
    assert full['sets']['returned'] == 3 and top['status'] == 'OK'
    ev.check_case(top, 'C', dg.cham_ca(top, 'C'))
    assert dg.cham_ca(top, 'C')['rr'] == 0 and dg.cham_ca(full, 'C')['rr'] == 1/3
    checks.append({'name': 'microrank_top11_keeps_native_and_O', 'pass': True})
    # Kiểm độc lập phải bắt sai hạng/khóa, không chỉ tính lại số đẹp.
    invalid = fake_record('A', [('A', 3), ('B', 2)])
    invalid['entity_ranking'][0]['key'] = [float('nan')]
    try:
        ev.independent_metrics(invalid, 'A')
    except ValueError:
        pass
    else:
        raise AssertionError('nonfinite key accepted')
    checks.append({'name': 'invalid_key_rejected', 'pass': True})
    return {'kind': 'synthetic_only', 'labels_read': False, 'methods_called': False,
            'checks': checks, 'n_checks': len(checks), 'pass': True,
            'bootstrap_cell_sizes': dict(Counter(cells.values()))}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    ap.add_argument('--manifest')
    ap.add_argument('--plan', help='Kế hoạch đã khai trước, thêm hash bản ghi trong RAM để kiểm nhãn giả')
    args = ap.parse_args()
    doc = synthetic()
    if args.manifest and args.plan:
        ap.error('chỉ nhận một trong --manifest hoặc --plan')
    if args.manifest or args.plan:
        source_path = args.manifest or args.plan
        if args.plan:
            draft = ev.read_json(ev.local(args.plan))
            draft['src_p3_sha256'] = draft['src_p3']['tong']
            draft['plan_path'] = args.plan
            draft['plan_sha256'] = ev.sha(ev.local(args.plan))
            unique = {}
            for table in draft['tables'].values():
                for meta in table['records']:
                    meta['sha256'] = ev.sha(ev.local(meta['path']))
                    unique.setdefault(meta['path'], meta)
            draft['unique_records'] = list(unique.values())
            manifest_path = draft
        else:
            manifest_path = ev.local(args.manifest)
        manifest, allow, records, metas, universe = ev.load_manifest(manifest_path, require_frozen=False)
        labels = ev.fake_labels(allow, universe)
        tables, validation = ev.score_tables(records, metas, labels, universe)
        doc['actual_records_fake_labels'] = {'manifest_or_plan': source_path,
                                             'manifest_or_plan_sha256': ev.sha(ev.local(source_path)),
                                             'counts': {t: {'n_cases': x['n_cases'], 'n_cells_fake': x['n_cells']} for t, x in tables.items()},
                                             'validation': validation}
        doc['real_labels_parsed'] = False
    doc['script_sha256'] = ev.sha(__file__)
    doc['evaluator_script_sha256'] = ev.sha(ev.__file__)
    doc['src_p3_sha256'] = ev.code_hash()
    ev.dump(args.output, doc)
    print(json.dumps({'output': args.output, 'checks': doc['n_checks'], 'pass': True, 'labels_read': False}, ensure_ascii=True), flush=True)


if __name__ == '__main__':
    main()
