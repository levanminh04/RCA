# Cùng PC graph, đổi hashseed scorer

Nguồn: `runs/example-pc/snapshot.json` và `runs/example-pc-hashseed1/snapshot.json`; ca dev đã chọn trước điểm. Hai snapshot có cùng271 graph nodes,896 edges và270 scored metrics. Không học lại graph. Hashseed0/1 là provenance của hai lượt scorer do người làm tạo; snapshot meta chưa tự lưu biến môi trường này. Source hashes và các kiểm alignment ở `paper/crossseed-pc.json`.

## RHT: sai số số học

Effective parent sets và y train/test giống nhau. Có168 node đổi thứ tự parents; X sau căn lại theo parent identity giống hệt. RHT khác0/270 node nếu dùng **atol đơn thuần1e−7**; khác0/270 khi dùng **atol=rtol=1e−7** như SPEC. Max absolute error=1.5567763300694537e-08. Phải giữ cả hai count để không gọi roundoff bằng thay đổi cơ chế. Top5 RHT cùng metric/cùng thứ tự; tập s≥3 cũng giống nhau.

## DA: thay đổi điểm và top5

DA khác25/270 theo atol đơn thuần, và25/270 theo atol+rtol1e−7. Max absolute error=1509.1518147708107. Top5 seed0: `["ts-order-service_latency", "ts-user-service_mem", "ts-execute-service_mem", "ts-rebook-service_cpu", "ts-price-mongo_mem"]`. Top5 seed1: `["ts-order-service_latency", "ts-user-service_mem", "ts-auth-service_socket", "ts-payment-service_diskio", "ts-rebook-service_cpu"]`. Đây là thay điểm/ranking, không chỉ tie display.

| Metric | DA seed0 | DA seed1 | Chênh tuyệt đối |
|---|---:|---:|---:|
| ts-execute-service_mem | 1530.375495624513 | 21.223680853702156 | 1509.1518147708107 |
| ts-price-mongo_mem | 1519.7047891521249 | 20.064070475827631 | 1499.6407186762974 |
| ts-payment-service_diskio | 27.311378326761847 | 1522.6408795519599 | 1495.3295012251981 |
| ts-auth-service_socket | 74.052444622977461 | 1532.2270257615103 | 1458.1745811385329 |
| ts-preserve-service_cpu | 1242.0974450168678 | 19.847453090295303 | 1222.2499919265724 |

Graph không DAG; SCC không tầm thường có kích thước[149, 6, 4, 2, 2, 2]. Cùng generation sets nhưng9 generation đổi thứ tự DAScorer thực tế. Script độc lập replay DA giữ **toàn bộ RHT seed0 cố định** và chỉ thay iteration order: vẫn có25/270 DA score đổi vượt tolerance, max error=1509.1518147720558. Vì vậy floating-point khác ở hồi quy không đủ giải thích thay đổi DA; set/SCC traversal có bằng chứng trực tiếp trong ca này. Boundary/graph mis-specification vẫn là giải thích khác của chất lượng root ranking, nhưng không giải thích chênh giữa hai replay đã giữ graph/score cố định.

Independent scoring của mỗi snapshot có2160 checks PASS, max absolute error≤2.220446049250313e−16. Raw resampling/parents có1080 array checks mỗi seed PASS, error0. Counts missing child evidence khi cùng generation: seed0=124, seed1=124; đây là các lần code cần evidence child dưới3 chưa xử lý. Toàn bộ ordered groups và mỗi delta được giữ trong JSON, không chỉ top5.

Giới hạn: đây là1 ca/2 seed với adjacency PC đã cache. Nó chứng minh rủi ro tái lập DA của ca này, không suy tỷ lệ lỗi cả dataset hoặc CIRCA gốc trên DAG. RHT còn roundoff do thứ tự parent/linalg; không có phép kiểm học PC lại trong bước này. Không chọn seed theo root label, không đổi snapshot hay scorer để điểm đẹp hơn.
