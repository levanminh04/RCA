# T-022 — Giao thức P3, adapter RE2 và đo pilot

- **Trạng thái:** SPEC đề xuất ngày 05/10/2026. Minh cho phép soạn tài liệu; chưa duyệt nội dung SPEC hoàn chỉnh hoặc triển khai.
- **Người làm:** Claude.
- **Người phản biện:** Codex.
- **Người soạn bản nháp:** Codex theo yêu cầu Minh; đây không phải phiên thực nghiệm T-022.
- **Thuộc gói MRP:** P3 — **Cổng:** G2.

## Mục tiêu

Phục vụ RQ1, RQ2 và DT18-NV3: tạo giao thức so sánh các phương pháp đã có trên dev, đủ đúng để làm P3/P4. Các phương pháp nhận bằng chứng quan sát, không nhận đáp án. Đầu ra phải cho biết chi phí thực và phần nào còn thiếu để xếp lịch qua đêm; không chạy benchmark đầy đủ trong task này.

## Đầu vào

- AGENTS.md; docs/STATE.md; docs/MRP.md P3/P4, §6–7; docs/DECISIONS.md Q-61–Q-70, Q-72; docs/WHY.md; docs/LESSONS.md; docs/PLAN-P3-G2.md.
- Đề tài/hướng dẫn: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md.
- Allowlist 30 dev RE2-TT: results/T-002/local-inspection/run-002/case-summary.csv, cases.json và summary.json; đối chiếu chia T-021 ở results/T-021/chia-theo-o/A-phan-tang.csv.
- Chỉ telemetry 30 ca dev được xác nhận nằm trong data/rcaeval/. Mốc từ kết quả metadata T-002 đã có; không đọc cases.parquet ở data/locked/ hoặc suy mốc từ vị trí giữa file.
- Hồ sơ/code: results/T-013/ (BARO, detector, cửa sổ); results/T-014/ và src/circa_kien_truc/; results/T-015/ và src/microrank/; results/T-016/ và src/torai/; results/T-017/ và src/simplerca/; results/T-018/ho-so-gdn.md, dinh-chinh-task-cu.md (bộ cột).
- results/T-006/cham/bang-so-sanh.md và results/T-007/kiem-dung-dan.md: bằng chứng lịch sử; không mặc định mọi phương pháp khớp mốc.
- Clone/runtime đã có trong môi trường T-013–T-017: chỉ đọc, kiểm tồn tại và version trước dùng. Không sửa hoặc cài vào môi trường chung; nếu thiếu môi trường phải trình phương án và dung lượng riêng.

## Đầu ra

Trong results/T-022/:
1. giao-thuc.md — dữ liệu, thời điểm thông tin có sẵn, hai chế độ, ứng viên, mapping, scoring, trạng thái lỗi và các giới hạn.
2. lua-chon-can-duyet.md và de-xuat-why.md — từng CANDIDATE, phương án đối lập thật, lý do, bằng chứng, điều kiện sai và kết luận phụ thuộc. Giao rõ nháp WHY cho cả Q-64, Q-65, Q-66, Q-67 đã quyết; không mở lại các quyết định này. Đề xuất bổ sung ghi chú ở WHY-19 rằng trạng thái cửa sổ đã được Q-64 thay thế, giữ bối cảnh lịch sử. Chưa tự ghi nguồn chung.
3. dung-lai-bang-chung.csv — từng phiên bản/code/cấu hình P3 → artifact đã kiểm → phạm vi hợp lệ → phần thiếu do P3 đổi giao thức.
4. allowlist-dev.json — đúng 30 ca, đường dẫn chỉ phía runner, provenance và fingerprint để dựng lại.
5. quy-tac-cot.json, mappings/ và cau-hinh/ — dự thảo quy tắc và cấu hình; ghi rõ proposed/approved. Không bật mặc định một cấu hình còn OPEN.
6. do-chi-phi.md — kết quả pilot tách đọc, chuẩn bị, detector/graph/scorer, ghi kết quả; phép chiếu toàn dev và đề xuất máy/lịch.
7. scripts/, tests/ và runs/<run-id>/ — script kiểm, fixture, stdout/stderr, config, thời gian/RAM, kết quả trung gian và lượt hỏng. Chỉ lưu snapshot cần kiểm, không sao telemetry mỗi run.

Trong src/p3/: reader/selector, kiểu dữ liệu cho ranker/detector, adapter giao thức, evaluator và runner dùng chung. Lõi phương pháp đã có chỉ import, không sửa. Gói này không bao gồm adapter Nezha/Eadro hoàn chỉnh.

## Phạm vi ghi

Sau khi Minh duyệt SPEC:
- src/p3/
- results/T-022/
- tasks/T-022-giao-thuc-p3/LOG.md
- dòng T-022 trong docs/STATE.md.

Không sửa SPEC đã duyệt, docs/WHY.md, docs/DECISIONS.md, data/README.md, method code cũ, task/results cũ hoặc runtime chung. Nháp WHY nằm trong results/T-022/; việc ghi vào nguồn chung cần Minh duyệt nội dung/phạm vi riêng. Nháp chưa được ghi vào WHY không đủ điều kiện dùng lựa chọn trong số khoa học P3.

Chạy Python không ghi bytecode; runtime/tmp/cache mới, nếu cần và đã nằm trong phạm vi, đặt trong results/T-022/work/. Không thêm dependencies hay kiểm soát mới vào repo ngoài phạm vi.

## Các bước và phụ thuộc

0. **Tự soát trước triển khai.** Kiểm SPEC đủ một phiên, input/runtime tồn tại và không mâu thuẫn nguồn. Nếu cần đổi phạm vi hoặc tách task, trình Minh trước. — kiểm: LOG mở phiên, danh sách OPEN và phạm vi được duyệt.
1. **Kiểm allowlist và bảng bằng chứng.** Ghép metadata/chia ô, đúng 30 dev; method version theo Q-62 và WHY-19. Kiểm artifact có thật và còn hợp lệ. — kiểm: tổng ca/ô, unique ID, đường dẫn không locked; bảng từng bản, không chỉ tên phương pháp.
2. **Soạn lựa chọn giao thức trước số benchmark.** Có thể làm song song bước 1 ở phần đọc nguồn. Trình các mục dưới và nháp WHY; Minh quyết trước khi dùng lựa chọn vào kết quả. — kiểm: mỗi mục có nguồn, phương án khác, giới hạn, chủ quyết và trạng thái; không chọn theo chênh accuracy.
3. **Cài reader/evaluator và phép kiểm giả.** Chỉ sau khi hợp đồng tương ứng đã chốt. Không cần chờ phần detector nếu chỉ cài fixture độc lập. — kiểm: fixture biết đáp án và replay artifact phù hợp; record nguyên đầu ra, ERROR/NO_EVIDENCE/unsupported rõ ràng.
4. **Đo pilot đúng cấu hình đã được phép.** Pilot chỉ chạy sau khi cấu hình liên quan đã được Minh duyệt và ghi vào docs/WHY.md; nháp WHY không đủ quyền chạy. Chọn tối đa ba ca dev theo yếu tố chi phí của từng phương pháp từ metadata: số điểm thời gian T và số cột thực d đưa vào detector; số span/operation với ranker trace. Nêu ca nào phủ mức nhỏ/trung vị/lớn của yếu tố nào; tổng byte telemetry chỉ là thông tin bổ sung, không bảo đảm đại diện. Không chọn theo root, loại lỗi hoặc accuracy; dùng lại snapshot hợp lệ khi đủ. BOCPD dùng tập cột Q-67 và đúng biên chuỗi/quy tắc trạng thái đã chốt cho chế độ (b), không lấy cách cắt quanh injection của reproduce_bocpd. Đo tuần tự, không có lượt nặng khác. — kiểm: file log từ đầu, elapsed từng bước, peak RSS/commit khi lấy được, bytes đọc/ghi, exit status và input shape. Timeout chỉ cho giới hạn dưới, không phải thời gian hoàn tất.
5. **Chiếu chi phí và bàn giao.** Quy về toàn 30 dev, số seed, episode và Q-40; nêu máy rảnh/tranh máy. Đề xuất lịch và phạm vi T-024/T-025, không tự khởi các task đó. — kiểm: phép chiếu có giả định, trường hợp sai, nguồn từng số; LOG cuối phiên và dòng STATE.

### Nội dung phải khóa ở bước 2

- **Chế độ (a):** áp dụng Q-64 theo timestamp: sau mốc 300 s; trước tối đa 300 s, không chồng lần tiêm trước. Không coi 300 dòng luôn là 300 giây; ghi cửa sổ thực khi dữ liệu thiếu. Mốc biết trước chỉ ở adapter chế độ (a).
- **Chế độ (b):** detector không nhận injection time, root/fault label hoặc tên/đường dẫn ca. Khóa warm-up, reference, thời điểm thống kê được phép dùng, alarm cadence, gộp episode, matching nhãn chỉ phía evaluator, thời điểm tính độ trễ và cửa sổ RCA sau alarm. Nêu detector nào nối ranker nào có cơ sở prior work, không tự ghép mọi ranker thành phương pháp mới.
- **Chuỗi đầu vào detector (b):** khóa full recording hay từng đoạn; nguồn chọn biên độc lập lỗi, độ dài/bước đoạn, khởi động lại hay giữ trạng thái và lịch sử có sẵn ở đầu chuỗi. Tách các mục này khỏi cửa sổ Q-64 của chế độ (a) và cửa sổ RCA sau alarm. Q-67 chỉ duyệt tập cột, không duyệt cách cắt 300+300 quanh injection. Full RE2 1.441 điểm là một phương án; đoạn chọn bằng lịch/quy tắc độc lập lỗi cũng có thể trình Minh với lý do và giới hạn, không chọn để ép chi phí vừa ngân sách.
- **Phạm vi (b):** recording RE2 được cắt quanh lỗi; BOCPD bản gốc có min–max cả window và sentinel cuối. Trình Minh: hồi cứu giữ code gốc với hạn chế boundary/look-ahead, hoặc preprocessing nhân quả khác prior cần WHY và kiểm bổ sung. Không gọi snapshot là stream vận hành liên tục; không nối các ca thành một stream giả.
- **CIRCA:** RHT-only/RHT+DA, model, mapping/meta rules, metric cô lập, nguồn graph và thời điểm xác định schema. Graph trace trước mốc không tự chứng minh preprocessing chỉ dùng normal.
- **MicroRank sửa đầu vào:** full-score/top truncation, mapping operation→service, exact-copy/conflicting identity, reference thiếu và service vắng trace. Không dùng T-007 làm số đích cho biến thể sửa.
- **TraceRCA:** lọc hữu hạn trước sort, tie, zero/NO_EVIDENCE; ghi tác động của finite+tie, không quy toàn bộ khác biệt cho một lỗi.
- **Bộ cột:** giao/hợp hoặc phương án theo ý nghĩa kênh, xử lý cột thiếu/mới/hằng, thời điểm schema có sẵn; áp cho phương pháp nào. T-018 cho thấy bộ cột tương quan root; fixed universe không tự xóa thông tin rò qua missingness. Không âm thầm bỏ error hoặc điền một ngưỡng riêng chưa được biện minh.
- **SLI và ứng viên:** cấu hình từ nguồn quan sát/kiến trúc hợp lệ, không theo root. Cùng universe đánh giá ở mức service nhưng phương pháp thiếu bằng chứng không được tự tạo điểm/rank cho service vắng; báo coverage và mẫu số đã khóa.
- **Chấm:** MRR, NDCG@5, Hit@1/3/5, AC@k/Avg@5 và Retrieval@K/Rerank@1 với K=5,10 theo Q-65; định nghĩa tie, metric→service, partial rank, root absent, lỗi/không bằng chứng; bootstrap theo ô với confidence/seed/số mẫu được nêu rõ. Ghi định nghĩa của RCAEval khi metric trùng nghĩa; không báo nhiều tên như nhiều bằng chứng độc lập.
- **Seed và chọn cấu hình:** TORAI ít nhất ba seed theo WHY-19/20. Không lấy nhãn root để học; cấu hình dev được dùng đúng ngân sách nhãn đã quyết.

## Kiểm đúng đắn

- Selector từ chối locked, ca ngoài whitelist, path traversal, ID không hợp lệ; label và locator chỉ ở runner/evaluator. Đổi locator giữ payload phải giữ kết quả.
- Fixture nhỏ có hạng đúng, hạng hòa, danh sách ngắn, trùng service, root vắng, điểm không hữu hạn, ERROR và NO_EVIDENCE. Tính độc lập, rồi đối chiếu RCAEval; khớp code tham chiếu không tự chứng minh công thức đúng.
- Ranking ngẫu nhiên kiểm kỳ vọng theo đúng universe/coverage và seed; không yêu cầu một lần ngẫu nhiên “gần” mốc mà không có sai số.
- Hai cửa sổ normal/normal, hoán vị dòng/cột phù hợp, dữ liệu thiếu và các nhánh dự phòng theo hồ sơ đã có; không chỉnh ngưỡng để kiểm đẹp.
- Bộ cột: so trước/sau xử lý và dấu vắng cột; kiểm tương quan với nhãn chỉ ở evaluator/audit, không đưa mapping root hoặc missing mask suy nhãn vào phương pháp.
- Detector: fixture known-answer cho alarm, sentinel, warm-up, timestamp; kiểm thay đổi nhãn/mốc tiêm phía evaluator không đổi alarm đầu vào chế độ (b).
- Không tái lập bảng 90 ca bằng 30 dev, không mở 60 test. Phân biệt mốc công bố có/không và bản gốc/bản sửa trong bảng bằng chứng.
- Chi phí đủ cho dự báo: tính overhead toàn tiến trình, seed và cache policy; không lấy thời gian hàm đơn lẻ làm tổng. Chưa đo đủ toàn dataset thì phép chiếu vẫn “chưa kiểm”.

## Tiêu chí xong

- Có đủ giao thức, code chung, bảng bằng chứng, đề xuất WHY, fixture và pilot; allowlist đúng 30 dev.
- Không lựa chọn OPEN bị dùng như DECIDED. Lựa chọn cần thiết đã được Minh duyệt và ghi vào WHY trước khi dùng số P3; kiểm trên file nguồn thật.
- Bộ chấm và các checks quan trọng đạt; lỗi thật không bị bỏ hoặc biến thành thứ tự cột.
- Có số chi phí theo cấu hình Q-67, hoặc bằng chứng lượt lỗi/giới hạn và đề xuất xử lý; không bắt BOCPD phải vừa để báo xong.
- LOG đủ tiếp nhận trên máy khác. Nếu đang chờ quyết định thiết yếu, chỉ báo phần đã hoàn tất và phần còn OPEN, không báo task xong.

## Không làm

Không benchmark đầy đủ 30 ca × sáu phương pháp; không mở test/RE3-OB; không chạy Nezha/Eadro; không đổi phương pháp, cửa sổ hay ngân sách; không chạy EC2, tải telemetry, commit/push hoặc tự cập nhật tài liệu chung.

## Chi phí ước lượng

CANDIDATE, **chưa kiểm**: 3–6 giờ công agent; 30–90 phút tổng pilot, mỗi lượt dưới 1 giờ; RAM 1–3 GB, đĩa tăng 0,1–0,5 GB nếu tái dùng môi trường và không nhân telemetry. Không tải mới, không GPU/EC2. Snapshot RAM trống hiện tại chỉ khoảng 2,74 GiB; phải kiểm lại trước lượt nặng.

Giả định tái dùng lõi/runtime và tối đa ba ca đại diện theo yếu tố chi phí của từng phương pháp. Sai nếu cần môi trường mới, scorer/graph hoặc alarm làm chi phí tăng. Nếu dự kiến một lượt trên 1 giờ, thiếu RAM hoặc task vượt một phiên: báo Minh và trình phương án trước, không tăng giới hạn âm thầm.

Đại diện chi phí phải xét T/d và quy mô span/operation như bước 4. Hoàn tất phần lựa chọn và ghi WHY trước đêm chạy code/pilot; phần code/fixture độc lập được chuẩn bị theo hợp đồng đã chốt ở bước 3. Thời gian chờ duyệt không nằm trong 3–6 giờ công và không được coi là đã giải quyết khi Minh chưa trả lời. Chưa quyết tách task; nếu dự kiến không vừa một phiên, trình phương án tách trước triển khai. Chi phí BOCPD sau giảm cột vẫn OPEN; pilot có thể chỉ cho timeout/giới hạn dưới, khi đó chưa đủ căn cứ xếp T-025 chạy qua đêm. Q-72 cho BOCPD ở T-025 chạy EC2 qua đêm tối đa 20 giờ; do-chi-phi.md chiếu theo trần này. Pilot T-022 vẫn trên laptop.

## Rủi ro và điều chưa chắc

Phép chiếu BOCPD giảm cột còn OPEN; chế độ (b) bị giới hạn bởi snapshot và preprocessing; schema cố định có thể mất tín hiệu; full-score/mapping đổi nghĩa độ đo. Chất lượng giao thức có thể chưa đủ dùng ở Nezha/Eadro dù pilot RE2 đạt; các task đó vẫn phải kiểm đầu vào. Dữ liệu thiếu root signal không được gọi là bằng chứng service vô can.
