# Ma trận phương pháp × phần dữ liệu — CANDIDATE, chưa duyệt

42 dòng yêu cầu gốc × 40 phần dữ liệu = 1680 cặp. [CSV đầy đủ](04-phuong-phap-x-dataset.csv) có nguồn, tín hiệu cần/có, normal, đơn vị, candidate ceiling, label budget và công sức từng cặp. Không có ô “chạy nguyên trạng”: kiểm chạy trong hồ sơ thường dùng adapter, nên không đồng nhất với raw dataset. Phân loại hiện tại: {'cần adapter': 728, 'chưa kiểm': 825, 'không chạy được': 127}.

“Cần adapter” xác nhận tín hiệu của phần đã xem và mô tả đường chuyển không dùng nhãn; **chưa bảo đảm pipeline mới đã chạy**. “Chưa kiểm” có giả định, trường hợp sai và việc P3 cần làm; không dùng chữ “có file” để suy schema. “Không chạy được” chỉ trong phần tín hiệu đã chỉ định. Không thêm trace giả cho Sock Shop. Chuỗi request latency tạo từ trace là tín hiệu dẫn xuất, không thành metric tài nguyên cùng điều kiện.

Hai hàng DecompRCA chỉ là prior work đã đọc để bàn Retrieval; không thêm vào danh sách RCA đã duyệt. GDN là detector, không RCA. SimpleRCA các rule đơn lẻ là alert nội bộ, không detector streaming đã xác lập.

## Header và chua_kiem

Sáu bảng nguồn đều giữ 16 cột nghiệp vụ và bốn cột provenance. Không có header mismatch. 27 hàng có chua_kiem trong nguồn được giữ nguyên. Mỗi giá trị nguyên bản nằm ở [yêu cầu hợp nhất](yeu-cau-dau-vao-hop-nhat.csv); không điền minimum statistical calibration bằng số dòng chạy được.

## Nhãn và tập ứng viên

Không dùng root gold để thêm một node bị vắng hoặc chọn SLI. P3 cần lập tập metric→service, operation→service, graph-node→service từ telemetry/inventory không nhãn. Báo số ca gold có mặt trước khi accuracy; vắng gold thì Hit@k trần 0. Không có candidate universe đã đo đầy đủ cho các release chưa mở. Root-level mapping ở [bảng V4](trung-gian/dataset_evidence/root-mapping.csv) là evidence/OPEN, không quyết định schema.

## Chi phí

Cột riêng giữ số quan sát và tính chất phép đo. [Runtime đã có](trung-gian/method_evidence/runtime.csv), [nhãn/cửa sổ](05-nhan-va-cua-so.md) và [kế hoạch P3](10-ke-hoach-p3-de-xuat.md) quy ngân sách toàn bộ×seed. Không dùng chi phí làm điểm chọn dataset. Không lấp ô bằng lượt chạy mới trong T020.
