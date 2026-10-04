# Thẻ Sock Shop của họ RCAEval — T-019

Ngày kiểm: 04/10/2026. P2 phục vụ G1, RQ1/RQ3 và câu của cô “vì sao dùng hoặc không dùng Sock Shop”. Thẻ mô tả bằng chứng; không chọn hoặc loại dataset, không chia dev/test.

**FACT metadata và file thật:** toàn ba biến thể SS tại revision ghim không có trace. Không có span để kiểm parent (cha–con), không ghép log–trace và không đo bậc root runtime (lúc chạy). Đây là giới hạn release, không phải phần chờ quyền. Đồ thị kiến trúc nguồn chỉ là bằng chứng tĩnh; không thay thế đồ thị quan sát.

Nguồn chính: [HF dataset](https://huggingface.co/datasets/phamquiluan/RCAEval), [bài RCAEval v2](https://arxiv.org/html/2412.17015v2), [code RCAEval](https://github.com/phamquiluan/RCAEval). Revision, hash và URL file nằm trong [download-plan.json](download-plan.json), [input-metadata-check.json](input-metadata-check.json), [source manifests](sources-audit/network-manifest.json). HF HEAD được kiểm vẫn bằng revision ghim; không trộn file giữa revision.

Trạng thái: FACT nguồn công bố khác FACT metadata/file thật; USER_CONFIRMED là phạm vi Minh giao trong SPEC/LOG; không có quyết định DECIDED chọn dataset. CANDIDATE là khả năng cần kiểm. OPEN nêu đầu vào và người cần giải quyết. Số đo không tự là bằng chứng nhân quả.


## RE2-SS


### 1. Danh tính, nguồn và phạm vi đã kiểm

| Mục | Nội dung |
|---|---|
| Hệ/biến thể | Sock Shop; RCAEval RE2-SS |
| Tác giả và nguồn công bố | Pham et al.; bài v2 §3, HF/code của tác giả. RE2: stress-ng cho tài nguyên/socket, tc cho mạng. RE3: sửa mã nguồn. Prometheus/cAdvisor/Istio và Vector/Loki/Elasticsearch; Jaeger được nguồn mô tả cho bộ benchmark, nhưng không có trace SS phát hành. |
| Giấy phép | FACT nguồn: HF card và README tác giả khai báo dữ liệu MIT; code có LICENSE MIT, cần giữ notice. Không suy license từ chỉ công khai. Snapshot và phạm vi nguồn ở sources-audit/source-report.md. |
| Tổng ca / ca có / ca được phép / thực kiểm | 90 metadata / 90 ca local đã hash / 90 ca được phép / 90 ca thực đọc toàn metric, log, injection |
| Chỉ kiểm metadata | Không có ca SS ở trạng thái metadata-only sau task. Nguồn ngoài SS không mở telemetry ngoài metric OB phục vụ lineage; không mở RE2-TT ngoài dev hoặc dữ liệu khóa. |
| Tái lập | acquire.py plan/acquire → inspect_files.py → build_card.py; lệnh và môi trường trong tai-lap.md. Census/file inventory, acquisition/manifest.json và inspection/manifest.json là kết quả gốc. |

Giới hạn: khác tên hệ không chứng minh độc lập; khai báo Jaeger của toàn benchmark không bảo đảm SS có dữ liệu Jaeger. Giấy phép nguồn không tự xác nhận mọi quyền bên thứ ba.


### 2. Bảng chung tiêu chí 1–9

| Tiêu chí MRP §4 | Kết quả và trạng thái | Phạm vi/nguồn | Giới hạn / nguyên nhân khác |
|---|---|---|---|
| 1. Công khai/tải/license | FACT: toàn file đọc được, hash đúng; nguồn khai báo MIT | acquisition/manifest.json; sources-audit/source-report.md | Truy cập xác nhận ngày kiểm; license công bố không là kiểm quyền bên thứ ba. |
| 2. Root và thời điểm | FACT: tên ca có root/fault/repeat; inject_time.txt cho lúc tiêm | census-cases.csv; inspection/cases.json | Tiêm khác onset quan sát; nhãn chỉ báo RE3 có giới hạn ở mục3. |
| 3. Parent trace | FACT: không có file trace ở toàn release | file-inventory.csv; census-summary.json | Không kiểm được parent/linkage/runtime graph; kịch bản graph kiến trúc là CANDIDATE riêng. |
| 4. Metric/log | FACT: 90/90 ca có cả hai, đều đọc được | inspection/cases.json; inspection/schemas.json | ID-like trong payload chưa là request join; metric/log có không đồng nghĩa mọi root hiện đủ tín hiệu. |
| 5. Root/vị trí | FACT: 5 root; vị trí runtime OPEN, liên hệ kiến trúc nguồn ở mục3 | census-cells.csv; sources-audit/architecture-root-positions.csv | Danh tính/root và topology có thể confound; hình tĩnh không pin deployment RCAEval. |
| 6. Nhóm lỗi | FACT nguồn: tài nguyên + mạng; không code fault ở RE2 | census-cells.csv; source report | Một biến thể riêng không đủ ba nhóm. Nhãn fault không chứng minh biểu hiện ở mỗi modality. |
| 7. Ngoài root | FACT khảo sát dải metric 3q với control, theo từng ca/ô/kênh | inspection/probe-summary.csv; inspection/probe-cases.csv; inspection/probe-cells.csv | Đồng thời vượt dải có thể do tải/drift/collector/OR nhiều kênh; chưa là lan truyền nhân quả. |
| 8. Normal | FACT: 720 điểm metric trước tiêm, nhịp 1 s | inspection/boundaries.csv | Không có nhãn healthy độc lập; đủ khảo sát hiện tại chưa bảo đảm đủ học mọi phương pháp. |
| 9. Bộ độc lập | FACT: RE1/2/3 cùng họ RCAEval; không tạo thêm bộ độc lập chỉ bằng SS | sources-audit/source-report.md; lineage/report.md | Tác giả/công cụ/collector cần so toàn bảng G1; khác testbed với TT/OB chưa đáp ứng cả ba trục. |

### 3. Nhãn, số ca và khả năng phân xử

| Root | Loại lỗi gốc | Nhóm theo nguồn | Số ca | Lần lặp |
|---|---|---|---|---|
| carts | cpu | tài nguyên | 3 | 1 / 2 / 3 |
| carts | delay | mạng | 3 | 1 / 2 / 3 |
| carts | disk | tài nguyên | 3 | 1 / 2 / 3 |
| carts | loss | mạng | 3 | 1 / 2 / 3 |
| carts | mem | tài nguyên | 3 | 1 / 2 / 3 |
| carts | socket | tài nguyên | 3 | 1 / 2 / 3 |
| catalogue | cpu | tài nguyên | 3 | 1 / 2 / 3 |
| catalogue | delay | mạng | 3 | 1 / 2 / 3 |
| catalogue | disk | tài nguyên | 3 | 1 / 2 / 3 |
| catalogue | loss | mạng | 3 | 1 / 2 / 3 |
| catalogue | mem | tài nguyên | 3 | 1 / 2 / 3 |
| catalogue | socket | tài nguyên | 3 | 1 / 2 / 3 |
| orders | cpu | tài nguyên | 3 | 1 / 2 / 3 |
| orders | delay | mạng | 3 | 1 / 2 / 3 |
| orders | disk | tài nguyên | 3 | 1 / 2 / 3 |
| orders | loss | mạng | 3 | 1 / 2 / 3 |
| orders | mem | tài nguyên | 3 | 1 / 2 / 3 |
| orders | socket | tài nguyên | 3 | 1 / 2 / 3 |
| payment | cpu | tài nguyên | 3 | 1 / 2 / 3 |
| payment | delay | mạng | 3 | 1 / 2 / 3 |
| payment | disk | tài nguyên | 3 | 1 / 2 / 3 |
| payment | loss | mạng | 3 | 1 / 2 / 3 |
| payment | mem | tài nguyên | 3 | 1 / 2 / 3 |
| payment | socket | tài nguyên | 3 | 1 / 2 / 3 |
| user | cpu | tài nguyên | 3 | 1 / 2 / 3 |
| user | delay | mạng | 3 | 1 / 2 / 3 |
| user | disk | tài nguyên | 3 | 1 / 2 / 3 |
| user | loss | mạng | 3 | 1 / 2 / 3 |
| user | mem | tài nguyên | 3 | 1 / 2 / 3 |
| user | socket | tài nguyên | 3 | 1 / 2 / 3 |

FACT metadata: 90 ca, 5 root, 6 mã lỗi, 30 ô đã có; không có collision khóa root×fault×repeat. Nguồn: census-summary.json/census-cases.csv. Không suy ô không xuất hiện là file bị mất.


**Vị trí root:** runtime có mặt và bậc vào/ra đều OPEN vì không có span. Không báo root “cô lập” hay bậc0 từ việc vắng trace. Hình kiến trúc Sock Shop công khai có Front-end nối Order/Payment/User/Catalogue/Cart bằng nét không mũi tên; Order→Shipping→Queue→Queue-Master có mũi tên. Với liên hệ tĩnh bỏ User bên ngoài và icon DB: front-end bậc không hướng5; orders2; carts/catalogue/payment/user1. Nguồn sources-audit/architecture-edges.csv và sources-audit/architecture-root-positions.csv; hình đã hash trong sources-audit/diagram-manifest.json; không đặt ngưỡng hub. Đây là FACT trên hình nguồn; áp dụng sang deployment RCAEval là CANDIDATE — chưa kiểm. Tên Cart/Order/User được giữ mapping nguồn; dịch tên sang carts/orders/user chưa xác nhận deployment. Vì cạnh front-end không có hướng, không tự báo in/out-degree cho nó.


### 4. Schema thật và chất lượng ba nguồn tín hiệu

| Nguồn | Phạm vi | Schema/chất lượng thực | Giới hạn |
|---|---|---|---|
| Trace | 0 file / 90 ca | Không có span; tổng span và mẫu số parent không xác định | Không phải trace rỗng; không có trace file. Không ghép ID với span. |
| Metric | 90/90; 129,690 hàng | 75–83 cột; 35 schema khác; time int64 epoch-second, các KPI double; 86,471 null; 0 infinite; duplicate time 0 | KPI theo entity_suffix; cpu/mem/diskio/socket/workload/error/latency-50/90. Đơn vị KPI chi tiết không có metadata chuẩn trong parquet; không tự suy ms/%/MB. |
| Log | 90/90; 7,566,220 hàng | timestamp int64 epoch-second; container_name/message string; direct trace/span ID column 0 ca; keyed/Spring context rows 0, hex16/32-like rows 249408 | Regex rộng có false positive như request/user ID, không là join. RE3 Spring context chứa ID-like thật nhưng thiếu trace phát hành; không thấy ID-key không chứng minh payload hoàn toàn không có ID. |

Parent: total span/root/reference/unique-parent/missing/ambiguous/resolve đều N/A, không gán0% hoặc100%. Schema/null/constant/all-null và tên entity từng ca ở inspection/cases.json, inspection/schemas.json; refinement tách hằng khỏi all-null ở inspection/quality-refinement.json. Mẫu số log-ID là số hàng log của biến thể; không phải tỷ lệ trace coverage. Metric hằng có thể do normal, lỗi thu thập hoặc workload không chạy.


### 5. Dữ liệu bình thường và mốc thời gian

| Nguồn | Biên đầu so injection (s) | Biên cuối (s) | Midpoint − injection (s) | Pre/post rows |
|---|---|---|---|---|
| Metric | -720 | 720 | 0 | 720 / 721 |
| Log | -720–-719 | 718–720 | -1–0.5 | 31450–46016 / 9847–49542 |

Injection nằm trong mọi cửa sổ metric; ca ngoài cửa sổ: 0. Toàn 90 ca có metric biên đối xứng ±720 s; bỏ file nhãn vẫn có thể suy mốc tiêm bằng midpoint. Biên log đọc riêng ở boundaries.csv; biên hàng không chứng minh cơ chế exporter và midpoint không là onset. Nguồn không có nhãn healthy riêng/onset/end/affected region đã xác minh.


Khảo sát dùng 2/3 đầu pre làm reference, 1/3 cuối pre làm control, post từ injection; không gọi đây là normal sạch đã được xác nhận. Warm-up, drift, tải biến đổi, lỗi trước đó hoặc clock làm giả định sạch sai. Nguồn telemetry/lịch sử tải độc lập mới kiểm được giả định đó; G1 chốt giao thức, không lấp unknown bằng phần đầu file.


Đối chiếu nguồn: paper §3.3 nói 10 phút bình thường; file metric thực có 720 s (12 phút) trước tiêm. Giữ cả hai, không sửa lời nguồn hay cắt dữ liệu để khớp. Có thể mô tả giao thức chung khác phạm vi xuất file/phiên chạy; thiếu converter/deployment gốc để phân xử. Số ca của biến thể khớp bảng README; số lặp thực theo ô ở mục3.


### 6. Ước lượng thô triệu chứng lan — tiêu chí 7

Khảo sát mô tả theo T002 mục6. Với mọi kênh số: median reference, dải phân vị q của |x−median|, xét vượt dải ở control/post. Không chọn SLI bằng root; root gắn sau phép tính tất cả entity. Kênh có <30 điểm hữu hạn bị bỏ và giữ mẫu số; band0 tách riêng, không chia0. Không chạy detector/RCA, không tạo nhãn lan.

| Nhóm tín hiệu | q | Ca hợp lệ | Control ngoài root | Post ngoài root | Ca có entity post > control |
|---|---|---|---|---|---|
| all_metrics | 0.95 | 90 | 42.463% | 66.151% | 90 |
| all_metrics | 0.99 | 90 | 31.911% | 59.407% | 90 |
| all_metrics | 0.995 | 90 | 30.894% | 58.860% | 90 |
| cpu | 0.95 | 90 | 5.650% | 9.832% | 90 |
| cpu | 0.99 | 90 | 2.545% | 5.470% | 90 |
| cpu | 0.995 | 90 | 2.146% | 4.836% | 90 |
| error | 0.95 | 62 | 0.122% | 4.134% | 16 |
| error | 0.99 | 62 | 0.122% | 4.134% | 16 |
| error | 0.995 | 62 | 0.122% | 4.134% | 16 |
| latency90 | 0.95 | 90 | 10.013% | 40.127% | 89 |
| latency90 | 0.99 | 90 | 5.687% | 34.470% | 89 |
| latency90 | 0.995 | 90 | 5.164% | 33.870% | 89 |
| mem | 0.95 | 90 | 31.694% | 49.592% | 89 |
| mem | 0.99 | 90 | 25.556% | 43.920% | 88 |
| mem | 0.995 | 90 | 25.165% | 43.658% | 88 |

Tỷ lệ trên chỉ dùng entity có tỷ lệ xác định ở cả control và post, lấy cùng entity cho hai cửa sổ; trung bình trong từng ca rồi trung bình ca hợp lệ. Không gộp thành phần trăm hàng hay tỷ lệ ca “lan”. Cột cuối chỉ bất kỳ tăng dương, chưa có ngưỡng mức tăng ý nghĩa. Tách theo ô ở inspection/probe-cells.csv và ca ở inspection/probe-cases.csv; từng kênh, band, mẫu số ở inspection/channel-bands.csv; tỷ lệ entity ở inspection/entity-rates.csv. Entity không tính cặp được lưu ở inspection/paired-entity-exclusions.csv.


Có 4,098 bộ (ca,kênh,q) band0 trong 20,649 bộ kiểm; giữ band0 và null trong artifacts. Không thể gọi toàn dòng OR là bằng chứng lan: nhiều kênh làm OR tăng, mem có thể drift, workload và collector thay đổi cũng tạo đồng biến. Nhìn latency/error/cpu/mem riêng và control để tránh chép một số trung bình. Không thấy thay đổi ở metric không chứng minh log/trace không lan. Không có trace để kiểm thông tin lan theo cạnh.


Ca/kênh không tính được: 84 bộ (ca,nhóm,q) không có entity ngoài root đủ tỷ lệ ở cả hai cửa sổ và 12 cặp (ca,kênh) không đủ30điểm hữu hạn reference. Danh sách, lý do và kênh ứng viên ở inspection/probe-exclusions.csv và inspection/channel-exclusions.csv; không biến vắng error-channel hay mất số đo thành “không có triệu chứng”.


### 7. Task nào chấm được bằng nhãn hiện có?

| Task đánh giá | Nhãn cần / thực có | Chấm được đến đâu | Giới hạn |
|---|---|---|---|
| Xếp hạng root | 90/90 service root theo tên ca; injection theo file | MRR/Hit@k và NDCG theo relevance một root có điều kiện giao thức G1 | Không root operation/span và không nhãn vùng; sổ ca đã nhìn phải được xét ở G1. |
| Phát hiện theo thời gian | Có injection; chưa onset/end quan sát | Chỉ phép chấm gắn khoảng tiêm nếu G1/P7 định nghĩa, xử lý biên lộ nhãn | Không báo F1 tự phát hiện từ cửa sổ đã căn tiêm hoặc gọi độ trễ từ onset. |
| Vùng ảnh hưởng | Không có ground truth (nhãn chuẩn) tập thành phần bị ảnh hưởng | Không chấm Precision/Recall/F1 vùng | Root và khảo sát dải ngoài root không là vùng thật. |
| Bất thường từng trace | Không trace và không nhãn từng trace | Không chấm trace-level | Một dòng root_cause log không là nhãn từng trace hoặc kết quả RCA. |

Khả năng huấn luyện giám sát, checkpoint, chuyển hệ và adapter còn tùy ngân sách nhãn/giao thức G1; không suy đủ học từ tổng số ca. Nhãn test chỉ để chấm theo MRP.


### 8. Rò nhãn và thông tin phục vụ G1

- Root/fault/repeat nằm ở tên thư mục; injection ở inject_time.txt; RE3 nhãn chi tiết còn có service/pod/host/message/time. Chỉ dùng census/chấm, không đưa đường dẫn hoặc nhãn vào phương pháp.
- Biên metric toàn release này đối xứng quanh injection. Đổi tên/bỏ inject_time không loại đường suy mốc; chưa chạy detector nên chưa chứng minh có detector khai thác. Giải pháp giao thức phải chốt G1, không tự thêm cách cắt.
- Runner chính thức đã kiểm đúng revision: runner-source/main.py:283 lấy service từ đường dẫn; :341–363 chọn SLI (chỉ báo chất lượng dịch vụ), có nhánh dùng service đó; :415 truyền sli vào phương pháp. URL/revision/hash ở runner-source/manifest.json. Chỉ đọc code, không chạy/import runner. Không có adapter mới trong T019 để tuyên bố đã loại rò.
- [Sổ ca đã nhìn](so-ca-da-nhin.csv): toàn90 RE2-SS đã có kết quả RCA T006 qua torai-SS; 100 RE1-SS non-disk qua fse-ss. RE1 25disk ở T006 chỉ census metadata; T019 đã đọc metric, chưa thấy RCA trực tiếp trong manifests đã kiểm. T007 đã chạy đủ90 RE2-OB; fse-ob không có bản ghi chung với RE2-OB theo clock/nội dung kiểm, không tự là độc lập khoa học. T019 đọc số đo SS và OB metric, không chạy phương pháp.
- Sổ phân biệt full metric-content, cùng dữ liệu hữu hạn thời gian sau bỏ hàng time-null, local byte-identical, và chưa xác lập; không đồng nhất time-only với identity. Sources tên khác không tạo test mới. Không tự chia dev/test hoặc đánh dấu ca được phép test.
- Chia theo ô và bảo toàn theo WHY04/MRP là phương án G1; chưa chọn trong task. RCAEval SS/TT/OB cùng họ collector/injector/tác giả, không đủ bộ độc lập chỉ từ khác hệ.


### 9. Kích thước và chi phí — tách khỏi khả năng phân xử

| Mục | Giá trị / nguồn | Giới hạn |
|---|---|---|
| Toàn file SS biến thể | 101,086,392 byte / census-summary.json | Đây là bytes các file Parquet/text công khai, không archive và không logical uncompressed. |
| Đã có trên máy | 270 file verified cho 90 ca ở data/T-019/ | acquisition/manifest.json; data ngoài git. |
| RAM/thời gian kiểm | inspection/manifest.json; inspection/resources-snapshot.json | Peak working set lấy trong lượt2, không tổng RAM laptop; tám phiên khác có thể làm wall time thay đổi. |
| Chi phí adapter | CANDIDATE — chưa kiểm | Chưa viết/chạy adapter RCA do phạm vi cấm. Thiếu trace đòi kịch bản tĩnh riêng; không suy chi phí RCA từ inspection. |

### 10. Những điều còn mở

| OPEN | Vì sao/giả định và khi sai | Đầu vào/người giải quyết | Kết luận phụ thuộc |
|---|---|---|---|
| Root runtime degree/parent/log-trace | Release không có trace; giả định hình tĩnh tương ứng sai khi version/deployment/workload khác | Trace mới hoặc xác nhận deployment từ tác giả; Minh chốt G1 kịch bản | RQ1 theo vị trí và đồ thị quan sát RQ3d. |
| Onset/end/normal sạch | File chỉ injection, cửa sổ đã căn tiêm; pre có thể warm-up/drift | Nguồn timeline/load độc lập và giao thức G1/P7 | RQ3a tự phát hiện và delay. |
| Nhãn vùng và lan causal | Không ground truth vùng; đồng biến do tải/collector/drift cũng có thể giải thích | Thiết kế P4/G3 theo kế hoạch, không mở test mới trong T019 | RQ3c, giải thích lợi ích đồ thị. |
| Nhãn detail RE3 lỗi association | Một duplicate ngoài cửa sổ; chỉ báo log không mã nguồn/onset | Tác giả xác minh annotation; Minh quyết cách dùng nhãn ở G1 | Chấm indicator sâu, không ảnh hưởng census root theo tên. |
| Đơn vị KPI/alias/deployment | Parquet thiếu unit chuẩn; labels nguồn dùng tên khác; chưa pin deployment SS RCAEval | Cấu hình thu thập/biến đổi từ tác giả hoặc source tương ứng | Mapping đồ thị/thời gian/self-time và adapter. |
| Test/dev/baseline/label budget | Task bị cấm chọn/chạy phương pháp; sổ ghi exposure thay quyết định | Minh tại tổng hợp G1 | P3/P7 hợp lệ, không coi dữ liệu đổi tên là chưa nhìn. |

Bằng chứng đủ cho census, file quality, nhãn, biên và khảo sát metric của release này. Chưa phân xử hiệu quả phương pháp đồ thị, nhân quả lan hay topology runtime. Thiếu trace có thể do phạm vi thu thập/instrumentation/phát hành; không chứng minh hệ Sock Shop không thể tạo trace. Không kết luận thắng/thua hoặc chọn thay Minh.


## RE3-SS


### 1. Danh tính, nguồn và phạm vi đã kiểm

| Mục | Nội dung |
|---|---|
| Hệ/biến thể | Sock Shop; RCAEval RE3-SS |
| Tác giả và nguồn công bố | Pham et al.; bài v2 §3, HF/code của tác giả. RE2: stress-ng cho tài nguyên/socket, tc cho mạng. RE3: sửa mã nguồn. Prometheus/cAdvisor/Istio và Vector/Loki/Elasticsearch; Jaeger được nguồn mô tả cho bộ benchmark, nhưng không có trace SS phát hành. |
| Giấy phép | FACT nguồn: HF card và README tác giả khai báo dữ liệu MIT; code có LICENSE MIT, cần giữ notice. Không suy license từ chỉ công khai. Snapshot và phạm vi nguồn ở sources-audit/source-report.md. |
| Tổng ca / ca có / ca được phép / thực kiểm | 30 metadata / 30 ca local đã hash / 30 ca được phép / 30 ca thực đọc toàn metric, log, injection; đủ 8 file nhãn chi tiết |
| Chỉ kiểm metadata | Không có ca SS ở trạng thái metadata-only sau task. Nguồn ngoài SS không mở telemetry ngoài metric OB phục vụ lineage; không mở RE2-TT ngoài dev hoặc dữ liệu khóa. |
| Tái lập | acquire.py plan/acquire → inspect_files.py → build_card.py; lệnh và môi trường trong tai-lap.md. Census/file inventory, acquisition/manifest.json và inspection/manifest.json là kết quả gốc. |

Giới hạn: khác tên hệ không chứng minh độc lập; khai báo Jaeger của toàn benchmark không bảo đảm SS có dữ liệu Jaeger. Giấy phép nguồn không tự xác nhận mọi quyền bên thứ ba.


### 2. Bảng chung tiêu chí 1–9

| Tiêu chí MRP §4 | Kết quả và trạng thái | Phạm vi/nguồn | Giới hạn / nguyên nhân khác |
|---|---|---|---|
| 1. Công khai/tải/license | FACT: toàn file đọc được, hash đúng; nguồn khai báo MIT | acquisition/manifest.json; sources-audit/source-report.md | Truy cập xác nhận ngày kiểm; license công bố không là kiểm quyền bên thứ ba. |
| 2. Root và thời điểm | FACT: tên ca có root/fault/repeat; inject_time.txt cho lúc tiêm | census-cases.csv; inspection/cases.json | Tiêm khác onset quan sát; nhãn chỉ báo RE3 có giới hạn ở mục3. |
| 3. Parent trace | FACT: không có file trace ở toàn release | file-inventory.csv; census-summary.json | Không kiểm được parent/linkage/runtime graph; kịch bản graph kiến trúc là CANDIDATE riêng. |
| 4. Metric/log | FACT: 30/30 ca có cả hai, đều đọc được | inspection/cases.json; inspection/schemas.json | ID-like trong payload chưa là request join; metric/log có không đồng nghĩa mọi root hiện đủ tín hiệu. |
| 5. Root/vị trí | FACT: 3 root; vị trí runtime OPEN, liên hệ kiến trúc nguồn ở mục3 | census-cells.csv; sources-audit/architecture-root-positions.csv | Danh tính/root và topology có thể confound; hình tĩnh không pin deployment RCAEval. |
| 6. Nhóm lỗi | FACT nguồn: code fault f1–f4; không tài nguyên/mạng trong RE3 | census-cells.csv; source report | Một biến thể riêng không đủ ba nhóm. Nhãn fault không chứng minh biểu hiện ở mỗi modality. |
| 7. Ngoài root | FACT khảo sát dải metric 3q với control, theo từng ca/ô/kênh | inspection/probe-summary.csv; inspection/probe-cases.csv; inspection/probe-cells.csv | Đồng thời vượt dải có thể do tải/drift/collector/OR nhiều kênh; chưa là lan truyền nhân quả. |
| 8. Normal | FACT: 720 điểm metric trước tiêm, nhịp 1 s | inspection/boundaries.csv | Không có nhãn healthy độc lập; đủ khảo sát hiện tại chưa bảo đảm đủ học mọi phương pháp. |
| 9. Bộ độc lập | FACT: RE1/2/3 cùng họ RCAEval; không tạo thêm bộ độc lập chỉ bằng SS | sources-audit/source-report.md; lineage/report.md | Tác giả/công cụ/collector cần so toàn bảng G1; khác testbed với TT/OB chưa đáp ứng cả ba trục. |

### 3. Nhãn, số ca và khả năng phân xử

| Root | Loại lỗi gốc | Nhóm theo nguồn | Số ca | Lần lặp |
|---|---|---|---|---|
| carts | f1 | mã nguồn | 4 | 1 / 2 / 3 / 4 |
| carts | f3 | mã nguồn | 4 | 1 / 2 / 3 / 4 |
| carts | f4 | mã nguồn | 4 | 1 / 2 / 3 / 4 |
| front-end | f1 | mã nguồn | 3 | 1 / 2 / 3 |
| front-end | f2 | mã nguồn | 3 | 1 / 2 / 3 |
| front-end | f3 | mã nguồn | 3 | 1 / 2 / 3 |
| orders | f1 | mã nguồn | 3 | 1 / 2 / 3 |
| orders | f3 | mã nguồn | 3 | 1 / 2 / 3 |
| orders | f4 | mã nguồn | 3 | 1 / 2 / 3 |

FACT metadata: 30 ca, 3 root, 4 mã lỗi, 9 ô đã có; không có collision khóa root×fault×repeat. Nguồn: census-summary.json/census-cases.csv. Không suy ô không xuất hiện là file bị mất.

FACT nguồn: HF bảng README ghi f1–f5 cho SS, nhưng prose F5 nói riêng OB; README GitHub ghi f1–f4. FACT release: chỉ f1–f4. Giữ cả hai lời nguồn và census; không tự thêm ca f5. f1 là sai giá trị tham số, f2 thiếu tham số, f3 thiếu lời gọi, f4 sai giá trị trả về theo paper; loại lỗi không chỉ định dòng code thực của từng ca.


**Tám root_cause.txt đã đọc:** mỗi file một dòng CSV, sáu trường: giờ ngắn, timestamp nanosecond, service, message, pod, host. Bốn file carts là WARN “POST not supported”; bốn file front-end là access log HTTP500. Không chứa dòng sửa mã, stack trace, nhãn từng span/trace hay vùng ảnh hưởng.

| Ca | Loại chỉ báo | Timestamp nhãn − injection (s) | Message ghép own log | Trong cửa sổ log? |
|---|---|---|---|---|
| re3ss_carts_f1_1 | warning HTTP method unsupported | 716 | 1 | True |
| re3ss_carts_f1_2 | warning HTTP method unsupported | 161 | 1 | True |
| re3ss_carts_f3_1 | warning HTTP method unsupported | 717 | 1 | True |
| re3ss_carts_f3_2 | warning HTTP method unsupported | 160 | 1 | True |
| re3ss_front-end_f1_1 | HTTP 500 access log | 567 | 1 | True |
| re3ss_front-end_f1_2 | HTTP 500 access log | 715 | 1 | True |
| re3ss_front-end_f2_1 | HTTP 500 access log | 30 | 1 | True |
| re3ss_front-end_f2_2 | HTTP 500 access log | -10893 | 0 | False |

FACT: 8 file chỉ có 7 nội dung byte khác nhau. Nhãn front-end_f2_2 trùng f2_1; timestamp ngoài ca f2_2 và message không khớp log ca đó. Bảy file còn lại khớp service+message một hàng/ca; ba timestamp floor khớp chính xác, bốn lệch 1 s. Nguồn sources-audit/label-audit.json, inspection/root-cause-labels.json. CANDIDATE: có thể chép lại nhãn ca cũ hoặc sai clock/export/association; chưa có lịch sử annotation để phân xử. Không coi tám file là tám nhãn chỉ báo hợp lệ, không thay nhãn tiêm bằng timestamp hàng log.


**Vị trí root:** runtime có mặt và bậc vào/ra đều OPEN vì không có span. Không báo root “cô lập” hay bậc0 từ việc vắng trace. Hình kiến trúc Sock Shop công khai có Front-end nối Order/Payment/User/Catalogue/Cart bằng nét không mũi tên; Order→Shipping→Queue→Queue-Master có mũi tên. Với liên hệ tĩnh bỏ User bên ngoài và icon DB: front-end bậc không hướng5; orders2; carts/catalogue/payment/user1. Nguồn sources-audit/architecture-edges.csv và sources-audit/architecture-root-positions.csv; hình đã hash trong sources-audit/diagram-manifest.json; không đặt ngưỡng hub. Đây là FACT trên hình nguồn; áp dụng sang deployment RCAEval là CANDIDATE — chưa kiểm. Tên Cart/Order/User được giữ mapping nguồn; dịch tên sang carts/orders/user chưa xác nhận deployment. Vì cạnh front-end không có hướng, không tự báo in/out-degree cho nó.


### 4. Schema thật và chất lượng ba nguồn tín hiệu

| Nguồn | Phạm vi | Schema/chất lượng thực | Giới hạn |
|---|---|---|---|
| Trace | 0 file / 30 ca | Không có span; tổng span và mẫu số parent không xác định | Không phải trace rỗng; không có trace file. Không ghép ID với span. |
| Metric | 30/30; 43,230 hàng | 81–108 cột; 10 schema khác; time int64 epoch-second, các KPI double; 39,329 null; 0 infinite; duplicate time 0 | KPI theo entity_suffix; cpu/mem/diskio/socket/workload/error/latency-50/90. Đơn vị KPI chi tiết không có metadata chuẩn trong parquet; không tự suy ms/%/MB. |
| Log | 30/30; 2,298,238 hàng | timestamp int64 epoch-second; container_name/message string; direct trace/span ID column 0 ca; keyed/Spring context rows 182493, hex16/32-like rows 182493 | Regex rộng có false positive như request/user ID, không là join. RE3 Spring context chứa ID-like thật nhưng thiếu trace phát hành; không thấy ID-key không chứng minh payload hoàn toàn không có ID. |

Parent: total span/root/reference/unique-parent/missing/ambiguous/resolve đều N/A, không gán0% hoặc100%. Schema/null/constant/all-null và tên entity từng ca ở inspection/cases.json, inspection/schemas.json; refinement tách hằng khỏi all-null ở inspection/quality-refinement.json. Mẫu số log-ID là số hàng log của biến thể; không phải tỷ lệ trace coverage. Metric hằng có thể do normal, lỗi thu thập hoặc workload không chạy.


### 5. Dữ liệu bình thường và mốc thời gian

| Nguồn | Biên đầu so injection (s) | Biên cuối (s) | Midpoint − injection (s) | Pre/post rows |
|---|---|---|---|---|
| Metric | -720 | 720 | 0 | 720 / 721 |
| Log | -720–-719 | 719–720 | -0.5–0.5 | 33351–43961 / 4434–43946 |

Injection nằm trong mọi cửa sổ metric; ca ngoài cửa sổ: 0. Toàn 30 ca có metric biên đối xứng ±720 s; bỏ file nhãn vẫn có thể suy mốc tiêm bằng midpoint. Biên log đọc riêng ở boundaries.csv; biên hàng không chứng minh cơ chế exporter và midpoint không là onset. Nguồn không có nhãn healthy riêng/onset/end/affected region đã xác minh.


Khảo sát dùng 2/3 đầu pre làm reference, 1/3 cuối pre làm control, post từ injection; không gọi đây là normal sạch đã được xác nhận. Warm-up, drift, tải biến đổi, lỗi trước đó hoặc clock làm giả định sạch sai. Nguồn telemetry/lịch sử tải độc lập mới kiểm được giả định đó; G1 chốt giao thức, không lấp unknown bằng phần đầu file.


Đối chiếu nguồn: paper §3.3 nói 10 phút bình thường; file metric thực có 720 s (12 phút) trước tiêm. Giữ cả hai, không sửa lời nguồn hay cắt dữ liệu để khớp. Có thể mô tả giao thức chung khác phạm vi xuất file/phiên chạy; thiếu converter/deployment gốc để phân xử. Số ca của biến thể khớp bảng README; số lặp thực theo ô ở mục3.


### 6. Ước lượng thô triệu chứng lan — tiêu chí 7

Khảo sát mô tả theo T002 mục6. Với mọi kênh số: median reference, dải phân vị q của |x−median|, xét vượt dải ở control/post. Không chọn SLI bằng root; root gắn sau phép tính tất cả entity. Kênh có <30 điểm hữu hạn bị bỏ và giữ mẫu số; band0 tách riêng, không chia0. Không chạy detector/RCA, không tạo nhãn lan.

| Nhóm tín hiệu | q | Ca hợp lệ | Control ngoài root | Post ngoài root | Ca có entity post > control |
|---|---|---|---|---|---|
| all_metrics | 0.95 | 30 | 34.685% | 60.210% | 30 |
| all_metrics | 0.99 | 30 | 26.677% | 51.566% | 30 |
| all_metrics | 0.995 | 30 | 26.173% | 51.039% | 30 |
| cpu | 0.95 | 30 | 5.077% | 14.840% | 30 |
| cpu | 0.99 | 30 | 2.556% | 9.979% | 30 |
| cpu | 0.995 | 30 | 2.158% | 9.234% | 30 |
| error | 0.95 | 30 | 0.332% | 7.410% | 23 |
| error | 0.99 | 30 | 0.052% | 4.318% | 23 |
| error | 0.995 | 30 | 0.052% | 3.920% | 22 |
| latency90 | 0.95 | 30 | 3.460% | 16.262% | 30 |
| latency90 | 0.99 | 30 | 1.905% | 13.998% | 30 |
| latency90 | 0.995 | 30 | 1.855% | 13.809% | 30 |
| mem | 0.95 | 30 | 26.439% | 45.479% | 27 |
| mem | 0.99 | 30 | 21.134% | 39.939% | 27 |
| mem | 0.995 | 30 | 21.031% | 39.758% | 27 |

Tỷ lệ trên chỉ dùng entity có tỷ lệ xác định ở cả control và post, lấy cùng entity cho hai cửa sổ; trung bình trong từng ca rồi trung bình ca hợp lệ. Không gộp thành phần trăm hàng hay tỷ lệ ca “lan”. Cột cuối chỉ bất kỳ tăng dương, chưa có ngưỡng mức tăng ý nghĩa. Tách theo ô ở inspection/probe-cells.csv và ca ở inspection/probe-cases.csv; từng kênh, band, mẫu số ở inspection/channel-bands.csv; tỷ lệ entity ở inspection/entity-rates.csv. Entity không tính cặp được lưu ở inspection/paired-entity-exclusions.csv.


Có 1,698 bộ (ca,kênh,q) band0 trong 7,449 bộ kiểm; giữ band0 và null trong artifacts. Không thể gọi toàn dòng OR là bằng chứng lan: nhiều kênh làm OR tăng, mem có thể drift, workload và collector thay đổi cũng tạo đồng biến. Nhìn latency/error/cpu/mem riêng và control để tránh chép một số trung bình. Không thấy thay đổi ở metric không chứng minh log/trace không lan. Không có trace để kiểm thông tin lan theo cạnh.


Ca/kênh không tính được: 0 bộ (ca,nhóm,q) không có entity ngoài root đủ tỷ lệ ở cả hai cửa sổ và 8 cặp (ca,kênh) không đủ30điểm hữu hạn reference. Danh sách, lý do và kênh ứng viên ở inspection/probe-exclusions.csv và inspection/channel-exclusions.csv; không biến vắng error-channel hay mất số đo thành “không có triệu chứng”.


### 7. Task nào chấm được bằng nhãn hiện có?

| Task đánh giá | Nhãn cần / thực có | Chấm được đến đâu | Giới hạn |
|---|---|---|---|
| Xếp hạng root | 30/30 service root theo tên ca; injection theo file | MRR/Hit@k và NDCG theo relevance một root có điều kiện giao thức G1 | Không root operation/span và không nhãn vùng; sổ ca đã nhìn phải được xét ở G1. |
| Phát hiện theo thời gian | Có injection; chưa onset/end quan sát | Chỉ phép chấm gắn khoảng tiêm nếu G1/P7 định nghĩa, xử lý biên lộ nhãn | Không báo F1 tự phát hiện từ cửa sổ đã căn tiêm hoặc gọi độ trễ từ onset. |
| Vùng ảnh hưởng | Không có ground truth (nhãn chuẩn) tập thành phần bị ảnh hưởng | Không chấm Precision/Recall/F1 vùng | Root và khảo sát dải ngoài root không là vùng thật. |
| Bất thường từng trace | Không trace và không nhãn từng trace | Không chấm trace-level | Một dòng root_cause log không là nhãn từng trace hoặc kết quả RCA. |

Khả năng huấn luyện giám sát, checkpoint, chuyển hệ và adapter còn tùy ngân sách nhãn/giao thức G1; không suy đủ học từ tổng số ca. Nhãn test chỉ để chấm theo MRP.


### 8. Rò nhãn và thông tin phục vụ G1

- Root/fault/repeat nằm ở tên thư mục; injection ở inject_time.txt; RE3 nhãn chi tiết còn có service/pod/host/message/time. Chỉ dùng census/chấm, không đưa đường dẫn hoặc nhãn vào phương pháp.
- Biên metric toàn release này đối xứng quanh injection. Đổi tên/bỏ inject_time không loại đường suy mốc; chưa chạy detector nên chưa chứng minh có detector khai thác. Giải pháp giao thức phải chốt G1, không tự thêm cách cắt.
- Runner chính thức đã kiểm đúng revision: runner-source/main.py:283 lấy service từ đường dẫn; :341–363 chọn SLI (chỉ báo chất lượng dịch vụ), có nhánh dùng service đó; :415 truyền sli vào phương pháp. URL/revision/hash ở runner-source/manifest.json. Chỉ đọc code, không chạy/import runner. Không có adapter mới trong T019 để tuyên bố đã loại rò.
- [Sổ ca đã nhìn](so-ca-da-nhin.csv): toàn90 RE2-SS đã có kết quả RCA T006 qua torai-SS; 100 RE1-SS non-disk qua fse-ss. RE1 25disk ở T006 chỉ census metadata; T019 đã đọc metric, chưa thấy RCA trực tiếp trong manifests đã kiểm. T007 đã chạy đủ90 RE2-OB; fse-ob không có bản ghi chung với RE2-OB theo clock/nội dung kiểm, không tự là độc lập khoa học. T019 đọc số đo SS và OB metric, không chạy phương pháp.
- Sổ phân biệt full metric-content, cùng dữ liệu hữu hạn thời gian sau bỏ hàng time-null, local byte-identical, và chưa xác lập; không đồng nhất time-only với identity. Sources tên khác không tạo test mới. Không tự chia dev/test hoặc đánh dấu ca được phép test.
- Chia theo ô và bảo toàn theo WHY04/MRP là phương án G1; chưa chọn trong task. RCAEval SS/TT/OB cùng họ collector/injector/tác giả, không đủ bộ độc lập chỉ từ khác hệ.


### 9. Kích thước và chi phí — tách khỏi khả năng phân xử

| Mục | Giá trị / nguồn | Giới hạn |
|---|---|---|
| Toàn file SS biến thể | 32,726,388 byte / census-summary.json | Đây là bytes các file Parquet/text công khai, không archive và không logical uncompressed. |
| Đã có trên máy | 98 file verified cho 30 ca ở data/T-019/ | acquisition/manifest.json; data ngoài git. |
| RAM/thời gian kiểm | inspection/manifest.json; inspection/resources-snapshot.json | Peak working set lấy trong lượt2, không tổng RAM laptop; tám phiên khác có thể làm wall time thay đổi. |
| Chi phí adapter | CANDIDATE — chưa kiểm | Chưa viết/chạy adapter RCA do phạm vi cấm. Thiếu trace đòi kịch bản tĩnh riêng; không suy chi phí RCA từ inspection. |

### 10. Những điều còn mở

| OPEN | Vì sao/giả định và khi sai | Đầu vào/người giải quyết | Kết luận phụ thuộc |
|---|---|---|---|
| Root runtime degree/parent/log-trace | Release không có trace; giả định hình tĩnh tương ứng sai khi version/deployment/workload khác | Trace mới hoặc xác nhận deployment từ tác giả; Minh chốt G1 kịch bản | RQ1 theo vị trí và đồ thị quan sát RQ3d. |
| Onset/end/normal sạch | File chỉ injection, cửa sổ đã căn tiêm; pre có thể warm-up/drift | Nguồn timeline/load độc lập và giao thức G1/P7 | RQ3a tự phát hiện và delay. |
| Nhãn vùng và lan causal | Không ground truth vùng; đồng biến do tải/collector/drift cũng có thể giải thích | Thiết kế P4/G3 theo kế hoạch, không mở test mới trong T019 | RQ3c, giải thích lợi ích đồ thị. |
| Nhãn detail RE3 lỗi association | Một duplicate ngoài cửa sổ; chỉ báo log không mã nguồn/onset | Tác giả xác minh annotation; Minh quyết cách dùng nhãn ở G1 | Chấm indicator sâu, không ảnh hưởng census root theo tên. |
| Đơn vị KPI/alias/deployment | Parquet thiếu unit chuẩn; labels nguồn dùng tên khác; chưa pin deployment SS RCAEval | Cấu hình thu thập/biến đổi từ tác giả hoặc source tương ứng | Mapping đồ thị/thời gian/self-time và adapter. |
| Test/dev/baseline/label budget | Task bị cấm chọn/chạy phương pháp; sổ ghi exposure thay quyết định | Minh tại tổng hợp G1 | P3/P7 hợp lệ, không coi dữ liệu đổi tên là chưa nhìn. |

Bằng chứng đủ cho census, file quality, nhãn, biên và khảo sát metric của release này. Chưa phân xử hiệu quả phương pháp đồ thị, nhân quả lan hay topology runtime. Thiếu trace có thể do phạm vi thu thập/instrumentation/phát hành; không chứng minh hệ Sock Shop không thể tạo trace. Không kết luận thắng/thua hoặc chọn thay Minh.


## RE1-SS — ghi ngắn

FACT toàn metadata/file: 125 ca =5root×5fault×5lặp, 25 ô; 125 metric+injection, log0/trace0. Tổng15,432,409byte. Đây là corpus metric, không đáp ứng trace TC3. Schema/biên được kiểm đủ125ca, census-summary.json và inspection/boundaries.csv theo artifacts. CANDIDATE kịch bản graph từ kiến trúc; không coi là trace benchmark.

Sổ lineage xác nhận local fse-ss100ca byte-identical RE1-SS local, nhưng chuyển Parquet HF có loại dòng thiếu time ở user_mem_1 và catalogue_disk_3 (disk không ở fse). Phần finite-time khớp với tolerance ghi manifest; không nói bản HF bảo toàn mọi dòng metric. T006 đã RCA100ca qua fse-ss;25disk chưa có evidence RCA trực tiếp. Không chọn/chia test.


## Kết quả gốc và phần cần Minh quyết

Đính chính task cũ ở dinh-chinh-task-cu.md; nội dung cần ghi tài liệu chung ở de-xuat-tai-lieu-chung.md. G1 quyết dùng/không dùng SS, kịch bản trace hay kiến trúc, phạm vi nhãn và cách chia sau khi xét sổ đã nhìn. Không có phương pháp RCA hoặc detector nào chạy trong T019.
