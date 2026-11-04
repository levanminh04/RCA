# T-049 — Tự rà và chuẩn bị thực nghiệm

Codex là người làm. Claude là người phản biện chính thức. Hồ sơ này ghi phần chuẩn bị và chạy thử. Kết cục K-b, nền T6 và lựa chọn E3b còn mở.

## Phạm vi câu hỏi

- K-b so E2-C với E2-VC, giữ E1-U và E5 bật. E2 lấy khoảng ngoài span trên cạnh cha–con khác chủ. VC dùng phủ đỉnh tối thiểu của đồ thị cạnh có cờ. Đỉnh thuộc mọi phủ tối thiểu nhận điểm lớn nhất của các cạnh nó phủ. Đồ thị trên 25 đỉnh dùng C. Cặp ở nền thắng phục vụ lựa chọn. Cặp đầy đủ cho biết hành vi khi E3(a) bật. Cần phân biệt dự phòng, không định danh và định danh thật trong phân tích.
- T6 thêm số lần xuất hiện của thao tác theo chủ trong N/A. Cổng đếm dùng thời lượng quan sát trace ở từng thế giới. Tần suất trace giữ nhị thức như bản D1 đã nghiệm thu ở T-046, trong khi log có mốc N dùng hiệu chỉnh phân tán. Kênh tăng vào lớp lan ngược, kênh giảm vào lớp lan xuôi. Tác động có thể đi qua tính hợp lệ, cờ, E5 và thứ tự trong tầng. Muốn phân biệt thay đổi tín hiệu với thay đổi tương quan giữa kênh phân vị và kênh đếm cần soi cả hai phía đổi hạng.
- T-049 phục vụ RQ3 trong phạm vi chọn thiết kế trên dev. Cả hai phép so chính giữ E5 bật và dùng quan hệ. Chưa có đủ tổ hợp để quy tác dụng cho tương tác VC × E5. Đối chứng bỏ quan hệ và quy tắc đơn giản, độ đúng phát hiện, vùng ảnh hưởng trên dữ liệu có nhãn và đánh giá độc lập là các phụ thuộc sau, theo MRP P6/P7. T-049 không lấy độ chênh đồ thị làm tiêu chí chọn thành phần.

Nguồn trực tiếp ở SPEC T-049, T-043 B2/B4/Phụ lục C, DT18 §2, hướng dẫn cô §1, WHY-67/70–72 và Q-236–238. Quyết định dùng nền z+S1 hiện hành chấp nhận cờ trái chiều theo dataset. Cờ ấy vẫn phải có trong hồ sơ khoa học.

## Tự rà và sửa

1. **Số học.** Native có thể tràn ở trung gian dù z cuối hữu hạn. `e4.py` giữ native trên mẫu thường và dùng phân số chính xác để phục hồi mẫu hữu hạn khi trung gian tràn. Chỉ nhận kết quả nếu cả hai điểm biểu diễn được. Giữ hợp đồng S21 khi điểm ngoài miền và lỗi native nếu tổng khóa ngoài miền. Bộ chạy ghi nguyên bản và dừng nếu phát hiện điểm z thực sự ngoài miền. Bản trước sửa và fixture T-053 phân biệt hai tình huống.
2. **Luật chọn.** Helper T-047 tính N1 và kết cục từng thế giới, nhưng giao diện cặp không có hành động cho K-b/T6. Helper T-049 dùng lại phép tính. K-b chờ Minh khi trái chiều, phụ thuộc quan sát hoặc GIÚP mà C-e chưa kiểm được. T6 báo kết cục P riêng và áp mặc định giữ bật khi phụ thuộc quan sát. Trường hành động phân biệt giữ, đề xuất bỏ và trình Minh. Chưa sử dụng helper để chọn trên số dev T-049.
3. **Tái sử dụng.** T1 T-053 có đủ ca, seed, xáo và mốc giả. Dấu vết xác nhận ứng viên không đi vào nhánh phục hồi. Bản tích hợp qua đối chiếu bit của đường native. Hai nền C trong seal T-053 đủ cấu hình, cửa sổ, trạng thái, thế giới và đầu ra trung gian. Số kiểm được ghi ở `tai-su-dung.json#/T1` và `#/K-b`. Tái sử dụng nền C khác máy vẫn cần đối chiếu pilot và khớp đầu vào. Nhánh C không chứng minh hành vi VC hoặc E3b.
4. **Chi phí.** Chi phí nạp ca và tính G3 khi cache nguội phát sinh theo cửa sổ. C và VC trong cùng nền chia sẻ đầu vào phân vị, nên giữ chung tiến trình và cache. Khi cần chạy lại nền, giữ cùng cửa sổ trên cùng máy. Tái sử dụng T1 loại được việc đọc và tính lại 238 bản ghi. Tái sử dụng hai nền C có thể loại thêm 164 bản ghi, tùy điều kiện so máy. Chưa chứng minh có thể thay lượt phương pháp VC bằng replay từ dấu vết cũ. Replay phải dựng được cả kênh và E5/FI, khóa S1, tầng và nhóm hòa.

## Dữ liệu đã ghim

- `o-cham.json#/CP`: tỷ lệ cha có cặp con chồng lấn hơn 1 ms dưới 5% ở hai tập. Không có hàng CP trong ma trận theo điều kiện bước 9.
- `o-cham.json#/E_X`: 17 ô E2-VC và 12 ô E3b lấy từ KS-16 đã ghép nhãn. Đây là các ô kích hoạt theo định nghĩa T0. Số lần VC thực sự định danh và số lần E3b thay tầng/hạng cần đo riêng. Tệp ô chấm tách khỏi đầu vào pha 1.
- `ma-tran.json#/K-b`: bốn cấu hình đã duyệt. `#/T6_conditional` khai cấu hình kế tiếp cho từng kết cục nền. Chỉ một cấu hình bật E3b được dùng cho lượt chọn chính.

## Các nhận xét trước ảnh hưởng T-049

- **T-047 F1 — đúng và đã xử lý ở công cụ mới.** Có thể có kết cục P và cờ trái chiều trong dữ liệu mà giao diện quyết định chưa có hành động. Fixture T-049 đi qua cả hai dạng trái chiều, GIÚP với C-e chưa kiểm được và GIÚP/HẠI/GIÚP. F9/F10 của T-047 là yêu cầu về phạm vi độ đo và cách diễn giải quan hệ. Bảng độ đo chính của T-049 còn chờ pha 2. Việc E6a dùng khóa cục bộ đã đối chiếu tại chuỗi và xếp hạng. E1/E2 vẫn dùng cạnh và E5 vẫn dùng quan hệ để phân loại.
- **T-053 F1–F3 — giữ các giới hạn áp dụng được.** Kênh đếm còn có thể đổi tính hợp lệ, cờ và tầng dù ít khi quyết định điểm max. Cờ trái chiều của gói thắng là căn cứ phải báo riêng theo dataset. Ca E2 thứ hai có dấu vết trong hồ sơ T-053. Có dữ liệu để đối chiếu tiếp, còn phải truy vết trên nhánh VC thực chạy. Hồ sơ T-048 về R0 cũng phân biệt xếp hạng chính với đồ thị còn được dựng cho chẩn đoán. Các nhận xét này định hướng đọc bằng chứng và không đổi ma trận T-049.

## Quyền chạy và bước kế tiếp

Pilot laptop đóng sáu lượt. RE2-TT nặng mất 228,53 giây cho bốn cấu hình, RAM đỉnh 2,11 GB. Cửa sổ này định danh một đỉnh ở cả ba thế giới trên nền thắng. Nezha có cờ E3b mất 16,67 giây cho hai cấu hình và cho 11 STOPPED cùng 3 tăng trong mỗi thế giới. Số đo nằm tại `pilot-laptop.json` ở các nhánh `pilot-laptop-re2-001` và `pilot-laptop-nezha-co-001`. Giữ một tiến trình RE2 nặng trên laptop ở mức RAM đã đo. Pilot này chưa đủ để chọn số tiến trình tối đa trên EC2 hoặc ngoại suy chi phí cho cả ma trận.

Đối chiếu cấu hình chạy chung cache với cấu hình chạy riêng, tắt cache và xáo thứ tự đạt trên RE2-VC và hai cửa sổ Nezha-E3b. Hai nền C trên cửa sổ RE2 nặng cũng khớp bản EC2 đã seal của T-053 về cấu trúc, tầng, cờ và nhóm hòa. Sai khác p và khóa số thực nằm trong dung sai đã dùng ở T-053. Nền C của cửa sổ Nezha đối chiếu cùng máy khớp. Các kiểm nằm ở `runs/hoi-quy-001/so-pilot-*.log` và `so-nen-t053-*.log`. Hai log so sánh đầu giữ lỗi đọc trường mô tả cửa sổ của công cụ. Bản sửa kiểm lại trên dữ liệu đã lưu, không chạy lại phương pháp.

**CHẶN lượt chính.** Q-238 và AGENTS mục 3.8 yêu cầu Minh duyệt dự toán riêng cho EC2 tính phí và lượt dài hơn một giờ. SPEC T-049 còn yêu cầu đối chiếu pilot hai máy trước khi dùng vế nền từ máy khác. Thiếu quyền pilot EC2 và số đo hiện hành của máy đó. Chưa xác định phân bổ chính hoặc lấy dự toán lịch sử làm ngân sách T-049.

Đề xuất duyệt riêng **tối đa 30 phút cho pilot EC2**, dùng đúng instance đã ghi trong SPEC. Làm lại các cửa sổ đại diện đã chạy laptop, đo tài nguyên trước khi chọn số tiến trình và giữ tất cả dấu vết. Tiền máy tối đa khoảng **0,06 USD**, theo 0,1197 USD/giờ từ danh mục AWS Linux On-Demand tại Sydney, chưa gồm lưu trữ và IP. Nguồn tại `runs/hoi-quy-001/gia-ec2.json`. Dựa trên số đo sau pilot, trình dự toán lượt chính với phân bổ cửa sổ, trần thời gian và lượng tệp cần chuyển.

Sau pilot, dùng cùng công cụ đối chiếu trên đầu ra đã xác thực. Nếu đủ điều kiện và có quyền lượt chính, đóng pha 1 K-b rồi mới ghép nhãn dev để chấm. Khi K-b trả hành động chờ Minh, giữ nền ở trạng thái mở và dừng T6 chính. Kết quả thực nghiệm, độ bền, phân tích cơ chế và nền T-050 hiện còn mở.
