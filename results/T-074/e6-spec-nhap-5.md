# Nháp SPEC bổ sung T-074 — E6 (K0), bản 5

- **Trạng thái:** NHÁP. Claude (phiên `danh-gia-w6`), 24/11/2026. Bản 5 = `e6-spec-nhap-4.md` + các thay đổi dưới (giữ hash bản 4 ở `SHA256SUMS-7`). Sửa theo CX-39, CX-39b (đáp ở LOG phiên 8).
- **Pha đọc** (bước 0–1) đã chạy 23/11 18:03–18:06Z (LOG phiên 7, `e6/SHA256SUMS`). Theo CX-39b, kết quả bước 0 cũ **không** dùng để phát ghi: làm lại bước 0 (bộ lọc đầy đủ) và bước 1 bổ sung ngay khi nhận S5 cho pha ghi.
- **Bộ thực thi:** `results/T-074/e6/v2/` thay `results/T-074/e6/sql-thuan.sh`, `sql-nghich.sh`, `kiem-sau-ghi.sh` (giữ nguyên làm lịch sử, không dùng).

## 1. Biến thể sức chứa (Minh chọn)

| Biến thể | Sức chứa | Ghi gì | Trường sức chứa sau ghi |
|---|---|---|---|
| **A** (đúng A3) | 96.000 = 41.705 + 53.460 làm tròn lên nghìn; còn 54.295 vé | ngày (11 trường ở 4 DB) + 3 bản sao sức chứa | `DICH` (96.000) |
| **B** (giữ 100.000; cần Minh duyệt ngoại lệ A3) | 100.000; còn 58.295 vé | chỉ ngày; 3 bản sao sức chứa **không ghi**, vẫn được kiểm bằng 100.000 | `CU` (100.000) |

SQL tĩnh: `v2/sql/A/`, `v2/sql/B/` (sinh bằng `v2/tao_sql.py`).

## 2. Bước 0 (làm lại khi nhận S5) — `v2/b0-v2.sh`

Một bộ lọc tiến trình cấm chung cho ba máy (`runner4`, `tai_linux`, `chuoi_tai`, `inj3`, `_het_han`, `_renew`, `rcaburn`, `stage_m1`, `run_m1`, `xuat_bo_sung`, `sau_v082`, `safe_export`, `orchestrator`, `k6 run`), loại chính lệnh dò; máy tải đếm container `rca-tai-*` **theo trạng thái** (`State`), không chỉ tên. Tiêu chí đạt như bản 4 §5 bước 0.

## 3. Bước 1 bổ sung / điều kiện yên — `v2/b1c-yen.sh` (chỉ SELECT)

Đơn theo `lifecycle_state`; `held`; outbox chưa gửi ở 4 DB (tìm cột mốc gửi theo tên; không có cột → "chưa kiểm được" = chưa yên); hàng đợi khác 0. Kết quả ngày và tồn kho đã đọc ở pha đọc giữ nguyên giá trị; `thuan-*.sql` so lại toàn bộ dưới khóa.

## 4. Pha ghi với `v2/chay.sh`

1. `bash chay.sh kiem <A|B> CU` → phải 0 (mọi trường còn cũ).
2. `bash b1c-yen.sh` → yên; dump 4 DB (bản 4 bước 2).
3. `bash chay.sh thuan <A|B>` — mỗi DB một giao dịch: đếm đúng 1 dòng; so **mọi** giá trị, kiểu JSONB, trường nhận diện/phiên bản (`status`, `source_config_version`, `row_version`, `eventId`, `schemaVersion`, `sourceConfigVersion`, `held`, `purchased`) với bước 1 bằng `IS DISTINCT FROM`; `jsonb_set(..., false)` (không tạo khóa); kiểm `ROW_COUNT`; **hậu kiểm trong giao dịch** (giá trị, kiểu, tập khóa JSON, số phần tử `ticketTypes`) trước COMMIT; in `DA_COMMIT` sau COMMIT. Dừng ngay ở DB lỗi đầu tiên.
4. `bash chay.sh kiem <A|B> DICH` → phải 0.
5. Mốc PostgreSQL, khóa bản (bản 4 bước 4, 7).

Mã thoát `chay.sh`: 0 đạt; 2 sai cách gọi/trùng lượt; 3 lỗi SQL (đã rollback); 4 mất kết nối; 5 lỗi psql khác hoặc không thấy `DA_COMMIT`; 6 trường sai trạng thái; 7 thiếu/trùng trường; 8 dòng phụ sai. Mỗi lượt một thư mục `/home/ubuntu/t074/e6/<chế độ>-<biến thể>-<mã lượt>/` (không ghi đè): `luot.txt`, `tien-do.txt` (BAT_DAU/KET_THUC từng DB), `<db>.out/.err`, `KET_QUA`, `MAT_KET_NOI` nếu có.

## 5. Lỗi và hoàn tác (thay bản 4 §7)

| Khi | Nhận biết | Xử lý |
|---|---|---|
| ~10% | lỗi ở bước 0–2, hoặc `thuan` mã 3 ở DB đầu | chưa ghi (DB lỗi đã rollback); dừng, giữ thư mục lượt |
| ~50% — lỗi SQL giữa chừng | `thuan` mã 3 ở DB thứ k | DB 1…k−1 đã COMMIT (theo `tien-do.txt` + `DA_COMMIT`), DB k rollback. `chay.sh kiem <A|B> DOC` xác nhận từng trường CU/DICH. Minh quyết: sửa nguyên nhân rồi chạy tiếp từ DB k, hoặc đảo bằng `chay.sh nghich <A|B> <các DB 1…k−1>` |
| ~50% — mất kết nối | `thuan`/`nghich` mã 4, file `MAT_KET_NOI` (mã lượt, DB, `application_name`, PID nếu đã in) | tìm phiên theo `application_name` trong `pg_stat_activity`; **chờ** phiên đó kết thúc; `chay.sh kiem-khoa <A|B> DOC <db>` (đọc dưới `FOR SHARE`); DB đó toàn CU → chưa ghi; toàn DICH → đã ghi; lẫn hoặc `KHAC`/`THIEU` → 99% |
| ~99% | `kiem` mã 6/7/8; giá trị thứ ba; mất log lượt | dừng; giữ máy ở điều phối; trình Minh. `nghich` chỉ chạy sau quyết định, chỉ trên DB đã xác định thuộc lượt; `nghich` tự từ chối khi thấy giá trị thứ ba, dòng thiếu, kiểu sai, `ticketTypeId` trùng |
| bước 7 lỗi | — | DB đã xác nhận → chỉ làm lại hiện vật |

Không `pg_restore`.

## 6. Bằng chứng kiểm đã có (không máy)

- `v2/thu/chay_thu.sh`: 26 phép thử giả lập trên laptop với `psql` giả (không kết nối DB) — **26/26 đạt** (`v2/thu/chay_thu.out`): dừng ở lỗi đầu (thuận, nghịch), nhánh mất kết nối, lỗi psql khác, thiếu `DA_COMMIT`, từ chối trùng mã lượt và giữ log cũ, hai lượt hai thư mục, `kiem` trả khác 0 khi psql lỗi 42, đủ 15 trường, thiếu/trùng trường, khóa JSON mất, mất dòng, dòng phụ sai, biến thể B. Phép đột biến (bộ chạy không dừng sau lỗi SQL) làm 2 phép thử trượt — bộ thử phát hiện được.
- **Chưa kiểm:** logic SQL trên PostgreSQL (NULL, kiểu JSONB, `jsonb_set` không tạo khóa, so số JSONB khác số 0 lẻ) — laptop không có PostgreSQL. `v2/thu/thu-sql-chi-doc.sql` (11 phép, chỉ đọc, bằng hằng JSONB, `BEGIN READ ONLY … ROLLBACK`) để chạy khi có quyền đọc exp-app, **trước** pha ghi.

## 7. Chi phí

Như bản 4 §8, cộng bước 0 làm lại + `b1c` + `thu-sql-chi-doc.sql` (~15 phút).
