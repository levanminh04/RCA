r"""T-006 bước 0.4: quan hệ giữa RE1 (Zenodo 14590730) và dữ liệu bài BARO fse-* (Zenodo 11046533).

Câu hỏi: số trong bài BARO (chạy trên fse-*) có so được với kết quả chạy trên RE1 không.
So: danh sách ca (service_lỗi/lần); với ca trùng tên: inject_time.txt, SHA-256 của data.csv, số dòng, số cột, tập cột,
khoảng thời gian; nếu khác hash thì so giá trị trên các cột chung.
Chỉ đọc metadata và dữ liệu số; không dùng nhãn cho phương pháp nào.
Cách dùng (từ D:\RCA-ext): python so_re1_fse.py data/RE1-OB data/fse-ob [file của a] [file của b]  (mặc định data.csv data.csv)
"""
import hashlib
import sys
from pathlib import Path

import pandas as pd


def ds_ca(root):
    return {f"{p.parent.parent.name}/{p.parent.name}": p.parent for p in Path(root).glob("*/*/inject_time.txt")}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(a_root, b_root, fa="data.csv", fb="data.csv"):
    print(f"so {fa} của {a_root} với {fb} của {b_root}")
    A, B = ds_ca(a_root), ds_ca(b_root)
    chung = sorted(set(A) & set(B))
    print(f"{a_root}: {len(A)} ca; {b_root}: {len(B)} ca; trùng tên: {len(chung)}")
    nhom = lambda s: sorted({k.split('/')[0] for k in s})
    print(f"  nhóm chỉ có ở {a_root}: {nhom(set(A) - set(B))}")
    print(f"  nhóm chỉ có ở {b_root}: {nhom(set(B) - set(A))}")
    print(f"  file trong một ca: {sorted(x.name for x in A[next(iter(A))].iterdir())} | {sorted(x.name for x in B[next(iter(B))].iterdir())}")
    tk = {"inject_khop": 0, "data_hash_khop": 0, "khac": []}
    for k in chung:
        da, db = A[k], B[k]
        ia = (da / "inject_time.txt").read_text().strip()
        ib = (db / "inject_time.txt").read_text().strip()
        tk["inject_khop"] += ia == ib
        ha, hb = sha(da / fa), sha(db / fb)
        if ha == hb:
            tk["data_hash_khop"] += 1
            continue
        xa, xb = pd.read_csv(da / fa), pd.read_csv(db / fb)
        cc = [c for c in xa.columns if c in xb.columns]
        info = {"ca": k, "inject": (ia, ib), "dong": (len(xa), len(xb)), "cot": (xa.shape[1], xb.shape[1]),
                "cot_chung": len(cc), "time": ((xa["time"].min(), xa["time"].max()), (xb["time"].min(), xb["time"].max()))}
        # so giá trị trên các mốc thời gian chung
        m = xa[cc].merge(xb[cc], on="time", suffixes=("_a", "_b"))
        info["dong_time_chung"] = len(m)
        diff = 0
        for c in cc:
            if c == "time":
                continue
            va, vb = m[c + "_a"], m[c + "_b"]
            both = va.notna() & vb.notna()
            if both.any() and ((va[both] - vb[both]).abs() > 1e-9 * (1 + vb[both].abs())).any():
                diff += 1
        info["cot_khac_gia_tri"] = diff
        tk["khac"].append(info)
    print(f"  ca trùng tên có inject_time giống: {tk['inject_khop']}/{len(chung)}; file cùng SHA-256: {tk['data_hash_khop']}/{len(chung)}")
    for info in tk["khac"][:8]:
        print("  khác:", info)
    if len(tk["khac"]) > 8:
        print(f"  ... còn {len(tk['khac']) - 8} ca khác")
    # Tóm tắt các ca khác
    if tk["khac"]:
        import collections
        print("  tóm tắt ca khác: số cột khác giá trị =", collections.Counter(i["cot_khac_gia_tri"] for i in tk["khac"]).most_common(5))
        print("  tóm tắt: (số dòng a, b) =", collections.Counter(i["dong"] for i in tk["khac"]).most_common(5))
        print("  tóm tắt: (số cột a, b, chung) =", collections.Counter((*i["cot"], i["cot_chung"]) for i in tk["khac"]).most_common(5))


if __name__ == "__main__":
    main(*sys.argv[1:])
