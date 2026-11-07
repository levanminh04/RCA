# Vận hành T-054 — dừng trước G3

Hiện hành: LOG phiên5, manifest-trien-khai-004.json, reports/tu-soat-004/bao-cao.md. Gói thu gọn đã kiểm; chưa LOCKED_G3, chưa main/test. Không chạy lại helper pilot cũ/create-only.

1. Kiểm checkpoint bằng Python main -X utf8 -B results/T-054/runs/trien-khai-004/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-004.json. Chỉ đọc.
2. Đọc de-xuat-khoa-g3.json, failure-policy-g3-candidate.json, de-xuat-ghi-so.md. Chờ Minh xét G3/nguồn/commit; không tự đổi cờ quyền.
3. Sau đúng grant: dựng nguồn runtime/private/label độc lập theo G1/metadata gốc, đủ60TT/34OB và ce_history từng TT; kiểm hash, attest_runtime v3. C-e đủ lịch sử mới tạo job tại t−300, còn lại thêm ce_support gắn source hash. TORAI A map riêng đúng3CSV/mỗi member, đủ3seed, ngoài A4. Không dùng đường dẫn/nhãn làm đầu vào phương pháp.
4. Lập plan bất biến từ matrix/config/env đã khóa: workers2, threads1, budget UNTIL_COHORT_COMPLETE không trần cộng dồn, timeout600s/C-d3 60s, poll0,1s/maxgap<5s nếu Minh duyệt đúng đề nghị. Main M1 seal trước C-d3; lỗi C-d3 giữ main. Ghim source/env/code/plan/authority; p7 run vẫn cần G3+test grant. Không phát plan DEV hoặc mặc định sinh từ hồ sơ cũ thành test.
5. status chỉ đọc; drain dừng phát mới và cho active kết thúc; resume chỉ cùng plan/root, nhận lại PID/token, không chạy đôi. Không auto retry. Lỗi nguồn/adapter/prep/clock hoặc method ERROR chưa phân xử: BLOCKED và dừng phát. Chỉ ERROR operation-mới đã khóa hoặc TIMEOUT đủ pha/monitor mới được tính trượt. Giữ mọi raw/partial/receipt.
6. Theo dõi tiến độ, RAM/đĩa/pagefile, không để máy sleep. Không tạo trần cộng dồn; khi lỗi, không tiến triển/lặp vô tận hoặc hàng chục giờ chưa xong, dừng/báo Minh. Không tự đổi cấu hình/chấm lượt chưa chạy thành TIMEOUT.
7. Đủ A4 và mọi binding/phân loại trước ghép nhãn. Các bảng phải khai support/missing; TIMEOUT không có trung gian thì N/A, không dựng N1/O/vùng=0. RE3 H1/H2/nguồn/adapter còn riêng cho bản cuối; không mở bằng grant94. Không SSH/cloud hoặc commit/push nếu chưa có quyền.

Lô thật2 slot có code snapshot trong pilot-2-worker-001/code. Code cuối bổ sung metadata giám sát và sửa nhánh timeout/mô tả sau lô; final checks riêng, không gọi byte code cuối là byte tạo mọi pilot. Freeze006 là ứng viên để xét khóa, không tự là G3.
