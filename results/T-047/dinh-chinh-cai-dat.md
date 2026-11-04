# C1 — đính chính cài đặt và trạng thái kiểm

C1 đã được Minh duyệt, áp đúng và commit một lần theo Q-233. Không còn là patch chưa được duyệt. Receipt: `runs/c1-ap-dung-001/commit.json`; patch đã áp: `runs/de-xuat-c1-003/de-xuat.patch`.

Bằng chứng trước sửa, ca đối chiếu và chuỗi raw → thứ tự tổng → mean/variance/rho → b → p được giữ nguyên tại `runs/t1-xao-dieu-tra-002/` và `runs/c1-ap-dung-001/before/results/T-047/dinh-chinh-cai-dat.md`. Lỗi đã xác nhận ở đó là tính tất định số học theo thứ tự trong cài đặt; không suy rằng hiệu quả RCA hoặc giả định thống kê đã được xác nhận.

C1 dùng tổng bù và thứ tự ô cố định. Giữ công thức, điều kiện phương sai bằng 0, ngưỡng rho, giới hạn b, số hoán vị/seed, G3/D1/S1, mức HẠI, ma trận và luật chọn. Source thực được ghim bằng hash trong metadata, tách khỏi revision nền. Các source lịch sử dùng để tái lập T-046 được đọc theo revision/manifest lịch sử, không đổi manifest cũ.

Kiểm tích hợp hiện tại: T1 đủ 238 lượt, ba seed và xáo hàng trùng byte; 82 đối chiếu tóm tắt R0 T-046 không lệch. Native 52 thật và30 C-e trước/sau C1 không đổi. Hai ca từng lệch p sau xáo nay trùng toàn bản ghi với seed0. Nguồn: `t1.json`, hai audit `runs/c1-delta-*-001/summary.json`, metadata pha1 của các lượt C1. Không miễn bất kỳ lệch nào chỉ vì đã duyệt patch. Khối K đã đủ 832 bản ghi thật và 480 giả; đối chiếu riêng K-đủ với phần tương ứng T-046 đều đạt tại kiem-k-pha1.json của hai lượt K C1. Không mở rộng kết luận thành tái lập toàn bộ A/A hoặc mọi trường native lịch sử.

OPEN: ý nghĩa thống kê và độ ổn định G3 trên chuỗi gần hằng ở mức chính xác máy; sửa thứ tự không xác nhận hiệu chuẩn và không tự thêm epsilon/sàn phương sai. T4/T4b mới, hiệu quả RCA và quyết định G3 vẫn ngoài phạm vi kiểm đã đạt.

Lỗi guard đường ghi là lỗi điều phối riêng trong adapter T-047, đã tái lập và sửa bằng chuẩn hóa tên sau resolve. Nó không làm thay đổi C1 hoặc phương pháp. Chi tiết, đối chứng chặn ngoài OUT và giới hạn suy luận nằm trong LOG và `runs/c1-guard-race-002/kiem-chuoi.json`.

## Đính chính sau phản biện — Phiên 7

**F1, thiếu nhánh báo cờ:** `scripts/pha2_t047.py::defaults` lấy lý do trình ở bước chọn, xung đột và phụ thuộc quan sát ở bước 8, nhưng không lấy `buoc8/P/trinh_Minh`. Vì vậy `khoi-k.json#/mac_dinh_ap` rỗng trong khi `#/buoc8/P/trinh_Minh` chứa E5. Đây là lỗi báo thiếu cờ, không là chứng nhận E5 đã được phân xử. Bộ chọn vẫn trả về E1+E2; thêm E5 trên nền ấy trái chiều theo dataset. Phải trình Minh trước khi dùng làm nền task (2).

Gói sửa này chỉ đính chính văn bản và nguồn số. Giữ nguyên helper, JSON gốc và luật; chưa sửa lỗi helper hoặc tự đặt cách xử lý nhánh trái chiều còn thiếu trong bảng mặc định. Minh cần quyết nhánh này trước phần phụ thuộc của task (2).

**F6, nhầm lý do dừng với nguyên nhân duy nhất:** giữ nguyên hai bản `runs/c1-method-analysis-e1-e2-001/analysis.md` dòng 13 và `runs/c1-method-analysis-e3-e5-001/analysis.md` dòng 57 làm lịch sử. Hai câu “chỉ vế C-e/mốc giả gây HẠI” sai: E3+E5 → E1+E3+E5 và E2+E3+E5 → E1+E2+E3+E5 đều vẫn HẠI khi bỏ N1. Luật dừng ở lý do đầu tiên khớp; trường `ly_do_hai_rieng` không liệt kê mọi điều kiện có thể dẫn đến HẠI ở các bước sau. Đường tính N1 đã kiểm giải thích vì sao vế này kích hoạt, không loại trừ tổn hại từ điểm xếp hạng.

**F7/F8, nhật ký và trạng thái:** đã nối các lượt nhìn số sau Phiên6 với cờ ghi muộn cho hai lượt chat chỉ đọc, không bịa thời điểm cũ; sửa ba đoạn báo cáo về trạng thái, dùng nền và nghiệm thu. Chưa đề nghị nghiệm thu hoặc dùng nền task (2); chờ kiểm diff và Minh quyết các phần còn mở. Tái lập số bổ sung ở `runs/dap-phan-bien-001/kiem_dap_phan_bien.py`, đầu ra `ket-qua.json`; bản trước sửa giữ trong `before/`. Không chạy lại M1 hoặc thay công thức/ngưỡng/ma trận/luật.
