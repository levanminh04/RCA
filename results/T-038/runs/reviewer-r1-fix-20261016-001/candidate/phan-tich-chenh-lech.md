# Bản đề nghị sửa R1 — chưa tiếp nhận vào kết quả hiện hành

Bản này được tạo bởi người phản biện sau lời Minh “DUYỆT SỬA TRONG PHIÊN NÀY”. Đây là gói sửa cụ thể đã kiểm; không là quyền đổi vai hoặc ghi đè đầu ra của người làm. Các root output, LOG/STATE/SPEC và shared code vẫn giữ nguyên.

Nguồn tĩnh bổ sung ba dependency dữ liệu: Skywalking → Elasticsearch, Alertsnitch → MySQL và Nacos → MySQL. Webhook HTTP Alertmanager → Alertsnitch giữ kiểu gọi chưa phân loại; cấu hình HTTP không xác nhận synchronous execution hoặc delivery. Mọi quan hệ có điều kiện profile và locator tới nguồn đã kiểm Git blob/SHA; không chép credential vào bản ghi.

Mô hình đề nghị có 110 entity, 993 operation, 513 relation, 50 binding và 139 signal. Có 170 cạnh entity, 343 cạnh operation; phép chiếu có 122 cạnh và phần entity-only có 48 cạnh. Nguồn số: checks/model.json và candidate/phan-tich-chenh-lech.json#/source_counts.

Kiểm đủ 1.069 graph: ở 979 graph entity, endpoints thêm 4 S/static-only, typed thêm 3 S/static-only và 1 unknown exclusion. Toàn phía trace và giao giữ nguyên. 90 kết quả operation bằng nguyên bản trước. Có kiểm độc lập từng khóa/members/phân hoạch loại trừ/mẫu số, input, lặp và đảo thứ tự. Không phải thực nghiệm RCA mới. Nguồn số: checks/comparison.json và candidate/summary.json#/rows.

| Mức/miền/view | Graph | S | T | Giao | Riêng tĩnh | Riêng trace |
|---|---:|---:|---:|---:|---:|---:|
| entity/A/endpoints | 30 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/A/typed | 30 | 162 | 0 | 0 | 162 | 0 |
| entity/N/endpoints | 30 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/N/typed | 30 | 162 | 0 | 0 | 162 | 0 |
| entity/full/endpoints | 30 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/full/typed | 30 | 162 | 0 | 0 | 162 | 0 |
| entity/s300/endpoints | 150 | 164 | 16–49 | 15–44 | 120–149 | 1–5 |
| entity/s300/typed | 150 | 162 | 0 | 0 | 162 | 0 |
| entity/s60/endpoints | 739 | 164 | 0–49 | 0–44 | 120–164 | 0–5 |
| entity/s60/typed | 739 | 162 | 0 | 0 | 162 | 0 |
| operation/A/endpoints | 30 | 341 | 0 | 0 | 341 | 0 |
| operation/A/typed | 30 | 340 | 0 | 0 | 340 | 0 |
| operation/N/endpoints | 30 | 341 | 0 | 0 | 341 | 0 |
| operation/N/typed | 30 | 340 | 0 | 0 | 340 | 0 |
| operation/full/endpoints | 30 | 341 | 0 | 0 | 341 | 0 |
| operation/full/typed | 30 | 340 | 0 | 0 | 340 | 0 |

Đây là min–max từng graph trong từng miền, không là số nguyên nhân hay độ phủ instrumentation. Mẫu số trace rỗng vẫn null; không đổi thành 0% coverage. Năm cặp riêng trace và các chuỗi source/mapping chưa có bằng chứng runtime giữ giới hạn cũ.

source-audit.json giữ riêng các địa chỉ UI→OAP, Prometheus alert/scrape và client discovery còn cần semantics/binding hoặc biểu diễn unknown protocol. Không ép chúng vào channel HTTP/RPC/internal để đóng mô hình. Grafana Deployment đã xem không cung cấp datasource address; vai trò visualization không tạo cạnh. Các phần này chưa cho semantic/runtime completeness; owner và bằng chứng cần nằm ngay từng mục.

R1 là lỗi trích/bản ghi nguồn: assembler cũ liệt kê các thành phần nhưng không đưa các dependency cấu hình này vào relations. Không quy lỗi cho dataset/collector. Bản sửa đề nghị chỉ phục hồi thông tin có nguồn, chưa xác minh lineage, lợi ích RCA, thiết kế P6, RQ3/RQ5/G3 hoặc quyền mở test.
