# Đề xuất làm rõ hồ sơ — không sửa hai bản nháp

Kiểm ngày04/10/2026. Người làm đang tích hợp hồ sơ chính. File này chỉ ghi nội dung đề xuất; không sửa draft/src/LOG/STATE. Hai vấn đề dưới là phạm vi adapter và đường incident telemetry, không phải phát hiện nhãn root đã được đưa vào score.

## 1. PC scorer helper dùng identity adapter theo suffix T-014

**Nguồn kiểm.** `src/circa_kien_truc/scoring.py:28–32` gọi `metric_mapping(graph.nodes)` rồi từ chối mọi row unmapped. Hàm dùng chung với kiến trúc, không chỉ với structural graph. `builder.py:8–24` nhận danh sách suffix workload/cpu/mem/socket/diskio/latency/quantiles/error và cắt service theo suffix dài nhất. Đây là adapter cho schema RCAEval đã kiểm ở task, không phải parser service_metric tổng quát. PC cần bảng metric, không cần T/S/L/E để học; việc gọi mapping ở scorer là để tạo Node(entity,metric), không đưa metatype vào PC.

**Đoạn hiện tại.** `paper/ho-so-circa-pc-draft.md:94–95` mô tả đúng parser gốc RCAEval và mismatch node_names/time. `§9` yêu cầu identity lossless nhưng chưa nói helper thực thi của T-014 đang có danh sách suffix hữu hạn. Người đọc có thể tưởng arbitrary tên `a_b` đều được helper chấm.

**Đề xuất chèn sau đoạn node_names ở §5:**

> Trong lượt T-014, graph_from_pc giữ nguyên tên cột, còn score_graph tạo Node bằng metric_mapping dùng chung với kiến trúc (`src/circa_kien_truc/scoring.py:28–32`). Hàm này chỉ nhận suffix nằm trong bảng builder của T-014; metric khác bị báo unmapped. Metatype T/S/L/E không được dùng để học PC hoặc chấm RHT ở nhánh PC. Đây là identity adapter theo schema RCAEval đã kiểm, không phải scorer wrapper nhận mọi tên service_metric. Nó còn giữ được service có underscore nhờ suffix dài nhất, khác parser split('_')[0:2] của RCAEval gốc. Với ca Train Ticket đã chọn, tất cả tên có đúng một separator nên identity của hai cách khớp; bằng chứng ở paper/pc-source-alignment.json. Đổi dataset cần viết/kiểm adapter lossless theo schema trước khi dùng.

**Đề xuất nối ở §9:**

> Với helper T-014, identity còn phải thuộc tập suffix đã khai báo; có tên service_metric hợp cú pháp chưa đủ. Không suy kiểm schema Train Ticket thành phủ mọi schema RCAEval hoặc mọi metric Prometheus.

**Vì sao và kết luận phụ thuộc.** Hồ sơ đầu vào/dataset portability cần điều kiện chạy thực tế, không chỉ điều kiện lý thuyết. Không ảnh hưởng số ví dụ đã chạy: check identity lossless/names/candidates PASS trên ca chọn. Chưa kiểm một helper identity tổng quát cho schema mới; làm ngoài phạm vi thiết kế adapter hiện tại sẽ cần lựa chọn riêng.

## 2. Architecture call graph trước mốc; metric preprocessing dùng cả sau mốc

**Nguồn kiểm.** `results/T-014/scripts/run_examples.py:12–16` ffill/đổi latency, cắt300 điểm trước và300 điểm từ mốc trở đi rồi gọi preprocess. `:34` build_graph nhận clean.columns. RCAEval `io/time_series.py:99–106` drop_constant trên toàn bảng được truyền vào và convert_mem. `builder.py:63–69` dùng columns đó tạo mappings. Empty-meta forwarding của CIRCA còn phụ thuộc metric nào hiện diện (`structural.py:295–303`). Vì vậy drop cột trên600 điểm có thể đổi candidate coverage và projection/parents, dù nguồn call edges chỉ là trace trước mốc.

**Đoạn cũ — §1:**

> Khác CIRCA-PC, nguồn graph không học từ tương quan metric của incident. Nó dùng service call graph và luật ánh xạ metric vào bốn meta metrics (nhóm ý nghĩa): Traffic (lưu lượng), Saturation (mức dùng tài nguyên), Latency (độ trễ), Errors (lỗi).

**Đoạn mới đề xuất:**

> Khác CIRCA-PC, quan hệ gọi service lấy từ trace trước mốc và các hướng meta-metric lấy từ cấu hình, không học từ tương quan metric của incident. Tuy vậy graph metric cuối của ví dụ T-014 dùng cột sau preprocessing600 điểm gồm300 trước/300 từ mốc trở đi. Drop_constant theo toàn600 điểm quyết metric hiện diện; projection và tập parents vì vậy có thể mang thông tin telemetry sau mốc. Chỉ phần call trace được xác nhận pre-mốc. Luật ánh xạ dùng bốn meta metrics: Traffic (lưu lượng), Saturation (mức dùng tài nguyên), Latency (độ trễ), Errors (lỗi).

**Đề xuất chèn trước Bước3 — ánh xạ schema:**

> Với ví dụ T-014, trước mapping dùng cùng protocol metric như PC: bỏ latency-50, đổi latency-90 thành latency, xử lý nonfinite bằng ffill/prefix0, rồi preprocess trên600 điểm quanh mốc. Cột hằng trên600 điểm bị bỏ; memory đổi byte→MB. RHT fit chỉ111 normal points nhưng danh sách cột này không được xác định chỉ từ train. Đây là lựa chọn input trong tái lập có mốc, không phải bằng chứng toàn graph kiến trúc độc lập với incident telemetry.

**Đề xuất thêm vào §8 — đường nhãn:**

> Window selection và drop_constant/column membership dùng telemetry sau mốc. Đó không phải root label trực tiếp, nhưng là đường thông tin incident vào graph metric/candidates; cần phân biệt với call graph dựng từ pre-mốc trace. Khi tự phát hiện phải dùng mốc ngoài và ghi rõ thời điểm có thể biết candidate schema.

**Vì sao và kết luận phụ thuộc.** Câu “graph pre-mốc” chỉ đúng cho call graph trong lượt ví dụ, không đủ cho mọi nguồn quyết graph metric. Hai yếu tố có thể giải thích thay đổi projected edge: thay call trace coverage hoặc thay metric membership. Không được quy mọi thay đổi edge cho incident correlation/label leakage khi chưa tách hai yếu tố. Ví dụ arithmetic và checks hiện tại giữ nguyên; điều kiện đánh giá online/prospective và CSV đầu vào cần câu chính xác hơn.

## 3. Normal đối chứng: ghi đúng pseudo boundary

Đối chứng `runs/normal-normal-architecture-pretrace/` có call trace **trước pseudo detect**, còn metric preprocessing dùng toàn720 điểm trước mốc tiêm thật, gồm300 điểm sau pseudo detect. Train/test đều trước mốc tiêm thật. Raw trace independent kiểm37472 span/20 edges; scoring2160 checks và raw1080 arrays đều PASS (`paper/normal-pretrace-verification.json`). Các graph/parents/arrays/scores của bản normal cũ và bản strictpretrace giống nhau ở ca này; không lấy sự giống đó thay kiểm cutoff.

**Đề xuất đổi nguồn control ở §7/§8:**

> Control normal/normal dùng trace trước pseudo detect và train/test trước mốc tiêm thật. Toàn bộ metric preprocessing vẫn dùng tập trước mốc tiêm thật tới current, không chỉ trước pseudo detect. Có60/270 metrics≥3; scorer top security_mem823.7241999953277 vẫn tồn tại sau khi kiểm số học và cutoff độc lập. Đó là kết quả của1 ca pre-injection proxy; drift/warmup, normal reference chưa phủ test, proxy regression sai hoặc pre-injection chưa hoàn toàn healthy còn là các giải thích khác. Nguồn: runs/normal-normal-architecture-pretrace/snapshot.json; paper/compare-normal-pretrace/comparison.json; paper/window-normal-pretrace/window-comparison.json; paper/normal-pretrace-verification.json.

Giới hạn: không gọi cờ numerically_verified tự gán là bằng chứng. Chỉ actual residual/score error, raw-array alignment và raw trace cutoff checks hỗ trợ kết luận ở đây. Chưa kiểm prevalence hoặc calibration toàn dataset; không cần chạy thêm dataset để kết thúc P1.
