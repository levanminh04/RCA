# -*- coding: utf-8 -*-
"""T-064 — manifest sha256 cho results/T-064/ (mọi file trừ chính manifest). Ghi results/T-064/manifest.json; không ghi đè
bản đã có (bản sau đặt tên manifest-<k>.json). Kèm hash các file ngoài results/T-064 mà kết luận dựa vào.
Dùng: py -3 -B results/T-064/kiem/tao_manifest_t064.py"""
import datetime as dt, hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parents[3]; T = R / 'results/T-064'
ra = T / 'manifest.json'; k = 2
while ra.exists():
    ra = T / f'manifest-{k}.json'; k += 1
def sh(p): return hashlib.sha256(p.read_bytes()).hexdigest()
f = {}
for p in sorted(T.rglob('*')):
    if p.is_file():
        rel = p.relative_to(T).as_posix()
        if rel != ra.relative_to(T).as_posix():  # bản manifest trước được ghim như một file
            f[rel] = sh(p)
NGOAI = ['docs/DECISIONS.md', 'docs/WHY.md', 'tasks/T-064-m1-flashticket/SPEC.md', 'results/T-062/ket-qua/phat-lai/bang-cham.json',
         'results/T-059/danh-muc-loi.json', 'results/T-063/manifest-2.json', 'src/m1_ft/cham.py', 'src/m1_ft/chay.py', 'src/m1_ft/chay_ca.py']
src = {p.relative_to(R).as_posix(): sh(p) for p in sorted((R / 'src/m1_ft').rglob('*.py'))}
out = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'pham_vi': 'results/T-064 (M1-FlashTicket: chọn bản, lô 1–5, V082)',
       'so_file': len(f), 'file': f, 'ngoai_T064': {x: sh(R / x) for x in NGOAI}, 'src_m1_ft': src}
ra.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(ra.relative_to(R).as_posix(), len(f))
