# Chiến dịch M1-FlashTicket — hồ sơ điều phối (ghi 13/11/2026, ~02:20 giờ VN = 12/11 19:20Z)

File này gom **mọi điều đã bàn và đã chốt** trong phiên Claude 12–13/11 để phiên khác tiếp nhận mà không cần lịch sử chat. Nguồn luật vẫn là `AGENTS.md`; nguồn trạng thái là `docs/STATE.md`; tiến độ sống ở `CHECKPOINT-CHIEN-DICH.md` (cùng thư mục).

**Cập nhật quyền 13/11/2026:** Minh duyệt sửa bốn SPEC và bốn file điều phối, giao Claude toàn quyền điều phối và triển khai trong phạm vi chiến dịch tới M4. Nguồn ở `docs/DECISIONS.md`, mục “Bổ sung quyền điều phối chiến dịch nhiều ngày”. Các phần dưới đã đồng bộ quyền này. Mục tiêu H1–H8, mốc M0–M4 và tiêu chí chọn tiếp tục theo kế hoạch đã duyệt.

## 0. Minh đã duyệt gì (nguyên lời ở `docs/DECISIONS.md`, mục 13/11/2026)

- 13/11: *"tổng thể đề xuất đã ổn, tuy nhiên tiếp thu các yếu tố bên dưới đây của codex … nếu hết usage giữa chừng cần tự động làm tiếp khi usage hồi phục … tạo ghi đầy đủ tài liệu … soạn prompt cho phiên mới … tôi sẽ gửi prompt và đi ngủ và chờ kết quả vào sáng mai"*. Đây là duyệt gói chiến dịch (bản đã chỉnh qua hai lượt phản biện của Codex) và lệnh ghi file.
- Mục tiêu (lời Minh): lấy **M1 bản P7 đã khóa làm nền**, phát triển bản thích nghi FlashTicket, khai thác dữ liệu quan sát phong phú hơn và xử lý hạn chế bộc lộ khi áp dụng thực tế. Kết thúc bằng **bản M1 đã tinh chỉnh mà Claude đề xuất chọn**, kèm code chạy được, cấu hình, kết quả từng ca, bằng chứng vì sao giữ/bỏ từng thay đổi, và dashboard. Bản chọn là **ứng viên** để Minh xem xét tiếp.
- Baseline: chỉ so khi M1 đã hoàn thiện, tinh chỉnh và khóa; chỉ vài baseline tiêu biểu; chọn sau. → Chiến dịch **không** so baseline.
- Mỗi ca **một lần thu chính**; chạy lặp để sau. Thử nhiều biến thể trên dữ liệu đã lưu.
- Giữ tín hiệu hiện tại; sau chạy chỉ rõ thao tác nào khiến M1 gắn cờ, đối chiếu với ảnh hưởng giao dịch, chú thích từng ca. Kết quả thô M1 giữ nguyên.
- Tải chuẩn phải có đăng nhập, đặt vé, thanh toán (bổ sung vào T-062). Không chờ nhóm hệ thống hoàn thiện mọi API; chỉ cần API lõi. Không thu lại dữ liệu mỗi lần `main` có commit mới.
- Collector theo **cách A** (T-058 KP-19): Docker ghi tên service vào từng dòng log, Collector đọc mọi file, lấy `service.name` từ dòng log.
- CPU-BOOK: đo CPU từng container trước khi kết luận; giảm cường độ là ứng viên, chưa chốt quota 0,5.
- Kiểm các span cha rỗng; nếu được thì bổ sung instrumentation. Mục tiêu: dữ liệu dồi dào, đầy đủ nhất cho RCA.
- Tự phản biện B16, tham khảo best practice, tránh nợ kỹ thuật.
- Grafana: hoàn thiện song song, Codex làm, Claude điều phối và kiểm.
- **Chưa merge production. Không push `main`.**

## 1. Luật phải giữ (ngoài AGENTS.md)

1. Không push `main`, không merge PR #17, không chạy `cd.yml`, không chạm máy 84 (`52.64.237.84`).
2. Không sửa `src/m1/` (bản P7 giữ nguyên hash). Bản mới ở `src/m1_ft/`.
3. Không đọc dữ liệu khóa (`data/locked/`), không dùng ô **đánh giá** của T-059.
4. Cách ly nhãn: M1 chỉ nhận `t`; sổ tiêm lỗi và nhật ký điều khiển không vào bộ đọc M1; đáp án chỉ ghép sau khi băm cả đợt.
5. Mật khẩu/token: không in vào file, log, prompt. **Claude không tự nhập mật khẩu vào hệ thống ngoài máy cục bộ** (đăng nhập Keycloak, Grafana, tạo tài khoản) → giao Codex.
6. Mọi thay đổi trên máy ghi vào `results/<task>/ha-tang/thay-doi.md` (lệnh, giờ UTC, hash cấu hình trước/sau). Mỗi máy chỉ một luồng được đổi tại một thời điểm.
7. Giữ mọi lượt, kể cả lượt hỏng. Không sửa `results/` của task đã đóng (T-058, T-059, T-061…): script ghim của T-058 (`stage-m1.py`, `run-m1.py`) dùng qua wrapper, không sửa.
8. Lựa chọn quan trọng phải có mục `docs/WHY.md` **trước khi** dùng trong kết quả (luật cứng 3) — đã được cấp quyền ghi (mục 6).
9. Số trong tài liệu lấy từ file kết quả, có đường dẫn. Câu "mọi/đều" phải có lệnh đếm.
10. Dừng khẩn: nếu tồn tại `D:/RCA-overnight/STOP` thì dừng ở ranh giới bước/chu kỳ, ghi checkpoint.

## 2. Bối cảnh kỹ thuật (đã kiểm, có nguồn)

- **Máy:** `exp-app` Oracle ARM `129.221.208.47` (FlashTicket Compose, Toxiproxy 3 proxy, quota CPU Booking 1.0, Booking đăng ký Eureka cổng 18082); `exp-obs` `213.35.116.128` (Prometheus, Loki, Tempo, Grafana + Infinity; compose `-p flash-ticket-obs-pinned`); máy tải AWS `3.24.8.49` (k6 1.4.2). Khóa và cách gọi: `docs/STATE.md` mục "Lưu ý", `tasks/T-062-dem-chang-1-4/SPEC.md` bảng máy, `results/T-062/chay/runner.py` (hàm `ssh`).
- **Bản đang chạy trên `exp-app`:** nhánh `rca/quan-sat-log` commit `6b21ed55`. Nhánh trên GitHub đã ở `fba6bc8` (merge `main` mới: K3s + bỏ API thống kê event-service) — **chưa** triển khai lên `exp-app`. PR #17 nháp, Auto-fix đang bật (đề xuất tắt — mục 6).
- **Kết quả T-062 (tải đọc, n = 1/ô):** 5/5 ô lỗi có đáp án ở hạng 1 theo cách chấm của `results/T-062/e2.py`; 4/4 ca không tiêm lỗi `CAUSE_FOUND`. Chi tiết: `results/T-062/bao-cao-sang.md`, `chay/thu-gia/LAN-CA-NEN.md`, `viec-cho-duyet.md`.
- **Tải T-062 chỉ đọc** (50/25/15/10 trên fixture) — do SPEC T-062 dòng C1 lấy `deploy/rca-test/workload.js` làm gốc, thu hẹp so với kế hoạch chặng 2 mà không nêu hệ quả (lỗi SL26). Trở ngại thật trên `exp-app`: chưa có VNPay giả (`results/T-058/ban-giao-chay-dem.md:87`), realm 1 tài khoản mua, 3 đơn fixture `CANCELLED`. Chuỗi mua có trong `D:/Project/flash-ticket-platform/deploy/rca-test/fixtures.py::purchase` (POST `/api/v1/orders` → POST `/api/v1/payments` → mở `paymentUrl` VNPay giả → chờ đơn → GET tickets); chưa kiểm trên `exp-app`.
- **Gói ca hiện chỉ xuất 7 truy vấn metric** (CPU/RAM container, p50/p90, lưu lượng, 5xx, dung lượng DB) — `results/T-062/ca/<mã>/cases/<mã>/prometheus.json`. Prometheus `exp-obs` có 545 tên metric: `jvm_*` 14, `db_client_connections_*` 13 (pool), `rabbitmq_*` 5, `redis_*` 29, `mongodb_*` 21, `postgresql_*` 19; **không** có `hikaricp_*`, **không** thấy CPU throttling (4 tên `container_cpu_*` đều là mức dùng). Chưa kiểm `rabbitmq_message_current` có tách queue/ready/unacked.
- **Prometheus chỉ lưu 2 ngày** (`storage.tsdb.retention.time=2d`, đọc 12/11 ~19:00Z; Codex kiểm lại, khớp). B16 §6 yêu cầu metric 14 ngày. Mẫu thô của cửa sổ D2+E1 T-062 (11/11 17:00Z → 12/11 02:30Z) đang được xuất về `results/T-062/ca/_metric-bo-sung/` (lệnh nền phát 12/11 ~19:15Z; kiểm `xuat.rc.txt`, `xuat.stderr.txt`, kích thước file `.jsonl.gz`).
- **Span gốc ca `a5539fba`** (`outputs/a5539fba/method-input.json`, Codex đếm lại khớp): Keycloak 4.012/7.899 span gốc (SELECT `PersistentUserSessionEntity` 2.580; SELECT và DELETE `OutboxEntryEntity` mỗi loại 600). `OutboxDrainerTask` là của Keycloak, code nhóm chỉ đăng ký (`services/keycloak-spi/.../RegistrationEventListenerFactory.java:84`) → muốn có span cha phải bọc **cả lượt chạy**. Span `*_db` gốc ở Spring: ticket 51, payment 45, event 41, booking 32 — chưa rõ nguồn. `parent_missing_in_window` = 10. Job định kỳ là gốc hợp lệ theo B16 §3.
- **Cơ chế 3 ca bình thường bị `CAUSE_FOUND`:** phép chấm E4 (`src/m1/e4.py`, h = phân vị 95 nền + 5% tương đối, không có sàn độ lớn) gắn cờ thao tác nền tần suất cao dịch ~0,1 ms. Phép thử dời mốc: đúng t 3/3, dời +120/+240 s 1/6. Nghi đầu dò bộ chạy lúc t+63 (H1), chưa phân xử với ngẫu nhiên (H3).
- **CPU-BOOK:** cờ lan mọi service (máy 2 lõi). Chưa đo CPU từng container.
- **Đồng hạng (đính chính N2):** M1 **có** gom nhóm hòa (`src/m1/xep_hang.py::_nhom`), bộ chuyển đổi cho cả nhóm cùng hạng `tie_group + 1` (`results/T-061/chuyen-doi.py:245`). Vậy không có chuyện xếp hơn kém theo tên. Nhưng `results/T-062/e2.py` chấm bằng **hạng nhóm** (nhóm 3 thành phần ở hạng 1 thì cả 3 tính hạng 1), còn bộ chấm P7(a) `src/p3/danh_gia.py` dùng **kỳ vọng dưới hoán vị ngẫu nhiên đều trong nhóm hòa** (§8.4). Chiến dịch dùng quy ước P7(a). Việc đầu của T-064: đếm kích thước nhóm hạng 1 ở 5 ca lỗi T-062 xem con số "5/5 hạng 1" có lạc quan không.
- **Grafana bản 6** (`results/T-062/codex/g1-that-2/BAO-CAO.md`): 9/9 ca khớp nguồn; 123 URL bằng chứng giải mã đúng một lần (lỗi mã hóa hai lần **đã sửa**, `giao-dien/dung-dashboard.py:433`); **0 URL Loki** ở bảng bằng chứng; còn điều hướng, lời diễn giải panel rỗng (`REVIEW-G1-5.md` G-2, G-3).
- **B16** (`D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`): đã quy định scheduler trace riêng (dòng 40), `instanceId`/`hostId` (§4), metric pool/queue/restart/OOM (§5). Thiếu đặc tả: bảng thuộc tính span bắt buộc, ghim phiên bản quy ước OTel, tên/đơn vị/histogram/nhịp thu metric, định nghĩa "khỏe" theo route. Triển khai chưa đạt: R-05 một phần, metric pool/queue chưa vào gói, throttling chưa thu, log hạ tầng chưa thu, retention 2 ngày. Chưa xác định cơ chế: SQL gốc Keycloak và `*_db` gốc Spring.
- **Bộ kiểm R (`results/T-062/kiem-du-lieu/bao-cao-B1.md`):** R-01, R-02, R-03, R-06, R-08, R-10 đạt; R-05 một phần; R-07 một phần; R-04 chưa kiểm (0 span PRODUCER/CONSUMER vì tải đọc); R-09 chưa phân xử.

## 3. Tổ chức: một chiến dịch, bốn hồ sơ

| Task | Việc | Người làm | Phản biện | SPEC |
|---|---|---|---|---|
| T-062 phụ lục 2 | Kiểm kê API lõi, VNPay giả, tài khoản thử, kịch bản mua vé | Codex (theo yêu cầu kịch bản Claude soạn) | Claude | `SPEC-PHU-LUC-2.md` (thư mục này) |
| T-063 | Quan sát bổ sung, B16 bản 2, bộ đóng gói, ô dev mới, thu dữ liệu dev bản 2 | Claude | Codex | `tasks/T-063-quan-sat-thu-dev-2/SPEC.md` |
| T-064 | M1-FlashTicket: biến thể H1–H8, chọn ứng viên | Claude | Codex | `tasks/T-064-m1-flashticket/SPEC.md` |
| T-065 | Dashboard Grafana | Codex | Claude | `tasks/T-065-giao-dien-grafana/SPEC.md` |

Luồng song song: L0 điều phối + phương pháp (Claude chính) · L1 tải (Codex) · L2 quan sát/đóng gói (Claude, có thể phiên phụ) · L3 dashboard (Codex) · L4 B16 bản 2 (Claude phụ) · L5 code M1 (Claude). Tối đa 2 phiên Claude phụ và 2 lượt Codex cùng lúc. Codex: `gpt-6.1-sol`, reasoning high, full access; brief ghi ra file rồi truyền qua stdin (`Get-Content brief.md -Raw | codex exec … -`), nhật ký ở `results/<task>/codex/`.

Quyền đổi máy: máy tải = L1; `exp-app` = L1 chỉ phần VNPay giả + tài khoản, xong rồi L2; `exp-obs` phần Collector/Prometheus = L2, phần Grafana = L3.

## 4. Các hướng M1 (T-064) và dữ liệu cần (T-063)

| Hướng | Lý do | Dữ liệu phải có | Ô dev phân xử |
|---|---|---|---|
| H1 DB/cache/broker thành nút; cạnh được xếp hạng | P7 gán span DB cho service, không ra cạnh gốc | tên queue trong span (chưa kiểm) | EVENT-DB-LAT, NET-GW-BOOK, REDIS-BOOK |
| H2 kênh JVM và cgroup | CPU-BOOK lan mọi service | GC, heap, CPU throttling (chưa thu) | CPU-BOOK |
| H3 kênh pool | họ lỗi T-059 | `db_client_connections_*` vào gói | ô dev mới (vd. POOL-EVENT) |
| H4 kênh queue | Saga qua RabbitMQ | ready/unacked theo queue (chưa kiểm) | ô dev mới (consumer chậm) |
| H5 thành phần "chết im" | P7 loại thành phần mất tín hiệu | nguồn sống/chết độc lập | ô dev mới: tạm dừng một service khác Ticket |
| H6 thao tác nền | 3 ca bình thường bị cờ ~0,1 ms | đã có | ca bình thường |
| H7 tải tăng so với sự cố | P7 coi tải tăng là bất thường | đã có | FLASH-HEALTHY + ô mới "tải tăng kèm lỗi" |
| H8 khác | sàn độ lớn E4; adapter lỗi khi container tạo lại; kênh log nghiệp vụ (`outcome`, `reasonCode`) | log nghiệp vụ khi có tải mua vé | theo từng điều chỉnh |

Ô dev mới đặt ở **vị trí khác** các ô đánh giá T-059; danh mục bổ sung ghi ở `results/T-063/o-dev-bo-sung.md` (không sửa T-059). Mỗi hướng phải ghi nút, cạnh, nơi đặt log/trace/metric và phép tính dùng cạnh (luật 18).

## 5. Cách chọn ứng viên

Khóa ở `results/T-064/tieu-chi-chon.md` (hash ghi vào LOG T-064 **trước** khi chấm biến thể đầu tiên). Tóm tắt: hai đại lượng (xếp hạng nút; số ca không tiêm lỗi không trả `NO_INTRINSIC_ANOMALY`, đếm thô), bảng cạnh riêng, quy ước hòa của P7(a), luật giữ hai hướng, đánh đổi → bản thay thế, 9 ca T-062 làm tập không hồi quy. Giữ cố định mục tiêu, cách chấm, phạm vi dữ liệu; **biến thể được mở rộng** trong H1–H8 khi có lý do kỹ thuật, ghi sổ biến thể trước khi chấm.

**Kết thúc tìm kiếm** theo tiêu chí hoàn thành (không theo trần thời gian): (a) mỗi hướng có ít nhất một bản đã cài, kiểm không nhãn, chấm — "không thử được" chỉ dùng khi thật sự không thể, **sau khi** đã tự sửa cấu hình/bộ đóng gói/instrumentation trong quyền; (b) các tổ hợp có căn cứ đã xét (một số thay đổi chỉ có ích khi kết hợp); (c) mỗi ca sai còn lại của bản đề xuất có phân tích cơ chế, hoặc ghi "chưa phân xử" kèm bằng chứng thiếu; (d) có bản đề xuất, bản thay thế (nếu có đánh đổi) và hồ sơ giữ/bỏ. Mốc 5 ngày làm việc của M3 chỉ là **mốc báo tiến độ**.

## 6. Quyền đã cấp (để chạy xuyên suốt)

**Ghi file repo RCA:** `tasks/T-062-dem-chang-1-4/`, `tasks/T-063-…/`, `tasks/T-064-…/`, `tasks/T-065-…/`; `results/T-062/`, `results/T-063/`, `results/T-064/`, `results/T-065/`; `src/m1_ft/`; dòng các task này trong `docs/STATE.md`; `docs/WHY.md` (chỉ **thêm mục mới ở cuối**, đánh số tiếp từ WHY-81, tiêu đề có mã task); `docs/DECISIONS.md` (chỉ **thêm mục theo ngày**, chép nguyên lời Minh). Không sửa dòng có sẵn của hai file đó; không sửa `AGENTS.md`, `LESSONS.md`, `MRP.md`.

**Repo FlashTicket** (`D:/Project/flash-ticket-platform`), chỉ nhánh `rca/quan-sat-log`: instrumentation (span bọc lượt chạy outbox Keycloak, thuộc tính queue, cấu hình agent), `deploy/rca-test/`, `deploy/observability/`, cấu hình log/nhãn. **Không sửa code nghiệp vụ.** Được push nhánh. Được tắt Auto-fix PR #17 (không tự merge `main` về nhánh nữa trong chiến dịch).

**`exp-app`:** build và triển khai từ nhánh; VNPay giả; tài khoản mua thử (Codex tạo); nhãn log Docker (cách A); Collector tại chỗ; bộ tiêm lỗi; dữ liệu thử tạo qua API (không sửa DB trực tiếp).
**`exp-obs`:** cấu hình Collector/Prometheus (thêm metric còn thiếu, **tăng retention**); file dashboard mới trong `pinned/provisioning/dashboards/` (giữ dashboard cũ); thư mục con mới trong `/opt/flash-ticket-obs/rca-ket-qua/`; khởi động lại container Grafana/Prometheus/Collector khi cần; ghi hash `pinned/compose.json` trước/sau nếu đổi.
**Máy tải:** kịch bản k6 mới.

**Hoàn thiện đầu vào cho H1–H8:** được sửa cấu hình, instrumentation, bộ đóng gói và bổ sung tín hiệu trong phạm vi trên mà không hỏi lại.
**Thu dữ liệu:** một đợt thu chính, mỗi ô một lần (ước 14–16 chu kỳ × 30 phút ≈ 7–8 giờ máy, hồ sơ luật 21 trước khi phát). Claude tự quyết xuất bù, thu bổ sung hoặc thu lại khi cần hoàn thiện đầu vào H1–H8 hoặc khắc phục phần thu sai. Rà khả năng dùng lại trước, ghi lý do, phạm vi ảnh hưởng và chi phí, giữ các lượt cũ. Can thiệp chưa xác nhận thì sửa cơ chế tiêm hoặc đầu dò trong quyền rồi kiểm lại. Thu lại theo ô bị ảnh hưởng, toàn đợt chỉ khi có bằng chứng ảnh hưởng toàn đợt. Ca vào tập chọn khai trước khi chấm, việc chạy lặp để sau. Quyền này đã được Minh duyệt bổ sung, không còn chờ xác nhận buổi sáng.

**Tự quyết chi tiết kỹ thuật** không đổi mục tiêu (tên metric, tỷ lệ hành trình tải khởi điểm 70/20/5/5, khoảng 20 tài khoản thử, tên ô dev mới): ghi lý do vào LOG; lựa chọn quan trọng thì thêm mục WHY.
**Lựa chọn ứng viên và revision:** Claude áp dụng `results/T-064/tieu-chi-chon.md`, tự chọn biến thể, tổ hợp và ứng viên theo tiêu chí đã trình. Kiểm luồng lõi rồi tự chọn revision phù hợp trong nhánh `rca/quan-sat-log`, ghi WHY, commit, image và cấu hình thực triển khai trước khi đóng băng. Bốn mục này không cần xin xác nhận lại.
**Lưu tiến độ repo RCA:** tiếp tục lưu code, cấu hình, kết quả và manifest. Commit/push repo RCA trình sau, việc chưa commit không chặn chiến dịch.

**Quyền điều phối:** Claude tự giao việc, tiếp nhận lại khi hồi hạn mức, tổ chức kiểm/phản biện theo phân vai T-062 phụ lục 2/T-063/T-064/T-065 và triển khai sửa trong gói được duyệt. Minh đã cấp quyền chạy xuyên suốt, không chờ duyệt lại các thao tác trong gói hoặc chờ chuyển prompt thủ công giữa các phiên. Phản biện vẫn giữ độc lập theo vai trò và bằng chứng.

**Dừng và hỏi Minh khi:** cần sửa code nghiệp vụ; cần đổi tiêu chí chọn sau khi đã xem kết quả; một hướng cần ô đánh giá hoặc dữ liệu khóa; việc vượt phạm vi máy/file trên. **Không dừng** vì chậm tiến độ: báo chênh lệch trong checkpoint và làm tiếp. Lỗi dữ liệu: xác định phạm vi ảnh hưởng, cách ly phần hỏng, làm tiếp phần không phụ thuộc (luật 21).

## 7. Mốc

| Mốc | Xong khi |
|---|---|
| M0 | SPEC bốn hồ sơ, tiêu chí khóa, checkpoint, cơ chế tự tiếp nhận và gọi lại Codex đã kiểm |
| M1 Nền sẵn sàng | API đã kiểm kê; tải mua vé chạy 2 lượt cho lưu lượng gateway giống nhau; bộ kiểm R chạy lại trên tải mới (R-04, R-09, R-05, R-07); quan sát bổ sung đã triển khai; bộ đóng gói mở rộng + đường phục hồi; lịch đầu dò chốt; B16 bản 2 nháp; Grafana G-a xong |
| M2 Đóng băng và thu | chốt commit/image/kịch bản tải/cấu hình Collector; xác nhận can thiệp từng ô; thu qua đêm; băm cả đợt |
| M3 Biến thể | H1–H8 đạt tiêu chí kết thúc ở mục 5; Grafana G-b xong |
| M4 Bàn giao | bản M1-FT đề xuất, code, cấu hình, kết quả từng ca, hồ sơ giữ/bỏ, dashboard nối bản mới (G-c), phản biện, dòng WHY/DECISIONS, đề xuất commit |

Điều phối theo đầu vào từng phần, các mốc là nơi tổng hợp kết quả. M0 chưa xong không chặn việc độc lập đã cấp quyền. Phân tích dữ liệu cũ, điều phối, retention, thiết kế đóng gói, M1 nền và Grafana P7 có thể làm song song.

| Nhánh | Có thể bắt đầu | Đầu vào cần trước khi kết luận |
|---|---|---|
| T-062 phụ lục 2 | Codex sẵn sàng, kiểm API và mock/tài khoản | Hành trình mua trọn và tải được kiểm trên cấu hình cuối chịu ảnh hưởng |
| T-063 | Phân tích, retention, B16, thiết kế thu/đóng gói | R-04/R-09 cần giao dịch thật, vòng kiểm → sửa thiếu hụt → kiểm lại |
| T-064 | P7 tương đương, thiết kế/cài theo đầu vào từng hướng | Dữ liệu tương ứng đã kiểm, đủ tập ca của phép so trước khi giữ/bỏ hoặc chọn cuối |
| T-065 | G-a/G-b trên P7, hợp đồng đầu ra với T-064 | G-c thử từ đầu ra phù hợp đầu tiên, kiểm cuối trên ứng viên M1-FT |

Trước khi phát lượt thu chính, xác nhận đồng thời tải, quan sát H1–H8, bộ đóng gói, phục hồi và lịch đầu dò trên cấu hình cuối. Ghim revision/image/workload/cấu hình → xác nhận can thiệp → thu → băm. Phối hợp từng thay đổi máy, kiểm tích hợp lại phần chịu ảnh hưởng sau restart hoặc tạo lại container. Tải chạy được và quan sát được sửa xong từng phần chưa tự chứng minh bản tích hợp cuối đã đúng.

Sau báo cáo sáng hoặc báo cáo mốc, tiếp tục bước có đủ đầu vào. Một nhánh bị chặn chỉ làm chờ phần phụ thuộc, các nhánh độc lập tiếp tục. Không ấn định trước phần tối đa làm được trong một đêm.

## 8. Hết lượt dùng và tự tiếp nhận

- Mốc lịch sử do Minh báo cho ngày 13/11 là Claude ~04:00 và Codex ~04:45 giờ VN. Mỗi lần tiếp nhận lấy giờ hiện tại và thông báo hạn mức thực tế để quyết định gọi tiếp, không dùng các giờ cũ cho những ngày sau.
- Mọi phiên cập nhật `CHECKPOINT-CHIEN-DICH.md` sau mỗi bước và ít nhất 30 phút một lần (dòng nhịp tim UTC, bước đang làm, việc tiếp, lệnh nền đang chạy).
- Lịch tự tiếp nhận `m1ft-tiep-nhan`: đọc checkpoint, kiểm phiên điều phối và tiến trình con đang chạy trước khi ghi nhịp tim hoặc nhận quyền. Nhịp tim cũ hơn 45 phút là dấu hiệu cần kiểm, chưa đủ để phát trùng công việc. Nếu chủ cũ còn hoạt động thì không tiếp quản song song. Lịch chỉ được báo đã sẵn sàng sau khi kiểm được trạng thái bật và lần kích hoạt. Trạng thái tạo lịch xem checkpoint, tôn trọng kết quả từ chối của công cụ.
- Gọi lại Codex khi hồi hạn mức là **đầu ra phải kiểm** của M0 (`results/T-063/dieu-phoi/`): script gọi, cách nhận biết hết hạn mức, tiến trình chờ, một lần thử "hết hạn → chờ → gọi lại". Lần trước tiến trình chờ chết khi ứng dụng khởi động lại (mã 4) — phương án cần kiểm: Windows Task Scheduler (tách khỏi ứng dụng) hoặc để lịch `m1ft-tiep-nhan` gọi lại theo checkpoint.

## 9. Báo cáo và tiếp tục nhiều ngày

Ghi báo cáo sáng khoảng 07:00 giờ VN theo ngày thực tế và báo cáo từng mốc. Nếu phiên nhận việc sau mốc cũ, ghi trạng thái hiện tại rồi làm tiếp. Báo cáo gồm đầu ra có bằng chứng, kiểm đã chạy, việc đang chạy, phần bị chặn và bước tiếp theo. Đến giờ báo cáo, hết một phiên hoặc chậm hơn dự toán đều không kết thúc chiến dịch.

Bốn điểm từng chờ xác nhận buổi sáng đã được xử lý tại mục 6 theo duyệt bổ sung 13/11. Claude tự quyết thu bổ sung/thu lại và revision trong quyền, áp dụng tiêu chí chọn đã trình, lưu tiến độ bằng manifest và trình commit sau. Chỉ hỏi lại đúng phần vượt phạm vi được cấp. Tiếp tục đến khi M4 đạt tiêu chí bằng chứng, ghi bàn giao và trạng thái lịch tiếp nhận tương ứng.
