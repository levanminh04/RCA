# T-074 — Thiết kế W6: khóa bản và thiết kế đánh giá FlashTicket (bản nháp 1)

- **Người soạn:** Claude, phiên `danh-gia-w6`, 20/11/2026. Người phản biện: Codex (chưa phản biện).
- **Trạng thái toàn hồ sơ:** đề xuất. **Chưa có mục nào được Minh duyệt.** Không dùng máy, không SSH; mọi "đã kiểm" dưới đây là đọc file hoặc code.
- **Đọc cùng:** `de-xuat-why.md` (các mục WHY đề xuất), `du-toan.json` (giờ máy, sức chứa, lỗi 10/50/99%), `cau-hoi-minh.md` (câu hỏi gom một lần).
- **Theo mục** của `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` §8.3 W6.

Ký hiệu trạng thái mỗi lựa chọn:

| Mã | Nghĩa |
|---|---|
| ĐX | đề xuất của người làm, chờ Minh duyệt |
| CHỜ-MINH | cần Minh chọn giữa các phương án (câu hỏi ở `cau-hoi-minh.md`) |
| CHỜ-W4 | phụ thuộc kết quả T-071/T-072 (độ trôi DB E2→E4, luật, quy tắc gom) |
| CHỜ-W5 | phụ thuộc kết quả T-073 (độ trễ chế độ (b), bộ xuất theo t̂) |
| ĐÃ-KIỂM | đã đọc file/code và đối chiếu; ghi nguồn |
| CHƯA-KIỂM | giả định chưa kiểm; ghi trường hợp sai và kết luận phụ thuộc (luật 5) |

---

## 0. Câu hỏi nguồn và phần hồ sơ này bao phủ (luật 13)

| Nguồn | Yêu cầu | W6/W7 bao phủ | Phần thiếu / phụ thuộc |
|---|---|---|---|
| DT18-NV3 | "Đánh giá bằng các độ đo phù hợp cho bài toán phát hiện và chẩn đoán… phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế", áp dụng trên hệ bán vé | Độ đo phát hiện, xếp hạng, vùng (§9); báo theo ô và theo ca; phân tích cơ chế ca sai (§10) | Vùng ảnh hưởng chỉ đo được khi có nhãn endpoint độc lập (§9.3) |
| DT18-NV2 | Xếp hạng nguyên nhân gốc, xác định vùng ảnh hưởng, phát hiện bất thường trên đồ thị | Ba bảng xếp hạng; vùng nghi ngờ | V082 không có đầu ra cạnh → bảng cạnh `UNSUPPORTED` |
| Cô, bước 4 | So với RCA cơ sở; Precision, Recall, F1, MRR, NDCG | SimpleRCA, BARO (§7); P/R/F1 phát hiện; MRR, NDCG@5 | Baseline đa nguồn/trace (MicroRank, TraceRCA, Nezha) không có trong §8.3 → OPEN, câu hỏi Q-W6-07 |
| MRP RQ5 | Kết quả có giữ trên hệ khác, lỗi tự tiêm, tải thay đổi | Ô đánh giá mới (vị trí chưa thấy khi phát triển), hai mức tải, hai chế độ | Số ô chạy được trên bản ghim ít (§4) → kết luận RQ5 hẹp |
| MRP RQ3a/b/c trên FlashTicket | Phát hiện, xếp hạng, vùng | Có (§9) | Phát hiện dùng luật Grafana (mức hệ thống); đồ thị không tham gia quyết định báo động (M-20 hoãn) |
| MRP RQ3d / QT8 | Lợi do dùng quan hệ: hơn nhánh bỏ quan hệ và hơn quy tắc đơn giản trên cùng đồ thị | Đề xuất chạy kèm `DC-bo-quan-he` và C-d1/C-d2/C-d3 (chỉ tính toán, §3.4) | Chỉ khi Minh duyệt; không có đối chứng đồ thị ngẫu nhiên (M-25) |
| B1.9 / D14 (Q-201) | Ba bản bắt buộc, che cả dẫn xuất, nhánh dự phòng khai trước, cả hai chế độ, RQ5 hai câu | §3 | Danh sách nhóm che cần kiểm kê code ở gói sau (§3.3) |
| T-059 / M7 | Chia theo ô; báo ba câu hỏi riêng | §4, §5 | Phần lớn ô đánh giá chưa có cách tiêm trên bản ghim (§4) |
| MRP §6.1 | Kết quả đầu của bản khóa giữ và báo nguyên | §8, §12 | — |

**Kết luận phạm vi:** hồ sơ này là thiết kế. Nó không trả lời RQ5 hay RQ3 trên FlashTicket. Nó định ra phép thử nào sẽ trả lời phần nào, và chỉ ra chỗ phép thử sẽ yếu (ít ô, DB trôi, một mẫu max).

---

## 1. Khóa bản (§8.3: "khóa digest FlashTicket, commit repo lab, sha256 bản M1, kịch bản và mức tải")

**ĐX.** Lập `results/T-0xx/khoa-w7.json` (task W7) trước lượt thu đầu tiên, gồm các mục dưới. Hash nằm trong manifest đó, không rải trong văn bản (AGENTS §10). Một mục đổi sau khi khóa thì lượt sau đó không thuộc đợt W7 (giữ, báo riêng).

| Mục | Giá trị hiện biết (nguồn) | Trạng thái |
|---|---|---|
| FlashTicket | revision `36a3725` nhánh `rca/exp-2026-11`; image `ft-local/*:arm64-t067-36a3725d` của 7 service, Keycloak `arm64-776d9c9e` (`results/T-071/e0-trang-thai.md`, kiểm 20/11 12:55Z) | ĐÃ-KIỂM tên image; **digest từng image chưa ghi** → khóa phải lấy `docker inspect` Id/RepoDigests lúc E6 |
| Cấu hình hiệu lực app | `compose-dir` của inj3 `/opt/flash-ticket-build/t067-compose/hieu-luc`; quota CPU Booking 1,0 | ĐÃ-KIỂM (e0); sha256 file cấu hình chưa có |
| Repo lab | `407b4f5` hiện chạy trên exp-app, exp-obs. W7 cần commit mới (runner đóng gói đầu vào, ô đánh giá trong inj3, adapter baseline) | CHỜ gói code; commit do Minh duyệt |
| Bản chụp mã M1 | `/srv/rca-lab/m1-snapshots/b0f79a4d…` (`runner4.py` dòng `M1_CODE`) | ĐÃ-KIỂM trong code |
| P7 | `method_version` `M1-T046-1` (`results/T-064/hop-dong-dau-ra.md` §1) | ĐÃ-KIỂM |
| V082 | cấu hình `cau_hinh_sha256` và `cau_hinh_file_sha256` ở `results/T-064/cau-hinh-de-xuat.json`; runner kiểm hash file trước khi chạy (`runner4.py::chay_v082`) | ĐÃ-KIỂM |
| Biến thể che (D14) | cấu hình mới, sinh từ V082 theo §3.3 | CHỜ gói code |
| Baseline | BARO: `RCAEval 259ea41 e2e/baro.py`; SimpleRCA: `src/simplerca` (T-017, M4) (`src/p3/adapters/*.py` dòng `VERSION`) | ĐÃ-KIỂM; adapter FlashTicket chưa có |
| Kịch bản tải | `load/scenarios/purchase-journey.js`, `load/profiles/purchase-journey.json`, `tai_linux.py` (repo lab); phiên bản k6 trên máy tải | sha256 lấy theo commit lab; phiên bản k6 chưa ghi |
| Mức tải | ×1 (hồ sơ hiện hành) và ×3 cả chu kỳ (như `BINH-THUONG-X3`, `CONSUMER-BOOK-SLOW-X3`) — §5.2 | ĐX |
| Bộ tiêm | `faults/injectors/docker/inj3.py` + mục ô đánh giá mới; `faults/toxiproxy/proxies.json` | CHỜ gói code |
| Luật cảnh báo | file `provisioning/alerting/` do T-072 chốt; giờ luật có hiệu lực | CHỜ-W4 |
| Bộ chế độ (b) | bộ nhận webhook, bộ gom, bộ xuất theo t̂ của T-073 | CHỜ-W5 |
| Trạng thái DB | mốc (dump) và chính sách §5.3 | CHỜ-MINH, CHỜ-W4 |
| Đồng hồ | độ lệch đồng hồ exp-app, exp-obs, máy tải (R-07 đòi) | chưa có số; đo ở E6 |

**Vì sao lấy digest ở E6, không lấy bây giờ:** khóa phải mô tả đúng máy lúc thu. Từ nay tới E6, T-071–T-073 còn đổi cấu hình (luật, bộ nhận). Lấy sớm thì phải lấy lại.

---

## 2. Chế độ (a) và (b)

| | Chế độ (a) | Chế độ (b) |
|---|---|---|
| Mốc vào lõi | t = mốc tiêm từ sổ, điều phối truyền vào (như thông tin vận hành biết trước; B1.9) | t̂ = lúc luật chuyển sang firing theo lần đánh giá (I1 `t_hat`) |
| Ai biết nhãn | runner đọc sổ để lấy t; phương pháp không đọc sổ | không ai đọc sổ trước khi đầu ra đã băm |
| Cửa sổ | N = [t−300, t), A = [t, t+300) | N = [t̂−300, t̂), A = [t̂, t̂+300) (D3, I1) |
| Ca không có cảnh báo | vẫn chạy (có t) | không có đầu vào → tính trượt trong mẫu số chính (§9.2) |
| Báo động giả | không áp dụng | có gói đầu vào và đầu ra; báo mô tả riêng |

**ĐX:** mọi bản (D14) và mọi baseline chạy ở **cả hai** chế độ trên cùng gói đã đóng. BARO và SimpleRCA ở (b) dùng đúng t̂ của sự cố được ghép (§8.3 nguyên văn).

**D13 (biến thể nền lùi ở chế độ báo động):** chỉ báo cáo. **ĐX:** không đưa vào đợt chính; để là tùy chọn tính toán (không tốn giờ máy thu nếu gói (b) đủ dài lùi `g`). Gói (b) theo W5 chỉ có `[t̂−300, t̂+300)`, nên D13 cần gói lùi thêm `g` → **CHỜ-W5** (biết `g` khi T-072 chốt luật).

---

## 3. D14 — các bản bắt buộc và nhóm thông tin che

### 3.1 Bản bắt buộc (B1.9, Q-201)

| # | Bản | Nội dung | Trạng thái |
|---|---|---|---|
| 1 | P7 khóa chạy thẳng | `run_m1.py` (P7) trên phần hợp đồng chung | ĐÃ-KIỂM có trong runner |
| 2 | Bản FlashTicket đã khóa | V082 = H5b + H8s1 + H8a | ĐÃ-KIỂM |
| 3 | V082 che từng nhóm thông tin phong phú | §3.3 | ĐX; danh sách nhóm cần kiểm kê code |
| (4) | Gói thông tin chung tối ưu riêng | Tùy chọn; **ĐX: không làm** — chưa có ứng viên nào được thiết kế; làm thêm là tối ưu trên dev mới | ĐX |

### 3.2 Nguyên tắc che (B1.9 nguyên văn)

Cùng ca, cùng cách chấm. Che cả đầu vào lẫn phần dẫn xuất trực tiếp. Thông tin bị che đi theo nhánh dự phòng khai trước. Không điền số 0 giả. Không bỏ ca.

### 3.3 Nhóm thông tin của V082 và nhánh dự phòng (ĐX, phải kiểm kê code trước khi khóa)

Phân biệt **thông tin** với **phép tính**. D14 che thông tin. H8s1 (sàn 1 ms) là phép tính, không là thông tin; phép bỏ H8s1 đã chạy ở T-069 bước 7.4 (V061), đó là phép bỏ thành phần, không là phép che.

| Nhóm | Thông tin | Thành phần dùng | Dẫn xuất phải che cùng | Nhánh dự phòng khai trước | Bằng chứng hiện có |
|---|---|---|---|---|---|
| G-live | Kênh liveness `live-down` từ gói bổ sung (`prometheus-bo-sung.json`, lần dò mới nhất, WHY-99) | H5b | kênh `metric|<svc>_live-down` trong `extra.kenh_co`; khóa ghi đè của H5b; chú thích `chet_im` | Chạy V082 không có gói bổ sung → H5b không có bằng chứng, giữ khóa P7 gốc. Cách nhận biết: chú thích `chet_im.thanh_phan` rỗng | `ho-so-chon.md` §17 (ca ebd5ef38: khi kênh vắng, khóa trả về khóa P7) — ĐÃ-KIỂM một ca |
| G-inst | Định danh nhiều chuỗi runtime cho một metric logic (instance/pod tạo lại) | H8a (H8-adapter gộp chuỗi) | chuỗi đã gộp | **Hai lựa chọn, CHỜ-MINH (Q-W6-04):** (i) hành vi P7 (lỗi "Multiple runtime series", ghi trượt, như WHY-96); (ii) giữ chuỗi mới nhất. (i) đúng chữ "không bịa dữ liệu" nhưng cho kết quả lỗi chạy; (ii) là một phép xử lý mới chưa có trên dev | `ho-so-chon.md` §15: lợi của H8a chỉ đến từ một ca (RECREATE-PAY) |
| (không thuộc V082) | Thuộc tính span bổ sung (`src/m1_ft/bo_sung.py::span_phu`), log phụ | H1, H6, H7, H8-log (không bật trong V082) | — | — | ĐÃ-KIỂM tĩnh: `chay_ca.py:96` chỉ nạp đầu vào mà `can_bo_sung()` của thành phần bật đòi; trong ba thành phần V082 chỉ `H5-liveness` khai (`bundles`, `bundles_bo_sung`; `h4_h5.py:93`), `H8-san`, `H8-adapter` không khai. Chưa kiểm động (chạy thật) |

**Phép kiểm kê bắt buộc trước khi khóa (gói code W7):** liệt kê mọi tệp/khóa đầu vào mà `src/m1_ft/chay_ca.py` với cấu hình V082 đọc ngoài đầu vào của P7; chạy V082 trên 3 ca dev với từng nhóm che và đếm khóa đầu ra khác P7 (soi trung gian, QT5). Nhóm nào che xong mà đầu ra vẫn khác P7 ở chỗ không giải thích được thì còn dẫn xuất chưa che.

**Vì sao chỉ hai nhóm:** V082 chỉ bật ba thành phần (`cau-hinh-de-xuat.json#/cau_hinh/thanh_phan`). H2, H3, H4 (JVM, pool, queue) bị bỏ ở T-064, nên kênh của chúng không vào V082. Nếu kiểm kê thấy nhóm khác thì thêm dòng và trình lại.

### 3.4 Đối chứng quan hệ (QT8, RQ3d) — ĐX, chỉ tính toán

- `DC-bo-quan-he` trên V082 (tắt E1, E2, E5; `src/m1_ft/thanh_phan/dc_bo_quan_he.py`).
- Quy tắc đơn giản trên cùng đồ thị: C-d1, C-d2, C-d3 (`src/m1/doi_chung.py`, chỉ báo cáo).
- Không tốn giờ máy thu. Thêm khoảng 1 phút tính/ca/chế độ (CHƯA-KIỂM, theo thời gian V082 ~50 giây cho hai lần chạy, §11).
- Không có đối chứng đồ thị ngẫu nhiên (M-25), nên kết luận dừng ở "lợi của phép dùng quan hệ".

---

## 4. Ma trận ô chạy được trên bản ghim (`36a3725`)

### 4.1 Nguồn

Ô đánh giá theo T-059 (`results/T-059/danh-muc-loi.md`, bảng "Danh mục theo D.9", cột Đợt = đánh giá) và danh sách đối chiếu ở `results/T-063/o-dev-bo-sung.md` dòng 3. Chia theo ô giữ nguyên (DECISIONS T-059 11/11; WHY-04). Ô đã dùng khi phát triển (T-063/T-064) **không** vào nhóm "vị trí mới".

### 4.2 Hiện trạng từng ô đánh giá (ĐÃ-KIỂM bằng đọc code; chưa ô nào được đầu dò xác nhận trên bản ghim)

| Ô | Root khai trước | Cách tiêm cần | Có gì trên bản ghim | Thiếu gì | Hạng |
|---|---|---|---|---|---|
| SLOW-EVENT | event-service | hook `http.delay` Event, đường `GET /api/v1/events/{id}`, target = sự kiện tải | Hook có (`event-service/.../RcaFaults.java:101,132`; `RcaFaultsWebConfig.java:33` mặc định đúng đường này). Tải gọi đường này mỗi hành trình (`purchase-journey.js:96`) | Mục ô trong `inj3.py`; chọn cường độ; đầu dò độc lập | A |
| POOL-BOOK | booking-service (pool là vị trí vật lý) | hook `pool.hold` Booking | Hook có (`booking-service/.../RcaFaults.java:102,163–165`) | Mục ô trong `inj3.py`; cường độ (pool max 5 theo T-063 22:47Z); đầu dò Hikari | A |
| TICKET-PAUSE | ticket-service | `docker pause` Ticket | Kiểu `pause` có (`inj3.py`, ô PAUSE-PAYMENT); liveness `:8084` có trong collector (`agent-docker-host.yaml:136`); tải có bước phát vé và `get_tickets` | Mục ô trong `inj3.py` | A |
| CPU-EVENT | event-service | đốt CPU trong cgroup Event | Kiểu `cpu` có (CPU-BOOK) | **Event không có quota CPU** (chỉ Booking 1,0; STATE). Đốt không quota ảnh hưởng cả máy, khác cơ chế CPU-BOOK | A nếu Minh chọn cách xử lý quota (Q-W6-03) |
| DB-BOOK-LAT | booking-service → booking_db | Toxiproxy trên JDBC của Booking | `proxies.json` chỉ có 4 proxy (event-jdbc, booking-redis, gateway-booking-http, booking-amqp) | Proxy mới; tạo lại Booking với URL DB qua proxy; giữ proxy suốt đợt | B |
| NET-GW-EVENT | api-gateway → event-service | Toxiproxy trên đường Gateway → Event | Như trên | Proxy mới; đổi route Gateway | B |
| NET-PAY-BOOK | payment-service → booking-service | Toxiproxy trên `BOOKING_SERVICE_URL` của Payment | Như trên | Proxy mới; tạo lại Payment | B |
| REDIS-GW | api-gateway → cache | Toxiproxy trên Redis của Gateway | Như trên | Proxy mới; tạo lại Gateway | B |
| HTTP5-BOOK | booking-service | hook `http.error` Booking, `GET /api/v1/orders/{orderId}`, đòi đúng chủ đơn | Hook có, nhưng **target là một mã đơn cố định** và Booking bắt buộc `subject` (`RcaFaults.java:103,129`). Tải tạo đơn mới mỗi hành trình (`purchase-journey.js:100,112`) → hook không chạm lưu lượng thật (cùng vấn đề SLOW-BOOK, T-063 ghi chú 22:50Z) | Sửa hook (đổi image → lệch bản ghim) hoặc thêm bước đọc đơn cố định vào hỗn hợp tải chung | C |
| SAGA-TICKET-FAIL | ticket-service | hook terminal trong `TicketService.issue` | Ticket **không có** module `src/rca-test` (chỉ Booking, Event có) | Code hook + build image Ticket mới | C |
| VNPAY-REFUND-LAT | payment-service → vnpay | Toxiproxy trên đường hoàn tiền | Mock VNPay có (`faults/mocks/vnpay/`) | Tải **không có bước hoàn tiền** (`purchase-journey.js` chỉ có tạo đơn, hủy, thanh toán, IPN, poll, lấy vé) | C |
| DB-BOOK-DOWN | booking_db | Can thiệp cô lập ở DB đích | — | Chưa có cách cô lập DB logic (T-059) | D (OPEN) |
| FLASH-HEALTHY | root = null | không can thiệp, tải flash | Có | Ngưỡng khỏe khai trước | đối chứng |

Hạng: **A** chỉ thêm mục vào bộ tiêm, không đổi image, không đổi topology. **B** đổi topology (proxy mới, tạo lại container với cấu hình khác; image không đổi). **C** đổi code/image hoặc đổi hỗn hợp tải. **D** chưa có cách làm.

### 4.3 Hệ quả cho kết luận

- Hạng A có 3 ô có sẵn cơ chế tiêm (SLOW-EVENT, POOL-BOOK, TICKET-PAUSE; chưa ô nào được đầu dò xác nhận) và 1 ô có điều kiện (CPU-EVENT). Ba hoặc bốn vị trí mới là **ít** để nêu mẫu hình (QT15, SL14). Bootstrap theo ô với 3–4 ô cho khoảng tin cậy rộng và suy biến dễ.
- Thêm hạng B lên 7–8 ô, gồm cả 2 ô cạnh mạng, 1 ô cạnh dữ liệu, 1 ô cache. Đây là các họ lỗi mà đồ thị có thể giúp định vị tuyến (T-059 "Kiểm điều gì"). Không có B thì câu "cạnh có ích trên vị trí mới" không phân xử được.
- Hạng B đổi topology so với lúc W4 chọn ngưỡng (E2/E4). Proxy thêm một chặng TCP cục bộ; ảnh hưởng tới p95 route và luật cảnh báo **CHƯA-KIỂM**. T-059 đòi giữ proxy "trong mọi ô, mọi pha, các đêm nền và đối chứng". Nếu thêm proxy sau W4, khoảng nền của W4 không có proxy → luật W4 chưa được đo báo động giả trên đúng topology W7.
- Hạng C đổi bản ghim (image Ticket mới, hoặc hỗn hợp tải khác dev). Kế hoạch §8.1 ghim một bản dùng xuyên W3–W7.
- **CHỜ-MINH (Q-W6-02):** chọn phạm vi A / A+B / A+B+C.

### 4.4 Nhóm "tình huống đã phát triển" (câu hỏi 3 của D.9)

T-069 đã thu lại 17 ô dev trên bản ghim ở chế độ (a), có đầu ra P7 và V082 (`results/T-069/bang-theo-o-2.md`). Theo luật 20, **ĐX** dùng lại 17 gói đó cho câu "lặp lại được trên tình huống đã phát triển" ở chế độ (a): chạy thêm baseline, bản che và đối chứng quan hệ trên các gói đã có (chỉ tính toán). Giới hạn phải ghi: các gói này thu **trước** khi khóa W6, DB khác trạng thái W7, và đã được xem kết quả (ô tụt CPU-BOOK-1). Vì vậy chúng chỉ là nhóm "đã phát triển", không bao giờ vào nhóm "vị trí mới".

Chế độ (b) cho nhóm này cần lượt mới (T-069 không chạy luật cảnh báo). **ĐX:** tùy chọn, 1 lần mỗi ô lỗi dev ở ×1 (11 chu kỳ, `du-toan.json#/phuong_an/nhom_da_phat_trien_b`). CHỜ-MINH (Q-W6-02).

### 4.5 Xác nhận can thiệp và chọn cường độ trên ô đánh giá

- Cường độ của ô đánh giá chọn bằng **đầu dò độc lập**, không bằng đầu ra RCA. Dùng chế độ `d2` của runner (can thiệp 150 s, đầu dò trước/trong/sau, không chạy RCA; `runner4.py::chay_d2`).
- Điều kiện xác nhận viết trước, theo T-059 từng ô ("Điều kiện xác nhận"). Ô không xác nhận được ở pilot thì không vào đợt chính; ghi lý do.
- **Vì sao không vi phạm chia ô:** chọn cường độ theo đầu dò không dùng nhãn trong phương pháp và không nhìn điểm của phương pháp nào. Rủi ro còn lại: người làm thấy tín hiệu telemetry khi xem đầu dò. Giảm bằng cách đầu dò không gọi app và không mở gói RCA (như `inj3.py` docstring).

---

## 5. Thiết kế đợt W7

### 5.1 Đơn vị và lặp

- Đơn vị: một chu kỳ `runner4` 3 × PHASE (PHASE = 600 s): 600 s nền, 600 s lỗi (hoặc không can thiệp), 600 s hồi phục. Đo thực tế 31,4 phút/chu kỳ trên 17 chu kỳ lượt chính T-069 (`results/T-069/thu/t069-chinh/chay/nhat-ky-3.jsonl`: "load started" đầu tiên 09:35:34Z, "Lượt thu xong" 18:29:18Z; lệnh ở LOG).
- **ĐX:** mỗi ô đánh giá × 2 mức tải (×1, ×3 cả chu kỳ) × 3 lần lặp. "Hai mức tải" theo DECISIONS T-059 ("các lần lặp hai mức tải của một ô đánh giá vẫn ở phía đánh giá"). Ba lần lặp theo WHY-04 (lặp đi cùng ô).
- Đối chứng: BINH-THUONG ×1 (3), BINH-THUONG-X3 (3), FLASH-HEALTHY (3). Lý do: đo K (kết luận ca khỏe) và báo động giả ở cả hai mức tải.
- **Vì sao ×3 cả chu kỳ, không dùng flash bậc ở t:** flash của runner tăng bậc đúng ở PHASE = t (`runner4.py::start_load`, `--buoc-tai PHASE`), tức trùng mốc tiêm. Khi đó "tải tăng" và "lỗi" cùng lúc, không tách được. ×3 cả chu kỳ giữ tải đều qua cả N và A.
- Mặt trái: ×3 cả chu kỳ không kiểm câu phụ RQ5 (tải tăng đột biến vs sự cố). Câu đó cần flash có bậc tách khỏi t; giữ OPEN.

### 5.2 Thứ tự

**ĐX:** trộn ngẫu nhiên theo khối với seed khai trước (ghi sha256 lịch trước khi phát). Mỗi khối chứa đúng một lần lặp của mỗi (ô, mức tải) và một mỗi đối chứng. Lý do: DB tích lũy và giờ trong ngày đổi theo thời gian (`lich-su/04` §3: truy vấn nền chậm ~1,7 lần sau ~8,5 giờ tải; `results/T-069/phan-tich/troi-trong-luot.txt`). Khối cân bằng làm vị trí trung bình của mọi ô như nhau, nên xu hướng tuyến tính không thiên về ô nào.

### 5.3 Kiểm soát trạng thái DB — **ứng viên, CHỜ-MINH (Q-W6-01), CHỜ-W4**

Sự thật đã có:
- `tbl_orders` 40.069 dòng lúc 02:31Z 20/11 (`thong-nhat.md` §1.2). Mỗi chu kỳ ×1 tạo 648 đơn (`results/T-069/thu/t069-chinh/tai-create-order.json`), ×3 khoảng 1.944 (CHƯA-KIỂM: suy từ 0,36 đơn/s × 3 × 1800 s, `results/T-071/e1/suc-chua.json#/nhu_cau_uoc`).
- Một đợt 57 chu kỳ (phương án A+B+CPU-EVENT) thêm tới 74.520 đơn theo giả định bảo thủ (`du-toan.json#/phuong_an/3`), tức gần gấp đôi bảng hiện tại.
- T-069: nguồn mẫu đuôi DB ở ô CPU-BOOK-1 là **ứng viên** (DB lớn / code đường mua / tranh chấp CPU / dao động), chưa phân xử (`dinh-chinh-1.md` §2). Không được thiết kế như thể DB là nguyên nhân đã biết.

| Phương án | Cách làm | Ưu | Nhược / điều kiện thất bại | Chi phí thêm |
|---|---|---|---|---|
| K0 | Giữ tích lũy, trộn khối (§5.2), ghi kích thước bảng tại mỗi ca làm hiệp biến | Rẻ; giống hệ chạy thật | Ca cuối đợt gặp DB lớn gấp 2–3 lần ca đầu; trộn khối chỉ chống thiên lệch giữa ô, không chống "điều kiện trôi trong đợt" | 0 |
| K1 | Khôi phục về mốc một lần trước đợt + trộn khối | Đầu đợt tái lập được | Trong đợt vẫn trôi như K0 | 1 lần khôi phục |
| K2 | Khôi phục về mốc đầu mỗi khối (mỗi ~6–9 chu kỳ) + trộn trong khối | Biên DB bị chặn trong mỗi khối; khối nào cũng cùng điều kiện đầu | Khôi phục chỉ PostgreSQL trong khi Redis (giữ chỗ, cache), RabbitMQ (hàng đợi, outbox) và mock còn trạng thái cũ → **có thể không nhất quán**; cần dừng tải, chờ hàng đợi rỗng, có thể phải khởi động lại service. Khôi phục thất bại hỏng cả khối | ~6–10 lần khôi phục; thời gian mỗi lần **chưa đo** |
| K3 | Như K0 nhưng thêm 2–3 ô "mốc" (ví dụ BINH-THUONG) rải đều để đo trôi trong đợt | Đo được trôi trên chính đợt | Không giảm trôi, chỉ đo | 2–3 chu kỳ |

Bốn điều kiện để khôi phục không thành sửa kết quả (`lich-su/04` §5): khai trước; áp như nhau mọi ô và mọi phương pháp; mốc không chọn theo điểm; báo cáo công khai hiện tượng trôi. Ở thiết kế này RCA chạy **sau** khi đợt đã đóng (§8), nên lúc chọn chính sách DB không ai thấy điểm của đợt W7 — điều kiện 3 được bảo đảm về cấu trúc.

**Đề xuất của người làm (ĐX, có điều kiện):** chọn bằng quy tắc khai trước dựa trên kết quả W4, áp **trước** khi xem bất kỳ đầu ra W7:
- Nếu T-071/T-072 cho thấy trôi E2→E4 làm đổi số cảnh báo hoặc p95 route vượt mức khai trước (mức do T-072 đặt) → K2, **với điều kiện** E6 chứng minh khôi phục nhất quán (§5.4).
- Ngược lại → K0 + ô mốc của K3.
- E6 trượt kiểm nhất quán → K0 + K3, ghi giới hạn "DB trôi trong đợt".

Mặt trái: quy tắc này nối W7 vào kết quả W4 (CHỜ-W4). Nếu W4 trễ, W7 trễ theo. Phương án khác: Minh chọn thẳng K0+K3 ngay (không chờ W4), chấp nhận giới hạn.

**Không đề xuất** thu nhỏ DB về cỡ ca cũ (~4k đơn): phải xóa dữ liệu nghiệp vụ và dễ bị hiểu là sửa cho giống điều kiện cũ (`lich-su/04` §4c).

### 5.4 E6 — phép đo khôi phục (khung S5, sau E5; cần SPEC bổ sung, SPEC T-074 "Phạm vi ghi")

**ĐX** nội dung phép đo (chưa có quyền chạy):
1. Chụp trạng thái: số dòng các bảng chính, đơn dở theo trạng thái, độ sâu hàng đợi RabbitMQ, khóa Redis theo tiền tố, trạng thái mock.
2. Khôi phục `booking_db`, `ticket_db`, `payment_db` (và DB khác nếu dump có) về mốc E1 (`results/T-071/e1/moc-db.json`). Đo thời gian từng bước, kể cả dừng/khởi động service nếu cần.
3. Kiểm nhất quán: so số dòng với `moc-db.json`; không còn đơn dở; hàng đợi rỗng; Redis không giữ chỗ mồ côi; một hành trình mua trọn; liveness tốt.
4. Chạy một chu kỳ BINH-THUONG (31 phút) sau khôi phục, đối chiếu tín hiệu nền với đầu E2.
5. **Tùy chọn, rẻ, phân xử một phần T-069** (luật 12): ngay sau khôi phục chạy CPU-BOOK-1 và HTTP5-EVENT (2 chu kỳ). Cùng image `36a3725`, DB nhỏ hơn hiện tại → tách được giả thuyết "DB lớn" khỏi "code đường mua" một phần (code giữ nguyên, DB đổi). Không tách được tranh chấp CPU. Đây là ô dev, không ảnh hưởng chia ô. Chi phí ~62 phút.

### 5.5 Hạn bán 02/12 22:16Z và sức chứa vé

- Booking bán tới 02/12 (`lich-su/04` §1). Sau mốc đó hành trình mua lỗi, mọi giờ "khỏe" sai.
- Gia hạn lần nữa là sửa dữ liệu (Minh). I13 cấm sửa DB từ E1 tới hết E5. Vậy chỉ có hai thời điểm sửa: **trong E1 (đang mở)** hoặc **ở E6**.
- Nếu E2–E5 kéo quá 02/12 thì W4/W5 cũng hỏng, không riêng W7. → **Câu cho điều phối (gấp):** E1 có nên gia hạn bán luôn không (Q-W6-08).
- Sức chứa: còn 73.834 vé (`results/T-071/e1/suc-chua.json#/con_lai`); W4+W5 dùng tối đa 26.136 (`#/nhu_cau_uoc/tong`). Phương án A+B+CPU-EVENT tiêu thụ 74.520 đơn theo giả định bảo thủ (mọi đơn giữ vé), 48.663 nếu chỉ đơn hoàn tất giữ vé (65%: 26.166/40.069, CHƯA-KIỂM cho W7) → **vượt** 47.698 vé còn lại sau W4+W5 tối đa (`du-toan.json#/phuong_an`, `#/suc_chua`). A+B không CPU-EVENT: 66.744 / 43.585. Phương án A (27 chu kỳ) đủ. Nâng sức chứa là sửa dữ liệu (Minh), đặt ở E1 hoặc E6.

---

## 6. R-07 — mốc của độ trễ phát hiện

- **Mặc định (§8.3 nguyên văn) — ĐX giữ:** chấm theo sự cố tiêm đã xác nhận trong cửa sổ khai trước; độ trễ = t̂ − t (mốc tiêm), gọi là **"độ trễ theo mốc tiêm"**. Không gọi là độ trễ từ lúc sự cố bắt đầu biểu hiện (MRP P7 Độ đo).
- **Tùy chọn (chỉ khi Minh chọn kết luận theo thời điểm bắt đầu tác động):** đầu dò dòng thời gian từ tín hiệu không dùng trong RCA (k6 theo route ở máy tải: thời gian từng request, mã trạng thái). Onset = lúc đầu tiên tỷ lệ lỗi hoặc p95 route của k6 vượt ngưỡng khai trước trong cửa sổ trượt; hồi phục tương tự.
  - Chi phí: **0 giờ máy thu nếu k6 đã ghi từng request** (khi đó chỉ là code phân tích ~0,5 ngày); nếu không, phải đổi đầu ra k6 cho mọi ô (đổi kịch bản tải → vào khóa bản). **CHƯA-KIỂM** k6 hiện ghi gì (`tai_linux.py` lưu `tai-out/`; chưa đọc).
  - Ô không có tác động endpoint (POOL-BOOK cường độ thấp, TICKET-PAUSE khi hàng đợi kịp hấp thụ) sẽ không có onset → báo riêng, không suy onset từ mốc tiêm.
- CHỜ-MINH (Q-W6-05).

---

## 7. Baseline

| Baseline | Vai trò | Bản | Trạng thái |
|---|---|---|---|
| SimpleRCA (M4, quy ước T-017) | Baseline đơn giản đa nguồn đã công bố (QT7) | `src/simplerca`, adapter `src/p3/adapters/simplerca.py` (định dạng RE2-TT) | ĐX bắt buộc (§8.3 "SimpleRCA (M4, quy ước T-017)") |
| BARO RobustScorer | Baseline metric | `RCAEval 259ea41 e2e/baro.py`, adapter `src/p3/adapters/baro.py` | Ứng viên theo §8.3; **ĐX đưa vào** |

**Chưa có adapter FlashTicket cho cả hai.** Adapter hiện nhận khung metric dạng bảng có cột `time` và span dạng RE2-TT (`baro.py::chay(metric_win, t, dataset='re2-tt')`). Gói ca FlashTicket là bundle Prometheus + OTLP qua `m1.adapter_flashticket`. Cần (gói code W7):

1. Chuyển gói ca → khung metric (từ `normalize_metrics`), span (từ `normalize_spans`), log (từ `normalize_logs`). Dùng đúng thực thể của inventory T-037 như M1, để tập ứng viên của mọi phương pháp như nhau (B1.9 "tập ứng viên khai trước theo loại nút").
2. Tham số `dataset` của BARO: `preprocess` của RCAEval có xử lý theo tên dataset. **CHƯA-KIỂM** nó làm gì với `re2-tt`. ĐX: dùng nhánh không lọc theo dataset (`dk_select_useful=False` như hiện tại) và khai rõ trong WHY.
3. Quy ước SimpleRCA (WHY-17) giữ nguyên: mean+3σ, đếm sự kiện, P95 trace ×3, từ khóa log, hòa theo nhóm, `abstain` khi toàn 0.
4. **Phép kiểm không nhãn (SL24, SL36) trên dev trước khi khóa:** chạy lại ra cùng kết quả; thứ hạng không trùng thứ tự cột; đếm số cột vào thật, số lần rơi nhánh dự phòng (`abstain`, cột hằng, IQR = 0); hai cửa sổ đều bình thường không "tìm ra" nguyên nhân.
5. Dev cho adapter: 17 gói T-069 và gói T-063 (chỉ dữ liệu phương pháp). Hiệu chỉnh adapter để chạy đúng, **không** chọn tham số theo điểm.

**Khóa danh sách và nhánh dự phòng của từng phép che trước khi thu** (§8.3): bảng §3.3 + bảng dự phòng baseline (`abstain` → `NO_EVIDENCE`, đếm vào mẫu số như trượt; lỗi chạy → `ERROR`, đếm trượt, phân loại theo luật 21).

**Baseline khác** (MicroRank, TraceRCA, Nezha có adapter ở `src/p3/adapters/`): không có trong §8.3. Bước 4 của cô và QT7 cần "baseline mạnh"; bài FSE 2026 công bố SimpleRCA top-1 0,80 trên RE2-TT (LESSONS ST9, số công bố, không phải số của repo này) nên nó là mốc mạnh. CHỜ-MINH (Q-W6-07) có thêm một baseline trace không; mặc định ĐX không thêm (chi phí adapter chưa ước lượng, T-062 `spec-chang-4-de-xuat.md` dòng 62).

---

## 8. Runner W7 — thu trước, RCA sau

### 8.1 Vì sao phải đổi runner hiện tại

- `runner4.py::m1_worker` chạy stage → P7 → `nhan_ca` → V082 → `sau_v082` cho từng ca **ngay trong đợt** (ĐÃ-KIỂM, dòng 212–235).
- `safe_export.py case` từ chối đóng gói khi chưa có `outputs/<id>/summary.json` (ĐÃ-KIỂM, dòng `if not (... 'summary.json').is_file(): raise SystemExit`). Tức gói đầu vào phụ thuộc đầu ra M1. Đây là bài học T-069 Bước 0 mục 0.8.
- `stage_m1.py` đọc **tiền tố có giới hạn** của file ghi vòng của Collector (ĐÃ-KIỂM, docstring). Vì vậy **không thể** dời việc chụp đầu vào tới sau đợt: capture có thể đã quay vòng. Thời hạn giữ của vòng ghi **CHƯA-KIỂM**.

### 8.2 Thiết kế (ĐX)

| Pha | Việc | Nơi chạy | Đọc nhãn? |
|---|---|---|---|
| T1 Thu (trong đợt) | Chu kỳ như runner4 (sổ, tải, tiêm, đầu dò, hồi phục). Tại t + PHASE + 150: `stage_m1` (chụp capture) + `xuat_bo_sung` (gói bổ sung) → **niêm gói đầu vào** (manifest + sha256), **không chạy M1**. | exp-obs | Runner đọc sổ để biết t; gói không chứa nhãn |
| T1b Chế độ (b) (trong đợt) | Bộ nhận T-073 ghi mọi bản ghi cảnh báo (I1) suốt đợt. Mỗi sự cố (theo quy tắc gom T-072): chụp gói theo t̂ đủ `[t̂−300, t̂+300)` (bộ xuất theo t̂ của T-073) → niêm. Gồm cả sự cố giả. | exp-obs | Không |
| T2 Đóng đợt | Danh sách gói (a) và (b) + sha256 → `dong-dot.json`; băm danh sách; ghi LOG trước khi chạy RCA | laptop nhận và kiểm | — |
| T3 RCA batch | Trên gói đã niêm: P7, V082, V082-che (§3.3), đối chứng quan hệ (§3.4), SimpleRCA, BARO; cả (a) và (b). Đầu ra băm. | máy tính toán (§11) | (a): t từ danh sách do điều phối truyền; phương pháp không đọc sổ |
| T4 Chấm | Ghép nhãn sau khi danh sách đầu ra đã băm; chấm theo §9 | laptop | Có (chỉ bộ chấm) |

- `safe_export.py`: thêm chế độ `case-input` chỉ đòi `cases/<id>/manifest.json` (bỏ điều kiện `summary.json`, đúng §8.3 nguyên văn). Chế độ `case` cũ giữ nguyên cho tuyến W5.
- Tuyến trực tuyến W5 (dashboard, `sau_v082.py`) **tách riêng**, không dùng gói hay đầu ra của W7. Nếu muốn demo cùng lúc thì là một tiến trình khác, đầu ra ở vùng khác (I9).
- Mã ca mờ như runner4 (`secrets`); ánh xạ mã → ô chỉ có trong sổ (user `ledger`).

### 8.3 Tranh chấp tài nguyên trong đợt (C4, I3)

`stage_m1` + `xuat_bo_sung` của chu kỳ k chạy trong lúc chu kỳ k+1 đang đo (như runner4). `xuat_bo_sung` truy vấn Prometheus sống. Bỏ chạy M1 trong đợt đã giảm tải so với runner4 (bớt P7 + V082 ~50 giây CPU/ca trên exp-obs). Phần còn lại **CHƯA-KIỂM** về tác động lên đo. ĐX: pilot đo thời gian và tải exp-obs của bước chụp; nếu đáng kể thì dời bước chụp vào 2 phút đầu chu kỳ sau (trước t của chu kỳ đó − 300, tức trong phần N chưa dùng). Phương án khác: thêm khoảng nghỉ giữa chu kỳ (tốn thời gian).

### 8.4 Quy tắc gói hợp lệ (khai trước, áp trước khi có đầu ra RCA)

Một ca vào mẫu số chính khi đủ cả năm:
1. Sổ đủ chuỗi sự kiện chu kỳ (bắt đầu, tải, mốc, tiêm/không tiêm, dừng, kết thúc); môi trường sạch trước và sau (`inj3 verify`).
2. Can thiệp xác nhận theo điều kiện viết trước của ô (đầu dò t+60, t+330). Không xác nhận → giữ, báo nhóm "can thiệp chưa xác nhận" (T-059 ba lớp).
3. Tải khỏe ở phần N theo tiêu chí I2 (hành trình xong, `dropped_iterations`, 429, lỗi HTTP) — tiêu chí cụ thể lấy từ T-071 (CHỜ-W4).
4. Telemetry đủ: gói có trace, log, metric phủ cửa sổ; Prometheus không khởi động lại trong `[t−300, t+300)`; số mẫu mỗi kênh không dưới mức khai trước (đặt ở pilot từ gói T-069).
5. Gói đã niêm, hash khớp hai đầu.

Ca không hợp lệ: giữ nguyên, báo bảng riêng có lý do. **Thay thế** chỉ khi lý do là hạ tầng (1, 3, 4, 5), tối đa 1 lần mỗi slot, bằng lịch con cuối đợt. Không bao giờ thay vì kết quả RCA (lúc đó chưa có kết quả nào).

### 8.5 Lỗi giữa chừng (luật 21) — chi tiết số ở `du-toan.json#/loi_giua_chung`

- Lỗi một chu kỳ (tiêm không khởi động, tải hỏng một lần): chỉ chặn chu kỳ đó; bù bằng lịch con. Chi phí 31 phút, bất kể xảy ra ở 10%, 50% hay 99%.
- Lỗi nguồn chung (mất telemetry, Prometheus khởi động lại, sai proxy/cấu hình tải, DB khôi phục sai): kiểm sau **mỗi** chu kỳ (điều kiện 3–5 ở §8.4) để phát hiện trễ tối đa 1–2 chu kỳ. Chỉ lỗi mà phép kiểm không bắt được mới lan ra. Lỗi phát hiện muộn ở 10/50/99% với phương án A+B+CPU-EVENT: mất 3,0 / 14,9 / 29,5 giờ thu nếu không có kiểm mỗi chu kỳ; tối đa ~1 giờ (2 chu kỳ) nếu kiểm bắt được.
- Lỗi phương pháp ở T3: đợt đã đóng, không thu lại. Lỗi chỉ chặn slot (ca × phương pháp × chế độ). Thêm quy tắc phân loại không buộc chạy lại slot đã xong (quy tắc phân loại tách khỏi vân tay code tính toán, SL38).
- Lỗi chấm: chấm lại, đầu ra giữ nguyên hash.
- Laptop mất mạng: lịch giao cho server; không mất chu kỳ (`thong-nhat.md` §1.5).
- Quét điều kiện suy biến ở pilot dev (luật 21c): BARO cột hằng/IQR 0, dưới 2 mẫu nền; SimpleRCA σ = 0, thiếu modality; V082-che với gói bổ sung rỗng; (b) t̂ trong 300 s đầu tải (N chứa lúc chưa có tải) hoặc t̂ + 300 vượt hết chu kỳ; sự cố vắt qua biên chu kỳ.

---

## 9. Độ đo theo đầu ra (§8.3 bảng)

### 9.1 Phát hiện (chế độ (b)) — ĐX, phụ thuộc quy tắc gom của T-072 (CHỜ-W4)

Mỗi chu kỳ chia ba đoạn theo sổ: nền `[S, t)`, lỗi `[t, t+600)`, hồi phục `[t+600, S+1800)`.

| Đại lượng | Định nghĩa |
|---|---|
| Cửa sổ dương | đoạn lỗi của ca có can thiệp đã xác nhận |
| Cửa sổ âm | đoạn nền của mọi ca, cộng đoạn lỗi và hồi phục của ca đối chứng khỏe đã xác nhận khỏe |
| Ghép | sự cố (sau gom) ghép với cửa sổ dương khi t̂ ∈ `[t, t+600+G)`; G (dung sai trễ) khai trước, ĐX G = 120 s. Nhiều sự cố cùng cửa sổ: tính một lần, báo số trùng |
| Recall | số cửa sổ dương có ≥ 1 sự cố ghép / số cửa sổ dương |
| Precision | số sự cố ghép được / số sự cố t̂ nằm trong đoạn được chấm |
| F1 | từ hai đại lượng trên |
| Bỏ sót | cửa sổ dương không có sự cố ghép, kèm lý do nếu xác định được (luật không phủ, tín hiệu dưới ngưỡng, mất quan sát) |
| Báo động giả mỗi giờ khỏe | sự cố không ghép trong cửa sổ âm / số giờ âm khỏe. Báo riêng với số của W4 (W4 dùng lượt ≥ 60 phút; đoạn nền W7 chỉ 10 phút ngay sau khi tải bắt đầu) |
| Độ trễ theo mốc tiêm | t̂ − t của sự cố ghép đầu tiên (R-07, §6) |

Đoạn hồi phục của ca lỗi không tính âm cũng không tính dương (chuyển tiếp). Lý do: sự cố còn kéo dài sau khi gỡ lỗi là hệ quả thật, không phải báo động giả.

### 9.2 Xếp hạng

- Độ đo: MRR, NDCG@5, Hit@1/3/5, AC@k, Avg@5 theo B1.9 và quy tắc nhãn T-059; hòa theo nhóm hòa (`tie_group`) với hạng kỳ vọng như WHY-17 và `cham_dev3.py` của T-064.
- Ba bảng khóa riêng: (1) điểm theo nhãn thật; (2) điểm theo tập nút chấp nhận (`{caller, callee}` cho ô cạnh); (3) bảng định vị cạnh có hướng, có loại — V082, P7, baseline ghi `UNSUPPORTED`.
- Chế độ (b): ca không có sự cố ghép **giữ trong mẫu số** (RR = 0, Hit = 0, NDCG = 0). Báo thêm điểm trên nhóm có cảnh báo. Nhiều sự cố ghép cùng cửa sổ: chấm đầu ra của sự cố có t̂ sớm nhất (khai trước); các sự cố sau báo mô tả.
- Ca khỏe: K = số ca khỏe mà phương pháp kết luận có nguyên nhân (như T-064). Ở (b), RCA trên sự cố giả báo mô tả.
- Báo theo ô, theo mức tải, theo chế độ, theo nhóm (vị trí mới / đã phát triển); so cặp theo ca (thắng/hòa/thua); bootstrap theo ô 10.000 mẫu, seed 20261005 (WHY-28). Với 3–8 ô, khoảng tin cậy chỉ để mô tả; không phát biểu "có ý nghĩa".

### 9.3 Vùng ảnh hưởng

- Chỉ tính Precision/Recall/F1 khi có nhãn độc lập cùng cấp: nhãn mức endpoint từ k6 theo route (T-059 "Ảnh hưởng endpoint"), dự đoán đưa về cùng mức endpoint. Nhãn này dùng cùng đầu dò dòng thời gian của R-07 tùy chọn (§6) → nếu Minh không chọn đầu dò đó, vùng ảnh hưởng chỉ báo "đồ thị con nghi ngờ", độ đúng **OPEN**.

### 9.4 Bảng diễn giải khai trước (ĐX; mỗi dòng nêu cả trường hợp không phân xử)

| Câu hỏi | So sánh | Hỗ trợ khi | Bác bỏ khi | Không phân xử khi |
|---|---|---|---|---|
| RQ5 "chuyển thẳng" | P7 trên ô đánh giá vs P7 trên ô dev (T-069) | P7 giữ AC@1/MRR trong khoảng của dev | P7 tụt rõ ở đa số ô mới | < 3 ô hợp lệ; ca trượt do thiếu quan sát |
| RQ5 "sau thích nghi" | V082 vs P7, cùng ca | V082 ≥ P7 ở đa số ô và không tụt ô nào quá 2 bậc | V082 < P7 ở đa số ô | V082 = P7 mọi ca (thành phần không kích hoạt trên ô mới) |
| Thông tin nào mang thay đổi | V082 vs V082-che từng nhóm | che nhóm X đưa V082 về P7 ở các ca V082 hơn P7 | che không đổi gì mà V082 vẫn khác P7 (còn dẫn xuất chưa che) | không ô nào có thành phần kích hoạt |
| So baseline | V082, P7 vs SimpleRCA, BARO | hơn ở đa số ô và theo ca | thua ở đa số ô | baseline `abstain`/lỗi ở đa số ca (adapter) |
| Lợi của phép dùng quan hệ (QT8) | V082 vs DC-bo-quan-he; V082 vs C-d1–d3 | hơn cả hai | không hơn | ít ô; các bản hòa |
| Giá của tự phát hiện | (b) vs (a), cùng phương pháp | — (mô tả) | — | Recall thấp làm mẫu số (b) toàn trượt |

---

## 10. Điểm yếu "một mẫu max trên kênh op gộp" (T-069) — ứng viên, CHƯA-KIỂM

**Quan sát đã kiểm** (`dinh-chinh-1.md` §2, §4): thứ tự ở CPU-BOOK-1 do khóa thứ hai (max z) của các kênh SQL gộp quyết định; z = một mẫu max chia IQR; P7 và mọi biến thể V060/V061/V066/V082 cùng hạng (`phan-tich/bien-the/hang.txt`). Đây là đặc tính lõi chung, không thuộc thành phần V082.

**Ảnh hưởng tới thiết kế W7 (ĐX):**
1. Không sửa lõi (R4, SPEC T-074 "Không làm"). Đánh giá đúng bản đã khóa.
2. Khai trước giả thuyết **chưa kiểm**: ô mà tín hiệu của service bị tiêm yếu (cường độ thấp, như SLOW-EVENT trễ nhỏ, POOL-BOOK giữ một phần pool) dễ bị mẫu đuôi DB của service khác vượt. Sai khi: mẫu đuôi DB không xuất hiện ở trạng thái DB của W7, hoặc tín hiệu tiêm đủ mạnh. Kết luận phụ thuộc: chỉ phần "phân tích ca sai" (DT18-NV3), không ảnh hưởng số chính.
3. Ghi trung gian để lần theo cơ chế (luật 15) không tốn máy: mỗi ca lưu kênh quyết định khóa thứ hai, service sở hữu, thao tác của mẫu max, mẫu max đó thuộc truy vấn nền hay đường bị tiêm. Lấy từ `#/extra/kenh_co` và span thô trong gói. Đối chiếu ca sai với ca đúng cùng ô.
4. BARO cũng lấy max robust z trên cửa sổ bất thường (`baro.py::diem_lai`), nên chịu cùng loại rủi ro mẫu đuôi. So BARO với V082 ở ca này cho biết điểm yếu là của "max một mẫu" nói chung hay của cách gộp kênh op của M1 — một phép phân xử miễn phí.
5. Phép kiểm rẻ có thể làm ngay trên dữ liệu đã có (đề xuất, chưa có quyền): đếm trên 17 gói T-069 số ca mà khóa thứ hai của thực thể hạng 1 đến từ mẫu truy vấn nền. Cho biết tần suất trên dev trước khi W7 thu.

---

## 11. Dự toán (tóm tắt; số ở `du-toan.json`)

| Phương án ô | Chu kỳ | Giờ thu | Đơn (bảo thủ) | Ghi chú |
|---|---|---|---|---|
| A (3 ô) | 27 | 14,1 | 35.640 | đủ sức chứa |
| A + CPU-EVENT (4 ô) | 33 | 17,3 | 43.416 | đủ, sát |
| A + B (7 ô; 8 nếu có CPU-EVENT) | 51–57 | 26,7–29,8 | 66.744–74.520 | vượt sức chứa còn lại (47.698) theo giả định bảo thủ; 8 ô vượt cả theo ước hoàn tất (48.663) |
| + nhóm đã phát triển (b) | +11 | +5,8 | +7.128 | tùy chọn |

Thêm: pilot/xác nhận can thiệp ô đánh giá ~1,5 giờ; E6 ~2–3 giờ (chưa đo) + 1 giờ tùy chọn phân xử T-069; K2 thêm 6–10 lần khôi phục (chưa đo). RCA batch: CHƯA-KIỂM, ước ~5 phút/ca/chế độ cho đủ bản → A+B+CPU-EVENT ≈ 9,5 giờ tính tuần tự (57 ca × 2 chế độ, chưa gồm sự cố giả ở (b)); chạy song song được (luật 19: dùng EC2 sẵn có — máy tải AWS rảnh sau khi thu — hoặc exp-obs; chọn khi có số đo pilot).

Đường găng (không có ngày, theo phụ thuộc; KE-HOACH §8.4 bổ sung 19/11): E5 xong → E6 → pilot ô đánh giá → khóa → W7 thu → đóng → RCA → chấm. Code W7 (runner, inj3, adapter baseline, bản che) viết song song W4–W5, không chờ máy.

---

## 12. Ghi WHY trước khi thu

Các mục ở `de-xuat-why.md` phải được Minh duyệt và phiên điều phối ghi `docs/WHY.md` (I6) **trước** lượt thu W7 đầu tiên. Lựa chọn nào chưa có WHY thì không dùng trong kết quả (luật 3).

---

## 13. Phụ thuộc và việc của gói sau

| Phụ thuộc | Từ | Ảnh hưởng mục |
|---|---|---|
| Độ trôi DB E2→E4; luật, quy tắc gom, `eval_interval`, `for` | T-071, T-072 | §5.3 chọn K; §9.1; tiêu chí khỏe §8.4 |
| Độ trễ xử lý chế độ (b); bộ xuất theo t̂; kiểm dữ liệu thực vào lõi | T-073 | §8.2 T1b; D13 |
| Khôi phục nhất quán | E6 (SPEC bổ sung) | §5.3 K2 |
| Code: runner thu-niêm; `safe_export case-input`; mục ô đánh giá trong `inj3.py`; adapter SimpleRCA/BARO cho FlashTicket; cấu hình V082-che; kiểm kê nhóm che | gói code W7 (SPEC riêng, worktree lab theo I10) | §3.3, §4, §7, §8 |
| Thời hạn vòng ghi Collector | đo chỉ đọc khi có khung exp-obs | §8.1 |
| k6 có ghi từng request không | đọc `tai_linux.py`/đầu ra (chỉ đọc) | §6, §9.3 |

## 14. Điều chưa chắc (tổng hợp)

- Mọi ô đánh giá **chưa** được đầu dò xác nhận trên bản ghim.
- Proxy mới (hạng B) có đổi hành vi luật W4 không: chưa kiểm.
- Khôi phục DB có nhất quán với Redis/RabbitMQ không: chưa kiểm (E6).
- Thời gian RCA batch, khôi phục DB, chụp gói trong đợt: chưa đo.
- Nhóm thông tin che của V082: mới suy từ cấu hình; cần kiểm kê code.
- Với 3–8 ô, mọi kết luận RQ5 là mô tả theo ô, không tổng quát.
