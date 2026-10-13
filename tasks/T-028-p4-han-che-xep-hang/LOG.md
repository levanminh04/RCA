# T-028 — Nhật ký

## Rà SPEC — vòng 1

- Ngày: 07/10/2026, múi giờ Asia/Saigon (+07:00). Codex; laptop Windows 11; repo D:/RCA-flashticket.
- Vai trò: người làm T-028; Claude là người phản biện kết quả. Đây là rà SPEC trước triển khai, không phải phiên phản biện kết quả của Claude.
- Phân loại yêu cầu: REVIEW. SPEC vẫn ĐỀ XUẤT, chưa được Minh duyệt. Chỉ ghi LOG theo quyền Minh giao riêng trong yêu cầu BƯỚC A.
- USER_CONFIRMED trong phiên: Minh giao Codex làm, Claude phản biện; rà độc lập toàn bộ SPEC, ghi LOG rồi dừng trình đề xuất; chưa chạy task. Không có quyết định nghiên cứu mới được chốt ở lượt này.
- FACT về đầu phiên: LOG chưa tồn tại; thư mục T-028 chỉ có SPEC.md. Git đã có thay đổi ngoài T-028 (DECISIONS, WHY, STATE; đầu ra/code T-026 và các thư mục lượt cũ). Không sửa hay hoàn tác các thay đổi đó.
- FACT về phụ thuộc: dòng T-026 trong STATE đã Xong; LOG T-026 phiên 8 ghi nguyên văn Minh "đóng task", ngày 07/10. Điều kiện T-026 đóng đã có bằng chứng trong repo. Đoạn kế hoạch cũ dưới STATE vẫn nhắc T-026 kế tiếp; LOG phiên 8 đã nói không dùng đoạn đó thay dòng trạng thái hiện hành. T-028 chưa có dòng STATE. Không cập nhật STATE trước khi Minh duyệt SPEC, theo yêu cầu phiên này.
- Đã dùng hai trợ lý nội bộ đọc các phần độc lập: nguồn/quyết định và schema/code. Không thay vai người phản biện; góp ý được kiểm lại trên nguồn và chỉ là đầu vào (QT18). Không dùng hơn hai subagent, không deep research.

### Phạm vi đã đọc và cách kiểm

1. AGENTS.md, STATE, toàn bộ SPEC T-028; cuối LOG T-026 để xác minh đóng task.
2. Đối chiếu trực tiếp MRP §3 RQ2 và P4; PLAN-P3-G2; DECISIONS (đặc biệt Q-33, Q-41, Q-59, Q-61–Q-85, Q-82 thay Q-81); WHY (các lựa chọn P3/Nezha và seed); LESSONS; review-prompt; DT18 và hướng dẫn cô 23/09.
3. Giao thức T-022 V2; hồ sơ đầu vào/công thức/giới hạn của BARO, CIRCA kiến trúc, MicroRank, TraceRCA, TORAI, SimpleRCA trong T-013–T-017; K1 về cơ chế, missing telemetry và đơn vị đánh giá. Dẫn các khác biệt bản cài từ hồ sơ, không mặc định tên phương pháp là bản nguyên trạng của bài.
4. Các JSON chấm và manifest T-024/T-026 đã có; nhãn/allowlist dev T-022 và T-026; ba CSV vị trí/ô T-021. Kiểm schema bằng đọc JSON/CSV, không gọi evaluator hay tính phân tích P4 mới.
5. Code src/p3/: selector, cửa sổ, đọc nhãn, bản ghi, evaluator, worker và các adapter liên quan; Nezha reader/wrapper. Lần theo guard, cửa sổ, chia N/A, O, trạng thái và phân bố hạng.
6. Lệnh chỉ đọc: Get-Content có đánh số dòng; rg/rg --files trên tài liệu/code; ConvertFrom-Json để đọc keys/schema; git status --short; Get-FileHash để giữ baseline trong RAM trước ghi LOG. Không import code, không sinh bytecode, không đọc telemetry test/locked, không chạy phương pháp, không tải hoặc dùng EC2.

### Kết luận vòng 1

Có **7 điểm CHẶN** (R1–R7) và **2 điểm KHÔNG CHẶN** (N1–N2). Tất cả sửa dưới đây là CANDIDATE, chưa áp dụng. Vòng rà chưa đạt điều kiện trình duyệt SPEC để triển khai.

Không thấy lỗi riêng về việc tách P4 xếp hạng khỏi phát hiện/chế độ (b), không dùng Eadro, không mở test, hoặc việc không cam kết đồ thị sẽ thắng. Những phần này khớp MRP/DT18/hướng dẫn cô. Các OPEN về clock/nền sạch/đại diện test và khác biệt bản cài là giới hạn thật, không tự biến thành lỗi chặn cần giải quyết hết trong T-028.

### R1 — CHẶN: đồng nhất số ca sai với mức trượt kỳ vọng

- **Ở đâu:** SPEC.md:52 và 61.
- **Cũ:** định nghĩa ca sai bằng Hit@k kỳ vọng < 1, rồi yêu cầu "tổng số ca sai khớp `1 − Hit@k` × số ca"; non-OK lại tách riêng.
- **Bằng chứng:** src/p3/danh_gia.py:96–107 trả Hit là tổng xác suất; :99–103 cho non-OK/root vắng Hit=0; :135–143 tổng hợp trung bình. Ca thật tại results/T-026/cham-a.md:501: TraceRCA dev-396c8dbf7d, root emailservice, hòa 1–3, Hit@1=1/3. Nguồn máy: results/T-026/cham-a.json → tables.main.methods.tracerca.per_case.dev-396c8dbf7d. Ca này là một ca sai theo SPEC nhưng đóng góp 2/3 vào tổng trượt kỳ vọng.
- **Mới đề xuất:** "Với k=1,5, đếm trực tiếp số ca OK có Hit@k < 1; non-OK báo riêng theo trạng thái. Báo riêng tổng mức trượt kỳ vọng Σca(1−Hit@k_ca), giữ non-OK có Hit=0. Kiểm tổng này bằng n×(1−Hit@k_bảng) trên đúng cohort và quy tắc gộp seed của bảng nguồn; không đồng nhất nó với số ca sai." Thay cả câu kiểm ở bước 1 và bullet kiểm đúng đắn.
- **Vì sao/ảnh hưởng:** tránh yêu cầu không thể đạt và sai mẫu số các nhóm hạn chế. Sai top-1 và top-5 là hai cột riêng; không cộng hai danh sách thành hai ca.
- **Phản bác đã xét:** trên RE2, root không hòa theo khóa đã lưu (T-024/cham-a.md:2305), nên công thức có thể tình cờ khớp. Nezha nằm trong phạm vi và có phản ví dụ thật; RE2 khớp không xác minh công thức chung.

### R2 — CHẶN: chưa chốt cohort/view, đơn vị seed và hợp đồng bằng chứng

- **Ở đâu:** SPEC.md:28–32, 38, 52–54, 61, 72.
- **Cũ:** chỉ nêu file chấm, "từng bảng"/"mọi bảng được dùng", "mỗi phương pháp × dataset × ca" và "hạng root (khoảng hòa)"; chưa chỉ rõ bảng nào làm chính, bảng nào chỉ kiểm điều kiện, xử lý seed thế nào.
- **Bằng chứng:** T-024 có cohorts.dev30/dev19; Q-82 yêu cầu giữ số chính và báo nhóm CIRCA vượt ngưỡng/nhóm còn lại (DECISIONS.md:89; WHY.md:358–362). T-026 có tables.main/sensitivity_A/sensitivity_B/trace_guard theo Q-84/Q-85 (DECISIONS.md:91–92). MicroRank Nezha bảng main: 22 OK, Hit@5=8/22 (cham-a.md:78,87); trace_guard: 21 OK và 1 ERROR, Hit@5=7/22 (cham-a.md:249,258). Đổi view thực sự đổi tập lỗi và ca sai.
- **Bằng chứng về seed/hạng:** WHY.md:194 yêu cầu phân tích từng ca dùng mọi seed; :269 gộp độ đo theo seed của ca trước. T-024 giữ rank_distribution_by_seed và per_seed. TORAI có phân bố hạng không nhất thiết đều trên một khoảng (giao-thuc-v2.md:301; danh_gia.py:54–90). Root TORAI B ở nhánh RCD 0/90 lượt, A phụ 2/90 lượt trong một ca, hòa RCD còn OPEN (T-024/cham-a.md:2320).
- **Mới đề xuất, bổ sung vào Đầu vào/bước 1/codebook/đầu ra:**
  - Bảng chính: RE2 dev30, Nezha tables.main với 22 ca. Sáu phương pháp giữ đủ trạng thái; trên Nezha chỉ bốn phương pháp có phép đo ranking, CIRCA/TORAI là UNSUPPORTED, không diễn giải số 0 thành chất lượng ranking hay root không có tín hiệu.
  - RE2 dev19 là phân tích có điều kiện theo WHY-36; giữ dấu 11 ca đã xác nhận lỗi, không đổi mẫu chính.
  - Nezha: đọc riêng các bảng A22/B21/trace_guard22 đã có để xác định chỗ thay Hit/trạng thái/ca sai; không chọn view theo kết quả. Đặc trưng cho ca/window thay đổi chỉ tính theo cùng codebook sau duyệt, chỉ trên cửa sổ dev được allowlist cho phép; nguồn giống nhau dùng lại. Báo điều kiện thay đổi cơ chế nếu có; không tính tích chéo view mới.
  - TORAI giữ seed 0,1,2: Hit phân tích lấy trung bình mỗi ca như T-024; lưu bằng chứng thứ hạng/nhánh theo từng seed. Ca là mẫu số, không coi 90 lượt là 90 ca. Codebook khai cách tổng hợp đặc trưng/gán đa nhãn khác seed trước tính.
  - ca-sai.json giữ phân bố hạng đã lưu theo seed và min/max là biên, không mặc định mọi hạng giữa hai biên có xác suất bằng nhau. Dòng phụ A giữ giới hạn hòa RCD.
  - Codebook khai theo đúng tín hiệu và tiền xử lý phương pháp thực nhận; đồ thị/độ lệch raw là bằng chứng phân tích, không tự là đặc trưng phương pháp đã nhận. RE2 SimpleRCA chia trace theo start, MicroRank/TraceRCA theo end, CIRCA graph N dùng end<t (giao thức:130–137; src/p3/adapters/circa.py:34–43). Nezha doc_cua_so chỉ đọc outer window; guard N do wrapper áp riêng (nezha.py:245–249; adapters/nezha.py:55,79–82). Không lấy chung start<t làm N mọi phương pháp/view. Thiếu dữ liệu hoặc đặc trưng không áp dụng ghi N/A kèm lý do, không điền 0 hay suy thành "không hiện lỗi".
  - Nhóm ô/vị trí lấy từ nhãn dev đã chốt T-022/T-026. CSV T-021 chỉ dùng để đối chiếu cùng dataset/giả thuyết clock/loại graph, không nối chỉ theo tên ca vì có nhiều dòng cùng ca.
- **Vì sao/ảnh hưởng:** hai người làm dùng cùng cohort, cùng đơn vị và cùng giới hạn thông tin; tránh quy khác cửa sổ/thiếu quan sát thành cơ chế của phương pháp. Không chạy lại phương pháp.
- **Phản bác đã xét:** Q-84/Q-85 vốn quyết cho T-026, không mặc nhiên bắt T-028 tính mọi đặc trưng trên mọi bảng. Đề xuất giữ việc đọc độ nhạy đã có và chỉ tính lại bằng chứng nơi nguồn/window thay đổi; chưa chọn thêm view hoặc ablation. Chi tiết đặc trưng được chốt ở codebook, không phải làm xong P4 ngay trong SPEC.

### R3 — CHẶN: điều kiện gọi là cơ chế không thực hiện được và mạnh hơn bằng chứng

- **Ở đâu:** SPEC.md:54,63 và yêu cầu đầu ra ở 73; đọc cùng rủi ro tại 87.
- **Cũ:** "một đặc trưng chỉ là cơ chế nếu phân biệt ca sai với ca đúng"; "xuất hiện ngang nhau ... không gọi là cơ chế gây sai".
- **Bằng chứng:** MicroRank Nezha main có Hit@1=0 trên 22/22 ca OK (T-026/cham-a.md:78,87): nhóm đúng hạng 1 rỗng. Tỉ lệ ở nhóm rỗng không bằng 0 và không so được. Ngoài ra, liên hệ sai/đúng không phân xử nhân quả; SPEC:87 đã nhận điều này. Q-33 yêu cầu các nguyên nhân khả thi khác (DECISIONS.md:39); MRP.md:171–179 giữ các giả thuyết P4 là ứng viên cần kiểm.
- **Mới đề xuất:** "Giữ đối chứng ca đúng cho k=1,5 riêng; ca đúng là OK có Hit@k=1, ca sai ranking là OK có Hit@k<1, non-OK tách riêng. Báo tỉ lệ và mẫu số khi cả hai nhóm có ca; thiếu nhóm ghi N/A và giới hạn không có đối chứng. Chênh tỉ lệ chỉ là bằng chứng liên hệ quan sát, không là điều kiện đủ hoặc bắt buộc để khẳng định nguyên nhân. Gán theo codebook đã chốt, không chọn/bỏ cơ chế hay đổi ngưỡng theo độ phân biệt. Phân biệt rào cản kiểm trực tiếp từ pipeline với cơ chế ứng viên/chưa kiểm nhân quả; giữ giải thích khả thi khác." Đồng bộ cách gọi trong bước 3, mục kiểm và tiêu chí xong.
- **Vì sao/ảnh hưởng:** không tự loại mọi cơ chế của phương pháp sai toàn bộ; không chọn tiêu chí theo kết quả và không gọi tương quan là nguyên nhân đã xác nhận. Rào cản trực tiếp như root ngoài tập được xếp vẫn có thể được chứng minh bằng hợp đồng đầu ra, không bị hạ thành suy đoán chỉ vì thiếu đối chứng.
- **Phản bác đã xét:** so với ca đúng là hữu ích và phải giữ. Lỗi ở việc dùng nó làm gate và từ "gây sai", không phải ở việc có đối chứng. T-028 không được chạy can thiệp nên giới hạn nhân quả phải được ghi ngay trong hợp đồng kết luận.

### R4 — CHẶN: tính mức tập trung trước khi chốt cách tính

- **Ở đâu:** SPEC.md:52–54.
- **Cũ:** bước 1 tính "ví dụ trùng top-k ... hoán vị trong cùng U" để biết đầu ra có phụ thuộc ca; bước 2 mới chốt codebook.
- **Bằng chứng:** chưa chọn k, đơn vị cặp ca/ô, danh sách ngắn, hòa, non-OK, seed hoặc quy tắc hoán vị. O của phương pháp khác U (WHY.md:247–251; giao-thuc-v2.md:314; T-024/cham-a.md:86–102). Sự tập trung có thể do topology, candidate coverage hoặc tải ổn định; riêng nó không chứng minh phương pháp không dùng dữ liệu ca. Q-33 áp cho nhận định này.
- **Mới đề xuất:** bước 1 chỉ trích các danh sách/độ đo đã chấm. Chuyển tính phép đo tập trung hiện có sang sau duyệt codebook. Bước 2 khai chính xác k, đơn vị, cách xử lý tie/danh sách ngắn/non-OK/seed, đối chứng và ý nghĩa kết luận. Đối chứng phải nêu điều kiện tập ứng viên O và chiều dài danh sách; U nếu dùng thì ghi riêng, không thay đối chứng có cùng điều kiện. Báo "mức tập trung/biến thiên đầu ra trong cohort", không tự kết luận thuật toán bỏ qua dữ liệu ca. Không chọn lại phép đo vì bảng kết quả đẹp.
- **Vì sao/ảnh hưởng:** tránh hai cách tính khác nhau và dùng kết quả trước khi khóa để chọn cách đo. Giữ phép phân tích SPEC đã yêu cầu, không thêm thí nghiệm hay gate.
- **Phản bác đã xét:** chữ "ví dụ" có thể chỉ là ý tưởng để hoàn thiện ở codebook. Vì vậy sửa tối thiểu là khai nó trong codebook và dời tính toán qua sau duyệt; không yêu cầu quyết mọi tham số ngay ở vòng rà này. Mức ngẫu nhiên ranking ở giao thức không tự là cùng một phép đo với tập trung; dẫn O/U ở đây để chỉ rõ điều kiện cần mô tả, không mặc định hai phép đo tương đương.

### R5 — CHẶN: điểm duyệt codebook chưa đáp ứng yêu cầu WHY có hiệu lực

- **Ở đâu:** SPEC.md:37,47,53,71,79.
- **Cũ:** ghi "nháp WHY" trong codebook; chỉ đòi Minh duyệt codebook rồi sang bước 3; cấm sửa docs/WHY.md.
- **Bằng chứng:** AGENTS.md:51 yêu cầu mục trong docs/WHY.md trước dùng lựa chọn quan trọng cho kết quả. PLAN-P3-G2.md:137–139 nói rõ nháp trong results không thay WHY có hiệu lực; giao-thuc-v2.md:5 áp cùng điều kiện. WHY hiện chưa có lựa chọn codebook T-028.
- **Mới đề xuất:** cuối bước 2 và tiêu chí xong ghi: "Trình codebook cùng văn bản WHY (chọn gì, vì sao, phương án, bằng chứng, kết luận phụ thuộc) và phạm vi ghi mục tương ứng để Minh duyệt. Chỉ sang bước 3 sau khi văn bản WHY đã được Minh duyệt và ghi vào docs/WHY.md. Duyệt codebook không mặc nhiên cấp quyền sửa docs/WHY.md; việc ghi chỉ thực hiện khi Minh duyệt đúng nội dung và phạm vi đó." Điều chỉnh câu cấm docs để giữ ngoại lệ chỉ sau lời duyệt riêng này; không cấp quyền viết rộng cả docs.
- **Vì sao/ảnh hưởng:** mọi tính/gán cơ chế có nguồn lý do hợp lệ. Đây là hoàn thiện điểm duyệt codebook đã có, không thêm cổng nghiên cứu mới.
- **Phản bác đã xét:** duyệt codebook có thể duyệt lựa chọn về nội dung nhưng không thay điều kiện nơi lưu của AGENTS. Chưa có văn bản codebook để trình nội dung WHY cụ thể ở vòng này; không tự tạo hoặc sửa WHY bây giờ.

### R6 — CHẶN: đóng băng cả nhãn sai do lỗi triển khai

- **Ở đâu:** SPEC.md:56, đọc cùng bước 4 tại 55.
- **Cũ:** mọi trường hợp đọc tay không khớp đều báo là giới hạn codebook, "không sửa nhãn đã gán".
- **Bằng chứng:** câu này không phân biệt tiêu chí chưa đủ với phép đo/gán không thực hiện đúng codebook. AGENTS.md:111 và Q-41 (DECISIONS.md:47; LESSONS.md:57) yêu cầu sửa/kiểm triệt để điều kiểm được. Đây là lỗi ràng buộc thiết kế; chưa có lỗi lập trình thực tế vì task chưa chạy.
- **Mới đề xuất:** "Nếu phép tính hoặc gán không thực hiện đúng codebook: sửa triển khai trong scripts/ thuộc phạm vi, giữ codebook và mọi lượt cũ, tính lại đúng các đầu ra bị ảnh hưởng; không chạy lại phương pháp. Nếu đã thực hiện đúng mà đọc tay chưa hỗ trợ giải thích cơ chế: giữ gán theo tiêu chí, báo cơ chế ứng viên/chưa kiểm và giới hạn codebook. Muốn đổi tiêu chí thì theo bước 4: dừng trình Minh, giữ bản/kết quả cũ."
- **Vì sao/ảnh hưởng:** tránh bàn giao nhãn biết sai; giữ khóa tiêu chí chống hindsight.
- **Phản bác đã xét:** cấm sửa nhãn để tìm câu chuyện khớp kết quả là đúng. Nhưng giữ tiêu chí khác với giữ một lỗi triển khai tiêu chí; sửa đúng codebook không phải chọn lại phương pháp hay ngưỡng.

### R7 — CHẶN về phạm vi: đã dự kiến hai phiên nhưng chưa tách hoặc có ngoại lệ

- **Ở đâu:** SPEC.md:83.
- **Cũ:** "Dự kiến hai phiên: phiên 1 bước 0–2; phiên 2 bước 3–6."
- **Bằng chứng:** AGENTS.md:95 định nghĩa task một phiên; :129 yêu cầu đề xuất tách ngay khi viết SPEC nếu dự kiến vượt một phiên. PLAN-P3-G2.md:61,99 giữ đúng điều kiện này. Việc có điểm chờ codebook không tự là quyết định của Minh cho ngoại lệ.
- **Đề xuất cụ thể, chờ Minh chọn:**
  - **Khuyến nghị theo luật hiện hành:** tách phần chuẩn bị/khóa codebook và phần tính/bản đồ thành hai task; T-028 giữ phần chuẩn bị bước 1–2 (bước 0 vẫn là rà trước triển khai), đầu ra codebook/nháp WHY/chi phí/LOG; phần bước 3–6 chuyển task tiếp theo với phụ thuộc codebook+WHY được duyệt. Sửa đồng bộ tên/mục tiêu/đầu ra/bước/tiêu chí/chi phí của SPEC T-028. Chưa cấp mã hoặc tạo SPEC task mới trong lượt này; nếu Minh chọn nhánh này phải trình đúng file/phạm vi task mới trước ghi.
  - **Phương án ít thay đổi tài liệu:** Minh duyệt rõ ngoại lệ riêng T-028 được làm hai phiên do điểm chờ codebook; SPEC:83 thay bằng "Minh duyệt ngoại lệ hai phiên riêng T-028 ngày ...: ...", giữ đủ LOG để tiếp nhận. Không sửa AGENTS hoặc suy ngoại lệ cho task khác. Chỉ ghi câu này khi Minh thực sự quyết.
- **Vì sao/ảnh hưởng:** phân chia đầu ra và phiên triển khai, không thay câu hỏi nghiên cứu hoặc bỏ kiểm để ép vừa một phiên. Công/chi phí 3–5 giờ và máy 10–45 phút vẫn là ước lượng chưa kiểm; việc chỉ đổi chữ thành "một phiên" không chứng minh đã vừa.
- **Phản bác đã xét:** hai phiên có thể thực tế hơn khi phải chờ duyệt và chính yêu cầu mở phiên của Minh đã nói cuối mỗi phiên. Nhưng yêu cầu cũng đòi tìm phần vượt một phiên chưa tách; chưa có lời duyệt ngoại lệ cụ thể. Vì vậy cần quyết định, không tự chọn nhánh.

### N1 — KHÔNG CHẶN: bắt độ nhạy ngưỡng cho thuộc tính không có ngưỡng tự chọn

- **Ở đâu/cũ:** SPEC.md:53 yêu cầu mỗi cơ chế có ngưỡng chính và ít nhất hai ngưỡng độ nhạy, ngay cả ví dụ root∈O hoặc hòa khóa.
- **Bằng chứng:** hòa bằng khóa thật là equality theo WHY.md:267; membership/status là thuộc tính rời rạc. QT3 (LESSONS.md:45) yêu cầu khoảng hợp lý, không yêu cầu tự tạo ngưỡng cho mọi thuộc tính.
- **Mới đề xuất:** "Với đặc trưng có ngưỡng số tự chọn: khai ngưỡng chính và ít nhất hai ngưỡng độ nhạy có lý do. Với membership/status/hòa theo giao thức: dẫn quy tắc có hiệu lực, ghi N/A cho độ nhạy ngưỡng; không tự thêm tolerance đổi nghĩa hòa."
- **Vì sao/ảnh hưởng:** bớt kiểm thừa và tránh thay quy tắc khoa học đã chốt.
- **Phản bác đã xét:** người soạn có thể chỉ muốn ngưỡng nơi có ngưỡng; do đó không chặn riêng, chỉ làm rõ phạm vi câu "mỗi".

### N2 — KHÔNG CHẶN: nghĩa vụ kiểm schema cần có tên trong codebook/đầu ra

- **Ở đâu/cũ:** SPEC.md:32 viện WHY/Q-74 nhưng bước 2/6 chưa nêu rõ phần kiểm schema đã giao P4.
- **Bằng chứng:** DECISIONS.md:82, Q-74 Q5; WHY.md:256,260–261; giao-thuc-v2.md:337–339; T-024/cham-a.md:2286 vẫn chuyển tương quan schema với nhãn cho P4. Raw audit có sẵn trong T-024/cham-a.json → raw_column_audit; không cần mở test hoặc chạy L*.
- **Mới đề xuất:** thêm vào bước 2 và báo cáo: "Dùng audit cột có sẵn để báo số/loại/cột vắng theo ca/ô và liên hệ với nhãn dev; đặt cạnh tập O/tập trả về sau tiền xử lý của phương pháp. Không đưa dấu cột vắng vào phương pháp, không chạy L*, không gọi liên hệ schema–root là tác động nhân quả đã tách."
- **Vì sao/ảnh hưởng:** không bỏ việc đã được quyết; số schema giúp xét giải thích khả thi khác của ca sai. Dùng lại audit thay quét lại telemetry khi đủ nguồn.
- **Phản bác đã xét:** codebook được phép bổ sung đặc trưng trước duyệt, nên SPEC viện quyết định có hiệu lực chưa chắc bỏ việc này. Không chặn riêng chỉ vì thiếu một ví dụ; ghi rõ giúp chốt phạm vi để không cần sửa thêm sau duyệt.

### Bản đồ ảnh hưởng và danh sách đề xuất gom theo file

- File cần sửa sau Minh duyệt: tasks/T-028-p4-han-che-xep-hang/SPEC.md, đúng các mục R1–R6 và N1–N2 được Minh chọn; R7 phải có nhánh Minh quyết trước sửa. LOG chỉ ghi thêm lời duyệt, phạm vi áp dụng và vòng rà toàn bộ tiếp theo.
- Tác động: định nghĩa/mẫu số và phân bố hạng (R1/R2); cách kết luận quan sát (R3/R4); thứ tự khai–duyệt–tính (R4/R5); sửa lỗi triển khai mà giữ tiêu chí (R6); phạm vi task/phiên (R7); tránh kiểm thừa và giữ nghĩa vụ schema (N1/N2).
- Không đề xuất đổi baseline, cấu hình P3, dữ liệu/dev-test, độ dài cửa sổ, mở test, chạy lại phương pháp, chọn đồ thị mới hoặc sửa kết quả task cũ. Không tạo quy trình/cổng hay phép kiểm mới.
- Nếu chọn tách ở R7: việc tạo SPEC task mới phải được trình đúng danh sách file và nội dung trước ghi; chưa được bao gồm trong quyền sửa SPEC T-028 này. Nếu duyệt WHY ở bước 2 về sau: trình văn bản và phạm vi riêng như R5; chưa sửa WHY trong vòng rà.
- Đề xuất này chưa được kiểm bằng chạy P4 vì SPEC chưa duyệt và codebook chưa có. Lỗi công thức/nhóm rỗng/view đã được xác minh bằng source code và số lưu sẵn; không cần chạy mới để kết luận các lỗi đó.

### Kết thúc phiên — dừng BƯỚC A, chờ Minh quyết

1. **Đã làm:** rà độc lập toàn bộ SPEC và đối chiếu các nguồn/đầu vào/code nêu trên; ghi 7 CHẶN, 2 KHÔNG CHẶN, có phản bác và sửa tối thiểu. Chưa sửa SPEC, chưa duyệt hoặc chạy BƯỚC B.
2. **File thay đổi:** chỉ tạo LOG.md này theo yêu cầu Minh. Không sửa SPEC/STATE/WHY/DECISIONS, code, kết quả hoặc dữ liệu. Không commit/push.
3. **Kiểm và kết quả:** JSON đầu vào chấm/manifest/nhãn/allowlist tồn tại và parse được; phản ví dụ hòa, nhóm đúng rỗng và thay view có nguồn thật. Kiểm cuối lượt đọc toàn LOG, đối chiếu hash 37 file baseline trong RAM (SPEC, nguồn điều khiển, giao thức, JSON và 20 file code p3), kiểm bộ file T-028 và diff/whitespace; kết quả sẽ ghi thêm ở dưới. Không thực nghiệm/phương pháp/đặc trưng P4 mới.
4. **OPEN/cần Minh quyết:** các sửa R1–R6/N1–N2 và nhánh R7. Chưa có lời "duyệt SPEC T-028". Clock/nền sạch/license/test của Nezha giữ OPEN theo nguồn. Không còn điều kiện chờ T-026 đóng vì đã đóng; vẫn giữ điều kiện trong SPEC để không tự dùng số chưa chấp nhận.

- **Bước tiếp chính xác:** Minh đọc mục Rà SPEC vòng 1 và chọn đề xuất/nhánh R7. Sau lời duyệt đúng đề xuất, Codex chỉ sửa SPEC trong phạm vi đã duyệt, ghi thêm LOG, rồi rà lại TOÀN BỘ SPEC như vòng 2; chưa chạy bước 1–6. Lệnh đọc khi tiếp: `Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/LOG.md'`; `Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/SPEC.md'`; đọc lại nguồn của từng thay đổi. Chỉ sau lời Minh "duyệt SPEC T-028" mới triển khai theo phạm vi/nhánh được chốt.
- **Lệnh cuối dự kiến:** kiểm hash/phạm vi trong RAM; đọc toàn LOG; `git diff --no-index --check -- /dev/null tasks/T-028-p4-han-che-xep-hang/LOG.md`; `git status --short`. Các lệnh chỉ đọc, không có output file. Ghi kết quả cuối bằng append, không sửa nội dung vòng rà.
- Chưa viết prompt phản biện kết quả cho Claude: task chưa triển khai/xong. Khi xong phải chép nguyên Prompt chung theo docs/review-prompt.md (G2 không có khối trọng tâm riêng), không thay bằng danh sách findings vòng rà này.

### Kết quả kiểm cuối vòng 1

- Đã đọc toàn bộ diff tạo LOG (134 dòng trước mục này). Không thấy mâu thuẫn mới giữa kết luận và đề xuất; mọi đề xuất giữ trạng thái chưa duyệt.
- Đối chiếu hash baseline: 37/37 file nguyên, gồm SPEC, STATE/WHY/DECISIONS, nguồn điều khiển, giao thức, JSON và code src/p3. Thư mục T-028 chỉ thêm LOG.md, SPEC.md nguyên. Các thay đổi ngoài task có từ đầu phiên được giữ intact.
- Kiểm whitespace không có thông báo lỗi; git diff --no-index --check trả mã 1 vì so file mới với /dev/null, chỉ có cảnh báo LF/CRLF. Không báo mã này là test thất bại hoặc đạt exit 0. Không chạy test hoặc thực nghiệm.
- Đã kiểm prefix byte của LOG sau append; bộ file cuối T-028 là SPEC.md và LOG.md. Lệnh chỉ đọc cuối trước trả lời: git status --short. Dừng chờ Minh quyết danh sách R1–R7/N1–N2; chưa sửa SPEC hoặc cập nhật STATE.
## Mở lượt sửa SPEC và rà vòng 2 — 07/10/2026

- Codex, người làm T-028; Claude là người phản biện. Thiết bị: laptop Windows 11; repo D:/RCA-flashticket. Chỉ sửa SPEC theo lời Minh duyệt và ghi thêm LOG. Chưa triển khai BƯỚC B.
- **Quyết định của Minh trong lượt:** duyệt R1, R3, R4, R5, R6, N1, N2 theo LOG vòng 1. R2 chỉ bản tối thiểu: bảng chính RE2 dev30 và Nezha main; A/B/trace_guard chỉ đọc số có sẵn để đánh dấu ca đổi trạng thái/Hit, không tính đặc trưng mới; dev19 chỉ dòng CIRCA Q-82; TORAI gộp ba seed theo ca, giữ bằng chứng từng seed; đặc trưng theo đúng N/A từng phương pháp; thiếu ghi N/A. R7 duyệt ngoại lệ hai phiên riêng T-028: phiên 1 bước 0–2 tới duyệt codebook + WHY; phiên 2 bước 3–6, không tách task. Bổ sung đường dẫn nhãn RE2-TT T-022 và điều kiện T-026 đã đóng ở LOG phiên 8.
- Lời duyệt trên là quyền sửa đề xuất SPEC, chưa phải lời “duyệt SPEC T-028”. Không sửa STATE/WHY/DECISIONS trong lượt này. R2 không áp dụng phần mở rộng của đề xuất vòng 1 ngoài bản tối thiểu Minh vừa chọn.
- **Checkpoint do ngữ cảnh bị nén (AGENTS mục 5a):** đã đọc luật, STATE, SPEC, LOG vòng 1 và các nguồn RQ2/P4/WHY/Q-82–85/T-026 phiên 8. SPEC còn bản đề xuất cũ; chưa sửa ở lượt này. Baseline file nguồn và byte SPEC/LOG lưu trong RAM để kiểm phạm vi. Bước tiếp: sửa đúng phạm vi vừa duyệt, đọc toàn bản sửa và đối chiếu toàn nguồn ở vòng 2, ghi kết luận, dừng trình Minh. Đề nghị mở phiên mới khi chuyển sang triển khai để tiếp nhận từ LOG này.

### Sửa SPEC theo lời Minh duyệt

- Đã sửa đúng SPEC.md: R1 ở bước 1/mục kiểm; R2 bản tối thiểu ở đầu vào/đầu ra/bước 2–3/kiểm/tiêu chí; R3 ở đối chứng và giới hạn kết luận; R4 dời phép đo tập trung sang bước 3 và khai trong codebook; R5 đồng bộ điểm duyệt codebook + WHY với phạm vi ghi; R6 tách lỗi triển khai khỏi giới hạn tiêu chí; N1 chỉ kiểm độ nhạy nơi có ngưỡng số tự chọn; N2 dùng audit schema có sẵn. R7 ghi đúng ngoại lệ hai phiên riêng T-028, không tách task. Bổ sung đường dẫn results/T-022/nhan-dev.json và nguồn đóng T-026 LOG phiên 8.
- Không áp phần mở rộng R2 vòng 1: không tính đặc trưng cho Nezha A/B/trace_guard; không phân tích phương pháp khác trên dev19. TORAI giữ ba seed theo ca của RE2; dòng UNSUPPORTED Nezha vẫn giữ trạng thái theo Q-85.
- Trạng thái SPEC vẫn đề xuất, chưa duyệt triển khai. Giữ nguyên mục tiêu RQ2, Eadro loại tới G2, phương pháp/cấu hình/cửa sổ và kết quả task cũ.

## Rà SPEC — vòng 2

- Phạm vi: đọc lại TOÀN BỘ SPEC sau sửa, gồm mục tiêu, điều kiện, đầu vào, đầu ra, phạm vi ghi, bước 0–6, kiểm, tiêu chí xong, phần không làm, chi phí và rủi ro. Đối chiếu trực tiếp DT18/advisor, MRP §3/P4, PLAN-P3-G2, DECISIONS, WHY, LESSONS, review-prompt, giao thức T-022, đầu vào chấm/manifest/nhãn/audit/vị trí và code đọc/chia cửa sổ src/p3. Không chỉ rà các đoạn sửa.
- **Kết luận:** không phát hiện điểm CHẶN hoặc điểm mơ hồ ảnh hưởng kết quả còn lại ở cấp SPEC. Không có đề xuất sửa mới. Các định nghĩa/chi tiết được giao cho codebook là việc bước 2, phải chốt và được Minh duyệt cùng WHY trước bước 3; chưa coi codebook hay cơ chế là đã xác nhận.

### Bằng chứng và phản bác đã xét trong vòng 2

- **Phạm vi khoa học:** SPEC:10–18,63,85 giữ P4 xếp hạng chế độ (a), chỉ dev; phần phát hiện/chế độ (b) để T-029. Khớp MRP:71,169–181 và DT18:16–18/advisor:26. MRP nói “cơ chế gây ra”, nhưng dữ liệu quan sát không tự phân xử nhân quả; SPEC:41,69,73,93 giữ rào cản trực tiếp/cơ chế ứng viên và giải thích khác. Không cần chạy can thiệp ngoài phạm vi để làm cho báo cáo trông kết luận được hơn.
- **Số ca, hòa, seed, nhóm rỗng:** SPEC:30,54,67,69 không còn đồng nhất số ca sai và tổng trượt. src/p3/danh_gia.py:96–107,135–143 xác nhận Hit là kỳ vọng và bảng là trung bình. Phản ví dụ đã lưu T-026/cham-a.json → tables.main.methods.tracerca.per_case.dev-396c8dbf7d vẫn phù hợp công thức mới. Nhóm đúng hạng 1 của MicroRank rỗng (T-026/cham-a.md:78,87) được báo N/A, không ép tỉ lệ bằng 0. T-024/cham-a.json → methods.torai_B.per_case có seed_metrics và status_by_seed_counts; gộp từng ca theo WHY:269, không đếm lượt thành ca. Hạng min/max chỉ là bằng chứng đã lưu, không dùng khoảng đó để tự chấm lại; giao thức:301 giữ nghĩa hòa khối TORAI.
- **Cohort/view và dữ liệu thật:** T-024/cham-a.json có cohorts.dev30/dev19, methods.*.per_case và summaries.dev30/dev19; T-026/cham-a.json có tables.main/sensitivity_A/sensitivity_B/trace_guard. SPEC:28–30,56,60,67,78 giữ bảng chính và giới hạn bản tối thiểu Minh duyệt. Dev19 chỉ CIRCA Q-82 (DECISIONS:89; WHY:358–362). Q-84/85 (DECISIONS:91–92; WHY:367–379) không bị đổi thành quyền tính đặc trưng mới trên bảng độ nhạy. Dòng UNSUPPORTED có Hit=0 trong file chấm nhưng không là bằng chứng chất lượng ranking hoặc root ngoài O (SPEC:28).
- **Cách chia và nhãn:** SPEC:56 dẫn cách chia theo từng phương pháp. Giao thức:130–137 và src/p3/adapters/circa.py:34–43 xác nhận start/end/train riêng. src/p3/nezha.py:245–255,270–282,293–306,319–320 chỉ lấy cửa sổ ngoài/ordinal; adapters/nezha.py:39–62,79–82,191–230 mới áp chia/guard cho từng phương pháp. SPEC:71 giữ nối nhãn sau đặc trưng không cần nhãn; chọn root để đọc đặc trưng là phân tích, không gửi vào phương pháp. Guard selector.py:58–88 và nezha.py:160–211 kiểm allowlist/path/hash. Không gọi worker/phương pháp hoặc đọc dữ liệu đo mới trong vòng này.
- **Schema, vị trí và khả thi:** các nhãn dev T-022/T-026 có cell/nhom_vi_tri_p75; CSV T-021 là nguồn metadata đối chiếu và có chiều graph/clock, không là dữ liệu đo được phép mở test. raw_column_audit của T-024 có union_columns/union_n/by_case và danh sách cột từng ca; đủ cho nghĩa vụ schema được khai tại bước 2/6 (SPEC:58,63,79; WHY:256–261; giao thức:337–339). T-013–17/K1 phân biệt kênh phương pháp dùng, giới hạn dữ liệu/biến thể và hạn chế tác giả; SPEC không coi mô tả của tác giả hay REVIEW cũ là kết luận theo ca. Thiếu hoặc không áp dụng ghi N/A, không bổ sung tín hiệu hay chạy L*.
- **Khóa lựa chọn, phép đo và sửa lỗi:** SPEC:55–60,69–70 chốt cách đo/ngưỡng trước tính; không chọn cơ chế/ngưỡng theo độ phân biệt. O/chiều dài danh sách được điều kiện hóa trong phép tập trung (WHY:247–251; giao thức:314); tập trung không tự chứng minh bỏ qua đầu vào. N1 không đổi equality của khóa hòa (WHY:267). SPEC:49,59,77,85 yêu cầu WHY được Minh duyệt đúng văn bản/phạm vi và ghi trước bước 3, khớp AGENTS mục 3.3/PLAN:137–139/giao thức:5. SPEC:61–62 cho sửa triển khai trái codebook nhưng giữ tiêu chí/mọi lượt; đổi tiêu chí vẫn phải trình. Không thêm cổng hoặc phép kiểm mới.
- **Phụ thuộc và phiên:** T-026 LOG phiên 8 ghi Minh “đóng task” ngày 07/10/2026; SPEC:23,89 dẫn đúng nguồn, không nâng clock/nền sạch OPEN thành đã xác nhận. SPEC:89 ghi ngoại lệ hai phiên đúng lời Minh, chỉ T-028; chi phí vẫn chưa kiểm. Các công việc tính/đối chứng/đọc tay vẫn thuộc phiên 2, không triển khai ở lượt sửa SPEC này.

### Kiểm kỹ thuật trong lượt và giới hạn

- Các lệnh chỉ đọc: Get-Content/rg; Python -B qua stdin để in dòng nguồn/schema JSON/metadata CSV và diff trong RAM. Không chạy thực nghiệm, kiểm giả hay đặc trưng P4; không mở test hoặc data/locked/.
- Một lệnh in nguồn bằng Python lỗi encoding cp1252; đổi stdout sang UTF-8 rồi đọc được. Ba lần tra schema dùng khóa giả định sai bị KeyError; dừng cách tra theo giả định và đọc cây khóa JSON trước, sau đó đọc đúng khóa thật (microrank_full/circa_ols_da, methods riêng với cohorts). Không dùng các lệnh lỗi làm bằng chứng khoa học; chúng không ghi file hoặc gọi phương pháp. Không lặp thêm cách tra sai.
- Đã đọc toàn SPEC sửa và diff đầy đủ so bản trước lời duyệt; kiểm phạm vi/hash/prefix LOG cuối lượt ghi ở mục dưới. SPEC và LOG là hai file được phép thay đổi; nguồn điều khiển, code và kết quả được giữ nguyên.

### Kết thúc lượt — dừng theo lời Minh

1. **Đã làm:** sửa SPEC đúng R1/R3/R4/R5/R6/N1/N2, R2 tối thiểu, R7 ngoại lệ hai phiên và hai bổ sung Minh duyệt; rà lại toàn SPEC vòng 2, không còn điểm chặn/mơ hồ ảnh hưởng kết quả được phát hiện. Minh nhắc “sửa xong thì dừng lại báo cáo tôi nhé”; dừng tại đây.
2. **File thay đổi:** tasks/T-028-p4-han-che-xep-hang/SPEC.md và LOG.md (chỉ ghi thêm). Không cập nhật STATE vì Minh chưa duyệt SPEC; không sửa WHY/DECISIONS hoặc file khác. Không commit/push.
3. **Kiểm và kết quả:** đối chiếu tài liệu, code đọc/chia cửa sổ và schema kết quả đã có; JSON chính parse được. Không triển khai phân tích. Kiểm cuối chỉ đọc: hash nguồn baseline, prefix LOG và bộ file T-028, diff/whitespace.
4. **OPEN/cần Minh quyết:** SPEC còn đề xuất, chờ lời “duyệt SPEC T-028”. Codebook/WHY chưa có và chưa duyệt; giới hạn clock/nền sạch/test/cơ chế nhân quả giữ OPEN, không tự chạy thêm để đóng chúng.

- **Bước tiếp chính xác:** dừng chờ Minh. Nếu Minh ghi “duyệt SPEC T-028”, mở phiên mới như checkpoint theo AGENTS mục 5a; đọc AGENTS.md, docs/STATE.md, SPEC.md và cuối LOG.md, ghi lời duyệt, cập nhật dòng T-028 STATE trong quyền được duyệt, rồi làm bước 1–2; trình codebook cùng văn bản WHY/phạm vi, dừng trước bước 3. Chưa có lệnh thực nghiệm được phép chạy ở lượt này. Lệnh đọc tiếp: Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/SPEC.md' -Encoding UTF8; Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/LOG.md' -Encoding UTF8 -Tail 80.
- **Lệnh cuối trước báo cáo:** kiểm hash/prefix chỉ đọc bằng Python -B qua stdin, git diff --no-index --check cho SPEC/LOG và git status --short; kết quả bổ sung ở dưới. Chưa viết prompt phản biện kết quả cho Claude vì task chưa triển khai/xong; khi xong chép nguyên mẫu docs/review-prompt.md.

### Kết quả kiểm cuối vòng 2

- Hash baseline: 38/38 file nguồn nguyên, gồm AGENTS/STATE/MRP/PLAN/DECISIONS/WHY/LESSONS/review-prompt, DT18/advisor, giao thức, nhãn/chấm/manifest chính, LOG đóng T-026 và toàn bộ file .py của src/p3. LOG T-028 giữ nguyên prefix byte trước lượt sửa. Thư mục task vẫn chỉ SPEC.md và LOG.md.
- Đã đọc đủ diff SPEC cũ → mới và toàn mục LOG vòng 2; phạm vi khớp lời duyệt. SPEC vẫn đề xuất. Không có output phân tích P4 mới; không commit/push.
- git diff --no-index --check cho hai file không có lỗi whitespace, chỉ cảnh báo LF/CRLF; mã 1 do so file mới với /dev/null, không diễn giải là exit 0. Dừng sau kiểm cuối git status --short, chờ Minh duyệt SPEC ở phiên tiếp theo.

## Rà SPEC — vòng 3

- Ghi mục rà lúc 2026-10-07T22:56:46+07:00; phiên ngày 07/10/2026; Codex, người làm T-028; Claude là người phản biện kết quả. Thiết bị: laptop Windows 11; repo D:/RCA-flashticket. Intent của lượt: REVIEW ở BƯỚC A; chỉ đọc và ghi thêm LOG theo yêu cầu Minh, chưa triển khai BƯỚC B.
- FACT khi tiếp nhận: SPEC vẫn đề xuất, chưa duyệt; LOG đã có vòng 1 và vòng 2 cùng phạm vi sửa Minh duyệt. Vòng này rà độc lập toàn bộ SPEC hiện tại, không mặc định kết luận vòng 2 đúng. STATE có dòng T-026 đã Xong; đoạn kế hoạch cũ ở mục Task đang mở chưa cập nhật không được dùng để mở lại T-026. T-028 chưa có dòng trong STATE; không thêm khi SPEC chưa được Minh duyệt, đúng yêu cầu lượt này.
- Không có quyết định khoa học mới của Minh trong lượt. Lời giao BƯỚC A không được coi là lời “duyệt SPEC T-028”.

### Phạm vi đối chiếu

- Đọc AGENTS.md, STATE, toàn SPEC và cuối LOG; đối chiếu trực tiếp docs/MRP.md (§3 RQ2/P4), docs/PLAN-P3-G2.md, docs/DECISIONS.md, docs/WHY.md, docs/LESSONS.md, docs/review-prompt.md, DT18 và advisor-2026-09-23.
- Đối chiếu giao thức V2 T-022; chấm/manifest T-024, T-026; nhãn và allowlist-dev.json T-022/T-026; ba CSV vị trí/chia ô T-021 mà SPEC liệt kê. Đọc hồ sơ chính P1 T-013–T-017, K1 và code src/p3 về selector, cửa sổ, tiền xử lý, adapter, bản ghi và chấm.
- Hai trợ lý chỉ đọc hỗ trợ đối chiếu tài liệu và dữ liệu/code; Codex tự xét kết luận và phản bác. Đây là hỗ trợ BƯỚC A, không thay Claude phản biện kết quả của task.

### Kết luận vòng 3 và danh sách đề xuất

**Không phát hiện điểm CHẶN, điểm mơ hồ ảnh hưởng kết quả hoặc lỗi KHÔNG CHẶN cần sửa mới trong SPEC hiện tại. Danh sách đề xuất sửa: không có.** Dừng BƯỚC A, trình Minh duyệt SPEC. Kết luận này ở cấp thiết kế SPEC; chưa xác nhận codebook, cơ chế theo ca hay kết quả P4 chưa được thực hiện.

### Bằng chứng và các khả năng phản bác đã xét

1. **Đúng phạm vi RQ2 và nguồn đề tài.** SPEC:10–18,63,85 giữ phân tích xếp hạng dev và cầu nối sang P5/P6; phần phát hiện/chế độ (b) để T-029. Khớp MRP:71,169–181, DT18:16–18 và advisor:26. MRP:31 nói “cơ chế nào gây ra”, nhưng dữ liệu quan sát không tự chứng minh nhân quả. SPEC:41,69,73,93 đã phân biệt rào cản trực tiếp của pipeline với cơ chế ứng viên/chưa kiểm nhân quả; không cần thêm can thiệp ngoài phạm vi để ép kết luận.
2. **Ca sai, hòa, seed và non-OK.** SPEC:28–30,54,67,69 dùng Hit kỳ vọng, tách số ca OK có Hit<1 khỏi tổng mức trượt; non-OK báo riêng, không suy UNSUPPORTED là root không có tín hiệu. src/p3/danh_gia.py:96–107,124–147 khớp cách đọc số. WHY:267–269/giao thức:300–301 giữ hòa khối TORAI và gộp seed theo ca; khoảng hạng không được dùng thay phân phối để tự chấm lại. Schema thật T-024 có methods.*.per_case, summaries và seed_metrics TORAI; T-026 có tables.main/sensitivity_A/sensitivity_B/trace_guard. Không có yêu cầu phải tạo dữ liệu thiếu để phủ bảng.
3. **Cohort và tính khả thi đầu vào.** SPEC:28–32,60,78 giữ bảng chính RE2 dev30/Nezha main; CIRCA dev19 chỉ dòng có điều kiện Q-82; A/B/trace_guard chỉ đánh dấu số đã có, không tính đặc trưng mới. Kiểm trực tiếp bằng đọc JSON/path/hash từ manifest: 420 records ở results/T-024/ban-ghi-dua-vao-cham.json và 248 unique_records ở results/T-026/ban-ghi-dua-vao-cham.json đều tồn tại, parse được, khớp hash và mã mờ. Allowlist thật là results/T-022/allowlist-dev.json và results/T-026/allowlist-dev.json; số mã dev duy nhất tương ứng 30 và 22. Header nguồn Nezha khớp bộ đọc; trace thiếu statusCode đúng lý do UNSUPPORTED tại src/p3/adapters/nezha.py:24–30. Đây là kiểm tính khả thi, không chạy lại phương pháp hay tính đặc trưng P4.
4. **Cửa sổ và tín hiệu đúng theo phương pháp.** SPEC:55–56 không áp chung start<t cho tất cả: SimpleRCA dùng start, MicroRank/TraceRCA dùng end; CIRCA có N đồ thị và train/test riêng. Khớp giao thức:130–137, src/p3/cua_so.py:21–39 và adapters/circa.py:34–43. Nezha giữ outer window, marker/arrays từng nguồn và wrapper chia riêng (src/p3/nezha.py:245–307,319–320; adapters/nezha.py:39–62,65–95). “Không chạy lại phương pháp” vẫn áp dụng: khi triển khai chỉ dùng selector/cắt cửa sổ/helper phù hợp; runner/worker hoặc adapters.*.chay là đường chạy phương pháp, không phải bộ đọc dùng cho P4.
5. **Tách nhãn, schema, phép đo và khóa tiêu chí.** SPEC:55–61,69–71 đặt codebook/ngưỡng/phép đo trước bằng chứng mới, nhãn nối sau đặc trưng không cần nhãn được ghi; đặc trưng cần root là phân tích. Đã thấy kết quả dev là nguy cơ neo còn lại được khai ở SPEC:96, không phải quyền chọn lại tiêu chí theo độ phân biệt. SPEC:57 điều kiện hóa đối chứng theo O/độ dài, không gọi đầu ra tập trung là chứng minh bỏ qua dữ liệu. SPEC:58,63 giữ nghĩa vụ schema của Q-74/WHY-27/giao thức:337–339; raw_column_audit thật có union_columns, union_n, by_case. Thuộc tính membership/status/hòa không bị ép tạo ngưỡng độ nhạy. Chi tiết còn giao codebook đúng bước 2, không là khoảng trống phải tự điền ở vòng rà.
6. **Vị trí root và thông tin cấu trúc.** Đã xét nghi ngờ nhóm vị trí T-021 không phải graph N theo ca: giao thức:326 quy định dùng nhom_vi_tri_p75 T-021; SPEC:33 dẫn đúng nguồn. Graph N tại SPEC:55–56 phục vụ đặc trưng quan hệ, không thay nhóm vị trí báo cáo. CSV vi-tri-root.csv:10–15 và goi-g1.md:174 đã khai Nezha dùng phút chồng ±60 s quanh tiêm, hub OPEN; phải giữ giới hạn này khi viết báo cáo, không suy là vị trí nhân quả hoặc nền sạch. Không có căn cứ yêu cầu tính lại vị trí hay sửa SPEC vì nghi ngờ này.
7. **Phụ thuộc, phạm vi phiên và kiểm vừa đủ.** T-026 LOG:1228–1240 ghi phiên 8, Minh “đóng task”; điều kiện SPEC:23 đã đạt nhưng các OPEN không tự đóng. SPEC:89 ghi ngoại lệ hai phiên riêng T-028 đã được Minh duyệt trong LOG vòng 2. Điểm dừng codebook + WHY tại SPEC:49,59,77 giữ quyền duyệt nội dung/phạm vi riêng; sửa triển khai trái codebook tại SPEC:62 không cho đổi tiêu chí theo kết quả. Không phát hiện nhu cầu thêm quy trình, cổng, lượt chạy hay tách task mới; chi phí vẫn là ước lượng chưa kiểm.

- Lệnh chuẩn bị ghi LOG lần đầu gặp thiếu tzdata khi lấy múi giờ, dừng trước thao tác ghi. Dùng offset UTC+07 theo múi giờ Minh cung cấp để ghi giờ; không cài gói hoặc đổi môi trường. Không có lượt phân tích/phương pháp bị chạy bởi lỗi này.

### Kết thúc phiên — dừng chờ Minh duyệt SPEC

1. **Đã làm:** rà độc lập toàn bộ SPEC hiện tại như vòng 3; đối chiếu nguồn, schema/kết quả đã lưu và bộ đọc/code; không phát hiện lỗi cần đề xuất sửa mới. Không thêm hoặc đổi quyết định khoa học.
2. **File thay đổi:** chỉ ghi thêm tasks/T-028-p4-han-che-xep-hang/LOG.md. Không sửa SPEC, STATE, WHY, DECISIONS, code, kết quả task khác hoặc dữ liệu; không commit/push.
3. **Kiểm và kết quả:** kiểm chỉ đọc JSON/manifest/path/hash/header và đối chiếu tài liệu/code nêu trên; nguồn đầu vào khả dụng. Không chạy test, phương pháp, kiểm giả hoặc tính đặc trưng P4; không mở test/data/locked. Kiểm cuối lượt: so hash nguồn và prefix LOG với baseline trong RAM, đọc toàn phần thêm, kiểm diff/whitespace và bộ file; kết quả ghi thêm phía dưới.
4. **OPEN/cần Minh quyết:** chờ đúng lời “duyệt SPEC T-028”. Codebook/WHY và bằng chứng cơ chế P4 chưa có, chưa duyệt; giới hạn clock/nền sạch/license/tính đại diện cho test vẫn OPEN theo nguồn. Khi viết tài liệu chính thức phải giữ giới hạn cửa sổ/cadence, vị trí T-021, non-OK và mức kết luận quan sát.

- **Bước tiếp chính xác:** dừng. Khi Minh ghi “duyệt SPEC T-028”, đọc AGENTS.md, docs/STATE.md, SPEC.md và cuối LOG; ghi lời duyệt, đăng ký dòng T-028 trong STATE trong phạm vi được phép, làm bước 1–2, trình codebook cùng văn bản WHY/phạm vi và dừng trước bước 3. Chưa có lệnh thực nghiệm nào được phép chạy ở lượt này. Lệnh đọc tiếp: Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/SPEC.md' -Encoding UTF8; Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/LOG.md' -Encoding UTF8 -Tail 90.
- **Lệnh cuối để bàn giao:** kiểm chỉ đọc hash/prefix bằng Python -B qua stdin, kiểm phần LOG mới và git diff --check, rồi git status --short; kết quả cuối được ghi tiếp dưới đây. Chưa viết prompt phản biện kết quả cho Claude vì task chưa thực hiện/xong; khi xong dùng nguyên mẫu docs/review-prompt.md.

### Kết quả kiểm cuối vòng 3

- Đã đọc toàn phần LOG thêm trong vòng này; không có đề xuất sửa hay kết luận khoa học mới bị nâng thành quyết định. Bộ file task vẫn chỉ SPEC.md và LOG.md.
- Đối chiếu baseline trong RAM: 52/52 file nguồn nguyên, gồm SPEC, STATE, tài liệu điều khiển, hồ sơ chính P1/K1, giao thức, đầu vào JSON/CSV/allowlist và code src/p3. Prefix byte của LOG trước lượt nguyên; chỉ phần ghi thêm của vòng 3 thay đổi. Danh sách git status giống đầu lượt, các thay đổi có sẵn ngoài task được giữ nguyên.
- Kiểm phần thêm không có trailing whitespace. git diff --check không báo lỗi whitespace; git diff --no-index --check cho LOG chỉ cảnh báo LF/CRLF, mã 1 do so file mới với /dev/null, không diễn giải là test thất bại hoặc exit 0. Không chạy test/thực nghiệm/phương pháp.
- Lệnh chỉ đọc cuối trước trả lời: kiểm prefix/phạm vi và dòng kết luận LOG bằng Python -B qua stdin, rồi git status --short. Dừng chờ Minh ghi “duyệt SPEC T-028”; SPEC và STATE chưa được sửa trong lượt này.

## Phiên triển khai 1 — bước 1–2, chờ duyệt codebook

- Mở phiên: 2026-10-07T23:07:34+07:00; Codex; laptop Windows 11 tại D:/RCA-flashticket; người làm T-028, Claude phản biện. Intent: EXECUTE trong SPEC vừa được duyệt.
- Quyết định của Minh (nguyên văn): “duyệt SPEC T-028 và triển khai”. Minh duyệt SPEC ngày 07/10/2026, bản hiện tại sau vòng rà 3. SPEC đã khóa; giữ nguyên file, lời duyệt có hiệu lực được ghi tại đây và dòng T-028 STATE.
- Điều kiện Nezha: T-026 đã được Minh đóng, LOG phiên 8. Các OPEN của T-026 vẫn nguyên. Không mở test/data/locked, không chạy lại phương pháp, không commit.
- Phạm vi phiên 1 theo SPEC: bước 1 chỉ trích danh sách/độ đo đã chấm; bước 2 soạn codebook + nháp WHY rồi trình Minh, chưa bước 3. Ghi kết quả bước 1 trong runs/<run-id>/ và bảng đọc được, script tại results/T-028/scripts/, codebook.md và chi-phi.md; LOG chỉ ghi thêm, STATE chỉ dòng T-028. WHY chung chưa có quyền ghi.
- Tiến độ từ đầu: đang chuẩn bị bước 1 (schema/nguồn và script). Dự kiến lượt trích số dưới một phút; không telemetry mới, không EC2/tải dữ liệu. Thời gian máy từng pha sẽ ghi ngay vào progress.jsonl; thời gian phiên và bước 2 ghi tiếp LOG/chi-phi. Hai trợ lý hỗ trợ phần script và thiết kế tiêu chí độc lập; không thay Claude phản biện chính thức.

### Checkpoint 2026-10-07T23:14:31+07:00

- Ngữ cảnh đã được nén; ghi checkpoint theo AGENTS mục 5a. Đã ghi lời Minh duyệt SPEC và thêm đúng dòng T-028 STATE. Script results/T-028/scripts/lap_danh_sach.py đã soạn, chưa chạy; codebook chưa ghi, chưa tính đặc trưng/mức tập trung hay gán cơ chế. Không sửa SPEC/WHY hoặc đầu vào.
- Tiếp theo: kiểm cú pháp script, chạy `py -3 -B results/T-028/scripts/lap_danh_sach.py --run-dir results/T-028/runs/danh-sach-001`; giữ mọi lượt; hoàn tất đầu ra bước 1 và bản codebook/WHY để trình tại điểm dừng bước 2. Đề nghị Minh mở phiên mới sau điểm dừng này để làm bước 3–6, đúng ngoại lệ hai phiên đã duyệt.

### Bước 1 hoàn tất — 2026-10-07T23:23:26+07:00

- Lượt `danh-sach-001`: bắt đầu 2026-10-07T23:14:32.986+07:00, kết thúc 23:14:34.131+07:00; thời gian chương trình 1.145980 s theo runs/danh-sach-001/manifest.json, từng pha ở progress.jsonl. Không có lượt thất bại. Chỉ đọc số chấm/bản ghi đã lưu.
- `step1.json` phủ 312 dòng chính, 12 tổng, CIRCA dev19 19 dòng và 11 ca loại; 396 dấu độ nhạy Nezha gồm 6 not_in_cohort ở B. Nguồn số: results/T-028/runs/danh-sach-001/step1.json; kiểm path/hash/status/seed/đẳng thức mức trượt trong validation.json. Tất cả evidence/mechanisms còn null.
- Đối chiếu độc lập với T-024/T-026 khớp từng main row và cả 12 tổng; không dùng hàm của script trích để đối chiếu. TORAI mẫu số theo ca, giữ ba seed. Non-OK tách ERROR/UNSUPPORTED; B không coi ca thiếu là lỗi. Bảng đọc được: results/T-028/danh-sach-ca-sai.md, tạo từ JSON bằng scripts/tao_bang_buoc1.py.
- Bước 2 đang soạn/tự kiểm codebook; chưa tính đặc trưng, D/D0, nhóm cơ chế hoặc đối chứng đúng/sai. Đã kiểm luật native: SimpleRCA strict > / ddof0 / events; trace MicroRank/TraceRCA ≥ / ddof1 / round2 ms, giữ hàng lặp; M3 xét từng seed; M0 chỉ gán sau gộp M1–M6. Các sửa trong bản nháp trước chốt, không điều chỉnh theo phân bố đặc trưng.

### Bước 2 — chốt codebook 2026-10-07T23:24:42+07:00

- **chốt codebook**: results/T-028/codebook.md, bản trình Minh duyệt; hash/bản nháp WHY và thời gian trong results/T-028/runs/chot-codebook-001/manifest.json. Tiêu chí cơ chế, primary/đa nhãn/seed, N/A, cửa sổ native, phép D/D0 và đối chứng theo O/chiều dài, audit schema, mẫu đọc tay/kiểm độc lập đã khai trước bằng chứng mới. Không có feature/D/cơ chế được tính.
- Nháp WHY-38 nằm nguyên văn tại codebook §9; xin quyền chỉ thêm đúng mục này cuối docs/WHY.md, không sửa mục cũ hoặc tài liệu chung khác. Chưa có lời duyệt codebook/WHY; chưa ghi WHY. SPEC đã duyệt không tự cấp quyền ghi WHY.
- Nguồn số đã trích và danh sách ca được giữ trong danh-sach-001; không sửa/rerun phương pháp, không mở test/data/locked, không commit. Thời gian/chi phí tại results/T-028/chi-phi.md. Dừng trước bước 3 theo SPEC:59,77.

### Kết thúc phiên triển khai 1 — 2026-10-07T23:27:12+07:00

1. **Đã làm:** ghi lời Minh duyệt SPEC; hoàn tất bước 1 trích danh sách ca sai và bước 2 chốt bản codebook trình duyệt. T-026 đã đóng. Chưa triển khai bước 3–6; chưa có kết luận cơ chế P4. Codebook/WHY là CANDIDATE chờ Minh, không tự nâng thành DECIDED.
2. **File thay đổi:** chỉ thêm đầu ra dưới results/T-028/ (danh sách chính xác dưới đây), ghi thêm LOG này và thêm/cập nhật đúng dòng T-028 STATE. Không sửa SPEC, WHY/DECISIONS, src, data hoặc đầu vào task khác. Các thay đổi có sẵn ngoài task được giữ nguyên. Không commit/push.
3. **Kiểm và kết quả:** danh-sach-001 đạt, 14.369 đối chiếu trong validation.json; độc lập từng dòng/tổng khớp T-024/T-026. JSON/JSONL parse, hai script AST, hash đầu vào/đầu ra và bản codebook chốt khớp. 41/41 nguồn baseline nguyên; LOG giữ prefix byte; STATE bỏ dòng T-028 trở về đúng baseline. Kiểm whitespace không có lỗi; git chỉ cảnh báo LF/CRLF có sẵn. Nguồn kiểm cuối: results/T-028/runs/chot-codebook-001/verification.json. Lần đầu lệnh kiểm cuối hiểu sai schema outputs của manifest (KeyError path), dừng trước ghi; sửa resolve basename và kiểm lại đạt, không chạy lại trích số/phương pháp. Lỗi kiểm này giữ trong verification.json. Không đọc raw/test/locked trong phiên; không ghi bytecode.
4. **OPEN/cần Minh quyết:** duyệt results/T-028/codebook.md và đúng văn bản/phạm vi WHY-38 trong §9: chỉ thêm một mục đó cuối docs/WHY.md. Dừng vì SPEC bước 2/tiêu chí xong yêu cầu duyệt riêng trước bước 3. Các OPEN clock/nền sạch/license/tính đại diện/test/nhân quả giữ theo nguồn. Chi phí bước 3–6 vẫn chưa kiểm.

Bộ đầu ra mới dưới results/T-028/:

- `results/T-028/chi-phi.md`
- `results/T-028/codebook.md`
- `results/T-028/danh-sach-ca-sai.md`
- `results/T-028/runs/chot-codebook-001/manifest.json`
- `results/T-028/runs/chot-codebook-001/verification.json`
- `results/T-028/runs/danh-sach-001/manifest.json`
- `results/T-028/runs/danh-sach-001/progress.jsonl`
- `results/T-028/runs/danh-sach-001/step1.json`
- `results/T-028/runs/danh-sach-001/validation.json`
- `results/T-028/scripts/lap_danh_sach.py`
- `results/T-028/scripts/tao_bang_buoc1.py`

- **Bước tiếp chính xác:** chờ Minh duyệt codebook và đúng văn bản/phạm vi WHY. Theo checkpoint AGENTS mục 5a, đề nghị mở phiên mới cho bước 3–6 sau duyệt. Phiên mới đọc AGENTS.md, docs/STATE.md, SPEC.md, cuối LOG, codebook.md và manifest chốt; kiểm SHA trước dùng. Khi có đúng lời duyệt, ghi lời duyệt LOG rồi chỉ append đoạn giữa BEGIN/END WHY-38 trong codebook §9 vào docs/WHY.md; kiểm phần cũ giữ nguyên. Chỉ sau đó viết/chạy script tính thống kê step3 theo codebook, dùng guard allowlist dev, ghi đặc trưng không nhãn trước nối nhãn. Chưa có script/lệnh step3 nên không chạy lại script trích đã có output hợp lệ. Lệnh đọc khởi đầu: `Get-Content -LiteralPath 'AGENTS.md' -Encoding UTF8`, `Get-Content -LiteralPath 'results/T-028/codebook.md' -Encoding UTF8`, `Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/LOG.md' -Encoding UTF8 -Tail 90`.
- **Lệnh cuối trước bàn giao:** Python `py -3 -B -` chỉ đọc kiểm prefix/baseline/STATE, manifest/hash, JSON/JSONL/AST và danh sách file; tiếp theo `git diff --check`. Kết quả cuối được đối chiếu sau ghi mục này. Không viết prompt phản biện cho Claude ở phiên 1 vì task chưa xong; cuối bước 6 sẽ chép nguyên Prompt chung + khối trọng tâm G2 từ docs/review-prompt.md.

## Phiên chốt sửa codebook đã duyệt — 08/10/2026

- Mở phiên: Codex, thiết bị LEVANMINH (Windows 11), vai trò người làm T-028; Claude là người phản biện. Chỉ hoàn tất sửa tài liệu ở điểm dừng bước 2 và bàn giao phiên bước 3–6; không tính đặc trưng theo ca, không chạy phương pháp, không mở test/data/locked, không commit.
- **Quyết định của Minh trong phiên — ghi trước mọi sửa đổi codebook/WHY:**

> Duyệt S1, S1b, S2, S3 (gồm S3.4), S4 đúng như bản hợp nhất. Thêm "; P0" vào danh sách loại đặc trưng kiểm độc lập ở §8. (a) Có thêm P0. (b) Có thêm bảng số liệu root cho BARO. (c) [Minh chọn nơi xử lý câu "lan có đáng kể"]. Duyệt ghi nguyên văn WHY-38 mới vào cuối docs/WHY.md, không sửa mục cũ. Ghi lời duyệt vào LOG trước khi sửa.
>
> sau cùng soạn prompt cho phiên tiếp theo

- USER_CONFIRMED: áp dụng đúng S1/S1b/S2/S3 gồm S3.4/S4 của bản hợp nhất; thêm P0 vào §8; nối nguyên văn WHY-38 mới vào cuối WHY. P0 và bảng dữ liệu root BARO được duyệt. Phạm vi còn lại theo SPEC đã duyệt; chỉ cập nhật dòng T-028 STATE.
- OPEN: mục (c) là nguyên văn chỗ trống, chưa nêu nơi Minh chọn. Giữ câu đề xuất trong codebook/WHY, không ghi thành quyết định giao T-029. Việc này không thay phạm vi T-028 đã duyệt.
- Bắt đầu bước sửa tài liệu: lưu bản codebook trước duyệt và giữ nguyên manifest/lượt cũ; sửa đúng các đoạn đã duyệt, kiểm WHY chỉ nối thêm, rồi soạn prompt thực hiện bước 3–6 trong phiên mới. Chưa có phép tính P4 mới; ảnh hưởng lên nhãn chưa tính.
- Ghi nhận kiểm đọc đầu phiên: lần xuất baseline có chữ Việt bị lỗi encoding cp1252; lần xuất toàn văn kế tiếp bị cắt vì dung lượng output. Đổi sang chỉ xuất metadata/hash, kiểm thành công; hai lỗi đọc không làm đổi file hoặc chạy thực nghiệm.
- Giờ máy ghi lời duyệt và bắt đầu sửa: 2026-10-08T07:57:47.1177031+07:00.

### Sửa tài liệu theo lời duyệt — 08/10/2026

- Đã áp dụng S1/S1b/S2/S3 gồm S3.4/S4 và thêm P0 vào danh sách §8; nối nguyên văn WHY-38 mới vào cuối WHY, không sửa mục cũ. Dòng T-028 STATE đã phản ánh lời duyệt. Bản codebook trước sửa được giữ nguyên byte tại runs/chot-codebook-002/codebook-truoc-duyet.md; bản đã duyệt tại runs/chot-codebook-002/codebook.md. Manifest chốt 001 và bước 1 giữ nguyên.
- Lần ghi manifest chốt 002 gặp lỗi ZoneInfoNotFoundError vì máy thiếu tzdata, sau khi đã ghi tài liệu và trước khi ghi manifest. Dùng giờ hệ thống có múi giờ +07, chỉ tiếp tục phần manifest; đã kiểm WHY không nối trùng, prefix cũ và snapshot codebook khớp. Không cài dependency, không chạy đặc trưng hoặc phương pháp. Lượt lỗi được ghi trong manifest.
- Câu mở đầu và §9/§10 codebook giữ nguyên lời trình/điểm dừng của bản cũ vì không nằm trong đề xuất sửa được duyệt. Lời duyệt mới và việc đã ghi WHY được xác nhận ở LOG này và manifest chốt 002; điều kiện bước 2 đã hoàn tất. Không coi lời chờ duyệt lịch sử là yêu cầu duyệt lại.
- Ảnh hưởng nhãn chưa tính: BARO local_nonpositive/M6 thành N/A, có thể đổi nhãn đa nhãn/primary/M0 tùy các cờ khác; CIRCA xét diagnostics.nodes sau prune và biên strict RHT<3, có thể đổi True/False/N/A. P0 và bảng root BARO là số mô tả, không đổi tiêu chí M5 hay tự tạo nhãn. TraceRCA giữ thứ tự primary M2 trước M6. Không có con số ảnh hưởng được suy đoán.
- Giờ máy hoàn tất sửa, bắt đầu kiểm: 2026-10-08T08:00:48.8075667+07:00.


### Kết thúc phiên chốt tài liệu — 08/10/2026

1. **Đã làm:** ghi nguyên lời Minh duyệt trước khi sửa; áp dụng đúng bản hợp nhất S1/S1b/S2/S3 gồm S3.4/S4, thêm P0 ở §8, nối nguyên văn WHY-38 và chốt bản dùng cho phiên tiếp. Điều kiện duyệt codebook/WHY ở bước 2 đã hoàn tất. Chưa thực hiện bước 3–6.
2. **File thay đổi:** results/T-028/codebook.md; chỉ nối cuối docs/WHY.md; chỉ nối LOG này; chỉ dòng T-028 docs/STATE.md. Thêm bốn file tại results/T-028/runs/chot-codebook-002/: codebook-truoc-duyet.md, codebook.md, manifest.json, verification.json. Không sửa SPEC, DECISIONS, src, data, đầu vào task khác hoặc các lượt cũ. Không commit/push.
3. **Kiểm và kết quả:** tái dựng codebook từ bản cũ bằng đúng các đoạn sửa đã duyệt, khớp toàn văn; WHY-38 khớp nguyên văn codebook, prefix WHY/LOG giữ nguyên byte; STATE chỉ đổi dòng T-028. Các file baseline khác và input/output bước 1 giữ hash; snapshot trước sửa khớp chốt 001, snapshot đã duyệt khớp codebook hiện tại. Không bytecode; git diff --check đạt, chỉ cảnh báo LF/CRLF có sẵn. Nguồn kiểm: results/T-028/runs/chot-codebook-002/verification.json. Các lỗi đọc/manifest và cách khôi phục đã giữ trong LOG/manifest/verification, không có lượt chạy phương pháp hoặc tính đặc trưng.
4. **OPEN/cần Minh quyết:** nơi xử lý câu hỏi “lan có đáng kể” chưa được chọn vì lời duyệt (c) còn là chỗ trống. Không giao trước cho T-029, không biến OPEN thành một cổng mới cho bước 3–6. Ảnh hưởng số nhãn của BARO/CIRCA, P0, bảng root BARO và toàn bộ bằng chứng P4 chưa tính. Các giới hạn clock/nền/coverage/đại diện/nhân quả giữ theo nguồn. Chưa ghi DECISIONS vì SPEC không cho phép và lời duyệt lần này chỉ cấp quyền ghi WHY/LOG; quyết định codebook đã được ghi ở hai nguồn được duyệt này.

- **Thời gian:** ghi lời duyệt/bắt đầu sửa lúc 2026-10-08T07:57:47.1177031+07:00; chốt tài liệu và manifest lúc 2026-10-08T08:00:47.873966+07:00 (nguồn: runs/chot-codebook-002/manifest.json); kiểm tài liệu đạt lúc 2026-10-08T08:02:13.632746+07:00 (nguồn: runs/chot-codebook-002/verification.json). Không có lượt dài hơn một giờ, không cloud/tải dữ liệu. Chỉ ghi thời gian lịch, không suy CPU/RAM/token.
- **Bước tiếp chính xác:** mở phiên mới Codex làm bước 3–6 theo prompt dưới đây. Đọc nguồn và kiểm snapshot/đầu ra hợp lệ; viết script mới dưới results/T-028/scripts/ để tính đúng codebook, chưa có script step3 nên chưa có lệnh chạy step3. Không chạy lại lap_danh_sach.py vì đầu ra bước 1 hợp lệ.
- **Lệnh đọc mở phiên:** `Get-Content -LiteralPath 'AGENTS.md' -Encoding UTF8`; `Get-Content -LiteralPath 'docs/STATE.md' -Encoding UTF8`; `Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/SPEC.md' -Encoding UTF8`; `Get-Content -LiteralPath 'tasks/T-028-p4-han-che-xep-hang/LOG.md' -Encoding UTF8 -Tail 110`; `Get-Content -LiteralPath 'results/T-028/codebook.md' -Encoding UTF8`; `Get-Content -LiteralPath 'results/T-028/runs/chot-codebook-002/manifest.json' -Encoding UTF8`.
- **Lệnh cuối trước bàn giao:** `py -3 -B -` với đoạn Python chỉ đọc kiểm prefix/hash, phạm vi file và lời bàn giao; sau đó `git diff --check`. Không chạy test hay phương pháp. Kiểm cuối sau khi ghi mục này chỉ đọc.
- **Checkpoint theo AGENTS 5a:** ngữ cảnh đã nén; bản đã duyệt, trạng thái và bước tiếp đã ghi đủ trong repo. Dừng ở đây và dùng phiên mới cho bước 3–6 đúng ngoại lệ hai phiên T-028; đây không phải một vòng rà codebook mới. Đề xuất nội dung commit sau khi task được Minh duyệt đóng: `T-028: phân tích hạn chế xếp hạng chế độ a trên dev`; chưa commit.

### Prompt cho phiên tiếp theo — Codex thực hiện bước 3–6

```text
Bạn là Codex, người làm T-028 tại D:/RCA-flashticket; Claude là người phản biện. Đọc AGENTS.md, docs/STATE.md, tasks/T-028-p4-han-che-xep-hang/SPEC.md và mục cuối LOG.md trước khi làm.

SPEC đã được Minh duyệt 07/10/2026. Ngày 08/10, Minh đã duyệt bản hợp nhất S1, S1b, S2, S3 gồm S3.4, S4; có thêm P0, bảng dữ liệu root cho BARO và P0 trong kiểm độc lập §8. WHY-38 mới đã được nối nguyên văn vào docs/WHY.md. Lời duyệt nằm trong LOG; bản chốt hiện hành và hash ở results/T-028/runs/chot-codebook-002/manifest.json, snapshot codebook.md cùng thư mục. Đọc results/T-028/codebook.md và WHY-38. Câu mở đầu/§9–§10 codebook và tiêu đề trạng thái SPEC còn lời đề xuất/điểm dừng lịch sử; lời duyệt trong LOG và manifest chốt 002 xác nhận điều kiện đã hoàn tất. Không xin duyệt lại hoặc nối trùng WHY-38. Không tự sửa các dòng lịch sử ấy.

Tiếp tục bước 3–6 của SPEC. Bước 1 đã có đầu ra hợp lệ tại runs/danh-sach-001/, danh-sach-ca-sai.md và chi-phi.md; kiểm nguồn/hash rồi dùng lại, không trích hoặc chạy phương pháp lại. T-026 đã được Minh đóng, xem LOG T-026 phiên 8. Chưa có đặc trưng, P0, D/D0 hoặc gán cơ chế T-028; chưa có script step3.

Chỉ ghi đúng Phạm vi ghi của SPEC: results/T-028/, LOG chỉ nối thêm và dòng T-028 STATE. Giữ mọi lượt, kể cả hỏng. Không sửa src, SPEC, tiêu chí codebook, WHY/DECISIONS hoặc task khác. Nếu cần đổi tiêu chí/phạm vi thì dừng trình Minh, giữ bản và kết quả cũ. Không mở test/data/locked; không chạy lại phương pháp hay thành phần phương pháp. Python dùng -B. Không commit/push.

Tính bằng chứng cho RE2-TT dev30 và Nezha-OB main qua bộ đọc có guard. Ghi thống kê mọi service/kênh không cần nhãn ra file trước, rồi mới nối nhãn phân tích. Giữ cửa sổ và mapping native, availability/N/A; payload Nezha chỉ ở RAM, chỉ lưu thống kê được phép. CIRCA dev19 dùng lại bằng chứng dev30; các view Nezha độ nhạy chỉ đánh dấu số status/Hit đã có.

Thực hiện đầy đủ codebook đã duyệt, đặc biệt: CIRCA xét diagnostics.nodes sau prune với RHT<3; BARO local_nonpositive/M6=N/A và có bảng dữ liệu root mô tả theo quy ước SimpleRCA; TraceRCA M6 kéo theo M2 nhưng không suy ngược. P0 so với số cờ cơ sở M5 True trên cùng tập đủ điều kiện, không dùng primary=M5; TORAI báo từng seed, không OR P0 hoặc coi seed là ca độc lập. P0 không là p-value hay nhãn lan. Giữ D/D0, đa nhãn/primary, kiểm độc lập gồm P0, đọc tay và nguyên nhân khả thi khác đúng codebook, không chọn lại tiêu chí theo kết quả.

Mục (c) về nơi xử lý câu “lan có đáng kể” còn OPEN vì Minh chưa điền nơi chọn; không tự giao T-029. Cuối T-028 báo bằng chứng kiểm được tới đâu và giải thích khác còn lại, không chốt trước có/không lan, không biến câu này thành cổng mới.

Ghi tiến độ và thời gian từng bước từ đầu; lượt dự kiến >1 giờ phải báo ước lượng và chờ Minh đồng ý trước. Mỗi số báo cáo dẫn đường dẫn nguồn. Khi xong, ghi báo cáo bốn mục theo AGENTS §7, bước tiếp/lệnh cuối và cập nhật dòng T-028 STATE. Soạn prompt phản biện cho Claude ở cuối LOG theo nguyên văn Prompt chung và trọng tâm áp dụng trong docs/review-prompt.md, chỉ điền thông tin trung tính. Đừng coi các khẳng định ở prompt này thay cho việc đọc nguồn.
```


## Tiếp nhận bước 3–6 — 08/10/2026, chờ đồng ý thời lượng

- Mở phiên: Codex, thiết bị LEVANMINH (Windows), người làm T-028; Claude phản biện. Bắt đầu đọc lúc 2026-10-08T08:57:30+07:00; kiểm nguồn hoàn tất lúc 2026-10-08T09:04:38+07:00. Thời gian lịch gồm trao đổi/ngắt lượt, không suy CPU/token. Nguồn: results/T-028/runs/tiep-nhan-001/manifest.json.
- Đã đọc AGENTS, STATE, SPEC và cuối LOG; toàn bộ codebook, WHY-38, review-prompt, LESSONS và bộ đọc/cắt cửa sổ. Làm ở repo chuẩn D:/RCA-flashticket. Một trợ lý Codex chỉ đọc hỗ trợ kiểm nguồn bước 1; không thay vai trò phản biện của Claude.
- FACT/USER_CONFIRMED từ nguồn: SPEC đã duyệt 07/10, bản hợp nhất và WHY-38 đã duyệt/ghi 08/10 theo LOG/chốt 002; T-026 đã đóng theo LOG phiên 8. Điều kiện bước 2 hoàn tất, không xin duyệt lại hoặc nối WHY. Đoạn tổng quan STATE còn câu T-026 kế tiếp lịch sử; dòng T-026/T-028 và LOG xác nhận trạng thái hiện hành. Không sửa đoạn tổng quan.
- Kiểm tái dùng bước 1: 498 tham chiếu script/input/bản ghi/output trong manifest danh-sach-001 khớp SHA-256 và byte nơi khai; JSON/JSONL parse. Codebook hiện hành/snapshot 002 khớp hash; WHY-38 khớp nguyên văn, không trùng và prefix cũ giữ nguyên; baseline bất biến chốt 002 khớp. Nguồn chi tiết: results/T-028/runs/tiep-nhan-001/manifest.json. Không trích lại danh sách hoặc chạy phương pháp.
- CANDIDATE, chưa kiểm: dự kiến lượt bước 3–6 khoảng 3–5 giờ agent, máy 10–45 phút, RAM 0,5–2 GB, đĩa 0,1–0,3 GB. Nguồn dự toán: SPEC mục Chi phí ước lượng và results/T-028/runs/tiep-nhan-001/manifest.json. Dùng dự toán thận trọng; chưa lấy lượt trích số ngắn làm xác nhận. Giả định bộ đọc/dữ liệu/mapping hợp lệ và không phải sửa triển khai nhiều lượt; nếu sai cần báo lại thời lượng. Không tải dữ liệu/EC2.
- OPEN: đã hỏi Minh đồng ý thời lượng vì AGENTS §3.8 và SPEC Chi phí yêu cầu chờ trước lượt >1 giờ. Chưa có câu đồng ý rõ cho ước lượng này; việc lặp prompt không được ghi thành đồng ý. Chưa viết/chạy step3, đặc trưng, P0, D/D0 hoặc gán cơ chế. Câu (c) nơi xử lý “lan có đáng kể” giữ OPEN, không là điểm chặn mới.
- Lỗi thao tác: đọc nhầm LOG ở gốc repo và output toàn văn bị cắt, đã đọc đúng theo từng đoạn; lần đầu lệnh ghi tiếp nhận bị SyntaxError trước thực thi, không tạo/sửa file. Giữ ghi nhận lỗi trong manifest; lần sau kiểm và ghi manifest đạt.

### Báo cáo bốn mục của lượt tiếp nhận

1. Đã làm: đọc nguồn, đối chiếu lời duyệt/hash; xác nhận đầu ra bước 1 tái dùng được. Chuẩn bị tiếp bước 3–6, chờ xác nhận thời lượng đã được quy định.
2. File thay đổi: thêm results/T-028/runs/tiep-nhan-001/manifest.json; chỉ nối LOG này và chỉ dòng T-028 STATE. Giữ mọi đầu ra/lượt cũ và thay đổi người dùng có sẵn. Không sửa codebook/SPEC/WHY/DECISIONS/src/data hoặc task khác; không commit/push.
3. Kiểm: hash nguồn/output/baseline đạt; WHY-38 nguyên văn/không trùng. Kiểm sau ghi: prefix LOG, STATE ngoài dòng T-028, baseline bất biến và whitespace. Kết quả kiểm cuối sẽ trả trong chat. Không đọc raw/test/locked hoặc chạy phương pháp.
4. Chưa chắc/cần Minh quyết: đồng ý lượt 3–5 giờ; các ước lượng tài nguyên chưa đo. Nơi xử lý câu hỏi lan giữ OPEN; chưa có kết quả cơ chế. Chưa soạn prompt phản biện kết quả vì bước 3–6 chưa xong; khi xong dùng nguyên Prompt chung, docs/review-prompt.md không có khối G2 riêng.

- Bước tiếp chính xác: sau Minh đồng ý, nối lời đồng ý vào LOG trước triển khai; đọc bộ đọc/adapter/giao thức/hồ sơ liên quan và viết script thống kê dưới results/T-028/scripts/, ghi mọi service/kênh không nhãn trước nối nhãn; giữ tiêu chí bản chốt 002. Chưa có script step3 nên chưa có lệnh chạy. Không chạy lap_danh_sach.py hoặc tao_bang_buoc1.py.
- Lệnh cuối trước bàn giao: `py -3 -B -` kiểm hash và ghi manifest tiếp nhận; tiếp theo `py -3 -B -` nối mục LOG này/cập nhật dòng STATE; kiểm cuối bằng `py -3 -B -` kiểm prefix LOG, STATE chỉ dòng T-028 và baseline, cùng `git diff --check`.

### Minh đồng ý thời lượng — 08/10/2026

- USER_CONFIRMED: Minh trả lời nguyên văn "ĐỒNG Ý" cho đề xuất lượt bước 3–6 dự kiến 3–5 giờ agent, máy 10–45 phút, RAM 0,5–2 GB, đĩa 0,1–0,3 GB (chưa kiểm, nguồn dự toán SPEC mục Chi phí). Lời này cho phép tiếp tục trong phạm vi SPEC đã duyệt; không đổi tiêu chí, không mở test hoặc chạy lại phương pháp.
- Ghi lời đồng ý trước triển khai. Bắt đầu bước 3: script mới dưới results/T-028/scripts/, ghi tiến độ/thời gian từ đầu; dùng lại danh-sach-001 và chốt 002. Hai trợ lý Codex hỗ trợ phần thống kê và phép tính trên bản ghi; Codex chịu trách nhiệm triển khai/kiểm/báo cáo, Claude vẫn là người phản biện.

### Bước 3 — triển khai và bắt đầu tính thống kê

- Lời đồng ý thời lượng đã được ghi trước triển khai. Dùng Python có sẵn D:/RCA-ext/envs/T-014-main/Scripts/python.exe với -B theo giao thức; Python mặc định thiếu numpy, không cài hoặc thay môi trường. Script helper chỉ thống kê/evaluator, không import runner, worker hoặc bộ xếp hạng.
- Smoke mọi lượt được giữ tại results/T-028/runs/smoke-thong-ke-001/manifest.json. Một lookup record smoke dùng sai key manifest Nezha đã được ghi và sửa; không phải lượt phương pháp. Thời gian/số của smoke chỉ lấy từ manifest đó. Các source snapshot của smoke đầu chưa lưu lúc chạy; giới hạn truy vết này được khai trong manifest, nguồn hiện hành có hash.
- Lượt buoc3-001 bắt đầu 09:16:43+07 ngày 08/10; dừng trước barrier nhãn do index thiếu mapping native torai/B của Nezha sang torai_B. Đã giữ toàn bộ file/lượt và script snapshot; lỗi/ngày/tiến độ ở runs/buoc3-001/manifest.json và progress.jsonl. Không đổi tiêu chí hoặc chạy lại phương pháp. Đây là lỗi triển khai được sửa theo SPEC bước 5.
- Lượt buoc3-002 bắt đầu 09:17:32+07; index đã kiểm đủ 372 bản ghi, sáu phương pháp và mọi ca dev bảng chính trước raw đọc. Nguồn: results/T-028/runs/buoc3-002/progress.jsonl; snapshot script/source hash và trạng thái ở manifest.json. Đang ghi từng file aggregate không nhãn; sau khi toàn bộ feature index được ghi mới mở step1/nhãn để phân tích.
- Mapping/cửa sổ giữ native. Phép tính operation có hai bản arithmetic theo native MicroRank (sort/groupby/round) và TraceRCA (Series/built-in round), không tính ji/PageRank. Bản chốt codebook giữ nguyên. Mọi payload/adjacency Nezha chỉ RAM, không ghi timestamp vector/chuỗi/span/log/cạnh.

### Checkpoint bước 3 — 08/10/2026, 09:36+07

- Thống kê mọi service/kênh đã ghi đủ trước nhãn ở runs/buoc3-002/features-no-label-index.json. Lượt 002 lỗi KeyError seed_metrics khi nối phân tích: trường chỉ có ở TORAI, bản ghi một seed lấy Hit trực tiếp từ dòng đã trích. Lỗi/traceback/giờ và mọi tệp giữ nguyên trong manifest/progress của lượt 002. Không đổi công thức/tiêu chí.
- Lượt tiếp buoc3-003 dùng lại toàn bộ aggregate có hash, chỉ đọc dev qua guard để dựng lại graph RAM đã mất khi tiến trình lỗi, đối chiếu audit graph; không tính lại thống kê tín hiệu hoặc trích bước 1/phương pháp. Barrier ghi thống kê trước nhãn của lượt 002 được giữ làm nguồn.
- Checkpoint ngữ cảnh: phạm vi SPEC/duyệt thời lượng đã ghi ở trên, đầu ra bước 1/chốt 002 bất biến; tiếp tục bước 3–6 trong phạm vi được duyệt. Chưa có bảng gán hợp lệ, chưa kiểm độc lập/đọc tay.

- Hiệu chỉnh mốc nhập tay checkpoint vừa trên: tiêu đề 09:36 là lỗi nhập giờ; tiến trình buoc3-003 thực bắt đầu 2026-10-08T09:33:07.059+07:00 theo manifest. Dùng mốc máy, không dùng tiêu đề nhập tay để tính chi phí.

- Rà source trước kiểm độc lập: schema TORAI/CIRCA đối chiếu372 source record; sửa fallback seed_metrics ở checker cho Nezha. Checker số học TraceRCA giữ numpy scalar tới sau built-in round; toy biên cho thấy chuyển float trước round có thể lệch native. Lỗi apply_patch bị từ chối do context không khớp, không file nào đổi; đã áp lại patch đúng. Lệnh đọc metadata gặp UnicodeEncodeError cp1252 khi in STATE; đọc lại với stdout UTF-8 đạt, không thay nguồn. Các thao tác này không là lượt phương pháp hoặc thay tiêu chí.
- Mốc máy checkpoint hiện tại: 2026-10-08T09:38:09.754052+07:00; producer tiếp tục tái dùng aggregate002 và graph RAM, chưa có output gán hợp lệ.

### Bước 4 đã ghi; tiếp phép đo D/D0 — 2026-10-08T09:38:53.008908+07:00

- buoc3-003 đã kiểm graph/aggregate tái dùng và ghi312 dòng gán theo tiêu chí cố định, nhưng lỗi duplicate keyword k ở dict seed pair D/D0. Sửa ghép dictionary, giữ lượt003 và ca-sai của lượt đó. Tiếp bằng script tiep_tu_gan_da_luu.py, không đọc raw/nhãn lại, lấy ca-sai003 đã lưu và chỉ tính D/D0.
- buoc3-004 lỗi thiếu numpy do dùng Python mặc định khi import evaluator; giữ manifest/tệp/snapshot004. Lượt005 dùng môi trường đã có nhưproducer, không cài dependency. Các lỗi trên ở phần thực thi khác nhau, không phải đổi tiêu chí hoặc lượt phương pháp. Mọi nguồn/snapshot/giờ ở runs/buoc3-003,004,005.

### Bước 3–5 — bảng và kiểm độc lập

- Kết quả đang dùng: runs/buoc3-005/manifest.json; gán tái dùng từ003, thống kê all-service tái dùng002. Không đọc/tính lại phương pháp. Bảng tổng hợp, schema, rootBARO, manual-selection và CSV được xuất từ evidence đã lưu.
- Kiểm ranking/membership/hòa/D/D0/P0/schema đạt, nguồn independent-ranking.json. Kiểm thống kê metric/span/log/operation/graph đạt, nguồn independent-statistics.json. Lượt checker thống kê đầu lỗi pandas.NA ở parent thiếu; giữ independent-statistics-attempt001.json, sửa kiểm null scalar theo dữ liệu và chạy lại. Không thay công thức/ngưỡng.
- Bước5 mẫu cố định được lưu tại manual-selection.json và manual-excerpts.json; Codex đọcRE2, trợ lý người làm đọcNezha, không thayClaude phảnbiện. Mốc đọc/kiểm: handoff-progress.jsonl và timestamp/elapsed trong từngfile kiểm. Bước4 đã ghi lúc2026-10-08T09:38:00.990+07:00 theo progress003.

### Checkpoint hoàn thiện bàn giao — 2026-10-08T09:54:18.183174+07:00

- Ngữ cảnh đã được nén; tiếp tục cùng phiên và gói bước 3–6 đã được Minh duyệt thời lượng. Nguồn hiện hành buoc3-005; thống kê tái dùng002, gán tái dùng003; mọi lượt hỏng giữ nguyên. Không đổi tiêu chí hoặc phạm vi.
- Đọc tay RE2/Nezha đã lưu tại manual-re2.json và manual-nezha.json trong runs/buoc3-005; đang hợp nhất ghi nhận đọc tay và kiểm bàn giao. Các bảng đã được đối chiếu độc lập với JSON ở report-review.json; chưa thay vai trò phản biện Claude.
- Hiệu chỉnh câu mốc bước4 ở mục trước: progress003 ghi labels_joined_for_analysis_only lúc 09:38:00.990+07; gán thực được ghi ở case_assignments_written lúc 09:38:04.460+07. Dùng stage cụ thể trong progress để tính thời gian, không dùng câu nhập tay.

- Kiểm bàn giao đầu giữ tại runs/buoc3-005/final-verification-attempt001.json: lỗi checker đòi key mechanisms không tồn tại ở view độ nhạy, trong khi step1 đã có mechanisms:null/evidence_computed:false; các view khớp toàn bộ step1. Đã sửa checker theo nguồn, không sửa view.
- Kiểm đóng gói đọc tay phát hiện metadata JSON Pointer record_source dùng / thay vì chuỗi rỗng cho toàn bản ghi. Chỉ sửa pointer trong manual-nezha/manual-reading; giữ bản trước sửa *-before-pointer-correction.json. Nhận định/số/tiêu chí/gán không đổi. Nguồn sửa và số tham chiếu: source_pointer_correction của hai file, kiểm đóng gói độc lập sẽ ghi manual-packaging-check.json.

### Tiếp sau gián đoạn usage — 2026-10-08T10:09:26.366380+07:00

- Minh báo phiên gián đoạn và yêu cầu tiếp tục. Kiểm tiến trình Python/py hiện không có. Lệnh Codex cuối trước gián đoạn `py -3 -B -` ghi cost-observed.json/nối chi-phi đã hoàn tất; không có lượt Python/phương pháp đang chạy.
- Hai trợ lý báo usage limit. verify_step1 đã kịp ghi manual-packaging-check.json đạt trước báo limit; native_stats chưa ghi toy-D-checks.json. Các artifact trước đó giữ nguyên. Codex làm tiếp phép thử giả D bằng stdlib từ bảng đã lưu; không gọi phương pháp hoặc raw. Nguồn kết quả/giới hạn: runs/buoc3-005/toy-D-checks.json.
- Phần bị gián đoạn là chuẩn bị bàn giao: kiểm cuối sau sửa checker, chốt manifest, cập nhật STATE và prompt Claude. Không trích bước1 hoặc chạy lại thống kê/phương pháp đã hợp lệ.

## Kết thúc phiên bước 3–6 — 2026-10-08T10:15:29.593504+07:00

### Báo cáo bốn mục

1. **Đã làm:** hoàn tất bước3–6 theo codebook chốt002 và WHY-38 đã duyệt. Tái dùng bước1/hash đã kiểm; thống kê RE2-TT dev30 và Nezha main qua guard, mọi service/kênh ghi trước nhãn; gán đa nhãn/primary và N/A theo phương pháp, P0 theo seed trên tập đủ điều kiện và số cờ cơ sởM5, D/D0 theo ca/ô. CIRCAdev19 dùng lại bằng chứngdev30; các viewNezha chỉ giữ status/Hit có sẵn. Không chạy lại phương pháp. Nguồn hiện hành: `results/T-028/runs/buoc3-005/manifest.json`, ca-sai/summary/concentration/schema/manual cùng thư mục; lineage giữ aggregate002/gán003. Các lỗi thực thi ở mapping/seed fallback/ghép D/môi trường/null checker/xuất bảng/pointer được giữ bản, sửa triển khai, không đổi tiêu chí.
2. **File thay đổi:** chỉ trong `results/T-028/` (scripts, ca-sai JSON/CSV, bản đồ, bảng đối chứng/phân tầng, rootBARO, schema/coverage, phân phối top-k, bảng phụ, đọc tay, chi phí và mọi runs), nối LOG này, chỉ dòngT-028 STATE. Chi tiết file/hash/byte tại `runs/buoc3-005/handoff-inventory.json` và manifest. Các thay đổi có sẵn của người dùng được giữ; SPEC/codebook/WHY/DECISIONS/src/taskkhác không sửa, không commit/push. CSV chỉ mã mờ/số/nhãn cơ chế; payloadNezha chỉ RAM, work không có payload. DòngSTATE chuyển “chờ phản biện”, chưa đóng task.
3. **Kiểm:** danh sách/hash bước1 khớp ở tiep-nhan-001; barrier all-service trước nhãn ở progress002. Kiểm độc lập và kiểm người làm:

   - `independent-ranking.json`: 22398 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/independent-ranking.json`.
   - `independent-statistics.json`: 24528 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/independent-statistics.json`.
   - `aggregation-review.json`: 46459 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/aggregation-review.json`.
   - `report-review.json`: 105097 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/report-review.json`.
   - `manual-packaging-check.json`: 3959 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/manual-packaging-check.json`.
   - `toy-D-checks.json`: 4 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/toy-D-checks.json`.
   - `final-verification.json`: 2342 kiểm đạt, nguồn `results/T-028/runs/buoc3-005/final-verification.json`.

   Đọc tay 70 mục phương pháp×ca/106 yêu cầu nhóm, mọi seed liên quan; 0 lệch tiêu chí. Nguồn: `manual-reading.json` và `manual-packaging-check.json`; từng nhận định/giá trị/N/A/nguồn ở `doc-tay.md`. Kiểm nguồn/pointer sau sửa metadata đạt. Phép thử giả D và một cặp đã lưu được kiểm bằng số hữu tỉ riêng, không chạy phương pháp; D=1 chỉ nói tập top-k trong cặp đó, không chứng minh bỏ dữ liệu. Kiểm parse/AST/bytecode/phạm vi/baseline/prefixLOG/STATE ngoài dòngT028 đạt ở final-verification. `git diff --check` đạt trước mục này (chỉ cảnh báo LF/CRLF ở file có sẵn); kiểm chốt manifest/phạm vi sẽ ghi `handoff-validation.json` sau khi nối prompt.
4. **Chưa chắc/cần Minh quyết:** bằng chứng kiểm được tới membership, hòa, diagnostics/score lưu, luật thống kê native, quan hệcallerN, schema, tập trung đầu ra và mức nền có điều kiện. Chưa phân xử nhân quả, thứ tự khởi phát và các giải thích khả thi khác theo từng nhóm. Không chốt có/không “lan có đáng kể”; nơi xử lý câu(c) còn OPEN do Minh chưa chọn, không tự giaoT-029 hoặc tạo cổng. Test/giữ ngoài chưa mở; tính đại diện, clock/nền/mốc và các phép can thiệp đổi đầu vào còn chưa kiểm. Chi phí đo được tại cost-observed.json; RAM/CPU/token chưa đo. Đĩa snapshot bàn giao 363785492 byte trên 203 file, nguồn handoff-inventory.json; gồm mọi lượt/bản cũ, vượt ước lượng đĩa chưa kiểm của SPEC. Không suy thời gian lịch thành CPU/token.

### Bước tiếp và lệnh cuối

- Bước tiếp chính xác: Minh mở phiên Claude Code mới ở `D:/RCA-flashticket`, dán nguyên prompt dưới; Claude đọc AGENTS, SPEC, LOG, toàn bộ đầu ra và nguồn thật, ghi duy nhất `tasks/T-028-p4-han-che-xep-hang/REVIEW.md` theo mẫu. Các trợ lý Codex chỉ kiểm người làm, không thay phản biện Claude. Sau REVIEW, người làm tiếp AGENTS bước7 bằng prompt có sẵn trong docs/review-prompt.md; không tự sửa theo finding khi Minh chưa quyết.
- Lệnh cuối đã chạy trước mục này: `py -3 -B -` chốt `runs/buoc3-005/manifest.json`, giữ manifest-before-handoff và snapshot script cuối; trước đó `py -3 -B results/T-028/scripts/kiem_chot_dau_ra.py --run-id buoc3-005 --output final-verification.json` đạt, `git diff --check` đạt. Lệnh sau khi nối mục này: `py -3 -B -` kiểm hash manifest/prompt/prefix/phạm vi và ghi handoff-validation; `git diff --check` là lệnh kiểm cuối.
- Nội dung commit đề xuất sau phản biện/Minh duyệt: `T-028: báo cáo hạn chế xếp hạng dev theo codebook đã chốt`. Chưa stage, commit hoặc push.

### Prompt phản biện Claude

Prompt chung dưới đây chép từ docs/review-prompt.md, chỉ điền mã task, đường dẫn và revision trung tính. SPEC ghi cổngG2; nguồn mẫu không có khối trọng tâm G2, nên không thêm khối của cổng khác.

```text
Bạn là người phản biện độc lập cho task T-028 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-028-p4-han-che-xep-hang/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-028-p4-han-che-xep-hang/SPEC.md, tasks/T-028-p4-han-che-xep-hang/LOG.md, các file đầu ra: results/T-028/codebook.md, results/T-028/danh-sach-ca-sai.md, results/T-028/ca-sai.json, results/T-028/ca-sai.csv, results/T-028/ban-do-han-che-xep-hang.md, results/T-028/bang-theo-o-va-doi-chung.md, results/T-028/BARO-du-lieu-root.md, results/T-028/schema-va-coverage.md, results/T-028/phan-phoi-top-k.md, results/T-028/bang-phu-co-dieu-kien.md, results/T-028/doc-tay.md, results/T-028/chi-phi.md, results/T-028/scripts/, results/T-028/runs/,
và kết quả `git diff 6c93e6dc31f0c991b4ac6d1cfd44fcc0e989c84c` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.
```

## Phiên bước 7 — tự soát độc lập rồi phản hồi REVIEW — 08/10/2026

- Codex, thiết bị LEVANMINH, người làm T-028; Claude là người phản biện. Minh giao tự soát trước mở REVIEW, ghi danh sách tự tìm vào LOG rồi mới đọc/đánh giá reviewer. Phiên này chỉ nối LOG và điền bảng cuối REVIEW; không sửa STATE, kết quả, script hay tài liệu khác; không commit.
- Bắt đầu kiểm độc lập: chưa mở REVIEW.md, không tin số/tóm tắt LOG; đọc SPEC/codebook và đầu ra thật, kiểm lại nguồn và tiêu chí. Hai trợ lý người làm chỉ đọc hai mảng khoa học/triển khai, cũng bị cấm đọc REVIEW trước lúc hoàn tất tự soát. Không test/data/locked, không chạy phương pháp. Mọi phát hiện là CANDIDATE cần Minh quyết, không tự sửa.
- Giờ máy mở phiên: 2026-10-08T11:02:23.9829864+07:00.


### Tự soát độc lập — kết luận ghi TRƯỚC khi mở REVIEW.md

- Đọc AGENTS, STATE/SPEC, LOG, codebook chốt 002, bản đồ, bảng theo ô/đối chứng, root BARO, schema/coverage, phân phối top-k, bảng phụ, đọc tay, chi phí và scripts. Đã đọc/parse toàn bộ JSON/JSONL và AST các script/snapshot dưới results/T-028; không mặc định file kiểm “passed” chứng minh kết quả đúng. Đối chiếu MRP P4, Q-33, WHY-38, DT18 và nguồn advisor.
- **Danh sách điểm tự tìm có đủ căn cứ: không có.** Chưa phát hiện lỗi ảnh hưởng tính đúng hoặc độ khớp nguồn trong phần đã kiểm. Không lập N1 cho một giới hạn đã được khai hoặc một nhận xét hình thức.
- Kiểm trực tiếp trên file thật: ca-sai gốc và bản buoc3-005 trùng byte; hash các output/check/script trong manifest khớp; Hit/cờ sai của mọi dòng OK khớp, non-OK giữ null đúng phạm vi. Tính lại P0 từ n/a/b và khối lượng phân phối top-k bằng số hữu tỉ đều khớp. Đối chiếu mẫu đọc tay/nhãn và source pointer hợp lệ; seed giữ riêng và không gộp P0 với primary.
- Trợ lý tự soát triển khai (không mở REVIEW): đối chiếu độc lập O/R/full key/certain-before/Hit trên các bản ghi gốc; P0 và các cặp D/D0/delta/V đã lưu không có sai khác. Tự soát khoa học đọc ghi nhận từng ca tay và kiểm nguồn/giới hạn; không thấy câu nâng M5/P0/proxy thành cơ chế lan đã xác nhận. Đây là hỗ trợ kiểm người làm, không thay reviewer.
- Q-33: bản đồ đã giữ các giải thích khác gồm caller tự bất thường/tác động chung, thiên hướng entity/operation/coverage/preprocessing, clock/nền/graph/mapping/nhãn và dao động hữu hạn; không dùng chênh M5−ΣP0 làm mức đáng kể. BARO root theo SimpleRCA không được gọi là dữ liệu BARO thực nhận; native trace dương do biên σN/làm tròn vẫn được nêu. Lựa chọn đã có WHY-38; barrier ghi mọi service trước nối nhãn hiện diện trong mã và progress.
- **Giới hạn tự soát:** chưa đọc lại toàn bộ cửa sổ raw hoặc tái lập phương pháp; M5/P0 đối chiếu dùng graph/caller_relation đã lưu và kiểm graph độc lập trên mẫu đã khai. Các bằng chứng kiểm đã có không loại hết lỗi số ở ngoài mẫu hoặc lỗi diễn giải mà reviewer có thể nêu. “Không tìm thấy” không là xác nhận tuyệt đối. Không mở test/data/locked, không chạy phương pháp, không ghi đầu ra kiểm ngoài LOG.
- Lệnh đọc kiểm tạm gặp KeyError khi hiểu metadata final_scripts như output phẳng và khi giả manual-nezha có trường cases; kiểm lại schema, sửa lệnh đọc RAM rồi tiếp. Lệnh đầu so cờ sai non-OK với False báo khác vì file đúng dùng null; đã kiểm riêng OK/non-OK, không ghi thành finding giả.
- Danh sách này được chốt trước khi mở REVIEW; sau đây mới đọc reviewer và đánh giá độc lập. Nếu phát hiện mới sau mở, sẽ ghi rõ thời điểm, không hồi tố thành điểm tự tìm trước REVIEW.

- Giờ máy chốt tự soát trước REVIEW: 2026-10-08T11:06:08.1439865+07:00.

### Đánh giá độc lập REVIEW — sau khi đã chốt tự soát

- Chỉ mở REVIEW sau mục tự soát và mốc 11:06:08+07 ở trên. Đối chiếu lại từng điểm với codebook, script, bản ghi/aggregate và hồ sơ P1 thật. Các kiểm sau đây là phản hồi reviewer, không hồi tố thành điểm tự tìm trước REVIEW. Không thêm N1: tự soát trước REVIEW không có finding đủ căn cứ; phần rộng hơn của R2/R4 ghi trong chính các điểm đó.
- **R1: ĐÚNG MỘT PHẦN, KHÔNG CHẶN.** Dữ kiện cấu trúc nên được nêu trực tiếp. Câu “phần lớn ca M0” không đúng khi đếm phương pháp×ca ở top-1: 23/50 mục M0 không có ancestor; không cộng top-1/top-5 thành hai ca. Nguồn: `results/T-028/ca-sai.json` → `/main_rows/*/mechanisms/1/assignment`, nối `/evidence/seed_evidence/*/ancestors`. Các tỉ lệ auth/frontend reviewer nêu khớp. Auth có span N nhưng không cạnh liên service; frontend có indegree=0, outdegree=7, nên không được gọi là “root không có cạnh”. Sáu graph RE2 20 cạnh có 25.794–34.533 span N hữu hiệu, các graph còn lại 55 cạnh có ít nhất 132.708; nguồn `results/T-028/runs/buoc3-002/features-no-label/RE2-TT/*.json` → `/aggregate/graph_end`. Không kết luận graph nhỏ là mất instrumentation: đường gọi/workload thực, cửa sổ, sampling hoặc coverage đều có thể cho hình đó.
- Phản bác mạnh nhất R1: bảng theo root và công thức P0 đã giữ số ancestor, nên phép so P0 tổng không sai. Phản bác này đứng: chỉ nhận sửa diễn giải, không đổi M0/M5. M5=False ở root không ancestor chỉ cho biết điều kiện nhận M5 không thể đạt; không chứng minh đây là nguyên nhân xếp sai, cũng không là bằng chứng cho/chống giá trị graph. Phải phân biệt graph phân tích liên service, graph operation MicroRank và graph metric CIRCA; `codebook.md:72–83`, `results/T-015/ho-so-microrank.md:203–209`, `results/T-014/ho-so-circa-kien-truc.md:127–131`.
- **R2: ĐÚNG MỘT PHẦN, KHÔNG CHẶN.** `results/T-028/scripts/tong_hop_bao_cao.py:61–79` chỉ xuất bảng proxy root, thiếu phần caller mà `results/T-028/codebook.md:68` yêu cầu. Tuy nhiên câu “cách giải thích … không có số” quá rộng: `native_stats.py:397–412` đã tính mọi service, checker `kiem_thong_ke_doc_lap.py:126–135` đã đối chiếu service trên mẫu đã khai, và `doc-tay.md:481,541,589,817,857` có ghi nhận caller. Không coi việc reviewer chỉ thấy một câu “root và hai caller” là bằng chứng không có các ghi nhận khác. Ví dụ BARO Nezha dev-27252dca60, recommendationservice thuộc giao ancestor/certain-before nhưng proxy τ3=False; nguồn `ca-sai.json` → seed evidence và `runs/buoc3-002/features-no-label/Nezha-OB/dev-27252dca60.json` → `/aggregate/trace_end/recommendationservice`.
- Phản bác mạnh nhất R2: mọi số đã có trong aggregate và có thể truy lại. Điều này đúng nhưng chưa thay được phần báo cáo cam kết. Phạm vi cần báo rộng hơn đề xuất chỉ đếm caller tăng trong ca M5: câu “mọi ca đủ dữ liệu” ở §3.3 bao gồm đối chứng và các caller không chắc chắn trước root. Đề xuất xuất root/caller theo dữ liệu đã lưu, quan hệ ancestor/certain-before giữ riêng; không tính lại tín hiệu hoặc đổi cờ. P95 root/caller cùng tăng hoặc chỉ caller tăng vẫn không phân xử lan, caller tự bất thường, tải/tài nguyên chung, clock hoặc nền.
- **R3: ĐÚNG MỘT PHẦN, KHÔNG CHẶN.** `ban-do-han-che-xep-hang.md:297–308` có đối chiếu tác giả theo phương pháp; thiếu nối rõ với từng nhóm theo SPEC dòng 41/72. TORAI `results/T-016/ho-so-torai.md:165–166`, SimpleRCA `results/T-017/ho-so-simplerca.md:79–81`, BARO `results/T-013/ho-so-baro.md:86` có hạn chế liên quan triệu chứng/root yếu/service bị ảnh hưởng. Chúng không xác nhận định nghĩa M5 gồm ancestor N và full key. MicroRank `results/T-015/ho-so-microrank.md:199` nói chất lượng tracing; phần cô lập/mapping ở dòng 203–209 là phân tích code riêng. CIRCA `results/T-014/ho-so-circa-kien-truc.md:127–131` tách giả định/lời tác giả với suy luận từ code. TraceRCA `results/T-015/tracerca-rcaeval.md:95–105` không xác nhận đã khảo sát đầy đủ bài gốc.
- Phản bác mạnh nhất R3: người đọc nối §6 với §7 được. Vẫn có nguy cơ đọc “liên quan” thành “tác giả đã nêu đúng cơ chế này”. Nhận sửa liên kết từng nhóm; không nhận cách ghi “không nêu” chỉ từ việc hồ sơ không có. Dùng “nêu trực tiếp / chỉ liên quan / chưa thấy trong nguồn đã khảo sát”; M0 là nhóm dư thao tác, không gán thành một hạn chế do tác giả phát hiện. Lỗi làm tròn M4 cũng không được quy cho tác giả.
- **R4: ĐÚNG, KHÔNG CHẶN; phạm vi rộng hơn reviewer.** `results/T-028/scripts/thuc_hien_buoc3_6.py:153–164` ghi đè lý do bất kỳ N/A nào. M6 base ở mỗi k bị đổi lý do trong cả 52 ca OK BARO và 30 ca TORAI RE2; nguồn `results/T-028/ca-sai.json` → `/main_rows/*/mechanisms/{1,5}/base_flags_all_OK_seeds/M6` và seed evidence. M6 explanation chỉ bị đổi khi có seed sai, không đổi lý do `no_OK_wrong_seed` của ca đúng. Ngoài ra TraceRCA Nezha dev-7b7c973198 (`/main_rows/261`): seed M5 là `root_not_returned`, cấp ca thành `seed_evidence_missing` ở cả hai k/base/explanation. Đây là lỗi chung hàm gộp, không chỉ BARO/TORAI.
- Phản bác mạnh nhất R4: lý do gốc vẫn ở seed, giá trị/nhãn không đổi. Đúng, nên chưa làm sai số gán; vẫn sai metadata cấp ca và dễ bị đọc thành thiếu dữ liệu. Không chọn tùy tiện lý do seed đầu nếu có nhiều lý do khác nhau. Sửa giữ lý do chung khi mọi seed N/A cùng lý do; với hỗn hợp, giữ N/A do chưa đủ bằng chứng và trình lý do từng seed. Không đổi OR, True/False/N/A, extent, số seed, primary hoặc P0.
- Nhận định chung reviewer “mọi tiêu chí xong đều đạt” cần hiểu có giới hạn: số/gán và đầu ra chính đạt trong kiểm đã làm, nhưng R2/R3 chính là hai phần trình bày cam kết chưa hoàn tất rõ. Chưa có căn cứ nâng chúng thành lỗi CHẶN hoặc suy số báo cáo sai.

### Đề xuất sửa gom theo file — CHƯA ÁP DỤNG, chờ Minh quyết

Tất cả dưới đây là CANDIDATE. Tác động: bổ sung diễn giải/báo cáo từ số đã lưu và sửa lý do N/A; không đổi codebook, tiêu chí, nhãn, threshold, phương pháp hoặc mở dữ liệu khóa. Không sửa SPEC/MRP/WHY/DECISIONS. Nếu Minh duyệt sửa, chỉ thực hiện các mục được chọn, giữ bản/lượt cũ. Phiên hiện tại chỉ ghi LOG và bảng cuối REVIEW.

**A. `results/T-028/ban-do-han-che-xep-hang.md` — R1, R2, R3**

1. R1, sau đoạn M0/§3 hiện chỉ nói cấu trúc/coverage “có thể còn giải thích”, thêm đoạn:
   > Ở top-1 có 23/50 mục phương pháp×ca M0 không có ancestor quan sát; đây không phải phần lớn nhóm M0. Auth RE2 có span N nhưng indegree=outdegree=0 trong graph phân tích; frontend Nezha có indegree=0 và outdegree=7. Không có ancestor làm M5=False khi graph khả dụng, chưa giải thích được vì sao phương pháp xếp sai. Nguồn: ca-sai.json → main_rows, assignment/seed ancestors; features-no-label buoc3-002 → aggregate/graph_end. Không đồng nhất graph này với graph native của phương pháp.
   Thêm ngay sau diễn giải P0:
   > RE2 có sáu graph N-end 20 cạnh với 25.794–34.533 span N hữu hiệu; các graph còn lại 55 cạnh có ít nhất 132.708. Tách MicroRank top-1 đủ P0 thành ba nhóm không chồng lặp: auth (4 bản ghi) có M5=0, ΣP0=0; graph 20 cạnh (6) có M5=0, ΣP0=1,935672514619883; graph 55 cạnh còn lại, đã loại auth (14), có M5=5, ΣP0=9,193680690019363. Chiều chênh vẫn âm; phép so tổng không sai. Đây là mô tả theo cấu trúc đã đo, không là cơ chế mới hoặc kiểm định nhân quả.
   Mọi số trỏ `results/T-028/ca-sai.json` → `/main_rows/*/evidence/seed_evidence/single/by_k/1/P0`, ancestor/certain-before và aggregate graph_end ở `runs/buoc3-002/features-no-label/RE2-TT/*.json`. Nêu riêng quan hệ gọi ít hơn có thể do workload/cửa sổ/sampling/coverage; không kết luận graph 20 cạnh bị hỏng.
2. R2, câu cũ M5 “Đã kiểm cha-con trong N, graph quality, full key/khối, proxy P95 và P0 có điều kiện” → sau khi bảng caller được xuất:
   > Đã đối chiếu cha-con trong N, graph quality, full key/khối và P0 có điều kiện. Proxy P95 đã tính cho mọi service; bảng caller-root-proxy.md trình root/caller theo ca và seed, giữ các split/τ đã khai. Phép kiểm độc lập số proxy chỉ bao phủ mẫu đã báo. Proxy là bối cảnh dữ liệu, không phân xử cơ chế lan hay đổi M5.
   Nếu Minh không duyệt xuất bảng, chỉ sửa câu để nói rõ “báo cáo hiện tổng hợp proxy root; số caller có trong aggregate và một số ca đọc tay, chưa có bảng hệ thống”. Cách này trung thực nhưng để yêu cầu §3.3 chưa hoàn tất; không đề nghị coi là sửa xong R2.
3. R3, §6 chưa có dòng nối nhóm → thêm đối chiếu ở từng nhóm, dẫn bảng §7 và nguồn P1:
   - M1: chất lượng/độ đầy đủ telemetry trong hồ sơ MicroRank/SimpleRCA chỉ liên quan việc root không có trong O; không ghi tác giả đã nêu đúng định nghĩa M1.
   - M2: lọc candidate BARO/ji TraceRCA là bằng chứng code; lời tác giả tương ứng chưa thấy trong các nguồn đã khảo sát. Không quy suy luận từ RCAEval cho bài TraceRCA gốc.
   - M3: chưa thấy lời tác giả về đúng bất định hòa được đo ở đây trong nguồn đã khảo sát; không suy thành tác giả không bàn hòa.
   - M4: lỗi làm tròn là lỗi implementation đã xác nhận trong P3, không là hạn chế do tác giả tự nêu.
   - M5: TORAI/SimpleRCA/BARO nêu các trường hợp root yếu hoặc affected service lên hạng; chỉ liên quan M5, không xác nhận quan hệ ancestor/certain-before hay lan. MicroRank tracing và CIRCA common cause/thiếu reference là bối cảnh liên quan, cũng không phải xác nhận M5.
   - M6: lời tác giả TORAI/SimpleRCA/MicroRank về triệu chứng yếu/không lệch latency chỉ liên quan các luật native trong task, không xác nhận cờ M6 trên cohort; BARO chỉ có mô tả root, M6=N/A. CIRCA có giả định thay đổi conditional distribution, không đồng nhất với ngưỡng cờ P4.
   - M0: không áp dụng phép đối chiếu “tác giả nêu M0”; đây là phần chưa được các cờ đã khóa mô tả.
   Nguồn: bốn hồ sơ/TraceRCA/CIRCA và dòng đã dẫn ở phần đánh giá R3. Giữ lời tác giả, bằng chứng code và kết quả task tách rõ. Không khảo sát thêm để lấp ô cho đủ.

**B. `results/T-028/scripts/tong_hop_bao_cao.py` và `results/T-028/scripts/xuat_ban_do.py` — R1–R3**

- Cũ: `proxy_tables` chỉ lấy root; renderer chỉ có bảng lời tác giả theo phương pháp và văn bản M5 chung.
- Mới: đọc lại các aggregate đã lưu, xuất cặp root/caller cho mọi ca có dữ liệu theo §3.3; mỗi seed giữ riêng. Caller dùng quan hệ đường đi dương tới root đã lưu ở §4, ghi riêng direct/ancestor/distance và certain-before. Tập giao phục vụ trỏ bằng chứng M5, không chọn toàn bộ bảng chỉ bằng M5=True. Root/graph/caller thiếu thì giữ N/A/lý do; non-OK giữ status và không gán cơ chế.
- Mỗi cặp có dataset/method/mã mờ/seed, Hit hoặc cờ đúng-sai ở hai k đã lưu, split native đã khai, P95N/P95A, số span mỗi phía, τ2/3/4 và availability/lý do. Giữ từng native service và mapping entity đã lưu; không tự gộp lại percentile hoặc tạo luật reduce mới khi một entity có nhiều native service. Trỏ đường dẫn aggregate và JSON pointer cho từng số. Không đọc raw, không gọi ranker/evaluator để tính lại phương pháp.
- Renderer xuất văn bản A, bảng caller và các dòng đối chiếu tác giả bằng nguồn hiện có. Không đổi công thức summary/P0 hoặc thứ tự primary.

**C. `results/T-028/scripts/thuc_hien_buoc3_6.py` — R4**

- Cũ, nhánh `elif any(v['value'] is None ...)`: mọi trường hợp trả `val(None, 'seed_evidence_missing')`.
- Mới: nếu mọi phần tử đều N/A và cùng một lý do, trả N/A với lý do chung; nếu còn nhiều lý do hoặc False xen N/A, giữ lý do chưa đủ bằng chứng cấp ca và kèm lý do từng seed để đọc được. Nhánh có True và nhánh toàn False giữ giá trị cũ; các bộ đếm/extent giữ nguyên. Caller ngoài hàm vẫn giữ `non_OK` hoặc `no_OK_wrong_seed` khi không có seed để gộp.
- Áp dụng lại **chỉ phép gộp metadata từ seed flags đã lưu**, bao gồm M5 TraceRCA. Không tính lại đặc trưng, P0, D/D0, score hoặc xếp hạng. Mặt trái cần tránh: chọn lý do seed đầu sẽ che N/A hỗn hợp; thay toàn bộ explanation sẽ làm mất lý do đúng của ca không có seed sai.

**D. Đầu ra dẫn xuất nếu Minh duyệt A–C**

- Thêm `results/T-028/caller-root-proxy.md` và JSON tương ứng trong một lượt sửa riêng `results/T-028/runs/phan-hoi-review-001/`; đây là báo số đã tính, không thêm phép kiểm/nhãn/ngưỡng.
- `results/T-028/ca-sai.json`: chỉ đổi lý do N/A cấp ca theo C. Bản mới nằm trong lượt sửa riêng; bản cũ lưu nguyên. `ca-sai.csv` dự kiến không đổi byte vì không chứa trường lý do.
- Những JSON đang chép cả dòng ca phải dùng bản metadata mới khi xuất bản mới: `manual-selection.json`, `manual-excerpts.json`, `manual-re2.json`, `manual-reading.json` trong lượt sửa riêng. Giữ nội dung quan sát và quy tắc chọn mẫu cũ. Các bản ở buoc3-003/004/005 và các bản “before” không được sửa.
- Lượt sửa riêng ghi manifest nguồn/hash, thời gian, phạm vi sửa và script snapshot theo cơ chế đã có; cập nhật nguồn trỏ ở các báo cáo được xuất từ bản mới. Không đổi số ca/nhãn/Hit/D/D0/P0; không bắt chạy lại các kiểm/thống kê không chịu ảnh hưởng. Báo cáo khác chỉ cần xuất lại nếu thực sự trỏ hoặc chép phần bị sửa; mọi thay đổi bổ sung ngoài mô tả này phải trình Minh trước.
- LOG của lượt sửa và dòng T-028 STATE chỉ cập nhật sau khi Minh duyệt thực hiện. Phiên hiện tại giữ STATE nguyên theo yêu cầu “chưa sửa file nào khác”.

### Kết thúc phiên bước 7 — AGENTS mục 7

1. **Đã làm:** tự soát độc lập và chốt “không có finding đủ căn cứ” vào LOG trước mở REVIEW. Đánh giá R1–R4 từ nguồn thật; R1–R3 đúng một phần, R4 đúng và có phạm vi rộng hơn. Tất cả KHÔNG CHẶN. Đã điền bảng cuối REVIEW, không thêm N1 và để trống cột Minh quyết. Gom đề xuất sửa theo file ở trên; chưa áp dụng.
2. **File đã đổi trong phiên:** chỉ `tasks/T-028-p4-han-che-xep-hang/LOG.md` (nối thêm) và `tasks/T-028-p4-han-che-xep-hang/REVIEW.md` (bảng người làm). Không sửa STATE/kết quả/scripts/WHY/SPEC hay file khác. Không commit/push.
3. **Kiểm đã chạy:** đọc/parse và các đối chiếu tự soát nêu trên; sau REVIEW đếm lại M0/graph/P0 phân tầng, kiểm proxy caller đã lưu, đối chiếu hồ sơ P1, kiểm lý do N/A seed→ca. Hash toàn bộ tập file theo dõi từ đầu phiên cho thấy ngoài LOG không file nào thay đổi; REVIEW kiểm riêng: phần trước bảng bổ sung còn nguyên byte, đủ bốn dòng R1–R4 và Minh quyết đều trống. LOG cũ còn nguyên byte. `git diff --check` không có lỗi whitespace; Git chỉ nhắc LF/CRLF của docs đã có thay đổi từ trước. Không mở test/data/locked, không chạy phương pháp hoặc tính lại tín hiệu raw.
4. **Chưa chắc/cần Minh quyết:** chọn các đề xuất A–D để sửa. Không coi nhận xét reviewer là lệnh sửa. Câu hỏi “lan có đáng kể”/nơi xử lý vẫn OPEN theo WHY-38; phiên này không quyết thay Minh. Kiểm trên đầu ra lưu không xác nhận nhân quả hay loại hết lỗi raw ngoài mẫu.

- Lệnh kiểm cuối trước ghi mục kết thúc: PowerShell đọc byte LOG/REVIEW, SHA256 prefix và bốn dòng phản hồi/cột trống, rồi `git diff --check`; kết quả: prefix nguyên, bốn dòng, cột Minh quyết trống, không lỗi whitespace. Lệnh kiểm hash dùng `Get-FileHash -LiteralPath … -Algorithm SHA256` theo danh sách đầu phiên, không ghi file.
- Hai lần chuẩn bị lệnh hash tạm không chạy được: V8 không có btoa; sau đó Windows từ chối lệnh chứa toàn bộ danh sách vì vượt chiều dài. Chuyển sang chia danh sách đọc thành các đoạn ngắn, kiểm đạt; không file nào bị ghi bởi hai lỗi đó.
- Bước tiếp theo chính xác: chờ Minh điền/chọn R1–R4 hoặc A–D. Khi có lời duyệt, đọc lại AGENTS, `tasks/T-028-p4-han-che-xep-hang/REVIEW.md:54–57` và mục đề xuất trong LOG; ghi lời duyệt trước sửa. Dùng `results/T-028/runs/buoc3-005/ca-sai.json` và `features-no-label-index.json` làm nguồn, chỉ sửa những file/đầu ra đã được chọn. Chưa có lệnh sửa được phép chạy trong phiên này.
- Checkpoint ngữ cảnh: tự soát trước REVIEW và đánh giá sau REVIEW đã được tách mốc; không làm lại bước 3–6 hoặc hồi tố finding. Bản gán hiện hành vẫn buoc3-005. Chỉ LOG/REVIEW được phép đổi theo lời Minh ở phiên này.
- Kiểm sau ghi LOG đạt: prefix LOG/REVIEW nguyên, đủ bốn dòng phản hồi và cột Minh quyết trống. Lệnh shell cuối đã chạy: kiểm SHA256 prefix bằng PowerShell; `git diff --check`; `rg -n` các tiêu đề tự soát/đánh giá/đề xuất/kết thúc và bốn dòng R1–R4 trong LOG/REVIEW; `Get-Date -Format o`. Giờ máy chốt phiên: 2026-10-08T11:18:23.0491520+07:00; thời gian từ mở phiên khoảng 16 phút.

## Phiên sửa sau phản biện — 08/10/2026

- Mở phiên 2026-10-08T12:45:10.4647107+07:00; Codex, máy LEVANMINH, người làm T-028; Claude phản biện.
- **Lời Minh duyệt, ghi trước sửa:** “duyệt sửa, sau sửa báo cáo lại tôi xem còn vấn đề nào tồn đọng trước khi đóng task không”. Phạm vi đã trình: A–D trong phiên bước 7 và bổ sung R5 với kết luận thu hẹp trong chat. Thực hiện R1–R4; R5 chỉ xác nhận thống kê graph/bậc đã lưu và cờ cơ sở MicroRank trên cohort, không khẳng định toàn topology giống hệt hoặc phần lớn chênh lệch do graph. M2 chỉ nối TraceRCA có ca thực. Đây là duyệt sửa, chưa duyệt đóng task/commit.
- Bản đồ tác động: sửa ba script thuc_hien_buoc3_6.py, tong_hop_bao_cao.py, xuat_ban_do.py trong results/T-028/scripts/; bản đồ/report caller và metadata ca cùng các bản dẫn xuất đã nêu ở A–D; tạo lượt riêng runs/phan-hoi-review-001 (manifest/nguồn/hash/snapshot/thời gian). LOG nối thêm, bảng người làm REVIEW ghi trạng thái sửa, dòng T-028 STATE cập nhật. Giữ mọi lượt cũ và nội dung reviewer; không sửa SPEC/codebook/WHY/DECISIONS/src hoặc dữ liệu.
- Cách làm: chỉ đọc aggregate/seed flags đã lưu; không đọc lại raw, không tính lại đặc trưng, không chạy phương pháp/P0/D/D0. Sửa gộp lý do N/A trước; báo đủ root/caller, mô tả cấu trúc và đối chiếu từng nhóm; tự kiểm phần chịu ảnh hưởng và báo tồn đọng. Ước lượng dưới một giờ, chưa có lượt máy dài. Không dùng trợ lý phụ, không commit.


### Checkpoint và kết quả sửa theo lời duyệt

- Checkpoint ngữ cảnh: phần sửa và tự kiểm đã xong trước nén ngữ cảnh; tiếp tục chốt manifest/LOG, không làm lại bước 3–6. Lượt hiện hành là results/T-028/runs/phan-hoi-review-001; phép đo gốc vẫn buoc3-005.
- R1: bản đồ đã báo đúng 23/50 mục M0 top-1 không có ancestor, tách ba nhóm MicroRank RE2 không chồng lặp; không coi việc thiếu ancestor là nguyên nhân xếp sai và không đồng nhất graph phân tích với graph native. Nguồn số và phân tầng: runs/phan-hoi-review-001/structure-description.json, dẫn trực tiếp ca-sai/aggregate gốc trong file.
- R2: xuất caller-root-proxy.md và runs/phan-hoi-review-001/caller-root-proxy.json cho mọi ca/seed, root cùng mọi proper ancestor đã lưu. Có 372 bản ghi seed và 1.756 dòng quan sát native; mỗi dòng giữ service/mapping, split, P95N/P95A, nN/nA, các τ đã khai, availability/lý do và JSON pointer nguồn. Không chọn bảng chỉ bằng M5=True, không gộp percentile mới. Non-OK chỉ là bối cảnh. Nguồn số: review-verification.json và caller-root-proxy.json của lượt sửa.
- R3: từng nhóm nối với phát biểu tác giả hoặc nói rõ chưa thấy trong các nguồn đã khảo sát. M2 chỉ nối TraceRCA có ca thực; không gán lỗi implementation M4 hoặc phần dư M0 thành hạn chế tác giả. Không mở khảo sát mới.
- R4: sửa merge_flags để giữ lý do chung khi mọi seed đều N/A; N/A hỗn hợp giữ lý do từng seed; True OR và False cùng bộ đếm/extent giữ nguyên. Áp dụng lại chỉ metadata từ seed đã lưu: 205 trường lý do cấp ca đổi, gồm 137 no_native_activation_threshold, 64 intermediate_not_saved_requires_rerun, 4 root_not_returned. Nguồn: metadata-changes.json và review-verification.json của lượt sửa. Hit, nhãn, giá trị cờ, P0, D/D0, score/rank và ca-sai.csv không đổi.
- R5: bổ sung mô tả Nezha trong bản đồ. Với MicroRank, cờ cơ sở M5=True ở 20 ca root khác frontend, nhưng chỉ 14 ca thuộc nhóm sai top-5 gán M5; không đánh đồng cờ cơ sở với gán ca sai. Các thống kê graph/bậc đã lưu khớp ở 22 ca; chúng không chứng minh toàn adjacency giống hệt hay frontend có trong mọi trace. So phương pháp không phân xử được lan, lỗi riêng caller, tác nhân chung hoặc thiên lệch điểm. Nguồn: structure-description.json, ca-sai.json và các aggregate được dẫn tại đó.
- Bản mới ca-sai/manual-selection/manual-excerpts/manual-re2/manual-reading nằm trong lượt riêng. Ghi chú đọc tay và quy tắc chọn mẫu giữ nguyên; doc-tay.md chỉ cập nhật nguồn metadata. Bản before-root và mọi buoc3-* giữ nguyên. Lần xuất report đầu và lần kiểm đầu cũng giữ trong report-attempt001, review-verification-attempt001.json; chỉ chỉnh nhãn/thứ tự bảng, không đổi số.
- Bảng người làm ở cuối REVIEW đã ghi trạng thái sửa R1–R4 và R5; phần reviewer trước bảng còn nguyên byte, cột Minh quyết để trống. Chỉ dòng T-028 trong STATE đổi thành chờ Minh xem trước khi đóng.

### Kết thúc phiên sửa — AGENTS mục 7

1. **Đã làm:** sửa A–D và bổ sung R5 trong phạm vi được duyệt. Báo cáo đã thu hẹp kết luận về graph/lan, báo hệ thống root/caller, nối hạn chế tác giả theo nhóm và giữ đúng lý do N/A. Sau tự kiểm chưa thấy lỗi tồn đọng cần sửa trong phạm vi T-028. Đây là kết luận tự kiểm, chưa phải Minh duyệt đóng.
2. **File đã đổi:** ba script trong results/T-028/scripts/; ca-sai.json; ban-do-han-che-xep-hang.md, bang-theo-o-va-doi-chung.md, bang-phu-co-dieu-kien.md, BARO-du-lieu-root.md, doc-tay.md, phan-phoi-top-k.md, schema-va-coverage.md, chi-phi.md; thêm caller-root-proxy.md và lượt runs/phan-hoi-review-001. LOG chỉ nối thêm; REVIEW chỉ bảng người làm; STATE chỉ dòng T-028. Danh sách/hash/snapshot đầy đủ trong manifest.json. SPEC, codebook, WHY, DECISIONS, src và các lượt cũ không đổi. Không commit/push.
3. **Kiểm đã chạy:** review-verification-source.py kiểm metadata trước/sau, sáu tình huống N/A chung/hỗn hợp/thiếu/OR, đối chiếu mọi dòng root/caller với thống kê nguồn, giữ mẫu/ghi chú đọc tay, bảng số cũ và AST ba script; kết quả passed trong review-verification.json. Đã kiểm hash 180 file lượt cũ và 8 file đo dùng lại; nhãn/Hit/P0/D/D0 giữ nguyên. Kiểm prefix reviewer và chỉ dòng T-028 STATE đổi đều đạt. Không mở test/data/locked, không đọc raw, không chạy phương pháp hoặc tính tín hiệu mới. Kiểm diff không có lỗi whitespace; Git chỉ nhắc LF/CRLF ở docs có thay đổi từ trước.
4. **Chưa chắc/cần Minh quyết:** nơi xử lý câu “lan có đáng kể” vẫn OPEN theo WHY-38; chưa giao mặc định cho T-029. Không coi M5/P0/proxy là phân xử nhân quả hoặc thứ tự khởi phát. Clock, nền sạch, coverage và tính đại diện vẫn là giới hạn đã khai, không phải lỗi mới hay phép kiểm bổ sung cần mở trong T-028. Minh xem báo cáo rồi quyết đóng task; chưa đóng hoặc tự mở thêm vòng review.

- Thời gian: lượt sửa bắt đầu 2026-10-08T12:48:10.994853+07:00; hoàn tất phần sửa/kiểm 2026-10-08T13:05:44.825227+07:00; 1053.830 giây wall time, gồm đọc/viết/kiểm. Producer metadata/bảng chạy 3.914 giây. Nguồn manifest.json; số dung lượng trong chi-phi.md/cost-observed.json là snapshot tại thời điểm đã ghi, không phải số cuối sau ghi bàn giao. Chốt LOG lúc 2026-10-08T13:11:07.862470+07:00.
- Ba lỗi chuẩn bị JavaScript do dấu Markdown backtick không chạy được tool, không gây mutation; đổi cách mã hóa chuỗi rồi chạy thành công. Giữ mọi lượt xuất/kiểm; không có lượt phương pháp mới.
- Lệnh đã chạy: py -3 -B results/T-028/scripts/tong_hop_bao_cao.py --run-id phan-hoi-review-001 --review-from buoc3-005; renderer xuat_ban_do.py cho lượt sửa; py -3 -B results/T-028/runs/phan-hoi-review-001/review-verification-source.py. Lệnh cuối trước ghi bàn giao: py -3 -B -c đọc manifest/review-verification/before-inventory/cost-observed và docs/review-prompt.md để đối chiếu. Sau ghi chỉ kiểm hash/file set/prompt/diff, không chạy lại phép đo.
- Bước tiếp theo chính xác: Minh đọc results/T-028/ban-do-han-che-xep-hang.md, caller-root-proxy.md, tasks/T-028-p4-han-che-xep-hang/REVIEW.md (bảng cuối) và runs/phan-hoi-review-001/review-verification.json; quyết có đóng T-028 hay còn sửa mục cụ thể. Nếu duyệt đóng, cập nhật đúng dòng T-028 STATE theo lời duyệt. Nội dung commit đề xuất sau khi Minh duyệt riêng: “T-028: hoàn tất bản đồ hạn chế xếp hạng và sửa theo phản biện”; chưa chạy git commit/push.

### Prompt phản biện chuẩn để dùng nếu Minh yêu cầu

Chép nguyên văn Prompt chung của docs/review-prompt.md, chỉ điền thông tin trung tính. File mẫu không có khối G2. Lưu sẵn theo AGENTS; không tự mở thêm phiên phản biện.

```text
Bạn là người phản biện độc lập cho task T-028 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-028-p4-han-che-xep-hang/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-028-p4-han-che-xep-hang/SPEC.md, tasks/T-028-p4-han-che-xep-hang/LOG.md, các file đầu ra: toàn bộ results/T-028/ (báo cáo, codebook, scripts, CSV/JSON và runs),
và kết quả `git diff 6c93e6dc31f0c991b4ac6d1cfd44fcc0e989c84c` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.
```


## Đóng T-028 theo duyệt của Minh — 08/10/2026

- Mở lượt 2026-10-08T13:18:32.830727+07:00; Codex, thiết bị LEVANMINH, người làm T-028; Claude phản biện.
- **Quyết định của Minh, ghi trước cập nhật trạng thái:** “đóng task”. Minh duyệt đóng sau báo cáo sửa R1–R4 và bổ sung R5; lời duyệt không cấp quyền commit/push hoặc quyết nơi xử lý câu “lan có đáng kể”.

### Kết thúc lượt đóng — AGENTS mục 7

1. **Đã làm:** ghi lời Minh duyệt đóng T-028 và chuyển đúng dòng T-028 trong STATE thành Xong (08/10/2026). Kết quả hiện hành vẫn runs/phan-hoi-review-001; phép đo gốc buoc3-005.
2. **File đã đổi:** chỉ nối thêm tasks/T-028-p4-han-che-xep-hang/LOG.md và sửa dòng T-028 trong docs/STATE.md. Không sửa báo cáo, manifest lịch sử, REVIEW, SPEC, codebook hoặc tài liệu quyết định. Không commit/push.
3. **Kiểm đã chạy:** đọc AGENTS, STATE, SPEC và mục cuối LOG; xác nhận báo cáo chính/bảng caller có thật và review-verification.json đã passed. Kiểm byte cho thấy LOG cũ còn nguyên, STATE chỉ đổi dòng T-028; git diff --check cho hai file đạt. Không chạy lại phương pháp/đặc trưng, không mở test/data/locked.
4. **Điều còn mở/cần Minh quyết:** T-028 đã đóng. Câu “lan có đáng kể” và nơi xử lý vẫn OPEN; đóng task không xác nhận nhân quả. Chưa có duyệt commit/push.

- Bước tiếp theo: không chạy thêm việc T-028. Nếu Minh duyệt commit/push, đọc git status và git diff để chọn đúng file thuộc T-028 cùng phần LOG/STATE liên quan; không đưa thay đổi task khác vào commit. Nội dung đề xuất: “T-028: hoàn tất bản đồ hạn chế xếp hạng và sửa theo phản biện”.
- Lệnh kiểm cuối đã chạy trước ghi báo cáo: git diff --check -- docs/STATE.md tasks/T-028-p4-han-che-xep-hang/LOG.md (đạt), trong lượt py -3 -B -c đóng task. Sau ghi chỉ kiểm lại diff và trạng thái, không chạy thực nghiệm.
