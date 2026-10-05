# T020 — audit ngữ nghĩa V1

FACT: đọc 877 dòng theo nội dung nguồn; 510 nội dung c khác nhau được đọc theo nhóm exact-content, các occurrence vẫn giữ riêng. Các dòng e/d, STATE và bốn gate được kiểm riêng. Không phân loại blanket theo task/tên file.

Đầu vào snapshot: `results/T-020/08-so-chuyen-g1.csv`; hash trong JSON. Có 683 overrides và 194 dòng giữ nguyên. Các override c→c thường sửa thẻ hoặc trạng thái, không phải thêm quyết định.

Giữ nguyên 533 match G1, 322 paragraph pending, 18 provenance STATE và bốn gate a/b. Mọi dòng và citation đã kiểm exact source line; các file được đọc được rehash cuối lượt. Thời gian script chỉ là replay/assert, không phải toàn thời gian đọc ngữ nghĩa.

Các điểm trọng yếu: T001 dataset không đóng cùng danh sách Q37/Q38; permission code không license là mệnh đề riêng OPEN. T015 variant/full-vs-top11/finite-tie/window vẫn G1 dù task đóng. Q55 ghi M4/WHY17 và đính chính nhưng không chọn P3. Q56 áp từng mục, E2 chuyển G1 và E6/D3 không áp. Q57 ghi WHY19/20 với trạng thái Đề xuất G1; không coi là lỗi chưa ghi common hoặc tự chọn window/seed từ context. Chi phí Q40/phạm vi bổ sung được ghi riêng, không biến thành D5.

Tiêu đề, fences, câu lệnh, progress và số kiểm đã làm là tham chiếu/evidence; nháp common V9 có trạng thái pending/applied riêng. Việc P3/P4 kiểm tiếp không bị dùng để cấp quyền mở raw/locked trong T020.

| Chuyển loại | Số occurrence |
|---|---:|
| c→c | 203 |
| c→d | 14 |
| c→e | 431 |
| e→c | 16 |
| e→d | 3 |
| e→e | 16 |

OPEN/giới hạn: đây là đầu vào tự kiểm nội bộ để root đối chiếu độc lập, không thay Claude review; không chứng minh 533 coverage cơ học bằng 533 quyết định khoa học. Một dòng có nhiều mệnh đề giữ trạng thái hỗn hợp và card liên quan; các thao tác common/quyền chi phí nằm trong evidence riêng. Không chọn baseline/dataset/split/label/window/retrieval hoặc thêm gate.

Tái lập bằng `py -3 -X utf8 results/T-020/trung-gian/exposure_ledger/build_v1_semantic_overrides.py`. Script chỉ đọc prose/snapshot/citation và ghi trong luồng này. Root hợp nhất theo id+source, kiểm nội dung gốc trong snapshot; không dựa oldclass sau rerun classifier.
