# Bộ dựng từ bản ghi có nguồn và bộ đối chiếu

Hai API build/compare và project giữ nguyên exports, Python3.12 standard library, không nhận nhãn/không tự đọc file. Hợp đồng R1 lịch sử ở results/T-036/hop-dong.md. T037 đã có delta builder SMTP được Minh duyệt, ghi tại results/T-037/hop-dong-smtp.md; comparator trước bản mới vẫn so cấu trúc theo giới hạn ghi ở đó.

Sau khi gói V2 được Minh duyệt và toàn hồi quy đạt, hợp đồng/pin mới là results/T-036/runs/doi-chieu-smtp-001/manifest.json và hop-dong.md. Runner phải nhận đường dẫn/SHA/created_utc từ manifest thực và kiểm module snapshot/live; không lấy HEAD hoặc đổi nhãn output cũ. Snapshot R1/T037 cũ vẫn nguồn của kết quả cũ.

Builder nhận smtp ở hai loại gọi, messaging=null; unknown không tự thành sync. Comparator mới nhận optional call channel; SMTP giữ marker ở endpoints/typed, trace thiếu channel không tự được điền từ static. Typed loại unknown. Context/provenance giữ host/port/TLS/outcome nhưng matching không xác minh authority/TLS hoặc delivery. HTTP/RPC legacy giữ quy tắc cấu trúc đã khai báo. Graph T035 nguyên bản không đổi, adapter P9 muốn phát channel cần quyền/nguồn riêng.

Resource binding/signal không tự thành cạnh runtime; shared metric không nhân mỗi operation. Hồi quy T036/R1/SMTP và T037 full model/fixture, TT1069, OB132 dùng runner nhận pin tường minh ở các run doi-chieu-smtp-001, lưu mọi lượt kể cả lỗi. Chỉ cập nhật bản hiện hành sau tất cả đạt; không suy nghiệm thu task/G3/test/commit. Các trường hợp cần authority/port/TLS hoặc runtime proof phải trình dữ liệu/schema riêng.
