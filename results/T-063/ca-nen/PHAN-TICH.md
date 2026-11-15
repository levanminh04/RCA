# T-063 — Ca không tiêm lỗi bị `CAUSE_FOUND`: đầu dò (H1) hay khác? (12/11/2026 21:50Z, Claude)

Câu hỏi SPEC T-063: "3 ca bình thường bị cờ do đầu dò (H1) hay ngẫu nhiên (H3)?" → quyết định lịch đầu dò của bộ chạy mới. Tiếp nối `results/T-062/chay/thu-gia/LAN-CA-NEN.md` mục 3.1 (phép kiểm còn thiếu: thời gian độc quyền E1 theo 10 s).

## 1. Phép kiểm

[`doc_quyen_10s.py`](doc_quyen_10s.py): với mọi kênh `op|…` M1 P7 gắn cờ ở 3 ca bình thường (`a5539fba`, `6c1a9fd8`, `e8661e0a`) và ca FLASH (`00eaea92`), tính lại thời gian độc quyền E1 = U của từng span bằng chính code M1 (`span.chuan_bi`, `span.mau_thao_tac`, cùng miền cắt với `chuoi._chay`) trên `method-input.json` đã lưu, so với ngưỡng `h` mà M1 đã dùng (`extra.don_vi_phan_vi[ma].h`), đếm theo khúc 10 s quanh t. Kết quả: [`doc-quyen-10s.json`](doc-quyen-10s.json). Chạy trên laptop (chỉ đếm, không chấm; lệch ulp không đổi phép so ngưỡng ở mức µs nguyên).

## 2. Quan sát

- **Không dồn quanh đầu dò t+63.** Khúc [50, 80) s chiếm 10% cửa sổ A. Số mẫu vượt trong khúc đó / tổng vượt ở A: Keycloak DELETE Outbox 1/135; Keycloak SELECT PersistentUserSession 0/68; Event `OutboxWorker.relay` 3/30; User `organizer_applications` 1/6; Event `tbl_event_sectors` 5/58; Event `tbl_outbox_messages` 1/25; Ticket `TicketJobs.cancel` 3/50. Không kênh nào vượt mức kỳ vọng đều.
- **Ba dạng thay đổi** (bảng theo khúc 60 s, N | A):
  - *Một đợt kéo dài*: Keycloak `DELETE OutboxEntryEntity` (chạy mỗi giây): vượt 0–5/60 ở N, rồi 37/60, **60/60**, 36/60 ở [t+60, t+240), về 1/60 ở khúc cuối. Trung vị thời gian độc quyền 99 µs (N) → 204 µs (trong đợt) → 112 µs (ngoài đợt). CPU container Keycloak, CPU JVM, GC Keycloak, CPU Postgres theo khúc 60 s **không đổi** trong đợt.
  - *Tăng dần qua A*: `TicketJobs.cancel` 3 → 9, 6, 5, 12, **18**/60; Payment `findDueForUpdate` 1–2 → 8, 7/60; Payment `tbl_outbox_messages` 4 → 8/60; Event `tbl_outbox_messages` 1 → 5/60.
  - *Định kỳ, dừng*: Keycloak `SELECT PersistentUserSessionEntity` chạy theo cụm ~3 phút một lần, vượt 20–34 mẫu mỗi cụm ở **cả N và A** (dao động giữa các cụm, không phải thay đổi).
- Độ lớn tuyệt đối: dưới 0,2 ms ở mọi kênh trên (vd. Keycloak DELETE +105 µs trung vị; `TicketJobs.cancel` trung vị 251 → 248–305 µs).
- **Phát hiện kèm:** metric mức bảng/thao tác của PostgreSQL trước 21:35Z 12/11 cho tốc độ **âm** (`postgresql_operations_total`, `postgresql_rows` của `keycloak_db`) — counter của nhiều bảng ghi đè nhau do mất `postgresql.table.name` (TD-02, `results/T-063/quan-sat/thay-doi-may.md`). Các metric này của 9 ca T-062 **không dùng được** để phân xử.

## 3. Kết luận (tách bậc)

- **H1 (đầu dò t+63) — không được ủng hộ** ở mức thời điểm vượt ngưỡng: không kênh nào dồn quanh t+63. Mẫu placebo cũ (t: 3/3, t+120: 0/3, t+240: 1/3) giải thích được mà không cần H1: ví dụ đợt Keycloak [t+60, t+240) — dời mốc +120 làm cửa sổ N chứa 60 s của đợt và A chứa 120 s, độ tương phản giảm. Chưa kiểm phép giải thích này cho cả 3 ca.
- **H3 "ngẫu nhiên thuần" — không mô tả đúng.** Thay đổi có cấu trúc thời gian (một đợt; xu hướng tăng), tức **thao tác nền không dừng** (non-stationary) ở thang phút: chính M1 phát hiện đúng là có thay đổi, nhưng thay đổi nhỏ (< 0,2 ms), trên thao tác nền không thuộc đường giao dịch của tải, và không đi kèm suy giảm giao dịch.
- **Cơ chế của từng đợt — chưa phân xử.** Ứng viên cho đợt Keycloak: autovacuum/checkpoint trên `keycloak_db`, khóa bảng outbox, xử lý nội bộ Keycloak. Thiếu: metric PostgreSQL theo bảng (đã có từ 21:35Z, TD-02), log hạ tầng Postgres (chưa thu — cách A của Collector), `pg_stat_activity`/autovacuum log. Ứng viên cho xu hướng tăng: bảng outbox/issuance lớn dần qua thời gian chạy; thiếu: kích thước bảng theo thời gian (đã có từ TD-02).

## 4. Hệ quả

- **Lịch đầu dò bộ chạy mới:** vẫn đặt đầu dò **đối xứng** ở N và A (cùng độ lệch so với đầu mỗi nửa) hoặc ngoài cửa sổ phương pháp. H1 không được ủng hộ, nhưng đối xứng loại hẳn yếu tố gây nhiễu này với chi phí 0.
- **T-064 H6/H8:** điều kiện thất bại thật của P7 ở ca nền là "thay đổi thật nhưng nhỏ của thao tác nền". Thành phần H6/H8 phải dựa trên nguyên lý (độ lớn có ý nghĩa thực hành, hoặc vai trò thao tác nền ngoài đường giao dịch), **không** dựa trên đáp án từng ca; và phải kiểm không che các ô có lỗi nhỏ thật (vd. EVENT-DB-LAT 30 ms).
- **T-063 thu dữ liệu:** thu log hạ tầng (Postgres, RabbitMQ, Redis, Mongo) qua cách A để các đợt kiểu này phân xử được ở đợt thu chính.
