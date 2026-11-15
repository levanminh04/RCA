# C4 — giao thức kiểm khả thi M1 bản đầu

Kế hoạch khóa trước đầu ra: `m1-execution-plan.json`. Hai mã mờ đã khai trước; ánh xạ vai trò và sổ lỗi chỉ dành cho người điều phối. M1 chỉ nhận bảy tham số: span, metric, log, inventory, aliases, `t`, params. Mã ca và đường dẫn không đi vào bảy tham số này.

STEER #4 đã hủy hai ca v1 sau khi thấy OOM; không có đầu ra M1 v1. File v1 giữ nguyên. `m1-execution-plan-v2.json` khóa 21:52:40Z, ghi rõ sửa sau quan sát OOM và trước đầu ra M1. V2 dùng normal22:01–22:11Z sau10phút ổn định, rồi pause event-service không trước22:17Z. Toàn bộ bằng chứng/diễn giải phải dùng đúng phiên bản; không dùng cửa sổ v1 làm phép thử giả.

## 1. Nguồn và chuyển đổi

Trace/log lấy từ file OTLP Collector trung tâm ghi song song khi xuất sang Tempo/Loki. Stager chốt byte đầu của từng file đang ghi, băm đúng prefix đã đọc, bỏ dòng cuối chưa hoàn tất, rồi lọc cửa sổ. Metric lấy bằng Prometheus API với bảy query cố định trong adapter. Đây chưa phải bộ đọc đầy đủ Tempo/Loki API; việc API kho trả mẫu đã kiểm riêng trong `grafana-evidence.json`.

Gói thô giữ `[t−600s,t+600s)`, rộng hơn cửa sổ M1 `[t−300s,t+300s)`. Span phải bắt đầu trong cửa sổ và kết thúc trước cận trên theo hợp đồng P7. ID hex được kiểm độ dài; root rỗng hoặc toàn số 0 được chuẩn hóa thành rỗng. Parent không có trong gói vẫn được giữ; không bịa root thay thế. Nanosecond đổi xuống microsecond bằng số nguyên cho API P7; diagnostics đếm span dưới một microsecond.

Metric gauge giữ timestamp nguồn bằng `timestamp(metric)`; không dùng timestamp lưới query giả làm lúc đo nguồn. Query mỗi 15 giây chọn một phần mẫu receiver 10 giây; không phục hồi các mẫu xen kẽ chưa được query chọn. RED là chuỗi dẫn xuất, khai rõ timestamp đánh giá PromQL và bước 15 giây. NaN giữ thiếu, không điền 0 hay forward-fill. Mỗi nguồn/entity có clock và chỉ số hàng riêng; nhiều chuỗi vật lý cùng ánh xạ một kênh mà chưa khai aggregation sẽ bị từ chối.

Log dùng timestamp Docker/OTLP. Severity đọc từ JSON Spring hoặc mức ghi trong log Keycloak; không biết mức thì giữ unknown. Không suy log lỗi từ thời gian sự cố. P7 không nhận kind/thuộc tính DB để tự thêm DB thành nút; DB client span vẫn thuộc JVM gọi.

Inventory giữ 32 thực thể từ mô hình T-037. `discovery-server` ánh xạ sang `config-discovery`. Prefix metric của DB đổi `_` thành `-` để tương thích quy ước cột, có alias trả về tên DB gốc. Không gộp host thiết kế với Oracle hoặc bỏ thực thể không quan sát được.

## 2. Khóa phương pháp và cách ly nhãn

39 SHA code M1/P3 khớp bản P7 khóa T-054 main013-v2. Params M1 lấy từ job M1 của plan đó, không chọn theo kết quả đêm nay. Adapter không được ghi đè params khóa. Runner kiểm manifest input, 39 pin và trường cấm đệ quy; chặn giá trị chứa mã mờ, đường dẫn ca và đường dẫn ledger. Nguồn code gốc trên laptop không được sửa.

User `rca` không đọc được `/var/lib/flash-ticket-ledger/ledger.jsonl` thuộc user `ledger`. Log công cụ tiêm/tải không được đưa vào filelog; không tạo Grafana annotation về lỗi trong nguồn RCA. Stager không đọc ledger; bộ điều phối chỉ chuyển `t` sang `request.json`. Tên component xuất hiện tự nhiên trong telemetry và inventory không phải nhãn tiêm lỗi.

Mỗi gói chạy hai lần với cache mới, lưu hai JSON canonical và SHA256. Diagnostics cần soi span, parent thiếu, entity quan sát, cạnh, nguồn metric thiếu và số lần E2 dự phòng. Nếu toàn rỗng hoặc ERROR, phải lần tới đầu vào; không biến lỗi adapter/điều phối thành kết quả phương pháp.

## 3. Phạm vi kết luận

Theo STEER #3, chỉ một lỗi pause khoảng 5 phút sau phép đo C3 và thêm một cửa sổ bình thường nếu chạy được. SPEC gốc đòi 3 lỗi+1 bình thường; không gọi hai cửa sổ này là đạt đủ 4/4. Mốc pause xác nhận bằng `docker inspect`; tác động/hồi phục quan sát bằng client tải độc lập. Hai nguồn này không đi vào M1.

## 4. Kết quả thực chạy v2

Hai gói đã đóng và nhận về `rca-ban-dau/cases/<id>/`; đầu ra ở `rca-ban-dau/outputs/<id>/`. Archive ở cùng thư mục gốc có SHA đối chiếu Oracle/laptop. Năm file đầu vào mỗi case được kiểm theo manifest; runner kiểm39pin nguồn, trường cấm và giá trị mã mờ/ledger. Scan đối chiếu credential đã sinh và mẫu JWT trước khi tải về không có match; đây không phải bộ dò mọi loại bí mật.

| Case | Span trong cửa sổ | Hàng metric chuẩn hóa, gói rộng | Log trong cửa sổ | Quan sát / trả hạng | Nút/cạnh trong graph | E2 dự phòng | Lặp cùng SHA |
|---|---:|---:|---:|---:|---:|---:|---|
| c12e47ab, normal22:01–22:11 | 32138 | 4617 | 23 | 17/17 | 7/8 | 0 | Có |
| f4a8c021, pause event | 26643 | 4505 | 234 | 17/16 | 7/8 | 0 | Có |

Cả hai trả `status=OK`, không lỗi hợp đồng. `metric_rows` gồm dữ liệu đóng gói rộng hơn cửa sổ M1; lõi tự cắt đúng N/A. Inventory vẫn32 thực thể; số quan sát không phải số inventory. Thời gian hai lần chạy normal khoảng3,90/3,71giây; ca pause2,96/2,96giây. Đây chỉ là thời gian của hai lượt trên máy này khi chạy đồng thời; không dùng làm benchmark tốc độ.

Không có trạng thái toàn rỗng. Nguồn số: `m1-feasibility-details.json`, `outputs/*/summary.json` và hai `method-output-*.json` mỗi case. Đầu ra được băm trước phân tích ledger/log tải; phương pháp/ngưỡng/adapter giữ nguyên theo planv2.

## 5. Ca pause thiếu kênh của chính event-service

`NO_VALID_CHANNEL=[event-service]`; service này không nằm trong16 thực thể được trả hạng. Đã lần tới đầu vào, không coi `status=OK` là đã chẩn đoán được lỗi.

| Tín hiệu event-service | Normal N/A | Pause N/A |
|---|---|---|
| Span | 3836/3832 | 3695/0 |
| CPU, memory: mỗi kênh có mẫu clock nguồn mới | 20/20 | 20/0 |
| Workload/error/p50/p90: mỗi kênh có mẫu hữu hạn | 20/20 | 20/3 |

Theo hợp đồng, span phải kết thúc trước cận trên; span sinh/hoàn tất sau unpause nằm ngoài nửa A đã khai. Gauge CPU/RAM không có timestamp nguồn mới trong A; adapter bỏ mẫu bị giữ lặp tại Prometheus, không biến lưới query thành mẫu đo mới. RED còn3mẫu hữu hạn, dưới `m_metric=5` khóa trước. Các đơn vị mang tên event-service có18 `NO_A`,4 `LOW_SUPPORT`; không thêm0 hay forward-fill để ép được điểm.

Giới hạn đã xác nhận: với kênh/cửa sổ này, pause trọn5phút làm thiếu đầu vào chấm event-service theo P7. Chưa phân xử đầy đủ vì sao Docker receiver không cập nhật gauge khi paused; cần đối chiếu raw OTLP metric/receiver với clock Prometheus trong một probe riêng. Phép thử tối thiểu sau này phải khai trước cách quan sát tài nguyên/liveness độc lập và xử lý thiếu dữ liệu, hoặc chọn cơ chế can thiệp vẫn giữ telemetry của service. Không đưa cờ pause của bộ tiêm hoặc nhãn service vào M1. Không sửa P7/ngưỡng trong đêm.

## 6. Tác động độc lập và đính chính giả định tuyến

Pause được xác nhận22:17:28.010777Z; unpause22:22:28.268351Z, khoảng300,258giây. Theo thời điểm bắt đầu request so với mốc xác nhận, trong pha pause có300request:100HTTP200,133HTTP503,67HTTP504. Availability vẫn100/100HTTP200. Catalog/detail là hai đường chịu tác động. Catalog có200 trở lại ở request22:23:00Z, detail22:23:01Z sau khi các lỗi trước đó hoàn tất; mốc Docker unpause sớm hơn mốc phục hồi API này.

Trong5phút trước **xác nhận** có1HTTP504: request bắt đầu22:17:28.000s, sau lệnh pause22:17:27.955803 nhưng trước xác nhận22:17:28.010777. Không gọi đó là lỗi tự phát trước can thiệp. Giữ nguyên nhóm thời gian ban đầu trong `load-impact.json`; `load-impact-detail.json` giải thích khoảng mốc và bổ sung5phút trước **lệnh yêu cầu**:300/300HTTP200. Không suy onset chính xác hơn dữ liệu client/command cho phép.

Lý do chọn service trong planv2 đã viết quá rộng: “all three read paths reach event-service”. Đối chiếu route gateway và log tải cho thấy availability đi tới booking-service; chỉ catalog/detail tới event-service. `m1-plan-v2-deviations.json` ghi đây là giả định sai của người làm. Giữ nguyên file kế hoạch đã khóa; không đổi tải, `t`, bộ đọc hay thuật toán theo kết quả.

Toàn bộ4800request có4403HTTP200,329HTTP503,68HTTP504; con số này gồm OOM/recreate trước lỗi chủ động, không gán hết cho pause. Log tải và ledger không đi vào phương pháp. C4 chỉ xác nhận đường chuyển đổi/chạy lặp; chưa đủ3lỗi+1normal của SPEC, chưa đủ chấm chính service bị pause, không có kết luận hiệu quả/RQ5.
