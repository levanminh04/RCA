# Kế hoạch P3–P4 tới G2

Ngày lập: 05/10/2026. Người soạn tài liệu: Codex. Repo: D:/RCA-flashticket.

## 1. Phạm vi và trạng thái

**USER_CONFIRMED:** Minh đồng ý lưu plan bản 3 và yêu cầu ghi việc song song, thời gian, EC2, dung lượng; tạo SPEC đợt 1 và prompt cho Codex phản biện.

**DECIDED:** giữ Q-61–Q-70: thứ tự dataset, phương pháp hai tầng, chia Eadro theo phiên, cửa sổ Q-64 và mốc G2 15–18/10/2026. Q-72: cho chạy BOCPD qua đêm trên EC2 ở T-025, tối đa 20 giờ, ngoại lệ Q-40. Q-79 (06/10/2026) bỏ trần 20 giờ này; Minh theo dõi và dừng khi thấy quá lâu. Không đổi cổng, không mở test.

**CANDIDATE:** lịch, các khoảng chi phí dưới đây, phân công task tương lai và cấu hình còn mở. Hai SPEC đợt 1 được soạn để phản biện và Minh duyệt; việc cho soạn tài liệu không phải duyệt chạy task, chạy qua đêm hay bật EC2.

**OPEN:** chi phí BOCPD sau giảm cột; RAM đỉnh của bản MicroRank sửa; cấu hình giao thức; danh sách phiên dev/test Eadro; phạm vi Eadro sau phép kiểm. Người quyết các lựa chọn này là Minh, người làm cung cấp bằng chứng.

Nguồn: [DECISIONS](DECISIONS.md), [MRP P3/P4 và G2](MRP.md), [gói G1](../results/T-021/goi-g1.md).

## 2. Task, phụ thuộc và công việc song song

Mã T-028/T-029 thay cách ghi T-028a/b để mỗi task có một mã số riêng; nội dung vẫn là hai phần P4. Các mã sau T-023 là dự kiến, chưa tạo SPEC.

| Task | Việc và đầu ra chính | Người làm / phản biện dự kiến | Phụ thuộc thực sự |
|---|---|---|---|
| T-022 | Giao thức P3, adapter RE2, bộ chấm, bảng dùng lại bằng chứng, đề xuất WHY, kiểm rò nhãn và đo pilot | Claude / Codex | SPEC và các lựa chọn cần thiết được Minh duyệt |
| T-023 | Kiểm điều kiện Eadro: chia phiên trước đọc số đo, ghép trace–phiên–mốc, nguồn no-fault; trình nhánh sử dụng | Codex / Claude | SPEC; danh sách phiên được phép đọc được Minh duyệt. Không cần chờ T-022 |
| T-024 | Sáu ranker tầng 1 trên 30 dev RE2-TT, chế độ (a); kết quả từng ca và kiểm bổ sung | Claude / Codex | T-022 hoàn tất, WHY có hiệu lực và SPEC T-024 được duyệt |
| T-025 | N-Sigma/BOCPD; bảng phát hiện riêng và RCA chế độ (b) cho các phương pháp đủ điều kiện | Codex / Claude | T-022 hoàn tất; khóa detector, cửa sổ do detector tạo và cách chấm trước benchmark |
| T-026 | Adapter và benchmark dev Nezha-OB, chỉ ranking biết trước cửa sổ | Codex / Claude | Chuẩn bị adapter sau T-022; benchmark sau **cả T-024 và T-025 hoàn tất** |
| T-027 | Eadro dev trong phạm vi Minh chọn từ T-023 | Codex / Claude | T-023 và T-026 hoàn tất. Đạt: chạy các phương pháp đủ đầu vào. Không đạt/OPEN: Minh chọn metric/log hoặc bỏ |
| T-028 | P4 xếp hạng: cơ chế ca sai, theo ca/ô/điều kiện, các giải thích khả thi khác | Claude / Codex | Kết quả ranking của các dataset được chấp nhận |
| T-029 | P4 phát hiện và tổng hợp trình G2 | Claude / Codex | T-025, phần phát hiện Eadro nếu dùng, và T-028 |

### Song song được ở cấp công việc

- T-022 và T-023: đọc nguồn, viết tài liệu, viết mã trong phạm vi khác nhau.
- Trong khi batch T-024/T-025 chạy: chuẩn bị adapter Nezha, đọc hồ sơ, chuẩn bị bảng P4 từ kết quả đã hợp lệ. Chưa benchmark Nezha.
- T-024 và T-025: có thể chuẩn bị mã/kiểm rẻ song song. Chạy hai batch nặng cùng máy chỉ là CANDIDATE, phải dựa trên số đo RAM/CPU ở T-022; hiện không xếp hai lượt nặng đồng thời.
- Phần tổng hợp P4 có thể bắt đầu từ kết quả đã đủ, nhưng kết luận cuối và G2 chờ tất cả phần đã chọn.
- Đo thời gian/RAM pilot trên máy không có công việc nặng khác. Không streaming archive Eadro, giải nén hoặc chạy ranker khác trong lúc đo.
- Không để hai task cùng sửa một file trong src/p3/. Giao thức chung do T-022 hoàn thiện trước; SPEC sau phải ghi đúng file adapter cần thêm.
- Phân công hai agent không tự cho phép hơn hai subagent hoặc thêm worker máy. Giữ luật chi phí trong AGENTS.

### Duyệt theo phụ thuộc

Đợt đầu: SPEC T-022/T-023. Đợt thực nghiệm: viết SPEC T-024–T-027 theo giao thức, số đo và nhánh Eadro đã được Minh quyết. Phần P4: duyệt khi biết khối lượng và bằng chứng cần phân tích. Đây là cách tổ chức các task hiện có, không thêm cổng.

## 3. Ước lượng thời gian

**Toàn bộ khoảng dưới đây là CANDIDATE, chưa kiểm.** “Công agent” là thời gian soạn/cài/kiểm/diễn giải, không phải giờ CPU; không gồm chờ Minh, phản biện và sửa. “Thời gian máy” chỉ là dự toán xếp lượt, không cộng thêm vào công agent khi hai phần chồng nhau.

| Task | Công agent | Thời gian máy dự trù | RAM tiến trình dự trù | Đĩa tăng dự phòng |
|---|---:|---:|---:|---:|
| T-022 | 3–6 giờ | 30–90 phút cộng các lượt nhẹ; mỗi lượt pilot dưới 1 giờ | 1–3 GB; peak bản sửa OPEN | 0,1–0,5 GB |
| T-023 | 2–4 giờ | 10–30 phút nếu streaming | 0,5–2 GB, chưa đo | 0,1–0,5 GB |
| T-024 | 2–4 giờ | 0,5–2 giờ, gồm I/O và seed | 1–3 GB, chưa đo đầy đủ | 0,2–1 GB |
| T-025 | 3–5 giờ | **OPEN: chưa đủ số đo để dự báo**; đo detector đúng giao thức ở T-022, rồi cộng RCA theo số episode báo động | detector cũ dưới 0,3 GB RSS; reranker dự trù 1–3 GB | 0,2–1 GB |
| T-026 | 3–5 giờ | 0,5–3 giờ, chưa kiểm | 0,5–3 GB, chưa đo | 0,5–2 GB |
| T-027 | 2–4 giờ nếu dùng | 0,5–3 giờ, chưa kiểm | 0,5–3 GB, chưa đo | 0,5–2 GB |
| T-028 | 3–5 giờ | 10–45 phút tổng hợp/kiểm rẻ | 0,5–2 GB, chưa đo | 0,1–0,3 GB |
| T-029 | 2–4 giờ | 10–45 phút tổng hợp/kiểm rẻ | 0,5–2 GB, chưa đo | 0,1–0,3 GB |

Tổng công agent dự trù: 20–37 giờ nếu dùng Eadro; 18–33 giờ nếu Minh chọn bỏ nhánh thực nghiệm Eadro. Đây không phải thời gian lịch: có phần song song, nhưng cũng có thời gian chờ duyệt và sửa. Mục tiêu mỗi task một phiên; nếu tự soát cho thấy không vừa, trình tách trước khi thực hiện.

Giả định: dùng lại lõi và môi trường đã có; không chạy PC/GDN tầng 2; một ca/phiên một lúc; không lưu lại toàn bộ telemetry cho mỗi lượt; không có sửa phương pháp mới. Khoảng sẽ sai nếu phải dựng lại môi trường, clock Eadro không xác minh được, scorer thay đổi, báo động quá nhiều hoặc snapshot trung gian lớn. Chưa kiểm vì lượt này chỉ soạn tài liệu, không chạy phương pháp hay mở dữ liệu đo mới.

### Bằng chứng làm căn cứ, không phải benchmark P3

| Nguồn đã có | Điều đã đo |
|---|---|
| results/T-005/do-kha-thi.md, bảng 2a/2b | MicroRank bản cũ: tổng 106/242 s, RSS 1.202/2.342 MB; BOCPD cũ 600 điểm mất 1.440 s, full 1.441 điểm vượt 1 giờ; N-Sigma mất 59 s |
| results/T-015/runs/tt-local/auth/run-ledger.csv | MicroRank sửa: một ca trên EC2, tổng tiến trình 14,653 s; chưa phải đo peak RAM, chưa phủ 30 ca |
| results/T-016/quy-mo-tt.md, mục 5 | TORAI sửa trên 30 dev: tổng khoảng 66 s trên EC2 cho lượt được dẫn; không tự áp sang máy/cấu hình mới |
| results/T-017/runs/run-dev-004/summary.json; kiem-dung-dan.md | SimpleRCA đã chạy 30 dev; thời gian trên laptop có công việc khác, không dùng làm benchmark chính thức |
| results/T-014/ho-so-circa-kien-truc.md | Ví dụ scoring và ghi snapshot khoảng 4,063 s; chưa gồm toàn bộ xây graph và chưa chốt scorer P3 |
| results/T-009/the-dataset.md, mục chi phí | Streaming hai archive từng mất 168,156 s; không thay cho thời gian kiểm alignment hay chạy RCA |

Q-40: tối đa **3 giờ chờ thực tế cho toàn ca một dataset/phương pháp**, chạy tuần tự, laptop hoặc EC2. BOCPD cũ 24 phút/ca chiếu 30 ca là khoảng 12 giờ; đó là cảnh báo, **không phải lịch được duyệt**. Giảm cột theo reproduce_bocpd ở Q-67 phải đo lại. Không chia thành nhiều lượt nhỏ để vượt trần tổng.

Mốc 12 giờ ứng với input 600 điểm cắt quanh mốc tiêm trong lượt tái lập cũ, không phải dự báo chế độ (b). Nếu giữ số chiều, máy và tải, ngoại suy theo số lần tính predictive từ 600 lên 1.441 điểm cho khoảng 69 giờ/30 ca; **chưa kiểm**, không phải số đã đo hay dự báo cấu hình giảm cột. Nguồn: results/T-013/trung-gian/chi-phi-va-sentinel.json và ho-so-bocpd.md §9. Số đo full 1.441 điểm hiện chỉ là không hoàn tất trong một giờ ở T-005.

Q-67 chỉ chọn tập cột, không cho detector cắt theo mốc tiêm. Trước pilot phải chốt biên chuỗi, độ dài/bước đoạn và quy tắc khởi động lại hoặc giữ trạng thái. Có thể đề xuất full recording hoặc các đoạn theo quy tắc độc lập lỗi; không mặc định full 1.441 điểm là lựa chọn duy nhất, không chia đoạn chỉ để làm đẹp chi phí. Snapshot RE2 vẫn có giới hạn biên được thu quanh sự cố. Nếu pilot timeout, chỉ báo giới hạn dưới và giữ dự báo OPEN; không suy thời gian hoàn tất từ timeout.

Chi phí T-025 cần tính bằng: chi phí detector + tổng số episode báo động nhân chi phí ranker đủ điều kiện. T-022 khóa cách gộp episode trước khi chấm; không chọn sau khi nhìn accuracy.

## 4. Đêm nào có thể chạy gì?

Đây là phương án để Minh duyệt sau SPEC và số đo, không phải lệnh khởi chạy.

| Giai đoạn | Việc hợp lý | Phần phải có trước |
|---|---|---|
| Trước đêm chạy | T-022 trình lựa chọn và nháp WHY; T-023 trình chia phiên/allowlist. Phần code và fixture độc lập có thể chuẩn bị song song theo hợp đồng đã chốt | Minh duyệt cấu hình và cho ghi WHY; duyệt danh sách phiên trước telemetry T-023. Chưa có các đầu vào này thì chỉ hoàn tất phần chuẩn bị |
| Đêm chuẩn bị | T-022 cài phần đã chốt và đo pilot; T-023 kiểm số đo trong allowlist | Các điểm chờ ở hàng trên đã giải quyết; không parsing nặng khi T-022 đo chi phí |
| Đêm batch RE2 | T-024 chạy một batch tuần tự, dự trù 0,5–2 giờ; agent có thể làm phần nhẹ khác | T-022 xong, kiểm bổ sung và ước lượng theo toàn 30 ca |
| Cùng đêm hoặc đêm kế tiếp | T-025 chạy sau T-024; BOCPD được chạy trên EC2 qua đêm, không trần 20 giờ (Q-79 thay Q-72), phần còn lại trong ngân sách đã trình | Số đo giảm cột, số episode dự trù, phạm vi chế độ (b), Minh duyệt lượt trên 1 giờ nếu có |
| Đêm mở rộng | Nezha sau cả T-024/T-025; Eadro sau Nezha và nhánh được Minh chọn | Adapter đã kiểm, chỉ dev, đủ đầu vào và ngân sách từng phương pháp |
| Phiên tổng hợp | P4 và trình G2 | Có kết quả, bằng chứng cơ chế; không chỉ bảng điểm trung bình |

Không có cơ sở hứa một đêm hoàn tất G2. Đêm đầu có các lựa chọn đang OPEN nên agent phải báo khi cần Minh quyết, không tự đoán để chạy tiếp. Các batch phải ghi tiến độ, thời gian từng bước, giữ lượt hỏng và có thể tiếp nhận qua LOG theo AGENTS; không tự đổi cấu hình giữa lượt.

Hiện chưa có task được chứng minh phải chạy suốt đêm. T-024 và T-025 có thể giao chạy lúc Minh ngủ để giảm thời gian ngồi chờ, sau khi đủ điều kiện; không có nghĩa batch cần dài tám giờ. T-025 chưa có lịch cho đến khi pilot đủ căn cứ. Riêng BOCPD ở T-025, Q-72 cho chạy qua đêm trên EC2 tối đa 20 giờ; Q-79 (06/10/2026) bỏ trần này: Minh theo dõi qua SSH và dừng khi thấy quá lâu; vẫn ghi tiến độ từng ca, giữ lượt hỏng. Phương pháp khác vượt Q-40 vẫn phải trình trước. Giữ mã task hiện tại; chưa quyết tách T-022 thành hai task. Việc duyệt giữa chừng là phụ thuộc lịch, không tự chứng minh task chắc chắn vượt một phiên; nếu dự kiến vượt một phiên thì đề xuất tách trước triển khai theo AGENTS §5a.

Mốc G2 15–18/10/2026 giữ theo Q-70. Sau pilot T-022 mới cập nhật dự báo lịch. Hiện chưa đủ bằng chứng kết luận chắc chắn kịp hoặc chắc chắn trễ.

## 5. Có cần EC2 không?

**Chưa có bằng chứng EC2 bắt buộc cho tầng 1.** T-022 và T-023 ưu tiên laptop; tầng 1 không cần GPU. T-024/T-025 bắt đầu bằng một worker nặng nếu số đo cho thấy RAM đủ.

**DECIDED:** Q-67 ghi “Không chạy EC2 qua đêm lúc này.” Q-72 (05/10/2026) thay phần này cho riêng BOCPD ở T-025: được chạy qua đêm trên EC2, tối đa 20 giờ, đầu vào không chọn theo mốc tiêm, ghi tiến độ từng ca, giữ lượt hỏng. Các việc khác vẫn theo Q-67. Q-79 (06/10/2026): bỏ trần 20 giờ cho BOCPD ở T-025; cho T-031 chạy TORAI B, A trên EC2. Lập phương án cloud không phải quyền bật máy, SSH, chuyển dữ liệu hay chạy EC2. Nếu cần thay quyết định này, trình Minh trước.

EC2 là CANDIDATE khi laptop thiếu RAM ngay cả với một worker, hoặc việc tách batch khỏi laptop có lợi sau khi đo. Chuyển sang EC2 không mặc nhiên giảm thời gian BOCPD và không bỏ trần Q-40. Cấu hình tham khảo để trình: CPU, không GPU; 8 GiB RAM cho một worker đã đo vừa, 16 GiB nếu cần dư địa; giữ 10–20 GB đĩa trống cho runtime/dev/kết quả. Chưa chọn loại máy hay vùng. Giá/giờ và tình trạng instance hiện tại OPEN, chưa tra hoặc kết nối máy; phải kiểm và trình trước sử dụng.

Snapshot laptop chỉ đọc lúc 18:19:50 ngày 05/10/2026, múi giờ +07:
- D còn 47.820.439.552 byte, khoảng 47,82 GB / 44,54 GiB.
- RAM tổng 16.454.388 KiB, trống 2.872.100 KiB, khoảng 2,74 GiB.
- Nguồn đo: Get-Volume -DriveLetter D và Get-CimInstance Win32_OperatingSystem. Đây là snapshot, không dự báo RAM trống qua đêm. Không suy lượng RAM này là đủ cho hai worker.

## 6. Dung lượng

GB ở đây là 10^9 byte; GiB là 2^30 byte. Dung lượng nguồn không phải RAM khi đọc vào bảng.

| Nguồn đã có | Dung lượng | Nguồn kết quả |
|---|---:|---|
| 30 dev RE2-TT | 656.358.942 byte, khoảng 0,656 GB | results/T-002/local-inspection/run-002/case-summary.csv; summary.json |
| Nezha-OB nguồn CSV | 2.677.369.464 byte, khoảng 2,677 GB | results/T-008/the-dataset.md |
| Eadro-TT ZIP | 48.923.113 byte, khoảng 49 MB | results/T-009/runs/download-001/manifest.json |
| Eadro-TT toàn representation logical | 1.477.635.868 byte; bỏ bản nested trùng đã xác minh còn 880.924.139 byte | results/T-009/runs/inspect-004/logical-member-sizes.json |

**Tải telemetry mới dự kiến: 0 byte.** Không cần tải RE3-OB trước G3, không tải GAIA lúc này. Nếu môi trường phải dựng lại, dung lượng gói phần mềm còn OPEN và phải trình riêng; không gọi nó là tải dataset.

Đĩa tăng dự phòng cho P3/P4: **5–10 GB, chưa kiểm**, gồm kết quả, cache, snapshot cần tái lập và lượt hỏng. Không phải cận trên. Streaming archive Eadro, không giải nén toàn bộ hoặc nhân bản source theo run. Không xóa lượt hỏng để lấy chỗ.

Nếu tương lai dùng EC2: source liên quan tối đa trước lọc khoảng 3,383 GB (dev RE2 + toàn Nezha-OB + ZIP TT), **không được chuyển mặc định toàn nguồn** vì chứa phần test. Transfer thực phải lấy allowlist dev; Eadro chỉ member được phép. Cộng runtime/kết quả theo SPEC đã duyệt; không chép khóa truy cập vào repo.

## 7. Điều cần chốt trong hai SPEC đầu

### T-022

Áp dụng cửa sổ Q-64, không mở lại độ dài. Đề xuất và khóa trước benchmark: scorer/coverage CIRCA; điểm đầy đủ và mapping MicroRank; finite/tie/NO_EVIDENCE TraceRCA; quy tắc bộ cột và cột thiếu; ứng viên/chấm ca lỗi; detector/warm-up/episode/matching và đầu vào chế độ (b). Nháp WHY trong results không thay mục WHY đã có hiệu lực.

T-022 phải giao rõ nháp WHY cho cả Q-64, Q-65, Q-66, Q-67 đã quyết và các lựa chọn còn mở. Nháp đề xuất bổ sung ghi chú ở WHY-19 rằng trạng thái cửa sổ đã được Q-64 thay thế; giữ bối cảnh lịch sử. Ghi vào docs/WHY.md vẫn cần Minh duyệt nội dung/phạm vi riêng. Chọn ca pilot theo yếu tố chi phí của từng phương pháp: số điểm và số cột thực của detector; số span/operation với ranker trace, không chỉ tổng byte telemetry và không theo accuracy.

Chế độ (b) có hai việc khác nhau: tìm mốc không dùng nhãn và RCA từ mốc đó. Recording RE2 vẫn được thu quanh sự cố; BOCPD nguyên bản có xử lý cả window dùng tương lai. T-022 phải trình cách diễn giải hồi cứu hoặc thay preprocessing nhân quả nếu cần; không tự gọi kết quả trên snapshot là giám sát online.

### T-023

**FACT từ metadata đã có:** bảng chia theo ô T-021 trộn dev/test trong cả 9 phiên fault Eadro-TT. Q-63 đã chọn chia theo phiên, nhưng danh sách phiên cụ thể chưa có. Mỗi root của TT thuộc một phiên; đổi sang chia phiên làm root ở hai phía khác nhau và cần khai báo.

T-023 lập đề xuất chia phiên chỉ từ nhãn/metadata, trình Minh duyệt allowlist trước mọi đọc mới dữ liệu đo. Hai phiên TT có nhãn faults=[] là ứng viên dữ liệu bình thường; tên no-fault không chứng minh sạch. Phiên không có nhãn không tự được đưa vào nền.

Nguồn: results/T-009/runs/run-001/labels.json, normal_intervals.json; results/T-021/chia-theo-o/A-phan-tang.csv. Không dùng bảng ô cũ để mở trọn phiên.

## 8. Đầu ra và cách trình G2

Có bảng baseline dev và kết quả từng ca, bảng phát hiện riêng, bản đồ hạn chế với số ca/tổng số và bằng chứng cơ chế. Phân biệt kiểm tái lập của bản gốc với kiểm cơ chế của bản sửa; không gọi “khớp” nếu hồ sơ ghi lệch hoặc không có mốc.

Tóm tắt bằng ba câu: phương pháp nào tốt trong điều kiện nào; thất bại ở đâu; hạn chế nào cần P5/P6 giải quyết. Hồ sơ vẫn trả lời đầy đủ **sáu câu tại MRP §7**. Minh duyệt G2; không yêu cầu đồ thị mới đã thắng hay P5/P6 đã hoàn tất.

## 9. Nhật ký lập tài liệu và đăng ký nguồn chung

Lượt này là soạn plan/SPEC, chưa mở phiên thực hiện T-022/T-023. Chỉ đọc repo, nguồn hướng dẫn, kết quả và metadata tài nguyên; không mở telemetry mới, không chạy phương pháp, không tải, không EC2, không commit/push. LOG thực hiện sẽ do người làm mở khi SPEC được Minh duyệt.

Đề xuất dòng nguồn chung, chờ Minh duyệt riêng:
“Q-71 — 05/10/2026: Minh đồng ý lưu plan P3–P4 tới G2 bản 3, tạo SPEC đợt 1 T-022/T-023 và prompt phản biện. Lịch/chi phí và các lựa chọn OPEN là dự kiến; chưa duyệt chạy task hoặc mở test; chạy qua đêm/EC2 chỉ cho BOCPD ở T-025 theo Q-72. Nguồn: yêu cầu Minh ngày 05/10/2026 và docs/PLAN-P3-G2.md.”
STATE sẽ đăng ký hai SPEC là đề xuất, chờ phản biện/duyệt; không ghi chúng đang chạy. Lượt này không tự sửa trạng thái task cũ.

Ngày 05/10/2026, Minh yêu cầu sửa theo phản hồi đối chiếu REVIEW của Claude: “ĐỒNG Ý VỚI CÁC SỬA ĐỔI TRÊN, SỬA LUÔN GIÚP TÔI”. Codex cập nhật đúng ba file: plan này, SPEC T-022 và SPEC T-023. Sửa dự báo BOCPD, giao nháp WHY cho quyết định đã chốt, hợp đồng input/state detector, chọn ca pilot theo yếu tố chi phí và các điểm chờ trước đêm chạy. Chưa quyết tách task hoặc ghi WHY chung; không đổi Q-40/Q-64/Q-67. Sự đồng ý này áp dụng sửa tài liệu, chưa khởi chạy task.

Bước tiếp theo: Minh duyệt SPEC hoàn chỉnh khi muốn triển khai; người làm trình các lựa chọn/nháp WHY của T-022 và allowlist của T-023 trước phần chạy phụ thuộc. Không tự thêm vòng phản biện vì phát sinh góp ý. Khi thực hiện T-022 người làm Claude, phản biện Codex; khi thực hiện T-023 người làm Codex, phản biện Claude. Phản biện trước triển khai của gói tài liệu không thay phân công phản biện kết quả T-023. Prompt dưới được giữ để dùng khi Minh yêu cầu.

## 10. Prompt cho Codex phản biện gói tài liệu

Minh yêu cầu một phiên Codex mới soát gói tài liệu trước triển khai. Vì bản nháp do Codex soạn, lượt này là soát lại theo yêu cầu Minh, không được coi là phản biện chéo khác agent của chính bản nháp. Phân công phản biện kết quả T-022/T-023 vẫn theo SPEC.

Prompt dùng nguyên “Prompt chung” trong docs/review-prompt.md, chỉ điền thông tin trung tính. G2 không có khối trọng tâm riêng trong mẫu. Hai SPEC hiện là đề xuất, chưa có LOG thực hiện hay kết quả khoa học; đó là trạng thái đầu vào, không phải tuyên bố đã xong.

```text
Bạn là người phản biện độc lập cho task T-022 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-022-giao-thuc-p3/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-022-giao-thuc-p3/SPEC.md, tasks/T-022-giao-thuc-p3/LOG.md, các file đầu ra: docs/PLAN-P3-G2.md, tasks/T-023-kiem-eadro/SPEC.md (hai SPEC đề xuất; LOG thực hiện và kết quả thực nghiệm chưa có),
và kết quả `git diff HEAD` nếu có.
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
