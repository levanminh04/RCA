# Đề xuất commit — chưa được duyệt

Nội dung: `T054: prepare main013 and record approved D1-D4/R3 and C-e exception`.

Chỉ commit sau Minh duyệt. `commit-files.json` là danh sách file ứng viên của delta013, không là lệnh git add cả working tree. `complete-preparation-diff.patch` dùng snapshot đầu phiên, nên không gộp thay đổi có sẵn của Minh. Nhiều file T054 và thay đổi trước013 chưa nằm trong Git; cần xét phần nền chưa stage khi Minh yêu cầu commit, không tự lấy toàn bộ file/untracked hoặc bỏ pin phụ thuộc. Main không tự thêm điều kiện commit: byte code/env/gói được ghim theo SPEC.

Loại khỏi commit mọi archive, raw parquet/CSV, executable/key, partial và file lock; giữ chúng tại chỗ và ghim trong manifest. Không commit bản đồ thật, nhãn private hoặc packet cũ có mapping thật. Không xóa lượt hỏng. Danh sách này không cấp quyền commit/push hoặc mở dữ liệu.
