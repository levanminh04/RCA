"""T-025: tiện ích chung (thư mục lượt, tiến độ, RAM, hash mã, đường dẫn hai máy).

Vai runner chế độ (b) chỉ đọc allowlist; không đọc `nhan-dev.json` (SPEC T-025 bước 1–3). Chỉ evaluator
(`danh_gia_b.py`) đọc nhãn, sau khi danh sách bản ghi đã chốt. Báo theo mã mờ.

Hai máy: laptop (Windows) và EC2 (`~/rca/T-025/`). Mã chạy từ ROOT (repo hoặc bản chép trên EC2); dữ liệu đọc
từ DATA_ROOT (biến môi trường T025_DATA_ROOT; mặc định ROOT). Trên EC2 DATA_ROOT = ~/rca/T-031/repo (chỉ đọc).
"""
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results' / 'T-025'
DATA_ROOT = Path(os.environ.get('T025_DATA_ROOT', str(ROOT)))
sys.path.insert(0, str(ROOT / 'src'))
sys.dont_write_bytecode = True

from p3 import selector  # noqa: E402

ALLOWLIST = ROOT / 'results/T-022/allowlist-dev.json'
TIMEOUT_S = {'bocpd': 21600}  # SPEC T-025: BOCPD 6 giờ mỗi ca; mọi lượt khác 3.600 s
TIMEOUT_MAC_DINH = 3600
EC2 = sys.platform.startswith('linux')


def timeout_cho(method):
    return TIMEOUT_S.get(method, TIMEOUT_MAC_DINH)


def bay_gio():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def hash_p3():
    """Như results/T-031/scripts/chung.py: sha256 của nối các tệp .py trong src/p3 theo đường dẫn POSIX."""
    files = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'src' / 'p3').rglob('*.py'))
    h = hashlib.sha256()
    per = {}
    for f in files:
        b = (ROOT / f).read_bytes()
        h.update(b)
        per[f] = hashlib.sha256(b).hexdigest()
    return {'tong': h.hexdigest(), 'tep': per}


def ram_trong_gb():
    import psutil
    return round(psutil.virtual_memory().available / 2**30, 2)


def nap_allowlist():
    return selector.nap_allowlist(ALLOWLIST)


def cau_hinh_runner():
    """Trên EC2: thay đường dẫn môi trường kiểu Windows của runner (như T-031 chay_ec2.py), không sửa src/p3."""
    from p3 import runner
    if EC2:
        B = Path.home() / 'rca' / 'T-025'
        runner.ROOT = ROOT
        # vai 'drain' dùng chung env main (có drain3 0.9.11), như T-031 chay_ec2.py
        runner.ENVS = {'main': str(B / 'envs/main/bin/python'), 'drain': str(B / 'envs/main/bin/python'),
                       'py38': str(B / 'envs/py38/bin/python')}
        # CIRCA: adapter chèn đường dẫn Windows mặc định (không tồn tại trên Linux) rồi import `circa`;
        # `circa` lấy từ PYTHONPATH dưới đây (cùng mã 0215e18).
        runner.PYTHONPATH = {'main': [str(B / 'src/RCAEval'), str(B / 'src/baro'), str(ROOT / 'src'), str(B / 'src/CIRCA')],
                             'drain': [str(ROOT / 'src')],
                             'py38': [str(B / 'src/RCAEval'), str(ROOT / 'src')]}
    return runner


class Luot:
    """Thư mục một lần chạy script: runs/<ten>-<nnn>/ với cau-hinh.json, tien-do.txt, ket-thuc.json."""

    def __init__(self, ten, cau_hinh=None, trang_thai=None):
        n = 1
        while (OUT / 'runs' / f'{ten}-{n:03d}').exists():
            n += 1
        self.dir = OUT / 'runs' / f'{ten}-{n:03d}'
        self.dir.mkdir(parents=True)
        self.t0 = time.perf_counter()
        self.trang_thai = Path(trang_thai) if trang_thai else None
        self.ch = {'ten': ten, 'bat_dau_utc': bay_gio(), 'script': sys.argv[0], 'argv': sys.argv[1:],
                   'script_sha256': sha256_file(sys.argv[0]), 'chung_sha256': sha256_file(__file__),
                   'src_p3': hash_p3(), 'python': sys.version, 'may': platform.platform(),
                   'hostname': platform.node(),
                   'data_root': str(DATA_ROOT), 'ram_trong_gb_luc_dau': ram_trong_gb()}
        self.ch.update(cau_hinh or {})
        (self.dir / 'cau-hinh.json').write_text(json.dumps(self.ch, ensure_ascii=False, indent=1), encoding='utf-8')
        self.tien_do = open(self.dir / 'tien-do.txt', 'a', encoding='utf-8')
        self.ghi(f'bắt đầu {ten}; RAM trống {self.ch["ram_trong_gb_luc_dau"]} GB')

    def ghi(self, msg):
        line = f'{bay_gio()} +{time.perf_counter() - self.t0:9.1f}s {msg}'
        print(line, flush=True)
        self.tien_do.write(line + '\n')
        self.tien_do.flush()
        if self.trang_thai:
            with open(self.trang_thai, 'a', encoding='utf-8') as f:
                f.write(f'{self.dir.name} {line}\n')

    def xong(self, tom_tat):
        doc = {'ket_thuc_utc': bay_gio(), 'tong_s': round(time.perf_counter() - self.t0, 1),
               'ram_trong_gb_luc_cuoi': ram_trong_gb(), 'tom_tat': tom_tat}
        ghi_json(self.dir / 'ket-thuc.json', doc)
        self.ghi(f'xong; {doc["tong_s"]} s')
        self.tien_do.close()
        return doc


def ghi_json(path, doc):
    Path(path).write_text(json.dumps(doc, ensure_ascii=False, indent=1, default=_mac_dinh), encoding='utf-8')


def _mac_dinh(o):
    import numpy as np
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    raise TypeError(type(o))


def don_bang_torai(run_dir):
    """Như T-031: ghi manifest rồi xóa bảng CSV TORAI (telemetry đã cắt) trong thư mục lượt."""
    bang = Path(run_dir) / 'bang'
    if not bang.is_dir():
        return None
    man = {p.name: {'bytes': p.stat().st_size, 'sha256': sha256_file(p)} for p in sorted(bang.glob('*.csv'))}
    (Path(run_dir) / 'bang-manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    for p in bang.glob('*.csv'):
        p.unlink()
    bang.rmdir()
    return man
