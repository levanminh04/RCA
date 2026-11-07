# Gói Minh duyệt để phát main 013

Trạng thái: đã đáp phản biện bản gốc, metadata sửa đang chờ Claude kiểm; chưa có quyền chạy. Một câu “Duyệt chạy main013 theo hồ sơ đã kiểm” sẽ được Codex ghi nguyên văn thành nguồn quyết định, với đúng protocol/source-bundle/manifest của gói này. Nếu code hoặc gói đổi, không dùng lại câu duyệt cho bản khác.

Câu duyệt đó cấp cùng lần nhưng ghi riêng từng quyền sau:

1. Khóa G3(a) cho đúng ứng viên013, cấu hình, ma trận1.640job+2vị trí C-e thiếu hỗ trợ, môi trường, phân lô30/30, một worker trên mỗi EC2 và policy trong hồ sơ. Laptop tối đa hai worker theo RAM/nhóm, TORAI A sau non-A của laptop.
2. Mở đúng60TT+34Nezha-OB test, giữ cửa sổ, U/alias, seed/world/mẫu số; không gồm RE3.
3. Codex làm người quản lý nguồn và evaluator: dùng các bản đồ nguồn/nhãn độc lập hiện có theo ref `source-bundle.json`; kiểm byte nguồn, tạo TT locator mờ bằng hardlink trong `data/locked/rcaeval-re2tt-60/<test-id>/`, ghép nhãn chỉ sau verify snapshot. Không sửa nguồn thô.
4. Chuyển đúng nguồn TT vào `/home/ubuntu/rca-p7/T-054/checkpoint013/data-root/` của từng EC2 theo bảng90tệp/30ca mỗi máy; metadata đủ60ca vẫn giữ toàn cohort. Chỉ code/metadata, grant và đúng phân lô được chuyển, không bản đồ thật/nhãn.
5. Phát và theo dõi main tới hết cohort, có thể dài hơn1giờ, không trần cộng dồn; giữ giới hạn method/monitor hiện hành. DRAIN/resume cùng plan/token/root theo runbook; không retry slot đã hỏng, không sửa thiết kế sau điểm hoặc tắt máy.
6. Cấp nguồn TORAI A đúng cohort60TT và180CSV tác giả cùng metric đã ghim, chạy seed0/1/2 sau phần chính của laptop. Thiếu/sai pin giữ BLOCKED; ca logts thiếu N giữ nguyên; lỗi chưa phân loại giữ attempt và dừng A. A là bảng phụ, không điều khiển A4.
7. Nhận, kiểm toàn snapshot/seal và chấm các bảng/độ nhạy/diễn giải đã khóa, gồm D4, sau đủ A4; giữ kết quả đầu. D1–D4/R3 đã chốt, H1 RE3 vẫn OPEN, RE3 giữ quyền riêng cho bản cuối.

Phạm vi ghi của lượt chạy sau duyệt: `results/T-054/runs/chuan-bi-main-013/{grants,activated-001,execution-receipts,received-main-*}/`, `results/T-054/runs/main-013/`, `results/T-054/reports/main-013/`; nối LOG và DECISIONS/WHY để lưu quyết định đúng lời Minh, cập nhật đúng dòng T-054 trong STATE. Trên EC2 chỉ vùng checkpoint013. Tạo hardlink TT theo công thức trên, không xóa dữ liệu hoặc đổi file thô. Lưu mọi attempt và archive nhận, kể cả hỏng.

Codex sẽ tự ghi nguồn lời duyệt và grant thật, kiểm lại hash/tài nguyên/identity, kích hoạt metadata, kiểm nguồn/chuyển và phát CLI; Minh không phải tự sửa JSON hoặc gõ lệnh. `grant-template.json` hiện có tất cả cờ quyền=false. Một bước bị chặn thì dừng đúng phần phụ thuộc và báo, không tự đổi gói để ép chạy.

Commit/push cần Minh duyệt riêng theo danh sách file. Nó không là điều kiện tự tạo thêm trước main: provenance thực chạy được khóa bằng manifest và code/env pins theo SPEC. Có thể Minh duyệt commit kèm câu duyệt cuối nếu muốn; khi chưa có thì giữ working tree và không commit. Không dùng quyền main để hợp thức hóa quyền lịch sử006.


Khi duyệt lượt dài: kịch bản toàn chuỗi trong cost-scenario.json khoảng9,1/18,3giờ dưới các giả định đã khai; không phải ETA/cận trên, chấm fullcohort chưa đo. Bản Minh xét phải là manifest sau đáp review, không pin gói trước sửa. Chỉ định quản lý nguồn/evaluator và các quyền ở trên chỉ có hiệu lực từ lời duyệt cuối đúng gói.
