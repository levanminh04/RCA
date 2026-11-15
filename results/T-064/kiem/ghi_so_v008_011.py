# -*- coding: utf-8 -*-
"""Ghi sổ biến thể V008–V011 (trước khi chạy/chấm)."""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
H7c = {'ma': 'H7-tai', 'tham_so': {'log_theo_luu_luong': True}}; H8 = {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}
BT = [('V008-H7c+H8s1', 'V006-H7+H8s1', [H7c, H8], 'H7c: log lỗi theo tỷ lệ trên request cho thành phần tăng theo tải ngoài; V006 còn cờ log_loi Gateway/Ticket ở ca FLASH (results/T-064/cham/kiem-cai-dat-2.json, kenh_co 00eaea92)', 'FLASH → NO_INTRINSIC_ANOMALY; ca lỗi giữ hạng'),
      ('V009-H1a', 'P7', [{'ma': 'H1a-canh'}], 'H1a: cạnh dữ liệu từ span CLIENT DB/Redis + cạnh gọi (span.mau_canh), chấm E4 cùng thang, xếp hạng cạnh; nút giữ P7', 'Bảng cạnh: đúng cạnh hạng 1 ở EVENT-DB-LAT, NET-GW-BOOK; chiếu về nút có thể làm xấu ca nút (CPU-BOOK)'),
      ('V010-H1b', 'V009-H1a', [{'ma': 'H1b-canh-dinh-vi'}], 'H1b: định vị cạnh có cờ (phía gọi / phía đích / riêng cạnh / không ảnh hưởng) bằng bằng chứng riêng của hai đầu (op SERVER, metric không lan) và tầng nút bên gọi', 'Giữ đúng cạnh hạng 1 ở hai ô cạnh; ca nút không bị chiếu xấu'),
      ('V011-H1b+H7c+H8s1', 'V008-H7c+H8s1', [{'ma': 'H1b-canh-dinh-vi'}, H7c, H8], 'Tổ hợp H1b với H7c + H8 (H1b đọc tầng sau các thành phần khác)', 'Như V008 ở nút, như V010 ở cạnh')]
src_sha = ft.sha_ma_nguon()
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8') as f:
    for ma, cha, tp, ly, kv in BT:
        d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=True)
        cfg = {'thanh_phan': tp}; (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        f.write(json.dumps({'loai': 'truoc_cham', 'utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'ma': ma, 'cha': cha, 'thay_doi': tp,
                            'ly_do_ky_thuat': ly, 'ky_vong': kv, 'vai_tro': 'kiem_cai_dat_9_ca_T062 (không dùng để chọn; tập chọn = dev bản 2)',
                            'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha}, ensure_ascii=False) + '\n')
print('ghi', len(BT), 'ma_nguon', src_sha[:12])
