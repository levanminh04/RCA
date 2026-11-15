L3 XONG MỘT PHẦN

Codex, người làm T-065. Kiểm bằng dữ liệu đã lưu và API Grafana/Infinity thật trên exp-obs, ngày 12/11/2026 UTC (13/11 giờ Việt Nam). Đây chưa phải nghiệm thu G-a/G-b và chưa phải phản biện chính thức.

Đã triển khai hai dashboard mới `t065-rca` và `t065-phat-lai`, dữ liệu trong thư mục mới `rca-ket-qua/t065-l3-001`. Hai dashboard bản 6 giữ nguyên. Không chạy lại M1.

Đầu ra và phép kiểm

- Đọc và kiểm manifest của đầu vào/đầu ra 9 ca, bản ghi 0.2, phát lại, chỉ mục, cấu hình và dashboard bản 6. Kiểm pin `chuoi.py` và `span.py` trước khi dùng quy tắc tiền xử lý. Kết quả: [kiem-hash-nguon.json](kiem-hash-nguon.json).
- Mở rộng định dạng 0.3, có chiều `ban=p7`, phiên bản phương pháp, cấu hình/hash và cửa sổ. Cả 18 bản ghi chính/phát lại qua schema. T-061/T-062 không sửa. [Lược đồ và giải thích](../../dinh-dang/README.md), [kiem-cuc-bo.json](kiem-cuc-bo.json#/schema).
- 9 ca giữ nguyên sự cố, hạng/vai trò, vùng nghi ngờ, 17 nút/14 cạnh service mỗi ca và phần phát lại. Kiểm cả dữ liệu xuất và kết quả bảng/đồ thị từ Infinity; chưa kiểm render trên browser. [Đối chiếu nguồn](doi-chieu-9-ca.json), [đối chiếu API](doi-chieu-api.json#/cases).
- 1.197 thao tác, 92 kênh `op` có cờ, 1.183 cặp thao tác có quan hệ cha–con; tổng 620.319 span sau tiền xử lý. `n_N/n_A` của mẫu M1, trạng thái, cờ và điểm e khớp nguồn. Bộ đếm span/gốc/mồ côi/span bọc/bỏ lặp khớp trung gian P7. [doi-chieu-9-ca.json](doi-chieu-9-ca.json).
- Đồ thị thao tác chỉ dùng cha–con resolve trong cùng trace, sau cắt cửa sổ và alias; giữ ví dụ trace/span xác minh. API kiểm đủ 153 cặp ca/service, kể cả service không có thao tác. Số nút/cạnh, hướng, số lần quan hệ, ví dụ và bán kính 32 khớp file xuất. Điểm e chỉ nằm trong chi tiết/menu, không dùng để xếp hạng thao tác hoặc định cỡ nút. [doi-chieu-api.json#/services](doi-chieu-api.json).
- Theo thuộc tính raw span: 234 thao tác HTTP, 463 SQL/cache, 117 job, 383 `khac`; không khai có message khi nguồn không có. Span link bằng 0 ở 9 ca; tính năng span link message ghi **chưa hỗ trợ**. Thuộc tính đích gọi chỉ để mô tả, không suy cạnh mới. Không xác nhận cơ chế nhân quả từ cạnh cha–con.
- 2.638 URL nguồn giải mã được JSON sau đúng một lần: 1.289 Tempo, 1.201 Loki, 148 Prometheus. Riêng bảng kênh M1 có 92 Tempo, 31 Prometheus, **4 Loki mới**. Đây là kiểm URL dữ liệu; chưa là kiểm href do browser render. [kiem-cuc-bo.json#/links](kiem-cuc-bo.json), [lien-ket.json](lien-ket.json).
- Miền nguồn `[lo,hi)` giữ nguyên. Dashboard/menu/URL dùng range Grafana `from=lo`, `to=hi−1ms`; cấp chính xác đến ms của giao diện. Không dùng ±15 phút. Chọn ca qua danh sách, bộ chọn ca ẩn để tránh đổi ca mà giữ range cũ. 18 nhóm biến trên hai trang được kiểm bằng Infinity thật. [doi-chieu-api.json#/variables](doi-chieu-api.json).
- Bản bàn giao: **189 request, 1.440 target**, không lỗi; 18 trang ca và 153 cặp ca/service khớp nguồn từng dòng. Dashboard API khớp cấu hình local, version hiện tại 6 và 3. [api-panels-6.json](api-panels-6.json), [doi-chieu-api.json](doi-chieu-api.json).

Mẫu API cho liên kết — không phải bấm thật

| Ca | Tempo | Loki ngữ cảnh service | Prometheus route HTTP |
|---|---|---|---|
| e8661e0a | 50 trace | 200 dòng (giới hạn) | 1 chuỗi, 40 mẫu |
| a89954d1 | 50 trace | 200 dòng (giới hạn) | 1 chuỗi, 41 mẫu |
| 00eaea92 | 50 trace | 16 dòng | 1 chuỗi, 41 mẫu |

Tất cả truy vấn thành công, datasource/query/range khớp URL. Số trace/dòng bị giới hạn không phải tổng của cửa sổ. Nguồn: [api-links-2.json](api-links-2.json), [doi-chieu-api.json#/link_samples](doi-chieu-api.json).

Kiểm thêm cả 4 URL Loki của kênh M1 `log_loi` và 9 URL log tương quan trace: thành công. Kênh log dùng severity ERROR/FATAL đúng đầu vào. Link thao tác ghi rõ log cùng trace hoặc chỉ ngữ cảnh service; không khẳng định từng log do thao tác đó phát. [api-links-extra.json](api-links-extra.json).

Lượt lỗi và cách xử lý

1. Schema gốc T-061 chưa khai các trường phát lại do T-062 đã thêm. Mở rộng đúng trong schema 0.3, không sửa schema cũ; kiểm lại đạt. [loi-luot-dau.json](loi-luot-dau.json).
2. JSONata index binding không dùng làm bảng bằng chứng lỗi compile, bảng ví dụ cạnh trả rỗng. Đã bỏ binding và đối chiếu số dòng/ví dụ thật, đạt. Giữ [api-panels-1.json](api-panels-1.json), [api-loi-lan1.json](api-loi-lan1.json); lượt sau ở [api-panels-2.json](api-panels-2.json).
3. Tự kiểm phát hiện nhầm mã OTLP CLIENT thành message trong lần dựng đầu. Đã sửa CLIENT=3, PRODUCER=4, CONSUMER=5 theo proto chính thức, thêm fixture; kiểm lại dữ liệu cuối đạt. Không dùng lần nhầm để suy có message. Thay đổi chỉ ở phân loại để hiển thị.
4. Thử hai panel hiện kết quả truy vấn rỗng trực tiếp: lượt 3 lỗi compile; lượt nhanh 4 không lỗi nhưng lời diễn giải null; lượt 5 lỗi compile. Giữ các file tương ứng. Theo AGENTS §5a, **dừng cách này sau ba lần**, rút hai panel thử khỏi bản bàn giao. Không thử lần thứ tư. Giữ panel hướng dẫn được cấu hình đặt trước các panel sống và mô tả điều kiện của bản 6; chưa kiểm mức nhìn thấy trên browser, không ghi phần diễn giải động là đã hoàn thành.

Phần còn thiếu, chủ xử lý và bước tiếp

| Phần | Bằng chứng thiếu / vì sao | Chủ và đề xuất tiếp |
|---|---|---|
| Bấm thật, ảnh, điều hướng, màu/bố cục render | Browser Use trả `browsers: []`, `The browser access host is unavailable`. Không thay bằng API hoặc ảnh dựng. | Claude điều phối cấp môi trường browser phù hợp. Kiểm danh sách → ca → service → thao tác → bằng chứng, trang phát lại; ít nhất 3 ca ×3 kho. [anh/README.md](anh/README.md). |
| Diễn giải rỗng riêng từng truy vấn | Hai panel thử chưa đạt. Chưa phân xử lỗi cách dựng biểu thức với giới hạn parser; API biên dịch lỗi và lời diễn giải null là bằng chứng hiện có. | Claude quyết cách khác hoặc tách phần này. Đề xuất đọc biểu thức/request đã giữ, rồi xuất kết quả truy vấn thành JSON sẵn từ lớp API/bộ xuất; tránh tiếp tục thử cùng khối JSONata. Chưa triển khai đề xuất. Không cần thu thêm telemetry để kiểm lỗi biểu thức này. |
| G-c trên M1-FT | Chưa có `results/T-064/ban-xuat/chi-muc-ban.json` khi kiểm 22:34Z. P7 đã có chiều bản nhưng chưa có đầu vào phù hợp/ứng viên cuối để kiểm tích hợp. | T-064 cung cấp chỉ mục và nguồn đã băm theo hợp đồng; T-065 nối bản rồi kiểm lại. Chưa nhận T-065 xong. |

G-a/G-b mới có bằng chứng đúng dữ liệu và API; chưa đủ phép kiểm giao diện trong SPEC. Task này góp phần giao diện minh họa DT18. Không xác nhận lợi ích RCA, nguyên nhân sai của M1, hoặc trả lời xong RQ5. Không thêm/đổi quyết định nghiên cứu.

Thay đổi máy và file

177 file mới trên exp-obs khớp local: 175 dữ liệu/chỉ mục/cấu hình trong thư mục mới, 2 dashboard mới. Tám file có trước được kiểm hash trước/sau đều giữ nguyên, gồm compose, Prometheus/Loki/Tempo/Collector, provider và hai dashboard bản 6. Dashboard cũ vẫn version 6/6 ở API cuối. Restart riêng Grafana hai lần; không có tunnel/browser riêng còn mở. [Biên bản và hoàn tác](../../thay-doi-may.md), [kiem-hash-may.json](kiem-hash-may.json).

Chỉ ghi `results/T-065/` và nối `tasks/T-065-giao-dien-grafana/LOG.md`. Không ghi docs/STATE theo brief hẹp hơn; điều phối cập nhật trạng thái task. Không commit/push/merge, không truy cập exp-app hoặc máy 84, không đọc data/locked.

Mã dựng thực tế dùng JavaScript `.mjs`, thay tên `.py` dự kiến, vì Python ghim không khởi chạy trong sandbox. Đây là thay đổi cách thực thi kỹ thuật, không đổi chức năng đã giao. Hướng dẫn dựng lại: [README](../../README.md). File `manifest.json` ở gốc T-065 liệt kê tập đầu ra ổn định; loại log chạy của bộ gọi đang cập nhật khỏi snapshot.
