# -*- coding: utf-8 -*-
"""Ghi sổ biến thể V014–V015 (trước khi chạy/chấm). Thiết kế H1c sau kiểm cài đặt V009–V011 trên 9 ca T-062 (WHY-82)."""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
H7c = {'ma': 'H7-tai', 'tham_so': {'log_theo_luu_luong': True}}; H8 = {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}
BT = [('V014-H1c', 'V010-H1b', [{'ma': 'H1c-canh-chung'}], 'H1c: hạng cạnh trong danh sách chung nút + cạnh (WHY-82) — sửa điều kiện thất bại của H1a/H1b (cạnh yếu đứng hạng 1 danh sách riêng, chiếu lên ngang gốc; results/T-064/cham/kiem-cai-dat-3.json)', 'AC@1 như P7; đúng cạnh top 3 ở 2/2 ô cạnh'),
      ('V015-H1c+H7c+H8s1', 'V011-H1b+H7c+H8s1', [{'ma': 'H1c-canh-chung'}, H7c, H8], 'Tổ hợp H1c với H7c + H8 (V011 bị cạnh event→event_db ở CPU-BOOK kéo xấu)', 'K = 0, AC@1 = 5, cạnh top 3 2/2')]
src_sha = ft.sha_ma_nguon()
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8') as f:
    for ma, cha, tp, ly, kv in BT:
        d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=True)
        cfg = {'thanh_phan': tp}; (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        f.write(json.dumps({'loai': 'truoc_cham', 'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'ma': ma, 'cha': cha, 'thay_doi': tp,
                            'ly_do_ky_thuat': ly, 'ky_vong': kv, 'vai_tro': 'kiem_cai_dat_9_ca_T062 (không dùng để chọn; tập chọn = dev bản 2)',
                            'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha}, ensure_ascii=False) + '\n')
print('ghi', len(BT), 'ma_nguon', src_sha[:12])
