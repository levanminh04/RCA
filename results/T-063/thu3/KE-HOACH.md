# T-063 thu bù 3 — Kế hoạch (bản 1, 14/11/2026 ~05:09Z, trước khi chạm máy; đo H4 bắt đầu 05:10:56Z)

Người làm: Claude, phiên B (`local_33bac1e1…`). Brief: `tasks/T-062-dem-chang-1-4/PHIEN-B-BRIEF.md`. Quyền: DECISIONS 13/11 "Bổ sung quyền điều phối…", "Chạy bộ điều phối đợt thu trên `exp-obs`"; 14/11 "Hook thử H3…".

Bản này ghi **trước** mọi đo đạc của thu bù 3. Phần nào chốt sau khi đo (cường độ pool, khả thi H4) có quy tắc chọn khai ở đây; kết quả đo và lựa chọn ghi ở mục "Bổ sung" cuối file, không sửa dòng trên.

## 1. Vì sao thu bù

T-064 cần ô lỗi để phân xử H3 (kênh pool) và H4 (kênh queue). Đợt thu 2 không có ô nào cho hai hướng này (`results/T-063/bao-cao.md` mục 2): POOL-EVENT không thử được vì hook `pool.hold` chỉ chạy ở Booking; CONSUMER-BOOK-SLOW không xác nhận được sau 3 lần (`chay/D2B-KET-QUA.md`).

## 2. Ô sẽ thu

Vị trí so với 12 ô đánh giá T-059 (DB-BOOK-LAT, POOL-BOOK, DB-BOOK-DOWN, REDIS-GW, TICKET-PAUSE, HTTP5-BOOK, SLOW-EVENT, NET-GW-EVENT, NET-PAY-BOOK, CPU-EVENT, VNPAY-REFUND-LAT, SAGA-TICKET-FAIL): mọi ô dưới khác vị trí.

| Ô | Hướng | Cách tiêm | Cường độ, lý do | Đầu dò độc lập (không qua M1, không gọi HTTP app) | Tập chấp nhận | Vị trí so với ô đánh giá |
|---|---|---|---|---|---|---|
| POOL-EVENT | H3 | hook `pool.hold` của Event (sửa điều kiện `poll()`, mục 3) | 4 hoặc 5 connection trên pool max 5; chọn bằng chạy thử ngắn theo quy tắc mục 4 | audit hook `pool.hold.started` (kèm `active/idle/pending` của MXBean); Prometheus `db_client_connections_usage{state=used}`, `db_client_connections_pending_requests` của pool Event | event-service | POOL-BOOK là Booking; ô này ở Event |
| CONSUMER-BOOK-SLOW-X3 (tên chốt sau đo) | H4 | toxic `bandwidth` downstream trên proxy `booking-amqp` (Booking ← broker), dưới tải ×3 suốt chu kỳ | rate 1 KB/s (nhỏ nhất của toxiproxy); chỉ thu nếu đo khả thi đạt (mục 5) | `rabbitmqctl` trong container broker: ready/unacked theo queue `booking.*.q`, `send_oct` kết nối của Booking; Prometheus `queue-ready/unacked` | booking-service; cạnh booking-service ↔ broker | NET-PAY-BOOK là HTTP Payment→Booking; SAGA-TICKET-FAIL là hook phát vé Ticket. Ô này ở kết nối AMQP Booking |
| BINH-THUONG | đối chứng bản build mới | không can thiệp, tải ×1 như đợt 2 | — | như ô BINH-THUONG đợt 2 | — | — |
| EVENT-DB-LAT | đối chứng ô cũ trên bản mới | toxic latency 30 ms `event-jdbc`, như đợt 2 | giữ nguyên đợt 2 để so cùng điều kiện | như đợt 2 | event-service | ô dev T-059 |
| BINH-THUONG-X3 | đối chứng cùng bậc tải với ô H4 | không can thiệp, tải ×3 suốt chu kỳ | cùng bậc tải ô H4 (brief 2c.1) | như BINH-THUONG | — | — |

Ô tùy chọn H8-adapter (container tạo lại trong cửa sổ): chỉ thu nếu `results/T-064/phien-c/YEU-CAU-O.md` có yêu cầu trước lúc khóa lịch, và đủ ba điều kiện của brief 2a. Lúc 05:15Z file chưa có. Lý do mặc định không thu: cách tiêm (tạo lại container giữa cửa sổ) cần thêm thao tác compose trong bộ tiêm, rủi ro cấu hình khi tạo lại, và chưa có câu hỏi T-064 cụ thể cần nó.

Vì sao bản build mới cần đối chứng: build lại image Event tạo bản triển khai khác bản đóng băng 2. Thêm vào đó, sửa `poll()` làm watchdog 100 ms của hook chạy ở Event cả khi không tiêm (đọc file điều khiển). Ca mới không gộp thẳng vào 13 ca cũ; BINH-THUONG và EVENT-DB-LAT trên bản mới cho biết nền và một ô cũ có đổi không.

## 3. Sửa hook H3 và build

- `services/event-service/src/rca-test/java/com/flashticket/event_service/testing/RcaFaults.java` dòng 69 (`start()`) và 163 (`poll()`): bỏ phép so `"event_service".equals("booking_service")`, chỉ giữ điều kiện `enabled`. Dòng 129 (yêu cầu `subject` chỉ cho Booking) giữ nguyên. Đối chiếu Booking: hai file chỉ khác ba dòng này (diff sau khi thay tên service), cùng audit `pool.hold.started`/`pool.acquire.failed`.
- Nền build: commit `6b21ed55` (bản đang chạy). Nhánh `rca/quan-sat-log` đã ở `fba6bc8` (có đổi code nghiệp vụ Event: bỏ API thống kê), nên **không** build từ đầu nhánh. Cách làm: commit sửa lên nhánh `rca/quan-sat-log` (nguồn lưu, push nhánh); trên `exp-app` build Event từ worktree tách tại `6b21ed55` + đúng bản vá đó (cherry-pick cục bộ, ghi SHA và hash bản vá). Hai file `src/rca-test` của `6b21ed55` và `fba6bc8` trùng nhau (đã kiểm `git diff --stat`), nên bản vá áp như nhau.
- Chỉ build và tạo lại `event-service`. Sáu service khác giữ image `arm64-t062-6b21ed55`.
- Kiểm sau triển khai: health, Eureka, luồng mua vé chạy (tải thử ngắn), audit `pool.hold.started` khi tiêm thử, không còn lease sau khi tắt.

## 4. Quy tắc chọn cường độ POOL-EVENT (khai trước khi đo)

Chạy thử ngắn không thu, tải ×1: mỗi giá trị 4 và 5 tiêm 150 s, nghỉ ≥ 90 s giữa hai lần. Đọc Prometheus pool Event (`used`, `pending`), audit (`active/idle/pending`), tỷ lệ lỗi hành trình và 5xx Event.
- Chọn **4** nếu: `used` của pool Event đạt 5 ở ít nhất một mẫu và `pending_requests` > 0 ở ít nhất một mẫu trong pha, **và** hành trình không hỏng toàn bộ (lý do: bão hòa một phần cho tín hiệu chờ pool mà service vẫn phục vụ, đúng cơ chế "cạn pool" khác "DB chết").
- Nếu 4 không cho `pending` > 0: chọn **5** (cạn hẳn), ghi rằng tải ×1 không đủ tranh chấp một connection còn lại.
- Nếu cả hai không làm `used` lên ≥ 4: hook chưa chạy; dừng ô, lần nguyên nhân.

## 5. Ô H4 — thứ tự thử

Lần 1–3 (đợt 2) thất bại ở ~0,5 msg/s. Giả thuyết (chưa kiểm): lưu lượng byte từ broker tới Booking nhỏ hơn 1 KB/s nên toxic không giới hạn được.

1. Đo trên bản hiện hành: tải 420 s, ×1 trong 180 s đầu rồi ×3 (`tai_linux.py --buoc-tai 180 --multiplier 3`; `tai_linux` cho tối đa ×3). Mỗi 15 s đọc `send_oct`/`recv_oct` kết nối AMQP của Booking và ready/unacked các queue `booking.*.q`.
   - **Khả thi** khi tốc độ byte broker→Booking ở bậc ×3 ≥ 1,5 KB/s (gấp 1,5 lần mức giới hạn nhỏ nhất). Khi đó thử toxic 1 KB/s 150 s dưới ×3: đạt nếu tổng unacked + ready của queue Booking tăng ≥ 10 ở cuối pha và quay về ≤ 2 sau khi gỡ.
   - Nếu < 1,5 KB/s: bậc ×3 không đủ; cách 1 cần tải > ×3 hoặc tăng tỷ lệ mua trong kịch bản — giao Codex (người làm phần tải) nếu cần, ghi brief ở `results/T-062/codex/`.
2. Hook làm chậm consumer: **chưa có quyền** (DECISIONS chưa có mục duyệt hook H4). Không làm; nếu cách 1 không đạt thì ghi đề xuất cho Minh.
3. Tối đa 3 lần thử mới cho mỗi hướng (AGENTS §5a).

Rủi ro đã biết của bandwidth trên AMQP: frame heartbeat bị kẹt sau phần tồn, Booking có thể đóng kết nối vì lỡ heartbeat rồi kết nối lại. Đây là cơ chế khác "consumer chậm". Chạy thử phải đọc log Booking và danh sách kết nối broker để phân biệt.

## 6. Thứ tự, thời lượng

Mỗi chu kỳ 30 phút (nền 10, lỗi 10, hồi phục 10) như đợt 2. Lịch dự kiến (chốt ở `lich-3.json`, băm trước khi phát):

1. BINH-THUONG (×1)
2. POOL-EVENT (×1)
3. EVENT-DB-LAT (×1)
4. BINH-THUONG-X3 (×3)
5. CONSUMER-BOOK-SLOW-X3 (×3), đặt cuối để phần tồn queue khi gỡ toxic không lan sang chu kỳ sau.

5 chu kỳ ≈ 2,5 giờ + M1 và đóng gói ca cuối ~15 phút. Trước đó: chạy thử ngắn trên `exp-obs` (pha rút ngắn, 2 chu kỳ: POOL-EVENT, ô H4) ≈ 25 phút; không phải ca RCA.

Thời gian chuẩn bị (ước, chưa kiểm): đo H4 ~10 phút, build + triển khai Event ~25 phút, chạy thử pool ~10 phút, viết bộ tiêm/bộ chạy bản mới ~45 phút. Đợt thu sớm nhất ~08:00Z, xong ~10:45Z, nếu `exp-obs` rảnh.

## 7. Bộ chạy và bộ tiêm bản mới

Không sửa `runner3.py`, `inj2.py`. Tạo:
- `thu3/inj3.py` (bản sao `inj2.py` + ô mới + đầu dò queue/pool), cài ở `exp-app:~/inj3.py`;
- `thu3/runner4.py` (bản sao `runner3.py`): gọi `inj3.py`; bậc tải theo từng chu kỳ trong lịch; sổ `so-thu3.jsonl`, nhật ký `nhat-ky-3.jsonl`, trạng thái `trang-thai-3.json`; pha rút ngắn qua biến môi trường chỉ dùng cho chạy thử. Diff và lý do ghi ở `thu3/runner4-diff.md`.

Chạy: `setsid -f nohup … < /dev/null`, `RCA_DP_OUT=~/rca-dieu-phoi/thu3`, M1 P7 qua `stage-m1.py`/`run-m1.py` ghim, xuất bổ sung `xuat_bo_sung.py` (±300 s).

## 8. Hồ sơ luật 21

| Lỗi ở | Loại | Phạm vi chặn | Xử lý | Chạy lại gì | Mất thêm |
|---|---|---|---|---|---|
| 10% (chu kỳ 1) | tải không khởi động 2 lần | cả lượt | dừng lượt (bộ chạy tự dừng), giữ sổ; kiểm máy tải, phát lại lịch đủ 5 chu kỳ với thư mục ra mới | cả lượt | ~2,5 giờ |
| 10% | hook/toxic không lên (`fault-start-failed`) | chỉ ô đó | bộ chạy ghi `m1-skipped`, chạy tiếp | ô đó, lượt bù sau | 30 phút |
| bất kỳ | can thiệp chạy nhưng đầu dò không xác nhận | chỉ ca đó | hậu kiểm theo `dieu-kien-xac-nhan-3.md`; ca không đạt ra khỏi tập chọn | ô đó nếu sửa được trong quyền | 30 phút |
| bất kỳ | môi trường không về sạch (`run-abort-dirty`) | cả máy | bộ chạy dừng; dọn tay; kiểm queue Booking đã hết tồn | các chu kỳ còn lại | dọn + 30 phút/ô |
| 50% (chu kỳ 3) | M1/stage lỗi một ca | ca đó | bộ chạy stage lại cùng t với mã mới, giữ thư mục cũ | không thu lại | ~3 phút |
| 50% | `exp-obs` khởi động lại / bộ chạy chết | chu kỳ đang chạy | lỗi tự hết (toxic/pause +5 s, lease ≤ 180 s, CPU timeout); phát lại runner với lịch các chu kỳ còn lại, thư mục ra mới | chu kỳ dở + còn lại | ≤ 30 phút + phần còn lại |
| 99% (chu kỳ 5) | bất kỳ | ô cuối | như trên | ô H4 | 30 phút |
| bất kỳ | phát hiện lỗi phương pháp/đóng gói | không chặn thu | dữ liệu thô giữ; đóng gói/M1 lại từ kho (Prometheus 30d, Tempo 14d) | không thu lại | phút/ca |
| bất kỳ | build mới làm hỏng luồng lõi (phát hiện ở kiểm sau triển khai) | trước thu | hoàn tác image Event về `arm64-t062-6b21ed55` (lệnh ở `thay-doi-may.md`) | không thu | ~5 phút |

Thêm quy tắc phân loại hoặc quyết định của Minh không buộc thu lại ca đã xong (dữ liệu thô giữ). Điều kiện suy biến đã biết quét ở chạy thử: hook không chạy ở Event, toxic AMQP làm rớt kết nối, tồn queue chưa hết khi sang chu kỳ sau.

## Bổ sung 1 — 05:25Z: số đo H4 trên bản hiện hành (bản 2, trước khi triển khai lại Event)

- Lệnh: tải `t3do-h4a` (05:10:56–05:18:01Z, ×1 rồi ×3 từ giây 180, exit 0, 1.082 hành trình, 0 hỏng); đầu dò `scripts/do_h4.py` mỗi ~15 s. Số: `do/do-h4a-tom-tat.json` (`scripts/phan_tich_do_h4.py do/do-h4a.jsonl 1794633056.5 180 420`).
- Byte broker→Booking (kết nối chứa consumer `booking.accept-payment.q`): ×1 trung bình 469 B/s (391–522); ×3 trung bình 1.393 B/s (1.302–1.566). Tồn queue Booking (ready + unacked) tối đa 2.
- Theo quy tắc khai trước ở §5 (≥ 1,5 KB/s ở ×3): **chưa đạt**. Ghi đúng kết quả này.
- **Lệch so với §5, có lý do (ghi trước khi thử):** vẫn thử trực tiếp toxic 1 KB/s dưới ×3 một lần, tính là lần thử mới thứ 1 của hướng "tăng lưu lượng" (AGENTS §5a). Lý do: ngưỡng 1,5 lần là biên an toàn tôi tự đặt, không phải điều kiện xác nhận; lưu lượng đo được (≈ 1,39 KB/s) vẫn vượt mức giới hạn 1 KB/s (toxiproxy tính KB = 1.000 byte, chưa kiểm trong mã nguồn toxiproxy), nên về nguyên lý hàng đợi phần dư ≈ 0,39 KB/s sẽ tồn dần. Phép thử trực tiếp rẻ (≈ 9 phút) và phân xử thẳng bằng điều kiện đạt đã khai ở §5 (tồn ≥ 10 cuối pha, ≤ 2 sau gỡ). Nếu không đạt: chuyển sang tải > ×3 hoặc tăng tỷ lệ mua (cần Codex sửa giới hạn `--multiplier ≤ 3` của `tai_linux.py` hoặc kịch bản k6).
- Thử trên **bản mới** (Event đã triển khai lại), vì đợt thu chạy trên bản mới. Thay đổi Event không chạm đường AMQP của Booking.

## Bổ sung 2 — 05:34Z: chọn cường độ POOL-EVENT = 5 (theo quy tắc §4)

Chạy thử 05:23:28–05:34Z trên bản mới (Event `arm64-t063h3-76b34d5e`), tải `t3do-pool` ×1 600 s; kịch bản `scripts/thu_pool.sh` → `do/thu-pool.jsonl`; Prometheus `scripts/pool_prom.py` → `do/thu-pool-prom.json` (bước 15 s; pha bỏ 15 s đầu).

| Pha | used (min–max) | idle | pending (min–max, tb) | 5xx Event /s | p50 server Event (ms, tb) |
|---|---|---|---|---|---|
| nền | 1–1 | 2 | 0 | không có mẫu | 19,4 |
| hold 4 (05:25:33–05:28:03Z) | 4–4 | 1–2 | 0–0 | không có mẫu | 15,0 |
| giữa | 0 | 5 | 0 | — | 11,9 |
| hold 5 (05:29:37–05:32:07Z) | 5–5 | 0 | 2–25, tb 10,1 | 0,18–0,34 | 7.780 (max 10.000) |
| sau | 0 | 5 | 0 | 0 | 9,8 |

- Hook chạy ở Event: audit có 3 dòng `pool.hold.started` (lease đầu và lần gia hạn 120 s). Bản ghi audit ghi trạng thái pool **trước** khi chiếm (active 0), nên không dùng `active` của audit làm đầu dò mức chiếm; dùng Prometheus.
- Mức 4: `used` lên 4 nhưng `pending` = 0 suốt pha, p50 không tăng → theo §4, không đủ tranh chấp ở tải ×1. **Chọn 5** (cạn hẳn).
- Mức 5: tải `t3do-pool` có 182 hành trình hỏng / 709, `dropped_iterations` 11 (cả lượt), exit 0. Ảnh hưởng mạnh lên hành trình, đúng cơ chế cạn pool: DB trực tiếp không bị can thiệp.
- Tính chất của hook (giống POOL-BOOK): mỗi lần gia hạn lease (120 s) hook nhả rồi chiếm lại; trong khe đó request đang chờ có thể lấy được connection.
- `inj3.py` đổi `POOL-EVENT` value 4 → 5 (sha256 mới `695cdc81…`, đã chép lên `exp-app:~/inj3.py`).

## Bổ sung 3 — 05:48Z: ô H4 khả thi theo điều kiện đạt khai ở §5

Chạy thử 05:35:49–05:45Z trên bản mới, tải `t3do-h4b` ×3 suốt 570 s; `scripts/thu_h4.sh` → `do/thu-h4b.jsonl` (đầu dò `inj3.py`), `do/thu-h4b-do.jsonl` (mỗi 10 s), `do/thu-h4b-booking-log.txt`.

- Toxic bandwidth 1 KB/s trên `booking-amqp` 150 s (05:37:58–05:40:27Z). Tồn queue Booking (ready + unacked, các `booking.*.q`): 0 ở nền; tăng dần từ +60 s; **109** ở +142 s (`booking.accept-payment.q` ready 76, unacked 20 = prefetch; `booking.tickets-issued.q` unacked 13). Đầu dò t+140: ready 67, unacked 33.
- Sau khi gỡ: 0 ở +152 s (phần tồn được giao ồ ạt, ~10,7 KB/s trong 10 s), 0 ở +30 s và +90 s.
- Cùng một kết nối AMQP của Booking suốt lượt (`<…4977.0>`, trạng thái `running`); log Booking trong khoảng thử không có dòng heartbeat/ngắt kết nối/khởi động lại consumer (`thu-h4b-booking-log.txt` rỗng). Vậy cơ chế là giới hạn thông lượng giao message tới consumer, không phải rớt kết nối.
- Tải: 2.051 hành trình, 156 hỏng (đều nằm trong khoảng có toxic hoặc ngay sau, chưa tách theo giờ), `dropped_iterations` 1, exit 0, multiplier 3.
- Đạt cả hai điều kiện §5 (≥ 10 cuối pha; ≤ 2 sau gỡ) ở lần thử mới thứ nhất. Lần 1–3 của đợt 2 không đạt vì tải ×1 (≈ 0,47 KB/s) thấp hơn mức giới hạn.
- **Chốt ô H4:** `CONSUMER-BOOK-SLOW-X3` = toxic bandwidth 1 KB/s downstream trên `booking-amqp`, cả pha lỗi 600 s, tải ×3 suốt chu kỳ. Đối chứng cùng bậc tải: `BINH-THUONG-X3`. Hệ quả cần biết khi phân tích: với 600 s, phần tồn dự kiến lớn hơn nhiều (chưa đo); message có thể sang DLQ nếu queue có TTL (chưa kiểm cấu hình TTL); sau gỡ, phần tồn được xử lý dồn trong vài giây ở đầu pha hồi phục.
- Tên ô giữ họ "CONSUMER-BOOK-SLOW" của `o-dev-bo-sung.md` vì cùng chỗ tiêm; cơ chế đúng là "đường giao message tới consumer Booking bị giới hạn thông lượng", không phải khâu xử lý của consumer chậm.

## Bổ sung 4 — 05:56Z: thêm ô tùy chọn RECREATE-PAY (H8-adapter) làm chu kỳ cuối

- Nguồn: `results/T-064/phien-c/YEU-CAU-O.md` (phiên C ghi ~05:50Z, "không phải lệnh"). Phiên B tự quyết theo ba điều kiện của brief 2a:
  1. **Vị trí không trùng ô đánh giá:** T-059 chia theo (vị trí × họ lỗi). Ô đánh giá có payment-service chỉ là cạnh `payment-service→booking-service` (NET-PAY-BOOK) và `payment-service→vnpay` (VNPAY-REFUND-LAT), họ khác. Ô này là (payment-service, tạo lại container) — họ không có trong T-059. Đạt.
  2. **Cách tiêm và xác nhận rõ:** `inj3.py start RECREATE-PAY` chạy `docker compose -p flash-ticket-payment-service -f payment-service.yml up -d --force-recreate --no-deps` trong `/opt/flash-ticket-app/compose-t062` với đúng image đang chạy (cách triển khai đã dùng ở T-062, TD-07); env/compose không đổi. Xác nhận ở `dieu-kien-xac-nhan-3.md`. Đạt.
  3. **Không làm chậm hai ô bắt buộc:** đặt **cuối lịch** (chu kỳ 6); hai ô bắt buộc và ba ô đối chứng chạy trước. Đợt dài thêm 30 phút (ước xong ~10:50Z thay vì ~10:20Z). Đạt.
- Lý do thu: H8-adapter (phiên C) hiện chỉ kiểm được cài đặt trên `thuong01`; cần một ca thật có tạo lại container trong cửa sổ để biết có xếp hạng đúng không.
- Hệ quả: chỉ một ca, một lần thu; ca gần với "triển khai lại" hơn là sự cố; P7 dự kiến báo lỗi adapter ở ca này (bộ chạy ghi `M1 LỖI` và thử stage lại một lần, không đóng gói `.tgz`) — gói ca của ca này phải đóng thủ công sau đợt (safe-export + tar + `xuat_bo_sung.py`), ghi ở bàn giao.
- `lich-3.json` mới (6 chu kỳ) sha256 `c0d4581b…`; `inj3.py` thêm loại `recreate` và đầu dò `payment_container` (sha256 `ba8f1341…`), `xac_nhan_ca_3.py` thêm nhánh RECREATE-PAY (`scripts/va_xac_nhan_recreate.py`).

## Bổ sung 5 — 06:20Z: lịch chốt và hồ sơ luật 21 cho 6 chu kỳ

- Lịch chốt `lich-3.json` (sha256 `c0d4581b…`, đã chép lên `exp-obs:~/rca-dieu-phoi/lich-3.json`): BINH-THUONG, POOL-EVENT, EVENT-DB-LAT, BINH-THUONG-X3 (×3), CONSUMER-BOOK-SLOW-X3 (×3), RECREATE-PAY. 6 × 30 phút = 3 giờ + M1 ca cuối ~10 phút.
- Chạy thử trước đợt: `runner4` một chu kỳ H4 rút ngắn (`thu-ngan/`, đạt: sổ 12 dòng, chuỗi hash đúng, P7 OK hai lần trùng, gói và gói bổ sung có, hậu kiểm xác nhận); RECREATE-PAY đứng riêng không tải (đạt; payment về UP trên Eureka sau ~100 s). Phát hiện khi thử: với pha 360 s, tồn queue H4 lên 616 ở t+330; với 600 s sẽ lớn hơn. Queue Booking là quorum, không TTL, không giới hạn độ dài; dead-letter chỉ khi giao lại quá 20 lần (`rabbitmqctl list_policies`), nên tồn không bị bỏ.
- Đóng băng bản 3: `results/T-063/dong-bang/dong-bang-3.json` (sha256 `1200ffe0…`), mục "Bản 3" ở `dong-bang.md`.

Thêm vào bảng luật 21 (§8):

| Lỗi ở | Loại | Phạm vi chặn | Xử lý | Chạy lại gì | Mất thêm |
|---|---|---|---|---|---|
| 99% (chu kỳ 6, RECREATE-PAY) | P7 ném lỗi adapter (dự kiến, chuỗi trùng khi container tạo lại) | chỉ ca đó | bộ chạy ghi `M1 LỖI`, stage lại một lần với mã mới; không đóng gói `.tgz`. Sau đợt: đóng gói tay từ `/opt/flash-ticket-rca/cases/<mã>` (safe-export + tar) và `xuat_bo_sung.py --t <t>`; P7 lỗi là kết quả đúng của ca này, không phải lỗi thu | không thu lại | ~10 phút |
| 99% | `compose up --force-recreate` lỗi | chỉ ca đó | `fault-start-failed`, `m1-skipped`; kiểm payment còn chạy (container cũ hoặc mới); nếu payment không lên: tạo lại tay theo `thay-doi-may.md` T3-13 | ô đó ở lượt bù | 30 phút |
| 80% (chu kỳ 5, H4) | tồn queue chưa hết khi sang chu kỳ 6 | chu kỳ 6 | điều kiện `ton_hoi60_le_2` của ca H4 bắt được; đầu dò t−240 của chu kỳ 6 ghi tồn; nếu tồn > 2 ở t−240 của chu kỳ 6 thì ghi ở hậu kiểm, ca RECREATE-PAY vẫn giữ (tập chấp nhận khác) | không | 0 |
| bất kỳ | tải ×3 dài 30 phút hết token/seed | chu kỳ ×3 | `tai_linux` cấp pool mới mỗi lần start và kiểm hạn seed theo bậc; lỗi start → bộ chạy thử lại sau 60 s, lần 2 lỗi thì dừng lượt (giữ ca đã thu) | các chu kỳ còn lại | 30 phút/ô |
