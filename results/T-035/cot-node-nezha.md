# Cột Node của Nezha-OB

**Kết luận: OPEN về nghĩa host.** Chưa dựng cạnh triển khai đã xác nhận. Có 8 giá trị Node và 11 pod gốc trên các cửa sổ dev. Mỗi pod gắn một giá trị trong phần đã đọc; productcatalogservice có hai pod ở hai ngày. Tính ổn định và tên dạng IP chỉ hỗ trợ tính nhất quán, không xác nhận nguồn định danh host. Nguồn số: `cot-node-nezha.json#/distinct_Node`, `#/pod_to_nodes_all_dev`, `#/cases`.

Reader dùng lại selection/hash/path guard của p3, lọc timestamp theo [t−300,t+300) trước khi xuất PodName/Node, đối chiếu Timestamp với TimeUnixNano và alias tường minh. Không sửa p3; không xuất Log, Node* numeric series hoặc dữ liệu ngoài dev. Thống kê từng phút ở `#/cases/<i>/per_minute` và tên cột Node* ở metric_Node_headers; không dùng chúng làm bằng chứng host riêng.

Đã đọc README, paper và mã phân tích đã tải; inventory mã dưới data/nezha không có mã thu bổ sung. Bài Nezha trang 8 mô tả Kubernetes và Node Exporter; không chỉ rõ cột Node của log được export từ khóa nào, hoặc những giá trị này có scope nào. README và mã analysis không cung cấp mapping host cụ thể. Nguồn trực tiếp và phần thiếu: `#/source_review`, `#/missing`. Không suy rằng dataset hoàn toàn không có quan hệ dịch vụ–máy; chỉ chưa đủ căn cứ nhận mapping này là host.

Để phân xử: cần mã collector/export định nghĩa cột, hoặc mô tả schema liên kết Node với hostId thật. Minh có thể giao nguồn bổ sung theo phạm vi riêng; không tải trong task. P9a cần hợp đồng service/instance/host + thời gian ownership; B16 §4 và §7 đã nêu nhu cầu nhưng runtime chưa kiểm. Không tự sửa câu G2, không gán chuỗi Node* cho service.
