# SMTP V2 đã triển khai và kiểm đủ ba nhánh

Minh duyệt Q-164. Shared221R1/100SMTPbaseline/29V2, FT1598, TT1069, OB132 đều đạt. Cả ba dùng cùng pin.json, manifest/code chung cố định trong run này; completion.json lưu pointer kết quả và số thực. Kết quả hiện hành mới chuyển sau đủ ba nhánh. Snapshot/hợp đồng/manifest T036 gốc và mọi output cũ giữ nguyên.

TT comparator-only khớp toàn kết quả cũ; delta thêm một cạnh SMTP mỗi mức, một key S/static-only endpoints và một unknown exclusion typed mỗi graph. Không đổi trace/mapping/giao hoặc đủ điều kiện typed. OB bằng nguyên toàn132output cũ. FT source/model không đổi; unknown SMTP với trace thiếu channel endpoint numerator1→0 đúng oracle.

Runtime/build/instrumentation/deployment lineage, authority/port/TLS/delivery và các OPEN nguồn giữ nguyên. Chưa xác nhận lợi ích RCA/RQ3/RQ5, chọn P6, nghiệm thu task hoặc mở G3/test.

Các lượt lỗi adapter/TTchecker giữ nguyên trong checks/ và preparation-attempts.json; không thay shared hoặc oracle để PASS. Báo cáo số thực theo cost.json từng nhánh và completion.json, không benchmark cô lập hoặc suy giờ công. Không tải thêm, khôngSMTPnetwork/test/commit/push. Chờ Claude soát và Minh nghiệm thu riêng. Prompt chuẩn ở prompt-claude.txt để Minh chuyển thủ công.
