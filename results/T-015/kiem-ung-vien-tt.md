# Tập ứng viên trên ba ca dev Train Ticket

Kiểm **3/30 ca dev**, ba ca cố định trong SPEC trước xem điểm; chưa chạy phương pháp trên 27 ca còn lại. Kết quả của **MicroRank-RCAEval sửa đầu vào**, cửa sổ ±600 giây, không phải MicroRank gốc đầy đủ. Cap 1 GB tính cả sao chép là diễn giải bảo thủ của người làm, không phải Minh ra lệnh thu 30→3. Kế hoạch round-robin trong SPEC đã thu hẹp; footer 30 ca chỉ xác nhận schema/quy mô, không thay cho chạy 30 ca. Không suy ba ca này thành coverage hoặc chất lượng detector của toàn dev. Bảng `bang-ung-vien-tt.csv` có 204 dòng thực thể–ca. Mỗi dòng giữ năm tầng: thực thể metric → service trong trace cửa sổ → service trong graph current → thứ hạng đầy đủ → service còn trong 11 operation đầu. Mở rộng phần kiểm dev do Minh quyết; không tự làm benchmark P3 hay phân tích P4.

Script `runs/tt-local/candidate-audit.py` chỉ đọc summary và snapshot của đúng ba ca. Nó tự dựng lại tập ứng viên và tập cạnh từ các quan hệ graph đã lưu; 11 phép so mỗi ca đều đạt (`runs/tt-local/candidate-audit.json`). Không chạy lại phương pháp hoặc đọc dữ liệu thô. Nhãn chỉ được đọc từ `label_after_ranking` sau khi đã kiểm prediction và graph; không dùng nhãn để chọn service hay giải thích trước kết quả.

| Ca | Thực thể metric | Service trong trace | Graph current | Service full | Operation rút gọn → service | Hạng root full / rút gọn |
|---|---:|---:|---:|---:|---:|---:|
| `re2tt_ts-auth-service_cpu_1` | 68 | 27 | 27 | 27 | 11 → 4 | 9 / vắng |
| `re2tt_ts-route-service_mem_1` | 68 | 27 | 27 | 27 | 11 → 5 | 2 / 2 |
| `re2tt_ts-route-service_socket_1` | 68 | 27 | 27 | 27 | 11 → 5 | 2 / 2 |

Nguồn từng hàng: `runs/tt-local/auth/primary-summary.json`, `runs/tt-local/re2tt_ts-route-service_mem_1/primary-summary.json`, `runs/tt-local/re2tt_ts-route-service_socket_1/primary-summary.json`. Tập operation và thứ tự được kiểm lại từ `example.json` trong cùng thư mục. Số full/rút gọn ở đây là service sau bỏ trùng theo lần xuất hiện đầu trong ranking operation.

68 là **thực thể có metric**, gồm service, Mongo/MySQL và dashboard; không coi đó là 68 service ứng dụng. Tên lấy phần đứng trước `_` của cột metric. Cả ba ca có 41 thực thể metric vắng trace cửa sổ; không thực thể nào trong số đó được xếp hạng. Không nối chúng vào đuôi ranking. Lý do là kernel chỉ nhận span, và graph tạo node operation từ span current; metric inventory không đi vào điểm (`src/microrank/graph.py:26`, `src/microrank/__init__.py:71–74,94–102`). Vắng trace có thể do coverage instrument, workload không gọi thực thể, sampling, hoặc cắt cửa sổ. Task không tách các nguyên nhân này bằng số liệu.

Ba graph hợp cả nhóm normal/anomaly đều có 199 cạnh operation và 55 cạnh giữa service. `ts-auth-service` không có cạnh **giữa service**, nhưng vẫn ở thứ hạng full: hạng 9,17,16 lần lượt ở auth CPU, route mem, route socket. Nó có hai cạnh nội bộ: `POST /api/v1/users/login → UserRepository.findByUsername → find ts-auth-mongo.user`; cả ba operation vẫn thuộc `ts-auth-service`. Vì vậy, “isolated service trong graph giữa service” không có nghĩa “không có mọi cạnh operation”. Không service nào trong ba ca không có mọi cạnh operation.

Để kiểm riêng trường hợp hoàn toàn không có cạnh, toy nhỏ không dùng dataset/nhãn tạo hai service, mỗi service có operation cùng tên, mọi parent đều thiếu. Cả hai graph có 0 cạnh operation; cả hai service vẫn có điểm và xuất hiện trong full/rút gọn. Kết quả ở `runs/tt-local/isolated-service-toy.json`, script bên cạnh. Điều đó kiểm hành vi kernel giữ node cô lập, vì node còn nối với trace ở bipartite graph (đồ thị hai phía). Nó không chứng minh một service thực tế không có cạnh sẽ có thứ hạng cao trên Train Ticket.

Ở ca auth CPU, 11 operation đầu chỉ thuộc station, route, train, basic. Auth có mặt trong full nhưng bị **cắt theo số operation**, dù full service rank=9. Đây là hệ quả khác với bị loại vì vắng trace. Code giữ `top_max+6`; mặc định `top_max=5` nên trả tối đa 11 operation (`src/microrank/official.py:231–235`). Adapter cũng lưu full riêng bằng giới hạn đủ lớn và gộp service sau đó (`src/microrank/__init__.py:94–102`). Do đó top-11 operation không phải top-11 service.

Ở hai ca route, root route còn ở cả full và rút gọn, đều hạng service 2. Tập rút gọn gồm station, route, train, config, price. Hạng khác auth phải được đọc từ **detector→nhóm trace→coverage/prior→PageRank/phổ→cắt output**. Luật ít nhất một span bị cờ tạo thêm cơ hội đưa trace dài vào nhóm bất thường. Đếm lại ba snapshot nguyên bằng `scripts/check_review_diagnostics.py` cho:

| Ca | Median normal / anomaly | Mean normal / anomaly | Trace ≥100 span normal / anomaly | Span bị cờ / current | Trace bất thường / current |
|---|---:|---:|---|---|---|
| auth CPU | 5 / 179 | 54,22 / 293,08 | 348/1.326 (26,24%) / 903/1.403 (64,36%) | 5.036/483.077 (1,04%) | 1.403/2.729 (51,41%) |
| route mem | 5 / 179 | 10,40 / 213,19 | 7/1.038 (0,67%) / 1.047/1.277 (81,99%) | 24.188/283.038 (8,55%) | 1.277/2.315 (55,16%) |
| route socket | 5 / 179 | 5,77 / 424,44 | 2/1.130 (0,18%) / 1.167/1.435 (81,32%) | 28.426/615.594 (4,62%) | 1.435/2.565 (55,95%) |

Nguồn: `runs/review-response/trace-length-stats.csv`; không chạy lại phương pháp hoặc đọc raw để bổ sung bảng. Ở auth, 903 trace dài bất thường không chứa bất kỳ operation auth quan sát được. 903 trace chứa station có giao 866 với tập dài; hai tập chỉ bằng số lượng, mỗi bên còn 37 trace riêng. Hợp mọi operation auth vẫn có 439 trace bất thường dưới 100 span. Vì vậy độ dài và loại trace gắn với grouping, rồi thay đổi các ô phổ. Tập node/cạnh hợp giống nhau không buộc điểm giống nhau. Dstar2 không trực tiếp đọc độ dài; prior code còn phụ thuộc occurrence. Chưa có ablation để quy mức ảnh hưởng riêng cho độ dài, operation mix, ngưỡng, prior hoặc graph. Workload drift (thay đổi thành phần tải), thiếu span và tài nguyên dùng chung còn là nguyên nhân khả thi khác chưa kiểm; không dùng vắng auth trong trace quan sát để bác mọi ảnh hưởng của auth.

Control auth nghiêm có 2.814/242.818 span bị cờ (1,16%) và 570/1.433 trace bất thường (39,78%), so với 1,04%/51,41% ở cửa sổ sự cố. Cùng CSV giữ nguồn control `runs/tt-local/auth/two-normal-summary.json`. Baseline khác độ dài/thành phần nên chênh tỷ lệ không đo hiệu quả; control đã là báo giả. Đây là giới hạn của CANDIDATE, chưa chứng minh Dstar2 chủ yếu đo trace dài hơn nguyên nhân lỗi.

Probe auth với 25/26/50/100/101 vòng cố định trước kiểm cho 25 khớp score lưu 0; 26/50/100 đổi top 11, 101 giữ top 11 nhưng đổi full. Ngay 100/101 chưa có bằng chứng hội tụ (`runs/review-response/iteration-probe.json`). Giữ 25 theo code, không chọn vòng theo root rank; không ngoại suy độ nhạy một snapshot thành tần suất toàn dev.

Với tập ứng viên service \(C_i\) của ca \(i\), trần coverage là \(Hit@k_i\le\mathbf1[r_i\in C_i]\), trong đó \(r_i\) chỉ được lấy từ nhãn sau prediction. Trên ba ca đã kiểm, root đều có trong \(C_{full}\), nên trần coverage full là 1 từng ca. Với tập service từ output 11 operation, trần coverage auth CPU là 0, hai ca route là 1. Đây là trần do coverage/cắt output, không phải Hit@k đo được. Trong full auth đứng hạng 9, nên còn cần \(k\ge9\) mới hit; trong hai ca route cần \(k\ge2\). Không lấy trung bình ba ca để đề xuất P3.

Kiểm biên và parent trên toàn cửa sổ được giữ riêng:

| Ca | Span / trace cửa sổ | Span mất parent không-null | Root marker thiếu parent | Trace cắt do cửa sổ | Trace nhiều root quan sát, kể cả mất parent |
|---|---:|---:|---:|---:|---:|
| auth CPU | 957.209 / 5.568 | 402 | 5.567 | 2 | 1 |
| route mem | 572.606 / 4.757 | 0 | 4.757 | 1 | 0 |
| route socket | 1.282.923 / 5.278 | 1.527 | 5.276 | 3 | 5 |

Nguồn là trường `census` và `io_metadata` của ba summary trên. Không có duplicate `(traceID,spanID)` hoặc spanID dùng lại giữa trace trong các cửa sổ này. Số span bắt đầu trước nhưng kết thúc tại/sau mốc tiêm là 11,7,8. Trace/span có thể đi qua biên, nên không được dùng startTime để gọi đoạn trước tiêm là hoàn toàn bình thường. Control nghiêm của runner lọc cả start và end trước tiêm.

Census dùng phép nhận null của pandas, khác audit group ban đầu. Audit graph lúc đầu bỏ sót token `<NA>`, nên nhầm root marker thành missing parent. Đính metadata bằng `scripts/correct_root_audit.py` trên runtime pin đạt cả ba ca; giữ snapshot gốc. Root normal/anomaly sau sửa lần lượt là 1326/1403 ở auth, 1038/1277 ở route mem, 1130/1435 ở route socket; missing parent trong các nhóm current này đều 0. Đây là nhóm **sau mốc**, khác census toàn cửa sổ ở bảng trên. Mỗi ca có cả bốn quan hệ graph mỗi phía khớp chính xác snapshot gốc; do đó đầu vào số, điểm và tập ứng viên không đổi. Nguồn: `runs/root-audit-correction/auth/audit-correction.json` và hai thư mục route cùng tên ca. Không dùng PASS của hai bộ đếm cùng sai làm bằng chứng null đúng.

Đề xuất cho P3 là đánh giá trên inventory đã chốt, nhưng phải báo coverage trước và ghi rõ protocol full hay output 11 operation. Không tự nối service vắng trace, đổi giới hạn hoặc gộp metric infrastructure thành service để tăng điểm. Đây là CANDIDATE **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**. Việc inventory mục tiêu và output nào làm cơ sở Hit@k còn cần Minh chốt; ba ca này chỉ cung cấp dữ kiện cơ chế.
