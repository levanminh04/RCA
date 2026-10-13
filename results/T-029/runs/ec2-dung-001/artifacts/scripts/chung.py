"""Bản cấu hình T-029 cho bản chép rca_b.py; chỉ ghi T-029 trên EC2."""
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ['T029_HOME']).resolve()
OUT = ROOT
DATA_ROOT = Path.home() / 'rca/T-031/repo'
B = Path.home() / 'rca/T-025'
READ_SRC = B / 'repo/src'
ALLOWLIST = ROOT / 'inputs/allowlist-dev.json'
TIMEOUT_MAC_DINH = 3600
EC2 = True
sys.dont_write_bytecode = True
from p3 import selector

def bay_gio():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def hash_p3():
    h = hashlib.sha256()
    per = {}
    for p in sorted((READ_SRC / 'p3').rglob('*.py')):
        h.update(p.read_bytes())
        per['src/' + p.relative_to(READ_SRC).as_posix()] = sha256_file(p)
    return {'tong': h.hexdigest(), 'tep': per}

def ram_trong_gb():
    import psutil
    return round(psutil.virtual_memory().available / 2**30, 2)

def nap_allowlist():
    return selector.nap_allowlist(ALLOWLIST)

def cau_hinh_runner():
    from p3 import runner
    runner.ROOT = ROOT
    runner.ENVS = {'main': str(B / 'envs/main/bin/python'), 'drain': str(B / 'envs/main/bin/python'), 'py38': str(B / 'envs/py38/bin/python')}
    runner.PYTHONPATH = {'main': [str(B / 'src/RCAEval'), str(B / 'src/baro'), str(READ_SRC), str(B / 'src/CIRCA')],
                         'drain': [str(READ_SRC)], 'py38': [str(B / 'src/RCAEval'), str(READ_SRC)]}
    return runner

def _default(o):
    import numpy as np
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.integer, np.bool_)): return o.item()
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, (set, tuple)): return list(o)
    raise TypeError(type(o))

def ghi_json(path, doc):
    Path(path).write_text(json.dumps(doc, ensure_ascii=False, indent=2, default=_default) + '\n', encoding='utf-8')

def progress(s):
    msg = f'{bay_gio()} {s}'
    print(msg, flush=True)
    with (ROOT / 'trang-thai.txt').open('a', encoding='utf-8') as f:
        f.write(msg + '\n')

class Luot:
    def __init__(self, ten, cau_hinh=None, trang_thai=None):
        n = 1
        while (OUT / 'runs' / f'{ten}-{n:03d}').exists(): n += 1
        self.dir = OUT / 'runs' / f'{ten}-{n:03d}'
        self.dir.mkdir(parents=True)
        self.t0 = time.perf_counter()
        self.ch = {'ten': ten, 'bat_dau_utc': bay_gio(), 'script': sys.argv[0], 'argv': sys.argv[1:],
                   'src_p3': hash_p3(), 'python': sys.version, 'hostname': platform.node(),
                   'data_root': str(DATA_ROOT), 'ram_trong_gb_luc_dau': ram_trong_gb()}
        self.ch.update(cau_hinh or {})
        ghi_json(self.dir / 'cau-hinh.json', self.ch)
        self.ghi(f'BAT_DAU {ten}')
    def ghi(self, s):
        msg = f'{self.dir.name} +{time.perf_counter()-self.t0:.1f}s {s}'
        with (self.dir / 'tien-do.txt').open('a', encoding='utf-8') as f:
            f.write(bay_gio() + ' ' + msg + '\n')
        progress(msg)
    def xong(self, tom_tat):
        ghi_json(self.dir / 'ket-thuc.json', {'ket_thuc_utc': bay_gio(), 'tong_s': time.perf_counter()-self.t0, 'tom_tat': tom_tat})
        self.ghi('XONG')

def don_bang_torai(run_dir):
    bang = Path(run_dir) / 'bang'
    if not bang.is_dir(): return None
    assert ROOT in bang.resolve().parents
    manifest = {p.name: {'bytes': p.stat().st_size, 'sha256': sha256_file(p)} for p in sorted(bang.glob('*.csv'))}
    ghi_json(Path(run_dir) / 'bang-manifest.json', manifest)
    progress('MANIFEST_TRUOC_XOA_BANG ' + str(bang))
    for p in bang.glob('*.csv'): p.unlink()
    bang.rmdir()
    return manifest
