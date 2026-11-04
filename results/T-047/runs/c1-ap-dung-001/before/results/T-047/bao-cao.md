# T-047 — báo cáo Phiên 5 tại điểm dừng T1

Trạng thái: **chưa hoàn tất; dừng trước khối K để trình C1 và quyền sửa src**. 2026-11-02T14:17:33+07:00.

- Đã tự rà SPEC với DT18, hướng dẫn của cô, MRP và nguồn quyết định; không mặc định SPEC đúng. Bước0/manifest hợp lệ được dùng lại. Pilot hai dataset đạt; thực hiện đủ T1, không đọc nhãn chấm.
- T1: 52 ca × 3 seed, 52 ca xáo hàng, 30 cửa sổ giả. Seed1/2 trùng seed0; xáo trượt tại hai p-value. Đối chiếu 82 tóm tắt R0 thật/C-e với bước10 T-046 không lệch. Đ5 D1 có 58 đơn vị hợp lệ, 0 đổi cờ khi T lệch±1%. Nguồn: `t1.json#/bat_bien`, `#/doi_chieu_T046`, `#/D5_tong`.
- Hồi quy T-047 cuối phiên: 152/152 qua trên dữ liệu giả, không thay kết quả T1. JUnit: `runs/hoi-quy-cuoi-phien5-001/junit.xml`. Bộ cũ và helper bước0 giữ nguyên hash; nguồn chứng cứ ở `kiem-helper.json`, `runs/phien5-tiep-nhan-001/kiem-tiep-nhan.json`.
- QT5: đọc 12 ca tỷ trọng một nhóm>90%, đếm đơn vị/cổng/trạng thái và so ca cùng dataset không cờ; chưa thấy lỗi bỏ nhóm đầu vào. Đây là giải thích tỷ trọng đã ghi, không xác nhận bất thường thật. `runs/b2-t1-seed0-001/qt5-phan-xu.json` và LOG.
- Usage ngắt phần soạn/rà, tiến trình T1 vẫn chạy. Seed2-001 gặp một guard trước nạp; giữ hai ca hoàn tất và dùng lại trong seed2-002 sau kiểm hash/config/seed. Nguồn lỗi guard cụ thể còn OPEN; nó chưa tạo bản ghi phương pháp sai. Mọi ca T1 cuối đã đủ. Không gọi lỗi đó là đã được giải thích hoàn toàn.
- C1 có chuỗi raw → thứ tự tổng → trung bình/phương sai/rho → b → p, kèm đối chiếu. Chi tiết, patch chưa áp dụng và bản đồ ảnh hưởng ở [đính chính](dinh-chinh-cai-dat.md). Không sửa src, h, ma trận hoặc luật chọn.

Phần đã đạt: kiểm cài đặt R0 trên dev và chẩn đoán lỗi tất định thật. Phần chưa đạt: tiêu chí T1 bất biến, K/D2/chọn khối/cơ chế khối/độ bền/độ nhạy/bảng2×2. DT18-NV2/NV3 và MRP P6 chỉ được hỗ trợ ở phần kiểm cài đặt; chưa có bằng chứng chọn khối mới hay hiệu quả RCA. Những nghĩa vụ của task(2), task(3), T4/T4b mới và RQ3/G3 giữ OPEN theo SPEC.

File đổi: chỉ `results/T-047/`, nối LOG và dòng T-047 của STATE. Giữ mọi thay đổi có sẵn; chưa sửa src/SPEC/WHY/DECISIONS, chưa commit/push. Đề xuất commit sau khi Minh duyệt phạm vi và xử lý điểm chặn: `feat(T-047): thêm driver, T1 và chẩn đoán bất biến G3`; chưa thực hiện.
