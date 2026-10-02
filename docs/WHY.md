# Tại sao chọn X

Mỗi mục trả lời một câu "tại sao" mà cô hoặc hội đồng có thể hỏi. Viết cho người không đọc repo.

Mỗi mục có một trạng thái:
- **Đã quyết:** Minh đã chốt; có mã trong DECISIONS.
- **Đề xuất:** chưa quyết; ghi rõ sẽ quyết ở cổng nào.
- **Chưa quyết:** chưa có đề xuất.

Mẫu một mục: chọn gì → vì sao → đã xét phương án nào → bằng chứng → kết luận nào phụ thuộc vào nó.

## WHY-01. Vì sao làm theo thứ tự: hiểu phương pháp → nhiều dataset → hạn chế → phương pháp đồ thị — Đã quyết (Q-36)

- **Chọn:** đi đúng chuỗi cô viết.
- **Vì sao:** cô phê bản trước "chưa rõ liên kết logic". Thiết kế phương pháp đồ thị phải trả lời được câu "thành phần này để sửa hạn chế nào". Muốn trả lời câu đó thì phải biết các hạn chế trước.
- **Phương án đã xét:**
  - Thiết kế phương pháp đồ thị trước, chạy baseline sau. Đây là cách v1 và v2 đã làm. Hệ quả: phải đi tìm chỗ đồ thị có ích, và lựa chọn thiết kế không có lý do gốc (LESSONS SL1, SL22).
- **Kết luận phụ thuộc:** toàn bộ phần lập luận của báo cáo.

## WHY-02. Vì sao hiểu "graph-based anomaly detection" theo cả nghĩa hẹp lẫn nghĩa rộng — Đã quyết (Q-36)

- **Chọn:** đồ thị tham gia trực tiếp vào điểm bất thường (nghĩa hẹp). Đồng thời, khoanh vùng và xếp hạng cũng chạy trên đồ thị (nghĩa rộng).
- **Vì sao:** Minh quyết chưa hỏi cô (Q-05), nên cách hiểu phải trả lời được cả hai câu cô có thể hỏi: đồ thị phát hiện bất thường ở đâu, và đồ thị giúp khoanh vùng, xếp hạng thế nào. DT18 cũng yêu cầu cả ba đầu ra: vùng ảnh hưởng, dấu hiệu bất thường, xếp hạng nguyên nhân. Trong MicroRCA và MicroRank, PageRank chỉ chạy sau khi đã phát hiện bất thường cục bộ, tức đồ thị không tham gia việc phát hiện (K1 §D.3). Nếu chỉ làm theo nghĩa rộng, câu hỏi "đồ thị phát hiện bất thường ở đâu" không có câu trả lời.
- **Phương án đã xét:**
  - Chỉ nghĩa rộng: phát hiện cục bộ rồi PageRank. Dễ làm hơn, nhưng có rủi ro trên.
  - Hai nghĩa không loại trừ nhau. Nghĩa hẹp chỉ đòi đồ thị tham gia tính điểm bất thường; nó vẫn đi cùng được bộ khoanh vùng và xếp hạng, hoặc học chung như Eadro (K1 §C.7). Vì vậy câu hỏi thật là đồ thị tham gia ở bước nào, không phải chọn một trong hai nghĩa.
- **Chưa kiểm:** khung bốn tầng ở P6 và cơ chế tách bất thường tự sinh khỏi kế thừa chỉ là ứng viên. Cơ chế đó nhắm vào giả thuyết "nhầm triệu chứng với nguyên nhân" của P4; khả năng tách của nó chưa kiểm. Thành phần cụ thể chọn sau P4, theo dữ liệu và hạn chế thực tế. DT18 yêu cầu các đầu ra, không bắt buộc kiến trúc bốn tầng.
- **Kết luận phụ thuộc:** cách tổ chức P6.

## WHY-03. Vì sao chọn dataset theo tiêu chí "phân xử được" — Đã quyết phần chọn theo tiêu chí (Q-03); danh sách cụ thể quyết ở G1

- **Chọn:** tiêu chí ở MRP §4. Đếm trước các con số: số service gốc khác nhau, vị trí của chúng trong đồ thị, có lan truyền hay không.
- **Vì sao:** RE2-TT chỉ có 5 service gốc ở 5 vị trí cố định, và đồ thị gần như giống nhau giữa các ca (LESSONS ST3). Mỗi vị trí chỉ có một service, nên RE2-TT không tách được tác động của vị trí khỏi danh tính service và loại lỗi, và không cho khái quát sang topology khác. Một cách dùng đồ thị có giúp trên 5 vị trí đó không thì vẫn kiểm được, nhưng chưa kiểm ("chưa biết" khác "không được", SL21). Muốn trả lời "đồ thị giúp khi nào" thì cần thêm dataset. v1 đã không đếm các con số này trước khi đặt giả thuyết (SL15).
- **Phương án đã xét:**
  - Dùng đúng ba tên cô nêu. Theo khảo sát cũ, Sock Shop bản RE2 không có trace, và LEMMA-RCA v4 không mô tả trace. Hai bộ này không kiểm được việc ánh xạ trace lên đồ thị. P2 kiểm lại trên file thật.
- **Kết luận phụ thuộc:** RQ1, RQ3.

## WHY-04. Vì sao chia dev/test theo ô và giữ một dataset ngoài thiết kế — Đề xuất (G1)

- **Chọn:**
  - Chia dev/test theo ô (thành phần gốc × loại lỗi).
  - Có ít nhất một dataset không được nhìn khi thiết kế ("nhìn" định nghĩa ở MRP §4: trước G3 chỉ được đọc metadata, schema và đếm nhãn).
- **Vì sao chia theo ô:** chọn cấu hình rồi báo kết quả trên cùng dữ liệu thì số đẹp hơn thực tế. Ba lần lặp của một ô gần như giống nhau, nên phải đi cùng nhau về một phía.
- **Vì sao cần dataset giữ ngoài:** nó kiểm phương pháp có phải chỉ khớp với một hệ không.
- **Phương án đã xét:** chia ngẫu nhiên theo ca. Cách này để lộ đáp án qua các lần lặp của cùng một ô.

## WHY-05. Vì sao chạy baseline bằng code chính thức, bản mới nhất — Đề xuất (G1)

- **Chọn:** code của tác giả hoặc của RCAEval, bản mới nhất (MRP P1 ghi revision). Kiểm tái lập so với số đã công bố. Phần khoa học giữ nguyên; phần giao thức (cách chọn mô hình, cách xử lý ca lỗi) có thể phải đổi, mỗi chỗ đổi ghi lý do (MRP P3).
- **Vì sao:** tự cài lại thì dễ đơn giản hóa đúng chỗ tạo ra giá trị của phương pháp. v1 làm vậy với MicroRCA (SL7). RCAEval cũng đã nhận rằng các baseline PageRank và CIRCA của họ âm thầm trả về thứ tự cột khi lỗi. Bản mới chỉ in thêm cảnh báo; đường trả thứ tự cột vẫn còn, nên adapter của nhóm phải tự đánh dấu ca lỗi (MRP P3). Dùng bản mới không tự bảo đảm số đúng.
- **Phương án đã xét:** dùng lại số công bố mà không chạy. Cách này không so được trên cùng giao thức, và không làm được phân tích từng ca ở P4.

## WHY-06. Vì sao đánh giá ba đầu ra (phát hiện, vùng ảnh hưởng, xếp hạng) bằng các độ đo khác nhau — Đề xuất (G3)

- **Chọn:**
  - Phát hiện: Precision, Recall, F1 theo cửa sổ thời gian.
  - Vùng ảnh hưởng: Precision, Recall, F1 trên tập thành phần.
  - Xếp hạng: MRR, NDCG@5, Hit@k.
- **Vì sao:** DT18 yêu cầu ba đầu ra. Cô nêu năm độ đo. Mỗi độ đo chỉ có nghĩa với một loại đầu ra: Precision, Recall, F1 cần nhãn đúng/sai cho từng đơn vị; MRR và NDCG cần một danh sách xếp hạng và đáp án (K1 §J).
- **Hệ quả cần nói thẳng:**
  - Với một nguyên nhân gốc mỗi ca và nhãn nhị phân, NDCG chỉ là một hàm của thứ hạng, nên không thêm thông tin mới so với MRR. Vẫn báo vì cô yêu cầu.
  - Dataset công khai không có nhãn vùng ảnh hưởng, nên Precision và Recall của vùng chỉ đo được trên FlashTicket.

## WHY-07. Vì sao so với nhánh không đồ thị và với đồ thị ngẫu nhiên giữ bậc — Đề xuất (G3)

- **Chọn:** ngoài baseline, so phương pháp đồ thị với:
  - (a) cùng bằng chứng nhưng không dùng đồ thị;
  - (b) cùng phương pháp trên đồ thị ngẫu nhiên giữ nguyên bậc của từng nút.
- **Vì sao:**
  - (a) tách phần lợi ích do "dùng thêm tín hiệu" khỏi phần lợi ích do "dùng quan hệ". Điều này chỉ đúng khi nhánh (a) bỏ mọi chỗ dùng quan hệ, kể cả đặc trưng tạo từ quan hệ như self-time hay hồi quy theo nút cha. Biên của nhánh (a) chốt trong spec P7 ở G3; nếu chỉ bỏ một bước thì kết luận chỉ nói về bước đó.
  - (b) kiểm lợi ích có đến từ cấu trúc phụ thuộc thật không, hay chỉ do số cạnh mỗi nút. Trên dev v1, đồ thị ngẫu nhiên gây đúng thiệt hại như đồ thị thật ở các ca xấu nhất. Nhờ vậy biết thiệt hại do cách lan truyền, không do cấu trúc (LESSONS ST5).
- Đợt khảo sát cũ không thấy bài RCA nào dùng đối chứng (b). Ý tưởng lấy từ v1 nhưng lý do đứng độc lập.

## WHY-08. Vì sao một lõi RCA chung cho dataset công khai và FlashTicket — Đã quyết (Q-36)

- **Chọn:**
  - Mỗi nguồn dữ liệu có một bộ chuyển đổi về cùng một định dạng nội bộ (span, chuỗi metric, bản ghi log).
  - Một lõi RCA duy nhất đọc định dạng đó.
- **Vì sao:** sản phẩm phải chạy đúng phương pháp đã được đánh giá. Nếu FlashTicket dùng một bản cài khác, kết quả thực nghiệm không nói được gì về sản phẩm.
- **Phương án đã xét:** viết riêng một bản cho sản phẩm. Nhanh hơn lúc đầu, nhưng hai bản sẽ lệch nhau.

## WHY-09. Vì sao giao yêu cầu quan sát cho nhóm hệ thống từ sớm — Đã quyết (Q-36)

- **Chọn:** viết "Yêu cầu quan sát cho RCA" (P9a) song song với P1, P2.
- **Vì sao:**
  - Ba bạn đang dựng FlashTicket ngay bây giờ. Thiếu loại span, thiếu trace_id trong log, hay lấy mẫu trace thấp thì không dựng được cạnh có kiểu, không ánh xạ log lên đồ thị được.
  - Sửa instrumentation sau khi hệ đã xong thì tốn hơn nhiều.
  - Minh đã nói stack có thể đổi theo RCA (Q-06).

## WHY-10. Vì sao chưa quyết dùng GNN — Chưa quyết (G3)

- **Tiêu chí để làm biến thể GNN ở tầng 2 của P6** (cần đủ cả ba):
  1. P4 cho thấy có loại bất thường phụ thuộc ngữ cảnh mà cách chấm thống kê theo từng phần tử bỏ sót.
  2. Có đủ dữ liệu để huấn luyện mà không lộ đáp án. GNN dự báo hành vi bình thường cần đủ dữ liệu bình thường; GNN có giám sát cần nhiều sự cố có nhãn. Các lần lặp của cùng một ô phải ở cùng một phía (WHY-04). Khi dataset có ít service gốc, mô hình có giám sát học được rằng nguyên nhân chỉ nằm trong vài service đó, tức thu hẹp tập ứng viên; phương pháp không giám sát không có lợi thế này, nên so hai loại phải nói rõ. Muốn kiểm khả năng tổng quát sang service gốc hay hệ chưa thấy thì phải chia theo service gốc hoặc theo hệ.
  3. Chạy được trên CPU của laptop 16 GB (Q-25).
- Nếu không đạt thì báo cáo nêu lý do bằng bằng chứng. GNN vẫn được trình bày ở phần khảo sát (P1: Eadro, DéjàVu, GDN).
- Lý do không làm mặc định: "dùng GNN" không phải tiêu chí khoa học (K1 §F). Cài một phương pháp không có câu hỏi nào cần nó trả lời là dấu hiệu đi sai (LESSONS CB6).

## WHY-11. Vì sao repo mới, code mới — Đã quyết (Q-08)

- **Vì sao:** code v1 mang theo các lựa chọn đã sai hoặc chưa kiểm, ví dụ sàn 1e-12 và cạnh nhị phân. Dùng lại code dễ kéo theo khung cũ (LESSONS SL22).
- **Dùng lại dữ liệu thô** sau khi kiểm revision, vì dữ liệu không mang lựa chọn phương pháp.

## WHY-12. Vì sao vai trò gắn theo task, và người phản biện phải khác người làm — Đã quyết (Q-13, thay Q-09)

- **Chọn:** Claude và Codex ngang hàng. Mỗi task ghi người làm và người phản biện; hai người này phải khác nhau. Bên nào hết token thì bên kia nhận tiếp từ LOG của task.
- **Vì sao khác người:** reviewer khác model ít chia điểm mù với người viết (LESSONS QT12).
- **Vì sao không cố định ai làm chính:** usage của mỗi bên có hạn. Cố định một bên làm chính thì công việc dừng mỗi khi bên đó hết lượt.
- Người phản biện chỉ báo lỗi ảnh hưởng tính đúng hoặc độ khớp đề tài; Minh quyết sửa điểm nào. Như vậy tránh vòng "mọi điểm phản biện đều phải sửa" của v1 (SL5).
