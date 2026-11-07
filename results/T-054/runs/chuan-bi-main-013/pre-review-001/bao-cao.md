# Chuẩn bị main 013 — chờ Claude kiểm và Minh duyệt chạy

Minh duyệt chuẩn bị013 và D1–D4/R3 ngày07/11/2026; sau đó duyệt ngoại lệ đúng một phép đối chiếu C-e. Codex là người làm, Claude là người phản biện. Đây là đầu ra chuẩn bị, chưa là nghiệm thu G3, lần chạy test hoặc kết quả nghiên cứu main. Quyền tại `preparation-permission.json` vẫn có g3/test_grant/main_dispatch=false.

## Kế hoạch thực chạy ứng viên

| Máy | Phần việc | Job | C-e thiếu hỗ trợ | Worker tối đa |
|---|---|---:|---:|---:|
| EC2_1, 16.176.181.251 | 30 TT: họ M1, T12, baseline BARO/SimpleRCA/TraceRCA và TORAI B | 448 | 2 | 2 |
| EC2_2, 13.236.44.106 | 30 TT còn lại, cùng các vế trên | 450 | 0 | 1 |
| Laptop | 34 OB và TT CIRCA/MicroRank/TORAI A | 742 | 0 | 2 |

Nguồn: `candidate-validation.json#/hosts`, `/jobs`, `/positions`; vị trí chi tiết trong `placement.json` và `prepared/`. Tổng1.640job+2vị trí C-e thiếu hỗ trợ, không bỏ ca. Trong đó 68slot OB UNSUPPORTED đã khai không gọi lõi; tối đa1.572lần gọi được hỗ trợ. Không dùng bảng35/25/OB của011 để phát013. Hai EC2 cũ giữ nguyên bản sao và nằm ngoài lịch này.

Các tuyến giữ local dùng lại bằng chứng hợp lệ thay vì dựng thêm môi trường. CIRCA/MicroRank và OB đã có tuyến Windows ghim; TORAI A cần ba CSV tác giả và metric, giữ nguồn riêng ở laptop. Việc chuyển chúng sang cloud sẽ cần thêm parity và truyền nguồn, chưa có bằng chứng giảm tổng thời gian. Hai EC2 mới xử lý phần TT nặng. Laptop tối đa2worker theo bằng chứng004; scheduler chỉ phát khi reservation×1,25 cộng reserve vừa RAM. Cả hai EC2 cùng loại máy, 2vCPU; chưa có bằng chứng mọi tải đều nhanh hơn hoặc hai worker luôn tăng tốc.

## Bằng chứng tuyến và sửa lỗi môi trường

`cloud-verification.json#/hosts` lưu15đối chiếu mới trên nguồn DEV đã được cấp. M1 TT chính dùng lại checkpoint012 sau kiểm pin; không chạy lại. Sáu vế C-a0/C-a1/bo-E1/bo-E2/bo-E5/T12-on đã đối chiếu đầu vào và kết quả theo trường phù hợp. C-d3 đọc một seal M1 thật từ012, trả UNSUPPORTED_CYCLIC đúng tham chiếu; ba nhánh DAG/cyclic/no-target vẫn có fixture. BARO, SimpleRCA, TraceRCA nhánh OK và ERROR, TORAI B đủ seed0/1/2 đi qua prep3.12 và method3.8. Các hàng có invocation/result/reference ghim, RSS, wall và maxgap. T12 kiểm world-block/tầng/vùng/cạnh ở đúng tham chiếu, không chỉ kiểm mã thoát.

14/15đối chiếu khớp nghiêm ngặt. C-e của dev-a5cabe5fa7 lệch30trường float, tối đa1ULP; đầu vào chuẩn hóa, thứ tự, nhóm hòa và trường rời rạc khớp. Minh duyệt ngoại lệ đúng phép này. `numeric-parity-Ce-audit.json` và `cloud-verification.json` giữ nguyên trạng thái lúc kiểm; `numeric-parity-Ce-decision.json`, `numeric-parity-Ce-lineage.json` và `parity-disposition.json` ghi quyết định tiếp theo. Không thêm tolerance vào phương pháp hoặc các lượt khác; không gọi toàn bộ15phép là khớp byte.

Các lỗi và sửa tối thiểu được giữ đầy đủ: lượt lớn đầu dừng vì event lặp utc; r2 chỉ chạy phần còn thiếu. TraceRCA trên Linux cần gốc có chữ lowercase rcaeval theo bộ phân loại hiện hành; đổi gốc đóng gói, không sửa code khoa học. TORAI cần bốn file causal-learn đã vá từ cùng revision RCAEval như môi trường gốc; chép vào env013, giữ .pre013. Hai lượt repair chỉ bổ sung Trace ERROR và ba seed TORAI chưa hợp lệ. Pilot/repair có exit1 do bước fixture thiếu metadata dù các job nêu trên đã có seal; lượt fixture riêng sau đó và lượt mã cuối đều đạt. Giữ các output/error/archive cũ, không dùng exit0 của một script để thay đối chiếu.

Mã cuối trên mỗi EC2 đạt101fixture (`ec2_1-fixture-current-received.json`, `ec2_2-fixture-current-received.json`). Gồm quyền run/resume, quyền chấm riêng, hai worker và hàng rào A, nguồn A sai pin/thiếu quyền, lỗi A chưa phân loại dừng phần còn lại, snapshot/A4 và các biên worker/monitor. Nhánh kích hoạt dương dùng cohort sinh giả60TT+34OB, đạt11kiểm ở `fixture-activation-003/summary.json`; không tạo LOCKED hoặc grant cho cohort thật. Hai fixture báo cáo thiếu A và chỉ có một seed A đều tạo89hàng, giữ A4 và không bình quân seed sống (`report-A-*/summary.json`). Fixture Windows đầu lỗi PID-parent ở worker giả ngắn, lần002 thiếu site-path; giữ cả hai. Lần003 dùng basePython và đúng site-packages đạt68kiểm transport. Linux đã kiểm trọn bộ mã cuối nên không rerun phương pháp thật vì sửa wrapper.

## Nguồn, quyền và vận hành

R1: runtime TT và bản chiếu nguồn đối chiếu được dựng riêng từ hai ref đã ghim; đủ60thành viên, giữ byte/hash/mốc/support, chỉ thay locator bằng mã mờ. OB đủ34. `R1-projection-check.json` và `sources/` ghi bằng chứng metadata; không là runtime attestation G3. Bản đồ gốc/nhãn chỉ nằm ở vùng private hiện có, không vào packet worker. Chưa tạo hardlink test hoặc chuyển byte test mới. Main sau duyệt sẽ materialize TT mờ trên laptop bằng hardlink, và chuyển đúng90tệp/30ca sang mỗi EC2; OB ở laptop dùng226tệp nguồn dùng chung đã có. Theo `launch-conditions.json`, nguồn TT mỗi máy khoảng0,59/0,63GiB; nguồn local406tệp đã có, không nhân bản cohort để viết báo cáo.

`main-packet.json` kê188tệp code/metadata, archive `main-code-metadata.tar.gz` không chứa raw test, nhãn evaluator hoặc bản đồ nguồn thật. Đã stage189tệp gồm chính bản kê lên mỗi máy và kiểm lại106pin code, hai runtime cùng bốn file vá (`ec2_*-final-environment.json`). Runtime main dùng Python3.12.3; TORAI dùng3.8.20. Interpreter main trỏ về bản Python ở checkpoint012, vì vậy phải giữ012. Snapshot packages và executable ghim ở `environments.json`, upstream revision/pins ở `upstream-pins.json`. Lần rà helper cuối bổ sung kiểm106file upstream/bản vá local trước phát (`local-external-code-pins.json`, `local-final-code-environment.json`), gồm CIRCA đúng revision đã dùng; không chạy lại phương pháp. Chỉ helper/main và metadata đổi; năm wrapper giữ nguyên sau101fixture. Mã/metadata sau bổ sung được đối chiếu lại trên mỗi EC2 ở `ec2_*-final-execution-environment.json`. Bootstrap có freeze/pip-check và log tải; không có bộ đếm network tuyệt đối để tuyên bố tổng byte tải chính xác. Các thư viện lớn khai kích thước trong log, không cài torch/CUDA; gói DEV khoảng56MiB. Mỗi lượt fixture/dev bị giới hạn timeout, tổng các lượt trên mỗi máy còn dưới giới hạn60phút của gói.

Lần kiểm cuối cloud còn23,7/24,1GiB, RAM khả dụng khoảng7GiB. Laptop còn15,17GiB và RAM khả dụng2,23GiB, đạt slot lớn nhất cộng reserve. Xem `ec2_*-final-environment.json#/resources`, `local-final-resource.json`. Điều kiện ứng viên: cloud còn8GiB theo kịch bản bảo thủ đã có; laptop còn10,062GiB cho nhận/giữ/chấm. Đây là kịch bản, không phải cận trên dung lượng đã chứng minh. RAM/đĩa/identity kiểm lại trước main; thiếu thì chờ, không giảm reservation hoặc xóa kết quả. AC=0, DC=2700giây tại lần đọc; D3 giữ AC đến xong nhận/kiểm/chấm rồi khôi phục2700giây.

Timeout và monitor giữ hợp đồng: method600giây, C-d3=60giây, một luồng số học, poll0,1giây, gap<5giây, không trần cộng dồn, không tựretry. Lỗi vận hành/nguồn/clock/mất quan sát giữ attempt, dừng và báo; chưa chạy không thành TIMEOUT. TORAI A một plan laptop, chỉ phát sau mọi non-A trong plan đó VERIFIED. Thiếu quyền/sai pin A preflight ghi BLOCKED đúng slot, không chạy; lỗi A chưa rõ giữ quy tắc dừng, ghi BLOCKED cho A chưa phát. A thiếu đủba seed thì chỉ khai thiếu. Toàn snapshot và A4 hợp lệ mới ghép nhãn/chấm; thiếu A không làm mất bảng chính đã đủ điều kiện.

Chạy chính dài hơn1giờ và cần Minh duyệt riêng. `cost-scenario.json` lặp thời gian DEV cho TT cho khoảng6,9giờ tuần tự mỗi EC2; giả sử hai worker chồng hoàn hảo thì EC2_1 khoảng3,45giờ. Đây chưa là ETA, chưa tính local/chuyển/nhận/chấm và giả định sai nếu ca test nặng hơn hoặc RAM/CPU gây chờ. Không hứa xong trong một đêm. Agent theo dõi tới hoàn tất hoặc điểm chặn; không tạo lịch tự động hay tắt máy.

## D1–D4/R3 và câu hỏi còn mở

D1 giữ nguyên sự không rõ của quyền đọc thời gian006, khai đúng cấu trúc thời gian cohort OB đã được dùng sửa adapter source_native. Không cấp quyền hồi tố bằng câu duyệt chuẩn bị. D2 cho trình main TT/Nezha khi H1 RE3 OPEN, không mở RE3. D4 thêm mô tả chênh Hit@5 cặp M1–M4 all34/remaining30/affected4 theo audit006, đủba world; A4/mức thống kê không đổi. Bảng nhóm không tách được tác động adapter khỏi độ khó ca. Quyết định nằm trong DECISIONS/WHY ngày07/11, chi tiết `OB-group-decision.json`. R3 giữ máy cũ ngoài lịch.

Nhánh OB lệch số mẫu chỉ có fixture; dev đã audit không có ca thật loại này, nên không thể bổ sung parity ca thật trước G3 bằng tập dev hiện có. Một ca A có logts thiếu N, giữ nguồn/mốc/ba seed; hành vi thật vẫn OPEN. H1 units/U/alias/r cần nguồn và quyền RE3 riêng. C-e ngoại lệ được chấp nhận cho một phép, không chứng minh mọi nguồn/môi trường đều tương đương.

013 làm cụ thể điều kiện đánh giá RQ3b và phần can thiệp tính toán RQ3d, chưa có hạng/độ đo test và chưa chứng minh lợi ích quan hệ. Nút là service/thành phần; trace tạo cạnh hướng caller→callee, log/metric gắn owner. E1 dùng quan hệ cha–con trừ hợp khoảng con, E2-C gán bằng chứng cạnh về callee, E5 dùng cạnh/SCC, E6a xếp tầng, E7 tạo vùng. C-a1 còn quan hệ qua E1; các vế bỏ thành phần phải được đọc theo tín hiệu còn giữ. Không có đối chứng đồ thị ngẫu nhiên nên không kết luận riêng lợi ích do cấu trúc thật. RQ3c chỉ mô tả vùng vì thiếu nhãn vùng độc lập; RQ3a/M1(b), LLM và đánh giá FlashTicket vẫn thuộc các phần tiếp theo của DT18/cô. Đồng thuận review không thay bằng chứng khoa học.

## Bước tiếp

Claude cần kiểm trên code/diff và output đã ghim; bản cài013 này chưa được Claude kiểm. Phần kế hoạch hai bên đã thống nhất gồm một plan A, A cuối/preflight và một lượt C-d3 từ seal thật; ngoại lệ C-e được Minh duyệt sau khi chạy. Đọc `de-nghi-duyet-main.md`, `../../runbook.md`, `wrappers-013.patch`, manifest và bằng chứng gốc. Chưa commit/push. Danh sách commit sẽ được kê riêng, loại raw/archives/private mapping, và chỉ thực hiện nếu Minh duyệt.
