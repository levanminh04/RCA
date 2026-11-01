"""T-045: chạy các lượt pha 1 RE2-TT còn thiếu trước D17 bằng 4 tiến trình song song (Minh duyệt "chạy 4 tiến trình",
chat 31/10/2026). Không đọc nhãn; không đọc verdict. Bản v2 (bản v1 dùng cho đợt d17-001: `chay_song_song_v1.py`).

Khác v1 (vì đợt d17-001 chết sau 2 phút, LOG phiên 1):
- Không cửa sổ: chạy bằng `pythonw.exe`; tiến trình con `python.exe` với CREATE_NO_WINDOW. Không còn console nào để bị
  đóng. stdout/stderr của bộ điều phối ghi vào `<đợt>/dieu-phoi.log`.
- Dừng ngay khi có lỗi đầu tiên: đơn vị rc khác 0, kiểm đơn vị trượt, ghép lỗi, hay ngoại lệ trong bộ điều phối thì tạo
  `<đợt>/DUNG`; đơn vị đang chạy chạy nốt, đơn vị chưa chạy bị bỏ qua.
- Kiểm từng đơn vị ngay khi xong: có `pha1.json` và hash khớp; `tham-so.json` của ca đúng PYTHONHASHSEED, đúng số cấu
  hình, đúng cờ mốc giả/xáo/cách khớp/ngưỡng của lượt; số bản ghi bằng số cấu hình; mọi bản ghi status OK hoặc
  NO_EVIDENCE (ERROR, UNSUPPORTED là dấu hiệu lỗi trên dev, dừng để soi).
- Chặn RAM: chỉ khởi đơn vị mới khi RAM trống ≥ ngưỡng (mặc định 2,5 GiB).
- Thứ tự: pha A chạy ca đầu (`dev-03d4910932`, có bản tham chiếu) của mọi lượt để kiểm sớm; pha B phần còn lại của
  khối K (đơn vị dài); pha C phần còn lại. Ghi `pha_A_xong` khi pha A xong.
- Ghi nguồn: git HEAD, trạng thái `src/`, sha256 của script và `src/m1*`.
Mỗi đơn vị là (lượt, ca): `chay_pha1.py --luot <lượt> --ds RE2-TT <đối số> --mot-ca <mã>`; ca đã có `pha1.json` thì
bỏ qua (chạy tiếp đợt hỏng bằng đợt mới). Lượt đủ ca thì ghép (`--chi-ghep`, Đ-1).
Chạy: pythonw.exe -B results/T-045/scripts/chay_song_song.py --dot <đợt> [--so 4] [--ram-gib 2.5]
      [--thu <mã ca> --chi-luot <l1,l2>] [--loi-gia]  (hai cờ cuối chỉ để thử bộ điều phối)
"""
import argparse
import ctypes
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / 'results/T-045/runs'
PY = 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe'
ENV = {'PYTHONPATH': 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages;D:/RCA-flashticket/src', 'PYTHONIOENCODING': 'utf-8'}
SCRIPT = ROOT / 'results/T-045/scripts/chay_pha1.py'
CREATE_NO_WINDOW = 0x08000000

# (tên lượt, PYTHONHASHSEED, đối số, số cấu hình); bộ d17 chỉ RE2-TT
LUOT = [
    ('b2-t1-re2-seed0-001', '0', ['--cau-hinh', 'T1'], 1),
    ('b2-t1-re2-mocgia-001', '0', ['--cau-hinh', 'T1', '--moc-gia'], 1),
    ('b2b-k16-re2-001', '0', ['--cau-hinh', 'K'], 16),
    ('b2b-k16-re2-mocgia-001', '0', ['--cau-hinh', 'K', '--moc-gia'], 16),
    ('b2-t1-re2-seed1-001', '1', ['--cau-hinh', 'T1'], 1),
    ('b2-t1-re2-seed2-001', '2', ['--cau-hinh', 'T1'], 1),
    ('b2-t1-re2-xao0-001', '0', ['--cau-hinh', 'T1', '--xao', '0'], 1),
]
for _k in ('nguong', 'nguong_cung_lop'):
    LUOT += [(f'b2b-d3-{_k}-re2-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k], 1),
             (f'b2b-d3-{_k}-re2-mocgia-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k, '--moc-gia'], 1)]
for _k in ('hoan_toan', 'nguong', 'nguong_cung_lop'):
    LUOT += [(f'b2b-d3-{_k}-sim08-re2-001', '0', ['--cau-hinh', 'K-E3', '--khop', _k, '--sim-th', '0.8'], 1),
             (f'b2b-d3-{_k}-sim08-re2-mocgia-001', '0',
              ['--cau-hinh', 'K-E3', '--khop', _k, '--sim-th', '0.8', '--moc-gia'], 1)]
# bộ d45 (sau D17, Minh duyệt 01/11/2026): T4 (9 cấu hình), T4 mốc giả RE2-TT (Q-c), T4b, khối K Nezha-OB
LUOT_D45 = [
    ('b4-t4-re2-001', '0', ['--cau-hinh', 'T4'], 9, 'RE2-TT'),
    ('b4-t4-nezha-001', '0', ['--cau-hinh', 'T4'], 9, 'Nezha-OB'),
    ('b4-t4-re2-mocgia-001', '0', ['--cau-hinh', 'T4', '--moc-gia'], 9, 'RE2-TT'),
    ('b4-t4b-re2-001', '0', ['--cau-hinh', 'T4b'], 1, 'RE2-TT'),
    ('b4-t4b-nezha-001', '0', ['--cau-hinh', 'T4b'], 1, 'Nezha-OB'),
    ('b5-k16-nezha-001', '0', ['--cau-hinh', 'K'], 16, 'Nezha-OB'),
]
BO = {'d17': [(L, s, a, n, 'RE2-TT') for L, s, a, n in LUOT], 'd45': LUOT_D45}
TAT_CA_LUOT = {x[0]: x for b in BO.values() for x in b}
CA_DAU = {'RE2-TT': 'dev-03d4910932', 'Nezha-OB': 'dev-14701a3bbb'}


class _MEM(ctypes.Structure):
    _fields_ = [('dwLength', ctypes.c_ulong), ('dwMemoryLoad', ctypes.c_ulong), ('ullTotalPhys', ctypes.c_ulonglong),
                ('ullAvailPhys', ctypes.c_ulonglong), ('ullTotalPageFile', ctypes.c_ulonglong),
                ('ullAvailPageFile', ctypes.c_ulonglong), ('ullTotalVirtual', ctypes.c_ulonglong),
                ('ullAvailVirtual', ctypes.c_ulonglong), ('ullAvailExtendedVirtual', ctypes.c_ulonglong)]


def ram_trong_gib():
    m = _MEM()
    m.dwLength = ctypes.sizeof(_MEM)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2 ** 30


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ca_re2():
    a = json.loads((ROOT / 'results/T-022/allowlist-dev.json').read_text(encoding='utf-8'))
    return sorted(c['opaque_id'] for c in a['cases'])


def ca_cua(ds):
    tep = {'RE2-TT': 'results/T-022/allowlist-dev.json', 'Nezha-OB': 'results/T-026/allowlist-dev.json'}[ds]
    return sorted(c['opaque_id'] for c in json.loads((ROOT / tep).read_text(encoding='utf-8'))['cases'])


def kiem_don_vi(L, seed, arg, so_ch, o):
    """Kiểm một đơn vị vừa xong. Trả danh sách lỗi (rỗng là đạt) và tóm tắt."""
    d = RUNS / L / 'ca' / o
    loi = []
    if not (d / 'pha1.json').exists():
        return ['thiếu pha1.json'], {}
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    du = (d / meta['tep']).read_bytes()
    if hashlib.sha256(du).hexdigest() != meta['sha256']:
        loi.append('hash bản ghi lệch pha1.json')
    ts = json.loads((d / 'tham-so.json').read_text(encoding='utf-8'))
    if str(ts.get('PYTHONHASHSEED')) != seed:
        loi.append(f"PYTHONHASHSEED {ts.get('PYTHONHASHSEED')} khác {seed}")
    if len(ts.get('cau_hinh') or []) != so_ch:
        loi.append(f"số cấu hình {len(ts.get('cau_hinh') or [])} khác {so_ch}")
    mong = {'moc_gia': '--moc-gia' in arg, 'xao': (int(arg[arg.index('--xao') + 1]) if '--xao' in arg else None),
            'khop': (arg[arg.index('--khop') + 1] if '--khop' in arg else 'hoan_toan'),
            'sim_th': (float(arg[arg.index('--sim-th') + 1]) if '--sim-th' in arg else None)}
    for k, v in mong.items():
        if ts.get(k) != v:
            loi.append(f'tham số {k} = {ts.get(k)!r}, mong {v!r}')
    recs = [json.loads(x) for x in du.decode('utf-8').splitlines() if x]
    if len(recs) != so_ch:
        loi.append(f'{len(recs)} bản ghi, mong {so_ch}')
    st = {}
    for r in recs:
        st[r['status']] = st.get(r['status'], 0) + 1
        if r['status'] not in ('OK', 'NO_EVIDENCE'):
            loi.append(f"{r['config_id']}: status {r['status']}: {str(r.get('error'))[:200]}")
        if r.get('opaque_id') != o:
            loi.append(f"bản ghi mang mã ca {r.get('opaque_id')}")
    return loi, {'sha256': meta['sha256'], 'status': st}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dot', required=True)
    ap.add_argument('--so', type=int, default=4)
    ap.add_argument('--ram-gib', type=float, default=2.5)
    ap.add_argument('--bo', default='d17', choices=sorted(BO), help='bộ lượt')
    ap.add_argument('--thu', default=None, help='thử: chỉ ca RE2-TT này, tên lượt có tiền tố thu-<đợt>-')
    ap.add_argument('--thu-nz', default=None, help='thử: ca Nezha-OB dùng cho lượt Nezha-OB')
    ap.add_argument('--chi-luot', default=None, help='thử: chỉ các lượt này (tên gốc, cách nhau dấu phẩy)')
    ap.add_argument('--loi-gia', action='store_true', help='thử: đơn vị thứ hai của mỗi lượt nhận đối số sai')
    a = ap.parse_args()
    dot = RUNS / a.dot
    dot.mkdir(parents=True, exist_ok=False)
    (dot / 'log').mkdir()
    out = open(dot / 'dieu-phoi.log', 'a', encoding='utf-8', buffering=1)
    sys.stdout = sys.stderr = out
    khoa = threading.Lock()
    pf = open(dot / 'progress.jsonl', 'a', encoding='utf-8', buffering=1)

    def ghi(x):
        with khoa:
            pf.write(json.dumps(dict(x, t=time.strftime('%Y-%m-%dT%H:%M:%S%z')), ensure_ascii=False) + '\n')

    def dung(ly_do):
        if not (dot / 'DUNG').exists():
            (dot / 'DUNG').write_text(ly_do + '\n', encoding='utf-8')
        ghi({'su_kien': 'dung_vi_loi', 'ly_do': ly_do})

    try:
        luot = BO[a.bo]
        if a.chi_luot:
            chon = a.chi_luot.split(',')
            luot = [x for x in luot if x[0] in chon]
        thu = {'RE2-TT': a.thu, 'Nezha-OB': a.thu_nz}
        if a.thu or a.thu_nz:
            luot = [('thu-' + a.dot + '-' + L, s, arg, n, ds) for L, s, arg, n, ds in luot if thu[ds]]
        ca_ds = {}
        for ds in ('RE2-TT', 'Nezha-OB'):
            ca_ds[ds] = [thu[ds]] if thu[ds] else ca_cua(ds)
            if a.loi_gia and thu[ds]:  # thử: hai ca, đơn vị thứ hai của mỗi lượt lỗi
                ca_ds[ds] = [thu[ds]] + [c for c in ca_cua(ds) if c != thu[ds]][:1]
        chung_ds = {ds: ['--ds', ds] + (['--ca', ','.join(ca_ds[ds])] if thu[ds] else []) for ds in ca_ds}
        git = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(ROOT), capture_output=True, text=True).stdout.strip()
        git_src = subprocess.run(['git', 'status', '--short', 'src'], cwd=str(ROOT), capture_output=True,
                                 text=True).stdout.strip()
        nguon = {'git_HEAD': git, 'git_status_src': git_src, 'pid': os.getpid(), 'argv': sys.argv[1:],
                 'sha256': {str(p.relative_to(ROOT)).replace('\\', '/'): sha(p) for p in
                            [SCRIPT, Path(__file__)] + sorted((ROOT / 'src/m1').glob('*.py'))
                            + sorted((ROOT / 'src/m1_danh_gia').glob('*.py'))}}
        (dot / 'nguon.json').write_text(json.dumps(nguon, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        if git_src:
            raise SystemExit(f'src có thay đổi chưa commit: {git_src}')
        # thứ tự: A = ca đầu của mọi lượt; B = phần còn lại của khối K; C = phần còn lại
        dau = {ds: (CA_DAU[ds] if CA_DAU[ds] in ca_ds[ds] else ca_ds[ds][0]) for ds in ca_ds}
        A = [(L, s, arg, n, ds, o) for L, s, arg, n, ds in luot for o in ca_ds[ds] if o == dau[ds]]
        B = [(L, s, arg, n, ds, o) for L, s, arg, n, ds in luot for o in ca_ds[ds] if o != dau[ds] and n > 1]
        C = [(L, s, arg, n, ds, o) for L, s, arg, n, ds in luot for o in ca_ds[ds] if o != dau[ds] and n == 1]
        viec = A + B + C
        con = {L: len(ca_ds[ds]) for L, _, _, _, ds in luot}
        con_A = [len(A)]
        loi_luot = {L: [] for L, *_ in luot}
        dem_thu = {L: 0 for L, *_ in luot}

        def env(seed):
            e = dict(os.environ)
            e.update(ENV)
            e['PYTHONHASHSEED'] = seed
            return e

        def chay(v):
            L, s, arg, n, ds, o = v
            chung = chung_ds[ds]
            try:
                if (dot / 'DUNG').exists():
                    ghi({'su_kien': 'bo_qua_DUNG', 'luot': L, 'ca': o})
                    return
                da_cho = False
                while ram_trong_gib() < a.ram_gib:
                    if not da_cho:
                        ghi({'su_kien': 'cho_ram', 'luot': L, 'ca': o, 'ram_trong_gib': round(ram_trong_gib(), 2)})
                        da_cho = True
                    time.sleep(10)
                    if (dot / 'DUNG').exists():
                        ghi({'su_kien': 'bo_qua_DUNG', 'luot': L, 'ca': o})
                        return
                arg_chay = list(arg)
                with khoa:
                    dem_thu[L] += 1
                    sai = a.loi_gia and dem_thu[L] == 2
                if sai:
                    arg_chay += ['--co-khong-ton-tai']  # thử: đối số lạ, tiến trình con phải thoát rc khác 0
                t0 = time.time()
                with open(dot / 'log' / f'{L}__{o}.txt', 'w', encoding='utf-8') as f:
                    rc = subprocess.run([PY, '-B', str(SCRIPT), '--luot', L, *chung, *arg_chay, '--mot-ca', o],
                                        env=env(s), cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT,
                                        creationflags=CREATE_NO_WINDOW).returncode
                loi, tom = (kiem_don_vi(L, s, arg, n, o) if rc == 0 else ([f'rc {rc}'], {}))
                ghi({'su_kien': 'don_vi', 'luot': L, 'ca': o, 'rc': rc, 'giay': round(time.time() - t0, 1),
                     'kiem': 'dat' if not loi else loi, 'ram_trong_gib': round(ram_trong_gib(), 2), **tom})
                if loi:
                    dung(f'{L} {o}: {loi[:3]}')
                with khoa:
                    con[L] -= 1
                    if loi:
                        loi_luot[L].append(o)
                    xong = con[L] == 0
                    if v in A:
                        con_A[0] -= 1
                        if con_A[0] == 0:
                            pf.write(json.dumps({'su_kien': 'pha_A_xong', 't': time.strftime('%Y-%m-%dT%H:%M:%S%z')},
                                                ensure_ascii=False) + '\n')
                if xong and not loi_luot[L]:
                    with open(dot / 'log' / f'{L}__ghep.txt', 'w', encoding='utf-8') as f:
                        rc = subprocess.run([PY, '-B', str(SCRIPT), '--luot', L, *chung, *arg, '--chi-ghep'],
                                            env=env(s), cwd=str(ROOT), stdout=f, stderr=subprocess.STDOUT,
                                            creationflags=CREATE_NO_WINDOW).returncode
                    ghi({'su_kien': 'ghep', 'luot': L, 'rc': rc})
                    if rc:
                        dung(f'ghép {L} rc {rc}')
            except Exception:
                ghi({'su_kien': 'ngoai_le', 'luot': L, 'ca': o, 'loi': traceback.format_exc()[-1500:]})
                dung(f'ngoại lệ ở {L} {o}')

        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        ghi({'su_kien': 'bat_dau', 'bo': a.bo, 'so_tien_trinh': a.so, 'so_don_vi': len(viec),
             'pha': [len(A), len(B), len(C)], 'luot': [L for L, *_ in luot], 'pid': os.getpid(),
             'ram_trong_gib': round(ram_trong_gib(), 2)})
        with ThreadPoolExecutor(max_workers=a.so) as ex:
            list(ex.map(chay, viec))
        ghi({'su_kien': 'xong', 'loi': {L: v for L, v in loi_luot.items() if v}, 'DUNG': (dot / 'DUNG').exists()})
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    except BaseException:
        ghi({'su_kien': 'ngoai_le_dieu_phoi', 'loi': traceback.format_exc()[-2000:]})
        dung('ngoại lệ trong bộ điều phối')
        raise


if __name__ == '__main__':
    main()
