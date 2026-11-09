"""B1 T-057: dựng cau-hien-hanh.md từ cau-hien-hanh.json (một nguồn, tránh lệch).

Chạy từ gốc repo: py -3 -B results/T-057/scripts/b1_md.py
"""
import json

d = json.load(open("results/T-057/cau-hien-hanh.json", encoding="utf-8"))
L = ["# Câu hiện hành của T-054, T-055, T-056 (H1)", "",
     "Sinh từ `results/T-057/cau-hien-hanh.json` bằng `py -3 -B results/T-057/scripts/b1_md.py`. " + d["cach_dung"], "",
     "Viết tắt: " + "; ".join(f"{k} = `{v}`" for k, v in d["viet_tat"].items()) + ".", "",
     "| Mã | Câu gốc ở | Chủ đề | Thay bởi | Câu hiện hành | Kiểm chéo |", "|---|---|---|---|---|---|"]
for m in d["muc"]:
    L.append(f"| {m['id']} | {m['goc']} | {m['chu_de']} | {', '.join(m['thay_boi'])} | {m['cau_hien_hanh']} | {m['kiem_cheo']} |")
L += ["", f"Tổng {d['dem']['tong']} mục. Codex chưa kiểm: {', '.join(d['dem']['codex_chua_kiem'])}.", ""]
with open("results/T-057/cau-hien-hanh.md", "x", encoding="utf-8") as f:
    f.write("\n".join(L))
print(len(d["muc"]))
