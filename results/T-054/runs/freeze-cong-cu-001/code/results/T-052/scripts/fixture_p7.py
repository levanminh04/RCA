"""Fixture qua đúng điểm vào P7; dữ liệu tổng hợp từ bộ sinh T-044."""
import copy
import hashlib
import sys
import time
from unittest.mock import patch

from common import ROOT, RUN, digest, dump, metadata, read, save, timing
import p7_entry as entry


def main():
    start = time.perf_counter()
    target = ROOT / 'results/T-052/fixtures-p7-001'
    target.mkdir()
    sys.path.insert(0, str(ROOT / 'results/T-044/tests'))
    from test_adapter import _re2, _nezha, U_S
    from p3 import nezha
    paths = {}
    paths['RE2-TT'], _, _ = _re2(target / 'tt')
    paths['Nezha-OB'], _ = _nezha(target / 'ob')
    _, config, _ = metadata()
    config = copy.deepcopy(config)
    config['config_id'] = 'M1'
    checks, records = [], []
    for ds, source in paths.items():
        row = copy.deepcopy(read(source)['cases'][0])
        root = source.parent
        for meta in row['files'].values(): meta['bytes'] = (root / meta['path']).stat().st_size
        member = hashlib.sha256(('fixture-' + ds).encode()).hexdigest()
        row['member_sha256'] = member
        if ds == 'RE2-TT': row['t'] = 1000
        oid = 'fixture-0123456789'
        manifest = {'dataset': ds, 'inventory': U_S if ds == 'RE2-TT' else nezha.UNIVERSE,
                    'members_locked': [member], 'cases': {oid: row}}
        save(target / (ds + '-manifest.json'), manifest)
        with patch('pathlib.Path.open', side_effect=AssertionError('data I/O before permission')):
            try: entry.select(manifest, oid, root, fixture=True)
            except PermissionError: checks.append(ds + ': permission_before_IO')
            else: raise AssertionError('missing permission guard')
        def denied(name, doc, ident=oid):
            try: entry.select(doc, ident, root, granted=True, fixture=True)
            except entry.InputError: checks.append(ds + ': ' + name)
            else: raise AssertionError(name)
        denied('outside_cohort', manifest, 'fixture-0000000000')
        bad = copy.deepcopy(manifest); bad['cases'][oid]['member_sha256'] = '0' * 64
        denied('wrong_membership', bad)
        bad = copy.deepcopy(manifest); next(iter(bad['cases'][oid]['files'].values()))['path'] = '../outside.parquet'
        denied('traversal', bad)
        bad = copy.deepcopy(manifest); next(iter(bad['cases'][oid]['files'].values()))['sha256'] = '0' * 64
        denied('bad_hash', bad)
        bad = copy.deepcopy(manifest); bad['cases'][oid]['root'] = 'HIDDEN_ROOT_FOR_EVALUATOR'
        denied('recursive_labels', bad)
        actual = entry.m1(manifest, oid, root, config, granted=True, fixture=True)
        assert actual['status'] in ('OK', 'NO_EVIDENCE'), actual.get('error')
        assert 'C-d3' not in actual['extra']['doi_chung']
        checks.append(ds + ': real_M1_reader_and_separated_cd3')
        other = 'fixture-abcdef0123'
        renamed = copy.deepcopy(manifest)
        renamed['cases'] = {other: renamed['cases'].pop(oid)}
        second = entry.m1(renamed, other, root, config, granted=True, fixture=True)
        assert dump(actual) == dump(second)
        checks.append(ds + ': opaque_rename_same_method_record')
        bad_config = copy.deepcopy(config)
        bad_config['tham_so_E3']['ghi_chu'] = oid
        try: entry.m1(manifest, oid, root, bad_config, granted=True, fixture=True)
        except (entry.InputError, Exception) as exc:
            assert isinstance(exc, entry.InputError), type(exc).__name__
            checks.append(ds + ': identity_value_rejected')
        else: raise AssertionError('identity leak not rejected')
        counts = []
        def spy(payload, t):
            assert isinstance(t, int) and isinstance(payload, dict)
            assert not {'root', 'fault', 'cell', 'opaque_id', 'files', 'case_dir'} & set(payload)
            counts.append((t, sorted(payload)))
            return {'status': 'SPY_ONLY'}
        for method in entry.METHODS:
            entry.baseline(manifest, oid, root, method, granted=True, fixture=True,
                           spies={method: spy})
        assert len(counts) == 6
        checks.append(ds + ': all_six_baseline_reader_routes')
        records.append(actual)
    output = target / 'method-records.json'
    sha = entry.seal(output, records)
    called = []
    def labels():
        called.append(True)
        return {'root': 'HIDDEN_ROOT_FOR_EVALUATOR'}
    try: entry.join_labels(output, '0' * 64, labels)
    except entry.InputError: pass
    else: raise AssertionError('bad seal accepted')
    assert not called
    entry.join_labels(output, sha, labels)
    assert called == [True]
    checks.append('labels_only_after_seal_verification')
    save(RUN / 'fixture-p7-001.json', timing('p7_fixtures', start, PASS=True, checks=checks,
          source_helpers={'path': 'results/T-044/tests/test_adapter.py', 'sha256': digest('results/T-044/tests/test_adapter.py')},
          record_sha256=sha, raw_test_opened=False,
          limits=['Baseline routing tested with spies; not baseline scientific validation or runtime measurement.',
                  'Fixture validates flow; actual test membership and source inventory materialize only after separate permission.']))


if __name__ == '__main__':
    main()
