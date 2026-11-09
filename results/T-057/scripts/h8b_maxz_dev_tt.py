"""H8b T-057 (đáp R2): điều kiện "max-z kênh hẹp" trên dev TT, từ bản native T-053. Chỉ đọc.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h8b_maxz_dev_tt.py results/T-057/maxz-dev-002.json
Nguồn: results/T-053/runs/k-dong-pha1-001/seal.json#/that (kiểm sha256 từng ban-ghi.jsonl.gz trước khi đọc);
chọn config_id = K-E1+E2+E5, dataset RE2-TT (nhãn: results/T-052/ket-qua-dev.json#/labels).
Kiểm tương đương: RR root tính lại từ khối = RR của M1 trong results/T-052/ket-qua-dev.json#/worlds/P/RE2-TT/per_case/M1.
Tiêu chí giống hệt results/T-057/scripts/h8_maxz_dev.py (dùng lại hàm kenh_manh, ngưỡng hẹp 0,2, bản theo hướng).
Phần OB lấy nguyên từ results/T-057/maxz-dev.json#/OB_dev. Mô tả; không xác nhận nguồn vật lý của kênh cực trị.
"""
import gzip
import hashlib
import json
import sys
from fractions import Fraction

sys.path.insert(0, "results/T-057/scripts")
import h8_maxz_dev as h8  # noqa: E402


def rr_khoi(blocks, root):
    pos = 1
    for b in blocks:
        ents = [e for g in b["groups"] for e in g]
        if root in ents:
            return sum(Fraction(1, pos + i) for i in range(len(ents))) / len(ents)
        pos += len(ents)
    return Fraction(0)


def main(outp):
    dev = json.load(open("results/T-052/ket-qua-dev.json", encoding="utf-8"))
    labels = dev["labels"]
    pc = dev["worlds"]["P"]["RE2-TT"]["per_case"]["M1"]
    seal = json.load(open("results/T-053/runs/k-dong-pha1-001/seal.json", encoding="utf-8"))["that"]
    hash_lech = [x["path"] for x in seal if hashlib.sha256(open(x["path"], "rb").read()).hexdigest() != x["sha256"]]
    if hash_lech:
        raise SystemExit(f"Lệch hash, dừng: {hash_lech}")
    recs = {}
    for x in seal:
        for line in gzip.open(x["path"], "rt", encoding="utf-8"):
            r = json.loads(line)
            rec = r.get("ban_ghi", r)
            cid = rec.get("config_id") or r.get("config_id")
            oid = r.get("opaque_id") or rec.get("opaque_id")
            if cid == "K-E1+E2+E5" and oid in labels and labels[oid]["dataset"] == "RE2-TT":
                recs[oid] = rec
    rows = []
    for oid in sorted(recs):
        rec = recs[oid]
        blocks = rec["worlds"]["P"]["blocks"] if "worlds" in rec and "P" in rec["worlds"] else rec["blocks"]
        root = labels[oid]["root"]
        order = [e for b in blocks for g in b["groups"] for e in g]
        first = [e for g in blocks[0]["groups"] for e in g] if blocks else []
        dung = first == [root]
        comp = next((e for e in order if e != root), None) if dung else (order[0] if order and order[0] != root else None)
        rk = h8.kenh_manh(rec, root, True)
        ck = h8.kenh_manh(rec, comp, True) if comp else None
        cs, rs, rw = (ck["kenh_s_max"] if ck else None), rk["kenh_s_max"], rk["kenh_rong_nhat"]
        rows.append({
            "ca": oid, "cell": labels[oid]["cell"], "nhom": "dung" if dung else "sai", "root": root, "doi_thu": comp,
            "rr_khoi": str(rr_khoi(blocks, root)), "rr_T052": str(Fraction(*pc[oid]["RR"]["phan_so"])),
            "co_don_vi_phan_vi": bool(rec.get("extra", {}).get("don_vi_phan_vi")),
            "root_kenh": rk, "doi_thu_kenh": ck,
            "doi_thu_thang_bang_kenh_hep": bool(cs and cs["do_rong"] is not None and cs["do_rong"] < h8.HEP
                                                and rw and rw["do_rong"] is not None and rw["do_rong"] > cs["do_rong"]
                                                and (rs is None or cs["s"] > rs["s"])),
            "root_thang_bang_kenh_hep": bool(rs and rs["do_rong"] is not None and rs["do_rong"] < h8.HEP),
        })
    sai = [r for r in rows if r["nhom"] == "sai"]
    dung = [r for r in rows if r["nhom"] == "dung"]
    ob = json.load(open("results/T-057/maxz-dev.json", encoding="utf-8"))["OB_dev"]
    out = {"lenh": "py -3 -B results/T-057/scripts/h8b_maxz_dev_tt.py " + outp,
           "nguon": "results/T-053/runs/k-dong-pha1-001/seal.json#/that; config K-E1+E2+E5",
           "kiem": {"hash_seal_khop": not hash_lech, "so_ca": len(rows),
                    "co_don_vi_phan_vi": sum(r["co_don_vi_phan_vi"] for r in rows),
                    "rr_khop_T052": sum(r["rr_khoi"] == r["rr_T052"] for r in rows)},
           "TT_dev": {"so_ca": len(rows), "sai": len(sai), "dung": len(dung),
                      "sai_thoa_dieu_kien_H8": [r["ca"] for r in sai if r["doi_thu_thang_bang_kenh_hep"]],
                      "dung_root_thang_bang_kenh_hep": sum(r["root_thang_bang_kenh_hep"] for r in dung)},
           "OB_dev": ob,
           "doc": "Mô tả theo tiêu chí H8: điều kiện đã xuất hiện trên dev. Chưa xác nhận nguồn vật lý của kênh cực trị, chưa chứng minh khóa thay thế tốt hơn.",
           "ca": rows}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps({k: out[k] for k in ("kiem", "TT_dev")}, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
