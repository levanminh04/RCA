# -*- coding: utf-8 -*-
"""T-069 bước 7 — áp lực CPU máy exp-app (PSI /proc/pressure/cpu, đầu dò inj3) và CPU cgroup Booking ở t−240, t+60, t+330, hồi+60;
ca cũ (sổ T-063) so ca mới (sổ T-069) cùng ô. Chỉ đọc sổ đã nhận (phía chấm).
Dùng: py -3 -B results/T-069/so_psi.py > results/T-069/phan-tich/psi.txt"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
R = 'D:/RCA-flashticket'
SO = {'cu-thu2': f'{R}/results/T-063/thu2/tiem-loi/so-thu2.jsonl', 'cu-thu3': f'{R}/results/T-063/thu3/thu/tiem-loi/so-thu3.jsonl',
      'moi': f'{R}/results/T-069/thu/t069-chinh/so.jsonl'}
TC = json.load(open(f'{R}/results/T-069/tieu-chi.json', encoding='utf-8'))
cu = {c['cu']['ma'][:8]: c['o'] for c in TC['cap_ca']}


def psi(p):
    """some avg10, avg60 và total (µs) của dòng 'some'."""
    for l in (p.get('psi_cpu_may') or []):
        if l.startswith('some'):
            d = dict(x.split('=') for x in l.split()[1:]); return float(d['avg10']), float(d['avg60']), int(d['total'])
    return None


def doc(f, chon):
    out = {}
    so = [json.loads(l) for l in open(f, encoding='utf-8')]
    for d in so:
        if d['event'] != 'cycle-begin' or not chon(d['opaque_id'][:8]): continue
        oid = d['opaque_id']; pr = {x['phase']: x['probe'] for x in so if x.get('opaque_id') == oid and x['event'] == 'probe'}
        out[oid] = (d['cell'], pr)
    return out


rows = {}
for k, f in SO.items():
    for oid, (cell, pr) in doc(f, (lambda m: m in cu) if k != 'moi' else (lambda m: True)).items():
        rows.setdefault(cell, {}).setdefault('cu' if k != 'moi' else 'moi', []).append((oid, pr))
print('ô; phía; mã; PSI some avg60 (%) ở t-240 | t+60 | t+330 | hồi+60; tăng total PSI giữa t+60→t+330 (s); Booking usage_usec tăng t+60→t+330 (s CPU); nr_throttled tăng')
for cell in dict.fromkeys(c['o'] for c in TC['cap_ca']):
    if cell not in rows: continue
    for phia in ('cu', 'moi'):
        for oid, pr in rows[cell].get(phia, []):
            ps = [psi(pr.get(ph, {})) for ph in ('t-240', 't+60', 't+330', 'hoi+60')]
            a60 = ' | '.join('-' if p is None else f'{p[1]:5.1f}' for p in ps)
            dt = (ps[2][2] - ps[1][2]) / 1e6 if ps[1] and ps[2] else None
            cg = [pr.get(ph, {}).get('cgroup_booking') for ph in ('t+60', 't+330')]
            du = (cg[1]['usage_usec'] - cg[0]['usage_usec']) / 1e6 if all(isinstance(x, dict) for x in cg) else None
            th = (cg[1]['nr_throttled'] - cg[0]['nr_throttled']) if all(isinstance(x, dict) for x in cg) else None
            print(f'{cell:22s}; {phia:3s}; {oid[:8]}; {a60}; {dt if dt is None else round(dt, 1)}; {du if du is None else round(du, 1)}; {th}')
