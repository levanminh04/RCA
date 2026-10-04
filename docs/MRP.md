# Chương trình nghiên cứu RCA (MRP v3)

- Trạng thái: **đã duyệt G0 ngày 02/10/2026 (Q-36)**. Soạn ngày 02/10/2026.
- Thay thế hoàn toàn MRP v1 và MRP-v2. Hai bản cũ chỉ còn giá trị lịch sử; không dùng khung của chúng.
- Người quyết: Minh. Claude và Codex ngang hàng; vai trò người làm và người phản biện gắn theo từng task (Q-13).

## 0. Tóm tắt một đoạn

Phần RCA đi đúng chuỗi cô yêu cầu, không nhảy cóc. Trước hết hiểu sâu kỹ thuật các phương pháp RCA đã có. Sau đó chạy chúng trên nhiều bộ dữ liệu công khai và chỉ ra chúng hỏng ở đâu, vì sao. Từ những chỗ hỏng đó mới thiết kế phương pháp đồ thị theo 5 bước của cô. Cuối cùng đưa phương pháp vào FlashTicket, vừa để demo vừa làm một bộ dữ liệu thực nghiệm có tiêm lỗi. Kết quả báo trung thực, kể cả khi đồ thị không thắng; cô sẽ định hướng tiếp qua các lần báo cáo tiến độ.

## 1. Căn cứ

| Nguồn | Nội dung dùng | File |
|---|---|---|
| Đề tài DT18 | Tên đề tài; NV2: nút là dịch vụ hoặc thành phần, cạnh là gọi hàm, thông điệp, phụ thuộc dữ liệu; log, trace, metrics ánh xạ lên đồ thị để xác định vùng ảnh hưởng, phát hiện bất thường, xếp hạng nguyên nhân gốc; NV3: thực nghiệm trên dữ liệu công khai trước, rồi trên hệ bán vé | `reference/sources/DT18-de-tai-va-nhiem-vu.md` |
| Hướng dẫn của cô | Nhận xét báo cáo, chuỗi 4 việc, 5 bước phương pháp, phần tích hợp sản phẩm | `reference/sources/advisor-2026-09-23.md` |
| Quyết định của Minh ngày 02/10 | Mốc, dataset, tiêu chí thành công, repo, vai trò agent, kho quan sát | `DECISIONS.md` |
| Bài học v1/v2 | Các sai lầm không được lặp lại | `LESSONS.md` (rút gọn), `reference/LESSONS-v1.md` (đầy đủ) |
| Kiến thức nền (đã lọc, chưa kiểm lại) | Phương pháp (K1), dữ liệu RE2-TT và checklist kiểm dataset (K2), dataset ứng viên (K3), ba họ thuật toán (K4) | `knowledge/` |

Bối cảnh hệ thống: FlashTicket có 5 service nghiệp vụ (event, booking, payment, ticket, user), API Gateway, broker, cache, Keycloak, cấu hình và khám phá dịch vụ; payment-service điều phối Saga. Ba bạn dựng hệ thống song song với phần RCA. RCA là đơn vị triển khai riêng, chỉ đọc kho quan sát. Kho quan sát đã duyệt làm baseline nhưng chưa chạy: OTel Java Agent → OTel Collector → Tempo (trace), Loki (log), Prometheus (metric), Grafana để xem. Stack có thể đổi nếu RCA cần.

## 2. Đọc hướng dẫn của cô thành việc cụ thể

### 2.1 Chuỗi bốn việc cô yêu cầu

| Câu của cô | Cách hiểu | Gói việc |
|---|---|---|
| "mới khảo sát sơ qua..., chưa sâu kỹ thuật của từng phương pháp" | Với mỗi phương pháp đã chọn: viết lại cơ chế bằng công thức, đọc code gốc, chạy tay trên một ca, nêu giả định và điều kiện thất bại | P1 |
| "thực nghiệm với 1 dataset → mở rộng ra các dataset public khác" | Chọn thêm dataset theo tiêu chí, chạy cùng các phương pháp trên cùng giao thức | P2, P3 |
| "chỉ ra vấn đề còn tồn đọng, hạn chế" | Hạn chế phải có bằng chứng: ca nào hỏng, phương pháp nào, cơ chế nào gây ra | P4 |
| "tiếp cận phương pháp đồ thị theo 5 bước" | Thiết kế phương pháp đồ thị **xuất phát từ các hạn chế ở P4** | P5–P8 |
| Phần 2: tích hợp vào hệ thống đặt vé | RCA chạy thật trên FlashTicket; demo tập trung vào phát hiện và chẩn đoán sự cố | P9, P10 |

**Vì sao giữ đúng thứ tự này** (WHY-01): cô phê bản trước "chưa thể hiện rõ liên kết logic". Liên kết logic ở đây là: hiểu cơ chế → thấy cơ chế hỏng ở đâu trên dữ liệu → mỗi thành phần của phương pháp đồ thị trả lời một chỗ hỏng cụ thể. v1 và v2 thiết kế phương pháp trước rồi mới tìm chỗ nó có ích (LESSONS SL1, SL22). Làm ngược lại thì không có câu trả lời cho "tại sao phương pháp có thành phần này".

### 2.2 Năm bước phương pháp

| Bước của cô | Gói | Đầu ra |
|---|---|---|
| 1. Mô hình đồ thị phụ thuộc giữa các dịch vụ | P5 | Đặc tả đồ thị có kiểu nút, kiểu cạnh; bộ dựng đồ thị từ trace và từ kiến trúc |
| 2. Graph-based anomaly detection, ánh xạ log/trace lên đồ thị; ví dụ PageRank anomaly, subgraph anomaly detection, GNN-based | P6 | Phương pháp phát hiện, khoanh vùng, xếp hạng chạy trên đồ thị |
| 3. Thử nghiệm trên dataset công khai | P7 (dùng dataset của P2) | Kết quả trên tập test và dataset giữ ngoài |
| 4. So với RCA cơ sở; Precision, Recall, F1, MRR, NDCG | P7 (dùng baseline của P3) | Bảng so sánh có khoảng tin cậy, tách theo điều kiện |
| 5. LLM diễn giải nguyên nhân và gợi ý xử lý | P8 | Lớp giải thích và đánh giá của nó |

### 2.3 Cách hiểu "graph-based anomaly detection" (WHY-02)

Minh quyết không hỏi cô lúc này, tự chọn cách hiểu tốt nhất rồi báo cáo. Cụm từ này có hai nghĩa:

- **Nghĩa hẹp:** đồ thị tham gia trực tiếp vào việc tính điểm bất thường.
- **Nghĩa rộng:** cả chuỗi phát hiện → khoanh vùng → xếp hạng chạy trên đồ thị, dù bước phát hiện có thể cục bộ.

K1 §D.3 ghi một phản ví dụ quan trọng: MicroRCA và MicroRank chỉ dùng PageRank **sau khi** đã phát hiện bất thường cục bộ, nên đồ thị không tham gia việc phát hiện. Nếu chỉ làm theo nghĩa rộng, cô hỏi "đồ thị phát hiện bất thường ở đâu?" sẽ không trả lời được.

**Chọn:** thiết kế thỏa cả hai nghĩa. Đồ thị tham gia vào điểm bất thường (tầng 2 ở P6). Cả chuỗi khoanh vùng và xếp hạng cũng chạy trên đồ thị (tầng 3, 4). Khung bốn tầng là ứng viên để tổ chức thiết kế, không phải yêu cầu của DT18; thành phần cụ thể chọn sau P4 (WHY-02). Ba ví dụ của cô được đặt vào đúng tầng mà tài liệu dùng chúng:

| Ví dụ của cô | Tầng | Lý do |
|---|---|---|
| Subgraph anomaly detection | Tầng 3: đồ thị con bất thường → vùng nghi ngờ | DT18 yêu cầu "xác định vùng ảnh hưởng". Các phần tử bất thường liên thông chỉ là vùng triệu chứng quan sát được, chưa chắc là vùng ảnh hưởng thật: thành phần gốc không có cạnh hoặc không có tín hiệu có thể nằm ngoài; hai bất thường độc lập có thể nằm liền nhau. Vì vậy gọi là "vùng nghi ngờ" cho tới khi có nhãn vùng để kiểm. Chỉ gọi bước này là subgraph anomaly detection khi có định nghĩa điểm bất thường và quy tắc quyết định cho đồ thị con |
| PageRank anomaly | Tầng 4: xếp hạng nguyên nhân | Trong MicroRCA và MicroRank, PageRank là thuật toán xếp hạng, không phải bộ phát hiện bất thường (K1 §E). MicroRCA chạy PageRank cá nhân hóa trên đồ thị con bất thường. MicroRank chạy PageRank trên đồ thị của trace bình thường và của trace bất thường, dùng kết quả làm trọng số cho spectrum analysis (phân tích phổ: so mức xuất hiện của từng thành phần trong trace bình thường và bất thường), rồi mới tính điểm nghi ngờ (K1 §C.3). Chỉ gọi là "PageRank anomaly" khi có điểm lệch so với PageRank lúc bình thường và ngưỡng rõ. Chọn biến thể sau P1 và P4 |
| GNN-based anomaly detection | Một biến thể của tầng 2 | Chỉ làm nếu thỏa tiêu chí ở WHY-10; nếu không, báo cáo nêu lý do bằng bằng chứng |

Ba thuật toán là ví dụ, không phải danh sách bắt buộc phải cài hết (Q-24). Mỗi thuật toán được làm khi có câu hỏi cần nó trả lời.

## 3. Câu hỏi nghiên cứu

Không câu nào giả định đồ thị sẽ thắng (Minh quyết 02/10: báo kết quả trung thực).

- **RQ1 — Phương pháp đã có.** Các phương pháp phát hiện bất thường và các phương pháp RCA tiêu biểu hoạt động theo cơ chế nào, và kết quả của chúng thay đổi thế nào giữa các dataset, loại lỗi và vị trí của service gốc trong đồ thị? → P1, P2, P3.
- **RQ2 — Hạn chế.** Các phương pháp đó (cả phát hiện lẫn RCA) thất bại ở những ca nào và vì cơ chế nào? → P4.
- **RQ3 — Phương pháp đồ thị.** Một phương pháp ánh xạ log, trace, metric lên đồ thị phụ thuộc để phát hiện, khoanh vùng và xếp hạng có khắc phục được các hạn chế ở RQ2 không, khi so với baseline mạnh nhất trên dữ liệu không dùng lúc thiết kế? → P5, P6, P7.
  - RQ3a: phát hiện sự cố (Precision, Recall, F1).
  - RQ3b: xếp hạng nguyên nhân gốc (MRR, NDCG, Hit@k).
  - RQ3c: vùng ảnh hưởng (Precision, Recall, F1), ở nơi có nhãn.
  - RQ3d: phần thay đổi có đến từ cấu trúc đồ thị thật không, hay đồ thị bất kỳ cũng cho kết quả tương tự? (đối chứng ở §6)
- **RQ4 — Giải thích.** LLM nhận bằng chứng có cấu trúc đồ thị có cho giải thích đúng, trung thành với bằng chứng và gợi ý xử lý dùng được hơn khi chỉ nhận bằng chứng dạng danh sách không? → P8.
- **RQ5 — Áp dụng trên FlashTicket.** Kết quả có giữ được trên một hệ khác các hệ trong dataset, với lỗi tự tiêm và tải thay đổi không? → P10.
  - Câu phụ (đề xuất **chưa kiểm**, chờ dữ liệu FlashTicket): flash sale làm tải tăng đột biến từ cổng vào; sự cố thường bắt đầu ở một thành phần rồi lan ngược lên phía gọi. Nếu giả định này đúng, hướng lan trên đồ thị có thể giúp phân biệt "tải tăng" với "sự cố". Giả định sai khi tải làm cạn tài nguyên ở một service (lúc đó tải gây ra sự cố thật). Dataset công khai thường giữ tải đều nên không kiểm được câu này; chỉ FlashTicket kiểm được.

Phát hiện bất thường không phải phần phụ của RCA: nó có hồ sơ phương pháp, baseline, độ đo và phân tích hạn chế riêng ở mọi gói (Q-30).

**Hoàn thành nghĩa là gì:** mỗi RQ có câu trả lời dựa trên phép thử hợp lệ, kèm điều kiện nó đúng và không đúng, và lý do (cơ chế) của kết quả, dù tốt hay xấu (Q-35). "Đồ thị không giúp ở X, vì Y" là một câu trả lời hợp lệ.

## 4. Dataset: chọn theo tiêu chí, không theo tên

Minh quyết 02/10: ba tên cô nêu (Train Ticket, Sock Shop, LEMMA-RCA) là ví dụ. Chọn theo tiêu chí dưới đây, kiểm trên file thật trước khi dùng (P2). Báo cáo phải trả lời được "vì sao dùng hoặc không dùng Sock Shop và LEMMA-RCA", vì cô đã nêu tên.

**Tiêu chí bắt buộc**

1. Công khai, tải được, giấy phép cho phép dùng.
2. Mỗi ca có nhãn thành phần gốc và thời điểm lỗi. Thẻ dataset ghi rõ thời điểm đó là lúc tiêm lỗi hay lúc bắt đầu biểu hiện (onset) quan sát được, vì hai mốc này cho các độ đo phát hiện khác nhau (P7).
3. Có trace với liên kết span cha–con. Lý do: bước 2 của cô là ánh xạ log/trace lên đồ thị. Bộ không có trace chỉ được dùng có chủ đích, làm kịch bản "đồ thị dựng từ kiến trúc, không từ trace", và phải nói rõ.
4. Có metric; có log càng tốt.

**Tiêu chí "phân xử được"** (LESSONS QT16; v1 hỏng vì bỏ qua bước này)

5. Nhiều service gốc khác nhau, nằm ở nhiều vị trí khác nhau trong đồ thị (lá, giữa, hub). RE2-TT chỉ có 5 service gốc và đồ thị gần như không đổi giữa các ca (LESSONS ST3), nên một mình nó không phân xử được "đồ thị giúp khi nào".
6. Có cả lỗi tài nguyên, lỗi mạng và lỗi mã nguồn. Lỗi mã nguồn quan trọng vì có thể không hiện ở metric mà hiện ở log và trace.
7. Có ca mà triệu chứng lan sang service khác service gốc. Nếu triệu chứng chỉ nằm ở service gốc thì bài toán không cần đồ thị.
8. Đủ dữ liệu bình thường để học ngưỡng.
9. Ít nhất một bộ độc lập: khác nhóm tác giả, khác công cụ tiêm lỗi, khác stack thu thập.

**Ứng viên cần kiểm ở P2:** RCAEval RE2 (Train Ticket, Online Boutique, Sock Shop) và RE3 (lỗi mã nguồn); Nezha (Online Boutique, Train Ticket); Eadro (Train Ticket, SocialNetwork); DeepTraLog (Train Ticket, có nhãn bất thường theo từng trace); LEMMA-RCA; cộng một lượt tìm có giới hạn các dataset công bố 2025–2026. Dữ kiện đã có: `knowledge/K3-dataset-ung-vien.md` (thông tin từ README và bài báo, **chưa kiểm trên file**). Theo khảo sát cũ, RE2-SS không có trace và LEMMA-RCA v4 không mô tả trace; P2 phải xác nhận lại.

**Chống thiên vị RCAEval khi chọn dataset** (Q-31)

- Dữ liệu RCAEval có sẵn trong `data/` chỉ vì tận dụng lần tải trước (Q-21). "Đã có sẵn" không được tính là lý do chọn.
- Việc P1 dùng code baseline của RCAEval cũng không phải lý do chọn dataset của RCAEval.
- Mọi ứng viên được chấm theo cùng bảng tiêu chí ở trên, điền đủ cho từng ứng viên rồi mới so. Chi phí tải và viết adapter chỉ ghi ở một cột riêng, không gộp vào điểm phân xử.
- Nếu chọn một bộ RCAEval, P2 phải chỉ ra nó hơn các ứng viên khác ở tiêu chí nào.
- Tiêu chí 9 (bộ độc lập) vẫn áp dụng như trên.

**Chia dữ liệu** (WHY-04)

- Mỗi dataset chia dev/test **theo ô** (thành phần gốc × loại lỗi), để các lần lặp của cùng một ô không nằm ở hai phía.
- Giữ ít nhất **một dataset hoàn toàn ngoài thiết kế** (dataset giữ ngoài). Trước G3, với bộ này chỉ được đọc metadata, schema và đếm nhãn; không xem dữ liệu đo, không chạy phương pháp trên từng ca. Vì vậy tiêu chí 7 (triệu chứng lan) của bộ này để OPEN đến G3, và thẻ dataset của nó ghi rõ phần nào chưa kiểm.
- Cách chia chốt ở G1, trước khi chạy bất kỳ phương pháp nào trên dữ liệu mới.
- Cách chia ở G1 ghi rõ cách dùng nhãn: nhãn nào để học (phương pháp có giám sát), nhãn dev nào để chọn cấu hình hay checkpoint, nhãn nào chỉ để chấm. Nhãn test chỉ để chấm. Phương pháp có giám sát học theo tập service của từng hệ nên không chuyển sang hệ khác được; G1 ghi rõ baseline nào chạy được trên dataset giữ ngoài với đúng đầu vào và ngân sách nhãn. Các phương pháp không cùng điều kiện bài toán (ví dụ có giám sát và không giám sát) không xếp chung một bảng mà không ghi rõ.
- 60 ca RE2-TT chưa mở của v1 có thể dùng làm test nếu P2 chọn RE2-TT. "Chưa mở" ở đây nghĩa là chưa ai xem kết quả phương pháp trên từng ca; v1 đã đọc schema và độ phủ trace của cả 90 ca (K2 §1). Các ca này có cùng 5 service gốc với 30 ca dev.

## 5. Các gói việc

Mỗi gói được chia thành các task trong `tasks/`, mỗi task có `SPEC.md` được duyệt trước khi làm (cách làm ở `AGENTS.md` mục 5). Phần dưới chỉ nêu mục tiêu, đầu ra và lý do.

### P0 — Nền (gói hiện tại)

Repo mới, MRP, quy trình agent, nhật ký quyết định. Xong khi Minh duyệt G0.

### P1 — Hồ sơ kỹ thuật các phương pháp phát hiện bất thường và RCA đã có

- **Chọn phương pháp** theo ba tiêu chí: phủ đủ các họ (thống kê trên metric, nhân quả, dựa trên trace, lan truyền trên đồ thị, đa nguồn, học có đồ thị); có code chạy được; được các bài gần đây dùng làm baseline. Ước lượng 8–12 phương pháp RCA.
- **Có hồ sơ riêng cho các bộ phát hiện bất thường** (Q-30), không chỉ cho phương pháp RCA: các bộ phát hiện trên chuỗi thời gian (ví dụ BOCPD trong BARO, N-Sigma, SPOT) và các bộ phát hiện dùng đồ thị (ví dụ DeepTraLog, GDN). Danh sách chốt cùng lúc với danh sách RCA.
- **Danh sách cụ thể chốt sau khi đọc code RCAEval bản mới nhất** (HEAD `259ea41`, kiểm ngày 02/10/2026). Ứng viên từ K1: BARO, N-Sigma, RCD, CIRCA, MicroRank, TraceRCA, MicroRCA, PDiagnose, Eadro, TORAI; và SimpleRCA của bài FSE 2026 (arXiv 2510.04711, báo top-1 0,80 trên RE2-TT, **chưa đối chiếu bản in**). Chưa kiểm phương pháp nào trong số này có sẵn trong RCAEval.
- **Mỗi phương pháp một hồ sơ cùng mẫu:**
  - bài toán và đầu vào;
  - từng bước xử lý, công thức chấm điểm viết lại bằng ký hiệu;
  - đồ thị dùng ở đâu, theo các vai trò ở K1 §3;
  - tham số mặc định, có file và dòng code;
  - chỗ code khác bài báo;
  - giả định và điều kiện thất bại do tác giả nêu;
  - một ví dụ chạy tay trên một ca, giải thích vì sao ra thứ hạng đó.
- **Đọc thêm hai bài đánh giá gần nhất:** FSE 2026 (SimpleRCA) và "Where Root Cause Analysis Fails: A Retrieval-Reranking Decomposition" (RCAEval ghi là NeurIPS 2026 Evaluations and Datasets).
- **Xong khi:** đủ hồ sơ, mỗi phương pháp chạy được một ca, Minh đọc hiểu được cơ chế mà không cần đọc code.
- **Vì sao:** đây là nhận xét đầu tiên của cô. Không hiểu cơ chế thì P4 chỉ nói được "phương pháp X sai", không nói được "vì sao".

### P2 — Kiểm và chọn dataset

- Với mỗi ứng viên ở §4: tải mẫu, đọc schema thật, viết **thẻ dataset**. Thẻ gồm: số ca; số service gốc và vị trí của chúng trong đồ thị; loại lỗi; ba nguồn tín hiệu có hay không và chất lượng (tỷ lệ span cha resolve được, log có trace_id không); độ dài dữ liệu bình thường; nhãn có những gì; giấy phép; kích thước. Với ứng viên dự kiến làm dataset giữ ngoài, chỉ làm phần §4 cho phép (metadata, schema, đếm nhãn).
- Đếm các con số "phân xử được" (§4, tiêu chí 5–8) trước khi đặt bất kỳ giả thuyết nào. Với tiêu chí 7 (triệu chứng lan) chỉ ước lượng thô, thử vài ngưỡng lấy từ dữ liệu bình thường; không gắn nhãn "lan" chính thức cho từng ca ở bước này.
- Kiểm rò nhãn: thư mục ca của RCAEval chứa tên service gốc (ví dụ `re2tt_ts-auth-service_cpu_1`). Phương pháp chỉ được nhận dữ liệu đo, không nhận tên ca hay đường dẫn. Kiểm cả runner, không chỉ phương pháp: `main.py` của RCAEval lấy service gốc từ tên thư mục ca, chọn SLI (chỉ báo chất lượng dịch vụ) của chính service đó rồi truyền cho phương pháp; CloudRanger, EasyRCA, MicroCause dùng SLI này khi xếp hạng. Adapter của nhóm chọn SLI từ cấu hình hoặc báo động quan sát được, độc lập với nhãn. Nếu một baseline cần biết trước vị trí triệu chứng thì ghi rõ đầu vào đó và nguồn hợp lệ. Kiểm cả bộ cột: ở RE2-TT, tập cột metric khác nhau giữa các ca và tương quan với service gốc (T-018); phương pháp học xuyên ca phải dùng bộ cột cố định chốt từ dữ liệu học.
- **Đầu ra:** bảng "task nào chấm được trên bộ nào" (phân biệt nhãn theo khoảng tiêm lỗi với nhãn bất thường quan sát được), đề xuất danh sách dataset và cách chia → Minh duyệt ở G1.
- **Vì sao:** v1 chọn một bộ rồi mới phát hiện nó không phân xử được câu hỏi (LESSONS SL15).

### P3 — Chạy baseline trên nhiều dataset

- Chạy các phương pháp của P1 trên **phần dev** của các dataset đã chọn. Phần test chỉ chạy ở P7, cùng lúc với phương pháp đồ thị.
- Cùng một giao thức cho mọi phương pháp: cùng cửa sổ dữ liệu, cùng tập ứng viên, cùng code tính độ đo. Code nào chọn mô hình bằng tập test thì đổi sang chọn trên dev; ví dụ Eadro (`codes/base.py`, hàm `fit`) giữ checkpoint có HR@1 cao nhất trên tập test. Giữ nguyên phần khoa học của tác giả, ghi phần đổi giao thức vào WHY (§6 mục 4).
- Hai chế độ:
  - (a) biết trước thời điểm sự cố, như bài gốc của phần lớn baseline;
  - (b) tự phát hiện, với các phương pháp có bộ phát hiện.
- **Chấm riêng phần phát hiện** (Q-30): các bộ phát hiện ở P1 được chấm bằng Precision, Recall, F1 theo cửa sổ thời gian, kèm số báo động sai trên mỗi giờ bình thường và độ trễ phát hiện (mốc tính như ở P7). Kết quả phát hiện báo thành bảng riêng, không gộp vào bảng xếp hạng.
- **Kiểm tái lập:** trên ít nhất một dataset, so với số các tác giả đã công bố. Lệch lớn thì dừng tìm nguyên nhân, không ghi "giới hạn" rồi đi tiếp (QT5). Bản RCAEval tháng 9/2026 chưa sửa hẳn lỗi PageRank và CIRCA trả về thứ tự cột, chỉ in thêm cảnh báo: khi phương pháp lỗi, wrapper `rca` (`RCAEval/e2e/__init__.py`) vẫn trả danh sách cột trong `ranks`, và `main.py` lưu nó như kết quả thường. Adapter của nhóm phải ghi ca lỗi là lỗi, không chấm thứ tự cột như dự đoán thật, không âm thầm bỏ ca lỗi khỏi mẫu đánh giá, và giữ lượt hỏng (§6 mục 10).
- Lưu kết quả từng ca.
- **Vì sao:** đây là việc "mở rộng thực nghiệm" cô yêu cầu. Bảng này cũng chính là phần baseline của bước 4, làm một lần dùng hai nơi.

### P4 — Phân tích hạn chế

- Chỉ dùng phần dev. Với mỗi ca mà một phương pháp xếp sai, mở dữ liệu đo ra xem vì sao, rồi xếp vào nhóm cơ chế.
- Làm tương tự cho phần phát hiện (Q-30): ca nào bộ phát hiện bỏ sót, báo động sai, hoặc báo trễ, và vì sao.
- **Giả thuyết cần kiểm** (chưa kiểm, có thể sai):
  - nhầm triệu chứng với nguyên nhân: độ trễ lan lên service gọi, nên service gọi bị xếp trên service gốc;
  - lỗi không hiện ở loại tín hiệu mà phương pháp dùng, ví dụ lỗi mã nguồn với phương pháp chỉ dùng metric;
  - service gốc không có tín hiệu, hoặc không có cạnh trong trace;
  - phải biết trước thời điểm sự cố;
  - không cho ra vùng ảnh hưởng hay lời giải thích.
- Mỗi hạn chế ghi: bao nhiêu ca trên tổng số, ở phương pháp nào, dataset nào, bằng chứng cơ chế, và tác giả có tự nêu không.
- Tách theo ô và theo ca trước khi nêu mẫu hình (QT15). Một ô không phải là mẫu hình.
- Nếu cơ chế "nhầm triệu chứng lan với nguyên nhân" chiếm phần đáng kể các ca sai, định nghĩa nhãn "lan" cho từng ca trên dev: ngưỡng lấy từ dữ liệu bình thường, báo độ nhạy theo vài ngưỡng, tránh định nghĩa vòng lặp kiểu "service lệch nhất không phải gốc". Định nghĩa khóa ở G3, trước khi mở test. Nhãn chỉ dùng để chấm và phân tích, không đưa vào phương pháp. Nếu cơ chế này không đáng kể thì không tách.
- **Đầu ra:** bản đồ hạn chế. Mỗi lựa chọn thiết kế ở P5–P6 phải trỏ về một dòng trong bản đồ này.
- **Vì sao:** đây là việc "chỉ ra vấn đề tồn đọng" của cô, và là cầu nối logic sang phương pháp đồ thị.

### P5 — Bước 1: Mô hình đồ thị phụ thuộc

- **Nút:** service; thêm thành phần hệ thống (database, cache, broker, gateway) ở nơi dữ liệu cho thấy chúng.
- **Cạnh có kiểu** đúng như DT18:
  - gọi đồng bộ: span CLIENT → SERVER;
  - trao đổi thông điệp: PRODUCER → CONSUMER;
  - phụ thuộc dữ liệu: service → database hoặc cache, từ span có thuộc tính database;
  - triển khai (service → máy) nếu dữ liệu có.
- **Nguồn dựng:**
  - quan sát được từ trace;
  - tĩnh, từ kiến trúc và cấu hình (cho bộ không có trace, và cho FlashTicket nơi biết kiến trúc).
  - So hai nguồn để đo độ phủ.
- **Theo thời gian:** đồ thị nền từ giai đoạn bình thường, và ảnh chụp theo từng cửa sổ. Ghi độ phủ: số cạnh thấy được, span mồ côi.
- **Đầu ra:** đặc tả hình thức của đồ thị, bộ dựng đồ thị dùng chung cho mọi dataset, thống kê đồ thị của từng dataset.
- **Vì sao không chỉ dựng đồ thị gọi giữa các service:** DT18 nêu rõ ba loại cạnh. Nhiều sự cố của hệ bán vé nằm ở database, broker, cache, và các thành phần này không phải service.

### P6 — Bước 2: Phát hiện bất thường trên đồ thị

Khung bốn tầng, lấy từ câu chữ của DT18 ("ánh xạ lên đồ thị để xác định vùng ảnh hưởng, phát hiện dấu hiệu bất thường và xếp hạng"). Khung này là ứng viên; DT18 yêu cầu các đầu ra, không bắt buộc kiến trúc này. Lựa chọn cụ thể trong mỗi tầng chốt trong spec P6, **sau P4**, trên phần dev.

1. **Ánh xạ.** Theo từng cửa sổ thời gian, gắn tín hiệu lên phần tử của đồ thị.
   - Cạnh: số lời gọi, độ trễ đo từ phía gọi, số lỗi.
   - Nút:
     - thời gian tự xử lý: độ trễ của span trừ phần nằm trong span con;
     - log lỗi và mẫu log: gắn vào span qua trace_id nếu có, nếu không thì theo service và thời gian;
     - metric tài nguyên.
2. **Chấm điểm bất thường có dùng đồ thị.** So từng phần tử với mức bình thường của chính nó. Cơ chế ứng viên (**chưa kiểm**): dùng đồ thị để tách bất thường **tự sinh** (từ chính thành phần) khỏi bất thường **kế thừa** (do thành phần phía dưới truyền lên). Ứng viên này nhắm vào giả thuyết "nhầm triệu chứng với nguyên nhân" của P4; chỉ giữ nếu P4 xác nhận hạn chế đó trên dev. Phát hiện bất thường có dùng đồ thị là bắt buộc (bước 2 của cô, DT18); P4 chỉ quyết định dùng cơ chế nào.
   - Các cách ứng viên:
     - quy tắc phân rã theo cây lời gọi;
     - hồi quy có điều kiện trên nút cha/con, giống CIRCA;
     - GNN dự báo hành vi bình thường, giống GDN.
   - Phát hiện ở mức hệ thống: báo sự cố khi điểm vượt ngưỡng học từ dữ liệu bình thường.
   - Quy tắc phân rã theo cây lời gọi sai khi:
     - lời gọi bất đồng bộ hoặc song song (trừ con làm sai thời gian tự xử lý);
     - thiếu span con;
     - lỗi tài nguyên không làm tăng độ trễ;
     - lỗi mã nguồn trả lỗi nhanh.
3. **Đồ thị con bất thường (vùng nghi ngờ).** Các phần tử bất thường liên thông với nhau tạo thành vùng nghi ngờ. Đây là vùng triệu chứng quan sát được, chưa chắc là vùng ảnh hưởng thật; chỉ gọi là vùng ảnh hưởng ở nơi có nhãn vùng để kiểm (P7). Chỉ gọi bước này là "subgraph anomaly detection" khi spec P6 có định nghĩa điểm bất thường và quy tắc quyết định cho đồ thị con.
4. **Xếp hạng nguyên nhân gốc.** Không loại ứng viên chỉ vì nó chưa vượt ngưỡng: thành phần gốc có thể không có cạnh hoặc không có tín hiệu (giả thuyết thứ ba của P4). Tập ứng viên chốt trong spec P6.
   - Các cách ứng viên:
     - PageRank cá nhân hóa, khởi đầu từ điểm bất thường tự sinh (kiểu MicroRCA);
     - PageRank trên đồ thị của trace bình thường và của trace bất thường, làm trọng số cho spectrum analysis, rồi tính điểm nghi ngờ (kiểu MicroRank). Nếu chỉ so hai PageRank thì là biến thể riêng, phải ghi khác biệt với MicroRank;
     - quy tắc "thành phần bất thường tự sinh nằm sâu nhất theo chiều gọi". Quy tắc này chưa định nghĩa chặt và đã bị phản biện (v2, chưa kiểm).
   - Chọn trên dev theo MRR của chính tầng này, không theo mức chênh so với nhánh không đồ thị (QT4).

**Đầu ra:** spec phương pháp. Mỗi lựa chọn ghi: hạn chế nào ở P4 nó nhắm tới, vì sao chọn, đã xét phương án nào, bằng chứng trên dev.

### P7 — Bước 3 và 4: Thực nghiệm và so sánh

- **Khóa trước** (cổng G3): cấu hình phương pháp, giả thuyết, bảng diễn giải kết quả, cách tính độ đo, danh sách so sánh. Khóa bằng commit. Sau đó mới chạy một lần trên phần test và dataset giữ ngoài.
- **So với:**
  - các baseline của P3;
  - nhánh **cùng bằng chứng nhưng không dùng đồ thị**. Spec P7 ghi rõ cấu trúc nào được coi là đồ thị (quan hệ cha–con trong trace, đồ thị service), thông tin nào giữ chung, bước nào bị loại. Ví dụ self-time và hồi quy theo nút cha đã dùng quan hệ; nếu nhánh này giữ chúng mà chỉ bỏ bước xếp hạng trên đồ thị thì kết quả chỉ nói về bước xếp hạng (WHY-07);
  - nhánh **đồ thị ngẫu nhiên giữ bậc**;
  - nhánh đồ thị tĩnh so với đồ thị quan sát.
- **Độ đo** (WHY-06):
  - Phát hiện: Precision, Recall, F1 theo cửa sổ thời gian; số báo động sai trên mỗi giờ bình thường; độ trễ phát hiện. Ghi rõ mốc của độ trễ: nếu dataset chỉ có thời điểm tiêm thì gọi là độ trễ tính từ lúc tiêm, không gọi là độ trễ từ lúc sự cố bắt đầu biểu hiện. Kết luận RQ3a giới hạn theo loại nhãn thời gian thật sự có.
  - Xếp hạng: MRR, NDCG@5, Hit@1/3/5. Báo thêm AC@k và Avg@5 để so được với số đã công bố của RCAEval.
  - Vùng ảnh hưởng: Precision, Recall, F1, chỉ ở nơi có nhãn thật (FlashTicket). Trên dataset công khai không có nhãn vùng thì chỉ báo "vùng có chứa thành phần gốc không" và kích thước vùng, gọi đúng tên là "vùng nghi ngờ".
- **Báo cáo:**
  - theo dataset, loại lỗi, vị trí thành phần gốc;
  - theo nhóm ca "lan" và "không lan", nếu P4 đã định nghĩa nhãn này;
  - khoảng tin cậy bootstrap lấy mẫu theo ô;
  - so từng cặp theo ca: bao nhiêu ca thắng, hòa, thua.

### P8 — Bước 5: LLM diễn giải và gợi ý xử lý

- **Đầu vào là gói bằng chứng có cấu trúc:** đồ thị con bất thường, danh sách xếp hạng kèm điểm, tín hiệu lệch nhất, vài dòng log tiêu biểu, đường lan truyền.
- **Đầu ra:** giải thích, các bước xử lý gợi ý, mức tự tin; được phép trả lời "không đủ bằng chứng".
- LLM **không** đổi thứ hạng. Model chọn ở P8; không bắt buộc là Gemini (Q-18). Gemini là một ứng viên, vì tài liệu nền tảng đã ghi nó cho lớp giải thích (`D:/Project/flash-ticket-platform/docs/architecture/aws-runtime-baseline.md` dòng 57).
- **Đánh giá:**
  - đúng: có nêu đúng thành phần gốc và loại lỗi theo nhãn không;
  - trung thành: mỗi khẳng định có truy về gói bằng chứng không (kiểm tự động);
  - hữu ích: thang chấm do người chấm;
  - so gói có đồ thị với gói dạng danh sách.

### P9 — Kho quan sát và tích hợp (chạy song song với P1–P8)

- **P9a, làm sớm:** viết "Yêu cầu quan sát cho RCA" để gửi nhóm hệ thống, vì hệ thống đang được dựng ngay bây giờ. Các yêu cầu dự kiến:
  - span có kind và thuộc tính chuẩn OTel cho HTTP, database, messaging, để dựng được cạnh có kiểu;
  - log có trace_id và span_id;
  - lấy mẫu trace 100% trong lúc chạy thực nghiệm;
  - `service.name` thống nhất trên cả ba tín hiệu;
  - metric tài nguyên theo service và máy;
  - đồng hồ các máy được đồng bộ;
  - thời gian lưu đủ dài để có dữ liệu bình thường.
  - Đối chiếu với chuẩn B16 đã duyệt (`D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md`).
- **P9b:** dịch vụ RCA đọc Tempo, Loki, Prometheus qua API của chúng, đổi sang **cùng định dạng nội bộ** mà các bộ chuyển đổi dataset dùng. Nhờ vậy cùng một lõi RCA chạy trên dataset công khai và trên FlashTicket (WHY-08).

### P10 — Thực nghiệm trên FlashTicket và demo

- **Tiêm lỗi:**
  - tài nguyên;
  - mạng;
  - lỗi mã nguồn, có thể bằng công cụ tiêm lỗi vào bean Spring;
  - lỗi phụ thuộc: database, Redis, RabbitMQ;
  - lỗi Saga: phát hành vé thất bại dẫn tới bù trừ.
- **Tải:** có kịch bản flash sale.
- **Người dựng bộ tạo tải và bộ tiêm lỗi:** Minh (Q-19).
- FlashTicket chạy trên EC2, không phải Kubernetes, nên công cụ tiêm lỗi chọn theo dạng triển khai này.
- **Nhãn:**
  - thành phần gốc biết sẵn, vì nhóm tự tiêm lỗi;
  - nhãn vùng ảnh hưởng cần giao thức riêng, chốt trước khi chạy. Nhãn phải lấy từ tín hiệu mà bộ chẩn đoán không dùng, nếu không Precision và Recall chỉ đo phương pháp khớp với chính nó (LESSONS SL18).
- **Demo:** báo sự cố → đồ thị con bất thường → danh sách nguyên nhân → giải thích của LLM. Minh tích hợp, Tuyến làm giao diện; phần phát hiện bất thường được demo ngang với phần RCA (Q-28).

## 6. Nguyên tắc thực nghiệm

1. **Dev để thiết kế, test để kiểm.** Test và dataset giữ ngoài chỉ mở một lần, sau G3, khi Minh cho phép.
2. **Baseline phải mạnh** trước khi nói đồ thị giúp, gồm cả baseline đơn giản đã công bố (QT7).
3. **Mỗi khẳng định về đồ thị cần đủ ba thứ** (QT8):
   - hơn nhánh cùng bằng chứng mà không dùng đồ thị;
   - hơn đồ thị ngẫu nhiên giữ bậc;
   - báo theo điều kiện và theo từng ca, không chỉ trung bình.
   - Vì sao cần đồ thị ngẫu nhiên (WHY-07): nếu đồ thị bất kỳ cũng cho kết quả như vậy thì lợi ích không đến từ quan hệ phụ thuộc thật.
4. **Prior work là mặc định.** Lấy đúng quy ước của bài hoặc code gốc, ghi file và dòng. Muốn lệch thì ghi lý do vào WHY (QT2).
5. **Kiểm chịu lực.** Mỗi lựa chọn riêng của nhóm được thay trong khoảng hợp lý trên dev. Nếu kết luận đổi dấu thì báo kèm độ nhạy (QT3).
6. **Soi giá trị trung gian** trước khi so sánh. Điểm cực lớn, toàn hòa, hay một nhóm kênh chiếm gần hết thì dừng tìm nguyên nhân (QT5).
7. **Kết quả quá đẹp cũng phải nghi.** Chạy phép thử giả: hai cửa sổ đều bình thường thì phương pháp không được "tìm ra" nguyên nhân.
8. **Không đưa nhãn vào phương pháp:** tên ca, đường dẫn, file nhãn, thời điểm tiêm lỗi ở chế độ tự phát hiện, và mọi đầu vào suy ra từ chúng (ví dụ chọn SLI theo service gốc, P2).
9. **Số trong tài liệu lấy từ file kết quả**, ghi đường dẫn (QT17). Đề xuất chưa kiểm ghi rõ là "chưa kiểm", kèm giả định và trường hợp nó sai.
10. **Giữ mọi lượt chạy**, kể cả lượt hỏng.

## 7. Cổng

Ở mỗi cổng, agent trả lời sáu câu, Minh quyết:

1. Phục vụ câu nào của cô hoặc DT18?
2. Dữ liệu có phân xử nổi câu hỏi không?
3. Baseline đủ mạnh chưa?
4. Giá trị trung gian có hợp lý không?
5. Kết luận đã tách theo điều kiện và theo ca chưa?
6. Còn lựa chọn nào chưa có câu trả lời "tại sao" không?

| Cổng | Sau gói | Minh duyệt gì | Phản biện chéo bắt buộc |
|---|---|---|---|
| G0 | P0 | MRP này | Có |
| G1 | P1, P2 | Danh sách phương pháp, dataset, cách chia dev/test | Có |
| G2 | P3, P4 | Bảng baseline trên dev, bản đồ hạn chế | Không bắt buộc |
| G3 | P5, P6 | Thiết kế khóa, giả thuyết, bảng diễn giải; cho phép mở test | Có |
| G4 | P7 | Kết quả và phân tích; báo cáo tiến độ cho cô | Có |
| G5 | P8 | Lớp giải thích | Không bắt buộc |
| G6 | P10 | Kết quả FlashTicket và demo | Có |

**Mốc:** Minh muốn có kết quả phương pháp đồ thị (tới G4) sớm nhất có thể, trước 20/10/2026. Hướng đi đúng được ưu tiên hơn tốc độ. Quyển đồ án nộp 30/12/2026 (Q-23).

## 8. Khung báo cáo tiến độ cho cô

Báo cáo đi theo đúng chuỗi của cô, mỗi phần mở bằng câu "phần này trả lời nhận xét nào":

1. Các phương pháp RCA đã có: cơ chế kỹ thuật (P1).
2. Thực nghiệm trên nhiều dataset: chọn dataset nào, vì sao; kết quả (P2, P3).
3. Hạn chế của các phương pháp đã có, kèm bằng chứng (P4).
4. Phương pháp đồ thị: mỗi thành phần trả lời hạn chế nào (P5, P6).
5. Kết quả so sánh (P7) và giải thích bằng LLM (P8).
6. Hướng tích hợp FlashTicket (P9, P10).
7. Câu hỏi xin cô định hướng.

## 9. Rủi ro

| Rủi ro | Dấu hiệu | Cách xử lý |
|---|---|---|
| Dataset không phân xử nổi | Ít service gốc, đồ thị không đổi, triệu chứng chỉ ở service gốc | Đếm ở P2, trước khi đặt giả thuyết; thêm bộ độc lập |
| Code baseline sai lặng lẽ | Thứ hạng bằng thứ tự cột; số lệch xa số công bố | Adapter ghi ca lỗi là lỗi (P3); kiểm tái lập ở P3 |
| Rò nhãn | Kết quả quá đẹp; tên ca lọt vào phương pháp | §6 mục 7, 8 |
| Thiết kế theo test | Nhìn kết quả test rồi sửa | Khóa ở G3; test mở một lần |
| FlashTicket chưa chạy được khi tới P10 | Kho quan sát chưa triển khai | Giao P9a sớm; P1–P8 không phụ thuộc FlashTicket |
| Phiên agent bị ngắt | Hết usage giữa chừng | LOG của task và quy trình đổi agent (`AGENTS.md` mục 7, 8) |
| Quy trình phình to | Viết thêm luật thay vì trả lời câu hỏi khoa học | LESSONS CB1, CB2 |

## 10. Câu hỏi còn mở (không chặn G0)

1. Model LLM cụ thể và khóa API cho thực nghiệm: quyết ở P8.

## 11. Thứ được kế thừa và thứ bỏ

- **Tham khảo, không neo:**
  - K1: bản đồ phương pháp. P1 phải kiểm lại các khẳng định quan trọng trên bài và code gốc.
  - K2: dữ liệu RE2-TT và checklist kiểm dataset.
  - K3: dữ kiện về các dataset ứng viên.
  - K4: dữ kiện về ba họ thuật toán cô nêu.
  - LESSONS: các sự thật đã đo và các bài học.
- **Dữ liệu đã mang về (02/10/2026):** 90 ca RE2-TT và 5 ca mẫu RCAEval từ lần tải trước, đã kiểm khớp hash của Hugging Face rồi chép vào `data/`; 60 ca chưa ai nhìn được để trong `data/locked/`. Chi tiết ở `data/README.md`. Mang về không có nghĩa là đã chọn RE2-TT; việc chọn dataset vẫn là của P2, duyệt ở G1.
- **Bỏ:**
  - code v1;
  - khung MRP-v2 (điểm cục bộ → lan truyền PageRank → so L/O/R);
  - các tham số của TD-v1.3, ví dụ sàn 1e-12;
  - các cổng và mã quyết định của v1/v2.
