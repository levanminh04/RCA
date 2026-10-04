"""T-007: TraceRCA có hòa điểm không? Ghi điểm ji của mọi thao tác mà không đổi phép tính.

Vì sao: xáo thứ tự dòng span (cùng tập span) làm thứ hạng TraceRCA đổi ở mọi ca. Hai cơ chế khả dĩ:
(a) nhiều thao tác cùng điểm ji, `sorted` (ổn định) giữ thứ tự xuất hiện của `anomal_df.operation.unique()`,
    nên thứ tự dòng quyết định thứ tự trong nhóm hòa;
(b) mean/std tính theo thứ tự dòng khác cho sai số làm tròn khác, làm đổi cờ bất thường của vài span.
Script bọc tên `sorted` trong module RCAEval.e2e.tracerca (hàm gọi `sorted(ji_dict.items(), ...)`) để chép lại
danh sách (thao tác, ji) trước khi trả nguyên kết quả. Chạy trên cả thứ tự gốc và thứ tự đã xáo (seed 1, như
chay_e2.py --tron 1), so điểm ji từng thao tác giữa hai thứ tự, và đếm nhóm hòa.

Chạy: <env>/bin/python hoa_diem_tracerca.py --out <file jsonl>
"""
import argparse
import builtins
import importlib
import json
import os
import sys

R = os.path.expanduser("~/rca")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "src", "RCAEval"))
from chay_e2 import COLS, DATA, HALF_US  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import glob
    import pandas as pd
    T = importlib.import_module("RCAEval.e2e.tracerca")  # module, không phải hàm cùng tên (xem trung_gian_microrank.py)
    bat = {}

    def sorted_ghi(it, *args, **kw):
        it = list(it)
        bat["ji"] = [(k, float(v)) for k, v in it]
        return builtins.sorted(it, *args, **kw)

    T.sorted = sorted_ghi  # tên toàn cục trong module tracerca; builtins không đổi
    cases = sorted(os.path.basename(d) for d in glob.glob(os.path.join(DATA, "re2ob_*")))
    tong = {"ca": 0, "ca_co_hoa_trong_top10": 0, "ca_ji_khac_giua_hai_thu_tu": 0}
    with open(a.out, "w") as fo:
        for c in cases:
            with open(os.path.join(DATA, c, "inject_time.txt")) as fi:
                inj_us = int(fi.readlines()[0].strip()) * 1_000_000
            tr = pd.read_parquet(os.path.join(DATA, c, "traces.parquet"), columns=COLS)
            base = tr[(tr["startTime"] >= inj_us - HALF_US) & (tr["startTime"] < inj_us + HALF_US)].reset_index(drop=True)
            kq = {}
            for ten, data in [("goc", base.copy()), ("xao", base.sample(frac=1, random_state=1).reset_index(drop=True))]:
                bat.clear()
                out = T.tracerca(data, inj_us, dataset="re2-ob")
                ji = {k: v for k, v in bat["ji"]}
                # lượt 3: giữ nguyên danh sách đưa vào sorted, đúng thứ tự, NaN ghi là None
                kq[ten] = {"ranks": list(out["ranks"]), "ji": ji,
                           "dau_vao_sorted": [[k, None if v != v else v] for k, v in bat["ji"]]}
            ji_g, ji_x = kq["goc"]["ji"], kq["xao"]["ji"]
            khac_ji = sorted(k for k in set(ji_g) | set(ji_x)
                             if not (k in ji_g and k in ji_x and (ji_g[k] == ji_x[k] or (ji_g[k] != ji_g[k] and ji_x[k] != ji_x[k]))))
            nhom = {}  # hòa = bằng nhau tuyệt đối, vì sorted so sánh giá trị chính xác
            for k in kq["goc"]["ranks"]:
                nhom.setdefault(ji_g[k], []).append(k)
            hoa = [g for g in nhom.values() if len(g) > 1]
            hoa_top10 = [g for g in hoa if any(k in kq["goc"]["ranks"][:10] for k in g)]
            p = c.split("_")
            with open(os.path.join(R, "work", "py312-pin", "tracerca", "results",
                                   "%s_%s_%s.json" % ("_".join(p[1:-2]), p[-2], p[-1]))) as f:
                giong_chinh = json.load(f)["0"] == kq["goc"]["ranks"]
            rec = {"case": c, "giong_luot_chinh": giong_chinh,
                   # lượt 2 (03/10 phiên 2): lưu đủ thứ hạng và điểm ji để tính khoảng giá trị khi phá hòa
                   "ranks_goc": kq["goc"]["ranks"], "ranks_xao": kq["xao"]["ranks"],
                   "ji_goc": {k: ji_g[k] for k in kq["goc"]["ranks"]},
                   "dau_vao_sorted_goc": kq["goc"]["dau_vao_sorted"], "dau_vao_sorted_xao": kq["xao"]["dau_vao_sorted"],
                   "so_ji_nan": sum(1 for _, v in kq["goc"]["dau_vao_sorted"] if v is None),
                   "so_thao_tac_co_diem": len(kq["goc"]["ranks"]), "so_ji_khac_giua_hai_thu_tu": len(khac_ji),
                   "ji_khac": khac_ji, "so_nhom_hoa": len(hoa), "nhom_hoa_cham_top10": hoa_top10,
                   "thu_hang_giong": kq["goc"]["ranks"] == kq["xao"]["ranks"]}
            fo.write(json.dumps(rec) + "\n")
            tong["ca"] += 1
            tong["giong_luot_chinh"] = tong.get("giong_luot_chinh", 0) + int(giong_chinh)
            tong["ca_co_hoa_trong_top10"] += int(bool(hoa_top10))
            tong["ca_ji_khac_giua_hai_thu_tu"] += int(bool(khac_ji))
            print(c, "| ji khác giữa hai thứ tự:", len(khac_ji), "| nhóm hòa:", len(hoa), "| nhóm hòa chạm top 10:",
                  len(hoa_top10), "| thứ hạng giống:", rec["thu_hang_giong"], flush=True)
    print("TONG", json.dumps(tong), flush=True)


if __name__ == "__main__":
    main()
