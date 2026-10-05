# Gói quyết định G1: phương pháp, dữ liệu và cách chia

**CANDIDATE — Codex đề xuất, Minh quyết; chưa đóng G1.** G1 là cổng duyệt đầu vào nghiên cứu sau bước hiểu phương pháp và khảo sát dữ liệu, chưa phải kết quả so baseline trên nhiều bộ. Gói này phục vụ tên đề tài DT18: xây dựng hệ thống bán vé phân tán có đồ thị phụ thuộc để giám sát và chẩn đoán; hướng dẫn của cô yêu cầu hiểu cơ chế → mở rộng dữ liệu công khai → tìm hạn chế → thiết kế đồ thị → áp dụng FlashTicket.

Minh cần quyết sáu thẻ dưới: biến thể phương pháp, gói dữ liệu, cách chia và tiếp xúc, ngân sách nhãn, quy tắc cửa sổ, độ đo truy hồi. Đề nghị giữ danh sách đã duyệt, dùng gói A đa nguồn có điều kiện, giữ RE2-TT 30 dev/60 test và không chọn cửa sổ bằng điểm. **Hiện chưa bộ giữ ngoài nào chứng minh đủ cả ba trục độc lập**; Bank chỉ là ứng viên metadata. Chưa có protocol public được xác lập để chấm phát hiện tự động liên tục không lộ mốc. Nhãn vùng ảnh hưởng độc lập chỉ dự kiến ở FlashTicket. Vì vậy dữ liệu public hiện có thể không phân xử được phát hiện tự động, vùng ảnh hưởng hoặc chuyển sang hệ độc lập, dù xếp hạng root có nhãn ở một số bộ.

Khuyến nghị đổi nếu có release bất biến, quyền dùng rõ, nhãn/normal/schema và provenance chứng minh bộ ngoài phù hợp; hoặc Minh chọn test chỉ TX0. Không dùng kết quả “đồ thị thắng” để chọn. Mọi lựa chọn sử dụng dưới đây **(chờ WHY — mục lý do chính thức trước sử dụng)**.

## Bằng chứng và sáu câu của cổng

T-020 là task tổng hợp này. Q-37/Q-38 là quyết định Minh về danh sách phương pháp; Q-54 là quyết định chuyển nhãn/cửa sổ sang G1; Q-56 chuyển độ đo Retrieval sang G1. Q-49/WHY-13 là Codex chọn bảo toàn Bank theo ủy quyền, **không là Minh chọn Bank thí nghiệm**. T-013, hồ sơ BARO/BOCPD/N-Sigma, đã được Minh duyệt sau sửa phản biện; không dùng R1 cũ làm chặn hiện trạng.

| Câu MRP §7 | Trả lời riêng | Bằng chứng/giới hạn |
|---|---|---|
| 1. Phục vụ câu nào của cô/DT18? | Hiểu kỹ thuật và chọn nhiều dữ liệu để chuẩn bị thực nghiệm | [Hồ sơ đọc nhanh](07-danh-sach-phuong-phap-va-doc-nhanh.md), [chín tiêu chí](01-bang-tieu-chi-hop-nhat.md), đối chiếu cô dưới đây |
| 2. Dữ liệu phân xử nổi không? | **Chưa đủ cho toàn bộ RQ** | Root-ranking có nhãn; blind detection, C9 và vùng ảnh hưởng thiếu như [V4](03-task-cham-duoc-va-che-do-b.md) |
| 3. Baseline đủ mạnh chưa? | Hồ sơ có cơ chế/biến thể và chạy kiểm; **chưa có bảng baseline P3 hoàn chỉnh** | [Checklist từng biến thể](trung-gian/method_evidence/method-checklist.csv), [ma trận](04-phuong-phap-x-dataset.md); GDN b chưa calibration đạt |
| 4. Trung gian hợp lý chưa? | Các phép kiểm được phép đã đối chiếu; không suy từ điểm cuối | [Kiểm số](09-kiem-cheo-so-lieu.md), [kiểm sâu](trung-gian/method_evidence/deep-source-audit.md); arithmetic không chứng minh pipeline đầy đủ |
| 5. Tách theo điều kiện/ca chưa? | Sổ/census/split có từng ca và ô; **chưa có phân tích hạn chế P4** | [Sổ ca](02-so-ca-da-nhin.md), [ba cách chia](06-phuong-an-dataset-va-chia.md); không trộn biết mốc/tự phát hiện |
| 6. Còn lựa chọn thiếu “tại sao”? | **Có**, cần Minh duyệt D1–D6 và lý do nháp | [Nháp tài liệu chung](de-xuat-tai-lieu-chung.md); không tự ghi WHY/DECISIONS |

## D1 — Biến thể nào làm baseline chính?

**Vì sao G1:** MRP §7 duyệt danh sách; các tên đã duyệt cần implementation rõ. Giữ năm RCA BARO, SimpleRCA M4, CIRCA, MicroRank, TORAI; đối chứng NSigma RCA, TraceRCA RCAEval, RCD; detectors BOCPD, NSigma, GDN. CIRCA có PC và kiến trúc. Không thêm SPOT hoặc DecompRCA vào danh sách. Họ supervised RCA chưa có đại diện; GDN là detector, không bù coverage RCA supervised. RQ1 không là khảo sát exhaustive mọi họ.

| Phương án (chờ WHY) | Nghĩa, bằng chứng, được/mất | Đảo ngược |
|---|---|---|
| D1-A tách tái lập và bản sửa | Tái lập code ghim riêng; baseline so sánh dùng MicroRank sửa đầu vào, TORAI sửa đã áp và output hữu hạn/ties tường minh. CIRCA ghi graph/scorer/DA/interval, không gọi mọi bản cùng một method. Được cơ chế hợp lệ; mất đồng nhất tuyệt đối published code | Trước chạy P3 có thể đổi; đã xem score thì đổi phải ghi thay đổi và không lựa bản thắng |
| D1-B code ghim làm bảng chính | Dễ so tác giả; nhưng overlap partitions, fallback/NaN, future/test-label paths có thể làm bảng không đúng bài toán. Không được coi code lỗi là mạnh baseline | Đổi trước chạy được; kết quả không hợp lệ chỉ tái lập |
| D1-C chỉ bản gốc đầy đủ | Giữ ý nghĩa thuật toán bài; schema kind/pod/root, công sức CIRCA empirical và detector MicroRank chưa đủ ở nhiều bộ; giảm coverage hiện có | Chuyển P3 có điều kiện, không âm thầm bỏ phương pháp đã duyệt |

**Khuyến nghị D1-A**, nhãn “sửa” chỉ đúng phần đã sửa, không gọi reproduction toàn bài. Không mở lại danh sách Minh đã chọn. Giữ conventions M4 đã áp, GDN b là diagnostic chưa ready; số seed/cutoff/ties dùng trong P3 cần ghi từ nguồn ghim và ngân sách, không tự chọn theo score. Nhánh SeverityScorer của TORAI giữ làm số trung gian để kiểm cơ chế; đề nghị thêm thành baseline riêng vẫn cần Minh quyết trong D1, chưa được thêm. Phản đối mạnh nhất: so bản sửa với benchmark tác giả không còn cùng implementation. Đổi khi pipeline gốc có schema đủ và tái lập không nhãn chứng minh hợp lệ. RQ1/RQ3b phụ thuộc fidelity/candidates; RQ3a tách detector; RQ3c không được thêm nhãn; RQ3d cần cùng evidence khi so graph. Nháp quyết định: “Minh chọn D1-__; các biến thể và vai trò theo bảng07; bản tái lập và baseline hợp lệ báo riêng.”

## D2 — Gói dữ liệu và bộ giữ ngoài

**Vì sao G1:** MRP §4/§7; cô yêu cầu mở rộng dữ liệu công khai. [40 phần dữ liệu](01-bang-tieu-chi-hop-nhat.csv) dùng cùng tiêu chí, nguồn và OPEN; chi phí riêng. Các split/census ở [V7](06-phuong-an-dataset-va-chia.md) là đề xuất có thể tái lập.

| Phương án (chờ WHY) | Được/mất và bằng chứng | Đảo ngược |
|---|---|---|
| A đa tín hiệu | TT/OB/RE3-TT; thêm Nezha-OB và Eadro-SN có điều kiện license. Nhiều root/hệ hơn TT, có trace/log/metric; test hai họ ngoài đã TX1, C9 chưa đủ | Trước mở test có thể đổi package; không biến bộ đã TX1 thành hoàn toàn ngoài thiết kế |
| B kiến trúc thiếu trace | TT và ba release Sock Shop; LEMMA nhánh phụ chưa đủ census/license/schema. So kịch bản thiếu trace có chủ đích; mất paired multi-signal và độc lập họ | Đổi được trước chạy; không dựng trace giả |
| C test chỉ TX0 | TT, RE1-TT, RE3-OB test; Nezha/Eadro chỉ dev. Tiếp xúc sạch hơn; ít đa nguồn test và RE3-OB schema chưa kiểm | Trước G3 đổi được nếu chưa mở đo; số liệu đã xem không “quên” được |

**Khuyến nghị A có điều kiện, và ghi hiện chưa có bộ giữ ngoài đủ tiêu chí**, không duyệt chạy dự phòng Bank. RCAEval trong A có nhãn, census và mốc tiêm đã kiểm trên phạm vi mẫu; đơn vị vật lý duration trace còn OPEN, hơn DeepTraLog ở task service-root/time và hơn LEMMA ở census/clock; Nezha/Eadro bổ sung root/hệ, không bị loại vì adapter tốn công. Không nói RCAEval hơn mọi ứng viên hoặc đã có sẵn nên chọn. Phản đối mạnh nhất: license và testTX1 khiếnA chưa có khả năng chuyển hệ độc lập được xác lập. Đổi với bằng chứng C1/C2/C3/C8/C9 ngoài họ hoặc Minh chọn định nghĩa test nghiêm hơn. RQ1/RQ3b đa điều kiện; RQ3a b chưa hợp lệ; RQ3c chỉ FlashTicket; RQ3d không suy static topology đủ phân xử. Nháp: “Minh chọn gói__; vai trò theo CSV__; held-out__ hoặc chưa có bộ đạt; điều kiện OPEN__.”

**Sock Shop:** census ba release có trace 0. Nên dùng ở B hoặc nhánh kiến trúc phụ, không thay bộ trace chính. Có metric/log tùy release, lỗi code ở RE3; trace RCA không chạy. RE2 đã TX2, RE1 chỉ ít ô chưa thấy kết quả; không báo như giữ ngoài. [Nguồn census](../T-019/census-summary.json) và bảng V2.

**LEMMA-RCA:** PR/Cloud cần tách Original/Preprocessed và ngày mẫu; không chứng minh Original không trace bằng mẫu processed. Root NFS ngoài app, instance và timeline còn xung đột; license NC/ND và quyền phái sinh OPEN. Không chọn RCA chính hoặc tạo ô từ datecapture. Giữ nhánh kiến trúc ứng viên cần nguồn nhãn/schema/license; đây là trả lời có căn cứ việc cô nêu tên, không yêu cầu phải cài release không chấm được. OT đã loại theo quyết định Minh, không mở lại.

**C9:** RCAEval/RE3-OB không độc lập họ; TRCA cùng byte Nezha. Bài OpenRCA khác tác giả RCAEval, nhưng nhóm cung cấp dữ liệu Bank thô, injector và collector chưa chứng minh độc lập; LEMMA khác provenance nhưng injector/collector/task còn OPEN; OpenRCA2.0 có overlap tác giả/collector. Không ứng viên nào chứng minh đủ 3/3. [Bảng từng trục](trung-gian/dataset_evidence/independence-axes.csv).

## D3 — Test TX1 và cách chia theo ô

**Vì sao G1:** MRP §4 định nghĩa “chưa mở” là chưa thấy kết quả method, còn held-out chỉ metadata/schema/đếm nhãn. TX0 chỉ metadata; TX1 đã xem thống kê đo; TX2 đã thấy kết quả method. Không đồng nhất đã chạy method với đã đọc ranks nếu chỉ time-only log.

| Phương án (chờ WHY) | Nghĩa và được/mất | Đảo ngược |
|---|---|---|
| D3-A test có TX1, công bố tiếp xúc | Theo nghĩa chưa thấy method-result; giữA/B với toàn ô và cấmTX2test. Có nhiều hệ; thống kê trước thiết kế gây thiên lệch tiềm tàng | Không khôi phục sạch tiếp xúc; có thể chuyểnTX1 sangdev trướcG3 |
| D3-B test chỉ TX0 | DùngC; ít prior descriptive influence; co hẹp cross-family test | Không mở thêm test trướcG3; chuyển thêmdev làm giảmtest |
| D3-C TX1 chỉ test tái lập | Báo riêng kết quả trênTX1, kết luận unseen chỉ TX0; thêm hai phạm vi kết luận | Có thể thu hẹp claim, không gộp sau để tăng mẫu |

Khuyến nghị **D3-A có khai báo giới hạn**, giữ toàn ô theo seed đã ghi và RE2-TT30/60. Phản đối mạnh nhất: TX1 đã gợi thiết kế nên “unseen” dễ bị hiểu quá; D3-C hoặcB tốt hơn nếu câu hỏi là hoàn toàn ngoài thiết kế. Đổi khi audit cho thấy per-case outputs/aliasesTX2 gián tiếp; ô đó phải dev. RE1-OB alias với125localTX2 chưa giải nên không chọn test. RQ1 có thể mô tả; RQ3a/b/d chưa thấy method không đồng nghĩa độc lập thiết kế; RQ3c không thay đổi. Nháp: “Minh chọn D3-__; TX1 được__ với giới hạn__; chia toàn ô theo script và CSV đã duyệt, test chỉ mở sau G3.”

## D4 — Nhãn nào được cấp cho phương pháp?

**Vì sao G1:** MRP §4 ngân sách nhãn, Q-54. MRP §4 ghi nhãn test chỉ chấm nhưng P3 chế độ (a) biết trước thời điểm; cần Minh làm rõ mốc ngoài nào được cấp khi chấm test, không tự coi đây là quyền đọc hay tune test. [V6](05-nhan-va-cua-so.md) tách fit/tune/score từng nhóm và42 hàng đầu vào.

| Phương án (chờ WHY) | Được/mất | Đảo ngược |
|---|---|---|
| D4-A normal theo từng hệ, dev labels tune, test labels chỉ score | Học scale/threshold/regressor từ normal; root gold không vào features; normal giữ ngoài độc lập chỉ cấp sau G3 và ngân sách đã duyệt. Có detector khả thi; normal cùng hệ là thông tin phải công bố | Đổi trước fit; đã dùng labels không gọi unsupervised/unseen |
| D4-B không có normal mới ở hệ ngoài | Kiểm zero-shot chuyển hệ rõ; GDN cột/embedding và operations mới có thể không chạy | Thêm normal tạo thí nghiệm khác, không so cùng budget |
| D4-C known-injection và blind là hai bảng | Cho mốc chế độ a, chế độ b chỉ detector hợp lệ; không gọi injected-delay là onset-delay. Tốn hai protocol nhưng tránh trộn label budget | Có thể thu hẹp bảng, không trộn các điều kiện |

Khuyến nghị **A cùngC**, chưa cấp label giữ ngoài ởtask này. Phản đối mạnh nhất: normal từ dev bị cắt bằng injection và load không đại diện; học threshold vẫn có bias. Đổi nếu không có normal sạch độc lập hoặc evaluator theo onset không tồn tại; giữ NA/known-injection. RQ1/RQ3b so cùng budget; RQ3a phụ thuộc timeline/negative coverage; RQ3c cần nhãn độc lập; RQ3d giữ evidence giống nhau. Nháp: “Minh chọn budget__; normal/fit__, tune chỉ dev, root gold chỉ evaluator; mốc thời gian mode (a) theo ngân sách Minh duyệt, mode (b) không cấp mốc; hai chế độ riêng.”

## D5 — Quy tắc cửa sổ chung

**Vì sao G1:** Q-54 chưa đủ căn cứ chọn số; MRP P3 đòi cùng cửa sổ. W-time 300s mỗi phía và sensitivity 600s, hoặc W-feasible chọn từ 300/600 bằng coverage/fit-normal trước score, là hai phương án trong [V6](05-nhan-va-cua-so.md). Không clip âm thầm. Default CIRCA 1min/111points không cùng111s; TORAI double-stride không là window-duration; GDN 5 tick khác training budget.

W-time dễ so, nhưng bỏ các stratum thiếu dữ liệu và không đủ normal. W-feasible tận dụng coverage, nhưng giao đủ fit có thể rỗng, và feasibility không chứng minh calibration. Cả hai đổi được trước chạy P3; sau nhìn score phải báo sensitivity và lý do thay đổi, không chọn winner.

Khuyến nghị **W-feasible, chưa chốt một số**. P3 kiểm normal-only completeness/requirements trên dev rồi khóa primary trước root-ranking; nếu không có giao thì báo không có bảng chung của stratum. Phản đối mạnh nhất: minimum của hồ sơ chỉ chạy được, không đủ threshold statistical; không ép nó thành chuẩn. Đổi khi normal control chứng minh thiếu coverage/calibration hoặc prior work đòi history dài khác; tái lập tác giả báo riêng. RQ1/RQ3a/b nhạy time/candidates; RQ3c/d không được giải thích window effect thành graph gain. Nháp: “Minh chọn quy tắc__; primary khóa từ normal trước score, sensitivity__, thiếu coverage ghi thiếu, author-config riêng.”

## D6 — Có thêm Retrieval@K và Rerank@1?

**Vì sao G1:** Q-56 chuyển đề xuất E2 của hồ sơ GDN/DecompRCA sang đây. D6-A thêm Kservice 5/10 theo evaluator ghim, báo conditional cùng finalMRR/Hit; D6-B chỉđộđo cuối, ít bảng nhưng khó phân biệt root vắng candidates. Đổi được trước P3 khi lưu đủ candidates, không tính lại từ output đã cắt mà giả universe.

Khuyến nghị **A**: service mapping độc lập gold, dedup/ties công bố; denominator0=NA; root vắng universe báo riêng. E2 đo root trong Kservice đầu **của thứ hạng**; không mặc nhiên là causal isolation một retriever độc lập. Conditional Rerank không thay chất lượng end-to-end. Phản đối mạnh nhất: metric→service mapping và prefix ranking có thể khiến ratio bị diễn giải như module performance. Đổi nếu không định nghĩa candidate/universe/mapping hợp lệ. RQ1/RQ3b phân rã chẩn đoán; RQ3a/c/d không thêm bằng chứng. Nháp: “Minh chọn__; RetrievalKservice__, Rerank conditional và final metrics cùng báo, NA khi mẫu số 0.”

## Đối chiếu từng yêu cầu giảng viên

| Yêu cầu | Gói này đáp ứng tới đâu |
|---|---|
| Hiểu sâu cơ chế | P1 hồ sơ/42biến thể, kiểm sâu MicroRank và TORAI theo lựa chọn tiên nghiệm; không chỉ chép abstract |
| Mở rộng dataset public | Chín tiêu chí chung/ba cấu trúc; SockShop/LEMMA có lý do; chưa thay proposal bằng kết quả P3 |
| Hạn chế phương pháp | Chuẩn bị nhãn/candidate/windows đểP4 kiểm; chưa kết luận graph phải thắng |
| 1. Đồ thị phụ thuộc | Kiểm parent/mapping/architecture eligibility, thiết kế ởP5 |
| 2. Graph anomaly | Detectors ngang RCA; PageRank ranking không gọi detector; chưa thiết kếP6 |
| 3. Thực nghiệm public | Split chưa mở test; [kế hoạchP3](10-ke-hoach-p3-de-xuat.md) dựa chi phí đã đo |
| 4. Precision/Recall/F1/MRR/NDCG | Tách detection/root/region labels và điều kiện; CI theo ô, không spans |
| 5. LLM giải thích | P8 sau ranking; không thêm LLM calls ởG1 |
| Tích hợp sản phẩm | P9/P10; giữ trách nhiệm hệ thống theoDT18, không dùng thư cũ giảm nhẹFlashTicket |

Ngoài sáu thẻ: cần nguồn bất biến và cơ chế đọc đúng dòng tiêu đề cho giữ ngoài, cùng quyền sử dụng/provenance. V7 đã cho phép đọc tiêu đề nếu đáp ứng điều kiện; Bank hiện thiếu artifact và cơ chế đáp ứng, không thiếu quyền đã cấp. Minh cần quyết cách xử lý chi phí lịch sử CIRCA vượt Q-40 nếu áp dụng. [Sổ chuyển G1](08-so-chuyen-g1.csv) ánh xạ 533 chỗ tìm được/533 chỗ, phần thuộc P3 không tạo cổng mới. [Đính chính](dinh-chinh-task-cu.md) giữ lịch sử, [nháp chung](de-xuat-tai-lieu-chung.md) chưa ghi vào nguồn chính thức.
