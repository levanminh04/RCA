# Bàn giao T-039 sau thu nguồn — 16/10/2026

**Task chưa hoàn tất.** Đã tự rà, kiểm pin/input, thu đúng nguồn Minh duyệt và xét lại khả thi. Minh giữ toàn phạm vi T-039; chưa có ngoại lệ thực hiện qua nhiều phiên hoặc quyết định tách. Không lập bản ghi/mapping/graph/đối chiếu, không nghiệm thu hoặc đóng G3.

Đọc `bao-cao-sau-tai.md` trước; nguyên lời Minh ở LOG Phiên 2 và `authorization-20261016.json`. Bản tự rà/proposal trước duyệt tải giữ nguyên mốc lịch sử, không còn là hiện trạng quyền tải. Bản bàn giao trước thu được giữ tại `runs/ket-sau-tai-001/truoc-ket-ban-giao.md`.

Nguồn đã đủ đúng danh sách, hash byte/Git blob/SHA256 đạt. Danh sách/capture ở `runs/thu-nguon-001/acquisition.json`; kiểm lại và profile ở `runs/khao-sat-nguon-001/`. Profile chỉ đếm/scan, chưa là semantic coverage. Registry `nguon.json` ghi đính chính commit→tree riêng tại T-039 theo Minh; pin và registry T-036 nguyên byte.

Còn phải làm đủ SPEC: coverage từng phần của toàn cây và nguồn gián tiếp; bản ghi/owner/provenance/điều kiện; oracle riêng trước code; mapping từ nguồn; dựng/chiếu/đối chiếu mọi graph hiện hành ở hai mức và hai views; lần theo nhóm mismatch và match tương ứng; tự kiểm/chi phí/bàn giao P6/P9. Generated/đăng ký handler, hai biến thể deployment và backend Cart phải được phân biệt. Revision ứng dụng→dataset/image/deployment, producer metadata và nghĩa Node/host vẫn OPEN. Không dùng nguồn cùng pipeline như xác nhận độc lập.

Bước tiếp phụ thuộc Minh: cho phép giữ task qua nhiều phiên, hoặc chọn tách và duyệt SPEC cụ thể trước sửa. Chọn giữ toàn phạm vi để xem lại khả thi sau nguồn chưa tự là ngoại lệ AGENTS §5. Không giảm phân tích để vừa một phiên; không tự chia mã task. Các nguồn tải đã được duyệt không cần xin lại.

Lệnh đọc tiếp: `Get-Content -Raw -LiteralPath 'results/T-039/bao-cao-sau-tai.md'`. Trước dùng số/source, kiểm manifest T-039 và pin T-036/T-035 từ input-verification.json. Không chạy lại script thu/prepare trên run cũ. Chưa cài gói, chạy code ứng dụng, baseline/RCA, mở dữ liệu khóa hoặc commit/push.

Prompt chung + Soát SPEC + G3 trung tính ở `prompt-claude-sau-tai.txt` và cuối LOG; Minh chọn gửi hay dừng, không tự mở lượt review mới. Đề nghị lưu nguyên ba quyết định đã nhận vào DECISIONS theo `de-nghi-ghi-quyet-dinh.md`; chưa có quyền sửa file chung. Nội dung formal report hiện chỉ là provenance, miền và các giới hạn, chưa phải độ khớp hoặc lợi ích RCA.
