# -*- coding: utf-8 -*-
"""Chấm các biến thể chạy ở vai trò KIỂM CÀI ĐẶT trên 9 ca T-062 (không dùng để chọn; tập chọn = dev bản 2).
Đọc đầu ra đã chép về results/T-064/bien-the/<mã>/ra-kiem-cai-dat-1/<id>/method-output-1.json; nhãn từ bảng phát lại T-062 đã băm.
Dùng: <py ghim> -B results/T-064/cham/cham_kiem_cai_dat.py <mã>... → results/T-064/cham/kiem-cai-dat-1.json"""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R))
from src.m1_ft import cham
bang = json.loads((R / 'results/T-062/ket-qua/phat-lai/bang-cham.json').read_text(encoding='utf-8'))
CANH = {c['id']: (c['root']['caller'], c['root']['callee'], c['root'].get('kind'))
        for c in json.loads((R / 'results/T-059/danh-muc-loi.json').read_text(encoding='utf-8'))['cells']
        if isinstance(c.get('root'), dict) and c['root'].get('type') == 'edge'}
LOAI = {'data': 'data', 'http': 'http'}
p7 = json.loads((R / 'results/T-064/cham/t062-p7.json').read_text(encoding='utf-8'))
out = {'vai_tro': 'kiem_cai_dat_9_ca_T062', 'P7': {'tong': p7['tong_ca_loi'], 'K': p7['K']}, 'ban': {}}
ARGS = [a for a in sys.argv[1:] if not a.startswith('--ra=') and not a.startswith('--tm=')]
RA = next((a[5:] for a in sys.argv[1:] if a.startswith('--ra=')), 'kiem-cai-dat-1.json')
TM = next((a[5:] for a in sys.argv[1:] if a.startswith('--tm=')), 'ra-kiem-cai-dat-1')  # thư mục đầu ra trong bien-the/<mã>/
for ma in ARGS:
    loi, kl, ca = {}, {}, {}
    for c in bang['ca']:
        f = R / 'results/T-064/bien-the' / ma / TM / c['ma'] / 'method-output-1.json'
        rec = json.loads(f.read_text(encoding='utf-8'))
        canh_r = None
        if c['o'] in CANH:
            a, b, k = CANH[c['o']]
            canh_r = cham.cham_canh(rec, (a, b, LOAI.get(k, k)))
        if c['tap_chap_nhan']:
            r = cham.cham_ca_loi(cham.chieu_canh_ve_nut(rec), c['tap_chap_nhan']); loi[c['ma']] = r
        else:
            r = cham.cham_ca_khong_loi(rec); kl[c['ma']] = r
        ca[c['ma']] = {'o': c['o'], 'verdict': rec.get('verdict'), 'nhom_hang_1': cham.nhom_hang_1(rec) if rec.get('status') == 'OK' else [],
                       **{k: r[k] for k in r if k in ('p1', 'p3', 'hang_ky_vong', 'k')},
                       'p7_verdict': p7['ca'][c['ma']]['verdict'], 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
                       **({'bang_canh': canh_r} if canh_r is not None else {})}
    tong = cham.tong_hop(loi); K = sum(v['k'] for v in kl.values())
    p7ca = {m: v for m, v in p7['ca'].items() if 'p1' in v}
    out['ban'][ma] = {'tong': tong, 'K': K, 'so_voi_P7': cham.so_sanh(tong, p7['tong_ca_loi']),
                      'khong_xau_di': cham.khong_xau_di(tong, p7['tong_ca_loi']),
                      'tut_qua_2_bac': cham.tut_qua_2_bac(loi, {m: v for m, v in p7ca.items()}), 'ca': ca}
    bc = [v['bang_canh'] for v in ca.values() if 'bang_canh' in v]
    out['ban'][ma]['bang_canh'] = {'so_o': len(bc), 'top3': sum(x.get('top3', 0) for x in bc if x.get('trang_thai') == 'OK'),
                                   'trang_thai': [x.get('trang_thai') for x in bc], 'hang': [x.get('hang_ky_vong') for x in bc]}
    print(f"{ma:18s} canh={out['ban'][ma]['bang_canh']} AC@1={tong['AC@1']:.3f} AC@3={tong['AC@3']:.3f} tong_hang={tong['tong_hang_cat']:.3f} K={K}/4  so_P7={out['ban'][ma]['so_voi_P7']}  "
          + ' '.join(f"{v['o'][:10]}:{(v.get('verdict') or '')[:6]}" for v in ca.values() if 'k' in v))
(R / 'results/T-064/cham' / RA).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
