"""Phép thử v2: quy tắc INSUFFICIENT_NORMAL_SPANS và supervisor chạy tiếp sau lỗi phương pháp chưa phân loại.
Chỉ đọc attempt BLOCKED thật (đầu vào test đã được cấp), không chạy phương pháp."""
import copy
import json
import sys
from pathlib import Path
from unittest.mock import patch

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
sys.path[:0] = [str(ROOT / 'results/T-054/scripts'), str(ROOT / 'src')]
from bien_nhan import (Blocked, UnclassifiedMethodError, DependencyBlocked, atomic, fingerprint, read_pin, ref,
                       known_operation_error)
from dieu_phoi import supervise, status, _kind, resolve_dependency


def events(q):
    return [json.loads(line) for line in open(q / 'events.jsonl', encoding='utf-8')]


def supervisor_checks(target):
    checks = []
    target.mkdir(parents=True, exist_ok=False)
    base = {'dataset': 'RE2-TT', 'opaque_id': 'fx', 'view': 'main', 'seed': None}
    jobs = [{'slot': dict(base, arm=a, opaque_id=o), 'kind': 'synthetic', 'evaluation_mode': 'test'}
            for a, o in [('baro', 'c1'), ('tracerca', 'c1'), ('simplerca', 'c1'), ('baro', 'c2'), ('tracerca', 'c2')]]

    def make_fake(marker, seen):
        def fake(item, plan, directory, budget, current, registered, emit):
            jid = fingerprint(item['slot'])
            if jid in current:
                return False
            seen.append(item['slot']['arm'] + item['slot']['opaque_id'])
            if item['slot']['arm'] == 'tracerca' and item['slot']['opaque_id'] == 'c1':
                emit({'job_id': jid, 'state': 'BLOCKED', 'reason': 'fixture', **marker})
            else:
                emit({'job_id': jid, 'state': 'VERIFIED'})
            return False
        return fake

    for name, marker, expect_all in [('unclassified_continue', {'method_unclassified': True}, True),
                                     ('dependency_continue', {'dependency_blocked': True}, True),
                                     ('infra_stops', {}, False)]:
        q = target / name
        seen = []
        with patch('dieu_phoi._run_one', side_effect=make_fake(marker, seen)):
            supervise({'mode': 'synthetic', 'workers': 1, 'jobs': jobs}, q)
        st = status(q)
        ev = events(q)
        if expect_all:
            assert len(seen) == 5 and st['counts'] == {'VERIFIED': 4, 'BLOCKED': 1}, (name, seen, st['counts'])
            assert any(e.get('state') == 'BLOCKED_CONTINUE' for e in ev)
            assert not any(e.get('state') == 'WAIT_ERROR' for e in ev)
            seen2 = []
            with patch('dieu_phoi._run_one', side_effect=make_fake(marker, seen2)):
                supervise({'mode': 'synthetic', 'workers': 1, 'jobs': jobs}, q)
            assert seen2 == [] and not any(e.get('state') == 'WAIT_ERROR' for e in events(q)), name
            checks.append(name + '_and_resume')
        else:
            assert len(seen) == 2 and any(e.get('state') == 'WAIT_ERROR' for e in ev), (name, seen)
            checks.append(name)

    jobs_a = [{'slot': dict(base, arm='circa', opaque_id='a'), 'kind': 'synthetic', 'evaluation_mode': 'test'},
              {'slot': dict(base, arm='torai_A', opaque_id='a', seed=0), 'kind': 'synthetic',
               'evaluation_mode': 'test', 'author_source_ref': {}},
              {'slot': dict(base, arm='torai_A', opaque_id='a', seed=1), 'kind': 'synthetic',
               'evaluation_mode': 'test', 'author_source_ref': {}}]

    def fake_a(item, plan, directory, budget, current, registered, emit):
        jid = fingerprint(item['slot'])
        if item['slot']['arm'] == 'torai_A':
            emit({'job_id': jid, 'state': 'BLOCKED', 'reason': 'fx', 'method_unclassified': True})
            return False
        emit({'job_id': jid, 'state': 'VERIFIED'})
        return False

    q = target / 'A_still_halts'
    with patch('dieu_phoi._run_one', side_effect=fake_a), patch('nguon.author_source', return_value={}):
        supervise({'mode': 'synthetic', 'workers': 1, 'jobs': jobs_a,
                   'auxiliary_A_policy': 'AFTER_NON_A_VERIFIED_PREFLIGHT_AND_PRESERVE_BLOCKED'}, q,
                  authority={'torai_A_source_grant': True})
    st = status(q)
    assert st['jobs'][fingerprint(jobs_a[2]['slot'])]['reason'] == 'A_QUEUE_HALTED_BEFORE_DISPATCH', st['jobs']
    checks.append('A_unclassified_still_halts_A')

    assert _kind(UnclassifiedMethodError('x')) == {'method_unclassified': True}
    assert _kind(DependencyBlocked('x')) == {'dependency_blocked': True} and _kind(Blocked('x')) == {}
    checks.append('kind_markers')

    parent = {'slot': dict(base, arm='M1', opaque_id='d'), 'kind': 'm1'}
    child = {'slot': dict(base, arm='C-d3', opaque_id='d'), 'kind': 'cd3',
             'main_dependency': {'slot': parent['slot'], 'job_sha256': fingerprint(parent)}}
    reg = {fingerprint(parent['slot']): parent}
    for row, exc_type in [({'state': 'BLOCKED', 'method_unclassified': True}, DependencyBlocked),
                          ({'state': 'BLOCKED'}, Blocked)]:
        try:
            resolve_dependency(child, reg, {fingerprint(parent['slot']): row}, target)
        except Blocked as exc:
            assert type(exc) is exc_type, (row, type(exc))
        else:
            raise AssertionError('dependency không bị chặn')
    checks.append('dependency_blocked_marker')
    return checks


def rule_checks(attempt, policy_path, target, data_root=None):
    attempt = Path(attempt)
    checks = []
    job = read_pin(ref(attempt / 'job.json'))
    if data_root:
        job = dict(job, data_root=data_root)
    envelope = read_pin(ref(attempt / 'result.json'))
    invocation = read_pin(ref(attempt / 'invocation.json'))
    target.mkdir(parents=True, exist_ok=True)

    def with_policy(rules):
        pol = json.loads(Path(policy_path).read_bytes())
        pol['scope'] = 'LOCKED_P7'
        pol['error_rules'] = rules
        pin = atomic(target / ('policy-' + str(len(rules)) + '.json'), pol)
        return dict(job, failure_policy_ref=pin)

    v2 = with_policy(['NEW_OPERATION_WITHOUT_NORMAL_BASELINE', 'INSUFFICIENT_NORMAL_SPANS'])
    audit = known_operation_error(v2, envelope, invocation)
    assert audit['rule'] == 'INSUFFICIENT_NORMAL_SPANS' and audit['single_normal_span_operations'], audit
    checks.append({'v2_accepts': [job['slot']['arm'], job['slot']['opaque_id']], 'audit': audit})
    v1 = with_policy(['NEW_OPERATION_WITHOUT_NORMAL_BASELINE'])
    try:
        known_operation_error(v1, envelope, invocation)
    except UnclassifiedMethodError:
        checks.append('v1_policy_still_unclassified')
    else:
        raise AssertionError('v1 nhận nhầm')
    bad = copy.deepcopy(envelope)
    bad['records'][0]['error'] = 'ValueError: something else'
    try:
        known_operation_error(v2, bad, invocation)
    except UnclassifiedMethodError:
        checks.append('wrong_error_string_unclassified')
    else:
        raise AssertionError('chuỗi lỗi sai vẫn nhận')
    return checks


if __name__ == '__main__':
    out = Path(sys.argv[1])
    result = {'supervisor': supervisor_checks(out / 'supervisor')}
    if len(sys.argv) > 2:
        result['rule'] = rule_checks(sys.argv[2], sys.argv[3], out / 'rule', sys.argv[4] if len(sys.argv) > 4 else None)
    result['PASS'] = True
    atomic(out / 'summary.json', result)
    print(json.dumps(result, ensure_ascii=False, default=str)[:3000])
