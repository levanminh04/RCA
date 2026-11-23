# -*- coding: utf-8 -*-
"""T-072 — đối chiếu bộ chấm offline (đúng code cham_offline.py) với lịch sử trạng thái Grafana trên lượt E3.

Đọc: results/T-071/e3/xuat-tin-hieu.json (chuỗi E3), results/T-072/e3/b9-lich-su.json (annotation Grafana),
bieu-thuc.json, nguong.json. Luật thử = bản sao luật p95 (cùng chuỗi tin-hieu/t072-p95-<route>) với ngưỡng 0,005 s.
Không đọc sổ tiêm. Ghi results/T-072/e3-doi-chieu-offline.json.
"""
import copy, json, pathlib, sys
G = pathlib.Path(__file__).parent
src = (G / 'cham_offline.py').read_text(encoding='utf-8')
assert src.rstrip().endswith('main()')
ns = {'__name__': 'cham_offline_lib', '__file__': str(G / 'cham_offline.py')}
exec(compile(src.rstrip()[:-len('main()')], 'cham_offline.py', 'exec'), ns)
X = G.parent / 'T-071' / 'e3' / 'xuat-tin-hieu.json'
bt = json.loads((G / 'bieu-thuc.json').read_text(encoding='utf-8'))
ng = json.loads((G / 'nguong.json').read_text(encoding='utf-8'))['nguong']
du = ns['Du'](); doc = json.loads(X.read_text(encoding='utf-8')); du.them(doc)
luat = list(bt['luat'])
for L in bt['luat']:
    if L['nhan'].get('t072_tin_hieu') == 'p95':
        T = copy.deepcopy(L); T['uid'] = 't072-thu-' + L['uid'][5:]; T['loai'] = 'thu'
        T['dieu_kien'] = dict(L['dieu_kien'], nguong=0.005)
        du.chuoi['tin-hieu/' + T['uid']] = du.chuoi.get('tin-hieu/' + L['uid'], {})
        luat.append(T)
kcs = ns['danh_gia'](dict(bt, luat=luat), du, ng)
ls = json.loads((G / 'e3' / 'b9-lich-su.json').read_text(encoding='utf-8'))
gf = {}
for a in ls['annotation']:
    gf.setdefault(a['uid'], []).append((a['prev_state'], a['new_state'], a['epoch'] / 1000))
luoi = sorted(du.luoi)
ra = {'cua_so_xuat': [luoi[0], luoi[-1]], 'pha_luoi_xuat_s': luoi[0] % 10, 'theo_uid': {}}
for L in luat:
    u = L['uid']
    off = [k for k in kcs if k['uid'] == u]
    g = gf.get(u, [])
    gp = [e for p, n, e in g if n.startswith('Pending')]; ga = [e for p, n, e in g if n.startswith('Alerting')]
    gn = [e for p, n, e in g if p.startswith('Alerting') and not n.startswith('Alerting')]
    o = {'so_khoang_offline': len(off), 'so_khoang_grafana': len(ga),
         'offline': [{'khoa': k['khoa'], 'pending': k['tp'], 'alerting': k['t_hat'], 'het': k['t_het'], 'cat': k['cat']} for k in off],
         'grafana': {'pending': gp, 'alerting': ga, 'het': gn, 'ly_do_het': [n for p, n, e in g if p.startswith('Alerting')]}}
    if off and ga:
        k = off[0]
        o['lech_s'] = {'pending': (k['tp'] - gp[0]) if gp else None, 'alerting': k['t_hat'] - ga[0],
                       'het': (k['t_het'] - gn[0]) if (k['t_het'] is not None and gn) else None}
    o['khop_so_khoang'] = len(off) == len(ga)
    ra['theo_uid'][u] = o
(G / 'e3-doi-chieu-offline.json').write_text(json.dumps(ra, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for u, o in ra['theo_uid'].items():
    sys.stdout.buffer.write(f"{u}: offline {o['so_khoang_offline']} / grafana {o['so_khoang_grafana']} lech {o.get('lech_s')}\n".encode())
sys.stdout.buffer.write(f"luoi {ra['cua_so_xuat']} pha {ra['pha_luoi_xuat_s']}\n".encode())
