# -*- coding: utf-8 -*-
"""Ghi sổ biến thể V012–V013 (trước khi chạy/chấm)."""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
BT = [('V012-H2', 'P7', [{'ma': 'H2-jvm'}], 'H2: kênh JVM/cgroup lớp tài nguyên (throttle, GC, heap, luồng blocked, CPU JVM) từ gói bổ sung; 9 ca cũ không có throttle', 'CPU-BOOK: thêm bằng chứng tự sinh ở Booking; có thể thêm cờ heap ở service khác'),
      ('V013-H3', 'P7', [{'ma': 'H3-pool'}], 'H3: kênh pool kết nối lớp tài nguyên (pending, used, wait)', 'EVENT-DB-LAT: thêm cờ pool Event; CPU-BOOK: cờ pool-wait cả nạn nhân (điều kiện thất bại đã ghi)')]
src_sha = ft.sha_ma_nguon()
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8') as f:
    for ma, cha, tp, ly, kv in BT:
        d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=True)
        cfg = {'thanh_phan': tp}; (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        f.write(json.dumps({'loai': 'truoc_cham', 'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'ma': ma, 'cha': cha, 'thay_doi': tp,
                            'ly_do_ky_thuat': ly, 'ky_vong': kv, 'vai_tro': 'kiem_cai_dat_9_ca_T062 (không dùng để chọn; tập chọn = dev bản 2)',
                            'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha,
                            'dau_vao_bo_sung': 'results/T-063/ca-t062-bo-sung/<id>/prometheus-bo-sung.json (SHA256SUMS)'}, ensure_ascii=False) + '\n')
print('ghi', len(BT), 'ma_nguon', src_sha[:12])
