# LEMMA IT — xác minh nguồn, giấy phép và khả năng bảo toàn

Báo cáo này khóa bằng chứng giai đoạn nguồn trước số đo. Sau đó Q-47 đã được thực hiện cho bốn ZIP: xem [kiểm file](kiem-file.md) và [thẻ hiện hành](the-dataset.md). Câu “chưa kiểm số đo” ở phần phân tích nguồn chỉ mô tả thời điểm của nhánh nguồn, không thay trạng thái mẫu hiện hành.

Kiểm ngày 03/10/2026 theo Q-47. Phạm vi: Product Review và Cloud Computing, mỗi hệ gồm Original/Preprocessed. OT đã bỏ khỏi khảo sát mới; nguồn cũ chỉ là lịch sử. Báo cáo này bổ sung thẻ 10 mục, không biến metadata thành kết quả chất lượng số đo. Quyết định bảo toàn thuộc gói cha và phải ghi trong WHY trước sử dụng.

**Kết luận:** nguồn công khai cho thấy LEMMA IT có tiềm năng đánh giá xếp hạng root theo pod/node trên scenario dài với metric/log. Bằng chứng để coi là bộ graph/trace đầy đủ vẫn thiếu. Giấy phép của đúng bản phát hành hiện hành còn mâu thuẫn NC/ND. **DECIDED tại gói cha: Q-49/WHY-13 bảo toàn OpenRCA Bank, không chọn LEMMA.** Phân tích dưới đây giải thích vì sao nếu xét LEMMA như lựa chọn thay thế thì chưa đủ căn cứ chia PR–Cloud thành hai bộ độc lập; không thêm quyết định giữ ngoài thứ hai.

## 1. Nguồn và phiên bản đã kiểm lại

- [comparison.json](runs/source-final-001/comparison.json) đối chiếu API hiện hành với lượt nguồn đầu: cả bốn HF revision, tập file, byte, Git/LFS object và README đều khớp. GitHub code cũng cùng revision. Không tự đổi sang nhánh PR chưa merge.
- [manifest nguồn mới](runs/source-final-001/manifest.json) lưu URL, thời gian UTC, trạng thái, hash và byte; [manifest thảo luận](runs/discussions-final-001/manifest.json) khóa năm thread. Các mã revision/hash chỉ nằm trong manifest/result.
- [arXiv abstract hiện hành](runs/source-final-001/sources/paper-abs.html) xác nhận v1 ngày 08/06/2024, v4 ngày 25/08/2026. [Paper v4 đã lưu](runs/run-001/sources/paper-v4.html) là nguồn mô tả; năm v4 không làm dữ liệu thành collection mới năm 2026. HF date token PR là 2021–2022, Cloud là 2023–2024; đây là tên archive, không tự chứng minh thời gian đo.
- Trang `www.lemmarca.info` vẫn lỗi SSL ở lượt này; trang GitHub Pages tác giả và catalog đọc được. Không bỏ qua xác minh TLS, không gọi site chết vĩnh viễn. Lỗi giữ trong manifest.

Tái lập offline: `py -3 -B results/T-011/scripts/verify_current_sources.py --verify`; thêm `--run discussions-final-001` để kiểm nguồn thảo luận. Script chỉ lấy nguồn/metadata, không gửi request archive.

## 2. Giấy phép: chưa có nguồn giải quyết NC/ND

| Đối tượng | Bằng chứng đúng phạm vi | Kết luận |
|---|---|---|
| Dữ liệu bốn HF kho hiện hành | README đều có frontmatter NC và mục nội dung ND; API cardData ghi NC. | Mâu thuẫn ngay trong cùng release; không chọn một trường theo thuận tiện. |
| Tuyên bố dữ liệu tại repo tác giả | README mở đầu NC nhưng mục License ND. | Cùng tác giả vẫn chưa thống nhất. |
| File LICENSE của kho code | File ngắn ghi NC và URL điều khoản, không chứa toàn bộ legal text. | Là chứng cứ về kho code; không tự cấp quyền cho mọi dataset hoặc baseline vendored. |
| Paper v4 Appendix F | Tuyên bố dataset ND; yêu cầu xem giấy phép baseline ở repo gốc. | Phân biệt giấy phép paper, dataset và baseline; arXiv paper license không thay dataset license. |
| Bốn HF PR ngày 26/08/2026 | Tất cả còn OPEN. API ghi tác giả PR không là owner/org member. | Chưa merge, chưa có xác nhận chủ dữ liệu; không dùng làm điều khoản đã có hiệu lực. |

Chi tiết mới làm rõ vì sao không thể chọn NC từ chữ “fix license”:

| Kho và thread | Thay đổi do người gửi PR mô tả | Phạm vi chứng minh |
|---|---|---|
| [Product Review Original #1](https://huggingface.co/datasets/Lemma-RCA-NEC/Product_Review_Original/discussions/1) | Đổi nội dung ND sang NC để khớp YAML. | Đề xuất của contributor. |
| [Product Review Preprocessed #1](https://huggingface.co/datasets/Lemma-RCA-NEC/Product_Review_Preprocessed/discussions/1) | Đổi YAML NC sang ND để khớp nội dung. | Đề xuất theo hướng ngược lại. |
| [Cloud Original #1](https://huggingface.co/datasets/Lemma-RCA-NEC/Cloud_Computing_Original/discussions/1) | Đổi nội dung sang NC. | Đề xuất của contributor. |
| [Cloud Preprocessed #2](https://huggingface.co/datasets/Lemma-RCA-NEC/Cloud_Computing_Preprocessed/discussions/2) | Đổi nội dung sang NC, sửa task category. | Không phải xác nhận của tác giả dataset. |

Snapshot API đầy đủ nằm trong `runs/discussions-final-001/sources/`; trạng thái và nội dung event được kiểm trực tiếp, không chỉ đọc tiêu đề. GitHub all-issues API không cho thấy trao đổi giải quyết license; một PR lịch sử không liên quan không được dùng để khảo sát OT thêm.

**OPEN:** cần chủ dữ liệu xác định điều khoản cho từng release/bản phái sinh để kết luận license chính xác và quyền ngoài phần giao nhau; task không gửi email/form. Hoàn tất xác minh nguồn không đồng nghĩa giải quyết xung đột giấy phép. Phần giao quyền bên dưới đủ cho hành động kiểm nội bộ đã duyệt Q-47, không cần chọn một license theo suy đoán.

**Đối chiếu hành động hẹp:** [CC BY-NC 4.0 §2(a)(1)](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en) cho phép sao chép và tạo bản chuyển đổi vì mục đích phi thương mại. [CC BY-ND 4.0 §2(a)(1)](https://creativecommons.org/licenses/by-nd/4.0/legalcode.en) cho phép sao chép và tạo bản chuyển đổi nhưng không chia sẻ bản chuyển đổi. Cả hai §2(a)(4) cho phép thay đổi kỹ thuật cần thiết; §4 đề cập trích xuất/tái sử dụng database. Do đó **không đúng** khi nói ND tự cấm tải, giải nén hay kiểm nội bộ. Sao chép source nguyên trạng và kiểm nội bộ phi thương mại, không chia sẻ dataset hoặc payload đã biến đổi, nằm trong giao quyền của cả hai tuyên bố. Nguồn lưu tại [manifest điều khoản](runs/license-terms-001/manifest.json). Đây là kết luận về hành động cụ thể đã được Q-47 duyệt, không chốt license duy nhất, không gọi LEMMA cấp phép kép, không kết luận quyền phân phối phái sinh. Root ghi lý do này trước tải; nhánh nguồn chưa tải telemetry. Các giới hạn cũ coi mâu thuẫn chặn mọi kiểm được thay bằng phân biệt hành động này.

## 3. Metadata đáp ứng bài toán đến đâu

| Câu hỏi | FACT nguồn/metadata | Phần chưa được xác minh |
|---|---|---|
| Có nhiều tín hiệu? | Kho Preprocessed có metric/log archive; Cloud 20240207 thiếu archive log xử lý, README giải thích có CloudTrail CSV. | Đồng bộ clock, độ phủ entity, NaN/gap/constant và join thực chưa kiểm. |
| Có graph cha–con? | README code nói raw có trace; paper B.3 nhắc Jaeger ở scenario storage/DDoS. | Chưa biết archive/member/schema parent-linked span. Jaeger logs không tự chứng minh một release có trace graph đầy đủ. |
| Có root/time? | README chỉ root MongoDB-v1 cho PR 20211203; code có một JSON label Cloud 20240124 và hằng số đánh giá. | Census toàn archive, mapping pod/host/service và graph position OPEN. Số date token không là số incident/lặp. |
| Có scenario khác benchmark nhỏ? | Paper B.1/B.3 mô tả OpenShift/CloudWatch, lỗi storage/resource/security/config, công cụ thủ công/OpenSSL/JMeter/Git thay đổi theo scenario. | Chưa map từng scenario/date với taxonomy tài nguyên/mạng/mã và tín hiệu thực. JMeter chủ yếu là workload/KPI, không tự gọi là công cụ tiêm của mọi ca. |
| Có khoảng normal? | Paper có thời gian quan sát trước tác động, lịch dài; Appendix J nói controlled fault và kiểm nhãn bằng chuyên gia. | Tuyên bố tác giả không xác minh normal sạch/warm-up/recovery, onset thật, hoặc độ chính xác từng nhãn. |
| Có đủ để chấm RQ? | CANDIDATE ranking pod/node khi xác minh nhãn/mapping. | Chưa xác lập service/operation ranking; chưa có nhãn vùng ảnh hưởng hay onset độc lập. Trace/graph task phụ thuộc schema thật. |

Nguy cơ hữu ích cho thiết kế sau: code công bố chọn KPI/metric theo case ID và một đoạn tạo timestamp giả. Không được chép logic đó vào adapter tự phát hiện; thông tin nhãn/chọn ca chỉ phục vụ census và chấm. Lời paper nói chất lượng nhãn cao không thay phép kiểm nhãn thực.

## 4. Thời gian: xác nhận tác giả có phạm vi rõ

[Cloud Preprocessed #1](https://huggingface.co/datasets/Lemma-RCA-NEC/Cloud_Computing_Preprocessed/discussions/1) có phản hồi ngày 12/12/2025 từ Zhengzhang Chen, API ghi org member. Phản hồi xác nhận PPTX dùng JST và metric/log dùng UTC; đổi ví dụ 11:30 JST thành 02:30 UTC là đúng. README Preprocessed hiện hành đã ghi điều này. Đây là FACT nguồn tác giả, chưa là kiểm clock file.

[label-time-check.json](runs/run-001/label-time-check.json) vẫn có bất nhất riêng: epoch Cloud 20240124 tương ứng 09:10:51 UTC; chuỗi `inject_time` là 03:10:51 không timezone. Chênh 6 giờ chỉ khi giả sử chuỗi UTC. Phản hồi về PPTX không nhắc JSON này, nên không giải được nó; không tự áp trừ 9 giờ hay sửa nhãn.

## 5. Độc lập: xét nhóm, công cụ, stack và raw lineage

| Cặp | Bằng chứng | Phán đoán và giới hạn |
|---|---|---|
| Original ↔ Preprocessed cùng hệ | README mô tả chuyển JSON metric thành NPY và trích/parsing log từ raw. | Cùng lineage; không dùng làm hai bộ độc lập hay chia cùng ca sang hai phía. |
| Product Review ↔ Cloud Computing | Cùng nhóm tác giả, paper và repo; B.3 dùng lại Microservice A/productpage-v1 và scenario/quy trình chung. Có khác OpenShift/CloudWatch, date token và công cụ tùy ca. | Chưa chứng minh độc lập đủ ba trục. Không khẳng định hai hệ dùng chung raw, cũng không đủ căn cứ coi Cloud là development độc lập với PR holdout. |
| LEMMA IT ↔ RCAEval | LEMMA do Zheng/Chen/Wang/Deng/Matsuoka/Chen, môi trường và controlled scenarios theo paper; RCAEval là nhóm Pham, stress-ng/tc/sửa mã trên các hệ benchmark, nguồn T-002. | Bằng chứng mức nhóm/collection/thu thập khác mạnh hơn chỉ khác tên. Vẫn dùng chung một số công nghệ Prometheus/Jaeger/Kubernetes; chưa có đối chiếu hash raw đầy đủ hoặc attestation không reuse. |
| LEMMA IT ↔ Nezha | Nezha nhóm Yu/Chen/Li/Chen/Li/Zheng, OTel/Tempo/Promtail/Loki, công cụ code Byteman/Hypno/Failpoint; LEMMA dùng Nezha như baseline. | Tên thư mục `Baseline/Nezha` và `root_cause_hipster.json` không chứng minh dùng lại corpus Nezha/Online Boutique. Khác collection có nguồn; reuse raw vẫn chưa kiểm byte. |
| LEMMA IT ↔ Eadro | Eadro nhóm Lee/Yang/Chen/Su/Lyu; Chaosblade, Jaeger/cAdvisor/Prometheus/InfluxDB/ELK trên TT/SN. | Khác nhóm/scenario; có công nghệ chung. Không suy độc lập tuyệt đối vì đổi tên platform. |
| LEMMA IT ↔ DeepTraLog | DeepTraLog nhóm Fudan, TT v0.2.0/SkyWalking, release trace/log. LEMMA hai platform theo paper, metric/log. | Khác collection/instrumentation là bằng chứng tích cực; không có census/hash raw xuyên bộ chứng minh không trùng. |

Nguồn cặp đối chiếu: [T-002](../T-002/the-rcaeval.md), [Nezha](../T-008/the-dataset.md), [Eadro](../T-009/the-dataset.md), [DeepTraLog](../T-010/the-dataset.md), cùng snapshot gốc các thẻ dẫn. Các thẻ này có thể được nhánh tương ứng cập nhật sau; metadata LEMMA khóa riêng trong manifest.

Phân tích giả định bảo toàn cả lineage IT không trở thành quyết định; Q-49/WHY-13 chọn OpenRCA Bank. LEMMA không giữ ngoài; kiểm telemetry hẹp được phép theo giao quyền vừa xác minh, nhưng nhánh nguồn chưa chạy. Giữ ngoài không giải license/nhãn/trace thiếu, không cam kết kết quả đánh giá hay đủ ba nguồn tín hiệu. Không tự coi LEMMA là độc lập với mọi ứng viên 2025–2026 chưa khảo sát ở nhánh này.

## 6. Tự phản biện của người làm trước Claude

1. **Phản biện:** giấy phép code NC có thể đủ kết luận data NC? **Kết quả:** không; data README và paper ND, thậm chí các PR sửa theo hai hướng. Đã giữ OPEN theo release.
2. **Phản biện:** các trường HF ghi NC là tự sinh nên có thể bỏ qua? **Kết quả:** README YAML thật cũng ghi NC, khớp API. Không phải chỉ lỗi giao diện.
3. **Phản biện:** bốn/sáu archive đủ census incident? **Kết quả:** không; file/ca/lặp khác đơn vị. Thẻ giữ count public file và label census riêng.
4. **Phản biện:** hai tên IT có độc lập không? **Kết quả:** nhiều thành phần và quy trình dùng chung, chưa đủ chứng minh. Khuyến nghị bảo toàn cả lineage tránh lựa chọn thuận tiện.
5. **Phản biện:** nguồn nói Jaeger là đã có graph? **Kết quả:** không; parent-linked schema và quality vẫn OPEN đến đúng quyền.
6. **Phản biện:** xác nhận JST sửa được mọi label? **Kết quả:** không; nó áp cho PPTX. JSON 20240124 giữ riêng.
7. **Phản biện:** paper v4 năm 2026 làm đây là dataset mới? **Kết quả:** không; collection date tokens/revision unchanged được kiểm. Không đếm lại raw/preprocessed hoặc revision paper thành bộ độc lập.

Không chạy phương pháp RCA, không đọc telemetry, không mở `data/locked`, không gửi thông tin ra ngoài bằng message. Kiểm số liệu và hash có trong [validation.json](runs/source-final-001/validation.json). Còn OPEN do cần tác giả/giữ ngoài được ghi rõ, không chuyển thành điều đã kiểm và không giao reviewer chịu trách nhiệm kiểm thay người làm.
