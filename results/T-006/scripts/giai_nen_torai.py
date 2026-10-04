r"""T-006 bước 0.3: giải nén đúng hai thư mục torai-OB/ và torai-SS/ từ dl/torai-data.zip vào data/.

Không giải nén, không đọc nội dung mục nào khác (torai-TT chứa ca khóa). Chỉ đọc danh sách tên mục để lọc.
Chạy từ D:\RCA-ext: py -3 <repo>/results/T-006/scripts/giai_nen_torai.py
In: số file, tổng byte mỗi thư mục, số ca (thư mục chứa inject_time.txt), CRC do zipfile tự kiểm khi giải nén.
"""
import zipfile
from collections import Counter

PREFIXES = ("torai-OB/", "torai-SS/")
z = zipfile.ZipFile("dl/torai-data.zip")
n_file, n_byte, n_case = Counter(), Counter(), Counter()
for info in z.infolist():
    name = info.filename
    if not name.startswith(PREFIXES) or name.endswith("/"):
        continue
    top = name.split("/")[0]
    z.extract(info, "data")  # zipfile kiểm CRC-32 khi đọc; sai thì báo lỗi BadZipFile
    n_file[top] += 1
    n_byte[top] += info.file_size
    if name.endswith("inject_time.txt"):
        n_case[top] += 1
for top in sorted(n_file):
    print(f"{top}: {n_file[top]} file, {n_byte[top]} B, {n_case[top]} ca")
