# Bổ sung G3(a) sau sửa F2/F4

Hồ sơ 003 là ứng viên kiểm lại. [Hồ sơ 002](ho-so-g3-002.md) giữ căn cứ thiết kế và giới hạn khoa học. [Giao thức 003](giao-thuc-p7-a-003.json) thay các đường vào và cập nhật tình trạng F3.

| Điểm | Đường kiểm bản 003 | Bằng chứng |
|---|---|---|
| F2, ca → dữ liệu | Quản lý dữ liệu cấp riêng bản đồ theo hash thành viên từ nguồn được duyệt. `attest_runtime` so từng dòng với cohort G1, mốc, tập file, kích thước, hash và hỗ trợ C-e hoặc trace guard. Runtime phải có biên nhận khớp cả bản kê và giao thức. | Fixture đổi mốc TT/OB, file, kích thước, hash, C-e và trace guard khi giữ nguyên mã ca. Bản kê sai bị từ chối cả khi cấp biên nhận và khi thử dùng biên nhận cũ. |
| F4, vế → bản ghi | `run_slot` nối bản ghi với dataset, ca, vế, phương pháp, biến thể, seed và dấu vân tay. `seal_for_a4` so tất cả lượt đã ghim với ma trận lấy từ cohort và giao thức. Evaluator kiểm lại trước khi đọc nhãn. | Fixture từ chối BARO thay SimpleRCA M4, bản ghi trùng và thiếu lượt. |
| F4, nguồn lỗi → chấm hay dừng | Biên nhận ghi bước chạy. Lỗi chưa rõ nguồn dừng trước seal. Điểm 0 cho `ERROR` phương pháp cần biên nhận phân loại được ghim riêng, liên kết bằng chứng, đầu vào và cấu hình đã xác minh. `TIMEOUT` chỉ được chấm theo quy tắc đã khóa và bằng chứng về bước chạy. | Fixture chặn lỗi cấu hình, lỗi hồ sơ dữ liệu và TORAI hết giờ trong chuẩn bị. Một lỗi phương pháp đã xác nhận giữ seed và cho chênh RR TT là 1/3 trên ví dụ giả. |

[Biên nhận fixture](runs/trien-khai-001/kiem-p7-v3-001/summary.json) xác nhận cơ chế trên metadata và kết quả giả. Bản đồ ca thật chỉ lập theo quyền dữ liệu tương ứng. Bên quản lý phải cấp hash nguồn riêng và hash bằng chứng phân loại từ kênh đã được phê duyệt. Hash chứng minh dữ liệu khớp bản đã ghim, còn tính đúng của nguồn cần được xác nhận khi lập bản đồ và biên nhận.

F3 đạt 12/12 trên hai ca dev ở tuyến baseline sau bước chọn nguồn. TORAI B TT kiểm seed 0. CIRCA và TORAI B OB giữ `UNSUPPORTED`. Biên nhận này có trước guard v3 và áp cho lát cắt đó. [Tổng hợp F3](runs/trien-khai-001/pilot-f3-summary-001.json)

Trước khóa G3 vẫn cần soát bản 003 và hoàn thiện SPEC P7. Các mục gồm quy trình lập bản đồ và chủ sở hữu, nguồn và quyền cấp biên nhận, thời hạn và chính sách hết ngân sách, điều phối đầy đủ ma trận, môi trường và revision, hai quy tắc độ nhạy, ngân sách và quyền dữ liệu. Trong giao thức 003, `timeout_s` để trống và chưa khai pha `TIMEOUT` được tính trượt. Kết quả T13 dev và công thức A4 giữ theo hồ sơ đã có.
