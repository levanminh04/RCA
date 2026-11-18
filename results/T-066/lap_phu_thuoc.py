# -*- coding: utf-8 -*-
"""T-066 bước 1: lập danh sách file bảo vệ (phần A của phu-thuoc.md).

Chỉ đọc. Mỗi file: đường dẫn nguồn, sha256 tính lại trên laptop, sha256 theo nguồn đối chiếu, nguồn đối chiếu.
Lệch nguồn đối chiếu thì in LỆCH và thoát mã 1 (luật toàn vẹn, mục 1).
Chạy: py -3 -I results/T-066/lap_phu_thuoc.py > results/T-066/bao-ve.tsv
"""
import hashlib
import json
import sys
import tarfile
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
RCA = Path('D:/RCA-flashticket')
ARC = Path('D:/RCA-archive')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def doc_ds(p, tien_to=''):
    out = {}
    for line in Path(p).read_text(encoding='utf-8').splitlines():
        h, f = line.split('  ', 1) if '  ' in line else line.split(' *', 1)
        out[tien_to + f.lstrip('*').lstrip('./')] = h
    return out


m3 = json.loads((RCA / 'results/T-064/manifest-3.json').read_text(encoding='utf-8'))
ds_m1 = doc_ds(ARC / 'hash-lists/exp-obs-m1ft-inputs.sha256')
ds_ca = doc_ds(ARC / 'hash-lists/exp-obs-cases.sha256')
thu2 = doc_ds(RCA / 'results/T-063/thu2/SHA256SUMS')
dong = []  # (nhóm, đường dẫn nguồn, sha256 tính lại, sha256 đối chiếu, nguồn đối chiếu)

# A1. Bản chụp mã goc-12 (mọi file; chay_ca.py import m1, m1_ft; m1 import p3)
for f, h in sorted(ds_m1.items()):
    if f.startswith('goc-12/'):
        p = ARC / 'exp-obs/m1ft-inputs' / f
        dong.append(('A1-ma-goc-12', str(p), sha(p), h, 'D:/RCA-archive/hash-lists/exp-obs-m1ft-inputs.sha256'))
# A1b. Mã src/m1_ft của repo RCA được manifest-3 ghim (đối chiếu chéo với goc-12)
for f, h in sorted(m3['src_m1_ft'].items()):
    dong.append(('A1b-src-m1_ft-manifest3', str(RCA / f), sha(RCA / f), h, 'results/T-064/manifest-3.json#/src_m1_ft'))
# A2. Cấu hình V082
for f in ('cau-hinh-de-xuat.json', 'bien-the/V082-V066+H8a/cau-hinh.json', 'manifest-3.json'):
    p = RCA / 'results/T-064' / f
    ref = m3['file'].get(f)
    dong.append(('A2-cau-hinh-V082', str(p), sha(p), ref or '-', 'results/T-064/manifest-3.json#/file' if ref else 'git (repo RCA, đã commit)'))
# A3. Gói ca
for f, h in sorted(ds_ca.items()):
    if f.startswith('ebd5ef38/'):
        p = ARC / 'exp-obs/cases' / f
        dong.append(('A3-goi-ca-ebd5ef38', str(p), sha(p), h, 'D:/RCA-archive/hash-lists/exp-obs-cases.sha256'))
p = RCA / 'results/T-063/thu2/ca/46aab4be.tgz'
dong.append(('A3-goi-ca-46aab4be', str(p), sha(p), thu2['ca/46aab4be.tgz'], 'results/T-063/thu2/SHA256SUMS'))
with tarfile.open(p) as t:
    for mem in sorted(t.getmembers(), key=lambda m: m.name):
        if mem.isfile() and (mem.name.startswith('cases/') or mem.name.endswith('method-input.json')):
            h = hashlib.sha256(t.extractfile(mem).read()).hexdigest()
            dong.append(('A3-goi-ca-46aab4be', f'{p}!{mem.name}', h, '(trong tgz)', 'results/T-063/thu2/SHA256SUMS (qua tgz)'))
# A4. Gói bổ sung và gói R9
for f, h in sorted(ds_m1.items()):
    if f.startswith(('bo-sung-dev2/46aab4be/', 'bo-sung-dev3/ebd5ef38/', 'out/r9-bo-sung/')):
        p = ARC / 'exp-obs/m1ft-inputs' / f
        dong.append(('A4-goi-bo-sung-R9', str(p), sha(p), h, 'D:/RCA-archive/hash-lists/exp-obs-m1ft-inputs.sha256'))
# A5. Cấu hình P7 và ghim của runner P7 (bản trên laptop; bản trên máy đã so bước 0)
for f in ('m1-p7-config.json', 'm1-source-pins.json', 'flashticket-inventory-source.json', 'stage-m1.py', 'run-m1.py', 'safe-export.py'):
    p = RCA / 'results/T-058/dem-2026-11-10' / f
    dong.append(('A5-p7-runner', str(p), sha(p), '-', 'git (repo RCA, results/T-058 đã commit)'))
# A6. Đầu ra chuẩn của phép hồi quy (manifest-3)
for f in ('kiem/nhan-luot5/l5/dev2/d0/V082-V066+H8a/46aab4be/method-output-1.json',
          'kiem/nhan-r9/r9/dev3/d0/V082-V066+H8a/ebd5ef38/method-output-1.json'):
    p = RCA / 'results/T-064' / f
    dong.append(('A6-chuan-hoi-quy', str(p), sha(p), m3['file'][f], 'results/T-064/manifest-3.json#/file'))

lech = [d for d in dong if d[3] not in ('-', '(trong tgz)') and d[2] != d[3]]
print('nhom\tduong_dan_nguon\tsha256_tinh_lai\tsha256_doi_chieu\tnguon_doi_chieu')
for d in dong:
    print('\t'.join(d))
print(f'# tong {len(dong)} dong; lech {len(lech)}', file=sys.stderr)
for d in lech:
    print('LỆCH', d, file=sys.stderr)
sys.exit(1 if lech else 0)
