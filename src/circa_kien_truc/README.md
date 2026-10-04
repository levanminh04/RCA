# Adapter CIRCA kiến trúc (T-014)

Đọc trace dev thành DataFrame với traceID/spanID/parentSpanID/serviceName/startTime (microseconds). `service_calls(traces, cutoff_seconds)` chỉ dùng span trước mốc; resolve cha bằng cặp traceID/spanID. Không nhận tên ca, nhãn gốc hay SLI từ nhãn.

`build_graph(columns, calls, circa_source)` gọi StructuralGraph tại revision0215e18 và dùng assumptions trong tests/alg/sgraph/index.yml. Empty meta-variable được code gốc chuyển tiếp cha. Luật suffix RCAEval: workload→Traffic (lưu lượng), cpu/mem/socket/diskio→Saturation (mức sử dụng tài nguyên), latency/quantiles→Latency (độ trễ), error→Errors (lỗi). Cột lạ hoặc không xác định service đánh dấu, không đoán. Có báo cáo mọi cột của schema được phép ở results/T-014/runs/schema-other-permitted.json; không khẳng định mọi cột Prometheus/host đều đã có mapping service.

Đặt PYTHONHASHSEED trước khi khởi động Python và lưu nó cùng graph. Nếu call/meta graph có chu trình, native visit xử lý mỗi node SCC một lần; thứ tự set có thể đổi cạnh metric. Report kiểm call/meta/metric riêng. Metric DAG không chứng minh call/meta input thỏa giả định DAG của CIRCA; giữ nguyên cạnh tác giả và báo giới hạn này.

Mặc định giữ metric đã ánh xạ nhưng cô lập, không thêm cạnh. Đây là sửa coverage có chủ đích **(chờ WHY, xem results/T-014/de-xuat-tai-lieu-chung.md)**. Đặt retain_isolates=False để kiểm coverage code gốc. Report luôn ghi original_missing_nodes. Service thiếu trace vẫn có meta-variable và luật nội service; không có cạnh gọi giả.

`score_graph(frame, graph, detect_time)` dùng RCAEval RHTScorer, CaseData interval1s/train111/test10 và current=td+300. Nó cũng chạy DA(threshold3) để kiểm cơ chế. RHT-only là cấu hình tham chiếu hai nguồn graph **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**; cấu hình đầy đủ bài Oracle là SVR+RHT+DA, khác linear default. Hàm trả metric→score, residual/training arrays và khóa hòa điểm. Lexical tie-break chỉ để trình bày, không làm đổi nhóm điểm.

Thiết lập PYTHONDONTWRITEBYTECODE=1 trước import để không viết cache vào source/env readonly. Caller thêm RCAEval/src repo vào sys.path và cung cấp clone CIRCA đúng revision. Cách dựng môi trường và ví dụ chạy ở results/T-014/moi-truong.md, scripts/build_all.py, scripts/run_examples.py. Không dùng adapter này như bộ tự phát hiện sự cố.
