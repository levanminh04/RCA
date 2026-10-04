"""T-007: in bảng markdown so mốc từ file JSON của so_moc.py, để số trong kiem-dung-dan.md lấy thẳng từ file.

Chạy: py -3 bang_md.py <so-moc.json> [<so-moc của bộ khác>.json]
Mỗi phương pháp một bảng: hàng = loại lỗi, cột = (mốc, mình, lệch) cho AC@1, AC@3, Avg@5.
Nếu có file thứ hai (bộ thư viện khác), thêm một dòng cho biết hai bộ có cùng giá trị ở mọi ô không.
"""
import json
import sys

COT = ["cpu", "mem", "disk", "socket", "delay", "loss", "AVERAGE"]
TEN = {"cpu": "CPU", "mem": "MEM", "disk": "DISK", "socket": "SOCKET", "delay": "DELAY", "loss": "LOSS", "AVERAGE": "AVERAGE"}


def so(x):
    return ("%.3f" % x).replace(".", ",")


def lech(x):
    s = ("%+.3f" % x).replace(".", ",")
    return "**%s**" % s if abs(x) > 0.02 + 1e-9 else s


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = json.load(open(sys.argv[1], encoding="utf-8"))
    b = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else None
    for m, v in a.items():
        o = {(r["loi"], r["chi_so"]): r for r in v["o"]}
        print("**%s** — %d/%d ô lệch quá 0,02 (in đậm); kết luận theo tiêu chí: %s\n" % (m, v["so_o_vuot"], v["so_o"], v["ket_luan"]))
        print("| Loại lỗi | AC@1 mốc | AC@1 mình | lệch | AC@3 mốc | AC@3 mình | lệch | Avg@5 mốc | Avg@5 mình | lệch |")
        print("|---|---|---|---|---|---|---|---|---|---|")
        for c in COT:
            cells = []
            for cs in ["AC@1", "AC@3", "Avg@5"]:
                r = o[(c, cs)]
                cells += [("%.2f" % r["moc"]).replace(".", ","), so(r["minh"]), lech(r["lech"])]
            print("| %s | %s |" % (TEN[c], " | ".join(cells)))
        if b is not None:
            ob = {(r["loi"], r["chi_so"]): r["minh"] for r in b[m]["o"]}
            khac = [k for k in o if abs(o[k]["minh"] - ob[k]) > 1e-12]
            print("\nHai bộ thư viện: %s\n" % ("cùng giá trị ở mọi ô" if not khac else "khác ở %d ô: %s" % (len(khac), khac)))
        print()


if __name__ == "__main__":
    main()
