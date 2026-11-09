"""H8 T-057: cơ chế "max-z kênh hẹp" có trên dev không. Chỉ đọc bản ghi dev đã lưu.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h8_maxz_dev.py results/T-057/maxz-dev.json
Nguồn: 22 bản ghi M1 dev OB chạy bằng code khớp pin main013-v2
  results/T-054/runs/sua-cd3-ob-001/nhan/ec2_*/ra/dev-*.json#/ban_ghi_cu (dinh-chinh-003 Đ11).
Nhãn root: results/T-052/ket-qua-dev.json#/labels/<ca>/root (chỉ để chấm, sau khi đọc khối).
Định nghĩa như results/T-054/reports/p7a-013-v2/phan_tich.py:280-293 (kênh F_I = 1, s, độ rộng = r_A − r_N
từ đơn vị phân vị cùng mã), thêm bản theo hướng: hướng "xuong" dùng r_xuong (T-055 dinh-chinh-001 Đ1a).
Ngưỡng "hẹp" = độ rộng < 0,2, như T-054 bao-cao.md §7.5. Dev TT không có bản ghi đủ trung gian: ghi KHONG_DU_DU_LIEU.
"""
import glob
import json
import sys

HEP = 0.2


def kenh_manh(rec, ent, theo_huong):
    ex = rec["extra"]
    dv = {u["ma"]: u for u in ex.get("don_vi_phan_vi", [])}
    out = []
    for k in ex.get("kenh_co", []):
        if k["thuc_the"] != ent or k["F_I"] != 1:
            continue
        u = dv.get(k["don_vi"])
        w = None
        if u is not None:
            if k["huong"] == "len" and u.get("r_len_A") is not None:
                w = u["r_len_A"] - u["r_len_N"]
            elif theo_huong and k["huong"] == "xuong" and u.get("r_xuong_A") is not None:
                w = u["r_xuong_A"] - u["r_xuong_N"]
        out.append({"don_vi": k["don_vi"], "huong": k["huong"], "s": k["s"], "do_rong": w})
    top_s = max(out, key=lambda x: x["s"], default=None)
    rong = [x for x in out if x["do_rong"] is not None]
    top_w = max(rong, key=lambda x: x["do_rong"], default=None)
    return {"kenh_s_max": top_s, "kenh_rong_nhat": top_w, "n_kenh_F_I": len(out)}


def main(outp):
    dev = json.load(open("results/T-052/ket-qua-dev.json", encoding="utf-8"))
    rows = []
    for f in sorted(glob.glob("results/T-054/runs/sua-cd3-ob-001/nhan/ec2_*/ra/dev-*.json")):
        r = json.load(open(f, encoding="utf-8"))
        rec = r["ban_ghi_cu"]
        oid = r["opaque_id"]
        blocks = rec["worlds"]["P"]["blocks"] if "worlds" in rec and "P" in rec["worlds"] else rec["blocks"]
        order = [e for b in blocks for g in b["groups"] for e in g]
        first = [e for g in blocks[0]["groups"] for e in g] if blocks else []
        root = dev["labels"][oid]["root"]
        dung = first == [root]
        comp = next((e for e in order if e != root), None) if dung else (order[0] if order and order[0] != root else None)
        row = {"ca": oid, "cell": dev["labels"][oid]["cell"], "nhom": "dung" if dung else "sai", "root": root,
               "doi_thu": comp, "file": f.replace("\\", "/")}
        for tag, th in (("theo_huong", True), ("chi_len", False)):
            rk = kenh_manh(rec, root, th)
            ck = kenh_manh(rec, comp, th) if comp else None
            cs = ck["kenh_s_max"] if ck else None
            rs = rk["kenh_s_max"]
            rw = rk["kenh_rong_nhat"]
            row[tag] = {
                "root": rk, "doi_thu": ck,
                "doi_thu_thang_bang_kenh_hep": bool(cs and cs["do_rong"] is not None and cs["do_rong"] < HEP
                                                    and rw and rw["do_rong"] is not None and rw["do_rong"] > cs["do_rong"]
                                                    and (rs is None or cs["s"] > rs["s"])),
                "root_thang_bang_kenh_hep": bool(rs and rs["do_rong"] is not None and rs["do_rong"] < HEP),
                "doi_thu_kenh_manh_hep": bool(cs and cs["do_rong"] is not None and cs["do_rong"] < HEP),
            }
        rows.append(row)

    def dem(tag):
        sai = [x for x in rows if x["nhom"] == "sai"]
        dung = [x for x in rows if x["nhom"] == "dung"]
        return {"so_ca": len(rows), "sai": len(sai), "dung": len(dung),
                "sai_do_doi_thu_kenh_hep": [x["ca"] for x in sai if x[tag]["doi_thu_thang_bang_kenh_hep"]],
                "dung_root_thang_bang_kenh_hep": sum(1 for x in dung if x[tag]["root_thang_bang_kenh_hep"]),
                "dung_doi_thu_hang2_kenh_manh_hep": sum(1 for x in dung if x[tag]["doi_thu_kenh_manh_hep"])}
    out = {"lenh": "py -3 -B results/T-057/scripts/h8_maxz_dev.py " + outp,
           "OB_dev": {"theo_huong": dem("theo_huong"), "chi_len_nhu_T054": dem("chi_len")},
           "TT_dev": {"trang_thai": "KHONG_DU_DU_LIEU",
                      "ly_do": "results/T-052/ket-qua-dev.json chỉ lưu kênh của root/đối thủ cho 53 dòng mechanism_traces, không có don_vi_phan_vi; không có bản ghi M1 dev TT đủ trung gian chạy bằng code khóa.",
                      "phep_bo_sung": "H14 (SPEC Phụ lục A nhóm C): chạy lại M1 trên 30 ca dev TT với đủ trung gian; cần Minh duyệt."},
           "so_sanh_test": {"P7a_TT_OB": "results/T-054/reports/p7a-013-v2/bao-cao.md §7.5: 6/10 ca sai (TT 2/3, OB 4/7); ca đúng root thắng bằng kênh hẹp 30/57 TT, 5/27 OB; đối thủ hạng 2 có kênh mạnh nhất hẹp 43/57 TT, 12/27 OB",
                            "RE3": "results/T-055/reports/re3/dinh-chinh-001.md Đ1b: 2/4 ca sai do kênh trace hẹp"},
           "ca": rows}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out["OB_dev"], ensure_ascii=False))
    for x in rows:
        if x["nhom"] == "sai":
            th = x["theo_huong"]
            print(x["ca"], x["cell"], "doi_thu", x["doi_thu"], "cs", th["doi_thu"] and th["doi_thu"]["kenh_s_max"],
                  "root_s", th["root"]["kenh_s_max"], "root_w", th["root"]["kenh_rong_nhat"])


if __name__ == "__main__":
    main(sys.argv[1])
