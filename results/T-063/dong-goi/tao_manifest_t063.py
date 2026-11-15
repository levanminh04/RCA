# -*- coding: utf-8 -*-
"""T-063 — manifest sha256 cho results/T-063/ (SPEC T-063 "Đầu ra"). Thư mục đã có SHA256SUMS/manifest riêng (thu2/,
thu3/thu/, thu3/thu-ngan/, ca-t062-bo-sung/, thu3/ qua thu3/manifest.json) chỉ ghi hash của file tổng đó; kiểm
từng thư mục con bằng `sha256sum -c` hoặc script tạo nó. Các file khác: hash từng file.
Dùng: py -3 -B results/T-063/dong-goi/tao_manifest_t063.py"""
import datetime as dt, hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parents[3]; T = R / 'results/T-063'
TONG = {'thu2/': 'thu2/SHA256SUMS', 'thu3/thu/': 'thu3/thu/SHA256SUMS', 'thu3/thu-ngan/': 'thu3/thu-ngan/SHA256SUMS',
        'ca-t062-bo-sung/': 'ca-t062-bo-sung/SHA256SUMS', 'thu3/': 'thu3/manifest.json'}
def sh(p): return hashlib.sha256(p.read_bytes()).hexdigest()
f, bo = {}, 0
for p in sorted(T.rglob('*')):
    if not p.is_file(): continue
    rel = p.relative_to(T).as_posix()
    if rel == 'manifest.json': continue
    if any(rel.startswith(k) and rel != v for k, v in TONG.items()):
        bo += 1; continue
    f[rel] = sh(p)
out = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'pham_vi': 'results/T-063 (T-063 quan sát, thu dev bản 2, thu bù 3)',
       'file_tong_thu_muc_con': {k: {'file': v, 'sha256': f.get(v) or sh(T / v)} for k, v in TONG.items()},
       'so_file_thuoc_thu_muc_con': bo, 'file': f}
(T / 'manifest.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(f), bo)
