# Rà nhóm khac trong lớp hiển thị — T-065 L5

Cập nhật 2026-11-14T08:46:18.857Z. Chỉ phân tích dữ liệu đã lưu. Không chạy lại M1 hoặc sửa đầu ra.

FACT: khac-audit.json#/inventory có 1.997 dòng ca/service/thao tác trên 22 ca P7, tương ứng 131 khóa service + tên thao tác. Không cộng ba bản thành các mẫu độc lập. Bộ audit kiểm hash dữ liệu L4 trước khi đọc.

Chọn hai ca 5fb8208f (dev2) và a5539fba (T-062) bằng thuật toán phủ tên, không dùng nhãn lỗi, hạng hoặc cờ. Hai luồng raw khớp hash theo manifest gốc. Có 491 span ví dụ phủ đủ 131 khóa tên. Nguồn: khac-audit.json#/sources, /samples, /checks và khac-audit-plan.json.

| Scope raw của span ví dụ | Số khóa service + tên | Thuộc tính quan sát |
|---|---:|---|
| io.opentelemetry.hibernate-6.0 | 68 | kind=1; thread.id, thread.name |
| io.opentelemetry.spring-data-1.8 | 60 | kind=1; code.function, code.namespace, thread.id, thread.name |
| io.opentelemetry.methods | 3 | kind=1; code.function, code.namespace, thread.id, thread.name |

Đầu vào → xử lý → đầu ra: các ví dụ không có messaging.system, db.system/db.system.name hoặc http.*; scope không khớp scheduling/quartz. Hàm xuat-du-lieu.mjs::kind vì thế rơi vào nhánh cuối trả khac. l4-raw.mjs dùng cùng hàm khi bổ sung metadata dev. Cả 491 ví dụ đều tái phân loại thành khac như dữ liệu xuất. Tên như SELECT hoặc Transaction.commit không được dùng để tự gán SQL.

Nhóm khac là nhánh dự phòng của bộ phân loại hiển thị. Nhóm này chứa các scope đủ cụ thể để giải thích loại instrumentation. Nó không đồng nghĩa mất thao tác, thiếu trace, không chấm M1 hoặc service khỏe. Không dùng nhóm này để suy nguyên nhân sự cố. Trạng thái và cờ M1 độc lập với nhãn loai, được giữ nguyên.

CANDIDATE: có thể thêm mô tả scope Hibernate/Spring Data/method bên cạnh khac nếu cần tên dễ đọc hơn. Căn cứ là metadata raw, không suy từ tên hàm. Mặt trái: tăng số nhóm và cần giữ ranh giới giữa span ORM/repository với lời gọi SQL thực. Phương án giữ khac kèm thông tin chi tiết hiện tại vẫn trung thực. Lượt này giữ nguyên nhãn và dashboard; không thêm quyết định thiết kế nghiên cứu.

Giới hạn: đã phủ mọi khóa service + tên hiện thuộc khac bằng ví dụ đã lưu. Chưa đọc lại mọi span của toàn bộ 22 ca để khẳng định mọi lần xuất hiện có cùng scope/thuộc tính. Hai raw stream được đọc hết để kiểm hash; chỉ các span ví dụ được phân tích metadata chi tiết. Bằng chứng đủ cho phần rà nhóm của P3, chưa xác nhận lợi ích của nhãn mới. Không cần chạy lại toàn bộ export/M1. Span link vẫn chưa có dữ liệu và chưa hỗ trợ.

Lệnh: node results/T-065/l5-khac-audit.mjs. Dùng lại khac-audit.json ở lượt tiếp, không chạy lại chỉ vì đổi phiên.
