# T-073 — Bảng chọn ô nghiệm thu E5 (bản 3: D3 Minh duyệt; phần danh sách và cách bốc khóa ở `khoa-boc-e5.json`)

Bản 3 (giờ máy 20/11 ~22:0xZ): ghi quyết định D3 của Minh, bỏ phương án theo họ, chép phần danh sách và cách bốc vào `khoa-boc-e5.json` để khóa. Bản 2, phiên `rca-w5`, giờ máy 20/11/2026 ~22:1xZ (bản 1 sửa theo Codex CX-07: điều kiện trước E5, cửa sổ mất quan sát khi không có cảnh báo, cách bốc bằng hạt Minh cấp sau khi khóa; phần giữ/loại không đổi). Theo quyết định Minh (LOG T-070 "Lượt 4", mục (e)): xét 17 ô T-069 theo **mô tả thiết kế**, không theo "từng báo được" hay "V082 từng xếp đúng"; khóa danh sách và cách bốc trước khi chạy; lần đầu là kết quả chính; lặp chỉ khi phép thử không thực hiện được do hạ tầng. **Chưa bốc thăm.**

## 1. Nguồn dùng và nguồn không dùng

| Dùng | Để xét gì |
|---|---|
| `results/T-069/bang-theo-o-chinh.json` — chỉ cột `o`, `loai` | danh sách 17 dòng ô và ô có lỗi hay không |
| Repo lab `407b4f5` `campaigns/schedules/lich-t069-chinh.json` | mức tải của từng ô (`multiplier`) |
| Repo lab `faults/injectors/docker/inj3.py` (`CELLS`) | cơ chế can thiệp thật của từng ô |
| `results/T-059/danh-muc-loi.json` (`operation`, `direction`, `intended_mechanism`) | thao tác và hướng lan theo thiết kế |
| `results/T-072/bieu-thuc.json` `T072-bieu-thuc-1` (luật, `tham_so_co_dinh.routes`, `khong_phu`) | tín hiệu luật W4 |
| FlashTicket `infrastructure/api-gateway/.../application.yaml` (chỉ đọc) | đường dẫn nào thuộc route nào |
| Repo lab `load/scenarios/purchase-journey.js` | tải ×1 có gọi thao tác bị can thiệp không |
| Repo lab `observability/collector/agent-docker-host.yaml` (`httpcheck`) | dịch vụ nào có đầu dò liveness |

**Không dùng:** mọi cột kết quả của bảng T-069 (hạng, `cu`/`moi`, `dk_*`, `create_order_201`, `su_kien`, `nhat_ky_m1`), kết quả phát lại luật trên ca cũ, ngưỡng E2 (chưa khóa). Lúc đọc file T-069 có thấy cột `create_order_201` trên màn hình; không dùng nó cho bất kỳ ô nào dưới đây.

## 2. Tín hiệu luật W4 (tóm tắt từ `T072-bieu-thuc-1`)

- `t072-p95-<route>`, `t072-loi-<route>` (5xx) ở **api-gateway**, route `booking` (`/api/v1/events/*/availability`, `/api/v1/orders/**`, …), `event` (`/api/v1/events/**`, …), `payment` (`/api/v1/payments/**`, `/api/v1/orders/*/payment`, …), `ticket` (`/api/v1/tickets/**`, `/api/v1/orders/*/tickets`, …).
- `t072-live`: lần dò liveness mới nhất là lỗi, theo `http_url`; đích dò gồm gateway 8081, các cổng 8082 (Booking), 8083 (Payment), 8084, 8085, 8086 (Event), discovery 8761, Keycloak 8080.
- `t072-mat-do`, `t072-mat-gw`: lớp quan sát, không mở RCA.
- Không phủ (T-072 tự ghi): lỗi không thành 5xx/độ trễ ở gateway, ví dụ hàng đợi RabbitMQ chậm sau khi request đã trả.

Tải ×1 (`purchase-journey`): gọi `GET /events`, `GET /events/{id}` (route event), `GET /events/{id}/availability`, `POST /orders`, `POST /orders/{id}/cancel`, `GET /orders/{id}` (route booking), `POST /payments` (route payment), `GET /orders/{id}/tickets` (route ticket).

"Nằm trong tín hiệu" ở bảng dưới nghĩa là **loại tín hiệu** của luật bao được triệu chứng theo thiết kế ô (đúng route, đúng dạng độ trễ/5xx/liveness). Nó không khẳng định cảnh báo sẽ bật: biên độ so với ngưỡng chưa biết vì ngưỡng E2 chưa khóa. Không bật cảnh báo trong cửa sổ khai là **ca bỏ sót** (kết quả), không phải lý do lặp.

## 3. Bảng 17 dòng

| # | Ô | Có lỗi | Chạy được ở tải E5 (×1) | Triệu chứng theo thiết kế → tín hiệu W4 | Kết luận |
|---|---|---|---|---|---|
| 1 | BINH-THUONG | không | có | — | **loại**: không có lỗi để tiêm |
| 2 | EVENT-DB-LAT | có — Toxiproxy `event-jdbc` trễ 30 ms trên JDBC của Event | có | `GET /events/{id}` đọc DB qua proxy → độ trễ route `event` ở gateway → `p95-event` | **vào thăm** |
| 3 | CPU-BOOK-1 | có — stress CPU 1 worker trong cgroup Booking (quota 1,0) | có | thao tác Booking chậm do tranh CPU → `p95-booking` | **vào thăm** |
| 4 | HTTP5-EVENT | có — hook `http.error` trên `GET /events/{id}` | có | origin trả 5xx qua gateway → `loi-event` | **vào thăm** |
| 5 | BINH-THUONG | không | có | — | **loại**: không có lỗi |
| 6 | REDIS-BOOK | có — Toxiproxy `booking-redis` trễ 200 ms | có | `GET /events/{id}/availability` đọc cache qua proxy → `p95-booking` | **vào thăm** |
| 7 | FLASH-HEALTHY | không | không (thiết kế là lượt flash) | — | **loại**: không có lỗi; không phải tải ×1 |
| 8 | NET-GW-BOOK | có — Toxiproxy `gateway-booking-http` trễ 300 ms | có | mọi request gateway → Booking chậm → `p95-booking` | **vào thăm** |
| 9 | BINH-THUONG | không | có | — | **loại**: không có lỗi |
| 10 | CPU-BOOK-2 | có — stress CPU 2 worker trong cgroup Booking | có | như #3 → `p95-booking` | **vào thăm** |
| 11 | HTTP5-EVENT-FLASH | có — cùng hook như #4 | **không**: thiết kế ô gắn với lượt flash (tải tăng ×3 trong cùng lượt) | `loi-event` | **loại**: không chạy đúng thiết kế ở tải ×1; ở ×1 nó trùng #4 |
| 12 | PAUSE-PAYMENT | có — `docker pause` container Payment | có | đầu dò 8083 không phản hồi → `t072-live`; `POST /payments` treo/hết giờ ở gateway → `p95-payment` hoặc `loi-payment` | **vào thăm** |
| 13 | BINH-THUONG | không | có | — | **loại**: không có lỗi |
| 14 | POOL-EVENT | có — hook `pool.hold` giữ 5 kết nối Hikari của Event | có (lịch T-069 chạy ở ×1) | request Event chờ lấy kết nối → `p95-event` (có thể 5xx khi hết giờ chờ) | **vào thăm** |
| 15 | CONSUMER-BOOK-SLOW-X3 | có — Toxiproxy `booking-amqp` băng thông 1 | **không**: lịch đặt `multiplier: 3` | hàng đợi RabbitMQ chậm sau khi request đã trả: **ngoài** tín hiệu W4 (T-072 `khong_phu`) | **loại**: tải ×3 và ngoài tín hiệu luật |
| 16 | BINH-THUONG-X3 | không | không (×3) | — | **loại**: không có lỗi; tải ×3 |
| 17 | RECREATE-PAY | có — tạo lại container Payment (`--force-recreate`) | có | trong lúc Payment khởi động lại: đầu dò 8083 lỗi → `t072-live` (`for` 20 s); `POST /payments` lỗi ở gateway → `loi-payment` | **vào thăm**, kèm ghi chú: gián đoạn chỉ kéo dài bằng thời gian khởi động lại, không duy trì 600 s như các ô khác |

**Tập vào thăm (9 ô):** CPU-BOOK-1, CPU-BOOK-2, EVENT-DB-LAT, HTTP5-EVENT, NET-GW-BOOK, PAUSE-PAYMENT, POOL-EVENT, RECREATE-PAY, REDIS-BOOK.

Không ô nào sửa dữ liệu DB (I13).

### Điều kiện phải kiểm ngay trước E5 (khung S4, trước khi tiêm; chỉ đọc trừ khi ghi khác)

Bảng chọn ô ở trên dựa trên thiết kế, không khẳng định môi trường lúc E5 sẵn sàng. Trước khi tiêm, người làm khung S4 kiểm và ghi vào `results/T-073/e5/` từng mục; mục nào không đạt là **lỗi hạ tầng trước tiêm**: sửa trong quyền của khung hoặc trình Minh, không bốc lại ô.

| # | Điều kiện | Ô cần | Cách kiểm |
|---|---|---|---|
| K1 | exp-app chạy đúng bản ghim (`rca/exp-2026-11`, image `arm64-t067-36a3725d`) | tất cả | `docker ps --format '{{.Names}} {{.Image}}'`, đối chiếu digest ghi ở T-067 |
| K2 | Event và Booking chạy biến thể `-P rca-test` (hook nhận lệnh) | HTTP5-EVENT, POOL-EVENT | `inj3.py ensure` thành công; đọc trạng thái hook không có lease còn hiệu lực |
| K3 | Toxiproxy có proxy của ô, đang bật, **không có toxic** còn sót | EVENT-DB-LAT (`event-jdbc`), REDIS-BOOK (`booking-redis`), NET-GW-BOOK (`gateway-booking-http`) | API Toxiproxy `GET /proxies`; `inj3.py verify` báo sạch |
| K4 | cgroup Booking tìm được, quota CPU 1,0 còn bật | CPU-BOOK-1, CPU-BOOK-2 | `inj3.py` tìm cgroup Booking; đọc `cpu.max` |
| K5 | container và project Compose Payment đúng tên mà `inj3.py` dùng; Payment đang chạy, không bị pause | PAUSE-PAYMENT, RECREATE-PAY | `docker inspect` trạng thái, nhãn project |
| K6 | tín hiệu luật có dữ liệu: route của ô có lưu lượng ở gateway trong 10 phút trước; đầu dò liveness của cổng liên quan (8083 Payment) có lần dò mới | tất cả | truy vấn nhẹ một khúc ≤ 10 phút |
| K7 | tải ×1 chạy được: sự kiện tải còn hạn bán, sức chứa vé đủ cho lượt E5 (C3 của T-070) | tất cả | kiểm chỉ đọc như E1 |
| K8 | luật W4 chính thức đã nạp và được đánh giá; contact point trỏ `http://t073-webhook:8080/t073/canh-bao`; bộ nhận `healthy`; bộ điều phối T-073 đang chạy và đọc spool | tất cả | Grafana (khung S4), `docker compose ps`, nhật ký bộ điều phối |
| K9 | kho quan sát sống: Prometheus, Collector, Loki, Tempo, Grafana Up; không file STOP; đồng hồ hai máy lệch NTP < 1 s | tất cả | `docker ps`, `chronyc tracking` |
| K10 | môi trường sạch trước chu kỳ (không còn can thiệp từ lần trước) | tất cả | `inj3.py verify` |

### Quyết định của Minh (D3, chat 20/11/2026 ~22:03Z, "Duyệt cả năm"; LOG T-070 lượt 6)

1. **Trọng số:** mỗi ô một phiếu, 9 ô (họ CPU có hai phiếu; nói rõ khi báo phạm vi demo).
2. **RECREATE-PAY:** giữ, với điều kiện sửa CX-06 điểm 5 (P7 lỗi "nhiều chuỗi runtime" thì V082 vẫn chạy) **đã kiểm đạt trên gói cũ trước S4**.
3. **Biên độ:** không lọc theo biên độ.
4. **Bốc:** khóa danh sách, trọng số và thứ tự trước; sau đó Minh cấp hạt.

## 4. Cách bốc thăm (khai trước, chưa chạy)

Bản 1 lấy hạt từ hash của chính bản thảo; bỏ cách đó (Codex CX-07: người làm có thể đổi một khoảng trắng, tính thử và giữ bản cho ra ô mong muốn — hash chỉ bảo vệ sau khi khóa). Cách thay:

1. **Khóa trước:** tập ô, trọng số (mỗi ô một phiếu) và thứ tự cố định dưới đây được chép nguyên vào `results/T-073/khoa-boc-e5.json`; sha256 của file khóa đó ghi vào LOG T-073. Từ lúc này không sửa file khóa.
2. **Sau khi khóa, Minh cấp một hạt độc lập**: một chuỗi bất kỳ Minh tự chọn, gửi trong chat, sau khi đã thấy sha256 khóa. Người làm và các agent không đề xuất hạt.
3. Người làm chạy đúng một lần đoạn mã dưới với hạt đó; ghi vào LOG **nguyên văn hạt**, sha256 file khóa, ô bốc được, giờ bốc, đầu ra lệnh. Bốc **một** lần; không bốc lại vì không thích ô.

Thứ tự cố định (theo ô, trọng số đều — D3 Minh duyệt):

| Thứ tự | Ô |
|---|---|
| 0 | CPU-BOOK-1 |
| 1 | CPU-BOOK-2 |
| 2 | EVENT-DB-LAT |
| 3 | HTTP5-EVENT |
| 4 | NET-GW-BOOK |
| 5 | PAUSE-PAYMENT |
| 6 | POOL-EVENT |
| 7 | RECREATE-PAY |
| 8 | REDIS-BOOK |

```python
import hashlib, random
THU_TU = ["CPU-BOOK-1", "CPU-BOOK-2", "EVENT-DB-LAT", "HTTP5-EVENT", "NET-GW-BOOK",
          "PAUSE-PAYMENT", "POOL-EVENT", "RECREATE-PAY", "REDIS-BOOK"]   # đúng bảng thứ tự đã khóa
hat_minh = "<chuỗi Minh cấp, nguyên văn>"
r = random.Random(int(hashlib.sha256(hat_minh.encode("utf-8")).hexdigest(), 16))
print(THU_TU[r.randrange(len(THU_TU))])
```

## 5. Quy tắc lặp (chỉ khi lỗi hạ tầng)

- **Lần đầu là kết quả chính**, kể cả khi trượt (không cảnh báo, RCA sai, quá N phút).
- Được chạy lại **cùng ô** (không bốc lại) khi và chỉ khi phép thử không thực hiện được do hạ tầng, có bằng chứng ghi lại:
  1. tải k6 không khởi động hoặc dừng giữa chừng;
  2. `inj3.py start` lỗi, hoặc kiểm sạch (`inj3 verify`) không đạt trước chu kỳ;
  3. mất quan sát: Prometheus, Collector hoặc Grafana khởi động lại hay ngừng trong `[mốc tiêm − 600, t̂ + 600)`; khi **không có cảnh báo** (không có t̂), cửa sổ xét là cửa sổ phát hiện đã khai `[mốc tiêm, mốc tiêm + 600 s)` (`khai-truoc-e5.json`). Mất quan sát ngoài cửa sổ này không là lý do lặp;
  4. dịch vụ T-073 dừng vì lỗi hạ tầng (sudo, đĩa, mạng tới exp-app) trước khi có kết quả.
- **Không** phải lý do lặp: không có cảnh báo trong cửa sổ khai (ghi **bỏ sót**); cảnh báo đến muộn; RCA trả kết quả sai hoặc lỗi phương pháp; kết quả hiện quá N phút.
- Tối đa 3 chu kỳ (SPEC T-073). Lần lặp ghi riêng, giữ mọi lần (luật cứng 10). Ô không tiêm được sau 2 lần vì hạ tầng của chính ô đó (ví dụ proxy thiếu): dừng, trình Minh; không tự bốc ô khác.
