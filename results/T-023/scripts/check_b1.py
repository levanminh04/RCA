"""Synthetic known-answer fixtures; no raw/archive input."""
import copy
import io
import json
from pathlib import Path
from b1_reader import Gate, Selector, admitted_logs, admitted_spans, stream_array

OUT = Path(__file__).resolve().parents[1]


def main():
    policy = {'hypotheses_seconds': {'H0': 0, 'H+8': 28800, 'H-8': -28800},
              'intervals': [{'session': 'test', 'role': 'test', 'start_s': 100000, 'end_s': 100010},
                            {'session': 'unlabelled', 'role': 'unlabelled', 'start_s': 200000, 'end_s': 200010}]}
    decoded = []
    def decoder(raw):
        assert b'CANARY' not in raw, 'semantic decoder saw forbidden content'
        decoded.append(raw)
        return json.loads(raw)
    def span(t, pid='p', **extra):
        return {'traceID': 'a', 'spanID': 'b', 'processID': pid, 'duration': 1000000,
                'tags': [{'key': 'quoted', 'value': 'startTime:100000000000 { ] escaped "'}],
                **extra, 'startTime': t * 1e6}
    spans = [span(100000, 'CANARY'), span(100000-28800, 'CANARY'), span(100000+28800, 'CANARY'),
             span(200000, 'CANARY'), span(99999, 'CANARY'), span(100010, 'CANARY'), span(50000)]
    env = json.dumps({'traceID': 'CANARY_ENVELOPE', 'processes': {'p': {'serviceName': 'safe'},
                     'CANARY': {'serviceName': 'CANARY_PROCESS'}}, 'spans': spans}).encode()
    gate = Gate(policy, 'dev')
    got = list(admitted_spans(env, gate, decoder))
    assert len(got) == 1 and got[0][1] == 'safe'
    assert gate.counts['denied_B1'] == 6 and len(decoded) == 2
    # Missing/duplicate clock, shadow nested clock, escaped braces and trailing bytes.
    bad = b'{"processes":{},"spans":[{"tags":{"startTime":1},"duration":1},{"startTime":50000000000,"startTime":50000000001,"duration":1}]}'
    gate2 = Gate(policy, 'dev')
    assert list(admitted_spans(bad, gate2, decoder)) == [] and gate2.counts['unknown_clock'] == 2
    alias = b'{"processes":{"p":{"serviceName":"CANARY"}},"spans":[{"startTime":50000000000,"\\u0073tartTime":100000000000,"duration":0,"processID":"p"}]}'
    alias_gate = Gate(policy, 'dev')
    assert list(admitted_spans(alias, alias_gate, decoder)) == [] and alias_gate.counts['unknown_clock'] == 1
    chunks = list(stream_array(io.BytesIO(b'[' + env + b',' + env + b']\n')))
    assert chunks == [env, env]
    for malformed in (b'[{"x":1}{"x":2}]', b'[{"x":1},,]', b'[{"x":1},]'):
        try:
            list(stream_array(io.BytesIO(malformed)))
            raise AssertionError('malformed array admitted')
        except ValueError:
            pass
    from b1_reader import fields, array_raw
    for malformed in (b'{"x":1 "y":2}', b'{"x":1,,"y":2}', b'{"x":1,}'):
        try:
            list(fields(malformed))
            raise AssertionError('malformed object admitted')
        except ValueError:
            pass
    for malformed in (b'[1 2]', b'[1,,2]', b'[1,]'):
        try:
            list(array_raw(malformed))
            raise AssertionError('malformed inner array admitted')
        except ValueError:
            pass
    # Log rejected under native and shift hypotheses; decoder cannot see service or message canary.
    import datetime as dt
    def line(t, text):
        prefix = dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%d %H:%M:%S.000')
        return prefix + ' INFO ' + text
    logs = json.dumps({'CANARY_SERVICE': [line(100000, 'CANARY Span reported: aa:bb:cc:'),
                                        line(200000+28800, 'CANARY'), 'CANARY without time'],
                       'safe': [line(50000, 'hello')]}).encode()
    lg = Gate(policy, 'reference')
    admitted = list(admitted_logs(logs, lg, decoder))
    assert len(admitted) == 1 and admitted[0][0] == 'safe'
    assert lg.counts['denied_B1'] == 2 and lg.counts['unknown_clock'] == 1
    # Policy applies identically to dev, reference, control; endpoints and span crossing.
    for role in ('dev', 'reference', 'control'):
        g = Gate(policy, role)
        assert not g.accept(100010) and not g.accept(99999, 100000) and g.accept(50000)
    # Native microseconds retained, never moved into a window by a hypothesis.
    assert got[0][2] == 50000 and got[0][3] == 50001
    allow = json.loads((OUT / 'allowlist-phien.json').read_text(encoding='utf-8'))
    selector = Selector(allow)
    for origin, member in [('outer', 'test/spans.json'), ('outer', 'unknown'),
                           ('TT Dataset/TT-all.txz', allow['approved_sessions'][0]['members'][0]['member']),
                           ('TT Dataset/no fault/TT-no-fault.txz', 'any')]:
        try:
            selector.require(origin, member)
            raise AssertionError('selector admitted forbidden member')
        except PermissionError:
            pass
    proposed = copy.deepcopy(allow)
    proposed['status'] = 'proposed'
    try:
        Selector(proposed)
        raise AssertionError('proposal admitted')
    except PermissionError:
        pass
    assert len(selector.members) == 145
    # Known-answer identity: exact, conflict, same ID scoped differently; parent outside window.
    from inspect_approved import identity_stats
    rows = [dict(key=('aa', 'bb'), signature='1', start=5, end=6, service='A', operation='o', refs=[]),
            dict(key=('aa', 'bb'), signature='1', start=5, end=6, service='A', operation='o', refs=[]),
            dict(key=('aa', 'cc'), signature='2', start=10, end=11, service='B', operation='o', refs=[('aa', 'bb')]),
            dict(key=('dd', 'bb'), signature='3', start=10, end=11, service='C', operation='o', refs=[])]
    ids = identity_stats(rows, (9, 12))
    assert ids['exact_extra_rows'] == 1 and ids['parent_outside_window'] == 1 and ids['conflict_keys'] == 0
    rows.append(dict(rows[0], signature='different'))
    ids = identity_stats(rows)
    assert ids['conflict_keys'] == 1 and ids['parent_conflicting'] == 1
    invalid = identity_stats([dict(rows[0], key=(None, None))])
    assert invalid['invalid_id_rows'] == 1 and invalid.get('usable_nonconflict_keys', 0) == 0
    boundary = identity_stats([dict(rows[0], start=10)], (5, 10))
    assert boundary.get('usable_nonconflict_keys', 0) == 0
    checks = ['timestamp_gate_before_span_decode', 'gate_before_process_service_decode',
              'native_and_plus_minus8_rejection', 'unknown_and_duplicate_clock_fail_closed',
              'nested_clock_not_selected', 'escaped_lexical_framing', 'gate_before_log_message_and_service',
              'all_roles_and_closed_boundary', 'native_unit_preserved', 'selector_145_no_test_unknown_nested',
              'identity_exact_conflict_scope_parent_outside_window', 'escaped_clock_alias_fail_closed',
              'strict_array_object_comma_grammar', 'missing_ID_not_usable', 'pre_window_excludes_injection_boundary']
    return {'PASS': True, 'checks': checks, 'span_gate': gate.result(), 'log_gate': lg.result(),
            'semantic_decodes': len(decoded), 'archive_opened': False}


if __name__ == '__main__':
    import argparse
    import traceback
    p = argparse.ArgumentParser()
    p.add_argument('--run-id', required=True)
    args = p.parse_args()
    run = OUT / 'runs' / args.run_id
    run.mkdir(exist_ok=False)
    try:
        result = main()
        (run / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print('PASS: ' + str(len(result['checks'])) + ' fixture groups; no archive opened')
    except Exception:
        (run / 'failure.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise
