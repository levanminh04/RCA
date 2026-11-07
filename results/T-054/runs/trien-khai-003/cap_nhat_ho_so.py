"""Đồng bộ hồ sơ hiện hành sau khi pilot dừng; không đổi quyết định khoa học."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path.insert(0, str(OUT / 'scripts'))
from bien_nhan import atomic as atomic_new, canonical, fingerprint, read_pin, ref
from dieu_phoi import status


def atomic(path, value):
    # Chỉ các hồ sơ hiện hành đã có snapshot before-files mới được thay.
    # Đầu ra run/manifest vẫn create-only và giữ mọi bản cũ.
    if path.parent == OUT and path.exists():
        assert (RUN / 'before-files' / path.name).exists()
        staged = RUN / 'updated-documents-003' / path.name
        pin = atomic_new(staged, value)
        temporary = path.with_name(path.name + '.update-pending')
        assert not temporary.exists()
        temporary.write_bytes(staged.read_bytes())
        temporary.replace(path)
        return ref(path)
    return atomic_new(path, value)


def update():
    pilot_dir = RUN / 'pilot-local-007'
    if any(status(RUN / name / 'queue')['controller'] is not None for name in ('pilot-local-007', 'pilot-local-008')):
        raise RuntimeError('Không cập nhật hồ sơ code đang chạy')
    p = read_pin(ref(OUT / 'protocol.json'))
    p.pop('fingerprint', None)
    p['implementation'] = 'DEV pilot local toàn tuyến đã có kết quả; thêm gói nhỏ hai ca và chẩn đoán luồng riêng. Chưa đủ phủ nhánh/throughput để đóng pha1 hoặc G3.'
    p['dev_pilot_authorized'] = True
    p['real_execution_ready_scope'] = 'main/test only; not a denial of recorded DEV pilot grant'
    p['not_yet_authorized'] = ['commit/push khóa', 'G3', 'mở test/RE3', 'chạy P7 chính', 'A ngoài đúng ca dev được grant']
    p['torai_scope'] = {'primary': 'B', 'auxiliary': 'A outside A4',
                        'source': ref(OUT / 'manifest-quyet-dinh-001.json'),
                        'choice_open': False, 'A_source_access_granted': 'one DEV case only',
                        'A_source_grant': ref(RUN / 'grant-A-dev.json'),
                        'baseline_both_already_run': 'results/T-024/cham-a.json; pin tại pilot-proposal checkpoint002'}
    p['open_choices'] = ['budget exhaustion scoring rule and numeric main caps', 'TORAI A source grant',
                        'test source/label binding authority', 'error-excluded and case-permutation formulas',
                        'main timeout/monitor-gap/resources', 'machine final plan after parity']
    p['required_permissions'] = ['G3 and finalized policy', 'main test grant', 'A source grant',
                                 'RE3 schema/adapter/final grant as separately scoped', 'SSH/sync if used']
    p['pilot_time'] = {'local_cap_s': 3600, 'cap_is_not_ETA': True,
                       'proposal_3h': 'historical unapproved proposal, not runtime estimate',
                       'current_metadata': ref(pilot_dir / 'metadata.json')}
    p['RE3_preparation'] = ref(RUN / 'hop-dong-re3.json')
    p['pilot_evidence'] = {'first_packet': ref(RUN / 'pilot-local-007/summary.json'),
                           'first_packet_parity': ref(RUN / 'pilot-local-007/parity-complete.json'),
                           'additional_packet': ref(RUN / 'pilot-local-008/metadata.json'),
                           'additional_packet_summary': ref(RUN / 'pilot-local-008/summary.json'),
                           'additional_packet_parity': ref(RUN / 'pilot-local-008/parity.json'),
                           'thread_diagnostic': ref(RUN / 'diagnostic-thread-001/summary.json')}
    p['timing_evidence'] = ref(RUN / 'thoi-gian-va-kich-ban.json')
    if 'runtime_dependencies_historical' not in p:
        p['runtime_dependencies_historical'] = p['runtime_dependencies']
    current_envs = read_pin(ref(RUN / 'environments-corrected.json'))
    paths = read_pin(ref(pilot_dir / 'plan.json'))['jobs'][0]['pythonpath']
    p['runtime_dependencies'] = {'environments': {
        name: {'python': env['python'], 'python_executable': env['executable']['path'],
               'python_executable_pin': env['executable'], 'packages': env['packages'],
               'PYTHONHASHSEED': 0, 'PYTHONPATH_append': paths, 'thread_environment': env['threads']}
        for name,env in current_envs.items()},
        'external_code': p['runtime_dependencies_historical']['external_code'],
        'verification': ref(RUN / 'external-code-checks.json'),
        'note': 'actual local DEV environments; not yet G3 main choice; standalone16 diagnostic not substituted here'}
    p['status'] = 'CANDIDATE_NOT_LOCKED'
    p['real_execution_ready'] = False
    p['fingerprint'] = fingerprint(p)
    atomic(OUT / 'protocol.json', p)
    m = read_pin(ref(OUT / 'matrix.json'))
    cohort = read_pin(p['cohorts_source'])
    m['auxiliary'] = [{'dataset': 'RE2-TT', 'opaque_id': 'test-' + member[:10], 'member_sha256': member,
                       'arm': 'torai_A', 'view': 'main', 'seed': seed, 'a4': False,
                       'worlds': ['P'], 'source_access': 'WAIT_A_SOURCE_GRANT'}
                      for member in cohort['cohorts']['RE2-TT']['members_locked_sha256'] for seed in (0, 1, 2)]
    m['torai_A'] = {'scope': 'auxiliary outside A4, already confirmed',
                    'source_grant': False, 'slots': 180, 'prep_calls_without_cache': 180,
                    'prep_calls_if_real_parity_passes': 60}
    m['counts']['auxiliary_A_core_calls'] = len(m['auxiliary'])
    m['RE3'] = {'status': 'CONTRACT_PREPARATION_ONLY', 'contract': ref(RUN / 'hop-dong-re3.json'),
                'matrix_not_finalized': True, 'not_in_main94': True}
    atomic(OUT / 'matrix.json', m)
    a = read_pin(ref(OUT / 'authorization.json'))
    a.update(source=ref(RUN / 'quyen-minh.txt'), pilot_grant=True, materialize_private=True,
             pilot_scope='selected local DEV plans with own source refs/cap; not a blanket grant',
             pilot_plan_refs=[ref(pilot_dir / 'plan.json'), ref(RUN / 'pilot-local-008/plan.json')],
             torai_A_source_grant='only plan-bound dev-a5cabe5fa7, not main A cohort',
             A_grant_ref=ref(RUN / 'grant-A-dev.json'),
             stop_before_main=True, g3=False, test_grant=False, ssh_grant=False, sync_grant=False,
             commit_push=False, RE3_telemetry=False)
    atomic(OUT / 'authorization.json', a)
    atomic(OUT / 'environment.json', {'status': 'ACTUAL_DEV_LOCAL_PILOT_ENVIRONMENTS_NOT_G3',
          'one_thread_environments': read_pin(ref(RUN / 'environments-corrected.json')),
          'diagnostic_only_environment': ref(RUN / 'diagnostic-thread-001/environment.json'),
          'main_thread_exception_not_approved': True, 'cloud': 'NOT_INSPECTED_NO_SSH',
          'test_opened': False})
    pilot = read_pin(ref(RUN / 'before-files/pilot-plan.json'))
    pilot.update(status='LOCAL_DEV_PIPELINE_MEASURED_NOT_FULL_COVERAGE_NOT_MAIN_READY',
                 current_local_metadata=ref(pilot_dir / 'metadata.json'),
                 torai_A={'scope': 'auxiliary confirmed; one DEV case grant received',
                          'main_source_grant': False, 'DEV_grant': ref(RUN / 'grant-A-dev.json')},
                 proposed_3h_not_ETA=True,
                 additional_local=ref(RUN / 'pilot-local-008/metadata.json'),
                 diagnostic=ref(RUN / 'diagnostic-thread-001/summary.json'),
                 remaining_before_main=['real parity/coverage evidence', 'remaining declared policies',
                                        'G3 and separate exact main grant', 'A source and pilot branch'])
    atomic(OUT / 'pilot-plan.json', pilot)
    old = read_pin(ref(RUN / 'before-files/source-manifest.json'))
    old['previous_manifest'] = ref(RUN / 'before-files/source-manifest.json')
    old['own_scripts'] = {f.relative_to(ROOT).as_posix(): ref(f) for f in (OUT / 'scripts').glob('*.py')}
    old['authority'] = ref(RUN / 'quyen-minh.txt')
    old['current_pilot'] = ref(pilot_dir / 'metadata.json')
    old['private_sources_materialized'] = 'selected DEV including one explicitly granted A case; not test/main A cohort/RE3'
    atomic(OUT / 'source-manifest.json', old)
    reuse = read_pin(ref(RUN / 'before-files/reuse.json'))
    reuse.update(real_driver_parity='FIELDWISE_LOCAL_DEV; MicroRank one-thread1ULP/diagnostic16 exact; second OB M1/T12 small float differences vs EC2; no main exception/tolerance approved',
                 evidence=[ref(RUN / 'pilot-local-007/parity-complete.json'),ref(RUN / 'pilot-local-008/parity.json')],
                 limitations='two-case full-route packet plus small two-case extension, not full-cohort/all-branch or independent test proof')
    atomic(OUT / 'reuse.json', reuse)
    print(json.dumps({'updated': ['protocol', 'matrix', 'authorization', 'pilot-plan', 'source-manifest'],
                      'A_choice_reopened': False, 'G3': False, 'main_run_started': False}))


if __name__ == '__main__':
    update()
