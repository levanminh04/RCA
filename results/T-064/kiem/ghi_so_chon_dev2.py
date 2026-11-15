# -*- coding: utf-8 -*-
"""Ghi sổ biến thể vai trò CHỌN trên tập dev bản 2 — lượt 1 (trước khi có dữ liệu đợt thu chính; ghi 13/11 ~08:30Z).
Theo results/T-064/tieu-chi-chon.md §4: (i) thêm riêng từng thành phần vào P7; (ii) bỏ từng thành phần khỏi bản gộp.
Tổ hợp đã có (V004, V006–V008, V011, V015) chạy lại trên tập chọn cùng mã nguồn. Mọi bản cùng mã nguồn (ma_nguon dưới).
Dùng: <py ghim> -B results/T-064/kiem/ghi_so_chon_dev2.py   (chạy một lần; từ chối nếu đã ghi)"""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
ft._nap_module_thanh_phan()
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "chon_dev2_luot1"' in so: raise SystemExit('đã ghi lượt 1')
H = {'H1a': {'ma': 'H1a-canh'}, 'H1b': {'ma': 'H1b-canh-dinh-vi'}, 'H1c': {'ma': 'H1c-canh-chung'}, 'H2': {'ma': 'H2-jvm'},
     'H3': {'ma': 'H3-pool'}, 'H4': {'ma': 'H4-queue'}, 'H5': {'ma': 'H5-liveness'}, 'H6a': {'ma': 'H6a-bo-trace-nen'},
     'H7': {'ma': 'H7-tai'}, 'H7c': {'ma': 'H7-tai', 'tham_so': {'log_theo_luu_luong': True}},
     'H8s0': {'ma': 'H8-san', 'tham_so': {'delta_ms': 0}}, 'H8s1': {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}}
GOP = ['H6a', 'H2', 'H3', 'H4', 'H5', 'H1c', 'H7c', 'H8s1']  # thứ tự tương đối giữ như V015 (H1c, H7c, H8s1)
cu = {  # bản đã có: dùng lại cấu hình trên đĩa (hash kiểm dưới)
    'V001-H8s0': ('P7', 'đối chứng cài đặt: δ = 0 phải trùng P7 ngoài extra.m1_ft', 'trùng P7 mọi ca'),
    'V002-H8s1': ('P7', 'H8 sàn 1 ms cho đơn vị span (cờ thao tác nền ~0,1 ms)', 'K giảm; ô lỗi giữ hạng (lỗi ≥ 30 ms)'),
    'V003-H6a': ('P7', 'H6a bỏ trace thao tác nền đã xác định', 'K giảm hoặc giữ; ô lỗi giữ hạng'),
    'V004-H6a+H8s1': ('V003-H6a', 'H6a cùng H8s1', 'K ≤ V002, V003'),
    'V005-H7': ('P7', 'H7 chuẩn hóa theo lưu lượng (FLASH)', 'K FLASH giảm; ô lỗi giữ'),
    'V006-H7+H8s1': ('V005-H7', 'H7 cùng H8s1', 'K ≤ V005'),
    'V007-H6a+H7+H8s1': ('V006-H7+H8s1', 'H6a + H7 + H8s1', 'K ≤ V006'),
    'V008-H7c+H8s1': ('V006-H7+H8s1', 'H7c (log theo lưu lượng) + H8s1', 'K ≤ V006'),
    'V009-H1a': ('P7', 'H1a cạnh dữ liệu/gọi/message chấm E4', 'đúng cạnh top 3 ở ô cạnh'),
    'V010-H1b': ('P7', 'H1b định vị cạnh theo phía gọi/được gọi', 'đúng cạnh top 3 ở ô cạnh'),
    'V011-H1b+H7c+H8s1': ('V010-H1b', 'H1b + H7c + H8s1', 'cạnh như V010, K như V008'),
    'V012-H2': ('P7', 'H2 kênh JVM (GC/heap/thread) tách áp lực CPU khỏi lan truyền', 'CPU-BOOK giữ hoặc tốt lên'),
    'V013-H3': ('P7', 'H3 kênh pool kết nối', 'EVENT-DB-LAT/CPU-BOOK giữ hoặc tốt lên'),
    'V014-H1c': ('P7', 'H1c danh sách chung nút + cạnh (WHY-82)', 'AC@1 không giảm; cạnh top 3'),
    'V015-H1c+H7c+H8s1': ('V014-H1c', 'H1c + H7c + H8s1', 'K giảm, cạnh top 3'),
}
moi = [
    ('V016-H7c', 'P7', ['H7c'], 'H7c riêng (thêm riêng vào P7 theo §4; trước đây chỉ thử cùng H8s1)', 'K FLASH giảm; ô lỗi giữ'),
    ('V017-H4', 'P7', ['H4'], 'H4 kênh queue ready/unacked/dlq theo consumer (TD-02). Ô consumer chậm đã loại (D2B); chỉ đo ảnh hưởng phụ', 'không đổi ô lỗi; K không tăng'),
    ('V018-H5', 'P7', ['H5'], 'H5 kênh sống/chết httpcheck (TD-04, bộ xuất bản 3) cho thành phần "chết im" (PAUSE-PAYMENT)', 'PAUSE-PAYMENT tốt lên; ô khác giữ'),
    ('V019-GOP', 'V015-H1c+H7c+H8s1', GOP, 'bản gộp mọi thành phần có cài (H1 dùng H1c theo WHY-82; H7 dùng H7c) — gốc cho phép bỏ từng thành phần (§4)', 'không xấu hơn từng phần; để so bỏ-một'),
] + [(f'V{20 + i:03d}-GOP-{x}', 'V019-GOP', [y for y in GOP if y != x], f'bỏ {x} khỏi bản gộp (§4 phép 2)', f'so với V019: đo đóng góp của {x}')
     for i, x in enumerate(GOP)]
src_sha = ft.sha_ma_nguon(); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); dong = []
for ma, (cha, ly, kv) in cu.items():
    cfg = json.loads((R / 'bien-the' / ma / 'cau-hinh.json').read_text(encoding='utf-8'))
    dong.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': cfg['thanh_phan'], 'ly_do_ky_thuat': ly, 'ky_vong': kv,
                 'vai_tro': 'chon_dev2_luot1', 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha})
for ma, cha, ds, ly, kv in moi:
    cfg = {'thanh_phan': [H[x] for x in ds]}
    d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=False)
    (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    dong.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': cfg['thanh_phan'], 'ly_do_ky_thuat': ly, 'ky_vong': kv,
                 'vai_tro': 'chon_dev2_luot1', 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha})
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print('ghi', len(dong), 'bản; ma_nguon', src_sha[:12])
