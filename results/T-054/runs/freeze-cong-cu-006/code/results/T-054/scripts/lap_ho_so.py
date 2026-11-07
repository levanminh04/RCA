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
            'torai_A': {'scope': 'A phụ ngoài A4, B chính theo P3 và Minh xác nhận lại',
                         'source_grant': False},
            'auxiliary': [{'dataset': 'RE2-TT', 'opaque_id': 'test-' + m[:10],
                           'member_sha256': m, 'arm': 'torai_A', 'view': 'main', 'seed': seed,
                           'worlds': ['P'], 'a4': False, 'source_access': 'WAIT_A_SOURCE_GRANT'}
                          for m in cohort['cohorts']['RE2-TT']['members_locked_sha256'] for seed in (0, 1, 2)],
            'test_sources_materialized': False}


def build_documents(destination=None):
    """Kiểm và xuất bản sao hồ sơ hiện hành, không reset quyền bằng mặc định cũ.

    Cập nhật hồ sơ phải có nguồn quyết định mới và manifest riêng. Lệnh này không
    còn tái sinh ứng viên cũ trước câu trả lời Minh về A/B hay tự hạ/nâng quyền.
    """
    current = {name: read_pin(ref(OUT / name)) for name in
               ('protocol.json', 'matrix.json', 'authorization.json', 'source-manifest.json')}
    source = current['source-manifest.json']
    for path, expected in source['own_scripts'].items():
        actual = ref(ROOT / path)
        if actual['sha256'] != expected['sha256']:
            raise ValueError('source-manifest chưa cập nhật code: ' + path)
    summary = {'status': current['protocol.json']['status'],
               'matrix': current['matrix.json']['counts'],
               'own_scripts': len(source['own_scripts']),
               'authorization': ref(OUT / 'authorization.json'),
               'documents_overwritten': False, 'test_opened': False}
    if destination is not None:
        target = Path(destination).resolve()
        if not (target.is_relative_to(OUT / 'runs') or target.is_relative_to(OUT / 'reports')):
            raise ValueError('đích hồ sơ ngoài phạm vi T054 runs/reports')
        target.mkdir(parents=True, exist_ok=False)
        copies = {}
        for name, value in current.items():
            copies[name] = atomic(target / name, value)
        summary['exported_documents'] = copies
        atomic(target / 'summary.json', summary)
    return summary


if __name__ == '__main__':
    import json
    print(json.dumps(build_documents(sys.argv[1] if len(sys.argv) > 1 else None), ensure_ascii=False))
