"""Fixture F2–F4 chỉ đọc output dev và dùng payload tổng hợp có sẵn."""
import copy
import shutil
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from common import OUT, ROOT, RUN, digest, read, save
from a4_v2 import cell_sign_exact, evaluate, ob_pass
from thong_ke import sign_exact
import p7_entry_v2 as entry


def denied(fn, exc=entry.InputError):
    try:
        fn()
    except exc:
        return
    raise AssertionError('fixture được chấp nhận khi phải từ chối')


def policy_checks(out, protocol):
    fake = OUT / 'fixtures-p7-001'
    checks = []
    for dataset, folder in [('RE2-TT', 'tt'), ('Nezha-OB', 'ob')]:
        old = read(fake / (dataset + '-manifest.json'))
        record = copy.deepcopy(next(iter(old['cases'].values())))
        repo = out / dataset
        files = {}
        for name, metadata in record['files'].items():
            relative = metadata['path']
            target = repo / ('data/locked/rcaeval-re2tt-60/synthetic/' + name if dataset == 'RE2-TT' else relative)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(fake / folder / relative, target)
            metadata['path'] = target.relative_to(repo).as_posix()
            files[name] = metadata
        record['files'] = files
        member = record['member_sha256']
        oid = 'test-' + member[:10]
        cohort = {'cohorts': {dataset: {'members_locked_sha256': [member]}}, 'inventory': {dataset: old['inventory']}}
        manifest = {'dataset': dataset, 'inventory': old['inventory'], 'cases': {oid: record}}
        save(repo / 'cohort.json', cohort)
        doc = dict(protocol, status='LOCKED_G3', cohorts_source={'path': 'cohort.json', 'sha256': digest(repo / 'cohort.json')})
        save(repo / 'protocol.json', doc)
        save(repo / 'runtime.json', manifest)
        args = (repo / 'protocol.json', digest(repo / 'protocol.json'), repo / 'runtime.json', digest(repo / 'runtime.json'))
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('đọc trước quyền')):
            denied(lambda: entry.open_runtime(*args), PermissionError)
        with patch.object(entry, 'ROOT', repo):
            runtime = entry.open_runtime(*args, granted=True)
            bad = dict(manifest, cases={})
            save(repo / 'runtime-incomplete.json', bad)
            denied(lambda: entry.open_runtime(*args[:2], repo / 'runtime-incomplete.json',
                                              digest(repo / 'runtime-incomplete.json'), granted=True))
        selection = entry.source_selection(runtime.manifest, oid, repo=repo)
        assert selection
        bad = copy.deepcopy(manifest)
        next(iter(bad['cases'][oid]['files'].values()))['path'] = '../not-allowed'
        with patch.object(entry.selector, 'sha256_file', side_effect=AssertionError('đọc trước kiểm locator')):
            denied(lambda: entry.source_selection(bad, oid, repo=repo))
        bad = copy.deepcopy(manifest)
        next(iter(bad['cases'][oid]['files'].values()))['sha256'] = '0' * 64
        denied(lambda: entry.source_selection(bad, oid, repo=repo))
        denied(lambda: entry.m1(runtime, oid, 'M1', {}))
        with patch.object(entry, 'source_selection', return_value=selection):
            for arm in ('M1', 'T12-on'):
                result = entry.m1(runtime, oid, arm, protocol['configurations'][arm]['config'])
                assert result['status'] in ('OK', 'NO_EVIDENCE'), result.get('error')
        checks.append(dataset + ': quyền, cohort ngoài runtime, gốc thật trên repo giả, hash, M1, T12')
        if dataset == 'RE2-TT':
            record['ce_history'] = 'insufficient'
            with patch.object(entry.selector, 'sha256_file', side_effect=AssertionError('đọc khi C-e thiếu hỗ trợ')):
                assert entry.source_selection(manifest, oid, repo=repo, view='ce') is None
            checks.append('TT: thiếu lịch sử C-e tách khỏi V0 và hạng')
    return checks


def statistics_checks():
    cells = {'a': 'x', 'b': 'x', 'c': 'y'}
    delta = {'a': Fraction(1, 3), 'b': Fraction(-1, 3), 'c': Fraction(3, 4)}
    assert cell_sign_exact(delta, cells)['p_exact'] == sign_exact(delta, cells)['p_exact'] == Fraction(1, 2)
    assert ob_pass(Fraction(1, 20), Fraction(1, 20)) and not ob_pass(Fraction(51, 1000), Fraction(1, 20))
    def record(status='OK', seed=None, first=True):
        groups = [['r'], ['other']] if first else [['other'], ['r']]
        return {'status': status, 'seed': seed, 'blocks': [{'groups': groups, 'key': [1]}] if status == 'OK' else []}
    def m1(status='OK'):
        row = record(status)
        row['worlds'] = {'P': record(), 'S_lo': record(first=False), 'S_hi': record()}
        return row
    labels = {o: {'root': 'r', 'cell': c} for o, c in cells.items()}
    left = {'a': m1(), 'b': m1(), 'c': m1('ERROR')}
    tt = {o: [record('ERROR' if (o == 'c' or (o == 'a' and s == 2)) else 'OK', s)
              for s in range(3)] for o in cells}
    ob = {o: [record('ERROR' if o == 'c' else 'OK')] for o in cells}
    result = evaluate((left, tt, labels), (left, ob, labels), torai_seeds=(0, 1, 2), expected_counts=(3, 3))
    primary, sensitivity = result['TT']['P'], result['TT']['S_lo']
    assert primary['counts']['both_miss'] == 1 and primary['counts']['cells_total_nonzero'] == 1
    assert primary['E04']['pass_formula'] != sensitivity['E04']['pass_formula']
    assert primary['McNemar_majority'] != primary['McNemar_all']
    assert primary['error_excluded_candidate']['kept'] == ['b']
    assert 'cả hai trượt' in primary['E04']['statement']
    return ['đảo dấu chính xác gồm ô 0', 'p bằng ngưỡng', 'worlds khác cách đọc',
            'ít ô hữu hiệu và cả hai trượt', 'TORAI lẫn seed và bản nhạy loại nguyên cặp']


def main():
    out = RUN / 'kiem-sua-002'
    out.mkdir()
    protocol = read(OUT / 'giao-thuc-p7-a-002.json')
    save(out / 'summary.json', {'PASS': True, 'checks': policy_checks(out, protocol) + statistics_checks(),
                               'inputs': 'Chỉ fixture tổng hợp; F3 chạy ca dev thật vẫn chờ quyền.'})


if __name__ == '__main__':
    main()
