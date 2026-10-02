# K2 — Kiến thức nền: dữ liệu

> Trích nguyên văn từ: bản tóm tắt kiểm dữ liệu RCAEval RE2-TT (cập nhật 22/09/2026); sự thật ST1–ST3 của bài học v1; danh sách câu hỏi kiểm dataset của cùng đợt khảo sát với K1. Đã bỏ: chính sách bàn giao, ghi chú chính sách cũ, hash của báo cáo và metadata, dòng về nơi lưu dữ liệu cũ, mọi link ngoài repo này. Giữ mã revision Hugging Face vì cần để tải đúng bản dữ liệu.
>
> **Chưa kiểm lại.** P2 kiểm trên file thật trước khi dùng.
>
> **Chính sách nhãn cũ:** dòng Leakage ở §1 ("root/fault EVALUATION ONLY, không fit/tune") là chính sách của v1, không phải luật hiện nay. Cách dùng nhãn hiện nay theo MRP §4 (chia dữ liệu) và §6.

## 1. RCAEval RE2-TT: năng lực đã kiểm ở v1

| Phạm vi | Sự thật |
|---|---|
| Dataset/revision | Hugging Face `phamquiluan/RCAEval`, `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e` |
| Complete metadata — RE2-TT | 90 ca: 5 root-service × 6 fault × 3 repeat. Metrics/traces 90, logs 89. Inject time trong window ở 90/90; không phải independent anomaly-onset truth |
| Full-subset traces | 90 schemas thống nhất, 67.345.051 spans; literal serviceName và cặp serviceName/operationName; parent chỉ resolve trong cùng trace. 27 services/161 operation pairs là **union audit**, không vocabulary/graph nhìn trước |
| Graph | Service identity literal, observed resolved parent→child relation. Không đủ CALLS/USES/messaging/causal semantics, typed resources hay complete topology |
| Coverage | Parent resolution tổng 98,45274372%; 7 ca dưới 90%. Giữ hard cases. Root có trong tập trace services 20–27 ở 90/90 **full cases**, không bảo đảm prefix |
| GT | Root service/fault/case/window có; operation-root/resource-root/affected-node/path absent. Injection target không có kiểm chứng độc lập riêng |
| Task được chấm | Known-window root-service ranking; graph/representation ablations theo service outcome; missingness analysis có giới hạn. Node/service anomaly F1 và operation localization trên RE2-TT **NOT EVALUABLE** |
| Multimodal — raw sample only | Log–metric DIRECT chỉ tại exact entity-second aggregation bin; log–trace và metric–trace SERVICE+TIME. Không request/span-event join. Không suy compatibility tất cả 89 logs từ samples |
| Detection | Chỉ partial injection-regime evaluation; thiếu healthy operational controls đa workload, onset/affected-entity labels độc lập. Known-window RCA không là detector end-to-end |
| Leakage | Case/path/root_cause.txt/presence/oracle metadata forbidden; root/fault EVALUATION ONLY, không fit/tune; inject_time chỉ external boundary cho known-window RCA, forbidden detection input. Telemetry counts trong window hợp lệ khác metadata/future counts |

## 2. Sự thật đã đo trên RE2-TT (bài học v1)

- **ST1 — Dữ liệu RE2-TT.** 90 ca = 5 service gốc × 6 loại lỗi (cpu, mem, disk, socket, delay, loss) × 3 lần lặp. Nhãn chỉ có: service gốc, loại lỗi, thời điểm tiêm lỗi. Không có nhãn vùng ảnh hưởng, operation gốc hay đường lan truyền.
- **ST2 — Trace.** 98,45% tham chiếu span cha resolve được trên cả 90 ca (7 ca dưới 90%). Trường `duration` đầy đủ, không âm, đơn vị chưa xác minh. `statusCode` rỗng toàn bộ. Log có ở 89/90 ca. Mỗi ca trace chạm 20–27 service.
- **ST3 — Đồ thị gần như hằng số.** 30 ca dev chỉ có 2 đồ thị dịch vụ khác nhau (27 nút/55 cạnh có hướng ở 24 ca; 20 nút/20 cạnh ở 6 ca). 5 service gốc nằm ở 5 vị trí cố định: auth không có cạnh nào; route và train không gọi service nào nhưng được 3 service gọi (không phải lá); order ở giữa; travel là hub. Final60 dùng lại đúng 5 service gốc này.

## 3. Câu hỏi kiểm dataset (checklist cho P2)


Những câu hỏi sau không thể trả lời đáng tin chỉ từ paper. P2 phải kiểm artifact/raw metadata; không suy đoán.

### O.1. Phiên bản, phả hệ và quyền dùng

1. Exact release, commit, dataset revision và checksum của từng Train Ticket, Sock Shop, Online Boutique, RCAEval RE2/RE3 và LEMMA-RCA candidate là gì?
2. Paper, repository, dataset card và archive có trỏ tới cùng snapshot không?
3. License cho raw telemetry, derived features và redistributable experiment artifacts là gì?
4. Service count dùng cách đếm nào: business services, infrastructure components, pods, instances hay loadgenerator?

### O.2. Trace và khả năng dựng graph

5. RE2-Train Ticket raw trace có stable operation identity hay chỉ có span name biến đổi theo ID/URL?
6. Exact fields và types trong `traces.parquet`/CSV là gì: `traceId`, `spanId`, `parentSpanId`, service, operation, kind, status, duration, resource attributes?
7. Có route template/RPC method ổn định hay chỉ raw URL/path có cardinality cao?
8. Bao nhiêu `parentSpanId` resolve được trong cùng trace; bao nhiêu orphan/root/multiple-parent anomalies?
9. Có thể phân biệt SERVER/CLIENT/PRODUCER/CONSUMER, database, cache và messaging spans không?
10. Service graph edges có thể dựng trực tiếp từ parent-child spans với hướng caller→callee không?
11. Operation graph edges có thể dựng ổn định giữa runs/versions không?
12. Trace sampling rate, head/tail sampling policy và coverage theo service/operation/fault type là gì?
13. Missing spans/services phân bố ngẫu nhiên hay tương quan với load, fault, language, error, sampling hoặc instrumentation?
14. Trace timestamps, metrics và logs có cùng clock/timezone và độ phân giải đủ để align không?

### O.3. Logs, metrics và liên kết đa nguồn

15. Logs có `traceId`/`spanId`/service-instance identity đủ để gắn vào trace graph không?
16. Log template IDs đã có sẵn hay phải parse; parser version/configuration và template stability giữa runs là gì?
17. Metrics map được đến service, pod, container, node, database và shared resource bằng key ổn định nào?
18. Metric names/units/sampling gaps có nhất quán giữa healthy và fault windows không?
19. Mỗi case thật sự có modality nào; tỷ lệ row/span/log missing là bao nhiêu, thay vì suy từ nhãn “multimodal” ở benchmark level?
20. Có thể phân biệt missing telemetry với giá trị 0/không có event không?

### O.4. Normal baseline, incident và labels

21. Healthy data dài bao lâu cho từng entity; có đủ để fit threshold/calibration theo workload regime không?
22. Healthy periods có contamination, warm-up, deploy/change, drift hoặc leakage từ cùng incident không?
23. Ground-truth anomaly time là injection timestamp, first symptom, alert time hay manually curated interval?
24. Detection label có ở timestamp/window/trace/entity level nào?
25. Root-cause ground truth chính xác là service, instance, pod, host, metric, log line/template, operation hay code line?
26. Dataset có nhãn affected components tách khỏi root cause không?
27. Có multi-root cases không; nếu có, root set và relative relevance/severity được ghi thế nào?
28. Candidate universe có chứa mọi true root không; alias/service naming được chuẩn hóa thế nào?
29. Fine-grained indicator trong RE2/RE3 là observed symptom hay injected/verified causal origin?
30. LEMMA-RCA v4 sau preprocessing còn chính xác bao nhiêu cases ở mỗi sub-dataset, và ground truth map đến node/pod/sensor nào?

### O.5. Tính khả thi của thí nghiệm sau này

31. Có thể tạo split theo incident/run và thời gian mà không rò cùng injection/workload vào train/test không?
32. Có đủ cases theo fault type/system để ước lượng uncertainty theo failure case thay vì theo span/row không?
33. Có artifact để dựng graph đúng, graph bị thiếu có kiểm soát và no-graph baseline trên cùng input không?
34. Có natural missingness cases hoặc chỉ có complete archive để tạo synthetic masks?
35. Compute/storage cần để chạy detector/ranker trên exact subset là bao nhiêu; subset nào giữ nguyên task/label semantics mà không cherry-pick?

