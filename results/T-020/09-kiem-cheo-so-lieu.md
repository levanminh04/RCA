# Kiểm chéo số liệu G1

Đây là các phép đã tính lại từ thành phần, không phải danh sách số chép từ báo cáo. [CSV đầy đủ](09-kiem-cheo-so-lieu.csv) ghi giá trị cũ, file/khóa gốc, phép tính, nguồn thành phần, giá trị tính lại và trạng thái. Chạy lại bước hợp nhất bằng `py -3 -X utf8 -B results/T-020/scripts/kiem_cheo_hop_nhat.py`.

## Quy tắc và phạm vi

SPEC ghi seed **20261004** trước đọc giá trị. Mẫu sắp theo SHA-256 của seed, task, đường dẫn và khóa; không chọn vì điểm đẹp. Mỗi task có nguồn khoa học được kiểm ít nhất năm đại lượng trong pool quan trọng; số quyết định vai trò, census, tiếp xúc, chia và chi phí được kiểm riêng. T-004 không có task/nguồn khoa học hiện hữu: [biên bản](trung-gian/dataset_evidence/T004-no-scientific-pool.json), không tạo mẫu giả.

Index bổ trợ có 167766 lá JSON, **không phải 167766 số đã kiểm**. Ngoài pool quan trọng, root chọn năm lá mỗi task có pool để phát hiện sai khác bất ngờ. Trong 60 mẫu bổ trợ, 51 tính lại được và chín còn OPEN. Hai kiểm sâu chọn trước theo hash: MicroRank của hồ sơ Codex và TORAI của hồ sơ Claude. Bản gốc và bản sửa được giữ riêng.

Tổng CSV hiện có **3248 phép: 3235 MATCH, bốn MISMATCH đã giải thích, chín OPEN**. Một nguồn có thể được kiểm theo nhiều công thức; đây không phải số incident độc lập. [Kết quả hợp nhất](runs/crosscheck-merge-assertions.json) giữ đếm theo task và các hàng quyết định trọng yếu. Không dùng kết quả method để lựa dataset, window hoặc split.

| Task nguồn | Phép trong CSV | Phạm vi nổi bật |
|---|---:|---|
| T-001 | 9 | Danh sách, họ, mặc định từ table/AST/code |
| T-002 | 571 | Census, biên, degree, thống kê theo ca và nguồn metadata |
| T-003 | 10 | Bank và đối chiếu nguồn archive |
| T-005 | 169 | Ca đã chạy, detector và chi phí tổng |
| T-006 | 1504 | Kết quả theo ca/ô và quan hệ tiếp xúc |
| T-007 | 70 | Đối chứng, ca đã nhìn |
| T-008 | 33 | Nhãn Nezha, ô và lineage |
| T-009 | 29 | Nhãn outer Eadro, không cộng bản mirror |
| T-010 | 14 | Inventory và aggregate DeepTraLog |
| T-011 | 15 | Census/aggregate LEMMA; năm lá raw-dependent OPEN |
| T-012 | 44 | Metadata, archive và hồ sơ public |
| T-013 | 17 | BARO/windows và kiểm số từ thành phần |
| T-014 | 20 | CIRCA, source/config và elapsed/queue |
| T-015 | 119 | MicroRank, TraceRCA, code/đồ thị và bốn audit counters |
| T-016 | 44 | TORAI/RCD, seed, gốc/sửa và tổng JSONL |
| T-017 | 10 | SimpleRCA và tổng từ kết quả riêng |
| T-018 | 22 | GDN, calibration và học một lần mỗi hệ/seed |
| T-020 | 87 | Ba split, ma trận, bao phủ G1, số ứng viên C9 |

Số hàng không thay bằng chứng về độ sâu: replay còn kiểm 2176 phép RHT/DA CIRCA, 1088 mảng đầu vào, 2226 so sánh SimpleRCA, TORAI trung gian và GDN checkpoint. [Bàn giao phương pháp](trung-gian/method_evidence/HANDOFF.md) ghi mức kiểm và dung sai; không suy khớp toàn pipeline từ điểm cuối.

## Sai khác MicroRank: giữ cả hai phiên bản

Nguồn `results/T-015/runs/tt-local/auth/example.json`, các khóa `/groups/{normal,anomaly}/audit/…`:

| Nhóm/đại lượng | Snapshot cũ | Tính độc lập theo định nghĩa hiện hành |
|---|---:|---:|
| normal / missing_parent_spans | 1326 | 0 |
| normal / explicit_root_spans | 0 | 1326 |
| anomaly / missing_parent_spans | 1403 | 0 |
| anomaly / explicit_root_spans | 0 | 1403 |

Archived `results/T-015/runs/source-versions/graph-before-null-audit-fix.py:26` không coi `<NA>` là root; `src/microrank/graph.py:32` hiện có. Phép join độc lập tại `results/T-015/scripts/independent_inputs.py:45` đếm missing khi vừa unresolved vừa không phải explicit root. Root đã đọc lại ba nguồn này và chỗ đưa graph vào PageRank tại `src/microrank/__init__.py:85`.

Các graph relations, trace counts và SLO của **ca kiểm này** khớp. Audit được lưu riêng, không đưa vào scorer. Vì vậy khác biệt có bằng chứng về định nghĩa/phiên bản bộ đếm; không tự kết luận lỗi xếp hạng hay mọi thứ hạng bất biến. [Bảng sai khác](trung-gian/method_evidence/mismatches.csv) và [đính chính](dinh-chinh-task-cu.md) giữ đề xuất cũ→mới; không sửa T-015.

## Chín mẫu OPEN

| Mẫu | Vì sao chưa tính lại | Giới hạn kết luận |
|---|---|---|
| T-003 compression_method=8 của một archive member | Chỉ có bản metadata directory đã lưu; chưa có thành phần độc lập để xác nhận byte mã nén | Không dùng mã nén này quyết vai trò dataset |
| Hai lá T-008: minimum PodSuccessRate và edge span count | Cần đọc lại raw TX1, ngoài phạm vi được cấp | Counts/nhãn/lineage đã kiểm không chứng nhận các thống kê đo này |
| T-010 error count=750 của một member | Aggregate cả ca là 1500 với hai member; không được chia đôi để giả phép tính độc lập | Không suy mỗi member có cùng phân bố |
| Năm lá T-011: thời gian/độ chênh của mảng NPY | Cần raw TX1; chỉ kiểm được metadata/census/bytes hiện có | Clock/mức đo và thích hợp mode b vẫn OPEN |

Đường dẫn/khóa cụ thể ở chín hàng OPEN trong CSV. Đây là mẫu bổ trợ; pool tối thiểu theo task vẫn đủ. Không ghi “chờ quyền” cho các phép aggregate hoặc metadata đã được phép và đã làm.

## Lượt thử, lỗi và bảo toàn

[ca-da-chay.csv](ca-da-chay.csv) giữ 16 lượt replay TX2/fixture, gồm 12 lượt exit0 và bốn lượt lỗi. Ba lỗi môi trường/API được giữ cùng retry; lượt MicroRank trả lỗi kiểm vì hai boolean audit khác, tách thành bốn bộ đếm phía trên. Tổng wall của subprocess là 78.406 giây, không dùng làm runtime chính thức của phương pháp. Không học thêm hoặc chạy trên dataset mới.

Lỗi verifier của root cũng được giữ: expected RE3-TT nhập từ trí nhớ, đếm cả stride nằm sau guard, và minimum fit lẫn infer-only zero. Retry sửa phép kiểm từ nguồn, không sửa dữ liệu để cho PASS. Chi tiết ở LOG và đính chính.

**Ngoại lệ phạm vi đã xảy ra:** subagent đọc nhầm `results/T-010/runs/schema-samples.json`, file mang tên schema nhưng chứa mẫu đo TX1. Đã báo Minh, dừng và loại khỏi schema proof. [Biên bản](trung-gian/dataset_evidence/scope-incident.md) ghi rõ; không tuyên bố toàn lượt không đọc raw. Không đọc `data/locked/`, không dùng payload này để quyết dataset hoặc tạo kết quả method.
