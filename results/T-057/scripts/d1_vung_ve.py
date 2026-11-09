"""Đ-1 T-057 (Minh duyệt 09/11/2026): vùng nghi ngờ E7 của các vế bỏ quan hệ so với M1. Chỉ đọc, mô tả.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/d1_vung_ve.py results/T-057/vung-ve-bo-quan-he.json
- Vế có E7 trong bản ghi (M1, bo-E1, bo-E2, bo-E5, T12-on): đọc record['region'].
- C-a0, C-a1 không có E7 theo thiết kế (src/m1/chuoi.py:96, DOI_CHUNG_KHONG_E7). Dựng lại bằng chính
  src/m1/e7.vung với T = nhóm đầu của khối đầu world P (src/m1/xep_hang.py:148), kênh = extra/kenh_co (đều có cờ),
  canh = extra/canh, inherited_by = record['inherited_by'].
- Kiểm tái dựng: áp cùng thủ tục lên bản ghi M1 và bo-E5, so với record['region'] đã lưu; phải khớp hết.
- Mô tả bằng src/m1_danh_gia/e7.mo_ta (như results/T-054/scripts/cham.py:481). Nhãn root chỉ dùng ở bước mô tả.
Đây là mô tả sau khi đã xem test (C-15 B); không đổi thiết kế.
"""
import glob
import json
import os
import sys
from types import SimpleNamespace

sys.path.insert(0, "src")
from m1 import e7  # noqa: E402
from m1_danh_gia import e7 as e7m  # noqa: E402

PT = "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json"
R = "results/T-055/reports/re3/phan-tich-re3.json"
Q = "D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received"
VE = ["M1", "bo-E1", "bo-E2", "bo-E5", "T12-on", "C-a1", "C-a0"]


def rec_of(path):
    r = json.load(open(path, encoding="utf-8"))
    return r["records"][0] if "records" in r else r


def tai_dung(rec):
    blocks = rec["worlds"]["P"]["blocks"] if "worlds" in rec and "P" in rec["worlds"] else rec["blocks"]
    T = list(blocks[0]["groups"][0]) if blocks else []
    kenh = [SimpleNamespace(co=True, ma=k["ma"], thuc_the=k["thuc_the"], lop=k["lop"]) for k in rec["extra"]["kenh_co"]]
    canh = [tuple(x) for x in rec["extra"]["canh"]]
    ib = rec.get("inherited_by") or []
    R1 = e7.vung(T, kenh, canh, ib, cach=1)
    R2 = e7.vung(T, kenh, canh, ib, cach=2)
    return {"T": T, "cach_1": {r: sorted(v) for r, v in R1.items()}, "cach_2": {r: sorted(v) for r, v in R2.items()}}


def mo_ta(region, root, O):
    return {f"cach_{k}": e7m.mo_ta(region["T"], {r: set(v) for r, v in region[f"cach_{k}"].items()}, root, O) for k in (1, 2)}


def main(outp):
    pt = json.load(open(PT, encoding="utf-8"))
    r3 = json.load(open(R, encoding="utf-8"))
    cases = []  # (bo, ca, root, {ve: rec})
    for k, v in pt["trung_gian_theo_ca"].items():
        ds, oid = k.split("|")
        cases.append((ds, oid, pt["cases"][ds][oid]["root"], {ve: v[ve]["result"] for ve in VE if ve in v}))
    q = {}
    for j in glob.glob(Q + "/ec2_*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json"):
        job = json.load(open(j, encoding="utf-8"))
        arm, oid = job["slot"].get("arm"), job["slot"].get("opaque_id")
        if arm in VE:
            q.setdefault(oid, {})[arm] = j[:-len("job.json")] + "result.json"
    for oid, m in q.items():
        cases.append(("RE3-OB", oid, r3["cases"][oid]["cell"].split("|")[1], m))

    kiem = {"so_ban_ghi": 0, "khop": 0, "lech": []}
    rows = []
    for ds, oid, root, paths in sorted(cases):
        recs = {ve: rec_of(p) for ve, p in paths.items()}
        row = {"bo": ds, "ca": oid, "root": root, "ve": {}}
        for ve, rec in recs.items():
            O = rec["sets"]["observed"]
            if ve in ("M1", "bo-E5", "bo-E1", "bo-E2", "T12-on") and rec.get("region"):
                if ve in ("M1", "bo-E5"):
                    td = tai_dung(rec)
                    kiem["so_ban_ghi"] += 1
                    ok = all(td[c] == rec["region"][c] for c in ("T", "cach_1", "cach_2"))
                    kiem["khop"] += ok
                    if not ok:
                        kiem["lech"].append([ds, oid, ve])
                reg = rec["region"]
                nguon = "record.region"
            elif ve in ("C-a0", "C-a1"):
                reg = tai_dung(rec)
                nguon = "tai_dung_e7.vung"
            else:
                continue
            row["ve"][ve] = {"nguon": nguon, "O": O, **mo_ta(reg, root, O)}
        rows.append(row)

    def tong(ds, ve, cach):
        xs = [r["ve"][ve][cach] for r in rows if r["bo"] == ds and ve in r["ve"]]
        if not xs:
            return None
        n = len(xs)
        return {"n": n, "ty_le_chua_root_ky_vong": sum(x["p"] for x in xs) / n,
                "co_ky_vong": sum(x["R_ky_vong"] for x in xs) / n,
                "co_tren_O": sum(x["R_ky_vong_tren_O"] or 0 for x in xs) / n}
    tom = {ds: {ve: {c: tong(ds, ve, c) for c in ("cach_1", "cach_2")} for ve in VE}
           for ds in ("RE2-TT", "Nezha-OB", "RE3-OB")}
    # kiểm so với tables.json#/regions (M1, T12-on) cho TT/OB
    t = json.load(open("results/T-054/reports/main-013-v2/tables.json", encoding="utf-8"))
    ref = {(x["dataset"], x["opaque_id"], x["arm"]): x for x in t["regions"]}
    lech_t = []
    for r in rows:
        for ve in ("M1", "T12-on"):
            x = ref.get((r["bo"], r["ca"], ve))
            if x and ve in r["ve"]:
                for c in ("cach_1", "cach_2"):
                    if abs(x[c]["p"] - r["ve"][ve][c]["p"]) > 1e-12 or abs(x[c]["R_ky_vong"] - r["ve"][ve][c]["R_ky_vong"]) > 1e-12:
                        lech_t.append([r["bo"], r["ca"], ve, c])
    out = {"lenh": "py -3 -B results/T-057/scripts/d1_vung_ve.py " + outp,
           "quyen": "Minh duyệt Đ-1, chat 09/11/2026: \"Duyệt Đ-1, làm tiếp\"",
           "kiem_tai_dung_tren_ban_ghi_co_E7": kiem,
           "kiem_voi_tables_regions": {"so_lech": len(lech_t), "lech": lech_t},
           "tom_tat": tom, "ca": rows,
           "gioi_han": "Vùng nghi ngờ, không có nhãn vùng; mô tả sau khi xem test. C-a0/C-a1 vốn không có E7: số ở đây là 'nếu áp E7 lên kênh và cạnh của vế đó'."}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({"kiem": kiem, "lech_tables": len(lech_t)}, ensure_ascii=False))
    for ds, d in tom.items():
        for ve, c in d.items():
            if c["cach_1"]:
                print(ds, ve, {k: (round(v["ty_le_chua_root_ky_vong"], 3), round(v["co_ky_vong"], 2), round(v["co_tren_O"], 3), v["n"]) for k, v in c.items()})


if __name__ == "__main__":
    main(sys.argv[1])
