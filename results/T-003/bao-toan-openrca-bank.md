# Quyết định bảo toàn OpenRCA Bank trước G3

Codex quyết theo quyền Minh giao Q-47, trước khi đọc số đo ứng viên. Bảo toàn toàn biến thể Bank và bản gốc AIOps Bank nếu xác định cùng lineage; không xem số đo, kết quả từng ca hoặc archive dự đoán agent. Được đọc metadata/schema/đếm nhãn. Không tự chỉ định các bộ còn lại là dev/test hay chọn danh sách thí nghiệm G1.

## Vì sao chọn

README chính thức OpenRCA công bố Bank có metric/log/trace, nhãn gồm root cause component, occurrence datetime, reason; Bank chỉ có entity pod và trace ngang giữa pod, không có cấu trúc triển khai dọc. FAQ xác nhận ý nghĩa parent/child span và timezone nhãn UTC+8. Đây là bằng chứng schema công bố, không phải chất lượng file thật. Bối cảnh ngân hàng khác các testbed TT/OB/SN giúp mở rộng miền đánh giá, nhưng không chứng minh riêng tiêu chí 9.

Nguồn ghim trong results/T-012/runs/run-002/sources/openrca-{README.md,commit.json,tree.json,paper.pdf}; kho chính thức https://github.com/microsoft/OpenRCA. Snapshot README đã đọc lại bởi root. Code MIT không thay giấy phép data; paper có điều khoản dữ liệu riêng cần đối chiếu trong thẻ T-012. Khi quyết Q-49 chưa tải dữ liệu và chưa đếm nhãn thật. Sau REVIEW chỉ đọc metadata/nhãn: [inventory](../T-012/runs/bank-metadata-001/summary.json), [census tái lập](../T-012/runs/bank-label-reproduce-002/census.json); không đọc số đo.

## Phương án khác đã xét

- Nezha OB/TT: census nhãn mạnh và ba nguồn được công bố, nhưng testbed/collector có overlap RCAEval. Cần kiểm file để biết chất lượng và không chọn chỉ vì MIT/code thuận tiện.
- Eadro SN: khác testbed TT, nhãn root/time nhiều, nhưng license data chưa rõ và injector/collector cần so với các họ; vẫn khảo sát thật, không giữ toàn bộ để tránh mọi bộ đều metadata-only.
- LEMMA IT: bối cảnh và scenario mới có triển vọng, nhưng NC/ND mâu thuẫn và trace chưa xác nhận; giữ nó làm bộ duy nhất có nguy cơ không dùng được ở G3. Original/Preprocessed không độc lập; không đọc Cloud rồi mặc định PR chưa nhìn độc lập.
- DeepTraLog: trace anomaly có ích cho task theo trace, nhưng root/time incident chưa chứng minh; chưa thích hợp làm bộ duy nhất bảo toàn cho ranking/root/time.
- AnoMod/OpenRCA2: có provenance/nhãn hứa hẹn nhưng release chưa census lúc quyết; điều này cũng đúng với Bank, không là lý do phân biệt. Chọn Bank vì miền banking và schema nguồn, không vì “phía khác chưa kiểm”. T012 đã kiểm ba archive nhỏ sau REVIEW; kết quả mới không được dùng để kể lại lý do quyết trước số đo.

## Điều chấp nhận chưa biết và giới hạn

Chưa biết tỷ lệ resolve parent, chất lượng đồng hồ/gap, liên kết nguồn, normal, vị trí root, triệu chứng ngoài root hoặc độ phù hợp adapter. Các phần này OPEN tới G3 theo MRP, không dùng mô tả nguồn thay số đo. Công cụ tiêm lỗi/collector gốc Bank chưa xác định nên tính độc lập tiêu chí9 chưa đạt bằng chứng đầy đủ. G1 vẫn phải xét khả năng dùng bộ này và ngân sách, không coi việc bảo toàn là đã chọn dataset thí nghiệm.

Nếu sau G3 dữ liệu không hỗ trợ task, báo giới hạn đúng nhãn/định dạng; không chỉnh thiết kế sau xem test, không tự thay bộ dựa kết quả đẹp. Việc chọn này chỉ nhằm giữ một ứng viên không bị nhìn trong thiết kế.


## Bổ sung sau R3 — 04/10/2026

Đã kiểm Drive inventory và ZIP directory bằng range; chỉ giải Bank/record.csv. Census 136 ca, 14 root, 8 reason, 9 ngày, 52 ô root×reason; [nguồn số](../T-012/runs/bank-label-reproduce-002/census.json). Metadata cho 2.829.139.841 byte tải, 26.400.499.433 byte logical; [directory](../T-012/runs/bank-metadata-001/zip-members.json). Pin id/size/modified/directoryhash/labelhash đúng bản quan sát; Drive có thể thay đổi, chưa whole-archive hash nên chưa immutable data revision. Không tải telemetry để “khóa hash”. RQ3 trên bộ này không kiểm lỗi mã nguồn. Quality, graph/symptom/normal/collector/injector vẫn OPEN tới G3 hoặc cần nguồn; bảo toàn giữ nguyên.
