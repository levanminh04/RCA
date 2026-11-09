"""B12b T-057 (sau phản biện G4 lượt 1): soát số theo DÒNG cho bao-cao-tien-do-co-002.md và dinh-chinh-001.md.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/b12b_soat_so.py results/T-057/soat-so-002.json
Khác b12_soat_so.py: mỗi mục có "neo" (chuỗi phải nằm trên cùng dòng với số), nên kiểm số ở đúng dòng/bảng, gồm mẫu số.
Giá trị đọc bằng con trỏ → định dạng kiểu Việt (dấu phẩy, làm tròn nửa lên) → phải có trên một dòng chứa neo.
Mục kiểu "dem" so một số nguyên đếm từ file với chuỗi viết tay trên dòng neo. Giữ script cũ; script này không kiểm ho-so-g4.md.
"""
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP

BC = "results/T-057/bao-cao-tien-do-co-002.md"
DC = "results/T-057/dinh-chinh-001.md"
F = {
    "PT": "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json",
    "R": "results/T-055/reports/re3/phan-tich-re3.json",
    "A": "results/T-054/reports/main-013-v2/a4.json",
    "K": "results/T-056/ket-qua.json",
    "K2": "results/T-056/ket-qua-002.json",
    "SCB": "results/T-057/so-cong-bo.json",
    "VV": "results/T-057/vung-ve-bo-quan-he.json",
    "MZ": "results/T-057/maxz-dev.json",
    "MZ2": "results/T-057/maxz-dev-002.json",
    "TV2": "results/T-057/truy-vet-han-che-002.json",
    "BD": "results/T-057/ban-do-dieu-kien.json",
    "DT": "results/T-057/dev-test.json",
    "B0R": "results/T-057/b0-re3-nhan-002.json",
}
MAU = {'bc_log_root': 'ở {}/30 ca nhưng', 'bc_log_top': 'theo số log lỗi ở {}/30', 'bc_maxz_test': 'có ở {}/14 ca', 'bc_maxz_TT': '({}/4 ca sai RE2-TT', 'bc_maxz_TT_n': '/{} ca sai RE2-TT', 'bc_maxz_OB': '{}/5 ca sai Nezha', 'bc_maxz_OB_n': '/{} ca sai Nezha', 'bc_M5_OB_Ca0': 'có {} ca một dịch vụ', 'bc_M5_OB_nd': '{} ca trễ mạng, 2 ca', 'bc_M5_OB_M1': 'Với M1 còn {} ca', 'bc_A_OB_nd': '({} trễ mạng', 'bc_A_OB': 'bên gọi trực tiếp": {} ca', 'bc_TT_win': 'RE2-TT {} ca thắng', 'bc_TT_tie': '{} hòa, 2 thua; RE3', 'bc_RE3_tie': '1 thắng, {} hòa', 'bc_R1_TT': '{}/60 ca RE2-TT', 'bc_R1_RE3': '{}/30 ca RE3-OB', 'bc_nguon_n': 'SimpleRCA ({} ca)', 'bc_nd_n': '({} ca)', 'dc_TT_win': 'TT {} thắng', 'dc_TT_tie': '/ {} hòa / 2 thua', 'dc_RE3_tie': '/ {} hòa / 1 thua', 'dc_MZ2_n': 'ở {}/30 ca TT', 'dc_MZ2_rr': 'khớp T-052 {}/30', 'dc_MZ2_sai': 'có {} ca sai', 'dc_MZ2_h8': '**{}/4 ca sai', 'dc_MZ2_dung': '; {}/26', 'dc_MZ2_dung_n': '/{} ca đúng', 'dc_A_TT_Ca0': '| {} → 0 | 8 → 0', 'dc_A_OB_Ca0': '| 1 → 0 | {} → 0', 'dc_A_RE3_M1': '| 1 → {} |', 'dc_B_OB': '**{} → 0**', 'dc_B_RE3_Ca0': '**{} → 2**', 'dc_B_RE3_M1': '**3 → {}**', 'dc_B_OB_nd': 'network_delay {},', 'dc_B_RE3_tt': 'C-a0 có {} ca có bên gọi', 'dc_A_OB_nd': '= {} network_delay', 'dc_nguon_n': 'ở {} ca root frontend', 'dc_re3_slot': '{}/420 slot', 'dc_scb_circa_n': 'n = {},'}
REG = []
# Bảng 5.1 báo cáo: neo là nhãn hàng
for neo, ve in (("| M1 (đồ thị)", "M1"), ("| M1 bỏ quan hệ (C-a0)", "C-a0"), ("| SimpleRCA |", "simplerca"), ("| BARO |", "baro")):
    for ds in ("RE2-TT", "Nezha-OB", "RE3-OB"):
        for k in ("rr", "ndcg@5"):
            REG.append((f"bc51_{ve}_{ds}_{k}", "SCB", f"/bang/{ds}/{ve}/{k}", 3, BC, neo))
for ds in ("RE2-TT", "RE3-OB"):
    for k in ("rr", "ndcg@5"):
        REG.append((f"bc51_torai_{ds}_{k}", "SCB", f"/bang/{ds}/torai_B/{k}", 3, BC, "| TORAI |"))
REG += [
    ("bc_TT_delta", "A", "/TT/P/delta", 3, BC, "**RE2-TT:**"),
    ("bc_TT_lo", "A", "/TT/P/E04/raw/lo", 3, BC, "**RE2-TT:**"),
    ("bc_TT_hi", "A", "/TT/P/E04/raw/hi", 3, BC, "**RE2-TT:**"),
    ("bc_OB_dMRR", "PT", "/so_cap/Nezha-OB|M1-simplerca|RR/delta_mean", 3, BC, "**Nezha-OB:**"),
    ("bc_RE3_abs", "R", "/so_cap/M1-simplerca|rr/delta|abs", 3, BC, "**RE3-OB (lỗi mã nguồn):**"),
    ("bc_nd_M1", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/M1", 3, BC, "MRR 0,900 so với"),
    ("bc_nd_Ca0", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/C-a0", 3, BC, "MRR 0,900 so với"),
    ("bc_nd_M4", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/simplerca", 3, BC, "MRR 0,900 so với"),
    ("bc_nd_n", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/n", None, BC, "MRR 0,900 so với"),
    ("bc_M5_OB_Ca0", "TV2", "/dai_luong_B_M5_goc/Nezha-OB|C-a0/M5", None, BC, "Trên toàn bộ 34 ca Nezha-OB"),
    ("bc_M5_OB_nd", "TV2", "/dai_luong_B_M5_goc/Nezha-OB|C-a0/M5_theo_loai_loi/network_delay", None, BC, "Trên toàn bộ 34 ca Nezha-OB"),
    ("bc_M5_OB_M1", "TV2", "/dai_luong_B_M5_goc/Nezha-OB|M1/M5", None, BC, "Trên toàn bộ 34 ca Nezha-OB"),
    ("bc_A_OB_nd", "TV2", "/dai_luong_A_doi_thu_dung_dau/Nezha-OB|C-a0/doi_thu_truc_tiep_theo_loai_loi/network_delay", None, BC, "Trên toàn bộ 34 ca Nezha-OB"),
    ("bc_A_OB", "TV2", "/dai_luong_A_doi_thu_dung_dau/Nezha-OB|C-a0/dem/doi_thu_truc_tiep_goi_root", None, BC, "Trên toàn bộ 34 ca Nezha-OB"),
    ("bc_TT_win", "PT", "/so_cap/RE2-TT|M1-C-a0|RR/win", None, BC, "RE2-TT 2 ca thắng"),
    ("bc_TT_tie", "PT", "/so_cap/RE2-TT|M1-C-a0|RR/tie", None, BC, "RE2-TT 2 ca thắng"),
    ("bc_RE3_tie", "R", "/so_cap/M1-C-a0|rr/tie", None, BC, "RE3-OB 1 thắng"),
    ("bc_R1_TT", "K2", "/tom_tat/RE2-TT/root_events_hon_moi_service_khac", None, BC, "quy tắc đếm đơn giản"),
    ("bc_R1_RE3", "K2", "/tom_tat/RE3-OB/root_events_hon_moi_service_khac", None, BC, "quy tắc đếm đơn giản"),
    ("bc_nguon_M1", "PT", "/tach_MRR/Nezha-OB|vi_tri_N_p75/nguồn/M1", 3, BC, "*Root là nút nguồn*"),
    ("bc_nguon_M4", "PT", "/tach_MRR/Nezha-OB|vi_tri_N_p75/nguồn/simplerca", 3, BC, "*Root là nút nguồn*"),
    ("bc_nguon_n", "PT", "/tach_MRR/Nezha-OB|vi_tri_N_p75/nguồn/n", None, BC, "*Root là nút nguồn*"),
    ("bc_log_root", "K", "/2_2_log_loi_RE3/tom_tat/root_has_logerr_increase", None, BC, "*Lỗi mã nguồn:*"),
    ("bc_log_top", "K", "/2_2_log_loi_RE3/tom_tat/root_top_by_d_log", None, BC, "*Lỗi mã nguồn:*"),
    ("bc_maxz_test", "BD", "/ca_theo_nhan/kenh_hep_doi_thu|len", None, BC, "8/14 ca M1 sai"),
    ("bc_maxz_TT", "MZ2", "/TT_dev/sai_thoa_dieu_kien_H8|len", None, BC, "8/14 ca M1 sai"),
    ("bc_maxz_TT_n", "MZ2", "/TT_dev/sai", None, BC, "8/14 ca M1 sai"),
    ("bc_maxz_OB", "MZ", "/OB_dev/theo_huong/sai_do_doi_thu_kenh_hep|len", None, BC, "8/14 ca M1 sai"),
    ("bc_maxz_OB_n", "MZ", "/OB_dev/theo_huong/sai", None, BC, "8/14 ca M1 sai"),
    ("bc_vung_TT", "VV", "/tom_tat/RE2-TT/M1/cach_1/ty_le_chua_root_ky_vong", 3, BC, "vùng nghi ngờ có chứa root"),
    ("bc_vung_OB", "VV", "/tom_tat/Nezha-OB/M1/cach_1/ty_le_chua_root_ky_vong", 3, BC, "vùng nghi ngờ có chứa root"),
    ("bc_vung_RE3", "VV", "/tom_tat/RE3-OB/M1/cach_1/ty_le_chua_root_ky_vong", 3, BC, "vùng nghi ngờ có chứa root"),
    ("bc_vung_co_min", "VV", "/tom_tat/Nezha-OB/M1/cach_1/co_ky_vong", 1, BC, "vùng nghi ngờ có chứa root"),
    ("bc_vung_co_max", "VV", "/tom_tat/RE2-TT/M1/cach_1/co_ky_vong", 1, BC, "vùng nghi ngờ có chứa root"),
    # Đính chính 001
    ("dc_TT_win", "PT", "/so_cap/RE2-TT|M1-C-a0|RR/win", None, DC, "TT 2 thắng / 56 hòa / 2 thua"),
    ("dc_TT_tie", "PT", "/so_cap/RE2-TT|M1-C-a0|RR/tie", None, DC, "TT 2 thắng / 56 hòa / 2 thua"),
    ("dc_RE3_tie", "R", "/so_cap/M1-C-a0|rr/tie", None, DC, "RE3 1 thắng / 28 hòa"),
    ("dc_MZ2_n", "MZ2", "/kiem/co_don_vi_phan_vi", None, DC, "có độ rộng kênh ở 30/30"),
    ("dc_MZ2_rr", "MZ2", "/kiem/rr_khop_T052", None, DC, "có độ rộng kênh ở 30/30"),
    ("dc_MZ2_sai", "MZ2", "/TT_dev/sai", None, DC, "dev TT có 4 ca sai"),
    ("dc_MZ2_h8", "MZ2", "/TT_dev/sai_thoa_dieu_kien_H8|len", None, DC, "dev TT có 4 ca sai"),
    ("dc_MZ2_dung", "MZ2", "/TT_dev/dung_root_thang_bang_kenh_hep", None, DC, "dev TT có 4 ca sai"),
    ("dc_MZ2_dung_n", "MZ2", "/TT_dev/dung", None, DC, "dev TT có 4 ca sai"),
    ("dc_A_TT_Ca0", "TV2", "/dai_luong_A_doi_thu_dung_dau/RE2-TT|C-a0/dem/doi_thu_truc_tiep_goi_root", None, DC, "| A. Ở ca sai"),
    ("dc_A_OB_Ca0", "TV2", "/dai_luong_A_doi_thu_dung_dau/Nezha-OB|C-a0/dem/doi_thu_truc_tiep_goi_root", None, DC, "| A. Ở ca sai"),
    ("dc_A_RE3_M1", "TV2", "/dai_luong_A_doi_thu_dung_dau/RE3-OB|M1/dem/doi_thu_truc_tiep_goi_root", None, DC, "| A. Ở ca sai"),
    ("dc_B_OB", "TV2", "/dai_luong_B_M5_goc/Nezha-OB|C-a0/M5", None, DC, "| B. Cờ M5 gốc"),
    ("dc_B_RE3_Ca0", "TV2", "/dai_luong_B_M5_goc/RE3-OB|C-a0/M5", None, DC, "| B. Cờ M5 gốc"),
    ("dc_B_RE3_M1", "TV2", "/dai_luong_B_M5_goc/RE3-OB|M1/M5", None, DC, "| B. Cờ M5 gốc"),
    ("dc_B_OB_nd", "TV2", "/dai_luong_B_M5_goc/Nezha-OB|C-a0/M5_theo_loai_loi/network_delay", None, DC, "B ở OB C-a0 theo loại lỗi"),
    ("dc_B_RE3_tt", "TV2", "/dai_luong_B_M5_goc/RE3-OB|C-a0/M5_co_ben_goi_truc_tiep", None, DC, "B ở RE3: C-a0 có"),
    ("dc_A_OB_nd", "TV2", "/dai_luong_A_doi_thu_dung_dau/Nezha-OB|C-a0/doi_thu_truc_tiep_theo_loai_loi/network_delay", None, DC, "A ở OB C-a0: 8 ca"),
    ("dc_dev_M1", "DT", "/bang_MRR/RE2-TT/M1/dev_MRR", 3, DC, "C-a0 dev TT"),
    ("dc_dev_Ca0", "DT", "/bang_MRR/RE2-TT/C-a0/dev_MRR", 3, DC, "C-a0 dev TT"),
    ("dc_dev_Ca0_OB", "DT", "/bang_MRR/Nezha-OB/C-a0/dev_MRR", 3, DC, "C-a0 dev TT"),
    ("dc_nguon_n", "PT", "/tach_MRR/Nezha-OB|vi_tri_N_p75/nguồn/n", None, DC, "ở 6 ca root frontend"),
    ("dc_re3_slot", "B0R", "/so_slot_kiem", None, DC, "420/420 slot"),
    ("dc_circa", "R", "/bang_theo_ve_P/circa/rr", 3, DC, "Dùng `R#/bang_theo_ve_P/circa`"),
    ("dc_circa_rht", "R", "/bang_theo_ve_P/circa_rht_aux/rr", 3, DC, "Dùng `R#/bang_theo_ve_P/circa`"),
    ("dc_scb_circa_n", "SCB", "/bang/RE3-OB/circa/n", None, DC, "có n = 60"),
]


def get(obj, ptr):
    lay_abs = ptr.endswith("|abs")
    if lay_abs:
        ptr = ptr[:-4]
    dem_len = ptr.endswith("|len")
    if dem_len:
        ptr = ptr[:-4]
    for p in ptr.strip("/").split("/"):
        obj = obj[int(p)] if isinstance(obj, list) else obj[p.replace("~1", "/")]
    if dem_len:
        return len(obj)
    if isinstance(obj, dict) and "phan_so" in obj:
        obj = obj["phan_so"][0] / obj["phan_so"][1]
    if isinstance(obj, dict) and "xap_xi" in obj:
        obj = obj["xap_xi"]
    if isinstance(obj, str):
        obj = float(obj)
    return abs(obj) if lay_abs else obj


def fmt(v, nd):
    if nd is None:
        return str(int(v))
    d = Decimal(str(v)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    return s.replace("-", "−").replace(".", ",")


def main(outp):
    cache = {k: json.load(open(p, encoding="utf-8")) for k, p in F.items()}
    lines = {p: open(p, encoding="utf-8").read().splitlines() for p in (BC, DC)}
    rows, lech = [], []
    for ma, f, ptr, nd, doc, neo in REG:
        try:
            v = get(cache[f], ptr)
            s = fmt(v, nd)
        except Exception as e:  # noqa: BLE001
            rows.append({"ma": ma, "trang_thai": "KHONG_DOC_DUOC", "loi": repr(e)})
            lech.append(ma)
            continue
        dong = [i + 1 for i, ln in enumerate(lines[doc]) if neo in ln]
        if ma in MAU:
            pats = [re.escape(MAU[ma].format(s))]
        else:
            pats = [r"(?<![\d,])" + re.escape(c) + r"(?![\d,]?\d)" for c in {s, s.replace("−", "-")}]
        ok_dong = [i for i in dong if any(re.search(pt, lines[doc][i - 1]) for pt in pats)]
        ok = bool(ok_dong)
        rows.append({"ma": ma, "file": F[f], "con_tro": ptr, "gia_tri": v, "chuoi": s, "tai_lieu": doc, "neo": neo,
                     "dong_neo": dong, "dong_khop": ok_dong, "trang_thai": "KHOP" if ok else ("KHONG_THAY_NEO" if not dong else "LECH")})
        if not ok:
            lech.append(ma)
    out = {"lenh": "py -3 -B results/T-057/scripts/b12b_soat_so.py " + outp, "tai_lieu": [BC, DC],
           "so_muc": len(rows), "so_lech": len(lech), "lech": lech,
           "gioi_han": "Kiểm số trên đúng dòng có neo, số đứng tách biệt; số đếm nhỏ khớp theo mẫu câu (MAU). Không kiểm ý nghĩa câu. Đã thử đột biến trước khi chạy chính (LOG phiên 3).",
           "muc": rows}
    with open(outp, "x", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
    print(len(rows), "muc;", len(lech), "lech:", lech)
    for r in rows:
        if r["trang_thai"] != "KHOP":
            print(r)


if __name__ == "__main__":
    main(sys.argv[1])
