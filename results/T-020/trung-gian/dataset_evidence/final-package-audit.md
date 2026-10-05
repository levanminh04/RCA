# Kiểm ngắn ba tài liệu tổng hợp cuối

Đã đọc toàn bộ `g1-goi-quyet-dinh.md`, `06-phuong-an-dataset-va-chia.md` (tên thật, không có 06-goi-dataset-va-chia.md), và `10-ke-hoach-p3-de-xuat.md`. Chỉ xét phát biểu dataset/split/C9, dùng evidence/census/ledger đã có. Không mở source raw, không chạy phép đo hoặc method mới, không sửa file root, không đổi lựa chọn.

Ba chỗ còn nên thu hẹp hoặc làm rõ:

1. **g1:50 — “Bank khác nhóm so RCAEval”.** Câu này mạnh hơn chứng cứ authors gốc. Có thể nói tác giả bài OpenRCA khác nhóm bài RCAEval; tác giả/đơn vị cung cấp raw AIOps cho Bank vẫn OPEN trong independence-axes.csv. Đề nghị: “Nhóm bài OpenRCA khác RCAEval; nhóm tạo raw Bank và injector/collector gốc chưa khóa.” Không suy cặp đạt trục tác giả từ tác giả gói tái dùng raw.
2. **06:79 — “Số đơn vị độc lập dùng cho resampling là ô”.** Ô root×fault là đơn vị phân cụm đề xuất cho bootstrap, chưa được chứng minh độc lập thống kê. Chính đoạn sau thừa nhận session/workload/ngày có thể phụ thuộc. Đề nghị: “Đơn vị phân cụm đề xuất cho resampling là ô; mức độc lập giữa các ô còn cần kiểm theo campaign/session/ngày.” Các count/cell/CI exploratory đang ghi không cần đổi.
3. **06:73 — nhóm “RE1-SS/RE2-SS/RE2-OB … đã TX2”.** Có thể hiểu toàn RE1SS125 đã TX2, trái bảng B ở cùng file: RE1SS100TX2+25TX1, trong đó15TX1 được đề xuất test. Đề nghị nêu đúng phạm vi “RE1SS có100TX2/25TX1; RE2SS90, RE2OB90 và BAROFSEOB100 đềuTX2”; giữ nguyên quy tắc cả ô chứa TX2 ép dev. Đây là làm rõ FACT tiếp xúc, không thay gói.

Một chỗ diễn đạt nên tránh tạo thêm gate quyền: **06:85/g1:104**, “Minh cung cấp/duyệt nguồn header-only”. V7 đã cho phép first-line khi exact newline/no inflation bảo đảm. Bank hiện thiếu artifact/mechanism bảo đảm điều kiện, không thiếu quyền đọc first-line. Có thể dùng “Cần nguồn/artifact và mechanism header-only đáp ứng V7; nếu cần dữ liệu hoặc thao tác ngoài phạm vi thì trình Minh riêng.” Không cần hỏi lại quyền đã có.

Không phát hiện thêm lỗi dataset/split/C9 quan trọng ở kế hoạch10 trong lượt đọc ngắn này. Các con số chia được trình bày nhất quán với ledger/tables đã kiểm trước đó; lượt này không tính lại split hoặc chứng nhận các ô độc lập. Các giới hạn TX1, chưa đủ C9, nhãn khác task, license/clock/schema và chưa có blind protocol được giữ rõ. G1 vẫn CANDIDATE, các đề xuất còn chờ Minh; audit này không phê duyệt gói.
