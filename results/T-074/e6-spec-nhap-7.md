# Nháp SPEC bổ sung T-074 — E6 (K0), bản 7

- **Trạng thái:** NHÁP. Claude (phiên `danh-gia-w6`), 24/11/2026. Bản 7 thay `e6-spec-nhap-6.md` (giữ nguyên; hash `SHA256SUMS-10`). Sửa theo CX-45b, CX-46, CX-46b (đáp ở LOG phiên 12). Phần không nhắc giữ như bản 4–6.
- **Căn cứ quyền:** Minh duyệt 24/11 "Duyệt kết hợp" (giữ SQL thuận v2 B nguyên văn; bỏ SQL nghịch; hoàn tác bằng khôi phục dump chụp ngay trước khi ghi, có thử khôi phục vào DB nháp; chạy có người theo dõi, mỗi lần một DB) và "Duyệt chạy thử" (thuận B + kiểm DICH trên DB nháp trước DB thật; lỗi → dừng DB đó, không ghi DB thật, báo điều phối). Biến thể **B** (DECISIONS 24/11 mục 1). Hai lời duyệt này hiện chỉ ghi ở LOG phiên 10; đưa vào DECISIONS cần trình Minh riêng (Luật 0).
- **Pha ghi chưa giao.** Codex kiểm v4 trước khi phát. Hạn bán hiện tại 02/12.

## 1. Bộ thực thi

| File | Người viết | Trạng thái |
|---|---|---|
| `e6/v3/b0.sh` | Codex | dùng được cho tiến trình/cron; **hai lỗi hiển thị đã đồng thuận** (lọc danh sách timer; cắt lease 300 ký tự) — chờ Codex sửa. **Chưa phát khi chưa có bản sửa đã kiểm.** |
| `e6/v3/b1c-yen.sh` | Codex | dùng được với `--phut-khong-tai N` |
| `e6/v4/chay.sh` | Claude | thay `v3/chay.sh` (giữ nguyên) |
| `e6/v4/thu/` | Claude | docker/psql/pg_dump/pg_restore/df/ps giả; bộ thử; đột biến |

SQL thuận/kiểm: nguyên văn `v2/sql/B` (sha256 khớp `v2/SHA256SUMS`, bộ chạy tự kiểm).

**Tập trường SQL B thực sự so trước khi ghi** (thay câu "so mọi giá trị đã khóa" của bản 5): Event — `status`, `source_config_version`, `row_version`, 5 ngày; `configured_quantity`. Booking snapshot — `event_status`, `source_config_version`, `row_version`, `sale_ends_at`; JSON `eventId`, `schemaVersion`, `sourceConfigVersion`, kiểu `ticketTypes`, 3 ngày, đúng một phần tử `ticketTypeId`, `configuredQuantity`; inventory — `event_id`, `configured_capacity`, `held`, `purchased` (**không** so `source_config_version`, `row_version` của inventory). Ticket — `event_status`, `source_config_version`, 2 ngày. Payment — `source_fee_version`, `event_ends_at`. Minh đã duyệt giữ SQL B nguyên văn.

## 2. Thủ tục pha ghi (có người theo dõi)

Mọi lệnh trên máy chạy nền (`setsid nohup … > log 2>&1 &`), người trực đọc log.

**Bước 0 — một lần đầu lượt.**
1. exp-app: `bash v3/b0.sh app`; exp-obs: `bash v3/b0.sh obs` (gồm máy tải). Mã 0 = **thu thập thành công**, không phải "sạch": người trực đối chiếu nội dung theo bản 4 §5 bước 0 (tiến trình cấm, cron, timer lạ, lease còn hạn, container, toxic). Dùng bản b0 đã sửa hai lỗi hiển thị.
2. exp-app: `bash v3/b1c-yen.sh --phut-khong-tai N`, `N` = số phút không tải người trực xác nhận từ lịch máy và đầu ra b0 (≥ 10 theo tiêu chí đã có). Phải `YEN`. Ghi `purchased`, `held`.
3. exp-app: `MOC_PURCHASED=<purchased> MOC_HELD=<held> bash v4/chay.sh mo-luot`. Bộ chạy đọc hằng số trong `v2/sql/B/thuan-booking.sql` (`held = 0`, `purchased = 41705`) và so: **lệch → mã 3, dừng trước Event, trình Minh** (SQL B chắc chắn trượt ở Booking). Đạt → `kiem-khoa` CU cả 4 DB; lưu `/home/ubuntu/t074/e6/moc-luot.txt`. Mọi lệnh sau đọc mốc từ file này; biến môi trường khác file → từ chối.
4. J01–J11 (`v2/thu/thu-sql-chi-doc.sql`, chỉ đọc).

**Mỗi DB** (`event` → `booking` → `ticket` → `payment`):
1. `bash v3/b1c-yen.sh --phut-khong-tai N` → `YEN`, `purchased`/`held` bằng mốc lượt (yên **trước** dump).
2. `bash v4/chay.sh chuan-bi <db>` — không ghi DB thật: đọc thuộc tính DB; **DB có ACL hoặc role setting riêng → mã 3, dừng DB đó** (đường hoàn tác đã duyệt không giữ được cấu hình đó; trình phương án khôi phục tay); kiểm đĩa; kiểm CU; bộ đếm DML; `pg_dump -Fc` + sha256; khôi phục vào DB nháp; băm; **thuận B + kiểm DICH trên DB nháp (bắt buộc)**; xóa DB nháp (không xóa được → `KET_QUA` ghi `CON_DB_NHAP <tên>`); bộ đếm DML đọc lại bằng nhau.
   - Điều băm chứng minh: nội dung các bảng `relkind = 'r'` và sequence của DB thật **tại lúc băm** khớp dump đã khôi phục. Không chứng minh: đối tượng khác (view, hàm, quyền); khoảng sau lúc băm; thay đổi rồi trả về giá trị cũ giữa hai lần đọc. Bộ đếm DML đọc hai lần bằng nhau là chốt phụ (thống kê PostgreSQL cập nhật trễ).
3. Người trực đọc `nhat-ky.txt`, rồi `bash v4/chay.sh ghi <db> <thư-mục-chuẩn-bị>`: chuẩn-bị phải `DAT`, có dấu chạy thử trên nháp, cờ khôi phục `co`, còn hạn 30 phút, chưa dùng; bộ đếm DML bằng lúc chuẩn-bị; kiểm CU lại. Chỉ sau đó mới tạo `app.txt` và phát SQL. rc 0 + `DA_COMMIT` + kiểm DICH → **20**; mọi trường hợp khác → xác định (§3).
4. `bash v3/b1c-yen.sh --phut-khong-tai N` (yên **sau** ghi; `purchased`/`held` không đổi).
5. Người trực xác nhận mã 20 rồi mới sang DB kế.

Sau DB cuối: `bash v4/chay.sh kiem DICH event booking ticket payment` → 0; mốc PostgreSQL (bản 4 bước 4); khóa bản (bản 4 bước 7).

## 3. Xác định kết cục

- **Lỗi trước khi phát SQL** (`ghi` trả 2 hoặc 3, thư mục lượt **không có** `app.txt`): chưa phát SQL lên DB thật. Đọc `KET_QUA`, sửa nguyên nhân, chuẩn-bị lại (chuẩn-bị cũ đã bị tiêu). Không gọi `xac-dinh` (nó trả 2).
- **Đã có `app.txt`:** `bash v4/chay.sh xac-dinh <db> <thư-mục-ghi>` chỉ kết luận khi: lượt ghi đã ghi `PSQL_XONG`, **hoặc** tiến trình ghi (`pid`) đã chết **và** không còn tiến trình nào trên máy mang `application_name` của lượt; nếu không → 11, theo dõi chính lượt đó. Sau đó chờ phiên PostgreSQL của lượt biến mất (≤ 120 s; còn → 11; không tự `pg_terminate_backend`), đọc dưới `FOR SHARE`, so **cả nhóm trường của DB** với đầu (toàn CU) và đích B, cùng PHU/BAO với mốc lượt:
  - **20 ĐÃ GHI**; **21 CHƯA GHI** (sửa nguyên nhân, chuẩn-bị mới, ghi lại);
  - **22**: `KET_QUA` = `KHAC_TRUONG` (trường E6 lẫn hoặc giá trị thứ ba) hoặc `KHAC_NGHIEP_VU` (trường E6 đúng một đầu nhưng PHU/BAO lệch mốc, ví dụ `purchased` đổi). **Giữ hiện trạng, không tự khôi phục; trình Minh** với từng trường/PHU/BAO lệch (đã in trong `nhat-ky.txt`). Xem §6 mục 1.
- Tên lạ ở `TRUONG`, `PHU` **và** `BAO` (chỉ `booking.purchased` cho Booking; DB khác không có `BAO`) → 7, gọi lại.

## 4. Khôi phục dump (chỉ khi Minh duyệt đúng ca)

`E6_KHOI_PHUC_MINH=<db> bash v4/chay.sh khoi-phuc <db> <thư-mục-LƯỢT-GHI>`:
1. Lượt ghi phải có `KET_QUA` `KHAC_TRUONG`/`KHAC_NGHIEP_VU`; dump lấy từ chuẩn-bị mà **chính lượt ghi đó** đã dùng, kiểm liên kết hai chiều (`chuan-bi.txt` ↔ `DA_DUNG/boi`) và đúng DB **trước** khi dừng dịch vụ. Dùng dump khác → khôi phục tay, chỉ khi Minh chọn rõ.
2. Thuộc tính DB (chủ, mã hóa, locale) hiện tại phải bằng lúc chuẩn-bị; DB mới tạo theo thuộc tính lúc chuẩn-bị.
3. Ghi OID DB gốc. Dừng dịch vụ; `Running` không thành `false` → **12** (in trạng thái đọc được; DB chưa đổi). Kết nối không về 0 sau 60 s → **17** (dịch vụ đang dừng; DB chưa đổi).
4. Đổi tên DB gốc thành `_hong_`; xác nhận bằng OID (gốc nằm ở `_hong_`, tên chính trống) — không xác nhận được → **16**.
5. Băm bản `_hong_` (bắt buộc; lỗi → trả tên cũ, **13**); in số dòng băm khác dump.
6. Tạo DB mới, ghi OID mới; `pg_restore --exit-on-error`. Lỗi tạo hoặc restore → **trả về**: chỉ xóa DB ở tên chính nếu OID đúng là OID mới của lượt; đổi `_hong_` về tên chính; xác nhận OID gốc ở tên chính và `_hong_` trống → **13**; không xác nhận được → **16** (`KET_QUA` ghi tên và OID quan sát được, dịch vụ đang dừng).
7. Băm DB mới = băm dump; kiểm CU → không đạt **14**.
8. Khởi động dịch vụ; chờ `running` + `healthy` (nếu có) ≤ 180 s → không đạt **15** (`KET_QUA` ghi trạng thái đọc được; DB đã khôi phục).
9. Bản `_hong_` giữ; xóa cần Minh duyệt.

## 5. Lỗi giữa chừng (luật 21)

| Khi | Nhận biết | Xử lý | Mất |
|---|---|---|---|
| ~10% — trước DB đầu | b0/b1c/`mo-luot` (mốc lệch SQL B)/J01–J11 trượt | chưa ghi gì; mốc lệch → trình Minh | phút |
| chuẩn-bị bất kỳ DB | mã 3 | chưa phát SQL lên DB đó; DB nháp đã xóa hoặc `CON_DB_NHAP`; sửa, chuẩn-bị lại | 3–8 phút/DB |
| ghi trả 2/3, không có `app.txt` | lỗi trước phát SQL | như dòng trên | 3–8 phút |
| ~50% — DB thứ k, đã phát SQL | xác định 21 | DB 1…k−1 giữ; sửa nguyên nhân; chuẩn-bị mới; ghi lại DB k | 5–15 phút |
| ~50% | xác định 20 | sang DB kế | 2 phút |
| ~50% | xác định 22 | **giữ hiện trạng**, trình Minh; nếu Minh duyệt khôi phục ca này → §4 | điều tra + 5–15 phút (ước) |
| ~50% | 11 | chờ, gọi lại `xac-dinh`; không tự kết thúc phiên/tiến trình | phút |
| ~99% — sau DB cuối | `kiem DICH` 4 DB trượt | `xac-dinh` DB trượt | ≤ 15 phút + điều tra |
| khôi phục | 12 / 17 | DB chưa đổi; dịch vụ: 12 có thể đang chạy, 17 đang dừng; người trực quyết | điều tra |
| khôi phục | 13 / 14 | 13: DB gốc ở tên chính (OID xác nhận), dịch vụ dừng; 14: DB mới ở tên chính, dịch vụ dừng | điều tra |
| khôi phục | 15 / 16 | 15: DB đã khôi phục, dịch vụ không khỏe; 16: chưa xác nhận DB nào mang tên chính — giữ máy, trình Minh | điều tra |

## 6. Cần Minh quyết

1. **Mã 22 có dẫn tới thay cả DB không (CX-46 điểm 5).**
   - **Đề xuất (a):** 22 → giữ hiện trạng, trình Minh từng ca; Minh duyệt ca nào thì khôi phục ca đó (`E6_KHOI_PHUC_MINH`). Bộ chạy đã tách `KHAC_TRUONG` / `KHAC_NGHIEP_VU` và in từng trường lệch, cùng danh sách dòng băm khác giữa dump và bản hiện tại (ở bước khôi phục) để Minh có căn cứ. **Lý do:** `KHAC_NGHIEP_VU` có thể do một đơn hợp lệ ngoài E6; thay cả DB sẽ loại đơn đó khỏi Booking trong khi DB khác có thể giữ phần giao dịch tương ứng. **Mặt trái:** nhánh lỗi chậm hơn (chờ Minh); các DB đã đạt 20 giữ ngày mới trong lúc chờ (hệ không tải nên không có đơn dùng ngày lệch).
   - **(b)** Minh duyệt trước một quy tắc: `KHAC_TRUONG` với PHU/BAO đúng mốc → được khôi phục không hỏi lại; `KHAC_NGHIEP_VU` → luôn hỏi. Nhanh hơn ở ca lỗi kỹ thuật thuần. Mặt trái: `KHAC_TRUONG` vẫn có thể kèm thay đổi ở bảng không được kiểm; chưa cài (cần duyệt).
   - **(c)** Bản 6: mọi 22 → khôi phục. Không đề xuất (lý do ở (a)).
   - **(d)** Sửa tay từng trường bằng `UPDATE` riêng: ngoài phạm vi đã duyệt (SQL B duy nhất), không đề xuất.
2. **Thay cả DB với dịch vụ dừng (bản 6 §8.2)** — giữ đề xuất; nay có xác nhận OID và báo trạng thái thật ở mọi nhánh lỗi.

## 7. Bằng chứng kiểm đã có (không máy)

- `v4/thu/chay_thu.sh`: kết quả ở `v4/thu/chay_thu.out` (số đạt/trượt ở LOG phiên 12). Gồm: mốc lượt so hằng số SQL B (41706 → dừng trước Event, DB không đổi; T08: Booking giả khớp mốc 41706 nhưng SQL B ghim 41705 → `mo-luot` dừng mã 3 với lý do `moc_lech_SQL_B`, không ghi file mốc); thiếu mốc lượt; mốc môi trường khác file; T32 = nhánh **kiểm DICH thất bại trên nháp** (SQL giả trả 0 và `DA_COMMIT`, kiểm trả 8, `KET_QUA` ghi `kiem_dich_tren_nhap_rc8`); cờ ACL → chuẩn-bị 3, `ghi` từ chối cờ `khong`; không xóa được nháp → `CON_DB_NHAP`; `xac-dinh` khi tiến trình ghi còn sống/còn tiến trình mang app → 11; tiến trình đã chết → đọc trạng thái; lỗi trước ghi → không `app.txt`; khôi phục: thiếu duyệt Minh, đưa thư mục chuẩn-bị, lượt ghi `DA_GHI`, liên kết ngược sai → 2; khôi phục đạt (OID gốc ở `_hong_`); restore lỗi → 13 với OID gốc ở tên chính; trả tên lỗi → 16; đổi tên đầu lỗi → 16; tạo DB lỗi → 13; băm bản hiện tại lỗi → 13; dịch vụ không dừng → 12 (`Running=true`); còn kết nối → 17; không khỏe → 15 (`true|unhealthy`); `BAO` lạ ở Booking và Event → 7; các ca v3 giữ lại.
- Phép đột biến: `v4/thu/dot-bien.out` (8 đột biến D1–D8, mỗi đột biến phải làm ít nhất một phép thử trượt). Lượt đầu D4 (bỏ so mốc với SQL B) không làm phép thử nào trượt, vì T02 dừng nhờ kiểm CU chứ không nhờ phép so; đã thêm T08 để tách riêng phép so, rồi chạy lại cả bộ thử và cả 8 đột biến.
- **Chưa kiểm:** mọi lệnh trên PostgreSQL thật (băm `\gexec`, dump/restore, CREATE/ALTER/DROP DATABASE, OID, `pg_stat_user_tables`), `docker stop/start`, `ps` trên exp-app. Bước chạy thử trên nháp là lần đầu SQL thuận chạy trên PostgreSQL, trên bản sao.

## 8. Thời gian S5 pha ghi (CHƯA-KIỂM)

Như bản 6 §7, cộng 4 × 2 lần `b1c` (~1 phút mỗi lần) và `mo-luot` (~2 phút): **≈ 75–130 phút**.

## 9. Phạm vi kết luận

Như bản 4 §9: E6 chỉ kết luận các bản sao trong PostgreSQL mang giá trị đích. Không kết luận dịch vụ đã dùng giá trị mới (cache, bộ nhớ).
