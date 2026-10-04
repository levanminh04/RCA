"""T-007: TraceRCA sắp thứ hạng với khóa NaN. Kiểm cơ chế và đo ảnh hưởng tới điểm. Không đổi lượt chính.

`RCAEval/e2e/tracerca.py` tính ji = 2·s·c/(s+c) cho mọi thao tác sau mốc; thao tác không có span bất thường có
s = c = 0 nên ji = NaN. Hàm gọi `sorted(ji_dict.items(), key=lambda x: x[1], reverse=True)` rồi mới bỏ NaN. So sánh
với NaN luôn sai, nên kết quả `sorted` không còn là thứ tự giảm dần và phụ thuộc thứ tự đầu vào (thứ tự xuất hiện
của thao tác, tức thứ tự dòng span).

Đầu vào: hoa.jsonl của hoa_diem_tracerca.py (lượt 3: có `dau_vao_sorted_goc`, `dau_vao_sorted_xao`).
Script này:
1. dựng lại thứ hạng bằng đúng phép sắp của hàm trên danh sách đã ghi; phải ra đúng `ranks_goc`, `ranks_xao`;
2. đếm ca có thứ hạng không giảm dần theo ji;
3. tính thứ hạng "bỏ NaN trước khi sắp" (ý định ghi trong code: "ignore ji nan"), giữ thứ tự đầu vào cho nhóm hòa;
4. chấm (AC@1, AC@3, Avg@5 theo loại lỗi, như main.py) bốn biến thể: lượt chính, xáo, bỏ-NaN-trước (gốc), bỏ-NaN-trước (xáo);
5. so với mốc Bảng 2 bài TORAI.
Tên ca chỉ dùng để chấm.

Chạy: py -3 phan_tich_sap_xep_tracerca.py <hoa.jsonl> <moc-torai-bang2-trace.json> --json <file ra>
"""
import argparse
import json
import sys

LOI6 = ["cpu", "mem", "disk", "socket", "delay", "loss"]
TEN = ["AC@1", "AC@3", "Avg@5"]


def svc(op):
    return op.split("_")[0].replace("-db", "")


def sap_nhu_ham(ds):
    """Đúng phép của tracerca: sorted(..., reverse=True) trên cả NaN, rồi bỏ NaN."""
    ds = [(k, float("nan") if v is None else v) for k, v in ds]
    return [k for k, v in sorted(ds, key=lambda x: x[1], reverse=True) if v == v]


def sap_bo_nan_truoc(ds):
    return [k for k, v in sorted([(k, v) for k, v in ds if v is not None], key=lambda x: x[1], reverse=True)]


def ac_vec(ranks, dap_an):
    s = []
    for op in ranks:
        if svc(op) not in s:
            s.append(svc(op))
    if dap_an not in s:
        return (0.0, 0.0, 0.0), None
    r = s.index(dap_an) + 1
    return (float(r <= 1), float(r <= 3), sum(float(r <= k) for k in range(1, 6)) / 5), r


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("hoa")
    ap.add_argument("moc")
    ap.add_argument("--json")
    a = ap.parse_args()
    moc = json.load(open(a.moc, encoding="utf-8"))["moc"]["TraceRCA"]
    BT = ["luot_chinh", "xao", "bo_nan_truoc_goc", "bo_nan_truoc_xao"]
    tong = {b: {f: [0.0, 0.0, 0.0] for f in LOI6} for b in BT}
    n = {f: 0 for f in LOI6}
    dem = {"ca": 0, "dung_lai_goc": 0, "dung_lai_xao": 0, "ca_co_nan": 0, "ca_khong_giam_dan": 0,
           "bo_nan_truoc_goc_bang_xao": 0, "hang_dap_an_doi_khi_bo_nan_truoc": 0}
    so_nan = []
    for line in open(a.hoa, encoding="utf-8"):
        r = json.loads(line)
        p = r["case"].split("_")
        dap_an, loi = "_".join(p[1:-2]), p[-2]
        g, x = r["dau_vao_sorted_goc"], r["dau_vao_sorted_xao"]
        dem["ca"] += 1
        dem["dung_lai_goc"] += int(sap_nhu_ham(g) == r["ranks_goc"])
        dem["dung_lai_xao"] += int(sap_nhu_ham(x) == r["ranks_xao"])
        k_nan = sum(1 for _, v in g if v is None)
        so_nan.append(k_nan)
        dem["ca_co_nan"] += int(k_nan > 0)
        ji = [r["ji_goc"][o] for o in r["ranks_goc"]]
        dem["ca_khong_giam_dan"] += int(any(ji[i] < ji[i + 1] for i in range(len(ji) - 1)))
        bg, bx = sap_bo_nan_truoc(g), sap_bo_nan_truoc(x)
        dem["bo_nan_truoc_goc_bang_xao"] += int(bg == bx)
        bien_the = {"luot_chinh": r["ranks_goc"], "xao": r["ranks_xao"], "bo_nan_truoc_goc": bg, "bo_nan_truoc_xao": bx}
        hang = {}
        for b, rk in bien_the.items():
            v, hang[b] = ac_vec(rk, dap_an)
            for i in range(3):
                tong[b][loi][i] += v[i]
        dem["hang_dap_an_doi_khi_bo_nan_truoc"] += int(hang["luot_chinh"] != hang["bo_nan_truoc_goc"])
        n[loi] += 1
    dem["so_ji_nan_moi_ca_min_max"] = [min(so_nan), max(so_nan)]
    print(json.dumps(dem, ensure_ascii=False))
    out = {"dem": dem, "o": []}
    print("%-8s %-6s %6s | %10s %6s %8s %8s" % ("loi", "chiso", "moc", "luot_chinh", "xao", "bo_nan_g", "bo_nan_x"))
    avg = {b: [0.0, 0.0, 0.0] for b in BT}
    for f in LOI6 + ["AVERAGE"]:
        for i in range(3):
            if f == "AVERAGE":
                v = {b: avg[b][i] for b in BT}
            else:
                v = {b: tong[b][f][i] / n[f] for b in BT}
                for b in BT:
                    avg[b][i] += v[b] / len(LOI6)
            m = moc[f][i]
            rec = {"loi": f, "chi_so": TEN[i], "moc": m}
            rec.update({b: v[b] for b in BT})
            rec.update({"lech_" + b: v[b] - m for b in BT})
            out["o"].append(rec)
            print("%-8s %-6s %6.2f | %10.3f %6.3f %8.3f %8.3f" % (f, TEN[i], m, v["luot_chinh"], v["xao"],
                                                                  v["bo_nan_truoc_goc"], v["bo_nan_truoc_xao"]))
    for b in BT:
        k = sum(1 for o in out["o"] if abs(o["lech_" + b]) > 0.02 + 1e-9)
        out["so_o_lech_qua_0_02_" + b] = k
        print("số ô lệch mốc > 0,02 —", b, ":", k, "/ 21")
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
