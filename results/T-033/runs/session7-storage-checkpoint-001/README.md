# T-033 — Checkpoint phiên 7: dừng vì vượt dung lượng

Codex là người làm, Claude là người phản biện. Task chưa hoàn tất. Đây là checkpoint xử lý lỗi trích trung gian, chưa là kết luận cơ chế hay báo cáo G2. Không có run detector nào được khởi lại.

Đã đọc AGENTS, STATE, toàn SPEC, LOG phiên 3–6 và bổ sung cuối phiên 5; các checkpoint Minh chỉ định; trực tiếp MRP RQ2/P4, DT18 NV2/NV3, advisor §1, toàn LESSONS và WHY-41. Tự kiểm 825 file nguồn cũ, 299 file mới và 460 file manifest phiên 6 đạt. LOG/STATE trong manifest phiên 6 được so với bản trước khi nối phiên 7. Nguồn và môi trường EC2 mới đạt; không worker trước lượt trích. Chi tiết ở `../session7-open-001/integrity.json`, preflight và các timer.

## Đã đạt và phần lỗi

- Đã kiểm lại lựa chọn đại diện/đối chứng đúng quy tắc đóng băng cho 40 nhóm gốc và 24 nhóm mới. `../session7-open-001/coverage-matching.json#/groups` ghi từng khác biệt ô, số chiều và coverage quan sát. Không coi ghép này là kiểm nhân quả hay collector đầy đủ.
- Đã khóa điểm cho 210 đường ca trước đọc giá trị: 30 ca × (5 đường BOCPD + 2 bộ cột N-Sigma). `../session7-open-001/points-lock.json#/units` ghi điểm báo đầu trước/sau proxy, điểm không báo gần nhất, proxy/cuối file, điểm khác đầu tiên của contrast đã lưu. Không chọn lại theo giá trị thuận lợi.
- Hai file khóa đã nhận và kiểm hash hai đầu. Các mẫu số input trùng, collapse, không kênh, lỗi và contrast không định nghĩa giữ trong nhóm phiên 6; không cộng thành tỷ lệ nguyên nhân.
- Trích trung gian đã lưu dừng sau 11 ca. Toàn bộ 13 file của lượt lỗi còn tại EC2 `~/rca/T-033/runs/session7-manual-001/`. Không xóa, không chạy lại detector. Không nhận 2,7 GB này về laptop; chỉ nhận hai file khóa nhỏ. Không dùng đầu ra trích dở để viết kết luận cơ chế.

Lỗi của Codex nằm ở `scripts/session7_extract.py`: mảng frozen thay đổi theo thời gian chỉ có 721 hàng hậu proxy, nhưng mã so hàng đầu với T toàn bản ghi là 1441. Điều kiện sai đi vào nhánh chép cả mảng ở mỗi điểm. Header của `Z_fixed`, `margin_fixed`, `mean_updated_minus_fixed`, `threshold_updated_minus_fixed`, `finite_statistics_both`, `contrast_defined` xác nhận shape này. Guard dự phòng 64 MiB trước ca không đủ cho file tiếp theo lớn hơn; vì chưa kiểm kích thước thực ngay trước ghi, tổng đã vượt trần trước lần guard kế tiếp. Đây là lỗi trích/cài đặt và kiểm dung lượng của người làm, không là lỗi detector, dataset hoặc cơ chế báo động.

Bằng chứng: `../session7-open-001/session7-extract-001.stderr`, `.timer.json`; `session7-storage-status-002.stdout#/files,/frozen_array_headers` trong cùng thư mục. Mã lỗi và mọi phiên bản controller lỗi được giữ. Lỗi controller chỉ ở laptop trước SSH được ghi riêng trong `local-failures.json`.

## Dung lượng, thời gian và EC2

`checkpoint.json` ghi đúng snapshot kiểm chỉ đọc 11/10/2026 09:49:18 +07:

- Tổng đầu ra EC2: 4.344.456.547 byte; trần đang được phép: 4.294.967.296 byte; vượt 49.489.251 byte.
- Lượt trích lỗi mới: 2.711.497.401 byte. Disk còn 1.616.633.856 byte. Không worker T-033.
- Lượt cuối chỉ nhận hai file khóa; không ghi thêm EC2. Không bật/tắt EC2, không cài package, không xóa thêm. Laptop có thể đóng vì không còn xử lý T-033 chạy.

`ledger.json` nối toàn timer từ snapshot cuối phiên 6. Charged mới là 350,9056568979851 giây, còn 14.049,094343102015 giây trong trần 14.400 giây mới. Bao gồm lượt SSH bị môi trường chặn, preflight, lượt trích lỗi, kiểm dung lượng và nhận khóa. Mức cũ 28.800 giây là hạch toán dự phòng chưa kiểm; thời gian thực tế cũ vẫn OPEN. Không dùng lịch, subtotal status hay thời gian nested để cấp giờ. Ledger lịch sử giữ nguyên. Lệnh chỉ đọc sau dừng pin snapshot mới trong RAM EC2 và giữ snapshot trên laptop, tránh ghi thêm ở máy đã vượt trần.

## Đề xuất cụ thể chờ Minh

Đề nghị Minh duyệt cùng một phạm vi sau:

1. Nâng riêng trần **đầu ra tại EC2 của T-033** từ 4 GiB lên **5 GiB** để giữ toàn bộ lượt lỗi và có chỗ cho bản trích đúng. Trần thời gian giữ theo Q-132. Không xóa, dọn hay nén lại file cũ.
2. Dùng bản sửa mới `results/T-033/scripts/session7_extract_v2.py`; giữ nguyên v1. Bản sửa dùng `post_indices` để lấy đúng một hàng hậu proxy, kiểm time/cột/shape; điểm trước proxy không có contrast fixed hậu proxy. Giữ toàn bộ giá trị nguồn và con trỏ; gzip JSON đầu ra mới là nén không mất dữ liệu. Trước mỗi ghi đo kích thước serialized/compressed thực và kiểm tổng/disk theo đúng trần, không dựa dự phòng theo ca. Tái dùng khóa điểm và coverage đã nhận; không chọn lại nhóm/điểm, không chạy detector.
3. Ghi vào thư mục lượt mới `runs/session7-manual-pilot-001/` rồi `session7-manual-rest-001/` trong `~/rca/T-033/`, nhận vào thư mục lượt mới trong `results/T-033/`. Một ca pilot trước; kiểm scalar/map/cờ/time/NaN/shape/hash/readback/byte trước rest. Rest loại pilot, không tính trùng. Tiếp đọc tay và tổng hợp nguyên SPEC sau khi trích đạt. LOG chỉ nối và duy nhất dòng T-033 STATE; không SPEC, nguồn cũ, DECISIONS, WHY, T-032, test/locked/heldout, commit hoặc push.

Ảnh hưởng: chỉ sửa cách chiếu/lưu trung gian chẩn đoán và dung lượng đầu ra mới; không thay đầu vào detector, tham số, CP/cờ, cách chấm hay tiêu chí nghiên cứu. Đọc tay/RQ2/P4 và căn cứ P6 vẫn chưa được hoàn thành.

**Dự toán chưa kiểm:** trích/kiểm/nhận khoảng 2–10 phút; output nén khoảng 30–300 MiB. Giả định việc bỏ lặp mảng hậu proxy làm giảm phần lớn dung lượng; có thể sai khi số điểm hoặc theta/matrix lớn, dữ liệu nén kém hoặc hash/IO chậm. Chưa chạy bản sửa vì đã dừng ở trần. Không coi dự toán là upper bound hoặc đủ căn cứ khởi rest. Pilot phải đo lại; không đủ trần thì checkpoint/trình, giữ nguyên phần chưa làm.

Bản sửa mới chỉ đạt đọc mã/AST/header schema, **chưa kiểm trên EC2, chưa sẵn sàng gọi là PASS**. `draft-static-check.json` pin mã và phần chưa kiểm. Metadata input hiện tại không có quyền mở rộng storage; draft từ chối `DRAFT_NOT_AUTHORIZED`. Minh chưa duyệt thì không launch.

## Bước tiếp và câu hỏi nguồn

Chờ Minh duyệt đúng đề xuất trên hoặc chỉ định phương án khác. Không có yêu cầu duyệt lại ngân sách thời gian. Nếu được duyệt: đọc checkpoint/LOG cuối; kiểm hash theo manifest; dựng input mới từ inventory cũ/mới cộng pin hai file khóa đã nhận, điền đúng quyền storage và explicit pilot ID; pin snapshot ledger cuối cộng mọi timer mới. Kiểm process/source/hash EC2 có đo trước pilot. Tự soát wrapper/scalar projection, chạy pilot rồi rest; chưa có CLI hoàn chỉnh nên không bịa lệnh launch.

Sau khi trích đạt còn phải đọc tay mọi nhóm và đối chứng, raw/fill/scale/historical statistics/likelihood/posterior/MAP/CP/chấm, log text và coverage ở điểm cần phân xử; tổng hợp các đầu ra SPEC, câu được phân xử và OPEN. Không nhận false alarm vận hành, trễ vật lý, nguyên nhân từ đồng xuất hiện hoặc độc lập thống kê các kênh. Thiếu trung gian/phép phân xử phải trình đúng phần và chi phí; không bỏ nhóm. Chưa soạn prompt Claude chính thức vì toàn task chưa hoàn tất.

Lệnh EC2 cuối: controller `session7_control.py remote-readonly session7-receive-locks-001 results/T-033/scripts/session7_receive_locks.py`, Python pin qua SSH stdin; payload và timer ở session7-open-001. Lệnh chốt laptop và kiểm cuối được ghi trong LOG/checkpoint manifest.
