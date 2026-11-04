# C1 — đính chính cài đặt và trạng thái kiểm

C1 đã được Minh duyệt, áp đúng và commit một lần theo Q-233. Không còn là patch chưa được duyệt. Receipt: `runs/c1-ap-dung-001/commit.json`; patch đã áp: `runs/de-xuat-c1-003/de-xuat.patch`.

Bằng chứng trước sửa, ca đối chiếu và chuỗi raw → thứ tự tổng → mean/variance/rho → b → p được giữ nguyên tại `runs/t1-xao-dieu-tra-002/` và `runs/c1-ap-dung-001/before/results/T-047/dinh-chinh-cai-dat.md`. Lỗi đã xác nhận ở đó là tính tất định số học theo thứ tự trong cài đặt; không suy rằng hiệu quả RCA hoặc giả định thống kê đã được xác nhận.

C1 dùng tổng bù và thứ tự ô cố định. Giữ công thức, điều kiện phương sai bằng 0, ngưỡng rho, giới hạn b, số hoán vị/seed, G3/D1/S1, mức HẠI, ma trận và luật chọn. Source thực được ghim bằng hash trong metadata, tách khỏi revision nền. Các source lịch sử dùng để tái lập T-046 được đọc theo revision/manifest lịch sử, không đổi manifest cũ.

Kiểm tích hợp hiện tại: T1 đủ 238 lượt, ba seed và xáo hàng trùng byte; 82 đối chiếu tóm tắt R0 T-046 không lệch. Native 52 thật và30 C-e trước/sau C1 không đổi. Hai ca từng lệch p sau xáo nay trùng toàn bản ghi với seed0. Nguồn: `t1.json`, hai audit `runs/c1-delta-*-001/summary.json`, metadata pha1 của các lượt C1. Không miễn bất kỳ lệch nào chỉ vì đã duyệt patch. Khối K đã đủ 832 bản ghi thật và 480 giả; đối chiếu riêng K-đủ với phần tương ứng T-046 đều đạt tại kiem-k-pha1.json của hai lượt K C1. Không mở rộng kết luận thành tái lập toàn bộ A/A hoặc mọi trường native lịch sử.

OPEN: ý nghĩa thống kê và độ ổn định G3 trên chuỗi gần hằng ở mức chính xác máy; sửa thứ tự không xác nhận hiệu chuẩn và không tự thêm epsilon/sàn phương sai. T4/T4b mới, hiệu quả RCA và quyết định G3 vẫn ngoài phạm vi kiểm đã đạt.

Lỗi guard đường ghi là lỗi điều phối riêng trong adapter T-047, đã tái lập và sửa bằng chuẩn hóa tên sau resolve. Nó không làm thay đổi C1 hoặc phương pháp. Chi tiết, đối chứng chặn ngoài OUT và giới hạn suy luận nằm trong LOG và `runs/c1-guard-race-002/kiem-chuoi.json`.
