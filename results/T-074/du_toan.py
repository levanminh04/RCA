import json, sys
CK = 31.39628955882353  # phút/chu kỳ, T-069 t069-chinh (17 chu kỳ)
D1, D3, DF = 648, 0.36*3*1800, 1512
CON_LAI, W45 = 73834, 26136
TY_LE_HT = 26166/40069
def pa(ten, o_loi, lap=3, muc=2, dc=(3,3,3), them=None):
    n_loi = o_loi*lap*muc
    n_x1 = o_loi*lap + dc[0]; n_x3 = o_loi*lap + dc[1]; n_fl = dc[2]
    n = n_loi + sum(dc)
    don = n_x1*D1 + n_x3*D3 + n_fl*DF
    return {"ten": ten, "so_o_loi": o_loi, "lap": lap, "muc_tai": muc,
            "chu_ky_loi": n_loi, "chu_ky_doi_chung": {"BINH-THUONG_x1": dc[0], "BINH-THUONG-X3": dc[1], "FLASH-HEALTHY": dc[2]},
            "chu_ky": n, "gio_thu": round(n*CK/60, 1),
            "don_bao_thu": round(don), "don_uoc_hoan_tat": round(don*TY_LE_HT),
            "du_suc_chua_bao_thu": don <= CON_LAI-W45, "du_suc_chua_uoc_hoan_tat": don*TY_LE_HT <= CON_LAI-W45}
P = [pa("A: SLOW-EVENT, POOL-BOOK, TICKET-PAUSE", 3), pa("A + CPU-EVENT", 4),
     pa("A + B (không CPU-EVENT)", 7), pa("A + B + CPU-EVENT", 8)]
nhom_b = {"ten": "nhóm đã phát triển, chế độ (b), 11 ô lỗi dev × 1 lần × ×1", "chu_ky": 11, "gio_thu": round(11*CK/60,1),
          "don_bao_thu": 11*D1, "tuy_chon": True}
def loi(n):
    h = n*CK/60
    return {f"{int(p*100)}%": {"chu_ky_da_thu": round(n*p,1), "gio_da_thu": round(h*p,1)} for p in (0.1,0.5,0.99)}
out = {
 "task": "T-074", "trang_thai": "ĐỀ XUẤT, chưa Minh duyệt; số có nguồn hoặc ghi CHƯA-KIỂM",
 "nguon": {
  "phut_moi_chu_ky": {"gia_tri": round(CK,2), "nguon": "results/T-069/thu/t069-chinh/chay/nhat-ky-3.jsonl: 'load started' đầu 09:35:34Z → 'Lượt thu xong' 18:29:18Z, 17 chu kỳ"},
  "don_chu_ky_x1": {"gia_tri": D1, "nguon": "results/T-069/thu/t069-chinh/tai-create-order.json (create_order 201)"},
  "don_chu_ky_x3_ca_chu_ky": {"gia_tri": D3, "nguon": "CHƯA-KIỂM: suy 0,36 đơn/s × 3 × 1800 s (results/T-071/e1/suc-chua.json#/nhu_cau_uoc/don_moi_giay_x1)"},
  "don_chu_ky_flash": {"gia_tri": DF, "nguon": "results/T-071/e1/suc-chua.json#/nhu_cau_uoc (ca 124242f0)"},
  "ve_con_lai": {"gia_tri": CON_LAI, "nguon": "results/T-071/e1/suc-chua.json#/con_lai (20/11 12:58Z)"},
  "W4_W5_toi_da": {"gia_tri": W45, "nguon": "results/T-071/e1/suc-chua.json#/nhu_cau_uoc/tong"},
  "ty_le_don_hoan_tat": {"gia_tri": round(TY_LE_HT,3), "nguon": "26.166 hoàn tất / 40.069 đơn (thong-nhat.md §1.2); đơn hủy/hết hạn trả vé — giả định CHƯA-KIỂM cho W7"},
  "v082_giay_moi_ca_hai_lan": {"gia_tri_tb": 49.9, "min": 23.96, "max": 92.98, "nguon": "nhat-ky-3.jsonl 'V082 xong' (16 ca)"}
 },
 "phuong_an": P, "nhom_da_phat_trien_b": nhom_b,
 "suc_chua": {"con_lai_sau_W4_W5_toi_da": CON_LAI-W45,
              "ghi_chu": "A+B vượt theo giả định bảo thủ; nâng sức chứa là sửa dữ liệu (Minh), chỉ ở E1 hoặc E6 (I13)"},
 "viec_them": {
  "pilot_xac_nhan_o_danh_gia": {"gio": 1.5, "trang_thai": "CHƯA-KIỂM: ~3,5 phút/ô theo chay_d2 (150 s tiêm + đầu dò + 30 s hồi), 2 mức tải, cộng khởi động tải"},
  "E6_do_khoi_phuc": {"gio": "2–3", "trang_thai": "CHƯA-KIỂM: dump ~300 MB (booking_db 189 MB, ticket_db 116 MB, lich-su/04 §2); thời gian pg_restore chưa đo; gồm 1 chu kỳ BINH-THUONG sau khôi phục"},
  "E6_tuy_chon_phan_xu_T069": {"gio": round(2*CK/60,1), "chu_ky": 2, "o": ["CPU-BOOK-1", "HTTP5-EVENT"]},
  "K2_khoi_phuc_moi_khoi": {"so_lan": "6–10", "gio_moi_lan": "CHƯA-KIỂM (đo ở E6)"},
  "K3_o_moc": {"chu_ky": 3, "gio": round(3*CK/60,1)},
  "rca_batch": {"phut_moi_ca_moi_che_do": "~5 (CHƯA-KIỂM)", "thanh_phan": "P7 ~1,5 + V082 ~0,8 + 2 bản che ~1,6 + DC-bo-quan-he ~0,8 + baseline ~0,5",
                "A_B_8_o_tuan_tu_gio": round(57*2*5/60,1), "song_song": "chia lô theo ca; chọn máy theo số pilot (luật 19)"}
 },
 "loi_giua_chung": {
  "pham_vi": "Phương án A+B+CPU-EVENT (57 chu kỳ); số tỉ lệ thuận cho phương án khác",
  "loi_cuc_bo_mot_chu_ky": {"anh_huong": "chỉ chu kỳ đó", "chay_lai": "1 chu kỳ bằng lịch con cuối đợt", "chi_phi_gio": round(CK/60,2), "giong_nhau_o_moi_ti_le": True},
  "loi_nguon_chung_khong_kiem_moi_chu_ky": {"mo_ta": "mất telemetry, Prometheus khởi động lại, sai proxy/cấu hình tải, khôi phục DB sai — phát hiện muộn", "mat": loi(57)},
  "loi_nguon_chung_co_kiem_moi_chu_ky": {"mo_ta": "kiểm §8.4 điều kiện 3–5 sau mỗi chu kỳ", "mat_toi_da_chu_ky": 2, "mat_toi_da_gio": round(2*CK/60,1), "giong_nhau_o_moi_ti_le": True,
                                       "gioi_han": "lỗi mà phép kiểm không bắt (ví dụ sai code đóng gói vẫn ra gói hợp lệ về hình thức) vẫn lan như dòng trên"},
  "loi_phuong_phap_o_T3": {"anh_huong": "chỉ slot ca × phương pháp × chế độ", "chay_lai": "slot bị ảnh hưởng, phút tính toán; không thu lại", "quy_tac": "quy tắc phân loại lỗi tách khỏi vân tay code tính toán (SL38)"},
  "loi_khoi_phuc_K2": {"anh_huong": "cả khối (6–9 chu kỳ) nếu không kiểm sau khôi phục", "phong_ngua": "kiểm nhất quán sau mỗi lần khôi phục trước chu kỳ đầu khối"},
  "het_han_ban_hoac_het_ve": {"anh_huong": "mọi chu kỳ sau mốc", "phong_ngua": "kiểm trước đợt: hạn bán > giờ kết thúc dự kiến + 24 giờ; vé còn > nhu cầu bảo thủ"},
  "mat_mang_laptop": {"anh_huong": "0 (lịch giao server)", "nguon": "thong-nhat.md §1.5"},
  "chay_lai_toan_bo_khi": "sai code tính toán hoặc sai nguồn ảnh hưởng tính đúng; trình Minh lý do và chi phí trước"
 }
}
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for p in P: print(p["ten"], p["chu_ky"], p["gio_thu"], p["don_bao_thu"], p["don_uoc_hoan_tat"], p["du_suc_chua_bao_thu"], p["du_suc_chua_uoc_hoan_tat"])
print(CON_LAI-W45, loi(57), round(57*2*5/60,1))
