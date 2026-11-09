"""B12 T-057: soát số của ho-so-g4.md và bao-cao-tien-do-co.md với file nguồn. Chỉ đọc.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/b12_soat_so.py results/T-057/soat-so.json
Mỗi mục: (mã, file, con trỏ JSON, số chữ số thập phân hoặc None cho số nguyên/chuỗi, tài liệu phải chứa).
Giá trị đọc từ file → định dạng kiểu Việt (dấu phẩy thập phân, làm tròn nửa lên) → phải có mặt nguyên chuỗi trong tài liệu.
Một mục LECH khi chuỗi định dạng không có trong tài liệu được khai. Không suy ngược từ tài liệu.
Con trỏ: phần tử phân tách bằng "/", khóa có "/" viết "~1". Hậu tố "|neg" đổi dấu, "|sub:a,b" lấy a − b của hai con trỏ.
"""
import json
import sys
from decimal import Decimal, ROUND_HALF_UP

HS = "results/T-057/ho-so-g4.md"
BC = "results/T-057/bao-cao-tien-do-co.md"
F = {
    "A": "results/T-054/reports/main-013-v2/a4.json",
    "PT": "results/T-054/reports/p7a-013-v2/phan-tich-nhom.json",
    "R": "results/T-055/reports/re3/phan-tich-re3.json",
    "K2": "results/T-056/ket-qua-002.json",
    "SCB": "results/T-057/so-cong-bo.json",
    "KPX": "results/T-057/kha-nang-phan-xu.json",
    "E5": "results/T-057/e5-thanh-phan.json",
    "VV": "results/T-057/vung-ve-bo-quan-he.json",
    "DT": "results/T-057/dev-test.json",
    "TV": "results/T-057/truy-vet-han-che.json",
    "BD": "results/T-057/ban-do-dieu-kien.json",
    "MZ": "results/T-057/maxz-dev.json",
    "DO": "results/T-057/do-thi-dt18.json",
    "B0": "results/T-057/b0-kiem-hash.json",
}
H, B, HB = [HS], [BC], [HS, BC]
REG = [
    # §0 / §5.1: A4 và mốc
    ("A4_TT_delta", "A", "/TT/P/delta", 3, HB),
    ("A4_TT_lo", "A", "/TT/P/E04/raw/lo", 3, HB),
    ("A4_TT_hi", "A", "/TT/P/E04/raw/hi", 3, HB),
    ("A4_OB_delta", "A", "/OB/P/delta", 3, H),
    ("RE3_M1_M4_delta", "R", "/so_cap/M1-simplerca|rr/delta", 3, H),
    ("RE3_M1_M4_abs", "R", "/so_cap/M1-simplerca|rr/delta|abs", 3, B),
    # §2 bảng chính
] + [
    (f"bang_{ds}_{ve}_{k}", "SCB", f"/bang/{ds}/{ve}/{k}", 3, H)
    for ds in ("RE2-TT", "Nezha-OB", "RE3-OB")
    for ve in ("M1", "C-a0", "simplerca", "baro")
    for k in ("rr", "hit@1", "avg@5")
] + [
    (f"bang_{ds}_torai_{k}", "SCB", f"/bang/{ds}/torai_B/{k}", 3, H) for ds in ("RE2-TT", "RE3-OB") for k in ("rr", "hit@1", "avg@5")
] + [
    (f"ndcg_{ds}_{ve}", "SCB", f"/bang/{ds}/{ve}/ndcg@5", 3, B)
    for ds in ("RE2-TT", "Nezha-OB", "RE3-OB") for ve in ("M1", "C-a0", "simplerca", "baro")
] + [
    ("ndcg_TT_torai", "SCB", "/bang/RE2-TT/torai_B/ndcg@5", 3, B),
    ("ndcg_RE3_torai", "SCB", "/bang/RE3-OB/torai_B/ndcg@5", 3, B),
    ("bang_RE2-TT_C-d2_rr", "SCB", "/bang/RE2-TT/C-d2/rr", 3, H),
    ("bang_Nezha-OB_C-d2_rr", "SCB", "/bang/Nezha-OB/C-d2/rr", 3, H),
    ("bang_RE3-OB_C-d2_rr", "R", "/bang_theo_ve_P/C-d2/rr", 3, H),
    ("bang_RE3-OB_C-d2_hit1", "R", "/bang_theo_ve_P/C-d2/hit@1", 3, H),
    ("SR90_hit1", "SCB", "/simplerca_RE2_TT_90_ca/hit@1", 3, H),
    # §4 câu 2
    ("TT_o_khac0", "KPX", "/A4/TT/o_khac_0", None, H),
    ("OB_M1_M4_o", "KPX", "/cap_MRR/Nezha-OB/M1-simplerca/o_khac_0", None, H),
    ("OB_M1_Ca0_o", "KPX", "/cap_MRR/Nezha-OB/M1-C-a0/o_khac_0", None, H),
    ("RE3_M1_M4_o", "KPX", "/cap_MRR/RE3-OB/M1-simplerca/o_khac_0", None, H),
    ("R1_TT", "K2", "/tom_tat/RE2-TT/root_events_hon_moi_service_khac", None, HB),
    ("R1_RE3", "K2", "/tom_tat/RE3-OB/root_events_hon_moi_service_khac", None, HB),
    # OB MRR cặp
    ("OB_M1_M4_dMRR", "PT", "/so_cap/Nezha-OB|M1-simplerca|RR/delta_mean/xap_xi", 3, B),
    ("OB_M1_Ca0_dMRR_C-a0", "SCB", "/bang/Nezha-OB/C-a0/rr", 3, HB),
    ("OB_M1_bo_E2", "PT", "/so_cap/Nezha-OB|M1-bo-E2|RR/delta_mean/xap_xi", 3, H),
    ("OB_M1_Cd2", "PT", "/so_cap/Nezha-OB|M1-C-d2|RR/delta_mean/xap_xi", 4, H),
    ("RE3_M1_Cd2", "R", "/so_cap/M1-C-d2|rr/delta", 3, H),
    ("RE3_M1_Cd1", "R", "/so_cap/M1-C-d1|rr/delta", 3, H),
    # nhóm lỗi, vị trí
    ("OB_nd_M1", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/M1", 3, HB),
    ("OB_nd_Ca0", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/C-a0", 3, HB),
    ("OB_nd_M4", "PT", "/tach_MRR/Nezha-OB|fault/network_delay/simplerca", 3, HB),
    ("OB_exc_M1", "PT", "/tach_MRR/Nezha-OB|fault/exception/M1", 3, H),
    ("OB_exc_M4", "PT", "/tach_MRR/Nezha-OB|fault/exception/simplerca", 3, H),
    ("OB_ret_M1", "PT", "/tach_MRR/Nezha-OB|fault/return/M1", 3, None),
    ("OB_ret_Ca0", "PT", "/tach_MRR/Nezha-OB|fault/return/C-a0", 3, H),
    ("OB_ret_M4", "PT", "/tach_MRR/Nezha-OB|fault/return/simplerca", 3, H),
    ("OB_nguon_M1", "PT", "/tach_MRR/Nezha-OB|vi_tri_N_p75/nguồn/M1", 3, HB),
    ("OB_nguon_M4", "PT", "/tach_MRR/Nezha-OB|vi_tri_N_p75/nguồn/simplerca", 3, HB),
    ("TT_loss_torai", "PT", "/tach_MRR/RE2-TT|fault/loss/torai_B", 3, H),
    # E5, vùng, đồ thị
    ("E5_TT_t2", "E5", "/bo/RE2-TT/tong_tang2", None, H),
    ("E5_OB_t2", "E5", "/bo/Nezha-OB/tong_tang2", None, H),
    ("E5_RE3_t2", "E5", "/bo/RE3-OB/tong_tang2", None, H),
    ("E5_RE3_ca", "E5", "/bo/RE3-OB/ca_co_tang2", None, H),
    ("VV_TT_M1_p", "VV", "/tom_tat/RE2-TT/M1/cach_1/ty_le_chua_root_ky_vong", 3, HB),
    ("VV_OB_M1_p", "VV", "/tom_tat/Nezha-OB/M1/cach_1/ty_le_chua_root_ky_vong", 3, HB),
    ("VV_RE3_M1_p", "VV", "/tom_tat/RE3-OB/M1/cach_1/ty_le_chua_root_ky_vong", 3, HB),
    ("VV_TT_M1_co", "VV", "/tom_tat/RE2-TT/M1/cach_1/co_ky_vong", 2, H),
    ("VV_OB_M1_co", "VV", "/tom_tat/Nezha-OB/M1/cach_1/co_ky_vong", 2, H),
    ("VV_TT_Ca0_co", "VV", "/tom_tat/RE2-TT/C-a0/cach_1/co_ky_vong", 2, H),
    ("VV_OB_Ca0_p", "VV", "/tom_tat/Nezha-OB/C-a0/cach_1/ty_le_chua_root_ky_vong", 3, H),
    ("VV_OB_Ca0_co", "VV", "/tom_tat/Nezha-OB/C-a0/cach_1/co_ky_vong", 2, H),
    ("VV_RE3_Ca0_co", "VV", "/tom_tat/RE3-OB/C-a0/cach_1/co_ky_vong", 2, H),
    ("VV_TT_boE5_p", "VV", "/tom_tat/RE2-TT/bo-E5/cach_1/ty_le_chua_root_ky_vong", 3, H),
    ("VV_kiem", "VV", "/kiem_tai_dung_tren_ban_ghi_co_E7/khop", None, H),
    ("DO_TT_nut", "DO", "/bo/RE2-TT|M1/so_nut_co_canh_hop", None, H),
    ("DO_TT_canh", "DO", "/bo/RE2-TT|M1/so_canh_hop", None, H),
    ("DO_TT_tt", "DO", "/bo/RE2-TT|M1/so_thuc_the_hop", None, H),
    ("DO_TT_T12_nut", "DO", "/bo/RE2-TT|T12-on/so_nut_co_canh_hop", None, H),
    ("DO_TT_T12_canh", "DO", "/bo/RE2-TT|T12-on/so_canh_hop", None, H),
    ("DO_RE3_tt", "DO", "/bo/RE3-OB|M1/so_thuc_the_hop", None, H),
    # truy vết, bản đồ
    ("TV_OB_Ca0_sai", "TV", "/dem/Nezha-OB|C-a0/sai", None, H),
    ("TV_OB_Ca0_tt", "TV", "/dem/Nezha-OB|C-a0/doi_thu_truc_tiep_goi_root", None, HB),
    ("TV_OB_M1_tt", "TV", "/dem/Nezha-OB|M1/doi_thu_truc_tiep_goi_root", None, None),
    ("BD_kenh_hep", "BD", "/ca_theo_nhan/kenh_hep_doi_thu|len", None, HB),
    ("BD_R1", "BD", "/R1_dung_o_ca_M1_sai/so", None, H),
    ("BD_Ca0", "BD", "/C_a0_dung_o_ca_M1_sai", None, H),
    # dev-test
    ("DT_TT_Ca0", "DT", "/so_sanh_M1_tru_ve/RE2-TT/C-a0/dev_delta", 3, H),
    ("DT_OB_Ca0", "DT", "/so_sanh_M1_tru_ve/Nezha-OB/C-a0/dev_delta", 3, H),
    ("DT_TT_boE1", "DT", "/so_sanh_M1_tru_ve/RE2-TT/bo-E1/dev_delta", 3, H),
    ("DT_TT_boE2", "DT", "/so_sanh_M1_tru_ve/RE2-TT/bo-E2/dev_delta", 3, H),
    ("DT_TT_boE5", "DT", "/so_sanh_M1_tru_ve/RE2-TT/bo-E5/dev_delta", 3, H),
    ("DT_OB_boE2", "DT", "/so_sanh_M1_tru_ve/Nezha-OB/bo-E2/dev_delta", 3, H),
    ("DT_OB_boE5", "DT", "/so_sanh_M1_tru_ve/Nezha-OB/bo-E5/dev_delta", 3, H),
    ("DT_OB_Cd2", "DT", "/so_sanh_M1_tru_ve/Nezha-OB/C-d2/dev_delta", 3, H),
    ("DT_OB_SR", "DT", "/so_sanh_M1_tru_ve/Nezha-OB/simplerca/dev_delta", 3, H),
    ("DT_TT_SR", "DT", "/so_sanh_M1_tru_ve/RE2-TT/simplerca/dev_delta", 3, H),
    ("DT_TT_Ca0_dev", "DT", "/bang_MRR/RE2-TT/C-a0/dev_MRR", 3, H),
    ("DT_TT_M1_dev", "DT", "/bang_MRR/RE2-TT/M1/dev_MRR", 3, H),
    ("DT_TT_boE2_dev", "DT", "/bang_MRR/RE2-TT/bo-E2/dev_MRR", 3, H),
    ("DT_OB_Ca0_dev", "DT", "/bang_MRR/Nezha-OB/C-a0/dev_MRR", 3, H),
    ("DT_kiem", "DT", "/kiem_cau_hinh_OB/so_trung_RR", None, H),
    # C-e
    ("CE_ok", "KPX", "/H7/C_e_TT/n_OK", None, H),
    ("CE_N1", "KPX", "/H7/C_e_TT/N1_mean", 1, H),
    ("CE_RR", "KPX", "/H7/C_e_TT/future_root_MRR", 3, H),
    ("CE_chance", "KPX", "/H7/C_e_TT/chance_returned_MRR", 3, H),
    # B0
    ("B0_khop", "B0", "/so_khop", None, H),
    ("B0_tong", "B0", "/so_file_kiem", None, H),
    # max-z dev
    ("MZ_sai", "MZ", "/OB_dev/theo_huong/sai", None, None),
    ("MZ_dung_hep", "MZ", "/OB_dev/theo_huong/dung_root_thang_bang_kenh_hep", None, None),
]


def get(obj, ptr):
    lay_abs = ptr.endswith("|abs")
    if lay_abs:
        ptr = ptr[:-4]
    for p in ptr.strip("/").split("/"):
        p = p.replace("~1", "/").replace("~0", "~")
        if p.endswith("|len"):
            obj = len(obj[p[:-4]])
            continue
        obj = obj[int(p)] if isinstance(obj, list) else obj[p]
    if isinstance(obj, dict) and "phan_so" in obj:
        obj = obj["phan_so"][0] / obj["phan_so"][1]
    if isinstance(obj, str):
        obj = float(obj)
    return abs(obj) if lay_abs else obj


def fmt(v, nd):
    if nd is None:
        return str(v)
    d = Decimal(str(v)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP)
    s = format(d, "f")
    if s.startswith("-0") and Decimal(s) == 0:
        s = s[1:]
    return s.replace("-", "−").replace(".", ",")


def main(outp):
    cache = {k: json.load(open(p, encoding="utf-8")) for k, p in F.items()}
    docs = {p: open(p, encoding="utf-8").read() for p in (HS, BC)}
    rows, lech = [], []
    for ma, f, ptr, nd, where in REG:
        try:
            v = get(cache[f], ptr)
        except Exception as e:  # noqa: BLE001
            rows.append({"ma": ma, "file": F[f], "con_tro": ptr, "trang_thai": "KHONG_DOC_DUOC", "loi": repr(e)})
            lech.append(ma)
            continue
        s = fmt(v, nd)
        cands = {s}
        if s.startswith("−"):
            cands.add("−" + s[1:]); cands.add("-" + s[1:])
        found = {}
        for doc in (where or []):
            found[doc] = any(c in docs[doc] for c in cands)
        ok = all(found.values()) if where else True
        rows.append({"ma": ma, "file": F[f], "con_tro": ptr, "gia_tri": v, "chuoi": s, "co_trong": found,
                     "trang_thai": "KHOP" if ok else "LECH"})
        if not ok:
            lech.append(ma)
    out = {"lenh": "py -3 -B results/T-057/scripts/b12_soat_so.py " + outp, "tai_lieu": [HS, BC],
           "so_muc": len(rows), "so_lech": len(lech), "lech": lech,
           "gioi_han": "Soát số có mặt trong tài liệu; không chứng minh số được đặt đúng câu. Số đếm viết tay (ví dụ 8 → 0, 2/124) đối chiếu ở mục đánh dấu where=None hoặc kiểm tay, ghi LOG.",
           "muc": rows}
    with open(outp, "x", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
    print(len(rows), "muc;", len(lech), "lech:", lech)
    for r in rows:
        if r["trang_thai"] != "KHOP":
            print(r)


if __name__ == "__main__":
    main(sys.argv[1])
