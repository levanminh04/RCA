# Vì sao M1 kết luận CAUSE_FOUND ở 4 ca không tiêm lỗi (T-062, khám phá — không phải kết quả chính)

Ngày 12/11/2026, Claude. Chỉ dùng dữ liệu đã đóng băng và M1 bản khóa P7 (không chỉnh). Đáp án đã ghép sau khi băm cả đợt.

## 1. Quan sát (có đường dẫn)

**Ca FLASH `00eaea92` — có lời giải thích hợp lý.** Cờ nằm ở kênh `workload` của gateway, booking, event, payment, ticket (rA 0,9–1,0, rN 0) và `error` của ticket/gateway — tải tăng thật 5→15 req/s và lỗi nền tickets 500 tăng theo tải (`ca/00eaea92/outputs/00eaea92/method-output-1.json#/extra/kenh_co`; `chay/k6-theo-pha.md`). M1 không có khái niệm "tải tăng khỏe": nó coi tải tăng là bất thường tự sinh. Đây là hành vi đúng thiết kế của M1, không phải lỗi; câu hỏi ca này đặt ra là *có muốn* M1 phân biệt tải tăng hợp lệ hay không (T-059 FLASH-HEALTHY).

**Ba ca bình thường — cờ nằm ở thao tác nền chạy định kỳ, độ dịch rất nhỏ.**

| Ca | Thành phần tầng 1 | Thao tác (kênh `op`) | n mỗi cửa sổ | tỷ lệ vượt ngưỡng nền → sự cố |
|---|---|---|---|---|
| `a5539fba` | keycloak | DELETE OutboxEntryEntity; SELECT PersistentUserSessionEntity | 300; ~1.290 | 0,04 → 0,45; 0,038 → 0,053 |
| `6c1a9fd8` | event-service, user-service | OutboxWorker.relay; find organizer_applications | 300; 20 | 0,027 → 0,10; 0 → 0,30 |
| `e8661e0a` | event-service, ticket-service | SELECT event_sectors / outbox_messages; TicketJobs.cancel | 750/300; 300 | 0,045 → 0,077; 0,037 → 0,083; 0,047 → 0,167 |

Số lần chạy ở hai cửa sổ bằng nhau; trung vị tổng thời lượng gần như không đổi (vd. 0,28 → 0,37 ms; `chay/lan-ca-nen.json`). Không cờ nào nằm trên route k6 gọi.

**Phép thử giả (placebo)** — dời mốc t trong cùng chu kỳ ổn định (`chay/thu-gia/ket-qua.jsonl`, mã `gia*` trên exp-obs):

| Mốc | Ca có CAUSE_FOUND |
|---|---|
| t khai báo (S+600) | 3/3 |
| t + 120 s | 0/3 (`NO_INTRINSIC_ANOMALY`) |
| t + 240 s | 1/3 |

## 2. Suy luận và ứng viên (chưa kiểm)

- **Cơ chế chung (có căn cứ từ trung gian):** phép chấm phân vị E4 (`src/m1/e4.py::nguong`, `cham_phan_vi`) đặt ngưỡng h = phân vị 95 nền + 5% (ε tương đối), không có ngưỡng độ lớn tuyệt đối; với n vài trăm mẫu, một độ dịch nhỏ của thao tác dưới 1 ms vẫn có p rất nhỏ → một thao tác → thành phần lên tầng 1 → `CAUSE_FOUND`. Đặc điểm này đã có trong bản P7; FlashTicket có nhiều thao tác nền tần suất cao (outbox poller mỗi giây) nên dễ chạm hơn dữ liệu công khai. **Chưa kiểm** lời giải thích này đủ cho cả 3 ca.
- **Vì sao đúng mốc t lại hay có cờ (placebo 3/3 so với 1/6):** ứng viên
  - (H1) **đầu dò của bộ chạy** (`inj.py probe` lúc t+63: `docker exec` vào Booking, đọc cgroup, socket tới Postgres/Redis, health Booking) gây nhiễu nhẹ trên máy 2 lõi dùng chung. Lịch đầu dò khớp mẫu placebo (cửa sổ sự cố chứa đầu dò t+63 → 3/3; dời +120 đưa đầu dò vào cửa sổ nền → 0/3; +240 cửa sổ sự cố chứa đầu dò t+483 → 1/3).
  - (H2) làm mới token k6 (mỗi 200 s): **không khớp** mẫu (+120 có nhiều lần làm mới trong cửa sổ sự cố hơn mà không có cờ).
  - (H3) ngẫu nhiên: 3/3 so với 1/6 trên n nhỏ chưa loại được.
- **Phép kiểm trực tiếp H1 chưa phân xử:** đếm span vượt ngưỡng theo thời gian dùng *tổng* thời lượng, còn M1 dùng *thời gian độc quyền* (E1) — sai đại lượng, không dùng làm bằng chứng (`chay/thu-gia/vuot-nguong-theo-thoi-gian.json` giữ lại). Một thao tác (organizer_applications, 20 mẫu) có vượt ngưỡng rải khắp cửa sổ sự cố, không dồn ở t+63 — nghiêng về H3 cho thao tác đó.

## 3. Bằng chứng còn thiếu và cách lấy (rẻ, dữ liệu đã có)

1. Tính lại thời gian độc quyền E1 theo từng 10 s cho các thao tác bị cờ bằng chính code M1 (`chuoi`/`span`) trên `method-input.json` đã lưu → xem vượt ngưỡng có dồn quanh t+63 (H1) hay rải đều (H3). ~1 giờ người, 0 giờ máy.
2. Placebo thêm các mốc khác (−120 s nếu không chạm khoảng nghỉ tải; nhiều mốc trong ca bình thường) để ước lượng tỷ lệ CAUSE_FOUND ở mốc ngẫu nhiên. Vài phút máy.
3. Thiết kế lượt sau: đầu dò của bộ chạy **ngoài** cửa sổ phương pháp hoặc cùng lịch ở cả nền và sự cố (đối xứng) — tách được H1 mà không cần phân tích lại.

Kết luận phụ thuộc: chưa được dùng "M1 báo động giả ở ca khỏe" làm căn cứ chọn thành phần chặng 4 trước khi tách H1/H3 và có ca khỏe đạt ngưỡng.

## 4. Phát hiện kèm theo: CPU-BOOK không cô lập

Ca `bf17acbf` (CPU-BOOK): cờ lan ra mọi service (gateway, event, payment, ticket, keycloak — latency, thao tác DB). Hai vòng lặp đốt CPU trong Booking (quota 1 CPU) chiếm trọn 1/2 lõi của máy dùng chung → các service khác chậm theo. Can thiệp **không** đạt điều kiện "cgroup khác không bị stress trực tiếp" của T-059 ở mức hệ thống (D2 chỉ kiểm cgroup Booking). Đáp án vẫn hạng 1, nhưng ô này chưa đo đúng câu hỏi "định vị CPU trong một service". Đề xuất: giảm cường độ (1 luồng, quota 0,5) hoặc thêm đầu dò CPU các cgroup khác ở D2.
