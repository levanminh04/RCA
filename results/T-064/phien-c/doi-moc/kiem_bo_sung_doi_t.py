# -*- coding: utf-8 -*-
"""Kiểm gói bổ sung xuất lại quanh t' (phiên C): ở mọi mốc chung với gói gốc quanh t, mọi chuỗi (kênh, nhãn) có cùng giá trị.
Chạy trên exp-obs: python3 kiem_bo_sung_doi_t.py <thư mục gói gốc bo-sung-dev2> <thư mục ra của xuat_bo_sung_doi_t.sh> <file mã ca>
In JSON: theo ca × d: số điểm chung, số điểm lệch, chuỗi chỉ có ở một bên (trong vùng chung), lỗi khúc, t và cửa sổ."""
import json, sys
G, R, F = sys.argv[1:4]
ids = open(F).read().split()
kq = {}
for i in ids:
    goc = json.load(open(f'{G}/{i}/prometheus-bo-sung.json'))
    for d in (-30, 30):
        moi = json.load(open(f'{R}/d{d}/{i}/prometheus-bo-sung.json'))
        lo, hi = max(goc['cua_so'][0], moi['cua_so'][0]), min(goc['cua_so'][1], moi['cua_so'][1])
        chung = lech = 0; mot_ben = []; vi_du = []
        bg = {b['channel']: b for b in goc['bundles']}; bm = {b['channel']: b for b in moi['bundles']}
        for ch in sorted(set(bg) | set(bm)):
            sg = {json.dumps(s['metric'], sort_keys=True): dict((float(a), v) for a, v in s['values'] if lo <= float(a) <= hi) for s in bg.get(ch, {'result': []})['result']}
            sm = {json.dumps(s['metric'], sort_keys=True): dict((float(a), v) for a, v in s['values'] if lo <= float(a) <= hi) for s in bm.get(ch, {'result': []})['result']}
            for k in sorted(set(sg) | set(sm)):
                a, b = sg.get(k, {}), sm.get(k, {})
                if bool(a) != bool(b):
                    mot_ben.append([ch, k, len(a), len(b)]); continue
                for ts in set(a) | set(b):
                    if ts in a and ts in b:
                        chung += 1
                        if a[ts] != b[ts]:
                            lech += 1
                            if len(vi_du) < 5: vi_du.append([ch, k, ts, a[ts], b[ts]])
                    else:
                        mot_ben.append([ch, k, ts, ts in a, ts in b])
        kq[f'{i}|{d}'] = {'t_goc': goc['t'], 't_moi': moi['t'], 'cua_so_moi': moi['cua_so'], 'phien_ban': moi['phien_ban'],
                          'diem_chung': chung, 'diem_lech': lech, 'vi_du_lech': vi_du, 'mot_ben': mot_ben[:20],
                          'so_mot_ben': len(mot_ben), 'loi_khuc': moi['loi_khuc'], 'dung_t': moi['t'] == goc['t'] + d}
print(json.dumps(kq, ensure_ascii=False, indent=1))
