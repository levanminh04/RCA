# Trạng thái

Cập nhật: 29/10/2026. Mốc quyết định ở [DECISIONS.md](DECISIONS.md); chi tiết/lịch sử ở LOG từng task.

## Hiện tại

- **T-044 — cài chuỗi M1 và kiểm đặc tả:** SPEC đã duyệt (29/10/2026). Cloud, branch `claude/sweet-hawking-dy078d`, chưa merge. Giai đoạn 2 xong bước 0–9: code `src/m1`, `src/m1_danh_gia`; 235/235 phép kiểm qua (97/97 phép T-043 trong phạm vi); tất định PASS; đột biến 21/21. Minh đã duyệt 20 cách hiểu ở [đính chính Phần II](../results/T-044/dinh-chinh-cai-dat.md) mục A (29/10/2026). **Chờ phản biện** Codex (prompt ở mục cuối LOG; Codex tự fetch branch). Chờ Minh: dòng DECISIONS và WHY đề xuất. Claude làm, Codex phản biện. Không đọc dữ liệu. [SPEC](../tasks/T-044-cai-dat-m1/SPEC.md), [LOG](../tasks/T-044-cai-dat-m1/LOG.md), [báo cáo](../results/T-044/bao-cao.md).
- **T-045 — chạy T1, T4, T4b, khối K trên dev:** SPEC đã duyệt (29/10/2026), chờ T-044 nghiệm thu; Codex làm (local), Claude phản biện. [SPEC](../tasks/T-045-chay-khoi-k-dev/SPEC.md).
- **T-043 — M1: thiết kế chuỗi chẩn đoán RCA:** **xong — đã đóng** (29/10/2026, Q-209; nghiệm thu trong phạm vi thiết kế); Claude làm, Codex phản biện. Đính chính [phiên 9](../results/T-043/dinh-chinh-phien9.md), [phiên 10](../results/T-043/dinh-chinh-phien10.md) (Đ15–Đ22); WHY-55–65. Không xác nhận hiệu quả hay cơ chế; OPEN ở [báo cáo](../results/T-043/bao-cao.md) §11. Lỗi đặc tả khi cài đặt ghi đính chính trong task cài đặt, không mở lại T-043 (Q-209). [SPEC](../tasks/T-043-thiet-ke-rca-m1/SPEC.md), [LOG](../tasks/T-043-thiet-ke-rca-m1/LOG.md).
- **T-042 — Đối chiếu baseline Nezha-OB:** **xong — đã đóng** (24/10/2026, Q-193); Codex làm, Claude phản biện. Minh đã dừng tìm nguyên nhân lệch OB và chấp nhận giới hạn (Q-192). [Báo cáo](../results/T-042/runs/normal-source-001/bao-cao.md), [LOG đóng task](../tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md). Giữ kết quả và các câu hỏi khoa học OPEN; không tự mở lại; chưa chọn baseline hoặc mở test/G3.
- **T-041 đã nghiệm thu và đóng** theo Q-186 sau gói sửa Q-185. [Báo cáo](../results/T-041/bao-cao.md), [bàn giao thiết kế](../results/T-041/ban-giao-phien-2.md), [LOG đóng task](../tasks/T-041-ra-soat-nen-p3-p5/LOG.md). Claude chưa kiểm lại bản sửa; không ghi thêm lượt phản biện đã hoàn tất.
- **G0/G1/G2 đã duyệt** (Q-36/Q-70/Q-149); **P5 đã đóng** (Q-176). RQ2/RQ3/RQ5 và G3 vẫn OPEN.
- **P6:** [kế hoạch đã lưu](PLAN-P6.md), chưa chọn phương pháp hoặc duyệt triển khai M1. [Đề xuất hướng Grafana](DE-XUAT-HUONG-GRAFANA-RCA.md) không duyệt nguyên văn (Q-188). Phần hạ tầng Grafana và báo động bằng luật đã quyết hướng trong [kế hoạch giai đoạn tới](KE-HOACH-GIAI-DOAN-TOI.md) (M-16, M-36, M-38). Phần còn lại là tài liệu tham khảo, quyết trong SPEC M1 và SPEC hạ tầng.
- **Dữ liệu khóa:** 60 ca test RE2-TT và phần test theo ô Nezha vẫn khóa; Eadro không dùng trong thực nghiệm tới G2 (Q-83), allowlist tại [T-023](../results/T-023/allowlist-phien.json); RE3-OB giữ ngoài, chưa tải. Đóng T-041 không mở test/G3.
- SPEC/báo cáo/manifest T-041 giữ trạng thái tại mốc trước nghiệm thu; quyết định hiện hành là Q-186 và LOG đóng task.

## Việc kế tiếp và chờ Minh

- M1: task cài đặt (1) tách thành T-044 và T-045 (Minh chốt 29/10/2026). Bước kế tiếp: mở phiên cloud làm T-044. Sau T-045 còn task (2) (K-b, T6–T12, KB) và (3) (T13, hồ sơ G3 theo A4, Q-211). Nhãn lan hoãn sang P10 (Q-210). Hoãn quyết: chế độ (b) ở P7 và RE3-OB, cả hai chặn G3. Nối log–span hoãn sang chặng 2 (Q-209). Phần thiết kế RCA không chờ ý kiến cô (Q-187); chỉ nhánh G/H chờ cô.
- Các phần chưa phân xử/thiếu nguồn giữ tại báo cáo T-041 §8 O01–O12 và [OPEN P5](../results/T-040/con-mo.json); nghiệm thu không xác nhận cơ chế hay lợi ích đồ thị. Không tự lấy lại nguồn EC2.
- P9a/T-004 chưa triển khai: nhận [R-01–R-10](../results/T-040/yeu-cau-quan-sat-p9.md), được bổ sung sau; OM-11 đã chuyển P9a, OM-07 hoãn ngoài P5 (Q-175); chưa gửi nhóm hệ thống.
- Việc hồ sơ cũ: ghi sổ Q-75 của T-022; ghi chú scratchpad T-030 ngoài repo; T-007 dọn marker sudo khi EC2 được bật lại. Giữ theo LOG liên quan, không mở lại nghiên cứu của task đã đóng.
- Git remote `github.com/levanminh04/RCA`; đã push tới `bc686d80` (29/10/2026). Phần nặng của T-032, T-041, T-042 giữ local theo cách của Q-181.

## Mục lục task đã đóng

| Chặng | Task đã đóng — liên kết tới LOG |
|---|---|
| P0 | [T-000](../tasks/T-000-nen-tang/LOG.md) |
| P1–P2 | [T-001](../tasks/T-001-danh-sach-phuong-phap/LOG.md), [T-002](../tasks/T-002-the-dataset-rcaeval/LOG.md), [T-003](../tasks/T-003-the-dataset-ngoai-rcaeval/LOG.md), [T-005](../tasks/T-005-do-kha-thi/LOG.md), [T-006](../tasks/T-006-kiem-dung-dan-laptop/LOG.md), [T-007](../tasks/T-007-kiem-dung-dan-ec2/LOG.md), [T-008](../tasks/T-008-the-dataset-nezha/LOG.md), [T-009](../tasks/T-009-the-dataset-eadro/LOG.md), [T-010](../tasks/T-010-the-dataset-deeptralog/LOG.md), [T-011](../tasks/T-011-the-dataset-lemma-rca/LOG.md), [T-012](../tasks/T-012-khao-sat-dataset-2025-2026/LOG.md), [T-013](../tasks/T-013-ho-so-baro/LOG.md), [T-014](../tasks/T-014-ho-so-circa/LOG.md), [T-015](../tasks/T-015-ho-so-microrank/LOG.md), [T-016](../tasks/T-016-ho-so-torai/LOG.md), [T-017](../tasks/T-017-simplerca/LOG.md), [T-018](../tasks/T-018-ho-so-gdn-decomprca/LOG.md), [T-019](../tasks/T-019-the-sock-shop/LOG.md) |
| P3–P4 | [T-020](../tasks/T-020-tong-hop-g1/LOG.md), [T-021](../tasks/T-021-goi-g1-thu-gon/LOG.md), [T-022](../tasks/T-022-giao-thuc-p3/LOG.md), [T-023](../tasks/T-023-kiem-eadro/LOG.md), [T-024](../tasks/T-024-cham-che-do-a/LOG.md), [T-025](../tasks/T-025-che-do-b/LOG.md), [T-026](../tasks/T-026-nezha-ob-che-do-a/LOG.md), [T-028](../tasks/T-028-p4-han-che-xep-hang/LOG.md), [T-029](../tasks/T-029-p4-han-che-phat-hien/LOG.md), [T-030](../tasks/T-030-cai-dat-p3/LOG.md), [T-031](../tasks/T-031-chay-khoa-pilot/LOG.md), [T-032](../tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md), [T-033](../tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md), [T-034](../tasks/T-034-g2-goi-trinh/LOG.md) |
| P5 | [T-035](../tasks/T-035-p5-do-thi-tu-trace/LOG.md), [T-036](../tasks/T-036-p5b-hop-dong-chung/LOG.md), [T-037](../tasks/T-037-p5b-flashticket/LOG.md), [T-038](../tasks/T-038-p5b-trainticket/LOG.md), [T-039](../tasks/T-039-p5b-online-boutique/LOG.md), [T-040](../tasks/T-040-p5b-tong-hop/LOG.md) |
| Chuẩn bị P6 | [T-041](../tasks/T-041-ra-soat-nen-p3-p5/LOG.md) |

T-020 đóng và được thay bằng T-021. Lịch sử nghiệm thu, giới hạn và các lượt chưa kiểm lại xem LOG của từng task; không suy mọi task đã hoàn tất phản biện chính thức.
