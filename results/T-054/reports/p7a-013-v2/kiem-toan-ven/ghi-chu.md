# Luồng A — kiểm toàn vẹn số liệu P7(a), 08/11/2026

Script `kiem.py` chỉ đọc. Kết quả ở `ket-qua.json`.

| Phép kiểm | Kết quả | Con trỏ |
|---|---|---|
| Chấm lại độc lập 1282 hàng world P: nhãn lấy từ CSV G1, scorer viết lại từ đặc tả hòa, không import `cham.py` hay `danh_gia` | 0 lệch; chênh lớn nhất = 0 ở rr, hit@1/3/5, ndcg@5; không cần Monte Carlo | `ket-qua.json#/A1_cham_lai_doc_lap` |
| A4 tái lập từ số độc lập | TT Δ = 0,044027…, OB ΔHit@5 = 3/34, trùng `a4.json` | `#/A1_cham_lai_doc_lap/A4_TT_delta`, `/A4_OB_delta_hit5` |
| Rò nhãn trong job/invocation/launch (4206 file) | Không có tên ca G1, đường dẫn riêng hay chuỗi `<root>_<fault>` | `#/A3_ro_nhan` |
| Thử giả | Không có bản ghi suy biến một khối. Xếp theo chữ cái và ngẫu nhiên đều cho MRR ở mức ngẫu nhiên. Xáo root giữa các ca: TT 0,17 (5 service gốc của TT luôn bất thường hơn trung bình), OB ≈ ngẫu nhiên | `#/A2_thu_gia` |
| Số trong báo cáo | 4 lỗi làm tròn hai lần, đã sửa trong `bao-cao.md`: TraceRCA OB 0,494 → 0,493; C-d2 OB 0,878 → 0,877; CI M1−C-d2 OB hi 0,041 → 0,040; CI M1−C-g OB lo 0,087 → 0,086. Không đổi kết luận | `#/A5_fail` (bản kiểm phát hiện); soát máy §4 (146 số) và §5 (75 số) sau sửa: hết lệch |

**Giới hạn.**
- Chấm lại độc lập kiểm phép chấm và phép ghép nhãn, không kiểm đầu ra phương pháp có đúng hay không. Phần đó thuộc kiểm tái lập/parity của các task trước.
- Phép so dev ↔ test ở OB chưa so được: số dev T-052 đo trước bản vá adapter 008. Trong lượt này không có số dev sau bản vá ở cấp bảng, nên giữ OPEN.

**Đính chính (08/11/2026, đáp REVIEW R1).** Dòng "Số trong báo cáo" ở trên trỏ cả 4 lỗi về `#/A5_fail`. Thực ra `A5_fail` chỉ có lỗi C-d2. 3 lỗi còn lại đến từ lần soát máy trước đây không lưu file; nay đã lưu ở `soat_bang.py` → `soat-bang.json`: bản gốc `../bao-cao-ban-dau.md` lệch 4/221 ô, bản hiện hành lệch 0/221. Việc sửa tại chỗ `bao-cao.md` là ghi ngoài phạm vi; xem `../dinh-chinh-001.md` Đ1.
