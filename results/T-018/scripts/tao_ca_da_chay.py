"""T-018: sinh results/T-018/ca-da-chay.csv từ tom-tat.json của các lượt GDN và runs/b3-chuan-bi.json.

Mỗi dòng: một ca × một lượt × một vai trò (học / chấm ca R-ca / chấm đoạn bình thường giữ ngoài).
Cột: ca, file_nguon, phuong_phap, muc_dich, ly_do (a/b/c theo prompt Đợt 1).
Chạy: py -3 tao_ca_da_chay.py
"""
import csv
import glob
import json
import os

R = r"D:\RCA-flashticket\results\T-018"
W = r"D:\RCA-ext\work\T-018\gdn\runs"
b3 = json.load(open(os.path.join(R, "runs", "b3-chuan-bi.json"), encoding="utf-8"))
HOC = {"re2tt5": b3["hoc_5"], "re2tt5_daocot": b3["hoc_5"], "lstar_n1": b3["hoc_1"], "lstar_n1_hoanvi": b3["hoc_1"],
       "lstar_n5": b3["hoc_5"], "lstar_n10": b3["hoc_10"]}
CA_RCA = "re2tt_ts-route-service_socket_1"
LY_DO = {"r1": "a (lặp T-005: kiểm tính lặp lại, trên đúng dữ liệu T-005)",
         "r1b": "b (cùng mô hình R1, đổi thứ tự cột CSV: phép kiểm mới)",
         "l": "b (cấu hình mới: bộ cột L*, cỡ tập học, seed, thứ tự cột)"}

rows = []
for f in sorted(glob.glob(os.path.join(W, "*", "tom-tat.json"))):
    t = json.load(open(f, encoding="utf-8"))
    n, data = t["nhan"], t["data"]
    ly = LY_DO["r1"] if n.startswith(("r1-", "r1s-")) else (LY_DO["r1b"] if n.startswith("r1b") else LY_DO["l"])
    if not t.get("chi_cham"):
        for c in HOC[data]:
            rows.append([c, f"data/rcaeval/{c}/metrics.parquet (720 dòng trước mốc)", "GDN 9853899 (học)",
                         f"lượt {n}: dữ liệu học bình thường", ly])
    rows.append([CA_RCA, f"data/rcaeval/{CA_RCA}/metrics.parquet (toàn ca)", "GDN 9853899 (chấm)",
                 f"lượt {n}: ví dụ tính tay / so giữa các lượt, chỉ số không cần nhãn", ly])
    for c in t.get("giu_ngoai", {}):
        rows.append([c, f"data/rcaeval/{c}/metrics.parquet (720 dòng trước mốc)", "GDN 9853899 (chấm)",
                     f"lượt {n}: phép kiểm bình thường vs bình thường", ly])
# lượt R1 bị dừng ở giới hạn 1 giờ trước khi ghi tom-tat.json (LOG); thêm tay 5 ca học của nó
for c in HOC["re2tt5"]:
    rows.insert(0, [c, f"data/rcaeval/{c}/metrics.parquet (720 dòng trước mốc)", "GDN 9853899 (học)",
                    "lượt r1-re2tt5-seed5: dữ liệu học bình thường (lượt dừng ở epoch 29/30; mô hình trùng T-005)", LY_DO["r1"]])
with open(os.path.join(R, "ca-da-chay.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["ca", "file_nguon", "phuong_phap", "muc_dich", "ly_do"])
    w.writerows(rows)
print(len(rows), "dòng;", len({r[0] for r in rows}), "ca khác nhau")
