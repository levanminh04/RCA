# Phản biện T-021

- **Người phản biện:** Codex — **Ngày:** 05/10/2026 — **Commit/diff đã đọc:** `git diff 5636b69`; đọc riêng toàn bộ đầu ra T-021 chưa được Git theo dõi.
- **Đã đọc:** AGENTS.md; STATE; SPEC và LOG T-021; mẫu REVIEW và review-prompt; MRP, DECISIONS, WHY, LESSONS; hai nguồn DT18/cô; toàn bộ Markdown, CSV, sáu script và các lượt kiểm trong `results/T-021/`. Đối chiếu bằng chứng liên quan của T-002, T-005–T-009, T-012, T-014–T-016, T-018–T-020 và K3. Kiểm hai hồ sơ CIRCA, MicroRank với bài/code chính thức tại revision trong manifest; kiểm thêm code TraceRCA RCAEval. Hai nhánh hỗ trợ chỉ đọc; Codex tổng hợp và chịu trách nhiệm bản này.

## Kết luận chung

Có **1 điểm CHẶN và 3 điểm KHÔNG CHẶN**. Điểm chặn thuộc căn cứ chọn cửa sổ và phạm vi RQ3a của Nezha; không đòi bỏ Nezha khỏi gói. Census, nhóm vị trí và bốn bản chia hiện tại tính đúng; chưa thấy bằng chứng phương pháp đã nhận nhãn trái phép trong T-021.

## Các điểm

### R1. Cửa sổ Nezha dựa vào khoảng giữa mốc tiêm, bỏ sót việc trace/log được chọn theo nhãn — CHẶN

- **Ở đâu:** `results/T-021/goi-g1.md:27,82,169,171`; bước 4 và 6 của SPEC, phần chọn cửa sổ và giới hạn RQ3a.
- **Sai gì:** gói gọi khoảng giữa hai mốc tiêm là thời gian “nghỉ”, rồi dùng nó làm căn cứ đề xuất dữ liệu bình thường trước mốc tối đa 300 s. Nhưng trace/log Nezha không có coverage liên tục trong khoảng này. Đây là giới hạn **đã kiểm**, không chỉ là chất lượng bình thường OPEN. Mục giới hạn tự phát hiện chỉ nêu RE2-TT và Eadro, bỏ Nezha.
- **Bằng chứng:**
  - `runs/kiem-phien-001/ket-qua.json:39–44` báo khoảng **mốc tiêm → mốc tiêm** 482/521/2.061 s và ghi rõ không có thời lượng tiêm. Script `kiem_phien.py:41–51` chỉ lấy hiệu hai timestamp bắt đầu. Nó không đo khoảng kết thúc lỗi → lần tiêm kế hay thời gian phục hồi.
  - `results/T-008/the-dataset.md:74,80` và `runs/sampling-leakage-001/result.json` xác nhận toàn 101 record: trace/log chỉ có file của phút tiêm, +1, +2; không có file giữa các lần tiêm. Riêng OB: 24 nhãn/72 file mỗi modality ngày đầu; 32 nhãn/96 file ngày sau. Construct chỉ có một file trace mỗi ngày. Đổi tên file không khôi phục dữ liệu bình thường bị thiếu.
  - Đã tính lại `kiem_phien.py` trong bộ nhớ bằng `py -3 -B -X utf8 -`; JSON khớp lượt lưu. Khoảng giữa mốc đúng, cách diễn giải thành “nghỉ” sai.
  - **Đã xét đoạn phản bác:** dòng 82 gọi normal Nezha “yếu”, còn câu 2 ghi nguồn no-fault Eadro “chưa kiểm”. Hai câu này không nói được rằng trace/log Nezha bị chọn theo nhãn ngay khi thu/xuất. Metric theo ngày vẫn là nguồn khác; finding không khẳng định mọi detector metric đều không dùng được.
- **Hậu quả:** Minh có thể duyệt một cửa sổ trước mốc không có trace/log tương ứng, hoặc hiểu rằng corpus Nezha phân xử phát hiện liên tục đa nguồn công bằng. Sự tồn tại và biên recording còn mang thông tin thời điểm từ nhãn. Chưa có bằng chứng rò này đã được dùng trong một lượt P3.
- **Đề xuất sửa:** sửa “nghỉ” thành khoảng giữa hai mốc tiêm. Đưa giới hạn capture của Nezha vào mục RQ3a và câu cửa sổ; phân biệt ranking biết trước cửa sổ với phát hiện liên tục. Ghi nguồn nền trace/log thực sự có và giới hạn của nó; giữ normal/clock của metric là OPEN. Dùng bằng chứng đã có, không cần thực nghiệm mới.

### R2. Phương án chia Nezha theo ngày không bảo toàn các lần lặp cùng ô — KHÔNG CHẶN

- **Ở đâu:** `results/T-021/goi-g1.md:169`; câu 1, phương án (b); bước 5 của SPEC.
- **Sai gì:** gọi phương án “mỗi phía một ngày” là “không rò”. Phương án này giải việc đọc chồng recording theo ngày, nhưng đưa các lần lặp của cùng root × loại lỗi sang hai phía. Đây là **mâu thuẫn của phương án CANDIDATE**, không phải lỗi của bốn CSV hiện tại.
- **Bằng chứng:** đếm nhãn OB trong `results/T-008/runs/run-001/labels.json` bằng `py -3 -B -X utf8 -`, nhóm theo `(service, fault)` rồi đếm số ngày: **23/33 ô xuất hiện ở cả hai ngày, chứa 46/56 ca**. Ví dụ `frontend × cpu_contention` có một record ở mỗi ngày. MRP:116 và WHY-04:43–45 yêu cầu các lần lặp cùng ô đi cùng phía vì chúng có thể để lộ đáp án.
- **Hậu quả:** nếu chọn phương án này, kết quả test kiểm cả những ô đã có lần lặp trong dev. Không được mô tả đó là loại bỏ mọi đường rò. Gói A đang đề xuất chia ô nên chưa mắc lỗi này.
- **Đã xét đoạn phản bác:** dòng 59 cho sửa WHY-04 nếu đổi đơn vị chia. Việc sửa quyết định có thể cho phép giao thức khác, nhưng không làm các lần lặp trở thành độc lập.
- **Đề xuất sửa:** bỏ khẳng định “không rò”; nêu rõ phương án chia ngày đánh đổi chồng recording lấy việc cắt 23 ô. Minh quyết giao thức sau khi biết đúng được/mất; không cần dựng thêm bản chia trong phiên phản biện.

### R3. Các lựa chọn bản baseline từ P1 chưa được chuyển đầy đủ vào gói quyết định G1 — KHÔNG CHẶN

- **Ở đâu:** `results/T-021/goi-g1.md:43,53–59`, mục 6; `results/T-021/de-xuat-tai-lieu-chung.md`; bước 6 của SPEC.
- **Sai gì:** bảng ghi TraceRCA làm đối chứng, nhưng không xác định bản nguyên trạng hay adapter lọc điểm không hữu hạn trước sort. Gói cũng không nối các lựa chọn scorer/coverage CIRCA và full-score/service mapping MicroRank còn **CANDIDATE cho G1**. Q-38 chốt tên/họ và hai nguồn đồ thị CIRCA, không tự chốt các lựa chọn này.
- **Bằng chứng:**
  - `results/T-015/ho-so-microrank.md:281` và `de-xuat-tai-lieu-chung.md:32–44` ghi lỗi raw và nháp policy finite-before-sort, tie, no-evidence đang chờ G1. [Code TraceRCA RCAEval tại revision được kiểm](https://github.com/phamquiluan/RCAEval/blob/259ea4167160256a74ad30004aa3d96a998c846e/RCAEval/e2e/tracerca.py#L86) sort trước khi lọc NaN.
  - Tính lại từ `results/T-007/runs/py312-pin/tracerca-hoa3.tar.gz`, chỉ đọc `hoa.jsonl` trong bộ nhớ: **90/90 ca có NaN; 79/90 ca có cặp điểm hữu hạn tăng trong thứ hạng raw**. Khớp `results/T-015/runs/tracerca-audit/seed0/t007-audit.json`. Ví dụ `re2ob_checkoutservice_cpu_2`: 0,0218579235 đứng trước 0,03125.
  - `results/T-014/de-xuat-tai-lieu-chung.md:21–49` để scorer RHT-only/RHT+DA và giữ metric cô lập chờ G1. `results/T-015/de-xuat-tai-lieu-chung.md:29` để full-score/service mapping chờ G1. Sáu câu hỏi T-021 không đưa các mục này ra quyết hoặc phân công thời điểm quyết lại.
  - **Đã xét đoạn phản bác:** WHY-05 đã yêu cầu adapter xử lý ca lỗi; các hồ sơ P1 đã nêu nháp sửa. Vì vậy finding không nói P3 đã chạy sai, hay bắt cài adapter ngay ở G1. Vấn đề là bảng được trình duyệt chưa chỉ rõ bản nào được duyệt và bản nào còn mở.
- **Hậu quả:** người triển khai P3 có thể tiếp tục dùng raw TraceRCA xếp sai hoặc tự chọn bản sửa/scorer/candidate policy. Những thay đổi này ảnh hưởng cả thứ hạng và tập ứng viên; không phải chi tiết không ảnh hưởng phương pháp.
- **Đề xuất sửa:** ghi tên bản và vai trò rõ, đưa các lựa chọn đã có từ T-014/T-015 vào phần Minh quyết. Nếu để xuống P3, ghi rõ OPEN và thời điểm cần quyết trước chạy; nối nháp WHY tương ứng. Không cần thêm phép kiểm.

### R4. Tập ứng viên chưa đủ SPEC; GAIA chưa được xét theo nhu cầu mà nó có thể bổ sung — KHÔNG CHẶN

- **Ở đâu:** SPEC phần Đầu vào, Đầu ra 1 và Tiêu chí xong; `results/T-021/goi-g1.md:102–121`; `dieu-kien-toi-thieu.csv`.
- **Sai gì:** SPEC yêu cầu mọi bộ có trong K3, không chỉ ba tên tối thiểu. Corpus gốc TraceRCA và dữ liệu mẫu MicroRCA vẫn vắng khỏi bảng/lý do không dùng. Với GAIA, câu “chỉ lỗi bộ nhớ, CPU” chưa giải thích vì sao không xét khả năng bổ sung recording liên tục, hệ ngoài TT/OB hoặc giữ ngoài độc lập.
- **Bằng chứng:**
  - `docs/knowledge/K3-dataset-ung-vien.md:215–216` liệt kê hai **nguồn dữ liệu** trên, không chỉ tên phương pháp. Không có dòng tương ứng trong hai đầu ra T-021.
  - K3:157–165 và [README chính thức GAIA](https://github.com/CloudWise-OpenSource/GAIA-DataSet#quick-start) mô tả trace liên tục hai tuần, trường parent_id, hệ MicroSS và record tiêm có thời điểm/thời lượng. Đây là bằng chứng **theo nguồn, chưa kiểm file**, có thể liên quan N2, N5 và N12; không chứng minh GAIA đã đủ chất lượng hay nên thay gói A.
  - Q-58 xét loại lỗi ở lớp gói. Gói đã có nguồn lỗi mã nguồn, nên việc riêng GAIA chỉ có CPU/memory không tự làm nó mất giá trị bổ sung. SPEC yêu cầu ứng viên trông mạnh mà chỉ thiếu kiểm file được đưa thành câu hỏi cho Minh; sáu câu hiện tại không có lựa chọn này.
  - **Đã xét đoạn phản bác:** bảng đã ghi “chưa kiểm trên file”; đây là khai báo đúng. Nhưng chưa kiểm không phải lý do khoa học đủ để loại, và không thay cho câu hỏi mà SPEC yêu cầu. FAMOS còn OPEN cả census/root/time; tôi không suy nó đã đủ mạnh.
- **Hậu quả:** chưa đạt tiêu chí “mọi bộ ... có một câu lý do không dùng”. Lựa chọn gói nhỏ nhất cũng chưa xét rõ ứng viên có thể khắc phục giới hạn recording đang nêu ở RQ3a.
- **Đề xuất sửa:** thêm một câu có nguồn cho từng corpus còn thiếu. Với GAIA, giải thích nhu cầu nào không bổ sung hoặc trình Minh lựa chọn kiểm file; giữ chất lượng/quyền dùng chưa xác minh ở đúng trạng thái. Không tự tải hoặc chọn GAIA.

## Điều đã kiểm và thấy đúng

- **Nguồn và quyết định:** DT18 yêu cầu đồ thị phụ thuộc và ba đầu ra; cô nêu ví dụ thuật toán/dataset. Gói không biến ba tên dataset hoặc ba họ ví dụ thành thuật toán/release bắt buộc. Q-37/Q-38, Q-58–Q-60 là quyết định của Minh; A/B/C, cửa sổ và các phương án mục 6 còn là đề xuất. Chưa thấy T-021 cam kết cơ chế P6 trước bằng chứng P4. RQ3c và chất lượng bộ giữ ngoài được giữ đúng giới hạn/OPEN.
- **Số liệu:** chạy lại sáu script bằng `py -3 -B -X utf8 -` qua stdin, chặn mọi thao tác ghi và thu đầu ra trong StringIO; không gọi bản chạy bình thường vì chúng ghi ngoài quyền của reviewer. Census khớp `census-002`; vị trí khớp `vi-tri-001`; bốn CSV và báo cáo chia khớp `chia-003`; bốn bảng chính, khoảng mốc tiêm và dung lượng khớp file lưu. Kiểm độc lập tập 735 ca RCAEval từ metadata HF và nhóm vị trí của 64 dòng RCAEval, 117 Eadro, 202 Nezha theo hai clock đều khớp. Các lượt cũ còn lưu báo cáo/stdout; LOG khai báo CSV chia đã bị ghi đè.
- **Cách chia hiện tại:** nguyên ô; TX2 chỉ ở dev; giữ ngoài toàn TX0; RE2-TT 10 ô/30 ca dev và 20 ô/60 ca test TX1. Gói A phân tầng có 50 ô/79 ca dev, 94 ô/148 ca test, 10 ô/30 ca giữ ngoài; mã nguồn 7/7 ca dev/test. Gói B có 35 ca mã nguồn dev. Không dùng kết quả phương pháp để chọn split. Lỗi hậu tố nhóm vị trí tạo báo “vắng một phía” giả đã được LOG khai báo, không làm đổi split.
- **Hai hồ sơ kỹ thuật:** đối chiếu [bài CIRCA](https://netman.aiops.org/wp-content/uploads/2022/08/KDD22-CIRCA.pdf), code gốc/adapter và [source MicroRank tại revision của hồ sơ](https://github.com/IntelligentDDS/MicroRank/tree/efd85e8e6f0fad30f6f8aaf0555e3324d8f5f982). Hồ sơ phân biệt đúng RHT-only với cấu hình CIRCA đầy đủ; detector/partition MicroRank gốc với span3σ của biến thể; fallback, preprocessing và output. Danh sách đã duyệt phủ thống kê, nhân quả, trace/lan truyền, đa nguồn và học đồ thị qua GDN; không có RCA có giám sát, đã khai báo và không tự coi là lỗi so với Q-38.
- **Đường nhãn và đồ thị:** không thấy root label chọn SLI/cột/ứng viên trong `src/microrank/` và `src/circa_kien_truc/`. Mốc tiêm chế độ (a) và biên recording là vấn đề giao thức đã trình, cộng thiếu sót R1. TraceRCA giữ identity service-operation và số span bất thường, nhưng không dùng cha–con/PageRank; so nó với MicroRank còn đổi detector, grouping và scorer, không cô lập lợi ích đồ thị. WHY-07 đã giữ đúng phạm vi đối chứng; thiết kế đối chứng P7 vẫn thuộc G3.
- **Phạm vi ghi:** diff từ mốc chỉ có DECISIONS, WHY và hai dòng STATE; Q-58–Q-60 và LOG xác định phần thay đổi docs chung có trước phiên làm đầu ra T-021. Không có diff của src/task cũ do T-021. Git không cung cấp lịch sử cho các file chưa theo dõi, nên không thể xác nhận mọi thao tác quá khứ chỉ từ diff. Phiên phản biện này chỉ tạo REVIEW.md; không ghi LOG/STATE/runs, không commit, không đọc dữ liệu khóa, không đọc dữ liệu đo mới hoặc repo lưu trữ, không chạy phương pháp hay thực nghiệm mới.

## Phản hồi của người làm (người làm điền sau)

| Điểm | Ý kiến người làm: đúng / sai / chưa kiểm được | Lý do | Minh quyết |
|---|---|---|---|
| R1 | Đúng; phạm vi rộng hơn điểm tự soát N3 của tôi | Kiểm lại `results/T-008/the-dataset.md:72-80`: trace/log Nezha chỉ có file phút tiêm, +1, +2 trên cả 101 record; không có file giữa hai lần tiêm. `kiem_phien.py` chỉ trừ hai mốc bắt đầu. Vậy "nghỉ ≈ 8,5 phút" sai, và đề xuất cửa sổ "trước mốc tối đa 300 s" ở câu 2 không có trace/log để lấy; mục 0 và mục 5 thiếu Nezha trong giới hạn RQ3a chế độ (b). Đồng ý mức CHẶN vì nó đổi câu hỏi cửa sổ Minh sắp quyết. Đề xuất sửa của reviewer đủ, không cần chạy mới. Mặt trái: không có | Duyệt sửa (05/10/2026) |
| R2 | Đúng | Đếm lại `results/T-008/runs/run-001/labels.json` (OB): 33 ô, 23 ô có ở cả hai ngày, chứa 46/56 ca — khớp reviewer. Phương án (b) cho Nezha phá nguyên tắc chia theo ô (MRP §4:116). Lỗi chỉ ở mô tả phương án, không ở bốn CSV. Tôi đã đề xuất (a) cho Nezha nên kết luận không đổi, nhưng câu được/mất phải sửa | Duyệt sửa (05/10/2026) |
| R3 | Đúng một phần | Đúng: bảng mục 2 ghi "TraceRCA biến thể đối chứng" không nói bản nguyên trạng hay bản lọc NaN trước sort (`results/T-015/ho-so-microrank.md:281`); scorer CIRCA (`results/T-014/de-xuat-tai-lieu-chung.md:21-30`) và full-score MicroRank còn CANDIDATE chờ G1 nhưng không có trong mục 6. Hẹp hơn reviewer nêu: SPEC Đầu ra 1 chỉ đòi "bản nào làm baseline, bản nào chỉ để tái lập", không đòi chốt scorer. Mặt trái của đề xuất: thêm 2–3 câu quyết vào gói vốn muốn gọn. Đề xuất của tôi: một bảng ngắn "đã chốt / OPEN, quyết trước khi chạy P3" thay vì thêm câu hỏi riêng | Duyệt sửa (05/10/2026) |
| R4 | Đúng | K3:213-215 liệt kê dữ liệu TraceRCA và MicroRCA; hai đầu ra T-021 không có dòng nào (grep). Một câu cho mỗi bộ là đủ: TraceRCA nội dung không mô tả (chưa kiểm), MicroRCA chỉ là dữ liệu mẫu, không trace span. GAIA: lý do "chỉ CPU, bộ nhớ" không trả lời nhu cầu nó có thể phủ (trace liên tục cho N5/RQ3a chế độ (b) — đúng chỗ R1 vừa chỉ ra Nezha thiếu; hệ ngoài TT/OB cho N2; độc lập N12). Theo SPEC (S12) phải thành câu hỏi tải/không cho Minh. Chưa kiểm GAIA trên file | Duyệt sửa (05/10/2026) |
| N1 | CHẶN (tự tìm) | Vị trí root Eadro-TT dựa trên đồ thị trace toàn file mà thẻ T-009 cấm diễn giải bậc 0 là cô lập vì trace có timestamp lịch sử, lệch biểu kiến (`results/T-009/the-dataset.md:95,282`). Gói dùng "27 root ở 5 nhóm vị trí", "27 ô root không có trong trace", ca bậc 0 làm lý do chính chọn Eadro-TT và làm dữ liệu cho giả thuyết 3 của P4. `vi-tri-root.csv` xếp ts-travel-service là "nguồn", ts-user/payment/seat/travel-plan "không có trong trace" — gợi ý trace export không đại diện phiên. Nguyên nhân khác (Q-33) chưa loại. Đề xuất: ghi cảnh báo này ở mục 0, 3.1, 5; hạ vai trò các nhóm vị trí Eadro thành "theo trace export, chưa chắc là cấu trúc gọi"; nêu điều này như một điều làm đổi đề xuất | Duyệt sửa (05/10/2026) |
| N2 | KHÔNG CHẶN (tự tìm) | RE3-OB giữ ngoài trùng hệ với Nezha-OB (dev) và trùng bộ công cụ với RE2-TT (dev). Mục 5 chỉ nói "kiểm khớp riêng Train Ticket"; cần nói nó không kiểm riêng được trục hệ hay trục bộ công cụ | Duyệt sửa (05/10/2026) |
| N3 | KHÔNG CHẶN (tự tìm) | Mục 3.1 N6 "11 ca Eadro root không có trong trace, 7 ca bậc 0": dev Eadro-TT chỉ có 1 ca bậc 0 (`chia-theo-o/A-phan-tang.csv`); 7 gồm 6 ca RE2-TT. Ghi tách theo bộ | Duyệt sửa (05/10/2026) |
| N4 | KHÔNG CHẶN (tự tìm) | Mục 3.5 "(100 ca)" không khớp tổng nào; RE1-SS còn 25 ca TX1. BARO-FSE-OB có trong CSV nhưng thiếu ở bảng 3.5 | Duyệt sửa (05/10/2026) |
| N5 | KHÔNG CHẶN (tự tìm) | RE3-OB TX0 dựa trên "không thấy nguồn tiếp xúc" (`tiep-xuc.csv`): vắng bằng chứng. Ghi rõ trong gói vì đây là điều kiện giữ ngoài | Duyệt sửa (05/10/2026) |
