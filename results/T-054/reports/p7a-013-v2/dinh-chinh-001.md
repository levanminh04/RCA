# Đính chính 001 — báo cáo P7(a) main013-v2, đáp REVIEW.md (08/11/2026)

Áp vào `bao-cao.md` (bản hiện hành, sha 88daa2…) và bản gốc dựng lại `bao-cao-ban-dau.md` (sha 6af085…). Không ghi đè báo cáo. Nguồn phản biện: `tasks/T-054-khoa-g3-chay-p7-a/REVIEW.md`. Minh duyệt ghi khi người làm không phản đối điểm nào.

## Đ1 — Ghi đè báo cáo trong luồng A (REVIEW R1)

- Ngày 08/11/2026, trong luồng A (T-055), tôi sửa tại chỗ 4 số làm tròn trong `bao-cao.md`. Quyền Q1 chỉ cho ghi `kiem-toan-ven/`, nên đây là ghi ngoài phạm vi (Luật 0 mục 8). Tôi khai tại đây và ở LOG T-054.
- **Bản gốc khôi phục được.** Lấy bản hiện hành, đảo đúng 4 chỗ sửa, cho kết quả trùng từng byte với sha256 trong `manifest.json` (6af085…). Bản này lưu ở `bao-cao-ban-dau.md`.
- **Bằng chứng lưu thành file.** `kiem-toan-ven/soat_bang.py` → `kiem-toan-ven/soat-bang.json` so 221 ô ở bảng §4 và §5:
  - bản gốc lệch đúng 4 ô: TraceRCA OB 0,494 (file 0,4935); C-d2 OB 0,878 (0,8775); CI M1−C-d2 OB hi 0,041 (0,0405); CI M1−C-g OB lo 0,087 (0,0865);
  - bản hiện hành lệch 0.
- `ghi-chu.md` trước đó trỏ cả 4 lỗi về `ket-qua.json#/A5_fail`. Thực ra mục đó chỉ có lỗi C-d2; 3 lỗi còn lại đến từ lần soát máy giờ đã lưu ở `soat-bang.json`.

## Đ2 — Giới hạn D1 cho RQ3d trên OB (REVIEW R2)

- D1 (DECISIONS, ngày 07/11): adapter OB đã được sửa sau khi đọc cấu trúc thời gian của cohort OB. Bốn ca bị ảnh hưởng: `test-3218391218`, `test-3a1afd6d4f`, `test-9712e01207`, `test-a8cc0373da`.
- Hai ca minh họa E1 ở §7.4 (`3a1afd6d4f`) và §7.5 (`3218391218`) thuộc nhóm này. 3/8 ca mà E1 giúp cũng nằm trong 4 ca này.
- Tính lại RR world P từ `results/T-054/reports/main-013-v2/tables.json#/rows`:

  | Cặp so | all34 | remaining30 | affected4 |
  |---|---|---|---|
  | M1 − bỏ E1 | +0,130 (8/25/1) | +0,079 (5/24/1) | +0,512 (3/1/0) |
  | M1 − bỏ E2 | +0,115 (7/25/2) | +0,131 (7/21/2) | 0 |
  | M1 − C-a0 | +0,164 (11/20/3) | +0,203 (11/17/2) | −0,125 |
  | C-a1 − C-a0 | +0,049 | +0,072 | −0,125 |

- **Sửa câu kết luận (§0, §7.4, §9 hàng RQ3d):**
  - Phần hơn trên OB so với C-a0 và phần của E2 vững khi bỏ 4 ca D1.
  - Phần của E1 trên 30 ca còn lại nhỏ hơn: +0,079, so với +0,130 trên đủ 34 ca. 3/8 ca E1 giúp nằm trong nhóm D1.
  - Phân xử ảnh hưởng của D1 lên E1 cần dữ liệu độc lập; với dữ liệu hiện có, điểm này vẫn OPEN.

## Đ3 — Ứng viên 1 ở §7.5 trên TT (REVIEW R3)

- Đọc vế C-e (cửa sổ t−300) đã chạy, đơn vị `op|ts-auth-service|UserRepository.findByUsername`:
  - `test-053c028c65`: C-e F_raw_len 0, e_len 0, r_len_A 0,020, r_len_N 0,044; ở cửa sổ lỗi e_len 2263,2, r_len_A 0,104, r_len_N 0,028.
  - `test-5e8f996191`: C-e F_raw_len 0, e_len 0, r_len_A 0,032, r_len_N 0,035; ở cửa sổ lỗi e_len 1438,7, r_len_A 0,098, r_len_N 0,037.
- **Trạng thái ứng viên 1 với TT:** không hỗ trợ ở 2/2 ca (kênh không lệch ở t−300). Không coi là bác bỏ: N của C-e khác N chính, và bất thường gián đoạn vẫn có thể có.
- Hai giải thích còn lại chưa phân xử được: lỗi lan qua đường không quan sát (auth không có cạnh, LESSONS ST3), hoặc tranh chấp tài nguyên chung. Phần OB vẫn OPEN, vì OB không có vế C-e.

## Đ4 — "TORAI B yếu ở nhóm bậc 0" (REVIEW R4)

- Nhóm bậc 0 có 13 ca: 12 ca root ts-auth-service, 1 ca train socket (`test-541642b59e`, có 136 operation mới).
- Trong 5 ca M1 thắng TORAI B ở nhóm này, 3 ca thuộc cùng ô auth|loss.
- Sửa câu ở §6 và §7.1 thành: "bậc 0 ≈ root auth (12/13); 3/5 ca thắng nằm trong một ô". Không còn là mẫu hình theo vị trí (QT15).

## Đ5 — Trạng thái và bàn giao (REVIEW R5)

- **§10 kết cục:** Minh chọn giữ M1 cho RE3 (D-55-1, LOG T-055). RE3 đã chạy và chấm trong T-055. Báo cáo RE3: `results/T-055/reports/re3/bao-cao-re3.md`.
- **C-d3 OB:** không có dòng nào trong `tables.json`. Đây đúng thiết kế ("OB không có solver mới", `tables.json#/limits`). SPEC dự kiến 34 dòng hỗ trợ/mô tả cho C-d3 OB; bản chấm không tạo các dòng này. Không ảnh hưởng bảng chính.
- **TORAI A:** đã chạy 6/180 slot trên 3 ca (`cda8dfc162` 3 seed, `2a0c838e6b` 2 seed, `edaa68b4cf` 1 seed). LOG dòng 2249 ghi "2 ca" là sai.
- **Tiêu chí xong:** chưa đủ bảng bắt buộc, vì bảng phụ TORAI A còn chờ Minh (luồng D giao Codex). Câu "đủ bảng bắt buộc" ở LOG dòng 2303 là nói quá.

## N1 — Điểm người làm tự tìm (sau T-056)

- §7.5 ứng viên 2 ("khóa ưu tiên độ rộng") nay có thêm bằng chứng mô tả từ T-056 phần 2 (`results/T-056/ket-qua-002.json`):
  - đếm số mẫu metric vượt 3σ tái lập đúng SimpleRCA M4 (TT 60/60, RE3 30/30);
  - ở 3/3 ca TT M1 sai, quy tắc đếm đặt root hạng 1.
- Đây vẫn là phân tích sau khi xem test, không phải kiểm định thiết kế (C-15 B).
