"""T-046 bước 3 (và phần cửa sổ thật cho bước 5): bảng phép kiểm theo G0, G1, G3 cho từng ca, không đọc nhãn.

Mỗi ca, các cửa sổ (A1, A5):
- 'aa' với R0 và K-đủ (A/A, chọn và chẩn đoán C1);
- 'that' với R0 ((c1), A2: tỷ lệ rơi về G0 ở cỡ thật); bản ghi phải trùng từng byte bản ghi T1-R0 của T-045.
C-e không chạy ở đây (chỉ sau khóa, bước 6).

Ghi `<lượt>/ca/<mã>.json` (bảng phép kiểm, không ghi bản ghi đầy đủ; kèm sha256 bản ghi chuỗi), `progress.jsonl` (giờ,
RSS) ngay từ đầu (SL25). Song song theo ca (`--so`), mỗi tiến trình một ca; ca đã có tệp thì bỏ qua (giữ mọi lượt).

Chạy: $PY -B results/T-046/scripts/b3_chay.py --luot results/T-046/runs/<tên> [--so 4] [--ca dev-…,…] [--cong G0,G4]
Bản 3 (B5): `--cong G0,G4` tính G4 cho metric và D1 cho đơn vị đếm; p G3 của đơn vị sự kiện lấy từ lượt b3-aa-001 khi ghép.
"""
import argparse
import hashlib
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import psutil

import t046
from t046 import ROOT

T045 = {'RE2-TT': ROOT / 'results/T-045/runs/b2-t1-re2-seed0-001/ban-ghi.jsonl',
        'Nezha-OB': ROOT / 'results/T-045/runs/b2-t1-nezha-seed0-001/ban-ghi.jsonl'}
CUA_SO = (('aa', 'R0'), ('aa', 'K-du'), ('that', 'R0'))


def tat_ha_toc():
    """Như results/T-045/scripts/chay_pha1.py: tắt EcoQoS cho chính tiến trình (không đổi kết quả tính)."""
    try:
        import ctypes
        from ctypes import wintypes

        class _PT(ctypes.Structure):
            _fields_ = [('Version', ctypes.c_ulong), ('ControlMask', ctypes.c_ulong), ('StateMask', ctypes.c_ulong)]
        s = _PT(1, 0x1, 0x0)
        k = ctypes.WinDLL('kernel32', use_last_error=True)
        k.GetCurrentProcess.restype = wintypes.HANDLE
        k.SetProcessInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k.SetProcessInformation.restype = wintypes.BOOL
        return bool(k.SetProcessInformation(k.GetCurrentProcess(), 4, ctypes.byref(s), ctypes.sizeof(s)))
    except Exception:
        return False


def _dong_t045(ds, oid):
    with open(T045[ds], encoding='utf-8') as f:
        for x in f:
            if f'"opaque_id":"{oid}"' in x and '"config_id":"T1-R0"' in x:
                return x.rstrip('\n')
    return None


def mot_ca(ds, oid, ra, cong_ds=t046.CONG):
    tat_ha_toc()
    mt = t046.moi_truong()
    out = {'dataset': ds, 'opaque_id': oid, 'cua_so': {}, 'pid': os.getpid(),
           'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED')}
    gio = {}
    for kieu, cfg in CUA_SO:
        t0 = time.perf_counter()
        ca, t, meta = t046.nap(ds, oid, kieu, mt)
        t1 = time.perf_counter()
        rec, cap, p = t046.chay_chuoi(ca, t, t046.cau_hinh(cfg), t046.CacheMoc())
        t2 = time.perf_counter()
        bang = t046.bang_phep(ca, t, p, rec, cap, tinh_cong=cong_ds)
        t3 = time.perf_counter()
        dong = t046.json_ban_ghi(rec, oid)
        x = {'meta': meta, 't_chay': t, 'config_id': p['config_id'], 'sha256_ban_ghi': hashlib.sha256(
            dong.encode('utf-8')).hexdigest(), 'bang': bang}
        if kieu == 'that':
            cu = _dong_t045(ds, oid)
            x['trung_T045'] = (cu == dong)
            if not x['trung_T045']:
                raise RuntimeError(f'bản ghi cửa sổ thật khác T-045: {oid}')
        out['cua_so'][f'{kieu}|{cfg}'] = x
        gio[f'{kieu}|{cfg}'] = dict({'nap': round(t1 - t0, 2), 'chuoi': round(t2 - t1, 2), 'bang': round(t3 - t2, 2)},
                                    **{g: round(v, 2) for g, v in bang['gio_cong'].items()})
        del ca, rec, cap
    out['gio'] = gio
    m = psutil.Process().memory_info()
    out['rss'] = m.rss
    out['dinh_rss'] = getattr(m, 'peak_wset', None)
    du = (json.dumps(out, ensure_ascii=False, sort_keys=True) + '\n').encode('utf-8')
    tam = ra / 'ca' / f'{oid}.json.tmp'
    tam.write_bytes(du)
    tam.replace(ra / 'ca' / f'{oid}.json')
    return oid, gio, out['dinh_rss']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--so', type=int, default=4)
    ap.add_argument('--ca', default='')
    ap.add_argument('--cong', default=','.join(t046.CONG), help='bản 3: G0,G4')
    a = ap.parse_args()
    ra = Path(a.luot)
    (ra / 'ca').mkdir(parents=True, exist_ok=True)
    tat_ha_toc()
    mt = t046.moi_truong()
    ds_ca = t046.danh_sach_ca(mt)
    chon = set(x for x in a.ca.split(',') if x)
    if chon:
        ds_ca = [x for x in ds_ca if x[1] in chon]
    lam = [(ds, o) for ds, o in ds_ca if not (ra / 'ca' / f'{o}.json').exists()]
    tham_so = {'argv': sys.argv[1:], 'cong': a.cong, 'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED'), 'cua_so': CUA_SO,
               'so_ca': len(ds_ca), 'can_chay': len(lam), 'phien_ban': t046.chuoi.PHIEN_BAN,
               'bat_dau': time.strftime('%Y-%m-%dT%H:%M:%S%z')}
    with open(ra / 'tham-so.json', 'ab') as f:
        f.write((json.dumps(tham_so, ensure_ascii=False) + '\n').encode('utf-8'))
    t0 = time.time()
    with open(ra / 'progress.jsonl', 'ab') as pf, ProcessPoolExecutor(max_workers=a.so) as ex:
        cong_ds = tuple(a.cong.split(','))
        fut = {ex.submit(mot_ca, ds, o, ra, cong_ds): (ds, o) for ds, o in lam}
        for i, f in enumerate(as_completed(fut), 1):
            ds, o = fut[f]
            try:
                oid, gio, dinh = f.result()
                rec = {'su_kien': 'xong', 'ca': oid, 'dataset': ds, 'gio': gio, 'dinh_rss': dinh, 'thu_tu': i,
                       'giay_tu_dau': round(time.time() - t0, 1), 'luc': time.strftime('%H:%M:%S')}
            except Exception as ex_:
                rec = {'su_kien': 'loi', 'ca': o, 'dataset': ds, 'loi': f'{type(ex_).__name__}: {ex_}',
                       'luc': time.strftime('%H:%M:%S')}
            pf.write((json.dumps(rec, ensure_ascii=False) + '\n').encode('utf-8'))
            pf.flush()
            print(json.dumps(rec, ensure_ascii=False)[:200], flush=True)
    print('xong', round(time.time() - t0, 1))


if __name__ == '__main__':
    main()
