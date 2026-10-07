"""Derived descriptions from the retained run; no raw input or chosen threshold."""
import argparse
import collections
import csv
import json
from pathlib import Path
from inspect_approved import csvsave, load, save, stats

OUT = Path(__file__).resolve().parents[1]


def main(run):
    sessions = json.loads((run / 'sessions.json').read_text(encoding='utf-8'))
    metrics = list(csv.DictReader((run / 'metric-stats.csv').open(encoding='utf-8-sig')))
    allow = load('results/T-023/allowlist-phien.json')
    for m in metrics:
        for k in ('n', 'invalid', 'duplicate_timestamps', 'cadence_non1'):
            m[k] = int(m[k])
        for k in ('min', 'max', 'q25', 'median', 'q75', 'mean', 'sd', 'start_s', 'end_s'):
            m[k] = float(m[k]) if m[k] else None
        m['constant'] = m['constant'] == 'True'
    roles = {s: x['role'] for s, x in sessions.items()}
    ref = next(s for s, role in roles.items() if role == 'reference')
    control = next(s for s, role in roles.items() if role == 'control')
    lookup = {(m['session'], m['service'], m['channel'], m['window']): m for m in metrics}
    whole = [m for m in metrics if m['window'] == 'session']
    comparisons = []
    for r in [m for m in whole if m['session'] == ref]:
        peers = [m for m in metrics if m['service'] == r['service'] and m['channel'] == r['channel'] and
                 ((m['session'] == control and m['window'] == 'session') or
                  (roles[m['session']] == 'dev' and m['window'].endswith('-pre')))]
        for m in peers:
            iqr = r['q75'] - r['q25']
            comparisons.append({'reference': ref, 'other_session': m['session'], 'other_role': roles[m['session']],
                                'service': m['service'], 'channel': m['channel'], 'other_window': m['window'],
                                'reference_n': r['n'], 'other_n': m['n'], 'other_duration_s': m['end_s']-m['start_s'],
                                'reference_median': r['median'], 'other_median': m['median'], 'reference_iqr': iqr,
                                'median_delta': m['median']-r['median'] if m['median'] is not None else None,
                                'delta_over_reference_iqr': (m['median']-r['median'])/iqr if iqr and m['median'] is not None else None,
                                'reference_constant': r['constant'], 'other_constant': m['constant']})
    csvsave(run / 'reference-comparisons.csv', comparisons)
    quarter = []
    for s in (ref, control):
        for r in [m for m in whole if m['session'] == s]:
            qs = [lookup[(s, r['service'], r['channel'], 'quarter-'+str(k))] for k in range(1, 5)]
            quarter.append({'session': s, 'service': r['service'], 'channel': r['channel'],
                            **{'quarter'+str(k+1)+'_median': q['median'] for k, q in enumerate(qs)},
                            'quarter_median_range': max(q['median'] for q in qs)-min(q['median'] for q in qs),
                            'whole_iqr': r['q75']-r['q25'],
                            'note': 'fixed quarters, no inferred warm-up cutoff'})
    csvsave(run / 'normal-quarters.csv', quarter)
    # Across-session content overlap is an export diagnostic, never an identity merge.
    safe_sets = {}
    for s in sessions:
        safe = list(csv.DictReader((run / (s+'-safe-spans.csv')).open(encoding='utf-8-sig')))
        safe_sets[s] = {(r['trace_id'], r['span_id'], r['signature']) for r in safe}
    overlap = []
    order = sorted(sessions)
    for i, s in enumerate(order):
        for t in order[i+1:]:
            common = safe_sets[s] & safe_sets[t]
            overlap.append({'session_a': s, 'session_b': t, 'safe_variants_a': len(safe_sets[s]),
                            'safe_variants_b': len(safe_sets[t]), 'identical_full_payload_service_variants': len(common),
                            'interpretation': 'export overlap evidence only; identity remains session scoped; censored rows not compared'})
    csvsave(run / 'cross-session-overlap.csv', overlap)
    normal_ops = {(x['service'], x['operation']): x['count'] for x in sessions[ref]['trace']['operations_admitted_rows']}
    control_ops = {(x['service'], x['operation']): x['count'] for x in sessions[control]['trace']['operations_admitted_rows']}
    op_comparisons = []
    for s, x in sessions.items():
        if x['role'] != 'dev':
            continue
        for op in x['trace']['operations_admitted_rows']:
            key = (op['service'], op['operation'])
            op_comparisons.append({'dev_session': s, 'service': key[0], 'operation': key[1],
                                   'dev_admitted_rows': op['count'], 'reference_admitted_rows': normal_ops.get(key, 0),
                                   'control_admitted_rows': control_ops.get(key, 0),
                                   'scope': 'all B1-safe historical content; not session/window normal'})
    csvsave(run / 'normal-operation-coverage.csv', op_comparisons)
    events = list(csv.DictReader((OUT / 'runs/metadata-001/events.csv').open(encoding='utf-8-sig')))
    audit = []
    for e in events:
        s = e['session']
        if e['proposed_role'] != 'dev':
            continue
        root = e['root_for_audit_only']
        for part in ('pre', 'post'):
            w = 'event-'+e['event_index']+'-'+part
            trace = next(x for x in sessions[s]['trace']['windows'] if x['window'] == w)
            logs = next(x for x in sessions[s]['log']['windows'] if x['window'] == w)
            ms = [m for m in metrics if m['session'] == s and m['window'] == w and m['service'] == root]
            audit.append({'session': s, 'event_index': e['event_index'], 'window': w,
                          'root_audit_only': root, 'fault_audit_only': e['fault_for_audit_only'],
                          'duration_s': trace['end_s']-trace['start_s'], 'all_safe_trace_rows_native': trace['span_rows'],
                          'all_safe_log_lines_native': logs['lines'], 'root_metric_channels': len(ms),
                          'root_metric_min_finite_n': min(m['n'] for m in ms),
                          'root_metric_invalid': sum(m['invalid'] for m in ms)})
    csvsave(run / 'event-audit.csv', audit)
    condition = []
    def add(item, scope, verdict, evidence, implication):
        condition.append(dict(condition=item, scope=scope, verdict=verdict, evidence=evidence, implication=implication))
    rp = str(run.relative_to(OUT)).replace('\\', '/')
    add('selector_B1_before_content', '5 approved sessions', 'PASS', 'runs/fixture-002/verification.json; '+rp+'/opened-members.csv',
        '145 approved members only; forbidden trace/log contents omitted')
    add('archive_and_member_integrity', 'ZIP and 145 logical members', 'PASS', rp+'/archive-verification.json; '+rp+'/opened-members.csv',
        'byte/SHA match T009 metadata, not a statement of dataset validity')
    for s, x in sessions.items():
        ms = [m for m in whole if m['session'] == s]
        good = len(ms) == 189 and all(m['n'] > 0 and m['invalid'] == 0 and m['duplicate_timestamps'] == 0 and m['cadence_non1'] == 0 for m in ms)
        add('metric_numeric_cadence', s, 'PASS' if good else 'FAIL', rp+'/metric-stats.csv',
            '27 service x 7 numeric channels; resource metric, not automatically SLI')
        tw = next(w for w in x['trace']['windows'] if w['window'] == 'session')
        add('trace_native_session_coverage', s, 'FAIL' if tw['span_rows'] == 0 else 'OPEN', rp+'/trace-window-coverage.csv',
            'native timestamp only; no hypothesis used for alignment; provenance clock unverified')
        ids = x['trace']['identity']
        add('trace_identity_conflicts', s+' (whole B1-safe export, not confirmed incident)' if x['role'] == 'dev' else s,
            'FAIL' if ids['conflict_keys'] else 'PASS', rp+'/sessions.json; '+rp+'/'+s+'-safe-spans.csv'
            +('; kiem-eadro.md section 4' if x['role'] == 'dev' else ''),
            'whole safe export includes historical conflict block; not a confirmed incident identity failure; own H-8 groups distinguished in report; no last-wins; excluded identities never compared'
            if x['role'] == 'dev' else 'safe subset only; no last-wins; excluded identities never compared')
        empty_own_hminus = not any(c['hypothesis'] == 'H-8' and c['interval'] == s and c['count'] > 0
                                  for c in x['log']['gate']['admitted_classifications'])
        add('log_clock_session_mapping', s, 'OPEN', rp+'/log-window-coverage.csv; '+rp+'/sessions.json',
            ('gate classifications support H-8 coordinate hypothesis in other approved sessions; own H-8 safe group empty here; '
             if empty_own_hminus else 'gate classifications support H-8 coordinate hypothesis with historical export; ')
            +'source timezone and per-event coverage unverified; no alignment applied')
        lw = next(w for w in x['log']['windows'] if w['window'] == 'session')
        add('log_native_session_coverage', s, 'FAIL' if lw['lines'] == 0 else 'OPEN', rp+'/log-window-coverage.csv',
            'native wall coordinate only; no offset applied; censored content unavailable')
    add('reference_numeric_coverage', 'reference vs control', 'PASS', rp+'/metric-stats.csv', 'observed full numeric series; faults=[] is label evidence only')
    add('reference_representativeness', 'reference-control and all 27 dev pre-windows', 'OPEN', rp+'/reference-comparisons.csv; '+rp+'/normal-quarters.csv',
        'descriptive differences recorded per service/channel; no clean segment selected; no proven equivalent workload or calibration')
    add('trace_normal_operation_coverage', 'reference vs 3 dev', 'OPEN', rp+'/sessions.json; '+rp+'/trace-window-coverage.csv',
        'safe historical operation mix cannot substitute for aligned normal/incident traces')
    add('trace_reference_control_independence', 'whole B1-safe exports before session filtering', 'OPEN', rp+'/cross-session-overlap.csv; '+rp+'/sessions.json',
        'overlap falls in reference interval under H-8; whole-export independence unverified; compatible with historical export and time filtering; clock and per-window validity unverified')
    add('BARO_NSigma_scorer_CIRCA_PC', 'numeric schema only', 'PASS', rp+'/metric-stats.csv; T013/T014 method profiles; docs/DECISIONS.md Q-62/Q-67',
        'necessary numeric schema only; CIRCA-PC remains tier 2 under Q-62 and subject to TT budget restriction Q-67; normal/config/benchmark pending separate decision')
    add('NSigma_BOCPD_detection', 'resource alarms vs SLI alarms', 'OPEN', rp+'/metric-stats.csv; T013 method profiles',
        'numeric possible; selected columns/config/reference and recording independence need valid protocol, no detector run here')
    add('TORAI_fixed', 'metric+logts', 'OPEN', rp+'/log-window-coverage.csv; T016 profile',
        'log service/time must be mapped; trace cannot replace missing log channel')
    add('SimpleRCA_M4', 'metric trace log votes', 'OPEN', rp+'/sessions.json; T017 profile',
        'metric numeric condition met; trace vote lacks confirmed window, log clock pending; partial modality is a separate choice')
    add('TraceRCA_finite_MicroRank_fixed', 'aligned trace normal/incident', 'OPEN', rp+'/trace-window-coverage.csv; '+rp+'/sessions.json; T015 profiles',
        'H-8 coordinate hypothesis has internal support; clock and per-window alignment unverified and not applied; whole-safe historical conflicts are not confirmed incident failures; no full trace claim yet')
    add('CIRCA_architecture', 'T/S/L/E and graph', 'OPEN', rp+'/metric-stats.csv; '+rp+'/sessions.json; T014 profile',
        'CPU/memory resource schema, rx/tx unit unknown; no metric request latency/errors or proven shared-clock graph')
    add('generalize_to_33k_test_export', 'dev population', 'OPEN', 'runs/approval-001/population-metadata.json',
        'dev 18k exports only; two 33k test exports not inspected')
    csvsave(OUT / 'bang-dieu-kien.csv', condition)
    aggregate = {'metric_whole_rows': len(whole), 'metric_finite_values': sum(m['n'] for m in whole),
                 'metric_invalid_values': sum(m['invalid'] for m in whole),
                 'constant_whole_channels_by_session': {s: sum(m['constant'] for m in whole if m['session'] == s) for s in sessions},
                 'reference_comparison_rows': len(comparisons), 'dev_pre_comparison_rows': sum(c['other_role']=='dev' for c in comparisons),
                 'reference_control_comparison_rows': sum(c['other_role']=='control' for c in comparisons),
                 'dev_pre_duration_stats_s': stats([float(e['q64_pre_available_s']) for e in events if e['proposed_role']=='dev']),
                 'dev_regular_pre_duration_stats_s': stats([float(e['q64_pre_available_s']) for e in events if e['proposed_role']=='dev' and int(e['event_index'])>0]),
                 'reference_control_delta_iqr_stats': stats([c['delta_over_reference_iqr'] for c in comparisons if c['other_role']=='control' and c['delta_over_reference_iqr'] is not None]),
                 'safe_reference_control_full_payload_overlap': next(r['identical_full_payload_service_variants'] for r in overlap if {r['session_a'],r['session_b']} == {ref,control}),
                 'dev_operation_rows_without_reference': sum(r['reference_admitted_rows']==0 for r in op_comparisons),
                 'verdict_counts': dict(collections.Counter(c['verdict'] for c in condition))}
    save(run / 'derived-summary.json', aggregate)
    return aggregate


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source-run', required=True)
    args = p.parse_args()
    summary = main(OUT / 'runs' / args.source_run)
    print(json.dumps(summary, ensure_ascii=True))
