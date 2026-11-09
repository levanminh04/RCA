"""H3 T-057: ổn định dev -> test của các vế M1-family. Chỉ đọc đầu ra đã lưu.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h3_dev_test.py results/T-057/dev-test.json
Nguồn:
  DEV = results/T-052/ket-qua-dev.json (dev, world P; tính bằng code T-052)
  PT  = results/T-054/reports/p7a-013-v2/phan-tich-nhom.json (test TT/OB, world P)
  R   = results/T-055/reports/re3/phan-tich-re3.json (RE3 test, world P)
  KHOA= results/T-054/runs/sua-cd3-ob-001/nhan/ec2_*/ra/dev-*.json, khóa ban_ghi_cu
        (M1 dev OB chạy bằng code khớp pin main013-v2, theo dinh-chinh-003 Đ11)
Phép kiểm cấu hình: so RR root của M1 dev OB trong DEV với RR tính lại từ blocks của KHOA.
"""
import glob
import json
import sys
from fractions import Fraction

VE = ["M1", "C-a0", "C-a1", "bo-E1", "bo-E2", "bo-E5", "C-d1", "C-d2", "C-g", "C-c", "T12-on",
      "simplerca", "torai_B", "baro", "tracerca", "microrank_full", "circa_ols_da"]
VE_PT = {"simplerca": "simplerca", "torai_B": "torai_B", "baro": "baro", "tracerca": "tracerca",
         "microrank_full": "microrank", "circa_ols_da": "circa"}


def fr(x):
    return Fraction(x["phan_so"][0], x["phan_so"][1])


def rr_from_blocks(blocks, root):
    pos = 1
    for b in blocks:
        ents = [e for g in b.get("groups", []) for e in g] if "groups" in b else b.get("entities", [])
        if root in ents:
            k = len(ents)
            return sum(Fraction(1, pos + i) for i in range(k)) / k
        pos += len(ents)
    return Fraction(0)


def main(outp):
    dev = json.load(open("results/T-052/ket-qua-dev.json", encoding="utf-8"))
    pt = json.load(open("results/T-054/reports/p7a-013-v2/phan-tich-nhom.json", encoding="utf-8"))
    r3 = json.load(open("results/T-055/reports/re3/phan-tich-re3.json", encoding="utf-8"))
    out = {"lenh": "py -3 -B results/T-057/scripts/h3_dev_test.py " + outp, "nguon": {
        "DEV": "results/T-052/ket-qua-dev.json#/worlds/P/<bo>/summary/<ve>/MRR/phan_so",
        "PT": "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json#/bang_theo_ve_P/<bo>|<ve>/MRR",
        "R": "results/T-055/reports/re3/phan-tich-re3.json#/bang_theo_ve_P/<ve>"}}

    # 1. Phép kiểm cấu hình dev OB so với code khóa
    labels = dev["labels"]
    pc = dev["worlds"]["P"]["Nezha-OB"]["per_case"]["M1"]
    kiem = []
    for f in sorted(glob.glob("results/T-054/runs/sua-cd3-ob-001/nhan/ec2_*/ra/dev-*.json")):
        rec = json.load(open(f, encoding="utf-8"))
        oid = rec["opaque_id"]
        b = rec["ban_ghi_cu"]
        root = labels[oid]["root"]
        rr_khoa = rr_from_blocks(b["blocks"], root)
        rr_dev = fr(pc[oid]["RR"])
        kiem.append({"ca": oid, "root": root, "rr_dev_T052": str(rr_dev), "rr_code_khoa": str(rr_khoa),
                     "trung": rr_dev == rr_khoa, "config_id_khoa": b.get("config_id"),
                     "file": f.replace("\\", "/")})
    out["kiem_cau_hinh_OB"] = {"so_ca": len(kiem), "so_trung_RR": sum(k["trung"] for k in kiem),
                               "ca": kiem,
                               "y_nghia": "M1 dev OB của T-052 so với M1 chạy lại trên dev bằng code khớp pin main013-v2 (adapter cũ, trước wrapper span gốc)."}

    # 2. Bảng MRR theo vế: dev, test
    bang = {}
    for ds, dsr in (("RE2-TT", "RE2-TT"), ("Nezha-OB", "Nezha-OB")):
        s = dev["worlds"]["P"][ds]["summary"]
        rows = {}
        for v in VE:
            d = s.get(v)
            vt = VE_PT.get(v, v)
            t = pt["bang_theo_ve_P"].get(f"{dsr}|{vt}")
            rows[v] = {"dev_MRR": float(fr(d["MRR"])) if d else None,
                       "dev_n": d.get("n") if d else None,
                       "test_MRR": t["MRR"]["xap_xi"] if isinstance(t, dict) else None,
                       "test_khoa_PT": f"{dsr}|{vt}" if t else None}
        bang[ds] = rows
    rows = {}
    for v in VE:
        vt = {"microrank_full": "microrank", "circa_ols_da": "circa"}.get(v, v)
        t = r3["bang_theo_ve_P"].get(vt)
        rows[v] = {"test_MRR": t.get("rr") if isinstance(t, dict) else None, "test_khoa_R": vt if t else None}
    bang["RE3-OB"] = rows
    out["bang_MRR"] = bang

    # 3. Chênh M1 - vế, dev và test, cùng chiều hay không
    def dau(x):
        return None if x is None else (1 if x > 1e-12 else (-1 if x < -1e-12 else 0))
    cmp = {}
    for ds in ("RE2-TT", "Nezha-OB"):
        cmp[ds] = {}
        m = bang[ds]["M1"]
        pairs = dev["worlds"]["P"][ds]["pairs_M1_minus"]
        for v in VE[1:]:
            r = bang[ds][v]
            dd = None if r["dev_MRR"] is None else m["dev_MRR"] - r["dev_MRR"]
            dt = None if r["test_MRR"] is None or m["test_MRR"] is None else m["test_MRR"] - r["test_MRR"]
            c = pairs.get(v, {}).get("counts", {})
            vt = VE_PT.get(v, v)
            sc = pt["so_cap"].get(f"{ds}|M1-{vt}|RR", {})
            cmp[ds][v] = {"dev_delta": dd, "dev_TWL": [c.get("win"), c.get("tie"), c.get("loss")],
                          "test_delta": dt,
                          "test_TWL": [sc.get("win"), sc.get("tie"), sc.get("loss")] if sc else None,
                          "test_khoa_so_cap": f"{ds}|M1-{vt}|RR" if sc else None,
                          "dau_dev": dau(dd), "dau_test": dau(dt),
                          "cung_chieu": (dau(dd) == dau(dt)) if dd is not None and dt is not None else None}
    cmp["RE3-OB"] = {}
    for v in VE[1:]:
        vt = {"microrank_full": "microrank", "circa_ols_da": "circa"}.get(v, v)
        sc = r3["so_cap"].get(f"M1-{vt}|rr")
        if sc:
            cmp["RE3-OB"][v] = {"test_delta": float(sc["delta"]), "test_TWL": [int(sc["win"]), int(sc["tie"]), int(sc["loss"])],
                                "CI_o": sc.get("CI_o"), "test_khoa_so_cap": f"M1-{vt}|rr", "dev": "không có dev RE3"}
    out["so_sanh_M1_tru_ve"] = cmp
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["kiem_cau_hinh_OB"]["so_trung_RR"]), "/", out["kiem_cau_hinh_OB"]["so_ca"])
    for ds in ("RE2-TT", "Nezha-OB"):
        for v, x in cmp[ds].items():
            print(ds, v, x["dev_delta"] and round(x["dev_delta"], 3), x["dev_TWL"], x["test_delta"] and round(x["test_delta"], 3), x["test_TWL"], x["cung_chieu"])


if __name__ == "__main__":
    main(sys.argv[1])
