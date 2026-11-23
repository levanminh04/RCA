# -*- coding: utf-8 -*-
"""T-069 bước 7 — tính lại z của đơn vị op từ span thô để đối chiếu s M1 ghi (chỉ đọc; chạy qua stdin hoặc cục bộ).
z = (max(A) − trung vị(N)) / IQR(N)  — như src/m1/e4.py::_diem_z_native; N = [t−300, t), A = [t, t+300) (cửa sổ của đầu ra).
Đơn vị op = mọi span của service có tên span đó (gộp mọi câu lệnh), như span.mau_thao_tac (xấp xỉ: không áp lọc span con
vượt biên của E1; đối chiếu bằng số với s ghi trong kenh_co).
Dùng: python3 - <raw-traces.jsonl> <N_bat_dau_s> <A_bat_dau_s> <A_ket_thuc_s> <service>|<ten span> [...]"""
import json, sys
import statistics
sys.stdout.reconfigure(encoding='utf-8')
f, n0, a0, a1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
can = [tuple(x.split('|', 1)) for x in sys.argv[5:]]
d = {k: {'N': [], 'A': [], 'maxA_q': None} for k in can}


def attr(xs, k):
    for a in xs:
        if a['key'] == k:
            v = a['value']; return v.get('stringValue') or v.get('intValue')


for line in open(f, encoding='utf-8'):
    o = json.loads(line)
    for rs in o.get('resourceSpans', []):
        svc = attr(rs['resource'].get('attributes', []), 'service.name')
        for ss in rs.get('scopeSpans', []):
            for sp in ss.get('spans', []):
                k = (svc, sp['name'])
                if k not in d: continue
                st = int(sp['startTimeUnixNano']) / 1e9
                w = 'N' if n0 <= st < a0 else ('A' if a0 <= st < a1 else None)
                if not w: continue
                du = (int(sp['endTimeUnixNano']) - int(sp['startTimeUnixNano'])) / 1e6
                d[k][w].append(du)
                if w == 'A' and (d[k]['maxA_q'] is None or du > d[k]['maxA_q'][0]):
                    at = sp.get('attributes', [])
                    d[k]['maxA_q'] = (du, (attr(at, 'db.query.text') or attr(at, 'db.statement') or '?')[:110])
for k, x in d.items():
    N = sorted(x['N']); A = x['A']
    if len(N) < 4 or not A: print(k, 'thiếu mẫu'); continue
    q = statistics.quantiles(N, n=4, method='inclusive')
    med, iqr = statistics.median(N), q[2] - q[0]
    print(f'{k[0]} | {k[1]}: nN={len(N)} nA={len(A)} med_N={med:.3f} ms IQR_N={iqr:.3f} ms max_A={max(A):.1f} ms '
          f'z={(max(A) - med) / iqr:.1f}\n    mẫu max A: {x["maxA_q"][1]}')
