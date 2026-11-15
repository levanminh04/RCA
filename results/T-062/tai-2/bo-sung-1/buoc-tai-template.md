# Đổi bậc tải trong một lượt

Lượt `l1step20261113a`, cấu hình 240 s, bậc tại 120 s, Multiplier 3. Hai scenario `constant-arrival-rate`: 12 hành trình/10 s trước bậc, 36/10 s sau bậc. Giữ hỗn hợp 70/20/5/5 và sự kiện hiện hành. Không gắn nhãn/tên ca/traceparent tự tạo vào request.

Mốc thực k6: @EPOCH@. Mỗi hàng là khoảng nửa mở [đầu, cuối); đơn vị rate là request/s. K6 gửi lấy `sentUtc`; k6 hoàn tất lấy thời điểm nhận response; gateway lấy timestamp B16 hoàn tất. Trễ mạng/độ dài hành trình có thể dịch request qua ranh giới khúc, nên báo cả ba cột, không gán rate request bằng rate hành trình. Callback mock và refresh Keycloak không đi gateway.

| Khoảng giây | K6 gửi | K6 gửi/s | K6 hoàn tất | K6 hoàn tất/s | Gateway toàn bộ | Gateway toàn bộ/s | Gateway khớp k6 | Gateway khớp/s | Gateway ngoài k6 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
@BINS@

Ngoài cửa sổ cấu hình, kể cả phần gracefulStop: @TAIL@. Tổng và phép nối ID request: @MATCH@.

Số hành trình bắt đầu theo scenario: @STARTS@. Kết quả: @COUNTS@. Đỉnh hành trình đang chạy quan sát từ start/end theo scenario: @PEAK@; đỉnh chung @PEAK_ALL@. Giá trị gauge `vus` lớn nhất được ghi là @VU_GAUGE@; giới hạn khai báo và hành trình đồng thời được báo riêng.

@CAPACITY@

20 VU là giới hạn **mỗi scenario**. K6 dự phòng tổng tối đa 40 cho trường hợp hai scenario chồng trong gracefulStop; 40 phiên PKCE thuộc cùng 20 người mua. Bản không có `-BuocTai` vẫn dùng một scenario tối đa 20 VU và Multiplier áp dụng từ đầu. Không tự tăng maxVUs từ kết quả pilot này; Claude quyết cấu hình đợt thu nếu can thiệp làm hành trình kéo dài hơn. Cột gateway ngoài k6 giữ riêng các request không nối được tới workload; không gán 401 của chúng thành lỗi token k6. Chỉ thời điểm/nhãn route chưa đủ khẳng định chủ sở hữu các request đó.

Nguồn: `bo-sung-1/k6-inspect.json`, `bo-sung-1/buoc-tai.json`, `out/l1step20261113a/{analysis.json,raw.json,raw.csv,gateway.jsonl,container.log,run.json,summary.json,inputs.sha256,outputs.sha256}`. Giữ mọi lượt hỏng nếu có; không thay đầu ra cũ.
