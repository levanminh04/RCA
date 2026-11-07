# Đính chính dự toán dung lượng

27,5 GiB là dự toán bảo thủ đã cộng chồng các bản sao; không phải dung lượng đã sinh, không là yêu cầu bắt buộc. Dự toán cũ còn ở `storage-forecast.json` để giữ lịch sử và được thay bằng `storage-copy-accounting.json`.

Đã đo 41 attempt DEV hợp lệ, kiểm hash trước khi dùng, đo nén trong bộ nhớ. Ngoại suy một bản kết quả khoảng 1.713 GiB; nhóm chưa có mẫu riêng dùng max cùng dataset và được đánh dấu fallback. Không chạy main/pilot test để ước tính.

| Mục cần giữ | Dự toán GiB |
|---|---:|
| Kết quả/trung gian native một lần, gồm bản nhận từ cloud; dự phòng 4 lần mức DEV | 6.851 |
| Archive nén truyền từ hai cloud; cùng dự phòng 4 lần | 0.464 |
| Tệp tạm của hai attempt đang chạy | 0.021 |
| M1 seal cho 94 ca | 0.225 |
| Báo cáo/metadata | 0.500 |
| Khoảng trống vận hành | 2.000 |
| Tổng | 10.062 |

Mục đích là phân tích cơ chế từ trung gian, kiểm nguồn–attempt–receipt, nhận kết quả từ cloud và dựng bảng; không cần một clone toàn bộ kết quả chỉ để viết báo cáo. Không cấp thêm cả cohort retry khi chưa có quyền retry. Mọi attempt thật, kể cả hỏng, vẫn giữ. Dữ liệu nguồn hiện có đã nằm trên đĩa và không được tính thêm lần nữa vào dung lượng mới.

D còn khoảng 15.52 GiB tại lần đo cuối. Kịch bản khoảng 10,1 GiB vừa ổ D. Rút đề xuất tạo C:/RCA-artifacts/T-054/main-011/; chưa tạo đường dẫn đó, không xóa/di chuyển dữ liệu. Hệ số 4 là kịch bản, không phải cận trên đã chứng minh. Ca phức tạp hoặc retry được duyệt sau này có thể cần thêm; khi đó xét số thực, không tự xóa kết quả để ép vừa ổ.
