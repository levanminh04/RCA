"""Phản ví dụ trên file/process giả cho các đường điều phối được sửa."""
import json
import sys
import time
import traceback
import copy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'results/T-054/scripts'))
from bien_nhan import OUT, Blocked, append, atomic, events, fingerprint, ref
import dieu_phoi as q


def main(destination):
    out = Path(destination).resolve(); out.mkdir(parents=True, exist_ok=False)
    checks = []
    def check(name, ok):
        assert ok, name
        checks.append(name)
    journal = out / 'torn.jsonl'
    committed = b'{"state":"PENDING"}\n'; tail = b'{"state":"RUNNING"'
    journal.write_bytes(committed + tail)
    check('readonly_ignores_only_uncommitted_tail', events(journal) == [{'state': 'PENDING'}])
    append(journal, {'state': 'VERIFIED'})
    rows = events(journal)
    check('completed_append_survives_torn_tail', rows[-1]['state'] == 'VERIFIED')
    recovery = rows[1]
    check('original_torn_bytes_preserved', (out / recovery['archive']).read_bytes() == tail)
    append(journal, {'state': 'STOPPED'})
    check('next_append_remains_parseable', events(journal)[-1]['state'] == 'STOPPED')
    bad = out / 'complete-but-corrupt.jsonl'; bad.write_bytes(b'{bad}\n')
    try:
        events(bad)
    except Blocked:
        checks.append('complete_corrupt_event_not_silently_ignored')
    else:
        raise AssertionError('complete corruption accepted')
    streamed = out / 'streamed'; streamed.mkdir()
    (streamed / 'resources.jsonl').write_bytes(b''.join(json.dumps({'sample': n}).encode() + b'\n' for n in range(5000)))
    (streamed / 'events.jsonl').write_bytes(b'{"job_id":"x","state":"RUNNING"}\n')
    with patch('pathlib.Path.read_bytes', side_effect=AssertionError('bulk read during status')):
        check('status_streams_large_history', q.status(streamed)['last_monitor']['sample'] == 4999)
    script = ('import sys;sys.path.insert(0,sys.argv[1]);from bien_nhan import append;'
              '[append(sys.argv[2],{"producer":sys.argv[3],"n":n}) for n in range(50)]')
    concurrent = out / 'concurrent.jsonl'
    writers = [q.launch(sys.executable, ['-c', script, str(ROOT/'results/T-054/scripts'), str(concurrent), str(n)],
                        out/('writer-'+str(n)+'.stdout'), out/('writer-'+str(n)+'.stderr')) for n in (1, 2)]
    codes = [p.wait(timeout=15) for p in writers]
    check('concurrent_append_processes_exit_ok', all(code == 0 for code in codes))
    pairs = {(r['producer'], r['n']) for r in events(concurrent)}
    check('concurrent_append_loses_no_event', pairs == {(str(p), n) for p in (1, 2) for n in range(50)})

    def job(n, sleep=.01):
        slot = {'dataset': 'SYNTHETIC', 'opaque_id': 'fixture-' + str(n), 'member_sha256': 'a'*64,
                'arm': 'M1', 'view': 'main', 'seed': None, 'source_sha256': 'b'*64,
                'window': [0, 300, 600], 'config_sha256': 'c'*64, 'environment_sha256': 'd'*64}
        return {'kind': 'synthetic', 'slot': slot, 'executable': sys.executable, 'a4': True,
                'timeout_s': 10, 'scenario': 'slow_ok', 'sleep_s': sleep,
                'synthetic_records': [{'status': 'NO_EVIDENCE', 'blocks': []}]}
    def plan(jobs, budget=None):
        value = {'schema': 'T054-PLAN-1', 'mode': 'synthetic', 'host_role': 'local', 'jobs': jobs,
                 'monitor': {'poll_s': .02, 'max_monitor_gap_s': 2, 'score_phases': ['method']}}
        if budget is not None:
            value['budget'] = budget
        return value
    capped = out / 'whole-budget'
    pl = plan([job(1, 4), job(2)], {'wall_s': 1.5, 'method_dataset_s': {}})
    q.supervise(pl, capped)
    st = q.status(capped)
    check('whole_budget_wait_visible', st['wait']['state'] == 'WAIT_BUDGET')
    check('whole_budget_does_not_launch_remaining', not (capped / fingerprint(pl['jobs'][1]['slot'])).exists())
    check('budget_limit_not_scientific_timeout', all(r.get('phase_state') != 'COMPLETE_UNVERIFIED' for r in st['jobs'].values()))
    check('budget_stop_has_evidence', len(list(capped.rglob('budget-stop.json'))) == 1)
    check('stopped_worker_has_no_fake_timeout_result', not list(capped.rglob('result.json')))

    cumulative = out / 'group-budget'
    many = plan([job(n, .15) for n in range(10)], {'wall_s': 30, 'method_dataset_s': {'SYNTHETIC|M1': .7}})
    q.supervise(many, cumulative)
    first = q.status(cumulative)
    check('method_dataset_cap_applied', first['wait']['reason'] == 'method_dataset')
    count_before = len(list(cumulative.rglob('job.json')))
    budget_before = (cumulative / 'budget-start.json').read_bytes()
    q.supervise(many, cumulative)
    check('resume_does_not_reset_budget', (cumulative / 'budget-start.json').read_bytes() == budget_before)
    check('resume_does_not_launch_after_cumulative_cap', len(list(cumulative.rglob('job.json'))) == count_before)

    drained = out / 'drain-pipeline'
    first_job = job(50)
    pipeline_job = job(51); pipeline_job['kind'] = 'torai_pipeline'
    pipeline_job['slot'] = dict(pipeline_job['slot'], arm='torai_B', seed=0)
    original_monitor = q._monitor
    def drain_after_first(*args, **kwargs):
        result = original_monitor(*args, **kwargs)
        append(drained / 'control.jsonl', {'action': 'DRAIN'})
        return result
    with patch.object(q, '_monitor', side_effect=drain_after_first), patch.object(q, 'pipeline', side_effect=AssertionError('pipeline after drain')) as invoked:
        q.supervise(plan([first_job, pipeline_job]), drained)
        check('drain_covers_torai_pipeline', invoked.call_count == 0)
    check('drain_does_not_create_unstarted_attempt', not (drained / fingerprint(pipeline_job['slot'])).exists())

    # C-d3 khai dependency trước output hash; nguồn scientific slot/plan không đổi sau main seal.
    from cham import snapshot_from_status, verify_snapshot
    from nguon import main_dependency_record
    from p7 import load_plan
    origin_root = out / 'synthetic-data'; origin_root.mkdir()
    origin = atomic(origin_root/'origin.json', {'schema': 'T054-GENERATED-FIXTURE'})
    parent = job(70)
    parent['slot'] = dict(parent['slot'], dataset='RE2-TT')
    blocks = [{'key': [1.0], 'groups': [['x']]}]
    parent['synthetic_records'] = [{'method':'M1','variant':'M1','config_id':'M1','mode':'a','seed':None,
        'status':'OK','blocks':blocks,'worlds':{w:{'blocks':blocks} for w in ('P','S_lo','S_hi')},
        'extra':{'dau_vao_cd3':{'canh':[['x','y']],'diem':{'x':[1,1],'y':[2,1]},'dich':['x']}}}]
    child = job(70)
    child['a4'] = False
    child['slot'] = dict(parent['slot'], arm='C-d3', config_sha256='e'*64)
    child.update(fixture_route='cd3', data_root=str(origin_root), fixture_origin=origin,
                 main_dependency={'slot':parent['slot'], 'job_sha256':fingerprint(parent)})
    dependency_plan = plan([parent, child]); dependency_plan['directory'] = str(out/'dependency')
    frozen = fingerprint(dependency_plan)
    pr = atomic(out/'dependency-plan.json', dependency_plan)
    load_plan(pr['path'], pr['sha256'])
    q.supervise(dependency_plan, out/'dependency')
    dep_state = q.status(out/'dependency')
    check('main_and_cd3_both_verified', all(r['state']=='VERIFIED' for r in dep_state['jobs'].values()) and len(dep_state['jobs']) == 2)
    check('dependency_plan_immutable', fingerprint(dependency_plan)==frozen and load_plan(pr['path'],pr['sha256'])==dependency_plan)
    snapshot = snapshot_from_status(dependency_plan, dep_state)
    check('full_snapshot_reads_sealed_dependency', len(verify_snapshot(snapshot, dependency_plan['jobs'])) == 2)
    sealpath = next((out/'dependency/seals').glob('*.json')); sealpin = ref(sealpath)
    raw = json.loads(sealpath.read_bytes()); altered = copy.deepcopy(raw)
    key = next(iter(altered['records'])); altered['records'][key]['extra']['dau_vao_cd3']['diem']['x']=[9,1]
    altered_pin = atomic(out/'altered-main-seal.json', altered)
    try:
        main_dependency_record(child, altered_pin)
    except Blocked:
        checks.append('rehashed_main_payload_swap_rejected')
    else:
        raise AssertionError('changed main payload accepted')
    check('original_main_seal_preserved', ref(sealpath)==sealpin)
    backwards = dict(dependency_plan, jobs=[child,parent])
    br=atomic(out/'backwards-plan.json', backwards)
    try:
        load_plan(br['path'],br['sha256'])
    except Blocked:
        checks.append('dependency_order_rejected_before_run')
    else:
        raise AssertionError('forward dependency accepted')
    check('source_metadata_only', True)
    atomic(out / 'summary.json', {'PASS': True, 'checks': checks, 'count': len(checks),
           'scope': 'synthetic files and worker processes; no public telemetry or scientific pilot',
           'whole_budget_state': st['wait'], 'group_budget_attempts': count_before})
    print(json.dumps({'PASS': True, 'checks': len(checks), 'output': str(out)}))


if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except BaseException:
        p = Path(sys.argv[1])
        if p.exists():
            atomic(p / 'failure.json', {'traceback': traceback.format_exc()})
        raise
