# DeepTraLog — kế hoạch kiểm file, chưa được duyệt telemetry

Nguồn chọn: [inventory](runs/run-001/inventory.csv), paper Table 1 và trang tác giả đã lưu. Chọn theo phủ fault case/biến thể và khả năng ghép nguồn; chưa nhìn số đo. **CANDIDATE — chưa kiểm**, chỉ thực hiện sau Minh xác định quyền đọc/holdout và giải quyết giấy phép. Không coi gói Q-45 là quyền mở số đo.

1. Census label/schema bên trong toàn 14 ZIP F01–F14: 124.562.627 byte. Mỗi F là fault case khác; đọc một F không biết root/instance của các F khác. Kiểm member trước, tìm label độc lập, rồi lập mapping root×fault×instance. Chưa biết có label riêng hay không, nên không cam kết census root sẽ đầy đủ.
2. Toàn 10 ZIP `TraceLogData/normal/`: 209.086.987 byte. Cần xác minh thời gian, schema, trace ID và association với F. Tên file ngày và F02–04 chưa đủ để ghép. Tổng raw lỗi+normal: 333.649.614 byte. Khi được phép telemetry, kiểm mọi raw trong phạm vi này để không bỏ root/lặp chưa biết.
3. `GraphData/graph_data.z01` đến `.z07` (mỗi phần 25.600.000 byte) và `graph_data.zip` (2.765.367 byte), tổng 181.965.367 byte. Phải đủ các phần; kiểm CRC/member, schema nhãn và ghép trace ID về raw. Tổng với bước 1–2: 515.614.981 byte. Không suy bậc service từ event graph.
4. `TraceLogData/alllog/alllog.zip.001`–`.004` (mỗi phần 51.380.224 byte), `.005` (7.695.736 byte), tổng 213.216.632 byte. Chỉ cần nếu lineage/coverage log không chứng minh được từ raw F/normal và nguồn; không cần parser/training để làm thẻ. Tổng tối đa bốn nhóm: 728.831.613 byte, chưa giải nén. Danh sách riêng từng normal/F và hash blob có trong inventory.

Không chọn F05 chỉ vì nhỏ nhất. Phủ 14 nhóm case là để tìm nhãn thật; sau đó nếu chỉ được duyệt schema/metadata thì dừng trước hàng telemetry. Nếu Minh giữ ngoài tới G3, chỉ census nhãn/schema đúng quyền, không parent-quality, không graph vị trí dựa số đo và không khảo sát triệu chứng.

Kiểm sau quyền đọc: (trace ID, span ID) và sentinel source; ghép unique/missing/ambiguous theo ca, alias service; graph cha→con đúng ca root; log ID riêng/payload/resolve; clock/normal và rò qua biên; các q theo SPEC khi có metric hợp lệ. Chưa có metric riêng thì ghi giới hạn và đề xuất phù hợp, không tự thay bằng latency.

Dung lượng giải nén và runtime chưa đo. Trước extract cần kiểm member sizes/ổ đĩa; mọi lượt thực thi >1 giờ phải báo Minh. Đây là phụ thuộc thực tế, không thêm cổng. Lệnh tiếp nhận nguồn: `py -3 -B results/T-010/scripts/collect_metadata.py --verify --validate-counts`.
