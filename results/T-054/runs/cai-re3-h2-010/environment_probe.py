"""Record effective test imports; no data files are read."""
from pathlib import Path
import sys
import json
import hashlib
import importlib
import importlib.metadata

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent
mode = sys.argv[1]
if mode == 'main':
    sys.path[:0] = [str(ROOT/'src'), str(ROOT/'results/T-054/scripts'), 'D:/RCA-ext/src/RCAEval',
                    'D:/RCA-ext/src/baro', 'D:/RCA-ext/work/T-014/CIRCA',
                    'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages']
else:
    sys.path.insert(0, str(ROOT/'src'))
    sys.path.extend(['D:/RCA-ext/src/RCAEval', 'D:/RCA-ext/src/baro'])
modules = {}
for name in ['numpy', 'pandas', 'pyarrow', 'sklearn', 'scipy', 'RCAEval'] + (['drain3'] if mode == 'main' else []):
    try:
        module = importlib.import_module(name)
    except ModuleNotFoundError:
        if name != 'pyarrow' or mode != 'py38':
            raise
        modules[name] = {'available': False, 'required_by_csv_method_process': False}
        continue
    p = Path(module.__file__)
    try:
        version = importlib.metadata.version({'sklearn': 'scikit-learn'}.get(name, name))
    except importlib.metadata.PackageNotFoundError:
        version = getattr(module, '__version__', None)
    modules[name] = {'path': str(p), 'version': version,
                     'init_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
value = {'scope': 'effective fixture environment, not cloud or held-out runtime certification',
         'python': sys.version, 'executable': sys.executable,
         'executable_sha256': hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
         'pythonpath': sys.path, 'modules': modules}
if mode == 'py38':
    from p3.re3 import validate_profile
    profile = json.loads((RUN/'synthetic-004/profile.json').read_text(encoding='utf-8'))
    validate_profile(profile)
    assert 'pyarrow' not in sys.modules
    value['RE3_profile_validation_without_pyarrow'] = 'PASS'
(RUN/('environment-'+mode+'.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'mode': mode, 'RCAEval': modules['RCAEval']['path']}))
