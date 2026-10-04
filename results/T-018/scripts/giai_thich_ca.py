"""T-018 B5 (bước giải thích, SAU khi đã có kết quả): dùng nhãn của ca R-ca để đọc kết quả GDN.

Nhãn chỉ dùng ở đây, không đưa vào mô hình: mốc tiêm (dòng 720 của file, tick = dòng − 5) và service gốc
(ts-route-service, lấy từ tên ca). Đọc mảng do chay_gdn.py lưu (lượt r1s-re2tt5-cham) và A_bien_the_b.npy do tinh_tay_gdn.py lưu.
Chạy: D:/RCA-ext/envs/py38-gdn/Scripts/python.exe giai_thich_ca.py
Ghi: results/T-018/runs/b5-giai-thich-ca.json
"""
import json
import os

import numpy as np

W = r"D:\RCA-ext\work\T-018\gdn"
RUN = os.path.join(W, "runs", "r1s-re2tt5-cham")
OUT = r"D:\RCA-flashticket\results\T-018\runs\b5-giai-thich-ca.json"
MOC_DONG = 720            # 720 dòng trước mốc (runs/tai-moc-tiem.json)
GOC = "ts-route-service"


def main():
    feats = [l.strip() for l in open(os.path.join(W, "data", "re2tt5", "list.txt")) if l.strip()]
    sc = np.load(os.path.join(RUN, "test_scores.npy"))           # N × T
    tau = float(np.load(os.path.join(RUN, "normal_scores.npy")).max())
    A = sc.max(axis=0)
    am = sc.argmax(axis=0)
    tick_moc = MOC_DONG - 5
    bd = A > tau
    truoc, sau = bd[:tick_moc], bd[tick_moc:]
    sau_idx = np.flatnonzero(sau) + tick_moc
    cot_sau = [feats[am[t]] for t in sau_idx]
    Ab = np.load(os.path.join(RUN, "A_bien_the_b.npy"))
    kq = {
        "tau": tau, "so_tick": int(A.size), "tick_moc_tiem": tick_moc,
        "bao_dong_truoc_moc": int(truoc.sum()), "bao_dong_tu_moc": int(sau.sum()),
        "bao_dong_dau_tien_tu_moc_cach_moc_s": (int(sau_idx[0] - tick_moc) if sau_idx.size else None),
        "ty_le_bao_dong_tu_moc_co_cot_dau_thuoc_goc": (round(float(np.mean([c.startswith(GOC + "_") for c in cot_sau])), 3) if cot_sau else None),
        "cot_dau_hay_gap_tu_moc": {c: cot_sau.count(c) for c in sorted(set(cot_sau), key=lambda c: -cot_sau.count(c))[:5]},
        "A_trung_vi_truoc_moc": float(np.median(A[:tick_moc])), "A_trung_vi_tu_moc": float(np.median(A[tick_moc:])),
        "thu_hang_cot_goc_tot_nhat_tai_A_max_sau_moc": None,
        "bien_the_b_bao_dong_truoc_moc": int((Ab[:tick_moc] > tau).sum()), "bien_the_b_bao_dong_tu_moc": int((Ab[tick_moc:] > tau).sum()),
    }
    t_s = tick_moc + int(A[tick_moc:].argmax())
    order = np.argsort(-sc[:, t_s])
    kq["tick_A_max_tu_moc"] = int(t_s)
    kq["thu_hang_cot_goc_tot_nhat_tai_A_max_sau_moc"] = int(min(i for i, j in enumerate(order) if feats[j].startswith(GOC + "_")) + 1)
    kq["top5_tai_A_max_sau_moc"] = [feats[j] for j in order[:5]]
    json.dump(kq, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(kq, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
