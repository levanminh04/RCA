# -*- coding: utf-8 -*-
"""Phiên C — kiểm lô trước khi chấm (SPEC T-064 "Kiểm đúng đắn"). Chỉ đọc đầu ra đã chép về repo.
Dùng: py -3 -B kiem_lo_phien_c.py <spec.json> <ra.json> <cặp đối chứng "A=B">...
- Mọi bản không phải đối chiếu d = 0: đủ ca, summary có `trung_sha` true, hai output cùng SHA.
- Cặp "A=B": so B với A sau khi bỏ `extra.m1_ft` và `variant` → danh sách ca trùng / khác (khóa khác ở mức ngoài cùng)."""
import hashlib, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket')
spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
dev = (R / 'results/T-064/kiem/ca-dev2-13.txt').read_text().split(); t62 = (R / 'results/T-064/kiem/ca-t062-9.txt').read_text().split()
IDS = {'dev2': dev, 't062': t62}
kq = {'ban': {}, 'doi_chung': {}}


def bo(rec):
    r = json.loads(json.dumps(rec)); (r.get('extra') or {}).pop('m1_ft', None); r.pop('variant', None); return r


for ten, mau in spec['ban'].items():
    if ten in ('P7', 'V032', 'V041'):
        continue
    x = {}
    for tap, ids in IDS.items():
        thieu, khong_trung, khong_ok, trung_mi = [], [], [], []
        for i in ids:
            o = R / mau[tap].format(id=i)
            s = o.parent / 'summary.json'
            if not s.exists():
                thieu.append(i); continue
            sm = json.loads(s.read_text(encoding='utf-8'))
            h = [hashlib.sha256((o.parent / f'method-output-{n}.json').read_bytes()).hexdigest() for n in (1, 2)]
            if not (sm['trung_sha'] and h[0] == h[1] == sm['output_sha256'][0]):
                khong_trung.append(i)
            if sm.get('status') != 'OK':
                khong_ok.append([i, sm.get('status')])
            if 'trung_method_input_goc' in (sm.get('moc') or {}):
                trung_mi.append(sm['moc']['trung_method_input_goc'])
        x[tap] = {'thieu': thieu, 'khong_trung_sha': khong_trung, 'status_khac_OK': khong_ok,
                  'trung_method_input_goc': [sum(trung_mi), len(trung_mi)] if trung_mi else None}
    kq['ban'][ten] = x
for cap in sys.argv[3:]:
    a, b = cap.split('=')
    y = {}
    for tap, ids in IDS.items():
        trung, khac, thieu = [], {}, []
        for i in ids:
            fa, fb = R / spec['ban'][a][tap].format(id=i), R / spec['ban'][b][tap].format(id=i)
            if not (fa.exists() and fb.exists()):
                thieu.append(i); continue
            ra, rb = json.loads(fa.read_text(encoding='utf-8')), json.loads(fb.read_text(encoding='utf-8'))
            byte = hashlib.sha256(fa.read_bytes()).hexdigest() == hashlib.sha256(fb.read_bytes()).hexdigest()
            ra2, rb2 = bo(ra), bo(rb)
            if json.dumps(ra2, sort_keys=True) == json.dumps(rb2, sort_keys=True):
                trung.append(i + (' (byte)' if byte else ''))
            else:
                khac[i] = sorted(k for k in set(ra2) | set(rb2) if json.dumps(ra2.get(k), sort_keys=True) != json.dumps(rb2.get(k), sort_keys=True))
        y[tap] = {'trung': trung, 'khac': khac, 'thieu': thieu}
    kq['doi_chung'][cap] = y
Path(sys.argv[2]).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for t, v in kq['ban'].items():
    print(t, {tap: (len(x['thieu']), len(x['khong_trung_sha']), x['status_khac_OK'][:3], x['trung_method_input_goc']) for tap, x in v.items()})
for c, v in kq['doi_chung'].items():
    print(c, {tap: (len(x['trung']), sum('(byte)' in s for s in x['trung']), x['khac'], len(x['thieu'])) for tap, x in v.items()})
