# -*- coding: utf-8 -*-
"""Ghi sổ biến thể vai trò CHỌN trên tập dev bản 2 — lượt 3 (13/11, TRƯỚC khi chạy lô trên exp-obs).

Lý do duy nhất của lượt 3: sửa lỗi phân loại cạnh trong H1 (phản biện T-064 lượt 1, điểm R1). Mã cũ gán loại `http`
cho mọi cạnh service → service lấy từ `m1.span.mau_canh`, gộp cả mẫu PRODUCER → CONSUMER. Mã mới tách mẫu theo loại span
(CLIENT → SERVER = http; PRODUCER → CONSUMER = message; khác = khong_ro) TRƯỚC khi chấm. Không thêm ý tưởng mới.

KHAI: lượt 3 chạy SAU khi đã xem kết quả lượt 1 và 2 trên cùng tập chọn. Các bản dưới đây là chạy lại nguyên cấu hình
của bản cha trên mã đã sửa; không cấu hình nào được chọn theo điểm. Trước khi ghi sổ, ca 98ea5ba4 (thuộc tập chọn) đã được
chạy thử trên laptop với V028 mã mới và với `gop_loai_cu` để kiểm cài đặt (đã thấy: Payment → Booking tách thành http 72 và
message 144; thứ tự nút và các cạnh có cờ không đổi ở ca này; `gop_loai_cu` cho lại đúng danh sách cạnh lượt 2).
Dùng: <py ghim> -B results/T-064/kiem/ghi_so_chon_dev2_luot3.py   (chạy một lần; từ chối nếu đã ghi)"""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
ft._nap_module_thanh_phan()
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "chon_dev2_luot3"' in so: raise SystemExit('đã ghi lượt 3')


def cfg_cua(ma):
    return json.loads((R / 'bien-the' / ma / 'cau-hinh.json').read_text(encoding='utf-8'))


def cu(cfg):
    """Cùng cấu hình nhưng mọi thành phần H1 chạy với gop_loai_cu = true (tái lập hành vi mã cũ)."""
    out = json.loads(json.dumps(cfg))
    for tp in out['thanh_phan']:
        if tp['ma'].startswith('H1'):
            tp.setdefault('tham_so', {})['gop_loai_cu'] = True
    return out


SUA = 'chạy lại nguyên cấu hình của bản cha trên mã đã sửa R1 (tách loại cạnh trước khi chấm)'
moi = [
    ('V038-R1-H1c', 'V014-H1c', cfg_cua('V014-H1c'), SUA, 'chưa biết: tách mẫu có thể sinh cờ cạnh mới; nếu không thì như V014'),
    ('V039-R1-H1c+H8s1', 'V028-H1c+H8s1', cfg_cua('V028-H1c+H8s1'), SUA, 'chưa biết; nếu không có cờ cạnh mới thì như V028'),
    ('V040-R1-H1c+H7c+H8s1', 'V015-H1c+H7c+H8s1', cfg_cua('V015-H1c+H7c+H8s1'), SUA, 'chưa biết; nếu không có cờ cạnh mới thì như V015'),
    ('V041-R1-H1c+H5b+H8s1', 'V034-H1c+H5b+H8s1', cfg_cua('V034-H1c+H5b+H8s1'), SUA, 'chưa biết; nếu không có cờ cạnh mới thì như V034'),
    ('V042-R1-H1c+H5b+H7c+H8s1', 'V033-H1c+H5b+H7c+H8s1', cfg_cua('V033-H1c+H5b+H7c+H8s1'), SUA, 'chưa biết; nếu không có cờ cạnh mới thì như V033'),
    ('V043-R1-H1a', 'V009-H1a', cfg_cua('V009-H1a'), SUA, 'chưa biết; lượt 1 H1a bị bỏ vì AC@1 giảm'),
    ('V044-R1-H1b', 'V010-H1b', cfg_cua('V010-H1b'), SUA, 'chưa biết; lượt 1 H1b bị bỏ vì AC@1 giảm'),
    ('V045-R1-GOP-H1cr', 'V031-GOP-H1cr', cfg_cua('V031-GOP-H1cr'), SUA, 'chưa biết; nếu không có cờ cạnh mới thì như V031'),
    ('V046-KC-V028', 'V028-H1c+H8s1', cu(cfg_cua('V028-H1c+H8s1')),
     'đối chứng mã nguồn: cấu hình V028 với gop_loai_cu trên mã lượt 3',
     'trùng đầu ra V028 lượt 2 ngoài variant, extra.m1_ft.{ban,ma_nguon_sha256,cau_hinh_sha256} và khóa chú thích mới'),
    ('V047-KC-V002', 'V002-H8s1', cfg_cua('V002-H8s1'), 'đối chứng mã nguồn: bản không có H1, cùng cấu hình V002 trên mã lượt 3',
     'trùng đầu ra V002 lượt 1 ngoài variant và extra.m1_ft.{ban,ma_nguon_sha256}'),
]
src_sha = ft.sha_ma_nguon(); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); dong = []
for ma, cha, cfg, ly, kv in moi:
    d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=False)
    (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    dong.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': cfg['thanh_phan'], 'ly_do_ky_thuat': ly, 'ky_vong': kv,
                 'vai_tro': 'chon_dev2_luot3', 'thiet_ke_sau_khi_xem_tap_chon': True, 'sua_loi': 'REVIEW luot 1 R1',
                 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha})
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print('ghi', len(dong), 'bản; ma_nguon', src_sha, now)
