# Tại sao chọn X

Mỗi mục trả lời một câu "tại sao" mà cô hoặc hội đồng có thể hỏi. Viết cho người không đọc repo.

Mỗi mục có một trạng thái:
- **Đã quyết:** Minh đã chốt; có mã trong DECISIONS.
- **Đề xuất:** chưa quyết; ghi rõ sẽ quyết ở cổng nào.
- **Chưa quyết:** chưa có đề xuất.

Mẫu một mục: chọn gì → vì sao → đã xét phương án nào → bằng chứng → kết luận nào phụ thuộc vào nó.

## WHY-01. Vì sao làm theo thứ tự: hiểu phương pháp → nhiều dataset → hạn chế → phương pháp đồ thị — Đã quyết (Q-36)

- **Lịch sử:** Q-36 duyệt chuỗi nghiên cứu ngày 02/10/2026. Q-89 bổ sung cách phân biệt căn cứ thiết kế ngày 09/10/2026 để khớp Q-88; không đổi thứ tự gói hoặc mở lại task đã đóng.
- **Chọn:** đi đúng chuỗi cô viết. Thành phần nhằm sửa hạn chế phải nối với bằng chứng P4. Thành phần đáp ứng DT18 hoặc nhu cầu kỹ thuật phải nêu đúng yêu cầu, lý do và phương án khác; không được suy từ sự cần thiết sang hiệu quả.
- **Vì sao:** cô phê bản trước "chưa rõ liên kết logic". Với thành phần nhằm sửa hạn chế, phải biết hạn chế và cơ chế trước khi chọn cách xử lý. DT18 cũng yêu cầu mô hình đồ thị, ánh xạ tín hiệu và các đầu ra phát hiện, vùng ảnh hưởng, xếp hạng; không cần dựng một hạn chế baseline để hợp thức hóa những yêu cầu đó.
- **Ba loại căn cứ:**
  - Sửa hạn chế: chỉ rõ bằng chứng P4, thông tin thành phần bổ sung hoặc giữ lại, giải thích khác và điều kiện thất bại.
  - Đáp ứng DT18: dẫn đúng đoạn yêu cầu; phân biệt yêu cầu đầu ra với cơ chế cụ thể do nhóm chọn.
  - Nhu cầu kỹ thuật: điều kiện để thu, ánh xạ hoặc xử lý đầu vào và triển khai phương pháp đã đặc tả. Ví dụ: dựng đồ thị từ đầu vào, ánh xạ tín hiệu, xử lý trường hợp thiếu tín hiệu. Nêu vì sao cần và phương án khác; xử lý thiếu tín hiệu không mặc nhiên chứng minh khắc phục hạn chế RCA.
- **Phương án đã xét:**
  - Thiết kế phương pháp đồ thị trước, chạy baseline sau. Đây là cách v1 và v2 đã làm. Hệ quả: phải đi tìm chỗ đồ thị có ích, và lựa chọn thiết kế không có lý do gốc (LESSONS SL1, SL22).
  - Buộc mọi thành phần nối với một hạn chế P4: dễ biến yêu cầu đề tài hoặc điều kiện triển khai thành hạn chế baseline chưa có bằng chứng. Phân biệt ba loại căn cứ vẫn phải so phương án và kiểm hành vi trên dev theo MRP §3, P6; không cho phép chọn cơ chế chỉ vì hợp khung có sẵn.
- **Bằng chứng và giới hạn:** DT18-NV2 tại `reference/sources/DT18-de-tai-va-nhiem-vu.md` §2; chuỗi nghiên cứu và năm bước tại `reference/sources/advisor-2026-09-23.md` §1; mức căn cứ tại MRP §3. Đây là căn cứ tổ chức nghiên cứu và yêu cầu thiết kế, không phải bằng chứng một cơ chế đồ thị đã hiệu quả. Hiệu quả và lợi ích do quan hệ thật vẫn phải đánh giá ở P7.
- **Kết luận phụ thuộc:** toàn bộ phần lập luận của báo cáo và căn cứ chọn thành phần ở G2, P5–P6. RQ3 vẫn hỏi phương pháp có khắc phục các hạn chế RQ2 hay không.

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

## WHY-13. Bảo toàn OpenRCA Bank trước G3 — Codex quyết theo ủy quyền Q-47

- Chọn: toàn biến thể Bank và AIOps Bank cùng lineage khi xác minh; chỉ metadata/schema/đếm nhãn trước G3. Chưa chọn dataset thí nghiệm hoặc chia dev/test thay G1.
- Vì sao: miền banking và schema công bố root/time/reason, metric/log/trace làm ứng viên đánh giá ngoài thiết kế; không chọn vì sẵn dữ liệu/code.
- Phương án đã xét: Nezha OB/TT, Eadro SN, DeepTraLog, LEMMA IT, AnoMod/OpenRCA2; trade-off và bằng chứng riêng ở results/T-003/bao-toan-openrca-bank.md và T012 sources run002.
- Chấp nhận chưa biết lúc quyết Q-49: chất lượng số đo, normal/graph/symptom, injector/collector Bank và census nhãn thực. Sau REVIEW đã kiểm metadata/đếm nhãn: 136 ca, 14 root, 8 reason, 9 ngày, 52 ô; nguồn results/T-012/runs/bank-label-reproduce-002/census.json. Không coi đủ tiêu chí9 hoặc bảo đảm dùng được ở G3.
- Kết luận phụ thuộc: khả năng đánh giá ngoài thiết kế G1/G3/RQ3; tiêu chí7 Bank OPEN tới G3. RQ3 trên Bank chỉ bao quát các reason CPU/memory/disk/network/JVM đã có, **không kiểm lỗi mã nguồn**. Không đổi thiết kế theo số đo giữ ngoài sau mở.
- Đính chính R3 (04/10, theo Q-51): lúc chọn, nhãn release của Bank cũng chưa xác minh; thiếu census không phân biệt Bank với AnoMod/OpenRCA2. Căn cứ chọn là miền banking và schema nguồn có root/time/ba nguồn, cùng chấp nhận bất định; không coi chưa kiểm của phương án khác là bằng chứng Bank tốt hơn. Census sau REVIEW không được kể lại như đã có lúc quyết.

## WHY-14. Kiểm nội bộ LEMMA khi nguồn license NC/ND còn khác — thực hiện phạm vi hẹp Q-47

- Chọn: chỉ tải bốn ZIP IT nguyên trạng, kiểm nội bộ phi thương mại, không phân phối payload gốc/phái sinh; không chọn một license thay tác giả.
- Bằng chứng: legalcode chính thức CC BY-NC4 và BY-ND4 §2(a)(1) đều cho reproduce; NC cho adapted phi thương mại, ND cho produce/reproduce adapted nhưng không Share; §2(a)(4) cho technical modifications. Root đã đối chiếu hai trang chính thức https://creativecommons.org/licenses/by-nc/4.0/legalcode.en và https://creativecommons.org/licenses/by-nd/4.0/legalcode.en; snapshots/source report results/T-011/runs/license-terms-001/ và xac-minh-nguon-va-doc-lap.md.
- Vì sao: mâu thuẫn vẫn ảnh hưởng quyền phân phối phái sinh/chọn license cuối, nhưng hai cách khai báo cùng cho hành động hẹp đang cần trong T003. Không suy ND cấm đọc hoặc xử lý nội bộ. Điều kiện phi thương mại áp theo nghiên cứu đề tài hiện tại, không cho triển khai thương mại.
- Phương án khác: dừng toàn kiểm LEMMA chờ tác giả; không cần cho hành động chung được cả hai nguồn cho phép. Chọn NC chỉ vì thuận tiện hoặc PR chưa merge là không hợp lệ.
- Giới hạn: tiêu chí1 license cuối vẫn OPEN; không xác nhận quyền của bên cấp hoặc quyền bên thứ ba; không chia sẻ substantial raw/adapted database, không gọi PR bên ngoài là quyết định tác giả. G1 và công bố dữ liệu phái sinh còn phụ thuộc việc tác giả giải nguồn.

## WHY-15. Vì sao dùng bộ thư viện `py312-pin` cho các phương pháp Python 3.12 — Đã quyết (Minh duyệt 04/10/2026, T-006)

- **Chọn:** RCAEval `259ea41` chế độ `[default]`, cài bằng `uv pip install --exclude-newer 2024-12-22` (ngày nộp bài RCAEval) trên Python 3.12. Bản chính: pandas 2.2.3, numpy 1.26.4, causal-learn 0.1.3.8, scikit-learn 1.6.0, scipy 1.14.1, torch 2.5.1. Cách dựng và danh sách gói: `results/T-006/moi-truong.md`, `results/T-006/runs/freeze-py312-pin.txt`.
- **Vì sao:** ở X1 (T-006), hai bộ thư viện cho kết quả tương đương: cùng khớp mọi mốc loại A (ví dụ cơ bản BARO; `reproduce_baro` 5/5 ô), và cùng điểm ở mọi ô CIRCA torai-OB. Khi hai bộ tương đương, chọn bộ ghim theo LESSONS SL29: gần thời điểm tác giả chạy hơn, ít rủi ro lệch hành vi (pandas 3 đổi copy-on-write và kiểu chuỗi).
- **Phương án đã xét:** `py312` (bản mới nhất ngày 03/10/2026): kết quả như nhau ở mọi phép kiểm X1, nhưng xa thời điểm công bố hơn.
- **Ghi thẳng về luật X1:** luật trong SPEC T-006 không nói mốc loại B có tính hay không. Ở cả hai bộ, CIRCA (mốc loại B) lệch quá 0,02 ở nhiều ô. Minh làm rõ sau khi đã thấy kết quả. Kết quả không phụ thuộc cách hiểu, vì hai bộ giống nhau ở mọi ô (REVIEW T-006 R1; `results/T-006/x1-chot-moi-truong.md`).
- **Giới hạn:** X1 không cho thấy bộ ghim "đúng hơn". Chưa kiểm với MicroRank, TraceRCA (thuộc T-007).
- **Kết luận phụ thuộc:** mọi số BARO, N-Sigma, CIRCA, N-Sigma phát hiện của T-006; E2, E3 của T-007.

## WHY-16. Cấu hình cửa sổ tham chiếu khi so MicroRank, TraceRCA với Bảng 2 bài TORAI — Đề xuất (G1) (Minh duyệt 03/10/2026, T-007; khôi phục 04/10/2026 sau khi bị mất khỏi file)

- Chọn: ±600 s quanh mốc tiêm (`--length 20`) làm cấu hình tham chiếu khi so với số bài TORAI; báo kèm ±300 s (SPEC T-007).
- Vì sao: `main.py` RCAEval đổi mặc định `--length` thành 20 từ commit `61326e5` (27/12/2024), trước bài TORAI (2026); BARO `--length 20` trùng 21/21 ô Bảng 3 bài TORAI (T-006).
- Phương án đã xét: ±300 s theo `docs/TORAI.md` (đó là lệnh chạy chính TORAI, không phải baseline); toàn ca (±720 s), không có bằng chứng.
- Giới hạn: bằng chứng gián tiếp với hai baseline trace; tác giả không công bố bộ đọc trace. Kết quả biến thể không dùng để chọn.
- Kết luận phụ thuộc: kết luận "khớp" của MicroRank và số ô lệch của TraceRCA trong `results/T-007/kiem-dung-dan.md`.

## WHY-17. Các quy ước M4 SimpleRCA của T-017 — Ghi nhận triển khai T017 (Minh duyệt ghi 04/10/2026, Q-55; chưa chốt P3)

Lựa chọn được ghi và khóa trong SPEC trước dev theo hồ sơ phiên T017. WHY chung được ghi sau thực nghiệm từ nháp đã có; không kể lại như đã tồn tại trước lượt chạy. Minh duyệt ghi nhận cách triển khai và giới hạn của T017, không chọn cấu hình baseline/dataset/split/window của P3. Các tham số dưới đây không được chọn theo accuracy hoặc chênh giữa phương pháp đồ thị và không đồ thị.

Chọn một bản cài độc lập của mô tả §3.1.2, đặt tên “SimpleRCA (M4, quy ước T-017)”. Vì sao: ba entrypoint tác giả và lớp SimpleRCA riêng đều dùng luật khác bài; việc gọi tên giống nhau không định danh được code sinh bảng 2. Phương án đã xét: chạy nguyên code nhánh rcaeval hoặc dùng lớp SimpleRCA riêng; đó là các đường code đối chiếu, không thực hiện yêu cầu Q37/Q38 cài theo bài. Không dùng số công bố thay cho triển khai hoặc kiểm đúng đắn. Bằng chứng: doi-chieu-code.md, manifest ba revision và PDF FSE trang5. Kết luận phụ thuộc: mọi số T017 chỉ nói về bản M4 này, chưa tái lập đúng chương trình tác giả.

Metric mặc định dùng mean+3std với ddof0 và upper tail strictly >. Vì sao: bài nêu 3sigma hoặc P95 mà không khóa lựa chọn; 3sigma cho một công thức xác định và không dùng nhãn. Đây không phải thống kê robust trước ngoại lệ dù bài dùng từ robust. Phương án khác P95 đã chạy trên ca ví dụ; không chọn cấu hình theo accuracy. Không lấy trị tuyệt đối vì bài nói exceeds; điểm giảm không tạo alert. Bằng chứng: SPEC khóa trước dev, core.py, unit-tests và sensitivity. Kết luận phụ thuộc: số cảnh báo và thứ hạng M4; chuyển sang P95 hoặc two-sided tạo biến thể khác.

Một giá trị metric vượt ngưỡng là một alert; cộng tất cả điểm trong cửa sổ (events). Trace và log mỗi modality một phiếu/service. Vì sao: diễn giải trực tiếp “current value” và “number of alerts” của bài, không thêm trọng số riêng. Phương án khác mỗi metric một phiếu (channels) cũng phù hợp một cách đọc của bài; đã kiểm riêng. Bài không định nghĩa đơn vị alert hay cách tổng hợp qua thời gian, nên chưa xác nhận events là cách tác giả chạy. Bằng chứng: hai cấu hình trong sensitivity và công thức hồ sơ. Kết luận phụ thuộc: score tăng theo số cột/tần suất/độ dài; không so score thô giữa các dataset. Alert count lớn có thể do persistence hoặc nhiều kênh tương quan, không chỉ do nguyên nhân mạnh.

Trace dùng P95 tuyến tính/service trong từng cửa sổ, một phiếu nếu P95 incident>3P95 normal. Vì sao: đúng mức service và ví dụ3x của bài; không dùng cây span, parent-child hay đồ thị. Phương án khác factor2/4 đã kiểm nhưng không chọn winner. Không đổi đơn vị duration khi lấy ratio vì cùng nguồn/cùng đơn vị; unit vật lý của parquet vẫn OPEN ở T002. Bằng chứng: example score/quantile độc lập và source §3.1.2. Kết luận phụ thuộc: bản này chấm span durations gộp theo service, chưa định danh service latency end-to-end của tác giả khi nhiều operation/span nội bộ.

Log dùng substring ERROR/FAIL/EXCEPTION không phân biệt hoa thường, một count/dòng, một phiếu nếu count>0. Vì sao: 0 là ngưỡng tối thiểu tường minh để kiểm rule; bài không công bố ngưỡng. Đây không bảo đảm “sudden spike” hay false-positive đã hiệu chỉnh. Phương án khác count>1/>10 đã kiểm tổng hợp; trên ca ví dụ thiếu log nên kiểm dữ liệu thực đó không phân xử được log threshold. Kiểm thêm ca thứ hai theo allowlist, có log: ngưỡng0/1/10 cùng một entity nhận phiếu và score/ranking không đổi; count được tính lại độc lập. Bằng chứng: known-answer tests; ca cpu1 thiếu log được giữ; runs/supplement-001/summary.json và runs/supplement-002/summary.json. Kết luận phụ thuộc: thứ hạng M4 có thể tăng do log lỗi nền, từ ghép như failure, hoặc quy mô lưu log; kiểm một ca không xác nhận calibration; G1 cần chốt dùng quy ước nào nếu đưa vào P3.

Cửa sổ ±300s và so riêng ±600s trên ca ví dụ; mốc tiêm chỉ đưa vào adapter biết trước thời điểm. Vì sao: tái dùng cấu hình kiểm T005, không tự chốt độ dài P3 theo Q54. Phương án khác toàn ca hoặc onset tự phát hiện cần giao thức khác; không giả định có detector SimpleRCA vận hành. Bằng chứng: injection-manifest kiểm lại hash nguồn T002, run progress, sensitivity. Kết luận phụ thuộc: số T017 thuộc known-incident mode; không dùng để đo tự phát hiện/độ trễ onset.

Ứng viên là union service quan sát được trong hai cửa sổ; giữ tên mặc định, chỉ alias tường minh từ schema. Vì sao: root có thể chỉ hiện ở một modality; lọc theo root hoặc danh sách service bị tiêm là rò nhãn. Regex pod từng làm nhầm tên database, đã bỏ bằng regression test và rerun004. Phương án khác giao ba modality bỏ mất ứng viên có dữ liệu thiếu; suy tên bằng regex không được chứng minh trên schema. Kết luận phụ thuộc: thứ hạng và denominator service; absent root sau chấm không được lén thêm vào phương pháp. Sau sửa N2 đã duyệt, adapter giữ cả định danh log normal và incident nhưng chỉ đếm message incident; service chỉ log normal có score0. N1 khóa danh tính 30 ca bằng manifest cố định cho runner/bộ lọc, kiểm resolve đúng ca trước đọc. Bằng chứng: runs/fix-n1n2-001/unit-tests.txt và runs/fix-n1n2-001/verification.json; run005 khớp toàn bộ30diagnosis của run004. Không thay tập ứng viên bằng danh sách root khi đánh giá.

Missing channel ghi unavailable; log bảng rỗng là0; normal metric≥2 finite, trace≥1 span/phía; bỏ NaN/inf có counters, không ffill hoặc floor. Vì sao: không chế tạo quan sát và không đưa dữ liệu tương lai backward vào baseline. Phương án ffill hoặc floor làm đổi count/threshold ở constant/missing. Bằng chứng: test missing/std0/negative-duration và counters run004. Kết luận phụ thuộc: min points chỉ là điều kiện tính toán, không bảo đảm ngưỡng ổn định thống kê.

Tie groups giữ đúng score; thứ tự lexical chỉ hiển thị; chấm fractional Hit và expected reciprocal rank trong nhóm hòa, kèm bounds. Allzero abstain. Vì sao: không biến thứ tự cột/tên thành chứng cứ root. Phương án optimistic hoặc pessimistic báo bounds nhưng không dùng chọn cấu hình; paper không nêu tie treatment. Bằng chứng: synthetic ties, output và evaluation separate sau serialize. Kết luận phụ thuộc: không so điểm tie-aware của nhóm trực tiếp với paper khi paper chưa rõ cách xử lý hòa.

Bằng chứng sau sửa N1/N2: `results/T-017/runs/fix-n1n2-001/verification.json`, `results/T-017/runs/fix-n1n2-001/unit-tests.txt`, `results/T-017/runs/fix-n1n2-001/independent-self-test.json`, và `runs/run-dev-005/summary.json`. 25 unittest,13 nhóm tự kiểm độc lập,2.458 so ví dụ đạt;30 diagnosis không đổi. Hai normal-control thực vẫn có điểm dương; không dùng để chứng minh đã hiệu chỉnh false-positive hoặc tìm nguyên nhân có ý nghĩa. Các đường dẫn `runs/...` thuộc `results/T-017/`; lõi và test thuộc `src/simplerca/`; SPEC thuộc `tasks/T-017-simplerca/`. Kết luận G1/P3 còn phụ thuộc quyết định giao thức sau này; chưa tái lập full90 hoặc chương trình sinh bảng2.

Ghi chú 05/10/2026: P3 dùng quy ước này (Q-74), xem WHY-33. Số `results/T-017/runs/run-dev-005/` không dùng lại nguyên trạng vì cửa sổ P3 đòi span kết thúc trước t+300 (WHY-22).

## WHY-18. Lý do của phép chẩn đoán GDN ở T-018 — Ghi nhận (Minh duyệt 04/10/2026, Q-56); không phải cấu hình P3

- **Đã dùng trong T-018:** (1) bộ cột cố định L\* = giao cột của 30 ca dev RE2-TT, chốt từ siêu dữ liệu trước khi nhìn kết quả; (2) ca thiếu cột thì điền trung vị tập học; (3) biến thể chuẩn hóa điểm lệch bằng trung vị/IQR của tập kiểm định thay cho của tập test; (4) dữ liệu học là đoạn trước mốc tiêm của các ca dev (nhãn dev dùng để học).
- **Vì sao:** code GDN chuẩn hóa điểm test bằng thống kê của chính tập test (dữ liệu tương lai) và mặc định chọn ngưỡng theo nhãn test; bộ cột RE2-TT khác nhau giữa các ca và tương quan với service gốc. Các lựa chọn trên là cách không dùng nhãn hay dữ liệu tương lai của ca được chấm.
- **Phương án đã xét:** dùng nguyên code (`report='val'`); bộ cột theo giao ca học và ca test như T-005 (phụ thuộc ca được chấm).
- **Trạng thái:** cách chạy này **chưa đạt**: trên dữ liệu bình thường giữ ngoài vẫn báo động sai 45–100 % số tick. Cấu hình GDN cho P3 chốt sau, khi đã xử lý lệch mức giữa các lượt chạy.
- **Bằng chứng:** `results/T-018/ho-so-gdn.md` mục 7–9; `results/T-018/runs/b6b7-phan-tich.json`; REVIEW T-018 R6.
- **Kết luận phụ thuộc:** các số chẩn đoán GDN của T-018.

## WHY-19. Bản TORAI dùng cho P3: bản sửa hai chỗ trong `src/torai/` — Đề xuất (G1) (T-016; Minh duyệt ghi 04/10/2026)

- **Chọn:** TORAI chính ở P3 là `src/torai/torai_sua.py`: code RCAEval `259ea41` chép nguyên văn, chỉ sửa (A) bỏ lần giảm mẫu metric thứ hai trong `_rcd_multimodal` (`torai.py:29`) và (B) ghép metric với logts theo vị trí trong từng nửa thay cho `concat` theo chỉ số (`torai.py:47-48`). Bản gốc chạy kèm trên torai-OB làm mốc tái lập. Đặt seed theo ca, ít nhất 3 seed. Mỗi lượt báo tỉ lệ cụm rơi nhánh dự phòng và điểm SeverityScorer không cụm.
- **Vì sao:** ở lệnh chính thức (`--length 10`), bản gốc đưa 0 cột metric vào bước nhân quả ở mọi ca OB, SS, TT dev đã thử, trái với bài §3.4 (CausalRanker phân tích chuỗi metric và log). Bản sửa đưa metric vào bước nhân quả như bài mô tả mà không đổi bước nào khác. Nó là bản cài RCAEval đã sửa hai lỗi, chưa tương đương TORAI của bài: gán cụm cứng, bỏ trace trong RCD, trọng số nguồn khác và nhánh dự phòng vẫn còn (`ho-so-torai.md` C4–C7). Lỗi nhiều khả năng do chuyển code: chú thích `torai.py:80` mô tả một lần giảm; `mmnsigma` giảm một lần; `mmrcd` ghép theo thời gian (`results/T-016/giam-mau-hai-lan.md` mục 4).
- **Phương án đã xét:**
  - Bản gốc nguyên trạng: tái lập số công bố, nhưng là "TORAI không có metric trong bước nhân quả"; hạn chế thấy ở P4 có thể chỉ là hệ quả của lỗi.
  - Bản sửa ghép theo thời gian (`merge_asof` như `mmrcd`): cần tự chọn quy tắc làm tròn giữa lưới metric (theo mốc tiêm) và lưới log (theo đầu file, lệch 0–14 s); bài không nêu. Chưa kiểm.
  - Sửa thêm (đưa trace vào RCD, GMM gán mềm, bỏ nhánh dự phòng): là thay đổi phương pháp, không phải sửa lỗi; không làm.
- **Bằng chứng:** `results/T-016/giam-mau-hai-lan.md` mục 3, 5; trung bình 5 seed, Avg@5 bản gốc / bản sửa: OB cửa sổ 10 0,913 / 0,909; OB 20 0,926 / 0,928; SS 10 0,952 / 0,955; SS 20 0,941 / 0,940; TT dev 10 0,880 / 0,880. Hai bản cho cùng điểm trong dao động giữa seed, vì phần lớn cụm rơi nhánh dự phòng ở cả hai (OB cửa sổ 10: 176/184 và 166/184 cụm).
- **Giới hạn:** chọn bản sửa không làm điểm tốt hơn; chỉ sửa hai lỗi đầu vào của bước nhân quả. Kết luận P3, P4 dựa trên bản này nói về bản cài RCAEval đã sửa; quy hạn chế cho TORAI theo bài vẫn OPEN ở các khác biệt C4–C7. Cửa sổ P3 chưa chốt (Q-54). Ghi chú 05/10/2026: cửa sổ P3 đã chốt ở Q-64 và Q-74 Q2, xem WHY-22. Bằng chứng ở mục này dùng `--length 10` của RCAEval, cùng độ dài 300 + 300 s nhưng không cùng cửa sổ thông tin với P3 (lưới 15 s của dữ liệu tác giả lệch mốc; ngưỡng `tracets_lat` toàn file). Nguồn đầu vào TORAI ở P3: WHY-29. Câu trước là trạng thái lúc ghi WHY-19 (04/10/2026), giữ để thấy lịch sử. Cách ghép (B) theo vị trí là một cách hiểu ý tác giả (chưa kiểm cách khác).
- **Kết luận phụ thuộc:** mọi số TORAI ở P3; mọi nhận định ở P4 về bước CausalRanker của TORAI.

## WHY-20. Đặt seed theo ca và số lần chạy cho TORAI, RCD — Đề xuất (G1) (T-016; Minh duyệt ghi 04/10/2026)

- **Chọn:** gọi `np.random.seed(s)` ngay trước mỗi lời gọi phương pháp cho từng ca; TORAI ít nhất 3 seed; RCD số seed tối đa vừa ngân sách Q-40 của dataset đó, tối thiểu 1, và ghi rõ số seed (RCD torai-OB cửa sổ 20 tốn 1,56 giờ/seed, TT khoảng 74 phút/seed, nên 5 seed vượt Q-40); báo trung bình và khoảng; phân tích từng ca dùng mọi seed.
- **Vì sao:** RCAEval không đặt seed (`rcd.py:458`; `torai()` không có tham số seed), nên một lượt `main.py` không lặp lại được. Với seed đặt theo ca, TORAI tất định: cùng seed hai lần, khác `PYTHONHASHSEED`, Linux và Windows đều cho thứ hạng giống hệt 90/90 ca (`results/T-016/ngau-nhien.md` mục 3). Giữa các seed, TORAI đổi thứ hạng ở tới 24/90 ca, top-1 tới 9/90 ca, dù sd Avg@5 ≤ 0,004 (mục 4); RCD dao động lớn hơn nhiều (T-006: 2–6/90 ca trùng thứ hạng giữa các lần).
- **Phương án đã xét:** không đặt seed như RCAEval (không tái lập được); seed 420 cố định như RCD gốc (tái lập được nhưng che dao động); trung bình 5 lần như bài (§4.2) mà không ghi seed (không tái lập được).
- **Kết luận phụ thuộc:** số TORAI, RCD ở P3; phân tích từng ca ở P4.

## WHY-21. Cách chấm dataset cho G1: hai lớp tiêu chí, quyền dùng, ba định nghĩa — Đã quyết (Q-58, Q-59, Q-60)

- **Chọn:** mỗi bộ chỉ phải đạt điều kiện tối thiểu (tải được, quyền dùng cho nghiên cứu, nhãn service gốc, thời điểm lỗi, tín hiệu phương pháp cần). Tiêu chí 5, 6, 7, 9 xét cho cả gói. Tiêu chí 1 hiểu theo Q-59. Mức tiếp xúc, vị trí service gốc và "bộ độc lập" theo ba định nghĩa ở Q-60.
- **Vì sao:** T-020 chấm từng bộ theo đủ 9 tiêu chí rồi kết luận "chưa bộ nào đạt". Không bộ công khai nào đạt hết, nên cách chấm đó loại sạch hoặc không quyết được gì. Câu cần trả lời là cả gói có phủ đủ câu hỏi nghiên cứu không: RE2-TT có nhiều lần lặp nhưng ít service gốc; Eadro-TT có nhiều service gốc; RE3 có lỗi mã nguồn. Về quyền dùng: đây là đồ án không thương mại; Nezha và Eadro được tác giả công bố công khai kèm bài báo để tái lập. Về TX1: v1 đã xem thống kê cả 90 ca RE2-TT, nên đòi test chỉ TX0 sẽ mất toàn bộ test RE2-TT và gần hết test đa tín hiệu. Về vị trí: tính được từ dữ liệu bậc đã có; nhóm "không có trong trace" phục vụ giả thuyết P4 "service gốc không có tín hiệu hoặc không có cạnh". Về độc lập: gần như mọi bộ công khai dùng Jaeger và Prometheus; đọc chặt thì tiêu chí 9 không bộ nào đạt được.
- **Phương án đã xét:** chấm đủ 9 tiêu chí cho từng bộ (T-020); chỉ dùng bộ có giấy phép bằng văn bản (mất Nezha, Eadro; mỗi hệ còn 5 service gốc); test chỉ TX0; vị trí theo kiến trúc khai báo; độc lập theo nghĩa không dùng chung thành phần nào.
- **Bằng chứng:** `tasks/T-020-tong-hop-g1/REVIEW.md` R1–R3 và bảng phản hồi; `docs/MRP.md:120`; `docs/knowledge/K2-du-lieu.md:15–17`; `results/T-020/trung-gian/exposure_ledger/public-census.csv`; `results/T-020/trung-gian/dataset_evidence/independence-axes.csv`; `results/T-009/runs/inspect-004/root-degree-whole-file.json`.
- **Giới hạn:** test có ca TX1 không còn "hoàn toàn chưa nhìn"; báo cáo phải khai báo. Chưa có giấy phép bằng văn bản cho Nezha, Eadro. Vị trí theo trace phụ thuộc độ phủ trace và đồ thị toàn file.
- **Kết luận phụ thuộc:** danh sách dataset, vai trò và cách chia ở G1 (T-021); mọi kết luận RQ1, RQ3 dùng các bộ này.

## WHY-22. Cửa sổ dữ liệu P3 và cách cắt trên từng nguồn — Đã quyết (Q-64, Q-74 Q2)

- **Chọn:** đoạn bình thường N = [t−300 s, t), đoạn sự cố A = [t, t+300 s), theo timestamp, nửa mở; N không chồng lần tiêm trước. Metric theo cột thời gian. Span chỉ vào khi bắt đầu ≥ t−300 và kết thúc < t+300. Log theo thời điểm dòng log. Runner cắt trước; tiền xử lý của tác giả chạy sau, chỉ trên dữ liệu trong cửa sổ. Bên trong cửa sổ, mỗi phương pháp chia N/A theo code tác giả đã kiểm ở P1. CIRCA dùng điểm quan sát thật cuối cùng trước t+300 làm điểm test cuối; đồ thị gọi dựng từ span đã kết thúc trước t. Thiếu dữ liệu thì ghi độ dài thực, không kéo dài cửa sổ. Nezha: chỉ áp cho metric. Eadro: dữ liệu bình thường lấy từ phiên no-fault (chưa kiểm; T-023).
- **Vì sao:** độ dài cửa sổ quyết định bộ nào có đủ dữ liệu bình thường, nên phải chốt cùng gói dataset ở G1. RE2-TT có 720 s trước mốc; Nezha có 482–521 s giữa hai lần tiêm; Eadro không có đoạn bình thường trước tiêm trong phiên. Biên cửa sổ là giới hạn thông tin: kết quả RCA có lúc t+300, nên chỉ dữ liệu đã có lúc đó được vào. Vì vậy span chưa kết thúc bị loại, điểm ngoài cửa sổ không được điền vào biên, và giá trị trước t−300 không được kéo vào bằng `ffill`. Ngoại lệ có khai báo: TORAI nguồn A dùng bin của tác giả phủ tới t+305 và ngưỡng `tracets_lat` tính trên toàn file (WHY-29); BOCPD ở chế độ (b) tiền xử lý trên cả bản ghi nên t̂ chỉ có sau cuối bản ghi (WHY-34). Các nhánh này chỉ có kết quả sau cuối file; chúng là hồi cứu, không cùng giới hạn thông tin t+300 / t̂+300 với các nhánh khác.
- **Phương án đã xét:** ±600 s (`--length 20`, cấu hình so mốc bài TORAI, WHY-16): không đủ nền ở Nezha. Toàn bản ghi: chỉ có ở RE2. Cắt theo số dòng như `main.py`: sai nghĩa khi dữ liệu có lỗ hoặc nhịp khác 1 s. Lọc span theo thời điểm bắt đầu: nhận span chưa kết thúc lúc t+300. Giữ thứ tự `main.py` (ffill toàn file rồi cắt): ô trống đầu cửa sổ nhận giá trị trước t−300. CIRCA `current = t+300`: điểm test cuối là giá trị điền, không quan sát.
- **Bằng chứng:** `results/T-021/goi-g1.md` §6 câu 2; `results/T-022/runs/allowlist-001/kiem-allowlist.json` (30/30 ca dev RE2-TT có mốc ở giây 720); RCAEval `259ea41` `main.py:308–315`, `RCAEval/classes/data.py:89–104`; `src/circa_kien_truc/scoring.py:38`; `tasks/T-022-giao-thuc-p3/REVIEW.md` (phản biện giao thức, điểm 1 và Q2).
- **Giới hạn:** cùng 300 + 300 s không có nghĩa cùng thông tin với `main.py --length 10` hay với cấu hình T-006 đã tái lập: khác thứ tự `ffill`, điểm cuối của CIRCA, lưới 15 s của dữ liệu TORAI tác giả. Kết quả nhạy với độ dài nền: trên 25 ca fse-OB DELAY, nền 300 → 360 dòng làm Avg@5 BARO giảm 0,224 (`results/T-013/cua-so-va-che-do-b.md:18`); không chọn cửa sổ theo phân tích đó. MicroRank khớp mốc bài ở ±600 s (T-007), nên số MicroRank, TraceRCA P3 không so trực tiếp với Bảng 2 bài TORAI.
- **Kết luận phụ thuộc:** mọi số P3 chế độ (a); cửa sổ RCA quanh báo động ở chế độ (b) (WHY-35); WHY-19 (ghi chú dưới).

## WHY-23. Báo Retrieval@K và Rerank@1 — Đã quyết (Q-65, Q-74 Q10)

- **Chọn:** với mọi phương pháp RCA, báo Retrieval@K (service gốc nằm trong K thực thể đầu) và Rerank@1 = AC@1 / Retrieval@K, K ∈ {5, 10}. Bảng chính tính hai độ đo này theo cùng quy tắc hòa với mọi độ đo khác (WHY-28). Bảng RCAEval riêng gọi `Evaluator.retrieval_service` và `rerank_service` của RCAEval `259ea41` (`RCAEval/benchmark/evaluation.py:162–210`) với `max_k = 10`, trên thứ tự gốc của phương pháp; ca không `OK` nạp danh sách rỗng.
- **Vì sao:** Hit@1 không cho biết root ở gần đầu hay ở xa. Retrieval@K và Rerank@1 tách hai trường hợp trên danh sách cuối: root nằm ngoài K thực thể đầu, và root nằm trong K đầu nhưng không đứng đầu (bài DecompRCA). Với phương pháp chỉ trả một thứ hạng, chính bài DecompRCA lấy tập ứng viên là K phần tử đầu (`results/T-018/decomprca.md:16`), nên "không truy hồi" ở đây là quy ước định nghĩa trên thứ hạng cuối, không chỉ ra bước nào của phương pháp hỏng. Muốn quy về bước, dùng bốn tập của WHY-26: root ngoài tập quan sát (đầu vào không có tín hiệu của root); trong tập quan sát nhưng không được trả về; được trả về nhưng hạng > K (lỗi ở điểm hoặc thứ tự). Tính từ thứ hạng đã có, không tốn chạy thêm. Bảng RCAEval giữ đúng hàm mà Q-65 chỉ định và cho phép so với số công bố.
- **Phương án đã xét:** định nghĩa theo K metric như Bảng 1 DecompRCA: với hệ ít service, bộ chọn ngẫu nhiên 15 metric đã trúng 0,82–0,90 (RE1-OB, RE1-SS), nên mức trần chủ yếu do cấu trúc. Không báo: mất phép tách. Chỉ dùng hàm RCAEval cho bảng chính: hàm không xử lý hòa, nên thứ tự cột thành bằng chứng.
- **Bằng chứng:** `results/T-018/decomprca.md` mục 3–4; `results/T-018/runs/b9-retrieval-ngau-nhien.json`; `results/T-021/goi-g1.md` §6 câu 3.
- **Giới hạn:** ở mức thực thể với một root, Retrieval@K = Hit@K và Rerank@1 là tỉ số gộp của hai tỉ lệ (`evaluation.py:203–210`); đây là cách trình bày khác của cùng thứ hạng, không phải bằng chứng độc lập (WHY-06). `Evaluator` mặc định `max_k = 5` trả `None` cho K = 10 (`evaluation.py:9`). `main.py:552–553` bỏ ca lỗi khỏi mẫu; bảng RCAEval của P3 không bỏ.
- **Kết luận phụ thuộc:** mô tả ở P4 root nằm ngoài K đầu hay trong K đầu nhưng không đứng đầu của danh sách cuối. Việc quy hạn chế về một bước của phương pháp dựa trên bốn tập (WHY-26) và giá trị trung gian đã lưu, không dựa riêng trên Retrieval/Rerank.

## WHY-24. Mốc tiêm ở chế độ (a) và ngân sách nhãn — Đã quyết (Q-66)

- **Chọn:** ở chế độ (a), mốc tiêm là thông tin vận hành biết trước, chỉ runner chế độ (a) đọc. Chỉ service gốc và loại lỗi là nhãn chấm. Ngân sách nhãn root của mọi baseline bằng 0: không học, không chọn cấu hình, không chọn ca bằng nhãn root. Kết quả chế độ (a) luôn báo cạnh chế độ (b).
- **Vì sao:** trong RCAEval, bản code P1 đã kiểm, mọi baseline tầng 1 nhận mốc tiêm (`main.py:311–315`); bài BARO báo riêng các dòng `[t_inject]`; RCAEval chạy TORAI bằng mốc tiêm thay `t̂_A` (`results/T-016/ho-so-torai.md:35`). Bỏ chế độ (a) thì không so được với số công bố. MicroRank bài gốc có bộ phát hiện trace riêng; bản P3 là bản RCAEval sửa đầu vào, nhận mốc tiêm. Không baseline nào trong Q-38 học từ nhãn root.
- **Phương án đã xét:** chỉ chạy chế độ (b): mất phép so với bài gốc, không tách được lỗi phát hiện khỏi lỗi xếp hạng.
- **Giới hạn:** chế độ (a) dễ hơn thực tế vì biết đúng lúc lỗi bắt đầu. Mốc tiêm không phải lúc biểu hiện. Ở chế độ (b), mọi đường suy ra mốc (tên ca, đường dẫn, file nhãn, cắt quanh mốc) bị cấm (luật cứng 6).
- **Bằng chứng:** `results/T-021/goi-g1.md` §6 câu 4; MRP §4, P3; `results/T-013/ho-so-baro.md` §1, §8.
- **Kết luận phụ thuộc:** cách đọc mọi số chế độ (a); tách nhãn chấm khỏi đầu vào phương pháp trong mọi adapter P3.

## WHY-25. Tập cột BOCPD và chạy qua đêm — Đã quyết (Q-67, Q-72)

- **Chọn:** BOCPD dùng **tập cột** theo `reproduce_bocpd`: tên chứa `latency-50` hoặc `_error`, bỏ `queue-master` và `rabbitmq_` (BARO `e35f4ec`, `baro/reproducibility.py:140–145`). Q-67 chỉ chọn tập cột, không chọn cách cắt 300 + 300 quanh mốc của hàm đó. Q-72: BOCPD chế độ (b) trên RE2-TT dev chạy qua đêm trên EC2 ở T-025, tối đa 20 giờ, đầu vào không chọn theo mốc tiêm, ghi tiến độ từng ca, giữ lượt hỏng; kết luận chi phí ghi cho bản cài BARO, không cho thuật toán BOCPD.
- **Vì sao:** đây là quy ước tác giả dùng khi báo kết quả phát hiện. Hàm `bocpd()` tự chọn mọi cột chứa `latency` và `_error`; ở T-005 nó chọn 76 cột và mất 1.440 s cho 600 điểm; cả ca 1.441 điểm không xong trong 1 giờ. Chi phí xấp xỉ O(T²d³) (`results/T-013/ho-so-bocpd.md` §9), nên giảm số cột theo đúng tác giả là cách giảm chi phí. Q-40 giới hạn 3 giờ cho toàn ca một dataset; Q-72 là ngoại lệ riêng cho BOCPD.
- **Phương án đã xét:** báo "không chạy đủ trong ngân sách" (áp cho CIRCA-PC ở Q-67); chạy một mẫu ca; cắt quanh mốc như `reproduce_bocpd` (cấm ở chế độ b, luật cứng 6); giữ 76 cột của `bocpd()`.
- **Giới hạn:** trên RE2-TT dev, tập cột này có 25–48 cột thô mỗi ca; số cột `_error` 3–20 và đổi theo ca (`results/T-022/cot-bocpd-dev.csv`). Sự có mặt cột `_error` tương quan với service gốc (`results/T-018/dinh-chinh-task-cu.md`, D1). Vậy số chiều đầu vào, chi phí và độ nhạy của BOCPD đổi theo lỗi. Tập cột và bước bỏ cột hằng dùng cả bản ghi, nên ở chế độ (b) đây là thông tin hồi cứu; chạy riêng từng ca không loại được ảnh hưởng này. Chi phí trên 1.441 điểm với tập cột này **chưa đo**; ngoại suy từ cấu hình cũ (≈ 69 giờ cho 30 ca) không áp cho cấu hình này.
- **Bằng chứng:** `results/T-005/do-kha-thi.md` bảng 2b; `results/T-013/trung-gian/chi-phi-va-sentinel.json`; `results/T-021/goi-g1.md` §6 câu 5; DECISIONS Q-67, Q-72.
- **Kết luận phụ thuộc:** mọi số phát hiện BOCPD P3; lịch và chi phí T-025.
- **Ghi chú 06/10/2026 (Q-79):** bỏ trần 20 giờ cho BOCPD ở T-025 trên EC2; các điều kiện khác của Q-72 giữ nguyên.

## WHY-26. Tập ứng viên, ánh xạ thực thể và bốn tập báo cáo — Đã quyết (Q-74 Q4)

- **Chọn:** chấm ở mức thực thể (service hoặc thành phần như DB). Universe U = 68 thực thể `ts-*` của RE2-TT, chốt từ metadata 30 ca dev, không từ nhãn: 41 `-service`, 26 DB, `ts-ui-dashboard`. Ánh xạ: metric → tiền tố trước `_` đầu tiên; span → `serviceName`; TORAI → `<service>_A`; bỏ trùng giữ lần đầu. Báo riêng bốn tập: inventory (U), tập quan sát của phương pháp, tập chấm (U), tập trả về (gồm cả thực thể ngoài U, đếm riêng). Phương pháp không có bằng chứng cho một thực thể thì không xếp nó; không điền phần thiếu. Mức ngẫu nhiên tính trên tập quan sát của phương pháp, kèm trên U.
- **Vì sao:** DT18 coi nút là "dịch vụ hoặc thành phần hệ thống"; RCAEval và TORAI xếp cả DB. Điền phần thiếu cho phương pháp điểm nhờ may. Mức ngẫu nhiên đúng phải dựa trên các thực thể phương pháp thật sự xếp; RCAEval cũng đếm ứng viên sau tiền xử lý (`main.py:322–329`).
- **Phương án đã xét:** chỉ `-service` (lệch RCAEval, TORAI); gộp DB vào service chủ (chưa có bảng sở hữu từ kiến trúc); điền ngẫu nhiên phần thiếu; mức ngẫu nhiên trên U (sai khi phương pháp chỉ thấy một phần U).
- **Bằng chứng:** `results/T-022/mappings/universe-re2tt-dev.json`, `runs/universe-001/`; `results/T-015/bang-ung-vien-tt.csv` (3 ca: 27 thực thể có trace trong ±600 s).
- **Giới hạn:** phương pháp trace chỉ thấy phần U có trace; trần coverage thấp không phải bằng chứng các thực thể vắng là vô can.
- **Kết luận phụ thuộc:** mọi độ đo xếp hạng; trần coverage MicroRank, TraceRCA.

## WHY-27. Bộ cột metric — Đã quyết (Q-74 Q5)

- **Chọn:** mỗi ca dùng cột có trong file của ca, qua tiền xử lý của từng phương pháp. Không bỏ cột `_error`. Không điền cột vắng. Không chạy bộ cột cố định L\*. Evaluator ghi audit số cột và cột vắng; P4 kiểm ảnh hưởng của schema.
- **Vì sao:** bỏ cột `_error` làm yếu baseline (LESSONS QT7). L\* (giao cột 30 ca dev, T-018) bỏ 23/25 cột `_error`, nên chênh giữa bản dùng cột trong file và L\* trộn hiệu ứng schema với việc mất tín hiệu lỗi; phép so đó không tách được hai phần.
- **Phương án đã xét:** hợp cố định, cột vắng điền NaN/0; giao cố định L\*; đối chứng L\* chạy kèm (đề xuất của phản biện; không chọn vì lý do trên).
- **Bằng chứng:** `results/T-018/dinh-chinh-task-cu.md` D1; `results/T-018/ho-so-gdn.md`; REVIEW T-022 (phản biện giao thức, điểm 6, Q5).
- **Giới hạn:** schema là một kênh thông tin. Số và loại cột đổi theo ca và tương quan root; nó đổi số alert SimpleRCA (WHY-17), số chiều BOCPD (WHY-25), tập ứng viên BARO, đồ thị metric CIRCA. Chạy riêng từng ca chỉ loại đường học xuyên ca, không loại ảnh hưởng này. Ở chế độ (a), cột bị bỏ vì hằng trong cửa sổ được xác định từ dữ liệu có sẵn lúc t+300.
- **Kết luận phụ thuộc:** BARO, CIRCA, TORAI, SimpleRCA, BOCPD, N-Sigma; mọi nhận định P4 có thể do schema.

## WHY-28. Chấm xếp hạng: trạng thái lỗi, một quy tắc hòa, bootstrap theo cặp ô — Đã quyết (Q-74 Q9, Q10)

- **Chọn:**
  - Trạng thái mỗi lượt: `OK` (danh sách khác rỗng); `NO_EVIDENCE` (phương pháp trả về bình thường với danh sách rỗng, giữ status gốc); `ERROR` (phương pháp ném ngoại lệ, giữ thông điệp; hoặc đầu ra vi phạm điều kiện hợp lệ đã khai trước: posterior BOCPD không hữu hạn, WHY-34); `TIMEOUT` (vượt giới hạn mỗi lượt khai trong SPEC của task chạy, trước khi chạy); `UNSUPPORTED`. Mọi trạng thái khác `OK` ở mẫu số, tính trượt. Ngân sách tổng (Q-40, Q-72): phép chiếu pilot vượt ngân sách thì quyết trước khi chạy, như Q-67 ("không chạy đủ trong ngân sách", không báo số); đã cam kết chạy đủ cohort mà hết ngân sách giữa chừng thì ca chưa chạy là `TIMEOUT`. Lỗi dữ liệu và lỗi runner sửa trước bảng khoa học, giữ lượt hỏng.
  - Hòa: hai phần tử hòa khi khóa xếp hạng thật của phương pháp bằng nhau. Khóa: BARO max robust z (tính lại bằng đúng lời gọi của hàm, phải ra đúng thứ tự chính thức); SimpleRCA, MicroRank điểm trong đầu ra; TraceRCA `ji` (WHY-32); CIRCA DA `(score, −index, z-score)`, RHT-only `score`; TORAI khóa hai cấp: khối là cụm (khóa = điểm cụm), trong khối là thứ tự RCD hoặc `y_train` ở nhánh dự phòng; dựng lại từ biến cục bộ, nối khối theo đúng code và phải ra đúng thứ tự chính thức. Các cụm cùng điểm chỉ hoán vị cả khối, giữ thứ tự trong khối; kỳ vọng tính chính xác trên các hoán vị khối (`giao-thuc-v2.md` §8.4), không coi mọi service của các cụm đó là một nhóm hòa. Mọi độ đo của bảng chính (MRR, NDCG@5, Hit@1/3/5, Avg@5, Retrieval@5/10, Rerank@1) tính kỳ vọng khi thứ tự trong nhóm hòa ngẫu nhiên đều. Cận lạc quan và bi quan (root ở hạng nhỏ nhất, lớn nhất) chỉ báo cho độ đo đơn điệu theo hạng root (Hit@k, MRR, NDCG@5, Avg@5, Retrieval@K). Rerank@1 là tỉ số gộp, mẫu số đổi theo hạng nên không đơn điệu (`giao-thuc-v2.md` §8.4 có phản ví dụ): chỉ báo giá trị chính và bootstrap. Root vắng → 0.
  - Bảng RCAEval riêng (WHY-23) trên thứ tự gốc.
  - Bootstrap: lấy lại 10 ô dev (root × loại lỗi) có hoàn lại, mỗi ô mang cả 3 ca; B = 10.000; seed 20261005; khoảng phân vị 95 %. So hai phương pháp thì dùng cùng mẫu lấy lại. Phương pháp nhiều seed: trung bình theo seed của từng ca trước. Mẫu có Retrieval = 0 thì Rerank là N/A, đếm số mẫu N/A.
  - Báo theo loại lỗi, ô, nhóm vị trí root và từng ca; số ca theo trạng thái.
- **Vì sao:** hai quy tắc hòa cho hai độ đo khác nhau trên cùng thứ hạng (hai thực thể cùng điểm, root đứng trước theo tên: Hit@1 kỳ vọng 0,5, AC@1 theo tên 1). Phá hòa theo tên hay thứ tự cột biến chúng thành bằng chứng (MRP P3). Điểm vô hướng bằng nhau chưa chắc là hòa khi phương pháp sắp theo khóa nhiều thành phần (CIRCA DA). TORAI nối trọn từng khối cụm (`src/torai/torai_sua.py:296–360`), nên hòa điểm cụm chỉ cho phép đổi chỗ cả khối: hai khối cùng điểm AB, CD với root A cho E[RR] = 2/3; coi bốn service là một nhóm hòa cho 25/48 (REVIEW T-022, V2-R2). Bỏ ca lỗi khỏi mẫu như `main.py:552–553` làm số đẹp hơn thật. Ba lần lặp của một ô gần như giống nhau, nên lấy mẫu theo ô (WHY-04, MRP P7); ghép cặp vì khác biệt giữa hai phương pháp mới là đại lượng cần khoảng.
- **Phương án đã xét:** kỳ vọng cho Hit/RR/DCG nhưng phá hòa theo tên cho hàm RCAEval (bản 1, mâu thuẫn); coi phương pháp chỉ trả thứ tự là không hòa (giữ thứ tự cột làm bằng chứng); TORAI coi mọi service của các cụm cùng điểm là một nhóm hòa, hoặc sắp phẳng theo tuple (trái cách code nối khối); bỏ ca lỗi khỏi mẫu; bootstrap theo ca; bootstrap không ghép cặp.
- **Bằng chứng:** REVIEW T-022 (phản biện giao thức, điểm 4, Q9, Q10); `RCAEval/graph_heads/rht.py:285`; `src/circa_kien_truc/scoring.py:66–68`; `RCAEval/e2e/baro.py:52–55`; `src/torai/torai_sua.py:286–366`; WHY-17 (quy ước hòa của SimpleRCA).
- **Giới hạn:** 10 cụm là ít; khoảng phân vị có thể hẹp hơn thực, và chỉ nói về tập ô này. Hòa bên trong bước RCD của TORAI chưa kiểm.
- **Kết luận phụ thuộc:** mọi bảng xếp hạng P3, P7.

## WHY-29. Nguồn đầu vào TORAI: chạy cả dữ liệu tác giả và bản tự dựng — Đã quyết (Q-74 Q3)

- **Chọn:** chạy TORAI bản sửa (WHY-19) trên hai nguồn. A: `logts.csv`, `tracets_err.csv`, `tracets_lat.csv` của tác giả (torai-TT). B: tự dựng từ parquet RE2 trên lưới 15 s gốc ở t−300 (20 bin mỗi phía); tên cột trace theo luật TT ở `giao-thuc-v2.md` §6.6 (operation chuẩn hóa; span chỉ có tên phương thức HTTP gán cho service của span con); `tracets_lat` học ngưỡng μ + 3σ trên span đã kết thúc trước t; `logts` bằng Drain riêng mỗi service (drain3 0.9.11, ngưỡng 0,4) học trên log trong cửa sổ. B làm dòng chính nếu qua cả ba phép kiểm khai báo trước, không dùng nhãn; không qua thì A làm dòng chính, ghi lệch lưới và ngưỡng toàn file. Không đổi sau khi thấy số.
  - K-B1: dựng `tracets_err`, `tracets_lat` theo quy ước tác giả (lưới của file tác giả, ngưỡng toàn file) và luật tên cột TT cho 30 ca dev; so với file tác giả theo đúng tên cột (cột, bin), không gộp về service; mọi ô của cột không ghép được tính là sai; ≥ 95 % ô trùng cho từng chuỗi, gộp 30 ca (như S9 của T-016). Thử tối đa 3 cách dựng, giữ mọi lần thử, chỉ so với file tác giả, chưa chạy TORAI. Luật tên cột sai ở ca khác mà không sửa được thì K-B1 để OPEN và trình Minh.
  - K-B2: tổng đếm mỗi service trong `logts` B bằng số dòng log của service đó trong cửa sổ, ở cả 30 ca.
  - K-B3: TORAI sửa chạy trên B ở 30 ca × 3 seed không lỗi.
- **Vì sao:** A không nhận cùng cửa sổ thông tin với các phương pháp khác: ở ca `re2tt_ts-auth-service_cpu_1`, lưới tác giả lệch 10 s so với đầu file, nên N phủ [t−295, t+5) và A phủ [t+5, t+305); ngưỡng `tracets_lat` tính trên toàn file, gồm sau mốc. B cùng nguồn và cùng cửa sổ với các phương pháp khác, nhưng là đầu vào khác tác giả và chưa kiểm trên TT. Phép kiểm khai báo trước, không nhìn kết quả xếp hạng. K-B1 cho biết phần trace của B (tên cột, gán service, đếm theo bin) có khớp file tác giả hay không khi dựng theo cùng quy ước; nó không kiểm `logts` (K-B2 chỉ kiểm tổng log tự nhất quán) và không kiểm lưới, ngưỡng riêng của B. K-B1 phải so theo cột vì TORAI tính z từng cột, chia tổng cả nguồn rồi mới cộng theo service (`src/torai/torai_sua.py:176–200, 206–235`); tổng (service, bin) trùng vẫn có thể cho điểm khác (REVIEW T-022, V2-R1). Ngưỡng 95 % và cách so theo tên cột lấy từ tiêu chí S9 của T-016 (`tasks/T-016-ho-so-torai/SPEC.md:95`).
- **Phương án đã xét:** chỉ A (đúng dữ liệu tác giả, lệch cửa sổ); chỉ B làm chính không điều kiện (đề xuất của phản biện; B chưa kiểm trên TT); A chính, B kiểm độ nhạy (bản 1).
- **Bằng chứng:** `results/T-016/dung-logts-tracets.md` §3–5 (đặc tả `tracets` khớp 100 % / 99,75 % trên OB; `logts` tốt nhất 50,2 % ô); LOG T-022 phiên 1 (20:25); REVIEW T-022 (phản biện giao thức, điểm 1, Q3); header `tracets_err.csv` của torai-TT (tên cột TT khác quy tắc OB); luật tên cột TT cho 157/157 tên cột ở ca dev `re2tt_ts-auth-service_cpu_1` (LOG T-022 phiên 4).
- **Giới hạn:** `logts` B khác tác giả (mốc thời gian log và cấu hình Drain chưa biết). Ca `re2tt_ts-auth-service_cpu_1` không có log parquet nhưng file tác giả có 223.924 lượt log; A và B nhận bằng chứng log khác nhau ở ca này. Lệch lưới A mới kiểm ở 1/30 ca. Luật tên cột TT mới kiểm tên ở 1/30 ca, chưa so giá trị ô. Ở Nezha, Eadro chỉ dựng được kiểu B.
- **Kết luận phụ thuộc:** mọi số TORAI P3; so TORAI với SimpleRCA (cùng dùng log); TORAI ở chế độ (b).

## WHY-30. CIRCA đồ thị kiến trúc ở P3 — Đã quyết (Q-74 Q6)

- **Chọn:** scorer RHT + DA (θ = 3), báo kèm RHT-only cùng lượt. Mô hình hồi quy khóa trước khi chạy evaluator: `ANMRegressor(regressor=SVR(kernel="sigmoid"))` như thực nghiệm bài nếu qua bốn phép kiểm không dùng nhãn, không thì LinearRegression. Bốn phép kiểm: (1) đúng cấu hình bài, gọi qua lớp RCAEval `RHTScorer(regressor=…)`, không sửa code; (2) 30/30 ca dev chạy không ném lỗi, mọi z hữu hạn, và không nút có cha hiệu lực nào rơi về z-score sau `ValueError` (ghi route từng nút: không cha, hồi quy thành công, `value_error_fallback`); (3) chạy hai lần cho đầu ra giống hệt; (4) tổng 30 ca ≤ 3 giờ (Q-40). Tên trong bảng: "CIRCA kiến trúc, SVR(sigmoid)+RHT+DA, cấu hình P3" hoặc "…, OLS+RHT+DA, cấu hình P3". Đồ thị gọi dựng từ span có thời điểm bắt đầu ≥ t−300 và kết thúc < t. Giữ metric cô lập làm ứng viên không cha. Điểm test cuối là điểm quan sát thật cuối cùng trước t+300. Builder chạy với `PYTHONHASHSEED=0`; dựng lại với hash seed 1, 2 ở 30 ca để đo độ nhạy (đếm ca đổi cạnh và đổi thứ hạng DA), không chọn seed theo kết quả.
- **Vì sao:** CIRCA theo bài là RHT + DA; thực nghiệm bài dùng SVR(sigmoid) (`CIRCA/circa/experiment/comparison/models.py:583–586`). "Đã kiểm" không chứng minh OLS là bản mạnh nhất, nhưng chọn mô hình bằng accuracy dev là dùng nhãn root (Q-66); phép kiểm không dùng nhãn chỉ trả lời "SVR có chạy đúng và đủ ngân sách không". Đồ thị chỉ từ span đã kết thúc trước mốc để không chứa cạnh do sự cố tạo ra. Builder nhạy với hash seed: seed 1 đổi cạnh ở 24 ca có call/meta graph chu trình.
- **Phương án đã xét:** OLS + RHT-only (khớp RCAEval CIRCA-PC, không phải CIRCA của bài); OLS + RHT + DA không xét SVR; chọn SVR hay OLS theo accuracy dev (cấm); coverage gốc (mất metric im lặng); đồ thị từ trace N∪A.
- **Bằng chứng:** `results/T-014/ho-so-circa-kien-truc.md:107–117, 148–150`; `results/T-014/dinh-chinh-task-cu.md:45–49`; `RCAEval/graph_heads/rht.py:133–164, 285`; REVIEW T-022 (phản biện giao thức, điểm 6, Q6).
- **Giới hạn:** T-014 đã thấy số SVR trên 25 ca MEM fse-OB (`results/T-014/ho-so-circa-pc.md:141`); số đó không được dùng làm căn cứ chọn. Cửa sổ RHT 1 s khác ý nghĩa thời gian của bài (1 phút). 300 s trace có thể thiếu cạnh ít lưu lượng so với 720 s của T-014; ghi số cạnh. Metric graph là DAG ở 30/30 ca, nhưng điều đó không chứng minh cấu trúc đúng giả định nhân quả của tác giả. RHT bắt `ValueError` của hồi quy rồi dùng z-score trực tiếp, không báo lỗi (`RCAEval/graph_heads/rht.py:118–124`); đường này có ở cả SVR và OLS, nên đầu ra hữu hạn không chứng minh hồi quy đã chạy. Vì vậy ghi route từng nút cho mô hình được khóa (như `src/circa_kien_truc/scoring.py:44–57`) và báo số nút rơi về z-score cạnh bảng CIRCA; lỗi do đầu vào NaN/inf xảy ra như nhau với OLS (REVIEW T-022, V2-T1). Số nút này trên 30 ca TT chưa kiểm.
- **Kết luận phụ thuộc:** mọi số CIRCA P3; mọi nhận định "đồ thị kiến trúc giúp hay không" ở P4.
- **Ghi chú 06/10/2026 (T-031):** Đổi mô hình khóa sang OLS (LinearRegression, mặc định RCAEval); SVR báo làm cấu hình phụ. Quyết định trước mọi lượt evaluator, không dùng nhãn (Q-80). Lý do: K-SVR1–4 đạt nhưng chẩn đoán không dùng nhãn cho thấy SVR(sigmoid) với tham số mặc định gần như không hồi quy trên metric RE2-TT: dự đoán gần hằng ở 89–105 nút mỗi ca pilot (`chan-doan-svr.json`). Nguyên nhân có hai phần, chưa tách định lượng: kernel tanh bão hòa khi đầu vào chưa chuẩn hóa (|γ·xxᵀ| trung vị 4–7), và `epsilon = 0,1` của SVR quá rộng so với thang y. Phép thử chuẩn hóa X, y (chỉ để chẩn đoán) làm số nút dự đoán gần hằng còn 0/3/0 ở 3 ca pilot. SVR sau chuẩn hóa có ổn định hay không thì chưa kết luận được, vì tỉ số tổng hợp là NaN. NaN này có thể do 0/0 ở nút có y hằng nhưng std ≈ 1e-17 (REVIEW T-031 R2; REVIEW-2 R2). Vì vậy cạnh đồ thị gần như không tác động lên điểm RHT. Nguồn: `results/T-031/chan-doan-svr.json`, `chan-doan-svr-chuan-hoa.json`, LOG T-031.

## WHY-31. MicroRank-RCAEval sửa đầu vào ở P3 — Đã quyết (Q-74 Q7)

- **Chọn:** cửa sổ WHY-22. Xếp đầy đủ mọi operation có điểm làm chính; báo kèm danh sách cắt top-11 của code. Thực thể = `serviceName`; điểm thực thể = điểm operation cao nhất. Giữ hợp đồng lỗi của code: `ValueError` khi có operation sau mốc không có nền, std nền không xác định (< 2 span), ID trùng khác nội dung, khóa mơ hồ, điểm không hữu hạn → `ERROR`, giữ thông điệp; trả về rỗng với `missing_window`, `no_anomalous_traces`, `no_normal_traces` → `NO_EVIDENCE`, giữ status gốc. `PYTHONHASHSEED=0`, kiểm thêm seed 1 trên ca pilot. Trước pilot, T-030 chạy MicroRank trên 30 ca chỉ để đếm ca lỗi theo nguyên nhân (không chạy evaluator) và báo Minh; có ≥ 1 ca lỗi thì dừng chờ Minh.
- **Vì sao:** `top_max` là tham số định dạng, không thuộc công thức điểm (T-015 §2.5); MRR, NDCG cần đủ thứ hạng. Đổi cách xử lý operation thiếu nền là đổi phương pháp. Mỗi ca lỗi tính trượt (WHY-28), nên nếu cửa sổ ±300 s làm nhiều operation thiếu nền, MicroRank bị phạt có hệ thống vì lựa chọn cửa sổ; Minh cần thấy số này trước khi có số khoa học.
- **Phương án đã xét:** giữ top-11 làm chính; coi operation mới là bất thường hoặc bỏ qua nó (đổi phương pháp, chưa có nguồn); ngưỡng dừng 3 ca (một ô).
- **Bằng chứng:** `src/microrank/__init__.py:31–56, 68–70, 94–103`; `results/T-015/ho-so-microrank.md`; REVIEW T-022 (phản biện giao thức, điểm 2, Q7).
- **Giới hạn:** chưa đếm số ca lỗi ở ±300 s (T-007 khớp mốc ở ±600 s). Không dùng số T-007 làm đích cho bản sửa.
- **Kết luận phụ thuộc:** số MicroRank P3; trần coverage.

## WHY-32. TraceRCA bản lọc hữu hạn ở P3 — Đã quyết (Q-74 Q8)

- **Chọn:** gọi hàm RCAEval `e2e/tracerca.py` nguyên trạng; đọc `ji_dict` lúc hàm trả về bằng `sys.setprofile` (cùng cách `src/circa_kien_truc/scoring.py:60–65` đọc `DAScorer`); giữ operation có `ji` hữu hạn, sắp giảm dần. `ji` NaN (support 0, hoặc không có span bất thường) → không xếp. Danh sách rỗng → `NO_EVIDENCE`; `KeyError` khi có operation mới sau mốc → `ERROR`. Thực thể = `serviceName`, lấy từ cặp (operation, serviceName) trong dữ liệu; một operation ứng nhiều service → `ERROR`. Điểm thực thể = `ji` cao nhất. Kiểm: khi không có NaN, danh sách sắp từ `ji_dict` phải trùng danh sách chính thức; trên ca pilot, `ji` phải khớp phép tính độc lập của T-015.
- **Vì sao:** hàm sắp cả NaN rồi mới bỏ (`tracerca.py:86–93`); NaN phá phép so sánh nên thứ tự sai, và lọc danh sách trả về không sửa được. `ji_dict` là biến cục bộ; đọc nó lúc trả về giữ nguyên công thức của tác giả. Bỏ NaN trùng ý định "ignore ji nan" của tác giả (`:90`).
- **Phương án đã xét:** lọc danh sách trả về (bản 1, không sửa được thứ tự); cài lại công thức (cầu nối, rủi ro lệch); support 0 xếp cuối với điểm 0 (thêm ứng viên giả ở đáy); giữ lỗi sắp (chỉ để tái dựng T-007).
- **Bằng chứng:** `results/T-015/tracerca-rcaeval.md` §2, §5–6; `results/T-015/runs/tracerca-audit/seed0/` (T-007: đổi thứ tự dòng làm đổi thứ hạng; lọc hữu hạn đổi vị trí service gốc ở 14/90 ca, gồm cả đổi quy tắc hòa); REVIEW T-022 (phản biện giao thức, điểm 3, Q8).
- **Giới hạn:** tác động NaN và hòa báo gộp, không quy cho một lỗi. Zero-support nhiều thì Retrieval thấp do quy ước; phải báo.
- **Kết luận phụ thuộc:** số TraceRCA P3.

## WHY-33. SimpleRCA ở P3 dùng quy ước M4 của T-017 — Đã quyết (Q-74 "Thêm")

- **Chọn:** SimpleRCA ở P3 là "SimpleRCA (M4, quy ước T-017)" theo đúng WHY-17: metric mean + 3σ (ddof 0, một phía, `>`), đơn vị alert "events"; trace P95 tỉ lệ 3; log từ khóa ERROR/FAIL/EXCEPTION, ngưỡng 0; tổng điểm toàn 0 → abstain (`NO_EVIDENCE`); hòa theo nhóm điểm. Cửa sổ WHY-22: runner lọc span (kết thúc < t+300) trước khi gọi adapter T-017, vì adapter chỉ lọc theo thời điểm bắt đầu.
- **Vì sao:** WHY-17 đã ghi lý do từng quy ước và để ngỏ việc chọn cho P3; giữ nguyên tránh chọn lại sau khi T-017 đã thấy số dev. Lọc span trước là để theo giới hạn thông tin của WHY-22 mà không sửa code T-017.
- **Phương án đã xét:** đơn vị "channels"; P95 cho metric; ngưỡng log khác (đã kiểm độ nhạy ở T-017, không chọn theo accuracy).
- **Bằng chứng:** WHY-17; `src/simplerca/adapter.py:55–82`; `results/T-017/runs/fix-n1n2-001/`.
- **Giới hạn:** số `results/T-017/runs/run-dev-005/` (±300 s, lọc span theo thời điểm bắt đầu) không dùng lại nguyên trạng ở P3. Điểm "events" tăng theo số cột và độ dài cửa sổ (WHY-17).
- **Kết luận phụ thuộc:** số SimpleRCA P3.

## WHY-34. Chế độ (b): chuỗi đầu vào và hai bộ phát hiện — Đã quyết (Q-74 Q11, Q12)

- **Chọn:** gọi là **phát hiện hồi cứu trên bản ghi đã chọn vì có sự cố**. Bộ phát hiện nhận cả bản ghi 1.441 điểm, một lần, không khởi động lại, không nhận mốc tiêm, root, loại lỗi, tên hay đường dẫn ca.
  - BOCPD: tập cột WHY-25; tiền xử lý giữ code tác giả trên cả chuỗi (bỏ cột hằng, `ffill`, điền 0, min–max), khai báo là look-ahead. Gọi `online_changepoint_detection` nguyên trạng, rồi tính lại run length `m[i] = argmax R[:, i+1]` (sau khi thấy điểm i), i = 0..T−1; điểm đổi là i ≥ 1 có `|m[i] − m[i−1]| > 1` (luật `find_cps`). Không còn sentinel. Ghi kèm điểm đổi của `maxes` gốc để đối chiếu. Trước `argmax`, mọi phần tử R[:, 1..T] phải hữu hạn; không đạt → `ERROR` (WHY-28), ca ở mẫu số, tính trượt; không điền 0, không cắt chuỗi.
  - N-Sigma: k = 3, `startsfrom = 100`, mean/std chỉ dùng quá khứ. Cột chính = tập cột BOCPD; đối chứng = mọi cột. Tiền xử lý: `inf → NaN`, `ffill`; không min–max, không bỏ cột hằng. Báo động gộp mọi cột, sắp thời gian, bỏ trùng.
- **Vì sao:** Q-74 Q11 chọn cả bản ghi. Cách này không phải chọn độ dài và bước đoạn, và SPEC T-022 cấm chia đoạn để vừa chi phí. Mốc luôn ở giây 720 không phải lý do để chọn giữa cả bản ghi và chia đoạn: cả hai đều đặt mốc ở vị trí cố định. Code gốc gán `maxes[t]` từ posterior chưa thấy điểm t và để `maxes[T] = 0`, sinh một điểm đổi giả ở cuối mọi ca (`_bocpd.py:196, 212–225`); tính lại từ R sửa cả hai mà không đổi code. Cùng tập cột thì so được hai bộ phát hiện; đối chứng mọi cột cho biết kết luận có phụ thuộc việc giới hạn cột không. Luật N-Sigma không đổi dưới biến đổi affine và cột hằng không bao giờ báo, nên không cần min–max (runner T-006 dùng min–max toàn chuỗi, tức dữ liệu tương lai). Posterior BOCPD có thể thành NaN khi tổng mật độ tràn về 0 hoặc ∞ (`_bocpd.py:86–108, 211, 220`); NumPy `argmax` trên cột NaN trả 0, nên nếu không kiểm, lỗi số học thành điểm đổi giả hoặc "không báo động" giả (`results/T-013/kiem-tra.json`, check `N3-positive-mass-condition`). Danh sách cột lấy theo cả bản ghi là hồi cứu với BOCPD (cùng bỏ cột hằng, min–max cả chuỗi), nhưng không đổi báo động N-Sigma tới mọi thời điểm τ: hàm xét từng cột, chỉ dùng giá trị tới τ (`baro/anomaly_detection.py:24–34`), tiền xử lý nhân quả, và cột chưa có dữ liệu trước τ không báo trước τ. Vì vậy kết quả RCA sau báo động N-Sigma có lúc t̂+300 (WHY-22); BOCPD thì không.
- **Phương án đã xét:** đoạn 600 điểm bước 300 (phải chọn độ dài và bước; SPEC cấm chia đoạn để vừa chi phí); tiền xử lý nhân quả cho BOCPD (biến thể mới); giữ sentinel (mọi ca có một "báo động" sau mốc); nối các ca thành một dòng (cấm); N-Sigma chỉ mọi cột.
- **Bằng chứng:** `D:/RCA-ext/src/baro/baro/_bocpd.py:187–227`; `baro/utility.py:208–214`; `baro/anomaly_detection.py:7–35`; `baro/reproducibility.py:140–166`; `results/T-013/cua-so-va-che-do-b.md` §2–4; `results/T-013/ho-so-nsigma-phat-hien.md`; REVIEW T-022 (phản biện giao thức, điểm 5, Q11, Q12).
- **Giới hạn:** vị trí điểm đổi BOCPD không phải thời điểm cảnh báo được, vì min–max và bỏ cột hằng dùng cả chuỗi; báo nó là "độ lệch vị trí điểm đổi hồi cứu". Không đo được cảnh báo trực tuyến hay báo động sai trong vận hành liên tục; dữ liệu bình thường chỉ 720 s/ca. Mọi ca có đúng 720 s nền trước lỗi; số phát hiện chỉ nói cho cấu hình nền cố định này. Với BOCPD, t̂ chỉ có sau cuối bản ghi (WHY-22). Chi phí BOCPD trên 1.441 điểm chưa đo (WHY-25).
- **Kết luận phụ thuộc:** mọi số phát hiện P3 (T-025); RCA chế độ (b).

## WHY-35. Chế độ (b): chấm phát hiện và tích hợp với ranker — Đã quyết (Q-74 Q13, Q14)

- **Chọn:**
  - Nhãn proxy, chỉ evaluator đọc: bất thường = [t_tiêm, cuối file], bình thường = trước đó (README RCAEval).
  - Chấm phát hiện bằng báo động thô, không gộp episode. Cửa sổ 60 s tính từ đầu file; cửa sổ dương nếu có báo động; không point-adjust. Chỉ chấm cửa sổ mà mọi điểm được bộ phát hiện đánh giá (N-Sigma từ chỉ số 100, BOCPD từ chỉ số 1); bỏ cửa sổ cuối chỉ có 1 điểm. Theo ca: phát hiện nếu có báo động trong đoạn bất thường; mỗi ca tối đa một sự kiện. Báo động sai mỗi giờ: mẫu số là giờ bình thường được đánh giá của từng bộ. Độ trễ: báo động đầu ≥ t_tiêm trừ t_tiêm ("độ trễ từ lúc tiêm" cho N-Sigma; "độ lệch vị trí điểm đổi hồi cứu" cho BOCPD).
  - Lượt RCA: báo động đầu mở lượt RCA ở t̂; thời gian trơ 300 s; báo động sau thời gian trơ là thông báo mới, được đếm, không chạy RCA. Cửa sổ RCA theo WHY-22 quanh t̂, cắt ở biên file.
  - Ranker: BARO, CIRCA kiến trúc, TORAI (nguồn chính theo WHY-29), mỗi cái với hai bộ phát hiện. Tên: "tích hợp P3: `<ranker>[<bộ phát hiện>]`".
  - Thành công chung: báo động đầu ghép đúng sự kiện (t̂ ≥ t_tiêm) và RCA tại đó xếp root trong top-k (quy tắc hòa WHY-28). Báo động đầu sai thì ca trượt. Thứ hạng tại báo động đầu, kể cả khi sai, được lưu và báo riêng.
- **Vì sao:** gộp episode với thời gian trơ để chấm làm một báo động sai trước mốc che các báo động đúng sau mốc (báo động sai ở t−100 trơ tới t+200). RCA tại báo động sai vẫn có thể trúng root do may, schema hoặc cửa sổ A chồng vào sự cố; đó không phải "phát hiện đúng rồi chẩn đoán đúng". README RCAEval là nguồn quy ước nhãn của chính dataset. Bài BARO ghép bộ phát hiện với CIRCA bản PC, không phải bản kiến trúc; TORAI giả định mốc từ bộ phát hiện ngoài nhưng không kiểm cặp cụ thể, nên các cặp ở đây là tích hợp của nhóm. RCA ở báo động đầu theo cách BARO dùng điểm đổi đầu tiên (`root_cause_analysis.py:284–290`).
- **Phương án đã xét:** chấm theo episode (bản 1); RCA ở mọi thông báo và lấy thông báo ghép đúng đầu tiên (tốn thêm lượt RCA; tách được chất lượng RCA khỏi báo động sai, nhưng lệch chính sách báo động đầu); chấm mọi cửa sổ, coi điểm chưa đánh giá là âm; nhãn theo bài BARO (corpus khác); MicroRank, TraceRCA ở chế độ (b) (cần suy trường trace thiếu: biến thể mới).
- **Bằng chứng:** `results/T-002/public-metadata/run-002/sources/hf-README.md:97`; `results/T-014/ho-so-circa-pc.md:100`; `results/T-016/ho-so-torai.md:25`; `results/T-015/ho-so-microrank.md` §9.1; REVIEW T-022 (phản biện giao thức, điểm 5, Q13, Q14).
- **Giới hạn:** thời điểm lỗi thật bắt đầu và kết thúc chưa biết; nhãn proxy giả định lỗi kéo dài tới cuối file. Biên cửa sổ 60 s trùng mốc vì mốc ở giây 720 (đặc điểm RE2-TT). Dữ liệu bình thường 6 giờ cho 30 ca.
  - **Biên file ở chế độ (b) (thêm 07/10/2026, T-025 REVIEW R1, R2).** Khi t̂ < giây 300, cửa sổ [t̂−300, t̂) vượt đầu file. Runner cắt dữ liệu và ghi độ dài thực (§5.5). Mỗi ranker xử lý phần thiếu khác nhau.
    - BARO dùng đúng các dòng có.
    - CIRCA: loader của RCAEval điền ngược phần trước đầu file, nên train vẫn 111 điểm (`RCAEval/classes/data.py:92–104`). Đây là code tác giả, giữ theo §5.4.
    - TORAI B: lưới 40 bin cố định của §6.6 điền 0 vào bin trước đầu file (`src/p3/torai_b.py:73, 78, 106, 113`). Bản tác giả không thêm hàng (`RCAEval/main.py:381–393`). Giao thức chưa nói trường hợp này. T-025 giữ nguyên lượt đã chạy và không chạy lại; số TORAI có điều kiện được tách theo "đủ nền" / "N có bù 0" (`results/T-025/cham/tach-torai-bu0.json`).
    - **Kết luận phụ thuộc:** chỉ các số có điều kiện của TORAI và CIRCA ở ca có t̂ < giây 300 (hay < giây 120 với CIRCA). Thành công chung không phụ thuộc, vì cả 3 ca có t̂ đúng đều sau giây 720. Nếu P4 cần thứ hạng TORAI ở các ca này, phải quyết lại cách xử lý biên trước khi chạy.
- **Kết luận phụ thuộc:** bảng phát hiện P3 (Q-30); RCA chế độ (b); chi phí T-025.

## WHY-36. CIRCA chỉ dùng bản gốc; không sửa lỗi làm tròn — Đã quyết (Q-82, thay Q-81)

- **Chọn:** CIRCA ở P3 chỉ dùng bản gốc đã khóa (OLS+RHT+DA, WHY-30, Q-80), không thêm biến thể sửa. Báo kèm: (1) 11/30 ca dev có nút điểm RHT > 1e10 do lỗi làm tròn; (2) kết quả so sánh trên 19 ca còn lại. Hai nhóm tách theo điểm của chính CIRCA, không dùng nhãn, chốt trước khi chấm.
- **Vì sao:** baseline phải là phương pháp của tác giả. Lỗi: residual gần 0, phép kiểm hằng của sklearn (`StandardScaler`) không nhận ra, nên chia cho số cực nhỏ, điểm khoảng 1e16; DA kéo nút cha lên đầu. Có lỗi này cả ở code CIRCA gốc lẫn RCAEval. Báo riêng 19 ca không vượt ngưỡng thì kiểm được kết luận có còn đứng khi bỏ 11 ca dev đã xác nhận lỗi làm tròn hay không, mà không cần sửa phương pháp. Phép so này không chứng minh 19 ca không còn điểm lạ nào khác của bản gốc.
- **Phương án đã xét:** V∞ (+∞ cho mọi metric đứng yên rồi đổi): đã cài và chạy (`results/T-031/runs/circa-vinf-001`, `k-vinf.json`), bỏ vì chạm 109 nút ở 28/30 ca, trong khi chỉ 11 nút có lỗi, và không gỡ được 11 ca. V1 (kiểm hằng trên metric thay vì trên residual): không làm, vì Minh chốt không sửa CIRCA.
- **Bằng chứng:** `results/T-031/chan-doan-diem-lon.json`; `results/T-031/k-vinf.json`; REVIEW T-031 R1; bài CIRCA mục 4.2, phương trình (3), (4); code CIRCA `0215e18` `circa/alg/common.py:46–52`, `circa/alg/ci/anm.py:21–31`.
- **Giới hạn:** phép so trên 19 ca có cỡ mẫu nhỏ hơn. 19 ca được tách theo đầu ra CIRCA trên cửa sổ A, nên không phải mẫu ngẫu nhiên. Trên dev, luật V∞ quét mọi nút có y train hằng theo sklearn: ngoài 11 nút vượt ngưỡng, 98 nút còn lại có điểm gốc ≤ 4 (`results/T-031/k-vinf.json`). Vậy cơ chế này không ẩn dưới ngưỡng ở dev. Chưa kiểm cơ chế khác (residual cỡ ulp do hồi quy khớp gần tuyệt đối). Ở 60 ca test (khóa tới G3) tách theo cùng luật > 1e10. Ở đó nhóm vượt ngưỡng chưa được xác nhận nguyên nhân.
- **Kết luận phụ thuộc:** so sánh với CIRCA ở RQ1, RQ3; nhận định về đồ thị ở P4.

## WHY-37. Đầu vào Nezha-OB — Đã quyết (Q-85)

T-026 chỉ dùng 22 ca Nezha-OB dev ở chế độ biết trước cửa sổ. Minh duyệt BARO, SimpleRCA M4, MicroRank và TraceRCA; TORAI B và CIRCA được ghi UNSUPPORTED. Các lựa chọn dưới đây được khai trước số phương pháp. Giao thức V2 giữ nguyên; phần áp dụng riêng cho Online Boutique nằm ở mục này.

**Chọn và lý do.** Dùng alias pod tường minh, gồm Frontend→frontend, và universe là 10 service đã quan sát. Không dùng nhãn root để chọn service, kênh hay SLI, không áp universe 68 của Train Ticket. BARO và SimpleRCA nhận 16 kênh mỗi pod cùng 5 kênh front, giữ giá trị gốc. Ba kênh Node* bị loại vì chưa có ownership để gán tín hiệu host về service; source_50, destination_50 và dependency không được dùng vì chưa có hợp đồng thời gian và ánh xạ phù hợp. BARO dùng 5 điểm N và 5 điểm A theo thứ tự từng nguồn, với Time của front làm marker chia nhóm. SimpleRCA dùng arrays riêng từng kênh và bỏ giá trị không hữu hạn theo lõi M4. Không dedup chung; số hàng lặp không phải số quan sát độc lập.

TORAI B thiếu statusCode và cadence metric khoảng 60 giây không khớp stride 15 hàng. Mỗi ca/view có một bản ghi UNSUPPORTED với seed null; không giả trường, đổi stride hoặc chạy biến thể cứu. CIRCA chỉ có 1–2 phép đo thật mỗi nguồn trong khoảng train. Code loader nội suy toàn đoạn trước chia train, nên ở 19/22 ca có khoảng đuôi train có thể lấy anchor từ A. Minh chọn UNSUPPORTED để tránh dùng nền lẫn dữ liệu sau mốc; không viết wrapper per-node hay sửa loader. Chưa gọi loader trên OB để đếm số ô hiệu lực.

Giữ ba bảng inject_time của Q-84. Thêm bảng độ nhạy cho MicroRank, TraceRCA và phần trace của SimpleRCA: N chỉ nhận span có end nhỏ hơn t−41 giây ngày 22/08 và t−32 giây ngày 23/08; A giữ điều kiện chia riêng của phương pháp. Khoảng bị bỏ không chuyển sang A. Đây là phép kiểm độ nhạy với lệch trace còn OPEN, không dịch đồng hồ và không xác nhận nền sạch. Kết luận ổn định hay đổi chiều phải khai theo QT3.

**Phương án đã xét.** Gói phiên 3 xét ghép union 110 Time rồi điền, bảng ordinal cho BARO, arrays native cho SimpleRCA, CIRCA per-node cùng phần điền biên và thăm dò CIRCA riêng. Minh chọn ordinal/arrays, bỏ CIRCA thay vì sửa hợp đồng biên. Nội suy metric về 1 giây, suy error từ success rate, dedup chung và cứu TORAI bằng nguồn TT không được chọn vì làm thay dữ liệu hoặc cấu hình.

**Bằng chứng.** Hai khối 001/002 và khối 003 ở results/T-026/kiem-dau-vao.md giữ hash, cửa sổ và thống kê. Alias, đơn vị, độ lệch ordinal và kênh nằm ở dòng 14253–14310; CIRCA và chính sách lặp ở 14318–14332. Code Nezha data_integrate.py:254–260 lấy service từ pod; RCAEval/classes/data.py:89–104 nội suy trước chia; src/p3/torai_b.py:60–78 yêu cầu statusCode và bù bin; src/torai/torai_sua.py:102–112 dùng stride 15 hàng. Quyết định nguyên văn và phạm vi phiên 4 nằm trong LOG của T-026.

**Giới hạn và kết luận phụ thuộc.** Nezha-OB đo metric khoảng 60 giây, chỉ 5 điểm mỗi phía, còn RE2-TT đo 1 giây. Khác biệt khi so T-024 không được quy riêng cho đổi hệ thống. Mọi trạng thái, thứ hạng, chi phí, bảng độ nhạy và so sánh hai dataset phụ thuộc các lựa chọn này. Nền sạch, recovery, thời điểm lỗi thật và đồng bộ tuyệt đối vẫn OPEN; mẫu dev nhỏ không chứng minh đại diện cho test.


## WHY-38. Codebook phân tích hạn chế xếp hạng chế độ (a) — Đã quyết (Minh duyệt codebook T-028 và nội dung mục này)

- **Chọn:** dùng `results/T-028/codebook.md` chốt trước lượt tính bằng chứng P4. Bảng chính là RE2-TT dev30 và Nezha-OB main, sáu phương pháp với trạng thái giữ nguyên. Ca sai OK xét riêng Hit@1/Hit@5 kỳ vọng theo hòa; mức trượt kỳ vọng và non-OK báo riêng. CIRCA dev19 chỉ dòng có điều kiện Q-82; các view Nezha độ nhạy chỉ đánh dấu status/Hit đã có. Không chạy lại phương pháp.

- **Vì sao:** RQ2 và yêu cầu của cô cần chỉ ra ca nào, phương pháp nào, dấu hiệu cơ chế nào. Khóa tiêu chí trước bằng chứng mới hạn chế chọn ngưỡng theo kết quả dev, nhưng không xóa được việc người làm đã thấy bảng T-024/T-026. Thống kê mọi service được ghi trước nối nhãn. Thiếu kênh/trung gian không được biến thành không có lỗi. Đối chứng đúng/sai có các quan hệ cấu trúc: M1/M2 kéo theo sai; M3 loại Hit=1; M5 True không thể xuất hiện ở ca đúng top-1; M6 SimpleRCA kéo theo sai top-1 và M6 TraceRCA kéo theo M2. Các bảng này không tự là kiểm chứng cơ chế độc lập.

- **Tiêu chí và primary:** giữ đa nhãn và thứ tự M1 → M2 → M3 → M4 → M5 → M6 → M0: rào cản tập, bất định hòa, cohort lỗi đã xác nhận, rồi dấu hiệu ứng viên. Primary chỉ để trình bày, không là nguyên nhân trội hoặc chuỗi nhân quả. TORAI giữ cờ từng seed, gộp nhãn theo ca và công khai any/all/partial; không dùng Hit trung bình seed để phát hiện hòa. M4 chưa chứng minh lỗi làm tròn gây từng thất bại. M5 mô tả ancestor quan sát được chắc chắn đứng trước root, không đo đầy đủ “độ trễ lan nên caller xếp trên root”. Proxy không đổi nhóm.

- **Luật cục bộ:** giữ tham số và cửa sổ native đã quyết. CIRCA xét các metric trong diagnostics.nodes sau prune; tập phải không rỗng và mọi score hữu hạn, cờ True khi tất cả RHT<3. RHT=3 đạt ngưỡng DA; metric bị loại không được coi bình thường. BARO giữ score có dấu nhưng local_nonpositive=N/A vì không có ngưỡng hoạt hóa native; TORAI cũng N/A theo giới hạn trung gian đã lưu. Trong bản ghi TraceRCA OK, M6 kéo theo M2 nên M2 là primary; chiều ngược không đúng. M6 khác nghĩa giữa các phương pháp, không dùng tỉ lệ để so mức bất thường trên một thang chung.

- **Bằng chứng dữ liệu root:** đặt score/coverage BARO cạnh các thống kê root đã khai theo quy ước SimpleRCA: từng metric với số quan sát, thiếu, μ/σ và events; trace với P95N/P95A; log với số dòng A và keyword count. Đây là trình bày lại thống kê mọi service, không là luật BARO, chuẩn chung hoặc nhãn mới. RE2 giữ cửa sổ SimpleRCA; Nezha dùng arrays riêng từng nguồn, không chia lại bằng marker BARO; trace chia start, log theo timestamp. Proxy end-split giữ riêng. Không có events không chứng minh không có tín hiệu; raw metric khác đầu vào BARO sau preprocessing; log lỗi A có thể là lỗi nền.

- **Proxy độ trễ:** giữ P95A>τ·P95N, τ chính 3, độ nhạy 2 và 4, cùng số quan sát/availability. Đây là span-duration, không phải end-to-end latency. Proxy chỉ là bối cảnh; không thay luật native hoặc primary. Không chia cho nền bằng 0, không đổi đồng hồ hoặc giả nền sạch.

- **Đối chiếu M5:** thêm P0 làm mức nền mô tả. Với root thuộc R và graph/mapping/ranking khả dụng, đặt n=|O|, a là số proper ancestor của root thuộc O, b là số entity chắc chắn trước root theo full key/khối. Null giữ vị trí root, cấu trúc hòa/khối và L; hoán vị đều danh tính O\{root} vào mọi vị trí còn lại, gồm vị trí không trả về. P0=1−C(n−1−a,b)/C(n−1,b). So số cờ cơ sở M5 True, không phải primary=M5, với ΣP0 trên cùng tập đủ điều kiện. TORAI báo từng seed, không OR P0 hoặc coi seed là các ca độc lập. Root ngoài R hoặc dữ kiện không khả dụng cho P0=N/A; a=0 chỉ khi graph khả dụng và không quan sát ancestor. Không p-value, không ngưỡng “đáng kể”, không dùng P0 làm nhãn lan trong T-028.

- **Giải thích khác và mức kết luận:** P0 giữ n/a/b và hòa, không giữ thiên hướng điểm riêng từng entity, số kênh/operation hoặc cấu trúc phương pháp. Chênh lệch có thể do lan, caller tự bất thường, tác động chung, sự cố đồng thời, cấu trúc chấm điểm, coverage/preprocessing, sai lệch cửa sổ/clock/nền/graph/mapping/nhãn hoặc dao động hữu hạn. Thành phần cohort và phụ thuộc ca/seed hạn chế khái quát hóa và đánh giá dao động. Dùng thống kê đã khai để nêu phần hỗ trợ, đã loại được hoặc chưa kiểm; không suy hướng tác động chỉ từ P95 và graph N. Lỗi triển khai xử lý theo SPEC, không gọi là cơ chế khoa học.

- **Phép đo đầu ra và schema:** giữ Dice overlap kỳ vọng top-1/top-5 trên phân phối hạng chính xác, kể cả hòa khối TORAI. D0 là hoán vị đều độc lập trên đúng O từng ca, giữ chiều dài trả về. Báo D, D0, D−D0 và 1−D; cân đều cặp ô, cùng ô riêng, seed trong ca riêng. Non-OK hoặc vi phạm điều kiện ghi N/A. 1−D gồm bất định hòa; sự tập trung không chứng minh bỏ qua dữ liệu ca. Audit schema dùng raw_column_audit T-024, chỉ bảng chéo dev; không chạy L* hoặc đưa dấu vắng vào phương pháp.

- **Phương án đã xét:** uniform trên cận hạng làm sai hòa khối TORAI; top-k hiển thị bỏ qua hòa; thay O bằng U làm lẫn coverage với hành vi ranking; ngưỡng chung không phản ánh tín hiệu native; một nguyên nhân duy nhất che đa cơ chế; đổi tiêu chí theo phân biệt sai/đúng gây chọn theo kết quả. Chỉ đếm M5 mô tả là phương án hợp lệ nhưng không có mức nền theo cơ hội, nên chọn bổ sung P0 có điều kiện. Dùng proxy làm điều kiện M5 sẽ đổi đối tượng đo mà vẫn chưa xác nhận lan, nên không chọn. Thêm ngưỡng BARO quanh 0 không giải quyết bằng chứng ở kênh khác, nên giữ score liên tục và bảng dữ liệu root. Không chạy can thiệp hoặc thành phần phương pháp để điền trung gian thiếu vì ngoài SPEC.

- **Bằng chứng thiết kế:** giao thức V2 T-022 §5–§8; WHY-22–33/36–37; SPEC T-028 bước 2–6; bản ghi/chấm T-024/T-026; code native và hồ sơ P1 dẫn trong codebook. Biên CIRCA đối chiếu RCAEval/graph_heads/rht.py:271–277; tập metric đối chiếu src/circa_kien_truc/scoring.py:69 và src/p3/adapters/circa.py:99–101. Bộ lọc TraceRCA đối chiếu RCAEval/e2e/tracerca.py:53–93 và src/p3/adapters/tracerca.py:43–63; score BARO đối chiếu results/T-013/ho-so-baro.md:31–36. Đây là căn cứ thiết kế; số nhãn, liên hệ và ảnh hưởng sửa chưa tính tại thời điểm chốt.

- **Kết luận phụ thuộc và phần còn mở:** mọi nhóm ca sai, số nhãn, bảng tín hiệu/schema và phép đo đầu ra T-028 phụ thuộc codebook này. M5/P0 riêng lẻ không xác nhận lan đáng kể. Cuối task báo toàn bộ bằng chứng kiểm được tới đâu, không chốt trước có lan hoặc không lan. Không áp cho chế độ (b), test, dataset khác, nhãn lan chính thức hoặc kết luận giá trị đồ thị. Clock/nền sạch, coverage và tính đại diện còn OPEN; can thiệp nhân quả ngoài phạm vi.

- **Đề xuất chờ Minh quyết:** xem xét đặt phần tổng hợp bằng chứng còn đủ/thiếu cho câu hỏi “lan có đáng kể” trong gói trình G2; T-029 là một lựa chọn theo PLAN. Nếu Minh chọn T-029, phạm vi được trình trong SPEC T-029 để duyệt riêng. Mục này không giao trước nhiệm vụ hoặc thực nghiệm cho T-029. Không đổi “chưa xác nhận” thành “không đáng kể” hoặc coi thành phần P6 nhắm vào lan đã được P4 xác nhận.


## WHY-39. Phân tích hạn chế phát hiện chế độ (b) — Đã quyết (Minh duyệt SPEC T-029)

- **Chọn:** phân tích 90 cặp (ca, bộ phát hiện) trên 30 ca dev RE2-TT theo thiết kế khóa trong SPEC T-029: phân loại S/E/Miss; cờ cơ chế N-Sigma N1–N4 và BOCPD B1–B4 kèm độ nhạy; ba can thiệp phân tích (I1 BOCPD trên tiền tố trước mốc, I2 như I1 với hazard 1/250, I3 RCA tại báo động đầu tiên sau mốc); định vị theo báo động đầu sau mốc của từng dịch vụ; kiểm nhãn proxy và schema; bảng chế độ (a) so với (b).
- **Vì sao:** MRP P4 và Q-30 yêu cầu phân tích hạn chế phát hiện như phân tích xếp hạng. T-025 cho thấy báo động đầu thường trước mốc nhưng chưa kiểm cơ chế. Cờ mô tả chỉ cho liên hệ; I1/I2 tách ảnh hưởng của dữ liệu sau mốc qua tiền xử lý, và của hazard, lên báo động trước mốc, vì posterior BOCPD ở i chỉ dùng dữ liệu ≤ i. I3 cho chênh có dấu theo từng ca giữa ba điểm chạy. Phép thử giả tại điểm không báo động ngăn gọi một cờ phổ biến là lời giải thích (áp cho B1, B4).
- **Ngưỡng:** N1 hai lần, N2 10·p0 với p0 = 0,0027, B4 bước nhảy chuẩn hóa MAD ≥ 3 với w = 30 s, đoạn MAD tối thiểu 30 điểm, dung sai điểm đổi ±5 s. Đây là quy ước phân tích, chưa kiểm; độ nhạy khai trước (N1 1,5/3; N2 5/20·p0; B4 2/5 và w 15/60; ±2/±10 s). Hazard 1/250 lấy từ giá trị có trong code tác giả, không chọn theo nhãn.
- **Dùng nhãn:** mốc 720 giống nhau ở mọi ca nên dùng từ đầu; root, loại lỗi, ô nối sau khi đặc trưng đã lưu. I1–I3 dùng mốc để cắt dữ liệu hoặc chọn báo động: là phân tích, không là phương pháp, không thay số P3.
- **Phương án đã xét:** chỉ đếm mô tả từ T-025 (rẻ nhưng không tách được cơ chế); chạy lại BOCPD đầy đủ với hazard mới (tách thêm ảnh hưởng lên độ trễ, nhưng khoảng 2,3 giờ EC2; để sau nếu Minh cần); chỉnh ngưỡng N-Sigma (là tinh chỉnh bộ phát hiện trên dev, không phải phân tích hạn chế); định vị BOCPD bằng bỏ từng cột (d lần chi phí, không chọn).
- **Bằng chứng thiết kế:** giao thức V2 §4, §7, §10; `src/p3/adapters/phat_hien.py`; `results/T-013/ho-so-bocpd.md`, `ho-so-nsigma-phat-hien.md`; `results/T-025/phat-hien.md` §3–§5.
- **Kết luận phụ thuộc:** bản đồ hạn chế phát hiện, phần phát hiện của gói G2 và mọi lựa chọn P6 trỏ về HP-n của T-029. Không áp cho test, Nezha, chế độ online hay nền khác 720 s. Thứ tự báo động đầu sau mốc không phải bằng chứng nhân quả hay nhãn lan.


## WHY-40. Lần theo nguyên nhân thất bại xếp hạng — Đã quyết (Minh duyệt SPEC T-032 ngày 09/10/2026)

**Chọn:** đọc code/trung gian trước; phát lại đúng phần thiếu tại F đóng băng; khóa nhóm bắt buộc từ cờ đa nhãn/non-OK, đọc đơn vị không trùng với đối chứng cùng điều kiện, lập trạng thái từng ca M5 và khả năng đo chờ. Đối chiếu khác phương pháp chỉ bổ sung bằng chứng kênh. A′ đã được Minh chọn trong thiết kế: giữ J0, so W-native với W-unit tại đầu vào spectrum; chưa là quyết định chạy.

**Vì sao:** phải biết bước nào tạo mất thông tin hoặc chênh điểm trước khi đề xuất xử lý. Caller đứng trên root hoặc duration tăng không phân biệt chờ phụ thuộc, xử lý tại caller, coverage và cách tính điểm.

**Phương án đã xét:** đọc mỗi k/cờ như ca độc lập (lặp công và dễ đếm trùng), chỉ đọc một ca rồi suy cả nhóm (thiếu coverage), dùng phương pháp khác xếp đúng thay đối chứng (khác kênh/công thức), can thiệp mọi phương pháp hoặc hạ duration/xóa caller (đổi nhiều yếu tố, dễ cho kết quả hiển nhiên), xáo trace TraceRCA giữ counts (bất biến theo công thức). Chọn ánh xạ nhóm và lõi toàn bộ, kèm A′ chỉ đổi toàn gói trọng số MicroRank trên J0. Đã xét J một cặp và batch cặp rời: điều kiện giữ số trace N/A và đổi partition giới hạn phép đổi vào sole-trigger bundle; không thay đồng bất thường giữa các operation khác nhau, nên bỏ khỏi thiết kế. B không can thiệp đã được xét nhưng không được chọn; giữ counts/nhóm gốc và đổi W cho câu hỏi trọng số cụ thể, không nhận phân xử toàn bộ caller/root. Đã xét thêm chạy toàn bộ P1/P2 trước khi hiểu bước chấm; đặt nhãn lan/tự sinh theo tỷ lệ duration; chỉ đọc đầu ra đã lưu. Lưới cửa sổ chưa tự phân xử cơ chế; tỷ lệ duration không xác định semantics chờ; chỉ đọc có thể thiếu trung gian ở bước quyết định. Phát lại giới hạn đúng phần thiếu và kiểm khớp giữ được câu hỏi mà giảm chi phí.

**Bằng chứng:** MRP P4, DT18-NV2/NV3, hướng dẫn cô §1 và đường tính trong code phương pháp ở revision đã tạo P3. Chưa có kết quả task này; lựa chọn là kế hoạch kiểm, không xác nhận giả thuyết.

**Kết luận phụ thuộc:** căn cứ cơ chế tính toán/ứng viên P5–P6, đầu vào K4 của tổng hợp G2 và yêu cầu quan sát FlashTicket; nguyên nhân vật lý và lợi ích đồ thị vẫn cần bằng chứng tương ứng. A′ được chọn không biến câu còn mở thành đã xác nhận. Chỉ phép so toàn gói weighting được hỗ trợ; không quy riêng cạnh/prior hoặc nguồn vật lý của counts. Có thể có tương tác với nhánh thiếu support và operation đạt max service, phải lưu trung gian. Khi phần lõi chưa phân xử caller/root, trình đúng bằng chứng/phép kiểm cần bổ sung và lựa chọn phụ thuộc; không dừng ở OPEN. Không chọn nhánh/ca theo tăng hạng root, không thêm seed/ngưỡng mới. Margin chuẩn hóa để so chênh có dấu giữa ca có thang điểm khác nhau, vẫn giữ điểm thô/mẫu số 0. Đây không là ngưỡng lan hoặc lựa chọn theo accuracy. Chỉ nối mục này vào docs/WHY.md khi Minh duyệt thực hiện đúng nội dung.


## WHY-41. Lần theo cơ chế phát hiện — Đã quyết (Minh duyệt SPEC T-033 ngày 09/10/2026)

**Chọn:** xác minh lõi native full/FF/I1 theo trạng thái nguồn, kể cả tái lập non-OK, trước; khóa nhóm/đối chứng và ánh xạ ca; phân rã mask × nguồn min/max trên tiền tố, lần theo độ trễ full và contrast ngưỡng N-Sigma cập nhật/cố định trước proxy. D chuyển sang kiem-tiep, chưa chạy. Nhánh mới là chẩn đoán; không chọn detector online hoặc đổi số P3.

**Vì sao:** cờ/số CP không chỉ bước gây báo; full/I1 đổi nhiều yếu tố. Giữ mask để so scale, giữ nguồn scale để so gói cột/d/prior, báo tương tác để không gán tổng effect cho một phần. Full cần cho trạng thái sau proxy; ngưỡng cố định cùng k native kiểm tác động cập nhật lịch sử, không chứng minh nền sạch. Đặt độ lệch sau proxy cạnh mật độ báo trước và chuỗi cờ qua proxy để không gọi báo đang tiếp diễn là vừa phát hiện sự cố; không thêm ngưỡng. Giữ raw prefix/mask/d/prior thì contrast nguồn scale/fill là khác biệt xử lý, không tự là thay đổi thật của hệ thống; đo đường likelihood/posterior/CP, không buộc đầu vào khác phải đổi CP. Tái dùng FF từ full giảm chạy trùng khi invariants đạt.

**Phương án đã xét:** chỉ so số CP (không chỉ bước); chỉ tiền tố (không giải thích sau proxy); thay prior ở khác chiều như cùng mô hình (không định nghĩa duy nhất); zero-padding hoặc thêm epsilon để đủ factorial (đổi phép tính và có thể tạo kết quả hiển nhiên); chạy surrogate rộng (thay nhiều thuộc tính); chọn D để báo hiệu quả (không có onset/end thật). Chọn native full + thiết kế hai yếu tố có giới hạn, giữ phần không tách được. Đã xét loại mọi range0/d0/input trùng/lỗi khỏi contrast: làm mất khác biệt xử lý hợp lệ hoặc biến không có khác biệt thành thiếu bằng chứng; thay bằng bốn trạng thái riêng, giữ output/lỗi native và mẫu số. Không chữa native để có effect. Không bắt mọi yếu tố phải tách độc lập mới cho phép báo căn cứ có điều kiện.

**Bằng chứng:** MRP P4, DT18-NV2/NV3, hướng dẫn cô §1, code detector ở revision đã chạy và nguồn đóng băng T-025/T-029. Chưa có kết quả task này; đây là kế hoạch kiểm, không xác nhận giả thuyết.

**Kết luận phụ thuộc:** căn cứ thành phần tiền xử lý/detector P6 và giới hạn đánh giá; mask/d/prior chưa tách, nhánh prefix/full đều còn nhìn trước, onset thật chưa biết. Các quy tắc native, factorial, ngưỡng cố định từ [:i_proxy] và chỉ số CP/m/delay là lựa chọn chẩn đoán khai trước; không có ngưỡng Late hoặc surrogate chọn từ accuracy. Cơ chế tính toán không tự xác nhận thay đổi vật lý, nền sạch hoặc ưu thế causal detector; thành phần hiệu chỉnh còn OPEN nếu chưa phân xử. Chỉ nối mục này vào docs/WHY.md khi Minh duyệt thực hiện đúng nội dung.


## WHY-42 — Ngoại lệ phát lại MicroRank trong T-032 (Minh duyệt 10/10/2026)

**Chọn:** Chỉ trong T-032/MicroRank, chấp nhận sai lệch float64 của score operation/service khi đồng thời ≤16 ULP biểu diễn và ≤16×2^-52 tương đối, không absolute floor; giữ exact trạng thái, mapping/tập ứng viên, thứ tự và partition hòa service, Hit@1..10 và toàn cờ M của T-028. Operation đảo chỉ trong cùng service, sát ngưỡng ở cả hai output và không làm đổi tổng hợp trong cùng output; không ép gần điểm thành hòa. Native–observed vẫn exact. Khóa ngưỡng trước bảng 30 RE2+22 Nezha, báo max ULP/relative từng ca; vượt thì dừng/trình, không tăng.

**Vì sao:** Ca pilot đã kiểm source/hash cho thấy native–observed exact nhưng native–frozen có lệch nhỏ ở số và thứ tự operation cùng service. Khớp byte toàn điểm giữ cho phát lại khác nền tảng chưa thực hiện được; chấp nhận sai lệch rộng hoặc chỉ so top1/top5 có thể che thay đổi service/nhóm hòa/cờ dùng trong phân tích. Comparator hẹp giữ các quyết định chấm và khoảng cách định lượng tới ngưỡng, không hợp thức hóa lỗi thuật toán.

**Phương án đã xét:** (1) Giữ exact và xử lý môi trường để tái lập nguồn; vẫn hợp lệ nhưng chưa xác định thành phần gây drift. (2) Phát lại laptop Windows/Python nguồn với exact; giảm khác nền tảng, cần quyền ngoại lệ EC2-only và đo RAM/thời gian capture toàn52, không bảo đảm exact. (3) Tolerance tuyệt đối chung hoặc bỏ thứ tự operation; không chọn vì có thể che thay đổi gần zero, giữa service hoặc trạng thái hòa. (4) Chỉ chấp nhận comparator hẹp khi score và các invariant đầu ra đều đạt; Minh chọn phương án này, không áp phương pháp khác.

**Bằng chứng và phần chưa kiểm:** runs/tiep-tuc-003/microrank-numeric-audit.json#/native_observed_exact, /float_exact_count, /other_difference_count, /max_absolute; native_vs_frozen/differences ở diagnostic-check. Hai đầu transfer/source hash đã kiểm. Ngưỡng là lựa chọn kiểm kỹ thuật sau khi đã thấy pilot, chưa là cận sai số lý thuyết hay bằng chứng nguyên nhân nền tảng. Bảng52/comparator/benchmark và khớp Hit/cờ M chưa chạy. Frozen P3 thiếu mask/partition lịch sử; counts bằng nhau không đủ chứng minh từng membership lịch sử bằng nhau.

**Kết luận phụ thuộc:** Chỉ các ca qua toàn hợp đồng được dùng trung gian mới cho phân tích MicroRank. Đạt comparator không tự xác nhận cơ chế vật lý, partition lịch sử hoặc lợi ích đồ thị; A′ vẫn cần đầy đủ lõi/khóa mẫu/nhóm N/A/invariant của SPEC. Ca đổi service order/hòa/chấm hoặc vượt số phải dừng MicroRank/A′ và trình. Các phương pháp khác giữ exact. Quyền thực hiện và kết quả kiểm tách riêng; chưa dùng lựa chọn này trong báo cáo trước Minh duyệt WHY.


## WHY-43 — Phát lại MicroRank trên laptop bằng khớp tuyệt đối (Minh duyệt 10/10/2026, Q-124)

**Chọn:** Minh đã quyết theo Q-124 ngày 10/10/2026 phát lại MicroRank đủ 30 RE2-TT và 22 Nezha-OB trên laptop nguồn bằng khớp tuyệt đối, không dung sai: một ca diagnostic đã có được audit hồi cứu, 51 ca mới; mỗi ca một native, native exact frozen mới một observed, observed exact native/frozen và toàn source/capture/mapping/count/operation/service/tie/Hit/cờ T-028 qua bridge v3. Pilot Nezha đo trước phần còn lại; mọi khác số hoặc kiểm không đạt dừng toàn nhánh. Minh đã duyệt theo Q-124 ngày 10/10/2026 mở rộng ngoại lệ EC2-only/current-thread Q-97/Q-100 chỉ cho phạm vi này, local4GiB/tổng12GiB/trần gói3giờ máy/2,5GiB mới và giữ gate RAM. Lựa chọn này đã quyết theo Q-124 ngày 10/10/2026, không thay Q-94; Q-111 đã rút Q-104, không dùng ngưỡng1e-9. Không dùng ca bị chặn và không chạy A′ trước đầy đủ lõi SPEC.

**Vì sao:** Ca từng vượt ngưỡng trên EC2 nay khớp tuyệt đối native–frozen và observed–native/frozen trên laptop hiện tại. Điều đó hỗ trợ thử nhánh exact ở máy vừa tái lập được ca ấy, đồng thời giữ nguyên mọi quyết định chấm và không nới tiêu chí sau kết quả. Nó chưa xác định thành phần gây drift, chưa bảo đảm ca khác sẽ exact và không biến laptop thành môi trường lịch sử đã khôi phục đầy đủ. Cần trung gian từng ca khớp để lần theo membership/own abnormal/context-only, counts, spectrum và caller/root; không lấy thành công của phép phát lại làm lời giải cơ chế.

**Phương án đã xét:** (1) Full52 laptop exact với trần local4GiB, giữ tổng12GiB, benchmark Nezha và checkpoint; Minh chọn theo Q-124 ngày 10/10/2026 vì một diagnostic cung cấp bằng chứng khả thi của exact, nhưng dự toán còn ngoại suy. (2) Giữ local2GiB, chuyển chunk đã đóng sang EC2/hash2đầu rồi đổi nơi lưu: có thể giữ dung lượng máy, nhưng cần quyền cụ thể, đo transfer và cách audit; không tự xóa lượt cũ hoặc coi bản sao không tính trần. (3) Chỉ benchmark một Nezha rồi trình dự toán lại, chưa quyền cohort còn lại: rẻ và giảm bất định trước cam kết nhưng MicroRank/G2/A′ tiếp tục thiếu lõi. (4) Tiếp EC2 bằng tiêu chí số mới hoặc bỏ ca vượt: chưa được Minh duyệt, không dùng. Giữ Q-94 không làm ca vượt ngưỡng hợp lệ. Không suy can thiệp thread/OS sẽ sửa drift khi chưa có phép phân xử thành phần ấy.

**Bằng chứng và phần chưa kiểm:** `results/T-032/runs/microrank-laptop-diagnostic-verification-001/check.json#/status` là PASS_SINGLE_CASE_EXACT_DIAGNOSTIC; `/native_observed_frozen_exact` và `/source_input_import_function_hook_checks_passed` true; `/verified_files` giữ 77 artifact đã kiểm hash, `/closed_sha256` và `/controller_sha256` ràng buộc manifest/controller; `/pids_checked_gone` xác nhận kết thúc. `/wall_s=99,6289197` giây; `/mode_summaries/native/cost` là worker7,391556s/peak1.255,56640625MiB; `/mode_summaries/observed/cost` là worker31,634068s/peak1.522,27734375MiB; `/new_bytes_closed=30.669.327`. Ngoại suy riêng chi phí 51 ca là84,6846phút và1.564.135.677B mới, không là upper bound. Chưa đo Nezha/ca lớn, chưa đủ audit bridge v3 cho ca laptop hoặc52ca, chưa có toàn bảng ULP/relative/invariant. Diagnostic `/intermediates_eligible_for_report`, `/cohort_authorized`, `/a_prime_authorized` đều false; không đổi chúng bằng diễn giải.

Môi trường laptop hiện tại được ghi ở `results/T-032/runs/microrank-laptop-diagnostic-001/environment.json`: Python3.12.10/package nguồn, hashseed0 và năm biến thread unset; `/threadpools_current` ghi OpenBLAS hiện16threads. `/source_thread_status=OPEN` và `/current_values_are_historical_evidence=false`; không biết thread/partition lịch sử. Khớp counts hay record không chứng minh membership lịch sử từng trace bằng nhau nếu nguồn không lưu mask. Chưa phân xử drift do Python/OS/BLAS/thứ tự số học hoặc thành phần khác; một ca laptop exact không chứng minh riêng “lỗi EC2”, “lỗi Linux” hay “lỗi thread”. Pipeline observer đã exact với native ở ca này, nhưng cơ chế và eligibility của ca khác vẫn phải kiểm riêng. Giới hạn đo peak tree theo poll có thể bỏ đỉnh ngắn; không dùng peak một ca để hạ gate RAM.

LOG T-032 tại mốc16:25:58 ngày10/10 ghi local992.372.033B trước diagnostic và EC2 3.743.441.061B. Cộng diagnostic closed cho local xấp xỉ1,023GB; cộng ngoại suy51ca vượt2GiB. Đây là inventory cũ cộng chi phí, không phải đo tổng hiện tại; phải đo lại cả local/EC2/tạm/lượt hỏng trước lượt lớn. Vì vậy trần local4GiB đã được Minh duyệt theo Q-124 ngày 10/10/2026, chỉ áp trong đúng phạm vi quyết định này. Nếu pilot/dự toán mới vượt3giờ/2,5GiB mới/local4GiB/tổng12GiB hoặc gate RAM không đủ, dừng trình; không tăng ngân sách hoặc giảm kiểm để hoàn tất bảng.

**Kết luận phụ thuộc:** Minh đã duyệt phạm vi chạy theo Q-124 và nội dung đoạn WHY này ngày 10/10/2026; chỉ sau từng ca đạt đầy đủ exact/source/capture/T-028/invariant, trung gian laptop mới được dùng trong phân tích MicroRank. Lõi toàn phương pháp còn phụ thuộc đủ52bảng, nhóm/đối chứng/caller-root theo SPEC; ca non-OK exact vẫn được giữ với đúng N/A, không cấp điểm/membership không tồn tại. Full52 exact, nếu đạt, chỉ xác nhận tái lập các đầu ra trong điều kiện hiện tại; không khôi phục partition lịch sử, không chứng minh nguyên nhân vật lý caller/root hoặc lợi ích quan hệ. A′ vẫn cần toàn điều kiện lõi/khóa mẫu/nhómN/A/sham/invariant của SPEC và quyền cũ, không được kích hoạt bởi một diagnostic hay một pilot. Các phương pháp khác giữ tiêu chí riêng/exact; ngoại lệ này không áp CIRCA. Nếu benchmark/cohort làm thay đổi bằng chứng hoặc dự toán, trình đoạn bổ sung cho Minh duyệt, không sửa WHY-42 hoặc tự nâng trạng thái cơ chế/RQ2/G2.

Bổ sung 10/10/2026 (Q-126): trần gói đổi thành 5 giờ máy; cổng RAM 4.554.752.000 byte thay bằng quy tắc dừng khi không đủ RAM cho worker hoặc RAM hệ thống đạt 95%.


## WHY-44 — Các phép đổi tất định của T-032 (Minh duyệt nối ngày 11/10/2026)

Nguồn nguyên văn: `results/T-032/thiet-ke-phep-doi-001.md` mục 11 và `results/T-032/thiet-ke-phep-doi-002.md` mục 5; chi tiết từng phép nằm trong hai file đó.

**Chọn:** ngoài A′, thêm các phép đổi tất định M-C1, M-D, T-D, B-1, K-1, K-2 như trên; SimpleRCA dùng phân rã cộng, không can thiệp; TORAI B định sau khi có trung gian.

**Vì sao:** P4 đòi chỉ ra bước làm mất hoặc đánh giá sai thông tin. Quan sát chênh lệch ở một bước chưa cho biết bước đó có làm đổi hạng hay không. Đổi đúng một bước trên trung gian đã khớp, với dự đoán ghi trước, phân biệt được hai giải thích dẫn tới hai hướng thiết kế khác nhau.

**Phương án đã xét:** chỉ đọc bảng và đối chứng (không phân biệt được "nơi chênh xuất hiện" với "bước gây đổi hạng"); hạ duration hoặc xóa caller theo nhãn (dùng nhãn, kết quả hiển nhiên; WHY-40 đã bác); đổi nhiều bước cùng lúc (không quy được cho bước nào); chạy lại bộ chia trace của bài MicroRank gốc (cần quyết định adapter về thời lượng của cả trace, để riêng).

**Bằng chứng:** code ở các file đã dẫn; chưa có kết quả. Đây là kế hoạch kiểm, không phải xác nhận giả thuyết.

**Kết luận phụ thuộc:** phần "hạn chế thuộc giả định/cách tính" của bản đồ P4 và căn cứ đề xuất ứng viên P5–P6. Nguyên nhân vật lý và lợi ích của đồ thị vẫn cần bằng chứng riêng.

**Bổ sung theo bản 002.** **Chọn thêm:** B-2 (thang độ lệch chuẩn cho BARO) và S-1 (đếm theo cột cho SimpleRCA). **Vì sao:** hai bảng mô tả cùng chỉ về một ứng viên là chuẩn hóa hoặc đếm theo độ biến thiên nền; cần phép đổi để phân biệt "nơi chênh xuất hiện" với "bước làm đổi hạng". **Phương án đã xét:** đặt sàn cho IQR (phải chọn giá trị, tùy ý); bỏ hẳn cột mem (đổi tập kênh, mất cả tín hiệu của root); chỉ mô tả (không phân xử). **Giới hạn:** hai phép được nghĩ ra sau khi xem dữ liệu dev, nên kết quả chỉ là bằng chứng trên dev cho ứng viên, không phải kiểm định độc lập.


## WHY-45 — Bảng mô tả, phép đổi thêm và gói bổ sung của T-032 (Minh duyệt ngày 11/10/2026)

Nguồn nguyên văn: results/T-032/thiet-ke-bang-mo-ta-004.md, thiet-ke-phep-doi-003.md, -005.md, -006.md, goi-bo-sung-007.md.

**Chọn:** (1) bốn bảng mô tả không gọi phương pháp, nối nhãn sau cùng: vị trí tín hiệu của root trong trace; xu hướng nền của cột metric; cấu tạo thời gian của lời gọi; tỷ lệ lời gọi chậm theo cạnh. (2) Mốc đếm: cờ theo mean + 3·std của nền; lời gọi chậm là vượt phân vị 95 của chính cạnh ở nền; chỉ xét cạnh có từ 20 lời gọi mỗi phía; mốc báo cáo 50% và 20%. (3) Tiêu chí mức đo được "dịch vụ gọi chờ root" theo ca: có cạnh đủ lời gọi; ở nền, span phía được gọi dài hơn span phía gọi ở không quá 1% lời gọi; mọi chỗ gọi trong mã nguồn là lời gọi chặn ở mọi phiên bản ứng viên. (4) Phép thử giả bằng mốc lùi vào đoạn nền. (5) Phép đổi thêm: bỏ cạnh theo loại ở CIRCA; bỏ cột log ở TORAI B; bộ chia trace theo bài MicroRank gốc. (6) Bảng vị trí trên chuỗi gọi của thực thể đứng trên root; bảng nối lời gọi chậm với span mang cờ; phát lại TORAI nguồn A có quan sát.

**Vì sao:** P4 đòi chỉ ra thông tin của root nằm ở đâu, bước nào làm mất nó, và quan hệ giữa dịch vụ bổ sung được gì. Thứ hạng và cờ không trả lời được; cần bảng theo vị trí và phép đổi đúng một bước.

**Phương án đã xét:** chỉ dùng thứ hạng và cờ (không cho biết vị trí tín hiệu); so trung vị từng phần của lời gọi (che mất ca có hai nhóm lời gọi chậm); ngưỡng cố định theo mili giây (phụ thuộc cạnh); định nghĩa nhãn lan (SPEC không cho); hỏi tác giả về phiên bản Train Ticket (Minh chọn chấp nhận giới hạn).

**Bằng chứng:** results/T-032/ket-qua-phien-10.md cho phần đã chạy. Phần của gói bổ sung chưa có kết quả, là kế hoạch kiểm.

**Giới hạn:** định nghĩa vị trí, mốc đếm và phép đổi thêm đều đặt sau khi đã xem kết quả dev trước đó, nên chỉ là bằng chứng trên dev cho ứng viên. Các mốc 20 lời gọi, phân vị 95, 50% do người làm đặt; số thô được lưu. Bộ chia trace theo bài gốc cần một quy ước lấy thời lượng cả trace, chưa kiểm.

**Kết luận phụ thuộc:** bốn đầu ra đầu của P4 trong T-032; mức đo được theo ca; căn cứ đề xuất ứng viên P5–P6. Lợi ích của đồ thị vẫn cần đánh giá riêng.


## WHY-46 — Bản sửa việc 4 và các bảng thêm của gói bổ sung T-032

Nguồn nguyên văn: results/T-032/goi-bo-sung-007.md phần "Bản sửa việc 4"; thiet-ke-phep-doi-009.md; thiet-ke-vi-tri-chuoi-goi-008.md; thiet-ke-kenh-metric-010.md.

**Chọn:** (1) Bộ chia trace gọi là "công thức của bài MicroRank gốc với span đầu do ta quy ước": span đầu là span khai báo không có cha; chạy riêng hai luật (bài: mức nền cộng 1,5 lần độ lệch chuẩn; code chia nhóm: cộng 1 lần, thêm 50 ms); mức nền theo code gốc; đếm trước, ca dưới 90% trace có đúng một span đầu ghi N/A. (2) Bảng vị trí trên chuỗi gọi báo hai mốc nền: mọi ứng viên, và chỉ thực thể có span. (3) "Span chờ root": span vượt ngưỡng bao một lời gọi chậm tới root chiếm từ 50% phần vượt. (4) Bảng tỷ lệ so với số tuyệt đối của TraceRCA. (5) Bảng cột metric thắng theo vị trí và lưu lượng.

**Vì sao:** dữ liệu không có nhãn loại span nên không chạy được đúng bộ chia gốc; P4 cần biết sai lầm có nằm dọc chuỗi gọi không và span nào tạo điểm.

**Phương án đã xét:** hệ số 1,5 cho cả hai luật (sai với code); trừ phần được span con che (khác code gốc, làm mất đẳng thức với thời lượng span đầu); coi mọi span mất cha là span đầu (hồ sơ P1 cấm); một mốc nền duy nhất (làm tỷ số phình vì thực thể không có span).

**Bằng chứng:** results/T-032/ket-qua-phien-11.md. Hai nhánh của (1) chưa có kết quả.

**Giới hạn:** (2) phần "chỉ thực thể có span" và (4) thêm sau khi đã xem kết quả; các mốc 90%, 50%, phân vị 95 do người làm đặt; mọi số là bằng chứng trên dev.

**Kết luận phụ thuộc:** phân loại hạn chế của MicroRank, TraceRCA, TORAI trong bản đồ P4; căn cứ đề xuất ứng viên P5–P6.


## WHY-47 — Hai phép kiểm ngoài gói cho TraceRCA và kết quả việc 4 của T-032

Nguồn nguyên văn: results/T-032/thiet-ke-phep-doi-011.md; thiet-ke-phep-doi-009.md.

**Chọn:** (1) Phép đổi công thức điểm của TraceRCA bản thư viện: giữ cờ từng span và tập ứng viên, thay điểm 2a/(n + H) bằng tỷ lệ a/n (có và không có mốc 20 span) và bằng số tuyệt đối a. (2) Bước xếp hạng của bài TraceRCA gốc, cài theo lời văn của bài: lời gọi theo cặp dịch vụ, một đặc trưng là độ trễ, nền trước mốc, ngưỡng 1 lần độ lệch chuẩn (thêm nhánh 3 lần), tập dịch vụ theo support 10% và chỉ số Jaccard, điểm trong tập là trị tuyệt đối của hiệu số trace có lời gọi bất thường vào và ra. (3) Ghi nhận hai nhánh chia trace của WHY-46 điểm (1) nay đã có kết quả.

**Vì sao:** (1) biến quan sát "điểm nghiêng về số tuyệt đối" thành kết quả can thiệp; (2) kiểm phương án dùng cạnh gọi có sẵn trong tài liệu trước khi đề xuất ứng viên mới cho P5–P6.

**Phương án đã xét:** chạy mã của tác giả TraceRCA (cần định dạng dữ liệu riêng, chưa dựng); thêm metric tài nguyên làm đặc trưng (hai dataset không cùng dạng); chỉ ghi quan sát, không can thiệp.

**Bằng chứng:** results/T-032/ket-qua-phien-11.md mục 4.2, 8, 9.

**Giới hạn:** (2) không phải mã của tác giả và không tái lập bài gốc; cả hai phép được nghĩ ra sau khi xem kết quả dev; nhánh 3 lần độ lệch chuẩn thêm sau khi thấy kết quả phép (1).

**Kết luận phụ thuộc:** phân loại hạn chế của TraceRCA và MicroRank trong bản đồ P4; lập luận "phép tính dùng cạnh gọi phải giữ hướng của cạnh" khi đề xuất ứng viên P5–P6.

## WHY-48 — Các phép kiểm còn lại của T-032 (bản thiết kế 012 và 013; Minh duyệt ngày 11/10/2026, Q-141)

Nguồn nguyên văn: results/T-032/thiet-ke-phep-doi-012.md; results/T-032/thiet-ke-phep-doi-013.md.

**Chọn:** (1) MicroRank, phép ghép: bộ chia trace theo bài gốc cùng lúc với số đếm riêng của nhóm bất thường (KT-3). (2) Bốn ca dừng vì thao tác không có ở đoạn nền: bỏ span của thao tác đó rồi chạy mã native, cho cả MicroRank và TraceRCA; đây là đổi đầu vào, kết quả không thay số đã chấm (KT-8). (3) CIRCA, bước DA: mô tả trên trung gian đã lưu phần được cộng cho từng nút và nút nguồn của nó (KT-15). (4) Mốc giả trên bảng span RE2-TT: so mốc thật với mốc giả ở cùng độ dài cửa sổ (150 giây và 100 giây, hai vị trí mốc giả), cho tỷ lệ trace bất thường và tỷ lệ span mang cờ theo thao tác (KT-1, KT-2). (5) Chuỗi cột độ trễ của root ở ba cặp ca cùng ô, lấy đúng bảng metric mà BARO nhận, đối chiếu với lời gọi chậm tới root (KT-12). (6) Bảng nối theo cây span cho nhánh ghép của MicroRank: thao tác cao nhất của thực thể đứng đầu có bao lời gọi chậm tới root hoặc span mang cờ của root không, so với mức nền của chính thao tác và với dịch vụ khác. (7) CIRCA, hai nhánh chẩn đoán cửa sổ: học trên 291 điểm thay cho 111; chấm 10 điểm ngay sau mốc thay cho 10 điểm cuối; mỗi nhánh kèm nhánh không cạnh để tính tỷ số điểm có cạnh trên không cạnh (KT-9).

**Vì sao:** sau phiên 12 còn các câu "vì sao" có cách kiểm rẻ trên dữ liệu đã có: phần MicroRank chưa giải thích sau khi thay bộ chia; cờ ở trace và thao tác không gắn với root là mức tự nhiên hay do sự cố; cột độ trễ của root phản ứng không đều; việc hồi quy theo nút cha làm tăng điểm là do lựa chọn cửa sổ hay do cách tính. Trả lời được thì bản đồ hạn chế P4 tách được phần thuộc cách tính, phần thuộc giao thức và phần thuộc dữ liệu.

**Phương án đã xét:** so mốc giả với mốc thật ở cửa sổ 300 giây (không làm được: trước mốc chỉ có 300 giây dữ liệu, nên dùng cửa sổ bằng nhau 150 và 100 giây); chỉ kiểm thao tác cao nhất theo tên (đã làm, không thấy lời gọi gián tiếp, nên thêm cây span và độ đặc hiệu); tính điểm TraceRCA của bốn ca từ số đếm thay vì gọi mã native (bỏ, vì gọi mã native giữ được bước lọc của adapter); chạy lại CIRCA với nhiều cặp cửa sổ (bỏ, hai nhánh đủ tách hai giải thích đã nêu); so hạng root giữa các nhánh cửa sổ của CIRCA (không dùng làm mốc, vì lỗi có thể chưa hiện trong 10 giây đầu); không chạy gì và giữ các câu ở trạng thái mở.

**Bằng chứng:** results/T-032/ket-qua-phien-12.md cho (1)–(3). Các phép (4)–(7) chưa có kết quả khi ghi mục này; kết quả sẽ ở results/T-032/ket-qua-phien-13.md.

**Giới hạn:** mọi phép là chẩn đoán trên 52 ca dev, nghĩ ra sau khi đã xem kết quả dev; các mốc đọc do người làm đặt trước khi chạy và không phải ngưỡng của phương pháp; (1) đổi hai bước cùng lúc; (2) và (7) đổi đầu vào hoặc cửa sổ đã khóa nên chỉ là nhánh chẩn đoán; (4) dùng cửa sổ ngắn hơn giao thức và chỉ làm được ở RE2-TT; (5) chỉ ba cặp ca; (6) dựa trên rất ít trace bất thường ở Nezha-OB. Dự đoán của (3) và (6) viết sau khi đã thấy một phần dữ kiện, ghi rõ trong file thiết kế.

**Kết luận phụ thuộc:** phân loại nguồn hạn chế (cách tính, giao thức, dữ liệu) của MicroRank, TraceRCA, CIRCA và kênh metric trong bản đồ P4; cách ghi bốn ca ERROR ở bảng G2; căn cứ đề xuất ứng viên P5–P6 (tiêu chí trace bất thường, bước lan điểm, hồi quy theo cấu trúc). Không kết luận nào về hiệu quả của phương pháp mới hay về tập test phụ thuộc vào mục này.

## WHY-49 — Phân xử các câu còn giá trị T-032 trong gói bổ sung chung

Minh cho thực hiện theo Q-144. Thiết kế chi tiết trước kết quả: results/T-032/runs/bo-sung-toan-dien-20261012-001/t32/design.md và README gói; file cũ chỉ đọc.

**Chọn:** matched windows/đại lượng nền và sau mốc cho return/exception, tính mọi dịch vụ trước nối nhãn; MicroRank lưu đầy đủ partition→graph→W→counts→DStar→service-max, can thiệp W×counts ở cùng support đủ điều kiện, đối chiếu native/M-D/nhánh ghép và ca đúng; CIRCA giữ tập nút và cha để tách độ dài học khỏi vị trí học/phân phối và giai đoạn chấm; probe định vị tín hiệu trên cạnh so owner-span, giữ dấu và báo missing; kiểm mã tác giả TraceRCA và TORAI A nếu dữ liệu cho phép. Phép cũ đã hợp lệ tái dùng.

**Vì sao:** các nhánh trước đổi nhóm trace hoặc cửa sổ nên chưa quy riêng trọng số/đếm, đáp ứng do lỗi, nguyên nhân độ nhạy hoặc thông tin quan hệ. Không hạng1 không chứng minh không có tín hiệu. Mỗi phép cần chuỗi trung gian và đối chứng tương ứng; thiếu support không biến thành số0.

**Phương án khác:** chỉ so hạng/đếm cờ (không phân xử); loại return hoặc ca thiếu cạnh (bỏ nhóm quan trọng); chạy baseline mới và thay bảng P3 (trái mục tiêu giữ nguồn); coi bản một đặc trưng là tái lập đầy đủ tác giả (sai đầu vào); dùng data giữ ngoài/test (chưa được phép). Các kiểm physical host/network/clock không có trường cần thiết được chứng minh giới hạn thay vì dựng nguyên nhân.

**Bằng chứng trước phép mới:** SPEC, kiem-tiep hiện tại, đầu ra T032 và MRP RQ2/P4/P5/P6, DT18/cô, LESSONS. Mọi kết quả mới CHƯA KIỂM khi ghi mục này; các giả thuyết có thể sai khi tín hiệu yếu/coverage không tương đương/support đổi hoặc nhánh khác cùng tạo chênh lệch.

**Kết luận phụ thuộc:** phân loại D/G/A/M; căn cứ đề xuất thành phần/quan sát P5/P6. Không khóa phương pháp mới, không chứng minh graph thắng/test hoặc định nghĩa nhãn lan vật lý. Lựa chọn chi tiết và các nhánh phát sinh được ghi thiết kế trước kết quả trong gói, cập nhật lý do chính thức khi khác nội dung này.

## WHY-50 — Phân xử các câu còn giá trị T-033 trong gói bổ sung chung

Minh cho thực hiện theo Q-144. Thiết kế trước kết quả nằm trong results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/; nguồn/cấu hình/số P3 cũ giữ nguyên.

**Chọn:** native sham từng ca trước nhánh mới; kiểm công thức NIW/Student-t và marginal nhất quán giữa các chiều bằng covariance principal submatrix, không dùng submatrix precision hay zero-padding. Fixed-X/d xét riêng dof=d+1→d+3, kappa1→4, precision I→4I như độ nhạy, không coi đó là lựa chọn tối ưu hay lời giải contrast mask cũ. Tiền xử lý causal: schema cung cấp độc lập nhãn, ffill quá khứ, fixed-scale sau100quan sát và expanding prequential, kiểm suffix invariance, zero-range/missing/state semantics. Đầu vào lặp: compress các vector lặp và ánh xạ elapsed-time, so hazard theo hàng và theo khoảng thời gian để tách đồng hồ khỏi đếm quan sát. N-Sigma đối chiếu history rolling100/expanding cùng raw/k/cột và joint flags của OR, std0/NaN; chấm đường nhạy endpointD trên cờ cũ; đọc toàn message/coverage của vùng khóa và probe vai trò quan hệ.

**Vì sao:** νnative=d+1 chưa tự là prior khác ở common dimensions; cùngX/cờkhác cần xét state. Lookahead đã xác nhận không tự chọn được pipeline online. Lặp84%ô chưa chứng minh tác động. Mốc/endpointproxy không phải onset/end thật. Causal contract không tự bảo đảm nhất quán tọa độ posterior khi scale đổi; nếu không đạt thì giữ đúng lỗi mô hình/diagnostic, không chọn P6.

**Phương án khác:** gán effect mask cho prior (không cô lập); zero-padding (mô hình khác); sweep tham số theo accuracy (thiên vị); gọi compressed row là một giây (sai đồng hồ); gọi INFO/success là nền sạch (không có chuẩn); đograph với feature/budget khác (không cô lập cấu trúc). Mức100/4/d+3 là diagnostic khai trước, phải nói giới hạn và kiểm độ nhạy cần thiết khi kết luận đổi dấu, không thêm ngưỡng theo điểm đẹp.

**Bằng chứng trước phép mới:** nguồn BARO/code frozen, SPEC, report002/kiem-tiep, bo-sung-bao-cao hiện tại, MRP/DT18/cô/LESSONS. Các nhánh mới CHƯA KIỂM; có thể không tách tác động hoặc không đủ chuẩn vật lý. Prior/state phép tính và fixture được agent ultra kiểm độc lập trước dùng số.

**Kết luận phụ thuộc:** căn cứ P6 về preprocessing/history/prior/clock và yêu cầu quan sát FlashTicket. Accuracy thật, onset/recovery, báo giả vận hành và lợi ích graph chỉ khẳng định khi có dữ liệu/đối chứng thích hợp; gói này không tự đóng RQ2/G2 hay mở test. Giữ mọi lỗi/non-OK, mẫu số/coverage riêng, không coi thời điểm phụ thuộc là quan sát độc lập.

### WHY-50 — Làm rõ phép tự kiểm trước lô mới, 12/10/2026

Native κ=1, predictive df=2 có predictive shape I; covariance Student-t không hữu hạn ở df=2. Trong kiểm marginal, lấy principal submatrix của Ψ=inv(scale) và của predictive shape khi cùng κ/df, không gọi đó là covariance hữu hạn. Fixturev1 nhầm shape2I đã dừng trước inference; giữ lỗi, bảnv2 sửa theo code và derivation độc lập.

Nhánh causal fixedscale học từ100raw đầu, transform chính100raw ấy để initialize posterior rồi chỉ release alarm từ chỉ số100; m/cờ nội bộ trong warmup không là outputonline. Schema/hyperparameters cung cấp từđầu, không lấy root/proxy. Suffixinvariance chỉ xét prefix>=100. Expanding coordinate drift là diagnostic chưa chứng minh nhất quán mô hình; không chọn P6 từ contract hay điểm. Các mức prior vẫn là độ nhạy fixedX/d, không giải thích contrast mask bằng cách gọi dof danh nghĩa đổi là prior riêng.

### WHY-49 — Hợp đồng đầu vào tác giả và cách tính giới hạn bộ nhớ, 12/10/2026

TraceRCA default cần latency/http_status và lịch sử, encoder import module không có trong repo tác giả. Nhánh supported chỉlatency chạy code feature-selection/flags cùng shortreference, haiđơnvịms/us dođơnvịdefault chưa xácminh và thresholdCLI1/Makefile3 khai trước. Selectorcode gốc sort arrays và chỉ xét pair cóhistory; pairthiếunền bịloạiqua featureselector nên cachefallbackcurrent khôngkíchhoạt ởnhánh này. Không gọi đây là táilập default/bài đầyđủ.

Full003 bị OOM ởPID214300 lúc12:26:24UTC; code giữ mọiFP vàtracecache. Giữkernel/script/progress, 13ca đã xử lý chỉ ởRAM nên khôngmạonhận là13đầura hợp lệ. Dùng backend streaming orderedFPgenerator nguyênversion, tracebitsets, top100unique scorevalues, top1000patternsstable trướcsingletonfilter. CôngthứcJ/inout/key giữ nguyên; không bỏ nonsingleton trước cap. Fixture32ca, trongđó4095/16383patterns, score/pattern/rank trùng từngbit mãgốc; tiếp kiểm nhánh cap1000 và ca thật trước sốfull. Đây tươngđươngphép tính được kiểm, không phải nguyêntrạngtoànpipeline tácgiả. Ghi từngbranch ngayrafile và progresspattern đểkhôngmấttrunggian khi runhỏng.

TORAI A: ngoài probe trongcửasổnative, đọc rawdevfull hợp lệ để nối đúng start-bin15s của sourceA CSV; sourcesA cólệchlưới/fullfilethreshold. Maxcolumn khôngthay tổngservice trace; mọi thiếu match làN/A, không phải0quan hệ. Nguồn/scorecũgiữ nguyên.

### WHY-50 — Tái dựng trạng thái theo run length và phân rã marginal, 12/10/2026

Conjugatestate trướcđiểm i của runlengthr là nativeupdate trên X[i-r:i] từprior; cácrunlength cậpnhật độc lập. Tái dựng riêngstates được hỏi thay allstates/alltimes để tiếtkiệm; phải khớp storedθ/nativebatchdensity trước dùng. Pilot4nguồn đạtbitexact; giữ lượtallstates chậm/paused/terminated và timermetadata, không đổi nativeCP/mgate hay môi trường cũ.

Với FF/PF cùng SF: kiểm Xcommon thật và default NIW marginalcoherence trênstate trước phân rã jointlogpdf thành logpdfcommonmarginal cộng logpdfextraconditional. Dof danhnghĩađổi không tựlà commonpriorđổi. Posteriorparent R và evidenceextra đều cóthểkhác; tách hai gói bằng intermediate/counterfactualcùngr khi đủ, giữ interaction/undefined/mẫu số. Fixed-d priorsweep trả lời độnhạy riêng, không lấy thay bằngchứng cho contrastmask.

### WHY-49 — Phép dùng hướng cạnh cho KT5, trước kết quả bổ sung

**Chọn:** trên các đặc trưng trace đã lưu của đủ 52 ca, xét chênh lệch có dấu giữa tỷ lệ cờ của lời gọi đến và lời gọi đi. Giữ cửa sổ, ngưỡng, tập tín hiệu và cách xử lý thiếu; đối chiếu phép gắn tín hiệu cho chủ span, bỏ quan hệ, và đổi cạnh có giữ bậc với seed định trước trong thiết kế worker. Mọi service được tính trước nối nhãn. Không có mẫu ở một vế thì giữ N/A, không thế bằng 0.

**Vì sao:** KT5 hỏi thông tin phía gọi có thể đặt lên dịch vụ được gọi ở bước nào. Chỉ bảng incoming/outgoing chưa kiểm phép tính thực sự dùng cạnh. Phép nhỏ này cô lập cách ánh xạ/hướng cạnh trên bằng chứng đang có; không phải một phương pháp P6 đã khóa hoặc đánh giá hiệu quả.

**Phương án khác:** dùng hạng của phương pháp cũ như giá trị đồ thị (không cô lập); đổi thêm đặc trưng/ngưỡng/cửa sổ (không phân xử cấu trúc); coi missing là im lặng (sai dữ liệu). Chênh lệch tỷ lệ không tự là tự xử lý hoặc chờ đồng bộ và có thể nhạy với support/mixture; vì vậy lưu cả tử số, mẫu số, missing và đối chứng. Kết quả mới chưa kiểm khi ghi lựa chọn này.

**Kết luận phụ thuộc:** thông tin quan hệ đủ đề xuất ứng viên ánh xạ ở P5/P6, điều kiện thất bại khi cạnh/tín hiệu thiếu; không chứng minh đồ thị tăng accuracy hay xác định nguyên nhân vật lý.

### WHY-49 — KT7 kiểm tổng cột của dịch vụ

Probe trước chỉ cột cao nhất; TORAI cộng các cột trace của dịch vụ nên không được dùng max-column làm tổng. Chọn dựng lại mọi cột, tổng normalized share, vector root và trace/severity margin nguồn A; nối mọi operation với cây raw đúng start-bin. Thiết kế `toraiA_allcolumns_design.md` ghi trước kết quả. Phương án khác là giữ giới hạn max-only nhưng câu service sum vẫn kiểm được nên bổ sung. Không có danh tính span bật cờ trong CSV, vì vậy association cùng operation không là attribution của flagged spans hoặc thời gian chờ. Không thay baseline, không chạy lại GMM/RCD; kết luận tổng-score và hướng quan sát P5/P6 phụ thuộc phép này.

### WHY-50 — Phân phối hai EC2 và tiếp tục khi chạy qua đêm

Sau khi T32 giải phóng CPU, chuyển ca15–30 của T33 sang EC2 T32, giữ ca1–14 trên T33, mỗi máy hai worker. Payload nén chỉ khoảng3MB gồm X/time/schema/m/CP và raw cột causal; không chép ma trận posterior R, predictive density, nhãn hoặc raw toàn bảng. Source pins→compact hash và native full sham từng ca là điều kiện dùng nhánh mới. Wrapper chỉ đổi nơi đọc/assignment, không đổi engine/causal. Monitor dừng worker gói mới tại START ca ngoài ownership; giữ mọi output trước đó và ghi rõ phần vừa bắt đầu là interrupted, không là complete. Không đổi kết quả lịch sử hoặc dùng marker giả.

Lý do là giảm chờ bằng hai EC2 đang có, không tải dữ liệu lớn hay chạy thêm vô cớ. Phương án để EC2 T32 rảnh làm ETA dài hơn; copy fullR không cần và tốn dung lượng. Thiết kế/pins/lệnh ở t33/migration-design.md và t32/t33-migration-001/.

Theo quyền Minh cho chạy qua đêm và tiếp tục hoàn tất, dùng lịch45phút trong cùng chat để nhận/kiểm/tổng hợp khi hàng đợi ổn định. Không tạo task nghiên cứu hoặc chat mới. Metadata ở continuation-automation.json; tự dừng lịch khi gói hoàn tất và báo cáo. Laptop/Codex cần mở cho lượt tiếp tục, EC2 tính độc lập. Chưa lấy trạng thái detached hoặc ETA làm bằng chứng câu hỏi nghiên cứu đã xong.

### WHY-49 — KT7 không bỏ phép dựng cờ còn kiểm được

T016 đã có candidate encoder mean+3std ddof1, lọc theo CSV extent trước fit, chưa phải code generator tác giả. Vì vậy thiếu ID trong CSV chưa đủ kết luận không thể dựng flag. Chọn kiểm30dev TT theo thiết kế toraiA_encoder_design.md: hai scope threshold rawfull/CSVextent, cùng TT column mapping; kiểm nativeA moments trước dùng và giữ mọi cell lệch. Thêm interval-threshold feasibility dưới hợp đồng strict duration threshold cố định để kiểm tính nhận diện flagged subset có điều kiện. Không tối ưu threshold/đổi CSV, không gọi candidate exact là source lineage đã xác minh. All-column superset0 rootdesc cho bound0 của mọi flagged subset chỉ với mapping/coverage có căn cứ. Kết luận provenance khác giới hạn vật lý; cả hai được ghi đúng phần sau kiểm.

### WHY-49 — KT7 kiểm ảnh hưởng của các ô dựng lại lệch

Count recipe trên30ca không hoàn toàn khớp sourceA. Tỷ lệ ô khớp cao không chứng minh chênh nhỏ không ảnh hưởng severity, nhất là N ít biến thiên. Chọn một phép scalar kiểm rẻ trên cùng column support, cửa sổ và các kênh khác: thay đúng count cells của recipe đã khai, dựng lại normalized column scores/service trace sum và trace/severity margin22cặp. Không chạy lại GMM/RCD, không nhận hạngRCA mới, không chọn recipe theo sign; giữ các trường hợp source/method bất định. Phần này phân xử độ nhạy tính toán của conclusions trước provenance mismatch, không xác minh generator gốc hoặc nguyên nhân vật lý.

### WHY-49 — KT7 thống nhất predicate trước kết luận bound, 13/10/2026

Audit đã chỉ ra allcolumns loại descendant cùng service owner, còn encoder hasroot đếm mọi descendant root. HTTP column mapping có thể đổi prefix sang service con; fixture root→other→root phân biệt hai phép đếm. Chọn kiểm matched A superset và native conditional top-k của đủ22pairs bằng cùng hasroot, theo t32/kt7-predicate-design-001.md đã ghi trước chạy. Giữ source/count/bin/strict-threshold contract, support và N/A; không đổi baseline hoặc ngưỡng để cứu kết luận. Phương án chỉ giữ cross-owner observation không trả lời bound rộng đã viết nên phải kiểm thêm. Tạm thu hẹp kết luận trong root-probes-report-v2.md, chưa biết kết quả phép kiểm mới.

### WHY-50 — K5 literal backend, bổ sung sổ ngày13/10/2026

Thiết kế backend-status-design-001.md được worker ghi trước chạy; mục WHY này được nối sau lượt worker hoàn tất, không nhận đã ghi WHY trước chạy. Chọn đọc grammar Response(status=int,msg=...,data=...) và ResponseEntity literal HTTP trong đúng union vùng đã khóa, giữ row/hash/container/logger và occurrence count. Phương án chỉ UI access bỏ sót thông tin backend đã có; gán0/1 thành health hoặc gán row cho invocation khi thiếu join sẽ vượt bằng chứng. Summary đã có nhưng cần source/conservation/grammar audit trước kết luận; semantics0/1 UNKNOWN, serialized HTTP không tự là wire outcome. Kết luận K5 về vị trí/độ hạt thông tin và thiếu phép nối phụ thuộc kiểm này.

### Đính chính phạm vi kết luận phụ thuộc WHY-47 — 13/10/2026

Minh duyệt gói bảy file cùng N1, N2 trong bản kiểm lại Claude ngày 13/10/2026, lời duyệt: “DUYỆT SỬA NHƯ ĐỀ XUẤT:”. Đây là đính chính căn cứ, không chọn baseline hoặc cơ chế P6. Giữ nguyên WHY-47 và kết quả cũ để truy lịch sử.

**Câu cũ → trạng thái hiện tại:** số 0/4 và 0/8 vẫn đúng cho bản cài theo lời văn ở nhánh to_p. Số đó không xác nhận trị tuyệt đối là nguyên nhân đủ gây thất bại, không chứng minh “phương án có sẵn trong tài liệu không đủ” hoặc “phép tính phải giữ hướng của cạnh”. Không dùng các câu này làm căn cứ đã xác nhận để chọn thiết kế G2/P5–P6. Giữ dấu còn là CANDIDATE (ứng viên) để so sánh, chưa DECIDED (đã quyết).

**Bằng chứng theo cả hai cấu hình:** trong 12 cặp thuộc 10 ca có quan hệ cũ, nhánh mã tác giả latency-only, ms, ngưỡng chọn đặc trưng 1 cho root trên / hòa / dưới là RE2-TT 3/0/1, Nezha-OB 7/0/1; ngưỡng 3 là RE2-TT 1/3/0, Nezha-OB 7/0/1. Ở RE2-TT, ngưỡng 1 có hai cặp root trên vì caller có điểm mặc định −1; ngưỡng 3 có một cặp root trên vì caller có điểm −1 và ba cặp hòa đều có root/caller bằng −1. −1 nghĩa là không có singleton pattern được giữ để chấm, không phải bằng chứng vào/ra bằng nhau. Danh sách cũ thực ra liệt kê 13 cặp thuộc 11 ca: cặp thêm dev-95e164235f không có quan hệ cũ vì NO_USEFUL_FEATURE; nhánh tác giả hòa có điểm ở ngưỡng 1, NO_EVIDENCE ở ngưỡng 3. Không bỏ cặp đó hoặc gộp thiếu bằng chứng thành hòa.

**Ứng viên có trung gian:** ở bảy ca Nezha-OB có quan hệ cũ, frontend đứng đầu bản theo lời văn; sáu ca lấy điểm cao nhất từ pattern 2–3 dịch vụ, một ca từ singleton. Mã tác giả chỉ chấm singleton sau các bước chọn/cap pattern. Đây là CANDIDATE giải thích việc frontend có thể thừa hưởng J của tập dịch vụ, chưa là phép đổi riêng một bước. Hai pipeline còn khác dựng invocation, chọn đặc trưng, gắn cờ và các quy tắc giữ pattern. Chưa xác định được một bước Y đủ giải thích mọi chênh lệch; chưa kết luận bản cũ sai lời văn bài báo từ riêng khác biệt code.

**Nguồn và phụ thuộc:** results/T-032/runs/bo-sung-toan-dien-20261012-001/doi-chieu-dien-giai-review-001.md §2–3; closure-ledger-review-001.json#/h6_pair_audit và /pattern_candidate. Các mục đó dẫn từng ca về cases.json cũ và Full008; hash nằm ở manifest-review-001.json. Đủ căn cứ rút suy rộng cũ và đề xuất ứng viên; chưa đủ chọn một cơ chế, xác nhận chờ vật lý hoặc lợi ích đồ thị. Mọi cấu hình vẫn dùng dev đã nhìn.

## WHY-51. Gói trình G2: thang mức bằng chứng chung và ứng viên P5/P6 có điều kiện bác bỏ — Đã quyết (Minh duyệt SPEC T-034 ngày 13/10/2026)

- **Chọn:** hợp nhất các hạn chế của T-028, T-029, T-032, T-033 thành bản đồ G2-Hn; mỗi dòng ghi một mức bằng chứng cao nhất theo thang CT (can thiệp), ĐC (đo cơ chế), LĐ (liên hệ có đối chứng), MT (mô tả), CK (chưa kiểm), kèm mức của từng nguồn con. Câu "vì sao" ở mỗi dòng ở một trong ba trạng thái: đã xác lập ở mức X, đã loại được giải thích Y, chưa phân xử vì Z. Ứng viên P5/P6 ghi căn cứ đúng mục đích: sửa hạn chế P4, đáp ứng DT18 hoặc nhu cầu kỹ thuật. Mỗi ứng viên có mức bằng chứng thật, giải thích khác, tín hiệu dùng và dự đoán bác bỏ được trên dev; không chọn, không xếp hạng theo kỳ vọng thắng. Tách ba mức dùng bằng chứng của MRP §3: đề xuất để thử, chọn thiết kế trên dev, khẳng định hiệu quả sau đánh giá. CT/ĐC không tự đủ để chọn thiết kế; không loại ứng viên chỉ vì hiện tượng mới đạt LĐ/MT nếu có căn cứ kỹ thuật và dự đoán kiểm được.
- **Vì sao:** cô yêu cầu chuỗi hiểu phương pháp → thực nghiệm → hạn chế → phương pháp đồ thị có liên kết logic (WHY-01). Thang chung giúp không đọc liên hệ thành nguyên nhân (SL23), nhưng không thay việc xét bằng chứng cho từng mục đích. Thành phần sửa hạn chế nối với bằng chứng P4; thành phần theo DT18 hoặc nhu cầu kỹ thuật nêu đúng lý do, không dựng một hạn chế để hợp thức hóa. Giữ ranh giới giữa đề xuất, lựa chọn và hiệu quả giúp tránh thiết kế trước rồi tìm kết quả biện minh (SL1, SL22). Điều kiện bác bỏ khai trước giữ QT4.
- **Phương án đã xét:** giữ nguyên bốn bản đồ riêng (người đọc phải tự hợp nhất, dễ đếm trùng); xếp hạng hạn chế theo "mức đáng kể" khi chưa có định nghĩa được chọn (không đủ căn cứ); viết luôn spec P6 trong gói G2 (vượt phạm vi tổng hợp, MRP đặt lựa chọn sau G2); chỉ cho ứng viên mức CT/ĐC hoặc bắt mọi thành phần dẫn hạn chế (trộn ngưỡng đề xuất với chọn thiết kế và bỏ căn cứ DT18/nhu cầu kỹ thuật); nêu ứng viên chỉ từ mã hạn chế mà không có lý do kỹ thuật, giải thích khác và dự đoán bác bỏ (không đủ căn cứ đề xuất theo MRP §3).
- **Bằng chứng thiết kế:** MRP §2.1, §3, §7, P4, P6; PLAN-P3-G2 §8; WHY-01, WHY-38–50, gồm phần nối ngày 13/10; LESSONS SL1, SL14, SL20, SL22, SL23, QT4, QT15.
- **Kết luận phụ thuộc:** quyết định G2 của Minh; spec P5/P6 dẫn G2-Hn cho thành phần nhằm sửa hạn chế, và dẫn căn cứ DT18 hoặc nhu cầu kỹ thuật cho thành phần khác; câu trả lời với cô về P3/P4. Thang mức bằng chứng là quy ước của dự án, không phải chuẩn ngoài; gói tổng hợp không tự xác nhận cơ chế còn mở hoặc lợi ích đồ thị.

### Bổ sung WHY-51 — Hai phép phân xử trong T-034, Minh duyệt 13/10/2026

- **Chọn:** thực hiện E1 can thiệp riêng quy tắc pattern trên cùng trung gian TraceRCA và E2 tính BOCPD đầy đủ trong miền log trên hai ca underflow, gồm FF/PF liên quan; giữ native sham, fixture, nguồn và baseline cũ. Thiết kế chi tiết trước nhánh đổi theo SPEC; không tối ưu tham số hoặc chọn phương pháp P6.
- **Vì sao:** E1 phân biệt đóng góp của quy tắc chấm với các khác biệt pipeline và giả thuyết chờ/lan; E2 phân biệt tác động tính toán số học với giới hạn của mô hình. Cả hai có kết quả có thể làm đổi mức kết luận P4 hoặc căn cứ đề xuất P6. Biết có underflow hoặc thấy thứ hạng hai pipeline khác nhau chưa trả lời tác động riêng này.
- **Phương án đã xét:** chỉ tổng hợp OPEN (giữ kết luận trung thực nhưng không hoàn thành phép còn làm được có giá trị); dùng chênh hai pipeline hoặc frozen-normalizer lineage thay can thiệp đầy đủ (không cô lập yếu tố hoặc chưa cập nhật đầy đủ posterior); chạy lại mọi baseline/tối ưu tham số (vượt câu hỏi cần phân xử). Chọn hai phép gọn với danh sách ca từ nguồn hiện có và kết luận theo điều kiện.
- **Bằng chứng để giao kiểm, chưa là kết quả:** `results/T-032/runs/bo-sung-toan-dien-20261012-001/closure-ledger-review-001.json#/pattern_candidate`, `/remaining_current_declared_computations`; bản đối chiếu đính chính §3 và §8; `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/zero-lineage-summary-001.json#/cases`, `/interpretation`. Quyền mới: lời Minh đưa hai phép vào T-034 trong SPEC. Số liệu mới chỉ được dùng sau kiểm tương đương và manifest của T-034.
- **Kết luận phụ thuộc:** mức quy nguyên nhân ở K3, ứng viên K5 và câu còn mở K6; nếu một phép không phân xử, ghi đúng phần đã kiểm và phần thiếu. Không tự đổi baseline, khóa thiết kế, xác nhận lan vật lý hoặc suy detector tốt hơn/lợi ích đồ thị. Phân công máy là lựa chọn thực hiện có thể đổi trong phạm vi tài nguyên đã duyệt, không là lựa chọn khoa học.

## WHY-52. Đồ thị phụ thuộc ở P5: mô hình chung hai mức, đầu vào của bộ dựng và cách tách task — Đã duyệt nội dung (14/10/2026, Q-150; SPEC T-035)

- **Chọn:**
  1. **Một mô hình chung phủ nhu cầu FlashTicket.** Nút: dịch vụ, gateway, cơ sở dữ liệu, cache, broker, nhà cung cấp danh tính, đối tác ngoài, máy. Cạnh: gọi, thông điệp, dữ liệu, triển khai. Thêm kiểu "gọi chưa phân kiểu" khi trace không có loại span. Phần dataset công khai thiếu được ghi là thiếu, không bỏ khỏi mô hình.
  2. **Mỗi nút, mỗi cạnh ghi nguồn bằng chứng:** trace, nguồn khác của dataset, tĩnh, suy ra.
  3. **Hai mức.** Mức thực thể là mức chính. Mức thao tác là lớp tùy chọn; mỗi thao tác thuộc về một thực thể; đặc tả v0 định nghĩa phép chiếu, cách giữ quan hệ nội bộ và thành phần không có thao tác quan sát được. Đây là phương án phải khảo sát ngay trên mọi ca dev, chưa chọn làm phương pháp P6.
  4. **Thông điệp đi qua nút broker** (phát → broker → nhận). Cạnh logic gửi → nhận chỉ suy ra khi có bằng chứng nối một bản tin cụ thể (ngữ cảnh tạo/link có nghĩa đã xác minh hoặc định danh bản tin trong phạm vi phù hợp). Cùng correlationId giao dịch không đủ.
  5. **Bộ dựng nhận** bảng span mở rộng, một khoảng thời gian, alias, universe; không nhận mốc tiêm, tên ca, đường dẫn, nhãn.
  6. **P5 xuất cấu trúc, độ phủ, địa chỉ tín hiệu;** không xuất tín hiệu hay điểm.
  7. **Tách P5** thành T-035 (từ trace) và T-036 (kiến trúc, so hai nguồn). P9a nhận danh sách thông tin cần theo từng quan hệ.
- **Vì sao:**
  - (1), (2): DT18 nêu ba loại cạnh và nút gồm thành phần hệ thống. FlashTicket có cơ sở dữ liệu, cache, broker, Saga, callback (MRP §1; B16 §1, §3, §5). Trace RE2-TT không có cột loại span (`results/T-002/local-inspection/run-002/cases.json`, `typed_span_kind_column`). Trace Nezha-OB chỉ có tám cột, không có loại span (`results/T-008/runs/file-audit-001/summary.json`). Bỏ khỏi mô hình mọi thứ dataset công khai thiếu thì mô hình không còn phủ đề tài. Gọi mọi cạnh cha–con là "đồng bộ" thì khẳng định điều dữ liệu không ghi. Căn cứ: đáp ứng DT18 và nhu cầu kỹ thuật, không phải sửa hạn chế P4.
  - (3): Minh giữ phương án dựng thao tác thành nút (14/10/2026). Các ứng viên G2 mục 5 cần thông tin mức lời gọi và cây lời gọi. Lớp thao tác giữ thêm phân biệt về tên và quan hệ thao tác so với gộp theo thực thể; không thay thế cây span và thời gian của từng lần thực thi. Bảng C5 chỉ rõ ứng viên nào còn cần dữ liệu span gốc. Lợi ích của mức thao tác chỉ kiểm ở P6.
  - (4): B16 §3 cho phép consumer dùng link thay quan hệ cha–con; bên gửi, bên nhận xử lý ở hai thời điểm. Nút broker giữ được hàng đợi làm nơi gắn metric (B16 §5: queue ready/unacked).
  - (5): luật cứng 6; cùng một mã cho hai chế độ và cho FlashTicket (WHY-08).
  - (6): MRP đặt việc chọn tín hiệu ở spec P6.
  - (7): nguồn tĩnh phụ thuộc lược đồ của T-035; gộp lại thì không vừa một phiên.
- **Phương án đã xét:**
  - Gán "đồng bộ" cho mọi cạnh cha–con: sai khi có gọi bất đồng bộ.
  - Suy kiểu từ tên bằng biểu thức chính quy: lặp SL34.
  - Chỉ mức dịch vụ: mất phương án Minh muốn giữ.
  - Chỉ mức thao tác: lệch định nghĩa nút của DT18 và tập ứng viên của baseline (WHY-26).
  - Cạnh gửi–nhận trực tiếp có thể dựng khi nối được bằng chứng, đồng thời giữ thông tin broker và hàng đợi riêng. Mô hình hiện tại chọn broker làm nút để biểu diễn rõ tài nguyên dùng chung và nơi gắn số đo hàng đợi.
  - Bộ dựng nhận mốc tiêm: đưa nhãn vào mã dùng chung.
  - P5 tính luôn tín hiệu: chọn trước P6.
- **Khảo sát Node:** bộ đọc bổ sung đặt trong `src/do_thi/`, lọc dev trước khi xuất trường, giữ kiểm nguồn và không sửa `src/p3`. Chỉ xác nhận nghĩa host khi tài liệu hoặc mã thu chứng minh nguồn định danh; ánh xạ ổn định/nhóm `Node*` không đủ. Thiếu thì OPEN.
- **Bằng chứng và giới hạn:** G2 mục 5, 6.2; thẻ T-002, T-008; B16 §3–§7. Chưa kiểm: nghĩa phía gọi/phía được gọi ở RE2-TT; tên thao tác ổn định; nghĩa cột `Node` của Nezha-OB. Fixture chỉ kiểm bộ dựng theo đặc tả của ta, không thay trace FlashTicket thật. Trace FlashTicket chưa được cung cấp hoặc chưa kiểm trong phạm vi task; không suy ra toàn hệ thống chưa có trace.
- **Kết luận phụ thuộc:** thống kê đồ thị P5; định nghĩa "lời gọi" và mức đồ thị P6 dùng; phạm vi T-036; danh sách yêu cầu cho P9a. Không là căn cứ cho lợi ích của đồ thị hay của mức thao tác.
