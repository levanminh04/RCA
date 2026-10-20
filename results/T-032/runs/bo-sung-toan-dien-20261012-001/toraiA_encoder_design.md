# KT7 — Kiểm encoder còn làm được, trước kết quả

Nguồn T016 có candidate dựng lại mean+3std (ddof1, strict >), không phải generator tác giả được xác minh. T016 cắt raw theo full CSV extent trước fit; nghĩa đó khác raw parquet toàn bản ghi. Kiểm đủ 30 ca dev TT, hai scope khai trước: raw full và raw trong extent của full bảng sourceA. Dùng TT column mapping của T022 đã dùng trong all-column probe, không áp cách gRPC OB cho TT.

Đọc raw theo allowlist và hash; bảng sourceA local phải tái tạo mean/std/max/mean A của mọi cột có điểm trong captured native40rows trước dùng. Giữ mọi cột lệch, không đổi source hoặc chọn threshold để tối đa khớp. Với từng recipe, lưu threshold/counts sai ở từng native bin và span flagged có root descendant; không gọi khớp aggregate là bằng chứng generator gốc.

Phép thứ hai không chọn ngưỡng từ điểm RCA: giả định một strict duration threshold cố định theo cột và observed bin counts nguyên. Tính giao interval [duration không-flag cao nhất, duration flag thấp nhất) của mọi bin. Nếu cắt tie/đếm vượt support/giao rỗng thì ghi infeasible. Nếu feasible, tập top-k duration trong từng bin được xác định dưới giả định này; ghi rõ conditional, không gọi origin đã xác minh. Không gán NaN/ffill source thành observed event; báo table-fill scope.

All-column superset không có root descendant cho 22 cặp cũng cho cận trên0 của mọi flagged subset quan sát được **nếu column/bin→raw span mapping đúng**. Không cần biết spanID CSV để lấy bound này; mapping/source coverage vẫn phải kiểm và khai. Giữ author lineage chưa có source là giới hạn provenance, không bỏ các phép count/interval có giá trị vẫn kiểm được.

Tính laptop với parquet đã có, không chuyển dữ liệu lớn, một worker. Ước3–8phút; không rerun TORAI/RCD/baseline, chỉ thư mục mới.
