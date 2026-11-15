# Máy tải C1 — T-062

Intent: EXECUTE. Codex là người làm C1 trên laptop Windows. Phạm vi theo brief v3 của Minh; không ghi LOG/STATE vì brief chỉ cho ghi `results/T-062/tai/` và `codex/`.

FACT: AWS `3.24.8.49`, Ubuntu x86_64, 2 vCPU, 7,7 GB RAM là máy tải chính. Dùng lại cài đặt lượt trước, không cài lại. Docker Engine Community 29.9.3 từ repo Docker chính thức; containerd 2.4.2; chrony 4.8-2ubuntu1. Bằng chứng: `cai-dat-tai.txt`, `kiem-lai-tai.txt`.

k6 1.4.2, image và digest đầy đủ ở `k6/cau-hinh.json#/image`. Image amd64, kích thước 110775510 byte theo `cai-dat-tai.txt`. Các lệnh chạy dùng digest, không dùng tag trôi. Container mang tiền tố `rca-tai-`; không xóa container hoặc đầu ra.

Kiểm đồng hồ AWS lúc 2026-11-11T18:38:42Z: chronyc system time nhanh 0,000000345 giây, last offset -0,000000861 giây; `NTPSynchronized=yes`, Leap status Normal. Nguồn `kiem-lai-tai.txt`.

exp-obs chỉ dự phòng. Không chạy tải ở đó trong bước chuẩn bị. Thư mục `/opt/rca-tai/` đã tạo ở lượt v2 và giữ nguyên. Kiểm chỉ đọc lúc 2026-11-11T18:38:44Z: chronyc system time chậm 0,000051908 giây, last offset -0,000055064 giây; `NTPSynchronized=yes`, Leap status Normal. Nguồn `kiem-lai-obs.txt`. Không thay đổi stack quan sát, compose, iptables hoặc `/opt/flash-ticket-obs/`.

Token đăng nhập bằng PKCE qua exp-app, Python in-memory qua SSH; stdout được giữ trong biến rồi pipe sang file quyền 0600 trên máy tải. Không lưu token trong repo. Thử refresh từ AWS qua Keycloak công khai trả 200; issuer nội bộ đúng như cấu hình Gateway. Nguồn `refresh-probe.json`. Mỗi VU giữ access/refresh trong bộ nhớ riêng, refresh khi tuổi access token đạt 200 giây. Lỗi refresh dừng lượt và giữ dữ liệu; không ghi response body. Phép thử 5 phút đã ghi 4 refresh thành công, 0 lỗi refresh và 0 HTTP 401; nguồn `chay-thu-5p/phan-tich.json#/counters` và `#/routes`. Đây là bằng chứng trong lượt 5 phút, chưa kiểm nhánh lỗi refresh hoặc tải dài.

Mỗi `Start-Tai` đăng nhập PKCE mới, vì vậy không nối phiên Keycloak quá 10 giờ. Thời lượng mỗi lượt 1–3600 giây. Refresh token báo idle lifetime 1800 giây; tải refresh ở 200 giây. Nếu chạy liên tục qua nhiều lượt, đăng nhập mới ở đầu từng lượt. Không có vòng nền giữ mật khẩu hoặc token trên laptop.

Đối chiếu nguồn: C1 cung cấp tải đọc cố định phục vụ thử nghiệm FlashTicket trong MRP P9, DT18-NV1/NV3. Một lượt 5 phút ở một mức tải không xác nhận khả năng mở rộng, ổn định giao dịch ghi, hoặc chất lượng RCA. Không thay đổi lựa chọn nghiên cứu, M1 hay dữ liệu khóa.

Tài liệu k6 đã đối chiếu: [Params](https://grafana.com/docs/k6/latest/javascript-api/k6-http/params/), [arrival-rate VU allocation](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/arrival-rate-vu-allocation/), [JSON output](https://grafana.com/docs/k6/latest/results-output/real-time/json/), [options](https://grafana.com/docs/k6/latest/using-k6/k6-options/reference/). Hành vi thực tế được kiểm trên image đã ghim; `k6 inspect` cần truyền `-e` trực tiếp. Hai lần inspect thiếu biến môi trường được giữ trong container `rca-tai-verify-001/002`; lần 003 thành công, không phát request tải.
