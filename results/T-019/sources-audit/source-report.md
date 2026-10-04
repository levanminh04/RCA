# Kiểm nguồn độc lập của T-019

Codex thực hiện trong vai người làm hỗ trợ T-019; đây không phải REVIEW của Claude. Không chạy RCA hoặc bộ phát hiện. Chỉ ghi `results/T-019/sources-audit/`.

## 1. Phạm vi và kiểm nguồn

Đã đọc AGENTS, SPEC/STATE/LOG T-019, MRP §4, mẫu thẻ và REVIEW T-002. Quét toàn văn 77 file báo cáo/SPEC/LOG/REVIEW cấp đầu của T-000–T-012 để định vị nhận định liên quan SS/RCAEval/collector. T-004 chưa có task/artifact. Quét từ khóa không thay kiểm đúng đắn của mọi phương pháp hay corpus khác. Danh sách file, dòng liên quan và hash: [prior-task-relevance-scan.json](prior-task-relevance-scan.json). Đọc sâu T-002 metadata/script/thẻ; T-006 §2.2–2.4 và log đối chiếu SS/biên; T-007 §1.3/BOCPD/biên; T-003 bảng tiêu chí và báo cáo tổng. Các thẻ T-008–T-012 được xét ở mức phả hệ và tiêu chí 9, không đọc thêm telemetry của chúng.

Tái dùng 8 snapshot nguồn T-002 sau kiểm SHA256/byte từng file. Ba trang HF có 1.000/1.000/815 entry; cộng lại đúng từng entry trong tree tổng và không trùng path. [source-reuse-checks.json](source-reuse-checks.json) lưu kết quả. HF metadata HEAD và revision ghim khớp tại lúc kiểm. Tải thêm nguồn chính thức tổng **652.287 byte**, không retry hoặc lượt lỗi; không tải telemetry. Mọi URL/revision/byte/hash nằm trong các manifest mạng/kiến trúc/hình. Hình kiểm cả git-blob oid theo tree, không chỉ hash tự tính. Lệnh tái lập là các script trong thư mục này; riêng `audit_labels.py` dùng Python/pyarrow đã có ở `D:/RCA-ext/envs/py312/`.

## 2. FACT từ nguồn công bố

Giấy phép dữ liệu có hai căn cứ riêng: dataset card HF khai báo MIT, và README tác giả nói dataset do họ phân phối dùng MIT. Không suy license dataset từ code baseline của bên khác. Căn cứ ghim: `results/T-002/public-metadata/run-002/sources/hf-README.md:2,192` và `github-README.md:366`; license văn bản ở cùng thư mục. Truy cập metadata hiện thành công; không chứng minh tất cả mirror có cùng nội dung.

[Bài RCAEval v2](https://arxiv.org/html/2412.17015v2), §3.2, quy định F1 sai giá trị tham số, F2 thiếu tham số, F3 thiếu lời gọi hàm, F4 sai giá trị trả về, F5 thiếu xử lý ngoại lệ. RE2 dùng stress-ng cho tài nguyên và tc cho mạng; RE3 sửa mã. §3.3 công bố Kubernetes, metric Prometheus/cAdvisor/Istio, log Vector/Loki/Elasticsearch và trace Jaeger/Elasticsearch; tải 10–200 request/s và 10 phút bình thường. Đây là giao thức công bố chung. Nó không chứng minh Sock Shop có trace trong artifact, hoặc mọi đoạn trước tiêm sạch.

Tree code RCAEval ghim không chứa đường dẫn injector/collector SS. Notebook code-level RCA ở code công bố là ví dụ **Online Boutique cartservice**, không phải định nghĩa lỗi sửa ở carts của Sock Shop. Vì vậy chưa có chứng cứ commit/source-line gây từng lỗi SS hoặc collector deployment tương ứng. Có thể bộ thu nội bộ chưa phát hành, hay code thu ở repo khác; absence tại tree không chứng minh công cụ không tồn tại.

## 3. FACT đếm từ metadata toàn release

Tính độc lập bằng [audit_metadata.py](audit_metadata.py), không gọi script cũ và không suy từ hai mẫu. [ss-census.csv](ss-census.csv), [ss-cells.csv](ss-cells.csv), [ss-files.csv](ss-files.csv), [ss-summary.json](ss-summary.json) giữ từng ca, ô và file. Không có khóa root×fault×repeat trùng.

| Bộ | Ca | Root | Ô có ca | Metric/log/trace | Byte file trong ca |
|---|---:|---:|---:|---|---:|
| RE1-SS | 125 | 5 | 25 | 125/0/0 | 15.432.409 |
| RE2-SS | 90 | 5 | 30 | 90/90/0 | 101.086.392 |
| RE3-SS | 30 | 3 | 9 | 30/30/0 | 32.726.388 |

RE1 và RE2 có các root carts/catalogue/orders/payment/user. RE1 lặp 5 mỗi ô; RE2 lặp 3 mỗi ô. RE3 có carts 12, front-end 9, orders 9 ca; fault F1=10, F2=3, F3=10, F4=7, F5=0; lặp 3–4 theo ô. Số ca khớp README/bài; fault table HF RE3-SS có lỗi nguồn: dòng 41 ghi F1–F5 nhưng prose dòng 52 nói F5 chỉ ở OB. GitHub README dòng 145 và tree chỉ có F1–F4. Giữ hai lời nguồn và số đếm thật.

Không có `traces.parquet` ở **mọi** ca của cả ba SS tại release ghim. HF card nói Sock Shop không traced và bỏ các CSV trace header-only trong bản nguồn. Có file log ở cả 30 RE3-SS, nên câu “13 ca RE3-SS có header-only logs.csv hoặc traces.csv” không cho phép kết luận 13 ca thiếu log: danh từ “hoặc” không xác định modality theo ca. Parent span, graph từ trace và ghép log–trace không áp dụng cho release này. Không gọi đó là thiếu quyền hoặc file trace rỗng đã đo.

## 4. FACT trên tám root_cause.txt và log thật

[label-audit.json](label-audit.json) kiểm đủ 8 nhãn bằng size/git-blob oid tree rồi đọc từng CSV row; đối chiếu service/message/timestamp với toàn log của chính tám ca. Mỗi file chứa **một hàng sáu trường**: thời gian rút gọn, timestamp nanosecond, service, message, pod, host. Bốn hàng carts F1/F3 là WARN “POST không hỗ trợ” và có Spring payload giống trace/span ID; bốn hàng front-end F1/F2 là access log HTTP 500 cho POST `/cart`. Không hàng nào có stack trace hoặc dòng mã nguồn. Đây là chỉ báo triệu chứng do tác giả gắn, không tự chứng minh instruction nào bị sửa.

Chỉ có **7 hash khác nhau**. Hai nhãn front-end F2 lặp 1/2 giống từng byte. Nhãn của lặp 2 nằm ngoài cửa sổ log của chính ca đó và trước injection 10.893 giây; không có service+message tương ứng. Bảy nhãn còn lại khớp đúng một payload; ba timestamp epoch floor khớp, bốn log timestamp lớn hơn floor nhãn 1 giây. Sai khác một giây có thể do quy đổi/làm tròn timestamp hoặc clock; chưa có converter gốc để phân xử. Nó khác lỗi lặp 2 lệch gần ba giờ.

Không sửa nhãn gốc, không tự đổi thành nhãn hàng lỗi khác. Ca lặp 2 vẫn có nhãn root/fault trong tên và injection riêng; lỗi **nhãn chỉ báo** không tự chứng minh telemetry hoặc nhãn service gốc sai. Hai payload giống nhau trong các ca khác cũng không chứng minh cả ca trùng, vì thông báo HTTP phổ biến và fault khác có thể cùng triệu chứng. Source chỉ báo lỗi này cần được phân biệt khi chấm fine-grained diagnosis (định vị chỉ báo chi tiết); không dùng 8 file làm 8 nhãn code-line độc lập.

## 5. Kiến trúc công bố và vị trí root

Repo ứng dụng chính thức và repo tài liệu đã ghim độc lập trong manifest. [Design](https://github.com/microservices-demo/microservices-demo/blob/9dff06fae4981921caec6a62393a6ebfce4b3e3f/internal-docs/design.md) dẫn [hình kiến trúc](https://github.com/microservices-demo/microservices-demo.github.io/blob/1ae9f90384364b961fe6bfb6c796ddba328c6ad8/assets/Architecture.png). Đã tải/view/kiểm git-blob hình. Hình nối Front-end tới Order/Payment/User/Catalogue/Cart bằng đường không có mũi tên. Phần Order→Shipping→Queue→Queue-Master có mũi tên. Không suy hướng năm nhánh đầu từ cách bố trí hình.

[architecture-edges.csv](architecture-edges.csv) lưu tám nét liên hệ rõ trong hình và việc có/không có mũi tên. [architecture-root-positions.csv](architecture-root-positions.csv) báo bậc không hướng của nét nội bộ: front-end 5; orders 2; carts/catalogue/payment/user đều 1. Bỏ hình external User và các icon DB gắn cạnh node không có nét nối riêng; không thêm cạnh từ suy đoán code. Tên số ít trên hình được ghi raw rồi đối chiếu tên chức năng trong compose, chưa khẳng định deployment RCAEval dùng cùng alias/revision. Không gọi số này là bậc vào/ra runtime, lá/hub theo định nghĩa phương pháp hoặc graph hoàn chỉnh.

**CANDIDATE — chưa kiểm áp dụng vào RCAEval:** nếu kiến trúc/phiên bản workload của release giữ các quan hệ trên, RE3 có một root ở Front-end nhiều nhánh và một ở Order có nhánh tiếp. Giả định sai nếu RCAEval sửa API, deployment hoặc routing. Đầu vào cần là manifest deployment/call-graph thực nghiệm ghim; owner G1/P5. Hình tĩnh cho nguồn đối chiếu và lý do có thể xét kịch bản kiến trúc, không xác nhận tiêu chí 5 runtime. Compose có 15 entry, gồm edge-router/user-sim/database/queue; số service công bố không là số node trace.

## 6. Vấn đề task cũ và nội dung bổ sung

**T-003, `results/T-003/the-dataset-ngoai-rcaeval.md:19`:** câu “Sock Shop thuộc T-002/P2” dẫn tới T-002 dù `results/T-002/the-rcaeval.md:560` nói rõ không viết thẻ SS ngoài SPEC. Bằng chứng phản bác: T-003 đã cảnh báo G1 phải trả lời Sock Shop, và T-002 kiểm schema hai mẫu; đây là vấn đề điều hướng/phạm vi, không sai số census. Kết luận bị ảnh hưởng là mức hoàn tất hồ sơ G1 cho Sock Shop. T-019 đã triển khai census toàn SS/nhãn/source kiến trúc và parent hoàn thiện thẻ. Đề xuất tối thiểu, sau Minh duyệt: đoạn cũ “Sock Shop thuộc T-002/P2; không tự thêm raw vào gói.” → “T-002 chỉ kiểm hai mẫu Sock Shop ngoài bốn thẻ chính; thẻ riêng Sock Shop và census toàn release nằm ở T-019. Gói T-003 không thêm raw Sock Shop.”

**T-002 source table, `results/T-002/public-metadata/run-002/sources/hf-README.md:41`:** lỗi F5 ở RE3-SS là lỗi nguồn đã snapshot, không sửa snapshot cũ. T-002 không có thẻ SS, nên không quy nó thành sai số kết quả của T-002. Đề xuất nếu cập nhật diễn giải `results/T-002/public-sources.md:61`: thêm “Bảng HF cũng ghi F1–F5 cho RE3-SS, nhưng GitHub README/tree chỉ có F1–F4; census chi tiết ở T-019.” Đây là bổ sung phạm vi mới, không phủ nhận đối chiếu TT đúng.

**Nguồn root_cause SS:** lỗi nhãn lặp 2 đã kiểm ở mục 4, chưa có task cũ khẳng định đọc đúng nó. Đề xuất tài liệu chung ghi giới hạn chấm chỉ báo và dẫn `label-audit.json`; không gán lỗi cho người làm T-002 chỉ vì task cũ để OPEN.

Không tìm thấy sai khác đáng kể khác ở các nhận định SS nguồn/phả hệ đã kiểm. Điều này không khẳng định toàn T-000–T-012 đúng. Phương pháp, tập TT/OB ngoài phạm vi và nguồn corpus khác không được tái lập trong nhánh này.

## 7. Phần chưa kiểm

Không có artifact trace SS để kiểm parent/join/degree runtime; release hiện xác nhận vắng file. Không có deployment/injector source ghim cho ca SS để kiểm code-line và nguồn sai khác thời gian; công cụ có thể ở repo chưa dẫn. Không chấm phương pháp hoặc detector theo giới hạn Minh. Không chọn/bỏ dataset hoặc chia dev/test; không thêm DECIDED.
