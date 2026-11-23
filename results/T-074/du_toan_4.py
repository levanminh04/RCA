# T-074 bản 4: dự toán tự đủ (thay du-toan.json, du-toan-3.json). Chạy: py -3 -I du_toan_4.py du-toan-4.json
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
CK = 31.39628955882353          # phút/chu kỳ, T-069 t069-chinh, 17 chu kỳ
D1, D3, DF = 648, 1944, 1512    # đơn/chu kỳ ×1, ×3 (khỏe 0bec9eca), flash
CON_LAI = 73834 - 26136 - 648 - 648
TY = 26166 / 40069
KEO_DAI_S = 90
def pa(ten, o, k3_them):
    bt1 = 3 + (3 if k3_them else 0)
    n = o * 6 + bt1 + 3 + 3
    don = (o * 3 + bt1) * D1 + (o * 3 + 3) * D3 + 3 * DF
    khoi = o * 2 + 3 + (1 if k3_them else 0)
    return {"ten": ten, "so_o_loi": o, "k3": "thêm 3 chu kỳ mốc" if k3_them else "dùng lại 3 đối chứng ×1 làm mốc",
            "chu_ky": n, "gio_thu_co_so": round(n * CK / 60, 1),
            "gio_neu_keo_dai_tai_90s": round(n * (CK + KEO_DAI_S / 60) / 60, 1),
            "chu_ky_moi_khoi": khoi, "so_khoi": 3,
            "K0_don_ca_dot_bao_thu": don, "K0_don_ca_dot_uoc_hoan_tat": round(don * TY),
            "K0_du_bao_thu": don <= CON_LAI, "K0_du_uoc_hoan_tat": don * TY <= CON_LAI,
            "K2_don_khoi_lon_nhat_bao_thu": round(don / 3),
            "loi_khi_khong_kiem_moi_chu_ky_gio": {f"{int(p*100)}%": round(n * CK / 60 * p, 1) for p in (0.1, 0.5, 0.99)},
            "loi_khoi_phuc_K2_hong_mat_toi_da_chu_ky": khoi}
P = [pa(t, o, k) for t, o in [("A", 3), ("A + CPU-EVENT", 4), ("A + B", 7), ("A + B + CPU-EVENT", 8)] for k in (False, True)]
out = {
 "task": "T-074", "ban": 4,
 "trang_thai": "ĐỀ XUẤT. Dự toán tại mốc E1 sau D1 và lượt E3; số vé thật đọc lại ở E6. Tự đủ: không kế thừa mục nào của bản trước.",
 "het_hieu_luc": ["du-toan.json (toàn bộ)", "du-toan-3.json (toàn bộ)",
   "riêng: du-toan.json#/loi_giua_chung/loi_khoi_phuc_K2 (6–9 chu kỳ), #/viec_them/K2_khoi_phuc_moi_khoi, #/viec_them/E6_do_khoi_phuc, #/viec_them/E6_tuy_chon_phan_xu_T069 (đã rút, bản 3 §G); du-toan-3.json#/loi_K2_moi_khoi/ghi_chu (11–20)"],
 "nguon": {
  "phut_moi_chu_ky": {"gia_tri": round(CK, 2), "nguon": "results/T-069/thu/t069-chinh/chay/nhat-ky-3.jsonl, 17 chu kỳ"},
  "don_x1": {"gia_tri": D1, "nguon": "results/T-069/thu/t069-chinh/tai-create-order.json (ca ×1)"},
  "don_x3": {"gia_tri": D3, "nguon": "tai-create-order.json#/0bec9eca/201 (×3 khỏe); ca lỗi ×3 785bfd0c = 1765; 1944 là cận trên"},
  "don_flash": {"gia_tri": DF, "nguon": "tai-create-order.json#/124242f0/201"},
  "ve_con_lai_cho_W7": {"gia_tri": CON_LAI, "cong_thuc": "73834 (E1) − 26136 (E2+E4 8 lượt+E5) − 648 (D1) − 648 (lượt dương E3)", "nguon": "results/T-071/e1/suc-chua.json; LOG T-070 lượt 6 (D1)"},
  "ty_le_hoan_tat": {"gia_tri": round(TY, 3), "nguon": "26166/40069 (thong-nhat.md §1.2); CHƯA-KIỂM cho W7"},
  "v082_giay_hai_lan": {"gia_tri": 49.9, "nguon": "nhat-ky-3.jsonl 'V082 xong', 16 ca"}},
 "phuong_an": P,
 "dinh_nghia_khoi": "1 khối = 1 lần mỗi cặp (ô, mức tải) + 3 đối chứng (+1 mốc nếu thêm K3); 3 lần lặp ⇒ 3 khối; K2 khôi phục trước mỗi khối ⇒ 3 lần",
 "suc_chua_cach_so": "K0: so K0_don_ca_dot với ve_con_lai_cho_W7. K2: so K2_don_khoi_lon_nhat với vé còn tại mốc khôi phục; chỉ dùng sau khi E6 xác nhận khôi phục tồn kho nhất quán",
 "cho_goi_b": {"bat_dong_bo_gio": 0, "keo_dai_tai_moi_chu_ky_s": KEO_DAI_S, "ghi_chu": "thiet-ke-w6-4.md §6; chọn ở câu 9 cau-hoi-minh-4.md"},
 "viec_them": {
  "pilot_xac_nhan_o_va_x3": {"gio": 2.0, "trang_thai": "CHƯA-KIỂM: chay_d2 ~3,5 phút/ô × 2 mức tải + khởi động tải; thêm đo flush_F ở ×3 (thiet-ke-w6-4.md §6)"},
  "E6": {"gio": "1,5–3,0", "nguon": "e6-spec-nhap.md §Chi phí; gồm 0,5 giờ nếu chạy 1 chu kỳ BINH-THUONG sau khôi phục"},
  "rca_batch": {"phut_moi_ca_moi_che_do": "~5 (CHƯA-KIỂM)", "thanh_phan": "P7 ~1,5; V082 ~0,8; 2 bản che ~1,6; DC-bo-quan-he ~0,8; baseline ~0,5"}},
 "loi_giua_chung_chung": {
  "loi_cuc_bo_mot_chu_ky": {"chi_phi_gio": round(CK / 60, 2), "xu_ly": "bù 1 lần chỉ khi xác nhận chưa tiêm hoặc hỏng đường thu có bằng chứng độc lập (thiet-ke-w6-4.md §2; bản 3 §B.1)"},
  "loi_nguon_chung_co_kiem_moi_chu_ky": {"mat_toi_da_chu_ky": 2, "mat_toi_da_gio": round(2 * CK / 60, 1)},
  "loi_phuong_phap_T3": "chỉ slot ca × phương pháp × chế độ; không thu lại",
  "mat_mang_laptop": 0}}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(CON_LAI)
for p in P: print(p["ten"], "|", p["k3"][:8], p["chu_ky"], p["gio_thu_co_so"], p["gio_neu_keo_dai_tai_90s"], p["chu_ky_moi_khoi"], p["K0_don_ca_dot_bao_thu"], p["K2_don_khoi_lon_nhat_bao_thu"], p["K0_du_bao_thu"], p["K0_du_uoc_hoan_tat"])
