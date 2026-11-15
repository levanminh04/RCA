# -*- coding: utf-8 -*-
"""Chấm tập chọn dev bản 2 (T-064, tiêu chí results/T-064/tieu-chi-chon.md, đáp án khai trước results/T-064/dap-an-dev2.json).
Dùng: <py ghim> -B results/T-064/cham/cham_dev2.py --tap <tap-chon.json> --dau-ra <thư mục> --ra <file.json> P7 V001 V002 ...
  <tap-chon.json>: {"ca": [{"ma": "<mã mờ>", "o": "<ô>"}...]} — khai trong LOG T-064 TRƯỚC khi chấm (ô lấy từ sổ, phía chấm).
  <thư mục>/<bản>/<mã>/method-output-1.json; bản "P7" = đầu ra ghim của run-m1 (outputs/<mã>/ trong gói ca).
Mọi bản so với P7 trên cùng tập. Chỉ đọc đầu ra; nhãn chỉ ở phía chấm."""
import argparse, hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R))
from src.m1_ft import cham
ap = argparse.ArgumentParser(); ap.add_argument('--tap', required=True); ap.add_argument('--dau-ra', required=True)
ap.add_argument('--ra', required=True); ap.add_argument('ban', nargs='+'); a = ap.parse_args()
DA = json.loads((R / 'results/T-064/dap-an-dev2.json').read_text(encoding='utf-8'))
LOI = {x['o']: x for x in DA['o_loi']}; KL = {x['o'] for x in DA['o_khong_loi']}
tap = json.loads(Path(a.tap).read_text(encoding='utf-8'))['ca']
for c in tap:
    if c['o'] not in LOI and c['o'] not in KL: raise SystemExit('ô không có đáp án khai trước: ' + c['o'])
D = Path(a.dau_ra)


def cham_ban(ma):
    loi, kl, ca = {}, {}, {}
    for c in tap:
        f = D / ma / c['ma'] / 'method-output-1.json'
        rec = json.loads(f.read_text(encoding='utf-8')) if f.exists() else {'status': 'MISSING'}
        r, canh = {}, None
        if c['o'] in LOI:
            x = LOI[c['o']]
            if x['root'] and x['root'].get('type') == 'edge':
                canh = cham.cham_canh(rec, (x['root']['caller'], x['root']['callee'], x['root'].get('kind')))
            r = cham.cham_ca_loi(cham.chieu_canh_ve_nut(rec), x['tap_chap_nhan']); loi[c['ma']] = r
        else:
            r = cham.cham_ca_khong_loi(rec); kl[c['ma']] = r
        ca[c['ma']] = {'o': c['o'], 'status': rec.get('status'), 'verdict': rec.get('verdict'),
                       'nhom_hang_1': cham.nhom_hang_1(rec) if rec.get('status') == 'OK' else [],
                       **{k: r[k] for k in r if k in ('p1', 'p3', 'hang_ky_vong', 'k')},
                       'sha256': hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None,
                       **({'bang_canh': canh} if canh is not None else {})}
    tong = cham.tong_hop(loi)
    K = sum(v['k'] for v in kl.values())
    Kf = sum(v['k'] for m, v in kl.items() if ca[m]['o'] == 'FLASH-HEALTHY')
    bc = [v['bang_canh'] for v in ca.values() if 'bang_canh' in v]
    return {'tong': tong, 'K': K, 'K_flash': Kf, 'so_ca_khong_loi': len(kl), 'ca': ca, 'loi': loi,
            'bang_canh': {'so_o': len(bc), 'top3': sum(x.get('top3', 0) for x in bc if x.get('trang_thai') == 'OK'),
                          'trang_thai': [x.get('trang_thai') for x in bc], 'hang': [x.get('hang_ky_vong') for x in bc]}}


kq = {ma: cham_ban(ma) for ma in a.ban}
if 'P7' in kq:
    p = kq['P7']
    for ma, v in kq.items():
        if ma == 'P7': continue
        v['so_voi_P7'] = cham.so_sanh(v['tong'], p['tong']); v['khong_xau_di'] = cham.khong_xau_di(v['tong'], p['tong'])
        v['tut_qua_2_bac'] = cham.tut_qua_2_bac(v['loi'], p['loi']); v['K_tang'] = v['K'] > p['K']
for v in kq.values(): v.pop('loi')
out = {'tap': a.tap, 'tap_sha256': hashlib.sha256(Path(a.tap).read_bytes()).hexdigest(),
       'dap_an_sha256': hashlib.sha256((R / 'results/T-064/dap-an-dev2.json').read_bytes()).hexdigest(),
       'tieu_chi_sha256': hashlib.sha256((R / 'results/T-064/tieu-chi-chon.md').read_bytes()).hexdigest(), 'ban': kq}
Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for ma, v in kq.items():
    t = v['tong']
    print(f"{ma:8s} AC@1={t['AC@1']:.3f} AC@3={t['AC@3']:.3f} tong_hang={t['tong_hang_cat']:.3f} K={v['K']}/{v['so_ca_khong_loi']} "
          f"canh={v['bang_canh']['top3']}/{v['bang_canh']['so_o']} so_P7={v.get('so_voi_P7', '-')} tut2={v.get('tut_qua_2_bac', '-')}")
