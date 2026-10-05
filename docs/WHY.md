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
- **Giới hạn:** chọn bản sửa không làm điểm tốt hơn; chỉ sửa hai lỗi đầu vào của bước nhân quả. Kết luận P3, P4 dựa trên bản này nói về bản cài RCAEval đã sửa; quy hạn chế cho TORAI theo bài vẫn OPEN ở các khác biệt C4–C7. Cửa sổ P3 chưa chốt (Q-54). Cách ghép (B) theo vị trí là một cách hiểu ý tác giả (chưa kiểm cách khác).
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
