# B1 — Kiểm chất lượng dữ liệu R-01–R-10 (chặng 1a), T-062

> **Bản 2 (12/11/2026), sửa theo R2 của `tasks/T-062-dem-chang-1-4/REVIEW.md`, Minh duyệt.** Bản 1 báo R-05 ĐẠT khi chỉ kiểm có `host.id` (rộng hơn điều đã kiểm). Bộ kiểm bản 2 tách (a) hiện diện host, (b) định danh instance log↔trace, (c) metric. Lần chạy đầu bản 2 báo thiếu host ở 32 chuỗi metric gộp `sum by(service_name)` — phép gộp của adapter bỏ nhãn theo thiết kế, nên (a) phần metric chỉ xét kênh gốc; sửa thêm này làm **sau** khi thấy kết quả. Bản 1 giữ ở `results/T-062/_ban-1/kiem-du-lieu/`.

Bộ kiểm: `kiem-r.py` (đọc gói ca đã đóng băng — cùng dữ liệu M1 đọc; ngưỡng ghi trong mã, khai trước khi chạy). Yêu cầu gốc: `results/T-040/yeu-cau-quan-sat-p9.md`.

So hai gói **ca bình thường** cùng độ dài (t±600 s):
- **Trước** — T-058 `c12e47ab` (bản FlashTicket cũ + agent gắn ngoài): `r-T058-c12e47ab.json`
- **Sau** — T-062 `a5539fba` (nhánh `rca/quan-sat-log` `6b21ed55`, 5 req/s, chu kỳ E1 đầu): `r-a5539fba.json`

| R | Nội dung | T-058 | T-062 | Số đo T-062 (con trỏ JSON `#/R/<R>/so_do`) |
|---|---|---|---|---|
| R-01 | Kiểu span, đích lời gọi | ĐẠT | **ĐẠT** | 76.383 CLIENT đều có `server.address`; cặp CLIENT→SERVER khác service: gateway→event 3.000, gateway→booking 1.500, … |
| R-02 | Tên thao tác ổn định | ĐẠT | **ĐẠT** | 12.760/12.760 SERVER có `http.route`; 0 tên span chứa UUID. Bảng ánh xạ B13→span: chưa kiểm (ngoài dữ liệu) |
| R-03 | Cạnh dữ liệu có DB logic + instance | ĐẠT | **ĐẠT** | 69.647 span DB; Event→`event_db` qua `127.0.0.1:15433` (proxy, đúng topology D1). Bảng DB logic→instance theo thời gian: chưa kiểm |
| R-04 | Địa chỉ thông điệp | chưa kiểm | **chưa kiểm** | 0 span PRODUCER/CONSUMER: hỗn hợp tải chỉ đọc, không sinh message |
| R-05 | host/instance trên 3 tín hiệu | **THIẾU** (instance trong thân log user/event không có trong trace) | **ĐẠT** (bộ kiểm bản 2) | (a) host có ở resource trace, resource log và metric gốc; (b) `instanceId` trong thân log B16 của 3 service có log trong cửa sổ (gateway, payment, ticket) đều thuộc `service.instance.id` của trace; (c) các kênh metric M1 dùng **không có** nhãn instance (không kiểm được phần này). **Còn lệch:** resource log mang ID tĩnh `<svc>-1` do Collector gắn (`#/R/R-05/so_do/KHONG_KHOP_RESOURCE_LOG`). Bảng service→instance→host theo thời gian: chưa kiểm |
| R-06 | Log nối span | **THIẾU** (16 dòng B16, 0 có traceId) | **ĐẠT** | 7.500 dòng B16, 7.500 có traceId/spanId, 7.500 nối được span có trong export (gateway 6.000, payment 900, ticket 600) |
| R-07 | Manifest lượt, mốc độc lập | chưa kiểm | **một phần** | có: commit/image (`ha-tang/A2-lan2-build-manifest.json`), agent 2.33.1 (Dockerfile), sampling `parentbased_always_on` (env), đồng hồ (`tai/may-tai.md`), lịch tải (`tai/out/<tag>/`), mốc tiêm + đầu dò độc lập (`tiem-loi/so.jsonl`). Chưa có: onset/hồi phục tính từ tín hiệu độc lập cho từng ca |
| R-08 | Lấy mẫu, drop | chưa kiểm (không có log gateway) | **ĐẠT** | 6.000 request gateway (log B16) đều có span SERVER gateway cùng trace. Drop của agent: chưa kiểm. Collector: có drop lúc đọc bù log 19:16–20:38Z (trước E1, `ha-tang/thay-doi.md`) |
| R-09 | Ranh giới trace mới | chưa kiểm | **chưa phân xử** | 15 span CLIENT của Booking có parent vắng trong export (có thể do cha ngoài cửa sổ hoặc scheduler); chưa phân loại (a)(b)(c) |
| R-10 | Nối nguồn tĩnh với runtime | THIẾU (5 commit khác nhau) | **ĐẠT** | 7 service ứng dụng cùng `service.version` = `6b21ed55…`; Keycloak giữ image cũ `776d9c9e` (không thuộc nhánh) |

## Kết luận và phần còn mở

- Đạt mục tiêu chặng 1a ở các yêu cầu đo được trên tải đọc: log nối span (R-06) và log mọi request gateway (R-08) — hai điểm thiếu lớn nhất của T-058 — đã đạt trên dữ liệu thật.
- Chưa kiểm được R-04, R-09 do hỗn hợp tải chỉ đọc (không có message, callback, scheduler có tải). Cần kịch bản đặt vé/thanh toán (chặng 2 §5 nói tải bắt buộc có đăng nhập và đặt vé — **chưa có**, C1 chỉ làm tải đọc theo brief).
- Lỗi vận hành phát hiện nhờ bộ kiểm: Collector exp-app ghim log theo ID container (KP-19) → sửa 20:38Z. Đề xuất (chờ Minh): đổi filelog sang glob/nhãn container để recreate không làm mất log.
- Bộ kiểm chạy trên một gói; muốn chạy định kỳ (Codex trông) thì gọi sau mỗi ca: `py -3 -B results/T-062/kiem-du-lieu/kiem-r.py results/T-062/ca/<mã>/cases/<mã> --ra results/T-062/kiem-du-lieu/r-<mã>.json`.
