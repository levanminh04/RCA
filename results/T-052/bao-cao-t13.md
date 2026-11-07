# T-052 — T13 dev và hồ sơ G3(a)

## 1. Tự đánh giá và đối chiếu yêu cầu

Đã triển khai phần được Minh cho phép sau tự soát. Codex là người làm; Claude là người phản biện chính thức. SPEC và mục cuối LOG đã được đọc ở lượt trước khi nhận đề bài; lượt này không phải đánh giá mù. Nhận xét ban đầu dựng lại từ DT18/cô, MRP, quyết định/lý do/bài học, code và kết quả nguồn; sau đó mới đọc lại SPEC và các phản biện/phản hồi.

Nguồn yêu cầu còn cần: RQ3b về hạng, RQ3d về phép dùng quan hệ, mô tả vùng RQ3c và hồ sơ khóa phép kiểm độc lập. RQ3a/(b) hoãn; P/R/F1 vùng cần nhãn độc lập P10, LLM ở P8, áp dụng FlashTicket ở P9/P10. Không coi task dev hoàn tất là đã trả lời các phần ấy.

Nhận xét trước SPEC: phải dùng lại KB/baseline/T12 có hash đúng; kiểm C-a native và cấu hình hiệu lực; giữ các ca bất lợi; báo theo bộ/loại lỗi/ô/vị trí/ca; khóa A4/tập ca/U/nhãn/máy trước test. Dev đã chọn lặp, C/VC×E5 và nguồn tĩnh chưa nối revision, nên chưa thể khẳng định lợi ích độc lập hoặc cơ chế vật lý. LOG Phiên 5 ghi thứ tự tiếp nhận và quyền nguyên văn.

SPEC hiện hành bao phủ các việc này. Giữ nền, ma trận, A4, cohort và phạm vi kết luận. Không có sửa nhỏ SPEC. Phần thiếu ở lúc bắt đầu là công cụ/parity/chấm/fixture/hồ sơ, đã được triển khai dưới quyền có điều kiện; không đổi nghĩa khoa học để đóng checklist. Phần thừa đã tránh: không chạy lại KB, K, toàn baseline hoặc toàn native chỉ để mang mã T-052; không mở lại task cũ hay thêm VC×E5, PageRank đảo, log–span.

## 2. Công việc đã chạy và tính đúng

Đã kiểm lại 29 đầu vào hồ sơ, 13 manifest upstream và 5 nguồn G1; bốn đầu ra bản sửa 003 khớp. Hash nguồn lịch sử và nguồn hiện hành tách riêng. Hai file src đã sửa ở phiên trước được kiểm lineage theo manifest 003; bản Git của chuoi.py cần biểu diễn CRLF để khớp hash nguồn cũ. Không thay manifest nguồn để bỏ qua lệch.

EC2 pilot-002: 15/15 so sánh native trên 5 cửa sổ TT thật/giả và OB, đúng nguồn cũ cũng chạy EC2, khớp mẫu đầu vào, cờ, tập, tầng, khóa, hòa/hạng, verdict/trạng thái và trường bản ghi ở ba worlds. Khác biệt chủ ý: C-a không dựng E7; C-d3 tách. Biên nhận: `runs/trien-khai-001/ec2-pilot-002/received/output/summary.json`. Đã kiểm byte/hash từng file nhận từ EC2.

Đã chiếu/kiểm 82 cửa sổ, tạo 492 bản ghi gọn sau seal; 328 đối chiếu compact KB khớp. Chỉ sau đó evaluator dùng nhãn dev. Đã băm và chấm lại 372 bản ghi baseline, đủ sáu phương pháp; chỉ số khớp nguồn. C-c/C-g được kiểm lại blocks ở 52 ca trên graph cuối và phiếu/hạng gốc, không chỉ chép số tổng. Nguồn: `prepared-seal.json`, `bang-doc-lap-summary.json`, `score-all-summary.json` trong cùng runs.

Local pilot TT: 6/6 baseline giữ trạng thái và thứ tự nhóm hòa so nguồn; TORAI seed0 dùng đúng Python3.8. Worker TORAI mới khớp nguyên đầu ra raw của tuyến cũ trên cùng CSV. OB local: M1/T12 khớp hạng ở ba worlds; đủ sáu tuyến baseline, CIRCA/TORAI vẫn UNSUPPORTED theo giao thức. Đây là các lát cắt dev để kiểm máy, không là cận thời gian cho mọi ca test/ba seed.

16 fixture A4/giao thức đạt, gồm đúng biên, suy biến, chuyển mức, đảo dấu có ô0, seed lẫn, hòa/lỗi, bootstrap ghép ô khác cỡ, Rerank N/A và O=0. 21 kiểm điểm vào P7 đạt trên dữ liệu giả: quyền/cohort/path/hash/nhãn, đổi mã mờ không đổi method output, M1 thật, sáu tuyến baseline bằng spies, ghép nhãn chỉ sau seal. Spies kiểm luồng, không thay kiểm khoa học baseline. Worker C-d3 thật, lỗi, timeout và JSON hỏng đều giữ hash hạng chính.

## 3. Kết quả mô tả trên dev

MRR tại P; các số ở `ket-qua-dev.json#/worlds/P/<dataset>/summary/<vế>`. Sáu baseline giữ đúng variant P3; TORAI trung bình seed trong ca. S_lo/S_hi lưu riêng, không giả rằng C-d có đủ ba worlds.

| Vế | TT, 30 ca | OB, 22 ca |
|---|---:|---:|
| M1 | 0.927778 | 0.872727 |
| bo-E1 | 0.858120 | 0.872727 |
| bo-E2 | 0.966667 | 0.720561 |
| bo-E5 | 0.944444 | 0.806061 |
| C-a0 | 0.983333 | 0.661883 |
| C-a1 | 0.983333 | 0.631167 |
| C-d1 | 0.698927 | 0.697727 |
| C-d2 | 0.916667 | 0.899242 |
| C-d3 | 0.000000 | 0.000000 |
| C-c | 0.883333 | 0.529780 |
| C-g | 0.754861 | 0.533430 |
| T12-on | 0.927778 | 0.872727 |
| baro | 0.768187 | 0.527002 |
| simplerca | 0.891111 | 0.537542 |
| microrank_full | 0.256513 | 0.170139 |
| tracerca | 0.756481 | 0.329654 |
| circa_ols_da | 0.640573 | UNSUPPORTED 22/22 |
| torai_B | 0.916667 | UNSUPPORTED 22/22 |

C-a0 là ablation chuỗi đã chọn, không dùng E1/E2/E5; C-a1 vẫn dùng E1 và quan hệ cha–con. C-d2 dùng khởi phát/khóa raw từ bằng chứng M1 đã có E1/E2. C-g chỉ đo thêm E6b sau SimpleRCA; C-c là RRF k=60. Không có đối chứng graph ngẫu nhiên. Không gọi mọi vế này là không đồ thị, hoặc suy lợi ích do topology thật.

M1−C-a0: TT 1 tăng/25 hòa/4 giảm, chênh −0,055556; OB 9 tăng/11 hòa/2 giảm, chênh +0,210844. M1−C-d2: TT 1/28/1; OB 3/17/2, chênh OB −0,026515. Nguồn từng ca: `#/worlds/P/<dataset>/pairs_M1_minus/<vế>`. Vì vậy dev chưa hỗ trợ phát biểu M1 hơn chung nhánh bỏ quan hệ hoặc quy tắc đơn giản. T13 không chọn lại nền theo bảng này.

MicroRank/TraceRCA TT giữ 4 ERROR trong mẫu số; CIRCA/TORAI OB giữ 22 UNSUPPORTED. Không diễn giải 0 của UNSUPPORTED thành hiệu quả thuật toán. SimpleRCA M4 trên OB giữ giới hạn tái lập đã chấp nhận ở T-042; hơn M4 không đồng nghĩa hơn bản đạt số tác giả.

Bảng `do-do-bo-sung.json#/expected_ties` bổ sung Retrieval@5/10 và Rerank@1 theo cùng định nghĩa evaluator; mẫu số bằng 0 ghi null. `#/baseline_native_order` giữ AC@k/Avg@5 nguyên gốc và seed của baseline, tách khỏi kỳ vọng hòa. M1 có một root mỗi ca nên kỳ vọng AC@k bằng Hit@k; không dựng thứ tự native tùy ý từ khối hòa.

Bootstrap/cặp và bảng theo fault/cell/vị trí N p75/p90/ca nằm trong `ket-qua-dev.json`. Vị trí N dựng từ K-R0 giữ span bọc có n_N>0 và G_N; không dùng A hoặc root để chọn nút. Mọi đầu cạnh thuộc tập nút ở 52 ca. Nhóm lịch sử từ nguồn G1 vẫn giữ riêng trong bản độc lập; không đồng nhất vắng quan sát với cô lập vật lý.

## 4. Chuỗi cơ chế và giải thích cạnh tranh

Đã đọc code E1/E2/E5/xếp hạng và frame nguồn sau kiểm hash. `mechanism_traces` trong kết quả lưu mọi ca đổi RR của các cặp chính, kênh root/tầng/top blocks và ca đối chiếu cùng root/fault nếu có. Ghép cùng root/fault không có nghĩa mọi điều kiện quan sát giống nhau.

E2: ở dev-a915aa2424, kênh exclusive của root giữ 3881,562205; E2-C gán cạnh travel→train điểm 4834,194981 cho train, giữ tầng1, khóa ưu tiên max làm RR root 1→1/3. Ca đúng đối chiếu dev-a5cabe5fa7 có root 5256,929712 vẫn vượt train 4506,080790 nên RR vẫn1. Đây là đường đầu vào kênh→gán cạnh→tầng/khóa→hạng, không chứng minh ai gây lỗi vật lý. Frame chính xác: `results/T-053/phan-tich-cap-003.json#/frames/K-E1+E5|dev-a915aa2424/new` và cặp `K-E1+E2+E5`, cùng hai frame của ca đối chiếu.

E5: ở dev-20acb4402d, bỏ latency-90 của root điểm 4209,481569 để lại exclusive 1132,987919; auth còn 1774,479167, root vẫn tầng1 nhưng RR 1→1/2. Frame cùng file, cặp `K-E1+E2`/`K-E1+E2+E5`. Không có ca đúng trùng đầy đủ chữ ký trong phân tích nguồn; giữ giới hạn, không gọi E5 sai vật lý ở mọi ca hoặc quy cho collector. Điểm đối thủ, tín hiệu không quan sát, tải và giả định phân lớp vẫn là các giải thích cần phân xử bằng dữ liệu phù hợp.

E1/E2 dùng span cấp request; graph gộp không đủ tái tạo duration/membership. E5 dùng cạnh và SCC, nhưng tự sinh theo luật không đồng nghĩa nguyên nhân vật lý. E6a sắp tầng/khóa, E7 dùng cạnh để tạo vùng. Kết quả xấu/tốt của C-d2 là phép so cấu hình cụ thể; không cô lập riêng mọi cơ chế.

## 5. Vùng, C-e và thống kê

Nguồn `vung-ce-va-vi-tri-001.json#/summary`: TT hai cách vùng chứa root kỳ vọng 86,67%/96,67%, rộng 2,9/10,7; OB 81,82%/95,45%, rộng 1,590909/2,909091. Tỷ lệ theo O tính từng ca trước gộp; vùng hợp báo riêng. T12 giữ RR nhưng có thể làm rộng vùng TT; không dùng RR bất biến để kết luận không ảnh hưởng.

C-e: 30 cửa sổ, 16 thực thể từng đứng đầu, top hai mỗi5/30, V0 CAUSE_FOUND 30/30, N1 trung bình14,7. RR root tương lai khoảng0,078727. `#/ce_summary` và `#/ce` giữ top mass/returned/O/coverage/root có mặt; không có nền lành độc lập, không dùng RR này chứng minh không thiên lệch hoặc hiệu chuẩn V0.

A4 được cài theo Q-246, không đổi tiêu chí. Ví dụ dev TT có CI M1−TORAI B [−0,066667; 0,122222], chưa đạt công thức E-04 ở lát cắt dev; OB đảo dấu Hit@5 có 3 ô hữu hiệu, p=1/8. Nguồn `ket-qua-dev-doc-lap-001.json#/A4_dev_illustration` và `#/OB_sign_dev_illustration`. Đây là kiểm công cụ/mô tả dev, không phải kết quả P7. Bootstrap vẫn có nguy cơ undercoverage; đảo dấu chỉ có hiệu lực theo H0 đã khai, không được nâng thành kết luận vô điều kiện.

## 6. Quyền, lỗi giữ lại và chi phí

Không sửa SPEC, src hoặc sổ quyết định/lý do ở lượt này. Chỉ thêm công cụ/kết quả/hồ sơ T-052, nối LOG và đổi đúng dòng T-052 STATE. Không mở test/RE3, không khởi động/cấp máy, không đổi ACL khóa, không commit/push. IP mới do Minh cấp; khóa key2.pem hoạt động.

Giữ đủ lượt hỏng: local001 gộp params hai lần; local002 lưu trace có set; local003 khác số thực khoảng2,8e−16 nhưng cờ/tầng/nhóm hạng giữ. Không nới comparator: đổi sang EC2 cùng nguồn rồi đạt so chính xác. EC2-001 thiếu module observer cham và SSH điều khiển hết giờ; đã kiểm worker qua kết nối mới, không chạy trùng. Lượt002 có PID riêng và biên nhận nhận/hash. Một lượt chấm dừng do lỗi bookkeeping evaluator trước ghi kết quả, đã sửa/giữ bản trước. OB-local001 thiếu thư mục log trước baseline, thời gian native chưa lưu đủ; không dùng thời gian ấy. Hash snapshot được bổ sung sau khi lượt ấy đã bắt đầu đọc, khớp; không gọi đó là tiền kiểm. OB-local002 kiểm trước đúng nguồn và ghi thời gian từng bước.

EC2 native parity: 266.278 giây; local sáu baseline TT: 82.536 giây; OB local toàn lát cắt: 63.091 giây. Pha chiếu 82 cửa sổ và chấm hợp nhất có thời gian trong prepared-seal/score-all-summary. Phần làm công cụ/đọc nguồn/viết hồ sơ tách khỏi thời gian máy. Dự toán SPEC 5–7 giờ là dự toán công cả gói, không dùng để hợp thức hóa chạy quá60 phút máy. Tổng thời gian máy có biên nhận và phần hỏng/bounds trong manifest thực thi; không khôi phục mốc chưa ghi.

## 7. Phần đã đạt, phần còn mở và bước tiếp

Đã có T13 dev đủ baseline/ablation/đối chứng, vùng/C-e, parity cần để tái dùng, công cụ thống kê và fixture điểm vào P7. Nghiên cứu trả lời các phép so trên dev và một số cơ chế tính toán, chưa chứng minh lợi ích độc lập, cơ chế vật lý chung, hiệu chuẩn verdict hay độ đúng vùng ảnh hưởng.

Hồ sơ G3 ở `ho-so-g3.md`; giao thức và cohort ở hai JSON kèm theo. Chưa xin coi đã khóa G3. Minh còn quyết nghiệm thu/phản biện và bản khóa; SPEC P7 phải chốt ma trận materialize, vị trí private map, worker/ngân sách toàn đợt và quyền mở. RE3 cần hợp đồng nguồn/adapter/U/alias từ metadata được phép trước lượt mở cuối; chưa tải. VC×E5, hướng PageRank đảo, nối log–span, A0 và revision snapshot giữ đúng giới hạn, không tự thêm thử.

Đề xuất tiếp tục một lượt Claude soát đầu ra mới trước quyết G3. Prompt nguyên văn theo mẫu nằm cuối LOG; không tự gửi và không chờ Claude để hoàn thành các phần đã được Minh giao. Commit chỉ là đề xuất khi Minh yêu cầu: `feat(T-052): hoàn tất T13 dev và hồ sơ chuẩn bị G3(a)`.
