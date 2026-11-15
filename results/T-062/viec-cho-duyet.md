# T-062 — Việc chưa làm và việc chờ Minh duyệt để chuẩn bị chặng 4 (12/11/2026)

Phân loại lý do: **[QUYẾT]** cần Minh quyết (agent không được tự chọn: đổi hướng, đổi chuẩn, production, code nghiệp vụ); **[THIẾU]** chưa đủ dữ liệu/thông tin, phải có bước trước; **[CHƯA LÀM]** agent làm được ngay, chỉ chưa làm (cần Minh duyệt theo Luật 0 vì là việc mới/ngoài phạm vi đã duyệt).

## A. Ảnh hưởng trực tiếp tới tính đúng của chặng 4 (làm trước)

| # | Việc | Loại | Vì sao chưa xong | Đề xuất của Claude |
|---|---|---|---|---|
| A1 | **Nguyên nhân CAUSE_FOUND ở ca không tiêm lỗi** (`chay/thu-gia/LAN-CA-NEN.md`) | [CHƯA LÀM] phần cuối | Đã tìm được cơ chế (E4 gắn cờ độ dịch rất nhỏ của thao tác nền tần suất cao) và mẫu placebo (đúng mốc t: 3/3; dời mốc: 1/6) nghiêng về **đầu dò của bộ chạy lúc t+63**; chưa phân xử H1/H3 vì cần tính lại thời gian độc quyền bằng code M1 | Duyệt làm ngay: tính E1 theo 10 s trên `method-input.json` đã lưu + thêm placebo (0 giờ máy, ~1–2 giờ). Lượt sau đặt đầu dò đối xứng/ngoài cửa sổ |
| A2 | **Ngưỡng sức khỏe** cho ca bình thường và FLASH (T-059 OPEN) | [QUYẾT] + [THIẾU] | Không có ngưỡng thì không có "ca khỏe", không đo được K' | Đề xuất: khỏe khi (i) không restart/OOM; (ii) 5xx = 0 ngoài lỗi nền đã khai; (iii) 429 = 0 (FLASH: 429 > 0 → nhóm "giới hạn ở Gateway"); (iv) p95 mỗi route ≤ nền +20 %; (v) không dropped iterations. Đo bằng k6 + Prometheus, ngoài dữ liệu RCA |
| A3 | **Lỗi nền route tickets 500** (GlobalExceptionHandler đứng trước TicketApiExceptionHandler) | [QUYẾT] | Sửa code nghiệp vụ FlashTicket cần Minh duyệt (Luật 0, GOV-154) | Sửa tối thiểu `@Order(HIGHEST_PRECEDENCE)` trên nhánh `rca/quan-sat-log` (route sẽ trả 404, vẫn không 2xx vì đơn fixture chưa phát vé) — hoặc giữ và khai là lỗi nền trong định nghĩa khỏe. Claude nghiêng về sửa: lỗi nền 10 % request làm nhiễu kênh error |
| A4 | **CPU-BOOK không cô lập** (cờ lan mọi service) | [CHƯA LÀM] | Phát hiện khi lần ca nền; D2 chỉ kiểm cgroup Booking | Giảm cường độ (1 luồng, quota 0,5) và thêm đầu dò CPU các cgroup khác vào D2; chạy lại D2 riêng ô này (~10 phút) |
| A5 | **REDIS-BOOK** không xác nhận được | [QUYẾT] | Hỗn hợp tải chuẩn (Minh duyệt 50/25/15/10) không có GET availability | Thêm 5 % GET availability (giảm event 50→45) cho mọi lượt từ chặng 4 — đổi chuẩn tải nên mọi so sánh với T-062 phải ghi rõ; hoặc bỏ ô khỏi dev |
| A6 | **Tiêu chí chọn chặng 4** (`spec-chang-4-de-xuat.md` bản 3) | [QUYẾT] | Đề xuất, chưa duyệt; còn ngưỡng và ưu tiên X/K' | Duyệt luật hai hướng + K' + X-cạnh như bản 3; ưu tiên X khi đánh đổi |
| A7 | **Baseline bắt buộc** | [QUYẾT] + [CHƯA LÀM] | Chọn baseline là quyết định nghiên cứu; adapter FlashTicket cho baseline chưa viết | BARO (metric), MicroRank hoặc TraceRCA (trace), Nezha (đa nguồn); viết adapter đọc gói ca T-062 (chưa ước lượng, khoảng 1 ngày người) |
| A8 | **Đường phục hồi M1 giữa lượt** (R5) | [CHƯA LÀM] | Lượt T-062 không cần dùng; là điều kiện của lượt dài sau | Wrapper tiếp nhận: stage lại cùng t với mã mới, giữ attempt cũ; kiểm đúng tình huống thư mục đã có |
| A9 | **Mốc S lệch 20 s / đầu dò trong cửa sổ** (R8, A1) | đã sửa một phần | `runner.py` đã lấy S từ lúc k6 chạy (bản 3); lịch đầu dò chưa đổi | Gộp với A1 khi sửa bộ chạy |

## B. Dữ liệu còn thiếu cho các ô và yêu cầu quan sát

| # | Việc | Loại | Vì sao | Đề xuất |
|---|---|---|---|---|
| B1 | **Tải có đặt vé/thanh toán** (chặng 2 §5) | [QUYẾT] + [THIẾU] | C1 chỉ được giao tải đọc; realm có 1 tài khoản người mua; mua vé tạo dữ liệu thật trong DB thử | Duyệt kịch bản giao dịch (đặt vé → mock VNPay IPN → phát vé) với N tài khoản thử; cần cho R-04, R-09, ô Saga/queue/pool (đánh giá) và C4-c/d/e |
| B2 | R-04, R-09 của B1 | [THIẾU] | Không có message/callback trong tải đọc | Sau B1 |
| B3 | R-05 binding manifest, R-07 onset/hồi phục độc lập | [CHƯA LÀM] | Bộ kiểm chưa đối chiếu manifest triển khai | Mở rộng `kiem-r.py` |
| B4 | Collector ghim log theo ID container (KP-19) | [QUYẾT] | Đổi cấu hình máy | Đổi filelog sang glob + nhãn container để recreate không mất log |
| B5 | Ô dev cho pool/queue/chết im (C4-c/d/e) | [QUYẾT] | T-059 chỉ có ô đánh giá cho các họ này | Thêm POOL-EVENT (dev) hoặc để C4-c/d/e ngoài chặng 4 |
| B6 | Phương sai giữa lặp | [THIẾU] | Mỗi ô mới 1 lặp | Lặp ×3 ở chặng 4 |

## C. Hồ sơ, sản phẩm, vận hành

| # | Việc | Loại | Đề xuất |
|---|---|---|---|
| C1 | PR FlashTicket #17: merge hay giữ nhánh | [QUYẾT] (production) | Giữ nhánh tới khi xong A3 và dọn secret `ENV_*`; merge cùng đợt nhóm hệ thống làm CD ARM |
| C2 | Commit repo RCA | [QUYẾT] | Commit mã, báo cáo, sổ, `ket-qua/`; để ngoài git `ca/` (1,6 GB) và `tai/out/` (347 MB), giữ hash trong manifest |
| C3 | Ghi DECISIONS: hướng tiêm lỗi (BOI-CANH), đính chính T-059 2i-B/2i-D, cường độ EVENT-DB-LAT 30 ms, bỏ REDIS-BOOK khỏi E1 T-062 | [QUYẾT] | Claude soạn dòng ghi để Minh duyệt |
| C4 | Phản biện chính thức T-062 | [QUYẾT] | Ghi Codex là người phản biện (đã 2 lượt); một lượt kiểm lại bản 3 (REVIEW-3) |
| C5 | Giao diện G1: liên kết Loki ở bảng bằng chứng, mục ① mở tab mới, lớp thao tác từ M1, tô vùng nghi ngờ, ô LLM (G4) | [QUYẾT] ưu tiên | Hai lỗi nhỏ sửa ngay ở phiên G1; phần còn lại sau chặng 4 |
| C6 | Trạng thái máy: iptables 8081 (không bền), Toxiproxy + quota Booking vẫn bật trên exp-app | [QUYẾT] | Giữ nguyên để chặng 4 dùng cùng topology; ghi rõ trong SPEC chặng 4 |
| C7 | Lịch tự tiếp nhận `t062-tiep-nhan` | — | Không tồn tại trên tài khoản mới; không cần |
