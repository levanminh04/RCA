# -*- coding: utf-8 -*-
"""T-064 bước 2: src/m1_ft với cấu hình rỗng phải cho bản ghi trùng SHA với P7 trên 9 ca T-062 (hai lần chạy).
Đầu vào: method-input.json P7 của từng ca (không đọc nhãn). Dùng (môi trường ghim):
  PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B results/T-064/kiem/tuong_duong_p7.py"""
import hashlib, json, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
import argparse
ap = argparse.ArgumentParser(); ap.add_argument('--src', default='D:/RCA-flashticket/src')
ap.add_argument('--ca', default='D:/RCA-flashticket/results/T-062/ca', help='<ca>/<id>/outputs/<id>/ hoặc <ca>/<id>/')
ap.add_argument('--ids', nargs='*'); ap.add_argument('--ra', default='D:/RCA-flashticket/results/T-064/kiem/tuong-duong-p7.json')
a = ap.parse_args()
sys.path.insert(0, a.src)
from m1_ft import chay as ft
CA = Path(a.ca)
ids = a.ids or sorted(p.name for p in CA.iterdir() if p.is_dir() and not p.name.startswith('_'))
import platform
kq = {'ma_nguon_sha256': ft.sha_ma_nguon(), 'cau_hinh': {'thanh_phan': []}, 'ca': {},
      'nen': {'may': platform.machine(), 'python': sys.version.split()[0]}}
for i in ids:
    o = CA / i / 'outputs' / i if (CA / i / 'outputs').exists() else CA / i
    inputs = json.loads((o / 'method-input.json').read_text(encoding='utf-8'))
    p7 = [hashlib.sha256((o / f'method-output-{n}.json').read_bytes()).hexdigest() for n in (1, 2)]
    sh, giay = [], []
    for _ in (1, 2):
        t0 = time.monotonic(); rec = ft.chay(inputs, {'thanh_phan': []}); giay.append(round(time.monotonic() - t0, 2))
        sh.append(hashlib.sha256((ft.canonical(rec) + '\n').encode()).hexdigest())
    kq['ca'][i] = {'p7_sha256': p7, 'ft_sha256': sh, 'trung': sh[0] == sh[1] == p7[0] == p7[1], 'giay': giay}
    print(i, kq['ca'][i]['trung'], giay, flush=True)
kq['tat_ca_trung'] = all(v['trung'] for v in kq['ca'].values())
Path(a.ra).write_text(json.dumps(kq, indent=1) + '\n', encoding='utf-8')
print('TAT CA TRUNG:', kq['tat_ca_trung'])
