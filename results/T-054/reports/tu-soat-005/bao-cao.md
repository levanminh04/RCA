# T-054 — chuẩn bị hai EC2+laptop, checkpoint005

Đã hoàn tất phần triển khai nhiều máy được Minh duyệt, dừng trước chạy chính. Đây là hồ sơ trình G3, chưa phải G3 đã khóa hoặc task P7 đã xong. Không có quyền mở test/main hoặc RE3 từ lượt SSH/dọn máy này.

## Dữ liệu và dọn máy

TT60 có sẵn:60ca/180parquet, **1.309.388.082byte (1,309GB;1,219GiB)**. Hash/byte đúng từng tên ca+tệp so HF revision đã pin; không đọc giá trị telemetry, không tải lại. Nguồn: runs/trien-khai-005/TT60-strict-source-verification.json#/files_verified.

SSH cả hai máy bằng host key đã ghim, không dựng lại môi trường. Cả hai2vCPU/~8GBRAM. Dùng T025/envs/main và T025/envs/py38 cùng nguồn RCAEval cũ. EC2_1 thiếu chỗ; Minh duyệt xóa đúng /home/ubuntu/rca/envs/py312 (~8,10GB), free từ1,462→9,563GB. Giữ T025/main, dữ liệu và toàn bộ kết quả task cũ. EC2_2 còn~14,63GB. Nguồn: *-inventory.json, approved-cleanup-ec2-1.json (stdout dòng deleted_exact_approved_directory), environments-005.json.

## Phân bổ ứng viên khóa

| Máy | Lô | Vị trí tối đa | Dữ liệu TT chuyển |
|---|---|---:|---:|
| EC2_1 | 30TT: family210+B90+C-d3 30+C-e≤30 |360|654.702.162byte/90tệp|
| EC2_2 | 30TT còn lại, cùng cơ cấu |360|654.685.920byte/90tệp|
| Laptop | OB442 (68UNSUPPORTED), TT5baseline300, A phụ180 |922|Giữ bản gốc|

Tổng1.642 vị trí, tối đa1.574 lượt method thực nếu bỏ68UNSUPPORTED; C-e thiếu lịch sử thay bằng dòng hỗ trợ có nguồn, không tự điền0. Gán ca TT theo byte để cân dữ liệu, không theo lỗi/nhãn/điểm. C-c/C-g/C-d1/2 là dẫn xuất, không thêm baseline. Nguồn: placement-005.json#/counts,/TT_transfer_bytes; matrix.json.

Hai EC2 nhận phần TT nặng vì ưu tiên thời gian theo chỉ đạo Minh. Laptop giữ OB để dùng dữ liệu ngày/phút và adapter đã kiểm, tránh chuyển file chung; giữ CIRCA/A theo môi trường Windows/nguồn tác giả hiện có. Đây là cách phân bổ theo bằng chứng hiện tại, không khẳng định tối ưu toàn cục. TORAI B dùng Linux đã có ở G2: nguồn RCD/IO đúng hash, import đạt; parsed digest4CSV+t+seed của DEV khớp Windows trên cả hai máy. Không chạy lại học TORAI chỉ để đo.

Mỗi máy tối đa2worker, mỗi method×dataset chỉ1lượt cùng lúc;1luồng tính số/method. RAM admission tính cả phần dự phòng: EC2 dự kiến2GiB/lượt×1,25, reserve768MiB; laptop theo peak đã có×1,25,reserve384MiB. Đây là ước lượng tài nguyên, không bảo đảm peak mọi ca. Không đủ RAM thì đợi/dừng phát và báo, không biến unrun thành TIMEOUT. Prep→method, M1 seal→C-d3 tuần tự; lô độc lập trên3máy chạy đồng thời. Không cần đo3/4worker hoặc dựng queue phân tán.

Transfer-plan005 ghi đủ từng tệp/hash/byte/máy/đích. Test chưa chuyển. Gửi allowlist vào vùng mới/partial, kiểm đủ trước dùng; bản gốc giữ laptop. Mỗi host có code/data/output prefix riêng; thu manifest/receipt/envelope nguyên bản, kiểm hash và snapshot trước ghép đúng union toàn plan, rồi mới nhãn. Thiếu/trùng/sai job bị chặn; không cộng hai kết quả của cùng dev thành hai ca độc lập. Không tự xóa remote sau nhận, không chạy lô thứ hai để dự phòng trùng. Output/temp toàn cohort chưa có upper bound; theo dõi free disk và DRAIN trước thiếu chỗ.

## Đã kiểm đúng thay đổi

Giữ40slot DEV cũ và2slot004, baseline G2 và mọi lượt hỏng. Chỉ thêm2lượt M1 trên cùng1ca DEV dev-a915aa2424 để kiểm tuyến mỗi máy. EC2_2: toàn trường khoa học được đối chiếu khớp native EC2_2, wall66,976648s, peakRSS cây1.746.251.776byte, maxgap0,24055s. Nguồn cloud-dev-summary.json. Đây là một mẫu, không chứng minh thời gian/parity mọi cấu hình hoặc mọi ca.

EC2_1: worker hoàn thành nhưng controller chụp danh tính trước exec nên ghi BLOCKED/cost sai. Giữ journal/cost gốc; nhận lại output và kiểm khớp nguồn EC2_2, không rerun method. Không dùng runtime/RSS lượt này cho dự toán. Sửa bắt tay token+argv trước pin PID; chín kiểm công cụ giả trên laptop và cả hai EC2 đạt. Source code cuối9script khớp gói kiểm Linux r2; phần khoa học nền93pin không đổi. Nguồn ec2-1-cloud-dev-summary-corrected.json, retained-failures.json, *-final-checks-r2.json.

60kiểm transport hiện hành đạt; trình biên dịch metadata giả giữ1.642vị trí (1.641job+1insufficient), ba hợp đồng máy/union đạt, thiếu lô/job/C-e bị chặn, protocol chưa khóa bị chặn trước source bundle. Không chạy dataset trong phép kiểm này. Giữ lỗi ghi summary trùng tên/partial; bản tổng kết hợp lệ materializer-final-checks.json khai nguồn phục hồi. Nhận cloud dùng API receive_paths/merge_partitions; runbook chỉ đúng cách ghép trong cùng process.

## Ước lượng và mốc dừng

**5–9giờ là kịch bản cho tính toán+chuyển+seal+chấm, chưa kiểm toàn cohort; không là trần cố định hoặc ETA toàn task.** Giả định cloud40–120s/lượt family/C-e, chỉ1mẫu thật~67s; hai worker khi RAM cho phép; baseline dùng timing có sẵn; setup/chuyển0,25–0,5h dự kiến. Nếu ca nặng/I/O/solver/lỗi/RAM khác, thời gian đổi. Đọc ca, phân tích cơ chế và báo cáo nghiên cứu còn riêng, chưa có số đáng tin. Không cần thêm benchmark mặc định chỉ để làm ETA đẹp hơn.

Không đặt trần cộng dồn P7; timeout từng lượt đề nghị600s/C-d3 60s, poll0,1s/maxgap<5s. Lỗi/không tiến triển/lặp vô tận/hàng chục giờ chưa xong thì dừng báo Minh. Ba sai khác số học cũ được chấp nhận riêng; không dung sai chung. Hai độ nhạy giữ nguyên, không đổi phép chính/mức OB.

## Minh cần xét trước main

1. Xét/khóa G3 đúng freeze007, protocol/host/placement/policy/nguồn được trình. Không tự gắn LOCKED_G3, không commit/push.
2. Grant test94 và chấm, quyền chuyển TT60 sang đúng hai EC2; sau quyền mới dựng/attest runtime/nguồn độc lập/nhãn và C-e support. Metadata compiler đã kiểm bằng dữ liệu giả, chưa có plan test nguồn thật. Nếu lỗi mới thì dừng đúng phần phụ thuộc.
3. TORAI A vẫn phụ ngoài A4; chỉ dev-a5cabe5fa7 đã được cấp. Cần grant3CSV tác giả đúng TTcohort trước biên dịch full plan hiện tại; không tự bỏ A hoặc suy quyền từ B.
4. RE3 giữ ngoài: hợp đồng metadata chuẩn bị đã có, H1/schema và H2/adapter thật còn OPEN/quyền riêng. G3(a) không hoàn thành nghĩa vụ RE3 hoặc tự mở30ca giữ ngoài. Chưa cài/kiểm adapter trên telemetry RE3.

AGENTS đã áp mục1/3 Minh duyệt: nới task/phiên khi checkpoint đủ; bắt buộc xem/tận dụng đầu ra cũ trước chạy thêm. Không áp mục2 chuyển phản biện tự động; prompt Claude vẫn do Minh chọn chuyển. Checkpoint004 trở về trước là lịch sử, không ép các hồ sơ mutable mới khớp manifest cũ. LOG/SPEC/STATE và manifest005 là điểm nhận tiếp; không mở lại task cũ. P7 chưa xong pha2, chưa trả lời RQ3 độc lập hoặc xác nhận cơ chế vật lý.
