# -*- coding: utf-8 -*-
"""Ghi sổ biến thể V001–V004 (trước khi chạy/chấm) và cấu hình từng bản."""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
BT = [('V001-H8s0', 'P7', [{'ma': 'H8-san', 'tham_so': {'delta_ms': 0}}], 'Đối chứng cài đặt của H8-san: δ = 0 phải cho bản ghi trùng P7 ngoài extra.m1_ft', 'Trùng P7 (thứ hạng, verdict, mọi khóa ngoài extra.m1_ft) trên 9 ca'),
      ('V002-H8s1', 'P7', [{'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}], 'H8: sàn độ lớn δ = 1 ms (hạt lập lịch CFS) cho đơn vị span; P7 cờ thao tác nền dịch ~0,1 ms (results/T-063/ca-nen/PHAN-TICH.md)', 'K giảm trên ca nền; 5 ca lỗi T-062 giữ hạng (độ dịch của lỗi tiêm ≥ 30 ms)'),
      ('V003-H6a', 'P7', [{'ma': 'H6a-bo-trace-nen'}], 'H6a: bỏ trace bảo trì thư viện (Hikari, Eureka, JGroups, health indicator) — gốc hợp lệ nhưng không phải hành vi ứng dụng (results/T-063/span-goc/PHAN-TICH.md)', 'Ít thay đổi: cờ ca nền nằm ở job ứng dụng/Keycloak, không ở trace bảo trì'),
      ('V004-H6a+H8s1', 'P7', [{'ma': 'H6a-bo-trace-nen'}, {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}], 'Tổ hợp H6a + H8-san (độc lập về cơ chế; kiểm tương tác)', 'Như V002')]
src_sha = ft.sha_ma_nguon()
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8') as f:
    for ma, cha, tp, ly, kv in BT:
        d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=True)
        cfg = {'thanh_phan': tp}; (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        f.write(json.dumps({'loai': 'truoc_cham', 'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'ma': ma, 'cha': cha, 'thay_doi': tp,
                            'ly_do_ky_thuat': ly, 'ky_vong': kv, 'vai_tro': 'kiem_cai_dat_9_ca_T062 (không dùng để chọn; tập chọn = dev bản 2)',
                            'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha}, ensure_ascii=False) + '\n')
print('ghi', len(BT), 'dòng; ma_nguon', src_sha[:12])
