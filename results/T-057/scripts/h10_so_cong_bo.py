"""H10 T-057: đủ độ đo MRP (AC@k = Hit@k, Avg@5, NDCG@5, MRR) từ bảng dòng; SimpleRCA trên đủ 90 ca RE2-TT.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h10_so_cong_bo.py results/T-057/so-cong-bo.json
Nguồn (world P):
  T  = results/T-054/reports/main-013-v2/tables.json#/rows (TT, OB; một dòng một ca-vế; TORAI B đã gộp seed trong ca)
  G  = results/T-054/reports/re3-ban-cuoi-001/re3-tables.json#/per_case (RE3; CIRCA lượt chính ERROR môi trường)
  C  = results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json#/per_case (CIRCA RE3 bổ sung)
  DEV= results/T-052/ket-qua-dev.json#/worlds/P/RE2-TT/per_case/simplerca (30 ca dev)
Kiểm: MRR, avg@5 tính lại so với PT#/bang_theo_ve_P và R#/bang_theo_ve_P.
Số công bố: chỉ những gì repo có (docs/LESSONS.md:10; results/T-034/goi-g2.md §2.7). Không tra nguồn ngoài.
"""
import json
import sys
from collections import defaultdict

KEYS = ("hit@1", "hit@3", "hit@5", "avg@5", "ndcg@5", "rr")


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def agg(rows):
    by = defaultdict(list)
    for arm, m in rows:
        by[arm].append(m)
    return {a: {"n": len(v), **{k: mean([x[k] for x in v if x.get(k) is not None]) for k in KEYS}} for a, v in by.items()}


def main(outp):
    t = json.load(open("results/T-054/reports/main-013-v2/tables.json", encoding="utf-8"))
    pt = json.load(open("results/T-054/reports/p7a-013-v2/phan-tich-nhom.json", encoding="utf-8"))
    g = json.load(open("results/T-054/reports/re3-ban-cuoi-001/re3-tables.json", encoding="utf-8"))
    c = json.load(open("results/T-054/reports/re3-ban-cuoi-001-circa/re3-tables.json", encoding="utf-8"))
    r3 = json.load(open("results/T-055/reports/re3/phan-tich-re3.json", encoding="utf-8"))
    dev = json.load(open("results/T-052/ket-qua-dev.json", encoding="utf-8"))
    out = {"lenh": "py -3 -B results/T-057/scripts/h10_so_cong_bo.py " + outp, "bang": {}, "kiem": {}}
    for ds in ("RE2-TT", "Nezha-OB"):
        rows = [(r["arm"], {k: r["metrics"].get(k) for k in KEYS}) for r in t["rows"]
                if r["dataset"] == ds and r["world"] == "P" and not r.get("auxiliary")]
        a = agg(rows)
        out["bang"][ds] = a
        lech = []
        for arm, v in a.items():
            p = pt["bang_theo_ve_P"].get(f"{ds}|{arm}")
            if p and abs(p["MRR"]["xap_xi"] - v["rr"]) > 1e-9:
                lech.append([arm, p["MRR"]["xap_xi"], v["rr"]])
            if p and abs(p["avg@5"] - v["avg@5"]) > 1e-9:
                lech.append([arm, "avg@5", p["avg@5"], v["avg@5"]])
        out["kiem"][ds] = {"so_ve": len(a), "lech_voi_PT": lech}
    rows = [(r["arm"], r["metrics"]) for r in g["per_case"] if r["world"] == "P" and r["arm"] != "circa"]
    rows += [(r["arm"], r["metrics"]) for r in c["per_case"] if r["world"] == "P"]
    a = agg(rows)
    out["bang"]["RE3-OB"] = a
    lech = []
    for arm, v in a.items():
        p = r3["bang_theo_ve_P"].get(arm)
        if p and (abs(p["rr"] - v["rr"]) > 1e-9 or abs(p["avg@5"] - v["avg@5"]) > 1e-9):
            lech.append([arm, p["rr"], v["rr"], p["avg@5"], v["avg@5"]])
    out["kiem"]["RE3-OB"] = {"so_ve": len(a), "lech_voi_R": lech}
    # SimpleRCA trên đủ 90 ca RE2-TT (30 dev + 60 test)
    dv = dev["worlds"]["P"]["RE2-TT"]["per_case"]["simplerca"]
    te = [r["metrics"] for r in t["rows"] if r["dataset"] == "RE2-TT" and r["world"] == "P" and r["arm"] == "simplerca"]
    allm = list(dv.values()) + te
    out["simplerca_RE2_TT_90_ca"] = {
        "n_dev": len(dv), "n_test": len(te),
        **{k: mean([m[k] for m in allm]) for k in ("hit@1", "hit@3", "hit@5", "avg@5")},
        "so_cong_bo": "SimpleRCA top-1 0,80 trên RE2-TT theo bài FSE 2026 (docs/LESSONS.md:10, ST9–ST10); chưa đối chiếu bản in, chưa biết cửa sổ/tập ca của bài.",
        "ghi_chu": "Ca dev từng dùng để chọn thiết kế M1, không dùng để chọn M4. Gộp chỉ để đối chiếu số công bố, không là kết quả P7.",
    }
    out["trang_thai_tai_lap"] = "results/T-034/goi-g2.md §2.7 (BARO tái lập trên dataset của bài; SimpleRCA chưa tái lập; TraceRCA/MicroRank bản P3 chưa có số công bố; TORAI bản gốc khớp, bản nguồn B chưa có số công bố)."
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["kiem"], ensure_ascii=False))
    print(json.dumps(out["simplerca_RE2_TT_90_ca"], ensure_ascii=False))
    for ds in out["bang"]:
        for arm in ("M1", "simplerca", "torai_B", "baro", "C-a0"):
            v = out["bang"][ds].get(arm)
            if v:
                print(ds, arm, {k: round(v[k], 3) if v[k] is not None else None for k in KEYS}, v["n"])


if __name__ == "__main__":
    main(sys.argv[1])
