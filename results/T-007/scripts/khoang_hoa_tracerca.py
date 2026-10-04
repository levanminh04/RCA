"""T-007: khoảng giá trị mỗi ô TraceRCA có thể nhận khi chỉ thay cách phá hòa điểm ji, NẾU thứ hạng được sắp đúng.

Lưu ý (phiên 2): giả định "thứ hạng của hàm là giảm dần theo ji" SAI ở 79/90 ca, vì hàm sắp cả khóa NaN rồi mới bỏ
(xem phan_tich_sap_xep_tracerca.py). Khoảng ở đây vì vậy là khoảng của biến thể "bỏ NaN trước khi sắp, phá hòa theo
mọi thứ tự", không phải của lượt đã chạy; cột "goc" (lượt chính) có thể nằm ngoài khoảng.

Đầu vào: hoa.jsonl của hoa_diem_tracerca.py (lượt 2, có ji_goc của mọi thao tác có điểm). Điểm ji không đổi theo
thứ tự dòng (đã kiểm 90/90 ca), nên mọi khác biệt do bộ đọc cho thứ tự dòng khác đều nằm trong việc sắp các thao tác
cùng điểm.

Với mỗi ca: nhóm thao tác theo ji bằng nhau tuyệt đối, xếp nhóm theo ji giảm dần. Service = phần trước "_" đầu tiên
(như main.py). G* = nhóm đầu tiên có thao tác của service đáp án.
- hạng tốt nhất = 1 + số service khác có thao tác ở nhóm trước G*;
- hạng xấu nhất = 1 + số service khác có thao tác ở nhóm trước G* hoặc trong G*.
Service đáp án không có thao tác nào thì trượt ở mọi cách. AC@k, Avg@5 của từng ca đơn điệu theo hạng, nên giá trị
nhỏ nhất (lớn nhất) của một ô là tổng các giá trị nhỏ nhất (lớn nhất) từng ca. Tên ca chỉ dùng để chấm.
So khoảng với mốc Bảng 2 bài TORAI và với lượt chính. Nhãn không đi vào phương pháp; đây chỉ là chấm.

Chạy: py -3 khoang_hoa_tracerca.py <hoa.jsonl> <moc-torai-bang2-trace.json> --json <file ra>
"""
import argparse
import json
import sys

LOI6 = ["cpu", "mem", "disk", "socket", "delay", "loss"]


def svc(op):
    return op.split("_")[0].replace("-db", "")


def ac_vec(rank):
    """(AC@1, AC@3, Avg@5) của một ca có đáp án ở hạng `rank` (None = trượt)."""
    if rank is None:
        return (0.0, 0.0, 0.0)
    return (float(rank <= 1), float(rank <= 3), sum(float(rank <= k) for k in range(1, 6)) / 5)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("hoa")
    ap.add_argument("moc")
    ap.add_argument("--json")
    a = ap.parse_args()
    moc = json.load(open(a.moc, encoding="utf-8"))["moc"]["TraceRCA"]
    tong = {f: {"n": 0, "min": [0.0] * 3, "max": [0.0] * 3, "goc": [0.0] * 3} for f in LOI6}
    so_ca_doi_duoc = 0
    for line in open(a.hoa, encoding="utf-8"):
        r = json.loads(line)
        p = r["case"].split("_")
        dap_an, loi = "_".join(p[1:-2]), p[-2]
        ji = r["ji_goc"]
        nhom = {}
        for op in r["ranks_goc"]:
            nhom.setdefault(ji[op], []).append(op)
        nhom_sx = [nhom[k] for k in sorted(nhom, reverse=True)]
        truoc, gstar = set(), None
        for g in nhom_sx:
            if any(svc(o) == dap_an for o in g):
                gstar = g
                break
            truoc |= {svc(o) for o in g}
        if gstar is None:
            tot = xau = None
        else:
            tot = 1 + len(truoc - {dap_an})
            xau = 1 + len((truoc | {svc(o) for o in gstar}) - {dap_an})
        # hạng ở lượt chính, tính lại từ ranks_goc
        s = []
        for op in r["ranks_goc"]:
            if svc(op) not in s:
                s.append(svc(op))
        goc = s.index(dap_an) + 1 if dap_an in s else None
        so_ca_doi_duoc += int(tot != xau)
        t = tong[loi]
        t["n"] += 1
        for i, (lo, hi, g0) in enumerate(zip(ac_vec(xau), ac_vec(tot), ac_vec(goc))):
            t["min"][i] += lo
            t["max"][i] += hi
            t["goc"][i] += g0
    ten = ["AC@1", "AC@3", "Avg@5"]
    out = {"so_ca_hang_dap_an_doi_duoc_khi_pha_hoa": so_ca_doi_duoc, "o": []}
    print("Số ca mà hạng của đáp án đổi được khi phá hòa:", so_ca_doi_duoc, "/ 90")
    print("%-8s %-6s %6s %6s %6s %6s  %s" % ("loi", "chiso", "min", "max", "goc", "moc", "mốc trong khoảng?"))
    avg = {"min": [0.0] * 3, "max": [0.0] * 3, "goc": [0.0] * 3}
    for f in LOI6:
        t = tong[f]
        for i in range(3):
            lo, hi, g0 = t["min"][i] / t["n"], t["max"][i] / t["n"], t["goc"][i] / t["n"]
            for k, v in (("min", lo), ("max", hi), ("goc", g0)):
                avg[k][i] += v / len(LOI6)
            m = moc[f][i]
            trong = lo - 0.005 <= m <= hi + 0.005  # mốc làm tròn 2 chữ số
            out["o"].append({"loi": f, "chi_so": ten[i], "min": lo, "max": hi, "goc": g0, "moc": m, "moc_trong_khoang": trong})
            print("%-8s %-6s %6.3f %6.3f %6.3f %6.2f  %s" % (f, ten[i], lo, hi, g0, m, "có" if trong else "KHÔNG"))
    for i in range(3):
        m = moc["AVERAGE"][i]
        lo, hi, g0 = avg["min"][i], avg["max"][i], avg["goc"][i]
        trong = lo - 0.005 <= m <= hi + 0.005
        out["o"].append({"loi": "AVERAGE", "chi_so": ten[i], "min": lo, "max": hi, "goc": g0, "moc": m, "moc_trong_khoang": trong})
        print("%-8s %-6s %6.3f %6.3f %6.3f %6.2f  %s" % ("AVERAGE", ten[i], lo, hi, g0, m, "có" if trong else "KHÔNG"))
    out["so_o_moc_trong_khoang"] = sum(o["moc_trong_khoang"] for o in out["o"])
    print("Số ô có mốc nằm trong khoảng:", out["so_o_moc_trong_khoang"], "/", len(out["o"]))
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
