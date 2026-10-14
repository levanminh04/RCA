"""T-032 preparation: verify copied files and old read-only sources, no method run."""
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import traceback

BASE = Path.home() / 'rca/T-032'
REPO = BASE / 'repo'
RUN = BASE / 'runs/prepare-002'

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for b in iter(lambda: stream.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def dump(name, data):
    (RUN / name).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')

def safe_relative(name):
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts
    assert 'locked' not in p.parts and 'T-033' not in p.parts
    assert p.suffix not in ('.pem', '.key')
    return p

def main():
    RUN.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    checks = []
    def check(path, wanted, provenance):
        actual = sha(path)
        row = {'path': str(path), 'expected': wanted, 'actual': actual,
               'pass': actual == wanted, 'source': provenance, 'bytes': Path(path).stat().st_size}
        checks.append(row)
        if not row['pass']:
            dump('checks.json', checks)
            raise ValueError('hash mismatch: ' + str(path))
    try:
        package = read(BASE / 'inputs/package-manifest.json')
        for row in package['files']:
            check(REPO / safe_relative(row['path']), row['sha256'], 'package-manifest.json#/files')
        print('PACKAGE_PASS', len(package['files']), flush=True)
        # Compare copied computational sources with the frozen Nezha index.
        i26 = read(REPO / 'results/T-026/ban-ghi-dua-vao-cham.json')
        code_count = 0
        for name, expected in i26['source_hashes'].items():
            if name.startswith('src/'):
                check(REPO / safe_relative(name), expected, 'T026 frozen index#/source_hashes')
                code_count += 1
        print('TASK_CODE_PASS', code_count, flush=True)
        ext = read(REPO / 'results/T-026/runs/session-005/external-code-manifest.json')
        ext_rows = []
        for name, expected in ext['external_source_hashes'].items():
            assert name.startswith('D:/RCA-ext/src/')
            remote = Path.home() / 'rca/T-025/src' / name.removeprefix('D:/RCA-ext/src/')
            check(remote, expected, 'T026 external-code-manifest.json')
            ext_rows.append(str(remote))
        print('EXTERNAL_CODE_PASS', len(ext_rows), flush=True)
        allow = read(REPO / 'results/T-022/allowlist-dev.json')
        assert allow['so_ca'] == len(allow['cases']) == 30
        raw_count = 0
        for case in allow['cases']:
            for name, row in case['files'].items():
                if row is None:
                    continue
                rel = safe_relative(row['path'])
                assert rel.parts[:2] == ('data', 'rcaeval')
                check(Path.home() / 'rca/T-031/repo' / rel, row['sha256'], 'RE2 dev allowlist')
                raw_count += 1
            print('RE2_PASS', case['opaque_id'], flush=True)
        for row in read(BASE / 'inputs/nezha-transfer-manifest.json')['files']:
            check(REPO / safe_relative(row['path']), row['sha256'], 'Nezha dev allowlist')
        print('NEZHA_PASS', flush=True)
        packages = {}
        for name in ('numpy', 'pandas', 'scipy', 'sklearn', 'networkx', 'pyarrow', 'psutil'):
            module = importlib.import_module(name)
            packages[name] = module.__version__
        expected_versions = {'numpy':'1.26.4', 'pandas':'2.2.3', 'scipy':'1.14.1',
                             'sklearn':'1.6.0', 'networkx':'2.8.8', 'pyarrow':'18.1.0', 'psutil':'6.1.1'}
        assert packages == expected_versions, (packages, expected_versions)
        import numpy as np
        import psutil
        env = {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(),
               'packages': packages, 'numpy_configuration': np.show_config(mode='dicts'),
               'env': {k:os.environ.get(k) for k in ('PYTHONHASHSEED','OMP_NUM_THREADS','OPENBLAS_NUM_THREADS',
                                                    'MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONPATH')},
               'cpu_logical': psutil.cpu_count(), 'memory': dict(psutil.virtual_memory()._asdict()),
               'disk': dict(psutil.disk_usage(str(BASE))._asdict()),
               'python_exception_authorized': 'Minh approved existing EC2 Python 3.12.3, frozen equality unchanged'}
        dump('environment.json', env)
        dump('checks.json', checks)
        dump('status.json', {'status':'PASS', 'checks':len(checks), 'package_files':len(package['files']),
                            're2_raw_files':raw_count, 'elapsed_s':time.perf_counter()-started,
                            'script_sha256':sha(__file__), 'research_started':False})
        print('PREPARATION_PASS', len(checks), flush=True)
    except BaseException as exc:
        dump('checks.json', checks)
        dump('status.json', {'status':'FAIL', 'error':str(exc), 'traceback':traceback.format_exc(),
                            'elapsed_s':time.perf_counter()-started})
        raise

if __name__ == '__main__':
    main()
