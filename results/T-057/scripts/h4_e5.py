"""H4 T-057: E5 như lớp phát hiện mức thành phần (tách tự sinh/kế thừa). Chỉ đọc đầu ra đã lưu.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h4_e5.py results/T-057/e5-thanh-phan.json
Nguồn: result.json M1 (TT/OB theo PT#/trung_gian_theo_ca/<bộ>|<ca>/M1/result; RE3 theo bản nhận Q, job.json#/slot/arm=M1).
Đếm từ extra/tang_P (1 = tầng 1, 2 = mọi kênh có cờ bị E5 giải thích, 3 = không có kênh cờ).
Nhãn root chỉ dùng để chấm sau (PT#/cases, R#/cases), không vào phép tính.
Kiểm: so tổng tầng 2 với PT#/E5_tac_dung_M1 (TT, OB).
"""
import glob
import json
import sys
from collections import Counter

PT = "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json"
R = "results/T-055/reports/re3/phan-tich-re3.json"
Q = "D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received"


def rec_of(path):
    r = json.load(open(path, encoding="utf-8"))
    return r["records"][0] if "records" in r else r


def dem(items, rr_m1, rr_bo):
    tong = Counter()
    per = []
    for oid, root, rec in items:
        tang = rec["extra"]["tang_P"]
        c = Counter(tang.values())
        rt = tang.get(root)
        per.append({"ca": oid, "root": root, "tang_root": rt, "n_tang1": c.get(1, 0), "n_tang2": c.get(2, 0),
                    "n_tang3": c.get(3, 0), "rr_M1": rr_m1.get(oid), "rr_bo_E5": rr_bo.get(oid)})
        tong.update({"tang1": c.get(1, 0), "tang2": c.get(2, 0)})
    n = len(per)
    root_t2 = [p["ca"] for p in per if p["tang_root"] == 2]
    doi = [p for p in per if p["rr_M1"] is not None and p["rr_bo_E5"] is not None and abs(p["rr_M1"] - p["rr_bo_E5"]) > 1e-12]
    return {"so_ca": n, "tong_tang1": tong["tang1"], "tong_tang2": tong["tang2"],
            "ca_co_tang2": sum(1 for p in per if p["n_tang2"] > 0),
            "root_o_tang2": root_t2, "so_root_o_tang2": len(root_t2),
            "root_o_tang1": sum(1 for p in per if p["tang_root"] == 1),
            "thuc_the_tang2_khong_phai_root": tong["tang2"] - len(root_t2),
            "ca_RR_doi_khi_bo_E5": [{"ca": p["ca"], "rr_M1": p["rr_M1"], "rr_bo_E5": p["rr_bo_E5"]} for p in doi],
            "theo_ca": per}


def rr_tu_cases(cases_list, ve):
    out = {}
    for c in cases_list:
        if ve in c and "opaque_id" in c:
            out[c["opaque_id"]] = float(c[ve])
    return out


def main(outp):
    pt = json.load(open(PT, encoding="utf-8"))
    r3 = json.load(open(R, encoding="utf-8"))
    out = {"lenh": "py -3 -B results/T-057/scripts/h4_e5.py " + outp, "bo": {}}
    for ds in ("RE2-TT", "Nezha-OB"):
        items = []
        for k, v in pt["trung_gian_theo_ca"].items():
            if k.startswith(ds + "|"):
                oid = k.split("|")[1]
                items.append((oid, pt["cases"][ds][oid]["root"], rec_of(v["M1"]["result"])))
        sc = pt["so_cap"][f"{ds}|M1-bo-E5|RR"]["cases"]
        rr_m1 = {c["opaque_id"]: float(c["M1"]) for c in sc}
        rr_bo = {c["opaque_id"]: float(c["bo-E5"]) for c in sc}
        res = dem(sorted(items), rr_m1, rr_bo)
        res["kiem_PT_E5_tac_dung_M1"] = {"PT": pt["E5_tac_dung_M1"][ds],
                                         "khop_tong_tang2": pt["E5_tac_dung_M1"][ds]["tong_thuc_the_tang2"] == res["tong_tang2"],
                                         "khop_ca_co_tang2": pt["E5_tac_dung_M1"][ds]["ca_co_thuc_the_tang2"] == res["ca_co_tang2"]}
        out["bo"][ds] = res
    items = []
    for j in glob.glob(Q + "/ec2_*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json"):
        job = json.load(open(j, encoding="utf-8"))
        if job.get("slot", {}).get("arm") != "M1":
            continue
        oid = job["slot"]["opaque_id"]
        root = r3["cases"][oid]["cell"].split("|")[1]
        items.append((oid, root, rec_of(j[:-len("job.json")] + "result.json")))
    sc = r3["so_cap"]["M1-bo-E5|rr"]["cases"]
    rr_m1 = {c["opaque_id"]: float(c["M1"]) for c in sc}
    rr_bo = {c["opaque_id"]: float(c["bo-E5"]) for c in sc}
    out["bo"]["RE3-OB"] = dem(sorted(items), rr_m1, rr_bo)
    out["gioi_han"] = ("Không có nhãn mức thành phần: không đo được thực thể bị hạ xuống tầng 2 là đúng (triệu chứng kế thừa) hay sai. "
                       "Chỉ đo chính xác phần hạ nhầm root và ảnh hưởng lên RR root.")
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for ds, v in out["bo"].items():
        print(ds, {k: v[k] for k in v if k not in ("theo_ca",)})


if __name__ == "__main__":
    main(sys.argv[1])
