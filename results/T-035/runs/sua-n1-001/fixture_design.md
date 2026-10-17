# Fixture hợp đồng messaging, ghi trước khi sửa bộ dựng

Ngày 15/10/2026. Trợ lý triển khai của Codex viết trong phạm vi gói sửa Minh đã duyệt. Đây là kiểm bộ dựng, không phải lượt phản biện chính thức và không là dữ liệu FlashTicket chạy thật.

Nguồn yêu cầu: SPEC T-035 mục mô hình chung, K5/K7 và tiêu chí 1/6/9; DT18-NV2; B13 mục 5.1–5.2 (exchange, routing key, queue theo consumer, publish lại cùng message ID); B16 mục 3/5 (ngữ cảnh tạo, retry, queue metric và không dùng message ID làm metric label). Mục đích là phân xử hai nghĩa khác nhau: định danh bản tin để nối bằng chứng và địa chỉ tài nguyên để gắn số đo.

## Oracle và thứ tự

`fixture_inputs.json` và `fixture_expected.json` được ghi lúc 2026-10-15T05:46:54.061847+00:00, trước sửa bộ dựng. Đáp án là các dictionary literal ở hai mức, kèm event count, witness, địa chỉ metric, số consumer chưa nối và diagnostic. Việc tạo đáp án không import bộ dựng, không tìm producer theo input và không lấy output của bộ dựng làm đáp án. Helper khi viết chỉ đóng gói các cạnh đã liệt kê trong từng tình huống; không tự suy cạnh từ span.

`check_messaging.py` chỉ import `build` và `project` từ bản code được kiểm, không dùng helper khóa cạnh hay kết quả entity để hoàn thiện phép chiếu. Checker so cả cạnh thao tác, cạnh thực thể, đếm và witness với literal; tự chiếu riêng từ operation để kiểm gộp count/witness. Giao diện project là năm phần cũ `(source,target,type,evidence_source,destination)` cộng chuỗi JSON canonical của dictionary `messaging` khi cạnh có dictionary này. Cạnh không messaging giữ năm phần.

Metric queue có địa chỉ `[broker,broker_scope,queue]`. Producer không được tự nhận queue; metric address của producer là null. Không suy queue hoặc identity scope từ `messaging.destination` cũ. Hai địa chỉ chỉ khác message ID hoặc attempt không thành hai metric. Giá trị exchange/routing key rỗng là giá trị có nghĩa, khác với thiếu trường.

## Các tình huống và phân xử

| Nhóm | Điều kiện | Kết quả mong đợi |
|---|---|---|
| 01 | Event phát một lần; Booking, Ticket, Payment nhận ba queue; verified link; không message ID; destination hai phía khác nhau | 1 cạnh phát, 3 cạnh nhận, 3 cạnh logic; 3 địa chỉ queue; không suy queue từ địa chỉ gửi |
| 02 | Hai queue của cùng service và cùng operation | Giữ 2 cạnh nhận và 2 cạnh logic ở cả hai mức, mỗi cạnh mang đúng queue |
| 03 | Hai lần nhận cùng queue, operation và ID; attempt khác nhau | Gộp cấu trúc, count 2 và hai witness; chỉ một địa chỉ queue, không có nút theo attempt/ID |
| 04–05 | Hai publish attempt cùng ID/scope | ID-only đa nghĩa; verified link tới từng attempt nối đúng, giữ hai sự kiện |
| 06–09 | Link chưa xác minh/sai semantics, thiếu nguồn hoặc sai kind; thêm tình huống ID độc lập hợp lệ | Bỏ link chưa đủ nghĩa; có thể dùng ID độc lập. Khi có verified message-creation link thì không fallback ID che lỗi nguồn |
| 10 | Lần lượt mâu thuẫn broker, broker scope, exchange, routing key, identity scope và message ID | Không tạo cạnh logic; diagnostic chỉ đúng nhóm mâu thuẫn; giữ cạnh endpoint quan sát được |
| 11 | Cùng consumer có một link hợp lệ và các link sai | Giữ cạnh từ link hợp lệ, báo từng vấn đề; không xóa bằng chứng hợp lệ khác |
| 12–13 | Cùng giá trị ID ở identity scope khác; cùng queue name ở broker scope khác | Chỉ nối trong scope tương ứng; địa chỉ queue theo broker scope không bị nhập |
| 14–17 | Không có nguồn ID, scope của consumer/producer chưa xác minh, hoặc đường gửi mâu thuẫn dù ID khớp | Không chọn tùy tiện; phân biệt no source, unverified và scope conflict |
| 18 | Chỉ cùng correlationId | Không có cạnh logic |
| 19–20 | Producer ngoài cửa sổ, consumer trong cửa sổ | Chỉ giữ cạnh nhận; không dùng nguồn ngoài cửa sổ qua link hay ID |
| 21–22 | Link hợp lệ nhưng thiếu broker scope hoặc queue | Có cạnh logic; không bịa địa chỉ metric; diagnostic địa chỉ thiếu đếm một lần trên consumer |
| 23–24 | Exchange/routing key là chuỗi rỗng, rồi cho một phía exchange khác | Rỗng-rỗng hợp lệ; rỗng-khác là mâu thuẫn, không coi rỗng là thiếu |
| 25 | Chỉ địa chỉ legacy khác nhau, verified link hợp lệ | Có logic, không suy địa chỉ queue từ legacy; báo metric address chưa đủ |
| 26–27 | ID-only đầy đủ, nguồn duy nhất; đổi giá trị ID nhất quán hai phía | Nối đúng và giữ nguyên cấu trúc/địa chỉ metric |
| 28 | Hai verified link thiếu nguồn trên một consumer | Hai vấn đề được đếm, witness consumer chỉ một khóa, unresolved đếm một consumer |

33 case: nhóm 10 tách sáu trường mâu thuẫn thành sáu case; các nhóm khác mỗi nhóm một case. Các fixture cũ vẫn được giữ và chạy riêng. Đáp án kiểm semantics của hợp đồng nội bộ đã chốt; không xác minh instrumentation thật, lợi ích RCA hoặc một thiết kế P6.

## Chạy và lưu cả lỗi

Từ repo, dùng Python đã ghim và `-B`:

```powershell
& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -B results/T-035/runs/sua-n1-001/check_messaging.py <thu-muc-moi>
```

Có thể thêm `--builder-path <duong-dan-ban-builder-lich-su>` để chạy phản chứng trước sửa. Mỗi lần tạo đúng một thư mục mới dưới `sua-n1-001`, lưu `result.json` gồm tất cả pass/fail/exception và hash nguồn. Exit khác 0 nếu bất kỳ case lỗi. Không ghi đè output cũ; không đọc dữ liệu thật, nhãn hoặc tập khóa.
