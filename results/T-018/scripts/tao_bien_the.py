"""T-018 B6/B7: tạo hai biến thể của dữ liệu re2tt5 cho phép kiểm thứ tự cột.

re2tt5_daocot/  : train.csv giữ nguyên, test.csv đảo thứ tự cột (hoán vị RandomState(2)), list.txt giữ nguyên.
                  Dùng với --chi-cham <mô hình R1>: kỳ vọng điểm giống hệt từng byte (GDN đọc cột theo tên).
lstar_n1_hoanvi/: như re2tt5_hoanvi nhưng từ lstar_n1.
re2tt5_hoanvi/  : train.csv, test.csv, ho/ giữ nguyên; list.txt hoán vị (RandomState(0)). Học lại: nút i của mô hình
                  ứng với một cột khác, nên khởi tạo khác; đo mức kết quả đổi.
Chạy: D:/RCA-ext/envs/py312/Scripts/python.exe tao_bien_the.py
"""
import os
import shutil

import numpy as np
import pandas as pd

D = r"D:\RCA-ext\work\T-018\gdn\data"


def main():
    src = os.path.join(D, "re2tt5")
    feats = [l.strip() for l in open(os.path.join(src, "list.txt")) if l.strip()]

    dc = os.path.join(D, "re2tt5_daocot")
    os.makedirs(dc, exist_ok=True)
    shutil.copy(os.path.join(src, "train.csv"), dc)
    shutil.copy(os.path.join(src, "list.txt"), dc)
    te = pd.read_csv(os.path.join(src, "test.csv"), index_col=0)
    cols = list(te.columns)
    perm = [cols[i] for i in np.random.RandomState(2).permutation(len(cols))]
    te[perm].to_csv(os.path.join(dc, "test.csv"))

    hv = os.path.join(D, "re2tt5_hoanvi")
    if os.path.exists(hv):
        shutil.rmtree(hv)
    shutil.copytree(src, hv)
    p = [feats[i] for i in np.random.RandomState(0).permutation(len(feats))]
    with open(os.path.join(hv, "list.txt"), "w") as f:
        f.write("\n".join(p) + "\n")
    print("daocot: test cols", len(perm), "dau:", perm[:3], "| hoanvi: list dau:", p[:3])

    # lstar_n1_hoanvi: như lstar_n1, list.txt hoán vị RandomState(0) (thêm 04/10, SPEC "Thay đổi trong lúc làm" mục 4)
    s1 = os.path.join(D, "lstar_n1")
    h1 = os.path.join(D, "lstar_n1_hoanvi")
    if os.path.exists(h1):
        shutil.rmtree(h1)
    shutil.copytree(s1, h1)
    f1 = [l.strip() for l in open(os.path.join(s1, "list.txt")) if l.strip()]
    p1 = [f1[i] for i in np.random.RandomState(0).permutation(len(f1))]
    with open(os.path.join(h1, "list.txt"), "w") as f:
        f.write("\n".join(p1) + "\n")
    print("lstar_n1_hoanvi: list dau:", p1[:3])


if __name__ == "__main__":
    main()
