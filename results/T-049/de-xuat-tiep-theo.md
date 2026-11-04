# Công việc tiếp theo sau T-049

Trạng thái là đề xuất, chưa là SPEC hoặc quyền chạy T-050. Codex làm, Claude phản biện theo kế hoạch hiện hành. Minh còn quyết nghiệm thu T-049 và nền đầu T-050.

## Quyết định để bắt đầu T-050

Đề nghị chốt E1-U + E2-C + E5, z+S1, E3(a)/E3b/E9/T12 tắt, E6a, cạnh quan sát; giữ epsilon=0,05 và alpha=0,01. Nền chi tiết ở [nen-de-nghi-T050.json](nen-de-nghi-T050.json). Cờ đánh đổi của E2 từ WHY-72 vẫn giữ. VC sửa đúng hai ca RE2 do C làm hỏng, nhưng làm hỏng hai ca Nezha; không đổi nền sang VC sau khi nhìn phân tích bổ sung. C-e không phân xử được tác hại khi VC có định danh. Không coi giữ C là đã chứng minh C tốt ở mọi điều kiện.

## T-050 — T9/T10

Câu hỏi T9 là lan truyền điểm theo cạnh bằng E6b có tốt hơn thứ tự cục bộ E6a+S1 trên nền đã chốt không. E6b là ứng viên theo ví dụ của cô và thiết kế T-043, không phải hệ quả tất yếu của kết quả VC/E3b. Chọn theo luật khai trước, không yêu cầu E6b phải thắng.

- Phép chính là E6a+S1 so với E6b, giữ tín hiệu, cửa sổ, tập ứng viên, E1/E2/E5, cổng và điểm đầu vào. E6a+S0 so với E6b chỉ báo kèm theo kế hoạch.
- Lưu nút/cạnh thực sự tham gia PageRank, khối lượng điểm trước/sau lan truyền, nút kế thừa có khối lượng 0, hội tụ, nhánh NO_POSITIVE_MASS và thứ tự dự phòng. Lần theo ca tăng/giảm và ca đúng có điều kiện tương ứng để phân biệt tác động của cạnh với thay quy tắc xếp hạng.
- T10 chỉ mô tả vùng nghi ngờ: root có nằm trong vùng, kích thước vùng và cách xử lý nhóm hòa. Đây là vùng trên cấu hình trung gian; cập nhật lại ở T-052 sau cấu hình cuối. Chưa có nhãn vùng đầy đủ thì không gọi là độ chính xác vùng ảnh hưởng.
- Dùng lại nền T-049, đầu vào và trung gian đã khóa khi kiểm đủ hash và trường phụ thuộc. Cửa sổ thật/giả vẫn theo giao thức 52+30, ba thế giới; không thêm ô ma trận hoặc mở test. Số bản ghi mới và thời gian phải được xác nhận khi soạn SPEC, không suy thời gian từ số cấu hình.

Đề nghị tổ chức phần máy ở EC2 để tránh hàng đợi laptop kéo dài như T-049. Dùng số worker đã được kiểm ổn định làm điểm xuất phát, đo trên phép E6b thực sự trước khi chốt. Đối chiếu dùng lại nền, môi trường và sai số trước khi chuyển phép so sang một máy. Laptop chuẩn bị/phân tích phần độc lập. Đây là đề xuất tổ chức cần được đưa vào SPEC, chưa tự đổi lịch chạy.

Phạm vi ghi đề xuất cho bước soạn SPEC là tasks/T-050-<tên-do-Minh-duyệt>/SPEC.md, LOG.md, results/T-050/ và dòng T-050 STATE. Mã phương pháp đã có phải được đọc và kiểm trước; chưa đề nghị sửa code dùng chung. Phát hiện lỗi cần sửa thì trình đúng file và tác động. Việc ghi DECISIONS/WHY để chốt nền phải có câu chữ và phạm vi được Minh duyệt riêng, không nằm trong quyền sửa báo cáo T-049.

## Phần chưa được T-050 thay thế

Phép 2×2 VC/E5, hiệu chuẩn N1/verdict, đối chứng quan hệ, hiệu quả độc lập, chế độ (b), RE3-OB và FlashTicket vẫn theo nghĩa vụ hiện hành. T-050 không tự trả lời hoặc bỏ các phần đó. Chuỗi kế tiếp theo kế hoạch là T-050 → T-051 (T11/T12/KB) → T-052 (T13 và hồ sơ G3). Hoàn tất các task không tự mở G3/test.

Nguồn là T-043 B2 E6/E7, B4 T9/T10 và Phụ lục C; docs/KE-HOACH-SAU-T047.md mục T-050 và cập nhật hiện hành; docs/MRP.md RQ3/P6/P7. Bằng chứng bàn giao là báo cáo T-049 và runs/dap-phan-bien-001/doi-chieu.json.
