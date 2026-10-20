# T-032 — BARO và SimpleRCA: nghiên cứu đang hoàn tất

Bản này trả lời phần BARO và SimpleRCA đã đọc và giữ rõ việc còn thiếu của cả sáu phương pháp. T-032 chưa xong, RQ2/G2 chưa đóng. Khớp phát lại và đủ bảng nguồn là điều kiện dùng trung gian; chúng chưa tự xác nhận nguyên nhân thất bại.

## Kết luận hiện có

**BARO — định vị được bước tạo điểm, chưa phân xử đủ nguyên nhân của mọi ca sai.** Trên 52 ca đã phát lại khớp, root vẫn có khóa/hạng. Trong các ca có caller trên root đã đọc, khóa caller xuất phát từ max robust-z của metric riêng caller, sau chuẩn hóa bằng median/IQR của nền; ánh xạ service lấy max metric. Code không nhận cạnh/caller/trace để truyền điểm hoặc ưu tiên caller theo tên. Có caller thắng bằng latency, cũng có mem/CPU. Nguồn: `results/T-032/runs/research-baro-manual-view-001/manual-review-001.json#/cases`, `#/M5_cases`; chuỗi gốc ở `results/T-032/runs/research-baro-006/closed/baro-saved-chains.json#/cases`.

Mười ca M5 union gồm 3 RE2 và 7 Nezha được giữ trạng thái riêng; bảng không chỉ giữ caller thắng. Các con số này lấy từ manifest BARO `/counts`, không là tỷ lệ cơ chế hoặc nhãn lan. `results/T-032/runs/report-simple-007/phan-xu-caller-root.json#/BARO_cases` giữ đủ 52 dòng, `source_M5_k` và từng caller có nguồn. Việc caller đứng trên root không đồng nghĩa caller ấy là winner top-1: một entity khác có thể thắng toàn bảng.

Đối chứng cùng ô travel|loss cho thấy cùng công thức và caller latency cao có cả trong ca đúng: dev-a5cabe5fa7 root mem 17,285714 dưới food latency 45,459443; dev-7f1b6b071d root mem 103,25 trên food latency 42,727881. Số nguyên bản và IQR/numerator ở `results/T-032/runs/research-baro-manual-view-001/reading-view.json#/cases/19` và `#/cases/15`; cặp đã khóa tại `#/locked_controls/8` và `#/locked_controls/11`. Giá trị/coverage khác, không phải can thiệp giữ mọi yếu tố. Đây là bằng chứng chống diễn giải “đặc tính max hoặc caller latency cao tự nó là nguyên nhân mọi ca sai”; chưa phân tách riêng ảnh hưởng scale, numerator hoặc mất thông tin.

Bước lọc constant riêng N/A và lấy giao thực sự bỏ một số cột. Ví dụ travel error mất khỏi giao ở cả ca sai dev-a915aa2424 và ca đúng dev-7f1b6b071d (`results/T-032/runs/research-baro-manual-view-001/reading-view.json#/cases/20/column_stages`, `#/cases/15/column_stages`). Root còn. Có thể định vị mất cột ở bước tính; chưa chứng minh giữ cột sẽ đổi hạng hoặc đây là lỗi dataset. Phần đọc chi tiết ở `results/T-032/runs/research-baro-manual-view-001/doc-tay-baro-001.md`.

**SimpleRCA — định vị bước tạo chênh điểm và phép nén thông tin; nguồn vật lý chưa phân xử.** Native đếm từng mẫu A finite vượt μN+3σN ở từng cột rồi cộng metric events; trace p95A>3p95N và log keyword count>0 mỗi kênh chỉ góp 0/1. Native không nhận quan hệ caller/root hoặc tách chờ/self-work. Điều kiện và chuỗi ở `results/T-032/runs/research-simple-manual-view-001/manual-review-001.json#/mechanisms`; code đúng pin ở `#/source_checks/code`. Scalar 52 ca và 14 ca M5 union (5 RE2,9 Nezha) có trạng thái riêng ở `#/counts_source`, `#/cases`, `#/M5_caller_root`; đây không là 14 nguyên nhân độc lập.

Ở order|loss RE2, dev-20acb4402d có root240 metric+1trace=241, inside-payment293+1trace+1log=295. Caller mem count195/root17 nhưng latency-50/90 caller27/71 thấp hơn root30/180. Đối chứng đúng cùng ô dev-260d332c8d có root595+1=596 trên caller330+1+1=332 dù caller trace/log vẫn alert. Bước cộng đa cột tạo chênh quan sát; cùng rule có root thắng. Khác coverage/giá trị nên chưa là can thiệp giữ mọi input. Nguồn manual `#/M5_caller_root/0`, `#/cases/6`, `#/cases/7`, `#/locked_controls/0/classes/0`; lớp k5 ở `#/locked_controls/5/classes/0` không là ca độc lập mới.

Phép 0/1 loại độ lớn vượt trace và tần suất log khỏi khóa xếp hạng. Nezha dev-9fd793feb7 có shipping metric16+trace1=17 dù p95A577830,45>threshold1487,55; checkout metric19+trace0=19 vẫn hơn root (`#/cases/50`, `#/M5_caller_root/12`). Các ca log caller/root khác count nhưng cùng vote1 giữ ở `#/cases/35`, `#/cases/39`, `#/cases/51`. Đây là mất thông tin tại bước tính; chưa chứng minh severity/frequency là căn cứ nhân quả tốt hơn hoặc đổi weighting sẽ cải thiện.

Root zero ở dev-607751ac0a và dev-63c30faf34 vẫn nằm trong ứng viên; các kênh có mẫu finite nhưng không vượt gate. Chưa gọi zero là root mất, collector sai, fault absent hoặc nền nhiễm. Đối chứng cùng checkout|network_delay dev-2bfc97b01e có root16 metric trên frontend1, trace/log0 cả hai (`#/cases/41`, `#/cases/42`, `#/cases/33`, `#/locked_controls/17/classes/0`). Recommendation dev-5467884de4 đúng k5 nhưng vẫn dưới caller; không là ca đúng k1 hoặc đảo ưu thế caller (`#/locked_controls/24/classes/0`). Caller thắng bằng memory/trace cũng có, nên không gán mọi M5 cho metric latency (`#/cases/43`).

Đọc chi tiết: `results/T-032/runs/research-simple-manual-view-001/doc-tay-simple-001.md`. Metadata/endpoint của25 yêu cầu/331 lớp và các cặp mô tả được giữ; full per-link row-witness/runtime discrimination còn OPEN ở manual `#/open_items`. Lớp khác cell chỉ cùng giao thức, không thay cùng fault/input. Scalar FrontLatency/PodServerLatency tương đương chưa chứng minh arrays trùng hoặc duplication. Bảng ghép giữ52 SimpleRCA ở `results/T-032/runs/report-simple-007/phan-xu-caller-root.json#/SimpleRCA_cases`,14 trạng thái ở `#/SimpleRCA_M5_case_statuses`, lớp khóa ở `#/SimpleRCA_locked_controls`; không nâng manual_complete hay physical-wait PASS.

## Phạm vi sáu phương pháp

| Phương pháp | Bằng chứng được nhập ở bản này | Câu chưa trả lời và phần thiếu |
|---|---|---|
| BARO | Chuỗi nguồn 52 ca; scalar root/caller, giữ/bỏ cột; 10 ca M5 có trạng thái; các cặp scalar đã đọc | Chưa đọc đầy đủ 501 class links và actual runtime paths; chưa nhận cơ chế của mọi nhóm hoặc nguồn vật lý tín hiệu |
| SimpleRCA | Chuỗi 52 PASS; 14 M5 riêng; 331 link metadata; cơ chế tính có điều kiện/đối chứng | Scalar 52 ca, 14 M5, cộng events/phiếu và đối chứng đã nhập; full row-witness/runtime paths và giải thích vật lý còn thiếu |
| MicroRank | Khung nguồn/seed/nhóm đầy đủ từ bao-phu-nhom | Tiêu chí Q-94 còn hiệu lực; ca bị chặn và chẩn đoán laptop theo Q-97/Q-100 tách riêng; chưa dùng lượt lệch, chưa cohort41 hay A′ |
| TraceRCA | Khung nguồn, nhóm non-OK và đơn vị đã khóa | Kiểm công cụ/pilot/lõi và chuỗi mean/std→support/confidence→ji→hạng còn cần hoàn tất |
| CIRCA OLS–DA | Khung nguồn/cấu hình và đơn vị đã khóa | Fixture/pilot exact và hồi quy→RHT→DA→khóa chưa đủ; không áp ngoại lệ MicroRank, không bỏ phép kiểm |
| TORAI B | Khung toàn đơn vị và seed riêng đã khóa | Trung gian, nhánh tính thật/dự phòng và đối chứng từng seed còn thiếu; không gộp seed để nhận cơ chế |

Nguồn khung: `results/T-032/bao-phu-nhom.json#/counts`, `#/units`, `#/groups`. SimpleRCA: `results/T-032/runs/research-simple-004/closed/manifest.json#/counts`, `#/files`; chuỗi lớn giữ trên EC2 với pin trong receipt, không chép lại hoặc suy luận từ đủ file. `results/T-032/runs/report-simple-007/chuoi-bang-chung.json#/methods` và `#/units` giữ tất cả đơn vị, kể cả non-OK/pending, không thu hẹp phạm vi theo mức dễ đọc.

## Thời gian chờ và quyết định nghiên cứu

Bảng trace hiện có 30 RE2 và 22 Nezha ở mức đo một phần theo schema/interval/coverage (`results/T-032/kha-nang-do-trace.json#/by_dataset`). **Đây là kết quả tạm, chưa là kết luận cuối về đo chờ:** chưa đọc instrumentation đúng phiên bản dataset và chưa phân loại gọi đồng bộ, song song hay bất đồng bộ cho từng caller/root theo Q-120. Hạng, parent–child và duration không xác nhận caller await root. Nguyên nhân vật lý vẫn OPEN; không nhận self-time, nhãn lan hoặc “lan đáng kể”. Metric Nezha 5N+5A là thứ tự adapter, không là mẫu đồng thời để ghép với span.

Bằng chứng BARO đủ đề xuất xét ngữ cảnh quan hệ hoặc bảo toàn thông tin bị lọc; chưa đủ chọn cơ chế tách chờ hay khẳng định đồ thị tăng RCA. Nếu phát triển ứng viên, phải nêu nút/cạnh, kênh ở đâu và phép tính dùng cạnh. Căn cứ DT18 về quan hệ tách khỏi bằng chứng một hạn chế; không dựng nguyên nhân để hợp thức hóa đồ thị.

Bản ghép nhập thêm bốn finding tính toán có điều kiện của SimpleRCA; chúng chưa đóng căn nguyên vật lý hoặc toàn nhóm. Năm đầu ra P4 hiện được phủ một phần: (1) định vị đóng góp số và mất một cột theo điều kiện; (2) tách khuyết công cụ/thiếu đầu vào khỏi hạn chế dataset; (3) mô tả đúng max/scale và đối chứng, chưa nhận tác động riêng là nguyên nhân chung; (4) quan hệ chỉ là thông tin ứng viên có thể bổ sung; (5) giữ công việc và câu hỏi còn thiếu theo phương pháp. Chưa có bằng chứng để chuyển mọi ô sang “cơ chế xác nhận”.

## Tiếp tục trong phạm vi đã duyệt

Đọc nốt full row-witness và actual paths của các lớp đối chứng BARO/SimpleRCA từ chuỗi đã kiểm. Thêm trạng thái theo ca trước khi nhận kết luận nhóm. Hoàn tất TraceRCA và MicroRank trước G2, rồi CIRCA/TORAI B theo Q-123. Diagnostic MicroRank một ca laptop đã exact và nhánh 52 ca laptop đã được duyệt theo Q-124/WHY-43 ngày 10/10/2026. Công cụ cohort đang chuẩn bị; phải đạt fixture, audit hồi cứu, pilot và dự toán trước phần còn lại. Chưa nhập diagnostic vào chuỗi nghiên cứu vì audit bridge/capture đầy đủ của nhánh này chưa xong; không đổi tiêu chí theo quyết định đã rút. Với trace, trình phạm vi/nguồn/dung lượng/thời gian nghiên cứu mã instrumentation trước khi làm theo Q-120.

Nếu cần can thiệp lọc/max/scale BARO để phân xử, trình đúng ca/đối chứng, thành phần giữ/đổi, prediction ở điểm/metric thắng/hạng, phạm vi và chi phí; chưa tự chạy. Thiếu semantics phải nêu yêu cầu instrumentation/clock/coverage FlashTicket và phần không thu hồi được từ dữ liệu hiện tại. Các quyết định P5–P6 về chờ/lan hoặc cơ chế đồ thị còn phụ thuộc phần này. Không cần đợi đồ thị mới để đọc hạn chế baseline, nhưng không dùng giới hạn đã khai để bỏ phép kiểm còn làm được.


## Kiểm và cập nhật phiên 6

Bản này giữ nguyên các scalar và kết luận BARO/SimpleRCA của lượt006. Đã kiểm lại hash các input/output, đối chiếu toàn bộ object Simple với chunk nguồn; sửa mục việc còn thiếu vốn ghi nhầm helper chưa xong. Cơ chế có điều kiện không đồng nghĩa toàn bộ lớp đối chứng đã được phân xử. TraceRCA đã đạt audit nguồn ERROR và hai pilot exact, cùng hash manifest đóng hai đầu; nguồn `runs/tracerca-pilots-transfer-001/check.json#/status` và `runs/tracerca-pilots-root-001/check.json#/validated_children`. Chưa dùng pilot để chứng nhận đủ52 ca hay cơ chế toàn phương pháp. Instrumentation đúng phiên bản vẫn chưa nghiên cứu; khả năng đo chờ giữ PROVISIONAL.
