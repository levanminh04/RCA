# Tự kiểm bản sửa hiện hành

Nguồn kiểm: `results/T-038/runs/sua-r1-20261017-001/source-checks.json` (11 điều kiện nguồn), `model-checks.json`, `results/T-038/runs/sua-r1-20261017-001/checks/full1069-002/verification.json`, `analysis-checks.json` và `final-verification.json` trong run sửa sau bước seal. Manifest bảo vệ nguồn, lịch sử, pin chung và input. Không đổi expected hash để chấp nhận nguồn lệch.

Đã kiểm bản ghi chính thức→build→graph→project→entity-only cùng bản; projection122 hợp entity-only48 bằng170 cạnh entity và không giao. 110 entity/993 operation/139 signal/50 binding, record cũ và mapping giữ nguyên; đồng bộ một mô tả role SMTP lịch sử; relation509→513. Operation edges343 giữ nguyên; thêm4 exclusion do không có operation evidence. Root phép chiếu121 là lỗi chưa tiếp nhận SMTP, đã sửa thành122.

Đủ1069/1069 graph theo index trước sửa và manifest T035:979 entity/90 operation. Tính độc lập từng khóa/members/reason exclusions/phân hoạch chỉ số/mẫu số/null/interval; replay bằng pin chung, lặp/đảo thứ tự/input bất biến và so toàn candidate đã kiểm. Delta từng graph được lưu, không sửa oracle theo kết quả. Operation output giữ nguyên tập/số và chỉ đổi mô tả SMTP; trace và giao của mọi graph giữ nguyên. Đã tổng hợp lại bảng theo family/full/union cùng chains.

Dùng lại các kiểm lịch sử nguồn/coverage/SMTP sau kiểm hash khi đầu vào không đổi; không chạy lại RCA hoặc ba nhánh không bị đổi. Tự kiểm này không thay phản biện chính thức hoặc nghiệm thu. Độ đủ nguồn ngữ nghĩa/runtime, lineage, protocol/binding và lợi ích RCA giữ OPEN theo source-audit và bàn giao.

Sự cố lượt này: công cụ đọc nguồn in lọt credential mặc định do che lọc chưa đủ. Đã báo Minh ngay; không chép giá trị đó vào file kết quả/báo cáo mới, không sử dụng để kết nối. Chi tiết không chứa giá trị tại `results/T-038/runs/sua-r1-20261017-001/incident.json`. Sự cố phạm vi đọc lịch sử vẫn được giữ ở coverage/incident.json, không bị nhận là đã hoàn tác.
