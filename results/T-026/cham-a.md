# T-026 — Xếp hạng tầng 1 chế độ (a) trên Nezha-OB dev

Ngày 07/10/2026. Codex làm, Claude phản biện. Chỉ 22 ca dev, không mở test. Mục tiêu RQ1/DT18-NV3: xếp service gốc khi biết cửa sổ. Không kết luận về giá trị đồ thị.

Trên bảng chính, BARO có Hit@1 cao nhất trong bốn phương pháp được chạy (0,3636); SimpleRCA có Avg@5 cao nhất (0,6318). Với MRR (mean reciprocal rank — trung bình nghịch đảo hạng), SimpleRCA đạt 0,5375 và BARO đạt 0,5270. Khi đổi mốc ca tranh chấp ở bảng A, BARO đạt 0,5497 còn SimpleRCA đạt 0,5247: thứ tự theo MRR đổi chiều. Vì vậy phép so này có điều kiện theo mốc; không gọi một phương pháp tốt hơn trên mọi độ đo. Khoảng bootstrap ghép cặp BARO−SimpleRCA trong bảng chính ở Hit@1, Avg@5 và MRR đều chứa 0. Nguồn: `cham-a.json → tables.main/sensitivity_A.methods.*.summary.main` và `tables.*.bootstrap.hieu`; xem bảng đầy đủ và các giới hạn dưới đây.

MicroRank có Hit@1, Hit@5 và MRR thấp hơn kỳ vọng xếp đều trên O=U=10 ở cả bốn bảng. Đầu danh sách tập trung vào currencyservice/cartservice/productcatalogservice; chưa xác định nguyên nhân. TraceRCA chưa phân biệt rõ với mức ngẫu nhiên qua các khoảng bootstrap hiện có của bảng chính. Nguồn: `cham-a.json → tables.*.methods.*.summary.main`, `tables.main.bootstrap.phuong_phap` và các record `per_case.*.source_path → entity_ranking`; diễn giải cùng các nguyên nhân khả thi ở mục dưới.

## Nguồn và lựa chọn đã khóa

Mọi số chấm trong báo cáo lấy từ `results/T-026/cham-a.json`, trường `tables`; mỗi ca có `source_path` và hash bản ghi. Manifest `ban-ghi-dua-vao-cham.json` được chốt lúc 2026-10-07T12:32:33.422894+00:00 (UTC), trước evaluator thật. Danh sách đã khai trong `runs/full-001/plan.json`. Không đổi cấu hình hoặc chọn lại bản ghi theo điểm.

Q-84 giữ ba bảng mốc; Q-85/WHY-37 khóa alias tường minh, U=10, 16 kênh pod + 5 front, loại Node*, giữ lặp. BARO dùng 5N+5A ordinal; SimpleRCA dùng arrays native, không điền. Bảng cắt N chỉ nhận end < t−41 s ngày 22/08 và end < t−32 s ngày 23/08, giữ A native; không dịch clock hoặc tích chéo với các mốc Q-84. BARO trong bảng này tham chiếu chính vì không dùng trace.

CIRCA và TORAI B là UNSUPPORTED theo Q-85, không gọi phương pháp. Số 0 của hai dòng này là quy tắc mẫu số khi không hỗ trợ dữ liệu, không phải đo chất lượng chẩn đoán. Seed/hashseed null; các phương pháp chạy có hashseed 0. Kiểm MicroRank hashseed 1 và đổi locator đã có trong pilot cùng hash, không chạy lại.

## Giới hạn đã khai trước

Nezha-OB đo metric khoảng 60 s, chỉ 5 điểm mỗi phía; RE2-TT đo 1 s. Cùng cửa sổ ±300 s không có nghĩa cùng cadence, số điểm hoặc độ phủ trace/log. Khác biệt với T-024 không được quy riêng cho đổi hệ thống. Nền sạch, recovery, thời điểm tiêm thật, đồng bộ tuyệt đối và lệch trace theo ngày còn OPEN. Hàng lặp không là quan sát độc lập; hull/giây có dòng không là quan sát liên tục.

## Quy tắc chấm

Các độ đo bảng chính dùng kỳ vọng khi thứ tự trong nhóm khóa bằng nhau được hoán vị đều. Root vắng và mọi trạng thái khác OK tính 0, giữ trong mẫu số. Retrieval@K=Hit@K; Rerank@1(K)=tổng Hit@1/tổng Hit@K, mẫu số 0 là N/A. Cận hòa chỉ cho độ đo đơn điệu, không cho Rerank. Bảng RCAEval dùng thứ tự gốc và báo riêng, không dùng để kết luận khi có hòa.

Bootstrap lấy lại các ô root × fault thực tế, mỗi ô mang toàn bộ ca; B=10.000, seed=20261005, khoảng phân vị 95%, mẫu ghép cặp cho mọi phương pháp. Rerank tính lại trên mỗi mẫu, đếm N/A. Không chép 10 ô × 3 ca của RE2. Khoảng chỉ nói về các ô dev này, không đại diện cho test.

## Độ dài nền trace thực và điểm dừng MicroRank

Nguồn `runs/session-005/trace-N-coverage.json`, từng mã ca trong `cases`; đây là metadata đầu vào, không là kết quả xếp hạng. Bảng ghi N chia theo thời điểm kết thúc của MicroRank/TraceRCA. SimpleRCA chia theo bắt đầu và cũng cắt theo end; không gọi các số này là độ dài train của SimpleRCA.

Khoảng N cho phép là 300 s ở chính và 259/268 s sau cắt 41/32 s. Khoảng đó là biên cửa sổ; end hull/start hull chỉ là max−min timestamp của span thực sự có. Hull và số span lặp không chứng minh độ phủ liên tục, nền sạch hoặc số mẫu độc lập.

| Mã ca | Cắt s | N chính biên s | N chính end hull s | N cắt biên s | N cắt end hull s | N cắt start hull s | Span N chính | Span N cắt | MicroRank cắt N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dev-14701a3bbb | 41 | 300 | 88.6578 | 259 | 47.6585 | 47.6939 | 33470 | 18311 | OK |
| dev-1ac905bc95 | 32 | 300 | 52.8378 | 268 | 20.6441 | 20.6459 | 19751 | 7849 | OK |
| dev-27252dca60 | 32 | 300 | 60.2120 | 268 | 28.1497 | 28.1682 | 25037 | 11561 | OK |
| dev-2bfc97b01e | 32 | 300 | 84.2220 | 268 | 52.2206 | 52.2218 | 31749 | 19537 | OK |
| dev-396c8dbf7d | 32 | 300 | 80.5135 | 268 | 48.5154 | 48.7562 | 31951 | 19247 | OK |
| dev-3b92690644 | 32 | 300 | 68.5077 | 268 | 36.4990 | 36.5749 | 26329 | 14017 | OK |
| dev-3e27669440 | 32 | 300 | 67.1166 | 268 | 35.1103 | 35.1120 | 25764 | 12486 | OK |
| dev-515c5f2190 | 32 | 300 | 81.7052 | 268 | 49.9070 | 49.9697 | 32892 | 19999 | OK |
| dev-5467884de4 | 41 | 300 | 96.9399 | 259 | 55.9427 | 55.9519 | 37756 | 22183 | OK |
| dev-55f99f3e0a | 32 | 300 | 41.1417 | 268 | 9.4113 | 9.4730 | 16158 | 4054 | OK |
| dev-5ada15752d | 41 | 300 | 47.6534 | 259 | 6.6538 | 6.6580 | 18497 | 2242 | ERROR |
| dev-607751ac0a | 41 | 300 | 95.8200 | 259 | 54.8128 | 54.8164 | 38966 | 21715 | OK |
| dev-63c30faf34 | 32 | 300 | 81.0123 | 268 | 49.0341 | 49.0348 | 32101 | 19006 | OK |
| dev-6c9afc9822 | 41 | 300 | 88.5717 | 259 | 47.6053 | 47.6105 | 34960 | 18846 | OK |
| dev-70629373f9 | 41 | 300 | 58.6575 | 259 | 17.6545 | 17.6700 | 23054 | 7375 | OK |
| dev-7b7c973198 | 32 | 300 | 69.2500 | 268 | 37.0805 | 37.1594 | 27490 | 14329 | OK |
| dev-7d3c2fe6d1 | 32 | 300 | 74.8609 | 268 | 42.8619 | 42.8649 | 30522 | 17166 | OK |
| dev-8ecd9880ed | 41 | 300 | 90.5051 | 259 | 49.4994 | 49.4972 | 36362 | 20272 | OK |
| dev-95e164235f | 32 | 300 | 85.5078 | 268 | 53.9492 | 53.9487 | 34784 | 21334 | OK |
| dev-9b9397a4dc | 41 | 300 | 83.7597 | 259 | 43.0042 | 43.0073 | 21736 | 13258 | OK |
| dev-9fd793feb7 | 32 | 300 | 56.1475 | 268 | 24.1397 | 24.1409 | 22533 | 9715 | OK |
| dev-b0f8b2e3ac | 41 | 300 | 53.5603 | 259 | 12.5439 | 12.5501 | 20859 | 5063 | OK |

MicroRank cắt N có 1/22 ca ERROR; mã ca: dev-5ada15752d. Nguồn trạng thái `cham-a.json → tables.trace_guard.methods.microrank_full.per_case` và bản ghi nguồn mỗi ca. Mọi ERROR được giữ trong mẫu số; không bỏ ca hoặc sửa phương pháp để cứu kết quả.

Nhánh MicroRank dừng ở ERROR đầu tiên theo Q-77/WHY-31. Minh duyệt có điều kiện tiếp tục 10 lượt chưa chạy sau khi chứng minh cắt N đúng, A giữ nguyên và membership ns/µs khớp. Bằng chứng `runs/session-005/microrank-stop-evidence-002.json` và quyết định nguyên văn trong LOG; lượt ERROR ban đầu và các kết quả sau điểm dừng đều được giữ. Không đổi ngưỡng, cửa sổ, seed hoặc dữ liệu vì kết quả.

Bảng độ nhạy cắt N có điều kiện vì phần trace N quan sát có thể quá ngắn, dù biên cho phép vẫn 259/268 s. ERROR do thiếu mẫu nền là hạn chế của phép cắt với hợp đồng MicroRank, không là phép đo riêng chất lượng xếp hạng trên ca đó. Đổi dấu trong bảng này phải đọc cùng độ phủ và trạng thái, không quy riêng cho khả năng chẩn đoán hoặc chứng minh đồng hồ đã đồng bộ.

Chi tiết ERROR và số operation có A nhưng <2 span N sau cắt; đường dẫn/từng operation có trong coverage JSON, thông điệp lỗi giữ từ bản ghi:

| Mã ca | Lỗi gốc | Operation N cắt <2 | Span N chính / op min–max | Span N cắt / op min–max | A giữ nguyên |
| --- | --- | --- | --- | --- | --- |
| dev-5ada15752d | ValueError: Normal std undefined (<2 spans) | 21 | 9–29 | 1–1 | True |

## Chính — 22 ca theo inject_time

Nguồn: `cham-a.json → tables.main`. 22 ca, 13 ô; cỡ ô: 1 ca × 4 ô, 2 ca × 9 ô.

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | Avg@5 | MRR | NDCG@5 | Retrieval@10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636 | 0.5455 | 0.7273 | 0.5727 | 0.5270 | 0.5507 | 1.0000 | 0.5000 | 0.3636 |
| SimpleRCA M4 | 0.3182 | 0.6818 | 0.8409 | 0.6318 | 0.5375 | 0.5973 | 1.0000 | 0.3784 | 0.3182 |
| MicroRank full | 0.0000 | 0.0909 | 0.3636 | 0.1182 | 0.1701 | 0.1530 | 1.0000 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.1061 | 0.4545 | 0.5227 | 0.3682 | 0.3297 | 0.3325 | 0.9545 | 0.2029 | 0.1111 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

| Phương pháp | OK | NO_EVIDENCE | ERROR | UNSUPPORTED | TIMEOUT |
| --- | --- | --- | --- | --- | --- |
| BARO | 22 | 0 | 0 | 0 | 0 |
| SimpleRCA M4 | 22 | 0 | 0 | 0 | 0 |
| MicroRank full | 22 | 0 | 0 | 0 | 0 |
| TraceRCA finite | 22 | 0 | 0 | 0 | 0 |
| CIRCA | 0 | 0 | 0 | 22 | 0 |
| TORAI B | 0 | 0 | 0 | 22 | 0 |

MicroRank top-11 dẫn xuất từ cùng lượt: hit@1=0.0000, hit@3=0.0909, hit@5=0.2273, mrr=0.0598, avg@5=0.0909. Không chạy thêm.

Cận bi quan–lạc quan do hòa (không là CI), nguồn `tables.main.methods.*.summary.main.can_bi_quan/can_lac_quan`:

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636–0.3636 | 0.5455–0.5455 | 0.7273–0.7273 | 0.5270–0.5270 | 0.5507–0.5507 | 0.5727–0.5727 | 1.0000–1.0000 |
| SimpleRCA M4 | 0.3182–0.3182 | 0.6818–0.6818 | 0.8182–0.8636 | 0.5311–0.5441 | 0.5845–0.6100 | 0.6182–0.6455 | 1.0000–1.0000 |
| MicroRank full | 0.0000–0.0000 | 0.0909–0.0909 | 0.3636–0.3636 | 0.1686–0.1717 | 0.1530–0.1530 | 0.1182–0.1182 | 1.0000–1.0000 |
| TraceRCA finite | 0.0909–0.1364 | 0.4545–0.4545 | 0.5000–0.5455 | 0.3163–0.3481 | 0.3141–0.3544 | 0.3545–0.3818 | 0.9545–0.9545 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |

Khoảng bootstrap 95% (Hit@1; MRR; Rerank K5), nguồn `tables.main.bootstrap.phuong_phap`:

| Phương pháp | Hit@1 CI | MRR CI | Rerank K5 CI | Rerank K5 N/A / 10000 |
| --- | --- | --- | --- | --- |
| BARO | 0.1364–0.6190 | 0.3460–0.7232 | 0.2308–0.7500 | 0 |
| SimpleRCA M4 | 0.0909–0.5716 | 0.3800–0.7202 | 0.1111–0.6667 | 0 |
| MicroRank full | 0.0000–0.0000 | 0.1395–0.2087 | 0.0000–0.0000 | 17 |
| TraceRCA finite | 0.0000–0.2540 | 0.2085–0.4788 | 0.0000–0.4615 | 0 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |

CI bootstrap ghép cặp 95% cho hiệu a−b; nguồn `tables.main.bootstrap.hieu`:

| Cặp | Hit@1 CI | Avg@5 CI | MRR CI |
| --- | --- | --- | --- |
| BARO − SimpleRCA M4 | -0.1500–0.2400 | -0.2000–0.0409 | -0.1468–0.1091 |
| BARO − MicroRank full | 0.1364–0.6190 | 0.1666–0.7091 | 0.1554–0.5653 |
| BARO − TraceRCA finite | 0.0000–0.5333 | -0.0459–0.4286 | 0.0051–0.3879 |
| SimpleRCA M4 − MicroRank full | 0.0909–0.5716 | 0.2524–0.7429 | 0.1952–0.5569 |
| SimpleRCA M4 − TraceRCA finite | -0.0870–0.5200 | 0.0150–0.5000 | 0.0080–0.4113 |
| MicroRank full − TraceRCA finite | -0.2540–0.0000 | -0.4714–-0.0478 | -0.3037–-0.0427 |

## Độ nhạy A — 22 ca, một ca dùng inject_timestamp

Nguồn: `cham-a.json → tables.sensitivity_A`. 22 ca, 13 ô; cỡ ô: 1 ca × 4 ô, 2 ca × 9 ô.

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | Avg@5 | MRR | NDCG@5 | Retrieval@10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.4091 | 0.5455 | 0.7273 | 0.5818 | 0.5497 | 0.5675 | 1.0000 | 0.5625 | 0.4091 |
| SimpleRCA M4 | 0.3182 | 0.6364 | 0.7955 | 0.6000 | 0.5247 | 0.5716 | 1.0000 | 0.4000 | 0.3182 |
| MicroRank full | 0.0000 | 0.0909 | 0.3636 | 0.1182 | 0.1701 | 0.1530 | 1.0000 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.0606 | 0.4545 | 0.5227 | 0.3591 | 0.3069 | 0.3157 | 0.9545 | 0.1159 | 0.0635 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

| Phương pháp | OK | NO_EVIDENCE | ERROR | UNSUPPORTED | TIMEOUT |
| --- | --- | --- | --- | --- | --- |
| BARO | 22 | 0 | 0 | 0 | 0 |
| SimpleRCA M4 | 22 | 0 | 0 | 0 | 0 |
| MicroRank full | 22 | 0 | 0 | 0 | 0 |
| TraceRCA finite | 22 | 0 | 0 | 0 | 0 |
| CIRCA | 0 | 0 | 0 | 22 | 0 |
| TORAI B | 0 | 0 | 0 | 22 | 0 |

MicroRank top-11 dẫn xuất từ cùng lượt: hit@1=0.0000, hit@3=0.0909, hit@5=0.2727, mrr=0.0689, avg@5=0.1000. Không chạy thêm.

Cận bi quan–lạc quan do hòa (không là CI), nguồn `tables.sensitivity_A.methods.*.summary.main.can_bi_quan/can_lac_quan`:

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.4091–0.4091 | 0.5455–0.5455 | 0.7273–0.7273 | 0.5497–0.5497 | 0.5675–0.5675 | 0.5818–0.5818 | 1.0000–1.0000 |
| SimpleRCA M4 | 0.3182–0.3182 | 0.6364–0.6364 | 0.7727–0.8182 | 0.5216–0.5278 | 0.5618–0.5814 | 0.5909–0.6091 | 1.0000–1.0000 |
| MicroRank full | 0.0000–0.0000 | 0.0909–0.0909 | 0.3636–0.3636 | 0.1686–0.1717 | 0.1530–0.1530 | 0.1182–0.1182 | 1.0000–1.0000 |
| TraceRCA finite | 0.0455–0.0909 | 0.4545–0.4545 | 0.5000–0.5455 | 0.2935–0.3254 | 0.2973–0.3377 | 0.3455–0.3727 | 0.9545–0.9545 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |

Khoảng bootstrap 95% (Hit@1; MRR; Rerank K5), nguồn `tables.sensitivity_A.bootstrap.phuong_phap`:

| Phương pháp | Hit@1 CI | MRR CI | Rerank K5 CI | Rerank K5 N/A / 10000 |
| --- | --- | --- | --- | --- |
| BARO | 0.1600–0.6818 | 0.3541–0.7573 | 0.2667–0.8235 | 0 |
| SimpleRCA M4 | 0.0909–0.5716 | 0.3642–0.7131 | 0.1212–0.6875 | 0 |
| MicroRank full | 0.0000–0.0000 | 0.1395–0.2087 | 0.0000–0.0000 | 17 |
| TraceRCA finite | 0.0000–0.1852 | 0.2042–0.4337 | 0.0000–0.3636 | 0 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |

CI bootstrap ghép cặp 95% cho hiệu a−b; nguồn `tables.sensitivity_A.bootstrap.hieu`:

| Cặp | Hit@1 CI | Avg@5 CI | MRR CI |
| --- | --- | --- | --- |
| BARO − SimpleRCA M4 | -0.1429–0.3500 | -0.1850–0.1391 | -0.1386–0.1962 |
| BARO − MicroRank full | 0.1600–0.6818 | 0.1714–0.7200 | 0.1667–0.5981 |
| BARO − TraceRCA finite | 0.0606–0.6364 | -0.0263–0.4391 | 0.0455–0.4261 |
| SimpleRCA M4 − MicroRank full | 0.0909–0.5716 | 0.2227–0.7200 | 0.1809–0.5496 |
| SimpleRCA M4 − TraceRCA finite | -0.0152–0.5417 | -0.0238–0.4900 | 0.0267–0.4145 |
| MicroRank full − TraceRCA finite | -0.1852–0.0000 | -0.4591–-0.0455 | -0.2605–-0.0374 |

## Độ nhạy B — 21 ca đồng thuận

Nguồn: `cham-a.json → tables.sensitivity_B`. 21 ca, 13 ô; cỡ ô: 1 ca × 5 ô, 2 ca × 8 ô.

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | Avg@5 | MRR | NDCG@5 | Retrieval@10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3810 | 0.5238 | 0.7143 | 0.5619 | 0.5283 | 0.5469 | 1.0000 | 0.5333 | 0.3810 |
| SimpleRCA M4 | 0.3333 | 0.6667 | 0.8333 | 0.6286 | 0.5433 | 0.5988 | 1.0000 | 0.4000 | 0.3333 |
| MicroRank full | 0.0000 | 0.0952 | 0.3333 | 0.1143 | 0.1687 | 0.1418 | 1.0000 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.0635 | 0.4286 | 0.5000 | 0.3381 | 0.2977 | 0.3007 | 0.9524 | 0.1270 | 0.0667 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

| Phương pháp | OK | NO_EVIDENCE | ERROR | UNSUPPORTED | TIMEOUT |
| --- | --- | --- | --- | --- | --- |
| BARO | 21 | 0 | 0 | 0 | 0 |
| SimpleRCA M4 | 21 | 0 | 0 | 0 | 0 |
| MicroRank full | 21 | 0 | 0 | 0 | 0 |
| TraceRCA finite | 21 | 0 | 0 | 0 | 0 |
| CIRCA | 0 | 0 | 0 | 21 | 0 |
| TORAI B | 0 | 0 | 0 | 21 | 0 |

MicroRank top-11 dẫn xuất từ cùng lượt: hit@1=0.0000, hit@3=0.0952, hit@5=0.2381, mrr=0.0627, avg@5=0.0952. Không chạy thêm.

Cận bi quan–lạc quan do hòa (không là CI), nguồn `tables.sensitivity_B.methods.*.summary.main.can_bi_quan/can_lac_quan`:

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3810–0.3810 | 0.5238–0.5238 | 0.7143–0.7143 | 0.5283–0.5283 | 0.5469–0.5469 | 0.5619–0.5619 | 1.0000–1.0000 |
| SimpleRCA M4 | 0.3333–0.3333 | 0.6667–0.6667 | 0.8095–0.8571 | 0.5405–0.5462 | 0.5885–0.6090 | 0.6190–0.6381 | 1.0000–1.0000 |
| MicroRank full | 0.0000–0.0000 | 0.0952–0.0952 | 0.3333–0.3333 | 0.1671–0.1704 | 0.1418–0.1418 | 0.1143–0.1143 | 1.0000–1.0000 |
| TraceRCA finite | 0.0476–0.0952 | 0.4286–0.4286 | 0.4762–0.5238 | 0.2837–0.3170 | 0.2815–0.3237 | 0.3238–0.3524 | 0.9524–0.9524 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |

Khoảng bootstrap 95% (Hit@1; MRR; Rerank K5), nguồn `tables.sensitivity_B.bootstrap.phuong_phap`:

| Phương pháp | Hit@1 CI | MRR CI | Rerank K5 CI | Rerank K5 N/A / 10000 |
| --- | --- | --- | --- | --- |
| BARO | 0.1429–0.6522 | 0.3414–0.7384 | 0.2353–0.8125 | 0 |
| SimpleRCA M4 | 0.1000–0.6000 | 0.3782–0.7336 | 0.1212–0.6875 | 0 |
| MicroRank full | 0.0000–0.0000 | 0.1376–0.2091 | 0.0000–0.0000 | 17 |
| TraceRCA finite | 0.0000–0.1930 | 0.1973–0.4285 | 0.0000–0.3889 | 0 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |

CI bootstrap ghép cặp 95% cho hiệu a−b; nguồn `tables.sensitivity_B.bootstrap.hieu`:

| Cặp | Hit@1 CI | Avg@5 CI | MRR CI |
| --- | --- | --- | --- |
| BARO − SimpleRCA M4 | -0.1579–0.2632 | -0.2063–0.0364 | -0.1516–0.1119 |
| BARO − MicroRank full | 0.1429–0.6522 | 0.1545–0.7143 | 0.1518–0.5827 |
| BARO − TraceRCA finite | 0.0435–0.6061 | -0.0381–0.4458 | 0.0317–0.4213 |
| SimpleRCA M4 − MicroRank full | 0.1000–0.6000 | 0.2450–0.7550 | 0.1948–0.5706 |
| SimpleRCA M4 − TraceRCA finite | -0.0159–0.5556 | 0.0368–0.5182 | 0.0559–0.4342 |
| MicroRank full − TraceRCA finite | -0.1930–0.0000 | -0.4500–-0.0318 | -0.2579–-0.0310 |

## Bổ sung — cắt trace N theo độ lệch ngày

Nguồn: `cham-a.json → tables.trace_guard`. 22 ca, 13 ô; cỡ ô: 1 ca × 4 ô, 2 ca × 9 ô.

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | Avg@5 | MRR | NDCG@5 | Retrieval@10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636 | 0.5455 | 0.7273 | 0.5727 | 0.5270 | 0.5507 | 1.0000 | 0.5000 | 0.3636 |
| SimpleRCA M4 | 0.3182 | 0.6818 | 0.8409 | 0.6318 | 0.5375 | 0.5973 | 1.0000 | 0.3784 | 0.3182 |
| MicroRank full | 0.0000 | 0.0909 | 0.3182 | 0.1000 | 0.1566 | 0.1334 | 0.9545 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.1591 | 0.3636 | 0.5909 | 0.3955 | 0.3640 | 0.3820 | 0.9545 | 0.2692 | 0.1667 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

| Phương pháp | OK | NO_EVIDENCE | ERROR | UNSUPPORTED | TIMEOUT |
| --- | --- | --- | --- | --- | --- |
| BARO | 22 | 0 | 0 | 0 | 0 |
| SimpleRCA M4 | 22 | 0 | 0 | 0 | 0 |
| MicroRank full | 21 | 0 | 1 | 0 | 0 |
| TraceRCA finite | 22 | 0 | 0 | 0 | 0 |
| CIRCA | 0 | 0 | 0 | 22 | 0 |
| TORAI B | 0 | 0 | 0 | 22 | 0 |

MicroRank top-11 dẫn xuất từ cùng lượt: hit@1=0.0000, hit@3=0.0909, hit@5=0.2273, mrr=0.0576, avg@5=0.0818. Không chạy thêm.

Cận bi quan–lạc quan do hòa (không là CI), nguồn `tables.trace_guard.methods.*.summary.main.can_bi_quan/can_lac_quan`:

| Phương pháp | Hit@1 | Hit@3 | Hit@5 | MRR | NDCG@5 | Avg@5 | Retrieval@10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636–0.3636 | 0.5455–0.5455 | 0.7273–0.7273 | 0.5270–0.5270 | 0.5507–0.5507 | 0.5727–0.5727 | 1.0000–1.0000 |
| SimpleRCA M4 | 0.3182–0.3182 | 0.6818–0.6818 | 0.8182–0.8636 | 0.5311–0.5441 | 0.5845–0.6100 | 0.6182–0.6455 | 1.0000–1.0000 |
| MicroRank full | 0.0000–0.0000 | 0.0909–0.0909 | 0.3182–0.3182 | 0.1552–0.1580 | 0.1334–0.1334 | 0.1000–0.1000 | 0.9545–0.9545 |
| TraceRCA finite | 0.1364–0.1818 | 0.3636–0.3636 | 0.5909–0.5909 | 0.3522–0.3758 | 0.3737–0.3904 | 0.3909–0.4000 | 0.9545–0.9545 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 | 0.0000–0.0000 |

Khoảng bootstrap 95% (Hit@1; MRR; Rerank K5), nguồn `tables.trace_guard.bootstrap.phuong_phap`:

| Phương pháp | Hit@1 CI | MRR CI | Rerank K5 CI | Rerank K5 N/A / 10000 |
| --- | --- | --- | --- | --- |
| BARO | 0.1364–0.6190 | 0.3460–0.7232 | 0.2308–0.7500 | 0 |
| SimpleRCA M4 | 0.0909–0.5716 | 0.3800–0.7202 | 0.1111–0.6667 | 0 |
| MicroRank full | 0.0000–0.0000 | 0.1335–0.1857 | 0.0000–0.0000 | 17 |
| TraceRCA finite | 0.0400–0.3182 | 0.2283–0.5211 | 0.0769–0.5000 | 0 |
| CIRCA | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |
| TORAI B | 0.0000–0.0000 | 0.0000–0.0000 | N/A–N/A | 10000 |

CI bootstrap ghép cặp 95% cho hiệu a−b; nguồn `tables.trace_guard.bootstrap.hieu`:

| Cặp | Hit@1 CI | Avg@5 CI | MRR CI |
| --- | --- | --- | --- |
| BARO − SimpleRCA M4 | -0.1500–0.2400 | -0.2000–0.0409 | -0.1468–0.1091 |
| BARO − MicroRank full | 0.1364–0.6190 | 0.2095–0.7100 | 0.1796–0.5748 |
| BARO − TraceRCA finite | -0.0435–0.4773 | -0.0429–0.3952 | -0.0138–0.3478 |
| SimpleRCA M4 − MicroRank full | 0.0909–0.5716 | 0.3000–0.7435 | 0.2189–0.5654 |
| SimpleRCA M4 − TraceRCA finite | -0.1591–0.5000 | 0.0240–0.4591 | -0.0315–0.3835 |
| MicroRank full − TraceRCA finite | -0.3182–-0.0400 | -0.5250–-0.0857 | -0.3605–-0.0737 |

## Độ nhạy và giới hạn kết luận

Bảng sau xét dấu chênh trung bình cho từng cặp trong bốn phương pháp có hỗ trợ. “Ổn định Q-84” chỉ có nghĩa dấu giữ ở chính/A/B; bảng cắt N báo riêng. Hòa hoặc đảo chiều được nêu điều kiện, không đổi thiết kế. Nguồn `tables.*.methods.*.summary.main`.

| Cặp | Độ đo | Chính | A | B | Cắt N | Q-84 | Cắt N so chính |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BARO − SimpleRCA M4 | hit@1 | 0.0455 | 0.0909 | 0.0476 | 0.0455 | Ổn định | Giữ dấu |
| BARO − SimpleRCA M4 | avg@5 | -0.0591 | -0.0182 | -0.0667 | -0.0591 | Ổn định | Giữ dấu |
| BARO − SimpleRCA M4 | mrr | -0.0105 | 0.0250 | -0.0150 | -0.0105 | Có điều kiện | Giữ dấu |
| BARO − MicroRank full | hit@1 | 0.3636 | 0.4091 | 0.3810 | 0.3636 | Ổn định | Giữ dấu |
| BARO − MicroRank full | avg@5 | 0.4545 | 0.4636 | 0.4476 | 0.4727 | Ổn định | Giữ dấu |
| BARO − MicroRank full | mrr | 0.3569 | 0.3796 | 0.3596 | 0.3704 | Ổn định | Giữ dấu |
| BARO − TraceRCA finite | hit@1 | 0.2576 | 0.3485 | 0.3175 | 0.2045 | Ổn định | Giữ dấu |
| BARO − TraceRCA finite | avg@5 | 0.2045 | 0.2227 | 0.2238 | 0.1773 | Ổn định | Giữ dấu |
| BARO − TraceRCA finite | mrr | 0.1973 | 0.2428 | 0.2306 | 0.1630 | Ổn định | Giữ dấu |
| SimpleRCA M4 − MicroRank full | hit@1 | 0.3182 | 0.3182 | 0.3333 | 0.3182 | Ổn định | Giữ dấu |
| SimpleRCA M4 − MicroRank full | avg@5 | 0.5136 | 0.4818 | 0.5143 | 0.5318 | Ổn định | Giữ dấu |
| SimpleRCA M4 − MicroRank full | mrr | 0.3674 | 0.3546 | 0.3746 | 0.3809 | Ổn định | Giữ dấu |
| SimpleRCA M4 − TraceRCA finite | hit@1 | 0.2121 | 0.2576 | 0.2698 | 0.1591 | Ổn định | Giữ dấu |
| SimpleRCA M4 − TraceRCA finite | avg@5 | 0.2636 | 0.2409 | 0.2905 | 0.2364 | Ổn định | Giữ dấu |
| SimpleRCA M4 − TraceRCA finite | mrr | 0.2079 | 0.2178 | 0.2456 | 0.1735 | Ổn định | Giữ dấu |
| MicroRank full − TraceRCA finite | hit@1 | -0.1061 | -0.0606 | -0.0635 | -0.1591 | Ổn định | Giữ dấu |
| MicroRank full − TraceRCA finite | avg@5 | -0.2500 | -0.2409 | -0.2238 | -0.2955 | Ổn định | Giữ dấu |
| MicroRank full − TraceRCA finite | mrr | -0.1595 | -0.1368 | -0.1290 | -0.2074 | Ổn định | Giữ dấu |

Cận 1/22 chỉ cho thay đổi trung bình Hit@k của một phương pháp khi một ca đổi đầu ra. Không dùng cận này cho hiệu hai phương pháp, Rerank hay khoảng bootstrap. Điểm trung bình và dấu không tự chứng minh khác biệt thống kê; CI từng cặp nằm trong `tables.*.bootstrap.hieu`.

## Bốn tập và mức ngẫu nhiên

Nguồn `tables.main.methods.*.per_case.*.four_sets/random` và `summary.random`. Inventory và tập chấm đều U=10. Tập O là sau tiền xử lý; root ngoài O có mức ngẫu nhiên O bằng 0. Thực thể ngoài U giữ chỗ và đếm riêng.

| Phương pháp | O trung bình | Root trong O | Root trả về | Random O Hit1 | Random O Hit5 | Random U Hit1 | Random U Hit5 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 10.0000 | 1.0000 | 1.0000 | 0.1000 | 0.5000 | 0.1000 | 0.5000 |
| SimpleRCA M4 | 10.0000 | 1.0000 | 1.0000 | 0.1000 | 0.5000 | 0.1000 | 0.5000 |
| MicroRank full | 10.0000 | 1.0000 | 1.0000 | 0.1000 | 0.5000 | 0.1000 | 0.5000 |
| TraceRCA finite | 10.0000 | 1.0000 | 0.9545 | 0.1000 | 0.5000 | 0.1000 | 0.5000 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1000 | 0.5000 |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.1000 | 0.5000 |

| Phương pháp | Inventory | O TB | Chấm | Trả về TB | O ngoài U | Trả về ngoài U |
| --- | --- | --- | --- | --- | --- | --- |
| BARO | 10 | 10.0000 | 10 | 10.0000 | [] | [] |
| SimpleRCA M4 | 10 | 10.0000 | 10 | 10.0000 | [] | [] |
| MicroRank full | 10 | 10.0000 | 10 | 9.8182 | [] | [] |
| TraceRCA finite | 10 | 10.0000 | 10 | 9.0909 | [] | [] |
| CIRCA | 10 | 0.0000 | 10 | 0.0000 | [] | [] |
| TORAI B | 10 | 0.0000 | 10 | 0.0000 | [] | [] |

## Diễn giải MicroRank và TraceRCA so với mức ngẫu nhiên

Nguồn độ đo: `results/T-026/cham-a.json → tables.*.methods.{microrank_full,tracerca}.summary.main`; nguồn khoảng bootstrap 95%: `tables.main.bootstrap.phuong_phap`, khóa `hit@1`, `hit@5`, `rr`, `avg@5`. Mức ngẫu nhiên là kỳ vọng khi xếp đều trên tập ứng viên, không phải một lượt chạy phương pháp. Với root thuộc tập n thực thể: Hit@K=min(K,n)/n; MRR=H_n/n, H_n=Σ(1/r), r=1…n; Avg@5=Σ[min(k,n)/n]/5, k=1…5. Root ngoài tập hoặc tập rỗng cho mốc 0. Trên cả bốn bảng OB, bốn phương pháp hỗ trợ đều có O=U=10 và root thuộc O: mốc Hit@1/Hit@5/MRR/Avg@5 là 0,100000/0,500000/0,292897/0,300000. Nguồn tập và membership: `tables.*.methods.*.per_case.*.four_sets/random`.

| Bảng | Phương pháp | Hit@1 | Hit@5 | MRR | Avg@5 |
|---|---|---:|---:|---:|---:|
| Chính | MicroRank full | 0.000000 | 0.363636 | 0.170139 | 0.118182 |
| Chính | TraceRCA finite | 0.106061 | 0.522727 | 0.329654 | 0.368182 |
| A | MicroRank full | 0.000000 | 0.363636 | 0.170139 | 0.118182 |
| A | TraceRCA finite | 0.060606 | 0.522727 | 0.306926 | 0.359091 |
| B | MicroRank full | 0.000000 | 0.333333 | 0.168717 | 0.114286 |
| B | TraceRCA finite | 0.063492 | 0.500000 | 0.297732 | 0.338095 |
| Cắt N | MicroRank full | 0.000000 | 0.318182 | 0.156620 | 0.100000 |
| Cắt N | TraceRCA finite | 0.159091 | 0.590909 | 0.364006 | 0.395455 |

MicroRank có điểm trung bình thấp hơn mốc trên cả bốn độ đo ở cả bốn bảng. Bảng cắt N vẫn giữ một ca ERROR trong mẫu số, như quy tắc chấm. Với bảng chính, các khoảng MRR và Avg@5 của MicroRank nằm dưới mốc; khoảng Hit@5 vẫn chứa 0,5. Không coi mọi điểm thấp hơn mốc là bằng chứng khác biệt thống kê. TraceRCA chính nhỉnh hơn mốc về điểm, nhưng cả bốn khoảng đều chứa mốc: chưa phân biệt rõ với ngẫu nhiên bằng các khoảng hiện có, chưa chứng minh tương đương. Các khoảng chỉ áp dụng cho dev và cách lấy lại mẫu theo ô đã khai.

| Phương pháp — chính | Hit@1: khoảng 95% | Hit@5: khoảng 95% | MRR: khoảng 95% | Avg@5: khoảng 95% |
|---|---|---|---|---|
| MicroRank full | 0.000000–0.000000 | 0.105263–0.652174 | 0.139525–0.208739 | 0.030000–0.232033 |
| TraceRCA finite | 0.000000–0.253968 | 0.260870–0.800000 | 0.208503–0.478781 | 0.168177–0.590909 |

### Sự tập trung và biến động thứ hạng trên 22 ca chính

Nguồn: `tables.main.methods.*.per_case.*.source_path → entity_ranking`, dùng `entity` và khóa `key` thật. Vị trí kỳ vọng của service là trung bình các vị trí trong nhóm khóa bằng nhau. Bảng dưới lấy trung bình và min–max **chỉ trên ca có trả service đó**; n/22 cho biết ca vắng, không gán ca vắng một hạng tốt. Đây là mô tả vị trí service, không phải MRR: MRR chấm kỳ vọng của 1/r theo quy tắc trên.

| Service | MicroRank: có trả /22 | Vị trí TB [min–max] theo hòa | TraceRCA: có trả /22 | Vị trí TB [min–max] theo hòa |
|---|---:|---|---:|---|
| adservice | 22 | 6.227273 [5–7] | 22 | 7.272727 [2–9] |
| cartservice | 22 | 2.500000 [1–4] | 22 | 6.272727 [3–9] |
| checkoutservice | 22 | 8.636364 [7–10] | 22 | 4.363636 [1–9] |
| currencyservice | 22 | 1.590909 [1–3] | 22 | 2.545455 [1–5] |
| emailservice | 20 | 9.200000 [8.5–10] | 13 | 8.615385 [2–10] |
| frontend | 22 | 3.681818 [2–4] | 22 | 1.636364 [1–3] |
| paymentservice | 20 | 8.975000 [8–9.5] | 14 | 7.785714 [4–9.5] |
| productcatalogservice | 22 | 2.227273 [1–4] | 22 | 4.409091 [3–8] |
| recommendationservice | 22 | 5.090909 [5–6] | 19 | 4.657895 [1–8] |
| shippingservice | 22 | 6.795455 [6–9.5] | 22 | 5.613636 [1–8] |

Để mô tả biến động, bảng tiếp theo đếm số thứ tự khác nhau trong 22 ca. Thứ tự ở đây là native (thứ tự gốc trong record), giữ cách phá hòa của đầu ra; “tập top-3” bỏ thứ tự của ba tên. Các số này không thay quy tắc hòa của độ đo và không chứng minh xếp hạng độc lập với ca.

| Phương pháp | Thứ tự đầy đủ khác nhau /22 | Thứ tự top-3 khác nhau /22 | Tập top-3 khác nhau /22 |
|---|---:|---:|---:|
| MicroRank full | 17 | 10 | 3 |
| TraceRCA finite | 22 | 17 | 8 |

MicroRank đặt currencyservice đầu 13 ca, cartservice 5 ca và productcatalogservice 4 ca; không hòa tại đầu các danh sách này. Ba service đó chỉ là root ở 1/22 ca, nên sự tập trung góp phần giải thích Hit@1=0 trong cohort này. Tuy vậy 17 thứ tự đầy đủ và 10 thứ tự top-3 cho thấy danh sách vẫn thay theo ca. Chưa xác nhận ba service đầu là hub (nút có vai trò trung tâm) hoặc chỉ được ưu tiên do danh tính. TraceRCA đặt frontend đầu native 13/22 ca; hai ca có hòa ở đầu, nên số lần đầu kỳ vọng theo hòa là 11,833333/22. Nguồn nhãn root chỉ dùng để chấm/mô tả sau đầu ra: `tables.main.methods.*.per_case.*.label`; nhãn không được đưa lại vào phương pháp.

### Trace A bị gắn bất thường và các nguyên nhân còn khả thi

Nguồn từng dòng dưới: `tables.main.methods.microrank_full.per_case.*.source_path → diagnostics.counts`. Theo `src/microrank/__init__.py:52–72`, `all` là số traceID trong A; `anomaly` là số traceID trong A có ít nhất một span vượt ngưỡng operation học từ N; `normal` là trace A không bị gắn bất thường. **Nhóm normal này thuộc A, không phải tập nền N.** Span N là `spans_before`; hàng lặp không là mẫu độc lập. Tỉ lệ anomaly/all chưa phải tỉ lệ false positive (báo bất thường sai), vì không có nhãn bất thường của từng trace.

| Mã ca | Trace A anomaly | Trace A all | anomaly/all | Span N |
|---|---:|---:|---:|---:|
| dev-14701a3bbb | 342 | 753 | 0.454183 | 33470 |
| dev-1ac905bc95 | 160 | 1122 | 0.142602 | 19751 |
| dev-27252dca60 | 94 | 991 | 0.094854 | 25037 |
| dev-2bfc97b01e | 225 | 828 | 0.271739 | 31749 |
| dev-396c8dbf7d | 324 | 890 | 0.364045 | 31951 |
| dev-3b92690644 | 296 | 935 | 0.316578 | 26329 |
| dev-3e27669440 | 516 | 832 | 0.620192 | 25764 |
| dev-515c5f2190 | 322 | 431 | 0.747100 | 32892 |
| dev-5467884de4 | 484 | 626 | 0.773163 | 37756 |
| dev-55f99f3e0a | 402 | 1141 | 0.352323 | 16158 |
| dev-5ada15752d | 189 | 1230 | 0.153659 | 18497 |
| dev-607751ac0a | 233 | 755 | 0.308609 | 38966 |
| dev-63c30faf34 | 594 | 769 | 0.772432 | 32101 |
| dev-6c9afc9822 | 218 | 769 | 0.283485 | 34960 |
| dev-70629373f9 | 300 | 1060 | 0.283019 | 23054 |
| dev-7b7c973198 | 332 | 970 | 0.342268 | 27490 |
| dev-7d3c2fe6d1 | 377 | 882 | 0.427438 | 30522 |
| dev-8ecd9880ed | 180 | 751 | 0.239680 | 36362 |
| dev-95e164235f | 264 | 803 | 0.328767 | 34784 |
| dev-9b9397a4dc | 139 | 420 | 0.330952 | 21736 |
| dev-9fd793feb7 | 466 | 1036 | 0.449807 | 22533 |
| dev-b0f8b2e3ac | 350 | 1086 | 0.322284 | 20859 |

Tỉ lệ trải từ 0.094854 đến 0.773163, trung bình 0.380872; 7/22 ca vượt 0,4. Nhóm normal trong A vẫn có 109–1041 trace mỗi ca. N ngắn theo thời gian không tự chứng minh nhóm normal dùng cho spectrum ít.

Đã tính lại ngưỡng/flags của hai ca có tỉ lệ cao bằng đúng phép chia end của code; mean và std từ N được đổi sang ms, làm tròn hai chữ số trước khi áp ngưỡng mean+3std, trên dữ liệu dev; không chạy lại phương pháp. `dev-5467884de4` có 484/626 trace A bị gắn bất thường; lời gọi `frontend_hipstershop.RecommendationService/ListRecommendations` góp 436/484 trace đó. `dev-63c30faf34` có 594/769 và lời gọi trên góp 553/594. Operation này có 586 và 504 span N phân biệt, ngưỡng tương ứng 54,05 và 47,95 ms; không có operation ngưỡng 0 trong hai ca. Sau khi tính không nhãn, đối chiếu nhãn cho thấy cả hai là recommendationservice network_delay. Vì vậy tỉ lệ cao có thể phản ánh dấu hiệu lỗi thực ở lời gọi tới service lỗi, chưa đủ quy cho N ngắn hoặc ngưỡng quá chặt. Nguồn dữ liệu: trace dev đã khai trong `results/T-026/allowlist-dev.json`; counts ở record trên; phép tính lại, giả định và kết quả chi tiết được ghi trong LOG phiên6, mục “R1 — tỉ lệ trace A gắn bất thường và giải thích thay thế”.

Các giải thích dưới đều **chưa kiểm nhân quả**; chúng có thể cùng góp phần. Không chọn một nguyên nhân chỉ vì nó khớp số gộp (Q-33).

| Khả năng | Giả định cần đúng và trường hợp không đủ giải thích | Vì sao chưa tách được trong task này |
|---|---|---|
| N ngắn/độ phủ không đều hoặc chưa sạch, chưa recovery | Cần nền làm lệch ngưỡng hoặc thiếu operation quan trọng. Giả thuyết chỉ do ít mẫu yếu đi nếu mọi operation đủ mẫu phân biệt và nền đại diện; hai ca trên có nhiều mẫu cho operation tạo phần lớn flags, nhưng chưa chứng minh nền sạch. | Metadata đã cho độ dài/số mẫu; không có xác nhận nền sạch/recovery hay phân phối operation trước thu thập. Bảng cắt N đổi khoảng nền nhưng không tách sạch độ phủ và nhiễm lỗi. |
| Load hoặc mix (cơ cấu lời gọi) đổi, hoặc triệu chứng lỗi thực | Cần thay đổi lời gọi/duration trong A giải thích flags. Flags do Recommendation ở hai ca phù hợp lỗi đã tiêm; điều đó không chứng minh flags của mọi ca đều đúng. Nếu load/mix không đổi và span bị flag không gắn triệu chứng lỗi thì giải thích này yếu đi. | Không có nhãn bất thường từng trace và đối chứng load/mix không lỗi tương ứng. Các file hiện có không phân biệt đủ các nguyên nhân đó. |
| Cấu trúc, coverage và spectrum (mẫu xuất hiện operation trong trace) ưu tiên một số service | Code dùng call graph, operation↔trace, PageRank và Dstar2; số trace anomaly chứa operation có thể tăng score khi weights và coverage còn lại giữ cố định. Nếu tập trung không đi theo các thành phần đó thì giả thuyết yếu đi; service đầu chưa được xác nhận là hub. | Record không giữ đủ weights/prior/coverage bên trong để quy riêng cho PageRank hay spectrum; tách chúng cần biến thể/can thiệp ngoài cấu hình đã khóa và phạm vi sửa. Nguồn cơ chế: `src/microrank/official.py:24–75,89–124,135–168`. |
| Cohort (nhóm ca), biến thể triển khai hoặc thiết lập nền khác bài công bố | Chênh số có thể do chọn ô/ca hoặc cửa sổ/cài đặt khác. Nếu cùng cohort, code, dữ liệu và quy tắc chấm vẫn lệch thì riêng giải thích này không đủ. | Table 3 là 56 ca, task chỉ 22 dev; chưa có hợp đồng tái lập MicroRank của bài đủ để đồng nhất các điều kiện. 34 ca test chưa được mở. README/pattern_ranker xác nhận normal riêng của Nezha, chưa xác nhận baseline MicroRank Table3 dùng construct_data. Nguồn: `results/T-008/sources/README.md:95`, `results/T-008/sources/pattern_ranker.py:212–219`, thẻ `results/T-008/the-dataset.md:56–61`. |

Các khả năng này giới hạn diễn giải baseline hiện tại; không dùng chúng để kết luận đồ thị tốt/xấu hoặc tự thay cấu hình sau khi đã thấy số.

## Theo loại lỗi — bảng chính

Nguồn `tables.main.methods.*.summary.grouped.fault`. Mỗi ô chỉ 1–2 ca, không suy mẫu hình từ một ô.

| Theo loại lỗi | n | BARO Hit1 / MRR | SimpleRCA M4 Hit1 / MRR | MicroRank full Hit1 / MRR | TraceRCA finite Hit1 / MRR |
| --- | --- | --- | --- | --- | --- |
| cpu_consumed | 4 | 0.5000 / 0.6875 | 0.0000 / 0.4792 | 0.0000 / 0.1712 | 0.5833 / 0.7778 |
| cpu_contention | 5 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 0.0000 / 0.1539 | 0.0000 / 0.3556 |
| exception | 3 | 0.3333 / 0.4643 | 0.3333 / 0.6111 | 0.0000 / 0.1944 | 0.0000 / 0.2194 |
| network_delay | 6 | 0.0000 / 0.2946 | 0.1667 / 0.3335 | 0.0000 / 0.1477 | 0.0000 / 0.1187 |
| return | 4 | 0.0000 / 0.1708 | 0.0000 / 0.2687 | 0.0000 / 0.2049 | 0.0000 / 0.2482 |

## Theo nhóm lỗi — bảng chính

Nguồn `tables.main.methods.*.summary.grouped.nhom_loi`. Mỗi ô chỉ 1–2 ca, không suy mẫu hình từ một ô.

| Theo nhóm lỗi | n | BARO Hit1 / MRR | SimpleRCA M4 Hit1 / MRR | MicroRank full Hit1 / MRR | TraceRCA finite Hit1 / MRR |
| --- | --- | --- | --- | --- | --- |
| mã nguồn | 7 | 0.1429 / 0.2966 | 0.1429 / 0.4155 | 0.0000 / 0.2004 | 0.0000 / 0.2359 |
| mạng | 6 | 0.0000 / 0.2946 | 0.1667 / 0.3335 | 0.0000 / 0.1477 | 0.0000 / 0.1187 |
| tài nguyên | 9 | 0.7778 / 0.8611 | 0.5556 / 0.7685 | 0.0000 / 0.1616 | 0.2593 / 0.5432 |

## Theo ô — bảng chính

Nguồn `tables.main.methods.*.summary.grouped.cell`. Mỗi ô chỉ 1–2 ca, không suy mẫu hình từ một ô.

| Theo ô | n | BARO Hit1 / MRR | SimpleRCA M4 Hit1 / MRR | MicroRank full Hit1 / MRR | TraceRCA finite Hit1 / MRR |
| --- | --- | --- | --- | --- | --- |
| adservice / cpu_contention | 1 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 0.0000 / 0.2000 | 0.0000 / 0.5000 |
| checkoutservice / exception | 2 | 0.5000 / 0.6250 | 0.0000 / 0.4167 | 0.0000 / 0.1250 | 0.0000 / 0.2667 |
| checkoutservice / network_delay | 2 | 0.0000 / 0.3125 | 0.5000 / 0.5528 | 0.0000 / 0.1250 | 0.0000 / 0.1667 |
| checkoutservice / return | 2 | 0.0000 / 0.2292 | 0.0000 / 0.3625 | 0.0000 / 0.1181 | 0.0000 / 0.1631 |
| emailservice / cpu_consumed | 1 | 1.0000 / 1.0000 | 0.0000 / 0.5000 | 0.0000 / 0.1181 | 0.3333 / 0.6111 |
| emailservice / network_delay | 2 | 0.0000 / 0.3750 | 0.0000 / 0.2917 | 0.0000 / 0.1181 | 0.0000 / 0.0556 |
| frontend / return | 2 | 0.0000 / 0.1125 | 0.0000 / 0.1750 | 0.0000 / 0.2917 | 0.0000 / 0.3333 |
| paymentservice / cpu_contention | 2 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 0.0000 / 0.1181 | 0.0000 / 0.1389 |
| productcatalogservice / exception | 1 | 0.0000 / 0.1429 | 1.0000 / 1.0000 | 0.0000 / 0.3333 | 0.0000 / 0.1250 |
| recommendationservice / cpu_consumed | 2 | 0.5000 / 0.7500 | 0.0000 / 0.4583 | 0.0000 / 0.2000 | 0.5000 / 0.7500 |
| recommendationservice / network_delay | 2 | 0.0000 / 0.1964 | 0.0000 / 0.1560 | 0.0000 / 0.2000 | 0.0000 / 0.1339 |
| shippingservice / cpu_consumed | 1 | 0.0000 / 0.2500 | 0.0000 / 0.5000 | 0.0000 / 0.1667 | 1.0000 / 1.0000 |
| shippingservice / cpu_contention | 2 | 1.0000 / 1.0000 | 1.0000 / 1.0000 | 0.0000 / 0.1667 | 0.0000 / 0.5000 |

## Theo nhóm vị trí root — bảng chính

Nguồn `tables.main.methods.*.summary.grouped.nhom_vi_tri_p75`. Mỗi ô chỉ 1–2 ca, không suy mẫu hình từ một ô.

| Theo nhóm vị trí root | n | BARO Hit1 / MRR | SimpleRCA M4 Hit1 / MRR | MicroRank full Hit1 / MRR | TraceRCA finite Hit1 / MRR |
| --- | --- | --- | --- | --- | --- |
| giữa hoặc hub (hub OPEN) | 10 | 0.2000 / 0.4226 | 0.1000 / 0.3893 | 0.0000 / 0.1536 | 0.1000 / 0.2961 |
| lá | 10 | 0.6000 / 0.7143 | 0.6000 / 0.7583 | 0.0000 / 0.1624 | 0.1333 / 0.3625 |
| nguồn | 2 | 0.0000 / 0.1125 | 0.0000 / 0.1750 | 0.0000 / 0.2917 | 0.0000 / 0.3333 |

## Từng ca — bảng chính

Nguồn `tables.main.methods.*.per_case`. Hạng a–b là nhóm hòa; ∞ là root vắng/non-OK. Theo ca của A/B/cắt N đầy đủ trong JSON, giữ cùng nguồn/hash và mẫu số.

| Mã ca | Root | Loại lỗi | BARO hạng / H1 / RR | SimpleRCA M4 hạng / H1 / RR | MicroRank full hạng / H1 / RR | TraceRCA finite hạng / H1 / RR |
| --- | --- | --- | --- | --- | --- | --- |
| dev-14701a3bbb | shippingservice | cpu_contention | 1 / 1.0000 / 1.0000 | 1 / 1.0000 / 1.0000 | 6 / 0.0000 / 0.1667 | 2 / 0.0000 / 0.5000 |
| dev-1ac905bc95 | frontend | return | 10 / 0.0000 / 0.1000 | 5–6 / 0.0000 / 0.1833 | 3 / 0.0000 / 0.3333 | 3 / 0.0000 / 0.3333 |
| dev-27252dca60 | productcatalogservice | exception | 7 / 0.0000 / 0.1429 | 1 / 1.0000 / 1.0000 | 3 / 0.0000 / 0.3333 | 8 / 0.0000 / 0.1250 |
| dev-2bfc97b01e | checkoutservice | network_delay | 2 / 0.0000 / 0.5000 | 1 / 1.0000 / 1.0000 | 8 / 0.0000 / 0.1250 | 6 / 0.0000 / 0.1667 |
| dev-396c8dbf7d | emailservice | cpu_consumed | 1 / 1.0000 / 1.0000 | 2 / 0.0000 / 0.5000 | 8–9 / 0.0000 / 0.1181 | 1–3 / 0.3333 / 0.6111 |
| dev-3b92690644 | checkoutservice | return | 3 / 0.0000 / 0.3333 | 2 / 0.0000 / 0.5000 | 8 / 0.0000 / 0.1250 | 7 / 0.0000 / 0.1429 |
| dev-3e27669440 | adservice | cpu_contention | 1 / 1.0000 / 1.0000 | 1 / 1.0000 / 1.0000 | 5 / 0.0000 / 0.2000 | 2 / 0.0000 / 0.5000 |
| dev-515c5f2190 | recommendationservice | cpu_consumed | 1 / 1.0000 / 1.0000 | 2 / 0.0000 / 0.5000 | 5 / 0.0000 / 0.2000 | 2 / 0.0000 / 0.5000 |
| dev-5467884de4 | recommendationservice | network_delay | 4 / 0.0000 / 0.2500 | 5 / 0.0000 / 0.2000 | 5 / 0.0000 / 0.2000 | 7 / 0.0000 / 0.1429 |
| dev-55f99f3e0a | checkoutservice | exception | 4 / 0.0000 / 0.2500 | 2 / 0.0000 / 0.5000 | 8 / 0.0000 / 0.1250 | 3 / 0.0000 / 0.3333 |
| dev-5ada15752d | frontend | return | 8 / 0.0000 / 0.1250 | 6 / 0.0000 / 0.1667 | 4 / 0.0000 / 0.2500 | 3 / 0.0000 / 0.3333 |
| dev-607751ac0a | checkoutservice | network_delay | 8 / 0.0000 / 0.1250 | 9–10 / 0.0000 / 0.1056 | 8 / 0.0000 / 0.1250 | 6 / 0.0000 / 0.1667 |
| dev-63c30faf34 | recommendationservice | network_delay | 7 / 0.0000 / 0.1429 | 8–10 / 0.0000 / 0.1120 | 5 / 0.0000 / 0.2000 | 8 / 0.0000 / 0.1250 |
| dev-6c9afc9822 | emailservice | network_delay | 2 / 0.0000 / 0.5000 | 4 / 0.0000 / 0.2500 | 8–9 / 0.0000 / 0.1181 | 9 / 0.0000 / 0.1111 |
| dev-70629373f9 | paymentservice | cpu_contention | 1 / 1.0000 / 1.0000 | 1 / 1.0000 / 1.0000 | 8–9 / 0.0000 / 0.1181 | 9 / 0.0000 / 0.1111 |
| dev-7b7c973198 | emailservice | network_delay | 4 / 0.0000 / 0.2500 | 3 / 0.0000 / 0.3333 | 8–9 / 0.0000 / 0.1181 | ∞ / 0.0000 / 0.0000 |
| dev-7d3c2fe6d1 | shippingservice | cpu_contention | 1 / 1.0000 / 1.0000 | 1 / 1.0000 / 1.0000 | 6 / 0.0000 / 0.1667 | 2 / 0.0000 / 0.5000 |
| dev-8ecd9880ed | checkoutservice | return | 8 / 0.0000 / 0.1250 | 4–5 / 0.0000 / 0.2250 | 9 / 0.0000 / 0.1111 | 5–6 / 0.0000 / 0.1833 |
| dev-95e164235f | paymentservice | cpu_contention | 1 / 1.0000 / 1.0000 | 1 / 1.0000 / 1.0000 | 8–9 / 0.0000 / 0.1181 | 6 / 0.0000 / 0.1667 |
| dev-9b9397a4dc | recommendationservice | cpu_consumed | 2 / 0.0000 / 0.5000 | 2–3 / 0.0000 / 0.4167 | 5 / 0.0000 / 0.2000 | 1 / 1.0000 / 1.0000 |
| dev-9fd793feb7 | shippingservice | cpu_consumed | 4 / 0.0000 / 0.2500 | 2 / 0.0000 / 0.5000 | 6 / 0.0000 / 0.1667 | 1 / 1.0000 / 1.0000 |
| dev-b0f8b2e3ac | checkoutservice | exception | 1 / 1.0000 / 1.0000 | 3 / 0.0000 / 0.3333 | 8 / 0.0000 / 0.1250 | 5 / 0.0000 / 0.2000 |

## RCAEval riêng — Chính — 22 ca theo inject_time

Nguồn `tables.main.methods.*.summary.rcaeval`; thứ tự gốc, không hòa kỳ vọng. Ca non-OK vẫn ở mẫu số.

| Phương pháp | AC1 | AC3 | AC5 | Avg5 | Retrieval5 | Retrieval10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636 | 0.5455 | 0.7273 | 0.5727 | 0.7273 | 1.0000 | 0.5000 | 0.3636 |
| SimpleRCA M4 | 0.3182 | 0.6818 | 0.8182 | 0.6273 | 0.8182 | 1.0000 | 0.3889 | 0.3182 |
| MicroRank full | 0.0000 | 0.0909 | 0.3636 | 0.1182 | 0.3636 | 1.0000 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.0909 | 0.4545 | 0.5455 | 0.3636 | 0.5455 | 0.9545 | 0.1667 | 0.0952 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

## RCAEval riêng — Độ nhạy A — 22 ca, một ca dùng inject_timestamp

Nguồn `tables.sensitivity_A.methods.*.summary.rcaeval`; thứ tự gốc, không hòa kỳ vọng. Ca non-OK vẫn ở mẫu số.

| Phương pháp | AC1 | AC3 | AC5 | Avg5 | Retrieval5 | Retrieval10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.4091 | 0.5455 | 0.7273 | 0.5818 | 0.7273 | 1.0000 | 0.5625 | 0.4091 |
| SimpleRCA M4 | 0.3182 | 0.6364 | 0.7727 | 0.6000 | 0.7727 | 1.0000 | 0.4118 | 0.3182 |
| MicroRank full | 0.0000 | 0.0909 | 0.3636 | 0.1182 | 0.3636 | 1.0000 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.0455 | 0.4545 | 0.5455 | 0.3545 | 0.5455 | 0.9545 | 0.0833 | 0.0476 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

## RCAEval riêng — Độ nhạy B — 21 ca đồng thuận

Nguồn `tables.sensitivity_B.methods.*.summary.rcaeval`; thứ tự gốc, không hòa kỳ vọng. Ca non-OK vẫn ở mẫu số.

| Phương pháp | AC1 | AC3 | AC5 | Avg5 | Retrieval5 | Retrieval10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3810 | 0.5238 | 0.7143 | 0.5619 | 0.7143 | 1.0000 | 0.5333 | 0.3810 |
| SimpleRCA M4 | 0.3333 | 0.6667 | 0.8095 | 0.6286 | 0.8095 | 1.0000 | 0.4118 | 0.3333 |
| MicroRank full | 0.0000 | 0.0952 | 0.3333 | 0.1143 | 0.3333 | 1.0000 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.0476 | 0.4286 | 0.5238 | 0.3333 | 0.5238 | 0.9524 | 0.0909 | 0.0500 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

## RCAEval riêng — Bổ sung — cắt trace N theo độ lệch ngày

Nguồn `tables.trace_guard.methods.*.summary.rcaeval`; thứ tự gốc, không hòa kỳ vọng. Ca non-OK vẫn ở mẫu số.

| Phương pháp | AC1 | AC3 | AC5 | Avg5 | Retrieval5 | Retrieval10 | Rerank K5 | Rerank K10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636 | 0.5455 | 0.7273 | 0.5727 | 0.7273 | 1.0000 | 0.5000 | 0.3636 |
| SimpleRCA M4 | 0.3182 | 0.6818 | 0.8182 | 0.6273 | 0.8182 | 1.0000 | 0.3889 | 0.3182 |
| MicroRank full | 0.0000 | 0.0909 | 0.3182 | 0.1000 | 0.3182 | 0.9545 | 0.0000 | 0.0000 |
| TraceRCA finite | 0.1364 | 0.3636 | 0.5909 | 0.3909 | 0.5909 | 0.9545 | 0.2308 | 0.1429 |
| CIRCA | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |
| TORAI B | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | N/A | N/A |

## So với T-024 — tách dataset

Nguồn OB: `cham-a.json → tables.main.methods.*.summary.main`; nguồn RE2-TT: `results/T-024/cham-a.json → methods.*.summaries.dev30.main`. Các dòng cùng phương pháp, không gộp dataset. RE2-TT có inventory khác và 30 ca; OB có 22 ca, thêm lỗi mã nguồn. Cadence, cửa sổ hiệu lực, loại lỗi và coverage khác nhau nên không quy chênh riêng cho đổi hệ thống.

| Phương pháp | OB Hit1 | RE2 Hit1 | OB MRR | RE2 MRR | OB Avg5 | RE2 Avg5 |
| --- | --- | --- | --- | --- | --- | --- |
| BARO | 0.3636 | 0.7000 | 0.5270 | 0.7682 | 0.5727 | 0.8000 |
| SimpleRCA M4 | 0.3182 | 0.8333 | 0.5375 | 0.8911 | 0.6318 | 0.9267 |
| MicroRank full | 0.0000 | 0.0667 | 0.1701 | 0.2565 | 0.1182 | 0.3133 |
| TraceRCA finite | 0.1061 | 0.7000 | 0.3297 | 0.7565 | 0.3682 | 0.7867 |

Mốc ngẫu nhiên cần đặt cạnh số thô vì kích thước tập ứng viên khác nhau. Bảng dưới lấy kỳ vọng đều theo từng ca/từng seed rồi trung bình, dùng công thức Hit/MRR/Avg@5 ở mục “Diễn giải MicroRank và TraceRCA”. Nguồn: OB `results/T-026/cham-a.json → tables.main.methods.*.per_case.*.four_sets/random`; RE2 `results/T-024/cham-a.json → methods.*.per_case.*.four_sets.by_seed/random.by_seed` (Hit đối chiếu `summaries.dev30.random`). Mọi root ở các dòng này thuộc tập tương ứng. O của RE2 MicroRank/TraceRCA là 20–27 service; O SimpleRCA có một ca 69, các ca còn lại 68. Mốc O vẫn được tính ở ca ERROR theo §8.7: đây là mốc lý thuyết trên tập quan sát, không phải một lượt xếp hạng thành công.

| Dataset/tập — mốc ngẫu nhiên | Hit@1 | Hit@5 | MRR | Avg@5 |
|---|---:|---:|---:|---:|
| OB U=O10, bốn phương pháp hỗ trợ | 0.100000 | 0.500000 | 0.292897 | 0.300000 |
| RE2 U68 / O BARO | 0.014706 | 0.073529 | 0.070648 | 0.044118 |
| RE2 O SimpleRCA, 68–69 | 0.014699 | 0.073494 | 0.070621 | 0.044096 |
| RE2 O MicroRank/TraceRCA, 20–27 | 0.039630 | 0.198148 | 0.151280 | 0.118889 |

Mốc Hit@1 của OB gấp 6,8 lần RE2 U68, nhưng chỉ gấp khoảng 2,523 lần RE2 O của hai phương pháp trace. Vì vậy chỉ so số thô hoặc chỉ thêm U sẽ bỏ mất điều kiện tập quan sát. Mốc random giúp đọc độ khó của tập ứng viên; tỉ số vượt mốc không là kiểm định khác biệt và không chuẩn hóa mọi khác biệt hệ thống, cadence, loại lỗi hay coverage thành một chất lượng chung. Không gộp hai dataset hoặc suy giá trị đồ thị từ phép so này.

CIRCA/TORAI không có phép đo chất lượng trên OB để so với T-024. T-024 còn có bảng 19 ca cho CIRCA, không lấy 19 ca đó làm cohort OB. Bài Nezha có MicroRank tại Table 3 trên 56 ca OB: AS@1=41,07%, AS@3=48,21%, AS@5=62,5%. Nguồn `runs/session-005/published-reference.json`, PDF lưu tại `results/T-008/sources/FSE2023_Nezha.pdf`, trang 8–9, §5.1–5.3.1. Cohort 56 ca khác 22 dev và bài không xác nhận cùng cửa sổ/cài RCAEval đã sửa/quy tắc hòa này; không so trực tiếp hoặc gọi tái lập. Table 3 không có BARO, SimpleRCA hoặc TraceRCA; không có số công bố tương ứng để so trong bảng đó.

Chênh với MicroRank Table3 vẫn chưa có nguyên nhân xác nhận. Trên 22 dev của T-026, MicroRank chính có 0 thành công@1, 2@3 và 8@5. Một phản ví dụ số học: nếu 34 ca ngoài dev có lần lượt 23, 25 và 27 thành công lồng nhau ở @1/@3/@5, tổng vẫn là 23/56, 27/56 và 35/56, tương ứng các phần trăm Table3 khi làm tròn. Đây chỉ là cấu hình khả thi về số học, không đọc hoặc khẳng định kết quả thật của test. Do đó 0/22 chưa loại trừ khác cohort; cũng chưa chứng minh cohort là nguyên nhân duy nhất. Khác nền/biến thể/cửa sổ và các khả năng Q-33 ở trên còn OPEN. Nguồn số dev: `tables.main.methods.microrank_full.summary.main`; nguồn số công bố: `runs/session-005/published-reference.json`.

## Kiểm đúng đắn và điều còn OPEN

Kiểm độc lập 609 method × ca × bảng (kể cả top-11) khớp từng độ đo/cận/trạng thái; phép tính độc lập dùng khóa trực tiếp, không dùng `src/p3/danh_gia.py` làm phép kiểm. 609 đối chiếu RCAEval theo hạng gốc cũng khớp. Nguồn `runs/evaluator-001/checks.json`; kiểm nhãn giả trên cả bốn bảng ở `runs/evaluator-fake-full-001/checks.json` trước chốt.

Selector/fixture 21/21 và hồi quy T-030 57/57 đã hợp lệ trên hash cuối phiên 4; không chạy lại khi hash không đổi. Mọi record/hash/source toàn vẹn; phương pháp trace giữ split operation. Mọi đầu ra TraceRCA OK/NO_EVIDENCE có ji kiểm độc lập; ERROR/TIMEOUT giữ trạng thái/thông điệp, không giả kiểm ji. Chi tiết đầy đủ `runs/full-001/diagnostics-continued-001.json`, không thấy khóa không hữu hạn hoặc sai thứ tự. Pilot không được dùng làm bằng chứng mọi ca sẽ OK.

OPEN: nền sạch/recovery, thời điểm tiêm thật, clock tuyệt đối, nguyên nhân lệch trace theo ngày, tính đại diện cho test và quyền dùng bằng văn bản chưa được tác giả phản hồi. Gỡ Nezha nếu tác giả phản đối theo Q-59. Không kết luận giá trị đồ thị. Giới hạn cần đưa vào tài liệu chính thức: cadence/coverage/lặp, các điều kiện độ nhạy, UNSUPPORTED, giới hạn mẫu ô nhỏ, MicroRank dưới mốc ngẫu nhiên với đầu danh sách tập trung nhưng nguyên nhân chưa tách, TraceRCA chưa phân biệt rõ qua khoảng hiện có, và mốc U/O khác nhau khi so dataset.
