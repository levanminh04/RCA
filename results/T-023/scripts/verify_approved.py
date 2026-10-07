"""Independent count/hash/window check from retained approved outputs, no telemetry."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import traceback
from b1_reader import Gate

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-023'


def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def records(p):
    return list(csv.DictReader(p.open(encoding='utf-8-sig')))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(source, fixture):
    checks = []
    def check(name, value):
        assert value, name
        checks.append(name)
    allow = load(OUT / 'allowlist-phien.json')
    before = load(OUT / 'runs/approval-001/allowlist-before.json')
    check('approval_exact_member_objects_seed_split', allow['approved_sessions'] == before['proposed_sessions'] and
          allow['seed'] == before['seed'] and allow['test_sessions'] == before['test_sessions'] and
          allow['unlabelled_sessions'] == before['unlabelled_sessions'])
    check('fixture_pass', load(OUT / 'runs' / fixture / 'verification.json')['PASS'])
    manifest = load(source / 'manifest.json')
    check('input_hashes_match_execution', all((ROOT/x['path']).stat().st_size == x['bytes'] and sha(ROOT/x['path']) == x['sha256'] for x in manifest['inputs']))
    check('stream_output_hashes_match', all((ROOT/x['path']).stat().st_size == x['bytes'] and sha(ROOT/x['path']) == x['sha256'] for x in manifest['outputs']))
    opened = records(source / 'opened-members.csv')
    wanted = {(m['origin'], m['member']): (s['session'], m) for s in allow['approved_sessions'] for m in s['members']}
    check('only145_approved_members', len(opened) == 145 and {(r['origin'], r['member']) for r in opened} == set(wanted))
    check('member_bytes_sha', all(int(r['bytes']) == wanted[(r['origin'], r['member'])][1]['bytes'] and
          r['sha256'] == wanted[(r['origin'], r['member'])][1]['sha256'] for r in opened))
    check('no_denied_sessions_containers', not any(r['session'] in allow['test_sessions'] + allow['unlabelled_sessions'] or r['origin'] in allow['denied_origins'] for r in opened))
    population = {r['session']: r['span_count_before_B1'] for r in load(OUT / 'runs/approval-001/population-metadata.json')}
    sessions = load(source / 'sessions.json')
    identity_checks = {}
    for s, result in sessions.items():
        safe = records(source / (s+'-safe-spans.csv'))
        tg = result['trace']['gate']['counts']
        check('trace_partition_'+s, tg['total'] == population[s] and tg['total'] == tg.get('admitted', 0)+tg.get('denied_B1', 0)+tg.get('unknown_clock', 0) and len(safe)==tg.get('admitted', 0))
        gate = Gate(allow['B1'], s)
        check('all_retained_spans_outside_forbidden_'+s, all(gate.accept(float(r['native_start_s']), float(r['native_end_s'])) for r in safe))
        groups = collections.defaultdict(set)
        multiplicity = collections.Counter()
        invalid = 0
        for r in safe:
            key = (r['trace_id'], r['span_id'])
            if not all(re.fullmatch('[0-9a-fA-F]+', x) for x in key):
                invalid += 1
                continue
            groups[key].add(r['signature'])
            multiplicity[(key, r['signature'])] += 1
        ids = result['trace']['identity']
        check('independent_identity_counts_'+s, len(groups)==ids['unique_keys'] and sum(len(v)>1 for v in groups.values())==ids['conflict_keys'] and
              sum(n-1 for n in multiplicity.values())==ids['exact_extra_rows'] and invalid==ids['invalid_id_rows'])
        for w in result['trace']['windows']:
            sub = [r for r in safe if w['start_s'] <= float(r['native_start_s']) < w['end_s']]
            check('trace_window_'+s+'_'+w['window'], len(sub)==w['span_rows'] and len({int(float(r['native_start_s'])) for r in sub})==w['distinct_seconds'])
        lg = result['log']['gate']['counts']
        check('log_partition_'+s, lg['total']==lg.get('admitted',0)+lg.get('denied_B1',0)+lg.get('unknown_clock',0) and
              sum(x['count'] for x in result['log']['services'].values())==lg.get('admitted',0))
        identity_checks[s] = {'rows': len(safe), 'keys': len(groups), 'variants': sum(map(len, groups.values())), 'invalid': invalid}
    comparisons = records(source / 'reference-comparisons.csv')
    check('reference_vs_control_and_all_pre', len(comparisons)==189*28 and sum(r['other_role']=='control' for r in comparisons)==189 and
          sum(r['other_role']=='dev' for r in comparisons)==189*27)
    check('all_27_pre_including_first_short', len({(r['other_session'],r['other_window']) for r in comparisons if r['other_role']=='dev'})==27)
    metric = records(source / 'metric-stats.csv')
    full = [r for r in metric if r['window']=='session']
    check('metric_service_channel_population', len(full)==5*27*7 and len({(r['session'],r['service'],r['channel']) for r in full})==945)
    check('metric_no_invalid_gaps_duplicates', all(int(r['invalid'])==0 and int(r['cadence_non1'])==0 and int(r['duplicate_timestamps'])==0 for r in full))
    check('fixed_quarters_partition_normal_n', all(sum(int(q['n']) for q in metric if q['session']==r['session'] and q['service']==r['service'] and q['channel']==r['channel'] and q['window'].startswith('quarter-'))==int(r['n']) for r in full if sessions[r['session']]['role'] in ('reference','control')))
    # Check exact numeric comparison formulas rather than interpreting difference as a verdict.
    lookup = {(r['session'],r['service'],r['channel'],r['window']):r for r in metric}
    for r in comparisons:
        ref = lookup[(r['reference'],r['service'],r['channel'],'session')]
        other = lookup[(r['other_session'],r['service'],r['channel'],r['other_window'])]
        assert int(r['reference_n'])==int(ref['n']) and int(r['other_n'])==int(other['n'])
        assert abs(float(r['median_delta'])-(float(other['median'])-float(ref['median'])))<1e-9
    checks.append('reference_comparison_formulas')
    ops = records(source / 'normal-operation-coverage.csv')
    check('operation_comparison_all3dev_safe_pairs', len(ops)==sum(len(x['trace']['operations_admitted_rows']) for x in sessions.values() if x['role']=='dev'))
    conditions = records(OUT / 'bang-dieu-kien.csv')
    check('condition_verdicts_derived_summary', dict(collections.Counter(r['verdict'] for r in conditions))==load(source / 'derived-summary.json')['verdict_counts'])
    check('all_native_session_and_event_windows_zero', all(w['span_rows']==0 for x in sessions.values() for w in x['trace']['windows']) and
          all(w['lines']==0 for x in sessions.values() for w in x['log']['windows']))
    check('cost_ram_recorded', load(source / 'cost.json')['peak_working_set_bytes'] > 0)
    return {'PASS': True, 'checks': checks, 'identity_independent': identity_checks, 'raw_archive_opened': False,
            'limitation': 'Denied record contents intentionally unavailable; fixtures/source audit establish decode order. Semantic claims apply only to safe subset.'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source-run', required=True)
    p.add_argument('--fixture-run', required=True)
    p.add_argument('--run-id', required=True)
    args = p.parse_args()
    run = OUT / 'runs' / args.run_id
    run.mkdir(exist_ok=False)
    try:
        result = main(OUT / 'runs' / args.source_run, args.fixture_run)
        (run / 'verification.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
        print('PASS ' + str(len(result['checks'])) + ' independent checks; no raw archive opened')
    except Exception:
        (run / 'failure.txt').write_text(traceback.format_exc(), encoding='utf-8')
        raise
