# T-065 L4 — kết quả G-c và phần mở L3

Trạng thái: **đạt phần dữ liệu/API; toàn task vẫn một phần vì chưa bấm thật**. G-c đã nối ba bản của chỉ mục hiện hành cho cùng 22 ca, gồm 9 ca T-062 và 13 ca dev bản 2. Đây là tích hợp giao diện, không khóa M1-FT hay nghiệm thu T-065.

## Dữ liệu và giao diện

- Hai UID mới: t065-l4-rca và t065-l4-phat-lai. Dữ liệu ở t065-l4-001. Mọi điều hướng giữ bản; chọn ca bằng bảng đặt đúng cửa sổ [t−300,t+300), URL dùng biên hi−1ms. Mã V041 có dấu + được percent-encode ở tham số bản. Folder Grafana vẫn là RCA do provider hiện hành; thư mục dữ liệu đã tách mới. Câu hỏi phân biệt hai nghĩa “thư mục” đã trình, chưa có trả lời, không tự sửa provider ngoài quyền L3.
- Trang ca hiện bản, trạng thái khóa/đề xuất/thay thế, hai hash cấp bản và nguồn đầu ra. Hai hash P7 trong chỉ mục là null: hiện đúng nguồn chưa cấp, không dựng hash cây mã. Mọi hash từng đầu ra đã kiểm.
- entity_ranking giữ nguyên thứ tự/key/tie_group. Nhóm thực thể hiển thị tie_group+1 như quy ước L3; hạng cạnh lấy nguyên trường hang của nguồn. Không xếp lại/chấm lại. V032/P7 hiện đúng “không có đầu ra cạnh”; V041 lấy extra.m1_ft.canh_xep_hang. Cạnh thao tác quan sát không bị dùng thay cho đầu ra cạnh.
- Trang chính không có đáp án. Phát lại T-062 ghép riêng đáp án gốc, bỏ nhận xét/hạng chấm P7 để không mang sang bản khác. Dev chưa có nguồn đáp án được cấp cho giao diện, hiện đúng giới hạn ấy.

## Kiểm cục bộ

Nguồn trước dùng: 66/66 đầu ra khớp SHA trong chỉ mục; 221/221 file L3 khớp manifest; 13/13 archive dev khớp SHA256SUMS. Nguồn cuối: chỉ mục không đổi và 66 đầu ra vẫn khớp. Xem kiem-hash-nguon.json, kiem-goi-dev2.json, kiem-nguon-cuoi.json.

kiem-cuc-bo.json là nguồn số, các trường rank_rows/flag_rows/unit_rows/edge_rows/operation_rows/urls:

| Đại lượng so với đầu ra nguồn | Số dòng/đối tượng | Kết quả |
|---|---:|---|
| Cặp bản × ca | 66 | Khớp |
| Thực thể: thứ tự, key, tie_group, lớp và số cờ | 1121 | Khớp |
| Cờ M1 đầy đủ | 1538 | Khớp nguyên giá trị, giữ số nguyên ns |
| Đơn vị M1 đầy đủ | 19892 | Khớp |
| Cạnh xếp hạng V041 | 456 | Khớp thứ tự, hạng, cờ, loại và nguồn xác minh |
| Thao tác: mẫu/trạng thái/cờ/đơn vị | 14955 | Khớp |
| URL bằng chứng | 33002 | Giải mã đúng một lần, đúng kho/query/biên |

Hồi quy P7: 9/9 ca giữ nguyên toàn bộ thao tác, cạnh thao tác và URL bằng chứng của L3; L3 trước đó đã đối chiếu nguồn bản 6. Schema 0.4: 66/66 bản ghi đạt (kiem-schema.json). Các phép chiếu phục vụ panel: 1.188/1.188 file khớp dữ liệu đầy đủ (kiem-phep-chieu.json).

Dev có đủ nguồn. Đọc streaming raw trace từ archive, kiểm hash theo manifest ca và đối chiếu 2.535.887 span sau cắt cửa sổ với đầu vào chuẩn hóa. Có 3.788 dòng thao tác trên 13 ca; 196 dòng message, loại dựa thuộc tính messaging hoặc OTLP PRODUCER/CONSUMER, không đoán từ tên. Span link bằng 0, vẫn ghi chưa hỗ trợ. Chi tiết từng ca: kiem-raw-dev2.json. Log theo thao tác là ngữ cảnh service, không khẳng định log do thao tác phát. Metric route chỉ tạo khi raw span có route/method. Không chạy lại M1 hoặc đọc nhãn khi xuất trang chính.

## Kiểm API

- Bản cuối api-panels-3.json và doi-chieu-api.json: 132 trang, 2442 target; toàn bộ ba bản × ca, trang chính/phát lại và biến bản/ca/service/cửa sổ đều khớp. Đối chiếu từng dòng thực thể, cờ, cạnh, bảng thao tác, liên kết thao tác và trạng thái snapshot với dữ liệu nguồn. API không thay bằng chứng href/render trên trình duyệt.
- api-links-3.json và kiem-links-api.json: 54 mẫu = 3 kho × 6 ca × 3 bản. Sáu ca gồm ba T-062 và ba dev2. Cả 54 truy vấn thành công và có dữ liệu. Đây là gọi API của URL, không phải bấm thật.
- api-snapshot.json và snapshot-summary.json: 374 cặp ca/service × 5 truy vấn = 1.870 target. 639 có dữ liệu, 1231 rỗng, 0 lỗi. Mỗi dòng có giờ UTC, cửa sổ, số dòng và request. Không suy nguyên nhân rỗng. Panel 28 đọc trường đã tính sẵn; đối chiếu API panel đã đạt, không thử thêm biểu thức JSONata cho trạng thái rỗng. Snapshot dùng chung bản vì query/cửa sổ ca/service giống nhau.

## Lỗi giữ lại và xử lý

1. Kiểm cục bộ đầu phát hiện màu LOW_SUPPORT đổi sang xám khi gắn cờ bản mới. Đã giữ quy tắc L3 (tím nếu thiếu hỗ trợ), kiểm lại khớp P7. loi-cuc-bo-1.json.
2. Lượt đọc raw đầu: GNU tar hiểu ổ D: là remote. Chuyển sang đường dẫn tương đối/cwd repo; lượt lỗi chưa sửa dữ liệu. loi-raw-1.json.
3. API đầy đủ lượt 1 bị IncompleteRead; lượt link cùng lúc Connection refused. Docker ghi sự kiện **oom**, rồi die exit 137 và start lúc 01:39:46Z (codex/l4-docker-events.jsonl); đây là lỗi tài nguyên/hạ tầng, không là kết quả M1. Agent không phát restart. Container giới hạn 768 MiB; OOMKilled ở lần inspect sau restart là false nên không dùng riêng cờ ấy để phủ nhận sự kiện OOM.
4. Đã tạo file phép chiếu để panel không đọc lặp tài liệu nguồn nhiều MB cho mỗi target, giữ nguồn đầy đủ. Chia bộ kiểm theo trang, lưu slot v2/v3 trên máy, không mất slot đã xong nếu API ngắt. Lượt 2 đạt trước bổ sung raw; lượt 3 đạt sau bổ sung loại/link raw. Giữ toàn bộ lượt, snapshot 1.870 truy vấn hợp lệ không chạy lại. Kết quả cuối không có restart mới; chưa khẳng định chịu được mọi mức tải đồng thời.

## Đối chiếu phần mở L3

- P1 của REVIEW.md: đúng, còn CHẶN nghiệm thu. Thử duy nhất cua.getState() trả browsers=[] và “The browser access host is unavailable”. Dừng theo brief, không tìm đường vòng, không nhập mật khẩu vào trang đăng nhập. Chưa có ảnh, bấm thật hay kiểm bố cục/màu thực tế.
- P2: cách xuất trạng thái API sẵn đã triển khai, đối chiếu API đạt. Chưa kiểm mức nhìn thấy trên browser.
- P3: đã đọc raw dev2 và kiểm message như số từng ca trong kiem-raw-dev2.json; không suy span link khi không có.
- P4: tiếp tục JavaScript vì môi trường Python ghim ở laptop không khởi chạy như L3; API chạy bằng Python sẵn trên exp-obs.

## Máy, phạm vi và phần còn mở

185 file có trước (cấu hình/provider, dashboard bản 6/L3 và dữ liệu L3) giữ hash. 2822 file dữ liệu/dashboard mới khớp byte local. Hash đầy đủ ở kiem-hash-may.json; thời điểm/rollback ở ../../thay-doi-may.md. Bản 6 vẫn version 6/6, L3 6/3, L4 2/2. Không sửa compose, datasource, kho hay collector; không chủ động restart; không tunnel/browser riêng còn mở. Chỉ ghi results/T-065 và nối LOG T-065. Không ghi docs/STATE/src/T-064; điều phối cập nhật STATE. Không commit/push/merge.

T-065 góp phần giao diện minh họa DT18; không xác nhận lợi ích RCA hoặc trả lời xong RQ5. Không thêm/đổi quyết định nghiên cứu. Cần đưa vào báo cáo chính thức: trạng thái bản vẫn tạm/thay thế, P7 chưa có hai hash cấp bản trong chỉ mục, các giới hạn liên kết log/span link và kiểm trình duyệt còn thiếu.

Bước tiếp đề xuất: Claude kiểm độc lập bằng prompt bàn giao, rồi thực hiện lượt bấm thật ở môi trường có browser host và phiên Grafana đã đăng nhập: danh sách → cùng ca đổi bản → service → thao tác → ba kho, trang phát lại; giữ ảnh ít nhất ba ca. Cách này bổ sung đúng bằng chứng còn thiếu, không cần chạy lại M1 hoặc các phép kiểm dữ liệu/API đã hợp lệ. Phương án chấp nhận giới hạn chỉ giữ trạng thái một phần, không nghiệm thu thay kiểm browser. Nếu cần folder Grafana riêng, trình thay đổi provider cụ thể trước vì quyền L3 không cho tự đổi provider.
