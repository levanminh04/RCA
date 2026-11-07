# T-054 — chuẩn bị nguồn thật và ba máy, checkpoint006

**Chưa sẵn sàng chạy main: kiểm tra nguồn thật phát hiện 4/34 ca OB bị điều kiện 5 hàng N + 5 hàng A của bộ đọc hiện tại từ chối.** Đã chuẩn bị danh sách ba máy, chuyển TT và hoàn tất kiểm tra để chỉ rõ điểm chặn. Dừng báo Minh; chưa chạy phương pháp hoặc chấm điểm, chưa khóa G3. Nguồn TORAI A phụ còn một ca thiếu hàng log trước mốc tiêm. Adapter RE3 nằm ngoài ba việc lần này và chưa triển khai.

## Quyền và mức tiếp xúc

Minh cấp đúng ba bước chuẩn bị tại quyen-minh.txt, diễn giải trong preparation-grant.json. Lượt này đã dùng nguồn test để chuẩn bị theo quyền: băm byte, đọc schema/header và timestamp cần cho mốc/cửa sổ/C-e; đã giải nén ba CSV tác giả đúng60ca. Không nói “test chưa từng được mở” sau lượt này. Không đọc giá trị metric/log message/operation để phân tích, không gọi phương pháp RCA, không tạo ranking, không ghép nhãn với kết quả hoặc xem độ đo. Code phương pháp/cấu hình/cohort/cửa sổ/seed không đổi từ ứng viên005.

Phạm vi nguồn A là chuẩn bị cohort theo gói đã trình, không còn chỉ dev. Quyền này không cho phát method A hay main94. Nguồn nhãn G1 được quản lý riêng để chuẩn bị evaluator; không vào packet cloud hoặc method. Không mở RE3, không commit/push, không bật/tắt máy hoặc dọn thêm.

## Phần1 — nguồn thật và danh sách

TT60 giữ180parquet/1.309.388.082byte, từng ca/tệp đúng SHA256/byte của HF revision đã pin. Mốc inject_time lấy từ gói tác giả có sẵn và khớp Git blob từng inject_time.txt trên HF cho đủ60ca; không tải dữ liệu mới. Ba CSV tác giả chỉ được giải nén cho đúng60ca vào vùng private mới:180CSV, **9.244.910byte**. Gói torai-data.zip91.262.227byte đúng SHA256 và biên nhận Figshare cũ. Thư mục cũ chỉ có DEV; không chép/ghi đè vào nó. Nguồn: checkpoint-01-sources.json, TT-injection-source-metadata.json/A-author-source.json trong vùng private được pin.

OB34 đúng G1 và fault_list native đã ghim. Dùng inject_time chính, không đổi sang inject_timestamp độ nhạy. Mỗi ca giữ đúng11nguồn metric và3minute-file trace+3log của giao thức baseline Q85/T026; không mở rộng theo cửa sổ10phút. Tổng226tệp nguồn khác nhau/1.598.103.311byte, hash Git blob và byte khớp cây nguồn Nezha revision d8140101fdb4e7dfb60d3ef9f64706f382b68470. Chỉ hash/header, không dựng payload tín hiệu. Nguồn: checkpoint-01-sources.json và OB-file-source-pins.json private.

C-e: **58ca verified,2ca insufficient** từ timestamp/cậnF/A0 cùng định nghĩa adapter và quan_sat. Đây là hỗ trợ thời gian quan sát, không chứng minh nền khỏe. Không chạy M1 để phân loại;2ca thiếu giữ dòng hỗ trợ gắn sourcehash, không gán0 hoặc bỏ khỏi mẫu số khai. Chứng cứ temporal riêng giữ r, F/H, ô và lý do, không coi hai trạng thái là kết quả khoa học. Nguồn: TT-Ce-temporal-evidence.json private, checkpoint-01-sources.json#/Ce_support.

Danh sách thật giữ đủ1.642vị trí=1.640job+2support. Đã kiểm cấu hình/seed/cửa sổ/env và các phụ thuộc. Chuẩn bị metadata runtime và nguồn riêng gắn đầy đủ thành viên G1; nhãn evaluator ở vùng private, tách khỏi lô phương pháp. Receipt hiện là PREPARATION-BINDING, không giả attest_runtime hoặc LOCKED_G3. Nguồn: checkpoint-01-plans.json và prepared/*.json.

## Danh sách bố trí dự kiến

| Máy | Phần việc | Job trong danh sách | Dòng hỗ trợ C-e | TT raw đã đặt |
|---|---|---:|---:|---:|
| EC2_1 ·13.211.127.97 |30TT: M1-family210, TORAI B90, C-d3 30, C-e28 |358|2|654.702.162byte/90tệp|
| EC2_2 ·3.107.156.186 |30TT còn lại: family210, B90, C-d3 30, C-e30 |360|0|654.685.920byte/90tệp|
| Laptop |OB442job; TT5baseline300; TORAI A phụ180 |922|0|Giữ nguyên bản gốc|

Trong OB442 có68job trảUNSUPPORTED theo giao thức đã khai; không chế đầu vào cho CIRCA/TORAI. Vì vậy tối đa1.572lượt phương pháp được hỗ trợ, không coi1.640job là1.640lượt học. C-c/C-g/C-d1/2 được dẫn xuất từ đầu ra đã khai, không chạy lại baseline để tạo chúng. Danh sách mã mờ từng TT/máy, cơ cấu vế và pin plan tại bo-tri-du-kien.json; đầy đủ từng job tại prepared/ec2_1-plan.json, ec2_2-plan.json, local-plan.json.

EC2 nhận TT nặng theo ưu tiên Minh; laptop giữ nguồn OB ngày dùng chung và các adapter/baseline phù hợp môi trường hiện có. Không cần mọi việc đều cloud. Mỗi host tối đa2worker và1luồng số học/phương pháp khi RAM cho phép; một slot/method×dataset cùng lúc. Prep→TORAI và M1seal→C-d3 phải tuần tự; hai EC2 và lô laptop độc lập song song. Không thêm cache liên vế hoặc lô pilot mặc định.

## Phần2 — chuyển và bảo toàn

Hai luồng SSH chuyển đồng thời, EC2_1~108,80s và EC2_2~109,36s kể từ sau kiểm nguồn đầu gửi; không cộng thành giờ trôi. Mỗi máy đúng90tệp. Kiểm SHA256/byte trước gửi, trong stream và đọc lại đĩa đích. Chỉ rename vùng partial thành data-root khi đủtệp/hash. Bản gốc laptop giữ nguyên. Không chuyển nhãn, OB raw hoặc CSV A lên EC2; không xóa nguồn/kết quả cũ. Nguồn: checkpoint-02-transfer.json và ec2_*-TT-transfer.json.

Đích dữ liệu là /home/ubuntu/rca-p7/T-054/ec2_1/main-005/data-root và ec2_2/main-005/data-root. Code từng host ở cùng parent/code, tiền tố khác nhau để không nhầm receipt khi nhận. “main-005” là tên vùng đã khai ở contract005, chưa có main queue hoặc phương pháp chạy trong đó. Packet128tệp mỗi máy có code đóng băng và metadata TT/plan chuẩn bị, tất cả được hash trước dùng; không chứa nhãn evaluator/A source/OB map. Không cần dựng lại môi trường T025 đã kiểm.

## Phần3 — kiểm trước chạy và lệnh

Cả ba host PASS:103pin code hiện hành, môi trường main đúng fingerprint, executable/PYTHONPATH, source selector/hash, mapping/cohort, config, seed, window, phụ thuộc, partition và policy ứng viên. Candidateauthority bị từ chối đúng WAIT_G3 trên cả ba máy; quyền chuẩn bị không phát được main. Không chạy thêm RCA hoặc baseline. Nguồn: checkpoint-03-preflight.json; ec2_*-preflight.json và local-preflight.json.

Sau staging, free disk EC2_1~8,816GB; EC2_2~13,884GB; laptop~16,791GB tại lúc kiểm. RAM khả dụng tương ứng~7,40/~7,37/~3,26GB; theo ước lượng reserve hiện tại có thể nhận2slot, nhưng không phải bảo đảm peak mọi ca. Driver vẫn kiểm RAM động, không đổi slot chưa chạy thànhTIMEOUT. Output/temp chưa có upper bound toàncohort, cần theo dõi đĩa/DRAIN khi thiếu. Lô nhận giữ pin/receipt/envelope gốc và phân vùng; union đủ/khôngtrùng trước nhãn như runbook005.

Laptop đang cắm điện, pin100%, nhưng sleep khi AC sau45phút; hibernateAC=0. **Phải giữ laptop thức trong main.** Chỉ đọc thiết lập, chưa tự đổi nguồn điện, chưa cài Scheduled Task. Nguồn: laptop-power-readonly.json.

commands-prepared.json chứa lệnh plan/status chính xác cho ba host và lệnh run candidate được giữ chặn. Không hướng dẫn dùng plan DEV/giả làm main. Sau Minh xét G3/cho main, activate_prepared.py nhận quyết định có pin đúng protocol/bundle, mới tạo bảnLOCKED, attest runtime v3 thật, khóa scope policy rồi biên dịch plan/authority cuối bằng compiler đã kiểm. Helper **không phát run**. Cần đưa metadata khóa cuối vào code_root từng host và kiểm pin trước phát. Đây là phần đóng metadata phụ thuộc quyết định cuối, không là vòng thiết kế/pilot mới. Đã kiểm preparation-grant không thể kích hoạt, không sinh activated-001. Không có main grant giả.

## Điểm dừng và giới hạn

Đã hoàn tất lượt chuẩn bị và kiểm tra; dừng báo Minh. Trước main cần xử lý mâu thuẫn nguồn thật với bộ đọc OB, sau đó Minh xét G3/quyền chạy, đóng metadata/authority cuối và giữ laptop thức. Không xin lại quyền nguồn/transfer đã được cấp trong lượt này. RE3 adapter chưa làm, không được tính là đã hoàn tất toàn bộ P7/giữ ngoài. Công việc chuẩn bị không trả lời RQ3 hoặc chứng minh phương pháp hiệu quả.

Giữ lỗi chuẩn bị: import datetime bị wildcard che tên; chọn OBminute ban đầu suy11file theo cửa sổ nhưng phát hiện không có trước khi đọc telemetry và sửa về đúng3file baseline. Giữ sources-failure.json và sources-failure-r2.json. TT/A đã dựng được dùng lại khi tiếp nhận, không giải nén lại hoặc đọc lại timestamp để sửa OB. Validator005 chạy trong lúc LOG đang được nối nên cuối báo lệchLOG; toàn kiểm nội bộ trước bước manifest đạt. Giữ LOG trước phiên và kiểm prefix, không phục hồi hash cũ để che thay đổi hợp lệ.

Không có ETA main mới từ chuẩn bị hash/transfer. Kịch bản0055–9giờ vẫn có điều kiện, chưa phải ETA bảo đảm hoặc toàntask; không đặt trần cố định. Không đánh đổi đủcohort/seed/nhánh để vừa giờ, không bắt đầu main trong phiên chuẩn bị này.


## Bổ sung kiểm timestamp cuối

Đã rà timestamp cả180CSV A:59ca có ít nhất20hàng mỗi phía cho cả3bảng; một ca test-541642b59e có logts N=0,A=41. Hai bảng trace của ca này đủ hai phía. Không gán bảng nguồn đủhash thành phương pháp đủđầuvào; đây là hạn chế nguồn cụ thể của A phụ. Chưa chạy nên không kết luận TORAI A sẽERROR hoặc mất toàn bộ kết quả. Đọccode thấy nhánh log bỏ qua a rỗng và nhánh RCD ghép min sốhàng normal nếu được gọi; kết cục còn phụ thuộc càiđặt/nhánh. Đề nghị giữ nguồn/t/seed nguyênbản, khai trướcG3, áp đúngquytắc lỗi hiệncó; không bù/dịchmốc/thaynguồn hoặc tự bỏA. Không tự thêm cổngduyệt/phépchạy mới từ phát hiện này. Nguồn A-input-limitation.json và source-temporal-final-check.json.

Kiểm log C-e bằng đúng int(timestamp*NS) của chuoi và chuẩn hóa tuple/list khi so JSON:60ca khớp cảF/H/đếmô, không khác trạngthái; vẫn58verified+2insufficient. Hai assertion đầu do so biểu diễn tuple với list, không là bằngchứng lệchsố học; một assertion tiếp làm lộ nguồnA thiếuN, đã chuyển sang báođúnghiệntrạng thay vì épđạt điều kiện20hàng. Giữ chứngcứgốc và bản temporal chínhxác riêng; không chạyphươngpháp.


## Trạng thái cuối — CHƯA sẵn sàng phát main vì bộ đọc OB

Kiểm timestamp11nguồn metric×34ca phát hiện4ca không thỏa guard5N+5A hiệncó, trên30/374cặp ca–nguồn. test-3218391218 có3N/5A ở11nguồn; test-3a1afd6d4f có2N/5A ở11nguồn; test-9712e01207 có5nguồn dư1hàng (6N/5A hoặc5N/6A); test-a8cc0373da có3nguồn5N/6A. Hai ca đầu chỉ có timestamp nguồn bắt đầu muộn hơn t−300; chưa xác định được vì sao thiếu phần trước đó; hai ca sau có timestamp sátbiên với daođộng cadence, không tựgán nguyênnhân vật lý. Chỉ quan sát timestamp và kíchthước, không đọc điểm hoặc thửphươngpháp.

Code src/p3/nezha.py _doc_cua_so bắt buộc len(rows)==10 và5normal. Vì vậy nguồnthật này sẽ bị từchối trước phươngpháp nếu phát nguyênbản. PASS của preflight trước là hash/schema/env/placement, **không phải** đã qua hợpđồng sốhàng. Báo cáo cuối lấy checkpoint-03-final.json, không dùng PASS sơbộ để nhận sẵn sàngmain. Nguồn/luồngchuyển TT/danh sách vẫn giữ hợp lệ.

Đã giữ4ca và toàn34OB, không tựnới guard/bù/cắt/đổimốc/loại ca/gánERROR hoặc0. Đây là điểm cần phânxử/sửabộđọc–giao thức trướcG3, không là phươngphápRCA thấtbại. Chưa sửa src vì ngoài gói chuẩn bị hiệnđượcgiao. Bước đềnghị tiếp là soáthợpđồngđọccửa sổ native và trình patch tối thiểu (src/p3/nezha.py, phần phụthuộc/test tươngứng sau khi xácđịnh), kiểm bằng mẫu tổnghợp; không chạy pilottest để chọn cách chođẹp. Phải trình rõ ảnhhưởng đầu vào cácvế và tínhso sánh, không tựáp cách thuận tiện.

source-bundle-final-prepared.json giữ open_before_run cho lỗiOB; activate_prepared.py từchối trước tạoLOCKED khi điểm này chưađượcgiảiquyết. Đã kiểm bằng activation-source-blocked.json. Một nguồnAthiếuN là hạnchế phụ riêng, chưa kếtluậnmethodERROR. RE3 vẫnngoài lượt. DỪNG báoMinh đúngyêu cầu.
