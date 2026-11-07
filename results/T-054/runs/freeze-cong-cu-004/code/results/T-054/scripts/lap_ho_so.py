"""Lập ứng viên từ metadata đã được phép; không materialize test."""
import importlib.metadata
import os
import platform
import shutil
import sys
from pathlib import Path
from collections import Counter

from bien_nhan import ROOT, OUT, atomic, fingerprint, read_pin, ref


def preflight():
    packages = {}
    for name in ('numpy', 'pandas', 'pyarrow', 'scipy', 'scikit-learn', 'networkx', 'psutil', 'drain3', 'causal-learn'):
        try: packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: packages[name] = None
    free_ram = None
    try:
        import psutil
        free_ram = psutil.virtual_memory().available
    except ImportError:
        pass
    return {'python': sys.version, 'executable': ref(sys.executable), 'platform': platform.platform(),
            'packages': packages, 'free_ram': free_ram, 'free_disk': shutil.disk_usage(ROOT).free,
            'threads': {k: os.environ.get(k) for k in ('PYTHONHASHSEED', 'OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS')},
            'test_opened': False, 'ssh_used': False}


def stable_environment():
    info = preflight()
    return {k: info[k] for k in ('python', 'executable', 'platform', 'packages', 'threads')}


def matrix(protocol, cohort):
    jobs, derived = [], []
    methods = ('baro', 'simplerca', 'microrank', 'tracerca', 'circa', 'torai_B')
    for ds in ('RE2-TT', 'Nezha-OB'):
        for member in cohort['cohorts'][ds]['members_locked_sha256']:
            oid = 'test-' + member[:10]
            for arm in (*methods, *protocol['configurations']):
                seeds = (0, 1, 2) if ds == 'RE2-TT' and arm == 'torai_B' else (None,)
                for seed in seeds:
                    jobs.append({'dataset': ds, 'opaque_id': oid, 'member_sha256': member, 'arm': arm,
                                 'view': 'main', 'seed': seed, 'supported_core': not (ds == 'Nezha-OB' and arm in ('circa', 'torai_B')),
                                 'worlds': ['P', 'S_lo', 'S_hi'] if arm in protocol['configurations'] else ['fixed'],
                                 'a4': arm == 'M1' or arm == ('torai_B' if ds == 'RE2-TT' else 'simplerca')})
            for arm in ('C-d1', 'C-d2', 'C-c', 'C-g', 'C-d3'):
                derived.append({'dataset': ds, 'opaque_id': oid, 'arm': arm, 'view': 'main', 'world': 'P',
                                'separate_worker': ds == 'RE2-TT' and arm == 'C-d3',
                                'support_contract_only': ds == 'Nezha-OB' and arm == 'C-d3'})
    ce = [{'dataset': 'RE2-TT', 'opaque_id': 'test-' + m[:10], 'arm': 'M1', 'view': 'ce',
           'history_status': 'OPEN_BEFORE_MATERIALIZE', 'a4': False}
          for m in cohort['cohorts']['RE2-TT']['members_locked_sha256']]
    return {'schema': 'T054-MATRIX-1', 'status': 'CANDIDATE_NOT_EXECUTABLE', 'main': jobs, 'derived': derived,
            'ce': ce, 'counts': {'main_slots': len(jobs), 'core_calls_excluding_unsupported': sum(j['supported_core'] for j in jobs),
            'separate_cd3_workers': sum(j['separate_worker'] for j in derived), 'ce_max': len(ce)},
            'torai_A': 'OPEN: chưa tự loại hoặc thêm trước Minh quyết', 'test_sources_materialized': False}


def build_documents():
    """Chỉ tạo hồ sơ CANDIDATE; không điền quyền/policy OPEN để phát lô."""
    import json
    import collections
    from pilot import plan_candidate
    sys.path.append(str(ROOT / 'results/T-052/scripts'))
    import common
    old_ref = ref(ROOT / 'results/T-052/giao-thuc-p7-a-003.json')
    old = read_pin(old_ref)
    cohort = read_pin(old['cohorts_source'])
    own = {p.relative_to(ROOT).as_posix(): ref(p) for p in (OUT / 'scripts').glob('*.py')}
    protocol = dict(old)
    protocol.pop('fingerprint', None)
    protocol.update(schema='T054-PROTOCOL-1', status='CANDIDATE_NOT_LOCKED',
                    entrypoint='results/T-054/scripts/p7.py', previous_protocol=old_ref,
                    implementation='checkpoint synthetic verified; real pilot still WAIT',
                    real_execution_ready=False,
                    required_permissions=['pilot grant and budget', 'G3 and finalized policy', 'test grant',
                                          'independent source/label provider and materialize permission'],
                    decision_changes=[], open_choices=['budget exception', 'TORAI A', 'source/labels provider',
                        'error-excluded and case-permutation formulas', 'timeouts/monitor-gap/resources', 'machine plan/deadline'])
    protocol['fingerprint'] = fingerprint(protocol)
    atomic(OUT / 'protocol.json', protocol)
    m = matrix(old, cohort)
    assert m['counts'] == {'main_slots': 1342, 'core_calls_excluding_unsupported': 1274,
                           'separate_cd3_workers': 60, 'ce_max': 60}
    atomic(OUT / 'matrix.json', m)
    atomic(OUT / 'authorization.json', {'schema': 'T054-AUTHORITY-1',
           'source': ref(OUT / 'runs/trien-khai-001/quyen-minh.txt'), 'implementation': True,
           'synthetic_fixtures': True, 'pilot_grant': False, 'ssh_grant': False, 'sync_grant': False,
           'g3': False, 'test_grant': False, 'materialize_private': False, 'commit_push': False,
           'note': 'False nghĩa là chưa có quyền riêng được ghi, không là Minh từ chối.'})
    atomic(OUT / 'environment.json', dict(preflight(), status='LOCAL_CODE_INSPECTION_ONLY',
                                         stable=stable_environment(), cloud='NOT_INSPECTED_NO_SSH'))
    atomic(OUT / 'source-manifest.json', {'schema': 'T054-SOURCE-1', 'own_scripts': own,
           'legacy_code': old['source_code'], 'upstream_manifests': [ref(ROOT / p) for p in (
               'results/T-052/manifest-dinh-chinh-g3-004.json', 'results/T-050/manifest-chay-lai-002.json',
               'results/T-053/manifest.json', 'results/T-054/manifest-soan-spec-001.json')],
           'snapshots': old['snapshots'], 'cohorts_source': old['cohorts_source'],
           'private_sources_materialized': False})
    atomic(OUT / 'reuse.json', {'status': 'CONDITIONAL_REUSE', 'stable_outputs_verified':
          {'T052': 576, 'T050': 297, 'T053': 2654, 'protocol_code': 93},
          'historical_pins_excluded': ['T052 LOG', 'docs/STATE.md'],
          'requirements': ['same member/window/config/seed/variant', 'input/intermediate/rank/region parity',
                           'source machine per window; exact decisions even cross-machine',
                           'new full driver must pass dev; hash alone insufficient'],
          'no_bulk_rerun': True, 'real_driver_parity': 'NOT_YET_RUN'})
    manifest, native = common.native_index()
    pilot = plan_candidate()
    selected = {'dev-a915aa2424', 'dev-a5cabe5fa7', 'dev-bcbd4f46ae', 'dev-03d4910932',
                'dev-607751ac0a', 'dev-2bfc97b01e', 'dev-63c30faf34', 'dev-5467884de4'}
    pilot['candidates'] = [{'opaque_id': oid, 'window': w, 'dataset': command['job']['dataset'],
           'native_machine': 'EC2' if command['platform'].startswith('Linux') else 'laptop',
           'native_command_pin': ref(ROOT / (item['path'].rsplit('/', 1)[0] + '/command.json')),
           'native_record': item} for (oid, w), (item, command) in native.items() if oid in selected]
    pilot['source_machine_counts'] = [{'dataset': ds, 'window': w, 'machine': host, 'n': n}
        for (ds, w, host), n in collections.Counter((c['job']['dataset'], w,
            'EC2' if c['platform'].startswith('Linux') else 'laptop') for (_, w), (_, c) in native.items()).items()]
    pilot['execution_plan_ready'] = False
    pilot['remaining_before_pilot'] = ['materialize selected DEV runtime/source binding in T054',
        'pin effective Python paths and per-stage TORAI environments', 'freeze final driver bytes',
        'choose exact minimal branch cover from candidates; budget and SSH grant',
        'C-d3 subprocess fixture passed; integrate sealed main -> worker job in registered real plan',
        'method-failure finalization requires decided policy and pinned classification evidence']
    atomic(OUT / 'pilot-plan.json', pilot)
    return {'matrix': m['counts'], 'own_scripts': len(own), 'test_opened': False}


if __name__ == '__main__':
    import json
    print(json.dumps(build_documents(), ensure_ascii=False))
