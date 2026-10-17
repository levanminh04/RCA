# Bàn giao T-039 cho phản biện

Đã triển khai dựng/đối chiếu trên toàn 132 graph Nezha-OB dev đã lưu, bằng snapshot T036 cũ đã ghim mà Minh duyệt dùng trực tiếp. T037/T038 và mã chung không được sửa. Phản biện chính thức: Claude; chưa nghiệm thu task/P5/G3. Phần xác nhận đầy đủ nguồn deployment chỉ đạt một phần vì lineage ngoài snapshot còn OPEN.

Đọc `nguon.json`, `bao-phu-nguon.md/json`, `ban-ghi.json`, `mapping.json`, `do-thi/`, `doi-chieu/tong-hop.json`, `phan-tich-chenh-lech.md`, `kiem-dung-dan.md`; manifest dẫn mọi file/hash. Mọi comparison có `conditional_reference=true`, domain dev-adapter và interval gốc. full có interval null là union miền adapter được phép, không cả ngày. N/A là tên cửa sổ theo giao thức, không tự chứng minh sạch/lỗi.

| Mức | Cửa sổ | Số graph | Giao/S endpoints | Giao/T eligible endpoints |
|---|---|---:|---:|---:|
| entity | full | 22 | 13/22 | 13/13 |
| entity | N | 22 | 13/22 | 13/13 |
| entity | A | 2 | 11/22 | 11/11 |
| entity | A | 20 | 13/22 | 13/13 |
| operation | full | 22 | 10/71 | 10/10 |
| operation | N | 22 | 10/71 | 10/10 |
| operation | A | 1 | 9/71 | 9/9 |
| operation | A | 21 | 10/71 | 10/10 |

Nguồn: `doi-chieu/tong-hop.json#/rows/*/views/endpoints`; từng row có input/output/interval. Có 10 entity mapping đã xác minh định danh nguồn; thao tác 20 literal verified, 32 candidate chưa verified, 3 SQL chưa có candidate (`#/mapping_counts`). Fraction1 trên eligible T không là đầy đủ trace. Typed có mẫu số trace0/null vì unknown; không kết luận sai kiểu. Chi tiết chuỗi evidence và từng nhóm/ca ở báo cáo chênh lệch.

Graph ở đây tham gia chuẩn hóa khóa, phép chiếu, giao và hiệu tập. Entity nodes là service/component/data/external có nguồn, operation giữ owner. Bindings tách DB logic với mysql instance; signals là địa chỉ log/trace/metric và điều kiện, chưa có giá trị đo hoặc host binding. Chưa có detector, score, lan truyền hoặc thứ hạng. Đạt phần mô hình/nguồn tham chiếu của DT18-NV2/NV3 và bước1 của cô; chưa trả lời hiệu quả cơ chế RQ3 hay toàn RQ5.

| Nơi nhận/owner | Đầu vào hoặc phép phân xử còn thiếu | Hệ quả và chi phí |
|---|---|---|
| T040 / Minh giao task | Registry, coverage, source→record→set, exclusions và các OPEN của cả ba nhánh; giữ pin nền và ngoại lệ rõ | Tổng hợp tính dùng được; chưa làm T040 bằng quyền T039. Công đọc/chốt chưa đo |
| Dataset/deployment authors; Minh duyệt thu | Commit app/build, image digest, rendered deploy và cấu hình collector/export CSV | Phân xử revision/alias/telemetry/Node; chưa có URL/revision/byte nên chưa tải. Chi phí thu chưa xác định; phải trình danh sách trước |
| P6 / Minh chốt SPEC | Literal verified20, candidate32 và SQL3; ví dụ match/mismatch cùng điều kiện | Cần xác minh tên/thời gian/availability khi chọn thao tác, giữ unknown và tập ứng viên; không tối ưu mapping theo tỷ lệ. Chưa có quyền chạy experiment mới |
| P9a/P9b / Minh và nhóm quan sát | Service/instance/pod namespace+UID, host ID có nghĩa, mapping hiệu lực theo thời gian; span kind/DB/messaging attributes; log trace/span IDs; source→export→schema | NodeName trong ứng dụng chưa chứng minh cột Node của dataset. Cần schema/collector+fixture join, không chỉ ổn định tên. Collector không khôi phục dữ liệu chưa ghi |
| Nguồn phụ / dataset authors | Producer Source/Target/Node, đầu vào/khóa/thời gian và sampling | Không dùng metadata ngày như đối chứng độc lập hoặc chọn P6; code đã đọc là consumer chưa xác định producer. Thu metadata/code mới phải duyệt riêng |

`de-xuat-bo-sung-nguon.md` tách phần có thể xử lý bằng source mới và phần cần chủ nguồn, giả định/điều kiện sai, owner và kết luận phụ thuộc. Không phải cổng mới hoặc yêu cầu tự chạy vượt SPEC. Còn nghi vấn revision/alias/domain/branch/static/telemetry được ghi theo từng nhóm; chưa có bằng chứng quy nguyên nhân vật lý của graph thiếu.

Lệnh tái lập sau khi Minh giao quyền chạy: `py -3 -X utf8 -B results/T-039/execute_pinned.py <ten-run-moi-chua-co>`; không import live src. Lệnh đọc/kiểm rẻ: `py -3 -X utf8 -B results/T-039/finish_results.py verify <ten-kiem-moi>` (chỉ tạo kết quả kiểm trong T039). Prompt trung tính cho Claude ở `prompt-claude.txt`, Minh chuyển thủ công. Chưa commit/push. Đề xuất commit sau nghiệm thu: `research: implement pinned T039 Online Boutique source graph comparison`.
