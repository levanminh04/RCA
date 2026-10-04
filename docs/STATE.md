# Trạng thái

Cập nhật: 02/10/2026. Không quá một trang. Chi tiết từng task nằm ở `tasks/<mã>/LOG.md`.

- **Cổng hiện tại:** G1. G0 đã duyệt ngày 02/10/2026 (Q-36).
- **Test và dataset giữ ngoài:** chưa chọn. 60 ca RE2-TT chưa ai nhìn đang khóa ở `data/locked/` (xem `data/README.md`).
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
| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | Xong (04/10/2026); Minh duyệt sau sửa R1 và N1–N3 | `tasks/T-013-ho-so-baro/` |

## Task đang mở

**T-001** và **T-002**, chạy song song, mỗi task một phiên. T-003 ghi trạng thái riêng bên dưới; T-004 (P9a, yêu cầu quan sát cho RCA) chưa triển khai.

**T-003** đã phản hồi REVIEW và sửa R1–R4 theo Q-51; kiểm lại toàn gói đạt. Bank bảo toàn metadata/nhãn trước G3 theo WHY-13, chưa chốt tập thí nghiệm G1. T-004 chưa triển khai.

## Đang chờ Minh

- T-003, T-012 đã đóng 04/10 (Minh xác nhận Q-51 gồm cả việc sửa SPEC T-012). License/clock/lineage còn OPEN theo thẻ. EC2 đã Stop (Minh báo 04/10); dữ liệu trên EC2 giữ nguyên.
