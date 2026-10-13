# Giải mã đầy đủ log trong vùng đã khóa

Giữ union vùng ±60giây quanh mọi điểm/đối chứng hiện hữu; mỗi raw row được đọc một lần. Không mở rộng để tìm kết quả đẹp. Schema source `timestamp, container_name, message`. Container chỉ là literal entity; chưa có alias chuẩn service hay span/trace ID cấu trúc.

Đọc mỗi message, xuất mọi lớp template sau phép thay timestamp/UUID/hexID/số bằng placeholder, giữ chữ/cấu trúc. Đây grouping đọc hiểu, không classifier true-fault. Các token fail/error/exception/timeout/success được đếm từ nguyên message trước normalization, báo observed words và không tự gán vận hành.

Access log được giải mã khi có request trong dấu nháy gồm method/target/HTTP-version, theo sau đúng status3digits và bytes. Giữ method, target, status thật, container và source row/time/digest; đếm nhóm status1xx–5xx. Không xem status2xx là chứng minh toàn hệ khỏe, hoặc4xx/5xx là nhãn sự cố của benchmark. Các layout không khớp giữ riêng; không gán status từ một số bất kỳ hay Java INFO. Tất cả template classes giữ trong output, tổng templatecounts+missing phải bằng toànregionrows; tổng parsed HTTP signature phải bằng parsedrows. Source row+digest chỉ ra message nguyên trạng khi cần xem.

Tách request-boundary/outcome được ghi trên subset accesslog khỏi outcome không có trên các Java/Mongo dòng khác; schema không có traceID/spanID/status field cấu trúc, sampling/drop/clock completeness hoặc chuẩn onset/negative. Kết quả giúp giải thích kênh quan sát và requirements FlashTicket, không tạo nhãn vận hành mới.
