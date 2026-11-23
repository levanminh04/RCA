# T-074 bản 3: dự toán sau D1 + lượt E3 (CX-08 điểm 5). Chạy: py -3 -I du_toan_3.py du-toan-3.json
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
CK = 31.39628955882353
D1, D3, DF = 648, 1944, 1512
CON_LAI_E1, W45_E1, THEM_D1, THEM_E3 = 73834, 26136, 648, 648
TY_LE_HT = 26166/40069
CON_LAI = CON_LAI_E1 - W45_E1 - THEM_D1 - THEM_E3
def pa(ten, o, k3_them):
    n_loi = o*3*2; dc = {"BINH-THUONG_x1": 3 + (3 if k3_them else 0), "BINH-THUONG-X3": 3, "FLASH-HEALTHY": 3}
    n = n_loi + sum(dc.values())
    don = (o*3 + dc["BINH-THUONG_x1"])*D1 + (o*3 + 3)*D3 + 3*DF
    return {"ten": ten, "k3": "thêm 3 chu kỳ mốc" if k3_them else "dùng lại 3 đối chứng ×1 làm mốc",
            "chu_ky": n, "gio_thu": round(n*CK/60, 1), "khoi_K2": {"so_khoi": 3, "chu_ky_moi_khoi": o*2 + 3 + (1 if k3_them else 0), "so_lan_khoi_phuc": 3},
            "don_bao_thu": don, "don_uoc_hoan_tat": round(don*TY_LE_HT), "du_bao_thu": don <= CON_LAI, "du_uoc_hoan_tat": don*TY_LE_HT <= CON_LAI}
P = []
for ten, o in [("A", 3), ("A + CPU-EVENT", 4), ("A + B", 7), ("A + B + CPU-EVENT", 8)]:
    P += [pa(ten, o, False), pa(ten, o, True)]
out = {"task": "T-074", "ban": 3, "trang_thai": "ĐỀ XUẤT; dự toán tại mốc E1 sau D1 và lượt E3; số vé thật phải đọc lại ở E6",
 "thay_cho": "du-toan.json#/phuong_an, #/suc_chua, #/viec_them/K2_khoi_phuc_moi_khoi, #/viec_them/K3_o_moc (các mục khác của du-toan.json giữ nguyên)",
 "nguon": {"phut_moi_chu_ky": round(CK, 2),
  "don_x1": {"gia_tri": D1, "nguon": "results/T-069/thu/t069-chinh/tai-create-order.json (ca ×1)"},
  "don_x3": {"gia_tri": D3, "nguon": "tai-create-order.json#/0bec9eca/201 (BINH-THUONG-X3, khỏe) = 1944; ca lỗi ×3 785bfd0c = 1765 — dùng 1944 làm cận trên, chưa có căn cứ mọi ô ×3 đạt số này"},
  "don_flash": {"gia_tri": DF, "nguon": "tai-create-order.json#/124242f0/201"},
  "ve_con_lai_E1": {"gia_tri": CON_LAI_E1, "nguon": "results/T-071/e1/suc-chua.json#/con_lai"},
  "W4_W5_E1": {"gia_tri": W45_E1, "nguon": "results/T-071/e1/suc-chua.json#/nhu_cau_uoc/tong"},
  "them_D1": {"gia_tri": THEM_D1, "nguon": "D1: E4 thêm 1 lượt ×1 1800 s (LOG T-070 lượt 6); 648 đơn theo mô hình ×1"},
  "them_E3": {"gia_tri": THEM_E3, "nguon": "lượt dương E3 ×1 1800 s (LOG T-070); 648 đơn theo mô hình"},
  "ty_le_hoan_tat": round(TY_LE_HT, 3)},
 "con_lai_cho_W7_theo_mo_hinh": CON_LAI,
 "phuong_an": P,
 "dinh_nghia_khoi": "một khối = một lần của mỗi cặp (ô, mức tải) + 3 đối chứng (+1 ô mốc nếu thêm K3); 3 lần lặp ⇒ 3 khối. K2 khôi phục trước mỗi khối ⇒ 3 lần (thay '6–10 lần, khối 6–9 chu kỳ' của bản 1–2)",
 "K2_moc": "mốc K2 phải là dump chụp ở E6 SAU khi sửa hạn bán và sức chứa; dump E1 (moc-db.json#/kho_ticket_type: sức chứa 100.000) sẽ đưa hệ về giá trị cũ",
 "loi_K2_moi_khoi": {"mat_toi_da_chu_ky": None, "ghi_chu": "khôi phục hỏng không phát hiện ⇒ mất cả khối (11–20 chu kỳ tùy phương án); kiểm nhất quán sau khôi phục trước chu kỳ đầu khối"}}
out["loi_K2_moi_khoi"]["mat_toi_da_chu_ky"] = {p["ten"] + " / " + p["k3"]: p["khoi_K2"]["chu_ky_moi_khoi"] for p in P}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(CON_LAI)
for p in P: print(p["ten"], p["k3"][:8], p["chu_ky"], p["gio_thu"], p["khoi_K2"]["chu_ky_moi_khoi"], p["don_bao_thu"], p["don_uoc_hoan_tat"], p["du_bao_thu"], p["du_uoc_hoan_tat"])
