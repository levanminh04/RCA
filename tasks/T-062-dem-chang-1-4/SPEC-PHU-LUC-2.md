# T-062 — Phụ lục 2: tải chuẩn có đăng nhập, đặt vé và thanh toán

- **Trạng thái:** đã duyệt (13/11/2026). Minh: "Đã duyệt bổ sung gói hoàn thiện tải chuẩn vào T-062, có luồng đặt vé và thanh toán"; "B1 — tải mua vé: việc này để claude lên kịch bản, claude điều phối"; duyệt tổng thể gói chiến dịch 13/11. `SPEC.md` gốc của T-062 giữ nguyên; file này là phần bổ sung.
- **Người làm:** Codex (`gpt-6.1-sol`, reasoning high), theo yêu cầu kịch bản dưới đây do Claude soạn. **Người phản biện:** Claude.
- **Bổ sung đã duyệt 13/11/2026:** áp dụng phần bổ sung cuối file về tự chủ, phụ thuộc và điều kiện hoàn thành. Căn cứ ở `docs/DECISIONS.md`, mục “Bổ sung quyền điều phối chiến dịch nhiều ngày”.
- **Thuộc:** `docs/techstack/KE-HOACH-GIAI-DOAN-2.md` chặng 2 ("Kịch bản tải bắt buộc có đăng nhập và đặt vé"; xong khi "một kịch bản cố định chạy lặp 2 lần cho lưu lượng giống nhau"). Hồ sơ chiến dịch: `CHIEN-DICH-M1-FT.md`.

## Mục tiêu

Sửa chỗ thu hẹp của T-062 (dòng C1 chỉ giao tải đọc trên đơn có sẵn). Có một kịch bản k6 theo **hành trình người mua** chạy được trên `exp-app`, sinh đủ HTTP, DB, cache, message và callback để: kiểm R-04, R-09; xác nhận ô REDIS-BOOK; phục vụ các hướng H1, H3, H4, H8 của T-064.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi | Phép kiểm | Quyết định phụ thuộc |
|---|---|---|
| API lõi nào chạy được trên bản đang triển khai? | Gọi từng API của hành trình, ghi mã trả về, thân lỗi rút gọn, trace id | Hành trình nào đưa vào tải; API hỏng thì ghi là lỗi nền đã khai, không sửa code nghiệp vụ |
| Chuỗi tạo đơn → thanh toán → phát vé có chạy trọn không? | Một đơn đi tới `COMPLETED`, có vé; đối chiếu `deploy/rca-test/fixtures.py::purchase` | Có tải mua trọn hay chỉ tới bước chạy được |
| Hai lượt cùng kịch bản có cho lưu lượng giống nhau? | Đếm request theo route ở gateway (Prometheus/log gateway), 2 lượt × 10 phút | Kịch bản được dùng làm chuẩn cho đợt thu |

## Đầu vào

`D:/Project/flash-ticket-platform` nhánh `rca/quan-sat-log` (`deploy/rca-test/`: `mock_vnpay.py`, `fixtures.py`, `workload.js`, `compose.yml`); `results/T-062/tai/` (kịch bản và cấu hình tải đọc, cách lấy token PKCE); `results/T-058/dem-2026-11-10/auth.py`; danh sách endpoint trong `CHIEN-DICH-M1-FT.md` mục 2.

## Yêu cầu kịch bản (Claude soạn; Codex cài)

1. **Mô hình mở**, nhịp đến cố định của **hành trình** (không phải request), `constant-arrival-rate`; mức tải mặc định cho tổng request ở gateway xấp xỉ 5 req/s như T-062 (tham số hóa; FLASH: ×3).
2. **Hành trình** (tỷ lệ khởi điểm, tham số hóa): 70% chỉ xem (danh sách sự kiện → chi tiết → `availability`); 20% mua trọn (tạo đơn có idempotency key → tạo thanh toán → VNPay giả gọi return/IPN → chờ đơn hoàn tất → lấy vé); 5% tạo đơn rồi bỏ (để hết hạn giữ chỗ); 5% tạo đơn rồi hủy.
3. **Tài khoản:** khoảng 20 người mua thử trong realm `flash-ticket`; token làm mới trước 300 s; đăng nhập ngoài cửa sổ phương pháp. Mật khẩu chỉ nằm trong file bí mật trên máy (`/opt/flash-ticket-app/env/…`, `/opt/rca-tai/secret/…`), **không** vào repo, log, báo cáo.
4. **Tồn kho:** sự kiện thử có đủ chỗ cho cả đợt thu (ước lượng số đơn mỗi chu kỳ × số chu kỳ, có dư); tạo qua API organizer/admin, không sửa DB trực tiếp.
5. **VNPay giả** chạy trên `exp-app` (từ `deploy/rca-test/mock_vnpay.py`), payment-service trỏ `VNPAY_*` về nó; không dùng VNPay thật, không ngrok.
6. **Không gửi** tên ca, trạng thái tiêm lỗi hay nhãn nào tới ứng dụng. Kết quả k6 xuất JSON/CSV theo route và theo bước hành trình (để đo ảnh hưởng giao dịch ngoài dữ liệu M1).
7. Mỗi chu kỳ dùng dữ liệu mới (đơn mới), không phụ thuộc trạng thái chu kỳ trước; ghi cách dọn hoặc cách giữ dữ liệu cũ không ảnh hưởng.

## Đầu ra

`results/T-062/tai-2/`: `api-kiem-ke.md` (+ `.json`), `k6/hanh-trinh.js`, `k6/cau-hinh.json`, `vnpay-gia.md`, `tai-khoan.md` (số lượng, cách tạo; không có bí mật), `lap-2-luot.md` (bảng lưu lượng theo route hai lượt), `thay-doi-may.md`; nhật ký Codex ở `results/T-062/codex/L1-*`.

## Phạm vi ghi

`results/T-062/tai-2/`, `results/T-062/codex/`, `results/T-062/ha-tang/thay-doi.md` (nối thêm); máy tải; trên `exp-app` **chỉ** VNPay giả, biến `VNPAY_*` của payment-service, tài khoản và dữ liệu thử; nhánh `rca/quan-sat-log` chỉ thư mục `deploy/rca-test/`. Không sửa code nghiệp vụ.

## Các bước

1. Kiểm kê API (chỉ đọc + gọi API bình thường) — kiểm bằng bảng mã trả về có trace id.
2. Dựng VNPay giả, tạo tài khoản, sự kiện thử — kiểm bằng một đơn tới `COMPLETED` có vé.
3. Viết kịch bản, chạy thử 5 phút — kiểm bằng tỷ lệ hành trình đo được so với cấu hình, không rơi lượt.
4. Hai lượt 10 phút — kiểm bằng bảng lưu lượng theo route (báo chênh lệch tuyệt đối và tương đối; không tự đặt ngưỡng đạt, Claude đánh giá).
5. Bàn giao cho T-063 (bộ kiểm R chạy lại trên tải này).

## Kiểm đúng đắn

Đối chiếu số request k6 gửi với số gateway nhận (log B16 hoặc metric) theo route; đếm span PRODUCER/CONSUMER > 0; đơn mua trọn có đủ chuỗi trạng thái; không có 401 do token hết hạn (lọc theo thời gian).

## Tiêu chí xong

Bốn đầu ra chính có đủ; chuỗi mua trọn chạy được hoặc ghi rõ dừng ở bước nào, mã lỗi gì, bằng chứng; hai lượt có bảng so. API hỏng do code nghiệp vụ là kết quả hợp lệ nếu được ghi rõ (không sửa).

## Không làm

Không sửa code nghiệp vụ; không merge/push `main`; không tiêm lỗi; không chạy M1; không đụng `exp-obs` ngoài lệnh đọc.

## Chi phí ước lượng

Chưa kiểm: 1–2 ngày làm việc của Codex; lượt chạy dài nhất 10 phút.

## Rủi ro và điều chưa chắc

Chưa kiểm: VNPay giả có chạy đúng trên ARM và với cấu hình payment-service hiện tại; đăng nhập 20 tài khoản qua PKCE từ máy tải; tốc độ hết hạn giữ chỗ so với độ dài chu kỳ; tải mua có làm đầy DB thử qua nhiều chu kỳ.

## Bổ sung đã duyệt — điều phối nhiều ngày, 13/11/2026

Phần này thay thế các câu cho phép coi chuỗi mua chưa chạy trọn là đã hoàn thành ở bảng “Câu hỏi” và “Tiêu chí xong”. Nội dung trước bổ sung giữ làm lịch sử.

- Hoàn thành khi hành trình mua trọn chạy được trên bản triển khai được dùng, có bằng chứng đơn `COMPLETED`, vé và message/callback cần cho bước kiểm quan sát, cùng các đầu ra và hai lượt kiểm lưu lượng đã yêu cầu. Khi hành trình dừng ở một bước, ghi bằng chứng và giữ phần phụ thuộc ở trạng thái chưa hoàn thành.
- Codex xử lý nguyên nhân thuộc kịch bản, mock, tài khoản, cấu hình và dữ liệu thử trong quyền. Khi cần sửa nghiệp vụ, trình đúng phần sửa và bằng chứng, đồng thời tiếp tục việc độc lập. Lỗi nghiệp vụ đã mô tả không thay thế bằng chứng tải mua trọn chạy được.
- Claude tự quyết tỷ lệ hành trình, số tài khoản và mức tải phù hợp từ số đo, trong phạm vi chiến dịch. Ghi cấu hình cuối và lý do trước lượt thu chính, dùng nhất quán trong các phép so tương ứng. Các giá trị khởi điểm ở trên phục vụ thử tải ban đầu.
- L1 bàn giao từng phần đã kiểm cho T-063, gồm mock/tài khoản, giao dịch chạy trọn và kịch bản tải. Phối hợp thay đổi `exp-app` với L2, kiểm lại đường tải và telemetry chịu ảnh hưởng sau khi tạo lại container hoặc đổi cấu hình. Hai lượt xác nhận chuẩn tải dùng cấu hình cuối tương ứng.
- Bổ sung phạm vi ghi `LOG.md` của phụ lục trong thư mục T-062, checkpoint L1 tại `results/T-062/tai-2/` và dòng phụ lục này trong STATE. Các task khác tiếp tục ghi hồ sơ của mình theo phân vai.
- Ước lượng 1–2 ngày là thông tin chưa kiểm. Làm tiếp theo phụ thuộc thực, cập nhật thời gian đã dùng và việc còn lại. Sau báo cáo sáng hoặc báo cáo mốc, tiếp tục tới đầu ra đã giao.
