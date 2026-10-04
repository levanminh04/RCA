# Đối chiếu số học của đối chứng bình thường

Code RHT chính thức chạy lại trên cùng EC2, cùng đồ thị và dữ liệu trả đúng từng điểm của 270 metric. Script độc lập trên EC2 kiểm 1080 giá trị trung gian, sai số lớn nhất 2,22e-16. Script chuẩn bị dữ liệu độc lập kiểm 1080 mảng và khớp. Nguồn: runs/normal-normal-pc-official-capture/, runs/normal-official-independent-linux/, paper/followup-normal-official-raw/.

Đối chiếu với laptop KHÔNG ĐẠT tolerance atol=rtol=1e-7: bốn metric khác điểm. ts-auth-service_latency đổi từ 41,9829 trên EC2 thành 287,4143 trên laptop. Ba metric còn lại lệch nhỏ hơn nhưng vẫn vượt tolerance. Lượt thất bại được giữ tại runs/normal-ec2-local-mismatch-001.json và paper/followup-normal-official-score/comparison.json. Không nới sai số để biến thành đạt.

Với auth_latency, cùng thứ tự sáu parent và mảng X/Y giống từng giá trị, nhưng ma trận hồi quy gần suy biến: một singular value khoảng 2,7e-17. Hệ số hồi quy thay đổi lớn giữa hai máy. Điều này phù hợp với nhạy số học của bài toán gần suy biến. Các nguyên nhân khả thi khác gồm thư viện đại số, thứ tự phép cộng/centering và bố trí bộ nhớ; với auth_workload còn có thứ tự parent khác. Chưa cô lập từng yếu tố, nên không quy duy nhất cho hệ điều hành hoặc thứ tự parent. Ghim phiên bản Python/package chưa bảo đảm cùng bản biên dịch và backend đại số.

Kết luận đối chứng lấy điểm chính thức trên EC2: 93/270 điểm >=3, top ts-security-service_mem=957,1627977273204. Không coi top này là nguyên nhân thật. Cả hai cửa sổ đều trước mốc tiêm, nhưng đây chỉ là đại diện bình thường chưa được xác nhận khỏe độc lập. Một ca không cho tỷ lệ báo nhầm của dataset. Kiểm số học đạt không làm phép kiểm âm tính đạt.
