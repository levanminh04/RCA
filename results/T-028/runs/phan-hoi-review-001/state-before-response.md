# Trạng thái

Cập nhật: 07/10/2026. Không quá một trang. Chi tiết từng task nằm ở `tasks/<mã>/LOG.md`.

- **Cổng hiện tại:** G1 đã duyệt ngày 05/10/2026 (Q-61–Q-69; chốt G1 ở Q-70); kế tiếp là P3. G0 đã duyệt ngày 02/10/2026 (Q-36).
- **Test và dataset giữ ngoài:** test: 60 ca RE2-TT (TX1, `data/locked/`) và phần test theo ô của Nezha-OB (Q-61, Q-63); Eadro-TT đã duyệt 3 dev/6 test ngày 05/10, danh sách tại `results/T-023/allowlist-phien.json`. Không dùng Eadro trong thực nghiệm tới G2 (Q-83); giữ ngoài: RE3-OB (chưa tải).
- **Remote git:** `github.com/levanminh04/RCA`. Đã có commit đầu tiên.

## Mục lục task

| Mã | Tên | Gói | Người làm | Người phản biện | Trạng thái | Thư mục |
|---|---|---|---|---|---|---|
| T-000 | Nền tảng: MRP v3 và quy trình | P0 | Claude | Codex | Xong (02/10) | `tasks/T-000-nen-tang/` |
| T-001 | Chốt danh sách phương pháp | P1 | Claude | Codex | Xong (03/10) | `tasks/T-001-danh-sach-phuong-phap/` |
| T-002 | Thẻ dataset họ RCAEval | P2 | Codex | Claude | Xong (04/10) | `tasks/T-002-the-dataset-rcaeval/` |
| T-003 | Gói thẻ dataset ngoài RCAEval | P2 | Codex | Claude | Xong (04/10) | `tasks/T-003-the-dataset-ngoai-rcaeval/` |
| T-005 | Đo khả thi môi trường và thời gian chạy | P1 | Claude | Codex | Xong (04/10) | `tasks/T-005-do-kha-thi/` |
| T-006 | Kiểm đúng đắn các phương pháp trên laptop | P1 | Claude | Codex | Xong (04/10). WHY-15 đã ghi. Q-52–54 đã ghi DECISIONS (Minh duyệt 04/10). Mục 11 điểm 3–6 của `kiem-dung-dan.md`: chuyển cho T-014 (CIRCA) và T-016 (RCD) đánh giá | `tasks/T-006-kiem-dung-dan-laptop/` |
| T-007 | Kiểm đúng đắn trên EC2 (MicroRank, TraceRCA, BOCPD) | P1 | Claude | Codex | Xong (04/10). Việc dọn còn lại: xóa `~/.sudo_as_admin_successful` khi bật lại EC2 của T-007 | `tasks/T-007-kiem-dung-dan-ec2/` |
| T-008 | Thẻ Nezha OB/TT | P2 | Codex | Claude | Xong (04/10) | `tasks/T-008-the-dataset-nezha/` |
| T-009 | Thẻ Eadro TT/SN | P2 | Codex | Claude | Xong (04/10) | `tasks/T-009-the-dataset-eadro/` |
| T-010 | Thẻ DeepTraLog TT | P2 | Codex | Claude | Xong (04/10) | `tasks/T-010-the-dataset-deeptralog/` |
| T-011 | Thẻ LEMMA-RCA | P2 | Codex | Claude | Xong (04/10) | `tasks/T-011-the-dataset-lemma-rca/` |
| T-012 | Khảo sát dataset 2025–2026 | P2 | Codex | Claude | Xong (04/10) | `tasks/T-012-khao-sat-dataset-2025-2026/` |
| T-014 | Hồ sơ CIRCA PC và kiến trúc | P1 | Codex | Claude | Xong (04/10/2026) | `tasks/T-014-ho-so-circa/` |
| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | Xong (04/10/2026); Minh duyệt sau sửa R1 và N1–N3 | `tasks/T-013-ho-so-baro/` |
| T-015 | Hồ sơ MicroRank, TraceRCA và detector trace | P1 | Codex | Claude | Xong (04/10/2026) | `tasks/T-015-ho-so-microrank/` |
| T-019 | Thẻ Sock Shop RCAEval | P2 | Codex | Claude | Xong (04/10/2026) | `tasks/T-019-the-sock-shop/` |
| T-016 | Hồ sơ TORAI, lõi RCD và biến thể RCD | P1 | Claude | Codex | Xong (04/10). Đã áp WHY-19, WHY-20, SL36, K1 C.5/C.8, Q-57; đính chính T-001/T-005/T-006 (D1–D6) | `tasks/T-016-ho-so-torai/` |
| T-017 | Hồ sơ SimpleRCA M4 và luật Type I/II | P1 | Codex | Claude | Xong (04/10/2026); Q-55 | `tasks/T-017-simplerca/` |
| T-018 | Hồ sơ GDN và đọc DecompRCA | P1 | Claude | Codex | Xong (04/10/2026); Q-56, WHY-18. E2 chuyển G1 | `tasks/T-018-ho-so-gdn-decomprca/` |
| T-020 | Tổng hợp G1: phương pháp, dataset, cách chia | P1, P2 | Codex | Claude | Đóng 05/10/2026: thay bằng T-021 (Minh đồng ý đề xuất 0); R1–R3 xử lý ở `results/T-021/goi-g1.md` mục 7 | `tasks/T-020-tong-hop-g1/` |
| T-021 | Gói G1 thu gọn | P1, P2 | Claude | Codex | Xong 05/10/2026: Minh trả lời 7 câu G1 (Q-61–Q-69), không thêm vòng phản biện (đề xuất 0) | `tasks/T-021-goi-g1-thu-gon/` |
| T-022 | Giao thức P3, adapter RE2, bộ chấm, pilot | P3 | Claude | Codex | Xong (06/10, Minh duyệt đóng). Giao thức V2 + WHY-22–35 (Q-74, Q-76); code/pilot chuyển T-030. Còn: ghi sổ Q-75 (mã để trống), chưa commit | `tasks/T-022-giao-thuc-p3/` |
| T-023 | Kiểm điều kiện dùng Eadro-TT | P3 | Codex | Claude | Xong (06/10, Minh duyệt đóng; Q-83). Không đưa Eadro vào thực nghiệm tới G2; không triển khai T-027 trong đợt này. Giữ kết quả kiểm và mọi run; clock/cửa sổ/lineage/reference còn OPEN. Chưa commit | `tasks/T-023-kiem-eadro/` |
| T-030 | Cài giao thức P3 trên RE2-TT dev: mã chung, fixture, D1, K-B1 | P3 | Claude | Codex | Xong (06/10, Minh duyệt đóng). Mã `src/p3/`, 57 test đạt; D1, phát lại khớp, K-B1 đạt. Phản biện Codex hai lượt: R1, R2, N1 đã sửa, Codex xác nhận; R3 đã sửa theo lời duyệt, Codex chưa kiểm lại. Chuyển sang T-031: chi phí BOCPD đo trên dữ liệu tổng hợp ≈ 27–83 giờ/30 ca, vượt Q-72; T-031 đo lại trên tiền tố (Q-77). Chưa commit | `tasks/T-030-cai-dat-p3/` |
| T-031 | Chạy P3 trên RE2-TT dev: kiểm khóa cấu hình, pilot chi phí | P3 | Claude | Codex | Xong (06/10, Minh duyệt đóng). Khóa CIRCA OLS (Q-80, Q-82; 11 ca vượt ngưỡng 1e10 báo riêng), TORAI nguồn B; MicroRank 4 ERROR tính trượt; chi phí và đề xuất T-024/T-025 ở `results/T-031/do-chi-phi.md`. Phản biện hai lượt: REVIEW R1–R4 và REVIEW-2 R1–R3 đã xử lý, Codex chưa kiểm lại lượt 2. Chưa commit | `tasks/T-031-chay-khoa-pilot/` |
| T-024 | Chấm tầng 1 chế độ (a) trên 30 ca dev RE2-TT | P3 | Codex | Claude | Xong (07/10, Minh duyệt đóng). Hai lượt phản biện đã xử lý; 420 bản ghi và số/bảng giữ nguyên. Nguồn code TORAI EC2 đã đối chiếu khớp (LOG phiên 7). Giới hạn CIRCA làm tròn và hòa ẩn RCD giữ rõ trong báo cáo. Chưa commit | `tasks/T-024-cham-che-do-a/` |
| T-025 | Chế độ (b): N-Sigma, BOCPD (EC2, TIMEOUT 6 giờ/ca), RCA tại báo động đầu | P3 | Claude | Codex | Xong (07/10, Minh duyệt đóng). Báo động đầu đúng BOCPD 3/30, N-Sigma 0/30; thành công chung bị chặn trước hết ở bộ phát hiện. Phản biện R1–R3, N1–N4 đã xử lý (sửa mô tả, tách số TORAI, WHY-35 "biên file"). Hai EC2 đã tắt. Chưa commit | `tasks/T-025-che-do-b/` |
| T-026 | Adapter và chấm tầng 1 chế độ (a) trên Nezha-OB dev (22 ca) | P3 | Codex | Claude | Xong (07/10, Minh duyệt đóng). R1/R2 đã sửa và kiểm đạt; 248 nguồn/số chấm giữ nguyên. Giữ 1 ERROR MicroRank cắt N; CIRCA/TORAI B UNSUPPORTED. Các OPEN nguyên nhân/nền/clock/test/license giữ trong báo cáo và LOG phiên7–8. Chưa commit | `tasks/T-026-nezha-ob-che-do-a/` |
| T-028 | P4: hạn chế xếp hạng chế độ (a) | P4 | Codex | Claude | Chờ phản biện: bước 3–6 theo chốt 002 đã ghi, kiểm độc lập/đọc tay đạt; nguồn runs/buoc3-005. Nơi xử lý "lan có đáng kể" còn OPEN; cơ chế quan sát chưa phân xử nhân quả. Chưa commit | `tasks/T-028-p4-han-che-xep-hang/` |

## Task đang mở

T-022 đã đóng 06/10; WHY cửa sổ và giao thức P3 đã có hiệu lực (WHY-22–35). T-030 đã đóng 06/10: mã chung `src/p3/` dùng được cho T-031, T-024, T-025. T-031 đã đóng 06/10: khóa cấu hình và bản ghi 30 ca dùng lại được cho T-024 (hash `src/p3` `8d4cc8196c87…`). T-024 đã đóng 07/10 theo Minh duyệt; kết quả chế độ (a) và hai lượt phản biện nằm trong task. T-025 đã đóng 07/10. Kế tiếp: T-026 (Nezha-OB dev, chế độ (a)), SPEC đã duyệt 07/10, Codex làm. T-023 đã đóng theo Q-83; không benchmark Eadro tới G2. Giữ báo cáo và nháp WHY trong results/T-023; clock/cửa sổ/reference còn OPEN. Việc chờ Minh ở từng dòng task. Kế hoạch G2: `docs/PLAN-P3-G2.md`. T-004 (P9a) chưa triển khai.

## Đang chờ Minh

- T-003, T-012 đã đóng 04/10 (Minh xác nhận Q-51 gồm cả việc sửa SPEC T-012). License/clock/lineage còn OPEN theo thẻ. EC2 đã Stop (Minh báo 04/10); dữ liệu trên EC2 giữ nguyên.
- T-022: ghi sổ Q-75, commit. T-030: commit; xóa ghi chú scratchpad phiên 1 (ngoài repo). T-031: commit. T-024 đã đóng 07/10, chờ duyệt commit; T-025 đã đóng 07/10, chờ duyệt commit. T-023 đã đóng (Q-83); còn đề xuất commit thay đổi đã duyệt.
