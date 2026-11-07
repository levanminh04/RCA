"""Create task-local runtimes, keeping checkpoint012 untouched."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path('/home/ubuntu/rca-p7/T-054/checkpoint013')
OLD = ROOT.with_name('checkpoint012')
ROOT.mkdir(parents=True, exist_ok=False)
for name in ('envs', 'python', 'cache', 'tmp'):
    (ROOT / name).mkdir()
ENV = dict(os.environ, UV_CACHE_DIR=str(ROOT / 'cache'), TMPDIR=str(ROOT / 'tmp'),
           UV_PYTHON_INSTALL_DIR=str(ROOT / 'python'), PYTHONDONTWRITEBYTECODE='1',
           PYTHONHASHSEED='0', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
UV = OLD / 'tools/uv'
logs = []
started = time.monotonic()


def run(args, timeout=600):
    tick = time.monotonic()
    proc = subprocess.run([str(a) for a in args], env=ENV, capture_output=True, text=True, timeout=timeout)
    logs.append(dict(args=list(map(str, args)), exit=proc.returncode, stdout=proc.stdout,
                     stderr=proc.stderr, seconds=time.monotonic() - tick))
    (ROOT / 'bootstrap-progress.json').write_text(json.dumps(logs, indent=2))
    print(json.dumps(dict(stage=str(args[1]), exit=proc.returncode, seconds=logs[-1]['seconds'])), flush=True)
    if proc.returncode:
        raise RuntimeError(proc.stderr[-3000:])
    return proc.stdout


try:
    frozen = run([UV, 'pip', 'freeze', '--python', OLD / 'envs/main/bin/python'])
    requirements = [r for r in frozen.splitlines() if r and not r.startswith('#')]
    requirements += ['requests==2.32.3', 'tqdm==4.65.0']
    run([UV, 'venv', '--python', OLD / 'envs/main/bin/python', ROOT / 'envs/main'])
    run([UV, 'pip', 'install', '--no-cache', '--python', ROOT / 'envs/main/bin/python', *requirements])
    run([UV, 'python', 'install', '3.8.20', '--no-cache'])
    run([UV, 'venv', '--python', '3.8.20', '--no-python-downloads', ROOT / 'envs/py38'])
    requirements38 = ('numpy==1.23.5 pandas==2.0.1 scipy==1.10.1 scikit-learn==1.2.2 '
                      'joblib==1.2.0 threadpoolctl==3.1.0 networkx==2.5 causal-learn==0.1.2.3 '
                      'matplotlib==3.7.5 psutil==5.9.5 requests==2.30.0 tqdm==4.65.0 '
                      'python-dateutil==2.8.2 pytz==2023.3 tzdata==2023.3 six==1.16.0').split()
    run([UV, 'pip', 'install', '--no-cache', '--python', ROOT / 'envs/py38/bin/python', *requirements38])
    for name in ('main', 'py38'):
        run([UV, 'pip', 'check', '--python', ROOT / f'envs/{name}/bin/python'])
        run([UV, 'pip', 'freeze', '--python', ROOT / f'envs/{name}/bin/python'])
    summary = dict(PASS=True)
except BaseException as exc:
    summary = dict(PASS=False, error=repr(exc))
summary.update(logs=logs, elapsed_s=time.monotonic() - started, disk_free=shutil.disk_usage(ROOT).free)
(ROOT / 'bootstrap.json').write_text(json.dumps(summary, indent=2))
print(json.dumps(summary), flush=True)
if not summary['PASS']:
    raise SystemExit(1)
