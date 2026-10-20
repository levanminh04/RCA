# Đề xuất hướng P6: chẩn đoán sự cố trên đồ thị phụ thuộc, dùng stack Grafana làm hạ tầng

- **Ngày soạn:** 20/10/2026. **Người soạn:** Claude, theo yêu cầu của Minh trong chat ngày 19–20/10/2026.
- **Trạng thái:** ĐỀ XUẤT. **Chưa được duyệt.** Tài liệu này không thay MRP, PLAN-P6, DECISIONS hay WHY. Mọi thay đổi kế hoạch chỉ có hiệu lực khi Minh duyệt và ghi vào DECISIONS.
- **Phản biện:** Codex đã phản biện ba lượt (ở chat) các bản đề xuất từ lượt 1 tới lượt 4. Các nội dung thêm sau lượt 4 chưa qua phản biện, gồm: RCA Workbench, Investigations đã GA, Coroot, kiến trúc chi tiết, giao diện và kịch bản vận hành.
- **Chưa làm gì để kiểm bằng chạy thật.** Mọi phần đánh dấu [ĐO] phải được kiểm ở lượt chạy thử (mục 14) trước khi trình như điều đã biết.
- **Bản sửa 1 (20/10/2026):** áp gói sửa theo phản biện của Codex (F01–F17) và tự soát của Claude (N1–N4), Minh duyệt trong chat ngày 20/10/2026. Thêm mục 18 (lộ trình và quan hệ với PLAN-P6). Danh sách chỗ sửa ở mục 16.
- **Bản sửa 2 (20/10/2026):** áp gói sửa nhỏ theo lượt kiểm lại của Codex (F07 còn lại, F18, F19, F14), Minh duyệt trong chat ngày 20/10/2026. Chi tiết ở mục 16.

## 0. Cách đọc nhãn

Mỗi khẳng định kỹ thuật mang một nhãn:

| Nhãn | Nghĩa | Ai đối chứng được bằng cách nào |
|---|---|---|
| **[TL]** | Tài liệu chính thức (hoặc mã nguồn chính thức) ghi như vậy | Mở đường dẫn ở mục 17, đọc đúng đoạn được dẫn |
| **[TÍNH]** | Tự tính từ con số trong tài liệu, kèm giả định | Làm lại phép tính; thay giả định bằng số thật |
| **[ĐX]** | Đề xuất thiết kế của nhóm. **Không phải** tính năng có sẵn của nền tảng | Đánh giá lập luận; nền tảng không hứa điều này |
| **[ĐO]** | Tài liệu không có thông tin. Chỉ biết khi chạy thử | Chạy thử theo mục 14 |
| **[REPO]** | Lấy từ file trong repo này hoặc repo FlashTicket | Mở file và dòng được ghi |

Nếu một khẳng định không có nhãn, coi đó là lời giải thích khái niệm chung, không phải dữ kiện để làm căn cứ.

---

## 1. Thuật ngữ và mã dùng trong tài liệu

### 1.1. Thuật ngữ quan sát hệ thống

| Thuật ngữ | Nghĩa dễ hiểu |
|---|---|
| **Request** | Một yêu cầu người dùng gửi vào hệ thống, ví dụ "đặt 2 vé". |
| **Trace** | Toàn bộ hành trình của **một** request qua các service. |
| **Span** | Một đoạn trong hành trình: một lần xử lý route, một truy vấn DB, một lần gửi thông điệp. Trace gồm nhiều span lồng nhau theo quan hệ cha–con. |
| **Kind** (loại span) | Vai trò của span. `SERVER`: đang nhận và xử lý request. `CLIENT`: đang gọi ra ngoài và chờ trả lời. `PRODUCER`/`CONSUMER`: gửi/nhận thông điệp qua hàng đợi. `INTERNAL`: việc nội bộ. |
| **Thao tác** (operation) | Tên của span, ví dụ `POST /orders/{orderId}/cancel` (B13) hay một truy vấn SQL. Nhiều request cùng một thao tác. |
| **Metric** | Chuỗi số theo thời gian, ví dụ số request mỗi giây. |
| **Log** | Dòng chữ ứng dụng ghi ra, ví dụ thông báo lỗi. |
| **RED** | Ba số chuẩn của một thao tác: **R**ate (số request/giây), **E**rrors (số lỗi), **D**uration (phân bố thời gian xử lý). |
| **OTel (OpenTelemetry)** | Chuẩn mở để thu trace, metric, log. |
| **OTLP** | Định dạng và giao thức chuẩn của OTel để gửi dữ liệu quan sát. |
| **Collector** | Chương trình OTel nhận, xử lý và chuyển tiếp dữ liệu quan sát. |
| **Lấy mẫu** (sampling) | Chỉ giữ lại một phần trace để tiết kiệm chỗ. **Tail sampling**: Collector chờ một khoảng thời gian (mặc định 30 giây) rồi mới quyết định giữ hay bỏ cả trace, nên có thể ưu tiên giữ trace lỗi và trace chậm. Span đến muộn hơn khoảng chờ có thể bị xử lý như một trace mới, nên không bảo đảm giữ trọn mọi trace lỗi (mục 4.5). |
| **Cửa sổ** | Khoảng thời gian dữ liệu được gộp lại để phân tích hoặc vẽ. |
| **Root** | Thành phần gây ra sự cố. **RCA** (root cause analysis): tìm root. |
| **Vùng nghi ngờ** | Tập thành phần có khả năng liên quan đến sự cố, dùng để trình bày cho người xem. |

### 1.2. Mã trong repo

| Mã | Ở đâu | Nghĩa |
|---|---|---|
| **DT18** | `docs/reference/sources/DT18-de-tai-va-nhiem-vu.md` | Tên và nhiệm vụ chính thức của đề tài. NV1: xây hệ bán vé và kiểm thử tải. NV2: mô hình đồ thị (nút là service hoặc thành phần; cạnh là gọi hàm, thông điệp, phụ thuộc dữ liệu); ánh xạ log, trace, metric lên đồ thị để xác định vùng ảnh hưởng, phát hiện bất thường, xếp hạng nguyên nhân. NV3: thực nghiệm trên dữ liệu công khai trước, rồi trên hệ bán vé. |
| **Thư 22/08 của cô** | `docs/reference/sources/advisor-2026-08-22-lich-su.md`; toàn bộ chuỗi thư về định hướng và tên đề tài: `docs/reference/sources/advisor-thu-dang-ky-de-tai.md` (lưu ngày 20/10/2026) | Mục tiêu 3: *"Đề xuất cơ chế lan truyền và xếp hạng nguyên nhân gốc dựa trên bằng chứng log/trace"*. |
| **5 bước của cô** | `docs/reference/sources/advisor-2026-09-23.md` | Bước 1 dựng đồ thị; bước 2 graph-based anomaly detection; bước 3 dataset công khai; bước 4 so với baseline; bước 5 LLM giải thích. |
| **Chế độ (a)** | MRP, G2 | Phương pháp RCA được cho biết trước mốc tiêm lỗi. Chỉ có trong thực nghiệm. |
| **Chế độ (b)** | MRP, G2 | Bộ phát hiện tự báo động; RCA chạy tại báo động. Đây là chế độ thật khi vận hành. |
| **G2** | `results/T-034/goi-g2.md` | Gói tổng hợp baseline và bản đồ hạn chế (26 dòng G2-H01 đến G2-H26). |
| **G2-H06** | `goi-g2.md` §3.2 | Lỗi trễ mạng: dấu hiệu nằm ở **span phía gọi** của lời gọi tới root. |
| **G2-H07** | `goi-g2.md` §3.2 | Lỗi trả về ở Nezha-OB: root không đứng hạng 1 dù có dấu hiệu. |
| **G2-H11** | `goi-g2.md` §3.2 | Thực thể bị xếp trên root phần lớn nằm ngoài chuỗi gọi qua root. |
| **G2-H13** | `goi-g2.md` §3.2 | CIRCA: kết quả nhạy với cửa sổ. |
| **G2-H16** | `goi-g2.md` §3.2 | Rào cản tập ứng viên, hòa ở biên cắt, ca dừng lỗi vì thao tác thiếu nền. |
| **G2-H19** | `goi-g2.md` §3.2 | Giới hạn của dữ liệu trace và metric (gồm root không được ai gọi). |
| **G2-H21, G2-H22** | `goi-g2.md` §3.2 | BOCPD và N-Sigma báo động trước mốc tiêm lỗi. |
| **UV-1** | `goi-g2.md` §5 | Ứng viên: *"Gắn thời gian lời gọi lên cạnh, tính cho dịch vụ được gọi."* Căn cứ: root đứng đầu theo span phía gọi ở 19/20 ca RE2-TT và 13/20 ca Nezha-OB, nhưng theo span của chính dịch vụ chỉ 8/26 ca RE2-TT. |
| **UV-6** | `goi-g2.md` §5 | Ứng viên: *"Dùng tín hiệu giảm và log tại root cho lỗi trả về sớm."* Căn cứ: ở 4 ca lỗi trả về, log lỗi tại root tăng ở cả 4 ca, tỷ lệ thành công ở frontend giảm. |
| **WHY-02** | `docs/WHY.md` | Hai nghĩa của "graph-based anomaly detection". Nghĩa hẹp: đồ thị tham gia trực tiếp vào việc tính điểm bất thường. Nghĩa rộng: cả chuỗi phát hiện, khoanh vùng, xếp hạng chạy trên đồ thị, dù bước phát hiện có thể cục bộ. MRP đang chọn thỏa cả hai. |
| **WHY-26** | `docs/WHY.md` | Bốn tập khi xếp hạng: inventory (mọi thành phần đã biết), tập quan sát (thành phần phương pháp thấy được), tập chấm, tập trả về. *"Phương pháp không có bằng chứng cho một thực thể thì không xếp nó; không điền phần thiếu."* |
| **P5** | T-035 đến T-040 | Mô hình đồ thị phụ thuộc: bộ dựng từ trace (`src/do_thi`), hợp đồng nguồn tĩnh (`src/do_thi_tinh`), mô hình FlashTicket theo thiết kế (T-037), bàn giao P6 (`results/T-040/ban-giao-p6.md`). |

### 1.3. Các yêu cầu thiết kế R1–R4 (rút từ chương 4 của báo cáo và G2)

| Mã | Hạn chế đã quan sát | Yêu cầu cho phương pháp mới |
|---|---|---|
| **R1** (giả thuyết) | Lỗi trễ mạng: dấu hiệu nằm ở **span phía gọi** của lời gọi tới root (G2-H06, đo trực tiếp vị trí ở mức ĐC). G2 ghi rõ: *"Chưa phân xử vì sao mỗi phương pháp xếp sai ở từng ca: mới là quan sát đặt cạnh thứ hạng"* (`ban-do-g2.json#/rows/5/vi_sao`). Vậy **chưa xác nhận** việc các phương pháp xếp sai là do gán bằng chứng cho bên gọi. | **Giả thuyết cần kiểm:** phân bổ bằng chứng theo quan hệ gọi có giúp xếp hạng tốt hơn cách gán cho service sở hữu span không. |
| **R2** | Lỗi trả về sớm: độ trễ không tăng; log lỗi tăng và tỷ lệ thành công giảm. SimpleRCA chỉ xét chiều tăng; BARO loại cột hằng ở đoạn nền (G2-H07, UV-6). | Dùng cả **log** và **tín hiệu giảm**, không chỉ tín hiệu tăng. |
| **R3** | Root bị loại sớm vì không có tín hiệu cục bộ, hoặc không được ai gọi (G2-H16, G2-H19). | Không loại ứng viên chỉ vì chưa vượt ngưỡng cục bộ. Không điền điểm mặc định cho thành phần thiếu bằng chứng (WHY-26). |
| **R4a** | Chế độ (b) trên RE2-TT: báo động đầu đúng hoặc sau mốc tiêm chỉ ở 3/30 ca (BOCPD) và 0/30 ca (N-Sigma); thành công toàn chuỗi cao nhất 0,067 (`goi-g2.md` §0). | Đánh giá RCA **tại cảnh báo thật**; đo chất lượng và mốc của bộ cảnh báo; không tin tuyệt đối vào thời điểm báo. |
| **R4b** (giả thuyết, chưa có căn cứ cơ chế) | G2 ghi *"Chưa phân xử vì sao có báo động trước mốc"* (`ban-do-g2.json#/rows/20/vi_sao`, G2-H21) và chưa phân xử nguyên nhân thống kê của N-Sigma (`#/rows/21/vi_sao`, G2-H22). | Tín hiệu ở các thành phần có thể lệch thời gian với nhau. Đây chỉ là giả thuyết để kiểm; **không được dùng báo động trước mốc làm bằng chứng** cho độ trễ lan truyền. |

---

## 2. Vì sao đề xuất đổi hướng

### 2.1. Những gì repo đã biết [REPO]

- Trên RE2-TT ở chế độ (a), SimpleRCA (không dùng quan hệ gọi) đạt Hit@1 0,833; TORAI B đạt 0,867, nhưng bước nhân quả của TORAI không quyết định hạng của root (G2-H15). Chưa có căn cứ nói đồ thị giúp, cũng chưa có căn cứ nói không giúp (`goi-g2.md` §0).
- Nezha-OB ở chế độ (a): mọi phương pháp chạy được đều yếu, tốt nhất BARO 0,364. Với lỗi trả về, BARO, SimpleRCA, TraceRCA đều đúng 0/4 ca.
- Chế độ (b) là điểm yếu lớn nhất (R4a).

### 2.2. Những gì công cụ công nghiệp đã làm được

**Grafana (bản tự cài, mã nguồn mở):**
- Thu thập, lưu trữ, truy vấn trace (Tempo), metric (Prometheus), log (Loki); vẽ biểu đồ; cảnh báo theo luật do người viết. [TL]
- **Service Graph** ở mức service, dựng từ trace, có cả cạnh tới DB. [TL]
- Các tài liệu đã đọc **không mô tả** cơ chế tự tìm root cho bản tự cài. Đây là "không thấy trong tài liệu đã đọc", không phải tài liệu khẳng định là không có.

**Grafana Cloud:**
- **Knowledge Graph và RCA Workbench:** sinh insight bằng luật có sẵn trên metric; khi có cảnh báo, đi ra các thực thể lân cận tới bậc 4 trên đồ thị thực thể (service, pod, node, DB…) để gom insight; xếp các insight lên một dòng thời gian cho **người xem tự kết luận**. Tài liệu không mô tả bước tự động xuất danh sách root đã xếp hạng, và không công bố độ chính xác. [TL]
- **Assistant Investigations:** agent LLM (model Claude) tự điều tra sự cố; **GA từ 29/07/2026**. [TL]
- Đánh giá do Grafana tự công bố: sự cố 1, có Knowledge Graph đúng 15/16 lần, không có đúng 1/16; sự cố 2, đúng 8/16 và 7/16 lần. Chính Grafana ghi sự cố 1 được chọn vì "hợp với Knowledge Graph", và tính nhất quán giữa các lần chạy chưa được giải quyết. [TL]

**Coroot:**
- Mã nguồn mở (Apache 2.0), tự cài được. [TL]
- RCA: *đi theo đồ thị phụ thuộc từ service bị ảnh hưởng, dùng các thuật toán ML, không dùng LLM*; LLM chỉ giải thích ở bước sau. [TL]
- RCA chỉ có ở bản Enterprise (từ 1 USD mỗi CPU core mỗi tháng), hoặc bản Community nối với Coroot Cloud, được 10 lượt điều tra miễn phí mỗi tháng. [TL]
- Nhà phát triển tự công bố tìm được root cho hơn 80% sự cố. Chưa có kiểm chứng độc lập. [TL: đây là lời tự công bố]

**Nghiên cứu đã có về "phụ thuộc cộng thứ tự thời gian":**
- PAL và FChain xếp thành phần theo thời điểm bắt đầu bất thường. [TL, theo bài tổng quan arXiv 2105.12378; chưa đọc bài gốc]
- Groot (eBay, ASE 2021): đồ thị sự kiện dựa trên luật; 952 sự cố thật; đúng 95% ở top-3, 78% ở top-1. [TL]
- LagRCA (FSE 2026, Alibaba): mô hình độ trễ lan truyền; 88,3% ở top-5, hơn baseline tốt nhất 21,8 điểm. [TL]
- BARO: lấy bất thường đầu tiên làm thời điểm sự cố, và ghi rõ bất thường đầu tiên **không** phải root. [TL]
- MicroRCA: đồ thị có thuộc tính cộng personalized PageRank trên đồ thị con bất thường. [TL]

### 2.3. Kết luận thẳng

- Việc đã có sản phẩm công nghiệp **không** làm mất đóng góp của đồ án. DT18-NV3 yêu cầu sản phẩm gồm *"cơ chế hỗ trợ chẩn đoán sự cố và giao diện minh họa kết quả phân tích"*; DT18 không đặt điều kiện cơ chế đó phải chưa từng tồn tại. [REPO]
- Điều **không được** tuyên bố: tính mới học thuật của "lan truyền trên đồ thị dịch vụ" (đã có MicroRCA, Groot), hay "tốt hơn" các công cụ trên khi chưa đo.
- Đóng góp được tách thành ba phần, **nói đúng mức**:
  1. **Xây dựng và tích hợp:** cơ chế hỗ trợ chẩn đoán và giao diện minh họa chạy trên FlashTicket, dùng stack công nghiệp làm hạ tầng; mô hình bằng chứng ở mức thao tác đúng DT18-NV2 và mục tiêu 2 của cô (nút và cạnh mức thao tác; ánh xạ log, trace, metric lên nút và cạnh có địa chỉ bằng chứng; phân biệt cạnh tĩnh và cạnh quan sát). Đồ thị có sẵn của Grafana ở mức service và gắn tín hiệu theo thực thể. [TL]
  2. **Điều chỉnh phương pháp có căn cứ:** các giả thuyết R1, R2, R3, R4b rút từ phân tích lỗi, kèm đối chứng cho thấy mỗi điều chỉnh sửa được ca nào, làm hỏng ca nào. Hiệu quả chưa kiểm.
  3. **Bằng chứng thực nghiệm:** đánh giá trên dữ liệu có đáp án cho câu hỏi "quan hệ phụ thuộc cộng thứ tự thời gian chỉ đúng root khi nào". Grafana và Coroot chưa công bố số đo kiểu này. Lượt tìm nhanh chưa thấy nghiên cứu nào đo đúng cách suy luận kiểu Workbench trên RCAEval hay Nezha; chỉ được nói "chưa thấy", không được nói "chưa có".
- Điểm yếu phải nói trước: tính mới học thuật thấp; có thể thua Investigations hoặc Coroot; bước 2 của cô (đồ thị tham gia trực tiếp vào phát hiện) chỉ được đáp ứng một phần.

---

## 3. Ranh giới: công cụ làm gì, nhóm làm gì

| Phần | Ai làm | Nhóm làm gì |
|---|---|---|
| Trace tự động (HTTP, DB, Redis, RabbitMQ) | OTel Java agent | Cấu hình |
| **Phần ứng dụng phải tự bổ sung** | — | Theo B16 §3: giữ `correlationId`, `traceId`, `messageId`, `requestId` qua retry, callback, outbox; thêm span ở ranh giới nghiệp vụ mà instrumentation tự động không biết (B16 dòng 26). Việc này của nhóm hệ thống và **không làm được chỉ bằng cấu hình** |
| Metric ứng dụng, log | Actuator/Micrometer → Prometheus; log JSON → receiver của Collector → Loki (đường B16 đã chọn, B16 dòng 24) | Cấu hình. Đổi đường xuất phải được nhóm hệ thống đồng ý |
| Thu, chuyển tiếp, lọc dữ liệu | OTel Collector | Cấu hình các ống (mục 4) |
| Lưu trace, metric, log | Tempo, Prometheus, Loki | Cấu hình, đặt thời hạn lưu |
| **Mở sự cố** | Luật cảnh báo của Grafana hoặc Prometheus | **Chọn luật, chọn ngưỡng, đo chất lượng** |
| Gửi thông báo theo nhóm nhãn | Notification policy của Grafana | Cấu hình. Grafana gộp **thông báo** theo nhãn, có nhắc lại theo `repeat_interval`, có thông báo khi nhóm thay đổi; **không** bảo đảm một sự cố chỉ gửi một lần [TL] |
| **Định nghĩa "một đợt sự cố", chống xử lý trùng** | — | **Nhóm tự làm** trong dịch vụ RCA (mục 6.1) |
| **Đồ thị mức thao tác, ánh xạ tín hiệu** | — | **P5 (đã có), thêm adapter OTLP** |
| **Lan truyền, xếp hạng** | — | **Phần nghiên cứu** |
| Giao diện | Grafana: Node graph, Infinity, data link, annotation, panel trace và log | Thiết kế dashboard; cấp dữ liệu cho Node graph |
| Tiêm lỗi, sinh tải | Toxiproxy, Envoy, Pumba, k6 | Viết kịch bản |
| Giải thích | LLM | Prompt dựa trên kết quả RCA (bước 5, làm sau) |

---

## 4. Luồng dữ liệu từ ứng dụng tới kho lưu trữ

### 4.1. Sơ đồ

```
FlashTicket
 ├─ OTel Java agent ── trace (OTLP) ──────────────► OTel Collector
 ├─ Actuator/Micrometer ── metric ứng dụng, JVM ──► Prometheus          (đường B16)
 └─ log JSON ── receiver của Collector ──────────► Loki                (đường B16)

OTel Collector — mỗi ống trace nhận MỘT BẢN SAO các span Collector thực nhận
 ├─ Ống "đếm"      : span ─► spanmetrics  ─► RED theo thao tác   ─► Prometheus
 │                         └► servicegraph ─► cạnh mức service    ─► Prometheus
 ├─ Ống "giữ trace": span ─► tail sampling ─┬─► Tempo           (cho người xem)
 │                                           └─► file OTLP JSON  (cho dịch vụ RCA đọc)
 └─ Ống "container": docker_stats ─► Prometheus
```

Mỗi tín hiệu chỉ có **một đường xuất**, đúng quy tắc B16 dòng 24 (*"Chỉ một đường xuất cho mỗi tín hiệu để tránh đếm trùng"*) [REPO]. spanmetrics là metric suy ra từ trace, khác với metric ứng dụng của Micrometer. Agent không được bật song song đường xuất metric và log khác với B16; nếu muốn đổi sang log qua OTLP thì phải đề xuất đổi B16 với nhóm hệ thống. [ĐX]

### 4.2. Ứng dụng: OTel Java agent

- Thư viện FlashTicket dùng đều có instrumentation tự động: Spring Web MVC 3.1+, Spring WebFlux 5.3+, Spring Cloud Gateway 2.0+, JDBC, MongoDB driver 3.1+, Lettuce 4.0+, Jedis 2.0+, RabbitMQ client 2.7+, Spring RabbitMQ 1.0+, HikariCP 3.0+, Logback 1.0+. [TL]
- Span SERVER của Spring MVC được đặt tên theo route (`http.route`), ví dụ `POST /orders/{orderId}/cancel`, không theo URL thô. [TL] Câu lệnh DB mặc định được che giá trị thành `?`. [TL] Vì vậy số thao tác bị giới hạn bởi số route và loại truy vấn, không phải số request.
- Mặc định của agent: xuất trace, metric, log đều qua OTLP; xuất metric mỗi 60.000 ms; sampler `parentbased_always_on`. [TL]
- **Nghĩa của `parentbased_always_on`:** span gốc (không có cha) dùng AlwaysOn, tức được lấy mẫu. Span có cha ở xa đã lấy mẫu thì mặc định AlwaysOn; cha ở xa **không** lấy mẫu thì mặc định **AlwaysOff**. [TL] Vậy chỉ giữ được mọi trace **khi không có bên nào phía trước gửi ngữ cảnh "không lấy mẫu"** vào FlashTicket. Phải kiểm điều kiện này ở cổng vào. [ĐO]
- Theo B16, metric ứng dụng và JVM đi qua Actuator/Micrometer, log đi dạng JSON qua receiver của Collector [REPO]. Vì vậy đường xuất metric và log mặc định của agent phải tắt hoặc không dùng, để tránh hai đường. [ĐX]
- Log: agent tự đưa `trace_id`, `span_id`, `trace_flags` vào MDC của Logback; in ra bằng `logging.pattern.level = trace_id=%mdc{trace_id} span_id=%mdc{span_id} trace_flags=%mdc{trace_flags} %5p`. [TL] Như vậy log JSON theo đường B16 vẫn mang được trace_id để nối với span. Việc trace_id có thật sự lên Loki và tìm được theo span hay không phải kiểm. [ĐO]
- Instrumentation runtime-telemetry của agent có metric JVM qua JMX (Java 8+) và JFR (Java 17+) [TL]. Nếu B16 đã lấy metric JVM qua Micrometer thì không dùng thêm đường này.
- **Phần ứng dụng phải tự bổ sung** (theo B16 §3): correlation qua retry, callback, outbox; span ở ranh giới nghiệp vụ. Không có phần này thì trace HTTP vẫn đầy đủ nhưng chuỗi xử lý có thể đứt ở outbox, retry, callback. [REPO]
- RabbitMQ: tùy chọn "receive telemetry" là thử nghiệm, mặc định tắt. Ở các instrumentation messaging khác (JMS, Pulsar), khi bật thì consumer bắt đầu trace mới, chỉ nối với producer bằng span link. [TL] FlashTicket rơi vào trường hợp nào thì phải xem trên dữ liệu thật. [ĐO]
- P5 dựng được cạnh thông điệp, nhưng **chỉ nhận link đã xác minh ngữ nghĩa**: link phải trỏ tới span PRODUCER trong miền đang dựng, các trường broker, exchange, routing key, message id phải khớp khi cả hai phía có [REPO: `dac-ta-do-thi.md` §89]. Adapter từ OTLP sang P5 vì vậy **không chỉ đổi định dạng JSON**: nó phải kiểm ngữ nghĩa và phạm vi của link, và ánh xạ đúng địa chỉ hàng đợi (broker, phạm vi, queue). [ĐX]
- Trạng thái lỗi của span HTTP: 5xx thì Error; 4xx thì span **SERVER để trống**, nhưng span **CLIENT đặt Error**; 1xx–3xx để trống. [TL]

### 4.3. Collector: nhân bản, không chia

- *"`otlp` receiver will send the same data to pipeline `traces` and to pipeline `traces/2`"*; *"Each exporter gets a copy of each data element."* [TL] Nghĩa là mỗi ống nhận đủ 100%, độc lập với nhau.
- Tài liệu Tempo và Elastic đều dặn: thành phần sinh metric từ span phải chạy **trước** tail sampling, nếu không metric bị tính trên tập thiếu. [TL]
- "100%" ở đây nghĩa là **mọi span mà Collector thực nhận**. Span bị bỏ ở phía ứng dụng (sampler, mất kết nối, lỗi exporter) thì Collector không thấy.

### 4.4. Ống "đếm"

**spanmetrics** [TL]:
- Sinh metric RED cho mỗi tổ hợp `service.name`, `span.name`, `span.kind`, `status.code` (thêm `collector.instance.id`, có thể bỏ).
- Bucket thời gian mặc định: 2, 4, 6, 8, 10, 50, 100, 200, 400, 800 ms, 1 s, 1,4 s, 2 s, 5 s, 10 s, 15 s. Đơn vị mặc định ms.
- `metrics_flush_interval` mặc định **60 giây**.
- Exemplar (mẫu trace gắn vào metric) **mặc định tắt**; bật thì tối đa 5 mẫu mỗi điểm dữ liệu, giữ trong một chu kỳ xuất.
- `metrics_expiration` mặc định 0, nghĩa là chuỗi metric không bao giờ hết hạn. [TL] Hệ quả cho luật ở mục 5.2.
- **Độ chính xác:** bộ đếm số lời gọi và số lỗi là số đếm trên các span Collector nhận. **Phân vị thời gian** (ví dụ p95) tính từ bucket histogram nên chỉ là **ước lượng**, độ mịn phụ thuộc bucket.

**servicegraph** [TL]:
- Ghép span CLIENT với SERVER, PRODUCER với CONSUMER, và CLIENT có `db.name` thành cạnh tới DB.
- Nhãn `client`, `server`, `connection_type`. Metric: số request, số request lỗi, histogram thời gian đo ở phía server và phía client, số span không ghép được.
- `store.ttl` mặc định **2 giây**, `max_items` 1.000; span chưa ghép được chờ tới khi có bạn ghép hoặc hết thời gian.
- Trạng thái **alpha**.
- **Không có** cạnh giữa các thao tác. Tài liệu không cho biết có đưa được tên span vào làm nhãn hay không.

### 4.5. Ống "giữ trace"

**tail sampling** [TL]:
- `decision_wait` mặc định **30 giây**; `num_traces` mặc định 50.000.
- Policy: `status_code`, `latency`, `probabilistic`, `rate_limiting`, `string_attribute`, `numeric_attribute`, `span_count`, `ottl_condition`, `composite`, `and`, `not`, `drop`… 
- Mọi span của một trace phải tới cùng một instance Collector. Một Collector trên một máy thì tự thỏa.
- **Span đến muộn** [TL]: khi quyết định còn trong bộ đệm, span đến muộn không làm đổi quyết định. Khi quyết định đã bị xóa khỏi bộ đệm và **không** bật decision cache, span đến muộn được coi như một trace mới và được quyết định lại. Có thể bật decision cache (`sampled_cache_size`, `non_sampled_cache_size`) để nhớ quyết định giữ/bỏ. Tài liệu không nói rõ span lỗi đến muộn của một trace đã bị bỏ có được xét lại hay không.

**Chính sách đề xuất** [ĐX]: **ưu tiên** giữ trace có lỗi và trace chậm hơn một ngưỡng; giữ ngẫu nhiên p% số còn lại. Chính sách này **không bảo đảm** giữ trọn mọi trace lỗi, vì span đến muộn và vì lỗi xảy ra sau khi đã quyết định. Mỗi lượt chạy phải ghi lại cấu hình sampling và số span bị bỏ, đúng như B16 dòng 103 yêu cầu [REPO]. Với tải demo nhỏ, giữ 100% (B16 cũng ghi lượt chạy demo hữu hạn dùng 100% trace [REPO]).

**Ước lượng thống kê từ trace đã lấy mẫu** [ĐX]: trace thuộc phần ngẫu nhiên được nhân trọng số 1/p khi đếm. Đây là thiết kế của nhóm, không phải tính năng của nền tảng.

**Kiểm sức chứa** [TÍNH]: 500 trace/s × 30 s = 15.000 trace đang chờ, dưới mức 50.000. Ở 2.000 request/s là 60.000, phải tăng `num_traces`.

**file exporter** (đích "cho RCA đọc") [TL]:
- Ghi OTLP JSON, mỗi dòng một lô. Mặc định định dạng JSON.
- Xoay vòng theo dung lượng: mỗi file tối đa 100 MB, giữ tối đa 100 file (mặc định khi bật rotation); `max_days` mặc định không giới hạn.
- Trạng thái **alpha**. **File không được ép ghi xuống đĩa**, có thể mất dữ liệu khi máy sập. Không có hàng đợi gửi lại.
- Container contrib có hệ thống tệp chỉ đọc; phải gắn volume ghi được.

**Vì sao không kéo hàng loạt trace qua Tempo:** tìm kiếm của Tempo mặc định trả **20 trace** mỗi truy vấn (cấu hình được ở querier), mỗi tập 3 span. [TL] Kéo hàng nghìn trace thì phải gọi lấy từng trace theo ID, rất chậm. Tempo vẫn dùng cho người xem chi tiết. [ĐX]

### 4.6. Kho lưu trữ

| Kho | Thông tin | Nhãn |
|---|---|---|
| Prometheus | `scrape_interval` và `evaluation_interval` mặc định 1 phút; giữ 15 ngày; trung bình 1–2 byte mỗi mẫu; exemplar cần bật cờ `--enable-feature=exemplar-storage`, mỗi exemplar khoảng 100 byte bộ nhớ | [TL] |
| Tempo | API lấy một trace: `GET /api/traces/<id>`, trả JSON OpenTelemetry (bản v1 ghi "mostly compatible"); tìm kiếm bằng TraceQL; giữ 14 ngày (`block_retention` = 336h); chế độ một tiến trình (monolithic) dùng cho dev/test, khuyên dùng khi lưu lượng dưới 25–35 MB/s hoặc 55.000–80.000 span/s; lưu trên đĩa cục bộ chỉ cho dev/test | [TL] |
| Loki | Nhận OTLP trực tiếp tại `/otlp`; mặc định **không tự xóa**; mỗi truy vấn tối đa 5.000 dòng; `service.name` thành nhãn `service_name`; mọi trường ngoài nội dung và thời gian được lưu dạng structured metadata | [TL] |
| Loki: trace_id | Nếu log đi qua OTLP: theo quy tắc trên, trace_id được lưu dạng structured metadata (suy luận từ quy tắc; tài liệu không nêu tên trường). Nếu log đi dạng JSON theo đường B16: trace_id nằm trong nội dung log JSON và phải được trích ra khi truy vấn hoặc khi nhận; cách cụ thể phụ thuộc receiver được chọn | [TL + suy luận]; [ĐO] |

**Bộ cài nhanh:** image `grafana/otel-lgtm` gói Collector, Prometheus, Tempo, Loki, Pyroscope, Grafana trong một container; dành cho phát triển, demo, kiểm thử; không dùng cho production. [TL]

---

## 5. Phát hiện sự cố

### 5.1. Grafana tự cài phát hiện thế nào

Bản tự cài **không tự phát hiện**. Nhóm viết **luật cảnh báo**. Mỗi luật là một câu điều kiện được máy kiểm đều đặn, ví dụ:

> Cứ mỗi 15 giây, đo tỷ lệ request `POST /orders` trả 5xx trong 1 phút gần nhất. Nếu vượt 5% và kéo dài ít nhất 30 giây, thì mở sự cố và gọi bộ chẩn đoán.

**Cấu trúc một luật do Grafana quản lý** [TL]:
1. **Truy vấn** lấy số từ một nguồn hỗ trợ cảnh báo (Prometheus, Loki…).
2. **Biểu thức**: Reduce (rút chuỗi thành một số), Math (tính toán), Resample (căn lại mốc thời gian), SQL, Threshold (so ngưỡng; có ngưỡng hồi phục để giảm chập chờn).
3. **Điều kiện**: một truy vấn hoặc biểu thức quyết định có báo hay không.
4. **Chu kỳ kiểm** (tài liệu lấy ví dụ 10s, 30s, 1m, 10m) và **thời gian chờ** (pending; đặt 0 thì bỏ qua trạng thái chờ).
5. **Một luật, nhiều đối tượng**: mỗi chuỗi số (ví dụ mỗi service, mỗi thao tác) là một cảnh báo riêng.
6. Trạng thái: Normal, Pending, Alerting, Recovering, NoData, Error.

Luật kiểu Prometheus: `for` là thời gian phải đúng liên tục; **không đặt `for` thì luật bật ngay ở lần đánh giá đầu tiên**; `keep_firing_for` giữ trạng thái báo thêm một khoảng sau khi điều kiện hết. Prometheus lưu chuỗi `ALERTS` với giá trị 1 khi cảnh báo ở trạng thái pending hoặc firing. [TL]

### 5.2. Các nhóm luật đề xuất cho FlashTicket [ĐX, dùng hàm có TL]

| Phát hiện | Cách viết | Hàm, căn cứ |
|---|---|---|
| Lỗi tăng | Tỷ lệ lỗi theo thao tác, **chỉ trên span SERVER** (5xx) | `rate()` [TL]; lý do ở mục 13, điểm 2 |
| Chậm | Phân vị 95 theo thao tác | `histogram_quantile()` [TL] |
| Lệch khỏi bình thường | So với trung bình và độ lệch chuẩn gần đây; hoặc so với cùng giờ tuần trước | `avg_over_time()`, `stddev_over_time()`, `offset 1w` [TL] |
| Service dừng hoặc im lặng | **Không** dùng `absent()` trên chuỗi spanmetrics: `absent()` chỉ bật khi không còn chuỗi dữ liệu [TL], mà spanmetrics mặc định không cho chuỗi hết hạn [TL], nên service dừng chưa chắc làm chuỗi biến mất. Dùng một trong: trạng thái scrape của chính service (Prometheus tự sinh chuỗi `up` cho mỗi target: 1 khi target truy cập được, 0 khi scrape thất bại [TL]), heartbeat do ứng dụng phát, hoặc **tốc độ request tụt về 0 trong khi tải đã biết vẫn chạy**. Phải tách lỗi của Collector khỏi lỗi ứng dụng | `rate()` [TL]; heartbeat [ĐX] |
| Sắp cạn tài nguyên | Dự báo tuyến tính | `predict_linear()` [TL] |
| Log lỗi tăng | Đếm dòng lỗi | LogQL `count_over_time`, `rate`, trong luật do Grafana quản lý; tài liệu Loki gợi ý một phép đếm tụt về 0 để bắt service im lặng [TL] |
| Hàng đợi ứ | Độ sâu hàng đợi | `rabbitmq_detailed_queue_messages` từ plugin `rabbitmq_prometheus`, cổng 15692 [TL] |
| Vượt ngân sách lỗi | Burn-rate hai cửa sổ | Trang theo dõi: cửa sổ dài 1 giờ, cửa sổ ngắn 5 phút, hệ số 14,4, tốn 2% ngân sách. Ví dụ 15% lỗi: báo sau khoảng 5 phút, tắt khoảng 5 phút sau khi hết lỗi [TL] |

Tên metric chính xác trong Prometheus phụ thuộc cách đổi tên từ OTLP sang Prometheus; phải xem lại khi dựng. [ĐO]

### 5.3. Các cơ chế khác (chỉ trên Grafana Cloud), để đối chiếu

| Cơ chế | Thời gian | Nhãn |
|---|---|---|
| Insight RequestRateAnomaly, LatencyAverageAnomaly | Nền 26 giờ, độ lệch chuẩn, kéo dài 5 phút | [TL] |
| LatencyAverageBreach | Phân vị 95 của 7 ngày, 5 phút | [TL] |
| LatencyP99ErrorBuildup | Đếm số phút vượt ngưỡng trong cửa sổ 1 giờ; tài liệu không ghi giới hạn | [TL] |
| ErrorRatioBreach | Phân vị 75 của 24 giờ; tài liệu không ghi thời gian | [TL] |
| 9 insight còn lại | Tài liệu không ghi | [TL] |
| Outlier detection (MAD) | So với trung vị trượt 24 giờ; cần ít nhất 3 chuỗi; đánh giá mỗi lần truy vấn | [TL] |
| Forecast | Mặc định học 90 ngày; tự nhận chu kỳ ngày khi có từ 2 ngày, chu kỳ tuần khi có từ 2 tuần; học lại mỗi 24 giờ | [TL] |

**Không phải cơ chế nào cũng chờ 5 phút.** Thời gian chờ ở bản tự cài là tham số do nhóm đặt.

### 5.4. Gom cảnh báo thành sự cố

- Notification policy của Grafana định tuyến cảnh báo theo nhãn và gộp nhiều cảnh báo thành một thông báo. [TL]
- Alertmanager (Prometheus): `group_by` gom theo nhãn; mặc định `group_wait` 30 giây, `group_interval` 5 phút, `repeat_interval` 4 giờ. [TL]
- Thông báo gửi tới dịch vụ RCA qua **webhook**. Payload của Grafana có `status`, `startsAt`, `endsAt`, `values`, `labels`, `annotations`, `generatorURL`, `fingerprint`, và ở mức nhóm có `groupKey`, `groupLabels`, `commonLabels`. [TL]

### 5.5. Độ trễ từ lúc lỗi bắt đầu tới lúc RCA nhận tin

**Minh họa cho một luật cụ thể**, không phải cận trên chung: luật "tỷ lệ 5xx trên span SERVER của một thao tác vượt ngưỡng", dữ liệu đi theo **một** đường: span → spanmetrics → Prometheus → luật → notification → webhook.

| Thành phần trên đường này | Mặc định | Đề xuất chỉnh [ĐX] | Nhãn |
|---|---|---|---|
| spanmetrics xuất metric | 60 s | 15 s | [TL] |
| Prometheus đọc metric từ Collector (nếu theo kiểu scrape) | 60 s | 15 s | [TL] |
| Chu kỳ kiểm luật | 60 s | 15 s | [TL] |
| Thời gian chờ (`for`, pending) | nhóm chọn | ví dụ 30 s | — |
| `group_wait` | 30 s | ví dụ 10 s | [TL] |

**Không cộng các dòng này thành một con số bảo đảm**, vì:
- Cửa sổ `rate[...]` không phải một khoảng chờ cố định: luật bật sớm hay muộn còn tùy lỗi mạnh tới đâu so với ngưỡng.
- `for` chỉ chạy khi điều kiện **tiếp tục đúng** ở mỗi lần kiểm [TL]. Lỗi không vượt ngưỡng thì **có thể không bao giờ báo**.
- Các khoảng có thể chồng lên nhau.

Độ trễ phát hiện và tỷ lệ bỏ sót của **từng luật** phải đo bằng tiêm lỗi. [ĐO] Luật trên metric ứng dụng của Micrometer có đường riêng, khoảng xuất riêng, phải đo riêng.

### 5.6. "Mốc tiêm" khi vận hành

- Khi vận hành **không có mốc tiêm**, chỉ có mốc cảnh báo.
- Khi thực nghiệm, mốc tiêm lấy từ log của công cụ tiêm lỗi (thời điểm gọi API Toxiproxy, lúc lệnh Pumba bắt đầu, lúc bật cờ). Mốc này **chỉ dùng để chấm điểm**: độ trễ phát hiện bằng thời điểm báo trừ thời điểm tiêm. Mốc này không bao giờ được đưa vào phương pháp (luật cứng số 6 trong AGENTS). [REPO]
- **Báo động giả** không đếm đơn giản trong "đoạn không tiêm lỗi". Đoạn không tiêm chưa chắc là hệ khỏe: có thể còn hàng đợi tồn, đang hồi phục, hoặc lỗi do chính tải. PLAN-P6 cũng phân biệt nhãn tiêm lỗi với sức khỏe được xác nhận độc lập [REPO]. Đề xuất [ĐX]:
  - Khai trước **tiêu chí "đoạn bình thường"**: đã qua một khoảng hồi phục sau lần tiêm trước; hàng đợi về mức nền; tỷ lệ lỗi và độ trễ phía người dùng (đo bởi k6) ở mức nền.
  - Chỉ đếm báo động giả trong các đoạn thỏa tiêu chí đó; các đoạn còn lại báo riêng.

### 5.7. Phần "nghiên cứu" của khâu phát hiện [ĐX]

1. Chọn ngưỡng và thời gian chờ từ các **lượt chạy bình thường**, không dùng nhãn lỗi.
2. Đo **độ trễ phát hiện** và **số báo động giả mỗi giờ** trên các lượt tiêm lỗi.
3. Báo rõ loại lỗi nào luật bắt được, loại nào không.
4. Nếu cô yêu cầu đồ thị tham gia trực tiếp vào phát hiện (nghĩa hẹp của WHY-02): ứng viên là điểm bất thường có điều kiện theo các nút lân cận, tức tách bất thường tự sinh khỏi bất thường kế thừa (MRP §P6 tầng 2). Chưa kiểm.

---

## 6. Dịch vụ RCA

### 6.1. Trình tự chạy [ĐX]

1. **Nhận thông báo.** Grafana gửi webhook kèm tên luật, nhãn (service, thao tác), giờ bắt đầu. Một sự cố có thể sinh **nhiều** webhook (nhắc lại, nhóm thay đổi, hồi phục), và một webhook có thể gộp cảnh báo của nhiều nguyên nhân. Vì vậy dịch vụ RCA phải tự làm hai việc [ĐX]:
   - **Định nghĩa "một đợt sự cố"**: ví dụ các cảnh báo bật trong cùng một khoảng thời gian ngắn, chưa có đợt mở nào đang chạy, được gom vào một đợt. Quy tắc cụ thể khai trước, không dựa vào nhãn tiêm lỗi.
   - **Chống xử lý trùng**: mỗi đợt chỉ chạy RCA một lần khi đến mốc chốt dữ liệu; webhook nhắc lại hay cập nhật chỉ ghi vào đợt đã có; webhook hồi phục đóng đợt.
2. **Xác định hai cửa sổ:**
   - Thời điểm bắt đầu pending, tùy loại luật:
     - **Luật Prometheus:** đọc chuỗi `ALERTS`; chuỗi này có giá trị 1 khi cảnh báo ở trạng thái pending **hoặc** firing [TL]. Mốc pending sớm hơn `startsAt`.
     - **Luật do Grafana quản lý:** `ALERTS` **không** chứa các luật này. Phải bật lịch sử trạng thái (`[unified_alerting.state_history]`, chọn `backend` là Loki, Prometheus, hoặc cả hai). Khi ghi vào Prometheus thì dùng metric `GRAFANA_ALERTS` (tên mặc định) qua remote write, Prometheus phải bật `--web.enable-remote-write-receiver` [TL]. Tài liệu nói ghi mọi thay đổi trạng thái của luật, nhưng **không nói riêng** chuỗi `GRAFANA_ALERTS` có trạng thái Pending hay không; phải kiểm [ĐO].
     - Chọn **một** loại luật cho mỗi lượt thực nghiệm, để cách lấy mốc nhất quán. Kịch bản ở mục 11 dùng luật Prometheus.
   - **Cửa sổ sự cố**: từ khoảng 2 phút trước lúc pending, tới **mốc chốt** = lúc báo + Δ (ví dụ Δ = 2 phút).
   - **Cửa sổ nền**: 10–30 phút ngay trước cửa sổ sự cố.
   - Độ dài chọn trên dữ liệu dev; báo cả độ nhạy khi dịch cửa sổ (R4a, G2-H13).
3. **Chờ tới khi dữ liệu của cửa sổ thực sự có:** RCA chỉ chạy sau **mốc chốt + thời gian chờ quyết định của tail sampling (`decision_wait`, mặc định 30 s) + một biên an toàn**. [TÍNH từ TL] Ngay cả vậy cũng **không bảo đảm** đủ trace, vì span đến muộn (mục 4.5). RCA ghi lại độ phủ trace của cửa sổ (số trace, số span không ghép được, số span bị bỏ) cùng kết quả.
   - Hệ quả: **thời gian trả kết quả** = lúc báo + Δ + `decision_wait` + biên + thời gian tính. Toàn bộ khoảng này phải tính vào **độ trễ toàn chuỗi** khi đánh giá.
   - Khi chạy lại offline, chỉ dùng dữ liệu có trước mốc chốt, để không dùng thông tin "tương lai" so với lúc kết quả được công bố.
4. **Lấy dữ liệu** của hai cửa sổ: trace từ file; RED theo thao tác và metric tài nguyên từ Prometheus; số đếm log lỗi từ Loki (LogQL metric), cộng vài dòng log mẫu.
5. **Dựng đồ thị** bằng bộ dựng P5, qua adapter từ OTLP JSON sang định dạng P5.
6. **Gắn tín hiệu** lên nút và cạnh (mục 6.2).
7. **Tính bằng chứng, xếp hạng** (mục 6.3).
8. **Ghi kết quả** (mục 6.4).
9. **Khi chạy offline**, cùng bộ code đọc CSV của RE2-TT hoặc Nezha thay cho file OTLP.

### 6.2. Ánh xạ log, trace, metric lên đồ thị

| Tín hiệu | Lấy từ | Gắn vào | Dùng để |
|---|---|---|---|
| Trace: quan hệ cha–con, kind, thời gian, trạng thái | File OTLP, hoặc Tempo | **Tạo nút thao tác và cạnh gọi.** Trên cạnh: số lời gọi, số lỗi, thời gian phía gọi (span CLIENT) so với phía nhận (span SERVER). Trên nút: phần thời gian không bị span con phủ | R1; dựng đồ thị; chọn trace mẫu |
| RED theo thao tác (spanmetrics) | Prometheus | **Nút thao tác** | Bộ đếm trên mọi span Collector nhận (trước lấy mẫu); phân vị chỉ là ước lượng từ bucket |
| RED theo cạnh service (servicegraph) | Prometheus | **Cạnh mức service** | Đối chiếu |
| Metric ứng dụng và JVM (Actuator/Micrometer, theo B16) | Prometheus | **Nút service** | Phân biệt lỗi tài nguyên với lỗi logic |
| Metric container: CPU, bộ nhớ, mạng, đĩa (receiver `docker_stats`, mỗi 10 giây, alpha, cần quyền vào Docker socket) [TL] | Prometheus | **Nút service** | Như trên |
| Pool kết nối DB (HikariCP) [TL] | Prometheus | **Nút service**, phía DB | Nghẽn kết nối |
| Độ sâu hàng đợi RabbitMQ [TL] | Prometheus | **Nút hàng đợi** | Lỗi kiểu ứ thông điệp |
| Log có trace_id/span_id (log JSON theo đường B16, trace_id lấy từ MDC) | Loki | **Đúng span, tức đúng nút thao tác** | R2 |
| Log không có trace_id | Loki | **Nút service**, theo thời điểm | R2, độ chính xác thấp hơn |

**Ba quy tắc dùng lại từ P5** [REPO: `dac-ta-do-thi.md` §46]:
- Metric chung của cả service là bối cảnh dùng chung, **không được nhân lên** thành bằng chứng riêng của từng thao tác.
- Chưa xác định service chạy trên máy nào thì không gắn metric của máy vào service.
- Cạnh tĩnh không lấp chỗ thiếu của quan sát.

**Giới hạn theo nguồn dữ liệu:**
- RE2-TT và Nezha: bộ chuyển dữ liệu dev đặt `kind=null` [REPO: `dac-ta-do-thi.md` dòng 19]. Cạnh chỉ là quan hệ cha–con **chưa phân kiểu**; không tách được thời gian chờ lời gọi khỏi thời gian tự làm việc khác. Trên hai bộ này chỉ được gọi là *khai thác quan hệ span quan sát được*.
- FlashTicket: *dự kiến* có kind; chỉ dùng sau khi xác minh dữ liệu xuất thật. [ĐO]
- Cạnh DB: trong mã Tempo v2.9.0, độ trễ phía server của cạnh DB lấy từ chính span phía client, nên không phải phép đo độc lập ở phía DB. [TL: mã nguồn] Đây là giới hạn của nguồn đo này, không phải kết luận chung.
- UV-6 (log, tín hiệu giảm) không phụ thuộc kind.

### 6.3. Xếp hạng [ĐX]

**Câu hỏi trọng tâm:** phân bổ bằng chứng theo vị trí ghi tín hiệu và theo quan hệ quan sát được, có giúp xếp hạng tốt hơn cách gán cho service sở hữu span không?

**Các điều chỉnh để kiểm** (đều là giả thuyết, hiệu quả chưa kiểm):
1. **R1 (UV-1):** bằng chứng ghi ở span phía gọi của lời gọi tới X được tính một phần cho X, hoặc cho chính cạnh đó, theo quy tắc khai trước. Công thức chọn trên dev. Căn cứ hiện có là **vị trí của dấu hiệu** (G2-H06, mức ĐC), chưa phải bằng chứng rằng các phương pháp sai vì gán cho bên gọi.
2. **R2 (UV-6):** dùng log lỗi và tín hiệu giảm (tỷ lệ thành công giảm) cho lỗi không làm tăng độ trễ.
3. **R4b:** nếu cách xếp hạng dùng thứ tự thời gian ("cái nào bất thường trước"), thì thử cho phép một khoảng dung sai, vì tín hiệu ở các thành phần có thể lệch thời gian với nhau. Việc lệch thời gian giữa nguyên nhân và triệu chứng đã được nghiên cứu ở nơi khác (LagRCA), nhưng **chưa có căn cứ** rằng nó xảy ra trên dữ liệu của đồ án. Báo động trước mốc (G2-H21, G2-H22) **chưa được phân xử nguyên nhân**, nên không được dùng làm căn cứ cho điều chỉnh này.

**Tập xếp hạng theo WHY-26 (R3):**
- Giữ đủ thành phần trong mô hình; báo độ phủ.
- Không loại ứng viên chỉ vì chưa vượt ngưỡng bất thường cục bộ.
- Thành phần được xếp hạng phải có điểm suy ra từ bằng chứng trực tiếp, hoặc từ quan hệ theo quy tắc đã khai.
- Thành phần chưa đủ bằng chứng được báo riêng, **không điền điểm mặc định**.
- Tập chấm, tập trả về và cách xử lý thiếu bằng chứng xác định trước khi so với baseline.

**Không cam kết:** PageRank, tách ba loại lỗi (mạng, bên gọi, bên được gọi), bộ phát hiện mới.

### 6.4. RCA trả về gì [ĐX]

1. **Danh sách xếp hạng**: ứng viên (mức thao tác và mức service), điểm, lý do ngắn.
2. **Đồ thị sự cố**: nút và cạnh, mỗi nút có vai trò:
   - **Nghi là nguồn**;
   - **Bị ảnh hưởng** (bất thường nhưng được giải thích bởi thành phần phía dưới);
   - **Bình thường**;
   - **Thiếu dữ liệu**.
3. **Đường lan truyền**: chuỗi cạnh từ nguồn nghi ngờ lên cổng vào.
4. **Bằng chứng trên từng nút và cạnh**: số liệu thay đổi so với nền, trace mẫu, dòng log mẫu, truy vấn metric.
5. **Lời giải thích** bằng LLM (bước 5, làm sau). LLM chỉ giải thích, không quyết định xếp hạng.

**Nơi ghi:**
- JSON qua API của dịch vụ RCA, để Infinity đọc.
- Postgres, để giữ lịch sử và chấm điểm lại.
- Dấu sự cố trên mọi biểu đồ: `POST /api/annotations` với `time`, `timeEnd`, `tags`, `text`; không chỉ định dashboard thì thành annotation của cả tổ chức. [TL]

**Lưu số liệu đồ thị theo từng phút** để vẽ lại nhanh cho mọi khoảng thời gian. [ĐX]

---

## 7. Giao diện

### 7.1. Tùy chỉnh được tới đâu

| Mức | Làm được gì | Nhãn |
|---|---|---|
| **Dùng nguyên, không đổi** | Service Graph trong Explore (mức service; vòng màu: xanh thành công, đỏ lỗi máy chủ, vàng lỗi, tím bị giới hạn; số trong nút là thời gian phản hồi và request/giây; kèm bảng RED; click service mở menu sang trace, metric). Panel Traces (một trace, theo biến `${traceId}`). Panel log. Exemplar (ngôi sao trên biểu đồ, click mở trace; chỉ hỗ trợ nguồn Prometheus). Trace sang log (lọc theo trace ID; lọc theo span ID nếu log có span ID; có thể nới thời gian, ví dụ ±2 s) | [TL] |
| **Tùy chỉnh bằng dữ liệu, không lập trình** | Panel **Node graph**: nhóm quyết định nút nào hiện, màu, kích thước, chữ, nét đứt, liên kết khi click, bằng các trường dữ liệu đưa vào. Dữ liệu lấy qua **Infinity datasource** (đọc JSON/CSV/XML/GraphQL từ URL; cần hai truy vấn: nút và cạnh) | [TL] |
| **Không làm được bằng cấu hình** | Đổi ý nghĩa màu của Service Graph có sẵn; đóng khung nhóm nút theo service; thanh trượt thời gian hay hoạt ảnh trong Node graph. Tài liệu không mô tả các tính năng này | [TL: không có trong tài liệu] |
| **Cần lập trình** | Panel riêng bằng React, công cụ `@grafana/create-plugin`; tài liệu hướng dẫn hiện yêu cầu Grafana 10 trở lên | [TL] |

### 7.2. Panel Node graph: mỗi trường nghĩa là gì trên màn hình

Cơ chế nhận dữ liệu [TL]: cần ít nhất khung cạnh (`id`, `source`, `target`); khung nút (`id`) là tùy chọn. Grafana nhận ra khung khi `frame.meta.preferredVisualisationType = 'nodeGraph'`, hoặc tên khung hay `refId` là `nodes`/`edges`. Mặc định hiện tối đa 200 nút; phần dư ẩn sau ký hiệu "Hidden nodes", click để mở. Bố trí: Layered (mặc định, hợp đồ thị service), Force (hợp từ 500 nút), Grid. Kéo để di chuyển, có nút phóng to/thu nhỏ. Click nút hoặc cạnh mở menu kèm liên kết; panel này không hỗ trợ "Actions".

| Người xem thấy | Ý nghĩa [ĐX] | Trường dữ liệu [TL] |
|---|---|---|
| Nút **đỏ**, có dấu nổi bật | Nghi là nguồn, hạng 1 | `color`, `highlighted` |
| Nút **cam** | Bị ảnh hưởng | `color` |
| Nút **xám** | Bình thường (có quan sát, không thấy bất thường) | `color` |
| Nút **tím nhạt**, có dấu "?" trong chữ | **Chưa xác định / thiếu dữ liệu**: chưa có quan sát đủ để nói bình thường hay bất thường. Không thấy lỗi **không** có nghĩa là bình thường | `color`, `mainstat` |
| Nút **to hơn** | Điểm nghi ngờ cao hơn | `nodeRadius` (pixel) |
| **Vòng màu quanh nút** | Tỷ lệ request bình thường / chậm / lỗi | `arc__*`, các phần cộng lại bằng 1 |
| Chữ **trong** nút | Ví dụ "#1 · 0,82" và "p95 +850 ms" | `mainstat`, `secondarystat` |
| Chữ **dưới** nút | Tên thao tác; dòng phụ là tên service | `title`, `subtitle` |
| Vị trí nút cố định | Mỗi service là một cột, đọc như sơ đồ kiến trúc | `fixedX`, `fixedY` (đã dùng thì mọi nút phải có) |
| Cạnh **dày** | Nhiều lời gọi | `thickness` |
| Cạnh **đỏ** | Lời gọi có thay đổi bất thường | `color` |
| Cạnh **nét đứt** | Có trong kiến trúc nhưng không thấy trong trace (phân biệt tĩnh và quan sát của P5) | `strokeDasharray` |
| Rê chuột lên cạnh | Ví dụ "chờ phía gọi 950 ms · xử lý phía nhận 50 ms" | `mainstat`, `secondarystat` của cạnh |
| Click vào nút | Menu "Xem trace mẫu", "Xem log lỗi", "Xem biểu đồ", chi tiết | `detail__*` và liên kết |

**Rủi ro cần thử sớm:** một người dùng trên diễn đàn Grafana báo click không hiện chi tiết `detail__*`, chưa có lời giải. [ĐO]

### 7.3. Hiển thị gì khi hệ có hàng nghìn request mỗi giây

- Đồ thị **không hiển thị từng trace**. Đồ thị hiển thị **các thao tác gộp lại trong một cửa sổ**. Số nút là số thao tác (vài chục đến vài trăm), không phải số request. Trace chỉ là ví dụ khi click vào. [ĐX]
- **"Đường đi của sự cố"** [ĐX]: mọi thao tác trên các đường gọi từ route bị ảnh hưởng ở cổng vào tới các ứng viên đứng đầu, cộng tài nguyên chúng dùng, cộng lân cận một bước.
- **Hai mức xem**, đổi bằng biến dashboard [ĐX]:
  - **Mức service**: tối đa khoảng 15 nút với FlashTicket (mục 7.5). Điểm service lấy bằng điểm cao nhất trong các thao tác của nó.
  - **Mức thao tác**: toàn bộ đường đi sự cố, xuyên các service.
- **Phân biệt service bằng mắt**: tên service ở dòng phụ, tông màu theo service, ghim vị trí theo cột.

### 7.4. Thời gian: cửa sổ nào được vẽ

- **Mặc định:** cửa sổ sự cố so với nền; màu biểu thị mức thay đổi so với bình thường. [ĐX]
- **Đổi khung giờ:** Infinity chèn được thời gian đang chọn vào URL; các biến thời gian có sẵn của Grafana được điền ở phía trình duyệt; Infinity có macro `${__timeFrom}` điền ở phía máy chủ; URL không dùng biến thời gian thì không làm mới khi đổi khung giờ. [TL] Vậy đổi khung giờ thì đồ thị vẽ lại cho khoảng đó.
- **"Tua" bằng click:** data link dùng được `${__value.time}` (thời điểm của điểm được click), `${__from}`, `${__to}`, và mở dashboard khác kèm `var-<tên>=...`. [TL] Click vào điểm nhô lên trên biểu đồ đường thì đồ thị nhảy sang đúng phút đó. [ĐX]

### 7.5. Con số 15 nút mức service

Theo `implementation-readiness.md` §3 của repo FlashTicket [REPO]: 5 service nghiệp vụ (event, booking, payment, ticket, user) + 3 service hỗ trợ (api-gateway, config-server, discovery-server) + 5 hạ tầng (PostgreSQL, MongoDB, RabbitMQ, Redis, Keycloak) + 2 bên ngoài (VNPay, SMTP) = **15**. Đây là cận trên ở mức service. Một sự cố chỉ dùng một phần. Nếu tách riêng bốn database nghiệp vụ và `keycloak_db` (§4 của cùng file) thì số nút dữ liệu tăng.

### 7.6. Bố cục dashboard [ĐX]

Ví dụ dưới đây dựng theo luồng **bắt đầu thanh toán** của B13 [REPO: B13 dòng 50–56, 126]: người mua gọi `POST /orders/{orderId}/payment-attempts` (thuộc Payment); Payment gọi `POST /internal/v1/orders/{id}/freeze-payment` (thuộc Booking) để khóa đơn; Booking đọc/ghi database của Booking. Các bước sau đó phối hợp qua thông điệp (`booking.accept-payment.v1`…) và không vẽ ở đây. Tên nút ở tầng cổng vào và tên database là **giả định**; tên thao tác thật chỉ biết khi có trace FlashTicket. [ĐO]

Lỗi được tiêm: Toxiproxy thêm trễ trên **kết nối** từ Booking tới database của Booking.

```
Dashboard "Sự cố #12 – 14:03 – Bắt đầu thanh toán chậm"  [khung giờ: 13:50 → 14:10]  [Mức: thao tác ▼]

  CỔNG VÀO                 PAYMENT                          BOOKING                         DỮ LIỆU
 ┌───────────────┐      ┌──────────────────────┐      ┌───────────────────────────┐     ┌────────────┐
 │route thanh    │═════▶│POST /orders/{orderId}│═════▶│POST /internal/v1/orders/  │════▶│ booking_db │
 │toán (cam)     │      │/payment-attempts     │      │{id}/freeze-payment        │  ▲  │ (? chưa rõ)│
 └───────────────┘      │ (cam)                │      │ (cam)                     │  │  └────────────┘
                        └──────────────────────┘      └───────────────────────────┘  │
                                                         cạnh truy cập DB: ĐỎ, #1 ────┘
  Rê chuột lên cạnh Booking → booking_db: "thời gian lời gọi DB 850 ms; trước sự cố 20 ms"

 [Bảng xếp hạng]  #1 đường truy cập booking_db từ Booking: lời gọi DB chậm, lỗi không đổi
                  #2 freeze-payment: thời gian không bị span con phủ không đổi, chậm do chờ lời gọi DB
 [Trace mẫu] [Log lỗi] [Biểu đồ p95, có dấu lúc cảnh báo / lúc tiêm lỗi] [Giải thích]
```

Số trên hình là **minh họa**, không phải số đo. Lưu ý về cách gọi tên:
- Thời gian của cạnh DB chỉ đo được ở **phía Booking** (span CLIENT có thuộc tính DB). Trong Tempo v2.9.0, độ trễ phía server của cạnh DB cũng lấy từ chính span client [TL: mã nguồn]. Vì vậy phép đo **không tách được** trễ mạng, chờ kết nối, hay database xử lý chậm.
- Kết luận đúng mức là "**đường truy cập DB chậm**". Muốn nói "database xử lý chậm" thì phải có quan sát ở phía database (ví dụ metric của chính Postgres).
- Vai trò "bị ảnh hưởng" của các nút cam là **suy luận** của RCA, không phải điều đã quan sát trực tiếp.
- **Quy tắc nhãn đáp án** khi chấm [ĐX]: lỗi tiêm trên kết nối Booking → DB được gán cho thành phần "đường truy cập DB của Booking" (cạnh), không gán cho database. Quy tắc này khai trước khi chạy.

| Panel | Hiển thị | Nguồn |
|---|---|---|
| ① Danh sách sự cố (trang chủ) | Mỗi dòng một sự cố; click mở dashboard của sự cố | Postgres hoặc API RCA |
| ② Node graph | Đường đi sự cố (mục 7.3) | API RCA qua Infinity |
| ③ Bảng xếp hạng | Thứ hạng, điểm, loại bằng chứng, cờ độ phủ | API RCA |
| ④ Trace mẫu | Bảng vài trace ID do RCA chọn; click một dòng thì panel Traces hiện trace đó | API RCA, Tempo |
| ⑤ Log | Log lỗi của service được chọn, hoặc của trace đang xem | Loki |
| ⑥ Biểu đồ RED | Ứng viên số 1 so với nền; annotation; exemplar | Prometheus |
| ⑦ Giải thích | Văn bản LLM | API RCA |
| ⑧ Service Graph có sẵn của Grafana | Đặt cạnh ② để đối chiếu | Tempo, Prometheus |

---

## 8. Lưu trữ, dung lượng, xóa dữ liệu

### 8.1. Grafana Cloud hay tự cài

| Cách | Ai chạy | Giới hạn |
|---|---|---|
| Grafana Cloud Free | Grafana Labs | 10.000 chuỗi metric, 50 GB log, 50 GB trace, 50 GB profile mỗi tháng; lưu 14 ngày; 3 người dùng; Application Observability 2.232 host-giờ; Assistant: 3 người dùng AI, mỗi người 40 triệu token mỗi tháng, thêm quỹ 25 triệu token cho lượt tự động; hết hạn mức thì bị chặn tới tháng sau, không bị tính tiền; Investigations tính phí từ 01/10/2026 [TL]. Knowledge Graph không tính giá riêng, tính theo host-giờ của Application Observability cộng khoảng 5–10% chuỗi metric [TL]; việc Knowledge Graph bật được trên gói Free là **suy luận**, không trang nào ghi đích danh |
| **Tự cài trên EC2** | Nhóm | Không có hạn mức dịch vụ; giới hạn bởi **ổ đĩa, RAM, CPU và tốc độ đọc ghi** của máy. Ở chế độ monolithic, các thành phần của Tempo dùng chung một nhóm tài nguyên, truy vấn có thể ảnh hưởng tới việc ghi, và có nguy cơ hết RAM [TL] |

**Khuyến nghị** [ĐX]: thực nghiệm chạy trên bản tự cài ở EC2. Grafana Cloud chỉ dùng nếu muốn so với Knowledge Graph. **Chưa có căn cứ** để nói một máy EC2 cụ thể chịu được toàn bộ stack cùng FlashTicket; phải đo (mục 14).

### 8.2. Ước lượng dung lượng [TÍNH]

Giả định (phải thay bằng số thật): 500 request/giây, 8 span mỗi request, tức 4.000 span/giây.

Mọi con số dưới đây là **giả định để hình dung**, không dùng để cam kết cấu hình.

- Kích thước mỗi span: tài liệu Tempo đặt ngưỡng monolithic 25–35 MB/s cho 55.000–80.000 span/s, suy ra khoảng **450 byte/span**. Con số này suy từ thông lượng, **không** cho biết kích thước của một dòng OTLP JSON trong file, cũng không cho biết dung lượng Tempo lưu sau khi nén.
- Trace ở toàn tốc: 4.000 × 450 B ≈ 1,8 MB/s ≈ **6,5 GB/giờ**. Ở 50 request/giây: khoảng 0,65 GB/giờ.
- Nếu giữ trọn 6,5 GB/giờ thì **1 ngày ≈ 156 GB; 2–3 ngày ≈ 312–468 GB**, vượt xa ổ 64 GB. Vì vậy ở tải lớn bắt buộc phải lấy mẫu, hoặc giữ rất ngắn, hoặc tăng ổ; dự toán thời hạn lưu phải tính theo **tỷ lệ giữ thực tế**.
- Grafana Cloud Free (50 GB trace/tháng) hết sau khoảng **8 giờ** ở toàn tốc.
- Metric: 10.000 chuỗi × 4 mẫu/phút × 1.440 phút × 2 byte ≈ **115 MB/ngày**.
- Tempo monolithic: 4.000 span/s thấp hơn ngưỡng 55.000 span/s về **thông lượng**, nhưng điều đó **không** chứng minh máy đủ RAM, CPU khi chạy cùng FlashTicket, Loki, Prometheus và truy vấn của RCA.
- Phải đo riêng [ĐO]: dung lượng file JSON, dung lượng Tempo, log, metric; RAM, CPU, đọc ghi trên cấu hình đích.

### 8.3. Ổ EC2 64 GB và việc xóa dữ liệu

- **Tăng dung lượng EBS** mà không cần tháo ổ hay khởi động lại máy; tối đa 4 lần thay đổi trong 24 giờ; **không giảm được**; sau khi tăng phải mở rộng hệ thống tệp. [TL]
- **Tự xóa dữ liệu cũ:**

| Kho | Mặc định | Đề xuất [ĐX] | Nhãn |
|---|---|---|---|
| Tempo | 14 ngày | Tính theo tỷ lệ giữ thực tế và dung lượng ổ; ở tải lớn có thể chỉ giữ được vài giờ (mục 8.2) | [TL] |
| Loki | **Không tự xóa** | **Bắt buộc bật** `retention_enabled`, đặt `retention_period`; compactor chạy một instance; index period 24 giờ | [TL] |
| Prometheus | 15 ngày | Thêm giới hạn theo dung lượng (`retention.size`, mặc định tắt) | [TL] |
| File trace cho RCA | Khi bật xoay vòng: 100 file × 100 MB | Tức tối đa khoảng 10 GB [TÍNH] | [TL] |

- Mỗi lượt thực nghiệm **lưu riêng đủ dữ liệu để chấm lại** vào thư mục run, phần còn lại để tự xóa [ĐX]. "Đủ" gồm: cửa sổ sự cố và cửa sổ nền của từng đợt; chuỗi metric mà các luật cảnh báo dùng, trên **toàn bộ** lượt chạy (cần để chọn ngưỡng và đếm báo động giả mỗi giờ); lịch sử trạng thái cảnh báo; sổ thực nghiệm; cấu hình sampling và số span bị bỏ. Không cần giữ toàn bộ trace của mọi thời điểm.
- B16 đang ghi giữ log và trace 7 ngày, metric 14 ngày [REPO: `B16-observability-baseline.md` dòng 97]. Mức này có thể phải rút ngắn khi chạy tải lớn; việc đổi cần nhóm hệ thống đồng ý.

---

## 9. Tiêm lỗi và sinh tải

| Loại lỗi | Công cụ | Cơ chế | Nhãn |
|---|---|---|---|
| Trễ một lời gọi; DB, Redis, RabbitMQ chậm | Toxiproxy đặt giữa hai thành phần | Proxy TCP. Toxic: `latency` (kèm `jitter`), `timeout`, `reset_peer`, `bandwidth`, `slow_close`, `limit_data`, `slicer`, `packet_loss`; `toxicity` là xác suất áp dụng (mặc định 1,0); `stream` là chiều. Thêm toxic bằng `POST /proxies/{proxy}/toxics`. Tắt proxy để mô phỏng mất kết nối | [TL] |
| — | Toxiproxy | **Không tạo được lỗi HTTP 500**: Toxiproxy là proxy TCP; tài liệu không liệt kê toxic mức HTTP. Đây là suy luận từ mô tả | [TL + suy luận] |
| Lỗi trả về HTTP **tại proxy** | Envoy fault filter đặt trước service | Trả mã HTTP chọn sẵn cho một tỷ lệ request; thêm trễ cố định; điều khiển được qua header nếu bật [TL]. Request bị chặn **ngay tại proxy**, không tới service đích, nên **không** có log lỗi hay span SERVER lỗi ở service đó. Đây là lỗi trên đường gọi, không phải lỗi bên trong service | [TL]; hệ quả là suy luận |
| Lỗi bên trong ứng dụng (có log lỗi tương ứng) | Cơ chế bật lỗi trong chính FlashTicket, ví dụ một cờ cấu hình khiến một thao tác ném lỗi và ghi log | Cần nhóm hệ thống thêm vào code. Đây là cách duy nhất trong bảng tạo ra đúng tín hiệu mà UV-6 cần kiểm (log lỗi tại root) | [ĐX] |
| Service chết, treo, cạn CPU hoặc bộ nhớ, mất gói | Pumba | `kill`, `stop`, `pause`, `rm`, `restart`; `netem delay/loss/duplicate/corrupt/rate`; `iptables loss`; `stress` (dùng stress-ng); chọn container theo tên, regex (`re2:`), nhãn; đặt thời lượng bằng `--duration` | [TL] |
| Hàng đợi ứ | Pumba `pause` container consumer | Thông điệp dồn lại | [TL cho lệnh; kết quả là suy luận] |

**Sinh tải bằng k6, executor `constant-arrival-rate`** [TL]: lập lịch bắt đầu một số **iteration** cố định mỗi khoảng thời gian (`rate`, `timeUnit` mặc định 1s, `duration`, `preAllocatedVUs`, `maxVUs`), độc lập với tốc độ trả lời của hệ. Đây là mô hình mở. **Nhưng** khi hết VU rảnh, iteration bị **bỏ** (*"iterations drop if there are no free VUs"*), và k6 đếm vào metric `dropped_iterations` [TL]. Vậy khi sự cố nặng, **tải thực có thể giảm** so với tải đặt ra. [ĐX] Mỗi lượt phải:
- Định nghĩa rõ **một iteration** của kịch bản bán vé gồm những request nào (một iteration có thể chứa nhiều request).
- Ghi lại tải mục tiêu và tải đạt được: `dropped_iterations`, số VU, tốc độ request thực.
- Đặt `maxVUs` đủ lớn so với độ trễ tối đa dự kiến.

k6 đẩy được kết quả vào Prometheus qua `-o experimental-prometheus-rw`; tính năng **thử nghiệm**; Prometheus 2.x cần bật `--web.enable-remote-write-receiver`. [TL]

**Nhãn đáp án** [ĐX]: mỗi lần tiêm ghi vào "sổ thực nghiệm": thành phần bị tiêm, loại lỗi, thời điểm bắt đầu và kết thúc. Sổ này chỉ dùng để chấm điểm.

---

## 10. Đánh giá

### 10.1. Dữ liệu offline dùng để làm gì

- **Chọn công thức trên dev, có đáp án.** Đây là nơi duy nhất có nhãn root đáng tin.
- **Kiểm trên các ca khó**, báo riêng: lỗi trễ mạng (R1), lỗi trả về (R2, chủ yếu ở Nezha), ca bị loại khỏi tập ứng viên (R3). Không lấy điểm trung bình của RE2-TT ở chế độ (a) làm số chính, vì nhiều phương pháp đã gần trần ở đó.
- **So với baseline đã công bố** (bước 3, bước 4 của cô).
- **Giữ tập test khóa** làm phép kiểm độc lập sau khi chốt thiết kế.
- **Đo bộ cảnh báo ở chế độ (b) trên RE2-TT** bằng cách chạy lại luật trên dữ liệu đã ghi, **chỉ với những luật có tín hiệu tương ứng** (bảng dưới).
- **Không làm được:** kiểm cặp CLIENT–SERVER (không có kind); chứng minh tính thực tiễn online.

**Luật hoặc tín hiệu nào chạy được trên nguồn nào** (sơ bộ, phải kiểm lại trên dữ liệu):

| Luật hoặc tín hiệu | RE2-TT | Nezha-OB | FlashTicket |
|---|---|---|---|
| Lỗi 5xx trên span SERVER | **Không đủ đầu vào để đánh giá đúng luật** (chương trình vẫn tính được, nhưng kết quả không có nghĩa): cửa sổ dev của RE2-TT không có span mang mã lỗi (G2-H19, mục D3; `ban-do-g2.json#/rows/18/hien_tuong`) và không có kind | Không có kind; trạng thái span phải kiểm | Dự kiến có [ĐO] |
| Độ trễ theo thao tác | Có, từ thời lượng span | Có, nền trace ngắn (G2-H19 D1) | Dự kiến có [ĐO] |
| Log lỗi | Có, theo dữ liệu G2 dùng cho UV-6 | Có ở các ca lỗi trả về (UV-6) | Dự kiến có [ĐO] |
| Độ sâu hàng đợi | Phải kiểm có metric tương ứng | Phải kiểm | Dự kiến có (RabbitMQ) [ĐO] |
| Luật cần nền dài (so với tuần trước, nền 26 giờ) | Không, đoạn nền ngắn | Không | Có nếu chạy tải nền đủ lâu |

Nhiệm vụ trên các bộ dữ liệu: RE2-TT ở chế độ (a) và (b); Nezha-OB chỉ ở chế độ (a), không dựng chế độ (b) từ trace và log đã cắt quanh mốc tiêm (PLAN-P6 M10) [REPO]; FlashTicket ở chế độ (b) khi có dữ liệu.

**So sánh công bằng:**
- Khi đánh giá **riêng khâu xếp hạng**, mọi phương pháp và đối chứng dùng **cùng mốc và cùng cửa sổ**. Đổi đồng thời thời điểm cảnh báo và phương pháp RCA thì không quy được lợi ích về bên nào.
- Tách ba con số, đúng như PLAN-P6 M9: chất lượng bộ phát hiện; RCA tại cùng mốc; thành công toàn chuỗi. [REPO]
- Điểm P3 cũ chỉ dùng lại khi điều kiện tương ứng (dữ liệu, cửa sổ, tập chấm, tiền xử lý) không đổi; nếu đổi thì phải chạy lại baseline.

### 10.2. Đối chứng

| Đối chứng | Vai trò |
|---|---|
| 6 baseline đã chạy ở P3 | Mốc học thuật |
| **Heuristic của nhóm**, cùng đầu vào: chọn thành phần sâu nhất hoặc bất thường sớm nhất trong vùng lân cận trên đồ thị. Đây **chỉ là heuristic do nhóm tự đặt**. Nó **không đại diện** cho PAL hay FChain: theo phản biện của Codex ngày 20/10/2026 (dẫn bài PAL §2 và luận án của tác giả FChain), PAL còn có bước chọn điểm đổi và phân loại mẫu lan truyền, FChain còn kết hợp phụ thuộc và kiểm chứng lúc chạy; Claude chưa tự đọc hai bài gốc. Heuristic này cũng **không phải sản phẩm Grafana** | Mốc "luật đơn giản" |
| **Nhánh bỏ quan hệ**, nhận cùng tín hiệu (gồm log và tín hiệu giảm của UV-6). WHY-07: nhánh "không đồ thị" phải bỏ **mọi** chỗ dùng quan hệ, kể cả đặc trưng tạo từ quan hệ như self-time; nếu chỉ bỏ một bước thì kết luận chỉ nói về bước đó [REPO] | Tách lợi ích của tín hiệu khỏi lợi ích của quan hệ. **Phải khai chính xác** nhánh còn giữ thông tin cấu trúc gì. Ví dụ: chỉ bỏ bước phân bổ caller–callee nhưng vẫn dùng thời gian không bị span con phủ, thì gọi là "bỏ phân bổ", không gọi là "không đồ thị" |
| **Đồ thị ngẫu nhiên giữ bậc** (WHY-07 (b), PLAN-P6 M7) [REPO] | Kiểm lợi ích có đến từ **đúng cấu trúc phụ thuộc** hay không. Không có đối chứng này thì chỉ được kết luận về bước tính, không kết luận về cấu trúc |
| Coroot (10 lượt miễn phí mỗi tháng qua Coroot Cloud), Grafana Cloud Knowledge Graph hoặc Investigations nếu hạn mức cho phép | Tham chiếu định tính trên FlashTicket; đầu ra không cùng dạng nên không chấm chung độ đo xếp hạng |

### 10.3. Độ đo

- Xếp hạng: Hit@1, Hit@3, MRR, NDCG; tách theo loại lỗi và theo từng ca.
- Phát hiện: độ trễ phát hiện; số báo động giả mỗi giờ; Precision, Recall, F1 theo cửa sổ.
- Khoanh vùng: vùng nghi ngờ có chứa root không; vùng rộng bao nhiêu.
- Toàn chuỗi: phát hiện đúng rồi xếp đúng.

---

## 11. Kịch bản vận hành thực tế

Mục này mô tả người dùng làm được gì và nhận được gì. Các con số là **minh họa**.

### 11.1. Người vận hành, ngày bình thường

1. Mở Grafana, vào **trang "Danh sách sự cố"**: trống hoặc chỉ có sự cố đã đóng.
2. Mở **Service Graph có sẵn**: thấy khoảng 10–15 nút service, vòng màu chủ yếu xanh; số trong nút là thời gian phản hồi và request/giây.
3. Mở dashboard RED: các thao tác chính như `POST /orders` (Booking) và `POST /orders/{orderId}/payment-attempts` (Payment) có tỷ lệ lỗi thấp, p95 ổn định.

Luồng nghiệp vụ dùng trong mục này theo B13 [REPO]: người mua tạo đơn bằng `POST /orders` (Booking); bắt đầu thanh toán bằng `POST /orders/{orderId}/payment-attempts` (Payment); Payment gọi `POST /internal/v1/orders/{id}/freeze-payment` (Booking) để khóa đơn; sau khi có kết quả thanh toán, Payment gửi `booking.accept-payment.v1` cho Booking, và gửi `ticket.issue.v1` cho Ticket để phát vé. Tên nút ở tầng cổng vào và tên database là **giả định** [ĐO].

### 11.2. Sự cố xảy ra: đường truy cập database của Booking chậm

Trong thực nghiệm, sự cố do Toxiproxy tạo: thêm 800 ms trễ trên **kết nối** từ Booking tới database của Booking, lúc 14:00:00 (ghi vào sổ thực nghiệm). Theo quy tắc nhãn khai trước (mục 7.6), đáp án là "đường truy cập DB của Booking".

1. **14:00–14:02.** Bắt đầu thanh toán chậm dần, vì `freeze-payment` phải chờ DB. k6 tiếp tục lập lịch theo nhịp đặt ra; nếu hết VU rảnh thì iteration bị bỏ và `dropped_iterations` tăng, nghĩa là **tải thực có thể thấp hơn tải đặt ra** (mục 9). Người làm thực nghiệm ghi lại cả hai.
2. **Khoảng 14:01–14:02.** Luật **Prometheus** "p95 theo thao tác vượt mức nền" chuyển sang **pending** cho `freeze-payment` và `payment-attempts`. Luật lỗi 5xx chưa bật, vì chưa có lỗi.
3. **Khoảng 14:02–14:03.** Hết thời gian `for`; cảnh báo chuyển **firing**. Alertmanager gửi webhook (các trường `status`, `labels`, `startsAt`… [TL]). Dịch vụ RCA thấy chưa có đợt nào đang mở, nên **mở đợt #12** và gom các cảnh báo cùng khoảng thời gian vào đó (mục 6.1). Webhook nhắc lại về sau chỉ ghi vào đợt #12, không chạy RCA lần nữa.
4. **Dịch vụ RCA:**
   - Đọc chuỗi `ALERTS` để biết lúc bắt đầu pending (khoảng 14:01).
   - Đặt cửa sổ sự cố khoảng 13:59 → **mốc chốt 14:05** (lúc báo + 2 phút); cửa sổ nền khoảng 13:30–13:59.
   - **Chờ tới khoảng 14:05:30 cộng biên an toàn** (mốc chốt + `decision_wait` 30 s) rồi mới đọc dữ liệu.
   - Đọc trace từ file, RED và metric từ Prometheus, số log lỗi từ Loki; ghi lại độ phủ trace của cửa sổ; dựng đồ thị; xếp hạng; ghi JSON, Postgres và annotation.
   - Kết quả có sớm nhất **sau 14:05:30**; thời gian tính cần đo [ĐO]. Toàn bộ khoảng từ 14:00 tới lúc có kết quả được tính vào độ trễ toàn chuỗi.
5. **Người vận hành nhận được:**
   - Một dòng mới trong "Danh sách sự cố": "#12 – 14:03 – Bắt đầu thanh toán chậm – nghi: đường truy cập booking_db".
   - Một dấu dọc trên mọi biểu đồ lúc 14:03 (annotation).

### 11.3. Người vận hành mở sự cố

1. **Click dòng #12** → mở dashboard "Sự cố #12", khung giờ đặt sẵn 13:50–14:10.
2. **Nhìn đồ thị mức thao tác** (hình ở mục 7.6):
   - Từ trái sang phải: cổng vào, Payment, Booking, dữ liệu.
   - **Cạnh truy cập DB từ Booking tới `booking_db` đỏ**, chữ "#1".
   - `payment-attempts` và `freeze-payment` **cam** (RCA suy luận là bị ảnh hưởng).
   - Nút `booking_db` **tím nhạt, có dấu "?"** (chưa xác định): chưa có quan sát nào ở phía database, nên RCA không kết luận database bình thường hay bất thường.
3. **Rê chuột lên cạnh** Booking → `booking_db`: "thời gian lời gọi DB 850 ms; trước sự cố 20 ms".
4. **Đọc bảng xếp hạng:** "#1 đường truy cập booking_db từ Booking: lời gọi DB chậm, lỗi không đổi"; "#2 freeze-payment: thời gian không bị span con phủ không đổi, chậm do chờ lời gọi DB".
5. **Click cạnh → "Xem trace mẫu"** → panel Traces hiện một trace: span `payment-attempts` của Payment dài khoảng 950 ms; bên trong là span gọi `freeze-payment`; trong đó là span truy vấn DB của Booking dài khoảng 850 ms.
6. **Click "Xem log lỗi"** → panel log hiện log của Booking trong cửa sổ sự cố (nếu ứng dụng có ghi, ví dụ cảnh báo chờ kết nối).
7. **Click điểm nhô lên ở biểu đồ p95** lúc 14:01 → đồ thị vẽ lại cho phút đó.
8. **Đặt cạnh Service Graph có sẵn của Grafana:** Service Graph cũng có **cạnh tới DB** và cho thấy độ trễ tăng ở mức service [TL]. Phần nhóm làm thêm là: mức **thao tác** (thao tác nào chậm), **cách phân bổ bằng chứng** giữa các thao tác, **xếp hạng**, và **dẫn được từ kết luận về bằng chứng** (trace, log, số liệu).
9. **Đọc panel giải thích** (khi đã có LLM): "Lời gọi từ Booking tới database của Booking chậm từ khoảng 14:00, làm chậm khóa đơn và bắt đầu thanh toán. Chưa có quan sát phía database để biết database xử lý chậm hay đường kết nối chậm. Gợi ý: kiểm tra kết nối và tải của database."

### 11.4. Ba biến thể để thấy R1, R2, R3

| Biến thể | Cách tạo | Người dùng thấy gì [ĐX] | Yêu cầu liên quan |
|---|---|---|---|
| Trễ trên đường gọi Payment → Booking (`freeze-payment`) | Toxiproxy latency giữa Payment và Booking | Cạnh Payment → Booking đỏ; rê chuột: "chờ phía gọi 950 ms · xử lý phía nhận 50 ms". `freeze-payment` không đỏ, vì Booking xử lý vẫn nhanh. Chỉ kiểm được khi có kind, và phần chênh vẫn có thể gồm cả chờ kết nối, không chỉ mạng | R1 |
| Booking ném lỗi bên trong `freeze-payment` và ghi log | Cơ chế bật lỗi trong code FlashTicket (mục 9, cần nhóm hệ thống thêm) | Độ trễ không tăng; span SERVER của Booking lỗi 5xx; log lỗi của Booking tăng; Booking đỏ nhờ bằng chứng log và tỷ lệ thành công giảm | R2 |
| (Biến thể khác của R2) Envoy trả 5xx trước Booking | Envoy fault filter | Lỗi **tại proxy**: Booking không chạy, **không** có log lỗi ở Booking. Đáp án là "đường gọi tới Booking", không phải Booking. Không dùng biến thể này để kiểm UV-6 | — |
| Ticket-service, nơi nhận `ticket.issue.v1` từ Payment (B13), bị dừng | Pumba `stop` ticket-service | Hàng đợi tương ứng ứ (luật độ sâu hàng đợi bật); nút hàng đợi đỏ; ticket-service không còn span nên hiện "thiếu dữ liệu", được báo riêng chứ không bị bỏ khỏi danh sách. Lưu ý ticket-service còn có API HTTP (ví dụ `GET /orders/{orderId}/tickets`), nên nó vẫn có thể có lưu lượng HTTP trước khi dừng | R3 |

### 11.5. Người làm thực nghiệm

1. Viết kịch bản: tải nền đủ lâu; tiêm một lỗi trong một khoảng; chờ hệ hồi phục theo tiêu chí "đoạn bình thường" (mục 5.6); lặp với các loại lỗi khác. Độ dài từng đoạn chọn sau lượt chạy thử.
2. Chạy. Mỗi lần tiêm ghi vào sổ thực nghiệm. Ghi cả tải mục tiêu và tải đạt được của k6.
3. Sau mỗi đợt sự cố, RCA tự chạy một lần và lưu kết quả vào Postgres.
4. Cuối lượt, một script đối chiếu sổ thực nghiệm với kết quả:
   - Độ trễ phát hiện và độ trễ toàn chuỗi.
   - Báo động giả mỗi giờ, chỉ trên các đoạn bình thường.
   - Hit@1, Hit@3, MRR theo loại lỗi.
   - So với các đối chứng ở mục 10.2.
5. Lưu đủ dữ liệu để chấm lại (mục 8.3) vào thư mục run.

### 11.6. Những gì người dùng **không** nhận được

- Không có cam kết "đúng root". Xếp hạng là gợi ý, kèm bằng chứng để người xem tự kiểm.
- Không có phát hiện tự động kiểu Cloud (Knowledge Graph, ML) ở bản tự cài.
- Không có hoạt ảnh lan truyền theo thời gian trong Node graph.
- Không tự sửa lỗi.

---

## 12. Đóng góp, nói đúng mức, và câu hỏi cho cô

### 12.1. Đóng góp

1. **Xây dựng và tích hợp:** cơ chế hỗ trợ chẩn đoán và giao diện minh họa chạy trên FlashTicket, tận dụng stack công nghiệp (đáp ứng DT18-NV3); mô hình đồ thị mức thao tác, ánh xạ log, trace, metric lên nút và cạnh, phân biệt cạnh tĩnh và cạnh quan sát (P5, đáp ứng DT18-NV2).
2. **Điều chỉnh phương pháp có căn cứ:** cơ chế lan truyền và xếp hạng, kiểm các giả thuyết R1, R2, R4b và quy tắc tập xếp hạng R3 (mục tiêu 3 trong thư 22/08 của cô). R1 và R4b là **giả thuyết**; căn cứ hiện có chưa xác nhận cơ chế (mục 1.3).
3. **Bằng chứng thực nghiệm:** đánh giá có đối chứng trên dữ liệu công khai có đáp án và trên FlashTicket.

### 12.2. Không được nói

- "Tốt hơn Grafana" hoặc "tốt hơn Coroot".
- "Grafana không giải quyết được R1–R4". R1–R4 là hạn chế của các baseline học thuật, không phải khoảng trống đã được chứng minh của Grafana.
- "Phương pháp mới". Lan truyền trên đồ thị dịch vụ đã có.
- "Đã có sản phẩm công nghiệp nên đồ án không có đóng góp công cụ". DT18 yêu cầu chính cơ chế và giao diện này.
- "Service Graph của Grafana không có cạnh DB". Có (mục 4.4).

### 12.3. Câu hỏi xin ý kiến cô

1. Chương 4 cho thấy ba nhóm hạn chế ở bước xếp hạng (R1–R3) và một hạn chế ở mốc phân tích (R4a). Nhóm dự định tập trung đóng góp vào cơ chế lan truyền và xếp hạng để xử lý R1–R3. Theo cô, trọng tâm này đã phù hợp chưa, hay nhóm nên đầu tư thêm vào phần phát hiện bất thường?
2. Với phần phát hiện, nhóm cân nhắc hai cách. Một là dùng luật cảnh báo chuẩn của hạ tầng giám sát để mở sự cố, rồi đo chất lượng của nó. Hai là tự xây bộ phát hiện có đồ thị tham gia trực tiếp. Theo cô, cách nào phù hợp với phạm vi và thời gian của đồ án?
3. Các nền tảng như Grafana và Datadog đã có tính năng tương quan sự cố. Nhóm dự định dùng chúng làm hạ tầng và làm đối chứng tham khảo, còn đóng góp nằm ở cơ chế và đánh giá trên dữ liệu có đáp án. Cô có lưu ý gì về cách trình bày đóng góp này khi bảo vệ?
4. Thực nghiệm trên FlashTicket cần tối thiểu những loại lỗi nào?

---

## 13. Những chỗ sẽ vỡ nếu dùng cấu hình mặc định

| # | Hiện tượng | Căn cứ | Cách sửa [ĐX] |
|---|---|---|---|
| 1 | Tiêm trễ trên 2 giây thì cạnh có thể **biến mất** khỏi Service Graph đúng lúc sự cố | `store.ttl` mặc định 2 giây; span không ghép được bị đếm riêng, không thành cạnh [TL]. Suy luận: span server xong trước, span client tới muộn hơn khoảng trễ [TÍNH] | Tăng `store.ttl` lớn hơn mức trễ lớn nhất sẽ tiêm. Không dựa vào Service Graph làm đồ thị chính |
| 2 | **Báo động giả trong flash sale** | FlashTicket trả 409 cho `SEAT_UNAVAILABLE`, `INSUFFICIENT_QUANTITY`… [REPO: B13 dòng 28, 101]. Theo quy ước OTel, 4xx làm span **CLIENT** thành Error [TL]. Tempo v2.9.0 coi span lỗi là span có `STATUS_CODE_ERROR` [TL: mã nguồn] | Luật lỗi chỉ dùng span SERVER (5xx); SLO loại trừ các mã hết vé hợp lệ |
| 3 | Cảnh báo chậm vài phút | Các mặc định 60 s ở mục 5.5 [TL] | Hạ về khoảng 15 s; đo lại từng luật |
| 4 | RCA chạy ngay khi có cảnh báo bị **thiếu trace** | `decision_wait` 30 s; span đến muộn [TL] | Chạy sau mốc chốt + `decision_wait` + biên (mục 6.1). **Chờ như vậy vẫn không bảo đảm đủ trace**; phải ghi lại độ phủ trace của mỗi lần chạy |
| 5 | Hết hạn mức Cloud hoặc đầy ổ | 50 GB trace/tháng; khoảng 6,5 GB/giờ ở tải giả định [TÍNH] | Tự cài; lấy mẫu khi tải lớn; bật retention của Loki |
| 6 | Luật "service dừng" không bao giờ bật | `absent()` chỉ bật khi không còn chuỗi; spanmetrics mặc định không cho chuỗi hết hạn [TL] | Dùng `up`, heartbeat, hoặc tốc độ request dưới tải đã biết (mục 5.2) |
| 7 | Một sự cố chạy RCA nhiều lần, hoặc nhiều sự cố bị gộp | Grafana gộp thông báo theo nhãn, có nhắc lại và thông báo khi nhóm đổi [TL] | Dịch vụ RCA tự định nghĩa đợt sự cố và chống xử lý trùng (mục 6.1) |
| 8 | Tải thực giảm đúng lúc sự cố nặng | k6 bỏ iteration khi hết VU rảnh [TL] | Ghi `dropped_iterations`; đặt `maxVUs` đủ lớn (mục 9) |

---

## 14. Chạy thử trước khi cam kết với cô

Đây là thao tác mới, **cần Minh duyệt riêng**. Chưa có căn cứ để ước lượng thời lượng; thời lượng thật chỉ biết khi bắt đầu làm. Bước S1 phải **chốt một bộ phiên bản** (Grafana, Tempo, Loki, Prometheus, Collector contrib, Java agent, Infinity) và đọc tài liệu đúng các phiên bản đó, vì nguồn ở mục 17 đang trộn tài liệu bản `latest`/`main` với mã Tempo v2.9.0.

| Bước | Việc | Trả lời câu hỏi nào |
|---|---|---|
| S1 | Dựng `grafana/otel-lgtm` trên EC2 cùng 2–3 service FlashTicket (nếu đã có) hoặc OpenTelemetry Demo | Máy chịu nổi không (RAM, CPU) |
| S2 | Collector theo mục 4.1 (đường xuất của B16); xem tên metric spanmetrics thực tế trong Prometheus; bật exemplar; bật tail sampling; bật file exporter; kiểm sampler ở cổng vào | Luồng ở mục 4 có chạy đúng không |
| S3 | Tiêm một toxic latency; đo thời điểm báo trừ thời điểm tiêm; kiểm Service Graph có mất cạnh không; kiểm log có trace_id trên Loki không; đo độ phủ trace sau mốc chốt; ghi `dropped_iterations` của k6 | Độ trễ phát hiện; vỡ số 1, 3, 4, 8; ánh xạ log |
| S4 | Xuất trace một cửa sổ → adapter → bộ dựng P5 → JSON → Infinity → Node graph; thử click, data link, `detail__*` | Giao diện ở mục 7 có làm được không |

**Ghi chú về OpenTelemetry Demo** (để thử sau; Minh yêu cầu ghi lại): ứng dụng nhiều service đã cài sẵn OTel; có cờ tạo lỗi bật tắt qua flagd tại `localhost:8080/feature`, ví dụ `paymentFailure` (lỗi trả về ở thanh toán), `paymentUnreachable` (không gọi tới được thanh toán), `kafkaQueueProblems` (consumer chậm, hàng đợi ứ), `productCatalogLockContention` (khóa bảng), `recommendationCacheFailure` (rò bộ nhớ), `adHighCpu`, `imageSlowLoad` (dùng Envoy fault); cần khoảng 6 GB RAM, hoặc khoảng 3 GB ở chế độ tối giản. [TL] Lợi ích: có hệ online có kind và có đáp án ngay, không phải chờ FlashTicket.

---

## 15. Phần còn thiếu và phải đo

**Phải đo [ĐO]:**
- Click vào nút Node graph có hiện `detail__*` không.
- RAM và CPU của toàn bộ stack cùng FlashTicket.
- Thời gian bộ dựng P5 xử lý một cửa sổ khoảng 15 phút.
- Khả năng đọc file trace ở tốc độ tải thực.
- Tên metric thực tế sau khi chuyển từ OTLP sang Prometheus.
- Thông điệp RabbitMQ nối trace bằng quan hệ cha–con hay bằng link.
- Log Logback có đi qua OTLP lên Loki kèm trace_id không.
- Độ dài cửa sổ tốt nhất; độ trễ phát hiện thật.

**Còn thiếu để thiết kế:**
- Công thức phân bổ bằng chứng (R1) và quy tắc thiếu bằng chứng (R3), chọn trên dev.
- Chỉ mục request/span theo thời gian (PLAN-P6 M2), vì đồ thị P5 đã gộp không giữ thời gian từng lần thực thi.
- Metric, log, nền (PLAN-P6 M3), gồm tín hiệu giảm.
- Bộ luật cảnh báo cụ thể và cách đo nó.
- Khảo sát tài liệu kỹ về tính mới của R1 trên dữ liệu có kind.
- Ý kiến của cô (mục 12.3).
- Cập nhật MRP, PLAN-P6, DECISIONS sau khi cô định hướng.

---

## 16. Những chỗ đã sửa so với các lượt trao đổi trước

| Đã nói trước | Sửa thành | Lý do |
|---|---|---|
| Investigations "đang public preview" | GA từ 29/07/2026 | Đã đọc trang tài liệu cũ, không kiểm ngày cập nhật |
| Coroot tự cài "có RCA" | RCA chỉ ở Enterprise, hoặc Community nối Coroot Cloud (10 lượt/tháng) | Đọc lại tài liệu Coroot |
| "Dùng Service Graph của Grafana" làm đồ thị | Service Graph chỉ ở mức service; đồ thị chính là P5 dựng từ trace thô | Service Graph không có cạnh giữa các thao tác |
| "Phương pháp minh bạch, không cần LLM" là điểm khác biệt | Bỏ. RCA Workbench dựa trên luật; Coroot đi theo đồ thị bằng ML, không LLM | Đã có sản phẩm làm |
| "Grafana chỉ phát hiện theo ngưỡng" | Luật PromQL/LogQL viết được thống kê; Cloud có insight, ML | Đọc lại tài liệu |
| RCA nhận luồng OTLP trực tiếp | RCA đọc file do Collector ghi; Tempo dùng khi xem chi tiết | Đơn giản hơn, không phải tự viết bộ nhận |
| "Chỉ xem thao tác của một service" | Hiện được toàn bộ đường đi sự cố xuyên service | Trình bày trước bị hiểu sai |
| Đầu vào RCA chỉ là RED | Gồm trace, RED, metric tài nguyên, hàng đợi, log | Trình bày trước thiếu |
| Hướng A "khớp đúng bước 2 của cô" | Chỉ đáp ứng một phần; phải hỏi cô | Codex phản biện lượt 1 |
| "Xếp hạng mọi thành phần" | Theo WHY-26: không điền điểm cho phần thiếu bằng chứng | Codex phản biện lượt 2 |
| Tách được ba nguyên nhân bằng chênh độ trễ | Không cam kết; chỉ kiểm được trên dữ liệu có kind; cạnh DB không có phép đo độc lập | Codex phản biện lượt 1, 2 |
| **Bản sửa 1 (20/10/2026), theo phản biện F01–F17 và tự soát N1–N4:** | | |
| RCA chờ 30 s rồi đọc tới 2 phút sau cảnh báo (F01) | Có mốc chốt; RCA chạy sau mốc chốt + `decision_wait` + biên; tính vào độ trễ toàn chuỗi (mục 6.1) | Tự mâu thuẫn; span đến muộn |
| `parentbased_always_on` "giữ mọi trace"; giữ 100% trace lỗi; RED "chính xác" (F02) | Có điều kiện; tail sampling chỉ ưu tiên; bộ đếm khác phân vị ước lượng (mục 4) | Đặc tả ParentBased; span đến muộn |
| Instrumentation chỉ cần cấu hình; adapter chỉ đổi định dạng (F03, N1) | Theo đường xuất của B16; phần ứng dụng phải tự bổ sung theo B16 §3; adapter phải kiểm ngữ nghĩa link (mục 3, 4.1, 4.2) | B16 dòng 24, §3; P5 §89 |
| Notification policy gom thành một sự cố, RCA chạy một lần (F04) | RCA tự định nghĩa đợt sự cố và chống xử lý trùng (mục 3, 6.1) | Tài liệu nhóm thông báo của Grafana |
| `absent()` cho service im lặng (F05) | `up`, heartbeat, hoặc tốc độ request dưới tải đã biết (mục 5.2) | spanmetrics không cho chuỗi hết hạn |
| Envoy trước payment làm log payment tăng (F06) | Envoy là lỗi tại proxy; lỗi R2 phải là lỗi trong ứng dụng (mục 9, 11.4) | Envoy chặn trước service |
| Root là `payment_db`, "database chậm" (F07) | "Đường truy cập DB chậm"; quy tắc nhãn khai trước (mục 7.6, 11) | Lỗi tiêm trên kết nối; cạnh DB chỉ đo phía client |
| Luồng Gateway → Booking `POST /bookings` → Payment `POST /payments` (F08, N4) | Luồng theo B13: Payment `payment-attempts` gọi Booking `freeze-payment` (mục 7.6, 11) | B13 dòng 50–56, 126, 154–160 |
| Service Graph "không chỉ ra cạnh DB" (F09) | Service Graph có cạnh DB; khác biệt nằm ở mức thao tác, phân bổ, xếp hạng, truy nguyên (mục 11.3) | Mã Tempo `upsertDatabaseRequest` |
| EC2 chỉ giới hạn bởi ổ đĩa; giữ trace 2–3 ngày (F10, N3) | Giới hạn cả RAM, CPU, đọc ghi; bỏ "2–3 ngày"; mọi số là giả định (mục 8) | Tài liệu deployment modes; 2–3 ngày ≈ 312–468 GB |
| k6 làm tải không giảm (F11) | Iteration bị bỏ khi hết VU; ghi `dropped_iterations` (mục 9) | Tài liệu k6 |
| R1 là nguyên nhân phương pháp xếp sai; báo trước mốc là căn cứ cho dung sai độ trễ (F12) | R1 là giả thuyết; R4 tách R4a/R4b; R4b chưa có căn cứ cơ chế (mục 1.3, 6.3) | `ban-do-g2.json` dòng 5, 20, 21 "chưa phân xử" |
| Nhánh bỏ quan hệ đủ để kết luận về quan hệ (F13) | Khai chính xác nhánh còn giữ gì; thêm đồ thị ngẫu nhiên giữ bậc (mục 10.2) | WHY-07, PLAN-P6 M7 |
| Chạy lại luật trên RE2-TT chỉ vướng nền ngắn (F14) | Bảng luật chạy được theo nguồn; RE2-TT dev không có span lỗi; so xếp hạng cùng mốc, cùng cửa sổ (mục 10.1) | G2-H19 D3; PLAN-P6 M9 |
| Báo động giả đếm trong đoạn không tiêm; chỉ lưu cửa sổ sự cố (F15) | Tiêu chí "đoạn bình thường"; lưu đủ dữ liệu để chấm lại (mục 5.6, 8.3) | PLAN-P6 |
| "Không thể đóng góp ở mức công cụ chẩn đoán" (F16) | Đóng góp tách ba phần: xây dựng và tích hợp, điều chỉnh phương pháp, bằng chứng (mục 2.3, 12.1) | DT18-NV3 |
| Cộng các khoảng thành cận trên 5,5 / 2,5 phút (F17) | Minh họa cho một luật, một đường dữ liệu; đo từng luật (mục 5.5) | `for` chỉ chạy khi điều kiện tiếp tục đúng |
| Heuristic là "xấp xỉ Workbench, PAL, FChain" | Chỉ là heuristic của nhóm (mục 10.2) | Phản biện Codex |
| Gắn nhãn [TL] cho câu "bản tự cài không có cơ chế tìm root" (N2) | "Không thấy trong tài liệu đã đọc" (mục 2.2) | Dùng sai nhãn |
| "Chạy thử 1–3 ngày" | Bỏ con số; S1 chốt bộ phiên bản (mục 14) | Không có căn cứ |
| **Bản sửa 2 (20/10/2026), theo lượt kiểm lại của Codex:** | | |
| `booking_db` tô xám (= bình thường) vì không có quan sát phía DB (F07 còn lại) | Thêm trạng thái "chưa xác định / thiếu dữ liệu" (tím nhạt, "?") ở mục 7.2; `booking_db` dùng trạng thái này (mục 7.6, 11.3) | Không thấy lỗi không có nghĩa là bình thường |
| Luật Grafana nhưng đọc `ALERTS` để lấy mốc pending (F18) | Tách hai trường hợp: luật Prometheus đọc `ALERTS`; luật Grafana phải bật lịch sử trạng thái (`GRAFANA_ALERTS` hoặc Loki), chưa rõ có ghi Pending; mục 11 dùng luật Prometheus (mục 6.1, 11.2) | Tài liệu lịch sử trạng thái cảnh báo của Grafana |
| Thứ tự lộ trình bỏ M5, M6, M8 (F19) | Thứ tự đầy đủ theo phụ thuộc PLAN-P6 (mục 18) | PLAN-P6 M6–M9 |
| Luật 5xx trên RE2-TT ghi "Không" (F14) | "Không đủ đầu vào để đánh giá đúng luật" (mục 10.1) | Phản biện Codex |

---

## 17. Nguồn

**Về phiên bản:** phần lớn tài liệu dưới đây là bản `latest` (Grafana, Tempo, Loki) hoặc nhánh `main` (Collector contrib, Java instrumentation), đọc ngày 19–20/10/2026; riêng mã Tempo là thẻ v2.9.0. Đây **chưa phải** một bộ phiên bản triển khai nhất quán. Bước S1 (mục 14) phải chốt phiên bản và đối chiếu lại các khẳng định [TL] với tài liệu của đúng phiên bản đó.

### Nguồn chính thức
- OTel Collector: [configuration](https://opentelemetry.io/docs/collector/configuration/), [architecture](https://opentelemetry.io/docs/collector/architecture/), [spanmetrics](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/spanmetricsconnector), [servicegraph](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/connector/servicegraphconnector), [tail sampling](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor), [file exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/fileexporter), [docker_stats](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/dockerstatsreceiver)
- OTel Java: [configuration](https://opentelemetry.io/docs/languages/java/configuration/), [supported libraries](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md), [logger MDC](https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/logger-mdc-instrumentation.md), [runtime telemetry](https://explorer.opentelemetry.io/java-agent/instrumentation/runtime-telemetry), [RabbitMQ](https://explorer.opentelemetry.io/java-agent/instrumentation/rabbitmq-2.7), [instrumentation settings](https://opentelemetry.io/docs/zero-code/java/agent/instrumentation/)
- OTel spec: [HTTP spans](https://opentelemetry.io/docs/specs/semconv/http/http-spans/), [logs data model](https://opentelemetry.io/docs/specs/otel/logs/data-model/)
- Tempo: [Service Graph](https://grafana.com/docs/tempo/latest/metrics-from-traces/service_graphs/), [custom service graphs](https://grafana.com/docs/tempo/latest/metrics-from-traces/service_graphs/custom-service-graphs/), [API](https://grafana.com/docs/tempo/latest/api_docs/), [TraceQL](https://grafana.com/docs/tempo/latest/traceql/construct-traceql-queries/), [TraceQL metrics](https://grafana.com/docs/tempo/latest/metrics-from-traces/metrics-queries/), [configuration](https://grafana.com/docs/tempo/latest/configuration/), [deployment modes](https://grafana.com/docs/tempo/latest/reference-tempo-architecture/deployment-modes/), [OTel Collector với Tempo](https://grafana.com/docs/tempo/latest/set-up-for-tracing/instrument-send/set-up-collector/otel-collector/), mã nguồn [servicegraphs.go v2.9.0](https://github.com/grafana/tempo/blob/v2.9.0/modules/generator/processor/servicegraphs/servicegraphs.go)
- Prometheus: [configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/), [alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/), [functions](https://prometheus.io/docs/prometheus/latest/querying/functions/), [query basics](https://prometheus.io/docs/prometheus/latest/querying/basics/), [HTTP API](https://prometheus.io/docs/prometheus/latest/querying/api/), [storage](https://prometheus.io/docs/prometheus/latest/storage/), [feature flags](https://prometheus.io/docs/prometheus/latest/feature_flags/), [Alertmanager](https://prometheus.io/docs/alerting/latest/configuration/)
- Loki: [retention](https://grafana.com/docs/loki/latest/operations/storage/retention/), [limits](https://grafana.com/docs/loki/latest/configure/loki-limits/), [metric queries](https://grafana.com/docs/loki/latest/query/metric_queries/), [OTLP](https://grafana.com/docs/loki/latest/send-data/otel/)
- Grafana: [Node graph](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/node-graph/), [Traces panel](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/traces/), [data links](https://grafana.com/docs/grafana/latest/panels-visualizations/configure-data-links/), [annotations API](https://grafana.com/docs/grafana/latest/developers/http_api/annotations/), [exemplars](https://grafana.com/docs/grafana/latest/fundamentals/exemplars/), [trace to logs](https://grafana.com/docs/grafana/latest/datasources/tempo/configure-tempo-data-source/configure-trace-to-logs/), [Service Graph view](https://grafana.com/docs/grafana/latest/datasources/tempo/service-graph/), [alert rule evaluation](https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rule-evaluation/), [queries and conditions](https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/queries-conditions/), [notification policies](https://grafana.com/docs/grafana/latest/alerting/fundamentals/notifications/notification-policies/), [webhook](https://grafana.com/docs/grafana/latest/alerting/configure-notifications/manage-contact-points/integrations/webhook-notifier/), [Loki alerting](https://grafana.com/docs/grafana/latest/datasources/loki/alerting/), [build a panel plugin](https://grafana.com/developers/plugin-tools/tutorials/build-a-panel-plugin), [otel-lgtm](https://grafana.com/blog/2024/03/13/an-opentelemetry-backend-in-a-docker-image-introducing-grafana-otel-lgtm)
- Infinity: [node graph](https://grafana.com/docs/plugins/yesoreyeram-infinity-datasource/latest/advanced-features/node-graph/), [URL](https://grafana.com/docs/plugins/yesoreyeram-infinity-datasource/latest/advanced-features/url/)
- Grafana Cloud: [bảng giá](https://grafana.com/pricing/), [gói Free](https://grafana.com/products/cloud/free-tier/), [giá Knowledge Graph](https://grafana.com/docs/grafana-cloud/platform/pricing-and-usage/knowledge-graph/), [giá Assistant](https://grafana.com/docs/grafana-cloud/platform/pricing-and-usage/assistant/), [Knowledge Graph](https://grafana.com/docs/grafana-cloud/knowledge-graph/introduction/), [base insights](https://grafana.com/docs/grafana-cloud/platform/knowledge-graph/reference/about-base-insights/), [causality](https://grafana.com/docs/grafana-cloud/monitor-applications/asserts/introduction/causality), [outlier detection](https://grafana.com/docs/grafana-cloud/machine-learning/outlier-detection/), [forecasting](https://grafana.com/docs/grafana-cloud/ai-tools/machine-learning/forecasting/), [Investigations GA](https://grafana.com/whats-new/2026-07-29-assistant-investigations-is-now-generally-available-in-grafana-cloud/), [blog Knowledge Graph + LLM](https://grafana.com/blog/knowledge-graph-as-context-for-llms-demonstrating-decisive-rca-and-faster-production-performance), [khảo sát 2026](https://grafana.com/press/2026/03/18/grafana-labs-4th-annual-observability-survey-reveals-a-field-at-a-crossroads-ai-economics-complexity-and-the-enduring-power-of-open-source/)
- Coroot: [AI overview](https://docs.coroot.com/ai/overview), [editions](https://coroot.com/editions), [README](https://pkg.go.dev/github.com/coroot/coroot@v0.28.0)
- Bổ sung ở bản sửa 1: [OTel Tracing SDK, ParentBased](https://opentelemetry.io/docs/specs/otel/trace/sdk/), [tail sampling: Late-Arriving Spans](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/tailsamplingprocessor), [Grafana: nhóm thông báo](https://grafana.com/docs/grafana/latest/alerting/fundamentals/notifications/group-alert-notifications/), [k6 dropped iterations](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/dropped-iterations/), [Prometheus jobs and instances (`up`)](https://prometheus.io/docs/concepts/jobs_instances/); bản sửa 2: [Grafana alert state history](https://grafana.com/docs/grafana/latest/alerting/set-up/configure-alert-state-history/)
- Công cụ khác: [Toxiproxy](https://github.com/Shopify/toxiproxy), [Pumba](https://github.com/alexei-led/pumba), [Envoy fault filter](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/fault_filter), [k6 constant-arrival-rate](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/), [k6 Prometheus remote write](https://grafana.com/docs/k6/latest/results-output/real-time/prometheus-remote-write/), [RabbitMQ Prometheus](https://www.rabbitmq.com/docs/prometheus), [OpenTelemetry Demo feature flags](https://opentelemetry.io/docs/demo/feature-flags/), [OpenTelemetry Demo Docker](https://opentelemetry.io/docs/demo/docker-deployment/), [AWS EBS Elastic Volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-modify-volume.html), [Google SRE workbook](https://sre.google/workbook/alerting-on-slos/)

### Nghiên cứu
- [Groot (arXiv 2108.00344)](https://www.arxiv.org/pdf/2108.00344); [LagRCA (FSE 2026)](https://conf.researchr.org/details/fse-2026/fse-2026-industry-papers/18/Bridging-the-Delay-Lag-Aware-Spatio-Temporal-Causal-Inference-for-Microservice-Root-); [BARO (arXiv 2405.09330)](https://arxiv.org/pdf/2405.09330); [MicroRCA](https://hal.archives-ouvertes.fr/hal-02441640); [TraceDiag (arXiv 2310.18740)](https://arxiv.org/pdf/2310.18740); [khảo sát có PAL, FChain (arXiv 2105.12378)](https://arxiv.org/pdf/2105.12378); [khảo sát chẩn đoán lỗi microservice (arXiv 2407.01710)](https://arxiv.org/pdf/2407.01710)

### Nguồn bên thứ ba (độ tin thấp hơn, chỉ dùng làm chỉ dẫn)
- Báo lỗi `detail__*` trên diễn đàn: [community.grafana.com](https://community.grafana.com/t/how-to-do-field-overrides-with-node-graph-panel/55931); bài về spanmetrics trước tail sampling: [oneuptime](https://oneuptime.com/blog/post/2026-08-25-span-metrics-before-tail-sampling/view)

### Trong repo
- `results/T-034/goi-g2.md` §0, §3.2, §5; `results/T-035/dac-ta-do-thi.md` dòng 19, §29–31, §46, §89; `results/T-040/ban-giao-p6.md`; `docs/WHY.md` (WHY-02, WHY-26); `docs/MRP.md`; `docs/PLAN-P6.md`; `docs/DECISIONS.md` (Q-23, Q-70)
- Repo FlashTicket: `docs/architecture/B13-api-and-event-contracts.md` dòng 28, 50–56, 101, 126, 154–160; `docs/architecture/B16-observability-baseline.md` dòng 24, 26, §3, dòng 97, 103; `docs/architecture/implementation-readiness.md` §3, §4
- Repo này, bổ sung ở bản sửa 1: `results/T-034/ban-do-g2.json` (`#/rows/5/vi_sao`, `#/rows/18/hien_tuong`, `#/rows/20/vi_sao`, `#/rows/21/vi_sao`); `docs/WHY.md` (WHY-07); `docs/PLAN-P6.md` (M7, M9, M10)

---

## 18. Lộ trình và quan hệ với PLAN-P6 [ĐX]

Grafana chỉ là hạ tầng. Phần RCA vẫn phải tự nghiên cứu, nên **P6 vẫn tiếp tục, nhưng thu hẹp**. Bảng dưới là đề xuất; PLAN-P6 trong repo **chưa đổi** cho tới khi Minh duyệt và ghi vào DECISIONS.

| PLAN-P6 | Theo hướng này | Ghi chú |
|---|---|---|
| M1 thiết kế và giao thức | **Giữ** | Thiết kế cơ chế RCA, bộ luật cảnh báo, giao thức đánh giá (mốc, cửa sổ, tập chấm, quy tắc nhãn, tiêu chí đoạn bình thường) |
| M2 chỉ mục trace theo thời gian | **Giữ** | Cần vì đồ thị P5 đã gộp không giữ thời gian từng lần thực thi |
| M3 metric, log, nền | **Giữ** | Gồm tín hiệu giảm cho R2 |
| M4 điểm và xếp hạng RCA | **Giữ** | Phần lõi |
| M5 phát hiện và vùng nghi ngờ | **Thu hẹp** | Luật cảnh báo; phần nối cảnh báo với RCA (đợt sự cố, mốc chốt); vùng nghi ngờ để trình bày |
| M6 baseline phát hiện | **Thu hẹp** | Đo bộ luật cảnh báo được dùng; không cài detector mới |
| M7 đối chứng cấu trúc | **Giữ** | Nhánh bỏ quan hệ (khai rõ phần còn giữ) và đồ thị ngẫu nhiên giữ bậc |
| M8 điều phối chạy | Giữ ở mức nhỏ | |
| M9 ma trận dev RE2-TT | **Giữ** | Xử lý dữ liệu offline: chế độ (a) và (b), chỉ với luật có tín hiệu (mục 10.1) |
| M10 ma trận dev Nezha-OB | **Giữ** | Chỉ chế độ (a) |
| M11 độ nhạy, cơ chế, lựa chọn | **Giữ** | Gồm độ nhạy theo cửa sổ (R4a) |
| M12 so sánh cuối, kiểm toàn chuỗi | **Giữ** | Tách chất lượng phát hiện, RCA tại cùng mốc, thành công toàn chuỗi |
| M13 hồ sơ G3 | **Giữ** | |
| C8 (BOCPD theo luồng), C12 (GDN), C15 (GNN) | **Không kích hoạt** | Trừ khi cô yêu cầu |
| C13, C14 (dữ liệu bổ sung) | Chờ cô quyết | |
| **Việc mới** | Chạy thử S1–S4 (mục 14); pipeline online và dashboard (một phần của P9); cơ chế bật lỗi trong ứng dụng cho R2 (cần nhóm hệ thống) | |

**Dữ liệu offline:**
- Phần **dev** của RE2-TT và Nezha-OB dùng để chọn công thức và thiết kế (M9, M10, M11).
- Phần **test** vẫn **khóa tới G3**, dùng ở P7 làm phép kiểm độc lập sau khi khóa thiết kế.
- Kết quả trên dev không được gọi là bằng chứng hiệu quả cuối cùng.

**Thứ tự đề xuất:**
1. Gửi chương 5 xin cô định hướng (mục 12.3). Việc này không phải chờ thực nghiệm.
2. Song song, nếu Minh duyệt: chạy thử S1–S4.
3. Sau khi có định hướng của cô: cập nhật MRP, PLAN-P6, DECISIONS; soạn SPEC M1.
4. Làm theo phụ thuộc trong PLAN-P6 [REPO]:
   - **M1** trước.
   - **M2, M3** sau giao diện M1, làm song song được.
   - **M4, M5** khi có đầu vào cần thiết của M2, M3; **M6** bắt đầu sau M1 khi có đầu vào của M2, M3, chạy song song được với M4, M5.
   - **M7** khi giao diện tính của M4, M5 đủ rõ (không phải chờ chúng thắng).
   - **M8** khi giao diện M2–M7 ổn định ở phần cần chạy.
   - **M9, M10** sau những thành phần được dùng của M4–M8; M10 độc lập với M9.
   - **M11**, rồi **M12**, rồi **M13**.
