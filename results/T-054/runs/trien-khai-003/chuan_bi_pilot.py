"""Pilot dev local theo lệnh Minh; không mở test, nguồn A hoặc RE3."""
import csv
import io
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path[:0] = [str(OUT / 'scripts'), str(ROOT / 'src')]
from bien_nhan import atomic, fingerprint, read_pin, ref, no_labels
from nguon import original_dev_sources, compare_sources

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8',
           PYTHONHASHSEED='0', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
MAIN = 'D:/RCA-ext/envs/T-014-main/Scripts/python.exe'
PY38 = 'D:/RCA-ext/envs/py38-rcdlock/Scripts/python.exe'
PATHS = [str(ROOT / 'src'), 'D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro',
         'D:/RCA-ext/work/T-014/CIRCA', 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']


def environment(executable):
    code = ('import sys,json; sys.path.insert(0,' + repr(str(OUT / 'scripts')) +
            '); sys.path.insert(0,' + repr(str(ROOT / 'src')) + '); sys.path.extend(' + repr(PATHS) + ')' +
            '; from lap_ho_so import stable_environment; print(json.dumps(stable_environment()))')
    run = subprocess.run([executable, '-B', '-c', code], env=ENV, capture_output=True, check=True)
    return json.loads(run.stdout)


def build(name, selected, arms=None, baseline_arms=None, include_cd3=True):
    dest = RUN / name
    dest.mkdir(exist_ok=False)
    private = Path('D:/RCA-ext/private/T-054') / name
    private.mkdir(parents=True, exist_ok=False)
    protocol = read_pin(ref(OUT / 'protocol.json'))
    cohort = read_pin(protocol['cohorts_source'])
    g1 = cohort['G1_source']; revision = g1['sha256']
    source = read_pin(ref(RUN.parent / 'trien-khai-002/source-current.json'))
    for relative, pin in source['legacy_code'].items():
        from bien_nhan import digest
        assert digest(ROOT / relative) == (pin if isinstance(pin, str) else pin['sha256']), relative
    code_pins = dict(source['legacy_code'])
    code_pins.update({p.relative_to(ROOT).as_posix(): ref(p)['sha256'] for p in (OUT / 'scripts').glob('*.py')})
    candidates = read_pin(ref(OUT / 'pilot-plan.json'))['candidates']
    env_main, env38 = environment(MAIN), environment(PY38)
    atomic(dest / 'environments.json', {'main': env_main, 'py38': env38, 'threads': 1})
    main_sha, py38_sha = fingerprint(env_main), fingerprint(env38)
    runtime_refs = {}; descriptor_refs = {}; runtimes = {}
    for ds, ids in selected.items():
        refs = {oid: next(c['native_command_pin'] for c in candidates
                         if c['dataset'] == ds and c['opaque_id'] == oid and c['window'] == 'that') for oid in ids}
        original = {'schema': 'T054-DEV-ORIGINALS-1', 'dataset': ds, 'g1_revision': revision,
                    'g1_ref': g1, 'selected_ids': ids, 'command_refs': refs,
                    'allowlist_ref': ref(ROOT / ('results/T-022/allowlist-dev.json' if ds == 'RE2-TT'
                                                 else 'results/T-026/allowlist-dev.json'))}
        normalized = original_dev_sources(original)
        # Chỉ ánh xạ mã mờ với member đã tính lại từ nguồn gốc, không đưa nhãn vào job.
        rows = {}
        for oid in ids:
            one = original_dev_sources(dict(original, selected_ids=[oid]))
            rows[oid] = next(iter(one['cases_by_member'].values()))
        runtime = {'dataset': ds, 'g1_revision': revision, 'inventory': cohort['inventory'][ds], 'cases': rows}
        compare_sources(runtime, original, ds, revision)
        key = 'TT' if ds == 'RE2-TT' else 'OB'
        runtime_refs[ds] = atomic(private / (key + '-runtime.json'), runtime)
        descriptor_refs[ds] = atomic(private / (key + '-originals.json'), original)
        runtimes[ds] = runtime
    jobs = []
    for ds, runtime in runtimes.items():
        for oid, row in runtime['cases'].items():
            t = row.get('t', row.get('t_ns', 0) // 10**9)
            common = {'source': row, 'data_root': str(ROOT), 'runtime_ref': runtime_refs[ds],
                      'independent_source_ref': descriptor_refs[ds], 'g1_revision': revision,
                      'inventory': runtime['inventory'], 't': t, 'pythonpath': PATHS,
                      'evaluation_mode': 'dev', 'code_pins': code_pins,
                      'm1_contract': ref(ROOT / 'results/T-043/hop-dong.json'),
                      'static_snapshot': protocol['snapshots'][ds], 'timeout_s': 600, 'executable': MAIN}
            for arm in (protocol['configurations'] if arms is None else arms):
                config = protocol['configurations'][arm]['config']
                slot = {'dataset': ds, 'opaque_id': oid, 'member_sha256': row['member_sha256'],
                        'arm': arm, 'view': 'main', 'seed': None, 'window': {'t': t, 'half_width_s': 300},
                        'source_sha256': fingerprint(row), 'config_sha256': fingerprint(config),
                        'environment_sha256': main_sha}
                jobs.append(dict(common, kind='m1', slot=slot, config=config, a4=arm == 'M1'))
            for arm in (('baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai_B')
                        if baseline_arms is None else baseline_arms[ds]):
                for seed in ((0, 1, 2) if ds == 'RE2-TT' and arm == 'torai_B' else (None,)):
                    cfg = {'method': arm, 'mode': 'a', 'source': 'P3-v2/Q85', 'half_width_s': 300}
                    is_torai = arm == 'torai_B' and ds == 'RE2-TT'
                    slot = {'dataset': ds, 'opaque_id': oid, 'member_sha256': row['member_sha256'],
                            'arm': arm, 'view': 'main', 'seed': seed, 'window': {'t': t, 'half_width_s': 300},
                            'source_sha256': fingerprint(row), 'config_sha256': fingerprint(cfg),
                            'environment_sha256': py38_sha if is_torai else main_sha}
                    jobs.append(dict(common, slot=slot, kind='torai_pipeline' if is_torai else 'baseline',
                                config=cfg, a4=arm == ('torai_B' if ds == 'RE2-TT' else 'simplerca'),
                                prep_executable=MAIN, method_executable=PY38, prep_environment_sha256=main_sha,
                                method_version='P3 frozen adapter; provenance source-current'))
            if ds == 'RE2-TT' and include_cd3:
                parent = next(j for j in jobs if j['slot']['opaque_id'] == oid and j['slot']['arm'] == 'M1')
                slot = dict(parent['slot'], arm='C-d3', config_sha256=fingerprint({'cd3': 'same sealed M1'}))
                jobs.append(dict(common, slot=slot, kind='cd3', a4=False, timeout_s=60,
                                 main_dependency={'slot': parent['slot'], 'job_sha256': fingerprint(parent)}))
    plan = {'schema': 'T054-PLAN-1', 'mode': 'dev', 'host_role': 'local', 'directory': str(dest / 'queue'),
            'jobs': jobs, 'inventories': cohort['inventory'], 'open_before_run': [],
            'monitor': {'poll_s': .2, 'max_monitor_gap_s': 5, 'score_phases': []},
            'budget': {'wall_s': 3600, 'method_dataset_s': {j['slot']['dataset'] + '|' + j['slot']['arm']: 1800 for j in jobs}},
            'scientific_timeout_scoring': 'NOT_ENABLED; preserve/block on failure; no test inference'}
    no_labels(plan)
    plan_ref = atomic(dest / 'plan.json', plan)
    authority = {'schema': 'T054-AUTHORITY-1', 'source': ref(RUN / 'quyen-minh.txt'),
                 'pilot_grant': True, 'materialize_private': True, 'plan_sha256': fingerprint(plan),
                 'torai_A_source_grant': False, 'g3': False, 'test_grant': False, 'ssh_grant': False,
                 'scope': 'local selected DEV only, stop before main run; cap one hour not ETA'}
    auth_ref = atomic(dest / 'authority.json', authority)
    atomic(dest / 'metadata.json', {'plan': plan_ref, 'authority': auth_ref, 'runtime_refs': runtime_refs,
                                  'original_refs': descriptor_refs, 'slot_count': len(jobs), 'test_opened': False})
    return plan_ref, auth_ref


if __name__ == '__main__':
    p, a = build(sys.argv[1], {'RE2-TT': ['dev-a5cabe5fa7'], 'Nezha-OB': ['dev-607751ac0a']})
    result = subprocess.run([MAIN, '-B', str(OUT / 'scripts/p7.py'), 'run', '--plan', p['path'],
                   '--sha256', p['sha256'], '--authority', a['path'], '--authority-sha256', a['sha256']],
                   env=ENV, capture_output=True)
    atomic(RUN / sys.argv[1] / 'launch.json', {'exit_code': result.returncode,
               'stdout': result.stdout.decode('utf-8'), 'stderr': result.stderr.decode('utf-8')})
    print(result.stdout.decode('utf-8')); print(result.stderr.decode('utf-8')); result.check_returncode()
