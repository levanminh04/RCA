"""T-045: chạy các lượt pha 1 RE2-TT còn thiếu trước D17 bằng 4 tiến trình song song (Minh duyệt "chạy 4 tiến trình",
chat 31/10/2026). Không đọc nhãn; không đọc verdict.

Mỗi đơn vị việc là (lượt, ca): một tiến trình `chay_pha1.py --luot <lượt> ... --mot-ca <mã>` với PYTHONHASHSEED của
lượt. Lượt nào xong đủ 30 ca thì ghép ngay (`--chi-ghep`, Đ-1). Đơn vị lỗi được ghi lại, không chạy lại tự động.
Tạo tệp `<đợt>/DUNG` để không nhận đơn vị mới. Tiến trình giữ máy không ngủ khi đang chạy (SetThreadExecutionState).

Danh sách lượt (D17 cần): T1 (seed 0, 1, 2; xáo; mốc giả); 16 cấu hình khối K (cửa sổ thật, mốc giả; dùng cho D1 phần
E1 bật/E2, D3 cách (a), D5); D3 cách (b), (c) (thật, mốc giả); D3 ngưỡng 0,8 ba cách (thật, mốc giả).
Chạy: $PY -B results/T-045/scripts/chay_song_song.py --dot d17-001 [--so 4] [--thu <mã ca>]
"""
import argparse
import ctypes
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / 'results/T-045/runs'
PY = 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe'
ENV = {'PYTHONPATH': 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages;D:/RCA-flashticket/src', 'PYTHONIOENCODING': 'utf-8'}
SCRIPT = str(ROOT / 'results/T-045/scripts/chay_pha1.py')

# (tên lượt, PYTHONHASHSEED, đối số)
LUOT = [
    ('b2-t1-re2-seed0-001', '0', ['--cau-hinh', 'T1']),
    ('b2-t1-re2-mocgia-001', '0', ['--cau-hinh', 'T1', '--moc-gia']),
    ('b2b-k16-re2-001', '0', ['--cau-hinh', 'K']),
    ('b2b-k16-re2-mocgia-001', '0', ['--cau-hinh', 'K', '--moc-gia']),
    ('b2-t1-re2-seed1-001', '1', ['--cau-hinh', 'T1']),
    ('b2-t1-re2-seed2-001', '2', ['--cau-hinh', 'T1']),
    ('b2-t1-re2-xao0-001', '0', ['--cau-hinh', 'T1', '--xao', '0']),
]
for _k in ('nguong', 'nguong_cung_lop'):
    LUOT += [(f'b2b-d3-{_k}-re2-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k]),
             (f'b2b-d3-{_k}-re2-mocgia-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k, '--moc-gia'])]
for _k in ('hoan_toan', 'nguong', 'nguong_cung_lop'):
    LUOT += [(f'b2b-d3-{_k}-sim08-re2-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k, '--sim-th', '0.8']),
             (f'b2b-d3-{_k}-sim08-re2-mocgia-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k, '--sim-th', '0.8',
                                                         '--moc-gia'])]


def ca_re2():
    a = json.loads((ROOT / 'results/T-022/allowlist-dev.json').read_text(encoding='utf-8'))
    return sorted(c['opaque_id'] for c in a['cases'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dot', required=True)
    ap.add_argument('--so', type=int, default=4)
    ap.add_argument('--thu', default=None, help='chế độ thử: một ca, một lượt T1, tên lượt có tiền tố thu-')
    a = ap.parse_args()
    dot = RUNS / a.dot
    dot.mkdir(parents=True, exist_ok=False)
    (dot / 'log').mkdir()
    luot = LUOT if not a.thu else [('thu-' + a.dot + '-t1', '0', ['--cau-hinh', 'T1'])]
    ds_ca = ca_re2() if not a.thu else [a.thu]
    chung = ['--ds', 'RE2-TT'] + (['--ca', a.thu] if a.thu else [])
    viec = [(L, s, arg, o) for L, s, arg in luot for o in ds_ca]
    con = {L: len(ds_ca) for L, _, _ in luot}
    loi = {L: [] for L, _, _ in luot}
    khoa = threading.Lock()
    pf = open(dot / 'progress.jsonl', 'a', encoding='utf-8')

    def ghi(x):
        with khoa:
            pf.write(json.dumps(dict(x, t=time.strftime('%Y-%m-%dT%H:%M:%S%z')), ensure_ascii=False) + '\n')
            pf.flush()

    def env(seed):
        e = dict(os.environ)
        e.update(ENV)
        e['PYTHONHASHSEED'] = seed
        return e

    def chay(v):
        L, s, arg, o = v
        if (dot / 'DUNG').exists():
            ghi({'su_kien': 'bo_qua_DUNG', 'luot': L, 'ca': o})
            return
        t0 = time.time()
        with open(dot / 'log' / f'{L}__{o}.txt', 'w', encoding='utf-8') as f:
            rc = subprocess.run([PY, '-B', SCRIPT, '--luot', L, *chung, *arg, '--mot-ca', o], env=env(s), cwd=str(ROOT),
                                stdout=f, stderr=subprocess.STDOUT).returncode
        ghi({'su_kien': 'don_vi', 'luot': L, 'ca': o, 'rc': rc, 'giay': round(time.time() - t0, 1)})
        with khoa:
            con[L] -= 1
            if rc:
                loi[L].append(o)
            xong = con[L] == 0
        if xong:
            if loi[L]:
                ghi({'su_kien': 'khong_ghep', 'luot': L, 'ca_loi': loi[L]})
                return
            with open(dot / 'log' / f'{L}__ghep.txt', 'w', encoding='utf-8') as f:
                rc = subprocess.run([PY, '-B', SCRIPT, '--luot', L, *chung, *arg, '--chi-ghep'], env=env(s),
                                    cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT).returncode
            ghi({'su_kien': 'ghep', 'luot': L, 'rc': rc})

    ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    except Exception:  # không phải Windows
        pass
    ghi({'su_kien': 'bat_dau', 'so_tien_trinh': a.so, 'so_don_vi': len(viec), 'luot': [L for L, _, _ in luot],
         'pid': os.getpid()})
    with ThreadPoolExecutor(max_workers=a.so) as ex:
        list(ex.map(chay, viec))
    ghi({'su_kien': 'xong', 'loi': {L: v for L, v in loi.items() if v}})
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    except Exception:
        pass


if __name__ == '__main__':
    main()
