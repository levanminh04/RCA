# Báo cáo sáng 13/11/2026 — chiến dịch M1-FlashTicket (ghi 02:25Z = 09:25 giờ VN, trễ mốc 07:00 do hết hạn mức Claude 23:55Z–~02:10Z)

Điều phối: Claude (nhận quyền 12/11 21:16Z). Chi tiết sống: `tasks/T-062-dem-chang-1-4/CHECKPOINT-CHIEN-DICH.md`. Mọi số dưới có nguồn ở file nêu.

## 1. Đã làm, đã kiểm

**Hạ tầng quan sát (T-063)** — biên bản, hash, hoàn tác: `results/T-063/quan-sat/thay-doi-may.md`.
- Prometheus giữ 30 ngày (trước 2 ngày); dữ liệu E1 T-062 còn truy được (TD-01).
- Nâng tên queue RabbitMQ, tên bảng PostgreSQL thành nhãn: trước đó mọi queue/bảng gộp một chuỗi, counter cho tốc độ âm (TD-02). Hệ quả: metric queue/bảng của 9 ca T-062 không dùng được.
- Thu CPU throttling, giới hạn CPU, restart, uptime theo container (TD-03).
- Bảo trì `exp-app` lượt 1 (TD-04..08): log của **12 dịch vụ** (gồm Postgres, RabbitMQ, Redis, Mongo) vào Loki theo nhãn compose, không mất log khi tạo lại container; đầu dò liveness 8 đích; Booking nối AMQP qua proxy (chuẩn bị ô consumer chậm); span bọc tác vụ định kỳ Keycloak (đạt ở lần thử 3). Image ứng dụng không đổi (`6b21ed55`).

**Tải mua vé (T-062 phụ lục 2, Codex L1)** — `results/T-062/tai-2/bao-cao-L1.md`, `lap-2-luot.md`.
- VNPay giả, 20 người mua, sự kiện 100.000 chỗ; giao dịch `COMPLETED` có vé.
- Hai lượt 10 phút: mỗi lượt 720 hành trình (70/20/5/5), 144 mua trọn, 0 lỗi/401/rơi lượt; gateway 3.097 vs 3.092 request (chênh 0,161%, chỉ ở bước poll). Claude kiểm số trên file và **chấp nhận làm chuẩn tải**.
- L1 tự phát hiện và sửa lỗi `traceparent` của k6 bản đầu (span gốc gateway mồ côi).

**Kiểm dữ liệu trên tải mua vé** — `results/T-063/kiem-r/BAO-CAO.md`: R-04 (message) ĐẠT lần đầu (1.561 producer/consumer); R-09 0 span mồ côi; R-01 chỉ thiếu ở thao tác điều khiển AMQP; R-05 một phần (instance id log ≠ trace).

**Phân tích cơ chế trên dữ liệu cũ** (T-063):
- CPU-BOOK (`cpu-book/PHAN-TICH.md`): phép thử có đối chứng — cùng ~0,95 lõi Booking dùng, 2 luồng đốt làm áp lực CPU máy ×6, p99 đường không qua Booking ×3; 1 luồng nhẹ hơn nhiều. Cơ chế: tranh CPU máy theo cụm (CFS), không lan qua lời gọi. Đề xuất hai ô CPU-BOOK-1/-2.
- Ca không lỗi bị `CAUSE_FOUND` (`ca-nen/PHAN-TICH.md`): giả thuyết đầu dò t+63 không được ủng hộ; nguyên nhân là thay đổi thật nhưng nhỏ (< 0,2 ms) của thao tác nền.
- Span gốc (`span-goc/PHAN-TICH.md`), "chết im" (`h5/PHAN-TICH.md`: pause làm mọi tín hiệu mất cùng lúc → đã thêm đầu dò liveness).
- B16 bản 2 (`b16-ban-2.md`, phiên Claude phụ): 11 thiếu đặc tả, 9 triển khai chưa đạt, 6 chưa rõ cơ chế, 17 đề xuất có nguồn. Chưa phản biện.

**M1-FT (T-064)** — `tasks/T-064-m1-flashticket/LOG.md`, `results/T-064/so-bien-the.jsonl`.
- `src/m1_ft` tắt thay đổi trùng SHA P7 9/9 ca trên `exp-obs`; laptop lệch chữ số cuối → mọi lần chấm chạy trên `exp-obs` (WHY-81).
- Thành phần: H1a/b/c (cạnh DB/cache/gọi, định vị, danh sách chung — WHY-82), H2 (JVM/cgroup), H3 (pool), H6a (trace bảo trì), H7a/b/c (chuẩn hóa theo tải), H8 (sàn độ lớn 1 ms).
- 15 biến thể **chỉ kiểm cài đặt** trên 9 ca T-062 (không phải tập chọn): tổ hợp H1c + H7c + H8 giữ AC@1 = 5, K = 0/4, đúng cạnh gốc hạng 2 ở 2/2 ô cạnh. H1c/H7c được thiết kế sau khi xem 9 ca này → không phải bằng chứng hiệu quả.

**Grafana (T-065, Codex L3)** — `results/T-065/kiem/001/BAO-CAO.md`: 2 dashboard mới, lớp thao tác P7, liên kết Loki; kiểm API 9 ca/1.197 thao tác không lỗi. **Đạt một phần.**

## 2. Đang chạy

- L1b (Codex): đổi bậc tải tại mốc t, độ bền tunnel/mock, kiểm lại giao dịch sau bảo trì. Codex hết hạn mức 23:51Z; **bộ gọi đang chờ thật** tới 03:13Z rồi tự gọi tiếp (lần đầu cơ chế hết hạn → chờ → gọi tiếp chạy ngoài mô phỏng; kết quả sẽ ghi ở `results/T-063/dieu-phoi/`).

## 3. Phần còn mở, việc kế tiếp

1. Sau L1b: kiểm R trên gói sau bảo trì → xác nhận can thiệp từng ô (`runner2.py d2`, ~45 phút) → chốt lịch 15 chu kỳ + hồ sơ luật 21 + hồ sơ đóng băng → **đợt thu chính ~7,5 giờ** (dự kiến bắt đầu trong ngày 13/11 nếu D2 đạt).
2. Thay SLOW-BOOK bằng HTTP5-EVENT ở hai mức tải (WHY-83) vì hook chỉ nhắm được một đơn cố định.
3. Phản biện chéo: Claude phản biện L1, L3; Codex phản biện T-063, T-064.
4. M1-FT: H4 (queue), H5 (liveness), chấm trên tập chọn dev bản 2 sau đợt thu.

## 4. Cần Minh quyết

- **Phát Codex full access** bị bộ phân loại an toàn của ứng dụng chặn (21:32Z); Codex đang chạy trong sandbox `workspace-write` (ghi được hai repo, có mạng). Hệ quả: L3 không có trình duyệt → phần bấm thử Grafana thật chưa làm. Cách gỡ: (a) Minh thêm quy tắc cho phép lệnh `py -3 results/T-063/dieu-phoi/goi_codex.py … --che-do full` trong cài đặt Claude Code; hoặc (b) Minh đăng nhập Grafana trong trình duyệt của ứng dụng (Claude không nhập mật khẩu), Claude bấm kiểm.
- **Lịch `m1ft-tiep-nhan`** chưa có (công cụ từ chối khi Claude tạo). Không có lịch thì khi ứng dụng khởi động lại, Minh phải dán lại `PROMPT-PHIEN-MOI.md`. Cách tạo: `tasks/T-062-dem-chang-1-4/LICH-TU-TIEP-NHAN.md`.
- Chưa commit repo RCA (theo quyền: trình sau).
