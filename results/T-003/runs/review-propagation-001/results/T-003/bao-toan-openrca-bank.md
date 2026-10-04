# Quyết định bảo toàn OpenRCA Bank trước G3

Codex quyết theo quyền Minh giao Q-47, trước khi đọc số đo ứng viên. Bảo toàn toàn biến thể Bank và bản gốc AIOps Bank nếu xác định cùng lineage; không xem số đo, kết quả từng ca hoặc archive dự đoán agent. Được đọc metadata/schema/đếm nhãn. Không tự chỉ định các bộ còn lại là dev/test hay chọn danh sách thí nghiệm G1.

## Vì sao chọn

README chính thức OpenRCA công bố Bank có metric/log/trace, nhãn gồm root cause component, occurrence datetime, reason; Bank chỉ có entity pod và trace ngang giữa pod, không có cấu trúc triển khai dọc. FAQ xác nhận ý nghĩa parent/child span và timezone nhãn UTC+8. Đây là bằng chứng schema công bố, không phải chất lượng file thật. Bối cảnh ngân hàng khác các testbed TT/OB/SN giúp mở rộng miền đánh giá, nhưng không chứng minh riêng tiêu chí 9.

Nguồn ghim trong results/T-012/runs/run-002/sources/openrca-{README.md,commit.json,tree.json,paper.pdf}; kho chính thức https://github.com/microsoft/OpenRCA. Snapshot README đã đọc lại bởi root. Code MIT không thay giấy phép data; paper có điều khoản dữ liệu riêng cần đối chiếu trong thẻ T-012. Data chưa tải và nhãn thực chưa đếm.

## Phương án khác đã xét

- Nezha OB/TT: census nhãn mạnh và ba nguồn được công bố, nhưng testbed/collector có overlap RCAEval. Cần kiểm file để biết chất lượng và không chọn chỉ vì MIT/code thuận tiện.
- Eadro SN: khác testbed TT, nhãn root/time nhiều, nhưng license data chưa rõ và injector/collector cần so với các họ; vẫn khảo sát thật, không giữ toàn bộ để tránh mọi bộ đều metadata-only.
- LEMMA IT: bối cảnh và scenario mới có triển vọng, nhưng NC/ND mâu thuẫn và trace chưa xác nhận; giữ nó làm bộ duy nhất có nguy cơ không dùng được ở G3. Original/Preprocessed không độc lập; không đọc Cloud rồi mặc định PR chưa nhìn độc lập.
- DeepTraLog: trace anomaly có ích cho task theo trace, nhưng root/time incident chưa chứng minh; chưa thích hợp làm bộ duy nhất bảo toàn cho ranking/root/time.
- AnoMod/OpenRCA2: thêm provenance mới nhưng còn reuse testbed/corpus và nhãn release chưa xác minh. T012 giữ đánh giá đầy đủ, không loại vì chưa có dữ liệu.

## Điều chấp nhận chưa biết và giới hạn

Chưa biết tỷ lệ resolve parent, chất lượng đồng hồ/gap, liên kết nguồn, normal, vị trí root, triệu chứng ngoài root hoặc độ phù hợp adapter. Các phần này OPEN tới G3 theo MRP, không dùng mô tả nguồn thay số đo. Công cụ tiêm lỗi/collector gốc Bank chưa xác định nên tính độc lập tiêu chí9 chưa đạt bằng chứng đầy đủ. G1 vẫn phải xét khả năng dùng bộ này và ngân sách, không coi việc bảo toàn là đã chọn dataset thí nghiệm.

Nếu sau G3 dữ liệu không hỗ trợ task, báo giới hạn đúng nhãn/định dạng; không chỉnh thiết kế sau xem test, không tự thay bộ dựa kết quả đẹp. Việc chọn này chỉ nhằm giữ một ứng viên không bị nhìn trong thiết kế.
