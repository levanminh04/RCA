"""T-031: tiện ích chung cho các script chạy (thư mục lượt, tiến độ, RAM, hash mã).

Chỉ runner/script đọc allowlist và mốc tiêm (chế độ a). Không đọc nhãn root hay loại lỗi.
Báo theo mã mờ. Chạy bằng T-014-main với PYTHONDONTWRITEBYTECODE=1.
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
OUT = ROOT / 'results' / 'T-031'
sys.path.insert(0, str(ROOT / 'src'))
sys.dont_write_bytecode = True

from p3 import nhan, selector  # noqa: E402

ALLOWLIST = ROOT / 'results/T-022/allowlist-dev.json'
NHAN = ROOT / 'results/T-022/nhan-dev.json'
TIMEOUT_S = 3600  # SPEC T-031: giới hạn mỗi lượt, mọi phương pháp


def bay_gio():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def hash_p3():
    """sha256 của nối các tệp .py trong src/p3 theo thứ tự đường dẫn POSIX; kèm hash từng tệp."""
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


def nap():
    """(allowlist, mốc tiêm). Mốc chỉ dùng để cắt cửa sổ chế độ (a), vai runner."""
    return selector.nap_allowlist(ALLOWLIST), nhan.nap_moc(NHAN)


class Luot:
    """Thư mục một lần chạy script: runs/<ten>-<nnn>/ với cau-hinh.json, tien-do.txt, ket-thuc.json."""

    def __init__(self, ten, cau_hinh=None):
        n = 1
        while (OUT / 'runs' / f'{ten}-{n:03d}').exists():
            n += 1
        self.dir = OUT / 'runs' / f'{ten}-{n:03d}'
        self.dir.mkdir(parents=True)
        self.t0 = time.perf_counter()
        self.ch = {'ten': ten, 'bat_dau_utc': bay_gio(), 'script': sys.argv[0], 'argv': sys.argv[1:],
                   'script_sha256': sha256_file(sys.argv[0]), 'chung_sha256': sha256_file(__file__),
                   'src_p3': hash_p3(), 'python': sys.version, 'may': platform.platform(),
                   'ram_trong_gb_luc_dau': ram_trong_gb(), 'timeout_moi_luot_s': TIMEOUT_S}
        self.ch.update(cau_hinh or {})
        (self.dir / 'cau-hinh.json').write_text(json.dumps(self.ch, ensure_ascii=False, indent=1), encoding='utf-8')
        self.tien_do = open(self.dir / 'tien-do.txt', 'a', encoding='utf-8')
        self.ghi(f'bắt đầu {ten}; RAM trống {self.ch["ram_trong_gb_luc_dau"]} GB')

    def ghi(self, msg):
        line = f'{bay_gio()} +{time.perf_counter() - self.t0:8.1f}s {msg}'
        print(line, flush=True)
        self.tien_do.write(line + '\n')
        self.tien_do.flush()

    def xong(self, tom_tat):
        doc = {'ket_thuc_utc': bay_gio(), 'tong_s': round(time.perf_counter() - self.t0, 1),
               'ram_trong_gb_luc_cuoi': ram_trong_gb(), 'tom_tat': tom_tat}
        (self.dir / 'ket-thuc.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1, default=str),
                                                encoding='utf-8')
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
    """Ghi manifest rồi xóa bảng CSV TORAI (telemetry đã cắt) trong thư mục lượt. Trả manifest."""
    bang = Path(run_dir) / 'bang'
    if not bang.is_dir():
        return None
    man = {p.name: {'bytes': p.stat().st_size, 'sha256': sha256_file(p)} for p in sorted(bang.glob('*.csv'))}
    (Path(run_dir) / 'bang-manifest.json').write_text(json.dumps(man, indent=1), encoding='utf-8')
    for p in bang.glob('*.csv'):
        p.unlink()
    bang.rmdir()
    return man


def chon_pilot(gia_tri):
    """gia_tri: {opaque_id: bộ yếu tố (tuple)}. Trả {'nho_nhat','trung_vi_duoi','lon_nhat'} -> mã mờ.

    Sắp theo bộ yếu tố (thứ tự từ điển); trung vị dưới = giá trị ở vị trí (n-1)//2 (đếm từ 0);
    trong mỗi giá trị, hòa thì lấy mã mờ nhỏ hơn (luật khai trước, LOG T-031 10:20)."""
    ds = sorted(gia_tri.items(), key=lambda kv: (tuple(kv[1]), kv[0]))
    vals = [tuple(v) for _, v in ds]

    def nho_nhat_co(v):
        return min(k for k, x in gia_tri.items() if tuple(x) == v)
    return {'nho_nhat': nho_nhat_co(vals[0]), 'trung_vi_duoi': nho_nhat_co(vals[(len(vals) - 1) // 2]),
            'lon_nhat': nho_nhat_co(vals[-1])}
