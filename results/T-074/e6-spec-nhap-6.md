# Nháp SPEC bổ sung T-074 — E6 (K0), bản 6

- **Trạng thái:** NHÁP. Claude (phiên `danh-gia-w6`), 24/11/2026. Bản 6 thay phần ghi/hoàn tác của `e6-spec-nhap-5.md` (giữ hash bản 5 ở `SHA256SUMS-8`). Phần không nhắc ở đây giữ như bản 4–5.
- **Căn cứ quyền:** Minh duyệt 24/11 "Duyệt kết hợp" (điều phối chuyển ~04:00Z): (1) giữ SQL thuận v2 biến thể B; (2) Codex sửa ngay lỗi nhỏ hai bên đồng thuận (CX-45: `v3/b1c-yen.sh`, `v3/b0.sh`), một phiên Codex khác kiểm (CX-45b); (3) **bỏ SQL nghịch** và cách phân loại 50% "toàn CU/toàn DICH/lẫn"; hoàn tác bằng **khôi phục từ dump chụp ngay trước khi ghi**, có thử khôi phục vào DB nháp trước; (4) chạy có người theo dõi, mỗi lần một DB. Minh duyệt 24/11 "Duyệt chạy thử" (điều phối ~04:10Z): sau khi thử khôi phục vào DB nháp, chạy SQL thuận B (nguyên file v2) và kiểm DICH trên DB nháp rồi mới ghi DB thật; lỗi → dừng DB đó, không ghi DB thật, báo điều phối. Biến thể **B** (giữ sức chứa 100.000, chỉ sửa ngày; DECISIONS 24/11 mục 1).
- **Sửa theo:** CX-41, CX-41b (đối chiếu ở LOG phiên 10).
- **Pha ghi chưa giao.** Codex kiểm v3 (2 phiên) trước khi phát. Hạn bán hiện tại 02/12.

## 1. Bộ thực thi v3 (`results/T-074/e6/v3/`)

| File | Người viết | Việc |
|---|---|---|
| `b0.sh` | Codex CX-45 | bước 0 chỉ đọc, ba máy |
| `b1c-yen.sh` | Codex CX-45 | kiểm yên (chỉ SELECT): đơn chưa kết thúc, `held`/`purchased`, 4 số outbox, hàng đợi |
| `chay.sh` | Claude | chuẩn-bị / ghi / xác-định / khôi-phục / kiểm; chỉ chiều thuận B; mỗi lần một DB |
| `thu/` | Claude | docker/psql/pg_dump/pg_restore/df giả; 64 phép thử; phép đột biến |
| `thu-codex/` | Codex CX-45 | thử cho hai script trên |

SQL thuận và kiểm: **nguyên văn** `v2/sql/B/thuan-<db>.sql`, `kiem-khoa-<db>.sql`, `truong.txt`, `phu.txt`; `chay.sh` từ chối chạy nếu sha256 lệch `v2/SHA256SUMS`. `v2/sql/B/nghich-*.sql` và chế độ `nghich`, `kiem … DOC` của v2 **không dùng**.

## 2. Thủ tục pha ghi (có người theo dõi; mỗi DB một vòng)

Thứ tự DB: `event` → `booking` → `ticket` → `payment`. Mọi lệnh chạy nền trên exp-app (`setsid nohup bash chay.sh … > <log> 2>&1 &`), người trực đọc log. Đứt SSH không giết tiến trình.

0. `bash v3/b0.sh` (ba máy) → đạt. `bash v3/b1c-yen.sh` → yên; ghi lại `purchased`, `held` làm **mốc kiểm yên** (`MOC_PURCHASED`, `MOC_HELD`). Chạy `v2/thu/thu-sql-chi-doc.sql` (J01–J11, chỉ đọc). `bash chay.sh kiem CU event booking ticket payment` → 0.
1. **Chuẩn-bị** `bash chay.sh chuan-bi <db>` — không ghi DB thật:
   1. đọc `pg_database_size`, chủ, mã hóa, locale, ACL; **kiểm đĩa**: thư mục `/home/ubuntu/t074/e6` còn ≥ kích thước DB + 1 GiB; volume PostgreSQL còn ≥ 2 × kích thước DB + 1 GiB (DB nháp + WAL; khi khôi phục còn giữ bản hỏng). Số tham chiếu: dump `-Fc` 4 DB nghiệp vụ ở E1 (20/11, ~40 nghìn đơn) tổng ~90 MB, lâu nhất 15 giây cho cả 5 DB (`results/T-071/e1/moc-db.json`); số đo thật lấy lúc chạy.
   2. `kiem-khoa` dưới `FOR SHARE`: cả nhóm trường của DB ở trạng thái **đầu** (toàn CU), PHU đúng, với booking `purchased`/`held` = mốc kiểm yên.
   3. chữ ký DML (`sum(n_tup_ins+n_tup_upd+n_tup_del)`) trước dump.
   4. `pg_dump -Fc` → file + sha256; `pg_restore -l` đọc được.
   5. tạo DB nháp `e6n_<db>_<mã>` (cùng chủ/mã hóa/locale, `template0`), `pg_restore --exit-on-error` dump vào đó.
   6. **băm nội dung** DB thật và DB nháp (một snapshot `REPEATABLE READ READ ONLY` mỗi bên): mỗi bảng `count(*)` và md5 của các md5 từng dòng đã sắp; mọi sequence; số bảng > 0. Phải trùng từng dòng. Trùng ⇒ dump khôi phục được **và** DB thật chưa đổi kể từ dump.
   7. **Chạy thử trên DB nháp (bắt buộc; Minh duyệt 24/11):** chạy SQL thuận B nguyên văn trên DB nháp (rc 0 và dấu `DA_COMMIT <DB nháp>`), rồi `kiem-khoa` mong **DICH** trên DB nháp. Trượt → mã 3, **dừng DB đó, không ghi DB thật, báo điều phối**. `ghi` từ chối thư mục chuẩn-bị không có dấu đạt bước này.
   8. xóa DB nháp, xác nhận không còn; chữ ký DML không đổi từ bước 3.
   → `DAT` (mã 0); mọi trượt → mã 3, **chưa ghi DB thật**.
2. Người trực đọc `nhat-ky.txt` của chuẩn-bị (đĩa, băm, số bảng), rồi phát **Ghi** `bash chay.sh ghi <db> <thư-mục-chuẩn-bị>`:
   - nhận chuẩn-bị `DAT` (gồm chạy thử trên nháp đạt), đúng DB, chưa quá 30 phút, **chỉ dùng một lần** (`mkdir DA_DUNG` nguyên tử), dump khớp sha256; chữ ký DML bằng lúc chuẩn-bị; `kiem-khoa` vẫn đúng đầu;
   - chạy thuận v2 với `application_name` riêng của lượt;
   - **rc 0 + `DA_COMMIT <db>`** + `kiem-khoa` đúng **đích B** → `DA_GHI` (mã 20).
   - **Mọi trường hợp khác** (rc 3, 5, 2, 125, đứt kết nối, thiếu dấu `DA_COMMIT`, kiểm sau không đạt) → **chưa rõ** → xác định (§3). Không suy "đã rollback" từ mã thoát.
3. Người trực xác nhận mã 20 rồi mới sang DB kế. Sau DB cuối: `bash chay.sh kiem DICH event booking ticket payment` → 0; mốc PostgreSQL (bản 4 bước 4); khóa bản (bản 4 bước 7).

Mã thoát `chay.sh`: 0 đạt; 2 sai cách gọi/khóa/file v2 lệch/danh sách trường không đọc được; 3 chuẩn bị không đạt (chưa ghi); 5 lỗi đọc; 6 sai trạng thái; 7 thiếu/lạ/lặp tên; 8 PHU/BAO sai; 11 phiên ghi cũ còn; 20 đã ghi; 21 chưa ghi; 22 khác cả hai; 12–15 khôi phục không đạt (§4). Khóa toàn cục `/home/ubuntu/t074/e6/.khoa-ghi-B` (mkdir nguyên tử) chặn hai tiến trình chuẩn-bị/ghi/khôi-phục cùng lúc; mỗi lượt một thư mục tạo nguyên tử, không ghi đè.

## 3. Xác định kết cục (thay §5 bản 5)

`bash chay.sh xac-dinh <db> <thư-mục-ghi>` (tự chạy trong `ghi` khi chưa rõ; gọi lại được):
1. Chờ phiên có `application_name` của lượt biến khỏi `pg_stat_activity` (≤ 120 s; còn → mã 11, người trực chờ rồi gọi lại; **không** tự `pg_terminate_backend`).
2. `kiem-khoa` dưới `FOR SHARE`; so **cả nhóm trường của DB đó** (theo `truong.txt`, so tên theo nghĩa đen) và PHU, BAO:
   - khớp **đích B** (Event 5 DICH + 1 CU; Booking 4 DICH + 2 CU; Ticket 2 DICH; Payment 1 DICH; sức chứa CU) và PHU/BAO đúng mốc → **ĐÃ GHI** (20);
   - khớp **đầu** (toàn CU) và PHU/BAO đúng mốc → **CHƯA GHI** (21) → tìm nguyên nhân, chuẩn-bị mới, ghi lại;
   - **khác cả hai** (kể cả trường đúng đích nhưng `purchased`/`held` khác mốc) → **KHÁC** (22) → khôi phục dump DB đó (§4);
   - đầu ra thiếu/lạ/lặp tên → mã 7, gọi lại; không quyết.
Không còn chiều nghịch nên không còn nhập nhằng "toàn CU là đảo thành công".

## 4. Khôi phục dump vào DB thật (chỉ khi KHÁC hoặc Minh quyết)

`E6_XAC_NHAN_KHOI_PHUC=<db> bash chay.sh khoi-phuc <db> <thư-mục-chuẩn-bị-đã-dùng>`:
1. dump khớp sha256; DB không có ACL/role setting riêng (ghi ở chuẩn-bị; có → khôi phục tay, dừng); đĩa đủ.
2. **Dừng dịch vụ ứng dụng của DB đó** (`docker stop`: event/booking/ticket/payment-service). Chờ kết nối tới DB về 0 (≤ 60 s); còn → mã 12, in danh sách kết nối, dịch vụ để dừng, người trực quyết.
3. `ALTER DATABASE <db>_db RENAME TO <db>_db_hong_<mã>` — **giữ bản hiện tại** (luật 10); in danh sách bảng khác giữa dump và bản này (thấy được có ghi lạ ngoài lượt không).
4. `CREATE DATABASE <db>_db` cùng chủ/mã hóa/locale; `pg_restore --exit-on-error`. Lỗi → xóa DB mới, đổi `_hong_` về tên cũ (trạng thái trước khôi phục), mã 13, dịch vụ để dừng.
5. Băm nội dung DB mới **trùng** băm DB nháp lúc chuẩn-bị (= nội dung dump); `kiem-khoa` đúng đầu. Không trùng → mã 14, dịch vụ để dừng.
6. `docker start` dịch vụ; chờ `running` và `healthy` (nếu có healthcheck) ≤ 180 s; không lên → mã 15.
7. Bản `_hong_` giữ lại; xóa cần Minh duyệt.

**Vì sao chọn thay cả DB thay vì khôi phục theo bảng:** dump `-Fc` khôi phục từng bảng (`pg_restore -t --data-only`) phải xóa dữ liệu bảng trước, vướng khóa ngoại và trigger, và dịch vụ vẫn có thể ghi xen; thay cả DB với dịch vụ dừng là một thao tác đã thử ở bước 1.5 trên chính dump đó. Mặt trái: dịch vụ của DB đó ngừng vài phút; mọi ghi sau thời điểm dump (nếu có) mất khỏi DB chính nhưng còn trong bản `_hong_` và hiện trong danh sách bảng khác.

## 5. Lỗi giữa chừng (luật 21)

| Khi | Nhận biết | Xử lý | Chạy lại / mất |
|---|---|---|---|
| ~10% — trước khi ghi DB đầu | b0/b1c/J01–J11/`kiem CU` trượt; chuẩn-bị mã 3 (đĩa, dump, thử khôi phục, băm khác, DML đổi) | chưa ghi gì; DB nháp đã xóa (hoặc báo còn); tìm nguyên nhân | chuẩn-bị lại 3–8 phút/DB |
| ~50% — DB thứ k | ghi trả ≠ 20 → xác định: 21 | DB 1…k−1 đã xác nhận 20, giữ; DB k chưa ghi; sửa nguyên nhân, chuẩn-bị mới, ghi lại DB k | 5–15 phút |
| ~50% | xác định: 20 | coi như đạt; sang DB kế | 2 phút |
| ~50% | xác định: 22 | khôi phục DB k (§4) → DB k về đầu; DB 1…k−1 giữ; trình Minh trước khi ghi lại DB k | 5–15 phút khôi phục (ước) + điều tra |
| ~50% | 11 (phiên cũ còn) | chờ; gọi lại `xac-dinh`; không tự kết thúc phiên | phút |
| ~99% — sau DB cuối | `kiem DICH` 4 DB trượt; mốc/khóa bản lỗi | `xac-dinh` từng DB trượt → như trên; mốc/khóa bản: chỉ làm lại hiện vật | ≤ 15 phút + điều tra |
| bất kỳ | khôi phục mã 12–15 | dịch vụ DB đó đang dừng; giữ máy ở điều phối; trình Minh | điều tra |

Trong lúc DB 1…k−1 đã ghi mà DB k chưa, các dịch vụ thấy ngày lệch nhau; hệ không có tải (bước 0) nên không có đơn mới dùng ngày lệch. W7 chỉ phát khi đủ 4 DB đạt 20 và `kiem DICH` 4 DB đạt.

## 6. Bằng chứng kiểm đã có (không máy)

- `v3/thu/chay_thu.sh`: **64/64 đạt** (`v3/thu/chay_thu.out`) với docker/psql/pg_dump/pg_restore/df giả. Gồm phản ví dụ CX-41/41b: rc 3 sau COMMIT → ĐÃ GHI (không "rollback"); thiếu `DA_COMMIT` → xác định; đích B Event 5 DICH + 1 CU, Booking 4 DICH + 2 CU → ĐÃ GHI; `purchased` 41706 → 8; `eventXstarts_at`, tên lạ, tên lặp, thiếu tên → 7; `truong.txt` sai dạng/rỗng, `phu.txt` không có → 2; tên DB lặp → 2; trùng mã lượt, khóa đang giữ → 2. Nhánh mới: thiếu đĩa (host/volume), ghi xen sau dump (băm khác), thử khôi phục lỗi, pg_dump lỗi, DML đổi, chuẩn-bị quá hạn/dùng lại/khác DB, phiên cũ còn, khôi phục đạt (băm sau = dump, dịch vụ chạy lại, giữ `_hong_`), pg_restore lỗi (trả tên cũ), còn kết nối, dịch vụ không khỏe, chạy thử thuận trên nháp (đạt; thuận lỗi; kiểm DICH trên nháp không đạt → mã 3, DB thật vẫn CU), `ghi` từ chối chuẩn-bị thiếu dấu chạy thử.
- Bộ thử bắt được một lỗi thật của bản viết đầu: `danh_gia` chia file theo `FNR==1`, với Ticket (không có dòng PHU) đầu ra kiểm bị đọc như danh sách PHU → mã 7 sai. Đã sửa (chia theo `FILENAME`).
- Phép đột biến (`v3/thu/dot-bien.out`): 6 đột biến, mỗi đột biến làm bộ thử trượt ít nhất một phép — D1 mã khác 0 coi là chưa ghi (kiểu v2): 6 trượt; D2 bỏ so băm thật/nháp: 1; D3 so tên kiểu regex: 1; D4 bỏ đối chiếu `purchased` với mốc: 3; D5 khôi phục không trả tên cũ khi `pg_restore` lỗi: 1; D6 `ghi` không đòi dấu chạy thử trên nháp: 1.
- **Chưa kiểm:** mọi lệnh trên PostgreSQL thật (bước 1.7 sẽ là lần đầu SQL thuận chạy trên PostgreSQL, trên bản sao) — `\gexec` băm, `pg_dump`/`pg_restore` vào DB nháp, `CREATE/ALTER/DROP DATABASE`, `pg_stat_user_tables` (bộ đếm gom theo chu kỳ, có thể trễ tới vài giây: chữ ký DML là chốt phụ; chốt chính là băm), `docker stop/start` dịch vụ.

## 7. Thời gian S5 pha ghi (CHƯA-KIỂM)

| Việc | Phút |
|---|---|
| bước 0 (b0, b1c, J01–J11, `kiem CU`) | 15–25 |
| 4 × chuẩn-bị (dump, thử khôi phục, băm; booking/payment lớn nhất) | 4 × 3–8 |
| 4 × người trực đọc + ghi + xác nhận | 4 × 4–8 |
| `kiem DICH`, mốc PostgreSQL, khóa bản | 20–30 |
| **Tổng** | **≈ 65–120** (1,1–2 giờ) |

Lỗi: mỗi lần chuẩn-bị lại +3–8; mỗi lần khôi phục một DB +5–15 (ước, chưa đo `pg_restore` trên exp-app) + điều tra. Bước 1.7 thêm ~1–2 phút/DB (đã tính trong chuẩn-bị).

## 8. Cần Minh quyết

1. ~~Bước 1.7~~ — **đã duyệt** (Minh 24/11 "Duyệt chạy thử"). Giới hạn còn lại: không thử được điều kiện chỉ có trên DB thật (khóa với phiên ứng dụng).
2. **Khôi phục thay cả DB với dịch vụ dừng (§4).** Đề xuất: duyệt cùng v3. Mặt trái: dừng một dịch vụ vài phút ở nhánh lỗi; bản `_hong_` chiếm đĩa tới khi Minh cho xóa.

## 9. Phạm vi kết luận

Như bản 4 §9: E6 chỉ kết luận các bản sao trong PostgreSQL mang giá trị đích. Không kết luận dịch vụ đã dùng giá trị mới (cache, bộ nhớ).
