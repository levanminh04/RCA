# Đính chính 003 — báo cáo P7(a) main013-v2 (R7, R8, R9: dấu span gốc Nezha và C-d3 OB)

Ngày 08/11/2026. Claude, người làm phần chạy/chấm/báo cáo T-054. Minh duyệt gói (DECISIONS, mục "T-054 — gói sửa R7–R9", và WHY-79).
Không ghi đè `bao-cao.md`, `dinh-chinh-001.md`, `dinh-chinh-002.md`. Đính chính này thay các câu nêu dưới đây.
Đầu ra lượt: `results/T-054/runs/sua-cd3-ob-001/` (manifest: `manifest-005.json`).

## Đ9 — Câu cơ chế E1×E5 ở §7.3 (R7)

Thay câu ở `dinh-chinh-002.md` Đ7 ("E1 trong M1 chủ yếu chặn tác dụng phụ của E5; phần của E2 chưa tách") bằng:

"Trong 10 ca TT giảm RR khi tắt E1, có 9 ca E5 loại cờ F_I của các kênh thời lượng toàn phần của root. Quan sát này xác nhận một bước xử lý làm mất bằng chứng ở cấu hình bỏ E1. Chưa xác định được mức đóng góp của cơ chế đó vào tổng lợi ích của E1, hoặc vai trò riêng của E2."

Lý do: bật E1 đổi cả giá trị đặc trưng (self-time) lẫn lớp kênh; ma trận thiếu vế để tách hai phần.

## Đ10 — Câu E2-C ở §7.4 (R8)

Trong câu thay thế ở Đ8, thay "nếu trễ nằm ở bên gọi, E2-C cũng gán cho mọi bên được gọi" bằng:
"E2-C gán bằng chứng cho bên nhận của mỗi cạnh có cờ đủ điều kiện, trên các span bọc hợp lệ (`src/m1/e2.py:38–41`, `src/m1/span.py:156`); nếu trễ nằm ở bên gọi, những cạnh của nó vượt ngưỡng sẽ gán bằng chứng cho bên nhận tương ứng."

## Đ11 — Nguyên nhân C-d3 OB không có dòng; rút câu "đúng thiết kế" (R9, N4)

**Thay câu ở `dinh-chinh-001.md` Đ5** ("C-d3 OB không có dòng ... Đây đúng thiết kế"). Câu đúng:

"C-d3 OB không có dòng vì giao thức không chạy solver OB. Căn cứ của quyết định đó là 22/22 ca dev `NO_TARGET` (T-052). Kết quả này do lỗi adapter: span gốc Nezha mang `ParentID = "root"`, adapter M1 truyền nguyên chuỗi vào lõi, lõi coi span đó là mồ côi, và `dich_cd3` loại span mồ côi khỏi tập gốc (`src/m1/adapter.py:208`, `src/m1/span.py:15, 125–127`, `src/m1/chuoi.py:617`, `src/m1/doi_chung.py:89–98`)."

**Bằng chứng lỗi và phạm vi:**

- Dev: 22/22 ca có `ParentID = root`, 0 span `SpanID = root` (66/66 file trace khớp hash).
- Kiểm tương đương trên dev, hai EC2, code khớp 106/106 pin của job M1 OB main013-v2 (`runs/sua-cd3-ob-001/dev-so-sanh.json#/tom_tat`):
  - 22/22 ca: bản ghi M1 với adapter cũ và với wrapper trùng hệt ngoài bốn trường đã khai trước khi chạy (`extra.dau_vao_cd3.dich`, `extra.dau_vao_cd3.so_span_goc_A`, `diagnostics.span.goc`, `diagnostics.span.mo_coi`). Khối ba world, kênh, vùng, `G_N`, cạnh, tầng, điểm không đổi.
  - Adapter cũ: C-d3 `NO_TARGET` 22/22 (tái lập lịch sử T-052). Wrapper: 9 OK, 2 NO_EVIDENCE, 11 NO_TARGET.
  - Đích dựng từ trung gian (đường dùng cho test) trùng đích lượt chạy đủ ở 22/22 ca; C-d3 từ trung gian trùng C-d3 lượt đủ ở 22/22 ca.
  - `dev-607751ac0a`: bản ghi EC2 (adapter cũ) trùng bản ghi laptop đã lưu `cai-ob-source-native-008/dev-ob-001`, 0 khác biệt.
- Hệ quả: lỗi không đổi hạng/kênh/vùng của M1 hay các vế M1 khác; chỉ đổi đích C-d3 và số đếm chẩn đoán. A4 và các bảng chính không đổi.

## Đ12 — C-d3 OB bổ sung, 34 ca test (sửa sau khi đã xem test)

**Khai báo (C-15 B):** đây là sửa adapter sau khi đã xem kết quả test. Không phải phép kiểm độc lập. Kết quả đầu của bản khóa (0 dòng C-d3 OB) giữ nguyên trong `reports/main-013-v2/`. Không chạy lại M1 trên test.

**Cách tính** (`runs/sua-cd3-ob-001/cd3_test.py`): mỗi ca lấy job/result M1 đã VERIFIED (kiểm hash result với `verified.json`), đọc lại trace qua bộ đọc/adapter đã ghim; dựng span gốc trong A hai cách. Cách cũ tái lập đúng `dau_vao_cd3` đã lưu ở 34/34 ca. Cách mới (wrapper) cho tập đích sửa; gọi `doi_chung.cd3` với `canh`/`diem` đã lưu. Chấm bằng `exact_score` (T-052) sau khi có đầu ra phi nhãn; đường chấm tái lập 60/60 ca C-d3 TT trong `tables.json`. Tiếp xúc ghi ở `runs/sua-cd3-ob-001/exposure.jsonl`.

**Kết quả** (`runs/sua-cd3-ob-001/cd3-test-cham.json`):

| Trạng thái | Số ca |
|---|---|
| OK (đích `frontend`) | 10 |
| NO_TARGET | 24 |

- MRR C-d3 trên 34 ca (ca không OK tính RR 0, như cách chấm C-d3 TT): 0,154.
- Trên 10 ca OK: RR C-d3 trung bình 0,525; M1 0,800; C-d2 0,800 (M1, C-d2 từ `reports/main-013-v2/tables.json#/rows`, world P).
- Từng ca OK (C-d3 / M1): `46c58be0b9` 1/1; `4dbcb97712` 0/0,5; `6ae17814a4` 1/1; `739318ce25` 0/1; `88dc4b2c47` 0/0,25; `e0653eb872` 1/1; `e37c6ad037` 1/1; `e6aad4f10b` 1/1; `f92f6a18c4` 0/1; `fd2c49f3cc` 0,25/0,25.

**Đọc:** mô tả, không kiểm định. 10 ca trải nhiều ô; không nêu mẫu hình theo ô. C-d3 không hơn M1 ở ca nào trong 10 ca; kém M1 ở 4 ca. Vì sao C-d3 trượt ở 4 ca chưa lần (chưa đọc khối C-d3 từng ca). 24 ca còn `NO_TARGET` sau sửa: tập gốc trong A không giao với thực thể có bất thường lan ngược (theo `dich_cd3`); chưa phân tích thêm.

## Trạng thái

- A4 (RQ3b) và bảng chính không đổi.
- RQ3d: OB có thêm đối chứng đường tới đích C-d3 trên 10/34 ca, ở mức mô tả, sửa sau khi xem test.
- `src/m1/adapter.py` vẫn còn lỗi; sửa chính thức sau khi TORAI A nhận/chấm xong (WHY-79).
- TORAI A (174 slot BLOCKED, 2 ca thiếu bộ ba seed) chạy sau, tuần tự, do Codex làm.
