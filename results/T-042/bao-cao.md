# Kết quả T-042 — đối chiếu baseline Nezha-OB

Ngày 24/10/2026. Codex làm; Claude phản biện. **Chờ phản biện, chưa nghiệm thu.**

Đã xác nhận hai quy ước metric làm đổi điểm và hạng trong M4, nhưng cả ba nhánh thay đổi đều không sửa được độ lệch chung. Không phát hiện adapter vi phạm hợp đồng trên 22 dev đã kiểm. Các khác biệt giữa M4, code cùng tên của tác giả và pipeline MicroRank là có thật; chương trình sinh hai bảng công bố vẫn chưa định danh đủ để quy hết chênh lệch.

Nguồn số chính: [summary](runs/evaluate-001/summary.json), con trỏ `/summary`, `/contrasts`, `/by_cell`, `/per_case`; [phân xử](phan-xu.json) lưu từng giả thuyết và phần thiếu. [Đối chiếu nguồn](doi-chieu.md) tách bài–code–repo. Hash/revision tại [nguồn](nguon.json), chuỗi MicroRank tại `runs/reuse-audit-001/micro-source-checks.json`.

## 1. Kết quả 2×2 trên cùng đầu vào

| Nhánh | Metric/đếm | Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 |
|---|---|---:|---:|---:|---:|---:|
| S0 | 3σ/events | 0.318182 | 0.681818 | 0.840909 | 0.537542 | 0.597265 |
| S1 | 3σ/channels | 0.242424 | 0.666667 | 0.848485 | 0.500295 | 0.572510 |
| S2 | P95/events | 0.181818 | 0.613636 | 0.659091 | 0.417776 | 0.446064 |
| S3 | P95/channels | 0.204545 | 0.500000 | 0.693182 | 0.409994 | 0.450823 |

Đủ 22 ca/nhánh đều OK; tập ứng viên10. Trace, log, cửa sổ, alias, dữ liệu thiếu và evaluator giữ nguyên. Hòa tính kỳ vọng P3; đã tính độc lập đủ 88 ca–nhánh. S0 khớp score, thứ tự, candidate và tie của T-026 ở từng ca; S0/S1 khớp 44 khoảng hạng root lịch sử T-032. Nguồn: summary `/checks`, diagnosis `/checks`; danh sách chốt `runs/full-001/diagnosis-list.json`.

| Phép đổi | MRR tăng / giữ / giảm theo ca | ΔMRR | Khoảng95% theo ô |
|---|---:|---:|---:|
| S1-S0 | 7 / 9 / 6 | -0.037247 | [-0.148360; 0.075975] |
| S2-S0 | 1 / 6 / 15 | -0.119766 | [-0.196744; -0.053062] |
| S3-S0 | 4 / 2 / 16 | -0.127548 | [-0.282391; 0.023578] |

Bootstrap ghép cặp theo 13 ô, B=10.000, seed20261005; dùng Python Random, cùng mẫu cho các nhánh, không phải khôi phục byte stream CI cũ của T-026. Khoảng chỉ mô tả tập ô dev nhỏ đã phân tích nhiều lần. Không dùng việc khoảng chứa0 làm bằng chứng tương đương. Interaction ở Hit@1 là 0.098485 và MRR 0.029466 (`/interaction`): không cộng hai main effect để dự đoán S3.

## 2. Chuỗi số phân xử tác động và phản chứng

**Đếm events → channels.** Ca `dev-396c8dbf7d` (email CPU-consumed): cùng ngưỡng/count, root metric/trace/log=31/1/0→11/1/0, tổng32→12; checkout=37/1/0→10/1/0, tổng38→11. Root từ hạng 2 lên1. Hai bên cùng 16 kênh; breadth theo kênh đảo ưu thế persistence theo mẫu. `emailservice_CpuUsage-m` có threshold0,1557827415892134/count4/vote4→1; `checkoutservice_MemoryUsage-Mi` threshold22,45703125/count5/vote5→1. Nguồn: diagnosis S0/S1 của ca, `/diagnosis/metrics/<channel>` và `/diagnosis/scores/<service>`; summary `/per_case/4`. Đây là tác động phép đếm trên điểm; chưa chứng minh checkout chờ root hay tín hiệu đã lan.

Phản chứng: `dev-3e27669440` (ad CPU-contention), S0 root33>frontend29, S1 root10<frontend12. Các kênh CPU/memory root cùng count5 mất ưu thế khi còn một phiếu/kênh; root từ1 xuống2. Nguồn diagnosis của ca `/diagnosis/scores/{adservice,frontend}`, metric `adservice_CpuUsage-m`, `adservice_MemoryUsage-Mi`; summary `/per_case/6`.

Ngay cùng ô shipping CPU-contention, `dev-14701a3bbb` giữ hạng 1 ở S1, còn `dev-7d3c2fe6d1` từ1 thành hòa1–3: shipping/currency/payment cùng9. Không gọi channels là lọc sạch tín hiệu giả. Hai ca CPU-consumed được sửa top1 ở hai ô đơn ca; ô recommendation CPU-consumed có hai ca và không nhánh nào top1. Nguồn `/by_cell` và `/per_case`, các diagnosis tương ứng.

**Ngưỡng 3σ → P95.** Cả 3.630 kênh–ca có 5 mẫu N; threshold giảm ở 3.030, bằng 600, không tăng; count tăng 1.202 và giữ 2.428. Tổng metric events 1.201→3.058. Nguồn `runs/reuse-audit-001/m4-mechanism.json#/P95_vs_sigma_threshold`, `/P95_vs_sigma_count`, `/total_metric_votes`. Sự chênh nhỏ của threshold chỉ có tác động khi đổi membership vượt ngưỡng; không quy mọi threshold thấp hơn thành nguyên nhân. Với 5 mẫu N và population std, số học thực cho max(N)−mean(N)≤2σ; vì vậy mean+3σ nằm trên hoặc bằng max(N), còn P95 nằm trong miền N. Điều này giải thích chiều tăng count trong phép đổi hiện tại. Nó chưa chứng minh nền ngắn là nguyên nhân của chênh với chương trình tác giả.

Ca shipping `dev-14701a3bbb`: root28→35, checkout12→36, root xuống2. Checkout PodServerLatencyP90 threshold0,9918928459844676→0,7324999999999999, count1→5; root CpuUsage threshold0,7961282448115465→0,6507533271169045 nhưng count vẫn5. Đầu vào→threshold→count→score→rank chỉ rõ bước đảo hạng. Cùng ô, `dev-7d3c2fe6d1` vẫn top1 ở S2; không suy P95 luôn ưu tiên competitor. Nguồn hai diagnosis S0/S2 của ca và `/per_case/0`, `/per_case/16`.

P95 không phải chỉ thêm tín hiệu của root: ca network-delay `dev-607751ac0a` root score0→4 nhưng vẫn cuối, vì competitor cũng tăng; không thêm bằng chứng phân biệt đủ để root đứng đầu. Đây là phản chứng cho suy luận “thêm alert sẽ sửa RCA”.

Đối chứng không nhãn: fixture N=A/constant abstain; hoán vị hàng/cột và locator không vào core đạt. Pilot thật hoán vị giữ score/rank/tie/count. N1–N2 thật ở metric ordinal2/3 và trace/log chia trung điểm vẫn có điểm metric dương ở nhiều service (cao nhất checkout16); chưa có root để chấm và không được dùng làm tỷ lệ false-positive hay xác nhận N sạch. Nguồn `runs/fixtures-001/checks.json`, `runs/pilot-001/{permutation,normal-control}.json`.

## 3. Theo đủ ô và từng ca

Nguồn toàn bộ hai bảng sau: summary `/by_cell` và `/per_case`; không chọn ca theo chiều hiệu ứng. Hạng có dạng a–b là nhóm hòa.

| Ô root × lỗi | n | S0 Hit@1 | S1 | S2 | S3 |
|---|---:|---:|---:|---:|---:|
| adservice × cpu_contention | 1 | 1.000000 | 0.000000 | 1.000000 | 0.000000 |
| checkoutservice × exception | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| checkoutservice × network_delay | 2 | 0.500000 | 0.000000 | 0.500000 | 0.500000 |
| checkoutservice × return | 2 | 0.000000 | 0.000000 | 0.000000 | 0.250000 |
| emailservice × cpu_consumed | 1 | 0.000000 | 1.000000 | 0.000000 | 1.000000 |
| emailservice × network_delay | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| frontend × return | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| paymentservice × cpu_contention | 2 | 1.000000 | 1.000000 | 0.500000 | 0.000000 |
| productcatalogservice × exception | 1 | 1.000000 | 0.000000 | 0.000000 | 0.000000 |
| recommendationservice × cpu_consumed | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| recommendationservice × network_delay | 2 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| shippingservice × cpu_consumed | 1 | 0.000000 | 1.000000 | 0.000000 | 1.000000 |
| shippingservice × cpu_contention | 2 | 1.000000 | 0.666667 | 0.500000 | 0.500000 |

| Ca dev | Root / lỗi | S0 hạng | S1 | S2 | S3 |
|---|---|---:|---:|---:|---:|
| dev-14701a3bbb | shippingservice / cpu_contention | 1 | 1 | 2 | 1 |
| dev-1ac905bc95 | frontend / return | 5–6 | 4–6 | 8–9 | 9 |
| dev-27252dca60 | productcatalogservice / exception | 1 | 2 | 2–3 | 5–8 |
| dev-2bfc97b01e | checkoutservice / network_delay | 1 | 2–3 | 1 | 1 |
| dev-396c8dbf7d | emailservice / cpu_consumed | 2 | 1 | 3 | 1 |
| dev-3b92690644 | checkoutservice / return | 2 | 2 | 3 | 3 |
| dev-3e27669440 | adservice / cpu_contention | 1 | 2 | 1 | 2 |
| dev-515c5f2190 | recommendationservice / cpu_consumed | 2 | 2 | 2–3 | 5 |
| dev-5467884de4 | recommendationservice / network_delay | 5 | 4–5 | 7 | 7–9 |
| dev-55f99f3e0a | checkoutservice / exception | 2 | 2 | 5–6 | 5 |
| dev-5ada15752d | frontend / return | 6 | 6 | 7 | 7 |
| dev-607751ac0a | checkoutservice / network_delay | 9–10 | 9–10 | 10 | 10 |
| dev-63c30faf34 | recommendationservice / network_delay | 8–10 | 8–10 | 9 | 9 |
| dev-6c9afc9822 | emailservice / network_delay | 4 | 2–3 | 7 | 4–5 |
| dev-70629373f9 | paymentservice / cpu_contention | 1 | 1 | 2 | 2–3 |
| dev-7b7c973198 | emailservice / network_delay | 3 | 3–5 | 8 | 6–8 |
| dev-7d3c2fe6d1 | shippingservice / cpu_contention | 1 | 1–3 | 1 | 2–3 |
| dev-8ecd9880ed | checkoutservice / return | 4–5 | 3–5 | 2 | 1–2 |
| dev-95e164235f | paymentservice / cpu_contention | 1 | 1 | 1 | 2–3 |
| dev-9b9397a4dc | recommendationservice / cpu_consumed | 2–3 | 4–5 | 3–4 | 4 |
| dev-9fd793feb7 | shippingservice / cpu_consumed | 2 | 1 | 2 | 1 |
| dev-b0f8b2e3ac | checkoutservice / exception | 3 | 2 | 3 | 2–3 |

CPU-contention có 5 ca: S0 chắc top1 cả 5; S1 còn 3 chắc, một hòa ba, một sai; S2 còn 3 chắc; S3 chỉ 1 chắc. Return vẫn không có top1 chắc: S3 chỉ đưa một ca vào hòa đầu. Các ô đơn ca không cho khái quát loại lỗi. Không có đối chứng đúng trong ô thì ghi đúng thiếu; không dựng thêm ca đúng.

## 4. MicroRank: đã có phân xử một phần

T-042 không chạy lại MicroRank. Nguồn gốc được kiểm qua manifest-final/review, core manifest,88 observed và352 metadata của 22 ca×4 nhánh, cùng22 case analysis: tổng465 kiểm file. Nguồn và con trỏ trong `runs/reuse-audit-001/micro-source-checks.json`. G2-H01/H02 và các can thiệp bộ chia trước đó vẫn có giá trị đúng phạm vi; khảo sát A.3 không nên được đọc thành chưa có công việc phân xử nào.

MicroRank main có0/22 top1. Thay bộ chia theo công thức bài với span đầu do repo quy ước cho7/22 top1 ở mo15/mo1p50; đây không phải full pipeline tác giả. Đổi đếm phủ M-C1, bỏ trọng số A′ và đếmDStar M-D cho sốtop1 khác nhau, không cộng vào hiệu ứng bộ chia vì chúng không cùng nhóm trace. Nguồn: `results/T-034/ban-do-g2.json` dòng G2-H01/H02, `/theo_o/tables/Nezha-OB/microrank_full`; bản gốc đã khớp manifest.

Nhánh ghép mo15c1 minh họa cơ chế tính toán và tính không đồng nhất: cùng ô recommendation CPU-consumed, `dev-515c5f2190` từ sai thành hạng 1 với A/N296/135 và root có trong cả296 trace A; `dev-9b9397a4dc` còn hạng 9 với A/N2/418, root operation thuộc anomaly_missing. Ca sau lại đúng trong mo1p50c1, nên kết luận phải nêu đúng nhánh. Cùng ô checkout exception, `dev-55f99f3e0a` đạt1 và `dev-b0f8b2e3ac` còn 3; root có8/33 so với1/47 trace A/N, dù đều support both. Nguồn dẫn xuất đã hash: micro-source-checks `/cases/7`, `/cases/19`, `/cases/9`, `/cases/21`, `/branches/{sham,mo15c1}/root_cells`; file nguồn tương ứng nằm tại `t32/micro-analysis-001/cases/Nezha-OB-<id>.json` trong gói T-032. Cả bốn sham đều sai; không có nhóm main Hit1 đúng để đối chiếu.

Đủ bằng chứng cho tác động partition/coverage/weight lên phép tính của repo. Chưa có chuỗi xác nhận chương trình Table3, normal source, preprocessing và evaluator từng ca. Thiếu clone upstream đầy đủ ở đường scratchpad cũ cũng giới hạn việc tái kiểm whole pipeline; hàm lõi trích vẫn đúng hash. Không gọi tất cả phần còn lại là lỗi dữ liệu hoặc lỗi PageRank.

## 5. Chênh lệch công bố được phân loại tới đâu

| Nhóm | Bằng chứng T-042 | Phần chưa trả lời |
|---|---|---|
| Lỗi cài đặt/đầu vào repo | Chưa phát hiện vi phạm Q84/Q85 trong22dev; S0 exact và raw-window audit độc lập | Không là chứng minh không còn mọi bug; cần hợp đồng tác giả để xác định tương đương |
| Khác giao thức có chủ đích | Q84/Q85: Time/alias/U10/165kênh/ordinal/loạiNode; start-vs-end, tie/mẫu số khai rõ | Chưa đo riêng tác động Node/nền/cửa sổ hoặc ánh xạ instance |
| Giả định/cách tính M4 | 2×2 cô lập threshold/count; có chuỗi đảo hạng và phản chứng ngay cùng ô | Không định danh chương trình sinh0,91; không xác nhận cơ chế vật lý |
| Giới hạn dữ liệu/phiên bản | Thiếu statusCode, cadence và provenance đồng hồ có hệ quả đã biết | Chưa có phép matched-program/release để quy độ lệch cho release hoặc dữ liệu |
| Chưa phân xử | Code/config/cohort/preprocessing/evaluator sinhTable2/Table3 | Cần nguồn tác giả và pipeline dev an toàn; không tự mở test |

Cách chấm không đủ giải thích top1 S0: native/lạc quan/bi quan đều7/22; bốn main baseline đều22OK nên loạiERROR không đổi mẫu số tại bảng này. SimpleRCA chỉ khác cohort bị chặn ở41/56=0,7321 **khi** dev thuộc đúngfull56 và cùngTop1. MicroRank vẫn có phản ví dụ số học23/56≈41,07%. Không dùng cận như kết quả test. Nguồn summary `/summary/S0`, `/conditional_cohort_bound`; định nghĩa và nguồn Table3 ở doi-chieu §4.

## 6. Hệ quả cho P4, P6/P7 và quan sát FlashTicket

Đây là đề xuất dùng bằng chứng, không sửa trạng thái hoặc kết luận tài liệu cũ.

| Dòng G2 | Giữ căn cứ nào / giới hạn mới |
|---|---|
| H01/H02 | Giữ các can thiệp repo đúng nhánh. Chưa gán cho toàn MicroRank tác giả hoặc cộng các hiệu ứng khác partition |
| H06 | Giữ quan sát vị trí tín hiệu phía gọi và phép ánh xạ tính toán; 2×2 không đo lợi ích đồ thị hay chứng minh chờ/lan vật lý |
| H07 | Giữ phản chứng thiếu mọi đáp ứng ở return; M4 thay metric chưa tạo top1 chắc cho nhóm này. Root khôngtop1 không đồng nghĩa dữ liệu không có thông tin |
| H08 | Giữ kết luận riêng M4: events vừa phân biệt vừa có thể đảo sai; channels không chữa chung. P95 bổ sung thêm độ nhạy, không làm thành hạn chế của mọi code SimpleRCA |
| H16 | Main22OB khôngERROR, candidate M4 vẫn10; không lấy lỗiTT hoặc lỗiguard làm mẫu sốmainOB. Hòa có tác động ở nhánh đổi nhưng không sửa gapS0 |
| H17 | M5 không chứng minh lan; chưa chọn cơ chế P6 bằng việc dẫn mã này |
| H18 | M0 vẫn là chưa phân loại, không được đổi thành nguyên nhân còn lại |
| H19 | Giữ thiếu trường/cadence/clock đã xác nhận; chưa quy phần chênh định lượng cho dataset |

Quan hệ có thể đặt tín hiệu span phía gọi lên đích và phân biệt phạm vi của cùng triệu chứng; đủ lý do đề xuất ứng viên từ bằng chứng vị trí đã có. M4 không dùng cạnh, còn code orig fallback có parent-child và MicroRank dùng cạnh để tính trọng số. Chưa có so matched-information bỏ quan hệ và quy tắc cùng đồ thị cho một thiết kế mới, nên T-042 không xác nhận lợi ích đồ thị hoặc chọn thành phần P6.

Đề nghị Minh giữ baseline hiện hành với tên/giới hạn đúng, chưa thay bằng S1/S2/S3 hoặc coi0,91 là mốc tái lập đạt. Việc chọn baselineP7 và mục tiêu cải thiệnNezha cần quyết trong thiết kế sau đối chiếu này. Có thể thiết kế ứng viên trên dev với giới hạn công khai; không dùng OPEN làm căn cứ đã xác nhận hoặc hiểu T-042 đã trả lời xongRQ2.

Hệ quả P9/FlashTicket: cần thời gian nguồn và đơn vị duration rõ; traceID/spanID/parent/span.kind/instance; log liên kết trace khi instrumentation có thể ghi; ownership host–pod–service; nhịp metric, giá trị thiếu và provenance preprocessing; lưu N đủ dài cùng metadata tải/recovery. Collector không tái tạo status, ID hay normal đã không được instrumentation/thu thập lưu. Những yêu cầu này phục vụ quan sát và so sánh, chưa chứng minh thêm trường sẽ tăng RCA. Không sửa chuẩn quan sát hệ thống trong T-042.

## 7. Phần nối tiếp cần Minh quyết

1. **Nguồn tác giả:** code/revision/config tạoTable2 vàTable3, danh sáchfull56 cùng dự đoán/score/tie/status từng ca dev; preprocessing CSV→parquet, quy tắcN/A/normal và evaluator. Nguồn cung cấp: tác giả/artifact maintainer, Minh quyết xin nguồn; không tự gửi thư hoặc tải.
2. **SimpleRCA:** entrypoint đã biết là orig/main.py→NezhaRCA, Python≥3.13/rcabench-platform/sáuparquet. Cần định danh schema/units/metric selection/windowing của lượt bảng; license upstream cònOPEN. Không chạy CLI mặc định có loader toàn tập. Thiết kế dev reader phải từ chối ca ngoàiallowlist trướcI/O, lọc miền thời gian trước trả giá trị, bỏ locator/root/fault khỏicore.
3. **MicroRank:** cần upstream preprocessing/detector/normal contract đúng bảnNezha đã dùng; hàm PageRank/spectrum trích chưa đủ xác định đầu vào. Không tự lấy span đầu làmfrontend-server root hoặc gọi nhánh thay partition là tái lập.
4. **Phép so nối tiếp:** sau khi định danh hợp đồng và được duyệt, chạy đúngprogram tác giả trên22dev, lưu trung gian trướcnhãn; so cùnginput vớiM4/repo rồi đổi từng yếu tố. Nếu cần patchsrc hoặc đổi giao thức, trình patch/file và phạm vi chạy lại; T-042 không cấp quyền đó.
5. **Chi phí chưa kiểm:** tối thiểu một phiên riêng cho dựng/kiểm hợp đồng; ước lượng công3–5giờ tương tự góiđọc này chưa gồm chờ tácgiả, không là cam kết. Chưa đủ thông tin RAM/thời gian/đĩa hoặc kích thước nguồn để cấp ngân sách cài/tải/chạy. Sau có schema/code/normal source, trình sốbyte và pilot khôngnhãn; không lấy5,05s/ca của bài làm ngân sách. Nếu chỉ cóprogram hoặc dữ liệu toàntập mà khôngcódev guard, phần thực thi vẫn chưa được duyệt.

## 8. Kiểm, chi phí và bàn giao

Đã kiểm nguồn566 mục ở nguon.json và chuỗi MicroRank465file riêng;22 fixture;22 window audit;88 phiếu/score độc lập;22S0 exact;88 độ đo P3/độc lập;44 khoảng hạng lịch sửS0/S1. Không chạy lại MicroRank, khôngtest/giữngoài/tảithêm/src/commit/push. Mọi đầu ra chỉ là thống kê/ngưỡng/phiếu/hạng/provenance, khôngpayloadraw.

Pilot5,679s + full161,136s (full dùng lại4pilot) cho tổngwall166,816s của hai lượt phươngpháp và audit gắn kèm; không cộng pilot theo từng tham chiếu. PeakRSS lấy mẫu329,781 MiB, có thể bỏ đỉnh ngắn; không nhận là upperbound RAM. Đĩa và hash cuối tại manifest.json. Các lượt kiểm đọc và nguồn có chi phí riêng; không dùng thời gian này so tốc độ với bài.

Trong lúc full chạy, evaluator được nối vào script kiểm độc lập sau khi worker đãimport; các hàm kiểm và phương pháp đang chạy không đổi. Snapshot byte tại full-001/source-kiem_doc_lap-at-start.py khớp hash đầu lượt; script nguồn trước khi thêm tổng hợp cũng được giữ. LOG ghi đủ thời điểm, lỗi lệnh chỉ đọc và lý do. Không sửa config/hash lịch sử để làm khớp bản mới.

Nguồn và đề xuất đủ bàn giao phần task này; câu hỏi toàn bộ gap và quyết định comparator vẫnOPEN. Prompt Claude nằm ở cuốiLOG theo mẫu hiện hành. Chưa có phản biện chính thức của Claude trong phiên này; Minh quyết nghiệm thu hoặc phần bổ sung.
