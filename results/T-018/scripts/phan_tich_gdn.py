"""T-018 B6/B7: phân tích các lượt GDN đã chạy (không học lại, không gọi code GDN).

Đọc mảng do chay_gdn.py lưu ở D:/RCA-ext/work/T-018/gdn/runs/<nhan>/. Với mỗi lượt:
- tau = max điểm đã làm trơn trên tập kiểm định (như code);
- kiểm lại tập kiểm định: số tick vượt tau phải bằng 0;
- 19 đoạn bình thường giữ ngoài: số tick báo động, số đợt báo động (chuỗi tick liền), số đoạn có báo động,
  báo động sai mỗi giờ (1 tick = 1 s), theo hai cách chuẩn hóa: code (trung vị/IQR của chính đoạn) và biến thể b
  (trung vị/IQR của tập kiểm định); thêm một phép CHẨN ĐOÁN "b_bo_cot_hang": như b nhưng lấy max chỉ trên các cột
  không hằng trong tập học (ngưỡng tính lại trên đúng các cột đó). Đây là phép kiểm cơ chế E2, không phải phương pháp;
- soi giá trị trung gian: cột hay là argmax của A(t) trên đoạn giữ ngoài, số cột IQR kiểm định < 1e-6, độ lớn A.
So giữa các lượt (cùng bộ cột): tương quan Pearson và Spearman của A(t) trên ca R-ca, Jaccard tập tick báo động.
Không dùng nhãn: đoạn giữ ngoài là dữ liệu trước mốc tiêm (bình thường theo giả định), ca R-ca chỉ so giữa các lượt.

Chạy: D:/RCA-ext/envs/py38-gdn/Scripts/python.exe phan_tich_gdn.py <nhan1> <nhan2> ...
Ghi: results/T-018/runs/b6b7-phan-tich.json (gộp, ghi đè theo lượt) và in bảng.
"""
import glob
import json
import os
import sys

import numpy as np

WORK = r"D:\RCA-ext\work\T-018\gdn"
OUT = r"D:\RCA-flashticket\results\T-018\runs\b6b7-phan-tich.json"
EPS = 1e-2


def lam_tron(a):
    s = np.zeros_like(a)
    for t in range(3, a.shape[0]):
        s[t] = a[t - 3:t + 1].mean(axis=0)
    return s


def diem(pred, gt, ref=None):
    err = np.abs(pred - gt)
    base = err if ref is None else ref
    med = np.median(base, axis=0)
    iqr = np.percentile(base, 75, axis=0) - np.percentile(base, 25, axis=0)
    return lam_tron((err - med) / (np.abs(iqr) + EPS)), iqr


def so_dot(mask):
    return int(np.sum(mask[1:] & ~mask[:-1]) + (1 if mask.size and mask[0] else 0))


def feats_of(nhan):
    tt = json.load(open(os.path.join(WORK, "runs", nhan, "tom-tat.json"), encoding="utf-8"))
    return [l.strip() for l in open(os.path.join(WORK, "data", tt["data"], "list.txt")) if l.strip()], tt


def mot_luot(nhan):
    d = os.path.join(WORK, "runs", nhan)
    feats, tt = feats_of(nhan)
    pv, gv = np.load(os.path.join(d, "val_pred.npy")), np.load(os.path.join(d, "val_gt.npy"))
    err_v = np.abs(pv - gv)
    sm_v, iqr_v = diem(pv, gv)
    tau = float(sm_v.max())
    kq = {"nhan": nhan, "data": tt["data"], "seed": tt["seed"], "so_epoch_chay": tt["so_epoch_chay"],
          "epoch_tot_nhat": tt["epoch_tot_nhat"], "val_loss_tot_nhat": (min(tt["val_loss"]) if tt["val_loss"] else None),
          "tau": tau, "tau_code": tt["tau"], "val_vuot_tau": int((sm_v.max(axis=1) > tau).sum()),
          "iqr_val_duoi_1e-6": int((np.abs(iqr_v) < 1e-6).sum()), "s_hoc": tt["s_hoc"]}
    # chẩn đoán (không phải phương pháp): cột hằng trong tập học = cột có min-max chuẩn hóa bằng 0 suốt tập học
    import pandas as pd
    tr = pd.read_csv(os.path.join(WORK, "data", tt["data"], "train.csv"), index_col=0)[feats].to_numpy(float)
    giu = (tr.max(axis=0) - tr.min(axis=0)) > 0
    kq["cot_hang_trong_tap_hoc"] = int((~giu).sum())
    sm_v2 = sm_v[:, giu]
    tau2 = float(sm_v2.max())
    kq["tau_bo_cot_hang"] = tau2
    tong = {"code": [0, 0, 0, 0], "b": [0, 0, 0, 0], "b_bo_cot_hang": [0, 0, 0, 0]}   # tick, đợt, đoạn có báo động, tổng tick
    argmax_dem = {}
    A_max = {"code": [], "b": [], "b_bo_cot_hang": []}
    for f in sorted(glob.glob(os.path.join(d, "ho_pred_*.npy"))):
        ca = os.path.basename(f)[len("ho_pred_"):-4]
        p, g = np.load(f), np.load(os.path.join(d, "ho_gt_%s.npy" % ca))
        sc_code = np.load(os.path.join(d, "ho_scores_%s.npy" % ca)).T
        sc_tay, _ = diem(p, g)
        assert np.abs(sc_tay - sc_code).max() < 1e-6 * max(1.0, np.abs(sc_code).max()), ca
        sc_b, _ = diem(p, g, ref=err_v)
        for k, sc in (("code", sc_code), ("b", sc_b), ("b_bo_cot_hang", sc_b[:, giu])):
            A = sc.max(axis=1)
            m = A > (tau2 if k == "b_bo_cot_hang" else tau)
            tong[k][0] += int(m.sum())
            tong[k][1] += so_dot(m)
            tong[k][2] += int(m.any())
            tong[k][3] += int(A.size)
            A_max[k].append(float(A.max()))
        for i in sc_code.argmax(axis=1):
            argmax_dem[feats[i]] = argmax_dem.get(feats[i], 0) + 1
    for k in ("code", "b", "b_bo_cot_hang"):
        gio = tong[k][3] / 3600.0
        kq["giu_ngoai_" + k] = {"tick_bao_dong": tong[k][0], "dot_bao_dong": tong[k][1], "doan_co_bao_dong": tong[k][2],
                                "so_doan": len(A_max[k]), "gio_binh_thuong": round(gio, 3),
                                "dot_bao_dong_moi_gio": round(tong[k][1] / gio, 2) if gio else None,
                                "ty_le_tick_bao_dong": round(tong[k][0] / tong[k][3], 4) if tong[k][3] else None,
                                "A_max_trung_vi": float(np.median(A_max[k])) if A_max[k] else None,
                                "A_max_lon_nhat": float(max(A_max[k])) if A_max[k] else None}
    tot = sum(argmax_dem.values())
    kq["giu_ngoai_cot_hay_la_argmax"] = [{"cot": c, "ty_le_tick": round(n / tot, 3)}
                                         for c, n in sorted(argmax_dem.items(), key=lambda kv: -kv[1])[:5]] if tot else []
    # ca R-ca: A theo code và biến thể b
    pt, gt_ = np.load(os.path.join(d, "test_pred.npy")), np.load(os.path.join(d, "test_gt.npy"))
    sc_t = np.load(os.path.join(d, "test_scores.npy")).T
    sc_tb, _ = diem(pt, gt_, ref=err_v)
    kq["ca_rca"] = {"bao_dong_code": int((sc_t.max(axis=1) > tau).sum()), "bao_dong_b": int((sc_tb.max(axis=1) > tau).sum()),
                    "bao_dong_b_bo_cot_hang": int((sc_tb[:, giu].max(axis=1) > tau2).sum()),
                    "A_max_code": float(sc_t.max()), "A_max_b": float(sc_tb.max()),
                    "cot_A_max_code": feats[int(sc_t.max(axis=0).argmax())], "cot_A_max_b": feats[int(sc_tb.max(axis=0).argmax())]}
    return kq, sc_t.max(axis=1), sc_tb.max(axis=1), tau, feats


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    nhans = sys.argv[1:]
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"luot": {}, "so_sanh": {}}
    cache = {}
    for n in nhans:
        kq, A, Ab, tau, feats = mot_luot(n)
        old["luot"][n] = kq
        cache[n] = (A, Ab, tau, feats)
        print(json.dumps(kq, ensure_ascii=False))
    for i, a in enumerate(nhans):
        for b in nhans[i + 1:]:
            if sorted(cache[a][3]) != sorted(cache[b][3]) or len(cache[a][0]) != len(cache[b][0]):
                continue  # chỉ so lượt cùng tập cột (A(t) là max qua cột nên không phụ thuộc thứ tự cột)
            Aa, Ab_ = cache[a][0], cache[b][0]
            ma, mb = Aa > cache[a][2], Ab_ > cache[b][2]
            u = (ma | mb).sum()
            old["so_sanh"][a + "|" + b] = {"pearson_A": float(np.corrcoef(Aa, Ab_)[0, 1]), "spearman_A": spearman(Aa, Ab_),
                                           "jaccard_bao_dong": float((ma & mb).sum() / u) if u else None,
                                           "bao_dong": [int(ma.sum()), int(mb.sum())]}
    json.dump(old, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(old["so_sanh"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
