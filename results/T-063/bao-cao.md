# T-063 — Báo cáo: bổ sung quan sát và đợt thu dữ liệu phát triển bản 2

Ghi 13/11/2026 19:38Z (14/11 giờ VN), Claude, phiên 2 của người làm. Báo cáo dựng từ file kết quả; chỗ nào lấy lại từ LOG phiên 1 mà chưa kiểm lại thì ghi rõ. Task là cài đặt, mô tả và phân xử ba câu hỏi cơ chế. Task **không** đánh giá phương pháp; việc chọn M1 thuộc T-064.

## 1. Đầu ra chính

| Đầu ra | Ở đâu | Trạng thái |
|---|---|---|
| Đợt thu chính, 13 chu kỳ | `results/T-063/thu2/` (1,3 GB) | Xong 13/11 07:13–14:01Z. `sha256sum -c thu2/SHA256SUMS`: 214/214 khớp (chạy lại 19:37Z) |
| Gói ca + đầu ra P7 | `thu2/ca/<mã>.tgz` (13 gói), `thu2/ca/<mã>/prometheus-bo-sung.json` | P7 trạng thái OK ở 13/13 ca, hai lần chạy trùng (`thu2/chay/nhat-ky-2.jsonl`, trường `deterministic`; theo LOG phiên 1) |
| Sổ tiêm lỗi, nhật ký | `thu2/tiem-loi/so-thu2.jsonl` (127 dòng, có `prev_sha256`), `thu2/chay/nhat-ky-2.jsonl` (40 dòng) | Chuỗi hash của sổ: phiên 1 báo đúng; phiên 2 chưa chạy lại phép kiểm chuỗi |
| Hậu kiểm can thiệp | `chay/xac-nhan-ca.json` (điều kiện khai trước, `chay/dieu-kien-xac-nhan.md`), `chay/xac-nhan-ca-2.json` ("Sửa sau 1") | 12/13 theo điều kiện khai trước; 13/13 sau sửa. Xem mục 4 |
| Đóng băng | `dong-bang.md`, `dong-bang/dong-bang-2.json` | Bản 2 ghi 07:13Z, trước khi phát |
| Hồ sơ luật 21 | `chay/HO-SO-LUOT.md`; phản biện trước lượt `tasks/T-063-quan-sat-thu-dev-2/REVIEW.md` | R1, R2 (chặn) đã sửa và kiểm (`chay/kiem-sua-R1/`, `kiem-tich-hop/BAO-CAO.md`) |
| Thay đổi máy | `quan-sat/thay-doi-may.md` (TD-01…TD-09) | Có lệnh, giờ, cách hoàn tác |
| Phân tích cơ chế | `span-goc/PHAN-TICH.md`, `cpu-book/PHAN-TICH.md`, `ca-nen/PHAN-TICH.md`, `h5/PHAN-TICH.md` | Xem mục 3 |
| B16 bản 2 | `b16-ban-2.md` | Tài liệu đề xuất, chưa qua phản biện |
| Điều phối | `dieu-phoi/` (`goi_codex.py`, thử mô phỏng và thử thật) | Gọi lại sau hết hạn mức: đã có một lần chờ thật rồi bị thay bằng lượt khác (checkpoint 13/11 02:32Z); chưa có lần "hết hạn → chờ → tự gọi lại" chạy trọn trên Codex thật |

## 2. Tín hiệu cho từng hướng H1–H8

Bảng gốc: `quan-sat/bang-huong-tin-hieu.md` (bản 12/11). Cột "trong gói" dưới đây đếm lại trên 13 gói bổ sung của đợt thu (`thu2/ca/*/prometheus-bo-sung.json`, 24 kênh).

| Hướng | Tín hiệu trong gói ca | Ô dev phân xử trong đợt thu | Thiếu gì |
|---|---|---|---|
| H1 cạnh DB/cache/broker | span CLIENT có `db.system`; span PRODUCER/CONSUMER RabbitMQ (R-04 đạt, `kiem-r/BAO-CAO.md`) | EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK | Không có ô lỗi ở cạnh message |
| H2 JVM/cgroup | `gc`, `heap`, `jvm-cpu`, `throttle`, `throttle-ratio`: 13/13 ca có chuỗi. `threads-blocked`: **0/13 ca có chuỗi** | CPU-BOOK-1, CPU-BOOK-2 | `threads-blocked` vắng đồng loạt vì kho không có chuỗi trạng thái này: truy vấn `count(jvm_thread_count) by (jvm_thread_state)` trên Prometheus `exp-obs` lúc 19:38Z chỉ trả `runnable`, `timed_waiting`, `waiting`. Kênh này vì thế không mang thông tin trong đợt thu |
| H3 pool | `pool-pending`, `pool-used`, `pool-wait`: 13/13 ca, 4 chuỗi mỗi ca | **Không có** | POOL-EVENT không thử được: hook `pool.hold` chỉ chạy ở Booking (`chay/D2B-KET-QUA.md`). Sửa cần đổi mã hook thử trong repo FlashTicket rồi build lại |
| H4 queue | `queue-ready`, `queue-unacked`, `queue-consumers`: 13/13 ca, 30 chuỗi mỗi ca | **Không có** | CONSUMER-BOOK-SLOW không xác nhận được sau 3 cách tiêm; lưu lượng message của tải (~0,5 msg/s) quá thấp để tồn queue |
| H5 chết im | `live-down`, `live-ms` (httpcheck 8 đích): 13/13 ca | PAUSE-PAYMENT | Chỉ một ô |
| H6 thao tác nền | trace, `thread.name`, span bọc job Keycloak (TD-08) | 4 ca BINH-THUONG | — |
| H7 tải tăng | `route-rate`, `route-5xx`; tải ×3 có xác nhận (`ty_le_tai_sau_truoc` = 3,0) | FLASH-HEALTHY, HTTP5-EVENT-FLASH | SLOW-BOOK-FLASH không thu (WHY-83) |
| H8 | không cần tín hiệu mới; log nghiệp vụ có trong `raw-logs.jsonl` | — | Chưa có ca container bị tạo lại trong cửa sổ để thử adapter |

**Hệ quả cho T-064.** H3 và H4 có tín hiệu nhưng không có ô lỗi tương ứng. Kết quả "không tác dụng" của hai hướng này trên dev bản 2 chỉ nói chúng không gây hại ở các ô đã thu, không nói chúng vô ích.

## 3. Ba câu hỏi cơ chế của SPEC

| Câu hỏi | Kết luận | Mức căn cứ | Nguồn |
|---|---|---|---|
| Span gốc nào hợp lệ, span nào mất ngữ cảnh? | Trên 9 ca T-062: gốc không phải điểm vào hay job Spring là tác vụ nền xác định được theo `thread.name` (job nội bộ Keycloak, Hikari, Eureka, JGroups, health indicator). Mồ côi ở Booking do bộ lọc health bỏ span cha | Đã phân loại lại trên 13 ca mới bằng cùng script (`span-goc/phan_loai_dev2.py` → `phan-loai-dev2.json`, 19:43Z). Trung bình mỗi ca, 9 ca cũ → 13 ca mới: gốc INTERNAL không nhận ra 3.438 → 13 (job Keycloak nay có span bọc, TD-08: Keycloak có 611 gốc job mỗi ca); mồ côi 10,2 → 1,0; gốc CONSUMER 0 → 0; gốc CLIENT có `db.system` 440 → 434 (không đổi; nhóm tác vụ nền của thư viện). Gốc CLIENT khác tăng 360 → 634, **chưa lần nguyên nhân** | `span-goc/PHAN-TICH.md`, `span-goc/phan-loai-dev2.json`, `kiem-r/BAO-CAO.md` |
| CPU-BOOK lan do tranh CPU hay do phụ thuộc? | Tranh CPU máy (máy 2 lõi): cùng mức CPU Booking, 2 luồng đốt làm PSI máy ×6 và p99 đường không qua Booking 22 → 69 ms; 1 luồng thì không | Phép thử có đối chứng trên `exp-app`. Chưa đo lịch CPU theo ms | `cpu-book/PHAN-TICH.md` |
| Ca bình thường bị cờ do đầu dò hay ngẫu nhiên? | Giả thuyết đầu dò không được ủng hộ: vượt ngưỡng không dồn quanh t+63. Thay đổi có cấu trúc, dưới 0,2 ms | Cơ chế từng đợt **chưa phân xử**. Trên dev bản 2, phép đếm của T-064 **chưa phân biệt được** ca bị cờ với ca không bị cờ theo autovacuum và checkpoint; chưa đủ căn cứ quy nguyên nhân cho hai ứng viên này, cũng chưa đủ để loại chúng (sửa theo REVIEW-2 R6; bản trước ghi "đã loại"). Khóa hàng: không có dòng chờ khóa | `ca-nen/PHAN-TICH.md`, `results/T-064/phan-tich/ghi-chu-co-che-dev2.md` Q4 |

## 4. Điểm lệch so với kế hoạch và điều phải biết khi dùng dữ liệu

1. **PAUSE-PAYMENT trượt điều kiện khai trước.** Điều kiện chép sai chuỗi trạng thái Docker (`running true` thay vì `paused true`). Payment có bị pause (httpcheck lỗi suốt pha; T-064 đọc được 20 mẫu `live-down` liên tiếp từ t+15 s). "Sửa sau 1" là sửa điều kiện sau khi xem dữ liệu. T-064 báo riêng tập 12 ca (khai trước) và 13 ca (sau sửa). **Chờ Minh** chọn tập nào là tập chính.
2. **Hai ô dev không vào đợt thu:** POOL-EVENT, CONSUMER-BOOK-SLOW (mục 2). REDIS-BOOK có trong đợt thu này (ở T-062 bị bỏ).
3. **Mỗi ô một lần thu.** Chưa đo dao động giữa các lần.
4. **FLASH-HEALTHY có độ trễ tăng thật** dưới tải ×3 (Q4 của T-064). Coi ca này là "không lỗi" hay báo riêng là câu hỏi định nghĩa, chờ Minh.
5. **Điểm mù theo dõi trong lúc thu:** phép kiểm "bộ chạy còn sống" dùng `pgrep -f` tự khớp chính nó. Không gây hậu quả ở lượt này vì bộ chạy không chết; đã sửa.
6. **Mất mạng laptop 13/11 ~04:19–05:00Z** xảy ra trước đợt thu; bộ chạy sau đó chuyển lên `exp-obs` (DECISIONS 13/11). Đây là sự cố hạ tầng, không ảnh hưởng dữ liệu đợt thu.

## 5. Đối chiếu "Tiêu chí xong" của SPEC

| Tiêu chí | Đạt? |
|---|---|
| Mỗi hướng H1–H8 có tín hiệu trong gói, hoặc ghi rõ thiếu gì | Đạt về tín hiệu. H3, H4 thiếu ô phân xử; `threads-blocked` không có chuỗi trên kho |
| Đợt thu xong, băm, có đầu ra P7 từng ca | Đạt |
| Ba câu hỏi cơ chế có kết luận hoặc "chưa phân xử" kèm bằng chứng thiếu | Đạt một phần: ca nền chưa phân xử; nhóm gốc CLIENT khác tăng trên tải mới chưa lần |
| Đầu ra còn thiếu so với SPEC | `manifest.json` của `results/T-063/` (hiện mới có `thu2/SHA256SUMS`); `o-dev-bo-sung.json`; `o-dev-bo-sung.md` còn ghi "nháp 1", trạng thái thật nằm ở `chay/D2B-KET-QUA.md` |

## 6. Việc còn lại và đề xuất

- Lần nhóm gốc CLIENT không phải DB tăng trên tải mua vé (đọc `chi_tiet` trong `span-goc/phan-loai-dev2.json`).
- Lập `manifest.json`; cập nhật trạng thái ô dev vào một file.
- **Ô cho H4 (trong quyền, chưa làm).** CONSUMER-BOOK-SLOW cần tải có lưu lượng message cao hơn mức ~0,5 msg/s hiện tại; kịch bản k6 mới trên máy tải thuộc quyền của chiến dịch (`CHIEN-DICH-M1-FT.md` mục 6). Ca mới thu trên cùng bản đóng băng thì so được với 13 ca hiện có. Chưa ước lượng được chi phí trước khi thử một bậc tải.
- **Ô cho H3 (cần Minh cho phép).** POOL-EVENT cần sửa mã hook thử `services/event-service/src/rca-test/.../RcaFaults.java` (điều kiện `poll()` chỉ cho `pool.hold` chạy ở Booking). Đường dẫn này không nằm trong danh sách được sửa của chiến dịch; phiên 1 đã dừng ở đây (`chay/D2B-KET-QUA.md`). Đề xuất của Claude: cho sửa đúng điều kiện đó trên nhánh `rca/quan-sat-log`, build lại image Event, thu POOL-EVENT kèm một ca BINH-THUONG và một ô cũ trên bản mới để so. Mặt trái: bản mới khác bản đã đóng băng, ca mới không gộp thẳng vào 13 ca hiện có. Phương án khác: chấp nhận H3 "chưa thử được trên ô lỗi".
- Cho tới khi có ô, hồ sơ chọn của T-064 ghi H3/H4 là "chưa thử được trên ô lỗi", không ghi là "bỏ".

## 7. Bổ sung sau phản biện lượt 2 (13/11 19:58Z)

Sửa theo `tasks/T-063-quan-sat-thu-dev-2/REVIEW-2.md` R5, R6. Các mục trên giữ nguyên trừ câu về autovacuum/checkpoint ở mục 3.

**Span thiếu cha trên 13 ca mới** (`span-goc/phan-loai-dev2.json`, khóa `<mã>/theo_service_nhom/*|mo_coi`): tổng 13 span, ở 3 ca. Mười ca còn lại không có.

| Nhóm | Số span | Quan sát | Trạng thái |
|---|---|---|---|
| Event, ca 5fb8208f và f20b0ca5 | 1 + 1 | JDBC trên luồng `HikariPool-1:connection-adder`. Người phản biện truy Tempo: span cha có thật nhưng kết thúc trước t khoảng 1.483 s và 2.871 s, ngoài cửa sổ đóng gói ±600 s (REVIEW-2 phụ lục A; người làm chưa truy lại) | Không phải mất bản ghi trong cửa sổ. Ứng viên chưa kiểm: luồng nền của pool giữ ngữ cảnh trace cũ. Đây là thao tác nền của thư viện, cùng loại với nhóm gốc CLIENT có `db.system` |
| Payment, ca 46aab4be (PAUSE-PAYMENT) | 11 | Người phản biện truy Tempo: hai span cha có trên kho, kết thúc khoảng t − 2,4 s, tức **trong** cửa sổ đóng gói, nhưng gói không có (người làm chưa truy lại) | **Chưa xác định bước làm thiếu.** Hai giải thích còn lại: span cha đến kho sau lúc đóng gói (Payment bị pause ngay sau đó, bộ xuất của nó có thể chưa đẩy lô cuối); hoặc đường xuất/đóng gói bỏ bản ghi. Phân xử cần file capture của lượt đó (`traces-2026-11-13T13-14-02…`, người phản biện báo không còn trên máy) hoặc log bộ xuất quanh lúc pause. Nếu không còn thì không phân xử được bằng dữ liệu đã lưu |

Hệ quả: 11 span mồ côi nằm đúng ở ca PAUSE-PAYMENT, ca duy nhất của H5. Chưa đo ảnh hưởng của chúng tới điểm M1 ở ca này; không coi chúng là nguyên nhân hạng của Payment.

**Gốc CLIENT không phải DB** (tổng 8.245 trên 13 ca; `chi_tiet` có `nhom = client_goc_khac`):

| Thành phần, tên span | Số | Nhận định |
|---|---|---|
| Booking `basic.ack` | 3.595 (≈ 276 mỗi ca) | Thao tác điều khiển AMQP của luồng listener, đã thấy ở pilot tải mua vé (`kiem-r/BAO-CAO.md`). Chỉ có khi có message, nên tải đọc cũ không có. Phần này gần bằng mức tăng 360 → 634 mỗi ca |
| discovery-server `POST` | 1.550 | Có sẵn ở tải cũ theo cùng cỡ (120 mỗi ca) |
| `PUT`/`GET` của các service, 260 mỗi loại | còn lại | Chưa đối chiếu từng tên; số bằng nhau giữa các service gợi ý lời gọi định kỳ tới Eureka (chưa kiểm) |

Vậy phần tăng chủ yếu là `basic.ack`, không phải mất ngữ cảnh mới. Nhóm `PUT`/`GET` chưa kiểm đích gọi.

Bổ sung 13/11 22:42Z: người phản biện (REVIEW-3, mục "Bằng chứng span bổ sung") đọc `url.full` và `server.address` của nhóm này trong `raw-traces.jsonl` và báo 3.100 span `PUT`/`GET` đều tới `http://127.0.0.1:8761/eureka/`. Người làm chưa tự đếm lại; nếu đúng thì đây là lời gọi định kỳ tới Eureka, không phải mất ngữ cảnh.

**Khóa hàng.** `quan-sat/thay-doi-may.md` TD-06 ghi đã bật `log_lock_waits=on`. Người làm chưa đọc lại cấu hình đang chạy. Kể cả khi bật, Postgres chỉ ghi lần chờ dài hơn `deadlock_timeout` (mặc định 1 s; chưa đọc giá trị thực), nên vắng dòng chờ khóa không loại được chờ khóa ngắn cỡ ms.

## Thu bù 3 — 14/11/2026 (phiên B, Claude; ghi ~10:55Z)

Các mục trên giữ nguyên, kể cả câu "H3, H4 không có ô lỗi" (đúng với đợt thu 2). Mục này ghi phần thu bù trên **bản 3**. Hồ sơ đầy đủ: `thu3/KE-HOACH.md` (bổ sung 1–5), `thu3/BAN-GIAO-B.md`, `thu3/thay-doi-may.md`.

**Bản 3 khác bản 2 ở đúng một thứ về ứng dụng:** image Event build từ `6b21ed55` + bản vá hook H3 (nhánh `rca/quan-sat-log` commit `e557307`; `dong-bang.md` mục "Bản 3"). Vì vậy 6 ca mới không gộp thẳng vào 13 ca bản 2.

| Ô | Hướng | Bậc tải | Hậu kiểm (khai trước) | Sau "Sửa sau" (chờ Minh) | Số đo đầu dò chính (`thu3/xac-nhan-ca-3*.json`) |
|---|---|---|---|---|---|
| BINH-THUONG | đối chứng bản 3 | ×1 | xác nhận | xác nhận | không can thiệp; 0/2.161 hành trình hỏng |
| POOL-EVENT | H3 | ×1 | xác nhận | xác nhận | `used` tb N 0,03 → L 5,0 → sau 0; `pending` max L 22; 740/2.149 hành trình hỏng |
| EVENT-DB-LAT | đối chứng ô cũ | ×1 | xác nhận | xác nhận | PG qua proxy 35,2 / 32,9 ms (bản 2: 34,4 / 32,6); 0 hỏng |
| BINH-THUONG-X3 | đối chứng H4 | ×3 | **không** (`C0`, lỗi cài script) | xác nhận (Sửa sau 1) | không can thiệp; 0/6.481 hỏng; tồn queue Booking 0 ở mọi đầu dò |
| CONSUMER-BOOK-SLOW-X3 | H4 | ×3 | xác nhận | xác nhận | tồn queue Booking t+60 / t+330 / hoi+60 = 4 / 654 / 0; cùng kết nối AMQP; 1.205/6.468 hỏng |
| RECREATE-PAY | H8-adapter (yêu cầu phiên C) | ×1 | **không** (httpcheck, lỗi đặt điều kiện) | xác nhận (Sửa sau 2) | Id payment đổi đúng một lần, StartedAt t + 5 s; mẫu thô lỗi liveness chỉ ở t+3…t+43; 19 hỏng |

- **Hai "Sửa sau"** (`thu3/dieu-kien-xac-nhan-3.md` mục "Sửa sau"): (1) script hậu kiểm quên BINH-THUONG-X3 trong bộ ô không lỗi của C0 — điều kiện đã khai không đổi; (2) điều kiện "phục hồi" của RECREATE-PAY dùng `query_range`, bị lookback 5 phút của chuỗi đẩy giữ giá trị cũ — sửa sang mẫu thô. Giữ cả hai kết quả. **Chờ Minh** nhận hay thu lại.
- **P7:** 5/5 ca có đầu ra chạy OK hai lần, đầu ra trùng SHA (`/opt/flash-ticket-rca/outputs/<mã>/summary.json`, `method-output-1/2.json`). Ca RECREATE-PAY: P7 ném `Multiple runtime series map to one logical metric…` ở cả hai lần stage (đúng tình huống H8-adapter cần), không có đầu ra P7; dữ liệu thô ở `exp-obs:/opt/flash-ticket-rca/cases/ebd5ef38`.
- **Bộ chặn rò mã ca kích hoạt một lần:** ca H4 lần đầu stage với mã `659a9dfb` bị chặn (`Case/ledger identifier leaked into method input values`). Lần theo: chuỗi `659a9dfb` nằm trong spanId `c9b4b659a9dfb45d` của một span `EVALSHA` trong `raw-traces.jsonl` — trùng ngẫu nhiên giữa mã mờ 8 ký tự hex và ID span, không phải nhãn lọt. Bộ chạy stage lại với mã `659a9dfb1ab0` theo thiết kế, P7 OK. Gói ca của ô này mang mã `659a9dfb1ab0`.
- **So với bản 2 (cùng ô):** BINH-THUONG và EVENT-DB-LAT trên bản 3 cho số đầu dò và tải cùng cỡ bản 2 (`thu3/so-sanh-o-cu.json`). PSI CPU toàn máy (`some avg60`) ở bản 3 là 15,3–16,5% (6 đầu dò của 2 ca), bản 2 là 11,8–15,6% (15 đầu dò của 5 ca); chưa phân xử là do watchdog hook mới ở Event, do giờ chạy, hay ngẫu nhiên (một ca mỗi ô). Không dùng điểm M1 trong phép so này.
- **Hệ quả cho T-064:** H3 có một ô lỗi (POOL-EVENT, cạn hẳn pool). H4 có một ô lỗi (CONSUMER-BOOK-SLOW-X3) kèm đối chứng cùng bậc tải. Cơ chế ô H4 là giới hạn thông lượng giao message tới consumer Booking, không phải khâu xử lý consumer chậm. Mỗi ô một lần thu.
- **Chưa làm / giới hạn:** chưa đóng gói `.tgz` cho ca RECREATE-PAY (giữ trên `exp-obs`, có hash); `manifest.json` của `results/T-063/` vẫn thiếu (chỉ có `thu3/thu/SHA256SUMS`); chưa đo dao động giữa các lần thu.
