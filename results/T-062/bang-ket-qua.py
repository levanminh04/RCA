#!/usr/bin/env python3
"""T-062: sinh bảng kết quả từng ô cho báo cáo sáng từ ket-qua/phat-lai/bang-cham.json (đã ghép đáp án sau khi băm).
Dùng: py -3 -B results/T-062/bang-ket-qua.py > results/T-062/bang-ket-qua.md"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
O = Path(__file__).resolve().parent
b = json.loads((O / 'ket-qua/phat-lai/bang-cham.json').read_text(encoding='utf-8'))
VT = {'nghi_nguon': 'nghi là nguồn', 'bi_keo_theo': 'bị kéo theo', 'binh_thuong': 'bình thường', 'thieu_du_lieu': 'thiếu dữ liệu'}
print('| Ca (mã mờ) | Ô lỗi | Đáp án T-059 (tập chấp nhận) | M1: kết luận | M1: hạng 1 | Hạng tốt nhất của đáp án | Vai trò M1 gán cho đáp án |')
print('|---|---|---|---|---|---|---|')
for c in b['ca']:
    kq = json.loads((O / 'ket-qua' / f"{c['ma']}.json").read_text(encoding='utf-8'))
    nut = {n['id']: n for n in kq['nut']}
    vt = ', '.join(f"{a}: {VT.get(nut[a]['vai_tro'], nut[a]['vai_tro'])}" if a in nut else f'{a}: không quan sát' for a in c['tap_chap_nhan']) or '—'
    hang = f"#{c['hang_tot_nhat']}" if c['hang_tot_nhat'] else ('—' if not c['tap_chap_nhan'] else 'không có hạng')
    print(f"| `{c['ma']}` | {c['o']} | {c['root']} ({', '.join(c['tap_chap_nhan']) or 'sức khỏe chưa xác nhận'}) | {c['ket_luan_m1']} ({c['trang_thai_m1']}) | {', '.join(c['hang_1_m1']) or '—'} | {hang} | {vt} |")
loi = [c for c in b['ca'] if c['tap_chap_nhan']]
k1 = sum(1 for c in loi if c['hang_tot_nhat'] == 1); k3 = sum(1 for c in loi if c['hang_tot_nhat'] and c['hang_tot_nhat'] <= 3)
ok = [c for c in b['ca'] if not c['tap_chap_nhan']]
fa = sum(1 for c in ok if c['ket_luan_m1'] == 'CAUSE_FOUND')
print()
print(f"Ca có lỗi: {len(loi)}; đáp án ở hạng 1: {k1}/{len(loi)}; trong top 3: {k3}/{len(loi)}. "
      f"Ca không tiêm lỗi mới (3 bình thường có lỗi nền tickets 500 + FLASH chưa xác nhận khỏe, có 429 ở Gateway): {len(ok)}; M1 kết luận CAUSE_FOUND: {fa}/{len(ok)} — "
      f"chưa phải tỷ lệ báo động giả trên ca khỏe (T-059: chưa có ngưỡng khỏe).")
print(f"Nguồn: `ket-qua/phat-lai/bang-cham.json` (sha256 manifest kết quả trước ghép `{b['sha256_manifest_ket_qua'][:16]}…`). n = 1 mỗi ô — chỉ là lượt phát triển đầu, không đủ để kết luận hiệu quả.")
