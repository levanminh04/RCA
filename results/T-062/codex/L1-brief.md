# Brief L1 cho Codex — T-062 phụ lục 2: tải có đăng nhập, đặt vé, thanh toán (12/11/2026 21:30Z)

Bạn là Codex (`gpt-6.1-sol`, reasoning high, full access), **người làm** phụ lục 2 của T-062 trong repo `D:\RCA-flashticket`. Phiên Claude điều phối chiến dịch M1-FlashTicket giao việc này; Claude là **người phản biện** của bạn. Minh đã duyệt SPEC và giao Claude toàn quyền điều phối (nguồn: `docs/DECISIONS.md`, mục "Bổ sung quyền điều phối chiến dịch nhiều ngày").

## Đọc trước (bắt buộc)

1. `AGENTS.md` (luật 0 có ngoại lệ 7: bạn được ghi trong đúng "Phạm vi ghi" của SPEC đã duyệt).
2. `tasks/T-062-dem-chang-1-4/SPEC-PHU-LUC-2.md` **toàn bộ, gồm phần bổ sung cuối file** — đây là đề bài. "Yêu cầu kịch bản" 1–7 do Claude soạn là yêu cầu bắt buộc.
3. `tasks/T-062-dem-chang-1-4/CHIEN-DICH-M1-FT.md` mục 1, 2, 6 (luật, bối cảnh, quyền).
4. `tasks/T-062-dem-chang-1-4/SPEC.md` bảng "Máy và truy cập"; `results/T-062/tai/` (lượt C1 của bạn: `bao-cao-C1.md`, `CHECKPOINT.md`, `chay-tai.ps1`, `c1.ps1`, `k6/`), dùng lại công cụ đã có, không cài lại.

## Quyền máy trong lượt này

- **Máy tải** `3.24.8.49`: bạn là agent duy nhất được thay đổi.
- **`exp-app`** `129.221.208.47`: bạn được thay đổi **chỉ**: chạy VNPay giả (từ `D:/Project/flash-ticket-platform/deploy/rca-test/mock_vnpay.py`), đặt biến `VNPAY_*` của payment-service và tạo lại **chỉ** container payment-service khi cần, tạo tài khoản người mua thử trong realm `flash-ticket` (Keycloak admin; mật khẩu đọc từ file trên máy, không in), tạo dữ liệu thử (sự kiện, chỗ) **qua API** organizer/admin. Không sửa DB trực tiếp, không tạo lại container khác, không đổi Collector/Toxiproxy/iptables/bộ tiêm lỗi. Từ bây giờ tới khi bạn ghi file `results/T-062/tai-2/EXP-APP-XONG` (nội dung: giờ UTC + danh sách thay đổi), **Claude không thay đổi `exp-app`**, chỉ đọc. Ghi file đó ngay khi phần thay đổi `exp-app` của bạn xong và đã kiểm; sau đó bạn chỉ đọc `exp-app` (trừ khi Claude trả quyền bằng file `results/T-062/tai-2/EXP-APP-TRA-QUYEN-<n>`).
- **`exp-obs`**: chỉ đọc (Prometheus/Loki/Tempo để đếm request gateway, span PRODUCER/CONSUMER). Prometheus vừa được Claude tăng retention 30d lúc 21:16Z; truy vấn phải **cắt khúc ≤ 10 phút** với metric nhiều chuỗi (sự cố `results/T-062/ca/_metric-bo-sung/SU-CO.md`).
- **Repo FlashTicket** `D:/Project/flash-ticket-platform`: chỉ nhánh `rca/quan-sat-log`, chỉ thư mục `deploy/rca-test/`. Không sửa code nghiệp vụ (`services/*/src/main`), không push. Nếu cần sửa trong `deploy/rca-test/`, commit cục bộ trên nhánh, ghi hash vào báo cáo; Claude quyết push.
- Bản ứng dụng đang chạy trên `exp-app`: nhánh `rca/quan-sat-log` commit `6b21ed55` (nhánh GitHub đã ở `fba6bc8`, **không triển khai lại** trong lượt này; Claude quyết revision cuối và sẽ báo nếu cần kiểm lại).

## Việc (theo bước SPEC, bàn giao từng phần)

1. **Kiểm kê API** của hành trình (danh sách sự kiện → chi tiết → `availability`; tạo đơn có idempotency key; tạo thanh toán; return/IPN VNPay; trạng thái đơn; lấy vé; hủy đơn) → `results/T-062/tai-2/api-kiem-ke.md` + `.json` (mã trả về, thân lỗi rút gọn, trace id). Route tickets trả 500 ở C1 (150/150): đọc log/trace để xác định cơ chế; nếu là lỗi nghiệp vụ thì ghi bằng chứng, không sửa.
2. **VNPay giả + tài khoản + sự kiện thử**: khoảng 20 người mua (Claude có thể đổi sau theo số đo); tồn kho đủ cho đợt thu (ước: số đơn mua/chu kỳ × 16 chu kỳ × hệ số dư 3). Kiểm: **một đơn đi tới `COMPLETED`, có vé**, có span PRODUCER/CONSUMER (message Saga) trong Tempo và callback VNPay giả trong log. Ghi `vnpay-gia.md`, `tai-khoan.md` (không bí mật). Ghi `results/T-062/tai-2/BAN-GIAO-1-giao-dich.md` ngay khi có một giao dịch chạy trọn đã kiểm (trace id, mã đơn, giờ UTC) — Claude dùng file này để bắt đầu kiểm R-04/R-09 song song.
3. **Kịch bản** `k6/hanh-trinh.js` + `k6/cau-hinh.json` theo "Yêu cầu kịch bản" 1–7 (mô hình mở theo hành trình, 70/20/5/5 khởi điểm, tham số hóa; token làm mới trước 300 s; đăng nhập ngoài cửa sổ phương pháp; không gửi nhãn/tên ca; JSON/CSV theo route và theo bước hành trình; mỗi chu kỳ dữ liệu mới). Bộ lệnh `Start/Get/Stop/Receive` tương thích `chay-tai.ps1` (thêm tham số kịch bản; không phá lệnh cũ). Chạy thử 5 phút: tỷ lệ hành trình đo được so với cấu hình, 0 lượt rơi, 0 lỗi 401 do token. Ghi `BAN-GIAO-2-kich-ban.md` khi đạt.
4. **Hai lượt 10 phút** cùng cấu hình → `lap-2-luot.md`: bảng request theo route ở gateway (Prometheus hoặc log B16) và theo k6, chênh lệch tuyệt đối và tương đối. **Không tự đặt ngưỡng đạt** (Claude đánh giá).
5. Đối chiếu số k6 gửi với số gateway nhận theo route; đếm span PRODUCER/CONSUMER > 0; đơn mua trọn có đủ chuỗi trạng thái.

## Luật cứng

1. Không push/merge `main`, không chạy `cd.yml`, không chạm máy 84 (`52.64.237.84`) hay khóa `.ppk` của nó.
2. Chỉ ghi: `results/T-062/tai-2/`, `results/T-062/codex/L1-*`, nối thêm `results/T-062/ha-tang/thay-doi.md`, nhánh `rca/quan-sat-log` thư mục `deploy/rca-test/`, máy tải, phần `exp-app` nêu trên. Không ghi `tasks/`, `docs/`, `src/`, results của task khác.
3. Không đọc `data/locked/`, không dùng ô đánh giá T-059, không tiêm lỗi, không chạy M1, không đọc sổ tiêm lỗi.
4. Mật khẩu/token/khóa: không in vào file, log, báo cáo, lệnh hiển thị. Không đọc `~/.bash_history`, `~/.ssh` trên máy. Dùng file bí mật trên máy (`umask 077`).
5. Mọi thay đổi máy: ghi `results/T-062/tai-2/thay-doi-may.md` (máy, lệnh, giờ UTC, hash cấu hình trước/sau, cách hoàn tác).
6. Có `D:/RCA-overnight/STOP` thì dừng ở ranh giới gần nhất, ghi checkpoint.
7. Lỗi hạ tầng: ghi, không xóa dữ liệu đã thu, không đoán nguyên nhân. Thử cùng một chỗ 3 lần không được thì dừng chỗ đó, ghi đã thử gì, làm phần độc lập.
8. Giữ mọi lượt chạy, kể cả lượt hỏng.

## Checkpoint và hạn mức

- Ghi `results/T-062/tai-2/CHECKPOINT.md` sau mỗi bước con và ít nhất 30 phút một lần: giờ UTC, bước, đầu ra đã có (đường dẫn), lệnh nền đang chạy (container k6, tiến trình), bước tiếp.
- Nếu lượt bị dừng do hết hạn mức, bộ gọi của Claude (`results/T-063/dieu-phoi/goi_codex.py`) sẽ gọi tiếp phiên này khi hồi: đọc checkpoint, không làm lại phần đã có đầu ra hợp lệ.

## Báo xong

File `-o` của lệnh này: dòng đầu một trong `L1 XONG`, `L1 XONG MỘT PHẦN`, `L1 CHẶN`. Sau đó: đã làm gì; file đã tạo; kiểm đã chạy và kết quả (kèm số, đường dẫn); phần chưa làm/bị chặn và vì sao (bằng chứng); trạng thái `exp-app` (đã ghi `EXP-APP-XONG` chưa); lệnh để bộ chạy dùng tải mới. Viết tiếng Việt, câu ngắn.

## Chế độ chạy của lượt này (bổ sung 22:10Z)

Lượt này chạy trong sandbox `workspace-write` của Codex: ghi được `D:\RCA-flashticket` và `D:\Project\flash-ticket-platform`, có mạng (SSH tới máy). Nếu một lệnh cần thiết bị sandbox chặn (ghi ngoài hai thư mục trên, v.v.), **không tìm cách vòng**: ghi lệnh, thông báo lỗi và bước bị ảnh hưởng vào `CHECKPOINT.md` và báo cáo, rồi làm phần độc lập.
