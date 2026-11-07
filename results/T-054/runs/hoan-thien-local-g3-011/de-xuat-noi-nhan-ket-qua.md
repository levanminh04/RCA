# Nơi nhận kết quả main — xin duyệt, chưa tạo

Số đo local ở011/local-inventory-before.json và lệnh Get-PSDrive hiện hành: D khoảng16,7GB trống; C khoảng53,5GB trống. Dự toán storage-forecast.json từ41attemptDEV đã kiểm hash cho tổng nhận/copy khoảng27,5GiB. Đây là dự toán bảo thủ có margin/temp/retry/copy, không là cận toán học hoặc cam kết kích thước.

Đề xuất:

- Dùng đúng thư mục mới `C:/RCA-artifacts/T-054/main-011/` làm nơi chứa archive nhận, các bản nhận đã xác minh và bản sao kết quả local. Chỉ tạo thư mục này và mô tả phạm vi hiện tại; kết quả thật chỉ được ghi sau quyền main/chuyển tương ứng.
- Code, nguồn sự thật, LOG, manifest, plan và báo cáo vẫn ở repo `D:/RCA-flashticket`; manifest trỏ đúng artifact được phép trên C. Queue tính toán laptop vẫn thuộc results/T-054 trong repo; không chuyển code hoặc dữ liệu nguồn sang C.
- Không di chuyển, xóa hoặc ghi đè dữ liệu sẵn có. Không tạo junction, không sửa quyền truy cập, không tự dọn kết quả. Nếu thư mục đích đã có nội dung thì dừng đối chiếu, không tiếp quản ngầm.
- Phạm vi ghi bổ sung cần lưu SPEC/DECISIONS trước dùng: thư mục C nêu trên chỉ chứa kết quả/receipt/manifest nhận của T054; không là repo nguồn thứ hai. Bản đồ receive-path có đường dẫn rõ, kiểm hash trước chấm.

Hệ quả: chỗ nhận không phụ thuộc khoảng trống hạn chế của D. RAM và đĩa từng EC2 vẫn phải kiểm khi được tiếp tục; chưa có máy nào được kiểm hoặc chép dữ liệu trong bước này. Không suy quyết định storage thành G3/main grant.


## Rút đề xuất sau câu hỏi của Minh

Chưa được duyệt, chưa tạo đường dẫn C. Dự toán cũ cộng chồng bản sao; thay bằng `storage-explained.md` và `storage-copy-accounting.json`. Tiếp tục dùng D theo kịch bản mới, không cần duyệt thêm nơi lưu lúc này.
