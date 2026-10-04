# Nháp nguyên văn cho tài liệu chung — chưa được Minh duyệt

Không sửa các file đích. Mọi mục dưới là CANDIDATE, trừ lời ủy quyền đã được Minh nêu trực tiếp. Không khóa dataset/split/cửa sổ P3.

## 1. docs/DECISIONS.md — ghi ủy quyền

Cũ: chưa có dòng T-014 Đợt 1.

Mới (chèn dòng, mã do Minh/phiên tổng hợp cấp để tránh đụng phiên khác):

`| Q-<mã kế tiếp> | 04/10 | Minh ủy quyền Codex tự viết và tự duyệt SPEC rồi triển khai T-014 theo prompt Đợt 1; người phản biện Claude. Ngoại lệ tự duyệt chỉ cho T-014; phạm vi ghi, dữ liệu và ngân sách giữ theo prompt. | tasks/T-014-ho-so-circa/SPEC.md và LOG.md; chưa duyệt đóng task hay cấu hình P3. |`

Lý do: quyết định phiên phải ở nguồn sự thật, nhưng prompt cấm người làm ghi DECISIONS. Kết luận phụ thuộc: tính hợp lệ của SPEC/phạm vi triển khai, không phải độ đúng của số liệu.

## 2. docs/WHY.md — scorer CIRCA tham chiếu

Cũ: chưa có mục chọn RHT hay RHT+DA của Q-38.

Mới:

`## WHY-<mã kế tiếp>. CIRCA scorer tham chiếu cho hai nguồn đồ thị — Đề xuất, chờ G1`

`- Chọn cho hồ sơ/kiểm T-014: RHT-only với LinearRegression và CaseData 1s của RCAEval là cấu hình tham chiếu chung; RHT+DA(threshold3) chạy riêng để kiểm cơ chế. Không chốt cấu hình P3.`

`- Vì sao: bản CIRCA-PC mà RCAEval/T-006 thực thi chỉ gọi RHT. Giữ cùng scorer và cửa sổ phục vụ đối chiếu hai cấu hình PC/kiến trúc với bản RCAEval. Đó là lý do chọn RHT-only cho biến thể kiến trúc tham chiếu; chưa cô lập tác động của nguồn đồ thị vì còn khác ứng viên, parent sets và chiều cạnh. Không chọn theo accuracy. Bài CIRCA đầy đủ dùng RHT+DA; thực nghiệm Oracle dùng SVR(sigmoid). Hai bản tham chiếu không được gọi là bản đầy đủ của bài.`

`- Phương án đã xét: (1) cấu hình tham chiếu chung linear RHT theo RCAEval; (2) mỗi nguồn theo prior work riêng: PC dùng linear RHT của RCAEval, kiến trúc dùng SVR(sigmoid)+RHT+DA của bài; (3) dùng SVR+RHT+DA cho cả hai nguồn. Phương án2 có căn cứ bài và cơ chế nâng điểm ancestor cho kiến trúc, nhưng khi so hai nhánh sẽ đổi cả mô hình/scorer. Phương án3 đổi mô hình/scorer của PC. PC cyclic làm DA không có cùng bảo đảm DAG; lý do này không loại DA trên metric graph kiến trúc đã cố định là DAG. RHT+DA với hồi quy tuyến tính đã kiểm ở hai nhánh; bản empirical SVR+RHT+DA kiến trúc đầy đủ chưa kiểm. Chưa chọn cấu hình P3.`

`- Bằng chứng: paper/cong-bo-circa.csv; hai hồ sơ T-014; snapshot và independent comparisons. Fixture DA trong SCC cho thấy có thể phụ thuộc thứ tự duyệt. Không suy điểm cao của một biến thể thành lý do chọn.`

`- Kết luận phụ thuộc: diễn giải ví dụ và yêu cầu đầu vào G1. Chênh PC/kiến trúc còn bị ảnh hưởng bởi candidate coverage, graph density, mapping và việc PC học cả đoạn fault; không chứng minh RQ3d. Ví dụ giữ272 ứng viên kiến trúc so với270 PC,156 so với30 metric không cha; native coverage kiến trúc chỉ124. Ngữ nghĩa chiều cạnh cũng khác. Metric output DAG30/30 không chứng minh call/meta graph thỏa giả định DAG:24/30 cyclic và cạnh thay đổi theo seed. Nguồn: runs/regression-route-summary.json; graphs/aggregate.json; hai hồ sơ.`

## 3. docs/WHY.md — mapping và coverage CIRCA kiến trúc

Cũ: Q-38 giao mapping riêng schema, chưa có mục WHY cho rule/coverage thực thi.

Mới:

`## WHY-<mã kế tiếp>. Adapter CIRCA kiến trúc cho schema RCAEval — Đề xuất, chờ G1`

`- Mapping theo ý nghĩa suffix: workload→Traffic; cpu/mem/socket/diskio→Saturation; latency/quantile→Latency; error→Errors. Cột lạ hoặc thiếu service đánh dấu, không đoán từ nhãn. Đây là adapter của schema RCAEval, không là mapping phổ quát cho mọi hệ.`

`- Call graph: resolve parent bằng (traceID,spanID), cả hai span trước mốc, nối caller→callee; không suy cạnh thiếu từ service nhãn. Luật meta và empty-meta forwarding gọi đúng code CIRCA theo cấu hình tests/alg/sgraph/index.yml.`

`- Adapter giữ mapped isolated metric như ứng viên không cha, không thêm cạnh. Đối chứng coverage gốc giữ riêng. Vì sao: nguồn trace không có một service không đồng nghĩa metric service đó không tồn tại; mất metric im lặng làm tập ứng viên đổi. Phương án gốc StructuralGraph.visit bỏ metric không có cạnh đã được kiểm và báo riêng; không coi candidate extension là thay đổi thuần nguồn graph.`

`- Bằng chứng: graphs/summary.csv và từng graph report; builder-fixtures.json; example-architecture và example-architecture-original-coverage. Sự thiếu trace có thể do instrumentation, tải/reference hoặc parent resolve; không phải bằng chứng độc lập nhân quả.`

`- Kết luận phụ thuộc: khả năng áp dụng đầu vào, candidate universe và ví dụ. Không khẳng định retention cải thiện accuracy; không chốt dùng adapter retention ở P3 trước Minh duyệt.`

Nối vào mục WHY mapping/coverage ở trên (nguyên văn đề xuất):

`- Call trace trước mốc nhưng graph chấm dùng mappings từ cột sau preprocessing600điểm gồm sau mốc; dropconstant và empty-meta forwarding vì vậy có thể mang thông tin incident telemetry. Giữ protocol metric của RCAEval để soi scorer/graph trong tái lập; chưa chọn protocol healthy-only/online choP3. Phương án xác định schema chỉ từ normal cần chốt timing/data availability trướcbenchmark, không chữa sau xemaccuracy. Kết luận phụ thuộc: phạmvi graphpre-mốc, nhãn/boundary và candidateuniverse; khônggọi adaptation là graph hoàn toàn độc lậpincident.`

## 4. docs/STATE.md — phần prose cũ

Cũ: `**T-001** và **T-002**, chạy song song, mỗi task một phiên.` trong Task đang mở; bảng ghi hai task Xong.

Mới đề xuất: `Task đang mở được xác định theo cột Trạng thái của Mục lục task. Chi tiết và vai trò từng task ở SPEC/LOG của task đó.`

Lý do: hai nguồn trong cùng file lệch, dễ giao sai task. Chưa sửa vì chỉ được sửa dòng T-014. Minh/phiên tổng hợp quyết nội dung đúng với tất cả phiên hiện hành. Kết luận phụ thuộc: routing phiên, không số khoa học.

## 5. Tài liệu khoa học chung sau review

Các đính chính nguyên văn cho T-001/T-006 và khác biệt PC directed edge ở dinh-chinh-task-cu.md. Không tự sửa bản đã phản biện. MRP/K1 nếu đưa vào hồ sơ tổng hợp cần phân biệt RHT-only linear1s của RCAEval với empirical CIRCA SVR+DA1min, metric candidates bị bỏ và phép kiểm normal-normal thất bại. Số phải lấy từ các file T-014 được dẫn; không dùng timing laptop tranh tải làm số chính thức. Đây là nội dung cần đưa vào tài liệu, không đề xuất thêm cổng/quy trình.

## 6. docs/knowledge/K1-phuong-phap-rca.md — tách paper và implementation

File đích: K1 §C.6, dòng Detector/score.


Đoạn cũ, nguyên văn K1 dòng206:

> - **Detector/score.** **NO SEPARATE ANOMALY DETECTOR**. Mỗi metric regression theo graph parents trên reference window; residual giả định Gaussian, chuẩn hóa và lấy maximum trong test interval. Cutoff cố định `3` lọc candidate. Graph trực tiếp quyết định parent set nên đổi graph có thể đổi score.

Đoạn mới đề xuất, nguyên văn:

> - **Detector/score.** **NO SEPARATE ANOMALY DETECTOR**. Mỗi metric regression theo graph parents trên reference window; residual giả định Gaussian i.i.d., chuẩn hóa và lấy maximum trong test interval. Paper §4.3 gọi các metric score dưới `3` là không thuộc root-cause indicators. Trong code CIRCA, cấu hình RHT+DA dùng ngưỡng `3` để quyết node nào nhận thêm child score và node nào truyền descendant evidence; code vẫn xếp mọi scored metric, không lọc output bằng ngưỡng này. RHT-only không có cutoff `3`. Ngưỡng này không phải incident detector. Graph trực tiếp quyết định parent set nên đổi graph có thể đổi score.

Lý do: câu cũ có thể được hiểu rằng code trả một candidate set đã lọc3 hoặc dùng3 để phát hiện incident. Hai cách hiểu đó không khớp code. Cách hiểu câu cũ chỉ mô tả abnormal-candidate concept của paper có nguồn, nên cần phân biệt phạm vi thay vì phủ nhận paper.

Kết luận phụ thuộc: universe dùng để đánh giá metric/service; ý nghĩa control normal/normal; yêu cầu có external detector khi triển khai; số nodes được giữ ở RHT/DA; không coi top1 từ ranker luôn là một incident/root có nghĩa. Không suy rằng score<3 chứng minh vô can: θ là heuristic của DA, không bảo đảm nhân quả trên mọi dữ liệu.


File đích: K1 §C.6, chèn sau Giới hạn tác giả (cũ: chưa có kiểm implementation T-014).

Mới đề xuất:

`- **Kiểm implementation P1 (T-014).** Trên30ca dev RE2-TT, graph gọi/meta có24ca cyclic, dù native visit trả metric DAG cho30ca. Rebuild với seed0/1 thay cạnh của24ca cyclic; không suy DAG đầu ra thành giả định DAG đầu vào đã đúng. Trên ca chọn trước theo số cột nhỏ nhất, RHT architecture khớp script độc lập từng điểm; control train/test/trace hoàn toàn trước mốc vẫn có60/270metric≥3. Điều này chỉ là kiểm P1 của một ca, không ước lượng false-positive toàn dataset; không gọi top1 normal là root có ý nghĩa. Nguồn: results/T-014/graphs/aggregate.json, runs/builder-hashseed-1.json, paper/compare-example-architecture/comparison.json, runs/normal-sanity-explained.json.`

Lý do: bằng chứng điều kiện chạy phải được phân biệt với tính hợp lệ khoa học. Nguyên nhân khác còn có trace thiếu, call cycle thật, thứ tự SCC, mapping, proxy regression và normal reference không phủ regime. Kết luận phụ thuộc: điều kiện áp dụng architecture và phép kiểm G1; không tự sửa graph hay thêm detector.

## 7. docs/DECISIONS.md — máy EC2 thay thế do Minh cung cấp (ghi nhận trước lượt chạy tiếp)

Cũ: chưa có ghi nhận EC2 thứ hai cho T-014.

Mục này giữ ghi nhận lịch sử tại thời điểm chỉ kiểm SSH, trước lệnh Minh chạy tiếp. Trạng thái hiện hành và cách báo ngân sách ở §8; hai lượt PC trên máy thứ hai đã hoàn tất.

Mới đề xuất (mã do Minh/phiên tổng hợp cấp):

`| Q-<mã kế tiếp> | 04/10 | Minh cung cấp EC2 thứ hai 3.26.62.217, key2.pem, yêu cầu kiểm SSH và cho chuyển sang máy này nếu cần EC2. Kiểm SSH thành công; không hiểu chỉ dẫn chuyển máy thành ngoại lệ ngân sách Q-40. | results/T-014/runs/ssh-ec2-2.json; tại thời điểm chỉ kiểm SSH chưa chạy method trên máy thứ hai. |`

Lý do: ghi rõ ủy quyền thay máy mà không tự tăng ngân sách. Kết luận phụ thuộc: khả năng kết nối/đầu vào môi trường và quyền chuyển máy; không phải runtime hay điểm phương pháp. Ước lượng trước chỉ dẫn chạy tiếp khi đó: lượt PC mới khoảng30phút, accounting đã10746.553/10800giây tính cả chờ; ngoại lệ Q-40 chưa có quyết định riêng. Đây là tình trạng trước lượt mới, không phải đề nghị chạy còn chờ. Không reset theo máy/task; kết quả cuối ở §8.

## 8. docs/DECISIONS.md — yêu cầu tiếp tục T-014 và phân biệt cách tính ngân sách

Cũ: máy thứhai mới được kiểmSSH; accounting cũ tính4171.455squeuekhông cóworker vào budget.

Mới đề xuất nguyên văn (mã do Minh/phiên tổng hợp cấp):

`| Q-<mã kế tiếp> | 04/10 | Minh yêu cầu: “vậy dùng ec2 chạy lại và hoàn thành toàn bộ task”; sau phản hồi REVIEW, Minh: “duyệt, sửa toàn bộ”. Đã chạy tiếp permutation và normal-PC trên EC2 thứ hai. Codex từng loại queue khỏi phép tính ngân sách; đây là cách triển khai của người làm, không phải bằng chứng Minh duyệt đổi định nghĩa Q-40. Worker đã ghi9335,006s, cộng dự phòng900s là10235,006s. Cộng queue4171,455s, các khối chạy/chờ đã ghi13506,461s, vượt10800s theo cách cộng này; cộng cả dự phòng là14406,461s, không phải thời gian thực đo. Ngoại lệ Q-40 cho lượt tiếp tục chưa có quyết định riêng. | results/T-014/runs/followup-cost.json; tasks/T-014-ho-so-circa/LOG.md; Q-40 hiện hành. |`

Lý do: lưu đúng lời Minh và phân biệt lời ấy với diễn giải của người làm. Chỉ dẫn chạy tiếp và duyệt sửa báo cáo có thật; chưa có chứng cứ trong repo rằng Minh duyệt riêng việc đổi ngân sách trước lượt chạy. Q-40 vẫn nói ba giờ chờ thực tế, không đặt lại theo máy/task. Tổng các khối đã ghi vượt ba giờ; tiny checks chưa có timer đủ và900s là khoản dự trù, không thay thời gian thực đo. Kết luận phụ thuộc: báo cáo chi phí và xử lý sai lệch/ngoại lệ Q-40; không ảnh hưởng phép tính khoa học đã kiểm. Không cam kết kiểm mới ngoài phạm vi hoặc dùng cách tính này làm quy tắc chung.

## 9. K1 §C.6 — giới hạn của PC stable và phép kiểm đổi cột

Cũ: chưa có kết quả học lại PC sau khi đảo cột ở quy môTrain Ticket.

Mới đề xuất nguyên văn:
`- **PC stable không đồng nghĩa toàn bộ pipeline bất biến theo cột.** T014 kiểm lại một ca dev273cột: skeleton giữ nguyên,667cặp endpoint và258/270điểm đổi; lần chạy đồng thời đổihost/compiler nên chưa tách riêng mọi nguyênnhân. Fixture cùngmáy chỉđổi nodeorder, giữ separating sets, xác nhận cơchế uc_priority=2 ưu tiên collider đãđịnhhướng theo thứtự duyệt. stable=True chỉ áp dụng skeleton removal. Không gọi cachedscorer permutation PASS là bằngchứng discovery invariant. Nguồn: results/T-014/runs/ec2-2-permuted/comparison.json; paper/orientation-order-fixture.json.`

Lý do: cho người tổnghợpG1 biết cột/time/window/version làđiều kiện thựcthi, không chỉ fileđầu vào. Kết luận phụthuộc: tính táilập/robustness của PC và quy tắc đóngbăng cấu hình P3. Không chọn thứtự/uc_priority từ accuracy, không kếtluận mọi667cạnh đổi chỉdo thứtự.
