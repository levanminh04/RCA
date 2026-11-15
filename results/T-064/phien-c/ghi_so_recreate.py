# -*- coding: utf-8 -*-
"""Phiên C — ghi sổ (chỉ thêm) TRƯỚC khi chạy trên ca RECREATE-PAY `ebd5ef38` (T-063 thu bù 3, phiên B).
Không tạo mã biến thể mới: chạy lại nguyên cấu hình đã có trên mã `goc-11` (b0f79a4d…). Ca CHƯA vào tập chọn: hậu kiểm theo
điều kiện khai trước trượt httpcheck; "Sửa sau 2" chờ Minh (results/T-063/thu3/BAN-GIAO-B.md mục 7). Kết quả là phân xử cài
đặt/hiệu quả có điều kiện cho H8-adapter, một ca một lần thu; không dùng chọn cho tới khi Minh nhận ca."""
import datetime, json, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "phan_xu_h8a_recreate"' in so: raise SystemExit('đã ghi')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
x = {'loai': 'chay_them', 'utc': now, 'vai_tro': 'phan_xu_h8a_recreate', 'phien': 'C', 'ca': 'ebd5ef38',
     'o_phia_cham': 'RECREATE-PAY', 'tap_chap_nhan': ['payment-service'],
     'ban': {'V058-KC-P7-dunglai-d0': 'P7 dựng lại (ca không có outputs/) — kỳ vọng ERROR adapter',
             'V032-H5b': 'V032 dựng lại — kỳ vọng ERROR adapter',
             'V060-H8a': 'P7 + H8-adapter', 'V061-V032+H8a': 'V032 + H8-adapter'},
     'goi_bo_sung': '/opt/rca-m1ft/bo-sung-dev3/ebd5ef38/prometheus-bo-sung.json',
     'ky_vong': 'P7, V032 ERROR; V060, V061 chạy được; hạng của payment-service chưa biết',
     'trang_thai_ca': 'chưa vào tập chọn — chờ Minh nhận Sửa sau 2', 'ma_nguon_sha256': ft.sha_ma_nguon()}
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print(now, x['ma_nguon_sha256'])
