# -*- coding: utf-8 -*-
"""Ghi sổ biến thể V005–V007 (trước khi chạy/chấm)."""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
H7 = {'ma': 'H7-tai'}; H8 = {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}; H6 = {'ma': 'H6a-bo-trace-nen'}
BT = [('V005-H7', 'P7', [H7], 'H7: bỏ kênh workload tăng tương ứng lưu lượng vào (điểm vào = nơi có nhiều span gốc SERVER nhất; τ = 0,2, κ = 1,5) + kênh lỗi thành tỷ lệ 5xx/tổng (SLI lỗi là tỷ lệ)', 'Ca FLASH bớt cờ workload/error; ca lỗi giữ hạng'),
      ('V006-H7+H8s1', 'P7', [H7, H8], 'Tổ hợp H7 + H8-san: ca FLASH còn cờ thao tác nền nhỏ (payment) mà H7 không xử lý', 'K giảm thêm so với V005'),
      ('V007-H6a+H7+H8s1', 'P7', [H6, H7, H8], 'Tổ hợp ba thành phần cài được trên dữ liệu cũ', 'Như V006')]
src_sha = ft.sha_ma_nguon()
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8') as f:
    for ma, cha, tp, ly, kv in BT:
        d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=True)
        cfg = {'thanh_phan': tp}; (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        f.write(json.dumps({'loai': 'truoc_cham', 'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'ma': ma, 'cha': cha, 'thay_doi': tp,
                            'ly_do_ky_thuat': ly, 'ky_vong': kv, 'vai_tro': 'kiem_cai_dat_9_ca_T062 (không dùng để chọn; tập chọn = dev bản 2)',
                            'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha}, ensure_ascii=False) + '\n')
print('ghi', len(BT), 'ma_nguon', src_sha[:12])
