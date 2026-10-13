"""T-033 kiểm nguồn/máy/lưới; mọi output chỉ trong T033_HOME."""
import contextlib
import hashlib
import io
import json
import os
import platform
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import scipy
import psutil

H = Path(os.environ['T033_HOME']).resolve()
RUN = H / 'runs' / os.environ['T033_PREFLIGHT']
RUN.mkdir(parents=True, exist_ok=False)
SRC = json.loads((H / 'inputs/source.json').read_text())
B = Path.home() / 'rca/T-025'

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def save(name, x):
    (RUN / name).write_text(json.dumps(x, indent=2, ensure_ascii=False, allow_nan=False))

for name, expect in SRC['native_hash'].items():
    assert sha(B / 'src/baro/baro' / name) == expect, 'Native source hash: ' + name
assert sha(B / 'repo/src/p3/adapters/phat_hien.py') == SRC['adapter_sha256']
from p3.adapters.phat_hien import cot_bocpd, tien_xu_ly_bocpd
env = {'python': sys.version, 'os': platform.platform(), 'arch': platform.machine(),
       'numpy': np.__version__, 'pandas': pd.__version__, 'scipy': scipy.__version__,
       'psutil': psutil.__version__, 'ram_available_bytes': psutil.virtual_memory().available,
       'disk_free_bytes': shutil.disk_usage(H).free, 'cpu_count': os.cpu_count(),
       'environment': {k: os.environ.get(k) for k in ['PYTHONPATH','PYTHONDONTWRITEBYTECODE','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','PYTHONHASHSEED']},
       'source_json_sha256': sha(H / 'inputs/source.json'), 'native_hash': SRC['native_hash'],
       'adapter_sha256': SRC['adapter_sha256']}
buf = io.StringIO()
with contextlib.redirect_stdout(buf): np.show_config()
env['numpy_build'] = buf.getvalue()
save('environment.json', env)
assert (np.__version__,pd.__version__,scipy.__version__) == ('1.26.4','2.2.3','1.14.1')
rows, missing, hash_bad = [], [], []
for case in SRC['cases']:
    paths = {}
    for name, m in case['files'].items():
        p = B / 'repo' / m['path']
        assert 'locked' not in p.parts
        if not p.is_file(): missing.append({'opaque_id':case['opaque_id'],'file':name,'meta':m}); continue
        if p.stat().st_size != m['bytes'] or sha(p) != m['sha256']:
            hash_bad.append(str(p)); continue
        paths[name] = str(p)
    if 'metrics.parquet' not in paths: continue
    df = pd.read_parquet(paths['metrics.parquet'])
    times = df['time'].to_numpy()
    assert len(times) == 1441 and np.isfinite(times).all()
    assert np.array_equal(times, times.astype(np.int64)) and np.all(np.diff(times)==1)
    matches = np.flatnonzero(times == case['proxy'])
    assert len(matches) == 1 and int(matches[0]) == 720
    cols = cot_bocpd(df.columns)
    full = tien_xu_ly_bocpd(df[cols])
    prefix = tien_xu_ly_bocpd(df[cols].iloc[:720].copy())
    assert set(prefix.columns) <= set(full.columns)
    assert full.shape[1] == case['expected']['bocpd']['input_shape']['cot_sau_tien_xu_ly']
    for detector, meta in case['flags'].items():
        p = H / 'inputs' / meta['path']
        assert sha(p) == meta['sha256']
        with np.load(p, allow_pickle=False) as z:
            assert np.array_equal(times, z['times'])
            assert np.array_equal(np.array(case['expected'][detector]['detector_columns']),z['columns'])
            assert z['Z'].shape == (len(times),len(z['columns']))
    rows.append({'opaque_id':case['opaque_id'], 'files':paths, 'time_start':int(times[0]),
                 'time_end':int(times[-1]), 'T':len(times), 'i_proxy':720,
                 't_proxy':int(times[720]), 'raw_columns':len(cols), 'full_d':full.shape[1],
                 'prefix_d':prefix.shape[1], 'mask_subset':True,
                 'full_status_source':case['expected']['bocpd']['status'],
                 'full_finite_input':bool(np.isfinite(full.to_numpy()).all()),
                 'prefix_finite_input':bool(np.isfinite(prefix.to_numpy()).all())})
save('inventory.json', {'status':'FAIL' if hash_bad else ('MISSING' if missing else 'PASS'),
      'cases':rows,'missing':missing,'hash_bad':hash_bad,'existing_files':sum(len(r['files']) for r in rows)})
assert not hash_bad, hash_bad
assert not missing, 'Dữ liệu thiếu: checkpoint, đo route trước chuyển'
assert len(rows) == 30
assert env['disk_free_bytes'] > SRC['budget_bytes']
save('verification.json', {'status':'PASS','cases':30,'files':sum(len(r['files']) for r in rows),
                          'no_telemetry_transfer_needed':True,'source_code_hashes_match':True,
                          'grid_proxy_flags_columns_match':True})
print(json.dumps({'status':'PASS','files':sum(len(r['files']) for r in rows),'disk_free':env['disk_free_bytes'],'ram_available':env['ram_available_bytes']}))
