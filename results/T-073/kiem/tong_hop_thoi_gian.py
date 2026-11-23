# -*- coding: utf-8 -*-
"""T-073: tổng hợp thời gian từng bước của tuyến (b) từ các file su-co/<mã>.json đã kéo về (lượt dev trên exp-obs).

    py -3 tong_hop_thoi_gian.py <thư mục chứa các lượt t073-dev-*> <file ra json>
Mỗi lượt: <lượt>/su-co/*.json, <lượt>/nhat-ky.jsonl. Chỉ đọc dữ liệu của bộ điều phối (không có nhãn).
"""
import glob
import hashlib
import json
import os
import sys

goc, ra = sys.argv[1], sys.argv[2]
ca = []
for f in sorted(glob.glob(os.path.join(goc, 't073-dev-*', 'su-co', '*.json'))):
    s = json.load(open(f, encoding='utf-8'))
    luot = f.replace(os.sep, '/').split('/')[-3]
    buoc = {b['ten']: {'giay': b.get('giay'), 'ok': b.get('ok'), 'loi': (b.get('loi') or '')[-200:] or None} for b in s['buoc']}
    xu_ly = sum(b['giay'] for b in s['buoc'] if b.get('giay') is not None and b.get('ok'))
    ca.append({'luot': luot, 'su_co': s['ma'], 'ma_ca_m1': s.get('ma_ca_m1'), 't_hat': s['t_hat'],
               'trang_thai': s['trang_thai'], 'buoc_loi': s.get('buoc_loi'), 'dev': s.get('dev'),
               'buoc': buoc, 'tong_xu_ly_giay_cac_buoc_ok': round(xu_ly, 2),
               'file': os.path.relpath(f, goc).replace(os.sep, '/'),
               'sha256': hashlib.sha256(open(f, 'rb').read()).hexdigest()})
json.dump({'mo_ta': 'Thời gian từng bước tuyến (b) trên exp-obs, lượt dev chạy trên ca cũ (capture giả từ gói cũ, '
                    'prometheus.json và gói bổ sung lấy từ file; nên stage và bổ sung nhanh hơn chạy sống).',
           'ca': ca}, open(ra, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps([(c['luot'], c['trang_thai'], {k: v['giay'] for k, v in c['buoc'].items()}) for c in ca], ensure_ascii=False))
