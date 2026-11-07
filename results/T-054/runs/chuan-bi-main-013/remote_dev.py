"""Run the bounded approved DEV cover through the real T054 supervisor."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
sys.path[:0] = [str(OUT / 'scripts'), str(ROOT / 'src')]
from bien_nhan import atomic, append, fingerprint, read_pin, ref, digest, events
from dieu_phoi import status, verify_attempt
from lap_ho_so import stable_environment, preflight
from nguon import compare_sources
from pilot import comparable

HOST = sys.argv[1]
REPAIR = len(sys.argv) > 3 and sys.argv[3] == 'missing'
WORK = OUT / ('runs/' + (sys.argv[2] if len(sys.argv) > 2 else 'checkpoint013-results'))
WORK.mkdir(exist_ok=False)
REMOTE = Path('/home/ubuntu/rca-p7/T-054/checkpoint013')
MAIN = REMOTE / 'envs/main/bin/python'
PY38 = REMOTE / 'envs/py38/bin/python'
METADATA = json.loads((ROOT / 'dev-metadata.json').read_bytes())
PINS = json.loads((ROOT / 'files.json').read_bytes())
START = time.monotonic()
steps = []


def save_step(name, value):
    atomic(WORK / (name + '.json'), value)
    steps.append(dict(step=name, **value))
    print(json.dumps(steps[-1]), flush=True)


def projection(record, kind):
    if kind == 'T12':
        return dict(world_blocks={w: record['worlds'][w]['blocks'] for w in ('P', 'S_lo', 'S_hi')},
                    P_tiers=record['extra']['tang_P'], P_region=record['region'],
                    edges=sorted(map(tuple, record['extra']['canh'])))
    fields = ('method', 'mode', 'seed', 'status', 'error', 'window', 'blocks', 'entity_ranking',
              'ranking_native', 'observed_entities', 'diagnostics')
    projected = {k: record.get(k) for k in fields}
    projected['input_shape'] = {k: v for k, v in (record.get('input_shape') or {}).items() if k != 'metric_columns'}
    metadata = {'information_boundary', 'pilot_only', 'pilot_view', 'source_view', 'source_provenance_file'}
    projected['extra'] = {k: v for k, v in (record.get('extra') or {}).items() if k not in metadata}
    return projected


def run_dev():
    environment = stable_environment()
    envcode = ('import sys,json; sys.path[:0]=' + repr([str(OUT / 'scripts'), str(ROOT / 'src')])
               + '; from lap_ho_so import stable_environment; print(json.dumps(stable_environment()))')
    env38 = json.loads(subprocess.check_output([str(PY38), '-B', '-c', envcode]))
    save_step('environments', dict(main=environment, py38=env38, resources=preflight()))
    code = {p: v['sha256'] for p, v in PINS.items() if p.endswith('.py')}
    selected = []
    refs = {}
    for entry in METADATA['jobs']:
        key = entry['reference_key']
        if REPAIR and key not in ({'tracerca-error'} if HOST == 'ec2-large-disk' else {'torai_B-0', 'torai_B-1', 'torai_B-2'}):
            continue
        on_large = key in ('C-a0', 'bo-E1', 'bo-E2', 'C-e', 'simplerca-None', 'tracerca-error')
        if on_large != (HOST == 'ec2-large-disk'):
            continue
        job = copy.deepcopy(entry['job'])
        runtime = dict(dataset='RE2-TT', g1_revision=job['g1_revision'], inventory=job['inventory'],
                       cases={job['slot']['opaque_id']: job['source']})
        compare_sources(runtime, entry['independent'], 'RE2-TT', job['g1_revision'])
        job.update(data_root=str(ROOT), executable=str(MAIN), pythonpath=[str(ROOT / 'upstream/rcaeval')],
                   code_pins=code, runtime_ref=atomic(WORK / 'sources' / (key + '-runtime.json'), runtime),
                   independent_source_ref=atomic(WORK / 'sources' / (key + '-independent.json'), entry['independent']),
                   m1_contract=ref(ROOT / 'results/T-043/hop-dong.json'),
                   static_snapshot=ref(ROOT / 'results/T-038/do-thi/thuc-the.json'))
        torai = job['slot']['arm'] == 'torai_B'
        job['slot']['environment_sha256'] = fingerprint(env38 if torai else environment)
        if torai:
            job.update(prep_executable=str(MAIN), method_executable=str(PY38),
                       prep_environment_sha256=fingerprint(environment))
        job['a4'] = False
        selected.append(job)
        refs[fingerprint(job['slot'])] = METADATA['references'][key]
    if HOST == 'ec2-large-disk' and not REPAIR:
        oldroot = Path('/home/ubuntu/rca-p7/T-054/checkpoint012/work')
        oldwork = oldroot / 'results/T-054/runs/checkpoint012-results'
        oldplan = json.loads((oldwork / 'dev-plan.json').read_bytes())
        parent = oldplan['jobs'][0]
        oldstate = status(oldwork / 'dev-queue')['jobs'][fingerprint(parent['slot'])]
        verify_attempt(Path(oldstate['attempt']), parent, oldstate['token'])
        selected.insert(0, parent)
        cd3 = copy.deepcopy(parent)
        cd3.update(kind='cd3', executable=str(MAIN), pythonpath=[str(ROOT / 'upstream/RCAEval')], code_pins=code,
                   timeout_s=60, a4=False, main_dependency={'slot': parent['slot'], 'job_sha256': fingerprint(parent)})
        cd3['slot'] = dict(parent['slot'], arm='C-d3', config_sha256=fingerprint({'cd3': 'same sealed M1'}),
                            environment_sha256=fingerprint(environment))
        cd3['config'] = {'cd3': 'same sealed M1'}
        selected.insert(1, cd3)
    # The known TraceRCA ERROR is last; it must be classified before any scoring.
    selected.sort(key=lambda job: job['slot']['opaque_id'] == 'dev-a5cabe5fa7' and job['slot']['arm'] == 'tracerca')
    groups = {j['slot']['dataset'] + '|' + j['slot']['arm'] for j in selected}
    plan = dict(schema='T054-PLAN-1', mode='dev', host_role=HOST, workers=2 if HOST == 'ec2-large-disk' else 1,
                directory=str(WORK / 'queue'), jobs=selected, open_before_run=[],
                budget=dict(wall_s=3000, method_dataset_s={g: 3000 for g in groups}),
                monitor=dict(poll_s=.1, max_monitor_gap_s=5, score_phases=[]))
    pp = atomic(WORK / 'plan.json', plan)
    authority_source = atomic(WORK / 'preparation-permission.json', METADATA['preparation_permission'])
    authority = dict(pilot_grant=True, g3=False, test_grant=False, source=authority_source, plan_sha256=fingerprint(plan))
    ap = atomic(WORK / 'authority.json', authority)
    if HOST == 'ec2-large-disk' and not REPAIR:
        append(WORK / 'queue/events.jsonl', dict({k: v for k, v in oldstate.items() if k != 'utc'}, job_id=fingerprint(parent['slot']),
                                               action='REUSE_VERIFIED_012_WITHOUT_RERUN'))
    done = subprocess.run([str(MAIN), '-B', str(OUT / 'scripts/p7.py'), '_supervise', '--plan', pp['path'],
                           '--sha256', pp['sha256'], '--authority', ap['path'], '--authority-sha256', ap['sha256']],
                          capture_output=True, timeout=3100)
    (WORK / 'dev.stdout').write_bytes(done.stdout)
    (WORK / 'dev.stderr').write_bytes(done.stderr)
    assert done.returncode == 0, done.stderr.decode(errors='replace')[-2500:]
    state = status(WORK / 'queue')
    rows = []
    for job in selected:
        s = job['slot']; key = fingerprint(s)
        current = state['jobs'].get(key)
        if current is None:
            rows.append(dict(slot=s, PASS=False, reason='PENDING')); continue
        if s['arm'] == 'M1' and s['view'] == 'main':
            rows.append(dict(slot=s, PASS=True, reuse='checkpoint012')); continue
        attempt = Path(current['attempt'])
        if s['arm'] == 'tracerca' and s['opaque_id'] == 'dev-a5cabe5fa7':
            expected = refs[key]['record']
            baseline = atomic(WORK / 'tracerca-error-reference.json', expected)
            audit = atomic(WORK / 'operation-error-audit.json', METADATA['error_audit'])
            envelope = read_pin(ref(attempt / 'result.json'))
            invocation = read_pin(ref(attempt / 'invocation.json'))
            atomic(attempt / 'dev-error-reproduction.json', dict(scope='DEV_BASELINE_REPRODUCTION_ONLY',
                origin='method_implementation_assumption', job_sha256=fingerprint(job), result_sha256=fingerprint(envelope),
                invocation_sha256=fingerprint(invocation), baseline_reference=baseline, input_audit=audit,
                code_evidence=[ref(ROOT / 'upstream/rcaeval/RCAEval/e2e/tracerca.py'), ref(ROOT / 'src/p3/adapters/tracerca.py')]))
        records = verify_attempt(attempt, job, current['token'])
        receipt_path = attempt / 'verified.json'
        if not receipt_path.exists():
            atomic(receipt_path, dict(job_sha256=fingerprint(job), result=ref(attempt / 'result.json'),
                 invocation=ref(attempt / 'invocation.json'), dev_error_reproduction=ref(attempt / 'dev-error-reproduction.json')))
        invocation = read_pin(ref(attempt / 'invocation.json'))
        record = records[0]
        passed = True
        expected_pin = None
        if key in refs:
            expected = refs[key]; expected_pin = expected['origin']
            if expected['kind'] == 'M1':
                a, b = comparable(expected['record'], expected.get('control', False)), comparable(record, expected.get('control', False))
            elif expected['kind'] == 'T12':
                a, b = expected['fields'], projection(record, 'T12')
            else:
                a, b = projection(expected['record'], 'baseline'), projection(record, 'baseline')
            passed = fingerprint(a) == fingerprint(b)
            if not passed:
                atomic(WORK / 'differences' / (key + '.json'), dict(expected=a, observed=b))
        samples = events(attempt / 'monitor.jsonl')
        row = dict(slot=s, PASS=passed, status=record['status'], reference=expected_pin,
                   result=ref(attempt / 'result.json'), invocation=ref(attempt / 'invocation.json'),
                   seconds=read_pin(ref(attempt / 'cost.json'))['wall_s'],
                   max_gap=max((x.get('max_monitor_gap_s', 0) for x in samples), default=None),
                   peak_rss=max((x.get('tree_rss', 0) for x in samples), default=None),
                   normalized_input_sha256=invocation['normalized_input_sha256'])
        if s['arm'] == 'C-d3':
            row['real_main_seal'] = invocation['main_seal_ref']
        rows.append(row)
    save_step('dev-summary', dict(PASS=all(r['PASS'] for r in rows), rows=rows,
                                 seconds=time.monotonic() - START, state=state['counts'], test_opened=False))


try:
    run_dev()
    if time.monotonic() - START < 3200:
        done = subprocess.run([str(MAIN), '-B', str(OUT / 'scripts/fixtures.py'), str(WORK / 'fixture')],
                              capture_output=True, timeout=min(350, 3500 - (time.monotonic() - START)))
        (WORK / 'fixture.stdout').write_bytes(done.stdout)
        (WORK / 'fixture.stderr').write_bytes(done.stderr)
        save_step('fixture-summary', dict(PASS=done.returncode == 0,
                                         stderr=done.stderr.decode(errors='replace')[-1800:]))
except BaseException:
    save_step('failure', dict(PASS=False, traceback=traceback.format_exc()))
save_step('finish', dict(PASS=all(s['PASS'] for s in steps if 'PASS' in s), seconds=time.monotonic() - START,
                         free_disk=preflight()['free_disk'], test_opened=False, main_started=False))
if not steps[-1]['PASS']:
    raise SystemExit(1)
