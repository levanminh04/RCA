# -*- coding: utf-8 -*-
"""Tạo cấu hình và ghi dòng `truoc_cham` cho lượt 4: đối chứng bỏ quan hệ (SPEC T-064 hàng 'Quan hệ có tác dụng tính toán không?').
Cặp cùng bản có/không quan hệ (DC-bo-quan-he tắt E1, E2, E5 của P7), thiết kế sau khi xem lượt 1-3 (khai).
Dùng: py -3 -B results/T-064/kiem/tao_luot4_doi_chung_bo_qh.py"""
import json, sys, datetime
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, 'D:/RCA-flashticket/src')
import hashlib
_SRC = Path('D:/RCA-flashticket/src')
def _canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
class ft:  # sao chép nguyên văn logic m1_ft.chay (môi trường cục bộ thiếu numpy/scipy; kết quả kiểm lại trên exp-obs)
    @staticmethod
    def sha_cau_hinh(c): return hashlib.sha256(_canon(c).encode()).hexdigest()
    @staticmethod
    def sha_ma_nguon():
        h = hashlib.sha256()
        for goc in ('m1', 'm1_ft'):
            for p in sorted((_SRC / goc).rglob('*.py')):
                if '__pycache__' in p.parts or 'tests' in p.parts: continue
                h.update(p.relative_to(_SRC).as_posix().encode() + b'\x00' + p.read_bytes() + b'\x00')
        return h.hexdigest()
R = Path('D:/RCA-flashticket/results/T-064')
DC = {'ma': 'DC-bo-quan-he'}
H5 = {'ma': 'H5-liveness', 'tham_so': {'chet_im_giay': 60}}; H8 = {'ma': 'H8-san', 'tham_so': {'delta_ms': 1}}; H1c = {'ma': 'H1c-canh-chung'}
BAN = [('V048-DC-P7-boQH', 'P7', [DC]),
       ('V049-DC-V002-boQH', 'V002-H8s1', [H8, DC]),
       ('V050-DC-V032-boQH', 'V032-H5b', [H5, DC]),
       ('V051-DC-V041-boQH', 'V041-R1-H1c+H5b+H8s1', [H5, H1c, H8, DC])]
so = R / 'so-bien-the.jsonl'; utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
with so.open('a', encoding='utf-8', newline='\n') as f:
    for ma, cha, tp in BAN:
        cfg = {'thanh_phan': tp}; d = R / 'bien-the' / ma; d.mkdir(parents=True, exist_ok=True)
        (d / 'cau-hinh.json').write_text(json.dumps(cfg, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        f.write(json.dumps({'loai': 'truoc_cham', 'utc': utc, 'ma': ma, 'cha': cha, 'thay_doi': [{'ma': 'DC-bo-quan-he', 'tham_so': {'bat_tat': {'E1': 'tat', 'E2': 'tat', 'E5': False}}}],
            'ly_do_ky_thuat': 'đối chứng bỏ quan hệ: cùng bản cha, chỉ tắt E1/E2/E5 của P7; so từng ô với bản cha (SPEC T-064; R2 REVIEW lượt 1)',
            'ky_vong': 'chưa biết: nếu quan hệ có tác dụng thì AC/hạng ở ô có truyền dẫn xấu đi; nếu bằng nhau thì quan hệ không đóng góp trên tập này',
            'vai_tro': 'doi_chung_bo_quan_he_luot4', 'thiet_ke_sau_khi_xem_tap_chon': True,
            'cau_hinh_sha256': ft.sha_cau_hinh(cfg), 'ma_nguon_sha256': ft.sha_ma_nguon()}, ensure_ascii=False) + '\n')
print('ok', utc, ft.sha_ma_nguon())
