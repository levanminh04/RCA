"""T-007: so kết quả chấm (cham.py --json) với mốc Bảng 2 bài TORAI (trich_moc.py).

Mỗi ô (loại lỗi × chỉ số AC@1, AC@3, Avg@5): mốc, kết quả của mình, độ lệch.
Tiêu chí khớp (SPEC T-007, chốt trước khi chạy): mỗi ô lệch ≤ 0,02. Không chỉnh tham số theo kết quả.
Số của mình dùng giá trị chưa làm tròn; mốc trong bài đã làm tròn 2 chữ số.

Chạy: python so_moc.py <moc.json> <phương pháp>=<cham.json> [...] [--cach bo_ca_loi]
"""
import argparse
import json
import sys

COT = ["cpu", "mem", "disk", "socket", "delay", "loss", "AVERAGE"]
CHI_SO = [("AC@1", 0), ("AC@3", 1), ("Avg@5", 2)]
NGUONG = 0.02


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("moc")
    ap.add_argument("cap", nargs="+", help="<MicroRank|TraceRCA>=<file json của cham.py>")
    ap.add_argument("--cach", default="bo_ca_loi")
    ap.add_argument("--json")
    a = ap.parse_args()
    moc = json.load(open(a.moc, encoding="utf-8"))["moc"]
    tong = {}
    for cap in a.cap:
        m, fp = cap.split("=", 1)
        ch = json.load(open(fp, encoding="utf-8"))
        assert len(ch) == 1, "mỗi file cham.json một thư mục"
        bang = ch[0][a.cach]
        print("== %s (%s, cách chấm ca lỗi: %s; ca lỗi: %s)" % (m, fp, a.cach, ch[0]["ca_loi"]))
        print("   %-8s %-6s %6s %6s %7s %s" % ("loi", "chiso", "moc", "minh", "lech", ""))
        o_lech = []
        rows = []
        for c in COT:
            for cs, k in CHI_SO:
                mc = moc[m][c][k]
                mn = bang[c][cs]
                d = mn - mc
                vuot = abs(d) > NGUONG + 1e-9
                o_lech.append(vuot)
                rows.append({"loi": c, "chi_so": cs, "moc": mc, "minh": mn, "lech": d, "vuot_0_02": vuot})
                print("   %-8s %-6s %6.2f %6.3f %+7.3f %s" % (c, cs, mc, mn, d, "VUOT" if vuot else ""))
        ket = "khop" if not any(o_lech) else "lech"
        print("   -> %d/%d ô lệch > %.2f; kết luận theo tiêu chí: %s" % (sum(o_lech), len(o_lech), NGUONG, ket))
        tong[m] = {"cach": a.cach, "so_o_vuot": sum(o_lech), "so_o": len(o_lech), "ket_luan": ket, "o": rows}
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(tong, f, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
