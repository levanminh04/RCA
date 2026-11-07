"""Fixture F2/F4 qua điểm vào mới, dùng metadata và kết quả phương pháp giả."""
from copy import deepcopy
from fractions import Fraction
import time
from unittest.mock import Mock, patch

from common import ROOT, RUN, digest, read, save
import p7_a4_v3 as a4
import p7_entry_v2 as v2
import p7_guard_v3 as guard
from p7_entry import InputError


def ref(path):
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path)}


def put(path, doc):
    save(path, doc)
    return ref(path)


def denied(fn, expected, exc=InputError):
    try:
        fn()
    except exc as err:
        assert expected in str(err), str(err)
        return
    raise AssertionError('đã chấp nhận đầu vào phải từ chối')


def dataset_metadata(out):
    members = {'RE2-TT': 'a' * 64, 'Nezha-OB': 'b' * 64}
    cohort = {'cohorts': {d: {'members_locked_sha256': [m]} for d, m in members.items()},
              'inventory': {d: ['r', 's'] for d in members}}
    conf = {'config_id': 'M1'}
    protocol = {'status': 'LOCKED_G3', 'cohorts_source': put(out / 'cohort.json', cohort),
                'configurations': {'M1': {'config': conf, 'sha256': v2.fingerprint(conf)}},
                'a4_record_contract': {'torai_B_seeds': [0, 1, 2], 'counts': {d: 1 for d in members},
                    'baselines': {'RE2-TT': {'worker': 'torai_B', 'method': 'torai', 'variant': 'B', 'timeout_s': 1},
                                  'Nezha-OB': {'worker': 'simplerca', 'method': 'simplerca', 'variant': 'M4', 'timeout_s': 1}},
                    'timeout_policy': {'score_phases': ['method']}}}
    protocol_ref = put(out / 'protocol.json', protocol)
    runtimes, oids = {}, {}
    for dataset, member in members.items():
        oid = oids[dataset] = 'test-' + member[:10]
        row = {'member_sha256': member, 'files': {'synthetic': {'path': 'unopened.fixture', 'bytes': 1, 'sha256': 'c' * 64}}}
        row.update({'t': 720, 'ce_history': 'verified'} if dataset == 'RE2-TT' else {'t_ns': 720_000_000_000, 'trace_guard_s': 41})
        doc = {'dataset': dataset, 'inventory': ['r', 's'], 'cases': {oid: row}}
        p = out / dataset
        runtime_ref = put(p / 'runtime.json', doc)
        private_ref = put(p / 'private.json', {'schema': 'P7-CASE-SOURCE-001', 'dataset': dataset, 'cases_by_member': {member: row}})
        receipt_path = p / 'receipt.json'
        denied(lambda: guard.attest_runtime(protocol_ref, runtime_ref, private_ref, receipt_path), 'Chưa có quyền', PermissionError)
        guard.attest_runtime(protocol_ref, runtime_ref, private_ref, receipt_path, granted=True)
        runtimes[dataset] = guard.open_runtime(protocol_ref, runtime_ref, ref(receipt_path), granted=True)
        mutations = ('time', 'path', 'digest', 'bytes', 'ce_history') if dataset == 'RE2-TT' else ('time', 'guard')
        for field in mutations:
            other = deepcopy(doc)
            changed = other['cases'][oid]
            if field == 'time':
                changed['t' if dataset == 'RE2-TT' else 't_ns'] += 60
            elif field == 'guard':
                changed['trace_guard_s'] -= 1
            elif field == 'ce_history':
                changed[field] = 'insufficient'
            else:
                name, value = {'path': ('path', 'different.fixture'), 'digest': ('sha256', 'd' * 64), 'bytes': ('bytes', 2)}[field]
                changed['files']['synthetic'][name] = value
            bad = put(p / f'changed-{field}.json', other)
            denied(lambda: guard.attest_runtime(protocol_ref, bad, private_ref, p / 'bad-receipt.json', granted=True),
                   'không khớp nguồn riêng')
            denied(lambda: guard.open_runtime(protocol_ref, bad, ref(receipt_path), granted=True), 'biên nhận không khớp')
        assert not (p / 'bad-receipt.json').exists()
    return runtimes, oids


def records(out, runtimes, oids):
    blocks = [{'key': [1], 'groups': [['r']]}]
    good = {'method': 'M1', 'variant': 'M1', 'config_id': 'M1', 'mode': 'a', 'status': 'OK',
            'worlds': {w: {'blocks': blocks} for w in a4.a4_v2.WORLDS}}
    refs = []
    with patch.object(v2, 'm1', return_value=good):
        for d, runtime in runtimes.items():
            p = out / d / 'M1'
            a4.run_slot(runtime, oids[d], 'M1', p)
            refs.append(ref(p / 'attempt.json'))
    for d, runtime in runtimes.items():
        arm, method, variant = a4.BASELINES[d]
        for seed in (0, 1, 2) if d == 'RE2-TT' else (None,):
            p = out / d / f'{arm}-{seed}'
            raw = {'method': method, 'variant': variant, 'mode': 'a', 'seed': seed,
                   'opaque_id': oids[d], 'status': 'OK', 'blocks': blocks}
            with patch.object(v2, 'baseline', return_value=[raw]):
                a4.run_slot(runtime, oids[d], arm, p, seed=seed, timeout_s=1)
            refs.append(ref(p / 'attempt.json'))
    return refs


def review_ref(out, label, attempt, classification, phase):
    key = v2.fingerprint(attempt)
    evidence = put(out / f'{label}-evidence.json', {'attempt_sha256': key, 'classification': classification, 'phase': phase})
    return put(out / f'{label}-review.json', {'schema': 'P7-FAILURE-REVIEW-001', 'assessments': {key: {
        'classification': classification, 'phase': phase, 'input_and_config_validated': True,
        'reason': 'fixture có căn cứ giả lập', 'evidence': evidence}}})


def main():
    start = time.perf_counter()
    out = RUN / 'kiem-p7-v3-001'
    out.mkdir()
    runtimes, oids = dataset_metadata(out)
    refs = records(out, runtimes, oids)
    checks = ['cohort gắn đúng mốc TT/OB, file, byte, hash, trace guard và C-e; kiểm quyền trước đọc']

    wrong = deepcopy(read(refs[-1]['path']))
    wrong['record'].update(method='baro', variant='native')
    wrong['record_sha256'] = v2.fingerprint(wrong['record'])
    wrong_ref = put(out / 'wrong-baseline.json', wrong)
    denied(lambda: a4.seal_for_a4(out / 'bad.json', refs[:-1] + [wrong_ref], runtimes), 'sai phương pháp')
    denied(lambda: a4.seal_for_a4(out / 'bad.json', refs + refs[:1], runtimes), 'thiếu, trùng hoặc sai')
    denied(lambda: a4.seal_for_a4(out / 'bad.json', refs[:-1], runtimes), 'chưa đủ')
    checks.append('bác BARO ở vế M4, bản ghi trùng và thiếu vế trước seal')

    p = out / 'blocked-runner'
    with patch.object(v2, 'm1', side_effect=InputError('fixture thiếu cấu hình')):
        denied(lambda: a4.run_slot(runtimes['RE2-TT'], oids['RE2-TT'], 'M1', p), 'thiếu cấu hình')
    assert read(p / 'attempt.json')['phase'] == 'source_or_runner'
    denied(lambda: a4.seal_for_a4(out / 'bad.json', [ref(p / 'attempt.json')] + refs[1:], runtimes), 'thiếu, trùng hoặc sai')
    p = out / 'unclassified-error'
    err = {'method': 'M1', 'variant': 'M1', 'config_id': 'M1', 'mode': 'a', 'status': 'ERROR', 'blocks': None,
           'error': 'cột metric không có trong hồ sơ nguồn: fixture'}
    with patch.object(v2, 'm1', return_value=err):
        a4.run_slot(runtimes['RE2-TT'], oids['RE2-TT'], 'M1', p)
    bad_error = [ref(p / 'attempt.json')] + refs[1:]
    denied(lambda: a4.seal_for_a4(out / 'bad.json', bad_error, runtimes), 'chưa được xác nhận nguồn')
    audit = review_ref(out, 'data-error', read(p / 'attempt.json'), 'data_error', 'source_contract')
    denied(lambda: a4.seal_for_a4(out / 'bad.json', bad_error, runtimes, failure_review_ref=audit), 'lỗi dữ liệu')
    checks.append('lỗi cấu hình và ERROR hợp đồng dữ liệu dừng trước seal')

    p = out / 'prep-timeout'
    timeout_cost = {'timed_out': True, 'wall_s': 1, 'peak_rss_mb': 1, 'read_bytes': 0, 'write_bytes': 0, 'exit_code': None}
    with patch.object(v2, 'source_selection', return_value={}), patch.object(v2, '_process', return_value=(None, timeout_cost)) as proc:
        attempt = a4.run_slot(runtimes['RE2-TT'], oids['RE2-TT'], 'torai_B', p, seed=0, timeout_s=1)
    assert proc.call_count == 1 and proc.call_args.args[2]['kind'] == 'torai_prep' and attempt['phase'] == 'torai_preparation'
    audit = review_ref(out, 'prep-timeout', attempt, 'declared_timeout', 'method')
    bad_timeout = refs[:2] + [ref(p / 'attempt.json')] + refs[3:]
    denied(lambda: a4.seal_for_a4(out / 'bad.json', bad_timeout, runtimes, failure_review_ref=audit), 'hết giờ ngoài quy tắc')
    checks.append('TORAI hết giờ ở chuẩn bị bị chặn dù có biên nhận gán nhầm sang bước phương pháp')

    label_reader = Mock(return_value={d: {o: {'root': 'r', 'cell': 'x'}} for d, o in oids.items()})
    forged = put(out / 'unvalidated-seal.json', {'schema': 'P7-A4-SEAL-001', 'failure_review_sha256': None,
                  'attempts': [read(r['path']) for r in bad_error]})
    denied(lambda: a4.evaluate_sealed(forged, runtimes, label_reader), 'chưa được xác nhận nguồn')
    label_reader.assert_not_called()
    checks.append('bản seal không qua kiểm bị chặn trước khi evaluator đọc nhãn')

    p = out / 'method-error'
    raw = {'method': 'torai', 'variant': 'B', 'mode': 'a', 'seed': 0, 'opaque_id': oids['RE2-TT'],
           'status': 'ERROR', 'blocks': [], 'error': 'fixture lỗi thuật toán trên dữ liệu hợp lệ'}
    with patch.object(v2, 'baseline', return_value=[raw]):
        attempt = a4.run_slot(runtimes['RE2-TT'], oids['RE2-TT'], 'torai_B', p, seed=0, timeout_s=1)
    audit = review_ref(out, 'method-error', attempt, 'method_error', 'method')
    path = out / 'seal.json'
    assert a4.seal_for_a4(path, refs[:2] + [ref(p / 'attempt.json')] + refs[3:], runtimes,
                         failure_review_ref=audit) == digest(path)
    denied(lambda: a4.evaluate_sealed(ref(path), runtimes, label_reader), 'seal không khớp')
    label_reader.assert_not_called()
    scored = a4.evaluate_sealed(ref(path), runtimes, label_reader, failure_review_ref=audit)
    label_reader.assert_called_once()
    assert scored['TT']['P']['delta'] == Fraction(1, 3) and scored['OB']['P']['delta'] == 0
    assert scored['TT']['P']['counts']['win'] == 1
    assert not (out / 'bad.json').exists()
    checks.append('lỗi phương pháp đã có bằng chứng giữ seed trong mẫu số và tính trượt; seal giữ hash biên nhận phân loại')
    save(out / 'summary.json', {'PASS': True, 'checks': checks, 'seconds': time.perf_counter() - start,
                               'scope': 'metadata và kết quả phương pháp giả; không mở dữ liệu khóa, không chạy phương pháp thật'})


if __name__ == '__main__':
    main()
