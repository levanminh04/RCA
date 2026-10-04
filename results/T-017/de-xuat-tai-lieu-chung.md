# Đề xuất tài liệu chung — bản nháp lịch sử đã được xử lý

**Trạng thái 04/10/2026:** Minh chốt theo Q-55. Bản chính thức đã ghi tại docs/WHY.md WHY-17, docs/DECISIONS.md Q-55 và docs/LESSONS.md SL34. WHY bỏ phương án chép điểm và thêm chứng cứ N1/N2/run005; DECISIONS giữ rõ quyền phiên đầu chỉ được SPEC/LOG ghi lại, chưa có prompt gốc trong repo. Những đoạn dưới giữ đề xuất trước duyệt, không thay bản chính thức hoặc chốt cấu hình P3.

Ở thời điểm lập nháp, không sửa tài liệu chung. Các lựa chọn triển khai đã khóa trong SPEC trước dev; các mục WHY dưới đây được ghi thành nháp sau lượt kiểm. Không chọn tham số theo điểm dev. Chưa thay quyết định G1/P3.

## 1. docs/DECISIONS.md — thêm sau dòng cuối

**Cũ → mới:** chưa có dòng → “04/10/2026 — Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026 cho T-017 SimpleRCA; chỉ ghi task/kết quả/src/simplerca/work T017 và dòng STATE; không mở locked, không commit/push.” Mã Q do Minh quyết, không tự cấp trong file chung.

**Vì sao:** lưu quyền và giới hạn ngoài chat. **Phụ thuộc:** provenance SPEC, không phải duyệt tham số phương pháp hay số kết quả.

## 2. docs/WHY.md — đề xuất thêm mục “Các quy ước M4 SimpleRCA của T-017”

**Cũ → mới:** chưa có mục → nguyên văn nháp dưới. Trạng thái Đề xuất (G1), chưa cấp WHY-number để tránh xung đột các phiên khác.

> Chọn một bản cài độc lập của mô tả §3.1.2, đặt tên “SimpleRCA (M4, quy ước T-017)”. Vì sao: ba entrypoint tác giả và lớp SimpleRCA riêng đều dùng luật khác bài; việc gọi tên giống nhau không định danh được code sinh bảng 2. Phương án đã xét: chạy nguyên code nhánh rcaeval, dùng lớp SimpleRCA riêng, hoặc chép điểm công bố; các phương án đó không thực hiện yêu cầu Q37/Q38 cài theo bài. Bằng chứng: doi-chieu-code.md, manifest ba revision và PDF FSE trang5. Kết luận phụ thuộc: mọi số T017 chỉ nói về bản M4 này, chưa tái lập đúng chương trình tác giả.

> Metric mặc định dùng mean+3std với ddof0 và upper tail strictly >. Vì sao: bài nêu 3sigma hoặc P95 mà không khóa lựa chọn; 3sigma cho một công thức xác định và không dùng nhãn. Đây không phải thống kê robust trước ngoại lệ dù bài dùng từ robust. Phương án khác P95 đã chạy trên ca ví dụ; không chọn cấu hình theo accuracy. Không lấy trị tuyệt đối vì bài nói exceeds; điểm giảm không tạo alert. Bằng chứng: SPEC khóa trước dev, core.py, unit-tests và sensitivity. Kết luận phụ thuộc: số cảnh báo và thứ hạng M4; chuyển sang P95 hoặc two-sided tạo biến thể khác.

> Một giá trị metric vượt ngưỡng là một alert; cộng tất cả điểm trong cửa sổ (events). Trace và log mỗi modality một phiếu/service. Vì sao: diễn giải trực tiếp “current value” và “number of alerts” của bài, không thêm trọng số riêng. Phương án khác mỗi metric một phiếu (channels) cũng phù hợp một cách đọc của bài; đã kiểm riêng. Bài không định nghĩa đơn vị alert hay cách tổng hợp qua thời gian, nên chưa xác nhận events là cách tác giả chạy. Bằng chứng: hai cấu hình trong sensitivity và công thức hồ sơ. Kết luận phụ thuộc: score tăng theo số cột/tần suất/độ dài; không so score thô giữa các dataset. Alert count lớn có thể do persistence hoặc nhiều kênh tương quan, không chỉ do nguyên nhân mạnh.

> Trace dùng P95 tuyến tính/service trong từng cửa sổ, một phiếu nếu P95 incident>3P95 normal. Vì sao: đúng mức service và ví dụ3x của bài; không dùng cây span, parent-child hay đồ thị. Phương án khác factor2/4 đã kiểm nhưng không chọn winner. Không đổi đơn vị duration khi lấy ratio vì cùng nguồn/cùng đơn vị; unit vật lý của parquet vẫn OPEN ở T002. Bằng chứng: example score/quantile độc lập và source §3.1.2. Kết luận phụ thuộc: bản này chấm span durations gộp theo service, chưa định danh service latency end-to-end của tác giả khi nhiều operation/span nội bộ.

> Log dùng substring ERROR/FAIL/EXCEPTION không phân biệt hoa thường, một count/dòng, một phiếu nếu count>0. Vì sao: 0 là ngưỡng tối thiểu tường minh để kiểm rule; bài không công bố ngưỡng. Đây không bảo đảm “sudden spike” hay false-positive đã hiệu chỉnh. Phương án khác count>1/>10 đã kiểm tổng hợp; trên ca ví dụ thiếu log nên kiểm dữ liệu thực đó không phân xử được log threshold. Kiểm thêm ca thứ hai theo allowlist, có log: ngưỡng0/1/10 cùng một entity nhận phiếu và score/ranking không đổi; count được tính lại độc lập. Bằng chứng: known-answer tests; ca cpu1 thiếu log được giữ; runs/supplement-001/summary.json. Kết luận phụ thuộc: thứ hạng M4 có thể tăng do log lỗi nền, từ ghép như failure, hoặc quy mô lưu log; kiểm một ca không xác nhận calibration; G1 cần chốt dùng quy ước nào nếu đưa vào P3.

> Cửa sổ ±300s và so riêng ±600s trên ca ví dụ; mốc tiêm chỉ đưa vào adapter biết trước thời điểm. Vì sao: tái dùng cấu hình kiểm T005, không tự chốt độ dài P3 theo Q54. Phương án khác toàn ca hoặc onset tự phát hiện cần giao thức khác; không giả định có detector SimpleRCA vận hành. Bằng chứng: injection-manifest kiểm lại hash nguồn T002, run progress, sensitivity. Kết luận phụ thuộc: số T017 thuộc known-incident mode; không dùng để đo tự phát hiện/độ trễ onset.

> Ứng viên là union service quan sát được trong hai cửa sổ; giữ tên mặc định, chỉ alias tường minh từ schema. Vì sao: root có thể chỉ hiện ở một modality; lọc theo root hoặc danh sách service bị tiêm là rò nhãn. Regex pod từng làm nhầm tên database, đã bỏ bằng regression test và rerun004. Phương án khác giao ba modality bỏ mất ứng viên có dữ liệu thiếu; suy tên bằng regex không được chứng minh trên schema. Kết luận phụ thuộc: thứ hạng và denominator service; absent root sau chấm không được lén thêm vào phương pháp.

> Missing channel ghi unavailable; log bảng rỗng là0; normal metric≥2 finite, trace≥1 span/phía; bỏ NaN/inf có counters, không ffill hoặc floor. Vì sao: không chế tạo quan sát và không đưa dữ liệu tương lai backward vào baseline. Phương án ffill hoặc floor làm đổi count/threshold ở constant/missing. Bằng chứng: test missing/std0/negative-duration và counters run004. Kết luận phụ thuộc: min points chỉ là điều kiện tính toán, không bảo đảm ngưỡng ổn định thống kê.

> Tie groups giữ đúng score; thứ tự lexical chỉ hiển thị; chấm fractional Hit và expected reciprocal rank trong nhóm hòa, kèm bounds. Allzero abstain. Vì sao: không biến thứ tự cột/tên thành chứng cứ root. Phương án optimistic hoặc pessimistic báo bounds nhưng không dùng chọn cấu hình; paper không nêu tie treatment. Bằng chứng: synthetic ties, output và evaluation separate sau serialize. Kết luận phụ thuộc: không so điểm tie-aware của nhóm trực tiếp với paper khi paper chưa rõ cách xử lý hòa.

**Lý do ghi nháp:** task không được sửa WHY chung. **Kết luận phụ thuộc:** mọi kết quả M4 ghi “chờ WHY” ở hồ sơ và kiểm đúng đắn. Minh có thể duyệt hoặc chọn quy ước khác ở G1; lúc đó phải chạy lại trên phạm vi đã chia hợp lệ.

## 3. docs/LESSONS.md — đề xuất bổ sung sự cố adapter T017

**Cũ → mới:** chưa có mục → “T017: regex suy pod từ tên làm gộp nhầm database hợp lệ (ts-assurance-mongo→ts). Kiểm tên bằng dữ liệu/schema, dùng alias tường minh; kiểm điểm trung gian và giữ/rerun mọi lượt bị ảnh hưởng.”

**Vì sao:** lỗi đã có bằng chứng và đã sửa, không phải nguy cơ giả định. **Phụ thuộc:** cách dựng adapter các dataset khác; không thay luật repo hay thêm cổng.

## 4. Chưa đề xuất chọn dataset, split, detector hoặc đồ thị

Không có. Type I/II là luật mô tả của tác giả, dùng nhãn injection/root/fault; chưa đủ đặc tả để tự tính đúng tỷ lệ. Số30dev không quyết định G1.
