# Báo cáo tiến độ phần RCA — kết quả thực nghiệm phương pháp đồ thị trên dữ liệu công khai

Người báo cáo: Lê Văn Minh. Ngày: 09/11/2026 (bản nháp, chờ phản biện nội bộ).
Đề tài: Xây dựng hệ thống bán vé theo kiến trúc phân tán có ứng dụng đồ thị phụ thuộc để giám sát và chẩn đoán sự cố.

Báo cáo đi theo đúng chuỗi cô hướng dẫn: hiểu phương pháp đã có → thực nghiệm trên nhiều dataset → chỉ ra hạn chế → phương pháp đồ thị theo 5 bước → kết quả → tích hợp hệ thống. Phần 1–3 đã báo chi tiết ngày 21/10/2026; ở đây chỉ tóm tắt. Phần 4–5 là phần mới.

Thuật ngữ:

- *RCA* (root cause analysis — chẩn đoán nguyên nhân gốc).
- *Root*: thành phần gây lỗi theo nhãn của dataset.
- *MRR* (mean reciprocal rank): trung bình của 1/hạng của root; 1 là luôn đứng đầu.
- *Hit@k*: tỷ lệ ca root nằm trong k vị trí đầu.
- *NDCG@5*, *Avg@5*: độ đo xếp hạng; Avg@5 là trung bình Hit@1…Hit@5, dùng để so với số công bố của RCAEval.
- *Baseline*: phương pháp RCA đã có, dùng để so sánh.

---

## 1. Các phương pháp RCA đã có

*Phần này trả lời nhận xét: "mới khảo sát sơ qua các phương pháp RCA đã có, chưa sâu kỹ thuật của từng phương pháp".*

Em đã đọc bài và mã gốc, chạy tay và kiểm số công bố cho sáu phương pháp xếp hạng và hai bộ phát hiện:

- BARO (đổi điểm thống kê trên metric);
- CIRCA (hồi quy theo đồ thị nhân quả);
- MicroRank (PageRank trên trace);
- TraceRCA (trace bất thường theo tập dịch vụ);
- TORAI (gom cụm mức nghiêm trọng, chịu được thiếu dữ liệu);
- SimpleRCA (bỏ phiếu đơn giản trên metric, trace, log, không dùng đồ thị);
- hai bộ phát hiện: BOCPD và N-Sigma.

Với mỗi phương pháp có hồ sơ cơ chế, giả định và điều kiện thất bại. Trạng thái tái lập số công bố:

- BARO và TORAI bản gốc khớp số của bài.
- Các bản đã sửa đầu vào để chạy trên dataset của em chưa có số công bố để so.

## 2. Thực nghiệm trên nhiều dataset

*Phần này trả lời nhận xét: "mở rộng thực nghiệm ra với các dataset public khác".*

Dataset được chọn theo tiêu chí, không theo tên: có nhãn root, có trace cha–con, nhiều loại lỗi, có ca lỗi lan sang dịch vụ khác, và có ít nhất một bộ độc lập. Mỗi bộ chia dev/test **theo ô** (cặp root × loại lỗi). Test bị khóa tới khi thiết kế phương pháp đã chốt.

| Bộ | Hệ | Vai trò | Số ca test |
|---|---|---|---:|
| RE2-TT (RCAEval) | Train Ticket | Dev 30 ca để thiết kế; test 60 ca | 60 |
| Nezha-OB | Online Boutique | Bộ độc lập; có lỗi mã nguồn | 34 |
| RE3-OB (RCAEval) | Online Boutique, lỗi mã nguồn | Giữ ngoài hoàn toàn, chỉ mở một lần cho bản cuối | 30 |

**Vì sao không dùng Sock Shop và LEMMA-RCA** (cô đã nêu tên):

- *Sock Shop:* các bản RCAEval của Sock Shop không có file trace, chỉ 3–5 root, và phần lớn đã được dùng ở giai đoạn trước. Không ánh xạ trace lên đồ thị được (bước 2 của cô).
- *LEMMA-RCA:* mẫu đã kiểm không có trace; nhãn root chỉ một thực thể mỗi ngày; giấy phép còn mâu thuẫn; dung lượng 53 GB và 33 GB.
- Eadro (Train Ticket, 27 root) đã kiểm nhưng chưa dùng, vì đồng hồ trace và cách ghép trace với mốc tiêm lỗi chưa xác nhận được.

## 3. Hạn chế của các phương pháp đã có

*Phần này trả lời nhận xét: "chỉ ra vấn đề còn tồn đọng, hạn chế của các phương pháp đã có".*

Bản đồ hạn chế có 26 dòng. Mỗi dòng ghi ca nào hỏng, phương pháp nào, cơ chế nào gây ra, và nguồn hạn chế là dữ liệu, bản cài hay giả định của phương pháp. Ba hạn chế dẫn tới thiết kế ở phần 4:

1. **Dịch vụ gọi bị nhầm là nguyên nhân.** Khi dịch vụ gốc chậm, dịch vụ gọi nó phải chờ, nên span của bên gọi cũng dài ra. Các phương pháp chấm theo dịch vụ sở hữu span thì chấm bên gọi.
2. **Trễ mạng nằm ở span phía gọi.** Với lỗi trễ mạng, span của chính root ít thay đổi. Trên Nezha-OB dev, BARO, SimpleRCA, TraceRCA xếp đúng root ở 0, 1, 0 trên 6 ca trễ mạng.
3. **Chuẩn hóa theo IQR suy biến khi nền phẳng** (BARO). Điểm khi đó tính theo đơn vị gốc.

## 4. Phương pháp đồ thị

*Phần này trả lời nhận xét: "tiếp cận phương pháp đồ thị theo 5 bước" — bước 1 và bước 2 của cô; và lời phê "chưa thể hiện rõ liên kết logic".*

**Bước 1 — Mô hình đồ thị phụ thuộc.**

- Nút là dịch vụ. Cạnh là lời gọi quan sát được từ trace.
- Đồ thị tĩnh từ kiến trúc có thêm cạnh dữ liệu và thông điệp. Trace của dataset công khai không cho dựng hai loại cạnh này, nên chúng chỉ kiểm được trên FlashTicket.

**Bước 2 — Phương pháp M1: chuỗi chẩn đoán có đồ thị tham gia.**

| Thành phần | Dùng đồ thị thế nào | Xử lý hạn chế nào |
|---|---|---|
| E1 — thời gian tự xử lý | Quan hệ cha–con của span: trừ thời gian span con khỏi span cha | Hạn chế 1 |
| E2 — bằng chứng trên cạnh | Phần thời gian của lời gọi nằm ngoài span phía nhận, gán cho dịch vụ được gọi | Hạn chế 1, 2 |
| E5 — tách bất thường tự sinh với kế thừa | Theo cạnh có hướng: bất thường của bên gọi được giải thích bởi bên được gọi thì hạ xuống | "Nhầm triệu chứng với nguyên nhân". Đây là phần đồ thị **tham gia phát hiện bất thường** mức thành phần |
| E7 — đồ thị con bất thường | Thành phần liên thông chứa thực thể đứng đầu | Yêu cầu "xác định vùng ảnh hưởng" của đề tài |

**Ba ví dụ thuật toán của cô:**

- *Subgraph anomaly detection:* E7 tạo vùng nghi ngờ. Chưa có quy tắc quyết định riêng cho đồ thị con.
- *PageRank:* PageRank cá nhân hóa được cài nhưng không giữ trong bản cuối, vì phép thử trên dev cho thấy nó làm kết quả kém đi. Có thử làm đối chứng (SimpleRCA + PageRank) trên test: kém SimpleRCA ở hai bộ, hơn ở một bộ.
- *GNN:* chưa làm, vì chưa đủ dữ liệu học không lộ nhãn và chưa thấy hiện tượng mà cách chấm theo từng phần tử bỏ sót.

Thiết kế được chọn trên dev, khóa trước khi mở test.

## 5. Kết quả so sánh

*Phần này trả lời bước 3 và 4 của cô (thử trên dataset công khai; so với RCA cơ sở bằng Precision, Recall, F1, MRR, NDCG) và yêu cầu đề tài "phân tích các trường hợp phương pháp hoạt động hiệu quả hoặc còn hạn chế".*

### 5.1 Kết quả chính

| Vế | RE2-TT MRR | Nezha-OB MRR | RE3-OB MRR | RE2-TT NDCG@5 | Nezha-OB NDCG@5 | RE3-OB NDCG@5 |
|---|---:|---:|---:|---:|---:|---:|
| M1 (đồ thị) | 0,975 | 0,875 | 0,925 | 0,982 | 0,906 | 0,944 |
| M1 bỏ quan hệ (C-a0) | 0,975 | 0,711 | 0,925 | 0,982 | 0,751 | 0,944 |
| SimpleRCA | 0,876 | 0,689 | 0,975 | 0,902 | 0,735 | 0,982 |
| TORAI | 0,931 | không chạy được | 0,544 | 0,942 | — | 0,662 |
| BARO | 0,806 | 0,534 | 0,487 | 0,811 | 0,570 | 0,610 |

So với baseline mạnh nhất của từng bộ:

- **RE2-TT:** M1 hơn TORAI 0,044 MRR, khoảng tin cậy [−0,033; 0,149]. Đạt mức "không thua quá 0,05" đã khai trước; chưa phân biệt được hơn hay kém.
- **Nezha-OB:** M1 hơn SimpleRCA 0,186 MRR. Phép kiểm khai trước (Hit@5) không đạt: chỉ 3 ô có chênh lệch, nên dữ liệu không đủ sức kết luận.
- **RE3-OB (lỗi mã nguồn):** M1 thấp hơn SimpleRCA 0,050 MRR, khoảng tin cậy chứa 0.

**Kết luận trung thực: phương pháp đồ thị chưa hơn rõ baseline mạnh nhất trên bộ nào.**

### 5.2 Đồ thị giúp khi nào, vì sao

**Giúp — Nezha-OB, lỗi trễ mạng.**

- MRR 0,900 so với 0,408 khi bỏ quan hệ, và 0,380 của SimpleRCA (10 ca).
- Khi bỏ quan hệ, ở 8 ca sai thì dịch vụ đứng đầu là **bên gọi trực tiếp** của root. Với M1, loại sai này còn 0 ca.
- Cơ chế: E2 lấy phần thời gian lời gọi nằm ngoài span phía nhận và gán cho dịch vụ được gọi. Đúng hạn chế 2 ở phần 3.

**Không giúp — RE2-TT và RE3-OB.** M1 bằng nhánh bỏ quan hệ. Ở hai bộ này, root thường là dịch vụ có tín hiệu lệch bền nhất của chính nó:

- một quy tắc đếm đơn giản đặt đúng root ở 48/60 ca RE2-TT và 28/30 ca RE3-OB;
- vì vậy quan hệ không còn chỗ để thêm thông tin.

**Hại hoặc yếu.**

- *Root là nút nguồn* (frontend, không có bên gọi): MRR 0,708 so với 0,958 của SimpleRCA (6 ca). E2 không gán được bằng chứng cho nút không có bên gọi.
- *Lỗi mã nguồn:* lỗi hiện ở bên gọi (mã lỗi, log lỗi), không ở chính root.
- *Một thực thể khác có một kênh lệch cực trị nhưng ngắn:* cách xếp theo giá trị lớn nhất đặt nó lên trên root. Điều kiện này có ở 8/14 ca M1 sai, và đã thấy trên dev.

**Phần quan hệ nào có tác dụng.** Phần hơn trên Nezha-OB đến từ việc **dùng quan hệ cha–con của span khi dựng bằng chứng** (E1, E2). Bước xếp hạng trên đồ thị gần như không đổi kết quả:

- M1 gần bằng quy tắc đơn giản "dịch vụ bất thường sớm nhất" trên cùng bằng chứng.
- E5 đổi hạng root ở 2/124 ca: giúp 1 ca, hại 1 ca.

Không có đối chứng đồ thị ngẫu nhiên, nên em không kết luận về lợi ích của cấu trúc phụ thuộc thật.

### 5.3 Phần chưa có

- **Precision, Recall, F1 của phát hiện sự cố:** chưa đo trong đợt này. Phát hiện mức hệ thống dự kiến dùng luật cảnh báo trên FlashTicket. Phép thử trước khi tiêm lỗi cho thấy M1 luôn trả "có nguyên nhân", nên M1 chưa có ngưỡng phát hiện đã hiệu chuẩn.
- **Precision, Recall, F1 của vùng ảnh hưởng:** dataset công khai không có nhãn vùng. Chỉ báo được vùng nghi ngờ có chứa root không: 0,950 (RE2-TT), 0,824 (Nezha-OB), 0,900 (RE3-OB), với cỡ vùng 1,4–3,9 dịch vụ.
- **Bước 5 (LLM diễn giải):** hoãn sau khi RCA chạy được trên FlashTicket.

### 5.4 Tính trung thực của đánh giá

- Test bị khóa tới khi thiết kế chốt. Kết quả đầu của bản khóa được giữ nguyên.
- Có ba chỗ sửa sau khi đã xem test, đã khai và báo riêng:
  - bộ đọc dữ liệu Nezha-OB;
  - một đối chứng phụ;
  - phân tích nguyên nhân ca sai.
- Các đề xuất sửa phương pháp rút ra từ đó sẽ thiết kế trên dữ liệu FlashTicket và kiểm trên lượt FlashTicket mới, không kiểm lại trên dữ liệu đã dùng.

## 6. Hướng tích hợp FlashTicket

*Phần này trả lời phần 2 của hướng dẫn: tích hợp phương pháp vào hệ thống đặt vé.*

- RCA chạy như một dịch vụ riêng, chỉ đọc kho quan sát: trace (Tempo), log (Loki), metric (Prometheus), qua cùng định dạng nội bộ đã dùng cho dataset công khai.
- Lỗi nghiệp vụ của bán vé (ngoại lệ, sai giá trị trả về, thiếu xử lý lỗi) giống RE3 hơn. Vì vậy hệ thống cần ghi:
  - span cho mọi dịch vụ;
  - lỗi ở span của dịch vụ phát sinh;
  - log lỗi có mã lỗi;
  - span hai đầu mỗi lời gọi.
- FlashTicket có cạnh dữ liệu (DB, Redis) và thông điệp (RabbitMQ), nên kiểm được phần cạnh mà dataset công khai thiếu.
- Kịch bản flash sale cho tải tăng đột biến và lỗi lan. Đây là loại dữ liệu mà quy tắc đơn giản có thể thất bại, và là nơi kiểm được đồ thị có giúp không.
- Ứng viên sửa M1 (chưa kiểm):
  - xếp theo độ bền của lệch thay vì giá trị lớn nhất;
  - chuẩn hóa không phụ thuộc đơn vị;
  - kênh lỗi gán theo cạnh gọi.

## 7. Câu hỏi xin cô định hướng

1. Dataset công khai em dùng khá "đơn giản": tín hiệu của chính dịch vụ gốc thường đủ để tìm nó. Em nên tìm thêm dataset khó hơn, hay dồn lực đánh giá trên FlashTicket với lỗi tự tiêm và tải flash sale?
2. Precision/Recall/F1 của phát hiện sự cố: em đánh giá trên FlashTicket (có đoạn bình thường và mốc lỗi do em kiểm soát) thay vì trên dataset công khai, có được không?
3. Việc quyết định "có sự cố hay không" em dùng luật cảnh báo; đồ thị dùng cho phát hiện mức thành phần và chẩn đoán. Cô có muốn đồ thị tham gia cả quyết định báo động không?
4. GNN có cần làm trong đồ án không, khi hiện chưa có căn cứ dữ liệu cho nó?
