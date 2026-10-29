# Bàn giao phiên thiết kế RCA — T-041

Ngày phân tích gốc 21/10/2026; sửa sau phản biện 23/10/2026 theo Q-185. Root chuẩn `D:/RCA-flashticket`. Người làm Codex; người phản biện chính thức Claude. Gói sửa đã hoàn thành và tự kiểm, **chờ kiểm lại phản biện, chưa nghiệm thu**. Chưa chọn/cài phương pháp P6, không đóng RQ2/RQ3/RQ5/G3 hoặc mở test. Quyền và lịch sử tại SPEC/LOG/DECISIONS; trạng thái mới theo LOG và dòng T-041 trong STATE, SPEC giữ lịch sử lần thực hiện gốc. Hash/revision tại manifest.

## 1. Bắt đầu từ file thật

1. Đọc `AGENTS.md`, `docs/STATE.md`, `tasks/T-041-ra-soat-nen-p3-p5/SPEC.md` và mục kết phiên cuối `LOG.md`. Đọc quyền hiện hành trước các prompt lịch sử.
2. Đọc `results/T-041/manifest.json`; kiểm bốn đích trong `outputs` (ba kết quả + SPEC) và nguồn thực dùng. Manifest không tự băm, không khóa LOG/STATE/DECISIONS đang có thể đổi. E025 kiểm toàn bộ 67 nguồn summary: 5 khớp hash, 62 thiếu ở đường dẫn khai báo (29 context, 29 graph-probe, 4 theta-density); không nhận đã kiểm raw toàn cohort hoặc dùng bản khác hash để thay. E022 giữ kết quả lịch sử của danh sách nguồn T-041 thực dùng, không đại diện đủ 67 nguồn.
3. Đọc `bao-cao.md`: §2 tự rà; §3 đường gọi thật; §4 dùng lại tới hàm; §5 chuỗi đúng/sai/phản bác; §6 H01–H26/A–G/mục tiêu; §7 hợp đồng thông tin; §8 OPEN và phần cần phân xử; §9 mức hoàn thành.
4. Tra `bang-chung.jsonl` theo ID, không in cả E001. E001 giữ trạng thái Git ban đầu rất dài, không phải dataset. E005/E012 là code/revision và danh mục hàm/dòng; E006–E008 là cặp/nguồn trung gian; E009 là duration theo operation; E010/E011 là mã và kết quả phép nhỏ; E014/E015 là kiểm nguồn thiếu ban đầu; E017 là đính chính nguồn cũ; E020 là native MicroRank. Lượt sửa: E024 giữ nguyên văn phản biện nhận trong tệp đính kèm và quyền sửa; E025 là N-Sigma/khả dụng toàn bộ nguồn summary; E026 là đối chiếu cùng operation và cùng ô; E027 là ID log Nezha và tương thích Grafana; các bản ghi sau giữ diff/tự kiểm/bàn giao.
5. Trước khi thiết kế, đọc trực tiếp phần mục tiêu trong `docs/MRP.md`, hai nguồn DT18/cô tại `docs/reference/sources/`, `docs/LESSONS.md`, lý do/quyết định liên quan; đọc phần hiện hành `docs/PLAN-P6.md`, không lấy quyền ở phụ lục cũ. `docs/DE-XUAT-HUONG-GRAFANA-RCA.md` vẫn là đề xuất. Không cần Minh copy báo cáo chat.

## 2. Nền đã kiểm và điều kiện dùng

- **P3 khác nhau theo dataset/mode.** TT metric 1s và OB 5N+5A ordinal không tương đương; marker thời gian OB không đồng bộ mọi kênh. MicroRank/TraceRCA chia span theo end; SimpleRCA theo start. Strict end và duplicate policy là một phần baseline. Đổi cửa sổ, schema, scope, nền, seed hay số học cần lượt riêng; không ghép điểm cũ vào pipeline mới.
- **Graph P5 có mục đích cấu trúc/địa chỉ.** Graph operation/entity gộp, witness và event_count không khôi phục request, duration hoặc membership. `do_thi.Prepared` bỏ hàng trùng hệt; adapter baseline Nezha giữ hàng đó. Muốn phân bổ owner–caller–callee phải giữ span/request/time index ngoài graph gộp. Phép trừ hợp khoảng con chỉ là thời gian chưa được con quan sát phủ, chưa là CPU/caller-work/network vật lý.
- **Quan hệ có mức căn cứ.** Untyped parent, CLIENT/SERVER xác minh, messaging verified link, DB/resource binding và quan hệ tĩnh không cùng nghĩa. Không fallback từ link verified lỗi sang ID. Hợp đồng tĩnh hiện hành ghim `T-036/runs/doi-chieu-smtp-001/`, gồm artifact-manifest; root R1 là lịch sử. Static signals là địa chỉ, chưa là dữ liệu runtime hoặc cạnh RCA.
- **Điểm và tập phải giữ nghĩa.** Metric sample votes, Boolean trace/log, signed robust z, residual và template severity không cùng đơn vị. Missing/new-operation/ERROR/UNSUPPORTED không được giả thành điểm 0. Giữ inventory/observed/modeled/scored/returned; nhãn service cần quy tắc gộp operation→service và hòa/blocks được khai trước.
- **Offline/online chung có điều kiện.** Hàm thuần có thể nhận cùng quan sát/scope/cutoff/state, nhưng chưa có lõi P6 được kiểm tương đương. Event end không là arrival; ±300 quanh alert cần dữ liệu tương lai; BOCPD cũ còn tiền xử lý cả file. Refractory notification chưa là lifecycle sự cố. MRP hiện hành và hướng Grafana khác nhau ở yêu cầu phát hiện; không tự thay yêu cầu MRP bằng lựa chọn hạ tầng.
- **Collector có giới hạn thông tin.** Có thể chuyển trường đã ghi, thêm observed time tại điểm nhận và báo drop. Kind/peer/message identity/outcome cần instrumentation; host/binding/revision cần deployment; onset/recovery/negative cần giao thức độc lập. B16 đã kiểm hash; chưa kiểm runtime nền tảng. P9a nhận R-01–R-10 theo nguồn T-040, chưa gửi nhóm hệ thống.

Phần dùng chung và khác biệt với `docs/DE-XUAT-HUONG-GRAFANA-RCA.md` được đối chiếu trực tiếp dưới đây (E027). Đề xuất vẫn chưa được duyệt; bảng không chọn cơ chế hoặc cửa sổ mới.

| Điểm của đề xuất | Dữ kiện đã xác minh | Dùng chung được gì / phần chưa tương thích |
|---|---|---|
| §6.1: nền 10–30 phút trước cửa sổ sự cố; cùng code đọc CSV RE2-TT/Nezha | Adapter Nezha trong quyền hiện tại chỉ đưa giá trị miền `[t−300,t+300)`; metric 5N+5A ordinal (báo cáo §3.1, E027) | Có thể chung giao diện lõi, chưa dùng nguyên nền đề xuất trên đầu vào dev này. Không suy toàn dataset không có lịch sử metric dài; mở rộng miền/cửa sổ cần giao thức và quyền riêng |
| §4.4/6.2: RED theo operation từ spanmetrics, p95 từ histogram | P3 đang dùng duration từng span; histogram/P95 không giữ từng request hoặc cùng support | Có thể khai cùng đại lượng mục tiêu, chưa coi biểu diễn/ước lượng và coverage tương đương. Cần giữ đơn vị, bucket, count, sampling và nguồn; không ghép điểm baseline cũ |
| §5.1/5.7: luật cảnh báo mở sự cố; phát hiện có graph là nhánh cân nhắc | MRP §2.3/P6 và WHY-02 hiện hành yêu cầu graph tham gia điểm bất thường | Dùng chung được thông báo/mốc và hợp đồng chấm toàn chuỗi. Luật cục bộ riêng chưa đáp ứng toàn yêu cầu hiện hành; chỉ Minh quyết đổi hướng, T-041 không thay MRP |
| §6.1: offline đọc CSV thay file OTLP bằng cùng code | Lõi thuần có thể nhận cùng quan sát/scope/cutoff/state; end-time khác arrival, dữ liệu đến muộn và sampling còn điều kiện | Chung code/format không tự chứng nhận cùng ngữ nghĩa hoặc offline=online. Adapter và điều kiện thời gian phải được đặc tả/kiểm theo nguồn trước triển khai |

Nguồn log cũng phải giữ rõ: T-008 có TraceID/SpanID và phép ghép theo file cùng phút; một header log thuộc allowlist dev đã được kiểm hash xác nhận có hai cột. P3 bỏ ID khỏi bảng log lõi. Adapter P6 cần giữ ID/provenance và kiểm missing/ambiguous/scope/time; chưa có tỷ lệ ghép toàn miền dev, không sửa adapter baseline P3 (E027; báo cáo §3.1/§4).

Bảng hàm và điều kiện chi tiết ở báo cáo §4; E012 chứa đường dẫn code/dòng và hash actual source. Không gọi runner để kiểm dùng lại: các hàm runner ghi file ngoài quyền T-041.

## 3. Kết luận có điều kiện và nguồn phản bác đã giữ

TraceRCA: ca sai order/disk lên hạng 1 khi đổi a/n; hai ca đúng cùng ô order/disk vẫn 1→1, còn ca khác ô route/socket hạ 1→10. E026 giữ phân tầng đủ loại lỗi; không lấy một cặp khác ô làm tác dụng chung của công thức. E1 có root singleton frequent bị top-selection loại; sửa điểm singleton không tự sửa selection. Không nhầm bản RCAEval, nhánh theo lời văn và mã tác giả.

MicroRank: E020 đã lần ba native capture; E026 thêm cùng station/find ở hai ca TT: coverage nhóm trace bất thường 87,5%↔41,7%, weight A khác khoảng 9,75 lần, DStar2 776,904651/hạng operation 1↔1,942160/hạng operation 4. Hai ca khác ô order/disk và auth/delay; nhóm trace/coverage/weights cùng đổi. Cờ cục bộ→membership là bước chung có ở ca đúng/sai; khác biệt này chưa cô lập nguyên nhân riêng PageRank. Các nhánh đã lưu phản bác bỏ weights như sửa phổ quát; phần quy nguyên nhân còn O05, không giao lại đọc tổng quát capture.

BARO/SimpleRCA: cùng cơ chế thang/đếm có mặt lợi và hại ở ca cùng ô; constant khác nearconstant. CIRCA: cực trị residual xuất hiện trước DA; bỏ cạnh đổi cả hồi quy lẫn DA và có ca đúng bị hạ. Composition/recency/phase/scale chưa cô lập đủ để chọn một cách chữa. TORAI B: log/template→severity/fallback đã lần với ca đúng singleton; không lấy hạng tốt làm xác nhận RCD/cấu trúc có lợi.

Return: E009 đã đọc đúng miền dev của bốn ca, toàn operation tại root, bốn cửa sổ; tổng count khớp trung gian. Có cả P95 tăng/giảm trong cùng ca. Không còn OPEN chung “chưa đọc duration theo operation”; vẫn chưa chứng minh feature mới định vị root hoặc onset vật lý.

Detection: E2 hiện hành kiểm hai ca FF/PF; sửa underflow đổi một số MAP/CP sau mốc nhưng không đổi báo đầu, không suy rộng cohort. E025: N-Sigma rolling tăng cờ OR ở 27/30 ca, giảm 3/30; 29 ca có std0 trigger cells, gồm cả ba ca giảm. Std0 là giải thích cạnh tranh chưa được cô lập, không gọi nguyên nhân chính. Chỉ 1/30 context ở đường dẫn summary hiện có đúng hash; giữ summary ở mức mô tả, không gọi báo trước tiêm là false alarm vận hành.

## 4. Phần còn mở và nơi nhận

Bảng đầy đủ phép phân xử, chi phí, owner và quyết định bị chặn ở báo cáo §8:

- **O01, nguồn có tên nhưng chưa tiếp cận:** E025 tại `/result/availability` liệt kê 67 đường dẫn của fast-summary, 5 PASS và 62 thiếu: 29 context, 29 graph-probe, 4 theta-density. Ba ca giảm N-Sigma đều thiếu context ở đây. Dấu vết EC2 ở `context-status-001.stdout`/`.timer.json`, `.stderr` rỗng; chưa biết EC2 còn giữ bản đúng byte. Minh/chủ nguồn quyết tiếp cận theo câu hỏi, không tự nhận lại toàn bộ hoặc chạy thay thế. Byte khai báo phần thiếu khoảng 29,2 MB, chi phí nhận/EC2 chưa đo; chặn từng chuỗi raw phụ thuộc nguồn, không vô hiệu hóa summary đúng hash.
- **O02/O03/O07, thiếu đầu vào hoặc semantics:** arrival/completeness; kind/queue/receive/clock; healthy/onset/recovery/load/binding và liên kết invocation đã xác nhận trong dev. Nezha nguồn có ID log nhưng P3 bỏ; phải kiểm ánh xạ dev, không suy toàn nguồn công khai thiếu liên kết. Log→span cũng chưa tự cung cấp nhãn outcome/onset vật lý độc lập. Minh/nhóm nền tảng/giao thức tải-tiêm cung cấp phần thiếu; M1 định nghĩa semantics sử dụng. Chặn kết luận online/physical/false-alarm/region thật liên quan.
- **O04/O05/O08/O10/O11, cần phép mới có giả thuyết:** selection singleton; MicroRank sau đổi bộ chia/đếm; CIRCA composition/residual; detector và underflow ngoài hai ca; schema×signal. Đọc hiện có đã làm và trỏ §5. Chỉ đề xuất can thiệp còn ảnh hưởng quyết định, giữ yếu tố so sánh phù hợp; chưa có quyền chạy trong T-041. Chi phí mới chưa đo; tham khảo runtime cũ không là dự toán giờ công.
- **O06, mô tả đã có, còn đánh giá:** feature giảm/log/operation duration cần support, composition và kiểm sức định vị; bốn ca đã xem không là test độc lập.
- **O09/O12, cần quyết định:** định nghĩa nhóm lan/“đáng kể”, hướng P6/MRP/Grafana và phạm vi tiếp. Khác biệt nền/biểu diễn/phát hiện đã nêu tại §2. Câu STATE chờ ý kiến cô có trước T-041; chưa tìm xác nhận nguyên lời trong DECISIONS, nên giữ nguồn/ý nghĩa điều kiện chờ M1 OPEN, không tự đặt hoặc gỡ. Các UV chưa thành quyết định; nghĩa vụ nguồn vẫn giữ trong MRP/P9/P10.

Không cần lặp điều tra tổng quát hoặc mở lại task cũ. Một thiết kế phụ thuộc OPEN phải nhận đúng bằng chứng/phép phân xử cần thêm, hoặc công bố giới hạn và hệ quả; thiếu quyền không xóa nghĩa vụ khoa học.

## 5. Bước tiếp chính xác

Bước hiện tại là **Claude kiểm lại phản hồi và bản sửa**, khi Minh chuyển prompt hiện hành ở mục kết phiên cuối LOG. Prompt theo mẫu, chỉ trả lời chat; chưa có quyền ghi REVIEW. Minh quyết dừng/sửa/nhận giới hạn/nghiệm thu; Q-185 chỉ duyệt sửa gói, chưa nghiệm thu T-041. Không tự gửi/mở phiên.

Khi Minh giao phiên2, dùng Prompt 2 hiện hành trong LOG rồi đọc trực tiếp gói này. Tự rà lại đề bài/nguồn/giả định và xây phương án trong chat theo quyền; không sửa file T-041, không tạo task/code/kết quả thiết kế trong repo khi chưa được giao riêng. Phải nêu node/edge, nơi log/trace/metric đi vào, phép dùng cạnh, hypothesis/alternatives/failure, nền/cutoff/candidate/aggregation và đối chứng tương đương. Tách căn cứ sửa hạn chế P4 khỏi đáp ứng DT18/nhu cầu kỹ thuật. Chưa cần hoặc được phép cài/chạy thiết kế trong T-041.

Phép kiểm rẻ để nhận gói: Python `-B` đọc manifest, kiểm SHA-256 của `outputs`, parse từng dòng JSONL và kiểm source theo path/manifest/pointer đã lưu; chỉ đọc nguồn dev được cấp quyền. Mã synthetic nằm ở E010 `/result/source`, namespace sửa ở E011; môi trường có sẵn ghi trong evidence/manifest. Không cài thêm, không gọi toàn bộ test suite tạo cache hoặc chạy baseline. Đọc E014/E015 trước khi truy raw N-Sigma để không nhận nhầm bản khác hash.
