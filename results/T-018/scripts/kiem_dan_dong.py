"""T-018: in lại mọi dòng code và dòng văn bản PDF được dẫn trong ho-so-gdn.md và decomprca.md (Tiêu chí xong 1).

Không đánh giá tự động; in ra để người làm và người phản biện đối chiếu bằng mắt.
- `file.py:N` hoặc `file.py:N-M` (cũng nhận `run.sh`, `.md`) → tìm file theo tên trong repo tương ứng của tài liệu.
- "dòng N" hoặc "dòng N–M" → dòng của văn bản PDF (gdn.txt cho hồ sơ GDN, decomprca.txt cho DecompRCA).
  Một số "dòng" trong tài liệu là số dòng của bảng, không phải PDF; khi đó phần in ra không liên quan, bỏ qua.
`main.py`, `main-ase.py` trong decomprca.md là của RCAEval; `main-ase.py` đọc ở commit fb8f20a (git show).
Chạy: py -3 kiem_dan_dong.py > ../runs/kiem-dan-dong.txt
"""
import os
import re
import subprocess

R = r"D:\RCA-flashticket\results\T-018"
GDN = r"D:\RCA-ext\src\GDN"
DEC = r"D:\RCA-ext\work\T-018\nguon\DecompRCA"
RCE = r"D:\RCA-ext\src\RCAEval"
NG = r"D:\RCA-ext\work\T-018\nguon"


def tim(root, ten):
    if ten.startswith("results/"):
        root = r"D:\RCA-flashticket"
    if os.path.exists(os.path.join(root, ten)):
        return os.path.join(root, ten)
    for d, _, fs in os.walk(root):
        if ".git" in d:
            continue
        if os.path.basename(ten) in fs and d.replace("\\", "/").endswith(os.path.dirname(ten)):
            return os.path.join(d, os.path.basename(ten))
    return None


def dong_file(path, a, b):
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        L = f.read().split(chr(10))
    return [(i, L[i - 1]) for i in range(a, min(b, len(L)) + 1)]


def main():
    pat_code = re.compile(r"`?([A-Za-z0-9_\-./]+\.(?:py|sh|md))`?:(\d+)(?:-(\d+))?((?:,\s*`?\d+(?:-\d+)?`?)*)")
    pat_pdf = re.compile(r"dòng (\d+)(?:[–-](\d+))?")
    for doc, root, txt in [("ho-so-gdn.md", GDN, "gdn.txt"), ("decomprca.md", DEC, "decomprca.txt")]:
        s = open(os.path.join(R, doc), encoding="utf-8").read()
        print("=" * 100)
        print("TÀI LIỆU", doc)
        seen = set()
        for m in pat_code.finditer(s):
            ten, a, b, them = m.group(1), int(m.group(2)), m.group(3), m.group(4)
            ranges = [(a, int(b) if b else a)]
            for x in re.findall(r"(\d+)(?:-(\d+))?", them or ""):
                ranges.append((int(x[0]), int(x[1]) if x[1] else int(x[0])))
            for a_, b_ in ranges:
                key = (ten, a_, b_)
                if key in seen:
                    continue
                seen.add(key)
                if doc == "decomprca.md" and ten == "main-ase.py":
                    out = subprocess.run(["git", "-C", RCE, "show", "fb8f20a6763b19ebf5b8a72abe8c24de7550d122:main-ase.py"],
                                         capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
                    lines = [(i, out[i - 1]) for i in range(a_, min(b_, len(out)) + 1)]
                    where = "RCAEval@fb8f20a:main-ase.py"
                else:
                    r0 = root
                    if doc == "decomprca.md" and (ten.startswith("RCAEval/") or ten == "main.py"):
                        r0 = RCE
                    p = tim(r0, ten)
                    if p is None:
                        print(f"\n--- {ten}:{a_}-{b_}  KHÔNG TÌM THẤY FILE")
                        continue
                    lines, where = dong_file(p, a_, b_), p
                print(f"\n--- {ten}:{a_}-{b_}  ({where})")
                for i, l in lines[:25]:
                    print(f"{i:5d}| {l[:160]}")
        print("\n" + "-" * 40, "dòng văn bản PDF", txt)
        T = open(os.path.join(NG, txt), encoding="utf-8", errors="replace", newline="").read().split(chr(10))  # chỉ ký tự xuống dòng, như sed -n
        seen = set()
        for m in pat_pdf.finditer(s):
            a = int(m.group(1))
            b = int(m.group(2)) if m.group(2) else a
            if (a, b) in seen or b - a > 40:
                continue
            seen.add((a, b))
            print(f"\n[PDF dòng {a}-{b}]")
            for i in range(a, min(b, len(T)) + 1):
                print(f"{i:5d}| {T[i - 1].strip()[:160]}")


if __name__ == "__main__":
    main()
