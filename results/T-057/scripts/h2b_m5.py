"""H2b T-057 (đáp R3): cờ M5 gốc cho M1 và C-a0, ba bộ; tách trực tiếp/gián tiếp và theo loại lỗi. Chỉ đọc.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h2b_m5.py results/T-057/truy-vet-han-che-002.json
- Đại lượng A (giữ từ H2, đổi tên): "đối thủ đứng đầu là bên gọi trực tiếp/gián tiếp của root" theo extra/canh.
- Đại lượng B: cờ M5 gốc, src/m1_danh_gia/m5.py co_M5(blocks world P, root, extra/G_N): có e ≠ root có đường e → root
  trong G_N và e chắc chắn đứng trước root. Với ca có M5, ghi các e thỏa và e là bên gọi trực tiếp (cạnh e → root
  trong G_N) hay chỉ gián tiếp.
Nguồn bản ghi: PT#/trung_gian_theo_ca/<bộ>|<ca>/<vế>/result (TT, OB); bản nhận RE3 (đã kiểm: b0-re3-nhan-002.json).
Loại lỗi: PT#/cases/<bộ>/<ca>/fault; RE3 từ R#/cases/<ca>/cell. M5 là quan sát, không tự chứng minh cơ chế lan.
"""
import glob
import json
import sys

sys.path.insert(0, "src")
from m1_danh_gia import m5  # noqa: E402

PT = "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json"
R = "results/T-055/reports/re3/phan-tich-re3.json"
Q = "D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received"


def rec_of(p):
    r = json.load(open(p, encoding="utf-8"))
    return r["records"][0] if "records" in r else r


def main(outp):
    pt = json.load(open(PT, encoding="utf-8"))
    r3 = json.load(open(R, encoding="utf-8"))
    old = json.load(open("results/T-057/truy-vet-han-che.json", encoding="utf-8"))
    items = []
    for k, v in pt["trung_gian_theo_ca"].items():
        ds, oid = k.split("|")
        c = pt["cases"][ds][oid]
        for ve in ("M1", "C-a0"):
            items.append((ds, oid, c["root"], c.get("fault"), ve, v[ve]["result"]))
    for j in glob.glob(Q + "/ec2_*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/job.json"):
        job = json.load(open(j, encoding="utf-8"))
        a, oid = job["slot"].get("arm"), job["slot"].get("opaque_id")
        if a in ("M1", "C-a0"):
            cell = r3["cases"][oid]["cell"].split("|")
            items.append(("RE3-OB", oid, cell[1], cell[2], a, j[:-len("job.json")] + "result.json"))
    rows = []
    for ds, oid, root, fault, ve, p in sorted(items):
        rec = rec_of(p)
        blocks = rec["worlds"]["P"]["blocks"] if "worlds" in rec and "P" in rec["worlds"] else rec["blocks"]
        GN = {tuple(x) for x in rec["extra"]["G_N"] if x[0] != x[1]}
        co = m5.co_M5(blocks, root, GN)
        e_list = []
        if co:
            vt = m5._vi_tri(blocks)
            nguon = m5._toi(GN, root) - {root}
            for e in sorted(nguon):
                if e in vt and m5._truoc_han(vt[e], vt[root]):
                    e_list.append({"e": e, "truc_tiep": (e, root) in GN})
        rows.append({"bo": ds, "ca": oid, "root": root, "loai_loi": fault, "ve": ve, "M5": co, "e_truoc_root": e_list})
    dem = {}
    for ds in ("RE2-TT", "Nezha-OB", "RE3-OB"):
        for ve in ("C-a0", "M1"):
            rr = [r for r in rows if r["bo"] == ds and r["ve"] == ve]
            m = [r for r in rr if r["M5"]]
            theo_loi = {}
            for r in m:
                theo_loi[r["loai_loi"]] = theo_loi.get(r["loai_loi"], 0) + 1
            dem[f"{ds}|{ve}"] = {"so_ca": len(rr), "M5": len(m),
                                 "M5_co_ben_goi_truc_tiep": sum(any(x["truc_tiep"] for x in r["e_truoc_root"]) for r in m),
                                 "M5_chi_gian_tiep": sum(not any(x["truc_tiep"] for x in r["e_truoc_root"]) for r in m),
                                 "M5_theo_loai_loi": theo_loi, "ca_M5": [r["ca"] for r in m]}
    # đại lượng A theo loại lỗi (từ truy-vet-han-che.json)
    A = {}
    for key, rr in old["theo_ca"].items():
        ds = key.split("|")[0]
        t = {}
        for r in rr:
            if r["nhom"] == "sai" and r.get("phia_tren") == "truc_tiep":
                f = pt["cases"][ds][r["ca"]].get("fault") if ds in pt["cases"] else r3["cases"][r["ca"]]["cell"].split("|")[2]
                t[f] = t.get(f, 0) + 1
        A[key] = {"dem": old["dem"][key], "doi_thu_truc_tiep_theo_loai_loi": t}
    out = {"lenh": "py -3 -B results/T-057/scripts/h2b_m5.py " + outp,
           "dai_luong_A_doi_thu_dung_dau": A, "dai_luong_B_M5_goc": dem, "so_ban_ghi": len(rows),
           "gioi_han": "M5 là quan sát (thực thể phía trên root theo G_N đứng chắc trước root); không tự chứng minh cơ chế lan. Mô tả sau khi xem test.",
           "theo_ca": rows}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(len(rows))
    print(json.dumps(dem, ensure_ascii=False))
    print(json.dumps({k: v["doi_thu_truc_tiep_theo_loai_loi"] for k, v in A.items()}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
