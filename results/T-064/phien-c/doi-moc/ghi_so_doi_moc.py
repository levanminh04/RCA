# -*- coding: utf-8 -*-
"""Phiên C — ghi sổ biến thể cho kiểm độ nhạy mốc (T-064 SPEC bước 6, §7), TRƯỚC khi chạy lô trên exp-obs.

KHAI: đây là kiểm độ nhạy, KHÔNG phải biến thể để chọn (vai_tro `do_nhay_moc`). Cấu hình mỗi bản = nguyên cấu hình bản
cha; khác duy nhất là mốc t' = t + d do CLI `chay_ca.py --doi-t d` (đầu vào dựng lại từ gói ca, `m1_ft/doi_moc.py`).
Bản cha: P7 (bản khóa), V032-H5b (đề xuất tạm), V041-R1-H1c+H5b+H8s1 (thay thế có cạnh) — theo `ho-so-chon.md` và
`ban-xuat/chi-muc-ban.json`. d ∈ {−30, +30} (SPEC bước 6). Chạy trên 13 ca dev bản 2 và 9 ca T-062. Thiết kế sau khi đã
xem lượt 1–3 (đã khai).
Hai bản phụ ghi cùng lúc, trước khi chạy:
- KC (kiểm cài đặt): P7 với `--dung-lai-dau-vao --doi-t 0` — đường dựng lại phải cho method-input và đầu ra trùng byte P7.
- TG (thử giả, AGENTS 5.4 / brief §3): P7 với d = −300: cửa sổ [t−600, t), phía A = [t−300, t) hoàn toàn trước mốc. Kỳ vọng:
  ở ca có tiêm lỗi, đáp án mất hạng 1 (nếu không thì phép kiểm độ nhạy ±30 s không có sức phân biệt). Chỉ để kiểm sức
  phân biệt, không dùng chọn. Ghi trước khi thấy bất kỳ kết quả d ≠ 0 nào trên exp-obs (đã thấy trên laptop: P7 ca T-062
  a5539fba với d = ±30 khi thử cài đặt).
Gói metric bổ sung: dev bản 2 dùng gói xuất lại quanh t' (`out/pc-bo-sung-dt/d<d>/`, kiểm khớp gói gốc ở mốc chung);
T-062 dùng gói gốc quanh t với `--bo-sung-t-goc` (chỉ hợp lệ khi kênh live-down/live-ms rỗng; mã kiểm và từ chối nếu không).
Dùng: <py ghim> -B results/T-064/phien-c/doi-moc/ghi_so_doi_moc.py  (chạy một lần; từ chối nếu đã ghi)"""
import datetime, json, pathlib, re, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
ft._nap_module_thanh_phan()
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "do_nhay_moc"' in so: raise SystemExit('đã ghi sổ dời mốc')
ma_max = max(int(m.group(1)) for m in re.finditer(r'"ma": "V(\d+)', so))


def cfg_cua(ma):
    return json.loads((R / 'bien-the' / ma / 'cau-hinh.json').read_text(encoding='utf-8'))


RONG = {'thanh_phan': []}
CHA = [('P7', 'P7', RONG), ('V032', 'V032-H5b', cfg_cua('V032-H5b')),
       ('V041', 'V041-R1-H1c+H5b+H8s1', cfg_cua('V041-R1-H1c+H5b+H8s1'))]
moi = []
for d in (-30, 30):
    for ngan, cha, cfg in CHA:
        moi.append((f'DM-{ngan}-t{d:+d}', cha, cfg, d, 'do_nhay_moc',
                    f'kiểm độ nhạy mốc: nguyên cấu hình {cha}, t\' = t {d:+d} s (SPEC T-064 bước 6, §7)',
                    'chưa biết; so từng ô với cùng bản ở d = 0: đổi hạng, đổi kết luận ở ca không lỗi, cờ cạnh'))
moi.append(('KC-P7-dunglai-d0', 'P7', RONG, 0, 'kiem_cai_dat_doi_moc',
            'kiểm cài đặt đường dựng lại đầu vào (--dung-lai-dau-vao --doi-t 0)',
            'method-input trùng byte bản P7 đã lưu và đầu ra trùng SHA P7 ở 22/22 ca'))
moi.append(('TG-P7-t-300', 'P7', RONG, -300, 'thu_gia_doi_moc',
            'thử giả: phía A = [t−300, t) hoàn toàn trước mốc', 'ca lỗi mất đáp án ở hạng 1 (kiểm sức phân biệt)'))
src_sha = ft.sha_ma_nguon(); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
dong, ten = [], []
for k, (duoi, cha, cfg, d, vt, ly, kv) in enumerate(moi, start=ma_max + 1):
    ma = f'V{k:03d}-{duoi}'
    p = R / 'bien-the' / ma; p.mkdir(parents=True, exist_ok=False)
    (p / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    dong.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': cfg['thanh_phan'], 'doi_t': d,
                 'ly_do_ky_thuat': ly, 'ky_vong': kv, 'vai_tro': vt, 'khong_dung_de_chon': True,
                 'thiet_ke_sau_khi_xem_tap_chon': True, 'phien': 'C',
                 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha})
    ten.append(ma)
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print(json.dumps({'ghi': ten, 'ma_nguon_sha256': src_sha, 'utc': now}, ensure_ascii=False))
