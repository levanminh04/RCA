# Đổi bậc tải trong một lượt

Lượt `l1step20261113a`, cấu hình 240 s, bậc tại 120 s, Multiplier 3. Hai scenario `constant-arrival-rate`: 12 hành trình/10 s trước bậc, 36/10 s sau bậc. Giữ hỗn hợp 70/20/5/5 và sự kiện hiện hành. Không gắn nhãn/tên ca/traceparent tự tạo vào request.

Mốc thực k6: 2026-11-13T03:02:18.618000+00:00. Mỗi hàng là khoảng nửa mở [đầu, cuối); đơn vị rate là request/s. K6 gửi lấy `sentUtc`; k6 hoàn tất lấy thời điểm nhận response; gateway lấy timestamp B16 hoàn tất. Trễ mạng/độ dài hành trình có thể dịch request qua ranh giới khúc, nên báo cả ba cột, không gán rate request bằng rate hành trình. Callback mock và refresh Keycloak không đi gateway.

| Khoảng giây | K6 gửi | K6 gửi/s | K6 hoàn tất | K6 hoàn tất/s | Gateway toàn bộ | Gateway toàn bộ/s | Gateway khớp k6 | Gateway khớp/s | Gateway ngoài k6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0-30 | 154 | 5.1333 | 153 | 5.1 | 157 | 5.2333 | 154 | 5.1333 | 3 |
| 30-60 | 154 | 5.1333 | 154 | 5.1333 | 156 | 5.2 | 153 | 5.1 | 3 |
| 60-90 | 153 | 5.1 | 154 | 5.1333 | 157 | 5.2333 | 154 | 5.1333 | 3 |
| 90-120 | 155 | 5.1667 | 155 | 5.1667 | 158 | 5.2667 | 155 | 5.1667 | 3 |
| 120-150 | 458 | 15.2667 | 455 | 15.1667 | 458 | 15.2667 | 455 | 15.1667 | 3 |
| 150-180 | 471 | 15.7 | 470 | 15.6667 | 475 | 15.8333 | 472 | 15.7333 | 3 |
| 180-210 | 460 | 15.3333 | 461 | 15.3667 | 463 | 15.4333 | 460 | 15.3333 | 3 |
| 210-240 | 468 | 15.6 | 467 | 15.5667 | 470 | 15.6667 | 467 | 15.5667 | 3 |

Ngoài cửa sổ cấu hình, kể cả phần gracefulStop: {"k6Completed":22,"k6Sent":18,"gatewayCompleted":22,"gatewayMatched":21,"gatewayOther":1}. Tổng và phép nối ID request: k6=2491, gateway=2516, missing=0, mismatch=0, extra=25.

Số hành trình bắt đầu theo scenario: {"standard":145,"increased":432}. Kết quả: {"journey_started":577,"journey_finished":577,"token_refresh_success":20}. Đỉnh hành trình đang chạy quan sát từ start/end theo scenario: {"standard":5,"increased":10}; đỉnh chung 10. Giá trị gauge `vus` lớn nhất được ghi là 10; giới hạn khai báo và hành trình đồng thời được báo riêng.

Trong lượt khỏe đã kiểm, maxVUs=20 mỗi scenario không gây dropped hoặc lỗi hành trình. Đây là kết quả ở mức tải/thời gian này, không bảo đảm đủ cho mọi lỗi hoặc chu kỳ dài.

20 VU là giới hạn **mỗi scenario**. K6 dự phòng tổng tối đa 40 cho trường hợp hai scenario chồng trong gracefulStop; 40 phiên PKCE thuộc cùng 20 người mua. Bản không có `-BuocTai` vẫn dùng một scenario tối đa 20 VU và Multiplier áp dụng từ đầu. Không tự tăng maxVUs từ kết quả pilot này; Claude quyết cấu hình đợt thu nếu can thiệp làm hành trình kéo dài hơn. Cột gateway ngoài k6 giữ riêng các request không nối được tới workload; không gán 401 của chúng thành lỗi token k6. Chỉ thời điểm/nhãn route chưa đủ khẳng định chủ sở hữu các request đó.

Nguồn: `bo-sung-1/k6-inspect.json`, `bo-sung-1/buoc-tai.json`, `out/l1step20261113a/{analysis.json,raw.json,raw.csv,gateway.jsonl,container.log,run.json,summary.json,inputs.sha256,outputs.sha256}`. Giữ mọi lượt hỏng nếu có; không thay đầu ra cũ.
