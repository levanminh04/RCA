# -*- coding: utf-8 -*-
"""Chạy nguyên `phan_loai.py` (không sửa) trên 13 ca dev bản 2 của đợt thu chính.
Chỉ thay nơi đọc gói (thư mục đã giải nén từ results/T-063/thu2/ca/<mã>.tgz: <thư mục>/<mã>/cases/<mã>/) và file ra.
Dùng: py -3 -B results/T-063/span-goc/phan_loai_dev2.py <thư mục giải nén> → results/T-063/span-goc/phan-loai-dev2.json"""
import sys
from pathlib import Path
goc = Path(sys.argv[1]).as_posix()
src = (Path(__file__).parent / 'phan_loai.py').read_text(encoding='utf-8')
a = "CA = R / 'results/T-062/ca'"; b = "'results/T-063/span-goc/phan-loai.json'"
assert src.count(a) == 1 and src.count(b) == 1
src = src.replace(a, f"CA = Path('{goc}')").replace(b, "'results/T-063/span-goc/phan-loai-dev2.json'")
sys.argv = [sys.argv[0]]
exec(compile(src, 'phan_loai.py', 'exec'))
