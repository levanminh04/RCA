"""T-018 B6 (chẩn đoán, không chạy mô hình): dữ liệu bình thường của ca khác nằm xa khoảng min–max học được đến đâu.

Với mỗi bộ dữ liệu GDN đã dựng (giá trị đã chuẩn hóa min-max theo tập học): tập học nằm trong [0, 1] theo định nghĩa.
Đo trên 19 đoạn bình thường giữ ngoài: tỷ lệ ô có giá trị ngoài [-1, 2] (lệch quá một lần khoảng học), theo loại metric;
tỷ lệ cột mà trung vị của đoạn nằm ngoài [-1, 2]; và giá trị tuyệt đối lớn nhất theo loại.
Chạy: D:/RCA-ext/envs/py312/Scripts/python.exe chan_doan_lech_phan_bo.py
Ghi: results/T-018/runs/b6-lech-phan-bo.json
"""
import glob
import json
import os

import numpy as np
import pandas as pd

D = r"D:\RCA-ext\work\T-018\gdn\data"
OUT = r"D:\RCA-flashticket\results\T-018\runs\b6-lech-phan-bo.json"


def main():
    kq = {}
    for ten in ["re2tt5", "lstar_n1", "lstar_n5", "lstar_n10"]:
        feats = [l.strip() for l in open(os.path.join(D, ten, "list.txt")) if l.strip()]
        loai = np.array([f.rsplit("_", 1)[-1] for f in feats])
        X = [pd.read_csv(f, index_col=0)[feats].to_numpy(float) for f in sorted(glob.glob(os.path.join(D, ten, "ho", "*.csv")))]
        A = np.concatenate(X)
        ngoai = (A < -1) | (A > 2)
        med_ngoai = np.mean([((np.median(x, axis=0) < -1) | (np.median(x, axis=0) > 2)) for x in X], axis=0)
        r = {"tong": {"ty_le_o_ngoai_[-1,2]": round(float(ngoai.mean()), 4),
                      "ty_le_cot_trung_vi_doan_ngoai_[-1,2]": round(float(med_ngoai.mean()), 4)}}
        for l in sorted(set(loai)):
            m = loai == l
            r[l] = {"so_cot": int(m.sum()), "ty_le_o_ngoai_[-1,2]": round(float(ngoai[:, m].mean()), 4),
                    "ty_le_cot_trung_vi_doan_ngoai_[-1,2]": round(float(med_ngoai[m].mean()), 4),
                    "max_abs": float(np.abs(A[:, m]).max())}
        kq[ten] = r
    json.dump(kq, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for t, r in kq.items():
        print(t, json.dumps(r, ensure_ascii=False))


if __name__ == "__main__":
    main()
