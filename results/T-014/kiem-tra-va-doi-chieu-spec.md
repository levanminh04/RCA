# Đối chiếu SPEC T-014 và giới hạn bằng chứng

FACT dưới đây lấy từ đầu ra đã lưu. PASS số học không đồng nghĩa graph là nhân quả hay scorer phân biệt được incident. Các lựa chọn cho P3 còn OPEN; không mở test/holdout.

| Tiêu chí xong | Kết quả đã kiểm | Bằng chứng |
|---|---|---|
| 1. Hai hồ sơ đủ9mục | Đã có bài toán, công thức, vai trò graph, defaults/file:dòng, code khác paper, giả định, ví dụ, đường nhãn, yêu cầu dataset khác. Source/revision/hash và công bố có trước chạy. | ho-so-circa-pc.md; ho-so-circa-kien-truc.md; paper/source-manifest.json; paper/cong-bo-circa.csv; LOG |
| 2. Builder và30graph/schema | Native YAML/factory khớp từng cạnh/coverage30ca. Mapping raw dev unknown0; service20–55edges, metric492–1163edges, isolates159–183; auth không call edge30ca. Input call/meta24cyclic dù output metric30DAG. Seed1 đổi cạnh24ca, seed0rebuild không đổi. Không gọi outputDAG là input causal hợp lệ. | graphs/aggregate.json; summary.csv; cycle-summary.csv; runs/native-yaml-equivalence.json; builder-hashseed-0/1.json |
| 3. RHT/DA và độc lập | Tham chiếu chung linearRHT theo RCAEval, DA3 riêng theo prior/mechanism, chưa chốtP3/chờWHY. Architecture272metric/2176phép và PC270/2160phép PASS; raw1088/1080arrays PASS. Seed0→1 trên PC cùnggraph không đổiRHT vượt tolerance, đổi25DA; replay chỉ đổi thứ tự vẫn tái hiện. | paper/compare-example-architecture/comparison.json; compare-example-pc-001/comparison.json; window-example-architecture-002; window-example-pc-001; crossseed-pc.json |
| 4. Ca chọn trước và hai ví dụ | loss3 được chọn minimumprocessed273trong30ca trước score. Cả hai có parents,111train/10test, hệ số/residual/scale/z/confidence/DA/ties tới từngmetric. Service gốc đọc sau rank; service rank1 ở hai graph là một ví dụ, không là accuracy benchmark. | runs/selection-before-scores.json; paper/vi-du-kien-truc.md/json; vi-du-pc.md/json; pc-source-alignment.json |
| 5. Chênh T006 và auditcũ | Đã kiểm và giữ reruns/fixtures/codegốc/Rpcalg. Samegraph/window scorer gốc–RE khớp2ca. MEM25 Rgraphlinear.864, SVR.960, linearDA.856, SVRDA.864; chưa tái lập.74. Backend/hướng/coverage đổi cùng nhau không cô lập nguyên nhân. N1–N5 có evidence, triển khai và đề xuất; không sửa taskcũ. | audit/bao-cao.md; verification.json; mem-target-summary.json; mem-prior-config-summary.json; dinh-chinh-task-cu.md |
| 6. PC quy mô TT/chi phí/progress | Default 600×273 xong; bổ sung full permutation và full normal-PC trên EC2₂ đều xong. Permutation FAIL bất biến: 667 cặp endpoint và 258 điểm đổi; host cũng đổi nên chưa quy riêng mọi thay đổi. Normal control FAIL 93/270≥3. Worker đã ghi9335,006s; +dự phòng900=10235,006s. Worker+queue đã ghi13506,461s, vượt10800s; cộng cả dự phòng14406,461s không phải thực đo. Q-40 vẫn là ba giờ chờ thực tế; ngoại lệ lượt tiếp tục chưa được quyết riêng. | runs/ec2-2-permuted/; ec2-2-normal/; followup-cost.json; bo-sung-ec2.md |
| 7. CSV/registry/bắtbuộc | Bảng đầu vào đúng16cột và9biến thể (4thamchiếu/DA,1empirical,4Rbackend audit). Registry ghi mọi realcase/purpose/a,b,c kể cảfailures; fixtures synthetic để riêng.30buildercensus không được gọi30caseRCAbenchmark. Mandatory corrections/proposals có nội dung. | yeu-cau-dau-vao.csv; ca-da-chay.csv; runs/verification-final.json |
| 8. Bàn giao/phạmvi | LOG kết thúc6ý+A–H và nguyên văn Prompt chung/G1, fullfilemanifest gồm repo/work/env/EC2; STATE chỉ dòngT014 được phép. Không commit/push, không ghi commondocs/taskcũ. Việc của7phiênkhác không được đưa vào file set T014. | LOG; manifest-files.csv; runs/state-updates.jsonl; verification-final.json |

Các phép kiểm bắt buộc ngoài bảng:

- Đầu ra thật không rỗng/hữu hạn, không wrapper fallback và không regressor ValueError fallback ở hai ví dụ. No-parent156kiếntrúc/30PC là cơ chế hợp lệ, không gọi nó là exception fallback (`runs/regression-route-summary.json`). PC rỗng/duplicate/parser lỗi được fixture kiểm và lưu đầy đủ.
- Architecture same-seed repeat và đảo cột khớp. PC cached scorer khớp nhưng full PC permutation FAIL; fixture cùng máy xác nhận cơ chế nhạy thứ tự uc_priority=2. Ca thật đổi cả host nên chưa quy riêng mọi thay đổi; bo-sung-ec2.md.
- Alpha/depth được kiểm trên fixture chain/collider và p≈.03: alpha.01 bỏ cạnh, .05/.1 giữ. Constant đưa thẳng PC có CI NaN, preprocess loại nó; duplicate singular wrapper có thể trả thứ tự cột; PC zeroedge trả [] mà không exception. Fixture nhỏ không thay quy môTT (`paper/kiem-pc-fixture.md`).
- **Normal-negative FAIL.** Control kiếntrúc chặt dùng windows và trace trước mốc giả:60/270≥3; arithmetic2160phép và raw1080arrays PASS, trace dictionaryjoin37472span/20edges khớp. Preprocessing của control dùng720điểm trước tiêm thật, gồm sau mốc giả; không tuyên bố nó là fully online causal control. Ranker không có detector/abstention. Không gọi security_mem823.7242 là root có ý nghĩa (`paper/normal-pretrace-verification.json`, `runs/normal-sanity-explained.json`).
- PC normal windows trên cached fault graph có 76/268≥3. Đã bổ sung full normal-PC riêng: 93/270≥3, không đạt đối chứng âm tính. Lặp RHT cùng EC2 khớp 270 điểm; độc lập Linux 1080 phép PASS và raw 1080 mảng PASS. Đối chiếu laptop FAIL bốn metric; xem normal-doi-chieu-so-hoc.md.
- Builder công thức độc lập đúng6DAG;24cyclic chỉ có nativeimplementation equivalence và hashseed sensitivity, không có chứng minh DAGformula/causal semantics. Đây là phạm vi kết quả, không việc bỏ phép kiểm rẻ để tránh finding.

Phần chưa kiểm và kết luận yếu đi:

| Phần | Lý do cụ thể và giả định | Khi giả định sai; việc phân xử |
|---|---|---|
| Giao thức chính xác sinh số BARO/TORAI/CIRCA paper | Có nguồn số trước chạy và thử backend/scorer, nhưng chưa có lệnh/config nguyên vẹn sinh đúng bảng. Không mởOraclecache/rawdata ngoàiallowlist. Không quy phần lệch còn lại cho một lỗi chắc chắn. | Nếu tác giả dùng windows/preprocess khác các file đang đối chiếu; cần code+revision+lệnh+caseuniverse của bảng, chỉ lọc allowlist trước đọc từngca. |
| Nhạy số học và permutation giữa hai máy | Full normal-PC đã chạy xong, đối chứng âm tính FAIL 93/270≥3. Bốn điểm khác giữa laptop và EC2; kiểm độc lập cùng EC2 đạt. Full permutation đổi cả host; chưa có lượt PC tham chiếu cùng host trong ngân sách còn lại. | Nếu backend đại số hoặc thứ tự phép cộng làm đổi nghiệm gần suy biến, ghim package chưa đủ; cần tách backend/parent order/centering. Fixture orientation cùng máy xác nhận một cơ chế nhạy thứ tự nhưng chưa replay separating sets của ca thật. |
| Alpha .01/.1/depth1 trên toànTT | Capdepth0 đã dùng45min khôngra graph, các default/repeat có ngân sách riêng. Không suy toy thành TT sensitivity hay cap luôn nhanh. | Nếu orientation/skeleton chi phí khác trênTT; kiểm profile+stack và cấu hìnhTT mới trong task có ngân sách. |
| Calibration/confounding/false-positive prevalence, toàn30caseRCA | ThuộcP3/P4 sauG1, không phải lýdoquyền để bỏ việcP1. Một ca arithmetic không chứng minh robustness/density/isolation causality. | Nếu reference/model/mapping không đúng; benchmark và đối chứng theo design được khóa sau, không chỉnh từ test. |
| Runtime sạch và networkbytes exact haiwheel/clone | Máy dùng chung, instrumentation; uv không giữcompressedwheelbytes. Versions+filehash ghim, payloadsaved+conservative accounting được báo riêng. Không dùngtiming tranh máy làm sốchínhthức. | Nếu cần so sánhchi phí chính thức; đo isolatedrun và lưutransfermetadata trongtaskđượcgiao, không suy từ logicalinstalledbytes. |

Lệch SPEC được ghi nối thêm ở cuốiSPEC: dùng metadataT002 thiếu29mốc; runner tiềnxửlýmain; targetedMEM25+factorialcachedgraph; pause/resume process củaT014; chuyểnnativeYAML serialization sauharness lỗi; backuphashseed lượtđầu vàcanonical0; fullPC permutationqueued; scorerCIRCAgốc kiếntrúc samecontext. Không đổi dữ liệu được phép, outputscope, P3design hay nhãn trong method.

## Trạng thái trước lượt EC2 thứ hai (lịch sử)

Đoạn sau mô tả lần bàn giao trước khi Minh yêu cầu chạy tiếp; trạng thái hiện hành của hai lượt đã hoàn tất ở mục kế tiếp và `bo-sung-ec2.md`. Tại lần bàn giao trước, full PC permutation chưa khởi worker: chờ EC2 có job khác tới hết 4171.455 giây ngân sách. Chỉ parent theo dõi ps/free, không chạy song song hai tiến trình nặng. Tổng các defaultattempt (tính cả chờ)=7142.584s; capdepth0=2703.969s. Trạng thái terminal được copyback cùngqueue/progress. Không còn worker T014 chạy sau bàn giao.


## Kiểm bổ sung theo chỉ dẫn tiếp tục của Minh

Đảo cột/học lại PC: hoàn tất 1725.452s; 667 cặp endpoint đổi, 258 điểm đổi vượt tolerance; cùng candidate=True. Direct RHT/snapshot, số học độc lập và raw arrays đều PASS.

Full normal-PC học trên 720×275 điểm/cột trước tiêm: hoàn tất 1917.001s; 93/270 điểm≥3, top ts-security-service_mem=957.1628. RHT chính thức lặp lại cùng máy khớp từng điểm; số học độc lập trên EC2 và raw arrays PASS. Đối chiếu laptop FAIL ở bốn metric; xem normal-doi-chieu-so-hoc.md.

Nguồn/trạng thái hiện hành: bo-sung-ec2.md; runs/followup-cost.json. Các ghi thiếu ngân sách ở bảng trước là trạng thái lịch sử trước việc sửa accounting queue. Cách tính worker+dự phòng dưới3h không chứng minh tuân thủ Q-40. Tổng các khối chạy/chờ đã ghi13506,461s; khoản900s dự phòng tách riêng. Chưa có quyết định riêng về ngoại lệ, không tự thay quy tắc chung. Kiểmfactor MEM25 đã làm thêm; independentrecount100config PASS.
