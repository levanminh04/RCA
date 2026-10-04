r"""T-006 bước 0.4 (phụ): so mục lục (central directory) của zip Zenodo 13305663 với zip RE1 (Zenodo 14590730).

main.py RCAEval tải `--dataset online-boutique`/`re1-ob` từ Zenodo 13305663 (online-boutique.zip), còn SPEC tải RE1-OB
từ Zenodo 14590730. Script này chỉ cần phần đuôi zip 13305663 (tải bằng HTTP Range, 128 KB), đọc CRC-32 và kích
thước từng file, so với zip RE1 đã tải đủ. Không tải nội dung dữ liệu của 13305663.
Cách dùng: py -3 so_muc_luc_zip.py <đuôi zip 13305663> <tổng byte zip 13305663> <zip RE1 đầy đủ> <tiền tố cũ> <tiền tố mới>
"""
import struct
import sys
import zipfile


def doc_cd(tail_bytes, total):
    eocd = tail_bytes.rfind(b"PK\x05\x06")
    _, _, _, _, n, cd_size, cd_off, _ = struct.unpack("<4sHHHHIIH", tail_bytes[eocd:eocd + 22])
    base = total - len(tail_bytes)
    cd = tail_bytes[cd_off - base: cd_off - base + cd_size]
    out, i = {}, 0
    for _ in range(n):
        h = struct.unpack("<4sHHHHHHIIIHHHHHII", cd[i:i + 46])
        crc, csize, usize, ln, le, lc = h[7], h[8], h[9], h[10], h[11], h[12]
        name = cd[i + 46:i + 46 + ln].decode("utf-8")
        out[name] = (crc, usize, csize)
        i += 46 + ln + le + lc
    return out


tail = open(sys.argv[1], "rb").read()
a = doc_cd(tail, int(sys.argv[2]))
z = zipfile.ZipFile(sys.argv[3])
b = {i.filename: (i.CRC, i.file_size, i.compress_size) for i in z.infolist()}
old, new = sys.argv[4], sys.argv[5]
a2 = {k.replace(old, new, 1): v for k, v in a.items()}
chung = set(a2) & set(b)
khac = [k for k in chung if a2[k][:2] != b[k][:2]]
print(f"zip 13305663: {len(a)} mục; zip RE1: {len(b)} mục; tên trùng sau khi đổi '{old}'->'{new}': {len(chung)}")
print(f"chỉ có ở 13305663: {sorted(set(a2) - set(b))[:5]} ({len(set(a2) - set(b))})")
print(f"chỉ có ở RE1: {sorted(set(b) - set(a2))[:5]} ({len(set(b) - set(a2))})")
print(f"mục trùng tên nhưng khác CRC-32 hoặc kích thước: {len(khac)} {khac[:5]}")
print(f"tổng byte giải nén: 13305663 {sum(v[1] for v in a.values())}, RE1 {sum(v[1] for v in b.values())}")
