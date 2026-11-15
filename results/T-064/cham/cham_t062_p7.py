# -*- coding: utf-8 -*-
"""T-064 bước 1: chấm P7 trên 9 ca T-062 theo tiêu chí P7(a) (kỳ vọng dưới hoán vị đều trong nhóm hòa),
so với cách chấm "hạng nhóm" của results/T-062/e2.py. Đọc nhãn từ bảng phát lại đã băm của T-062 (sau khi chạy).
Dùng: py -3 -B results/T-064/cham/cham_t062_p7.py  → results/T-064/cham/t062-p7.json"""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R))
from src.m1_ft import cham
CA = R / 'results/T-062/ca'; BANG = R / 'results/T-062/ket-qua/phat-lai/bang-cham.json'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
bang = json.loads(BANG.read_text(encoding='utf-8'))
loi, khong_loi, chi_tiet = {}, {}, {}
for c in bang['ca']:
    f = CA / c['ma'] / 'outputs' / c['ma'] / 'method-output-1.json'
    rec = json.loads(f.read_text(encoding='utf-8'))
    d = {'o': c['o'], 'method_output_sha256': sha(f), 'verdict': rec.get('verdict'), 'status': rec.get('status')}
    if c['tap_chap_nhan']:
        r = cham.cham_ca_loi(rec, c['tap_chap_nhan']); loi[c['ma']] = r
        d.update(r, tap_chap_nhan=c['tap_chap_nhan'], hang_nhom_e2=c['hang_tot_nhat'])
    else:
        r = cham.cham_ca_khong_loi(rec); khong_loi[c['ma']] = r; d.update(r, nhom_hang_1=cham.nhom_hang_1(rec))
    chi_tiet[c['ma']] = d
out = {'nguon_bang_cham_sha256': sha(BANG), 'cham_py_sha256': sha(R / 'src/m1_ft/cham.py'),
       'tong_ca_loi': cham.tong_hop(loi), 'K': sum(v['k'] for v in khong_loi.values()), 'n_khong_loi': len(khong_loi),
       'ca': chi_tiet}
(R / 'results/T-064/cham/t062-p7.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for m, d in chi_tiet.items():
    print(m, d['o'], d.get('verdict'), 'nhom1=', d['nhom_hang_1'], 'p1=%.3f p3=%.3f E=%s e2=%s' % (d['p1'], d['p3'], d['hang_ky_vong'], d['hang_nhom_e2']) if 'p1' in d else f"k={d['k']}")
print('TONG', out['tong_ca_loi'], 'K=', out['K'], '/', out['n_khong_loi'])
