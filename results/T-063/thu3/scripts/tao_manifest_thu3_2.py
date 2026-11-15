# -*- coding: utf-8 -*-
"""T-063 thu3 — manifest-2 (REVIEW-4 R7: sau dòng Minh nhận hai sửa nối vào dieu-kien-xac-nhan-3.md; giữ manifest.json cũ) cho results/T-063/thu3/ (trừ thu/ và thu-ngan/ đã có SHA256SUMS riêng, và chính manifest).
Dùng: py -3 -B results/T-063/thu3/scripts/tao_manifest_thu3_2.py"""
import datetime as dt, hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parents[4]; T = R / 'results/T-063/thu3'
f = {}
for p in sorted(T.rglob('*')):
    rel = p.relative_to(T).as_posix()
    if p.is_file() and not rel.startswith(('thu/', 'thu-ngan/')) and rel != 'manifest-2.json':
        f[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
sub = {d: hashlib.sha256((T / d / 'SHA256SUMS').read_bytes()).hexdigest() for d in ('thu', 'thu-ngan') if (T / d / 'SHA256SUMS').exists()}
ngoai = {k: hashlib.sha256((R / k).read_bytes()).hexdigest() for k in ('results/T-063/dong-bang/dong-bang-3.json', 'results/T-063/dong-bang/dong-bang-3-truoc-chot.json')}
(T / 'manifest-2.json').write_text(json.dumps({'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'pham_vi': 'results/T-063/thu3 (thu bù 3)',
    'file': f, 'SHA256SUMS_thu_muc_con': sub, 'ngoai_thu3': ngoai}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(f), sub)
