# RE3 trước G3 — bằng chứng và phần chưa phân xử, checkpoint011

Đây là chuẩn bị nguồn và adapter. Chưa đánh giá RE3; chưa có profile thật đủ điều kiện sử dụng. Không lấy việc cài H2 xong làm bằng chứng dataset đã được diễn giải đúng.

| Mục | Phân loại và bằng chứng | Hệ quả |
|---|---|---|
| Metric time | FACT: card HF đã ghim ghi Unix seconds. Guide tác giả mới mô tả bước lấy mẫu 1 giây cho RE2/RE3 | Không kiểm cadence thực bằng giá trị; không suy r từ mô tả chung |
| Trace startTime/duration | CANDIDATE cho release cũ: microseconds, phù hợp Jaeger và guide converter mới | Chưa có chứng cứ nối exporter lịch sử với đúng HF revision đủ rõ để đóng toàn bộ hợp đồng |
| Log timestamp | OPEN: converter mới xuất timestamp ns và time seconds; release HF có schema 3 cột | Không gán ns cho release cũ chỉ vì converter mới làm vậy |
| Status code | FACT theo lời tác giả: released datasets dùng gRPC, 0 OK; tracets_err cộng mã | Guard đã cho khai miền mã rõ; không tự nhị phân hóa hoặc gọi tổng mã là số span lỗi |
| Inventory quan sát | FACT: hợp serviceName/container_name của đúng 30 ca đã ghim có 11 tên | Không là deployment manifest hoặc bằng chứng đủ alias |
| Metric owner | FACT schema: 28 prefix; 17 tên ngoài hợp owner trace/log quan sát | Không tự xóa prefix hoặc ghép frontend-external vào frontend; cần nguồn/policy có lý do |
| U, alias, r | OPEN ở profile thật | Reader chặn profile thiếu; mọi kết luận RE3 phụ thuộc |

Hợp owner toàn cục: adservice, cartservice, checkoutservice, currencyservice, emailservice, frontend, paymentservice, productcatalogservice, recommendationservice, redis, shippingservice. Không công bố membership hoặc số dòng theo ca.

Quyền B: đúng hai cột owner, 60 lần đọc cột, tổng 1.380.569 byte trong giới hạn 16 MiB. Biên nhận ở `inventory-owner-global.json`: `/completed_column_reads`, `/budget/received`, `/union`, `/measured_signals_or_times_read`. Không lưu raw page/owner rows. Directory ZIP chỉ đọc metadata; không có deployment/collector manifest trong danh sách entry. Không mở file telemetry từ ZIP.

Nguồn chính: [phản hồi tác giả](https://github.com/phamquiluan/RCAEval/issues/64#issuecomment-6659996848), guide và converter ghim revision ở `upstream-main-ref.json`; dữ liệu HF giữ revision ở `hf-current-metadata.json`. Code benchmark đóng băng không nâng theo main upstream. Guide mới tự nói có khác biệt với scripts release cũ; không dùng sự giống tên cột thay provenance.

Khả năng hỗ trợ: M1, BARO, SimpleRCA, TraceRCA, MicroRank, CIRCA có tuyến RE3 trong H2 và kiểm bằng dữ liệu tổng hợp010. TORAI B có thêm kiểm gRPC011; TORAI A và các nhánh không khai trong ma trận RE3 không tự được bật. Chạy thật còn phụ thuộc profile/native units/owner policy, giao thức, ma trận vế, nguồn và quyền RE3 riêng. ERROR chưa biết giữ BLOCKED; không tự tính 0. Đây là hỗ trợ cài đặt có điều kiện, chưa xác nhận trên dữ liệu giữ ngoài.

Cần tác giả/người giữ nguồn trả lời: đơn vị từng cột của đúng HF revision; collector/exporter và cách lọc namespace của metrics; deployment/inventory gốc, ánh xạ frontend-external và các prefix khác; cách xác định độ phân giải quan sát r. Chưa gửi câu hỏi mới ra ngoài.

Hệ quả trước G3: chưa hoàn tất H1 theo điều kiện đã nêu. Có thể tiếp tục xin căn cứ nguồn. Nếu Minh muốn main TT/Nezha trước khi đóng H1, cần quyết định rõ việc để các mục trên OPEN tới trước đánh giá RE3 cuối; đây là thay đổi điều kiện trước G3 đang xin xét, chưa được tự coi là đã duyệt. Không có trở ngại này trong code main TT/Nezha đã tự kiểm, nhưng điều kiện quản trị nghiên cứu vẫn còn.
