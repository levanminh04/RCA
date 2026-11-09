"""Ghim đầu ra T-057 (sha256, bytes). Chạy từ gốc repo: py -3 -B results/T-057/scripts/manifest.py results/T-057/manifest.json
LOG và STATE là tài liệu sống, không ghim. Không ghi đè file đã có (chế độ "x")."""
import glob
import hashlib
import json
import os
import sys

outp = sys.argv[1]
files = sorted(p.replace(os.sep, "/") for p in glob.glob("results/T-057/**/*", recursive=True)
               if os.path.isfile(p) and not os.path.basename(p).startswith("manifest"))
files.append("tasks/T-057-ho-so-g4/SPEC.md")
out = {"schema": "T057-MANIFEST-1", "ngay": "2026-11-09", "trang_thai": "CHO_PHAN_BIEN_G4",
       "lenh": "py -3 -B results/T-057/scripts/manifest.py " + outp,
       "ghi_chu": "Ghim đầu ra T-057 lúc trình phản biện. LOG và STATE là tài liệu sống, không ghim.",
       "files": {p: {"sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(), "bytes": os.path.getsize(p)} for p in files}}
with open(outp, "x", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print(len(files))
