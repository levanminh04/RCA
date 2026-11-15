# Bối cảnh cho phiên tiếp quản T-062 (ghi 12/11/2026, trước khi Minh đổi tài khoản Claude)

Phiên Claude gốc (11–12/11) không truy cập được từ tài khoản mới. File này gom những gì đã bàn trong chat mà repo chưa ghi đủ. Nguồn chính thức vẫn là AGENTS.md, docs/STATE.md, docs/DECISIONS.md và LOG từng task.

## Cách làm việc với Minh

- Tiếng Việt, câu ngắn, dễ hiểu; trả lời thẳng câu hỏi trước, rồi đề xuất kèm lý do.
- Không đoán ý; Minh duyệt thì làm luôn, không trình lại. Minh đã cho phép chạy liên tục T-062 (xem SPEC).
- Minh muốn thấy kết quả trực quan, dùng được; ghét nhãn khó hiểu (ví dụ "không cờ" bị chê vô nghĩa).

## Đã xong hôm nay (đã ghi sổ)

- T-061 (định dạng kết quả RCA 0.2, Infinity) nghiệm thu; T-059 (danh mục lỗi) nghiệm thu; T-058 khép (chưa phản biện). DECISIONS mục ngày 11/11 đã ghi.
- Infinity 4.1.6 đã cài trên Grafana `exp-obs`, nguồn `infinity-rca`, dữ liệu `/opt/flash-ticket-obs/rca-ket-qua/`; Minh đã thấy dashboard "T-061 thử Infinity" chạy (`results/T-061/exp-obs/README.md`).
- Nguồn dữ liệu G2: Infinity + file chỉ mục danh sách sự cố; chấm điểm luôn bằng script trên file đã băm, không trong Grafana.

## Repo FlashTicket `D:/Project/flash-ticket-platform` (chưa commit, nhánh `main` cục bộ)

- Hơn 100 file sửa/mới do Codex làm trước đó: chuẩn log B16 (LogFields, BusinessTelemetry, SafeStackTracePrinter…), Dockerfile nhúng OTel agent, workflow CI/CD build ARM (mục a), compose, khởi tạo PostgreSQL, `deploy/rca-test/` (Toxiproxy, netem, CPU, mock VNPay, faultctl, k6), `deploy/observability/`. Không chỉ là log.
- Claude đã (12/11, Minh cho sửa thẳng): gỡ hook tiêm lỗi khỏi code nghiệp vụ. `OrderController`, `EventController` trả về bản gốc; `TicketService` bỏ hook, giữ log nghiệp vụ. Hook Booking/Event chuyển sang `services/<svc>/src/rca-test/` (`RcaFaults.java` + `RcaFaultsWebConfig.java` = bộ chặn HTTP theo route sau xác thực, trước controller; route khai ở `src/rca-test/resources/application-rca-test.yaml`), chỉ build khi `./mvnw clean -P rca-test`. Build thường không chứa (đã mở jar kiểm). Ticket bỏ hẳn hook. `faultctl.py` bỏ `ticket.fail`.
- Đã kiểm: 7 service `mvnw clean verify -DskipTests` đạt; booking/event `-P rca-test` test hook đạt (8 và 7 test). Test đầy đủ cần DB/MQ, chưa chạy (để CI trên PR).
- Sao lưu trước khi sửa: `D:/RCA-ext/backup-flashticket-20261112/`.
- **`cd.yml` triển khai production (máy 84) khi push `main`. `ci.yml` chạy trên PR vào `main`.** Chỉ dùng nhánh `rca/quan-sat-log` + PR.

## Quyết định về cách tiêm lỗi (Minh đồng ý hướng, chưa ghi DECISIONS)

- Lỗi hạ tầng: công cụ ngoài ứng dụng (Toxiproxy, Pumba, docker pause). Trễ mạng giữa hai service: thử Toxiproxy giữa hai service thay netem (host network).
- Lỗi nghiệp vụ (Saga phát vé FAILED): dữ liệu thật gây thất bại; `TicketService` đã có nhánh FAILED tự nhiên `EVENT_CANCELLED`. Ô này chỉ thuộc đợt đánh giá; làm trước chặng 6.
- Lỗi trong code (5xx, chậm, giữ pool): module riêng `src/rca-test` như trên, bật/tắt real time qua file điều khiển (`faultctl`, lease ≤ 300 s).
- Đính chính T-059 (`yeu-cau-code-nhom.md` 2i-B, 2i-D theo cách tiêm mới) **chờ Minh duyệt**.
- Danh mục D.9 không có kịch bản lỗi cho user-service (thiếu sót, chưa xử lý).

## Lớp thao tác và LLM (đã bàn)

- Hướng 1 (hiển thị thao tác, cạnh cha–con quan sát được, trạng thái/cờ M1, `e` chỉ trong chi tiết, kích thước nút cố định, panel thao tác theo service đã chọn) — Minh đồng ý làm trước; SPEC phần D (gồm D2 áp đúng tiền xử lý `chuoi.py`: cắt cửa sổ, `he_span`, alias) chưa ghi.
- Hướng 2 (M1 xếp hạng thao tác) là ứng viên; LLM được gợi ý thao tác bên trong service mà không đổi hạng service (hợp P8).
- Nhãn nút đề xuất: đỏ "#hạng / nghi là nguồn", cam "#hạng / bị kéo theo", xám "(trống) / bình thường", tím "? / thiếu dữ liệu"; mã lớp M1 chỉ trong chi tiết. Menu chi tiết nên có liên kết Explore Tempo/Loki/Prometheus.

## Mẹo kỹ thuật đã gặp

- Gọi Codex từ PowerShell: ghi brief ra file và truyền qua stdin (`Get-Content brief.md -Raw | codex exec … -`); truyền chuỗi trực tiếp bị tách thành nhiều tham số.
- Python trên laptop: `py -3 -B`; script dùng `-I` thì stdout cp1252 làm hỏng tiếng Việt → in qua `sys.stdout.reconfigure(encoding='utf-8')`.
- M1 cần môi trường ghim: `D:/RCA-ext/envs/py312-pin/Scripts/python.exe` với `PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages`.
- Grafana trong container: sửa file provisioning gắn bind mount phải `docker restart` mới nạp; Node graph cần 10–20 s tính bố cục.
- `docker compose` trên `exp-obs` phải có `-p flash-ticket-obs-pinned`.
- Lịch tự tiếp nhận (scheduled task) bị bộ phân loại an toàn của ứng dụng chặn khi Claude tự tạo; Minh tạo tay nếu muốn.
- Docker Desktop trên laptop đã tắt; không cần cho T-062.

## Việc tay của Minh (12/11, trước khi ngủ)

- `gh auth login`: **xong** (tài khoản `levanminh04`).
- Mở cổng Oracle cho `3.24.8.49/32` TCP 8081, 8080: Minh đang điền form (cần bấm "Add Ingress Rules").
- Chưa rõ: boot volume backup, chặn bypass `main`, lịch tự tiếp nhận.
