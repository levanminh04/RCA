from pathlib import Path
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
MD = HERE / 'md-partition'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


checks = []


def check(label, value):
    checks.append({'label': label, 'pass': bool(value)})


for attempt in (1, 2, 3):
    base = MD / f'attempt-{attempt:03}'
    manifest = read(base / 'manifest.json')
    for row in manifest['files']:
        check(f'manifest {attempt}: {row["path"]}', sha(MD / row['path']) == row['sha256'])

sources = read(MD / 'attempt-003/sources.json')
for rel, row in sources.items():
    check('input source: ' + rel, sha(REPO / rel) == row['sha256'])

summary = read(MD / 'attempt-003/summary.json')
check('status PASS', summary['status'] == 'PASS')
check('52 cases, 48 PASS, 4 native ERROR N/A', summary['n_cases'] == 52 and summary['status_counts'] == {'PASS': 48, 'N/A': 4})
check('no ranker or PageRank executed', summary['methods_executed'] == [] and not summary['pagerank_executed'])
check('8 interval fixtures passed', summary['interval_fixtures']['pass'] and summary['interval_fixtures']['checked'] == 8)

old = read(REPO / 'results/T-032/runs/microrank-md-001/collect-001/summary.json')
refs = {(c['dataset'], c['opaque_id']): c for c in old['cases']}
cohort = []
for case in summary['cases']:
    cid = case['opaque_id']
    if case['status'] != 'PASS':
        check(cid + ': N/A stays ERROR', case['source_status'] == 'ERROR')
        continue
    check(cid + ': all extraction checks', all(case['checks'].values()) and len(case['checks']) == 7)
    traces = read(MD / 'attempt-003' / case['per_trace_file'])
    transitions = Counter()
    for tr in traces:
        transitions[tr['native_group'] + '->' + tr['md_group']] += 1
        for br in ('native', 'md'):
            check(cid + ': OR ' + tr['traceID'] + ' ' + br,
                  (tr[br + '_group'] == 'A') == any(v[br + '_flags'] > 0 for v in tr['services'].values()))
    check(cid + ': transitions independently counted', dict(transitions) == case['transitions'])
    for br in ('native', 'md'):
        check(cid + ': old counts ' + br, case['totals'][br] == refs[case['dataset'], cid]['counts'][br])
        check(cid + ': A/N totals ' + br,
              sum(t[br + '_group'] == 'A' for t in traces) == case['totals'][br]['anomaly']
              and len(traces) == case['totals'][br]['all'])
        check(cid + ': span flags ' + br,
              sum(v[br + '_flags'] for tr in traces for v in tr['services'].values()) == case['totals'][br]['abnormal_spans'])
    for op, row in case['operations'].items():
        check(cid + ': coverage counts ' + op,
              row['native']['A'] + row['native']['N'] == row['md']['A'] + row['md']['N']
              and row['native']['own_flag_traces'] <= row['native']['A']
              and row['md']['own_flag_traces'] <= row['md']['A'])
    post = case['postanalysis']
    root = post['root']
    for caller, row in post['caller_witnesses'].items():
        witness = []
        for i, tr in enumerate(traces):
            v = tr['services'].get(caller, {'native_flags': 0, 'md_flags': 0})
            if v['native_flags'] > 0 and v['md_flags'] == 0 and tr['native_group'] == tr['md_group'] == 'A':
                witness.append(i)
        check(cid + ': witness ' + caller,
              len(witness) == row['n_caller_flags_lost_but_trace_stays_A']
              and witness == [w['trace_index'] for w in row['witnesses']])
    if post['callers_above']['native']:
        cohort.append({'case': cid, 'dataset': case['dataset'],
                       'native_callers_above': post['callers_above']['native'],
                       'md_callers_above': post['callers_above']['md'],
                       'witness_n': {s: post['caller_witnesses'].get(s, {}).get('n_caller_flags_lost_but_trace_stays_A', 0)
                                     for s in post['callers_above']['native']},
                       'matched_correct_controls': post['matched_correct_controls_dataset_fault']})

runtime = summary['runtime_s'] + sum(read(MD / f'attempt-{n:03}/failure.json')['runtime_s'] for n in (1, 2))
result = {'checks': checks, 'n_checks': len(checks), 'n_mismatch': sum(not c['pass'] for c in checks),
          'caller_above_native_cohort': cohort, 'cohort_n': len(cohort),
          'cohort_cases_with_witness': sum(any(r['witness_n'].values()) for r in cohort),
          'cohort_with_caller_still_above_md': sum(bool(r['md_callers_above']) for r in cohort),
          'cohort_with_matched_native_correct_control': sum(bool(r['matched_correct_controls']) for r in cohort),
          'runtime_all_attempts_s': runtime, 'summary_sha256': sha(MD / 'attempt-003/summary.json'),
          'limits': ['Verification of saved quantities is not a physical waiting experiment.',
                     'It does not recompute PageRank or attribute every unchanged score to flag retention.']}
(HERE / 'kiem-md-doc-lap.json').write_text(json.dumps(result, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k not in ('checks', 'caller_above_native_cohort')}, ensure_ascii=False, indent=2))
assert not result['n_mismatch']
