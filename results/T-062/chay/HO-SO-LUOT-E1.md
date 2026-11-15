# Hồ sơ lượt E1 (T-062) — trước khi phát

> Bản 2 (12/11/2026): sửa dòng xử lý lỗi M1 theo R5 `tasks/T-062-dem-chang-1-4/REVIEW.md` (Minh duyệt). Bản 1: `results/T-062/_ban-1/chay/HO-SO-LUOT-E1.md`. Lượt E1 đã chạy theo bản 1; 9/9 ca M1 thành công nên đường phục hồi không được dùng.

- **Lịch:** `lich.json` (khai 19:06Z, trước D2). 10 chu kỳ × 30 phút (10 nền / 10 lỗi / 10 hồi phục) ≈ 5 giờ + 3 phút M1 ca cuối. Ô không qua D2 bị bỏ ở `lich-sau-d2.json` kèm lý do; không thêm ô.
- **Tải:** AWS `3.24.8.49`, k6 1.4.2 (digest ghim), 5 req/s hỗn hợp 50/25/15/10, mỗi chu kỳ một container mới (đăng nhập PKCE mới, ngoài cửa sổ phương pháp). FLASH-HEALTHY: 5→15→5 req/s.
- **M1:** bản khóa P7 trên exp-obs (`stage-m1.py`, `run-m1.py` của T-058, adapter và config khớp hash khóa — `results/T-062/ca/_nguon/`). Mỗi ca: `t` = mốc can thiệp đã xác nhận (giây nguyên; ca bình thường/FLASH = mốc giữa), gói t±600 s, cửa sổ phương pháp [t−300, t+300), chạy 2 lần, kiểm trùng SHA. Chạy trong pha hồi phục của chính chu kỳ (sau t+750 s).
- **Cách ly nhãn:** M1 chỉ nhận `t`. Sổ `tiem-loi/so.jsonl` (hash nối dòng) và `nhat-ky.jsonl` có tên ô, không vào exp-obs. Mã ca 8 hex ngẫu nhiên. Đáp án chỉ ghép ở `e2.py --phat-lai` sau khi băm cả đợt.

## Gặp lỗi mới ở 10% / 50% / 99% (luật 21)

| Lỗi | Phạm vi chặn | Xử lý | Chạy lại gì | Thời gian mất |
|---|---|---|---|---|
| Bật lỗi của một ô thất bại (inj.py lỗi) | chỉ ô đó | ghi `fault-start-failed`, không chạy M1 cho chu kỳ, chu kỳ vẫn chạy hết để giữ nhịp | không tự chạy lại; ghi vào báo cáo | 0 (chu kỳ đó thành dữ liệu nền) |
| M1/stage/export lỗi trên một ca | chỉ ca đó | `M1 LỖI` trong nhật ký; dữ liệu capture vẫn trên exp-obs | **chưa có đường phục hồi đã kiểm** (bản 2, sửa R5 REVIEW.md): `stage-m1.py`/`run-m1.py` (T-058, đã ghim) tạo thư mục với `exist_ok=False` nên không gọi lại được cùng mã; ứng viên chưa kiểm: stage lại cùng `t` với mã mờ mới, giữ attempt cũ — cần wrapper tiếp nhận ở task sau, kiểm trước lượt dài | chưa ước lượng được (phụ thuộc giai đoạn hỏng) |
| Tải không khởi động (2 lần) | dừng lượt (hạ tầng) | dừng ở ranh giới, ghi `cycle-abort` | các chu kỳ còn lại, sau khi sửa tải | phần còn lại |
| Ứng dụng hỏng/OOM/restart giữa chu kỳ | chu kỳ đó | ghi lại; chu kỳ không dùng làm ca sạch (đánh dấu ở báo cáo bằng đầu dò/khởi động lại container) | không tự chạy lại | 30 phút nếu Minh muốn bù |
| Phát hiện sai **code tính toán** (stage/run/convert) | ảnh hưởng tính đúng → toàn bộ | dừng, trình Minh | chạy lại M1 trên gói đã đóng băng — cần mã mới hoặc wrapper tiếp nhận (chưa kiểm, xem dòng M1) | khoảng 4 s/ca chạy M1 khi đường này có; chưa tính phần đóng gói lại |
| Laptop mất nguồn/ngủ | dừng | tải chu kỳ đang chạy tự kết thúc (container 1800 s); toxic/hook tự hết (lease ≤180 s; CPU `timeout`; toxic **không** tự hết → `inj.py cleanup`) | tiếp từ chu kỳ kế tiếp | thời gian gián đoạn |
| STOP | dừng ở ranh giới | `inj.py cleanup`, Stop-Tai | — | — |

Ở 99%: các ca đã xong giữ nguyên, chỉ thiếu ca cuối; E2 chạy trên các ca đã có (đợt = các ca có M1). Ở 10% hay 50% như trên — không có lỗi nào buộc chạy lại chu kỳ đã xong trừ sai code tính toán (khi đó chạy lại M1 trên gói đã đóng băng; đường chạy lại chưa kiểm — dòng M1 ở trên).

**Điều kiện suy biến đã biết đã quét ở D2/A2:** tickets 500 cố định (nền); Booking quota 1 CPU có throttling nhẹ ở nền (cùng cho mọi chu kỳ); REDIS-BOOK có thể không có lưu lượng qua cache trong hỗn hợp cố định (D2 phân xử).
