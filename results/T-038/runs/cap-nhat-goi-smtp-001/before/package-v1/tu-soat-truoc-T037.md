# Tự soát độc lập trước đọc đề xuất T-037

Ngày 16/10/2026, trợ lý người làm T-038, không phản biện chính thức.

FACT: pin T-036 build từ chối channel smtp; compare v1 gộp HTTP/RPC cùng type và không có chiều transport cho chặng mail. SMTP client→server khác chặng broker→consumer; không lấy async downstream delivery để gán RabbitMQ messaging. Không ép smtp thành rpc/http.

CANDIDATE tối thiểu: cho channel smtp trên gọi-đồng-bộ/gọi-chưa-phân-kiểu, messaging phải null. Type đồng bộ chỉ khi bằng chứng riêng cho đoạn client→mail-server; TT chỉ thấy JavaMailSender interface + cấu hình, implementation instrumentation chưa ghim, vì thế TT giữ gọi-chưa-phân-kiểu. Context giữ nguyên host/port/TLS và điều kiện nguồn, không nâng port 465 thành TLS verified. Thư đến hộp người nhận và MIME/recipient/message ID không thành node hay edge.

Để không lẫn SMTP với HTTP/RPC ở cùng endpoint, ứng viên cần marker transport SMTP riêng trong khóa cả hai view; chỉ trace có channel smtp tường minh mới dùng marker đó. Trace thiếu transport vẫn nguyên unknown, không lấy từ static. Endpoints vì vậy là đầu mút trong miền SMTP tách riêng, giống phần messaging vốn tách theo vai trò. Đây là đổi hợp đồng phải trình duyệt chứ không áp dụng cục bộ.

Không cần mở rộng address-schema trong gói tối thiểu vì chưa cần so port/TLS/address: context giữ literal và provenance; key chỉ xác nhận owner/endpoints + protocol, không xác nhận TCP authority, TLS, thư hay delivery. Muốn đối chiếu authority/port/TLS chính xác cần đề xuất riêng với telemetry/schema thực tế, không dựng giả dữ liệu benchmark.

Chưa kiểm: candidatecode và hồi quy chưa chạy ở thời điểm ghi mục này; synthetic không chứng minh runtime.
