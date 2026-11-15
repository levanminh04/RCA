# Đính chính kịch bản v1 — parent không được xuất

FACT phát hiện 12/11/2026 ~22:43Z. Kịch bản v1 tự gửi traceparent với trace ID/span ID ngẫu nhiên để đối chiếu request. Không xuất span client tương ứng. Đây là lỗi của L1: gateway nhận context có cha không tồn tại trong kho, làm sai dữ liệu phục vụ R-09. Không quy lỗi này cho instrumentation ứng dụng.

`parent-v1-vs-khong-header.jsonl`: trace v1 mẫu `206402e5dba5c8219b11fb79cdbdcfb0` có 17 span, SERVER `GET event` mang parent vắng và không có root. Trace probe không gửi traceparent `b10d3b381a35edf1eba152ead094705e` có 6 span, SERVER gốc, không có parent vắng. Đây là phép kiểm cơ chế trên hai trace, không phải thống kê toàn bộ các trace.

Giữ nguyên pilot `l1p20261112a` và lượt 10 phút `l1r20261112a`: số giao dịch/lưu lượng vẫn là quan sát thật, nhưng không dùng như cấu hình chuẩn cuối hoặc bằng chứng R-09. Lượt `l1r20261112b` dừng sớm lúc phát hiện; giữ container, raw JSON/CSV, summary, log và manifest. Không diễn giải lỗi do dừng thành lỗi phương pháp. Trong lượt b còn có 6 request đọc kiểm ID của L1; chúng được tách bằng ID khi đối chiếu.

Sửa: bỏ header traceparent khỏi k6. Chỉ đọc `X-Request-Id` và `X-Correlation-Id` ứng dụng trả về; nối với log gateway bằng requestId trước, correlationId chỉ khi có đúng một log tương ứng. Event-service có requestId riêng trong response, nên dùng correlationId hiệu lực được gateway ghi lại; không giả sử requestId của mọi downstream trùng gateway. Không gửi tên ca/nhãn/mã lượt, không sửa ứng dụng.

Gateway exporter cũng nhận đủ completed/failed/rejected/cancelled, để không bỏ các response lỗi trong các lượt sau. Bằng chứng lưu lượng v1 không bị sửa. Analyzer giữ hỗ trợ đọc traceId của v1, dùng ID trả về cho v2.

Phạm vi kiểm lại: chỉ kịch bản tải và phép xác nhận phụ thuộc (pilot 5 phút + 2 lượt 10 phút của source cuối). Không tạo lại tài khoản/sự kiện/mock, không redeploy. Lý do phải chạy lại: header thay đổi cấu trúc trace của mọi request, nên bằng chứng cũ không xác nhận telemetry đầu vào cuối. Chi phí thêm 25 phút lịch tải, từng lượt dài nhất 10 phút. Bản mới bắt đầu ở `l1p20261112v2`; chưa báo đạt trước khi đủ đầu ra.
