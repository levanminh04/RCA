# Bộ dựng đồ thị phụ thuộc P5

Đặc tả: `results/T-035/dac-ta-do-thi.md` (v2.1), bản trước chạy ở `dac-ta-do-thi-v0.md`; v1 và mã trước sửa được giữ trong `results/T-035/runs/sua-n1-001/before/`. Đây là bộ dựng cấu trúc và độ phủ, chưa phát hiện bất thường hoặc xếp hạng.

`build(spans, interval, aliases, universe)` trả hai đồ thị thực thể/thao tác. `interval` dùng nanosecond hoặc null cho toàn bảng được caller cho phép. `Prepared` tạo chỉ mục một lần cho nhiều khoảng. `from_p3` thêm các trường tùy chọn rỗng. `project` trả tập nút/cạnh chiếu từ mức thao tác; inventory được giữ riêng ở đồ thị thực thể. Thao tác thuộc thực thể bằng khóa cặp, component_context giữ endpoint không có thao tác quan sát.

Không đưa locator, tên ca, mốc tiêm, root, fault hoặc nhãn vào API này. Runner T-035 chọn file theo allowlist, kiểm hash, cắt Nezha bằng p3; bộ đọc Node bổ sung chỉ lọc dev và kiểm đồng hồ trước xuất giá trị. Các CSV mức ngày chỉ được so mô tả ngoài bộ dựng.

Môi trường đo dùng Python 3.12, numpy/pandas `py312-pin`; Parquet reader pyarrow có sẵn từ môi trường T-014. Không cài hoặc đổi môi trường trong T-035. Phiên bản và vị trí thực tế ở `results/T-035/runs/day-du-001/environment.json`. Máy khác cần dựng dữ liệu theo `data/README.md`, môi trường theo các manifest môi trường P3 và có reader Parquet đúng phiên bản đã ghi; nếu thiếu, dừng phần đọc Parquet, không bỏ kiểm hash hoặc đổi dataset.

Tại máy đo:

```powershell
$env:PYTHONHASHSEED='0'
& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -B results/T-035/fixture/check.py <tên-run-mới>
& 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -B results/T-035/scripts/run.py <tên-run-mới> --pilot
```

Chỉ chạy lượt đầy đủ khi chi phí pilot dưới trần và có quyền trong SPEC. Tên run phải mới; file kết quả dùng chế độ tạo mới, giữ lượt lỗi. Lệnh của phiên thực tế và thứ tự tiếp nhận nằm trong LOG T-035. `scripts/report.py` chỉ ghép nhãn sau khi toàn bộ đồ thị và thống kê không nhãn đã ghi.

## Messaging v2

Adapter xác minh nghĩa các trường `messaging.broker`, `broker_scope`, `exchange`, `routing_key`, `queue`, `identity_scope`, `identity_scope_verified`, `message_id` trước khi điền. Exchange/routing rỗng khác thiếu. Địa chỉ phát và queue nhận tách riêng. `messaging.destination` cũ chỉ giữ như thông tin legacy: không tự là queue hoặc phạm vi message ID. Cờ scope verified là xác nhận namespace, không là chứng minh chỉ có một producer quan sát.

Cạnh thông điệp có `messaging` (broker, broker_scope, exchange, routing_key, queue) và `queue_metric_address`. Địa chỉ metric chỉ đầy đủ khi có broker + scope triển khai/vhost + queue; không dùng message ID/attempt. Queue không thuộc cạnh producer. Nhiều cạnh mang cùng địa chỉ metric cùng tham chiếu một chuỗi, không nhân bằng chứng. Consumer hai queue cùng operation vẫn tách cạnh sau phép chiếu.

Link message_creation đã xác minh trỏ PRODUCER trong miền và không có thông tin đối nghịch thì nối, dù hai phía có destination/queue khác nhau. Nếu có link xác minh, không fallback bằng ID để che thiếu nguồn hoặc mâu thuẫn. Không có link xác minh mới xét ID trong cùng broker/broker_scope/identity_scope đã xác minh, với một producer; các trường cùng hiện diện còn phải tương thích. Correlation không là bằng chứng nối. `messaging_diagnostics` ghi count/witness vấn đề; đọc cùng unresolved_messages, không cộng các cờ thành tỷ lệ nguyên nhân. Nguồn ngoài cửa sổ không được nối.

`do_thi.builder.edge_key` trả khóa cấu trúc: 5 trường cũ, thêm chuỗi JSON canonical của messaging khi có. `project` trả các khóa này. Consumer API phải giữ phần mở rộng khi so/gộp cạnh; không cắt lại về source/target hoặc destination. Cạnh không messaging giữ schema cũ.

Fixture bổ sung: `results/T-035/runs/sua-n1-001/check_messaging.py`; inputs/expected và thiết kế được ghi trước sửa code. Chạy checker với tên thư mục con mới, xem `--help`. Hồi quy dùng runner cũ với tên run mới trong phạm vi được duyệt; không chạy lại `report.py` để ghi đè graph cũ. So sánh và nguồn tài liệu v2 ở `runs/sua-n1-001/`. Chỉ các fixture mô tả hợp đồng nội bộ; chưa là adapter OTel hoặc bằng chứng runtime FlashTicket.

## Chính sách đầu vào v2.1

Tên thao tác thiếu ở mọi dtype về None trước tạo khóa. ID thực thể quan sát/component và ID thao tác phải thuộc hai miền không giao; va chạm bị từ chối identifier_collision ở build/Prepared và project. Inventory-only được giữ riêng, không tính là nút quan sát. ID đầu ra hợp lệ giữ nguyên.

Các cột thời gian phải hữu hạn, nguyên, không âm và trong int64; kiểm cả phép cộng/đổi microsecond sang nanosecond trước thực hiện, dùng cột ns khi có. Vi phạm báo invalid_time. Kiểu thực thể gộp inventory/span/endpoint: unknown không hạ kiểu đã biết; hai kiểu đã biết mâu thuẫn báo conflicting_entity_type thay vì chọn theo dòng cuối.

Bản trước v2 và phép kiểm bổ sung trong results/T-035/runs/sua-hop-dong-001/. Oracle được ghi trước code; các kiểm K5 phải đọc cùng đáp án đích literal vì hai phép chiếu có thể cùng sai. Đây là sửa hợp đồng/cài đặt, chưa là bằng chứng về hiệu quả RCA.
