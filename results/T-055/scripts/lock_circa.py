"""T-055 D-55-9: gói khóa bổ sung RE3 chỉ vế CIRCA, chạy laptop (môi trường CIRCA đã kiểm).

Dùng lại profile/runtime/nguồn độc lập của gói chính (cùng byte), protocol riêng (arms = circa), policy lỗi v2.
Đầu ra: results/T-054/runs/re3-ban-cuoi-001/meta-circa/ (trong repo và bản sao trong code root cục bộ).
"""
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LR = Path('D:/RCA-ext/T-055/work-re3-local')
sys.path[:0] = [str(ROOT / 'results/T-054/scripts'), str(ROOT / 'src')]
from bien_nhan import fingerprint  # noqa: E402

META = 'results/T-054/runs/re3-ban-cuoi-001/meta'
MC = 'results/T-054/runs/re3-ban-cuoi-001/meta-circa'
MAIN = 'results/T-054/runs/chuan-bi-main-013-v2'
DATA_ROOT = 'D:/RCA-ext/T-055/data-root'


def L(p):
    return json.loads((ROOT / p).read_bytes())


def ref(rel):
    raw = (ROOT / rel).read_bytes()
    return {'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def write(rel, value):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, ensure_ascii=False, indent=1, sort_keys=True).encode()
    with open(p, 'xb') as f:
        f.write(raw)
    return {'path': rel, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def main():
    main_protocol = L(META + '/protocol.json')
    profile_ref, runtime_ref = ref(META + '/profile.json'), ref(META + '/runtime.json')
    ind_ref = ref('results/T-055/runs/nguon-001/independent-source.json')
    runtime = L(runtime_ref['path'])
    contract = L(MAIN + '/dispatch-contract.json')['hosts']['local']
    code_pins = dict(L(MAIN + '/code-pins.json')['code_pins'])
    overlay = ref('results/T-055/overlay-v2/results/T-054/scripts/bien_nhan.py')
    code_pins['results/T-054/scripts/bien_nhan.py'] = overlay['sha256']
    config = main_protocol['dispatch']['hosts']['ec2_1']['configurations']['circa']
    fp = write(MC + '/failure-policy.json', {
        'schema': 'T054-FAILURE-POLICY-1', 'scope': 'LOCKED_RE3', 'dataset': 'RE3-OB',
        'error_rules': ['RE3_METHOD_ERROR_IS_MISS'], 'code_evidence': [],
        'monitor': {'max_monitor_gap_s': 5, 'poll_s': 0.1, 'score_phases': ['method']},
        'timeout_s': {'main_slot': 600},
        'unknown_errors': 'v2 (D-55-9): ERROR phương pháp = trượt; ERROR môi trường/import (ModuleNotFoundError, ImportError, OSError, MemoryError, PermissionError) = BLOCKED.',
        'overlay': overlay})
    env = contract['environment_sha256']
    host = {'code_pins': code_pins, 'configurations': {'circa': config}, 'environments': env,
            'm1_contract_ref': main_protocol['dispatch']['hosts']['ec2_1']['m1_contract_ref'],
            'failure_policy_ref': fp, 'data_root': DATA_ROOT, 'pythonpath': contract['pythonpath'],
            'executable': contract['executable'], 'prep_executable': contract['prep_executable'],
            'method_executable': contract['method_executable']}
    slots = []
    for m in main_protocol['members']:
        oid = 'test-' + m[:10]
        row = runtime['cases'][oid]
        slots.append({'dataset': 'RE3-OB', 'opaque_id': oid, 'member_sha256': m, 'arm': 'circa', 'view': 'main',
                      'seed': None, 'window': {'t': row['t'], 'half_width_s': 300},
                      'source_sha256': fingerprint(row), 'config_sha256': fingerprint(config),
                      'environment_sha256': env['main']})
    protocol = {k: main_protocol[k] for k in ('schema', 'dataset', 'status', 'final_version', 'case_count',
                                               'cell_count', 'members', 'g1_revision', 'worlds', 'metrics',
                                               'seed_aggregation', 'support_policy')}
    protocol.update(arms={'circa': [None]}, slots=slots, variants={'circa': ['ols+rht_da', 'ols+rht']},
                    partitions={'local': [fingerprint(s) for s in slots]}, dispatch={'hosts': {'local': host}},
                    supplement_of=ref(META + '/protocol.json'),
                    reason='D-55-9: 30 slot CIRCA của lượt chính lỗi ModuleNotFoundError trên EC2 (môi trường, không phải phương pháp); chạy lại riêng vế CIRCA trên môi trường CIRCA đã kiểm, trước ghép nhãn.')
    protocol_ref = write(MC + '/protocol.json', protocol)
    binding_ref = write(MC + '/runtime-binding.json', {
        'protocol_sha256': protocol_ref['sha256'], 'profile_sha256': profile_ref['sha256'],
        'runtime_sha256': runtime_ref['sha256'], 'independent_source_sha256': ind_ref['sha256']})
    grant_ref = write(MC + '/grant.json', {
        're3_grant': True, 'g3': True, 'source': ref('results/T-055/grants/minh-re3-source.json'),
        'protocol_sha256': protocol_ref['sha256'], 'profile_sha256': profile_ref['sha256'],
        'runtime_sha256': runtime_ref['sha256'], 'independent_source_sha256': ind_ref['sha256'],
        'runtime_binding_sha256': binding_ref['sha256'], 'commit_push_grant': False,
        'operator': 'Claude; reviewer Codex (sau)'})
    tmpl = next(j for j in L(MAIN + '/activated-001/local-plan.json')['jobs'] if j['slot']['arm'] == 'circa')
    tmpl_plan = L(MAIN + '/activated-001/local-plan.json')
    jobs = []
    for s in slots:
        job = copy.deepcopy(tmpl)
        for k in ('main_dependency', 'author_source_ref', 'm1_contract'):
            job.pop(k, None)
        job.update(kind='baseline', slot=s, config=config, code_pins=code_pins, evaluation_mode='heldout',
                   source=runtime['cases'][s['opaque_id']], t=s['window']['t'], g1_revision=runtime['g1_revision'],
                   inventory=runtime['inventory'], data_root=DATA_ROOT, pythonpath=host['pythonpath'],
                   executable=host['executable'], prep_executable=host['prep_executable'],
                   method_executable=host['method_executable'], timeout_s=600, protocol_ref=protocol_ref,
                   runtime_ref=runtime_ref, independent_source_ref=ind_ref, runtime_binding_ref=binding_ref,
                   re3_grant_ref=grant_ref, re3_profile_ref=profile_ref, failure_policy_ref=fp, re3_host='local',
                   a4=False, static_snapshot=None)
        jobs.append(job)
    plan = {'schema': 'T054-PLAN-1', 'mode': 'heldout', 'host_role': 'local', 'jobs': jobs,
            'directory': str(LR / 'results/T-054/runs/re3-ban-cuoi-001/queue-circa').replace('\\', '/'),
            'protocol_ref': protocol_ref, 're3_grant_ref': grant_ref, 're3_profile_ref': profile_ref,
            'budget': tmpl_plan['budget'], 'monitor': tmpl_plan['monitor'], 'open_before_run': [],
            'preparation_only': False, 'workers': 2,
            'resources': {'expected_peak_bytes': {'RE3-OB|circa': 1073741824}, 'factor': 1.25,
                          'reserve_bytes': 402653184, 'note': 'TT CIRCA laptop ~0,84 GB; RE3 nhỏ hơn TT'},
            'inventories': {'RE3-OB': runtime['inventory']}}
    plan_ref = write(MC + '/local-plan.json', plan)
    # Bản sao vào code root cục bộ, cùng đường dẫn tương đối.
    for rel in [META + '/profile.json', META + '/runtime.json', META + '/protocol.json',
                'results/T-055/runs/nguon-001/independent-source.json', 'results/T-055/grants/minh-re3-source.json',
                'results/T-055/grants/minh-re3.txt', fp['path'], protocol_ref['path'], binding_ref['path'],
                grant_ref['path'], plan_ref['path']]:
        dest = LR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, dest)
    print(json.dumps({'protocol': protocol_ref['sha256'][:12], 'grant': grant_ref['sha256'][:12],
                      'plan': plan_ref['sha256'], 'jobs': len(jobs)}))


if __name__ == '__main__':
    main()
