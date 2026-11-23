# -*- coding: utf-8 -*-
"""T-069 bước 7 — log/trace/metric của bản ghim có khác bản 3 không? So độ phủ đầu vào M1 giữa ca cũ và ca mới cùng ô (chỉ đọc đầu ra V082).
Dùng: T069_MOI="o:mã,..." py -3 -B results/T-069/so_do_phu.py > results/T-069/phan-tich/do-phu.txt
Mỗi cặp: số span, span gốc, span mồ côi; số kênh (chấm) hợp lệ; số cạnh quan sát; số dòng log theo service (N); nguồn coverage
có trạng thái khác OK; số kênh metric. Không dùng nhãn ngoài tên ô."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
R = 'D:/RCA-flashticket'; ban = 'V082-V066+H8a'
TC = json.load(open(f'{R}/results/T-069/tieu-chi.json', encoding='utf-8'))
moi = [x.split(':') for x in os.environ['T069_MOI'].split(',')]


def cu_path(ma):
    for base in (f'{R}/results/T-064/kiem/nhan-r9/r9', f'{R}/results/T-064/kiem/nhan-luot5/l5'):
        for g in ('dev2', 'dev3'):
            p = f'{base}/{g}/d0/{ban}/{ma}/method-output-1.json'
            if os.path.exists(p): return p


def tom(m):
    d = m['diagnostics']; sp = d.get('span', {}); cv = m.get('coverage', {})
    log = {e: v['N']['dong'] for e, v in (m['extra'].get('thong_ke_log') or {}).get('theo_thuc_the', {}).items()}
    return {'span': sp.get('so_span'), 'goc': sp.get('goc'), 'mo_coi': sp.get('mo_coi'), 'cham': d.get('so_cham_hop_le'),
            'canh': d.get('so_canh_quan_sat'), 'nguon_cv': len(cv), 'cv_khong_ok': sorted(k for k, v in cv.items() if isinstance(v, dict) and v.get('trang_thai') != 'OK'),
            'metric': len([k for k in cv if k.startswith('metric:')]), 'log': log}


dem = {}
print(f'{"ô":22s} {"cũ→mới":20s} {"span":>17s} {"gốc":>13s} {"mồ côi":>10s} {"kênh":>11s} {"cạnh":>7s} {"metric":>9s}  cv≠OK(cũ|mới)')
logs = []
for cp in TC['cap_ca']:
    o = cp['o']; k = dem.get(o, 0); dem[o] = k + 1
    cung = [m for oo, m in moi if oo == o]
    if k >= len(cung): continue
    pc, pm = cu_path(cp['cu']['ma']), f'{R}/results/T-069/dau-ra/dev3/d0/{ban}/{cung[k]}/method-output-1.json'
    if not pc or not os.path.exists(pm): continue
    a, b = tom(json.load(open(pc, encoding='utf-8'))), tom(json.load(open(pm, encoding='utf-8')))
    print(f'{o:22s} {cp["cu"]["ma"][:8]}→{cung[k]:10s} {a["span"]:>8}→{b["span"]:<8} {a["goc"]:>6}→{b["goc"]:<6} {a["mo_coi"]:>4}→{b["mo_coi"]:<5} {a["cham"]:>5}→{b["cham"]:<5} {a["canh"]:>3}→{b["canh"]:<3} {a["metric"]:>4}→{b["metric"]:<4}  {a["cv_khong_ok"]}|{b["cv_khong_ok"]}')
    logs.append((o, a['log'], b['log']))
print('\nDòng log trong cửa sổ N theo service (cũ→mới):')
ents = sorted({e for _, a, b in logs for e in list(a) + list(b)})
for o, a, b in logs:
    print(f'{o:22s} ' + ' '.join(f'{e[:10]}:{a.get(e, 0)}→{b.get(e, 0)}' for e in ents if a.get(e) or b.get(e)))
