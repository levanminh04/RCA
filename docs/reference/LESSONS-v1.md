# Bài học từ RCA v1 (22/09 – 02/10/2026)

Mục đích: để mọi phiên làm việc sau không lặp lại sai lầm của v1 **và của chính đợt cải tổ 01–02/10 (mục 2b)**. Đọc file này trước khi thiết kế, chọn tham số, diễn giải kết quả hoặc thêm quy trình.

Nguồn: kết quả v1 trong `results/task-e/`, tài liệu v1 trong `docs/v1-ref/` và repo P (`docs/research-rca/`), đợt phản biện độc lập 01–02/10 (tóm tắt ở `docs/handoffs/G0-tai-lieu-nen.md`), nghiên cứu tài liệu trong `docs/research-notes/`.

## 1. Sự thật đã xác lập (không đo lại, trừ khi spec yêu cầu)

- **ST1 — Dữ liệu RE2-TT.** 90 ca = 5 service gốc × 6 loại lỗi (cpu, mem, disk, socket, delay, loss) × 3 lần lặp. Nhãn chỉ có: service gốc, loại lỗi, thời điểm tiêm lỗi. Không có nhãn vùng ảnh hưởng, operation gốc hay đường lan truyền. (`dataset-audit/TASK-B-RCAEval-audit.md` §12)
- **ST2 — Trace.** 98,45% tham chiếu span cha resolve được trên cả 90 ca (7 ca dưới 90%). Trường `duration` đầy đủ, không âm, đơn vị chưa xác minh. `statusCode` rỗng toàn bộ. Log có ở 89/90 ca. Mỗi ca trace chạm 20–27 service.
- **ST3 — Đồ thị gần như hằng số.** 30 ca dev chỉ có 2 đồ thị dịch vụ khác nhau (27 nút/55 cạnh có hướng ở 24 ca; 20 nút/20 cạnh ở 6 ca). 5 service gốc nằm ở 5 vị trí cố định: auth không có cạnh nào; route và train không gọi service nào nhưng được 3 service gọi (không phải lá); order ở giữa; travel là hub. Final60 dùng lại đúng 5 service gốc này.
- **ST4 — Chia dữ liệu.** dev30/final60 chia theo ô (service × loại lỗi), 3 lần lặp của một ô đi cùng nhau. Dev: auth(cpu, delay), order(disk, loss), route(mem, socket), train(cpu, delay), travel(disk, loss). Danh sách ca: `configs/task-f-td13-frozen-release-v2.json`.
- **ST5 — C1 trên dev30 (thiết kế TD-v1.3).** MRR: L = 0,744; O = 0,702; R = 0,678.
  - 17 ca root đã hạng 1 ở L: PPR không lật ca nào (kể cả ở bin5, bin20).
  - 4 ca HARM nặng: một service không phải root có điểm 10⁹–10¹² do sàn 1e-12; chiếm 89% tổng thiệt hại. R (đồ thị ngẫu nhiên) gây thiệt hại y như O ở các ca này.
  - 2 ca HARM nhẹ ở auth (không có cạnh). 2 ca HELP ở travel/loss.
- **ST6 — Thăm dò trên dev30 (đã nhìn cả O; sửa lại 02/10 sau khi tách theo ô).** Chỉ đổi sàn 1e-12 → 1: L = 0,766; O−L trung bình = +0,029 (PPR). Dấu của O−L trung bình đổi theo cách chuẩn hóa: đây là điều duy nhất phép thăm dò này xác lập được, tức kết luận "đồ thị làm hại" của v1 là do cách chuẩn hóa.
  - **Không có mẫu hình "đồ thị giúp ở lỗi mạng".** Tách theo ô (mỗi ô 3 ca), O−L với PPR, cách `abs1`: travel/loss +0,363; auth/delay −0,072; order/loss 0; train/delay 0; cả 6 ô còn lại 0. Trung bình nhóm lỗi mạng +0,073 là do **một ô** kéo lên.
  - travel/loss là ô duy nhất có O−L dương ở cả ba cách chuẩn hóa (+0,252; +0,363; +0,130). order/loss và train/delay bằng 0 ở cả ba cách.
  - travel là hub của đồ thị và mỗi service gốc chỉ có một ô lỗi mạng trên dev, nên không tách được "lỗi loss" khỏi "vị trí hub". Một ô không đủ để nói gì về loại lỗi.
  - auth không có cạnh nào mà O−L vẫn khác 0 (ví dụ +0,306 với diffusion, `abs1`). Thay đổi ở đó là do điểm của các service khác bị dồn lại, không phải thông tin quan hệ về root. Không được tính là "đồ thị giúp".
  - O−R trung bình dương (+0,024 đến +0,036) cũng chủ yếu từ travel/loss (+0,307 ở `abs1`); 8/10 ô có |O−R| dưới 0,02. Câu cũ "O−R > 0 trên cả 30 ca" là sai: đó là trung bình, không phải từng ca.
  - Cách `baro` trong script đổi cùng lúc hai thứ (thang đo và cách gộp kênh) và sinh điểm cực lớn ở 2 ca; số của nó không dùng để kết luận. (`results/v2-prelim/README.md`)
- **ST7 — C5 trên dev30.** F1: G = 0,670; ALL = 0,691; L = 0,073. L với lag3 đạt 0,651, với bin10 đạt 0,652. Hàm mục tiêu chọn λ: 4,19% giá trị (các kênh dính sàn 1e-12) chiếm 99,99999998% tổng loss. Chuỗi phát hiện → chẩn đoán: MRR 0,471; 17 lần báo động trước thời điểm tiêm lỗi trong 4,5 giờ bình thường.
- **ST8 — Baseline.** Dev30: BARO (adapter) MRR 0,659; RCD 0,253. E1 (kết quả công bố của RCAEval trên 90 ca, giao thức khác): top-1 BARO 0,667; TraceRCA 0,644; MicroRank 0,144.
- **ST9 — Final60.** Chưa mở nhãn, chưa có dự đoán, chưa chấm. Telemetry đã tải và chuyển đổi đủ 60/60 ca (v1 G30–G33), dùng lại được. E1 từng xem kết quả baseline công bố trên cả 90 ca (đã khai).
- **ST10 — Tài liệu ngoài (đọc từ arXiv, chưa đối chiếu bản in).** Bài FSE 2026 (arXiv 2510.04711v2) xếp RE2-TT: 67% ca triệu chứng chỉ ở service bị tiêm, 17% không rõ triệu chứng, 17% triệu chứng mạnh hơn ở service khác. Baseline không dùng đồ thị "SimpleRCA" đạt top-1 0,80 trên RE2-TT (BARO 0,67). Changelog RCAEval 9/2026: các baseline PageRank và CIRCA từng âm thầm trả về thứ tự cột; số MicroRank/CIRCA cũ, kể cả trong E1, phải kiểm lại trước khi trích.

## 2. Sai lầm của v1 và nguyên nhân gốc

- **SL1 — Câu hỏi chính lệch đề tài.** C1 là một ablation "quan hệ có thêm giá trị không" trong bài toán đã biết cửa sổ sự cố. Đề tài và cô cần một cơ chế giám sát và chẩn đoán dùng đồ thị, có so với baseline. *Nguyên nhân:* Task C chọn theo tiêu chí "kiểm chứng được, bảo vệ được"; sau Dev30 không có bước nào đối chiếu lại với DT18 và 5 bước của cô.
- **SL2 — Lựa chọn "chịu lực" lệch prior work mà không ai kiểm.** Sàn 1e-12 (BARO và sklearn dùng 1) quyết định dấu của kết luận chính. Phép thử độ nhạy đã đăng ký (relative floor) không chạm tới nó. *Nguyên nhân:* có ma trận provenance (25/38 lựa chọn là riêng của study) nhưng không kiểm lựa chọn nào làm đổi kết luận.
- **SL3 — Giá trị trung gian vô lý được ghi là "giới hạn" rồi đi tiếp.** Điểm 1e12, ngưỡng 2e14, một nhóm kênh chiếm gần 100% hàm mục tiêu. *Nguyên nhân:* cổng review chỉ dừng khi có lỗi cài đặt hoặc rò rỉ nhãn; câu "kết quả yếu không phải thực thi sai" thành vé qua mọi cổng.
- **SL4 — Áp luật "không cứu kết quả" lên development.** Luật đó đúng cho final. Trên dev, biết khuyết tật mà vẫn freeze là sai.
- **SL5 — Hạ tầng lớn hơn khoa học.** ~14.000 dòng script/test cho Task G so với ~3.900 dòng code khoa học; 4 vòng chuẩn bị G30–G33 không thêm thông tin khoa học; HMAC, trust domain, kiểm hash 6.202 tệp; 117 mã quyết định. *Nguyên nhân:* mọi finding của reviewer đều được coi là bắt buộc sửa; reviewer được bảo "tìm lỗi" thì luôn tìm ra.
- **SL6 — Nhầm "đúng kỹ thuật" với "hợp lệ khoa học".** Rất nhiều PASS về cài đặt và provenance trong khi câu hỏi lệch và thiết kế có khuyết tật.
- **SL7 — Đơn giản hóa prior work đúng chỗ tạo ra giá trị của đồ thị.** MicroRCA phát hiện bất thường trên **cạnh** (độ trễ lời gọi), lấy đồ thị con bất thường, cạnh có trọng số. v1 dùng cạnh nhị phân trên cả đồ thị, chỉ đếm số span, bỏ độ trễ.
- **SL8 — Đo "giá trị đồ thị" trên một đồ thị gần như hằng số (ST3)** mà không nêu hệ quả: thực chất là đo 5 vị trí trong một topology.
- **SL9 — So G với L trong C5 bị lẫn năng lực mô hình.** L lag1 gần như không có biến dự báo. Nhờ có ALL và lag3 mới lộ ra.
- **SL10 — Bằng chứng cục bộ chưa phải baseline mạnh.** L không dùng độ trễ span và log, trong khi một baseline đơn giản đã công bố đạt cao hơn (ST10). So "đồ thị với cục bộ" chỉ có nghĩa khi cục bộ đủ mạnh.
- **SL11 — Văn bản khó đọc với con người.** Dày mã, hash, nhãn trạng thái; người chủ đồ án khó tự đánh giá. Cô từng phê bản do AI viết "mơ hồ, chưa rõ liên kết logic".
- **SL12 — Ngữ cảnh mỗi phiên quá nặng.** ~150 KB luật và trạng thái, hai repo, lịch sử giữ nguyên byte trong file trạng thái → hay hết usage giữa chừng.
- **SL13 — Dùng công cụ nặng cho câu hỏi nhanh (02/10).** Agent chạy deep research với 6 subagent (~1,36 triệu token) để trả lời 4 câu hỏi ngắn; hết cửa sổ usage 5 giờ mà chưa làm việc chính. *Nguyên nhân:* không ước lượng chi phí, không hỏi trước khi dùng thao tác tốn kém.

## 2b. Sai lầm của đợt cải tổ 01–02/10 (do agent soạn G0 gây ra)

Minh yêu cầu ghi rõ. Các sai lầm này cùng loại với sai lầm của v1, lặp lại ngay trong lúc viết bài học về v1.

- **SL14 — Đặt giả thuyết H1 từ trung bình nhóm, không tách theo ô.** MRP-v2 và ST6 bản đầu viết "đồ thị giúp ở lỗi mạng, không giúp ở lỗi tài nguyên". Thực tế chỉ một ô (travel/loss) ủng hộ; 2 ô bằng 0; 1 ô âm ở service không có cạnh. Lập luận kiểu này cho phép chọn một ô bất kỳ rồi gọi tên cả nhóm. *Nguyên nhân:* thấy trung bình nhóm hợp với nguyên lý trong tài liệu thì dừng kiểm; vi phạm chính CB4 và QT8 vừa viết. Dữ liệu từng ca có sẵn, tách theo ô mất vài phút.
- **SL15 — Không đánh giá sớm bộ dữ liệu có phân xử nổi câu hỏi hay không.** Các dữ kiện đã có trước khi viết H1: đồ thị gần như hằng số; chỉ 5 service gốc, trong đó 1 không có cạnh và 2 không gọi ai; 67% ca RE2-TT triệu chứng chỉ ở service bị tiêm (ST10); final chỉ có 6 ô lỗi mạng. Từ đó đoán trước được: RE2-TT rất khó cho thấy đồ thị giúp, và kết cục dễ xảy ra nhất của RQ1 là "không đủ bằng chứng". Kế hoạch vẫn đặt RQ1/H1 làm trọng tâm và chỉ ghi điều này ở mục rủi ro.
- **SL16 — Chỉ nhận sai khi người khác chỉ ra.** Lỗi H1 lộ ra nhờ reviewer bên ngoài, không phải nhờ agent tự kiểm. Nếu không có reviewer thì nó sẽ đi tới G3 hoặc tới final.
- **SL17 — Ghi sai dữ kiện trong chính file bài học.** "route và train là lá" (sai: bậc vào 3); "O−R > 0 trên cả 30 ca" (sai: là trung bình). Viết từ trí nhớ, không đối chiếu số đã tính.
- **SL18 — Đưa góp ý của subagent vào tài liệu mà chưa tự nghĩ kỹ.** Câu về nhãn FlashTicket "dựa trên kết quả phía người dùng" (MRP §9, WHY-09): kết quả phía người dùng chỉ cho biết giao dịch nào bị ảnh hưởng, không cho biết service nào. Cả 10 điểm của subagent phản biện đều được "xử lý", đúng kiểu SL5 của v1.
- **SL19 — Biến `baro` trong script thăm dò bị trộn hai thay đổi** rồi vẫn đưa số vào bảng so sánh.
- **SL20 — Gắn "hoàn thành nghiên cứu" với "đồ thị phải thắng ở đâu đó".** Cách đặt này tạo áp lực tìm cho ra một điều kiện đồ thị thắng, tức là nguồn gốc của SL14.
- **SL21 — Ngay sau khi rút H1 lại kết luận quá tay theo chiều ngược lại.** Agent viết "RE2-TT gần như không cho thấy được đồ thị giúp". Cái đã đo chỉ là: trên dev30, với **một kiểu** dùng đồ thị (lan truyền điểm của nút bằng PPR/diffusion), chỉ một ô cải thiện. Chưa thử bằng chứng theo cạnh (độ trễ từng lời gọi). Con số "67% ca triệu chứng chỉ ở service bị tiêm" là của bài ngoài, chưa kiểm trên dữ liệu của nhóm. Kết quả RCAEval đã công bố còn gợi ý ngược lại: phương pháp chỉ dùng metric yếu ở lỗi mạng, phương pháp dùng trace mạnh ở delay. Trạng thái đúng là **chưa biết**, không phải "không được".
- **SL22 — Bám khung của v1 khi soạn v2 (anchor).** MRP-v2 giữ nguyên xương sống của v1: chấm điểm từng service bằng metric (cộng số span), rồi lan điểm trên đồ thị, so L/O/R; chỉ vá thêm nhánh LE. Agent không tự hỏi lại từ đề tài: với một hệ thống có trace, cách dùng đồ thị nào là tự nhiên nhất; lỗi không hiện ở metric (lỗi mã nguồn, hiện ở log và trace) thì sao; có nên dùng bộ dữ liệu khác RE2 không. Minh phải hỏi thì các câu này mới được đặt ra.
- **SL23 — Tư vấn hướng mới bằng các khẳng định quá rộng, chưa kiểm (02/10).** Khi đề xuất "chấm trên cạnh, lấy service bất thường sâu nhất", agent nói: "v1 không dùng log" (chỉ đúng với C1; C5 có đếm dòng log); "lỗi mã nguồn thì metric bỏ sót" (v1 có metric error, latency, workload); "6 loại lỗi RE2 đều hiện ở metric" (chưa kiểm; trên dev30 metric chỉ đưa root lên hạng 1 ở 17/30 ca). Quy tắc "sâu nhất" cũng chưa được định nghĩa và chưa nêu giả định. Kiểm trên dữ liệu ngay sau đó cho thấy bằng chứng theo cạnh kém hơn thời gian tự tiêu của span (`results/v2-prelim/README.md`, thăm dò 2). Bài học: đề xuất chưa kiểm thì phải ghi rõ là chưa kiểm, kèm giả định và trường hợp nó sai.

## 3. Quy tắc rút ra

- **QT1 — Mục đích trước.** Mỗi thành phần, thí nghiệm, tài liệu phải nói được nó phục vụ mục nào của DT18, bước nào của cô, câu hỏi nào trong MRP-v2. Không nói được thì không làm.
- **QT2 — Prior work là mặc định.** Lấy đúng quy ước của paper hoặc code gốc, ghi file và dòng. Muốn lệch phải có lý do và bằng chứng dev, ghi vào `docs/WHY.md`.
- **QT3 — Kiểm "chịu lực" trước khi freeze.** Thay từng lựa chọn riêng của study trong khoảng hợp lý trên dev. Nếu dấu của kết luận chính đổi, lựa chọn đó phải được biện minh bằng nguyên lý hoặc prior work, và báo kèm độ nhạy.
- **QT4 — Tiêu chí chọn không thiên vị giả thuyết.** Bằng chứng cục bộ chọn theo MRR của L; toán tử đồ thị chọn theo MRR của O; không bao giờ chọn theo O−L. Nếu lúc thăm dò đã nhìn thấy kết quả của nhánh khác thì ghi rõ.
- **QT5 — Soi giá trị trung gian trước khi so sánh.** Điểm > 1e6, toàn hòa, ngưỡng cực lớn, một nhóm kênh chiếm gần hết hàm mục tiêu → dừng và tìm nguyên nhân. Không ghi "giới hạn" rồi đi tiếp.
- **QT6 — Dev để sửa, final để kiểm.** Khuyết tật thấy trên dev thì sửa, có nguyên lý. Final60 chỉ mở một lần, sau khi đã khóa thiết kế, giả thuyết và bảng diễn giải (cổng G3) và Minh cho phép (cổng G4).
- **QT7 — Cục bộ phải mạnh.** Trước khi nói đồ thị giúp, L phải ngang hoặc hơn các baseline đơn giản đã công bố (BARO, SimpleRCA) trên cùng dữ liệu.
- **QT8 — Khẳng định về đồ thị cần đủ ba thứ:** hơn L; hơn đồ thị ngẫu nhiên giữ bậc (R) hoặc context không theo đồ thị (ALL); và báo theo điều kiện (loại lỗi, từng ca), không chỉ trung bình.
- **QT9 — Cổng khoa học trước cổng kỹ thuật.** Ở G1, G3, G4 phải trả lời 6 câu hỏi trong MRP-v2 §7. PASS về cài đặt không thay các câu trả lời này.
- **QT10 — Chuyện cấp hướng đi phải hỏi Minh.** Câu hỏi nghiên cứu, dataset, thêm hoặc bỏ thành phần, mở final, đổi cổng. Agent đề xuất, không tự quyết, không đoán ý.
- **QT11 — Quy trình vừa đủ.** Freeze bằng commit; ở final ghi hash dự đoán trước khi chấm; giữ mọi lượt chạy kể cả hỏng. Không thêm HMAC, khóa, trust domain, vòng review mới, mã quyết định cho thao tác vận hành. Muốn thêm cơ chế kiểm soát phải hỏi Minh.
- **QT12 — Review gọn.** Một reviewer, phiên mới (tốt nhất khác model), chỉ nhận spec + diff + kết quả. Chỉ báo lỗi ảnh hưởng tính đúng hoặc độ khớp đề tài. Minh quyết cái nào sửa; không sửa theo mọi finding.
- **QT13 — Viết cho người đọc.** Tiếng Việt, câu ngắn, nêu "tại sao". Hash và mã nằm trong manifest, không rải trong văn bản. Mỗi lựa chọn quan trọng có một mục trong `docs/WHY.md` mà cô đọc hiểu được.
- **QT15 — Tách theo ô và theo ca trước khi nêu mẫu hình.** Muốn viết "X giúp ở nhóm Y" phải kèm: bao nhiêu ô trong nhóm ủng hộ trên tổng số ô, số từng ô, và yếu tố bị trộn (vị trí trong đồ thị, service). Một ô không phải là mẫu hình. Service không có cạnh không được tính là bằng chứng cho hay chống đồ thị.
- **QT16 — Hỏi "dữ liệu này phân xử nổi không" trước khi đặt giả thuyết.** Đếm số ô, số vị trí khác nhau trong đồ thị, số ca thật sự có lan truyền. Nếu kết cục dễ xảy ra nhất là "không đủ bằng chứng" thì nói ngay với Minh lúc lập kế hoạch, không để ở mục rủi ro và không đợi tới cuối.
- **QT17 — Con số trong tài liệu phải lấy từ kết quả đã tính, không viết từ trí nhớ.** Ghi kèm file nguồn.
- **QT18 — Góp ý của subagent hay reviewer là đầu vào, không phải lệnh.** Chỉ đưa vào tài liệu sau khi agent tự kiểm được nó đúng; chưa kiểm được thì ghi là "đề xuất chưa kiểm" và để Minh quyết.
- **QT14 — Ngữ cảnh nhẹ, tiết kiệm usage.** Đọc theo `docs/START-HERE.md`. Gói việc nhỏ hơn nửa cửa sổ usage. Sau mỗi bước ghi kết quả ra file và cập nhật STATE. Câu hỏi nhanh thì trả lời nhanh. Thao tác tốn kém (nhiều subagent, deep research, chạy dài) phải báo trước chi phí ước lượng và được Minh đồng ý.

## 4. Dấu hiệu đang đi vào vết xe đổ — thấy thì dừng lại

- **CB1.** Đang viết thêm quy tắc, phép kiểm, biên nhận thay vì trả lời một câu hỏi khoa học.
- **CB2.** Đang mở thêm một vòng review hoặc "chuẩn bị" vì reviewer vừa nêu thêm finding.
- **CB3.** Một con số vô lý được mô tả bằng chữ "giới hạn đã khai".
- **CB4.** Kết luận "đồ thị giúp" hoặc "không giúp" chỉ dựa trên một cấu hình hoặc một trung bình.
- **CB5.** Tài liệu trạng thái dài hơn 1 trang, hoặc phải đọc hơn 5 file mới bắt đầu làm được.
- **CB6.** Đang cài mọi phương pháp cô nêu làm ví dụ mà không có câu hỏi nào cần nó trả lời.
- **CB7.** Đang đổi thiết kế sau khi đã nhìn kết quả final.
- **CB8.** Đang đoán ý Minh ở một việc cấp hướng đi.
- **CB10.** Một giả thuyết vừa đặt khớp "đẹp" với nguyên lý trong tài liệu mà chưa xem số từng ô.
- **CB11.** Kế hoạch có một nhánh kết thúc bằng "dữ liệu không hỗ trợ" mà nhánh đó đoán trước được từ dữ kiện đang có.
- **CB12.** Đang viết "đã xử lý" cho mọi điểm của một bản phản biện.
- **CB9.** Đang dùng nhiều subagent hoặc công cụ nặng cho một việc có thể tự làm trong vài bước.

## 5. Những thứ của v1 đáng giữ

- Thiết kế đối chứng L/O/R. Đợt nghiên cứu tài liệu không tìm thấy bài RCA nào dùng đồ thị ngẫu nhiên giữ bậc làm đối chứng; đây là điểm mạnh về phương pháp.
- Tách dev/final theo ô; giữ mọi ca trong mẫu số; kết quả từng ca; giữ lượt chạy hỏng.
- Loader, evaluator, `src/rca`, dữ liệu final đã chuyển đổi.
- Thói quen phân biệt "đã đo" với "suy luận" — viết bằng lời thường, không cần hệ thống nhãn.
