# T-074 — W6: khóa bản và thiết kế đánh giá

- **Trạng thái:** đã duyệt triển khai 20/11/2026 theo quyền Minh cho phiên điều phối (SPEC T-070), phần **thiết kế** (không máy); mọi lựa chọn khoa học trong đầu ra là **đề xuất chờ Minh duyệt**. Soạn bởi phiên điều phối T-070.
- **Người làm:** Claude (phiên `danh-gia-w6`, mức High; lặp lỗi thì điều phối báo Minh xét XHigh).
- **Người phản biện:** Codex.
- **Thuộc gói MRP:** P9, P10 — **Cổng:** chuẩn bị G6.

## Mục tiêu

Kế hoạch giai đoạn 2 §8.3 W6 (nguyên văn yêu cầu ở đó): khóa digest FlashTicket, commit repo lab, sha256 M1, kịch bản, mức tải; D14 bắt buộc (P7 khóa chạy thẳng, V082 đầy đủ, V082 che từng nhóm thông tin kể cả dẫn xuất; cả hai chế độ); ma trận ô chạy được trên bản mới; dự toán giờ máy và quy tắc gói hợp lệ; R-07; baseline (SimpleRCA M4, BARO RobustScorer ứng viên; BARO ở (b) dùng cùng t̂); runner W7 đóng gói đầu vào không phụ thuộc đầu ra M1; độ đo theo đầu ra (§8.3 bảng). Ghi WHY trước khi thu. Nguồn: MRP (RQ đánh giá), DT18, hướng dẫn của cô — đọc trực tiếp theo AGENTS §6.4.

Task là **thiết kế**; kết quả là hồ sơ để Minh duyệt trước W7. Không thu dữ liệu.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Giải thích khác / lựa chọn | Bằng chứng cần | Phần còn mở |
|---|---|---|---|
| Kiểm soát trạng thái DB giữa các ô W7 thế nào? | Khôi phục về mốc + trộn thứ tự ô (đề xuất Claude cũ, `lich-su/04` §5) / giữ tích lũy / khối theo mốc | T-069 (`dinh-chinh-1.md` §2), độ trôi E2→E4 của T-071, phép đo khôi phục ở E6 | Ứng viên, Minh duyệt |
| Điểm yếu "chấm một mẫu max trên kênh op gộp" (T-069) ảnh hưởng thiết kế đánh giá ra sao? | Đặc tính lõi chung (P7 và mọi biến thể cùng) | `dinh-chinh-1.md` §2, §4; `phan-tich/bien-the/hang.txt` | Ứng viên chưa kiểm; không sửa lõi (R4) |
| Runner W7 đóng gói đầu vào độc lập đầu ra M1? | `safe-export.py` đòi `summary.json` (T-069 Bước 0, mục 0.8) | Đọc code `safe_export.py`, `runner4.py` | Code là gói sau, thiết kế ở đây |
| Hạn bán 02/12 22:16Z có đủ cho W7? | Gia hạn lần nữa là sửa dữ liệu (Minh) | Dự toán giờ máy | — |

## Đầu vào

`docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8.3; `docs/MRP.md`; `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md`, `advisor-2026-09-23.md`; `docs/LESSONS.md`, `docs/WHY.md`, `docs/DECISIONS.md` phần liên quan; T-043 SPEC (B1.9, D3), T-059 (quy tắc nhãn, M7), T-017 (SimpleRCA), T-013 (BARO), T-064 (V082, D14), T-069 (`dinh-chinh-1.md`); `docs/techstack/ban-giao-dieu-phoi-2026-11-20/thong-nhat.md` §1.2, §1.4. Repo lab `407b4f5` (chỉ đọc).

## Đầu ra

- `results/T-074/thiet-ke-w6.md`: từng mục của §8.3 W6 — chọn gì, phương án đã xét, bằng chứng, kết luận phụ thuộc, phần chờ Minh.
- `results/T-074/de-xuat-why.md`: các mục WHY đề xuất (chưa ghi `docs/WHY.md`).
- `results/T-074/du-toan.json`: giờ máy theo ô, mức lặp, phương án lỗi 10/50/99% (luật 21).
- `results/T-074/cau-hoi-minh.md`: quyết định cần Minh, mỗi mục kèm đề xuất, mặt trái, phương án khác.

## Phạm vi ghi

Ngoài `LOG.md` và dòng T-074 trong `docs/STATE.md`: `results/T-074/`. Không ghi repo lab, không máy (E6 cần SPEC bổ sung khi tới S5).

## Các bước

1. Đọc nguồn trực tiếp (MRP, DT18, cô, LESSONS) và các task dẫn ở Đầu vào.
2. Soạn `thiet-ke-w6.md` theo từng mục §8.3; nêu rõ đâu là ứng viên.
3. Dự toán và mục luật 21; câu hỏi Minh.
4. Báo điều phối; prompt Codex soát SPEC/thiết kế.

## Kiểm đúng đắn

Mỗi lựa chọn có nguồn, phương án khác, điều kiện thất bại (luật 3, 18). Không coi ứng viên là đã xác nhận (luật 5). Không dùng dữ liệu khóa (luật 1).

## Tiêu chí xong

Hồ sơ thiết kế đủ mục §8.3 W6, mỗi lựa chọn có trạng thái (đề xuất / chờ Minh / phụ thuộc kết quả W4–W5); dự toán có số; câu hỏi gom một lần.

## Không làm

Thu dữ liệu; chạy E6; sửa lõi; mở test hay dataset giữ ngoài.

## Chi phí ước lượng

Không giờ máy.

## Rủi ro và điều chưa chắc

Thiết kế phụ thuộc kết quả W4 (độ trôi DB) và W5 (độ trễ chế độ (b)); các phần phụ thuộc ghi rõ và cập nhật sau.

## Prompt bàn giao

Ở `LOG.md`, mục cuối mỗi lượt.
