# Gói bổ sung T032/T033 — tổng hợp ngày 13/10/2026

**Đã hoàn tất các phép kiểm và phần giải thích đã xác định của gói bổ sung.** Hai EC2 hoàn tất 240/240 lượt; kiểm toán độc lập và bảo toàn được dẫn ở cuối báo cáo. Đây là báo cáo người làm, không tự nghiệm thu T032, đóng RQ2/G2 hoặc chọn P6.

## 1. Đọc kết quả ở đâu

| Nội dung Minh cần | Tài liệu |
|---|---|
| Top 1/2/3 đầy đủ, mẫu số, các biến thể và cách chấm khi hòa | [Bảng xếp hạng](t32/ranking-explanation-001.md), kèm JSON có số từng ca/seed và nguồn |
| Thuật toán nào dùng đồ thị, log/trace/metric đặt ở đâu; đồ thị thống kê khác đồ thị gọi dịch vụ | [Đầu vào và đồ thị](t32/ranking-explanation-002-inputs-graphs.md) |
| MicroRank, CIRCA, return/exception, P99, phép tính trên cạnh | [Báo cáo T032](t32/REPORT.md) và [ledger T032 cuối](t32/ledger-progress-003.md) |
| TORAI A và đường chạy mã tác giả TraceRCA có đủ đầu vào | [Báo cáo nhánh root](root-probes-report-v3.md) |
| BOCPD, N-Sigma, log backend, cửa sổ và giới hạn phát hiện | [Báo cáo T033](../../../T-033/runs/bo-sung-toan-dien-20261012-001/t33/report-final-004.md) |
| Từng câu KT1–16/K1–7 đã trả lời tới đâu | `closure-ledger.json` và các ledger nguồn được dẫn trong đó |
| Kiểm toán, hash, lỗi được giữ và bàn giao | `audit/`, `manifest-final.json`, `checkpoint-final.md`, `handoff-final.txt` |

Gói này ghi bổ sung dưới hai task hiện có. Các báo cáo cũ, bảng P3/P4 và nghiệm thu lịch sử giữ nguyên. Những bản `progress` và checkpoint trước chỉ mô tả thời điểm chúng được ghi; bản tổng hợp cuối và ledger cuối chỉ rõ đầu ra nào thay phần diễn giải cũ.

## 2. Gói bổ sung trả lời được gì

Kết quả có giá trị cho việc chọn hướng P5/P6 vì đã lần thêm từ đầu vào qua phép tính đến hạng hoặc báo động. Một số giải thích trước đây được củng cố; một số phải thu hẹp. Gói không chứng minh phương pháp đồ thị mới sẽ tốt hơn, không chọn một thiết kế P6 bằng kết quả dev, và không tạo nhãn vật lý chưa có trong dữ liệu.

| Nhóm câu hỏi | Bằng chứng phân xử mới | Hệ quả cho P5/P6 |
|---|---|---|
| Return/exception có thật sự thiếu tín hiệu? | Log tại root có phản ứng; có metric tỷ lệ thành công giảm. Luật chỉ đếm tăng hoặc bỏ cột hằng ở nền có thể không sử dụng phản ứng đó. Phân tích duration giữ nền/cửa sổ và composition phù hợp. | Cần xét chiều của tín hiệu, kênh quan sát và việc giữ cột; không quy mọi ca sai thành dataset không có tín hiệu. |
| MicroRank sai ở trọng số, counts hay phân nhóm? | Đã thu dictionary, graph, ma trận, prior, weights, counts, DStar và phép max theo service; đối chứng W×counts trên support chung. Tác dụng đổi W phụ thuộc phân nhóm, có điều kiện giúp và điều kiện làm kém. | Không có căn cứ cho quy tắc chung “bỏ trọng số là sửa được”. Phải nêu support và chuỗi tính toán khi thiết kế scoring. |
| CIRCA chỉ nhạy vì ít điểm train? | Giữ nút/cha và test; so đoạn sớm/gần, đoạn dài và các mẫu cùng số điểm trải trên đoạn dài. Độ dài đơn lẻ không giải thích đủ. | Cần xét phân phối, thời điểm, pha lấy mẫu và residual scale; không coi tăng train là lời giải đã chứng minh. |
| TORAI A nghiêng về service khác vì đâu? | Dựng mọi cột đóng góp, tổng service và margin; kiểm counts dựng lại, ảnh hưởng các ô lệch và cùng predicate descendant. | Đường tạo điểm được giải thích; candidate encoder và quan hệ quan sát có hợp đồng cụ thể. Không suy nguyên nhân vật lý từ hạng hoặc cây thiếu quan hệ ẩn. |
| TraceRCA tác giả có đầu vào nào chạy được? | Chạy đủ đường latency với nền sẵn có, các cấu hình khai trước; kiểm công thức điểm, mining/caps và nhóm hòa. | Cần so sánh nghiêm túc phương pháp có sẵn. Không suy mọi phương án dùng cạnh hiện có đều không đủ từ một bản cài khác. |
| BOCPD phụ thuộc prior, tiền xử lý và lặp mẫu thế nào? | Giữ nguồn native và chạy các can thiệp đã khai trên đủ 30 ca; kiểm X/schema, m/CP, warmup và ánh xạ thời gian. | Có bằng chứng về độ nhạy tính toán. Chưa có nhãn độc lập để gọi nhiều hoặc ít CP là tốt hơn. |
| Log có outcome không? | Đọc cả access log và literal phản hồi backend, kiểm lại toàn bộ message trong vùng đã khóa; đối chiếu mã nguồn công khai có điều kiện. | Có thông tin outcome ở vị trí cụ thể; còn phải phân biệt phản hồi nghiệp vụ, HTTP được serialize, trạng thái trên đường truyền và invocation được nối đúng. |

Nguồn cho các dòng T032: `t32/findings.json`, báo cáo và ledger tương ứng. Nguồn T033: `engine-final-summary-001.json`, các summary theta/marginal/rolling/log và audit trong hai thư mục bổ sung. Không cộng các cờ hay các cơ chế chồng lấn thành tỷ lệ “nguyên nhân thất bại”.

## 3. BOCPD: đã chạy đủ, nhưng không dùng số CP làm chất lượng

30 ca × (native sham + 7 nhánh) = 240 lượt, gồm 30 phép đối chiếu native và 210 can thiệp. EC2 T33 giữ ca 1–14; EC2 T32 giữ ca 15–30. Mỗi ca phải khớp m/CP native trước khi dùng can thiệp. Các đầu ra đã nhận bằng hash ở hai phía.

| Cấu hình | Tổng CP trên 30 ca | Điều có thể kết luận |
|---|---:|---|
| Native | 437 | Mốc đối chiếu đã đóng băng |
| Prior predictive df tăng từ 2 lên 4 | 443 | Độ nhạy với prior trên cùng X, số chiều và hazard |
| Kappa từ 1 lên 4 | 425 | Độ nhạy với sức nặng prior; không phải mức tối ưu |
| Precision-scale từ I lên 4I | 952 | Thay prior shape làm thay đổi đường posterior và cờ; không gọi thêm cờ là tốt hơn |
| Causal fixed scale | 876 | Cùng gói thay schema/tiền xử lý và chỉ phát cờ sau warmup; không cô lập riêng scaling |
| Causal expanding scale | 701 | Có giới hạn thay hệ tọa độ khi trạng thái posterior chưa chuyển tương ứng; chỉ là chẩn đoán |
| Bỏ hàng lặp, hazard theo hàng giữ lại | 360 | Đồng thời thay evidence, đơn vị run length và quy tắc quyết định CP |
| Cùng chuỗi nén, hazard theo thời gian trôi qua | 361 | So với nhánh nén theo hàng có thể kiểm riêng hazard exposure trong điều kiện đã nén |

Nguồn: T033 `engine-final-summary-001.json#/slots` và `/paired_diagnostics`; báo cáo T033 giữ đủ bảng từng ca. Tổng CP chỉ là số đếm các cờ của các phép tính tương ứng. Cờ sau warmup của causal và cờ native không có cùng điều kiện đủ tư cách ở đoạn đầu; không lấy dịch chuyển báo động đầu làm cải thiện độ trễ. So native với chuỗi nén không cô lập collector hoặc quantization. Hai nhánh nén dùng cùng X nhưng thay hazard cho tập thời điểm CP khác ở 15/30 ca; gần bằng tổng số cờ không có nghĩa gần bằng các thời điểm.

Các phép theta và marginal còn chỉ ra hai giới hạn diễn giải quan trọng. Thứ nhất, dấu của một số so sánh với trạng thái MAP cũ là hệ quả của cách chọn comparator; không được gọi tỷ lệ dấu ấy là tỷ lệ cơ chế gây CP. Thứ hai, prior trên các kênh chung có tính nhất quán marginal; không gọi riêng việc dof danh nghĩa đổi theo số chiều là bằng chứng prior gây khác biệt. Hai đường parent weight bằng 0 đã được lần tới underflow khi chuẩn hóa; log-lineage với normalization đóng băng không thay thế một lần chạy counterfactual log-domain đầy đủ.

## 4. Những kết luận đã được sửa trong chính gói

**TORAI A:** hai recipe có cùng tổng 333 ô lệch nhưng khác nhau ở hai ô, nên câu “hai bảng counts giống nhau” đã được sửa. Bộ lọc descendant cũ và `hasroot` không cùng nghĩa; đã bổ sung fixture phân biệt và kiểm lại matched A cùng native conditional top-k. Bản cũ được giữ để truy vết. Số 0 chỉ dùng trong đúng quan hệ quan sát và hợp đồng mapping/count/bin đã kiểm, không là thời gian chờ vật lý bằng 0.

**TraceRCA:** các trường điểm, key/nhóm hòa và đặc trưng được giữ khi thêm instrumentation; thứ tự hiển thị bên trong nhóm hòa có thể đổi. Không mô tả toàn bộ danh sách hiển thị là bit-exact. Nhánh latency được hỗ trợ không phải tái lập đầy đủ pipeline mặc định cần status/history và decoder còn thiếu.

**Log backend:** không viết “không có outcome ở backend”. Đã thu literal phản hồi ở backend; nghĩa nghiệp vụ của mã nguồn công khai được ghi có điều kiện vì chưa xác minh revision/container thực sự triển khai trong benchmark. Không tự chuyển status nghiệp vụ thành nhãn onset, clean negative hoặc outcome của từng span.

**Điều phối:** supervisor EC2 T32 gặp `FileExistsError` vì dùng cùng tên file hoàn tất với worker. Worker vẫn ghi đủ phần việc; cả 128 output của máy này có receipt. Không có exit code worker được supervisor ghi đầy đủ, nên không giả định hoặc ghi lại chúng thành 0. Chi tiết ở `supervisor-reconciliation-001.json`; lỗi, stdout/stderr và các lượt thử hỏng khác đều được giữ.

## 5. Còn câu hỏi nào sau gói này?

Ledger cuối bao phủ 23 câu hỏi nguồn bằng 26 dòng chi tiết; các phép kiểm hữu hạn hiện đã xác định trong gói đã hoàn tất và kiểm toán trong phạm vi ghi rõ. Điều đó không bảo đảm không bao giờ xuất hiện câu hỏi mới, cũng không biến P5/P6/test thành công việc đã thực hiện.

| Phần còn lại | Thiếu gì cụ thể | Vì sao không thể thay bằng thêm số đếm trên kết quả này |
|---|---|---|
| Physical onset, recovery/end, false alarm vận hành | Mốc ảnh hưởng thực và đoạn khỏe được xác minh độc lập | Proxy tiêm lỗi, cờ detector và status quan sát không tự tạo ground truth ấy |
| Giải thích network/queue/caller work/clock | Timestamp nhận/queue, sai số clock, ngữ nghĩa sync/async và độ phủ | Các nguyên nhân khác nhau có thể cho cùng duration quan sát |
| Phụ thuộc host/resource/data/message còn ẩn | Mapping deployment, tài nguyên và quan hệ tương ứng | Cây gọi dịch vụ không ghi đủ mọi loại phụ thuộc |
| Lineage generator/dataset deployment | Mã hoặc manifest/revision/container khớp nguồn thực | Candidate khớp nhiều ô hay câu log khớp mã công khai chưa chứng minh đúng phiên bản tạo dữ liệu |
| Phương pháp P5/P6 hoàn chỉnh | Quyết định nút/cạnh/ánh xạ, xử lý missing, scoring, calibration và đối chứng cùng evidence | Gói cung cấp căn cứ và điều kiện thất bại; chưa chọn và đánh giá một phương pháp mới |
| Khả năng tổng quát trên test | Khóa thiết kế/giao thức và quyền mở G3 | Toàn bộ phân tích bổ sung hiện tại dùng dev đã nhìn |

Các giới hạn này phải giữ cùng nguồn và hệ quả trong ledger. Nếu có thêm đúng revision, trường quan sát hoặc một thiết kế được giao, câu tương ứng vẫn có thể kiểm tiếp và vẫn có giá trị. Không gọi chúng là vô giá trị hoặc dùng “ngoài SPEC” để bỏ một phép kiểm đã làm được bằng dữ liệu hiện có.

## 6. Khớp MRP, DT18 và hướng dẫn của cô

MRP P4/RQ2 yêu cầu lần theo hạn chế và phân xử giải thích liên quan tới lựa chọn tiếp theo. Gói này bổ sung các chuỗi tính toán, ca đúng/sai, đối chứng và giới hạn nêu trên. DT18 yêu cầu đồ thị có nút dịch vụ/thành phần và quan hệ gọi, message hoặc phụ thuộc dữ liệu, cùng ánh xạ log/trace/metric. Chỉ một đồ thị phụ thuộc thống kê từ metric không tự đáp ứng mọi ngữ nghĩa quan hệ ấy; appendix chỉ rõ đồ thị từng baseline thực sự dùng.

Hướng dẫn của cô yêu cầu hiểu sâu phương pháp có sẵn rồi mới thiết kế và so sánh phương pháp đồ thị. Kết quả TraceRCA tác giả và các tương tác MicroRank/CIRCA giúp tránh dựng lý do cải tiến quá rộng. Lợi ích của cấu trúc ở phương pháp mới vẫn phải đánh giá với đối chứng cùng tín hiệu, bỏ quan hệ và quan hệ ngẫu nhiên phù hợp sau khi thiết kế được khóa. Gói bổ sung không tự nghiệm thu G2, chọn P6 hoặc mở test.

## 7. Bảo toàn và bàn giao

Hai cây kết quả mới nằm dưới T032/T033. Chỉ nối LOG/WHY/DECISIONS trong quyền đã giao và cập nhật hai dòng trạng thái; SPEC, code dùng chung, data, môi trường, baseline và kết quả cũ giữ nguyên. Không commit/push/xóa. `old-immutable-verification.json` đã kiểm 155.209 file cũ; kiểm prefix và diff cuối gói được dẫn trong checkpoint cuối. Manifest cuối liệt kê phạm vi snapshot và hash để lần theo tất cả đầu ra, kể cả lượt lỗi.

Prompt `handoff-final.txt` chép các khối mẫu để Minh tự chuyển nếu muốn phản biện chính thức. Audit trong gói là kiểm hỗ trợ; không thay người duyệt hoặc tự tạo vòng phản biện. Sau báo cáo hoàn tất, lịch heartbeat được dừng. Các EC2 không được tắt hoặc xóa dữ liệu tự động.

## 8. Kiểm cuối và phạm vi chứng nhận

[Chỉ mục audit](audit/audit-index-002.json) ghi từng phép kiểm, hash, giới hạn replay và các lượt lỗi được giữ. Audit độc lập bảng xếp hạng kiểm 668 hash nguồn, 1.059 bản chấm ca/seed và 50 hàng tổng hợp. Audit BOCPD kiểm đủ 30 nguồn, 240 slot, 210 đầu vào can thiệp và ánh xạ/quy tắc CP; không tuyên bố chạy lại toàn bộ posterior độc lập. Audit001 lỗi cách hiểu hash worker vẫn được giữ; audit002 xác minh riêng wrapper và worker gốc đúng referent, không sửa assignment.

Bảo toàn cuối: `controlled-verification-final.json` kiểm prefix bốn file nối thêm và đúng hai dòng STATE; `final-verification.json` kiểm snapshot `manifest-final.json` của hai cây bổ sung. Kiểm 155.209 file cũ đã đạt trong `old-immutable-verification.json`, không lặp lại khi không có rủi ro mới. Các kết quả FAIL/ERROR lịch sử không bị xóa hoặc đổi thành PASS.
