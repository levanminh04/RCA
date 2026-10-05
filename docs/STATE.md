# Trạng thái

Cập nhật: 05/10/2026. Không quá một trang. Chi tiết từng task nằm ở `tasks/<mã>/LOG.md`.

- **Cổng hiện tại:** G1 đã duyệt ngày 05/10/2026 (Q-61–Q-69); kế tiếp là P3. G0 đã duyệt ngày 02/10/2026 (Q-36).
- **Test và dataset giữ ngoài:** test: 60 ca RE2-TT (TX1, khóa ở `data/locked/`, xem `data/README.md`) và phần test theo ô của Nezha-OB, Eadro-TT (Q-61, Q-68); giữ ngoài: RE3-OB (chưa tải).
- **Remote git:** `github.com/levanminh04/RCA`. Đã có commit đầu tiên.

## Mục lục task

| Mã | Tên | Gói | Người làm | Người phản biện | Trạng thái | Thư mục |
|---|---|---|---|---|---|---|
| T-000 | Nền tảng: MRP v3 và quy trình | P0 | Claude | Codex | Xong (02/10) | `tasks/T-000-nen-tang/` |
| T-001 | Chốt danh sách phương pháp | P1 | Claude | Codex | Xong (03/10) | `tasks/T-001-danh-sach-phuong-phap/` |
| T-002 | Thẻ dataset họ RCAEval | P2 | Codex | Claude | Xong (04/10) | `tasks/T-002-the-dataset-rcaeval/` |
| T-003 | Gói thẻ dataset ngoài RCAEval | P2 | Codex | Claude | Xong (04/10) | `tasks/T-003-the-dataset-ngoai-rcaeval/` |
| T-005 | Đo khả thi môi trường và thời gian chạy | P1 | Claude | Codex | Xong (04/10) | `tasks/T-005-do-kha-thi/` |
| T-006 | Kiểm đúng đắn các phương pháp trên laptop | P1 | Claude | Codex | Xong (04/10), chưa commit (Minh dặn). WHY-15 đã ghi. Q-52–54 đã ghi DECISIONS (Minh duyệt 04/10). Mục 11 điểm 3–6 của `kiem-dung-dan.md`: chuyển cho T-014 (CIRCA) và T-016 (RCD) đánh giá | `tasks/T-006-kiem-dung-dan-laptop/` |
| T-007 | Kiểm đúng đắn trên EC2 (MicroRank, TraceRCA, BOCPD) | P1 | Claude | Codex | Xong (04/10). Việc dọn còn lại: xóa `~/.sudo_as_admin_successful` khi bật lại EC2 của T-007 | `tasks/T-007-kiem-dung-dan-ec2/` |
| T-008 | Thẻ Nezha OB/TT | P2 | Codex | Claude | Xong (04/10) | `tasks/T-008-the-dataset-nezha/` |
| T-009 | Thẻ Eadro TT/SN | P2 | Codex | Claude | Xong (04/10) | `tasks/T-009-the-dataset-eadro/` |
| T-010 | Thẻ DeepTraLog TT | P2 | Codex | Claude | Xong (04/10) | `tasks/T-010-the-dataset-deeptralog/` |
| T-011 | Thẻ LEMMA-RCA | P2 | Codex | Claude | Xong (04/10) | `tasks/T-011-the-dataset-lemma-rca/` |
| T-012 | Khảo sát dataset 2025–2026 | P2 | Codex | Claude | Xong (04/10) | `tasks/T-012-khao-sat-dataset-2025-2026/` |
| T-014 | Hồ sơ CIRCA PC và kiến trúc | P1 | Codex | Claude | Xong (04/10/2026), chưa commit | `tasks/T-014-ho-so-circa/` |
| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | Xong (04/10/2026); Minh duyệt sau sửa R1 và N1–N3 | `tasks/T-013-ho-so-baro/` |
| T-015 | Hồ sơ MicroRank, TraceRCA và detector trace | P1 | Codex | Claude | Xong (04/10/2026), chưa commit | `tasks/T-015-ho-so-microrank/` |
| T-019 | Thẻ Sock Shop RCAEval | P2 | Codex | Claude | Xong (04/10/2026), chưa commit | `tasks/T-019-the-sock-shop/` |
| T-016 | Hồ sơ TORAI, lõi RCD và biến thể RCD | P1 | Claude | Codex | Xong (04/10), chưa commit (Minh dặn). Đã áp WHY-19, WHY-20, SL36, K1 C.5/C.8, Q-57; đính chính T-001/T-005/T-006 (D1–D6) | `tasks/T-016-ho-so-torai/` |
| T-017 | Hồ sơ SimpleRCA M4 và luật Type I/II | P1 | Codex | Claude | Xong (04/10/2026), chưa commit; Q-55 | `tasks/T-017-simplerca/` |
| T-018 | Hồ sơ GDN và đọc DecompRCA | P1 | Claude | Codex | Xong (04/10/2026), chưa commit; Q-56, WHY-18. E2 chuyển G1 | `tasks/T-018-ho-so-gdn-decomprca/` |
| T-020 | Tổng hợp G1: phương pháp, dataset, cách chia | P1, P2 | Codex | Claude | Đóng 05/10/2026: thay bằng T-021 (Minh đồng ý đề xuất 0); R1–R3 xử lý ở `results/T-021/goi-g1.md` mục 7; chưa commit | `tasks/T-020-tong-hop-g1/` |
| T-021 | Gói G1 thu gọn | P1, P2 | Claude | Codex | Xong 05/10/2026: Minh trả lời 7 câu G1 (Q-61–Q-69), không thêm vòng phản biện (đề xuất 0); chưa commit | `tasks/T-021-goi-g1-thu-gon/` |

## Task đang mở

Không có task mở. Việc kế tiếp: viết SPEC task P3 bậc 1 (RE2-TT + RE3-OB, phương pháp tầng 1, Q-61, Q-62), gồm phép kiểm Eadro-TT (Q-61, Q-64). Chưa có WHY cho cửa sổ (Q-64) và nguồn dữ liệu bình thường của Eadro; phải ghi trước khi dùng trong kết quả (luật cứng 3). T-004 (P9a) chưa triển khai.

## Đang chờ Minh

- T-003, T-012 đã đóng 04/10 (Minh xác nhận Q-51 gồm cả việc sửa SPEC T-012). License/clock/lineage còn OPEN theo thẻ. EC2 đã Stop (Minh báo 04/10); dữ liệu trên EC2 giữ nguyên.
- Duyệt SPEC task P3 bậc 1 (sẽ trình trong chat).
