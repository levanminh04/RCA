"""H6 T-057: đồ thị M1 thực dùng trên P7(a) và RE3, so với DT18-NV2. Chỉ đọc đầu ra đã lưu.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h6_do_thi.py results/T-057/do-thi-dt18.json
Nguồn: result.json của vế M1 và T12-on (đường dẫn ở PT#/trung_gian_theo_ca/<bộ>|<ca>/<vế>/result);
RE3: bản nhận Q (ngoài repo), lọc job.json#/slot/arm = M1.
Đếm: nút có cạnh trong extra/canh; thực thể trong extra/tang_P (tập xếp hạng); thực thể dạng DB/cache theo tên.
"""
import glob
import json
import re
import sys

PT = "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json"
Q = "D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received"
DB = re.compile(r"(mongo|mysql|redis|db|cache|rabbit|kafka|postgres)", re.I)


def rec_of(path):
    r = json.load(open(path, encoding="utf-8"))
    return r["records"][0] if "records" in r else r


def tom(recs):
    nodes_u, edges_u, ent_u = set(), set(), set()
    per = []
    for oid, rec in recs:
        ex = rec.get("extra", {})
        canh = [tuple(e) for e in ex.get("canh", [])]
        nodes = {x for e in canh for x in e}
        ents = set(ex.get("tang_P", {}).keys())
        nodes_u |= nodes
        edges_u |= set(canh)
        ent_u |= ents
        per.append({"ca": oid, "n_canh": len(canh), "n_nut_co_canh": len(nodes), "n_thuc_the": len(ents),
                    "n_thuc_the_khong_canh": len(ents - nodes)})
    def mm(k):
        v = [p[k] for p in per]
        return [min(v), max(v)] if v else None
    return {"so_ca": len(per), "nut_co_canh_hop": sorted(nodes_u), "so_nut_co_canh_hop": len(nodes_u),
            "so_canh_hop": len(edges_u), "so_thuc_the_hop": len(ent_u),
            "thuc_the_dang_DB_cache_theo_ten": sorted(e for e in ent_u if DB.search(e)),
            "nut_co_canh_dang_DB_cache": sorted(n for n in nodes_u if DB.search(n)),
            "min_max": {k: mm(k) for k in ("n_canh", "n_nut_co_canh", "n_thuc_the", "n_thuc_the_khong_canh")},
            "theo_ca": per}


def main(outp):
    pt = json.load(open(PT, encoding="utf-8"))
    out = {"lenh": "py -3 -B results/T-057/scripts/h6_do_thi.py " + outp, "bo": {}}
    for ds in ("RE2-TT", "Nezha-OB"):
        for ve in ("M1", "T12-on"):
            recs = []
            for k, v in pt["trung_gian_theo_ca"].items():
                if k.startswith(ds + "|") and ve in v:
                    recs.append((k.split("|")[1], rec_of(v[ve]["result"])))
            out["bo"][f"{ds}|{ve}"] = tom(sorted(recs, key=lambda x: x[0]))
    recs = []
    for j in glob.glob(Q + "/ec2_*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json"):
        job = json.load(open(j, encoding="utf-8"))
        if job.get("slot", {}).get("arm") != "M1":
            continue
        rp = j[:-len("job.json")] + "result.json"
        recs.append((job["slot"].get("opaque_id"), rec_of(rp)))
    out["bo"]["RE3-OB|M1"] = tom(sorted(recs, key=lambda x: str(x[0])))
    out["bo"]["RE3-OB|M1"]["nguon"] = Q + " (job.json#/slot/arm = M1)"
    out["kieu_canh_quan_sat"] = ("extra/canh chỉ lưu cặp (bên gọi, bên được gọi) dựng từ trace; không có trường kiểu cạnh. "
                                 "Theo results/T-040/ban-giao-p6.md:19-20, trace dev không có kiểu cạnh, cạnh dữ liệu/thông điệp không dựng được từ trace.")
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    for k, v in out["bo"].items():
        print(k, v["so_ca"], "nut_co_canh", v["so_nut_co_canh_hop"], "canh", v["so_canh_hop"], "thuc_the", v["so_thuc_the_hop"],
              "DB_ent", len(v["thuc_the_dang_DB_cache_theo_ten"]), "DB_nut_canh", v["nut_co_canh_dang_DB_cache"], v["min_max"])


if __name__ == "__main__":
    main(sys.argv[1])
