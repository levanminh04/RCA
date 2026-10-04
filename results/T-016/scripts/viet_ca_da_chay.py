"""T-016: ghi results/T-016/ca-da-chay.csv: mỗi dòng một (ca, khối chạy). Cột: ca, file_nguon, phuong_phap, muc_dich,
ly_do (a: kiểm lặp lại 1-2 ca; b: cấu hình/code/quy mô mới; c: bằng chứng đầu ra cũ sai), khoi, seed, may.
Danh sách ca lấy từ file kết quả trong thư mục khối (không đọc nhãn ngoài tên ca)."""
import csv
import re
from pathlib import Path

W = Path("D:/RCA-ext/work/T-016")
OB, SS, TT1 = "D:/RCA-ext/data/torai-OB", "D:/RCA-ext/data/torai-SS", "D:/RCA-ext/data/torai-TT"
TT30 = "D:/RCA-ext/work/T-016/data/torai-TT"
K = [  # (thư mục khối, gốc dữ liệu, phương pháp, mục đích, lý do, máy)
    ("thu-harness-torai", OB, "TORAI gốc cửa sổ 10", "chạy thử harness (S3)", "b: harness mới", "laptop"),
    ("thu-harness-torai_sua", OB, "TORAI sửa cửa sổ 10", "chạy thử bản sửa (S5)", "b: code mới", "laptop"),
    ("s3-main-torai-ob-len10-seed0/output/results", OB, "TORAI gốc cửa sổ 10 (main.py nguyên văn + seed)", "S3a tương đương harness", "b: harness mới, đặt seed", "laptop"),
    ("s3-harness-torai-ob-len10", OB, "TORAI gốc cửa sổ 10", "S3a/S3c", "b: harness mới", "laptop"),
    ("s3-harness-torai-ob-len10-thuthap", OB, "TORAI gốc cửa sổ 10 + thu trung gian", "S3b wrapper không đổi hành vi", "b", "laptop"),
    ("s3-harness-torai-ob-len10-lan2", OB, "TORAI gốc cửa sổ 10", "S3c chạy lại cùng seed", "a/b", "laptop"),
    ("s3-harness-torai-ob-len10-hash12345", OB, "TORAI gốc cửa sổ 10, PYTHONHASHSEED=12345", "S3d tất định", "b", "laptop"),
    ("s6-thu-sua-len20", OB, "TORAI sửa cửa sổ 20", "S6 thử thời gian", "b: code mới", "laptop"),
    ("s9-chay-ban-dung-torai", "D:/RCA-ext/work/T-016/s9-ca-dung/torai-OB", "TORAI gốc cửa sổ 10 trên logts/tracets tự dựng", "S9 ảnh hưởng của bản dựng", "b: dữ liệu dựng mới", "laptop"),
    ("s9-chay-ban-dung-torai_sua", "D:/RCA-ext/work/T-016/s9-ca-dung/torai-OB", "TORAI sửa cửa sổ 10 trên bản tự dựng", "S9", "b", "laptop"),
    ("s9-chay-ban-figshare-torai", OB, "TORAI gốc cửa sổ 10", "S9 đối chứng bản Figshare", "b", "laptop"),
    ("s9-chay-ban-figshare-torai_sua", OB, "TORAI sửa cửa sổ 10", "S9 đối chứng", "b", "laptop"),
    ("s12-ct-torai", OB, "TORAI gốc cửa sổ 10, thu đủ dữ liệu", "S12 ví dụ tính tay", "a: 1 ca", "laptop"),
    ("s12-ct-torai_sua", OB, "TORAI sửa cửa sổ 10, thu đủ dữ liệu", "S12 ví dụ tính tay", "a: 1 ca", "laptop"),
    ("s11b-rcd-ss-len10", SS, "RCD cửa sổ 10", "S11b đối ứng Windows cho so Linux", "b: đặt seed; a: lặp lại cấu hình T-006", "laptop"),
]
for ds, root in (("ob", OB), ("ss", SS)):
    for cfg, pp in (("goc-len10", "TORAI gốc cửa sổ 10"), ("sua-len10", "TORAI sửa cửa sổ 10"),
                    ("goc-len20", "TORAI gốc cửa sổ 20"), ("sua-len20", "TORAI sửa cửa sổ 20")):
        K.append((f"s7-{ds}-{cfg}", root, pp, "S7 so số công bố, giá trị trung gian, ngẫu nhiên", "b: code mới / cấu hình mới (seed)", "laptop"))
    for cfg, pp in (("goc-len10-placebo", "TORAI gốc, phép thử giả"), ("sua-len10-placebo", "TORAI sửa, phép thử giả"),
                    ("goc-len10-hoanvi", "TORAI gốc, hoán vị cột"), ("sua-len10-hoanvi", "TORAI sửa, hoán vị cột")):
        K.append((f"s8-{ds}-{cfg}", root, pp, "S8 kiểm không cần nhãn", "b: cấu hình kiểm mới", "laptop"))
for cfg, pp in (("suaA-len10", "TORAI chỉ sửa (A) cửa sổ 10"), ("goc-len10-ML", "TORAI gốc cửa sổ 10, Metric+Log"),
                ("sua-len10-ML", "TORAI sửa cửa sổ 10, Metric+Log")):
    K.append((f"s7-ob-{cfg}", OB, pp, "S7", "b", "laptop"))
for m in ("torai", "torai_sua"):
    for L in (10, 20):
        K.append((f"s10-thu-{m}-len{L}", TT30, f"TORAI {'gốc' if m == 'torai' else 'sửa'} cửa sổ {L}", "S10 thử thời gian TT", "b: quy mô mới", "laptop"))
for cfg, pp in (("goc-len10", "TORAI gốc cửa sổ 10"), ("sua-len10", "TORAI sửa cửa sổ 10"),
                ("goc-len20", "TORAI gốc cửa sổ 20"), ("sua-len20", "TORAI sửa cửa sổ 20")):
    K.append((f"s10-tt-{cfg}", TT30, pp, "S10 quy mô Train Ticket (30 ca dev đã chứng minh trùng)", "b: quy mô mới", "laptop"))
for b, root, pp, md in (("s11-torai-goc-ob-len10", OB, "TORAI gốc cửa sổ 10", "S11 Linux"),
                        ("s11-torai-goc-ss-len10", SS, "TORAI gốc cửa sổ 10", "S11 Linux"),
                        ("s11-torai-sua-ob-len10", OB, "TORAI sửa cửa sổ 10", "S11 Linux"),
                        ("s11-torai-sua-ss-len10", SS, "TORAI sửa cửa sổ 10", "S11 Linux"),
                        ("s11-tt-torai-goc-len10", TT1, "TORAI gốc cửa sổ 10", "S11 thời gian chính thức TT"),
                        ("s11-tt-torai-sua-len10", TT1, "TORAI sửa cửa sổ 10", "S11 thời gian chính thức TT"),
                        ("s11-tt-rcd-len10", TT1, "RCD cửa sổ 10", "S10/S11 RCD quy mô TT"),
                        ("s11-rcd-ss-len10", SS, "RCD cửa sổ 10", "S11 Linux (điểm mở 5 T-006)"),
                        ("s11-rcd-ob-len20", OB, "RCD cửa sổ 20", "S11 đủ 90 ca (điểm mở 3 T-006)"),
                        ("s11-tt30-torai-goc-len10", TT30, "TORAI gốc cửa sổ 10", "S10 thời gian chính thức, Linux/Windows TT"),
                        ("s11-tt30-torai-sua-len10", TT30, "TORAI sửa cửa sổ 10", "S10 thời gian chính thức, Linux/Windows TT"),
                        ("s11-tt30-rcd-len10", TT30, "RCD cửa sổ 10", "S10 RCD quy mô TT (SPEC thay đổi 4)")):
    K.append((f"ec2/{b}", root.replace("D:/RCA-ext/data", "~/rca/T-016/data (bản chép của D:/RCA-ext/data)"), pp, md,
              "b: hệ điều hành mới / quy mô ca mới" if "ob-len20" not in b else "b: T-006 chưa chạy đủ 44/90 ca", "EC2"))

rows = []
for d, root, pp, md, ld, may in K:
    p = W / d
    seeds = sorted([x for x in p.glob("seed*") if x.is_dir()]) or [p]
    for sd in seeds:
        for f in sorted(sd.glob("*.json")):
            if f.name == "lenh.json":
                continue
            ten = f.stem.replace("_failed", "")
            m = re.match(r"(.+)_([a-z0-9]+)_(\d+)$", ten)
            if not m:
                continue
            svc, loi, so = m.groups()
            rows.append({"ca": f"{svc}_{loi}/{so}", "file_nguon": f"{root}/{svc}_{loi}/{so}/",
                         "phuong_phap": pp, "muc_dich": md, "ly_do": ld, "khoi": d,
                         "seed": sd.name if sd.name.startswith("seed") else "seed0 (main.py có seed)", "may": may})
rows.append({"ca": "checkoutservice_cpu/1", "file_nguon": f"{OB}/checkoutservice_cpu/1/",
             "phuong_phap": "script tính tay độc lập (tinh_tay.py), gốc và sửa", "muc_dich": "S12 ví dụ tính tay",
             "ly_do": "a: 1 ca", "khoi": "runs/s12-tinh-tay-*.json", "seed": "seed0", "may": "laptop"})
with open("results/T-016/ca-da-chay.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["ca", "file_nguon", "phuong_phap", "muc_dich", "ly_do", "khoi", "seed", "may"])
    w.writeheader()
    w.writerows(rows)
print(len(rows), "dòng;", len({r['ca'] for r in rows}), "ca khác nhau;", len({r['khoi'] for r in rows}), "khối")
