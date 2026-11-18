# -*- coding: utf-8 -*-
"""T-066 bước 3: so gói do bộ xuất chung mới (repo lab campaigns/runner/xuat_bo_sung.py) sinh ra với 7 gói chuẩn.

Phép chính (tiêu chí xong 2): kênh live-down, so tập bộ (http_url, timestamp, giá trị) — phải trùng hoàn toàn.
Báo thêm: 23 kênh còn lại, so tập bộ (metric chuẩn hóa, timestamp, giá trị).
Gói chuẩn: archive D:/RCA-archive/exp-obs/m1ft-inputs (hash đã kiểm ở phu-thuoc.md A4); gói mới: results/T-066/r9-xuat/.
Chạy: py -3 -I results/T-066/so_r9.py > results/T-066/r9-tong-quat.json
"""
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ARC = Path('D:/RCA-archive/exp-obs/m1ft-inputs')
MOI = Path('D:/RCA-flashticket/results/T-066/r9-xuat')
CHUAN = {('46aab4be', 'd0'): ARC / 'bo-sung-dev2/46aab4be/prometheus-bo-sung.json'}
CHUAN.update({('ebd5ef38', d): ARC / f'out/r9-bo-sung/{d}/ebd5ef38/prometheus-bo-sung.json'
              for d in ('d-60', 'd-30', 'd-15', 'd0', 'd15', 'd30')})
XUAT = Path('D:/Project/flashticket-rca-lab/campaigns/runner/xuat_bo_sung.py')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def bo(bundle, chi_url):
    s = set()
    for x in bundle['result']:
        k = x['metric'].get('http_url', '') if chi_url else json.dumps(x['metric'], sort_keys=True)
        for t0, v in x['values']:
            s.add((k, float(t0), v))
    return s


kq = {'bo_xuat': {'duong_dan': 'flashticket-rca-lab/campaigns/runner/xuat_bo_sung.py (chưa commit lúc chạy)',
                  'sha256': sha(XUAT)},
      'lenh_xuat': "ssh exp-obs 'python3 - --t <t>' < xuat_bo_sung.py > results/T-066/r9-xuat/<ca>-<d>.json",
      'goi': [], 'tong_ket': {}}
dat_live, dat_khac = 0, 0
for (ca, d), p in CHUAN.items():
    c = json.loads(p.read_text(encoding='utf-8'))
    m_path = MOI / f'{ca}-{d}.json'
    m = json.loads(m_path.read_text(encoding='utf-8'))
    muc = {'ca': ca, 'd': d, 'goi_chuan': str(p), 'goi_chuan_sha256': sha(p), 'goi_chuan_phien_ban': c['phien_ban'],
           'goi_moi': str(m_path), 'goi_moi_sha256': sha(m_path), 'goi_moi_phien_ban': m['phien_ban'],
           't_trung': c['t'] == m['t'], 'cua_so_trung': c['cua_so'] == m['cua_so'], 'loi_khuc_moi': m['loi_khuc']}
    bc = {b['channel']: b for b in c['bundles']}
    bm = {b['channel']: b for b in m['bundles']}
    muc['kenh_trung_tap'] = sorted(bc) == sorted(bm)
    lc, lm = bo(bc['live-down'], True), bo(bm['live-down'], True)
    muc['live_down'] = {'so_bo_chuan': len(lc), 'so_bo_moi': len(lm), 'chi_chuan': len(lc - lm), 'chi_moi': len(lm - lc),
                        'so_bo_gia_tri_1_chuan': sum(1 for x in lc if x[2] == '1'),
                        'vi_du_lech': sorted(lc ^ lm)[:5], 'trung': lc == lm}
    khac = {}
    for ch in sorted(set(bc) - {'live-down'}):
        a, b = bo(bc[ch], False), bo(bm.get(ch, {'result': []}), False)
        if a != b:
            khac[ch] = {'so_bo_chuan': len(a), 'so_bo_moi': len(b), 'chi_chuan': len(a - b), 'chi_moi': len(b - a)}
    muc['kenh_khac_lech'] = khac
    muc['kenh_khac_trung'] = not khac
    dat_live += muc['live_down']['trung'] and muc['t_trung'] and muc['cua_so_trung']
    dat_khac += not khac
    kq['goi'].append(muc)
kq['tong_ket'] = {'so_goi': len(CHUAN), 'live_down_trung': dat_live, 'kenh_khac_trung_ca_23': dat_khac,
                  'tieu_chi_2_dat': dat_live == len(CHUAN)}
json.dump(kq, sys.stdout, ensure_ascii=False, indent=1)
print()
