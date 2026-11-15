# -*- coding: utf-8 -*-
"""Phiên C — ghi sổ biến thể H8-adapter, H8-log (T-064 H8), TRƯỚC khi chạy lô trên exp-obs.

KHAI:
- Thiết kế sau khi đã xem kết quả lượt 1–3 trên tập chọn (như mọi bản từ V009).
- H8-adapter thiết kế sau khi xem gói metric của `thuong01` (ca chạy thử 11/11, không thuộc tập chọn/không hồi quy) và
  đếm trên 37 gói: 22 ca của hai tập không có metric logic nào > 1 định danh (`phien-c/h8-adapter/dem-chuoi-trung.json`).
- H8-log thiết kế sau khi đếm log nghiệp vụ theo ca × service trên 22 ca (`phien-c/h8-log/dem-log-nghiep-vu.json`) và
  bảng chéo severity × outcome (`cheo-severity-outcome-*.json`). Người làm biết mã ca ↔ ô (sổ `sau_cham`), nên đã thấy, ví
  dụ, event-service chỉ có log (FAILED) ở hai ca HTTP5-EVENT; payment không có log SUCCESS ở A ở một ca. Định nghĩa kênh
  theo ngữ nghĩa B16 (FAILED ∪ UNKNOWN là kết cục lỗi; REJECTED, RETRY không), không chỉnh theo đáp án.
- Phép 1: thêm riêng vào P7. Phép 2: thêm vào V032-H5b (đề xuất tạm). Không tổ hợp khác.
- `thuong01`: kiểm cài đặt H8-adapter (P7 dựng lại phải ném lỗi adapter; V060 phải chạy được). Không chấm, không chọn.
Dùng: <py ghim> -B results/T-064/phien-c/ghi_so_h8.py   (chạy một lần; từ chối nếu đã ghi)"""
import datetime, json, pathlib, re, sys
sys.path.insert(0, 'src')
from m1_ft import chay as ft
ft._nap_module_thanh_phan()
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro": "h8_phien_c"' in so: raise SystemExit('đã ghi sổ H8 phiên C')
ma_max = max(int(m.group(1)) for m in re.finditer(r'"ma": "V(\d+)', so))
v032 = json.loads((R / 'bien-the' / 'V032-H5b' / 'cau-hinh.json').read_text(encoding='utf-8'))
TP = {'H8a': {'ma': 'H8-adapter'}, 'H8lk': {'ma': 'H8-log-kq'}, 'H8lc': {'ma': 'H8-log-chuoi'}}
LY = {'H8a': 'nối chuỗi metric của container tạo lại trong cửa sổ khi chỉ khác nhãn runtime và không chồng lấn mốc mẫu '
             'gốc (h8_adapter.py; nhu cầu kỹ thuật: P7 ERROR cả ca)',
      'H8lk': 'phân loại dòng lỗi của kênh log_loi theo outcome B16 (FAILED ∪ UNKNOWN) thay severity (h8_log.py)',
      'H8lc': 'hai kênh metric từ log nghiệp vụ: tỷ lệ kết cục lỗi (lớp lỗi), SUCCESS/s (lớp lưu lượng) (h8_log.py)'}
KV = {'H8a': 'trùng bản cha (ngoài extra.m1_ft) ở 22/22 ca vì 0 ca có tình huống; không phải bằng chứng hiệu quả',
      'H8lk': 'chưa biết; đầu vào (bảng chéo 22 ca, cheo-severity-outcome-22ca.json): ERROR trùng FAILED ở 10.424/10.424 dòng; chỉ 4.490 dòng UNKNOWN đổi lớp, ở 10 ca (9 ca T-062: payment N 225/A 225, riêng 00eaea92 A 660; 46aab4be: 5 dòng ở A). Ca khác phải trùng bản cha ngoài extra.m1_ft',
      'H8lc': 'chưa biết'}
moi = []
for k in ('H8a', 'H8lk', 'H8lc'):
    moi.append((f'{k}', 'P7', {'thanh_phan': [TP[k]]}, k))
    moi.append((f'V032+{k}', 'V032-H5b', {'thanh_phan': v032['thanh_phan'] + [TP[k]]}, k))
src_sha = ft.sha_ma_nguon(); now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
dong, ten = [], []
for n, (duoi, cha, cfg, k) in enumerate(moi, start=ma_max + 1):
    ma = f'V{n:03d}-{duoi}'
    p = R / 'bien-the' / ma; p.mkdir(parents=True, exist_ok=False)
    (p / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    dong.append({'loai': 'truoc_cham', 'utc': now, 'ma': ma, 'cha': cha, 'thay_doi': [TP[k]], 'ly_do_ky_thuat': LY[k],
                 'ky_vong': KV[k], 'vai_tro': 'h8_phien_c', 'phep': 1 if cha == 'P7' else 2,
                 'thiet_ke_sau_khi_xem_tap_chon': True, 'phien': 'C', 'cho_WHY': True,
                 'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': src_sha})
    ten.append(ma)
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print(json.dumps({'ghi': ten, 'ma_nguon_sha256': src_sha, 'utc': now}, ensure_ascii=False))
