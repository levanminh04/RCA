# -*- coding: utf-8 -*-
"""Lô 5 (phiên 5, điều phối) — ghi sổ (chỉ thêm) TRƯỚC khi chạy: V066–V072 (WHY-96), V073–V081 (dời mốc thêm),
và dòng `chay_them` cho các bản hiện hành trên 6 ca thu bù 3 (WHY-95). Tạo cấu hình bien-the/<mã>/cau-hinh.json."""
import datetime, json, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "luot5' in so: raise SystemExit('đã ghi')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
src = ft.sha_ma_nguon()
H5 = {'ma': 'H5-liveness', 'tham_so': {'chet_im_giay': 60}}
S1 = {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}
H1C = {'ma': 'H1c-canh-chung'}; H8A = {'ma': 'H8-adapter'}; H3 = {'ma': 'H3-pool'}; H4 = {'ma': 'H4-queue'}
DC = {'ma': 'DC-bo-quan-he'}
moi = [
 ('V066-V041-boH1c', 'V041-R1-H1c+H5b+H8s1', [H5, S1], 'doi_chung_bo_quan_he_R6',
  'V041 bỏ H1c: tách riêng tác dụng H1c trong V041 (REVIEW-3 R6)'),
 ('V067-DC-V041-boQH-tron', 'V041-R1-H1c+H5b+H8s1', [H5, S1, DC], 'doi_chung_bo_quan_he_R6',
  'V041 bỏ toàn bộ quan hệ: bỏ H1c và tắt E1/E2/E5 (REVIEW-3 R6)'),
 ('V068-V061+H3', 'V061-V032+H8a', [H5, H8A, H3], 'luot5_to_hop', 'V070 bỏ H4'),
 ('V069-V061+H4', 'V061-V032+H8a', [H5, H8A, H4], 'luot5_to_hop', 'V070 bỏ H3'),
 ('V070-V061+H3+H4', 'V061-V032+H8a', [H5, H8A, H3, H4], 'luot5_to_hop', 'bản gộp quanh V032 cho ô thu bù 3'),
 ('V071-V041+H8a', 'V041-R1-H1c+H5b+H8s1', [H5, H1C, S1, H8A], 'luot5_to_hop', 'bản có cạnh + H8-adapter'),
 ('V072-V071+H3+H4', 'V071-V041+H8a', [H5, H1C, S1, H8A, H3, H4], 'luot5_to_hop', 'bản có cạnh + H8a + H3 + H4'),
]
cfg_cha = {'P7': [], 'V032-H5b': [H5], 'V041-R1-H1c+H5b+H8s1': [H5, H1C, S1]}
dm = []
n = 73
for d in (-60, -15, 15):
    for cha in ('P7', 'V032-H5b', 'V041-R1-H1c+H5b+H8s1'):
        ten = {'P7': 'P7', 'V032-H5b': 'V032', 'V041-R1-H1c+H5b+H8s1': 'V041'}[cha]
        dm.append((f'V0{n}-DM-{ten}-t{d:+d}', cha, cfg_cha[cha], d)); n += 1
rows = []
for ma, cha, tp, vt, ld in moi:
    cfg = {'thanh_phan': tp}
    p = R / 'bien-the' / ma; p.mkdir(parents=True, exist_ok=False)
    (p / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    rows.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': tp, 'ly_do_ky_thuat': ld + ' (WHY-96)',
                 'ky_vong': 'chưa biết', 'vai_tro': vt, 'thiet_ke_sau_khi_xem_tap_chon': True, 'phien': '5-dieu-phoi',
                 'tap': ['tap-chon-dev3-17', 'tap-dev3-19-do-nhay', 'khong-hoi-quy-T062'],
                 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src})
for ma, cha, tp, d in dm:
    cfg = {'thanh_phan': tp}
    p = R / 'bien-the' / ma; p.mkdir(parents=True, exist_ok=False)
    (p / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    rows.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': [{'doi_t_giay': d}],
                 'ly_do_ky_thuat': 'độ nhạy mốc, đường WHY-87 (WHY-96)', 'ky_vong': 'chưa biết',
                 'vai_tro': 'luot5_do_nhay_moc (không dùng chọn)', 'thiet_ke_sau_khi_xem_tap_chon': True,
                 'phien': '5-dieu-phoi', 'tap': ['dev2-13', 'T062-9', 'thu-bu-3 (6 ca)'],
                 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src})
hien_hanh = ['V001-H8s0', 'V002-H8s1', 'V003-H6a', 'V004-H6a+H8s1', 'V005-H7', 'V006-H7+H8s1', 'V007-H6a+H7+H8s1',
             'V008-H7c+H8s1', 'V012-H2', 'V013-H3', 'V016-H7c', 'V017-H4', 'V018-H5', 'V032-H5b', 'V038-R1-H1c',
             'V039-R1-H1c+H8s1', 'V040-R1-H1c+H7c+H8s1', 'V041-R1-H1c+H5b+H8s1', 'V042-R1-H1c+H5b+H7c+H8s1',
             'V043-R1-H1a', 'V044-R1-H1b', 'V045-R1-GOP-H1cr', 'V048-DC-P7-boQH', 'V049-DC-V002-boQH',
             'V050-DC-V032-boQH', 'V051-DC-V041-boQH', 'V060-H8a', 'V061-V032+H8a', 'V062-H8lk', 'V063-V032+H8lk',
             'V064-H8lc', 'V065-V032+H8lc']
for b in hien_hanh: assert (R / 'bien-the' / b / 'cau-hinh.json').exists(), b
rows.append({'loai': 'chay_them', 'utc': now, 'vai_tro': 'luot5_ca_thu_bu_3', 'phien': '5-dieu-phoi',
             'ca': ['86dea661', '659a9dfb1ab0', '1e5a3dc5', 'ebd5ef38', '7d1ee32f', '0a45b2e0'],
             'ban': hien_hanh + ['V058-KC-P7-dunglai-d0 (chỉ ebd5ef38: P7 dựng lại)'],
             'ghi_chu': 'chạy lại nguyên cấu hình đã có trên 6 ca thu bù 3, mã nguồn hiện hành; P7 của 5 ca dùng lại đầu ra '
                        'của phiên B (đã 2 lần trùng); bản H1 lượt 1–2 (lỗi R1) và họ GOP V019–V031 không chạy lại — '
                        'đại diện bởi bản R1 V038–V045. Các cặp đã có (V032, V060, V061 trên ebd5ef38) không chạy lại.',
             'ma_nguon_sha256': src})
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in rows: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print(now, src, len(rows), [r.get('ma') for r in rows])
