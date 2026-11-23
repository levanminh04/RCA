# T-069 — Đính chính 2 (theo phản biện kiểm lại CX-05 F1–F4; Minh duyệt 20/11/2026 "Duyệt cả năm", mục D5)

Không đổi kết quả W3 (`bang-theo-o-2.json`; CX-05 chấm lại độc lập: V082 AC@1 9 → 9, AC@3 11 → 11, hạng cắt 13 → 14, K 4 → 4; CPU-BOOK-1 hạng 3 ở lượt chính và lượt lặp). File gốc và `dinh-chinh-1.md` giữ nguyên, đã ghim trong `SHA256SUMS`/`SHA256SUMS-2`. Chỗ nào file này mâu thuẫn với `dinh-chinh-1.md` thì theo file này. Nguồn phản biện: `results/T-070/codex/CX-05-tin-cuoi.md` (thread `01a1faec-3f75-7222-b402-af3eaa4e487a`).

## 1. Năm thao tác Booking không phải "kênh chỉ có ở bản ghim" (F1)

Thay câu `dinh-chinh-1.md` §2 "kênh chỉ có ở bản ghim gồm `INSERT tbl_orders`, `INSERT tbl_order_items`, `SELECT/UPDATE tbl_purchase_limits`, `POST /internal/v1/orders/{orderId}/purchase-snapshot` …":

> Năm thao tác này **đã có ở ca cũ** và **mới có cờ bất thường ở ca mới**. `phan_tich_o.py` trừ hai tập (đơn vị, hướng) lấy từ `extra.kenh_co`, tức tập kênh *có cờ*, không phải tập kênh *hiện diện*.

Kiểm (người làm, 20/11 ~22:04Z, chạy lại độc lập): đọc `results/T-063/thu2/ca/19b17e22.tgz` → `outputs/19b17e22/method-input.json` mảng `[0]` (194.714 span), đếm `owner == "booking-service"` theo `operation`: `INSERT booking_schema.tbl_orders` 216, `INSERT booking_schema.tbl_order_items` 216, `SELECT booking_schema.tbl_purchase_limits` 428, `UPDATE booking_schema.tbl_purchase_limits` 428, `POST /internal/v1/orders/{orderId}/purchase-snapshot` 144 — trùng số của CX-05.

Giữ: code Booking **có đổi** giữa `6b21ed55` và `36a3725d` (`OrderRepository.java`; mẫu `select distinct …` chỉ có ở bản mới). Thay đổi code vẫn là **ứng viên** nguồn mẫu đuôi; ảnh hưởng riêng chưa tách được vì image, trạng thái DB và thời điểm thu cùng đổi.

## 2. "Hai cách khớp ở các kênh SQL lá" là sai (F2)

Thay câu `dinh-chinh-1.md` §3 "Hai cách khớp ở các kênh SQL lá đã liệt kê (span không có con)":

> Ngay ở kênh SQL lá, điểm thô của `z_kiem.py` và điểm M1 (E1-U) **có thể khác**: adapter đưa hai đầu span về micro giây nguyên trước khi lấy hiệu (`src/m1/adapter_flashticket.py:217`), còn `z_kiem.py` lấy hiệu ở nano giây và chia cửa sổ theo lúc bắt đầu. Phản ví dụ (CX-05): Keycloak `SELECT keycloak_db.OUTBOX_ENTRY` ca cũ 195,1 (thô) so với 192,42 (E1-U, khớp `#/extra/kenh_co` của M1); ca mới 698,3 so với 696,21.

Cách dùng giữ như `dinh-chinh-1.md` §3: giải thích hạng bằng điểm M1 trong đầu ra; `z-kiem*.txt` chỉ để mô tả mẫu SQL quan sát được. Thứ tự Ticket → Keycloak → Booking ở ca tụt vẫn đúng (CX-05 xác nhận trực tiếp). Người làm chưa chạy lại hai số của phản ví dụ.

## 3. Thu hẹp câu định lượng CPU, DB, PSI (F3)

Thay câu `dinh-chinh-1.md` §2 "CPU PostgreSQL ở nền tăng 4–5 lần, CPU service ứng dụng không đổi … PSI máy cao hơn ở mọi ô":

> Mọi số CPU/PSI nêu theo **ô, cửa sổ và đại lượng**. Theo `phan-tich/cpu-container-nen.txt` (CX-05 đọc): ở `BINH-THUONG` được đo, CPU Payment 0,015 → 0,044 lõi (không phải "không đổi"); PostgreSQL 0,080 → 0,300 lõi ở CPU-BOOK-1 và 0,269 → 0,412 ở BINH-THUONG-X3 (hệ số khác nhau, "4–5 lần" không đại diện chung). PSI (`phan-tich/psi.txt`): ở BINH-THUONG thứ tư, `some avg60` tại t−240 đi 15,6 → 15,5, trong khi tổng thời gian chờ t+60…t+330 tăng 42,5 → 49,7 giây; không viết "cao hơn ở mọi ô".

Bảng kích thước bảng (4,8×, 7,2×, 6,2×) trong `dinh-chinh-1.md` §2: số học đúng; số đếm từng ca tại `t` **chưa có file truy vấn lưu riêng** (`kiem-db.txt` dùng hai mốc đầu lượt) — ghi mức xác nhận là "số đếm do người làm ghi lúc chạy, chưa có bản xuất theo từng `t`".

## 4. Giới hạn của D4 ở bản 2 (F4)

Bổ sung `dinh-chinh-1.md` §7: trong `bang_theo_o_2.py`, phân loại mặc định là `chua_phan_loai` và biểu thức `phan_loai != 'ha_tang'` cho D4 = true cả khi chưa rõ nguyên nhân. Bản 2 vì vậy *dừng kết luận* khi có ca chưa phân loại; nó chưa phải phép xác định "lỗi không do hạ tầng". Trên dữ liệu thực, D4 = false không bị ảnh hưởng: đủ 17 chu kỳ chính, 17/17 đầu ra V082 `OK`, danh sách ứng viên D4 rỗng.

## 5. Không đổi

Kết luận W3 (`dinh-chinh-1.md` §1), phép bỏ từng thành phần (§4), độ phủ 17 cặp (§5), phạm vi ghi thực tế (§6). R1 (Minh duyệt): dùng V082 cho demo, công khai CPU-BOOK-1.
