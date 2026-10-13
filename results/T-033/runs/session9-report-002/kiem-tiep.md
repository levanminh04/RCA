# T-033 — Bằng chứng còn thiếu và phép phân xử cần Minh quyết

Những mục dưới đây là đề xuất **chưa kiểm**, chưa có quyền thực hiện ngoài SPEC hiện tại. Không đổi khóa điểm, threshold, hazard, nhãn P3 hoặc mở test. Task đã xác định đường tính ở điểm khóa; các kết luận vật lý và lựa chọn phương pháp còn OPEN. Chủ quyết định là Minh; người thực hiện/nguồn cấp dữ liệu chỉ xác định sau duyệt.

Chi phí là dự toán chưa đo, không cam kết: phụ thuộc cỡ dữ liệu, số chiều, nhịp thu và mức giữ theta. Ưu tiên dùng trung gian sẵn có và run dev nhỏ có câu hỏi phân xử; không chạy một lô surrogate rộng chỉ để có thêm cờ. Giữ mọi run/lỗi và ledger/timer; chưa có đề xuất tải mới >5GB hoặc đổi trần hiện hành.

## K1. Báo trước proxy có phải false alarm và phần nào là trễ vật lý?

- **Giải thích cạnh tranh:** thay đổi thật trước injection; lỗi nền; tải/coverage/clock đổi; detector báo biến thiên bình thường; tín hiệu sự cố xuất hiện sau proxy; detector phản ứng sau tín hiệu.
- **Bằng chứng hiện có:** raw→statistics/density→flag/CP và offset theo proxy đã lưu; không có chuẩn onset/negative sạch độc lập. File `do-tre-sau-moc.json`, `chuoi-bang-chung.json`, `tai-log.json` chỉ trả lời đường tính.
- **Input/owner cần:** Minh duyệt thu dev có fault activation/effective onset theo sự kiện ngoài detector, negative không tiêm được kiểm vận hành, workload generator timestamp/rate, clock offset và sampling/drop counters. Không dùng thời điểm vượt threshold làm nhãn onset.
- **Phép phân xử:** giữ detector/version/input/threshold/hazard và giao thức P3 gốc; chạy đối chứng cùng workload/sampling/clock trên run không tiêm và run tiêm với onset ghi độc lập. Báo cạnh nhau first alarm, first-post proxy và offset từ onset được cung cấp; lỗi nền vẫn ghi. Không thay tiêu chí sau nhìn kết quả.
- **Dự đoán phân biệt:** alarm đi cùng sự kiện được xác minh trước proxy hỗ trợ thay đổi thật; alarm trên negative sạch và telemetry hợp lệ hỗ trợ false alarm vận hành; telemetry bất thường bắt đầu muộn hỗ trợ phần tín hiệu/protocol, còn tín hiệu bắt đầu sớm nhưng margin/MAP vượt muộn hỗ trợ phản ứng mô hình. Không đủ điều kiện thì không quy nguyên nhân.
- **Phạm vi/chi phí chưa kiểm:** trước hết thiết kế một cặp dev cho một workload/fault; instrumentation và xác minh sự kiện khoảng1–2 ngày công, run15–30 phút mỗi bên, hash/projection phút đến chục phút. Có thể sai nếu negative không sạch, injection chưa phản ánh failure thực, clock không đủ chính xác hoặc telemetry bị lấy mẫu. **P6 phụ thuộc:** ngưỡng phát hiện, đánh đổi false alarms, tiêu chí trễ và loại tín hiệu được dùng.

## K2. N-Sigma: lịch sử, phân phối, lượng hóa và nhiều cột

- **Giải thích cạnh tranh:** history thích ứng mean/std; lượng hóa/zero variance; thiếu quan sát; nonstationary load; phân phối đuôi dày; OR thêm cột dù mọi phép so riêng giữ nguyên.
- **Đã phân xử:** cùng x có margin đổi với history; wide/narrow cột chung exact; thêm cột tạo first sớm hơn trong ca có chênh. Freeze tại proxy không làm first-post sớm hơn ở tập hiện hữu, nhưng đổi tập cờ. Chưa có causal baseline được chọn.
- **Phép kiểm tối thiểu:** tại P6, đặc tả trước các ứng viên history chỉ dùng quá khứ, xử lý ít quan sát/std0/NaN và quy tắc gộp, với k/SLI theo lý do đã duyệt. So trên cùng dev và cùng telemetry/clock với local baseline giữ provenance. Trước đánh giá accuracy, kiểm forecast/threshold trên input fixture và negative được K1 xác minh. Không coi N1/N3 là phép kiểm stationary hoặc independent columns.
- **Yếu tố giữ/đổi:** giữ raw/time/cột/coverage khi phân xử history; giữ history/statistics của cột chung khi phân xử aggregation; không đồng thời đổi scaling, window và threshold rồi gán effect cho một thành phần. Nếu cần kiểm multiplicity, khai giả định phụ thuộc/independence và đo joint flags, không dùng m×tail như sự thật.
- **Dự đoán:** cùng x và statistics giống thì cờ cột phải giống; chỉ gộp đổi thì các cờ cột giữ nguyên. Nếu contrast history chỉ đổi lịch báo về sau mà first không đổi, không nhận nó sửa first-delay. Khác negative/workload sẽ cần tách với effect thuật toán.
- **Phạm vi/chi phí chưa kiểm:** thiết kế hai ứng viên có căn cứ trước, pilot1dev và mở đủ30dev sau kiểm; tính thống kê dự kiến phút đến dưới1giờ EC2, công phân tích nửa–một ngày. Không phải quyền chạy hiện tại. **P6 phụ thuộc:** chọn history/aggregation/SLI; thất bại khi không có negative hoặc missing semantics khiến false flag không thể chấm.

## K3. BOCPD: kênh, mu/covariance và prior riêng

- **Giải thích cạnh tranh:** đổi X/history do scale; bỏ cột làm đổi evidence; đổi d/prior; covariance/volume term; số học; quy tắc suy CP. Factorial hiện tại phân xử scale trong mask và gói mask/d/prior, không prior riêng.
- **Bằng chứng có:** likelihood/mass/posterior/m/CP tại tất cả điểm khóa; theta ở các điểm observer giữ. 160 điểm không giữ theta không đồng nghĩa thiếu update; các parent−1 là padding.
- **Bổ sung tối thiểu cần trình:** chỉ khi lựa chọn P6 cần attribution theta tại điểm cụ thể, xin phép thu đúng parent states trước/sau và log-density decomposition tại điểm contrast chưa lưu, giữ input/params/version và so m/CP exact với run PASS. Đây là targeted instrumentation replay cần duyệt riêng vì yêu cầu hiện tại cấm rerun PASS; không tự chạy. Chọn một ca scale khác và một ca bundle khác đã khóa, giữ đối chứng có/không effect. Không thu toàn R/covariance mọi thời điểm chỉ để đủ file.
- **Prior riêng:** trước can thiệp, phải định nghĩa mô hình có ý nghĩa khi chiều đổi; zero-padding hay giữ dof danh nghĩa không tự là “cùng prior”. Xét phương án prior/projected marginal có căn cứ, fixed-space channel intervention hoặc d-sensitive sensitivity; mỗi phương án nêu phần khác cùng, giới hạn và failure condition. Minh duyệt định nghĩa rồi mới tính.
- **Dự đoán:** trong fixed input/d/prior, theta/density decomposition phải tái tạo mass/posterior và m/CP; thay scale có thể đổi toàn history nên không quy effect cho một sample. Chỉ có decomposition khác không chứng minh physical cause; prior-alone effect chỉ được gọi sau contrast thực sự cô lập prior trong mô hình đã định nghĩa.
- **Chi phí chưa kiểm:** đọc thêm nguồn/model và soạn can thiệp1–2 ngày công; targeted replay một tiền tố từng đo có thể vài phút đến trên30phút, full có thể nhiều giờ tùy d và storage. Ước lượng bằng pilot trước xin lô, không hứa dưới1giờ hoặc trong trần còn lại. **P6 phụ thuộc:** chọn prior/dimension/channel handling; không phân xử được bằng intermediates hiện có tại các theta-absent.

## K4. Preprocessing causal không nhìn trước

- **Giải thích cạnh tranh:** scale lookahead, mask lookahead, gói d/prior và tương tác. Full/I1 khác CP không chứng minh một scaler online sẽ tốt hơn.
- **Thiết kế cần:** chọn ứng viên mask/scale chỉ từ quá khứ, khai warmup/missing/range0/d0, chính sách cập nhật prior khi tập cột đổi. Xét fixed admissible schema, expanding/rolling statistics hoặc scaler robust có căn cứ; không chọn theo nhãn/root/onset hoặc tối ưu từ test.
- **Phép phân xử:** kiểm causal contract bằng thêm suffix và giữ output prefix, với cùng input prefix và không reset engine; giữ baseline native retrospective như contrast có giới hạn, thêm causal local baseline tương đương cho đánh giá P6. Freeze tại proxy hiện hữu chỉ là chẩn đoán.
- **Dự đoán:** suffix không làm đổi X/m/CP prefix của ứng viên causal; nếu đổi thì chưa đạt causal preprocessing. Kết quả tốt/xấu trên dev phải báo theo ca và coverage, không suy từ trung bình hoặc số CP.
- **Phạm vi/chi phí chưa kiểm:** đặc tả/fixture một–hai ngày công; pilot oneprefix rồi dự toán30dev bằng thời gian thực, có thể vài giờ đến nhiều hơn một ngày máy. Cần SPEC/ngân sách riêng. **P6 phụ thuộc:** detector online hợp lệ và so baseline tương đương; chưa chứng minh thành phần khắc phục false alarms.

## K5. Trace/log/workload và coverage

- **Giải thích cạnh tranh:** hệ không có sự kiện; collector không ghi đủ; service/entity mapping thiếu; request/trace semantics khác; tải thực đổi; log chỉ mẫu chưa phản ánh errors.
- **Bổ sung:** source metadata về workload units/aggregation, duration units, span/status semantics, collector sampling/drop/heartbeat và clock. Với log, xin đọc/giải mã semantics trên toàn tập message của vùng định trước và giữ log absence=N/A. Không lấy hai mẫu first/last làm chứng cả bin không lỗi. Owner nguồn benchmark/collector hoặc Minh quyết dataset/run mới.
- **Giữ/đổi:** giữ detector và vùng đọc khóa để chỉ thêm metadata/semantic checks; raw/group totals phải bảo toàn. Với run mới, ghi load độc lập và sampling counters rồi so conditional pairs. Không chữa raw benchmark bằng collector của FlashTicket.
- **Dự đoán:** missing instrumentation được xác nhận từ schema/present counters; thiếu observed events chỉ trở thành no-request nếu có completeness và request boundary độc lập. Duration start bin không trở thành completion/own-time khi chưa có phép dựng đúng semantics.
- **Chi phí chưa kiểm:** đọc tài liệu/metadata1–2 ngày công, projection trên dữ liệu sẵn phút đến chục phút nếu được duyệt; không đảm bảo tác giả cung cấp metadata. Kênh chưa từng ghi không phân xử được bằng code hiện hữu. **P6 phụ thuộc:** chọn feature/cạnh/training evaluation và giới hạn claims; B16 chỉ đặt yêu cầu quan sát, runtime completeness vẫn phải đo.

## K6. Quan hệ đồ thị có bổ sung thông tin tính toán?

- **Ứng viên:** node service/instance/host phù hợp dữ liệu; call/message edges từ parent/link, chạy-trên từ metadata. Metric ở node, log outcome nối node/span, duration/status trên edge. Tính residual conditional-parent hoặc consistency theo path, khai rõ phép dùng cạnh và giữ channel provenance. Lý do DT18 riêng với lý do sửa hạn chế đã được phân xử.
- **Giải thích cạnh tranh:** multivariate không adjacency đã đủ; graph chỉ thêm feature/window; edge sai/thiếu; shared host là common cause; thêm tín hiệu log/trace mới tạo benefit thay vì cấu trúc.
- **Phép phân xử P6/P7:** cùng signals/windows/coverage/causal preprocessing/candidate set/tuning budget, so local hoặc multivariate baseline phù hợp với graph; khi đánh giá tác dụng cấu trúc, thêm bỏ quan hệ và graph ngẫu nhiên giữ các điều kiện cần tương đương. Không gọi comparator còn dùng path/candidate topology là hoàn toàn không cấu trúc.
- **Dự đoán:** nếu adjacency có vai trò, chỉ đổi quan hệ trong điều kiện cố định phải đổi intermediate/residual/output theo giả thuyết; improvement phải có bằng chứng theo ca/ô, không chỉ mean. Nếu tín hiệu thiếu/edge không xác minh, benefit hoặc cause claims vẫn OPEN.
- **Chi phí chưa kiểm:** chưa có method/spec/parameter nên chưa ước lượng giờ máy hợp lệ; soạn mô hình và estimator1–3 ngày công, đo pilot trước trình ngân sách. **P6 phụ thuộc:** thành phần graph, nơi đặt ba kênh và căn cứ khóa thiết kế; T-033 không chọn mô hình.

## K7. Giả định thời lượng D của đoạn sự cố

- **Câu hỏi:** chấm proxy→cuối file giả định sự cố tiếp diễn bao lâu? Đây là thời lượng/kết thúc, không thay chuẩn onset.
- **Giải thích cạnh tranh:** lỗi kết thúc khi load/fault tool dừng; tác động còn kéo dài; labels chỉ cho injection start; detector báo một sự kiện khác về sau.
- **Cần Minh quyết:** nguồn start/end/fault recovery hoặc lưới D làm sensitivity với lý do đã khai trước. Giữ dự đoán và số P3 gốc; báo các cách chấm cạnh nhau. Không chọn D từ điểm đẹp, không đổi S/E của first alarm để che early.
- **Dự đoán/giới hạn:** độ đo đổi theo D cho thấy phụ thuộc giả định end; không xác nhận D thật hoặc onset. Thiếu recovery log thì chỉ sensitivity, physical validity OPEN.
- **Chi phí chưa kiểm:** chỉ chấm lại dự đoán đã lưu, dự kiến phút EC2 và nửa ngày diễn giải; thu onset/end độc lập thuộc K1. **P6 phụ thuộc:** endpoint/cửa sổ đánh giá. Chưa tạo do-nhay-D.json và chưa chạy phép D.

Minh có thể nghiệm thu phần computational của T-033 với các giới hạn trên hoặc chọn một gói bổ sung có câu hỏi rõ. Claude phản biện là đầu vào để Minh quyết, không tự mở quyền chạy hay chọn thiết kế. Actual giờ EC2 lịch sử vẫn OPEN; ledger mới chỉ duy trì dự phòng hành chính và tổng timer xử lý mới đúng quyết định ngân sách đã có.
