"""T-045: chạy pha 1 của M1 theo từng ca (LOG phiên 1, Đ-1), không đọc nhãn.

Mỗi ca: adapter nạp dữ liệu → `runner.pha1([ca], {mã mờ: t}, cấu hình, <lượt>/ca/<mã mờ>)` → giải phóng. Sau cùng ghép
dòng của mọi ca theo (config_id, opaque_id) thành `<lượt>/ban-ghi.jsonl` và ghi `<lượt>/pha1.json` cùng trường như
`runner.pha1`. Ghép cho đúng byte như một lần gọi chung, vì pha1 đặt cache cổng mới cho mỗi ca (S38) và sắp dòng theo
cấu hình rồi ca; phép kiểm `--kiem-ghep` so hai cách trên các ca được chọn.

Mốc t: RE2-TT từ `p3.nhan.nap_moc(results/T-022/nhan-dev.json)` (chỉ mốc tiêm; Q-66, CĐ11); Nezha-OB từ allowlist.
Mốc giả (`--moc-gia`): chỉ RE2-TT, t′ = t − 300.
Xáo hàng (`--xao <seed>`, Đ-3): xáo span, hàng metric, dòng log; với Nezha-OB hoán vị mốc riêng của nguồn metric cùng
hoán vị hàng metric.
Ghi `progress.jsonl` (thời gian, RSS, đỉnh RSS theo ca) từ đầu (SL25).

Chạy (sau `source results/T-045/scripts/moi_truong.sh`):
  $PY -B results/T-045/scripts/chay_pha1.py --luot <tên> --cau-hinh T1 [--ds RE2-TT|Nezha-OB|all] [--ca dev-…,…]
      [--dau N] [--moc-gia] [--xao 0] [--khop hoan_toan] [--doc-nhom-vong co_vong] [--kiem-ghep]
"""
import argparse
import gc
import hashlib
import json
import os
import random
import sys
import time
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))

from m1 import adapter, runner  # noqa: E402
from p3 import nezha, nhan, selector  # noqa: E402

RUNS = ROOT / 'results/T-045/runs'
NUA = 300


def tat_ha_toc():
    """Windows 11 hạ tốc (EcoQoS) tiến trình nền không cửa sổ: đơn vị chạy qua bộ điều phối mất 50–54 s thay vì 18 s
    (LOG phiên 1). Tắt việc hạ tốc cho chính tiến trình này (ProcessPowerThrottling = 4, EXECUTION_SPEED, trạng thái
    0); không đổi cài đặt hệ thống, không đổi kết quả tính."""
    try:
        import ctypes

        class _PT(ctypes.Structure):
            _fields_ = [('Version', ctypes.c_ulong), ('ControlMask', ctypes.c_ulong), ('StateMask', ctypes.c_ulong)]
        from ctypes import wintypes
        s = _PT(1, 0x1, 0x0)
        k = ctypes.WinDLL('kernel32', use_last_error=True)
        k.GetCurrentProcess.restype = wintypes.HANDLE
        k.SetProcessInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k.SetProcessInformation.restype = wintypes.BOOL
        return bool(k.SetProcessInformation(k.GetCurrentProcess(), 4, ctypes.byref(s), ctypes.sizeof(s)))
    except Exception:
        return False


def _rss():
    m = psutil.Process().memory_info()
    return m.rss, getattr(m, 'peak_wset', None)


def _ghi(f, obj):
    f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + '\n')
    f.flush()


def cau_hinh(ten, khop, doc_nhom_vong, sim_th=None):
    mt = runner.ap_dinh_chinh(json.loads((ROOT / 'results/T-043/ma-tran-thu.json').read_text(encoding='utf-8')))
    ts3 = dict(runner.TS_E3, khop=khop)
    if sim_th is not None:  # D3 tùy chọn: ngưỡng của Nezha (OB 0,9; TT 0,8); không đổi ma trận
        ts3['sim_th'] = sim_th
    ts5 = dict(runner.TS_E5, doc_nhom_vong=doc_nhom_vong)
    sinh = runner.sinh_cau_hinh(mt, {}, dict(runner.R0))
    out = []
    for x in ten.split(','):
        if x in ('T1', 'T4', 'T4b'):
            out += sinh[x]
        elif x == 'K':
            out += sinh['K']
        elif x.startswith('K-'):  # một cấu hình khối K theo tên, ví dụ K-E3
            c = [c for c in sinh['K'] if c['config_id'] == x]
            if not c:
                raise SystemExit(f'không có cấu hình {x}')
            out += c
        else:
            raise SystemExit(f'nhóm cấu hình lạ: {x}')
    if ts3 != runner.TS_E3 or doc_nhom_vong != runner.TS_E5['doc_nhom_vong']:
        hau_to = f"|khop={khop}|sim={ts3['sim_th']}|nv={doc_nhom_vong}"
        out = [runner._cau_hinh(c['buoc'], c['config_id'].split('-', 1)[1] + hau_to, c['bat_tat'], c['tham_so_E4'],
                                c['nhanh_z'], ts3, ts5) for c in out]
    return out


def danh_sach_ca(ds, chon, dau, moc_gia):
    re = selector.nap_allowlist(ROOT / 'results/T-022/allowlist-dev.json')
    nz = nezha.nap_allowlist(ROOT / 'results/T-026/allowlist-dev.json')
    out = []
    if ds in ('RE2-TT', 'all'):
        out += [('RE2-TT', o) for o in sorted(re)]
    if ds in ('Nezha-OB', 'all') and not moc_gia:
        out += [('Nezha-OB', o) for o in sorted(nz)]
    if chon:
        out = [x for x in out if x[1] in chon]
    if dau:
        out = [x for x in out if x[0] == 'RE2-TT'][:dau] + [x for x in out if x[0] == 'Nezha-OB'][:dau]
    return out, re, nz


def nap_ca(ds, oid, re, nz, moc_re, moc_gia, hop_dong, U_re):
    if ds == 'RE2-TT':
        t = moc_re[oid] - (NUA if moc_gia else 0)
        ca = adapter.ca_re2tt(re, oid, t, ROOT, hop_dong, U_re)
    else:
        ca = adapter.ca_nezha(nz, oid, ROOT, hop_dong)
        t = ca['t']
    return ca, t


def xao(ca, seed):
    rng = random.Random(seed)
    rng.shuffle(ca['spans'])
    rng.shuffle(ca['logs'])
    n = len(ca['metrics'])
    hv = list(range(n))
    rng.shuffle(hv)
    ca['metrics'] = [ca['metrics'][i] for i in hv]
    tg = ca['params_ca'].get('thoi_gian_nguon') or {}
    for k, v in list(tg.items()):
        if isinstance(v, list):
            if len(v) != n:
                raise ValueError(f'mốc nguồn {k}: {len(v)} mốc cho {n} hàng')
            tg[k] = [v[i] for i in hv]
    return ca


def ghep(luot_dir, ds_ca, ds_ch):
    dong = []
    for oid in ds_ca:
        d = luot_dir / 'ca' / oid
        meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
        du = (d / meta['tep']).read_bytes()
        if hashlib.sha256(du).hexdigest() != meta['sha256']:
            raise SystemExit(f'hash lệch ở {d}')
        for x in du.decode('utf-8').splitlines():
            if x:
                r = json.loads(x)
                dong.append(((r['config_id'], r['opaque_id']), x))
    dong.sort(key=lambda z: z[0])
    du_lieu = ('\n'.join(x for _, x in dong) + '\n').encode('utf-8')
    (luot_dir / 'ban-ghi.jsonl').write_bytes(du_lieu)
    h = hashlib.sha256(du_lieu).hexdigest()
    meta = {'tep': 'ban-ghi.jsonl', 'sha256': h, 'so_ban_ghi': len(dong), 'phien_ban': runner.chuoi.PHIEN_BAN,
            'cau_hinh': sorted(c['config_id'] for c in ds_ch), 'so_ca': len(ds_ca)}
    (luot_dir / 'pha1.json').write_text(runner._json(meta) + '\n', encoding='utf-8')
    return h, len(dong)


def song_song(a, luot_dir):
    """Chế độ chạy song song (LOG phiên 1, mục chạy song song): mỗi tiến trình một ca (`--mot-ca`), ghi vào
    <lượt>/ca/<mã>/ như `runner.pha1` cho một ca; sau cùng `--chi-ghep` ghép theo Đ-1. Ca đã có `pha1.json` thì
    không chạy lại (giữ mọi lượt)."""
    hop_dong = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
    U_re = json.loads((ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    moc_re = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')  # chỉ mốc tiêm (Q-66, CĐ11)
    ds_ch = cau_hinh(a.cau_hinh, a.khop, a.doc_nhom_vong, a.sim_th)
    chon = set(x for x in a.ca.split(',') if x)
    ds_ca, re, nz = danh_sach_ca(a.ds, chon, a.dau, a.moc_gia)
    if a.chi_ghep:
        thieu = [o for _, o in ds_ca if not (luot_dir / 'ca' / o / 'pha1.json').exists()]
        if thieu:
            raise SystemExit(f'chưa đủ ca để ghép: {thieu}')
        h, n = ghep(luot_dir, [o for _, o in ds_ca], ds_ch)
        cd = {o: json.loads((luot_dir / 'ca' / o / 'chan-doan-adapter.json').read_text(encoding='utf-8'))
              for _, o in ds_ca}
        (luot_dir / 'chan-doan-adapter.json').write_text(json.dumps(cd, ensure_ascii=False, indent=1) + '\n',
                                                        encoding='utf-8')
        print('sha256', h, 'so_ban_ghi', n)
        return
    ds = dict((o, d) for d, o in ds_ca)
    if a.mot_ca not in ds:
        raise SystemExit(f'ca không thuộc danh sách của lượt: {a.mot_ca}')
    d = luot_dir / 'ca' / a.mot_ca
    if (d / 'pha1.json').exists():
        print('da_co', a.mot_ca)
        return
    d.mkdir(parents=True, exist_ok=True)
    tham_so = {'argv': sys.argv[1:], 'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED'),
               'cau_hinh': [c['config_id'] for c in ds_ch], 'moc_gia': a.moc_gia, 'xao': a.xao, 'khop': a.khop,
               'sim_th': a.sim_th, 'doc_nhom_vong': a.doc_nhom_vong, 'phien_ban': runner.chuoi.PHIEN_BAN}
    (d / 'tham-so.json').write_text(json.dumps(tham_so, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    t0 = time.time()
    ca, t = nap_ca(ds[a.mot_ca], a.mot_ca, re, nz, moc_re, a.moc_gia, hop_dong, U_re)
    if a.xao is not None:
        ca = xao(ca, a.xao)
    t1 = time.time()
    rss_nap = _rss()[0]
    runner.pha1([ca], {a.mot_ca: t}, ds_ch, d)
    t2 = time.time()
    rss, dinh = _rss()
    (d / 'chan-doan-adapter.json').write_text(json.dumps(dict(ca.get('chan_doan_adapter') or {}, dataset=ds[a.mot_ca]),
                                                         ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    with open(d / 'progress.jsonl', 'w', encoding='utf-8') as pf:
        _ghi(pf, {'su_kien': 'ca', 'ca': a.mot_ca, 'dataset': ds[a.mot_ca], 'tat_ha_toc': tat_ha_toc(),
                  'giay_nap': round(t1 - t0, 2),
                  'giay_pha1': round(t2 - t1, 2), 'rss_sau_nap': rss_nap, 'rss': rss, 'dinh_rss': dinh,
                  'xong': time.strftime('%Y-%m-%dT%H:%M:%S%z')})
    print(f'{a.mot_ca} nap {t1 - t0:.1f}s pha1 {t2 - t1:.1f}s dinh {(dinh or 0) / 2**30:.2f}GiB', flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', required=True)
    ap.add_argument('--cau-hinh', default='T1')
    ap.add_argument('--ds', default='all')
    ap.add_argument('--ca', default='')
    ap.add_argument('--dau', type=int, default=0)
    ap.add_argument('--moc-gia', action='store_true')
    ap.add_argument('--xao', type=int, default=None)
    ap.add_argument('--khop', default='hoan_toan')
    ap.add_argument('--doc-nhom-vong', default='co_vong')
    ap.add_argument('--sim-th', type=float, default=None)
    ap.add_argument('--kiem-ghep', action='store_true')
    ap.add_argument('--mot-ca', default=None, help='chạy song song: chỉ chạy ca này vào <lượt>/ca/<mã>, không ghép')
    ap.add_argument('--chi-ghep', action='store_true', help='chạy song song: ghép mọi ca đã xong của lượt')
    a = ap.parse_args()
    luot_dir = RUNS / a.luot
    if a.mot_ca or a.chi_ghep:
        tat_ha_toc()
        return song_song(a, luot_dir)
    if luot_dir.exists():
        raise SystemExit(f'lượt đã có, dùng tên mới (giữ mọi lượt): {luot_dir}')
    luot_dir.mkdir(parents=True)
    hop_dong = json.loads((ROOT / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
    U_re = json.loads((ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    moc_re = nhan.nap_moc(ROOT / 'results/T-022/nhan-dev.json')  # chỉ mốc tiêm (Q-66, CĐ11)
    ds_ch = cau_hinh(a.cau_hinh, a.khop, a.doc_nhom_vong, a.sim_th)
    chon = set(x for x in a.ca.split(',') if x)
    ds_ca, re, nz = danh_sach_ca(a.ds, chon, a.dau, a.moc_gia)
    tham_so = {'argv': sys.argv[1:], 'PYTHONHASHSEED': os.environ.get('PYTHONHASHSEED'),
               'cau_hinh': [c['config_id'] for c in ds_ch], 'ca': [o for _, o in ds_ca], 'moc_gia': a.moc_gia,
               'xao': a.xao, 'khop': a.khop, 'sim_th': a.sim_th, 'doc_nhom_vong': a.doc_nhom_vong,
               'phien_ban': runner.chuoi.PHIEN_BAN}
    (luot_dir / 'tham-so.json').write_text(json.dumps(tham_so, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    t_bat_dau = time.time()
    chan_doan = {}
    mem_ca = []
    with open(luot_dir / 'progress.jsonl', 'w', encoding='utf-8') as pf:
        _ghi(pf, {'su_kien': 'bat_dau', 'thoi_diem': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'so_ca': len(ds_ca),
                  'so_cau_hinh': len(ds_ch), 'rss': _rss()[0]})
        for i, (ds, oid) in enumerate(ds_ca):
            t0 = time.time()
            ca, t = nap_ca(ds, oid, re, nz, moc_re, a.moc_gia, hop_dong, U_re)
            if a.xao is not None:
                ca = xao(ca, a.xao)
            t1 = time.time()
            rss_nap = _rss()[0]
            runner.pha1([ca], {oid: t}, ds_ch, luot_dir / 'ca' / oid)
            t2 = time.time()
            rss, dinh = _rss()
            chan_doan[oid] = dict(ca.get('chan_doan_adapter') or {}, dataset=ds)
            if a.kiem_ghep:
                mem_ca.append((ca, t))
            del ca
            gc.collect()
            _ghi(pf, {'su_kien': 'ca', 'i': i + 1, 'ca': oid, 'dataset': ds, 'giay_nap': round(t1 - t0, 2),
                      'giay_pha1': round(t2 - t1, 2), 'rss_sau_nap': rss_nap, 'rss': rss, 'dinh_rss': dinh,
                      'giay_tu_dau': round(t2 - t_bat_dau, 1)})
            print(f'{i + 1}/{len(ds_ca)} {ds} {oid} nap {t1 - t0:.1f}s pha1 {t2 - t1:.1f}s rss {rss / 2**30:.2f}GiB '
                  f'dinh {(dinh or 0) / 2**30:.2f}GiB', flush=True)
        h, n = ghep(luot_dir, [o for _, o in ds_ca], ds_ch)
        _ghi(pf, {'su_kien': 'ghep', 'sha256': h, 'so_ban_ghi': n, 'giay_tu_dau': round(time.time() - t_bat_dau, 1)})
        if a.kiem_ghep:  # Đ-1: một lần gọi chung cho các ca đã chọn phải cho đúng byte của bản ghép
            d = luot_dir / 'kiem-ghep-chung'
            kq = runner.pha1([c for c, _ in mem_ca], {c['opaque_id']: t for c, t in mem_ca}, ds_ch, d)
            ok = kq['sha256'] == h
            _ghi(pf, {'su_kien': 'kiem_ghep', 'sha256_chung': kq['sha256'], 'sha256_ghep': h, 'khop': ok})
            print('kiem_ghep', 'KHOP' if ok else 'LECH', kq['sha256'], h)
        _ghi(pf, {'su_kien': 'xong', 'giay': round(time.time() - t_bat_dau, 1), 'dinh_rss': _rss()[1]})
    (luot_dir / 'chan-doan-adapter.json').write_text(json.dumps(chan_doan, ensure_ascii=False, indent=1) + '\n',
                                                    encoding='utf-8')
    print('sha256', h, 'so_ban_ghi', n)


if __name__ == '__main__':
    main()
