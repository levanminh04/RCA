# -*- coding: utf-8 -*-
"""Ghi sổ biến thể vai trò CHỌN trên tập dev bản 2 — lượt 2 (13/11 19:30Z, TRƯỚC khi chạy lô trên exp-obs).

KHAI: mọi bản lượt 2 được thiết kế SAU khi đã xem kết quả lượt 1 trên cùng tập chọn (cơ chế Q1–Q4 và Q5–Q6 ở
results/T-064/phan-tich/ghi-chu-co-che-dev2.md). Đây là thiết kế trên dữ liệu đã xem; kết quả lạc quan hơn lượt 1.
Trước khi ghi sổ, ba ca của tập chọn (46aab4be, 4af494a5, 83073ed1) đã được chạy thử trên laptop với H5b và H1c-bỏ-pool
để kiểm cài đặt (đã thấy: Payment lên nhóm đầu ở 46aab4be; cạnh event→event_db vẫn `phia_goi` do jvm-cpu ở 4af494a5).
Dùng: <py ghim> -B results/T-064/kiem/ghi_so_chon_dev2_luot2.py   (chạy một lần; từ chối nếu đã ghi)"""
import json, datetime, pathlib, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
ft._nap_module_thanh_phan()
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "chon_dev2_luot2"' in so: raise SystemExit('đã ghi lượt 2')
POOL = ['pool-pending', 'pool-used', 'pool-wait']
JVM = ['throttle', 'throttle-ratio', 'gc', 'heap', 'threads-blocked', 'jvm-cpu']
H = {'H1c': {'ma': 'H1c-canh-chung'}, 'H2': {'ma': 'H2-jvm'}, 'H3': {'ma': 'H3-pool'}, 'H4': {'ma': 'H4-queue'},
     'H5': {'ma': 'H5-liveness'}, 'H6a': {'ma': 'H6a-bo-trace-nen'}, 'H7c': {'ma': 'H7-tai', 'tham_so': {'log_theo_luu_luong': True}},
     'H8s1': {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}},
     'H1cp': {'ma': 'H1c-canh-chung', 'tham_so': {'bo_kenh_dinh_vi': POOL}},
     'H1cr': {'ma': 'H1c-canh-chung', 'tham_so': {'bo_kenh_dinh_vi': POOL + JVM}},
     'H5b': {'ma': 'H5-liveness', 'tham_so': {'chet_im_giay': 60}}}
GOP = ['H6a', 'H2', 'H3', 'H4', 'H5', 'H1c', 'H7c', 'H8s1']
moi = [
    ('V028-H1c+H8s1', 'V015-H1c+H7c+H8s1', ['H1c', 'H8s1'],
     'bản tối giản: lượt 1 cho H7c không tác dụng trên tập chọn (V008 = V002); tiêu chí §5(4) ưu tiên ít thành phần',
     'bằng V015 trên tập chọn; trên T-062 K có thể tăng ở ca FLASH (H7c từng giảm K ở đó)'),
    ('V029-H1c+H5+H7c+H8s1', 'V015-H1c+H7c+H8s1', ['H5', 'H1c', 'H7c', 'H8s1'],
     'thêm H5 (giữ theo luật 1 trên tập B ở lượt 1) vào ứng viên V015', 'tập A như V015; tập B: PAUSE-PAYMENT từ vắng lên có hạng'),
    ('V030-GOP-H1cp', 'V019-GOP', [x if x != 'H1c' else 'H1cp' for x in GOP],
     'Q2: kênh pool đo kết nối từ bên gọi tới đích, là tín hiệu của cạnh; không dùng làm bằng chứng riêng của bên gọi khi định vị (kênh vẫn vào thứ hạng nút)',
     'cạnh đúng trở lại ở REDIS-BOOK và NET-GW-BOOK (như V022); EVENT-DB-LAT còn mất vì jvm-cpu'),
    ('V031-GOP-H1cr', 'V030-GOP-H1cp', [x if x != 'H1c' else 'H1cr' for x in GOP],
     'Q2: thêm bỏ kênh JVM/cgroup bổ sung (H2) khỏi định vị — điều kiện thất bại đã ghi ở H2/H3: nạn nhân cũng tăng, chưa kiểm là không lan; định vị chỉ dùng span SERVER và kênh không lan của P7',
     'cạnh đúng top 3 ở 3/3 ô như V014; K vẫn như V019 (K do H2 thêm cờ nút, không do định vị)'),
    ('V032-H5b', 'V018-H5', ['H5b'],
     'Q3: thành phần không phản hồi đầu dò sống từ sau t tới hết cửa sổ (≥ 60 s = 4 bước dò, trước t phản hồi đủ) là quan sát trực tiếp, không cùng thang với điểm lệch s → đặt thành nhóm đầu thứ hạng. Thiết kế sau khi xem ca PAUSE-PAYMENT; chỉ có 1 ô loại này',
     'tập B: PAUSE-PAYMENT hạng 1; mọi ca khác như V018 (không thành phần nào chết im)'),
    ('V033-H1c+H5b+H7c+H8s1', 'V029-H1c+H5+H7c+H8s1', ['H5b', 'H1c', 'H7c', 'H8s1'], 'H5b trong ứng viên V015', 'tập A như V015; tập B: PAUSE-PAYMENT hạng 1'),
    ('V034-H1c+H5b+H8s1', 'V028-H1c+H8s1', ['H5b', 'H1c', 'H8s1'], 'H5b trong bản tối giản', 'tập A như V028; tập B: PAUSE-PAYMENT hạng 1'),
    ('V035-KC-V015', 'V015-H1c+H7c+H8s1', ['H1c', 'H7c', 'H8s1'], 'đối chứng mã nguồn: cùng cấu hình V015 trên mã lượt 2 (tham số mới mặc định tắt)', 'trùng đầu ra V015 lượt 1 ngoài extra.m1_ft.{ban,ma_nguon_sha256} và variant'),
    ('V036-KC-V018', 'V018-H5', ['H5'], 'đối chứng mã nguồn: cùng cấu hình V018', 'trùng V018 lượt 1 ngoài các khóa trên'),
    ('V037-KC-V019', 'V019-GOP', GOP, 'đối chứng mã nguồn: cùng cấu hình V019', 'trùng V019 lượt 1 ngoài các khóa trên'),
]
src_sha = ft.sha_ma_nguon(); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); dong = []
for ma, cha, ds, ly, kv in moi:
    cfg = {'thanh_phan': [H[x] for x in ds]}
    d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=False)
    (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    dong.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': cfg['thanh_phan'], 'ly_do_ky_thuat': ly, 'ky_vong': kv,
                 'vai_tro': 'chon_dev2_luot2', 'thiet_ke_sau_khi_xem_tap_chon': True,
                 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha})
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print('ghi', len(dong), 'bản; ma_nguon', src_sha)
