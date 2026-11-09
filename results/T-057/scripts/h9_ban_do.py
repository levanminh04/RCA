"""H9 T-057: bản đồ điều kiện liên bộ (124 ca test). Chỉ đọc; mô tả sau xem test (C-15 B).

Chạy từ gốc repo: py -3 -B results/T-057/scripts/h9_ban_do.py results/T-057/ban-do-dieu-kien.json
Phần 1 — ca sai của M1 (root không đứng riêng khối đầu), lấy từ results/T-057/truy-vet-han-che.json#/theo_ca.
  Mỗi ca kèm: C-a0 có đúng không (cùng file), R1 có đúng không (K2#/theo_ca, chỉ TT/RE3), và nhãn cơ chế
  CHÉP từ báo cáo/đính chính đã có (CO_CHE, kèm nguồn). Không gán cơ chế mới.
Phần 2 — MRR theo loại lỗi và vị trí N, ba bộ, chép từ PT#/tach_MRR, R#/tach/fault, K#/2_5_vi_tri_N.
Không cộng các nhãn thành tỷ lệ nguyên nhân; một ca có thể thuộc nhiều nhãn. Một nhóm nhỏ không là mẫu hình (QT15).
"""
import json
import sys

CO_CHE = {
    "test-053c028c65": ("kenh_hep_doi_thu", "BC54 §7.5; DC54-1 Đ3"),
    "test-5e8f996191": ("kenh_hep_doi_thu; E1 tăng kênh của đối thủ", "BC54 §7.2, §7.5"),
    "test-7a22c1c7ba": ("ca_hai_kenh_rong; E1 chuyển độ lệch sang span con", "BC54 §7.2, §7.5"),
    "test-07fef64ba3": ("kenh_hep_doi_thu", "BC54 §7.5"),
    "test-3218391218": ("kenh_hep_doi_thu (ca D1)", "BC54 §7.5; DC54-1 Đ2"),
    "test-4dbcb97712": ("kenh_hep_doi_thu; root nút nguồn (frontend)", "BC54 §7.5; DC54-4 Đ13"),
    "test-d46d61c932": ("kenh_hep_doi_thu", "BC54 §7.5"),
    "test-3eca4ed46f": ("ca_hai_kenh_hep", "BC54 §7.5"),
    "test-88dc4b2c47": ("E5 hạ root xuống tầng 2; root nút nguồn (frontend)", "BC54 §7.4, §7.5"),
    "test-fd2c49f3cc": ("root chỉ có kênh log s = 1", "BC54 §7.5"),
    "test-0d4b3947ca": ("IQR nền = 0, z theo đơn vị gốc", "DC55-1 Đ1a"),
    "test-cde8f873f5": ("kenh_hep_doi_thu (trace), sai cả ở C-a0", "DC55-1 Đ1b"),
    "test-d07d23cade": ("kenh_hep_doi_thu (trace), sai cả ở C-a0", "DC55-1 Đ1b"),
    "test-428cf2c868": ("E5 bỏ F_I kênh mạnh của root; thang log", "DC55-1 Đ2"),
}


def main(outp):
    tv = json.load(open("results/T-057/truy-vet-han-che.json", encoding="utf-8"))
    k2 = json.load(open("results/T-056/ket-qua-002.json", encoding="utf-8"))
    k = json.load(open("results/T-056/ket-qua.json", encoding="utf-8"))
    pt = json.load(open("results/T-054/reports/p7a-013-v2/phan-tich-nhom.json", encoding="utf-8"))
    r3 = json.load(open("results/T-055/reports/re3/phan-tich-re3.json", encoding="utf-8"))
    r1 = {x["opaque_id"]: x for x in k2["theo_ca"]}
    sai = []
    thieu_nhan = []
    for ds in ("RE2-TT", "Nezha-OB", "RE3-OB"):
        ca0 = {x["ca"]: x for x in tv["theo_ca"][f"{ds}|C-a0"]}
        for x in tv["theo_ca"][f"{ds}|M1"]:
            if x["nhom"] != "sai":
                continue
            oid = x["ca"]
            cc = CO_CHE.get(oid)
            if cc is None:
                thieu_nhan.append(oid)
            rr1 = r1.get(oid, {}).get("R1_events")
            sai.append({"bo": ds, "ca": oid, "root": x["root"], "doi_thu": x["doi_thu"], "doi_thu_phia_tren": x["phia_tren"],
                        "C_a0_dung": ca0[oid]["nhom"] == "dung",
                        "R1_dat_root_hang1": (rr1 == 1.0) if rr1 is not None else None,
                        "co_che": cc[0] if cc else None, "nguon_co_che": cc[1] if cc else None})
    dem_nhan = {}
    for s in sai:
        for tag in ("kenh_hep_doi_thu", "IQR", "E5", "nút nguồn", "ca_hai_kenh", "log"):
            if s["co_che"] and tag in s["co_che"]:
                dem_nhan.setdefault(tag, []).append(s["ca"])
    nhom = {"loai_loi": {"RE2-TT": pt["tach_MRR"]["RE2-TT|fault"], "Nezha-OB": pt["tach_MRR"]["Nezha-OB|fault"],
                         "RE3-OB": {f: {ve: (v["rr"] if isinstance(v, dict) else v) for ve, v in d.items()} for f, d in r3["tach"]["fault"].items()}},
            "vi_tri_N": {"RE2-TT": pt["tach_MRR"]["RE2-TT|vi_tri_N_p75"], "Nezha-OB": pt["tach_MRR"]["Nezha-OB|vi_tri_N_p75"],
                         "RE3-OB": {kk: vv for kk, vv in k["2_5_vi_tri_N"].items() if kk.startswith("RE3-OB")}},
            "nguon": "PT#/tach_MRR; R#/tach/fault; K#/2_5_vi_tri_N"}
    out = {"lenh": "py -3 -B results/T-057/scripts/h9_ban_do.py " + outp,
           "ca_sai_M1": sai, "so_ca_sai": {ds: sum(1 for s in sai if s["bo"] == ds) for ds in ("RE2-TT", "Nezha-OB", "RE3-OB")},
           "ca_thieu_nhan_co_che": thieu_nhan, "ca_theo_nhan": dem_nhan,
           "R1_dung_o_ca_M1_sai": {"so": sum(1 for s in sai if s["R1_dat_root_hang1"]), "co_R1": sum(1 for s in sai if s["R1_dat_root_hang1"] is not None)},
           "C_a0_dung_o_ca_M1_sai": sum(1 for s in sai if s["C_a0_dung"]),
           "nhom": nhom,
           "gioi_han": "Nhãn cơ chế chép từ báo cáo/đính chính, không gán mới; mô tả sau xem test; không cộng thành tỷ lệ nguyên nhân."}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(out["so_ca_sai"], out["ca_thieu_nhan_co_che"], out["R1_dung_o_ca_M1_sai"], out["C_a0_dung_o_ca_M1_sai"])
    print({kk: len(v) for kk, v in dem_nhan.items()})
    for s in sai:
        print(s["bo"], s["ca"], s["doi_thu"], s["doi_thu_phia_tren"], s["C_a0_dung"], s["R1_dat_root_hang1"], s["co_che"])


if __name__ == "__main__":
    main(sys.argv[1])
