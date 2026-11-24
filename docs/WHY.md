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

## WHY-02. Vì sao hiểu "graph-based anomaly detection" theo cả nghĩa hẹp lẫn nghĩa rộng — Đã quyết (Q-36); điều chỉnh hướng ngày 22/10/2026

- **Chọn:** đồ thị tham gia trực tiếp vào điểm bất thường (nghĩa hẹp). Đồng thời, khoanh vùng và xếp hạng cũng chạy trên đồ thị (nghĩa rộng).
- **Vì sao:** Minh quyết chưa hỏi cô (Q-05), nên cách hiểu phải trả lời được cả hai câu cô có thể hỏi: đồ thị phát hiện bất thường ở đâu, và đồ thị giúp khoanh vùng, xếp hạng thế nào. DT18 cũng yêu cầu cả ba đầu ra: vùng ảnh hưởng, dấu hiệu bất thường, xếp hạng nguyên nhân. Trong MicroRCA và MicroRank, PageRank chỉ chạy sau khi đã phát hiện bất thường cục bộ, tức đồ thị không tham gia việc phát hiện (K1 §D.3). Nếu chỉ làm theo nghĩa rộng, câu hỏi "đồ thị phát hiện bất thường ở đâu" không có câu trả lời.
- **Phương án đã xét:**
  - Chỉ nghĩa rộng: phát hiện cục bộ rồi PageRank. Dễ làm hơn, nhưng có rủi ro trên.
  - Hai nghĩa không loại trừ nhau. Nghĩa hẹp chỉ đòi đồ thị tham gia tính điểm bất thường; nó vẫn đi cùng được bộ khoanh vùng và xếp hạng, hoặc học chung như Eadro (K1 §C.7). Vì vậy câu hỏi thật là đồ thị tham gia ở bước nào, không phải chọn một trong hai nghĩa.
- **Chưa kiểm:** khung bốn tầng ở P6 và cơ chế tách bất thường tự sinh khỏi kế thừa chỉ là ứng viên. Cơ chế đó nhắm vào giả thuyết "nhầm triệu chứng với nguyên nhân" của P4; khả năng tách của nó chưa kiểm. Thành phần cụ thể chọn sau P4, theo dữ liệu và hạn chế thực tế. DT18 yêu cầu các đầu ra, không bắt buộc kiến trúc bốn tầng.
- **Điều chỉnh ngày 22/10/2026** (M-38 trong `docs/KE-HOACH-GIAI-DOAN-TOI.md`): tách hai mức. Mức hệ thống (có sự cố hay không) do luật cảnh báo Grafana quyết. Mức thành phần (thành phần nào bất thường, tự sinh hay kế thừa) dùng đồ thị lúc chẩn đoán; nghĩa hẹp được đáp ứng ở mức này. Nhánh đồ thị tham gia quyết định báo động hoãn (M-20).
  - Vì sao: chương 5 của báo cáo tiến độ đã trình cô theo hướng này. DT18 viết "phát hiện dấu hiệu bất thường", không bắt buộc đồ thị phải quyết định báo động.
  - Rủi ro: cô hiểu bước 2 là đồ thị phải quyết định báo động. Khi đó kích hoạt nhánh hoãn, dùng lại phần tính điểm thành phần.
- **Kết luận phụ thuộc:** cách tổ chức P6; cách đo câu hỏi về phát hiện sự cố (RQ3a).

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
- **Cách dùng sau G3 — C-15 B, Q-247 (ghi 04/11/2026):** giữ kết quả đầu của bản khóa và báo nguyên. Bản sửa sau khi dùng test để thiết kế khai rõ, báo riêng, không gọi là kiểm độc lập. Tách sửa lỗi cài đặt khỏi sửa thiết kế, giữ lịch sử và chạy lại các phương pháp chịu ảnh hưởng trong phạm vi Minh duyệt. Kiểm độc lập bản sửa dùng dữ liệu phù hợp chưa dùng sau khóa, gồm lượt FlashTicket mới. RE3-OB chỉ mở một lần cho bản cuối. Quyền mở test/giữ ngoài vẫn cần Minh duyệt riêng. “Đã xem” và “đã dùng để thiết kế” phải khai riêng; TX1 được chấp nhận có khai báo Q-60, không gọi toàn test là mù hoàn toàn. RE3 kiểm tổ hợp hệ OB/công cụ RCAEval/lỗi mã nguồn chưa có ở dev, không tách được hiệu ứng riêng hệ hoặc công cụ (T-021 §5).

## WHY-05. Vì sao chạy baseline bằng code chính thức, bản mới nhất — Đề xuất (G1)

- **Chọn:** code của tác giả hoặc của RCAEval, bản mới nhất (MRP P1 ghi revision). Kiểm tái lập so với số đã công bố. Phần khoa học giữ nguyên; phần giao thức (cách chọn mô hình, cách xử lý ca lỗi) có thể phải đổi, mỗi chỗ đổi ghi lý do (MRP P3).
- **Vì sao:** tự cài lại thì dễ đơn giản hóa đúng chỗ tạo ra giá trị của phương pháp. v1 làm vậy với MicroRCA (SL7). RCAEval cũng đã nhận rằng các baseline PageRank và CIRCA của họ âm thầm trả về thứ tự cột khi lỗi. Bản mới chỉ in thêm cảnh báo; đường trả thứ tự cột vẫn còn, nên adapter của nhóm phải tự đánh dấu ca lỗi (MRP P3). Dùng bản mới không tự bảo đảm số đúng.
- **Phương án đã xét:** dùng lại số công bố mà không chạy. Cách này không so được trên cùng giao thức, và không làm được phân tích từng ca ở P4.

## WHY-06. Vì sao đánh giá ba đầu ra bằng các độ đo khác nhau, và vì sao MRR là độ đo chính của xếp hạng — Độ đo/biên E-04 theo M-30, M-44, M-45; A4 cập nhật Q-246 (Q-211 giữ lịch sử)

- **Chọn:**
  - Phát hiện: Precision, Recall, F1 theo cửa sổ thời gian; số báo động giả mỗi giờ bình thường; độ trễ phát hiện (MRP P7). Độ đo chính của phát hiện chốt ở SPEC phát hiện (D3 của T-043).
  - Vùng ảnh hưởng: trên FlashTicket, Precision, Recall, F1 so với nhãn vùng độc lập. Trên dataset công khai chỉ báo vùng nghi ngờ có chứa root không và kích thước vùng; khi nhiều ứng viên cùng đứng đầu, tính kỳ vọng theo D20 của T-043.
  - Xếp hạng: **MRR là độ đo chính** (C-08, M-30). Mọi độ đo khác đều tính và báo (M-07): Hit@1/3/5, NDCG@5, AC@k, Avg@5, hạng của root ở từng ca, số ca thắng/hòa/thua theo cặp, mức ngẫu nhiên. Hòa tính theo kỳ vọng.
  - "Độ đo chính" chỉ dùng ở ba chỗ: chọn biến thể trên dev; câu kết luận chính; phép kiểm thống kê chính (KE-HOACH D.6).
  - Chọn trên dev theo MRR của từng cấu hình, bằng luật C và luật chọn khối của SPEC T-043 (Phụ lục C, B4; D2 trong Q-199). Không chọn theo khoảng chênh so với đối chứng.
- **Biên E-04 trên RE2-TT** (đã duyệt, M-44, M-45; đầy đủ ở KE-HOACH D.1):
  - So với TORAI B, khai trước. Không chọn lại baseline theo từng độ đo sau khi xem kết quả.
  - MRR: Δ = 0,05, dùng để kết luận. Hit@1: Δ = 2/30 ca dev, 4/60 ca test, chỉ để mô tả.
  - Cách đọc: khoảng tin cậy 95% của chênh MRR (phương pháp mới trừ TORAI B). Báo đồng thời hai câu. (1) Cận dưới lớn hơn −Δ thì đạt E-04 theo công thức; ngược lại "chưa chứng minh được". (2) Khoảng nằm trọn trên 0 là hơn; trọn dưới 0 là kém; chứa 0 là "chưa phân biệt được" theo CI danh nghĩa của giao thức. E-04 chỉ xét câu (1). Theo Q-246, lưu cận thô và cận làm tròn 12 chữ số thập phân ROUND_HALF_EVEN; dùng cận làm tròn để so strict, bằng biên không đạt. CI suy biến (lo = hi ở cùng độ chính xác) mà qua biên phải ghi cùng câu "đạt E-04 theo công thức; CI suy biến", kèm số ô khác 0, số ô tổng chênh âm, số ca cả hai trượt và giới hạn bootstrap. Ít ô/rời rạc có thể undercoverage cả khi lo < hi; kết quả không tự bảo đảm hiệu chuẩn sai số.
  - Điểm ước lượng chênh không vượt Δ chỉ báo kèm; không gọi là phép kiểm không thua.
  - Sức phân biệt thấp: power của câu (1) khoảng 0,19 theo giả định ở KE-HOACH D.1 (công thức ở Phụ lục C của `docs/KHAO-SAT-SAU-K1-K6.md`). Vì vậy "chưa chứng minh được" là khả năng lớn và phải báo đúng như vậy.
  - Khi không đạt, Q-246 chọn phương án (c) của KE-HOACH D.1: báo cỡ hiệu ứng/CI, câu đầu "Không đạt E-04. Chưa chứng minh được không thua quá 0,05". Đã đối chiếu mức TORAI B hơn SimpleRCA TT dev khoảng 0,02556 MRR (T-034/bang-baseline.json#/ranking_mode_a/RE2-TT_dev30/methods). Mức đó chưa đủ thiết lập biên M1/M2 mới, nên giữ 0,05. Q-211 mục 8 và lý do từng không chọn (c) giữ là lịch sử; cách mới giữ câu thất bại bắt buộc để không làm mềm kết quả. Phương án thống kê (b)/(c) này khác RCA chế độ (b) được hoãn Q-245.
  - Nezha-OB không đặt Δ.
- **Phép thống kê** (A4, Q-246; khóa trước G3; Q-211 là lịch sử của phần được thay):
  - Giữ câu chính E-04 trên 60 ca TT so TORAI B và câu phụ Hit@5 trên test Nezha-OB so SimpleRCA M4. Thay Holm bằng chuyển mức một chiều: OB ban đầu p ≤ 0,025, nâng 0,05 chỉ khi E-04 tại P qua biên và lo < hi. TT không nhận mức từ OB. Chỉ P quyết A4, S_lo/S_hi là độ nhạy; không chọn world thuận lợi. TORAI B đã Hit@5 = 1 trên TT dev nên không đặt giả thuyết Hit@5 TT.
  - E-04 dùng cận bootstrap trên, mức một phía danh nghĩa 0,025. OB đảo dấu nguyên ô một phía tại 0, trọng số theo ca, H0 là bất biến dấu vector tổng chênh theo ô (KS-08); liệt kê p chính xác không tự chứng minh kiểm định chính xác dưới giả thuyết chỉ nói trung bình ≤ 0. Hiệu lực chuyển mức danh nghĩa 0,05 phụ thuộc từng phép kiểm; bộ lọc lo < hi không sửa undercoverage bootstrap. Chuyển đảo dấu TT quanh 0 thành phép nhạy, không dùng đảo dấu dịch biên làm kiểm E-04. Đây là cả hai thay đổi so Q-211, không chỉ đổi Holm.
  - Bootstrap cặp theo ô dùng lại src/p3/danh_gia.bootstrap, 10.000 mẫu, seed 20261005 theo WHY-28, trung bình seed mỗi ca trước lấy lại ô. Lưu code/numpy/thuật toán/phân vị/thứ tự ca/ô. Báo số ô hữu hiệu/cả hai trượt/CI suy biến và cảnh báo ít ô. Số mô hình giả về ô thưa không là ước lượng xác suất trên test. Khoảng chứa 0 ghi "chưa phân biệt được".
  - Hoán vị theo ca và McNemar Hit@1 là phụ, báo giới hạn phụ thuộc giữa ca cùng ô. McNemar hai phía dùng một cặp nhị phân/ca: seed TORAI đạt nếu status OK và root chắc hạng 1; ca đạt nếu ≥2/3 seed, all-3 báo độ nhạy; M1 đạt khi root chắc hạng 1. Lỗi là 0. Bảng chính vẫn kỳ vọng hòa/trung bình seed. Không coi ba seed là ba ca. Bỏ Wilcoxon như Q-211.
  - Các phép so khác (Nezha-OB, RE3-OB, T13, đối chứng): chỉ báo cỡ chênh kèm khoảng tin cậy. Không gộp dataset.
  - Ca lỗi tính là trượt; báo thêm bản loại ca lỗi để xem độ nhạy. Ghi sổ mỗi lần xem test.
  - Vì sao một giả thuyết chính: thử nhiều giả thuyết rồi chọn cái đạt dễ cho kết quả may. Cái giá: kết luận chính hẹp.
  - Chế độ (b) đợt P7 chính hoãn Q-245, G4 báo thiếu P/R/F1 M1 công khai. RE3-OB nguyên bộ cho bản cuối theo Q-247/Q-248, chưa có quyền mở. C-e TT mô tả và cặp quan sát↔hợp snapshot D8 nằm trong hồ sơ xin P7, ngoài A4; quyền chạy cấp riêng.
- **Vì sao:**
  - DT18 yêu cầu ba đầu ra. Cô nêu năm độ đo. Mỗi độ đo chỉ có nghĩa với một loại đầu ra: Precision, Recall, F1 cần nhãn đúng/sai cho từng đơn vị; MRR và NDCG cần một danh sách xếp hạng và đáp án (K1 §J).
  - MRR có trong danh sách của cô, MRP P6 đã khai từ trước, và dùng toàn bộ thứ hạng.
  - Hit@3 chạm trần ở RE2-TT dev và che đúng lỗi "root ở hạng 2" mà thiết kế muốn sửa (KE-HOACH D.6, số ở `results/T-034/bang-baseline.json`). Vì vậy không làm độ đo chính.
  - TORAI B gần trần trên RE2-TT dev, nên không thể chứng minh "hơn" có ý nghĩa thống kê. Đây là lý do dùng biên không thua E-04.
- **Phương án đã xét:**
  - Hit@1 làm độ đo chính, như phân tích trước đây (M-02). Bỏ vì chỉ nhìn hạng 1 và có thể ngược chiều với các độ đo khác (ví dụ ở KE-HOACH D.6).
  - Bản E-04 đầu (M-27): đọc theo điểm ước lượng ở cả MRR và Hit@1, so với baseline tốt nhất theo từng độ đo. Đã thay bằng bản KS-07.
- **Hệ quả cần nói thẳng:**
  - Với một nguyên nhân gốc mỗi ca và nhãn nhị phân, NDCG chỉ là một hàm của thứ hạng, nên không thêm thông tin mới so với MRR. Vẫn báo vì cô yêu cầu.
  - Dataset công khai không có nhãn vùng ảnh hưởng, nên Precision và Recall của vùng chỉ đo được trên FlashTicket.
  - MRR dev của cấu hình được chọn bị lạc quan, vì được chọn trong nhiều cấu hình (SPEC T-043 B4).
- **Kết luận phụ thuộc:** câu kết luận chính về RE2-TT ở P7; luật chọn trên dev của T-043; mọi bảng so với baseline.

## WHY-07. Vì sao so với nhánh không quan hệ và với quy tắc đơn giản trên cùng đồ thị — Đề xuất (G3)

- **Chọn:** ngoài baseline, so phương pháp đồ thị với:
  - (a) cùng bằng chứng nhưng không dùng quan hệ;
  - (b) quy tắc đơn giản trên cùng đồ thị, ví dụ chọn thành phần bất thường sâu nhất hoặc sớm nhất.
- **Vì sao:**
  - (a) tách phần lợi ích do "dùng thêm tín hiệu" khỏi phần lợi ích do "dùng quan hệ". Điều này chỉ đúng khi nhánh (a) bỏ mọi chỗ dùng quan hệ, kể cả đặc trưng tạo từ quan hệ như self-time hay hồi quy theo nút cha. Biên của nhánh (a) chốt trong spec P7 ở G3; nếu chỉ bỏ một bước thì kết luận chỉ nói về bước đó.
  - (b) kiểm phép tính phức tạp trên đồ thị có hơn một quy tắc đơn giản dùng cùng đồ thị không (M-19).
- **Đã bỏ: đồ thị ngẫu nhiên giữ bậc** (Minh quyết ngày 22/10/2026, M-25 trong `docs/KE-HOACH-GIAI-DOAN-TOI.md`).
  - Lý do từng giữ: kiểm lợi ích có đến từ cấu trúc phụ thuộc thật không, hay chỉ do số cạnh mỗi nút. Trên dev v1, đồ thị ngẫu nhiên gây đúng thiệt hại như đồ thị thật ở các ca xấu nhất; nhờ vậy biết thiệt hại do cách lan truyền, không do cấu trúc (LESSONS ST5). Đợt khảo sát cũ không thấy bài RCA nào dùng đối chứng này.
  - Hệ quả của việc bỏ: kết luận chỉ nói về lợi ích của bước lan và của phép dùng quan hệ; không khẳng định lợi ích do cấu trúc phụ thuộc thật (MRP RQ3d, §6 mục 3).

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

### Bổ sung WHY-52 — Tách địa chỉ phát, queue nhận và phạm vi định danh bản tin (15/10/2026, Q-154)

- **Chọn:** tách exchange/routing phía phát, queue phía nhận và identity scope của message ID; metric queue có địa chỉ broker + phạm vi triển khai/vhost + queue. Link tạo bản tin đã xác minh có thể nối hai phía khác địa chỉ, nhưng phải kiểm nguồn và các trường phạm vi cùng hiện diện. ID fallback chỉ nhận phạm vi được xác minh và một nguồn tạo quan sát xác định; không dùng correlation hoặc che mâu thuẫn của link bằng fallback. Queue tham gia khóa cạnh và phép chiếu. Thiếu thông tin được ghi rõ, không tự suy từ destination cũ.
- **Vì sao:** B13 §5.1–5.2 quy định exchange/routing riêng và queue theo consumer, gồm sự kiện tới nhiều consumer; B16 §3 và §5 yêu cầu nối ngữ cảnh bản tin và số đo queue riêng. Hợp đồng v1 dùng chung destination cho nối bản tin và địa chỉ queue nên không phủ trường hợp này. Đây là nhu cầu kỹ thuật/DT18 về trao đổi thông điệp và ánh xạ metric, không là hạn chế RCA đã chứng minh trên dev.
- **Phương án đã xét:** chỉ bỏ so destination (không bảo đảm giữ địa chỉ queue khi gộp/chiếu); ép mọi phía chung destination (mất phân biệt queue); nối mọi bên cùng broker hoặc correlation (không có bằng chứng bản tin); giữ v1 và giao thiếu sót cho P9 (không đạt phạm vi mô hình chung của T-035). Chọn tách thông tin, giữ link/ID và điều kiện từ chối tường minh.
- **Bằng chứng / phần chưa kiểm lúc chốt:** nguồn kiến trúc và luồng code v1 xác định mâu thuẫn thiết kế; fixture mới và hồi quy chưa chạy khi viết bổ sung này. Thiết kế trước code tại results/T-035/runs/sua-n1-001/design.md. Dự kiến dev không messaging giữ nguyên, phải kiểm lại; không dùng dự kiến làm số liệu. Bản trước sửa được giữ trong thư mục before/ của lượt này.
- **Điều kiện thất bại:** namespace/ID/link được adapter diễn giải sai; source không có trong miền; nhiều lần phát không phân biệt được; địa chỉ queue thiếu deployment/vhost; routing thực khác hợp đồng. Khi đó giữ unresolved/diagnostic và không xác nhận đủ quan sát thực tế.
- **Kết luận phụ thuộc:** tiêu chí mô hình/C9 của T-035 và hợp đồng T-036/P9; không tự xác nhận trace FlashTicket thật, lợi ích đồ thị, chọn P6 hay đóng task. Kết quả kiểm phải dẫn file sau chạy; sự đồng ý sửa không là bằng chứng thiết kế đã đúng.

### Bổ sung WHY-52 — Chuẩn hóa dữ liệu thiếu, miền ID và chính sách lỗi đầu vào (15/10/2026, Q-155)

- **Chọn:** tên thao tác thiếu ở dtype pandas khác nhau đều về None trước tạo khóa. Giữ ID hiện hành và từ chối rõ va chạm giữa miền ID thực thể/component với ID thao tác; kiểm cả dựng và API project. Thời gian phải không âm, nguyên và biểu diễn được an toàn trong int64 nanosecond trước ép/cộng/nhân. Kiểu unknown không thay kiểu đã biết; hai kiểu đã biết khác nhau bị từ chối, không chọn theo thứ tự dòng.
- **Vì sao:** đặc tả đã hứa giữ tên null, địa chỉ đúng thực thể và từ chối thời gian sai; DT18-NV2 cần nút/cạnh phản ánh đúng thành phần. Phản ví dụ nhỏ đã tái lập lỗi dtype, đổi/mất đích cạnh, wrap thời gian và kiểu phụ thuộc thứ tự. Đây là sửa cài đặt/hợp đồng kỹ thuật, không là hạn chế RCA của dataset hoặc bằng chứng lợi ích đồ thị.
- **Phương án khác:** thêm namespace vào mọi ID sẽ hỗ trợ va chạm nhưng đổi địa chỉ/schema và toàn đầu ra hợp lệ; chọn từ chối minh bạch trong gói sửa tối thiểu đã duyệt. Không suy loại đích từ chuỗi ID. Bỏ kiểm thời gian hoặc chọn kiểu cuối cùng che đầu vào mâu thuẫn. Dùng một hàm project để kiểm chính nó không đủ phát hiện lỗi chung; oracle mới phải ghi đích literal độc lập.
- **Bằng chứng / chưa kiểm khi viết:** nhận xét Minh chuyển được lưu nguyên văn tại runs/sua-hop-dong-001/nhan-xet-duoc-minh-chuyen.txt. Thiết kế và oracle mới sẽ ghi trước code. Phương án sửa và hồi quy chưa chạy; dự kiến dữ liệu hợp lệ giữ nguyên phải được kiểm, chưa được dùng như kết quả.
- **Điều kiện thất bại / hệ quả:** nguồn cần dùng ID va chạm bị từ chối rõ; muốn hỗ trợ phải trình đổi namespace riêng. Metadata kiểu mâu thuẫn cần chủ nguồn xác minh, không xác định kiểu nào đúng. Quyền nhận trọn bộ dựng, K1/K5/K7 và bàn giao T-036/P9 phụ thuộc kết quả; không tự trả lời RQ3, xác nhận runtime FlashTicket, chọn P6 hoặc đóng task.


### Bổ sung WHY-52 — Làm rõ span-parent và ngoại lệ phép chiếu (15/10/2026, Q-156)

- **Chọn:** ghi đúng chính sách đã cài: cặp span cha–con tìm được trong cùng khoảng, có ít nhất một đầu PRODUCER/CONSUMER, được lưu dạng span-parent ở mức thao tác; không chiếu loại quan hệ này thành cạnh phụ thuộc thực thể. Cạnh messaging cần bằng chứng riêng theo hợp đồng. cross_entity_parent_events vẫn đếm các cặp khác chủ quản thuộc nhóm này.
- **Vì sao:** DT18-NV2/MRP P5 yêu cầu nút và cạnh có nghĩa rõ. Quan hệ cha–con của span có kind messaging chưa đủ tự xác nhận lời gọi hoặc nối bản tin. Code dựng/chiếu và bảng K5 đã có ngoại lệ, nhưng đặc tả mục 1 và câu “cặp còn lại” ở mục 3 chưa nêu nó. Đây là đồng bộ hợp đồng kỹ thuật với hành vi hiện có, không là phát hiện hạn chế RCA hoặc thay phương pháp P6.
- **Phương án đã xét:** thêm cạnh gọi cho mọi cặp loại này sẽ đổi cách diễn giải khi chưa có bằng chứng về quan hệ; chỉ dựa bảng K5 để giải thích không sửa được mâu thuẫn trong đặc tả hình thức. Chọn làm rõ định nghĩa, phép chiếu và số đếm, giữ bộ dựng.
- **Bằng chứng và giới hạn:** src/do_thi/builder.py tạo span-parent khi một đầu là PRODUCER/CONSUMER, bỏ loại này ở bước gộp thực thể và project; kiem-dung-dan.md/K5 đã ghi ngoại lệ. Phản ví dụ nhỏ đã tái lập trong bộ nhớ trước duyệt. Phép kiểm sau sửa sẽ lưu trong runs/dong-bo-span-parent-001/; không dùng việc được duyệt làm bằng chứng đã kiểm xong. span-parent là quan hệ đã gộp theo thao tác cùng witness, không giữ đầy đủ cây/thời gian từng lần thực thi.
- **Kết luận phụ thuộc:** độ nhất quán đặc tả/bộ dựng và bàn giao T-036/P9. Không khẳng định nguyên nhân vật lý, đầy đủ quan sát messaging runtime, lợi ích đồ thị hoặc đã đóng task/P5/G3/RQ3.


## WHY-53 — P5b: nguồn tĩnh, đối chiếu và chia công việc (15/10/2026, Q-157)

- **Chọn:** thực thể đầy đủ, chủ động khảo sát thao tác khi có bằng chứng; tách nguồn thiết kế/code/quan sát và khả năng biểu diễn/lợi ích RCA. Hợp đồng và công cụ chung T-036 trước; FlashTicket T-037, TT T-038, OB T-039; tổng hợp T-040. Chi tiết phương án đã duyệt lưu LOG T-036 Phiên 1, phần T-036 thành SPEC.
- **Vì sao:** DT18-NV2 và MRP P5 yêu cầu cả gọi, trao đổi thông điệp và phụ thuộc dữ liệu. Nguồn B12–B16 có các đường async, công việc nền và tài nguyên dùng chung mà trace benchmark không tự đại diện đầy đủ. Đây là căn cứ mô hình/nhu cầu kỹ thuật, chưa là bằng chứng cơ chế RCA.
- **Phương án khác:** chỉ lấy operation có trong trace sẽ bỏ yêu cầu thiết kế chưa quan sát; dựng mọi hàm vượt câu hỏi nghiên cứu và chưa có code FT mới; làm một task toàn P5b quá rộng cho một phiên; mỗi hệ tự đặt hợp đồng dễ lệch nghĩa. Chia theo phụ thuộc cho phép ba nhánh đọc nguồn độc lập, nhưng đổi hợp đồng chung và tổng hợp tuần tự.
- **Đối chiếu:** giữ graph trace, ánh xạ có nguồn; tách miền, kiểu và địa chỉ, báo giao/phần riêng hai phía với mẫu số rõ. Static không là runtime ground truth. Giữ DB logic khác instance dùng chung và producer/consumer là vai trò để không tạo tài nguyên/operation giả. So đầu mút khác xác minh kiểu. Không chọn mapping nhằm tăng khớp.
- **Bằng chứng và phần chưa kiểm:** nguồn yêu cầu/thiết kế đã xác định nhu cầu; T-036 chưa cài công cụ hoặc chạy fixture. Giả định hợp đồng dùng được cho cả ba hệ còn cần fixture và đối chiếu nguồn để phân xử. FT mới chưa có code ứng dụng theo Minh; revision ứng dụng sinh TT/OB chưa xác minh. Duyệt kế hoạch không biến giả định thành FACT.
- **Điều kiện thất bại:** mô hình không giữ được địa chỉ/ownership/instance; alias mơ hồ; nguồn sai revision; trace thiếu; mapping làm mất kiểu hoặc phạm vi. Phản ví dụ ảnh hưởng hợp đồng phải dừng phần phụ thuộc và trình sửa; không âm thầm bỏ nhóm quan trọng.
- **Kết luận phụ thuộc:** nguồn/graph và mô tả độ khớp P5b; đầu vào P6/P9. Chưa xác nhận runtime, ích lợi đồ thị hoặc đóng RQ3/RQ5/G3. Ước lượng T-036 2–4 giờ công, toàn gói 15–24, chưa đo và chưa gồm review; không suy cần EC2. Tải nguồn phải có đề xuất dung lượng/revision riêng.


### Bổ sung WHY-53 — Chuẩn bị ba SPEC, độ đủ nguồn và chi phí (15/10/2026)

**Trạng thái:** Minh duyệt ghi tài liệu đề xuất theo Q-159–Q-163. Ba SPEC chưa được duyệt triển khai hoặc tải nguồn. Phương án P5b gốc ở LOG T-036 Phiên 1 là căn cứ phạm vi; các dự toán ở đó chưa là số đã đo.

- **Chọn cho bản đề xuất:** T-037 khảo sát đầy đủ FlashTicket theo thiết kế; T-038 truy nguồn Train Ticket và so RE2-TT dev; T-039 truy nguồn Online Boutique/Nezha và so Nezha-OB dev. Thực thể đầy đủ trong snapshot đã chứng minh; thao tác khi có bằng chứng. Cùng ghim hợp đồng v1 sau sửa R1 và code T-036 theo manifest nghiệm thu, không tự chuyển sang bản mới.
- **Vì sao kiểm cả nguồn bị loại:** inventory toàn snapshot là nhận định về phạm vi nguồn, không phải về các file đã tải. Cấu hình, template, schema/interface, mã sinh/đầu vào sinh mã, build/deployment, submodule hoặc LFS có thể chứa định danh hay quan hệ. Danh sách đuôi file chưa phân xử được chúng có liên quan hay không. Đây là nhu cầu tính đúng của mô hình DT18-NV2/MRP P5, chưa là bằng chứng hạn chế hoặc lợi ích RCA.
- **Phương án khác:** tải cả repo chưa bảo đảm đọc đủ nguồn và có thể tốn dung lượng; chỉ whitelist một số loại file có thể bỏ quan hệ; chỉ lấy các service đã thấy trong trace sẽ thu hẹp inventory theo quan sát. Đề xuất kiểm toàn cây snapshot, phân loại phần đọc/loại trừ, lần theo tham chiếu liên quan và trình bổ sung đúng phần thiếu. Chưa chốt repository revision, tập tệp hoặc số byte; không tải trong lượt chuẩn bị.
- **Chi phí:** giờ công lịch sử FT 4–6, TT 4–6, OB 3–5 chỉ là dự toán CANDIDATE chưa đo, chưa gồm phản biện/chờ nguồn. Truy revision và phân xử chênh lệch có thể lâu hơn phần chạy máy. Thời gian máy, peak RAM và tổng dung lượng còn OPEN; chưa chứng minh dự toán cũ tính mọi run/lượt lỗi/lặp lại/bản trung gian. Phải tách nguồn tải, kết quả và mọi lượt cần giữ khi lập tổng; đo pilot sau khi có quyền, không giảm kiểm hoặc thu hẹp câu hỏi để vừa giờ.
- **Song song:** ba nhánh độc lập về nguồn và output sau khi từng SPEC được Minh duyệt triển khai; dùng cùng pin T-036. Sửa hợp đồng chung, ghi quyết định và tổng hợp phải thống nhất trước khi chạy phần phụ thuộc. STATE là file chung nên đọc lại và cập nhật tuần tự đúng dòng task; không tự mở/gửi chat từ quyền chuẩn bị.
- **Bằng chứng/phần chưa kiểm:** nguồn yêu cầu DT18/cô, MRP P5/P6/P9, bàn giao T-036 và phương án gốc xác định nghĩa vụ; độ đủ nguồn TT/OB, revision sinh dataset, alias runtime, phạm vi một phiên, thời gian/RAM/đĩa và lợi ích RCA đều chưa kiểm trong ba task này. T-036 được nghiệm thu chỉ xác nhận công cụ trong phạm vi đã kiểm.
- **Điều kiện thất bại và phụ thuộc:** nguồn bị loại chứa quan hệ; deployment không khớp revision; alias sai owner/scope; hợp đồng mất nghĩa hoặc nguồn quan trọng chưa được phép đọc. Khi đó dừng kết luận/phần xử lý phụ thuộc và trình nguồn hoặc sửa hợp đồng cần thiết. Trước duyệt triển khai phải phân xử tính khả thi một phiên; nếu quá rộng, đề xuất tách phần truy nguồn/coverage và phần dựng/đối chiếu, không tự chia mã task hoặc giảm tiêu chí. Các kết luận toàn snapshot, giải thích chênh lệch, T-040 và lựa chọn P6/P9 phụ thuộc đúng bằng chứng này.

Ngoại lệ reviewer Codex phiên sạch chỉ cho lượt soát ba SPEC T-037–039. Người làm vẫn Codex; phân công phản biện kết quả theo quy tắc và chỉ định hiện hành, không suy ngoại lệ này thành quyền phản biện kết quả hoặc ghi REVIEW.

### Bổ sung lý do: phân biệt protocol SMTP trong đối chiếu và hợp nhất phiên bản

Chọn theo Minh duyệt Q-164 ngày16/10/2026: giữ builder SMTP T037 đã kiểm; comparator optional call channel/marker SMTP ở cả hai view; unknown giữ nguyên. Vì sao: phân biệt cùng owner nhưng khác chặng protocol khi so nguồn, đáp ứng nhu cầu kỹ thuật P5/DT18-NV2, không là bằng chứng sửa hạn chế RCA. Đã xét giữ comparator cấu trúc (hợp lệ nếu chấp nhận giới hạn hiện tại), marker SMTP và schema địa chỉ tổng quát. Gói đề nghị marker; không xác minh authority/port/TLS/delivery.

Bằng chứng: T037 graph003 và delta đã duyệt; T038 nguồn MailService/config có provenance; T039 run004 có comparer132graph; preview V2 oracle29/checks và comparison-before-after chỉ chứng minh hành vi synthetic/rebuild. Full1069/132 replay và tiếp nhận chung chưa chạy ở giai đoạn đề xuất, chỉ ghi kết quả sau artifact thực. Trace thiếu channel có thể giảm giao theo thiết kế; không phải cạnh nguồn sai hoặc không có runtime. Mapping nhầm/channel suy/type tự nâng và accepted=delivered là failure. Runtime/build/instrumentation/địa chỉ vẫn OPEN cần dữ liệu chủ nguồn. Phụ thuộc: biểu diễn TT SMTP, khả năng so P5b và common pin; chưa chọn P6/khẳng định lợi ích/G3.

**Bằng chứng triển khai V2 sau lựa chọn đã duyệt:** toàn hồi quy và ba nhánh đã được chạy trong cùng phiên; xem results/T-036/runs/doi-chieu-smtp-001/completion.json và final-verification.json. Comparator-only TT/OB giữ nguyên kết quả cũ; TT thêm SMTP có đúng phần thay theo oracle, FT thiếu channel tách khỏi SMTP. Đây xác nhận hợp đồng/tiếp nhận trong miền dữ liệu đã kiểm, không là lợi ích RCA hoặc runtime proof. Giữ mọi OPEN nêu trong lý do và bàn giao.

## WHY-54 — Đối chiếu baseline Nezha-OB (T-042; Minh duyệt nội dung theo Q-189, 23/10/2026)

Đối chiếu chương trình, đầu vào và cách chấm trước khi diễn giải độ lệch Nezha-OB. Dùng lại kết quả hợp lệ; trên dev kiểm riêng hai quy ước M4 mà bài chưa khóa đủ: ngưỡng metric và đơn vị đếm cảnh báo. Thiết kế 2×2 cho phép quan sát tác động riêng và tương tác, giữ các thành phần khác. Không chọn nhánh theo mức gần số công bố. Phương án chạy ngay CLI tác giả chưa phù hợp vì chưa xác định preprocessing sinh bảng và có loader ngoài miền dev. Các phép M4 chỉ phân xử quy ước M4; không xác nhận code sinh Bảng 2. Các kết luận P4 dựa trên M4 và việc chọn baseline P7 phụ thuộc giới hạn này.


### Bổ sung WHY-54 — Tiếp tục phân xử chương trình và đầu vào (24/10/2026, Q-190)

Minh đã duyệt tiếp tục trong phiên tới khi không còn phân xử được bằng nguồn/quyền hiện có. Chọn lần chương trình gốc, rồi thay từng khác biệt có nguồn; không tìm cấu hình theo nhãn để đuổi theo số công bố. Kế hoạch trước chạy tại results/T-042/runs/continuation-001/plan.json. Giữ SPEC cũ và mọi đầu ra cũ để phân biệt lịch sử với quyền bổ sung.

Nguồn local đã kiểm có nhánh main.py riêng, nhánh NezhaRCA đăng ký CLI, mã chuyển đổi benchmark và evaluator; chưa chứng minh nhánh/revision nào sinh bảng công bố. Mã chuyển đổi giữ Duration nguyên, trong khi kernel chú thích và chia như nanosecond; log xuất time/message không có level. Vì thế so literal với đổi đơn vị có căn cứ vật lý, và so time native với timestamp datetime như một can thiệp riêng, không âm thầm sửa hợp đồng. Nhánh NezhaRCA chỉ chạy metric+trace khi không có severity thật; phép này là partial diagnostic, không giả làm chương trình đầy đủ. Sáu kênh và Network_Latency của main.py dùng timestamp từng nguồn; không đồng bộ bằng thứ tự hàng front.

MicroRank: giữ nguyên nhóm/weight khi đối chiếu Dstar2 với Ochiai được bài/code nêu; đổi riêng graph trên phân hoạch repaired và chạy nguyên kernel RCAEval để phân biệt cài đặt/đầu vào với giả định phương pháp. Dùng lại trung gian đã ghim, không lặp PageRank cho đổi công thức. Nguồn prior ở ảnh bài local được đọc trước; chỉ can thiệp nếu công thức xác định đủ. Không suy thiếu scratchpad là hết bằng chứng.

Phương án khác đã xét: gán INFO hay đoán severity (không có nguồn); mở normal/test ngoài allowlist (không được phép); cài CLI Python3.13/toàn platform để thực hiện phép thuần pandas (tốn hơn và vẫn không giải quyết hợp đồng); chạy mọi công thức/threshold rồi chọn tốt nhất (trộn lựa chọn với đánh giá). Dùng hàm AST không sửa trong RAM, fixture trước và kiểm độc lập trung gian; không chép source tác giả vào src hay phân phối code không rõ license. Đây là lựa chọn chẩn đoán nội bộ, không xác nhận quyền phát hành.

Chưa kiểm khi ghi: độ lớn/tác động của các khác biệt, lỗi graph có xuất hiện trên22dev không, formula/prior có cải thiện đúng nhóm không, exact source kernel có tái hiện điểm công bố không. Kết quả không tốt chưa bác bỏ mọi bản phương pháp; khác biệt schema/unit/evaluator chưa tự chứng minh bảng công bố sai. Nguy cơ: nhánh không phải nhánh công bố, window P3 khác normal tác giả, thiếu level/instance/span-kind, native tie do set order. Giữ riêng quan sát, can thiệp, suy luận và OPEN.

Kết luận phụ thuộc: phần giải thích độ lệch, hạn chế nào thuộc adapter/giao thức/phương pháp và nhu cầu quan sát FlashTicket; chưa chọn baseline hay thiết kế mới, chưa mở G3 hoặc nghiệm thu. Dự toán chưa đo: các phép thuần CPU local dự kiến phút, mỗi lượt dưới1giờ; không tải/cài, không mở test, không đổi code chung.


### Bổ sung WHY-54 — Severity có trong log thô và can thiệp biểu thức prior (24/10/2026, Q-190)

Probe cấu trúc log trên dev phát hiện severity thật trong JSON lồng ở message; vì thế không còn đủ căn cứ dừng nhánh log chỉ vì converter không xuất level. Lưu histogram N/A × service × giá trị severity bằng pass chỉ-log mới: probe trước không lưu chiều này, không chạy lại method hợp lệ. Sau đó chạy nguyên kernel log và vote với metric/trace N1 đã ghim, không đọc lại các modality đó. Trước chạy khóa ba hợp đồng: L0 giữ nguyên chữ severity và null; L1 uppercase các giá trị quan sát, null giữ nguyên; L2 như L1 nhưng bỏ dòng không có severity. L0/L1 đi theo hành vi code null!=INFO nên bị đếm non-INFO, không được gọi là severity lỗi đã biết. L2 là chẩn đoán với độ phủ thiếu, không phải toàn bộ log. Không gán INFO cho dòng thiếu. So khác biệt trên cùng thông tin, không chọn cách cho số tốt nhất. Kiểm hash-seed 0/1/2 trên histogram vì set iteration có thể đổi thứ tự log đồng điểm rồi đổi Borda. Đây là kiểm tính ổn định cài đặt, không lặp chọn winner.

Ảnh p06 của bài MicroRank đã khớp manifest T-015 và đọc trực tiếp Eq7. Do đó có thể đổi riêng prior bất thường sang mixture các nghịch đảo chuẩn hóa, giữ ma trận/kind/scope hiện tại. Thêm control chỉ chuẩn hóa prior cũ để tách độ lớn và hình dạng. Probe span được phép tiếp tục xác định coverage-tree kind và phân biệt với coverage-set kind code; không mặc định thiếu span.kind chặn phép đại số. Trace không đủ cây/duplicate được ghi riêng, không tự sửa theo ý. Các dự đoán tác động vẫn chưa kiểm khi ghi.

Cả hai bổ sung phân xử mất thông tin ở converter/công thức, chưa định danh script sinh bảng công bố. Kết luận lợi ích phương pháp, lựa chọn thiết kế và G3 giữ OPEN.

**Tiếp tục sau probe:** severity đã lưu histogram đủ22ca; dùng lại output hợp lệ. Cây sau end split đủ19.080 trace, không cycle/missingparent/multiroot; cây identity bỏ bản lặp chỉ để định kind, giữ occurrence trong scope/PageRank. Phân biệt coverage-tree kind với coverage-set có thể chạy bằng map hash, không cần thêm dữ liệu. Bổ sung prospective: giữ Eq7 và đổi riêng kind A; rồi đổi kind N; sau đó đổi scope occurrence sang unique operation như hai nghĩa có thể của bài. Không chọn winner. Timestamp metric:9ca có TimeStamp của adservice lệch khoảng200.000.000giây so với Time; kiểm projection trên chính hàng dev đã chọn, không nhập hàng khác ngoài allowlist. Mọi can thiệp là diagnostic, chưa xác nhận tác giả dùng chính nó.


### Bổ sung WHY-54 — Đổi riêng nguồn normal N và kiểm đầu–cuối N (24/10/2026, Q-191; trước kết quả)

Chọn thử N theo hai phút converter đã xác định, giữ A300 và chương trình/cấu hình/kênh/clock/evaluator. Lý do: có khác biệt đầu vào cụ thể còn chưa được trình phép phân xử, đáp ứng RQ1/RQ2 và kiểm độ lệch baseline P3 trước P7. Phương án kéo dài A chưa được duyệt, đổi đồng thời N/A sẽ trộn tác động; chạy sweep để khớp bài không cung cấp provenance. Dùng lại đối chứng hợp lệ, không chạy lại toàn bộ.

N thay thế là ứng viên normal, chưa được chứng minh sạch; inventory có metric trùng byte với cây dữ liệu lỗi nên không suy tên thư mục thành trạng thái khỏe. Một phút có thể chỉ có một mẫu metric. Giữ min_normal_metric=2 của M4; kênh thiếu ghi unavailable. Main native có fallback theo pool; đếm rõ, không coi giá trị fallback A là ước lượng độc lập từ N. MicroRank thiếu operation/SLO hữu hạn ghi lỗi đúng, không fill. N ngày23 nằm sau một số ca: bộ bọc truyền hai nhóm trực tiếp, giữ timestamp, kiểm tương đương trên dữ liệu mà phép chia gốc hợp lệ; không sửa core dùng chung.

Đổi N thay cùng nguồn, độ dài và số mẫu/phủ nên chỉ quy kết cho gói lựa chọn nền trong cấu hình đã kiểm. Thêm kiểm hai mẫu đầu/cuối N metric và hai nửa trace/log đủ dữ liệu để phát hiện sự thay đổi, không dùng nhãn để chọn kênh. Nó không tự xác nhận hồi phục lỗi trước; không khẳng định TT có nền sạch chỉ từ điểm cao. Giữ các giải thích cạnh tranh là CANDIDATE cho tới khi có chuỗi đầu vào -> xử lý -> trung gian -> đầu ra. Exact metric-normal, bridge và chương trình lịch sử sinh bảng vẫn OPEN dù N làm tăng điểm.

Chưa kiểm khi ghi: số mẫu/phủ thật trong hai phút, độ lớn/tác động đổi N, trạng thái đầu–cuối N và khả năng chạy MicroRank. Nếu thiếu dữ liệu, không kéo dài/nội suy hoặc đổi A để hoàn thành bảng; báo đúng phần thiếu và quyết định phụ thuộc. Không chọn thiết kế/baseline hay khẳng định lợi ích đồ thị từ phép này.


### Bổ sung WHY-54 — Kiểm số học F2 trước diễn giải (Q-191, 24/10/2026)

F2 NumPy trên một số kênh gần hằng tạo |chênh mean hai cặp|/std5 vượt cận Cauchy sqrt(5), do làm tròn mean khi tín hiệu chênh ở vài ULP. Không gọi đây là biến động vật lý. Giữ output ban đầu, tính lại riêng thống kê F2 trên đúng22dev/kênh/cửa sổ, không chạy lại method: Fraction.from_float giữ chính xác giá trị binary64 đã vào pipeline, tính mean/delta/variance bằng hữu tỷ rồi mới chuyển float cho hiển thị/std. Không epsilon/floor, không đổi ngưỡng/phương pháp hay chọn kênh. Đối chiếu counts/timestamps/min/max với F2 cũ; cận sqrt(5) là phép kiểm số học, không là ngưỡng nhận định recovery. Báo cáo dùng F2-stable-001 thay thống kê chuẩn hóa ban đầu. Lựa chọn này chỉ sửa độ ổn định số học của phần mô tả, không đổi diagnosis/score đã freeze.

## Nhóm WHY-55 đến WHY-65 — Thiết kế M1 (T-043; Minh duyệt theo Q-209, 29/10/2026)

- Chép từ `results/T-043/why-de-xuat.md` (mã WHY-M1-01 đến 11, theo thứ tự). Đường dẫn tương đối trong các mục dưới tính từ `results/T-043/`. Mã WHY-M1-xx nhắc trong văn bản ứng với WHY-55 + (xx − 1).
- Đây là lý do của thiết kế trên dev, chưa phải bằng chứng hiệu quả. "Chưa kiểm" giữ nguyên nghĩa giả thuyết (luật cứng 5).

## WHY-55. Chia N/A theo thời điểm kết thúc của span — Đã quyết (Q-209; WHY-M1-01, T-043)

- **Chọn:** span thuộc A khi end ≥ t (SPEC B1.1). Quan hệ cha–con dựng trên toàn miền; tính đặc trưng rồi mới chia (B1.2).
- **Vì sao:**
  - Cùng quy ước với MicroRank và TraceRCA ở P3, nên so với baseline không trộn hai cách chia.
  - Một span kết thúc sau t có thời lượng chịu ảnh hưởng của sự cố, nên xếp vào A.
  - Tính đặc trưng trước khi chia giữ đúng thời gian độc quyền của span cha qua mốc (fixture 44).
- **Phương án đã xét:** chia theo start (`cua_so.py` đếm `spans_N` theo start). Lệch quy ước baseline; span bắt đầu trước t nhưng chậm vì sự cố bị xếp vào N.
- **Bằng chứng:** T-032 bảng C tách trước và sau theo end của span phía gọi. Đối chiếu KS-16 khớp đúng 26/26 ca RE2-TT (LOG phiên 7).
- **Giới hạn:** span rất dài trải qua mốc mang một phần thời gian trước sự cố.
- **Kết luận phụ thuộc:** mọi đơn vị trace của M1.

## WHY-56. Điểm E4 cố định; nhánh z chỉ báo cáo (D24) — Đã quyết (Q-209; WHY-M1-02, T-043)

- **Chọn:** điểm của chuỗi là e_d của E4 (tỷ lệ vượt ngưỡng nền sau cổng kiểm định). T4b chỉ báo cáo nhánh z. Khối K không đảo E4/z.
- **Vì sao:**
  - E4 cho điểm trong [0; 1] ở mọi loại đơn vị và không phụ thuộc đơn vị đo, nên ghép được kênh đếm với kênh phân vị (fixture 76b).
  - Nhánh z nhạy với IQR nhỏ (G2-H09; fixture 76c) và phụ thuộc đơn vị khi c = 1 (fixture 76a).
  - Chọn giữa hai cách chấm sau khi nhìn số dev sẽ thêm một bậc tự do vào luật chọn.
- **Phương án đã xét:**
  - T4b quyết định cách chấm (Codex B27-4): bị thay bằng D24.
  - Nhánh z làm điểm chính: chưa có căn cứ trên dev.
- **Bằng chứng:** fixture 75, 76, 81, 82 kiểm 109/109 (`fixture/ket-qua-kiem.json`). G2-H09 không phân xử E4 với nhánh z mới (LOG phiên 6, B28-3).
- **Giới hạn (đánh đổi theo D24):**
  - bão hòa: mọi mẫu A vượt ngưỡng thì không phân biệt độ lớn;
  - trôi nền cho điểm cao khi không có lỗi (fixture 81);
  - biên ε·|q| phụ thuộc mức tuyệt đối;
  - cổng giả định mẫu độc lập (B1.3; mô phỏng AR(1) cho tỷ lệ qua cổng 7,3–38,6% khi hệ số 0,5–0,98).
  Chỉ có T4, T4b làm phép độ nhạy. Cách chấm của M1 không còn phương án thay thế ở mức quyết định.
- **Kết luận phụ thuộc:** mọi kết cục khối K và luật C; tỷ lệ `CAUSE_FOUND` ở mốc giả.
- **Bổ sung 01/11/2026 (T-045; Q-223). Phần trên giữ nguyên làm lịch sử; quyết định D24 chưa đổi.**
  - T4b trên 52 ca dev: MRR nhánh z 0,8005, R0 0,6385; RE2-TT 0,983 so với 0,718; Nezha-OB 0,551 so với 0,530 (`results/T-045/t4b.json#/MRR_z`, `#/MRR_R0`). Chỉ báo cáo, không dùng để chọn.
  - R0 và nhánh z dùng cùng cờ, tầng và tập ứng viên; nhánh z chỉ thay điểm của đơn vị phân vị bằng z không bị chặn, kênh đếm vẫn trong [0; 1] (`src/m1/chuoi.py`, khối E4). Vì vậy nhánh z đổi cả cách ghép hai loại kênh, không chỉ sửa bão hòa. Bão hòa của E4 là một ứng viên giải thích, chưa xác lập.
  - Điều số này hỗ trợ: với cùng cờ, đổi cách chấm cho thứ hạng rất khác; cổng hiện tại không làm thứ hạng tốt thành bất khả thi trên RE2-TT dev. Chưa có phép E1, E2 trên nền z.
  - Giới hạn đối chứng (LESSONS QT7, MRP §6): R0 (0,718 trên RE2-TT) thấp hơn SimpleRCA (0,891), nên E1+E2 hơn R0 chưa đủ cho khẳng định rộng về lợi ích dùng quan hệ. Nghĩa vụ đối chứng không đồ thị đủ mạnh xử lý trước khi khóa danh sách so sánh ở G3.
  - Giữ hay đổi thang điểm phải quyết trước bất kỳ lần chạy lại khối K nào (LOG T-045 phiên 2, QĐ-4, chờ Minh). Không chọn z vì MRR dev cao.

## WHY-57. Luật trạng thái quan sát trên dev (hoàn thiện D12) — Đã quyết (Q-209; WHY-M1-03, T-043)

- **Chọn:** đặc tả v1 mục 2.2, với luật F phương án (a) theo Q-207 (`dinh-chinh-phien9.md` Đ9; thay luật v1.1 đề xuất ở `dinh-chinh-phien8.md` Đ1).
  - Mỗi file nguồn phủ [bản ghi đầu, bản ghi cuối + r); r là độ phân giải mốc. F là bao các file. Khe K là phần của F không thuộc file nào (khe dương giữa hai file).
  - H là bao bản ghi của nguồn trên cả cửa sổ đang xét.
  - Phần ngoài F là XÁC NHẬN THIẾU THU khi có căn cứ phía xuất; phần trong K là OPEN; phần trong F ∩ H ngoài K là A0; phần trong F ngoài H là OPEN.
  - T^chắc = |(F ∩ H) \ K ∩ phía|; T^max = |F ∩ phía|.
  - Ô biên tách theo giây thực.
  - Metric không tham gia T.
  - Thông tin khoảng ghi đi vào phương pháp qua `params.coverage` do runner cấp (Đ2).
- **Vì sao:**
  - "Ngoài khoảng ghi của file" là bằng chứng thiếu thu mà B1.3b đã liệt kê, khi có căn cứ phía xuất.
  - Khe giữa hai file không xác định được là thiếu thu hay đã thu: nó có thể là lúc không có sự kiện, đệm khi xuất, mất bản ghi ở biên file hoặc phần không được xuất. Vì vậy khe là OPEN; ba thế giới quét phần này thay vì chọn một bên là sự thật.
  - Với Nezha-OB, căn cứ phía thu/xuất là điều kiện xuất dữ liệu: mỗi lần tiêm chỉ có ba file phút (`results/T-008/the-dataset.md` §8). Metric theo ngày cho thấy hệ vẫn chạy ngoài F: 740/740 điểm PodWorkload dương ở 22/22 ca (`runs/bien-F-001/ket-qua.json#/tong_hop`). Không suy thiếu thu từ việc không thấy bản ghi.
  - A0 nói về "khoảng có bản ghi" của nguồn, không cắt tại t.
  - Tính H riêng từng phía làm giây cuối mỗi phía thành OPEN giả khi mốc là giây nguyên (lượt thử nhanh `ks16/runs/thu-nhanh-001`).
- **Phương án đã xét:**
  - H theo từng phía: báo kèm ở `T_bien_the_H_theo_phia`.
  - Coi cả F là A0: bỏ mất trạng thái OPEN ở đầu, cuối cửa sổ khi nguồn thưa.
  - Gộp khe giữa hai file vào F làm A0 (bản v1): coi thời gian không thuộc file nào là đã quan sát.
  - Loại khe khỏi F làm thiếu thu (bản v1.1): coi khe là chắc chắn chưa thu. Cả hai cách đều chọn một bên mà dữ liệu không phân xử được.
- **Bằng chứng:**
  - KS-16 pha 1: trace và log Nezha-OB chỉ phủ 41–97 giây ở N và 84–140 giây ở A ở cả 22 ca, ở cả hai bản luật; 488/660 ô N là thiếu thu. RE2-TT không có ô OPEN.
  - Hai bản v1 và v1.1 chênh T ở 12/22 ca Nezha-OB, tối đa 1,21 s (1,01%). Số ô kích hoạt không đổi. 4/1.420 đơn vị đếm đại diện đổi quyết định cổng (`runs/so-v1-v11-004/ket-qua.json`; `dinh-chinh-phien8.md` Đ5). Đây là độ nhạy, không là sai số so với sự thật.
  - Theo (a), đơn vị đếm đại diện phụ thuộc quan sát: RE2-TT 5 (có sẵn, 0 phát sinh thêm), Nezha-OB 4 (đều do khe, đúng bốn đơn vị lật giữa v1 và v1.1) (`runs/khe-open-002/ket-qua.json#/tong_hop`).
- **Giới hạn:**
  - A0 chưa kiểm được trên dữ liệu công khai (D12). Kết luận vẫn ghi "dưới A0".
  - Mép ngoài của F lấy theo bản ghi đầu và cuối. Đây là giả định chưa kiểm, không có cận sai số. Nó sai khi việc xuất bắt đầu trước bản ghi đầu (hoặc kết thúc sau bản ghi cuối) mà không có sự kiện; khi đó T bị đánh giá thấp. Dev có khoảng không bản ghi dài tới 1,212 s giữa hai file, nên mật độ ở mép không loại được một khoảng cỡ đó.
  - Ba thế giới chỉ quét phần bất định đã đưa vào T (khe và phần F ngoài H), không bao bất định ở mép ngoài.
- **Kết luận phụ thuộc:**
  - T của mọi đơn vị đếm; OBS_DEPENDENT; dự đoán "E3b trên Nezha-OB OBS_DEPENDENT" của SPEC mất căn cứ.
  - Chế độ (b) trên Nezha-OB không được dùng `params.coverage` dựng từ file phút, vì file phút mang thông tin phút tiêm (Đ2).

## WHY-58. Span bọc dạng chặt — Đã quyết (Q-209; WHY-M1-04, T-043)

- **Chọn:** w có đúng một con, con ở thực thể khác, cha của w cùng thực thể.
- **Vì sao:** khi đó g(w) đúng là phần ngoài span bên được gọi. Dạng lỏng (cho thêm con cùng thực thể) làm g(w) trừ cả thời gian của các con ấy.
- **Phương án đã xét:** dạng lỏng.
- **Bằng chứng:** hai dạng trùng nhau ở mọi ca dev: RE2-TT 1.643.384, Nezha-OB 338.829 (`ks16/dem-khong-nhan.json#/tong_hop/*/wrap_strict`, `wrap_loose`). Vì vậy trên dev lựa chọn này không đổi kết quả.
- **Kết luận phụ thuộc:** E1 (bỏ span bọc khỏi mẫu); E2.

## WHY-59. Danh mục kênh và hướng chấm — Đã quyết (Q-209; WHY-M1-05, T-043)

- **Chọn (`hop-dong.json#/kenh`):**
  - giữ mọi cột metric có trong file;
  - tài nguyên chấm hai hướng ở mọi cấu hình;
  - tỷ lệ thành công chỉ chấm khi E3 bật;
  - metric front của Nezha-OB gắn vào `frontend`.
- **Vì sao:**
  - Theo WHY-27, không bỏ cột cho baseline; dùng cùng nguyên tắc cho M1.
  - B1.4 liệt kê "tài nguyên giảm" như một lớp riêng, không gắn với E3.
  - D2d chỉ cho E3 thêm hướng xuống cho tỷ lệ thành công.
- **Phương án đã xét:**
  - Chỉ giữ P90: là một lựa chọn riêng, lệch WHY-27.
  - Chỉ chấm tài nguyên giảm khi E3 bật: SPEC không gắn hướng này với E3.
- **Bằng chứng:** chưa có bằng chứng dev cho bất kỳ phương án nào. Đây là quy ước đặt trước thực nghiệm.
- **Giới hạn:** nhiều phân vị tương quan làm tăng "số kênh" trong khóa K.
- **Kết luận phụ thuộc:** R0 và mọi cấu hình. Đổi sau khi xem số dev là thay đổi thiết kế, phải trình Minh.

## WHY-60. Hợp đồng severity theo nguồn — Đã quyết (Q-209; WHY-M1-06, T-043)

- **Chọn:** ánh xạ theo từng nguồn; UNKNOWN không tính là lỗi hay không lỗi; kênh severity gọi đúng là "mật độ dòng lỗi có severity xác định"; NO_BASELINE, NO_A khi không có dòng xác định.
- **Vì sao:**
  - So khớp nguyên chữ `ERROR` cho 0 dòng lỗi, vì giá trị trên dev là chữ thường (T-042 `continuation-001`, `#/values`).
  - Tiền lệ T-042 chỉ hỗ trợ ý "cách đọc trường ảnh hưởng kết quả" (`results/T-042/runs/continuation-001/bao-cao-bo-sung.md:18`). Nó không là bằng chứng cách đọc nào cho RCA tốt hơn (LOG phiên 6, B26-3).
- **Phương án đã xét:** đổi UNKNOWN thành INFO (che thiếu thông tin); đặt ngưỡng độ phủ (chưa có căn cứ).
- **Bằng chứng:** KS-16: adservice và cartservice có log nhưng không có severity xác định ở cả N và A (`ks16/dem-khong-nhan.json#/cases/*/log`).
- **Giới hạn:** độ phủ severity khác nhau giữa N và A vẫn OPEN (N9). Chưa có căn cứ chọn cách hiệu chỉnh. Mục này không quy định cách phân loại mẫu Drain khi có UNKNOWN; phần đó ở `dinh-chinh-phien10.md` Đ15.
- **Kết luận phụ thuộc:** kênh log lỗi cơ bản (E3 tắt) ở Nezha-OB; phân loại mẫu Drain khi E3 bật (Đ15).

## WHY-61. Chưa dùng nối log–span trong bản P7 (lựa chọn ưu tiên phạm vi) — Đã quyết (Q-209; WHY-M1-07, T-043)

- **Chọn:** E3 đếm theo thực thể và thời gian. Nối log–span là ứng viên chặng 2, khóa trước chặng 3 (`bang-chuyen-giao.json`, dòng `log_span`).
- **Vì sao:** ưu tiên phạm vi. Dùng nối cần thiết kế thêm: kênh (a) và trạng thái khi thiếu liên kết; hợp đồng E5 theo request cho (b); phạm vi phép thử. Phạm vi phép thử chưa thiết kế, nên chưa nói được phải nhân rộng khối K hay không. Chưa ước lượng phần việc. Đây không phải kết luận rằng nối quá tốn hay không thử được trên dev.
- **Phương án đã xét:**
  - Một lõi có nhánh khi thiếu liên kết (dùng nối ở Nezha-OB, nhánh không nối ở RE2-TT). Khả thi, không trái WHY-08: WHY-08 đòi một lõi và định dạng chung, không đòi mọi dataset có cùng loại thông tin; E3 hiện đã có nhánh theo dataset (severity ở Nezha-OB, từ khóa ở RE2-TT).
  - Ứng viên khi dùng: (a) tỷ lệ lần thực hiện thao tác có log lỗi; (b) E5 theo request trong cùng trace (SPEC E3).
- **Lý do cũ đã rút** (`dinh-chinh-phien10.md` Đ18): "dùng nối ở một dataset làm phép tính khác nhau giữa hai dataset"; "chưa có câu hỏi trên dev mà nối phân xử được".
- **Bằng chứng:** RE2-TT không có cột ID, không thông điệp nào chứa chuỗi hex 32 ký tự (KS-16 pha 1). Nezha-OB: 1.537.834/1.539.335 dòng khớp đúng một span (99,90%), 1.501 dòng không khớp, 0 dòng lệch thời gian (`ks16/dem-khong-nhan.json#/cases/*/log_span_join/tong`).
- **Câu hỏi OPEN:** nối log–span có cải thiện RCA không. Nezha-OB dev phân xử được câu này.
- **Dự toán (chưa kiểm; `dinh-chinh-phien10.md` Đ22):** code nối và số đo KS-16 dùng lại được (pha 1 trên 22 ca Nezha-OB, gồm nối: tổng 92,2 s, RSS tối đa 1,41 GB). (a) khoảng nửa đến một phiên thiết kế cộng phản biện, phần cài trong task cài đặt (1); (b) ít nhất một phiên thiết kế riêng. Phép thử đề xuất: một cặp bật/tắt (a) tại cấu hình thắng, chỉ Nezha-OB. Cache M1 chưa có sẵn.
- **Giới hạn:** hoãn có thể đẩy một phép phân xử khả thi trên dev ra sau, làm tăng phần phải thiết kế và đánh giá ở chặng sau. Chưa có bằng chứng buộc phải cài nối ngay, cũng chưa có bằng chứng bỏ nối không mất lợi ích.
- **Kết luận phụ thuộc:** E3, E5; bảng chuyển giao (dòng `log_span`).

## WHY-62. E5 có tương quan giữ ở trạng thái ứng viên (bước 1 của SPEC) — Đã quyết (Q-209; WHY-M1-08, T-043)

- **Chọn:** chưa đưa vào `ma-tran-thu.json`.
- **Vì sao:** chưa có hợp đồng khả thi trên dev (thẻ MicroHECL).
- **Hợp đồng nếu sau này đề xuất phải ghi:**
  - **chuỗi được so:** metric của cạnh hiện tại và cạnh kề, cùng loại tín hiệu;
  - **cách căn thời gian:** cùng lưới theo phút hoặc 10 giây, mốc theo end;
  - **số mẫu (cấu hình được dẫn):** MicroHECL dùng 60 điểm; đây là cấu hình của bài, không là số mẫu tối thiểu chung. Dev có 5 + 5 điểm metric ở Nezha-OB; trace Nezha-OB chỉ có 4–9 ô 10 giây ở N và 8–14 ô ở A;
  - **chuỗi hằng:** tương quan không xác định, nên không tỉa và ghi UNSUPPORTED;
  - **thiếu dữ liệu:** không nội suy;
  - **điều kiện thất bại:** hai chuỗi trôi cùng chiều (RE2-TT metric 1 giây, tự tương quan) có tương quan cao mà không có quan hệ nhân quả; bão hòa; trễ pha.
- **Kết luận phụ thuộc:** fixture 57 (điều kiện thất bại của E5) vẫn chưa có cách sửa đã kiểm.

## WHY-63. Định nghĩa ô kích hoạt và kiểu quan sát O1–O4 — Đã quyết (Q-209; WHY-M1-09, T-043)

- **Chọn:** `dinh-nghia-pha2.json`, băm trước pha 2 của KS-16.
- **Vì sao:**
  - Ô kích hoạt E_X là nhóm ca mục tiêu khai trước của thành phần. Định nghĩa dựa trên dữ liệu và nhãn của chính ca, không dựa trên đầu ra M1 (chưa cài).
  - E_X không là điều kiện cần để hạng root đổi: thành phần có thể đổi hạng root ở ca ngoài E_X qua điểm của thực thể khác (`dinh-chinh-phien9.md` Đ10). E_X cũng không là bằng chứng cơ chế, lợi ích hay khả năng chuyển sang FlashTicket.
  - Luật C giữ nguyên (Q-207): P > M trong E_X là yêu cầu ưu tiên lợi ích trong nhóm mục tiêu, là chính sách chọn trên dev. Nếu chưa dừng ở bước 1–4, ca có ΔMRR gộp > δ nhưng P ≤ M tới bước 7 (Minh quyết). P ≤ M không có nghĩa lợi ích chỉ nằm ngoài nhóm (`dinh-chinh-phien10.md` Đ17). Luôn báo P′, M′. Câu hỏi cơ chế xét bằng trung gian từng ca; chuyển giao xét ở P10.
  - E1, E2 dùng đúng định nghĩa của số xem trước trong SPEC (8/11, 2/6), nên số T0 khớp số xem trước.
  - SPEC không định nghĩa O1–O4 (LOG phiên 7, R7-2). Người làm đặt theo điều kiện thất bại S7, G2-H19 và luật "quan sát được" B1.9.
- **Phương án đã xét:**
  - E3 theo dữ liệu (log lỗi root tăng) thay cho theo loại lỗi mã: lẫn tác dụng với điều kiện.
  - E5 theo cờ M5 của một baseline duy nhất: hẹp và phụ thuộc baseline được chọn.
- **Bằng chứng:** `ks16/dem-sau-ghep-nhan.json#/o_kich_hoat`. E3 có 4 ô nên là thành phần ít ca. Các thành phần khác ≥ 6 ô.
- **Giới hạn:** ô kích hoạt của E5 dùng M5 trên bản ghi baseline. M5 là đồng xuất hiện, không đo đủ mệnh đề "lan" (`results/T-028/codebook.md:95`). Các giới hạn khác của nhóm mục tiêu ghi ở `dinh-chinh-phien9.md` Đ10.
- **Kết luận phụ thuộc:** "thành phần ít ca" trong luật chọn khối (E3 bị ép bật nếu không HẠI, D2a); P, M của luật C (Q-207): nhãn kết cục ở bước 8 của khối K; quyết định ở T6, T9, T11, T12 và K-b.

## WHY-64. C-h (PRISM) giữ ở trạng thái ứng viên, chưa vào bản P7 — Đã quyết (Q-209; WHY-M1-10, T-043)

- **Chọn:** chưa đưa C-h vào T13. C-h là ứng viên (`dinh-chinh-phien10.md` Đ16).
- **Vì sao:** định nghĩa hiện có chưa xác định được từ đầu vào tới thứ hạng. Còn thiếu: có dùng cổng và cờ E4 hay không; chấm tuyệt đối hay theo hướng; tỷ lệ thành công khi R0 tắt E3; gộp theo thời gian (phụ lục PRISM chưa cho đủ quy tắc); thang khi IQR = 0; kênh thiếu; thực thể không có thuộc tính bên ngoài. Chọn cách xử lý sau khi thấy kết quả sẽ làm phép so khó diễn giải.
- **Phương án đã xét:**
  - Giữ C-h với định nghĩa hiện có: không chọn, vì người cài phải tự thiết kế tiếp.
  - Hoàn thiện công thức ngay: chưa đủ nguồn (gộp thời gian). Bài PRISM đưa một họ điểm lệch với thang dương; IQR chỉ là một lựa chọn.
- **Hệ quả:** chưa có phép so với quy tắc phân biệt thuộc tính nội bộ và bên ngoài, không dùng quan hệ. Các đối chứng đã duyệt khác giữ nguyên.
- **Điều kiện thêm lại:** công thức khóa trọn vẹn trước khi chạy, ghi phần kế thừa PRISM và phần tự thích nghi, Minh duyệt. Khi đó phép so với M1 vẫn trộn cách chấm và cách dùng quan hệ, nên không dùng riêng để quy lợi ích cho E5.
- **Kết luận phụ thuộc:** T13 (RQ3d chỉ còn các đối chứng C-a0, C-a1, C-d1, C-d2, C-d3).

## WHY-65. Thực thể có dữ liệu nhưng không có kênh OK thì không trả về — Đã quyết (Q-209; WHY-M1-11, T-043)

- **Chọn:** ghi `NO_VALID_CHANNEL`, không trả về, RR = 0 nếu là root; báo riêng số ca.
- **Vì sao:** đây là cách đọc đúng câu "thực thể có ít nhất một kênh OK được xếp theo ba tầng" của B1.6. Xếp thực thể không có phép chấm nào là xếp ngẫu nhiên, trái WHY-26 ("điền phần thiếu cho phương pháp điểm nhờ may").
- **Phương án đã xét:** đưa vào tầng 3. Không chọn vì tầng 3 là "có phép chấm, không có cờ".
- **Kết luận phụ thuộc:** MRR khi root chỉ có kênh LOW_SUPPORT.

## WHY-66. Đường xử lý log và Drain của E3: cách khớp (a), ngưỡng 0,4, độ sâu 4 — Đã quyết (Q-223; đề xuất 1, 3 của `results/T-044/de-xuat-why.md`; cách khớp (a) chốt ở D17, Q-218)

- **Chọn:**
  - Chuỗi vào Drain: Nezha-OB lấy `log` của JSON ngoài, dùng `message` nếu `log` là JSON có `message` kiểu chuỗi; RE2-TT dùng `message` nguyên văn. Adapter làm việc này, không phải lõi.
  - Che token UUID → IP (kèm cổng) → HEX → NUM, ranh giới không dính chữ hoặc số; tắt phần che sẵn của drain3; bỏ che "chuỗi trong ngoặc" của đặc tả v1.
  - Một Drain chung học trên mọi dòng N, theo thứ tự (mốc, thực thể, nội dung); đơn vị là cặp (thực thể, mẫu). Khớp dòng A chỉ trên mẫu đã biết của chính thực thể; không học thêm từ A.
  - Cách khớp (a) khớp hoàn toàn; drain3 0.9.11 với sim_th = 0,4, độ sâu 4, max_children 100, max_clusters không giới hạn, extra_delimiters rỗng, parametrize_numeric_tokens True.
- **Vì sao:**
  - Chuỗi vào Drain cho cùng kết quả với `log_parsing.py` của Nezha (commit `d8140101fdb4`, dòng 94–127) mà không gọi tên dịch vụ (WHY-08).
  - Cách khớp (a) là hàm suy luận của chính drain3 0.9.11 ("Match shall be perfect (sim_th=1.0)"). Lý do chỉ là bám hàm gốc; không có căn cứ (a) an toàn hơn (b) về mất dòng lỗi.
  - Ngưỡng 0,4: mặc định của drain3 cho 95 mẫu so với 73 của tác giả trên log Online Boutique dùng cho bài TORAI; ngưỡng cao hơn tách tới 1.398 mẫu (`results/T-016/dung-logts-tracets.md` dòng 44–60). Với cách khớp (a), sim_th chỉ ảnh hưởng lúc học mẫu từ N.
- **Phương án đã xét:** truyền nguyên cột `Log` như adapter P3; mỗi thực thể một Drain riêng; khớp theo ngưỡng (b) hoặc theo ngưỡng trong mẫu cùng lớp (c); giữ che ngoặc; mẫu che riêng của Nezha (gắn câu log cụ thể, trái WHY-08); ngưỡng của Nezha 0,9 (OB), 0,8 (TT).
- **Bằng chứng:** fixture MASK1–7, NEZ1–4, KHOP1–2, U1–U6 của T-044. Trên dev (T-045, không nhãn, đo trước khối K): RE2-TT ba cách khớp gần như trùng, 0/997 dòng lỗi A vào mẫu thường; Nezha-OB ngưỡng 0,4 thì dòng lỗi A vào mẫu thường (a) 1.706/4.128, (b) 2.833, (c) 0; ngưỡng 0,9 thì 0 ở mọi cách (`results/T-045/e3-khong-nhan.json`). Minh chốt cách khớp (a) ở D17 sau khi xem các số này (Q-218).
- **Giới hạn đã quan sát (T-045, mô tả):** ô "mẫu mới" bật cả ở cửa sổ không lỗi (RE2-TT 83 thực thể trong 24/30 cửa sổ giả). Dòng rơi vào ô này ở thực thể vượt lên trên root hiếm khi có tên lỗi theo luật phân loại; phần lớn khác số token với mọi mẫu đã học, nên với cách khớp (a) không thể khớp (`results/T-045/e3-noi-dung-mau.json`; báo cáo T-045 mục 6.7). Ngoại lệ Java nhiều dòng bị tách thành từng dòng log. Đây là suy luận chưa phân xử về nguyên nhân gây hại.
- **Kết luận phụ thuộc:** kênh log khi E3 bật ở 8/16 cấu hình khối K; UV-6; kết cục của E3 theo luật C ở T-045 (E3 không vào bản P7 ở bản hiện tại). Nếu thử lại E3, thay đổi tách mẫu hay cách chấm ô "mẫu mới" là thiết kế mới, cần mục WHY mới trước khi chạy.

## WHY-67. Cổng từng đơn vị của E4 ở chế độ mới: G3 cho đơn vị phân vị, D1 cho đơn vị đếm — Đã quyết (Q-228; T-046)

- **Chọn:** G3 theo SPEC T-046 A3 (khối theo tự tương quan; biên theo bao bản ghi H làm tròn ô 10 giây và khoảng ghi F; 2.000 hoán vị; seed sha256; rơi về G0 khi dưới 5 khối). D1 theo SPEC T-046 B2. α = 0,01. Bật bằng `params.che_do`; thiếu khóa thì giữ G0, D0, để tái lập T-044, T-045.
- **Vì sao:**
  - G0 coi mẫu độc lập. Ở A/A dev, G0 qua cổng 0,300 và có cờ 0,127 ở metric RE2-TT (`results/T-046/chan-doan-cong-ban3-sua2.json#/qua_cong_aa/R0|RE2-TT|metric/G0`).
  - G3 có ô tệ nhất thấp nhất theo luật bản 4 (0,089; `results/T-046/ung-vien-sua2.json#/minimax`).
  - D1 giảm mẫu log thường từ 0,066 xuống 0,039 ở A/A.
- **Phương án đã xét:**
  - G1. Luật bản 4 đếm p < α, là đại lượng không cùng nghĩa giữa G1 và G3: G1 có thể qua cổng mà chênh không vượt biên ε. So theo cờ trên cùng phép, số dev không cho căn cứ chọn G1: ô tệ nhất hiệu −0,0036, khoảng 95% theo ca [−0,0125; 0,0078]; metric RE2-TT G3 ít cờ hơn, hiệu +0,0051, khoảng [0,0017; 0,0085] (`results/T-046/so-cap-g1-g3.json`). G1 nhạy hơn trên dữ liệu tổng hợp, không dùng Monte Carlo, chạy nhanh hơn. Độ nhạy trên dữ liệu thật chưa so. **Giữ G3 là lựa chọn thực dụng giữ kết quả luật cũ**, không phải kết quả của một luật đúng đại lượng.
  - G4: 0,272 ở A/A dev. GE, DE: không có ngưỡng đạt. D0: hiện hành.
- **Giới hạn:**
  - Không đạt mức (a) ≤ 2α ở mọi ô. Luật minimax đặt sau khi nhìn số (a), theo quyền Minh giao (Q-226).
  - Cờ từng đơn vị không có nghĩa thống kê danh nghĩa. Ở C-e: metric 0,026–0,027; op_full 0,029; op_excl hướng xuống 0,171, chưa rõ nguyên nhân (`results/T-046/kiem-sau-khoa-sua2.json`).
  - Metric Nezha-OB OPEN: 5 điểm mỗi phía, G3 rơi về G0.
  - G3 là phép Monte Carlo, lệch nguyên tắc ở SPEC T-043 B1.3; tất định nhờ seed. p nhỏ nhất 1/2.001.
  - Thiết kế sau khi xem A/A dev. C-e chồng lấn A/A và đã xem từ 16:02, trước hai lần khóa lại.
- **Cơ chế là ứng viên:** giữ giá trị, động học bền, trôi. Chưa tách được phần đóng góp. Mem qua cổng nhiều nhưng gần như không tạo cờ.
- **Điều kiện thất bại:** bước 10 không tái lập số; hoặc dữ liệu cùng cỡ về sau cho tỷ lệ cờ ở cửa sổ không lỗi vượt xa mức đã báo.
- **Kết luận phụ thuộc:** cờ F_raw của mọi cấu hình T-047; E5; mọi câu "đã sửa cổng".

## WHY-68. `verdict`: chưa chọn được trên dev — Đã quyết (Q-228; T-046)

- **Kết quả với (G3, D1)** (`results/T-046/ung-vien-sua2.json#/to_hop`): V0, V3, V1 báo CAUSE_FOUND 30/30 ở A/A RE2-TT, trượt (b). V4 (q* = 0,09) trượt (c1): 22/30, 4/22. q* đổi 0,085; 0,095; 0,09 giữa các lượt chỉ khác biên khối.
- **Chọn:** không khóa `verdict` cho bản P7 ở T-046. V0 giữ trong mã, ghi rõ: không phân biệt được cửa sổ có lỗi trên dev. Không cài V4 vào `src`, vì không có phần nào dùng.
- **T-047:** báo V0 và số thực thể tầng 1 ở C-e; luật C dùng số đó với mức HẠI khai trước trong SPEC T-047 (Q-227). Đại lượng này không trung tính với số kênh; ghi giới hạn ở T-047.
- **Vì sao không thêm ứng viên:** A/A 150 giây không cùng cỡ cửa sổ thật; C-e là phép kiểm lại duy nhất và đã xem. Đây là giới hạn của dữ liệu hiện có.
- **Kết luận phụ thuộc:** vế mốc giả T-047; đầu ra `verdict` ở P8; hồ sơ G3; FlashTicket cần hiệu chuẩn với dữ liệu cùng cỡ.

## WHY-69. Thang điểm ở chế độ mới: S1 (E4 cộng khóa phụ độ lớn T4c) — Đã quyết (Q-228; T-046; sửa D24)

- **Bằng chứng:** (S) mở: tỷ lệ kênh phân vị có cờ đạt rA = 1 là Nezha-OB 0,271; RE2-TT 0,034 (`results/T-046/thang-diem-sua2.json#/bao_hoa_R0_that`). Luật khai trước (LOG T-046, 16:05): S1 nếu T4c giảm số cửa sổ có khối đầu nhiều thực thể ở ít nhất một dataset. Nezha-OB 1 → 0; RE2-TT 0 → 0.
- **Tác động không nhãn:** giải được 1 cửa sổ hòa ở khối đầu, nhưng đổi thứ hạng rộng hơn: khối đầu RE2-TT 3/30, Nezha-OB 4/22; thực thể đầu 3/30, 3/22; cặp đổi quan hệ 44/10.277, 12/102 (`#/hoa_khoa_tang1`). Tốt hay xấu cần nhãn (T-047).
- **Chọn:** khóa (max s, max m, số kênh, Σs), như T4c đã kiểm ở T-044; áp ở mọi thế giới, chỉ khi bật tham số và E6a.
- **Phương án:** S0 (giữ E4; hợp lý nếu T-047 cho thấy S1 hại). S2: không định nghĩa, không tính (WHY-56; bão hòa nằm ở metric 5 điểm).
- **Giới hạn:** người làm đã thấy MRR của T4c và nhánh z ở T-045; luật quyết không dùng MRR.
- **Kết luận phụ thuộc:** nền khối K ở T-047; D24.

## WHY-70. Vế mốc giả T-047 dùng số thực thể tầng 1 và mức HẠI thực dụng — Đã quyết về cách thử (Q-231), chưa hiệu chuẩn

- **Chọn:** thay đại lượng tỷ lệ `CAUSE_FOUND` của vế C-e bằng chênh trung bình số thực thể tầng 1 tại P, trên cùng tập cửa sổ hợp lệ của hai nhánh. HẠI khi chênh lớn hơn 1 thực thể/cửa sổ. Dùng Fraction và dấu `>`; giữ V0 để báo cáo. Phép độ bền dùng cùng đại lượng và helper.
- **Vì sao dùng đại lượng này:** Q-227 yêu cầu báo V0 và số thực thể tầng 1, dùng số tầng 1 cho vế HẠI. Số tầng 1 mô tả độ rộng tập bị gắn bất thường tự sinh, còn V0 chỉ cho biết tập đó rỗng hay không.
- **Vì sao mức 1:** đây là dung sai thực dụng cho phép tăng ròng tối đa một thực thể mỗi cửa sổ, không phải ngưỡng suy ra từ xác suất sai đã hiệu chuẩn. Mức này nới so với ứng viên count 0,10 chưa được duyệt. Không chọn mức nhằm giữ hoặc loại E1, E2, E3 hay E5.
- **Các phương án đã xét:** không cho tăng ròng; ứng viên count 0,10; các mức 0,5 và 2. Các mức này đều chưa có hiệu chuẩn. Mức 0,5 và 2 được dùng để báo độ nhạy bằng cách tính lại toàn bộ luật C và bộ chọn, không dùng để chọn lại mức chính.
- **Lịch sử bằng chứng đã xem:** trước khi đề xuất mức 1, hai agent đã biết cấu hình thắng T-045, đã xem số C-e G0/D0 và các tóm tắt G3/D1 hiện có. Nguồn là bản ghi C-e T-045 tại `results/T-045/runs/b2b-k16-re2-mocgia-001/ban-ghi.jsonl`, trường `extra.tang_P`, và summary `results/T-046/runs/b10-kiem-src-001/ca/*.json`, trường `cua_so/ce|R0/tom_tat/tang1`, `cua_so/ce|K-du/tom_tat/tang1`; kiểm theo manifest tương ứng. Lựa chọn không độc lập với dữ liệu đã xem.
- **Điều bằng chứng chưa xác nhận:** số cấu hình bị loại ở từng mức không chứng minh cấu hình thắng đã định sẵn hoặc ngưỡng đúng. Việc một mức phân tách mức tăng của E2 và E3 trong kết quả cũ không xác nhận E2 an toàn, E3 hại hoặc mức đó có căn cứ khoa học. Không dùng kết cục do ngưỡng tạo ra để tự chứng minh ngưỡng.
- **Giới hạn:** đại lượng phụ thuộc số kênh, tập thực thể và coverage; tăng giảm giữa cửa sổ có thể bù trừ. Bật riêng E5 với cùng tín hiệu/cổng chỉ có thể giữ hoặc giảm số tầng 1, nên vế xét số tăng không bắt được tác hại riêng của E5. S1 chỉ đổi thứ tự trong tầng nên không đổi số tầng 1 hoặc V0. Số tầng 1 giảm không tự chứng minh chất lượng RCA tăng. C-e không có nhãn thực thể bất thường đủ để hiệu chuẩn đại lượng này.
- **Cách bảo toàn các điều kiện khác:** helper riêng trong `results/T-047/scripts/luat_c_t047.py` giữ UV-6, điều kiện E5, thứ tự luật C và các ngưỡng RR; không sửa `src`. Kiểm hồi quy với vế cũ trước khi chạy dữ liệu. Pha 2 và bootstrap dùng chung helper; giữ `khong_moc_gia` để đối chiếu.
- **Điều kiện diễn giải thất bại:** kết quả đổi đáng kể ở 0,5 hoặc 2 thì báo phụ thuộc dung sai; không chọn lại mức có kết quả thuận lợi. Nếu hồi quy tích hợp lệch, hoặc đại lượng không tính được do lỗi tính toán, thiếu trường bắt buộc, ERROR hay UNSUPPORTED, dừng phần phụ thuộc và trình bằng chứng thiếu. Riêng mẫu số C-e bằng 0 vì mọi cửa sổ của cặp đều bị loại do INSUFFICIENT_EVIDENCE (D2f): ghi CHUA_KIEM_DUOC, không áp vế này, tiếp tục các vế còn lại và bộ chọn với cờ được giữ; không gọi là đã qua vế C-e. Cấu hình thắng có cặp mang cờ này thì trình Minh trước khi dùng làm nền cho task (2).
- **Kết luận phụ thuộc:** loại cấu hình và chọn khối T-047, kết cục E1/E2/E3/E5 và đầu vào task (2). Mức 1 không xác nhận hiệu chuẩn cổng, `verdict` P7, cơ chế hay lợi ích RCA; các kết luận đó vẫn cần bằng chứng tương ứng.


## WHY-71. D24 hiện hành: z+S1 — Đã quyết để chọn thiết kế trên dev (Q-237)

- **Chọn gì:** thay E4+S1 bằng z+S1; giữ epsilon=0,05, alpha=0,01, G3/D1, khóa S1 và các quy tắc xếp tầng. Không đổi lịch sử WHY-56/WHY-69: các mục đó mô tả lựa chọn tại thời điểm trước T-048/T-053.
- **Vì sao:** T-048 đã làm T4/T4b và cặp đổi thang ở R0, E1+E2 theo B5; T-053 kiểm ngoại lệ số học, T1 chịu ảnh hưởng và chạy lại đủ khối K. Trên dev đã kiểm, phép đổi giữ cờ/cổng/U/FI/tầng, nên có căn cứ dùng để chọn tiếp. Minh chấp nhận ứng viên cùng các giới hạn đã báo; không lấy đồng thuận hai agent làm bằng chứng khoa học.
- **Phương án đã xét:** giữ E4+S1; z+S0 báo kèm; đổi epsilon/alpha theo lưới T4 chỉ là phép độ nhạy. Không chọn thêm ngưỡng hoặc cách chuẩn hóa mới sau khi nhìn điểm.
- **Bằng chứng:** results/T-048/t4.json, t4b.json và luat-c.json#/comparisons; results/T-053/runs/kiem-cuoi-001.json và runs/dap-phan-bien-001/kiem-tra.json#/analysis. Audit lưu tái dựng hạng ở đủ 52 ca, ba thế giới và hồ sơ các ca đổi RR của cấu hình thắng. Hash theo manifest tương ứng; nguồn quản trị trước quyết định lưu tại results/T-049/nguon-truoc-ghi-quyet-dinh/.
- **Đã xác nhận tới đâu:** có những cặp đổi khóa/kênh quyết định RR; bão hòa và mixed PV/đếm có thể cùng tồn tại. Chưa tách thành phần đóng góp nhân quả hoặc xác định cơ chế vật lý cho mọi ca; không cộng số cờ chồng lấn thành tỷ lệ nguyên nhân. z không bị chặn trên trong khi điểm kênh đếm giữ thang E4. Có cả ca được sửa và bị làm hỏng; không suy việc đếm không thắng max là không có tác hại.
- **Điều kiện thất bại/cần xử lý:** ngoại lai lớn, mixed PV/đếm, đổi đơn vị không nhất quán hoặc tần suất E3b có thể đổi tương quan điểm. T6 phải lần theo chuỗi kênh/cờ/điểm/khóa và so ca đúng với sai. Kiểm adapter về đơn vị FlashTicket còn ở bước tích hợp; không đòi bất biến khi tùy ý đổi chung các giá trị của kênh đếm. Sai khác cờ/hợp lệ hoặc cần đổi chính sách tràn thì dừng kết luận phụ thuộc và trình Minh.
- **Số học:** tích hợp cách phục hồi trung gian của results/T-053/scripts/z_on_dinh.py vào src/m1/e4.py ở T-049, kiểm đường native bình thường và các fixture biên. Điểm hoặc tổng khóa thật sự ngoài miền biểu diễn vẫn theo hợp đồng hiện hành; không cắt điểm/cứu riêng một hướng.
- **Kết luận phụ thuộc:** K-b/T6 và nền cho T-050 trở đi; đối chứng QT7 và hồ sơ G3. Lợi ích trên dữ liệu độc lập, verdict, chế độ (b), RE3-OB và triển khai FlashTicket vẫn chưa được xác nhận.

## WHY-72. Nền đầu T-049: E1-U + E2-C + E5 dưới z+S1 — Đã quyết có điều kiện (Q-237)

- **Chọn gì:** dùng gói thắng của T-053, giữ E3(a) tắt. Đây là điểm xuất phát cho K-b/T6; không thay thế các phép kiểm bối cảnh về sau.
- **Vì sao:** bộ chọn khai trước chọn E1+E2+E5 trong cả ba thế giới; bước 8 trình E2, không có xung đột khác. Minh chấp nhận đánh đổi theo dataset đã nêu, thay vì để nguồn quyết định tiếp tục ghi OPEN. Cờ TRÁI CHIỀU vẫn được giữ nguyên.
- **Bằng chứng số:** results/T-053/runs/k-cham-001/khoi-k.json#/chon_khoi và /buoc8; /cap/E1+E5|E1+E2+E5/theo_the_gioi/P/MRR_bat: gộp 1411/1560, RE2-TT 167/180, Nezha-OB 48/55. Thêm E2 trên E1+E5 làm RE2-TT giảm 7/180 và Nezha-OB tăng 1328683/8731800; kết cục là TRÁI CHIỀU theo dataset, không phải GIÚP. Audit T-053 lần theo hai ca mất RR và ca đối chứng đúng; chưa quy nguyên nhân vật lý của lỗi.
- **Phương án đã xét:** R0 z, gói cũ E1+E2, E1+E5 và các cấu hình còn lại của đủ 16 cấu hình K. K-b còn phải thử VC đúng bối cảnh. E3(a) bị loại theo luật trong lượt này; không suy kết quả đó sang E3b.
- **Giới hạn độ bền:** results/T-053/runs/bootstrap-ec2-001/do-ben.json#/loai và /tan_suat_thang: 893/1000 mẫu có cấu hình được chọn; 107 mẫu không đạt bước 8 về thành phần đồ thị. Trong 893 mẫu, gói này thắng 249, E2 thắng 281. Không gọi lựa chọn vững trên dữ liệu độc lập. Các cờ N1 và mức h=1 là dung sai thực dụng chưa hiệu chuẩn; h=0,5/2 chỉ báo độ nhạy.
- **Vai trò đồ thị:** E1 dùng quan hệ cha–con để tạo thời gian độc quyền; E2 gán bằng chứng khoảng ngoài span theo cạnh; E5 dùng quan hệ/lớp kênh để tách bằng chứng kế thừa và tự sinh trước xếp hạng. E6a chưa lan truyền điểm theo đồ thị. Kết quả này chưa phân xử lợi ích riêng của cấu trúc phụ thuộc thật so với các đối chứng P7.
- **Điều kiện thất bại và phụ thuộc:** K-b có thể đổi gán cạnh, T6 thêm kênh tần suất; nếu nền đổi thì xác định lại phần chạy phụ thuộc. K-b trên nền E5 bật chỉ cho tác dụng C/VC có điều kiện E5 bật, không kiểm đủ tương tác VC × E5. T-051/T-052 và quyết định G3 còn giữ nghĩa vụ này; không tự thêm ô ma trận hoặc đổi nền để đóng câu hỏi.


## WHY-73. Nền đầu T-050 sau K-b/T6 — Đã quyết (Q-239)

- **Chọn gì** E1-U + E2-C + E5 trên z+S1, E6a và cạnh quan sát. E3(a), E3b, E9, T12 tắt. Giữ epsilon, alpha và cổng theo WHY-71.
- **Vì sao** K-b giữ C theo luật. VC khôi phục hai ca RE2 bị C làm hỏng ở T-053 và làm hỏng hai ca Nezha. T6 cho KHÔNG TÁC DỤNG và đề nghị tắt E3b. E1/E2/E5 còn sử dụng quan hệ để tạo và phân loại bằng chứng.
- **Phương án và bằng chứng** C/VC và bật/tắt E3b đã so trong bối cảnh T-049. Nguồn là `results/T-049/k-b.json#/K-thang-VC`, `results/T-049/t6.json#/T6-C-E3b`, `results/T-049/runs/dap-phan-bien-001/doi-chieu.json` và `results/T-049/nen-de-nghi-T050.json`, kiểm theo manifest T-049.
- **Giới hạn và phụ thuộc** Cờ đánh đổi của E2 theo WHY-72 vẫn là giới hạn khi diễn giải. C-e của K-b chưa phân xử tác hại khi VC thực sự định danh. Phép 2×2 VC/E5, hiệu quả độc lập, hiệu chuẩn verdict, chế độ (b), RE3-OB và FlashTicket còn OPEN. T9 dùng nền này để chọn cách xếp hạng trên dev.

## WHY-74. Hành động T9 khi E6b KHÔNG TÁC DỤNG — Đã quyết trước pha 1 (Q-240)

- **Chọn gì** Nếu kết cục kết hợp theo luật C là KHÔNG TÁC DỤNG, đề xuất giữ E6a+S1, tắt E6b. HẠI vẫn dẫn tới bỏ E6b. D2a/D2f vẫn áp cho KHÔNG ĐỦ CA và phụ thuộc quan sát.
- **Vì sao** DT18 §2 và hướng dẫn của cô đòi các đầu ra chẩn đoán có dùng đồ thị, đồng thời nêu PageRank như ví dụ. MRP §2.3 và WHY-02 đặt mục tiêu dùng đồ thị trong chuỗi. MRP P6 tầng 4 giao chọn ứng viên trên dev. E6a xếp theo tầng và điểm mà E1/E2/E5 đã tính từ dữ kiện quan hệ. E7 dùng cạnh để dựng vùng. Bản E6a có xếp hạng dựa trên bằng chứng đã dùng đồ thị, với bước sắp thứ tự cục bộ.
- **Phương án đã xét** Giữ E6b theo ngoại lệ Phụ lục C bước 6 nếu bước sắp thứ tự phải trực tiếp dùng cạnh để đáp ứng chức năng. Minh duyệt cách hiểu cho phép dùng E6a trong trường hợp lợi ích E6b chưa đạt ngưỡng.
- **Bằng chứng** T-043 B2/B4 và Phụ lục C, `src/m1/xep_hang.py` phần `k_tang` và `xep`, đối chiếu P1 và bản kiểm lại của Claude trong LOG T-050. Dữ kiện dev về tập trung của v dùng để đặt giả thuyết, chưa có kết quả E6b.
- **Điều kiện thất bại và phụ thuộc** Nếu E6b thay đổi thứ hạng, phân biệt phần do lan truyền và khóa phá hòa. KHÔNG TÁC DỤNG chỉ cho biết lợi ích chưa đạt ngưỡng trên nền và thang đã khai. T-051 phụ thuộc kết cục T9 và cách xử lý các cờ theo luật.

## WHY-75. Nền và vế mốc giả của T-051 — Đã quyết có điều kiện (Q-241)

- **Nền.** Giữ nền WHY-73 với E6a+S1 và cạnh quan sát. T9 so với E6b trên chiều bên gọi → bên được gọi. Lượt đã ghim cho kết cục HẠI ở bước 3 trên cả ba thế giới, ΔMRR gộp −1/30. Nguồn là `results/T-050/cham-002/luat.json#/theo_the_gioi` theo manifest chạy lại và `results/T-050/dinh-chinh-va-kiem-lai.md`. Cờ đánh đổi E2 theo WHY-72 vẫn còn.
- **Giới hạn.** Đây là lựa chọn điểm xuất phát trên dev chế độ (a). Biến thể đảo chiều PageRank còn OPEN. Hiệu quả trên dữ liệu độc lập và chất lượng vùng ảnh hưởng còn cần bằng chứng riêng.
- **N1.** Giữ WHY-70 và hợp đồng T-051. Trên cùng cửa sổ giả RE2 hợp lệ của cặp, dùng chênh trung bình số thực thể tầng 1 tại P, tính bằng Fraction và xét HẠI khi tăng nghiêm quá 1. Dùng N1 để mô tả độ rộng tập tự sinh vì V0 chỉ phân biệt tập rỗng và có phần tử trong trường hợp đủ bằng chứng. Báo V0, mẫu số và độ nhạy h=0,5/2. Mức chính là dung sai thực dụng. Hiệu chuẩn verdict vẫn OPEN. Phân biệt mẫu số bằng 0 do thiếu bằng chứng với lỗi hoặc thiếu trường bắt buộc.

## WHY-76. Nền cuối T-051 và phạm vi T13 — Ghi theo Q-242/Q-248

- **Chọn gì:** giữ E1-U, E2-C, E5, z+S1, E6a, cạnh quan sát; E3(a), E3b, E6b, E9 và hợp cạnh T12 tắt. E3 tắt vẫn giữ kênh log lỗi cơ bản. T13 chỉ mô tả, giữ cờ đánh đổi E2, giới hạn VC×E5, chiều đảo PageRank OPEN và hạn chế dev chọn lặp.
- **Căn cứ sau T-051:** T11/E9 KHÔNG TÁC DỤNG theo luật khai trước ở ba worlds; ΔMRR tại P gộp 1/104, TT 1/60, OB 0; C-e ΔN1=7/30 trên 30 cặp. T12 KHÔNG TÁC DỤNG; ΔMRR=0 từng dataset nhưng F_I đổi ở 17 TT và 2 OB, nhóm hạng đổi 11 ca. C-e ΔN1=−7/10 chỉ xét tăng nên chưa phân xử loại quá tay. Nguồn T-051/t11-001 và t12-001/score/{law,metrics,mechanisms}.json, đính chính và manifest bổ sung cuối.
- **Phương án:** giữ E9/hợp snapshot nếu đủ lợi theo luật đã duyệt, hoặc giữ nền quan sát. Q-242 nghiệm thu lựa chọn nền quan sát/E9 tắt. T13/P7 giữ kết quả âm và cặp T12 mô tả, không đổi nền theo điểm test.
- **Bằng chứng đối lập:** M1 vs K-R0 TT giảm 1/18 (1 tăng/4 giảm/25 hòa), OB tăng khoảng 0,211 (9/2/11); C-d2 cao hơn M1 OB. Bỏ E1 hại TT/OB bằng; bỏ E2 và E5 có dấu khác giữa hai bộ. Mục tiêu bỏ mô-đun đồ thị làm chất lượng giảm chưa được hỗ trợ chung trên dev. Nguồn results/T-053/runs/k-cham-001/kq.json#/cau_hinh, results/T-051/kb-002/score/{metrics,scores}.json, results/T-051/t12-001/score/regions-controls.json.
- **Điều kiện thất bại/phụ thuộc:** KB kiểm ba vế ở nền cuối, chưa đủ tương tác C/VC×E5 (WHY-72/73). E9 Nezha chưa tới phép xét thời gian theo đính chính; T12 có thay tập/kênh/vùng dù RR root giữ. Snapshot chưa xác minh revision benchmark. T13 phải báo hạn chế từng phép, P7 kiểm độc lập đúng phạm vi, P9/P10 nhận quan hệ thiếu đầu quan sát. Lựa chọn dev không chứng minh bất thường tự sinh là nguyên nhân vật lý.

## WHY-77. Verdict, C-e, phạm vi P7(a) và chuyển mức A4 — Đã ghi theo Q-245–Q-248

- **Chọn và vì sao:** giữ V0 truy vết, chấm P7(a) từ hạng/trạng thái hỗ trợ. WHY-68 cho thấy V0 bão hòa và ứng viên mới chưa hiệu chuẩn. Nền cuối C-e có CAUSE_FOUND 30/30, N1 14,7, nên chưa dùng V0 mở sự cố hoặc làm mức tin cậy root.
- **C-e:** giữ phân bố hạng đầu để hỏi có ưu tiên lặp một thực thể. Dev có 16 thực thể từng đứng đầu, hai thực thể mỗi 5/30, top hai 10/30; MRR nhãn root thật sau mốc giả 0,0787266 so chance trên 68 thực thể 0,0706479; Hit@1=0/30. Nguồn T-051/kb-002/ce.json, nhan-dev ghép sau, T-053/chi-so-day-du.json#/K-E1+E2+E5/tong_hop/ce. RR của root tương lai không kiểm trực tiếp thiên lệch và mốc trước tiêm chưa chứng minh nền lành. P7 xin C-e mô tả trên tối đa 60 cửa sổ TT M1 cuối, không dùng chọn/hiệu chuẩn; khóa thiếu lịch sử/hỗ trợ/mẫu số và ngân sách trước mở. Mục đích là kiểm lại mẫu hình dev trên ca mới; phương án chỉ-dev sẽ thiếu phần kiểm lại đó.
- **A4:** nhận chuyển mức một chiều của Claude với CI E-04 không suy biến tại P mới nâng OB từ 0,025 lên 0,05. Nó giữ cách đọc E-04, không cần p E-04 riêng, và cho phép câu phụ có ngưỡng rộng hơn khi câu chính qua. Phương án cố định 0,025 dễ hơn nhưng không nhận lợi ích đó. Holm đầy đủ cần quyết định E-04 ở thêm mức 0,05; Q-246 thay cả Holm lẫn phép chính TT. Hai world nhạy không cấp thêm mức.
- **Giới hạn A4 đã xét:** CI percentile ít ô có thể hẹp hơn thực cả khi lo<hi. Bộ lọc suy biến chỉ hạn chế chuyển mức, không chữa sai số TT. Đạt theo công thức kèm cảnh báo ngay trong câu khi suy biến, luôn báo ô hữu hiệu/ô thua/ca cùng trượt. Đảo dấu OB chỉ có hiệu lực theo H0 hoán đổi dấu, không tự kiểm mọi phân bố có trung bình≤0. Giữ kết luận danh nghĩa/có điều kiện; synthetic không xác minh hiệu chuẩn cho benchmark.
- **Nguồn thống kê:** src/p3/danh_gia.bootstrap và WHY-28 (seed 20261005); [Canay, Romano, Shaikh 2017](https://home.uchicago.edu/amshaikh/webfiles/weakrand.pdf) về điều kiện đối xứng của randomization, [Bretz et al. 2009](https://doi.org/10.1002/sim.3495) về chuyển mức và [Holm 1979](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf) là phương án đã xét. Các nguồn không chứng minh điều kiện thống kê được thỏa trên tập ca này.
- **Phạm vi phụ thuộc:** hoãn (b) là lời Minh Q-245; hệ quả Q-66/P/R/F1 ghi riêng, D3/D16 vẫn trước kết luận (b)/khóa FT. RE3 cho bản cuối với hợp đồng nguồn khóa trước mở, không dùng bốn root metadata làm U. TX1/ca liền kề Nezha/RE3 cùng hệ-công cụ và mọi lần xem phải khai. P7 chạy locked trên local theo Q-42; quyền khác cần Minh cấp riêng.


## WHY-78. Tổ chức hồ sơ T-054 và ranh giới đánh giá — ghi theo Q-250, chưa khóa G3

- **Chọn gì trong kế hoạch:** một task hai pha theo yêu cầu Minh; bản SPEC hợp nhất giữ điều kiện chuyển pha và các quyền riêng. Không mở lại T-052 đã nghiệm thu phần dev/hồ sơ. Các chính sách còn OPEN không được gọi là đã quyết chỉ vì SPEC được ghi.
- **Vì sao:** hồ sơ T-052 004 chỉ ra các liên kết nguồn→thực thi→seal→nhãn và toàn driver còn thiếu; lập luận khoa học không được thay bằng đủ file/hash hoặc chạy không lỗi. Cần hoàn thiện/kiểm trên dev trước khi Minh xét bản khóa và grant test.
- **Nhãn và phép kiểm chính:** chặn mọi evaluator khi slot A4 còn BLOCKED/PENDING để không thấy gần đủ chênh lệch rồi sửa nhánh chính. Slot ngoài A4 chạy nguyên pin sau mốc xem phải khai; sửa code có dùng test theo C-15 B. Phương án công bố theo bậc chỉ dùng khi Minh quyết trước G3. Quy tắc này giữ phép so chính, không xóa lịch sử tiếp xúc metadata G1.
- **Nguồn/máy:** OB ở laptop vì file metric ngày và một số file phút dùng chung dev/test; khai bản sao lịch sử EC2 theo preflight/Q-93, không kết luận đã đọc giá trị test hoặc vi phạm cũ. Native T-053 có cả hai máy; pilot mới đối chiếu đúng máy nguồn từng cửa sổ, có T-050 cho C-c/C-g. C-a0 cung cấp trường vị trí N trong miền đã kiểm; không dự toán thêm toàn bộ K-R0.
- **Vận hành:** partition cố định, cùng controller đơn máy giúp tránh dựng hệ điều phối phân tán trên đường găng. Hai EC2 và laptop dùng cho lô độc lập, đủ quyền và có ích theo chỉ đạo Minh; EC2 2 phải có nhánh driver cụ thể còn thiếu, không chạy lại chỉ để dùng máy. Cache TORAI kiểm trên laptop nơi sẽ áp dụng. Nếu setup lớn hơn phần tiết kiệm hoặc không có lô cần thiết, báo Minh cho máy nghỉ.
- **Bằng chứng và điều kiện thất bại:** phase/nguồn/config chưa rõ thì không chấm trượt; max monitor gap dưới ngưỡng đã khai là điều kiện cần, không đủ chứng minh không sleep. Gói đúng byte code thực chạy cùng hash/blob provenance khắc phục rủi ro checkout đổi line ending; tách code_root/data_root/output_root. Mất phiên agent/SSH có thể tự tiếp tục; reboot cần resume thủ công trừ quyền startup riêng. ETA chưa đo toàn bundle/local sau dọn nên các mốc sáng là có điều kiện.
- **Phương án đã xét:** một máy local; cloud TT dev để phủ nhánh/cùng máy nguồn; cloud test cần ngoại lệ quyền dữ liệu; cache prep TORAI; công bố theo bậc. Chọn lô/worker/timeout cụ thể và ngoại lệ cạn ngân sách/TORAI A vẫn chờ bằng chứng hoặc Minh quyết, không tự chọn để vừa hạn.
- **Nguồn:** SPEC T-054, hồ sơ T-052 004/giao thức 003, native/seal T-053, nguồn T-050, Q-42/Q-63/Q-74/Q-93/Q-243–Q-248, hai lượt phản biện chat và bản đáp tại results/T-054/runs/soan-spec-001/. Hash và lệnh kiểm ở manifest/LOG task, không rải trong văn bản.
- **Kết luận phụ thuộc:** tính hợp lệ bản P7(a), mẫu số/diễn giải A4, cách báo kết quả đầu và sau khi đã xem test; không xác nhận hiệu quả độc lập, cơ chế vật lý, RQ3a hoặc độ đúng vùng. Phương án cạn ngân sách P7 khác câu P3 §8.3 phải được Minh quyết riêng trước G3; Q-250 không giải mâu thuẫn đó thay Minh.


## T-054 — biểu diễn metric theo nguồn cho OB trước G3, 06/11/2026

Minh duyệt có điều kiện theo mục mới DECISIONS; Codex tự soát và tiếp nhận đúng phạm vi báo cáo007. Chọn cài ứng viên source_native opt-in để giữ mẫu thật ở cửa sổ gốc khi số hàng khác nhau. Đây là nhu cầu adapter/hợp đồng, không là cơ chế sửa lỗi RCA đã xác nhận. Bằng chứng: reader yêu cầu5N5A rồi ghép bảng; lõiM1 yêu cầu mọi nguồn cùng số hàng; kiểm timestamp006 xác nhận4ca bị từ chối trước method. Phương án bỏ guard đơn lẻ không sửa phép ghép; cắt/bù/lưới/dịch mốc làm đổi input; bỏca/gán0 làm sai nghĩa lỗi. BARO per-column cho phép đề xuất chạy theo source rồi ghép khóa;8fixture feasibility007 chưa thay kiểm toàn tuyến. M1 dùng index nguồn tường minh, không giả timestamp hoặc observation. Điều kiện thất bại: mapping sai, điểm/hòa/preprocessing khác, unsupported/missing không đúng; phải dừng phần phụ thuộc. Mặc định legacy/TT giữ đường cũ; cần exactparity normalizedinput/trunggian/hạng/vùng ở dev và fixture. Phụ thuộc: toàn OB P7, code/binding/snapshot/lịch003máy; không chứng minh lợi ích, RQ3a, vùng ảnh hưởng hoặc cho phép mở test.


## T-054 — H2: adapter RE3 với profile tường minh, 06/11/2026

Minh duyệt cài theo báo cáo009. Nhu cầu kỹ thuật: RE3 có schema riêng; source time/r/U/alias chưa đủ nguồn, worker hiện chọn TT/Nezha và TORAI lọc ts-* làm rỗng metric OB trong kiểm tổng hợp. Chọn reader/profile riêng, kiểm hợp đồng trước I/O và dispatch/chấm held-out riêng; không sửa công thức M1/kernel baseline. Phương án tái dùng nguyên adapter TT làm mất metric; giả tên dataset hoặc tự đoán đơn vị/U từ nhãn làm sai đầu vào. Thêm tham số dataset tùy chọn giữ mặc định cũ cho BARO/CIRCA/TraceRCA; literal re2-tt không tự chứng minh sai số. Bằng chứng metadata/code và27kiểm ở009, chưa kiểm trên RE3 thật. Điều kiện thất bại: profile thiếu/sai, alias va chạm, clock không biểu diễn chính xác, owner ngoài U, source/grant khác binding; dừng trước method. Inventory/đơn vị/r/semantics status còn OPEN; duyệt cài không biến giả định thành FACT. Phụ thuộc: khả năng thực thi RE3 bản cuối và bảng riêng; không xác nhận hiệu quả RCA, RQ3/RQ5 hay mở dữ liệu. Các kiểm tổng hợp mới sẽ nằm ở checkpoint010.


### H2 — giữ đủ hai bản ghi CIRCA trên RE3

Bộ nhận và timeout đang chỉ khai hai vế CIRCA cho TT, trong khi adapter trả cả chính/phụ cho RE3. Minh duyệt bổ sung hai file theo010. Mở đúng điều kiện dataset sang TT hoặc RE3; không bỏ vế phụ hoặc đổi nghĩa timeout. Kiểm fixture đủ/thiếu variant và current; chưa kiểm RE3 thật.


## T-054 — gRPC status và metadata inventory, 07/11/2026

Nguồn tác giả mới `CONVERT.md`, ghim riêng trong checkpoint011, nói benchmark phát hành lưu mã gRPC, 0 là OK; `tracets_err` gốc cộng mã thay vì đếm span lỗi. Guard H2 chỉ nhận 0/1 là giả định. Minh duyệt profile gRPC khai rõ và giữ nguyên giá trị/kernel; không chuyển thành 0/1. Code benchmark đã chọn không nâng phiên bản; converter mới chỉ làm bằng chứng hợp đồng nguồn. Gọi tổng mã là số lỗi sai nghĩa; đổi sang đếm lỗi sẽ đổi baseline. Đã kiểm fixture về miền mã, tổng và tuyến worker; chưa đọc statusCode RE3 thật.

Minh cấp quyền riêng đọc tên owner như metadata toàn cohort. Không dùng nhãn root hoặc phân bố theo fault để chọn U. Hợp tên quan sát không chứng minh deployment hay alias; nguồn thiếu giữ OPEN. Không áp đơn vị của converter mới cho release cũ khi schema khác. Lựa chọn này ảnh hưởng profile/khả năng hỗ trợ RE3 và hồ sơ G3, không chứng minh hiệu quả RCA hay cấp quyền main.

## T-054 — sửa F9 bằng đường dẫn định vị mờ, 07/11/2026

**Bằng chứng.** Hai gói ứng viên EC2 trong manifest 011 đều mang locator có tên gốc ở bản kê runtime và nguồn đối chiếu độc lập của đủ 60 ca TT. Biên nhận chuyển 006 xác nhận cả hai EC2 cũ đã nhận tệp qua tên thư mục có dịch vụ gốc và dạng lỗi. Các nguồn và cách đối chiếu nằm trong mục xử lý F9 của LOG T-054. Quan sát này chứng minh kênh lộ qua đường dẫn. Chưa có bằng chứng từ đó rằng phương pháp đã dùng nhãn.

**Lựa chọn.** Dùng thư mục theo mã mờ và giữ đủ cohort. `p7_entry_v2.open_runtime` đối chiếu toàn bộ cohort và inventory (danh mục thực thể) với G1. `source_selection` kiểm gốc đường dẫn, tên parquet và SHA-256 cùng số byte của tệp. Tên thư mục gốc của ca không phải điều kiện đọc. `p7_guard_v3.attest_runtime` tính binding (dấu ràng buộc) cả trên locator. Vì vậy lập bản chiếu mờ từ nguồn đối chiếu đã ghim độc lập trên laptop, giữ nguyên dấu nội dung và số byte của parquet rồi ghim lại bản kê, nguồn đối chiếu, biên nhận và kế hoạch phụ thuộc. Tạo nguồn đối chiếu từ chính bản kê runtime sẽ làm mất phép kiểm độc lập. Chỉ chuyển bản chiếu mờ cần cho worker. Bản đồ mờ sang đường dẫn thật nằm ở vùng riêng trên laptop và dùng khi chuẩn bị tệp chuyển.

**Phương án đã xét.** Cắt bản kê theo máy rồi sửa guard thành hai lớp sẽ phải đổi hợp đồng T-052. Cách đó không cần cho F9 vì kế hoạch ghim đã kiểm đủ tập job của từng máy và mỗi máy chỉ nhận parquet thuộc lô đó. Kiểm trong bộ nhớ xác nhận 60 mã mờ qua guard, bản kê bị cắt và locator sai lệch với nguồn đối chiếu bị chặn, ca chưa có tệp hoặc tệp sai SHA-256 cũng bị chặn.

**Giới hạn và điều kiện sử dụng.** Mã theo `results/T-052/ke-hoach-tap-test.json#/opaque_rule` có thể dò từ tên công khai. Dấu nội dung cũng có thể dùng để đối chiếu với bản nguồn khi có tệp tương ứng. Mục tiêu là bỏ tên có nhãn khỏi đường dẫn mà phương pháp hay nhật ký có thể dùng vô tình. Khả năng tái nhận diện có chủ đích nằm ngoài bảo đảm của biện pháp này. Trước khi dùng gói thật, cần chạy lại phép B1 hiện có và kiểm mọi locator chuyển ra ngoài, gồm bản kê, nguồn đối chiếu, đường dẫn staging và nhật ký chuyển. Đây là điều kiện để coi F9 đã được xử lý cho gói mới. Kiểm trong bộ nhớ chưa xác nhận gói thật, parity (độ tương đương) baseline/OB hoặc câu hỏi RQ3b/RQ3d.

## T-054 — quyền, hàng chờ A và giới hạn trước chạy 013, 07/11/2026

Minh duyệt gói chuẩn bị013 và D1–D4/R3. Kiểm quyền phát main ở CLI cùng quyền G3/test để mọi đường run/resume dùng cùng điều kiện. Một supervisor laptop giữ tập slot bất biến. TORAI A chỉ được phát sau khi các slot khác A đã VERIFIED. Nguồn A thiếu quyền hoặc sai pin có biên nhận theo slot trước phát; lỗi chưa phân loại khi A chạy giữ attempt và dừng theo policy, ghi BLOCKED cho phần A chưa phát. Báo cáo giữ toàn ma trận và khai nhóm A chưa đủ seed/ca. Hai plan cùng host không phù hợp hợp đồng ghép hiện tại. Chỉ sắp A cuối danh sách chưa đủ khi hai worker hoạt động. Lý do là ngăn phần phụ làm mất bảng chính đã đủ điều kiện, giữ nguyên các ngưỡng và mẫu số thống kê.

Tái dùng M1 TT012, fixture C-d3 DAG/cyclic/no-target012, parity OB008 và nguồn CSV A đã audit006 sau kiểm hash. Chỉ chạy các tuyến dev thực sự khác. R1 dùng bản chiếu mờ từ nguồn đối chiếu riêng, giữ đầy đủ cohort/byte/hash, không đổi guard T052. D1 khai tiếp xúc đã dùng sửa adapter; D2 để profile RE3 OPEN cho đợt cuối; D4 là bảng mô tả nhóm đã xác định trước điểm. Hạn chế logts A thiếu N và nhánh OB lệch số mẫu vẫn phải khai theo bằng chứng hiện có. Gói chuẩn bị và đồng thuận phản biện chưa trả lời RQ3b/RQ3d bằng test.

## T-054 — sai khác C-e trên máy mới, 07/11/2026

Phép đối chiếu M1 C-e dev-a5cabe5fa7 khác30trường float, mỗi trường1ULP. Normalized-input digest, cấu trúc/tầng/hạng/nhóm hòa/các trường rời rạc khớp, theo numeric-parity-Ce-audit.json của013. Minh duyệt đúng ngoại lệ đó. Giữ kết quả nguyên bản và công bố giới hạn, dùng tiếp cho bằng chứng tuyến đã đo. Chưa xác định cơ chế số học riêng, không gán nguyên nhân BLAS/CPU hoặc thêm dung sai toàn cục. Các sai khác mới vẫn cần phân xử.


## T-054 — căn cứ phân lô và pin vận hành ứng viên013, 07/11/2026

CANDIDATE để Minh xét cùng G3: hai EC2 mới cùng loại máy và đều đã có ổ30GiB; chia TT30/30 để dùng cả hai và giữ trọn nguồn từng ca, EC2_1 tối đa2worker, EC2_2 một worker như phép phủ môi trường đã kiểm. Không dùng lại lịch35/25+OB của011 khi máy cũ không truy cập được. Giữ OB, CIRCA, MicroRank và TORAI A trên tuyến Windows đã có bằng chứng và nguồn riêng; chuyển thêm sẽ cần dựng/parity/truyền mà chưa có bằng chứng giảm tổng thời gian. Laptop tối đa2worker theo pilot004, chỉ chạy đồng thời khi reservation và reserve cho phép. Đây là bố trí vận hành ứng viên, không là kết luận EC2 nào cũng nhanh hơn hoặc hai worker luôn tăng tốc. Kịch bản lặp thời gian DEV chỉ giúp trình chi phí dài hơn1giờ, không là ETA của cohort test.

Để ghim đúng byte thực chạy, giữ106pin code repo/helper và pin106file upstream/bản vá local cùng hai runtime; cloud dùng bản source lowercase rcaeval đúng byte upstream và4file causal-learn đã vá như tuyến gốc. Không đổi công thức hoặc tham số khoa học. Đường nhận vẫn verify snapshot trước nhãn; source-map thật và nhãn ở laptop, chỉ runtime/bản chiếu TT mờ đủcohort vào packet. R1 không sửa guard T052. Bằng chứng, các lần hỏng và giới hạn ở runs/chuan-bi-main-013/bao-cao.md. G3/test/nguồn A/chuyển/main/chấm và commit vẫn theo quyền riêng.


## T-054 — đáp F1/F2 của Claude, ứng viên vận hành013 sửa sau review, 07/11/2026

Minh cho phép ghi phần Codex kiểm độc lập đồng ý với phản biện; nguồn nguyên văn được lưu cùng gói. Nhận F1 về thiếu bằng chứng thông lượng/ảnh hưởng tranh tài nguyên và F2 về dự toán thiếu phần local+chuyển/nhận/chấm. Chọn để TRÌNH KHÓA phương án F1(a): cả hai EC2 một worker, laptop tối đa hai theo scheduler/RAM và A cùng nhóm chạy sau non-A. Đây là sửa ứng viên trước G3, không ghi thành quyền chạy. Không khẳng định H1 tranhCPU hay H2 vế vốn nặng đã được phân xử; cũng không khẳng định đổi worker giữ nguyên TIMEOUT hoặc tổng thời gian. Giữ nguồn dữ liệu/config/case/seed/mẫu số và method600giây/C-d360giây; thay tranh chấp tài nguyên có thể đổi trạng thái TIMEOUT nên phải chốt trước test. Bằng chứng DEV hiện có và fixture cho phép kiểm tuyến với một worker; không chạy lại phương pháp chỉ vì metadata đổi.

600giây là ngân sách wall-clock ứng viên thực dụng, không là cận trên chi phí mọi ca. Giữ vì giao thức/pilot đã dùng và phân loại có bằng chứng pha/monitor; DEV đã đo không chứng minh test đều hoàn tất trong hạn. Đặt cùng một worker trên hai EC2 để giảm bất đối xứng đồng thời; không tăng timeout hoặc chọn theo kết quả test. Phần chi phí theo từng vế phải tách số đo chạy đơn/chạy chồng và proxy; không lấy số chồng rồi mặc định chia2 như tốc độ đã đo. F2 bổ sung kịch bản laptop, truyền/hash/nhận và chấm bằng số đo cũ đã kiểm hash; thiếu số đo whole-cohort giữ giả định/điều kiện sai, không gán ETA đã xác minh. Đường găng chỉ là kết quả có điều kiện của kịch bản.


## T-054 — khóa G3(a) theo ứng viên013 sau phản biện, 07/11/2026

Khóa đúng ứng viên013 sau đáp F1/F2: hai EC2 một worker, laptop tối đa hai theo RAM/nhóm, A sau non-A; method 600 giây, C-d3 60 giây, poll 0,1 giây, maxgap dưới 5 giây; không trần cộng dồn. Lý do giữ nguyên các mục WHY 07/11 trước (phân lô, F1/F2, C-e). Lượt kiểm lại của Claude không thấy điểm CHẶN; metadata sau sửa chỉ đổi số worker EC2_1 và hash dẫn xuất. Đổi người thực hiện từ Codex sang Claude không đổi code, plan, cấu hình hay mẫu số; nó chỉ đổi ai vận hành và ai phản biện. Kết luận phụ thuộc: RQ3b/RQ3d chỉ được trả lời bằng kết quả đầu của bản khóa này; giới hạn OB/A/RE3 và dự toán chưa kiểm giữ như hồ sơ.


## T-054 — v2 sau BLOCKED main013, 07/11/2026

Chọn chạy lại toàn bộ dưới v2 vì vân tay job gồm mọi pin code và failure-policy: thêm quy tắc làm đổi vân tay của 1640 job, seal v1 không khớp plan mới. Phương án khác: cầu nối hai phiên bản (sửa phần chấm chưa chạy ở quy mô đủ, rủi ro cao hơn); giữ BLOCKED (vẫn phải sửa supervisor, bảng TraceRCA/MicroRank TT thiếu ca); dừng (A4 thiếu). Quy tắc mới cùng họ với operation mới không có nền đã khóa: giả định ≥2 mẫu nền của phương pháp không thỏa trên dữ liệu hợp lệ, nên tính trượt, không đổi mẫu số. Quét 60 ca TT (chỉ đọc đầu vào): 3 ca có operation 1 span bình thường (0e0bdcd10b, 5e8f996191, 541642b59e). Supervisor chạy tiếp sau lỗi phương pháp chưa phân loại vì lỗi đó không lan sang slot khác; lỗi nguồn/hạ tầng vẫn dừng vì có thể lan. Không tách bảng quy tắc ở lượt này để giảm phần sửa sau mở test. Bằng chứng tính đúng: so v1↔v2 trên slot trùng. Kết luận phụ thuộc: bảng TraceRCA/MicroRank TT và C-c; A4 không đổi định nghĩa.


## WHY-79. Sửa dấu span gốc Nezha bằng wrapper và C-d3 OB bổ sung — T-054, 08/11/2026

**Chọn gì.** Chuẩn hóa `ParentID = "root"` của trace Nezha thành parent rỗng bằng một wrapper trong `results/T-054/runs/sua-cd3-ob-001/lane.py`, chạy ngay sau `src/m1/adapter.py::ca_nezha` đã ghim; không sửa `src` ở lượt này. Tính C-d3 cho 34 ca OB test từ trung gian M1 đã lưu (`canh`, `dau_vao_cd3.diem`, `kenh_co`) cộng tập span gốc trong A dựng lại qua đúng bộ đọc/adapter đã ghim + wrapper; không chạy lại M1 trên test.

**Vì sao.** Adapter M1 chỉ coi `None`/`''` là parent rỗng, nên span gốc Nezha bị đếm là mồ côi và `dich_cd3` rỗng ở 34/34 ca test và 22/22 ca dev (K3:87 và `src/do_thi/builder.py:79` đã biết dấu này). Theo code, `cha=None` ở cả hai cách, nên span bọc, E1, E2, `G_N` không đổi; chỉ đích C-d3 và số đếm chẩn đoán đổi — kiểm bằng dev. Sửa `src/m1/adapter.py` tại chỗ sẽ đổi hash đang ghim trong plan/protocol main013-v2 (gồm 180 job TORAI A chờ chạy), plan RE3 và plan chấm T-055.

**Phương án đã xét.** (1) Sửa `src` ngay: chặn TORAI A, phá pin của phần không liên quan. (2) Sửa chung `_rong` trong lõi: chạm cả TT/RE3. (3) Không chạy C-d3 OB, ghi "chưa đánh giá do lỗi adapter": còn C-d1/C-d2, thiếu đối chứng đường tới đích. (4) Chạy lại M1 OB trên test với wrapper: thêm tiếp xúc test, không cần vì C-d3 chỉ phụ thuộc trung gian đã lưu + span gốc.

**Bằng chứng.** `kiem-wrapper.json` (3 trường hợp span; driver chế độ cũ tái lập bản ghi `dev-ob-001` 25/25 khóa); `dev-so-sanh.json` (22 ca dev, hai EC2); `cd3-test-phi-nhan.json` (34/34 ca chế độ cũ tái lập đúng `dau_vao_cd3` đã lưu); kiểm đường chấm trên 60 ca C-d3 TT khớp `tables.json`.

**Kết luận phụ thuộc.** Bảng C-d3 OB bổ sung là **sửa sau khi đã xem test** (C-15 B), không là phép kiểm độc lập; không đổi A4 hay bảng chính. `src/m1/adapter.py` còn lỗi cho các lượt OB sau: sửa chính thức sau khi TORAI A nhận/chấm xong, đề xuất riêng kèm ghim mới.

**Cập nhật 08/11/2026.** TORAI A đã tạm hoãn vô thời hạn (DECISIONS, mục “TORAI A tạm hoãn vô thời hạn”). Mốc sửa `src/m1/adapter.py` đổi thành: chỉ sửa khi có lượt chạy Nezha-OB mới, kèm ghim lại pin (DECISIONS, mục “mốc sửa adapter Nezha”). Câu “sau khi TORAI A nhận/chấm xong” ở trên không còn hiệu lực.

## WHY-80. Vị trí, tải và nhãn cho T-059 — Gói sửa đã duyệt, 11/11/2026

- **Chọn và vì sao.** `GET /api/v1/events/{id}` ở revision `9eea593a` đọc PostgreSQL qua `EventService.readPublic` và `EventRepository.find`. Dùng tuyến Event→event_db ở phát triển và Booking→booking_db ở đánh giá để kiểm chuyển vị trí trong cùng cơ chế trễ JDBC. Hai tuyến dùng cùng DB vật lý. Giữ proxy Event trong mọi ô, mọi pha và các đêm nền của chiến dịch để sự có mặt của proxy không chỉ ra nhãn. Phương án chỉ dùng Booking làm giảm cấu hình 2i, đồng thời bỏ cơ hội thử cạnh JDBC trên dữ liệu phát triển. Pool Event có cấu hình Hikari riêng nhưng thiếu hook, đầu dò và xác nhận hiệu lực. Consumer phát vé hiện chỉ có vị trí Ticket. Phạm vi chuyển vị trí đối với hai cơ chế này cần báo rõ.
- **Nhãn và điều kiện.** Tiêm tại Hikari Booking chiếu về `booking-service`. Can thiệp ở DB đích chỉ nhận `booking_db` khi đường trực tiếp và đường qua proxy cùng xác nhận mất khả dụng, DB đối chứng vẫn khỏe. Tiêm trên tuyến JDBC giữ nhãn cạnh. Mất kết nối từ một caller có thể trông giống mất DB. Vì vậy cần kiểm độc lập và giữ riêng đáp án mà telemetry phân biệt được.
- **Tải và quota.** Cùng hỗn hợp cho mọi ô, mọi pha, các đêm nền và đối chứng khỏe. Tốc độ được phép đổi theo lịch khai trước. Luồng đặc thù ưu tiên chạy chung ở nhịp thấp. Nếu cần hồ sơ riêng, đối chứng dùng cùng lịch nghiệp vụ và báo riêng phần suy được loại ca từ tuyến quan sát. Chi phí thêm gồm fixture, kiểm đúng nhịp và đo tải đến từng backend. Gateway ghim Spring Cloud BOM `2025.1.3`; kiểm bytecode JAR `5.0.3` thấy bucket theo route × khóa địa chỉ kết nối. B4 xác nhận revision/config hiệu lực và ghi ngưỡng số request/giây thực đến từng service, khoảng đo, giới hạn sức khỏe trước lượt chấm. Các cảnh báo của ca bị giới hạn vẫn được báo ở nhóm riêng. Ưu tiên giữ quota thật, chốt phương án quota thử trước khi khóa nếu cần vượt giới hạn của cấu hình thật. Đổi quota làm đổi điều kiện triển khai và phải ghi R-10.
- **Phép so và giới hạn.** Báo kết quả ở mức tải tham chiếu trên vị trí đánh giá và hiệu ứng đổi tải trong cùng ô đánh giá. Đếm thêm mọi lượt của mức tải thứ hai vào dự toán. Ghi cả ca thiếu bằng chứng, ca bị giới hạn và ca tải suy giảm. Quy tắc này giúp phân biệt ảnh hưởng của vị trí, tải và cách sinh dữ liệu. Hiệu lực can thiệp, mức tải, số lượt và lợi ích đồ thị cần số đo sau. Căn cứ: SPEC T-059, D.9, WHY-04, B1.9 T-043, PLAN §5 và phản biện lượt 1–2.

## WHY-81. T-064: chạy và chấm M1-FT trên `exp-obs` (cùng nền với P7) — 12/11/2026 21:30Z

- **Chọn gì.** Mọi lần chạy M1-FT dùng để chấm (P7 tham chiếu, biến thể, tổ hợp) chạy trên `exp-obs` (aarch64) bằng đúng venv của P7 (`/opt/flash-ticket-rca/venv`, Python 3.12.3, numpy 1.26.4, scipy 1.14.1), user `rca`, từ thư mục làm việc riêng `/opt/rca-m1ft/` (không sửa thư mục ghim T-058). Laptop chỉ dùng cho kiểm đơn vị và thử nhanh, không dùng số của laptop trong bảng chấm.
- **Vì sao.** Phép kiểm tương đương P7 (SPEC T-064 bước 2) trên laptop x86 (cùng phiên bản numpy/scipy) cho bản ghi lệch P7 ở chữ số cuối của số thực (vd. khóa hạng `0.3080217566889036` so với `0.30802175668890364`, `results/T-064/kiem/tuong-duong-p7-laptop-x86.json`), dù tất định trong từng máy. Trên `exp-obs` cả 9 ca trùng SHA hai lần chạy (`results/T-064/kiem/tuong-duong-p7-exp-obs.json#/tat_ca_trung`). Lệch ulp có thể đổi thứ tự khi hai khóa gần nhau, nên so biến thể với P7 phải trên cùng nền. Thêm nữa `exp-obs` nhanh hơn laptop (~6–10 s/ca so với ~10–18 s/ca, cùng file) — luật 19.
- **Phương án đã xét.** (a) Chạy trên laptop và so "tương đương cấu trúc" (cùng thứ hạng/verdict): bỏ vì SPEC yêu cầu trùng SHA và vì lệch ulp có thể đổi thứ tự hòa. (b) Ép số thực về số chữ số cố định: đổi đầu ra P7, vi phạm "tắt thay đổi thì y hệt P7".
- **Bằng chứng.** Hai file JSON trên; hash cây mã `src/m1` trên máy trùng bản ghim (`m1-source-pins.json`, 39/39) và trùng `src/m1` trong `/opt/flash-ticket-rca`.
- **Kết luận phụ thuộc.** Mọi bảng chấm T-064. Nếu sau này đổi nền chạy, phải lặp phép kiểm tương đương trước khi dùng số.

## WHY-82. T-064 H1c: xếp hạng cạnh trong danh sách chung nút + cạnh — 12/11/2026 22:40Z

- **Chọn gì.** Biến thể H1c xuất cạnh theo **danh sách xếp hạng chung**: duyệt thứ hạng nút của bản (nhóm hòa theo thứ tự), ngay sau mỗi nhóm nút chèn các cạnh có cờ và được định vị `rieng_canh` (H1b) mà đầu mút tốt nhất thuộc nhóm đó, sắp theo điểm e giảm dần. Hạng của một cạnh = 1 + số phần tử (nút hoặc cạnh) đứng trước nó. Bảng nút chấm qua phép chiếu của tiêu chí (cạnh hạng k → hai đầu hạng k nếu chưa có hạng tốt hơn); bảng cạnh dùng đúng hạng này.
- **Vì sao.** Kiểm cài đặt trên 9 ca T-062 (`results/T-064/cham/kiem-cai-dat-3.json`, vai trò kiểm cài đặt, **không** phải tập chọn): H1a/H1b xếp cạnh trong danh sách riêng, nên cạnh yếu giữa hai nút không phải gốc đứng hạng 1 (SLOW-BOOK: `payment-service→payment_db` e = 0,033; HTTP5-EVENT: `keycloak→keycloak_db` 0,037), phép chiếu đẩy hai đầu lên ngang gốc → AC@1 5 → 3,67. Hạng trong danh sách cạnh riêng không so được với hạng nút, trong khi tiêu chí chiếu theo cùng con số k. Danh sách chung làm con số k có cùng nghĩa ở hai bảng ("phần tử thứ k đáng nghi"). Cạnh đặt sau đầu mút tốt nhất vì bất thường cạnh là lời giải thích cho bất thường của nút đó.
- **Phương án đã xét.** (a) Danh sách cạnh riêng (H1a/H1b) — giữ làm đối chứng, đã thấy điều kiện thất bại trên. (b) Ngưỡng điểm e tối thiểu cho cạnh — không có nguyên lý chọn ngưỡng, dễ khớp theo ca. (c) Đổi phép chiếu — là đổi tiêu chí sau khi xem kết quả, không được (tiêu chí mục 2).
- **Điều kiện thất bại.** Cạnh không bao giờ đứng trên đầu mút tốt nhất của nó: gốc dạng cạnh có hạng cạnh ≥ 2 (vẫn có thể top 3). Nếu đầu mút tốt nhất của cạnh gốc xếp thấp (vd. nút bên gọi không bất thường), cạnh cũng xếp thấp.
- **Bằng chứng / trạng thái.** Thiết kế sau khi xem kiểm cài đặt trên 9 ca T-062; tập chọn (dev bản 2) chưa có, chưa xem. Báo rõ trong hồ sơ chọn rằng H1c được thiết kế sau kiểm cài đặt trên 9 ca T-062.
- **Kết luận phụ thuộc.** Bảng cạnh và bảng nút của mọi biến thể H1c; luật giữ 3 của tiêu chí cho H1.

## WHY-83. T-063: thay SLOW-BOOK bằng HTTP5-EVENT ở hai mức tải trong đợt thu dev bản 2 — 12/11/2026 22:54Z

- **Chọn gì.** Đợt thu dev bản 2 không dùng SLOW-BOOK; thay bằng HTTP5-EVENT ở tải chuẩn và HTTP5-EVENT-FLASH (cùng hook, cùng cường độ, tải ×3), hook Event nhắm sự kiện tải mới `3e7c1df9-ada4-4081-94a1-548b80a5da86`.
- **Vì sao.** Hook `http.delay`/`http.error` của `src/rca-test` bắt buộc `targetId` (`RcaFaults.java:103`), Booking còn bắt buộc `subject` của chủ đơn (dòng 129). Tải mua vé (phụ lục 2) tạo đơn mới mỗi hành trình, nên SLOW-BOOK nhắm một đơn cố định không chạm lưu lượng thật. Sửa hook sang "mọi đơn" cần sửa `services/booking-service/src/rca-test` và build lại image — ngoài danh sách đường dẫn được ghi rõ trong quyền (`CHIEN-DICH-M1-FT.md` mục 6). T-059 `split_rules` "Phát triển" cho phép: "Nếu SLOW-BOOK chưa đạt thì thay bằng một ô dev đủ bằng chứng, ghi trước khi chạy", và yêu cầu một ô dev chạy ở hai mức tải để đối chiếu cùng lỗi dưới tải khác (phục vụ H7).
- **Phương án đã xét.** (a) Sửa hook + build lại: hiệu quả nhất nhưng vượt phạm vi đường dẫn đã ghi → chỉ làm nếu Minh mở quyền. (b) Thêm bước "tra cứu đơn cố định" vào tải: làm đổi hỗn hợp tải vì một ô lỗi, chỉ chạm phần nhỏ lưu lượng. (c) Bỏ hẳn phép so hai mức tải: mất đối chứng cho H7.
- **Hệ quả.** Mất ô "service chậm" ở Booking trong đợt dev (giữ CPU-BOOK, REDIS-BOOK, NET-GW-BOOK ở Booking). HTTP5-EVENT là lỗi 5xx (không phải chậm) — đối chiếu hai mức tải đo lỗi, không đo trễ. Ghi giới hạn này trong hồ sơ chọn.
- **Kết luận phụ thuộc.** Danh mục ô và lịch đợt thu dev bản 2 (`results/T-063/o-dev-bo-sung.md`, `lich-2.json`); đánh giá H7.

## WHY-84. T-063: revision FlashTicket cho đợt thu dev bản 2 — giữ image `6b21ed55` — 13/11/2026 02:18Z

- **Chọn gì.** Đợt thu dev bản 2 chạy đúng các image đang chạy trên `exp-app`: 7 service `ft-local/<svc>:arm64-t062-6b21ed55` (booking/event build `-P rca-test`), Keycloak `ft-local/keycloak:arm64-776d9c9e`. Thay đổi so với T-062 chỉ ở cấu hình quan sát/tiêm (TD-01..08), không build lại.
- **Vì sao.** Đầu nhánh `rca/quan-sat-log` là `fba6bc8` (merge `main`: K3s, bỏ API thống kê organizer của Event, cấu hình discovery Payment→Booking mặc định tắt, mở probe liveness/readiness). Đọc diff code nghiệp vụ `6b21ed55..fba6bc8` (`results/T-063/dong-bang/revision-ung-vien.md`): luồng mua trên Docker với discovery tắt không đổi hành vi; API bị bỏ không thuộc tải. Luồng lõi đã kiểm trên `6b21ed55` (giao dịch `COMPLETED` có vé, hai lượt 10 phút — `results/T-062/tai-2/lap-2-luot.md`). Build lại chỉ để theo `main` sẽ buộc kiểm lại luồng lõi mà không thêm tín hiệu cho H1–H8; Minh chốt không thu lại mỗi lần `main` có commit mới (DECISIONS, chiến dịch 13/11).
- **Phương án đã xét.** Build từ `fba6bc8`: được liveness `permitAll` (đầu dò 200 thay 401) — lợi ích nhỏ, H5 đã dùng được mã 401. Build kèm sửa hook `src/rca-test`: ngoài đường dẫn được ghi rõ trong quyền (WHY-83).
- **Kết luận phụ thuộc.** Hồ sơ đóng băng `results/T-063/dong-bang.md`; mọi ca dev bản 2. Nếu sau này dùng revision khác, dev bản 2 không còn là cùng hệ thống.

## WHY-85. T-064 H8-sàn: sàn độ lớn 1 ms cho đơn vị thao tác — ghi bổ sung 13/11/2026 22:48Z

- **Ghi muộn.** Mục này được thêm **sau** khi sàn đã dùng trong kết quả hai lượt chọn (thiếu sót của người làm, phản biện T-064 lượt 1 điểm R3). Nguyên lý dưới đây có từ trước khi chấm, trong docstring `src/m1_ft/thanh_phan/h8_san.py` và sổ `results/T-064/so-bien-the.jsonl` (dòng V002); mục này không thêm lý do mới sau khi xem điểm.
- **Chọn gì.** Với đơn vị thao tác (`op|…`, `canh|…`), bỏ cờ của một hướng khi độ vượt trung bình của các mẫu A ngoài ngưỡng nhỏ hơn δ = 1 ms. Đơn vị metric, log, đếm không đổi. δ = 0 phải trùng P7 (đã kiểm, V001).
- **Vì sao.** Quan sát (đã kiểm, `results/T-063/ca-nen/PHAN-TICH.md`, `results/T-064/cham/t062-p7.json`): E4 của P7 không có sàn độ lớn, nên thao tác nền dịch khoảng 0,1 ms với vài trăm mẫu vẫn được gắn cờ, và 4/4 ca không tiêm lỗi của T-062 bị kết luận có nguyên nhân.
- **Trạng thái của con số 1 ms: ngưỡng thực dụng, giả thuyết chưa kiểm.** Lý do đã ghi trước là "dịch nhỏ hơn hạt lập lịch CPU thì không phân biệt được với nhiễu lập lịch". Đây là **suy luận chưa kiểm**: tài liệu CFS mô tả độ mịn lập lịch, không xác lập 1 ms là ranh giới giữa lỗi và nhiễu của phép đo này; chưa có số đo nhiễu trên máy thu. Trường hợp nó sai: nhiễu thật lớn hơn hoặc nhỏ hơn 1 ms nhiều lần. Không kiểm được trong task vì mỗi ô chỉ một lần thu; cần chạy lặp ca bình thường hoặc quét δ.
- **Phương án đã xét.** (a) Không sàn (P7): K 4/5 trên tập A. (b) Sàn tương đối theo ngưỡng h: dự đoán từ số đã có là đổi CPU-BOOK-2 lấy EVENT-DB-LAT, chưa chạy (`results/T-064/phan-tich/ghi-chu-co-che-dev2.md` Q6). (c) Quét nhiều giá trị δ trên tập chọn: dễ khớp quá với 12–13 ca, chưa làm.
- **Điều kiện thất bại (đã thấy).** Lỗi thật có độ vượt dưới 1 ms bị bỏ cờ: ở CPU-BOOK-2 hai thao tác của Booking có độ vượt khoảng 411 và 506 µs bị bỏ, đáp án tụt hạng 1 → 2. Độ vượt lớn nhất bị bỏ ở ba ca không lỗi là 762–985 µs, sát sàn, nên K nhạy với δ (`results/T-064/chu-thich-thao-tac-nen.md` mục 3).
- **Bằng chứng.** Tập A: K 4 → 3, AC@1 và AC@3 không đổi, EVENT-DB-LAT 2 → 1, CPU-BOOK-2 1 → 2 (`results/T-064/cham/chon-dev2-luot1-tap12.json#/ban/V002-H8s1`). Một lần thu mỗi ô.
- **Kết luận phụ thuộc.** Mọi bản có H8s1 (V002, V028, V034…) và vị trí đứng đầu của V002 theo §5 trên tập A. Nếu δ đổi, các kết luận này phải chấm lại.

## WHY-86. T-064 H5b: thành phần "chết im" từ 60 s được xếp nhóm đầu — ghi bổ sung 13/11/2026 22:48Z

- **Ghi muộn.** Thêm sau khi H5b đã dùng trong kết quả lượt chọn 2 (R3 của phản biện T-064 lượt 1). Nguyên lý có trước khi chấm, trong docstring `src/m1_ft/thanh_phan/h4_h5.py::_chet_im` và sổ biến thể (dòng V032, 13/11 19:31Z).
- **Chọn gì.** Một service được coi là chết im khi đầu dò sống của chính nó phản hồi ở mọi mẫu trước t (ít nhất 4 mẫu), rồi từ mẫu không phản hồi đầu tiên sau t tới hết cửa sổ không phản hồi lại lần nào, và đoạn đó dài ít nhất 60 s. Thành phần chết im được đưa lên nhóm đầu của bảng xếp hạng.
- **Vì sao.** Cơ chế đã lần (`ghi-chu-co-che-dev2.md` Q3): khi một service bị dừng suốt pha lỗi, mọi kênh của nó mất mẫu, P7 loại nó khỏi danh sách. H5 (kênh liveness chấm theo độ lớn) trả nó về danh sách nhưng kênh nhị phân có độ lớn tối đa 1, không so được với độ trễ hàng trăm của các service chịu hậu quả, nên chỉ đứng hạng 4.
- **Vì sao 60 s.** Bằng 4 bước dò 15 s, để một lần dò hụt hay một lần khởi động lại ngắn không bị coi là chết. Con số này **chưa kiểm** trên ca khởi động lại thật; tập chọn không có ca như vậy.
- **Phương án đã xét.** (a) H5 theo độ lớn: hạng 4 (V018). (b) H2 kênh tài nguyên: hạng 4 nhưng K tăng (V012). (c) Nhân hệ số cho kênh liveness: không có nguyên lý chọn hệ số.
- **Điều kiện thất bại.** Service chết vì một service khác (hậu quả) vẫn được đưa lên nhóm đầu; đầu dò mất đường mạng nhưng service còn sống bị coi là chết; chết ngắn hơn 60 s không được nhận.
- **Bằng chứng và giới hạn.** Tập B: PAUSE-PAYMENT vắng → hạng 1 (`results/T-064/cham/chon-dev2-luot2-tap13.json#/ban/V032-H5b/ca/46aab4be`); H5b chỉ báo chết im ở đúng ca này trong 22 ca (`results/T-064/kiem/kiem-luot2.json#/chet_im`). **Thiết kế sau khi xem đúng ca này, chỉ một ô**: đây không phải bằng chứng độc lập về hiệu quả.
- **Kết luận phụ thuộc.** V032, V033, V034 và vị trí đứng đầu của V032 trên tập B; cả hai còn phụ thuộc việc Minh có nhận tập B hay không.

## WHY-87. T-064 Kiểm độ nhạy mốc: dựng lại đầu vào từ gói ca với t' = t + d, xuất lại gói metric bổ sung quanh t'

- **Chọn gì.** `chay_ca.py --doi-t d` dựng lại cả bảy tham số M1 từ gói ca (`m1_ft/doi_moc.py`), đi đúng đường của runner ghim `run-m1.py`: `adapt(..., t')`, cấu hình khóa P7 cộng `params_ca`, cùng các phép kiểm trường cấm và rò giá trị. Mọi nơi dùng t đều dùng t': `inputs[5]`, cửa sổ cắt span/log/metric của M1, `span_phu`, H5b. Gói metric bổ sung (chỉ có [t−300, t+300]) được xuất lại quanh t' bằng đúng bộ xuất `results/T-063/dong-goi/xuat_bo_sung.py`. Với 9 ca T-062, gói gốc quanh t chỉ được dùng khi các kênh cấu hình đọc tới (live-down, live-ms) rỗng; `chay_ca.py` kiểm điều này và từ chối nếu không đúng.
- **Vì sao.** `method-input.json` của P7 chỉ chứa [t−300, t+300). Nếu chỉ đổi `inputs[5]`, cửa sổ của M1 hụt |d| giây ở một đầu: A ngắn đi khi d = +30, N ngắn đi khi d = −30. Khi đó phép kiểm độ nhạy trộn hai hiệu ứng, dời mốc và mất dữ liệu. Gói ca chứa dữ liệu thô [t−600, t+600). Cả 22 ca được đóng gói lúc t + 783…808 s, nên có đủ dữ liệu cho |d| ≤ 300.
- **Đã xét.** (1) Chỉ đổi `inputs[5]`: bị loại vì trộn hiệu ứng như trên. (2) Cắt bớt cửa sổ còn [t'−270, t'+270]: bị loại vì đổi độ dài N/A so với P7. (3) Dùng gói bổ sung quanh t cho mọi ca: một phần cửa sổ của kênh live sẽ nằm ngoài gói, độ phủ A/N của kênh đó đổi.
- **Bằng chứng.** Dựng lại với d = 0 cho `method-input.json` trùng byte bản đã lưu (laptop, a5539fba; trên `exp-obs` là bản V058, 22 ca, xem `BAN-GIAO-C.md`). `chay_ca.py` cũ và mới cho đầu ra trùng byte ở đường mặc định (V041, a5539fba). 26 gói bổ sung xuất lại: 252.125 điểm chung trùng giá trị gói gốc, 0 lệch (`doi-moc/kiem-bo-sung-doi-t.json`). Bộ đệm đầu vào kiểm hash khi đọc.
- **Kết luận phụ thuộc.** Kết quả dời mốc ±30 s của P7, V032, V041 (V052–V057), phép thử giả d = −300 (V059).
- **Giới hạn.** Mỗi ô một lần thu. Dời mốc là phép kiểm độ nhạy của phương pháp với mốc t do người dùng đưa vào, không phải đo dao động giữa các lần thu.

## WHY-88. T-064 H8-adapter: nối chuỗi container khi chỉ khác nhãn runtime và không chồng lấn trong mốc mẫu gốc

- **Chọn gì.** Trước adapter ghim, các chuỗi của cùng một metric logic (kênh, thực thể) được nối theo thời gian khi thỏa cả ba điều kiện: (i) chỉ khác nhau ở `container_id`, `container_name`, `service_instance_id`; (ii) không chồng lấn trong mốc mẫu gốc (`timestamp()`): mẫu cuối của chuỗi trước sớm hơn mẫu đầu của chuỗi sau; (iii) kênh có mốc mẫu gốc. Ở mỗi mốc đánh giá có nhiều điểm, giữ điểm có mốc gốc mới nhất. Không thỏa điều kiện thì giữ hành vi P7 (adapter ném lỗi). Mặc định tắt.
- **Vì sao.** Đây là nhu cầu kỹ thuật (luật 18), không phải cách xử lý một hạn chế phương pháp. Khi một container bị tạo lại trong [t−600, t+600], P7 ERROR cả ca. FlashTicket Compose chạy một container cho mỗi service. Lần theo `thuong01`: trong mốc gốc, chuỗi cũ và mới không chồng lấn (ví dụ api-gateway [−609, −509] s và [−499, 591] s). Phần trông như chồng lấn trên lưới đánh giá là do lookback ~300 s của PromQL lặp lại mẫu cuối của container đã dừng. Giữ điểm có mốc gốc mới nhất cho đúng giá trị mà một chuỗi duy nhất đã cho.
- **Đã xét.** (1) Cộng hoặc lấy trung bình các chuỗi: bị loại vì sai khi hai container không đồng thời (cộng lặp mẫu cũ vào mẫu mới) và vì cần khai phép gộp. (2) Bỏ nguồn bị trùng: mất kênh cpu/mem của thực thể vừa tạo lại, đúng nơi có thông tin. (3) Gộp cả khi chồng lấn: chỉ đúng với nhiều bản sao, cần phép gộp khai báo; chưa có trường hợp này nên không làm.
- **Bằng chứng.** `phien-c/h8-adapter/dem-chuoi-trung.json` (37 gói: chỉ thuong01 bị lỗi). Test `src/m1_ft/tests/test_h8.py`: tách giả cpu+mem booking của a5539fba tại t+60 theo đúng ngữ nghĩa lookback; adapter ghim ném lỗi; nối lại cho rows, owners, indices, clocks, coverage, aliases trùng bản gốc; chồng lấn và khác nhãn ngoài runtime thì không nối. Trên exp-obs: thuong01 P7 ERROR, bản có H8-adapter chạy được (14 nhóm nối, 0 nhóm không nối); 22 ca trùng bản cha. **Đính chính chú thích mã:** `mat_mau` không phải chỉ số mất thông tin. Ở thuong01 `mat_mau` = 12: mỗi mẫu là mẫu gốc cuối của container cũ, nằm cùng bước lưới 15 s với mẫu đầu của container mới (ví dụ −509 s và −499 s), nên không phải mẫu mới nhất ở mốc đánh giá nào. Một chuỗi liên tục cũng không bao giờ trả các mẫu này. Docstring của `h8_adapter.py` ("điểm bị bỏ luôn là bản lặp… `mat_mau == 0`") cần sửa ở lần đóng gói mã kế tiếp; chưa sửa vì sẽ đổi `ma_nguon_sha256` đã ghi trong đầu ra.
- **Kết luận phụ thuộc.** V060, V061; mọi bản sau có H8-adapter.
- **Điều kiện thất bại.** Nhiều bản sao chạy song song; nhãn khác ngoài nhóm runtime (ví dụ chuyển host); container mới có mức tài nguyên khởi động khác hẳn nên bị gắn cờ (thông tin thật, nhưng có thể không phải gốc).

## WHY-89. T-064 H8-log: kết cục nghiệp vụ theo hợp đồng B16 — phân loại dòng lỗi (H8-log-kq) và hai kênh metric (H8-log-chuoi)

- **Chọn gì.** Trường `outcome` của log JSON được dùng theo ngữ nghĩa B16 (`B16-observability-baseline.md` dòng 56): FAILED ∪ UNKNOWN là kết cục lỗi; SUCCESS, REJECTED (từ chối theo luật nghiệp vụ) và RETRY (lỗi tạm, tự thử lại) là kết cục không lỗi.
  - **H8-log-kq:** dòng có `outcome` được phân loại lỗi theo kết cục thay vì severity, trong kênh `log_loi` sẵn có (cùng đơn vị, E4 đếm, cổng D1, lớp lan ngược).
  - **H8-log-chuoi:** thêm hai kênh metric 15 s theo service, qua đường metric chung (E4 phân vị + G3): `log-kq-loi` là tỷ lệ kết cục lỗi (lớp "lỗi"); `log-kq-ok` là số SUCCESS/s (lớp "lưu lượng"). Ô được đóng dấu ở đầu ô để không trộn N với A.
  - Nút là thực thể ghi log. Không thêm cạnh. Nơi đặt: log ứng dụng, qua Collector, vào `raw-logs.jsonl` của gói ca (`bo_sung.log_phu`).
- **Vì sao.** `outcome` là trường hợp đồng, còn severity do người viết code chọn. Kênh `log-kq-ok` phủ phần xử lý bất đồng bộ qua RabbitMQ (saga thanh toán, phát vé), phần mà kênh `workload` HTTP của P7 không thấy.
- **Đã xét.**
  - (1) Thêm đơn vị log mới bằng cách bọc `don_vi_log`: P7 dùng cổng D1, mà mốc N của mỗi đơn vị log được tính bên trong `chuoi._chay` từ dòng lỗi theo severity, nên đơn vị mới lệch số dòng và ERROR. Không thể làm mà không sửa `src/m1`.
  - (2) Một đơn vị cho mỗi `reasonCode`: nhiều phép thử hơn, tăng cờ giả; chưa có căn cứ.
  - (3) Tính RETRY là lỗi: RETRY|SMTP_UNAVAILABLE của ticket là nền liên tục khoảng 3.500 dòng/300 s, sẽ lấn tín hiệu FAILED.
- **Bằng chứng đầu vào.** `h8-log/dem-log-nghiep-vu.json`, `cheo-severity-outcome-22ca.json`. Trong cửa sổ của 22 ca, ERROR trùng FAILED ở 10.424/10.424 dòng. H8-log-kq chỉ đổi lớp 4.490 dòng UNKNOWN, ở 10 ca. Kết quả chấm ở `BAN-GIAO-C.md`.
- **Khai.** Thiết kế sau khi đã xem số đếm theo ca × service. Người làm biết mã ca ↔ ô (ví dụ event-service chỉ có log FAILED ở hai ca HTTP5-EVENT). Định nghĩa kênh theo B16, không chỉnh theo đáp án.
- **Kết quả** (`cham/h8.json`): H8-log-kq không đổi đại lượng chấm nào (phép 1, 2). H8-log-chuoi: phép 1 GIU (l1), PAUSE-PAYMENT — → 4, tổng hạng 15 → 13, ở một ô đã xem trước; phép 2 không tác dụng.
- **Kết luận phụ thuộc.** V062–V065.
- **Điều kiện thất bại.** Dịch vụ chỉ ghi log khi lỗi (event-service): N rỗng. Phía gọi ghi FAILED cho lỗi của bên được gọi (lan ngược xử lý như `log_loi`). `log-kq-ok` đổi theo tải (H7 không áp cho kênh này). user-service không ghi log nghiệp vụ, nên không có kênh này.


## WHY-90. T-063 — Build lại riêng Event từ `6b21ed55` + bản vá hook H3, thu trên "bản 3" — chép từ results/T-063/thu3/de-xuat-WHY.md ngày 14/11/2026 (điều phối)

- **Chọn gì:** sửa `RcaFaults.java` của Event (bỏ phép so tên service ở `start()` và `poll()` để `pool.hold` chạy ở Event; điều kiện `subject` của `http()` giữ nguyên), commit `e557307` trên `rca/quan-sat-log`. Image Event build từ worktree tách tại `6b21ed55` (bản đang chạy) + đúng bản vá đó → commit cục bộ `76b34d5e`, image `ft-local/event-service:arm64-t063h3-76b34d5e`. Sáu service khác, env, compose, Collector, Toxiproxy giữ nguyên.
- **Vì sao:** POOL-EVENT không thử được vì hook chỉ chạy ở Booking (`chay/D2B-KET-QUA.md`); Minh duyệt sửa hook (DECISIONS 14/11). Không build từ đầu nhánh `fba6bc8` vì nhánh đã merge code nghiệp vụ mới của Event (bỏ API thống kê) — sẽ đổi hành vi ngoài hook.
- **Phương án đã xét:** (1) build từ `fba6bc8`: loại vì đổi code nghiệp vụ; (2) chấp nhận H3 "chưa thử được": loại vì Minh đã cho sửa; (3) chọn đúng nền `6b21ed55` + bản vá: chọn.
- **Bằng chứng:** `thu3/thay-doi-may.md` T3-03…T3-05; test `RcaFaults*` 8/8 đạt trên `exp-app`; audit `pool.hold.started` ở Event khi tiêm thử (`thu3/KE-HOACH.md` bổ sung 2).
- **Hệ quả, giới hạn:** ca thu bù 3 nằm trên bản triển khai khác bản đóng băng 2 (watchdog hook 100 ms chạy ở Event cả khi không tiêm; container Event mới). Không gộp thẳng với 13 ca bản 2; dùng BINH-THUONG và EVENT-DB-LAT trên bản 3 để so. Nhãn `service.version` của Event vẫn là `6b21ed55…` vì lấy từ env, env không đổi (image mang nhãn revision `76b34d5e`).
- **Kết luận phụ thuộc:** mọi kết quả M1 trên ô POOL-EVENT, CONSUMER-BOOK-SLOW-X3 và hai ô đối chứng bản 3.


## WHY-91. T-063 — Cường độ POOL-EVENT = 5 connection (cạn hẳn pool max 5) — chép từ results/T-063/thu3/de-xuat-WHY.md ngày 14/11/2026 (điều phối)

- **Chọn gì:** `pool.hold` = 5 trên pool Hikari Event (max 5), 600 s.
- **Vì sao:** quy tắc khai trước (`KE-HOACH.md` §4): chọn 4 nếu có `pending` > 0; chạy thử ×1: mức 4 cho `used` = 4, `pending` = 0 suốt pha, p50 không tăng → không có tín hiệu chờ pool. Mức 5: `used` 5, idle 0, `pending` 2–25 (tb 10,1), 5xx Event 0,18–0,34/s, p50 lên tới 10 s; 182/709 hành trình hỏng (`KE-HOACH.md` bổ sung 2; `do/thu-pool-prom.json`).
- **Phương án đã xét:** 4 (bão hòa một phần) — không đủ tranh chấp ở tải ×1; tăng tải cho mức 4 — không làm vì đổi thêm một biến so với ô cũ.
- **Hệ quả:** ô là "cạn hẳn pool", gần với triệu chứng DB không phản hồi ở phía người gọi; phân biệt dựa trên kênh pool (`used` = max, `pending` cao) và DB khỏe. Hook nhả rồi chiếm lại mỗi 120 s khi gia hạn lease.
- **Kết luận phụ thuộc:** phân xử H3 trên POOL-EVENT.


## WHY-92. T-063 — Ô H4: toxic bandwidth 1 KB/s trên AMQP của Booking dưới tải ×3, đối chứng BINH-THUONG-X3 — chép từ results/T-063/thu3/de-xuat-WHY.md ngày 14/11/2026 (điều phối)

- **Chọn gì:** `CONSUMER-BOOK-SLOW-X3`: toxic bandwidth 1 KB/s downstream trên proxy `booking-amqp` cả pha lỗi, tải hành trình ×3 suốt chu kỳ; đối chứng `BINH-THUONG-X3` cùng bậc tải.
- **Vì sao:** đợt 2 thử 3 cách ở tải ×1 không tồn queue. Đo trên bản hiện hành: byte broker→Booking ×1 tb 469 B/s, ×3 tb 1.393 B/s (`do/do-h4a-tom-tat.json`) — ×1 thấp hơn mức giới hạn nhỏ nhất của toxiproxy (1 KB/s), ×3 cao hơn. Thử 150 s ở ×3: tồn queue Booking 0 → 109, về 0 sau gỡ, cùng một kết nối, không có log heartbeat/ngắt (`KE-HOACH.md` bổ sung 3).
- **Phương án đã xét:** (1) tải > ×3 hoặc tăng tỷ lệ mua: cần sửa `tai_linux.py`/k6 (Codex), không cần vì ×3 đạt; (2) hook làm chậm xử lý consumer trong `src/rca-test` Booking: chưa có quyền Minh; (3) chọn (×3 + bandwidth).
- **Lệch kế hoạch đã ghi:** ngưỡng khả thi khai trước 1,5 KB/s ở ×3 không đạt (1,39 KB/s); vẫn thử trực tiếp vì phép thử rẻ và có điều kiện đạt riêng đã khai (`KE-HOACH.md` bổ sung 1).
- **Hệ quả, giới hạn:** cơ chế là giới hạn thông lượng giao message tới consumer Booking, không phải khâu xử lý consumer chậm; ô chạy ở bậc tải khác 13 ca cũ (×3), nên chỉ so được với BINH-THUONG-X3. Chưa kiểm TTL/DLQ của queue khi tồn 600 s.
- **Kết luận phụ thuộc:** phân xử H4; K của ca không lỗi ở tải ×3.


## WHY-93. T-063/T-064 Nhận "Sửa sau 1" và "Sửa sau 2" của thu bù 3; ô RECREATE-PAY vào tập chọn; điều kiện thất bại lookback của H5b — ghi 14/11/2026 (điều phối)

- **Chọn gì:** dùng `results/T-063/thu3/xac-nhan-ca-3-sua-sau.json` (6/6) theo quyết định Minh 14/11/2026 ("Nhận cả hai", DECISIONS). Ca RECREATE-PAY `ebd5ef38` và BINH-THUONG-X3 `1e5a3dc5` được xem là đã xác nhận.
- **Vì sao:** Sửa 1 chỉ sửa script cho khớp điều kiện đã khai; Sửa 2 dùng cùng nguồn đầu dò, bỏ hiệu ứng lookback 5 phút của `query_range` (mẫu thô cho thấy payment phục hồi ở ~t+53 s). Phương án thu lại bị loại vì Minh nhận.
- **Mặt trái:** cả hai sửa làm sau khi đã xem kết quả; ghi rõ ở `dieu-kien-xac-nhan-3.md`.
- **Điều kiện thất bại của H5b (WHY-86), từ BAN-GIAO-C §4d:** kênh liveness `httpcheck_error` đẩy qua OTLP không có dấu stale, nên `query_range` giữ giá trị 1 tới ~t+343 trong khi mẫu thô chỉ hụt ở t+3…t+43. Thời gian hụt thật ~50 s < ngưỡng 60 s, nên H5b kích hoạt do lookback, không do thành phần thật sự im 60 s. **Chưa kiểm** hệ quả lên các ca khác; chưa quyết sửa bộ xuất (`results/T-063/dong-goi/xuat_bo_sung.py`) hay chỉ ghi giới hạn.
- **Kết luận phụ thuộc:** mọi kết luận về H5b trên RECREATE-PAY; kết luận H8-adapter ở ca này (V060/V061 xếp payment hạng 1 nhờ nối chuỗi, không nhờ H5b).


## WHY-94. T-064 Đính chính thời điểm của WHY-87, 88, 89 (REVIEW-3 R8) — ghi 14/11/2026 (điều phối, phiên 5)

- **Sự kiện:** WHY-87 (dời mốc), WHY-88 (H8-adapter), WHY-89 (H8-log) được chép vào file này lúc 07:33–07:40Z 14/11, **sau** khi phiên C đã tính và chấm: sổ `results/T-064/so-bien-the.jsonl` ghi V052–V059 trước chấm 05:19:19Z, sau chấm 06:39:09Z; V060–V065 trước chấm 05:39:46Z, sau chấm 07:24:00Z. Tiêu đề ba mục không ghi "ghi muộn". Đây là vi phạm thứ tự của luật cứng 3 đã xảy ra.
- **Phần có trước kết quả:** lý do kỹ thuật, kỳ vọng và cấu hình trong dòng sổ `truoc_cham` (05:19:19Z, 05:39:46Z); docstring `src/m1_ft/doi_moc.py`, `thanh_phan/h8_adapter.py`, `thanh_phan/h8_log.py` trong cây mã `05273b2e…`/`b0f79a4d…` đã ghim trước lô; nháp WHY trong `results/T-064/phien-c/NHAT-KY.md` lúc 05:47Z (giữa lô).
- **Phần thêm sau kết quả:** đính chính `mat_mau` của H8-adapter (WHY-88), mọi câu dẫn số chấm.
- **Hệ quả:** ba mục không là bằng chứng độc lập và không có hiệu lực ngược. Không chạy lại (không khôi phục được thứ tự). Kết luận dùng WHY-87–89 giữ đúng nhãn "thiết kế sau khi xem dev" đã ghi trong sổ.


## WHY-95. T-064 Tập chọn dev bản 3 (17 ca) và đáp án cho ca thu bù 3 — ghi 14/11/2026 trước khi chấm (điều phối, phiên 5)

- **Chọn gì:** tập chọn chính mới `results/T-064/tap-chon-dev3-17.json` = 13 ca của `tap-chon-dev2-13.json` + 4 ô thu bù 3 có vai mới: POOL-EVENT `86dea661` (H3), CONSUMER-BOOK-SLOW-X3 `659a9dfb1ab0` (H4), BINH-THUONG-X3 `1e5a3dc5` (ca không lỗi ×3, đối chứng của ô H4), RECREATE-PAY `ebd5ef38` (H8-adapter). Ca lỗi 11, ca không lỗi 6. Tập 13 ca giữ làm lịch sử và độ nhạy.
- **Hai ca trùng vai không vào tập chính:** BINH-THUONG `7d1ee32f` và EVENT-DB-LAT `0a45b2e0` là lần thu thứ hai của ô đã có trong tập (ô cũ `eb48d6b3`/`729604d2`/`83073ed1`/`f20b0ca5`, `4af494a5`), thu để so bản 3 với bản 2 (WHY-90). Đưa vào tập chọn sẽ cho hai ô này trọng số gấp đôi và trái `tieu-chi-chon.md` §1 ("mỗi ô một lần thu"); chạy lặp để sau (hồ sơ chiến dịch §6). Hai ca được chạy cùng mọi bản và báo riêng thành nhóm "đối chứng bản 3" kèm tập 19 ca để báo độ nhạy, không dùng để chọn.
- **Đáp án** (khuôn `dap-an-dev2.json`, nguồn `results/T-063/thu3/BAN-GIAO-B.md` §5, `thu3/KE-HOACH.md` §2): POOL-EVENT gốc nút `event-service`, tập {event-service} (T-059: pool là vị trí vật lý, service là nút chiếu, như POOL-BOOK); RECREATE-PAY gốc nút `payment-service`, tập {payment-service}; BINH-THUONG-X3 ca không lỗi (K). CONSUMER-BOOK-SLOW-X3: gốc cạnh `booking-service → broker`, loại `message`; bảng cạnh chấm đúng cạnh này. **Tập chấp nhận ở bảng nút chờ Minh** (có tính `broker` không; câu hỏi gửi 14/11 ~11:45Z). Ca này chỉ được chấm sau khi Minh trả lời; quyết định sẽ ghi DECISIONS và bổ sung vào mục này bằng một WHY mới.
- **Phương án đã xét:** (1) gộp cả 6 ca (19 ca) làm tập chính: loại vì lý do trên; (2) chỉ thêm 3 ô lỗi, bỏ BINH-THUONG-X3: loại vì ô H4 chạy ở ×3 cần ca không lỗi cùng bậc tải để đo K (WHY-92); (3) chọn 17 ca.
- **Giới hạn:** ô ×3 (CONSUMER, BINH-THUONG-X3) khác bậc tải với 13 ca cũ; bốn ô mới thu trên bản 3 (WHY-90); RECREATE-PAY và BINH-THUONG-X3 vào tập nhờ hai "Sửa sau" làm sau khi xem hậu kiểm (WHY-93). Người làm đã thấy đầu ra P7 của 5 ca thu bù 3 (bàn giao B) và kết quả V058/V032/V060/V061 trên RECREATE-PAY (bàn giao C) trước khi khai tập này.
- **Kết luận phụ thuộc:** mọi áp §4, §5 trên tập dev bản 3; phân xử H3, H4, H8-adapter.


## WHY-96. T-064 Lô 5: đối chứng bỏ toàn bộ quan hệ của V041 (REVIEW-3 R6), tổ hợp H3/H4/H8-adapter, thêm d ∈ {−60, −15, +15}, chạy song song laptop — ghi 14/11/2026 trước khi chạy (điều phối, phiên 5)

- **Đối chứng R6.** V051 (V041 + DC) còn H1c (cạnh từ cặp span cha–con, chiếu về nút khi chấm) nên không phải bỏ toàn bộ quan hệ. Thêm V066 = V041 bỏ H1c (H5b + H8s1) và V067 = V066 + DC-bo-quan-he. Phép so: V041 → V067 (bỏ toàn bộ: H1c và E1/E2/E5); V041 → V066 (riêng H1c); V066 → V067 (riêng E1/E2/E5 trên nền không H1). Căn cứ "bỏ trọn": với E1 = `tat`, E2 = `tat`, E5 = False, E6 = `a`, lõi `src/m1` không dùng cạnh khi xếp hạng (PageRank chỉ ở E6b; E7 chỉ dựng vùng báo cáo); H5b, H8s1 không đọc cạnh. Phương án khác: chỉ thu hẹp chữ ở §12 (reviewer ưu tiên); loại vì SPEC hỏi trực tiếp "quan hệ có tác dụng tính toán không" và bản thay thế có cạnh V041 là ứng viên; chi phí 2 bản × 28 ca.
- **Tổ hợp mới cho ô thu bù 3.** Luật giữ §4 cần phép 2 (bỏ khỏi bản gộp) cho H3, H4, H8-adapter. Bản gộp quanh bản đứng đầu: V070 = V032 + H8-adapter + H3 + H4; bỏ từng phần: V069 (bỏ H3), V068 (bỏ H4), V061 (bỏ cả hai; có sẵn); bỏ H8-adapter: so V061 với V032 (có sẵn). Bản có cạnh: V071 = V041 + H8-adapter, V072 = V071 + H3 + H4. Lý do kỹ thuật: H3, H4 thêm kênh tài nguyên pool/queue gán về service (đã cài, chưa có ô); H8-adapter cần để P7 không ERROR ở ca container tạo lại. Kỳ vọng: chưa biết; điều kiện thất bại của H3/H4 ghi ở docstring `h2_h3_kenh.py`, `h4_h5.py`.
- **Dời mốc thêm.** d ∈ {−60, −15, +15} cho P7, V032, V041 trên 13 ca dev bản 2 và 9 ca T-062; d ∈ {−60, −30, −15, +15, +30} cho ba bản đó trên 6 ca thu bù 3. Cùng đường của WHY-87 (dựng lại đầu vào với t′ = t + d, xuất lại gói bổ sung quanh t′; |d| là bội của bước lưới 15 s). Mục đích: tìm ngưỡng lật ở các ô nhạy (HTTP5-EVENT, PAUSE-PAYMENT, 83073ed1) — chỉ báo cáo theo §7, không dùng chọn. Bản đề xuất cuối nếu khác ba bản này được chạy dời mốc ở lô sau.
- **Chạy song song laptop (luật 19).** `exp-obs` (ARM 2 lõi) giữ phần cần Prometheus và ca RECREATE-PAY (dữ liệu thô chưa qua bộ quét, không chép về laptop): xuất bù, dời mốc, mọi bản trên `ebd5ef38`. Laptop (x86, 12 luồng) chạy phần d = 0 còn lại từ gói ca và gói bổ sung đã có trong repo. Điều kiện dùng kết quả laptop: chạy trước 4 cặp (bản, ca) đã có đầu ra `exp-obs` (V041, V061, V013, V018 trên ca dev bản 2) và đầu ra phải trùng byte `method-output-1.json`; lệch thì bỏ tuyến laptop, chạy hết trên `exp-obs`. Mỗi cặp chạy hai lần trùng SHA (WHY-81). Hash gói bổ sung trên laptop đối chiếu `SHA256SUMS` trên `exp-obs` trước khi chạy.
- **Kết luận phụ thuộc:** phạm vi kết luận về quan hệ cho V041; giữ/bỏ H3, H4, H8-adapter; bản đề xuất trên tập dev bản 3; độ nhạy mốc.


## WHY-97. T-064 Đáp án ô CONSUMER-BOOK-SLOW-X3: tập chấp nhận nút {booking-service, broker}, báo kèm {booking-service} — ghi 14/11/2026 trước khi chấm (điều phối, phiên 5)

- **Chọn gì:** theo quyết định Minh ("A, báo kèm điểm B", DECISIONS 14/11), `results/T-064/dap-an-dev3.json` ghi tập chấp nhận nút của CONSUMER-BOOK-SLOW-X3 = {booking-service, broker}; `results/T-064/dap-an-dev3-B.json` giống hệt trừ tập này = {booking-service}, chỉ để báo độ nhạy. Gốc: cạnh booking-service → broker, loại `message` (bảng cạnh chấm đúng cạnh này ở cả hai bản đáp án).
- **Vì sao:** T-059 `label_rules` "Chấm cạnh" (2): ô gốc cạnh được chấm định vị qua tập chấp nhận chung {caller, callee}, áp y hệt cho mọi phương pháp; các ô cạnh khác của tập chọn đã theo quy ước này (EVENT-DB-LAT, REDIS-BOOK, NET-GW-BOOK). `broker` có trong inventory nên phương pháp xếp được nó.
- **Phương án đã xét:** B = {booking-service} đúng chữ khai trước ở `thu3/KE-HOACH.md` §2 nhưng lệch quy ước các ô cạnh khác; giữ làm phép độ nhạy.
- **Mặt trái:** sửa sau khai trước (dù trước khi chấm biến thể); người làm đã thấy đầu ra P7 của ca (booking hạng 1, broker ở nhóm cuối), nên với P7 hai đáp án cho cùng điểm. Tập rộng hơn chỉ làm điểm lạc quan hơn ở bản xếp broker trên booking.
- **Kết luận phụ thuộc:** điểm ca 659a9dfb1ab0 và phân xử H4 trên tập dev bản 3; nếu thứ tự §5 khác giữa A và B, hồ sơ chọn nêu rõ.

## WHY-98. T-064 Bản đề xuất cuối V082 (H5b + H8s1 + H8a) — ghi 14/11/2026 sau quyết định Minh (điều phối, phiên 5)

- **Chọn gì:** `V082-V066+H8a` = P7 + H5-liveness (chết im 60 s) + H8-san (1 ms) + H8-adapter; cấu hình `results/T-064/bien-the/V082-V066+H8a/cau-hinh.json`.
- **Vì sao:** theo `tieu-chi-chon.md` §5 trên tập chọn dev bản 3 (17 ca: 11 lỗi, 6 không lỗi), V082 đứng đầu: AC@1 9/11, AC@3 11/11, tổng hạng cắt 13, K 4/6 (`results/T-064/cham/chon-dev3-d0-v082-A.json#/ban/V082-V066+H8a/chon`), so với P7 7/11, 9/11, 23, 5/6. Không hồi quy 9 ca T-062 (K 4 → 1). Đáp án A và B cho cùng kết quả. Phép 2 quanh V082: H8a giữ (l1, nhờ ca RECREATE-PAY), H8s1 giữ (l2, K −1).
- **Phương án đã xét:** V061 (H5b + H8a; K 5/6), V071 (V082 + H1c; tổng hạng 14, cạnh đúng top 3 ở 3/4 ô cạnh — H1c đạt §4 l3 nhưng §5 đặt xếp hạng nút trước bảng cạnh), V068–V070 (thêm H3/H4: không đổi điểm), V072 (thêm H3+H4 vào V071: mất bảng cạnh do bước định vị cạnh (`CanhDinhVi`, `src/m1_ft/thanh_phan/h1_canh.py`) coi kênh pool là bằng chứng riêng bên gọi).
- **Bằng chứng và giới hạn:** V082 thiết kế sau khi xem điểm tập chọn (sổ dòng 180) nên số dev lạc quan; chênh giữa các bản đầu bảng là một ca; lợi của H8a chỉ từ một ca (ebd5ef38); H3/H4 không được phân xử (ô của chúng đã hạng 1 ở P7). Bản không có đầu ra cạnh.
- **Kết luận phụ thuộc:** cấu hình đề xuất, chỉ mục xuất cho T-065 (G-c), hồ sơ chọn §15, phản biện cuối T-064 và mọi đánh giá sau dùng V082.

## WHY-99. T-064 Kênh liveness `live-down` theo "lần dò mới nhất" (REVIEW-4 R9) — ghi 15/11/2026 trước khi chạy lại (điều phối, phiên 5)

- **Chọn gì:** kênh `live-down` tại bước s = 1 nếu lần dò có kết quả gần nhất trước s (trong 5 phút) là lỗi (mẫu thô `httpcheck_error` có giá trị 1); = 0 nếu là phản hồi (mẫu thô `httpcheck_status` có giá trị 1, mọi mã); không có lần dò nào thì bỏ điểm. Dựng từ mẫu thô (range vector) bằng bộ xuất mới `results/T-064/kiem/r9/xuat_live_down_moi.py`; logic `_chet_im` của H5b (`src/m1_ft/thanh_phan/h4_h5.py`) và các kênh khác không đổi.
- **Vì sao:** biểu thức cũ `max by(http_url)(httpcheck_error) or …` qua `query_range` giữ mẫu lỗi cũ trong lookback, nên ở RECREATE-PAY (lỗi t+3…t+43, phản hồi lại từ t+53) H5b đọc thành "chết im" 285 s, trái điều kiện "không phản hồi lại tới hết cửa sổ" của WHY-86 (REVIEW-4 R9; điều kiện thất bại đã nêu ở WHY-93).
- **Phương án đã xét:** `max_over_time(httpcheck_error[15s])` — loại: làm mất chết im ở PAUSE-PAYMENT 46aab4be, vì khi request treo đầu dò chỉ ghi lỗi mỗi ~30 s (`results/T-064/kiem/r9/so-live-down.json`). Giữ biểu thức cũ và khai lại nghĩa H5b là "đã thấy lỗi trong lookback" — loại: đổi nghĩa thành phần. Sửa bộ xuất đã ghim của T-063 — loại: đổi pin T-063.
- **Bằng chứng:** phép kiểm chỉ đọc `results/T-064/kiem/r9/so-live-down-2.json`: trên 140 gói có kênh, 134 không lệch điểm nào; chỉ 6 gói ebd5ef38 lệch; chết im mất ở 5 gói ebd5ef38 (d −60…+15) và giữ ở 46aab4be mọi mốc. Ngữ nghĩa mới được chọn sau khi đã thấy hai ca này (sửa sau, dev).
- **Kết luận phụ thuộc:** H5b trên RECREATE-PAY; điểm của 12 slot chạy lại (V061, V068–V072, V082 ở d = 0; V082 ở d −60, −30, −15, +15, +30); bản kế tiếp của chỉ mục xuất, cấu hình đề xuất, hồ sơ chọn §15–16.

## WHY-100. T-068 Đồ thị dịch vụ hiển thị đọc trace gốc (phương án A, `service-graph-4`/`-5`) — ghi 19/11/2026 sau khi dùng (đính chính thiếu WHY, phản biện Codex)

- **Chọn gì:** đồ thị dịch vụ trên trang sự cố (panel 40, 42, 43 của `t065-l8b-rca`) dựng từ trace gốc của ca, chỉ đọc, hash theo manifest gói. Cửa sổ và chia nền/sự cố theo `campaigns/g1/l8b-xuat.py` `dev3_template`. Cạnh: span cha–con khác chủ (dịch vụ → dịch vụ); span DB phía client → thực thể `db.name` nếu thuộc `classes`, nếu không thì → instance của `db.system`; span RabbitMQ PRODUCER/CONSUMER qua `broker`. Mỗi cạnh ghi số span N/A, số lỗi, p50/p95 thời lượng span con. Nút và hai đầu cạnh phải thuộc `classes`; phần không vẽ được ghi số. Hạng và màu nút lấy từ `ranking_rows` của đúng bản + ca. Đồ thị chỉ hiển thị, không tham gia xếp hạng.
- **Vì sao:** bản 2–3 dựng cạnh hạ tầng từ trường `dich_quan_sat` của file ca. Trường này không giữ `db.name`, và hai nhánh xuất ghi khác quy ước (`l4-raw.mjs` thêm hậu tố ` (<db.system>)`, `l8b-xuat.py` không thêm), nên đồ thị dừng ở instance và không đều giữa các ca (LOG T-068 "Phiên 1 (tiếp)", N1–N2). Trace gốc có `db.name` (7ffb2305: 190.917/201.743 span DB) và đủ thuộc tính RabbitMQ. Minh muốn "đồ thị vẽ chi tiết nhất có thể".
- **Phương án đã xét:** B — sửa `l8b-xuat.py` cho giữ `db.name`: loại vì đổi file ca, phá hồi quy byte T-066; để bộ xuất chung của W5. C — giữ bản 3, chỉ sửa câu kết luận (Codex R4): loại vì không đáp ứng yêu cầu chi tiết của Minh.
- **Bằng chứng:** rà soát bước 0 (LOG phiên 2: 29/29 gói khớp hash; 29/29 ca span DB đều CLIENT; `classes` có đủ DB logic postgresql); kiểm chéo số quan hệ cha–con từ trace = `canh_thao_tac` của file ca, 29/29; bộ kiểm độc lập: v4 85/85, v5 84/84 trên laptop + 1/1 trên exp-obs (`results/T-068/kiem/`); đối chứng âm bản 2: 16/16 (`results/T-068/a/doi-chung-am-2.json`).
- **Giới hạn và điều kiện thất bại:** cạnh là quan sát trace trong cửa sổ, đơn vị là span, không phải request. Không có cạnh DB logic → instance (không có trong dữ liệu). Ca mới cần gói trace (`/srv/rca-lab/m1/cases/<ca>`). Nếu bộ xuất đổi quy tắc cửa sổ, kiểm chéo `canh_thao_tac` sẽ dừng bộ dựng.
- **Kết luận phụ thuộc:** chỉ phần hiển thị DT18/P10 (G6). Không là căn cứ cho RQ3d hay lợi ích của việc dùng quan hệ trong phương pháp.

## WHY-101. T-068 Nút chú thích của ca "không có đầu ra" giữ link tới bảng trạng thái, không đặt `var-dv`/`var-op` — ghi 19/11/2026

- **Chọn gì:** ca mà bản không xếp hạng (ví dụ p7/ebd5ef38) vẽ hai nút chú thích nối bằng một cạnh chú thích (node graph của Grafana không nhận khung cạnh rỗng). Cả hai nút có link mở panel 3 "Bản, hash, trạng thái" của đúng bản, ca, cửa sổ. Từ `service-graph-5`, link không đặt `var-dv`, `var-op`.
- **Vì sao:** người xem cần biết vì sao bản không có đầu ra; panel 3 có trạng thái chạy và hash. `var-dv` rỗng làm truy vấn biến `op` gọi `thao-tac-vue/<ca>/.json` và báo 400. Bỏ hai biến thì Grafana chọn giá trị đầu.
- **Phương án đã xét:** nút chú thích không link (đề xuất đã duyệt trước đó, R1) — Minh chọn giữ link ngày 18/11. Đặt `var-dv=__khong_co__` — loại: `__khong_co__` là giá trị rỗng của `op`, không phải của `dv`; vẫn gọi file không tồn tại.
- **Bằng chứng:** bấm thật 19/11 sau khi sinh lại: link mở panel 3, mọi truy vấn 200, không còn 400 (LOG T-068 phiên 3); bộ kiểm độc lập buộc nút chú thích có link panel 3 và không có `var-dv`/`var-op`; đối chứng âm 11, 12.
- **Kết luận phụ thuộc:** chỉ cách hiển thị.

## WHY-102. T-069 Hai tầng tiêu chí của W3: ngưỡng tụt theo ô và điều kiện dừng theo tổng D1–D5 — ghi 20/11/2026 sau khi dùng (đính chính thiếu WHY, phản biện Codex R1)

- **Chọn gì:** (1) một ô lỗi **tụt** khi `hang_cat` của V082 mới > hạng cũ + 1 (SPEC T-069 dòng 58, làm rõ ở phiên 2); (2) điều kiện dừng kết luận theo tổng trên các ô ghép được: D1 AC@3 giảm, D2 AC@1 giảm ≥ 2, D3 V082 kém P7 mới, D4 V082 lỗi chạy không do hạ tầng, D5 K tăng ≥ 2. Kế hoạch §8.2 W3: "V082 tụt thì dừng, trình Minh". **Quan hệ:** ô tụt (1) là điều phải trình Minh dù D1–D5 không kích hoạt; D1–D5 chỉ quyết việc dừng kết luận tổng. Không bù ô tụt bằng ô tốt lên.
- **Vì sao:** mỗi ô chỉ một lần thu (cộng lặp), không ước lượng được phương sai; ngưỡng +1 bậc cho dời mốc 15 s (T-064 §16 đổi AC@1 một ca). Tổng D1–D5 bắt suy giảm diện rộng; ngưỡng theo ô bắt hỏng cục bộ mà tổng che (như CPU-BOOK-1 1 → 3 trong khi AC@1 tổng 9 = 9).
- **Phương án đã xét:** chỉ dùng tổng — loại: ô tốt lên bù ô tụt (đã xảy ra ở lượt chính). Chỉ dùng theo ô với ngưỡng 0 bậc — loại: dời mốc 15 s đã đổi một ca.
- **Bằng chứng:** `results/T-069/bang-theo-o.json#/dieu_kien_dung`, `#/hang`; `results/T-069/dinh-chinh-1.md` §1. Người làm đã áp tầng (2) mà bỏ tầng (1) khi đề xuất chuyển W4/W5 (sai, đính chính).
- **Kết luận phụ thuộc:** kết luận W3 và quyết định cho V082 vào demo (W4/W5).

## WHY-103. T-072 "p95 theo route ở gateway" = theo mã route Spring Cloud Gateway — ghi 20/11/2026 trước khi dùng (Minh duyệt D4, LOG T-070 lượt 6)

- **Chọn gì:** p95 và tỷ lệ 5xx tính trên histogram `http_server_request_duration_seconds` của `service_name="api-gateway"`, gom theo nhãn `http_route` = id route của gateway (`booking`, `event`, `payment`, `ticket`, …), không phải từng đường dẫn API. Một route gộp nhiều API và method.
- **Vì sao:** đây là mức chi tiết duy nhất của histogram ở gateway; giá trị `http_route` quan sát ở 5 thời điểm 18–20/11 chỉ gồm 5 id route có tải, `user`, `/actuator/health/{*path}` và chuỗi không nhãn (401) (`results/T-072/khao-sat/khao-sat-1.out`); id route khớp `application.yaml` gateway FlashTicket `36a3725d`.
- **Phương án đã xét:** theo đường dẫn API (không có trong metric gateway; phải lấy từ span hoặc phía service); tách theo method trong route (ít request mỗi ô, p95 dao động); một p95 chung toàn gateway (route đông che route ít).
- **Giới hạn:** API chậm trong một route đông có thể không đẩy p95 của cả route vượt ngưỡng; chưa đo độ lớn che lấp.
- **Kết luận phụ thuộc:** mọi số báo động giả và phát hiện của W4; t̂ của chế độ (b) (W5). Nguồn: `results/T-072/de-xuat-why.md` WHY-a, `bieu-thuc.json` `T072-bieu-thuc-1`.

## WHY-104. T-072 Tập route có luật: `booking`, `event`, `payment`, `ticket` — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** luật p95 và luật lỗi chỉ cho bốn route này.
- **Vì sao:** bộ tải `purchase-journey.js` (lab `407b4f5`) chỉ gọi bốn route này; ngưỡng chọn từ E2 nên route không có tải thì không có căn cứ; `user` 0 request/5 phút ở cả 5 thời điểm khảo sát.
- **Không phủ:** `user`, `event-images`, `payment-vnpay-callbacks`, request không khớp route (liveness của `user-service` vẫn có).
- **Kết luận phụ thuộc:** phạm vi phát hiện của W4. Nguồn: `de-xuat-why.md` WHY-b.

## WHY-105. T-072 Cửa sổ 5 phút và chặn khi < 30 request — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** `rate`/`increase` trên `[5m]`; luật p95 và lỗi chỉ có giá trị khi route có ≥ 30 request trong 5 phút.
- **Vì sao:** `payment`, `ticket` ≈ 70 request/5 phút ở ×1 (`khao-sat/kiem-xuat-1.jsonl`); cửa sổ 1 phút chỉ ≈ 14 mẫu, p95 gần max, dễ báo giả; giữa hai lượt tổng = 0 thì không tính p95 (NoData → OK).
- **Phương án đã xét:** 1m (quá ồn ở route ít request); 10m (trễ phát hiện dài).
- **Đánh đổi:** tín hiệu còn chứa lỗi tới 5 phút sau khi lỗi dừng (khoảng cháy dài; gom 300 s); lỗi làm lưu lượng route tụt dưới 30/5 phút làm luật route đó im (quan sát: `ticket` về 0 ở PAUSE-PAYMENT).
- **Kết luận phụ thuộc:** độ nhạy và độ trễ phát hiện W4. Nguồn: `de-xuat-why.md` WHY-c.

## WHY-106. T-072 Lỗi = 5xx, cần ≥ 3 lỗi 5xx trong 5 phút — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** tỷ lệ lỗi = request 5xx / tổng request của route trong 5 phút; luật chỉ kích hoạt khi ≥ 3 lỗi 5xx; không tính 401, 409, 429.
- **Vì sao:** 5xx là lỗi phía máy chủ (gồm 503 circuit breaker, 504 timeout gateway), quan sát ở HTTP5-EVENT, PAUSE-PAYMENT; 409/401 là nghiệp vụ/xác thực; 429 do giới hạn tốc độ theo địa chỉ nguồn, phụ thuộc mức tải (T-071 theo dõi riêng). Ba lỗi tránh mở sự cố vì một request hỏng (một lỗi trên 70 request đã là 1,4%).
- **Phương án đã xét:** tính cả 429 (loại); không đặt số lỗi tối thiểu (ngưỡng từ E2 có thể là sàn, một lỗi đủ mở sự cố).
- **Giới hạn:** tổ hợp (route, mã 5xx) xuất hiện lần đầu: `increase` không thấy phần trước mẫu đầu; lỗi kéo dài vẫn thấy từ mẫu thứ hai. Luật `loi-booking`, `loi-ticket` chưa có dương thật (`results/T-072/ke-hoach-e3-duong.md`).
- **Kết luận phụ thuộc:** báo động giả và phát hiện lỗi 5xx của W4. Nguồn: `de-xuat-why.md` WHY-d.

## WHY-107. T-072 Liveness ba trạng thái theo lần dò mới nhất, tuổi tối đa 60 s — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** mỗi đích dò, lần dò mới nhất trong 5 phút là mẫu mới nhất của `httpcheck_error` (lỗi) hoặc `httpcheck_status{http_status_code!=""}` (có phản hồi); dò tốt / dò lỗi nếu tuổi ≤ 60 s; thiếu lần dò nếu không có lần nào tuổi ≤ 60 s. `t072-live` cháy khi dò lỗi liên tục 20 s; thiếu lần dò thuộc luật mất quan sát `t072-mat-do`, không thuộc lớp hệ thống.
- **Vì sao:** cùng ngữ nghĩa "lần dò mới nhất" với WHY-99; quan sát PAUSE-PAYMENT 19/11: khi lỗi, receiver vẫn ghi `httpcheck_status` giá trị 0 không có `http_status_code`, lỗi ghi mỗi 30 s; 60 s ≥ hai nhịp.
- **Khác WHY-99:** thêm tuổi tối đa 60 s (trạng thái "thiếu"); kênh `live-down` của M1 không đổi.
- **Phương án đã xét:** `max_over_time(httpcheck_error[15s])` (WHY-99 đã loại); `for` 0 (lần dò lẻ mở sự cố); `for` 60 s (có thể lỡ RECREATE-PAY ≈ 50 s).
- **Chưa kiểm:** độ trễ nạp mẫu lúc Grafana đánh giá; phân xử ở E3.
- **Kết luận phụ thuộc:** phát hiện liveness W4; phân lớp hệ thống/quan sát. Nguồn: `de-xuat-why.md` WHY-e.

## WHY-108. T-072 Nhịp đánh giá 10 s; `for` 60 s (p95, lỗi), 20 s (liveness) — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** một nhóm luật, `interval` 10 s; `for` như trên; `keep_firing_for` 0.
- **Vì sao:** Grafana nhận khoảng đánh giá là bội của 10 s [theo tài liệu Grafana, chưa kiểm trên bản đang chạy]; 10 s bằng nhịp mẫu histogram và nhịp dò; mỗi truy vấn luật ≤ 0,03 s trên Prometheus (`kiem-xuat-1.jsonl` trường `dt`). `for` 60 s: bước nhảy p95 dưới 1 phút không mở sự cố.
- **Kết luận phụ thuộc:** độ trễ phát hiện (W6–W7), số báo động giả. Nguồn: `de-xuat-why.md` WHY-f.

## WHY-109. T-072 Gom sự cố: ghép khi cách ≤ 300 s; quy về phút chứa t̂ — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** khoảng cháy lớp hệ thống ghép thành một sự cố khi t̂ mới ≤ max t_hết + 300 s; lớp quan sát gom riêng; quy về phút chứa t̂; vắt qua biên đếm một lần theo phút bắt đầu; bắt đầu trong biên không vào tử số; đang cháy lúc bắt đầu khoảng không đếm (`results/T-072/quy-tac-gom.json`, `T072-gom-2`).
- **Vì sao:** 300 s bằng cửa sổ rate (WHY-105) và nửa cửa sổ dữ liệu RCA.
- **Tiêu chí dùng:** R5 (Minh duyệt 20/11): ≤ 1 sự cố / 6 giờ khỏe ×1 trên E4; E4 9 lượt (D1).
- **Kết luận phụ thuộc:** tử số báo động giả W4. Nguồn: `de-xuat-why.md` WHY-g.

## WHY-110. T-072 Quy tắc chọn ngưỡng từ E2: biên k và sàn — ghi 20/11/2026 trước khi dùng (Minh duyệt D4)

- **Chọn gì:** chỉ dữ liệu E2, chỉ bước thuộc phút khỏe ×1 (phân loại T-071 bản khóa `b63f2e09`); S(t) = min trong [t − for, t]; M = max S theo route; θ_p95 = làm tròn lên 0,001 của max(1,5·M, M + 0,05 s); θ_lỗi = làm tròn lên max(2·M, 0,05); cần ≥ 120 bước/route, thiếu thì dừng trình (`results/T-072/quy-tac-chon-nguong.json`, `T072-chon-nguong-2`).
- **Vì sao:** θ ≥ max S thì luật không cháy trên E2 (khớp ngữ nghĩa `for`); biên k và sàn cho trôi giữa E2 và E4 và cho bucket thô (p95 ~0,03–0,15 s nằm trong bucket 0,025–0,25 s); sàn lỗi 5% ≈ 3,5 lỗi trên 70 request, khớp WHY-106.
- **Giới hạn:** k và sàn là **biên vận hành khai trước**, không phải ước lượng từ dữ liệu; số trôi của một truy vấn DB trong T-069 (`troi-trong-luot.txt`) không xác nhận hệ số cho từng route (Codex CX-06). Không chỉnh θ bằng tay; đổi sau E4 → ghi "sửa sau", giữ kết quả đầu.
- **Phương án đã xét** (T-072 `de-xuat-why.md` bản 2, WHY-h): phân vị cao (ví dụ 99%) của tín hiệu E2 — loại: chấp nhận trước một số cảnh báo trong mẫu và phụ thuộc số bước; chọn θ theo R5 trên E2 — loại: R5 là tiêu chí kết luận E4, dùng nó để chọn θ làm E4 mất tính độc lập về mục tiêu; ngưỡng cố định theo kinh nghiệm — loại: không có căn cứ trên hệ này.
- **Bằng chứng (chỉ kiểm code, không chọn):** ngưỡng thử trên T-067 + ca khỏe `1e5debb6` (`results/T-072/kiem-code/nguong-thu.json`): θ thử booking 0,098, event 0,097, payment 0,235, ticket 0,095 s; 0 sự cố trên 88 phút khỏe tạm; bước nhảy giả 0,5 s trong 120 s bị bắt.
- **Điều kiện thất bại:** E4 trôi vượt biên → báo động giả tăng (không sửa θ bằng E4); pha lưới đánh giá Grafana khác lưới xuất có thể cho S(t) nhỉnh hơn M [chưa kiểm]; p95 duy trì gần mốc bucket nhạy với vài request chậm.
- **Kết luận phụ thuộc:** ngưỡng luật W4, kết quả R5 trên E4, t̂ của chế độ (b). *(Sửa 21/11 ~02:50Z: thay hai phương án điều phối tự nêu ở bản ghi đầu bằng nội dung WHY-h của T-072.)*

## WHY-111. T-073 Ngưỡng phủ cửa sổ khi nghiệm thu W5: trace lỗ ≤ 30 s, metric lỗ ≤ 4 × bước, log không bắt buộc — đặt 20/11/2026, khóa 22/11/2026 trước E5; mục WHY ghi bổ sung **sau** E5 (23/11)

**Thời điểm.**
- Quy tắc được thêm vào `check_core_input.py` ngày **20/11/2026 22:03Z**, LOG T-073 lượt 7, khi sửa theo Codex CX-06 điểm 5–6.
- Quy tắc được đưa vào `khai-truoc-e5.json` nháp 2 cùng lúc. Ngày **22/11/2026**, file khóa ở bản `T073-khai-e5-khoa-1` (sha256 ghi LOG T-073 lượt 11).
- E5 chạy **23/11/2026 02:07–02:38Z**.
- Mục WHY này được viết **sau** khi đã thấy kết quả E5, trong đó 6 nguồn Payment trượt ngưỡng. Hai ngưỡng **không đổi** sau E5. Mục này chỉ bổ sung lý do còn thiếu theo luật cứng 3. Đây không phải lần chọn lại.

**Chọn gì.**
- Với mỗi nguồn, lấy mốc thời gian của các mẫu thực nằm trong [t̂−300, t̂+300).
- Lỗ lớn nhất = max(mẫu đầu − (t̂−300), khoảng giữa hai mẫu liền nhau, (t̂+300) − mẫu cuối).
- **Trace** (toàn bộ span, theo mốc kết thúc): bắt buộc; thiếu phủ khi lỗ > 30 s.
- **Mỗi nguồn metric có trong gói:** bắt buộc; thiếu phủ khi lỗ > 4 × bước của nguồn (bước 15 s → 60 s; bước 10 s → 40 s), hoặc khi không có mẫu nào.
- **Log:** không bắt buộc, chỉ báo.
- `du_cua_so` chỉ đúng khi mọi nguồn bắt buộc đều đủ. Khi đúng, được viết "lõi nhận đủ cửa sổ"; khi không, viết "đã hiển thị nhưng thiếu phủ".

**Vai trò.** Đây là **quy ước nghiệm thu** cho câu chữ của W5: "dữ liệu thực sự vào lõi quanh t̂" (kế hoạch §8.2, CX-06). Ngưỡng này **không** đo được thiếu bao nhiêu thì kết quả xếp hạng thay đổi. Nó không đánh giá phương pháp và không thuộc tiêu chí `ket_qua_chuc_nang`.

**Vì sao chọn như vậy.** LOG lượt 7 không ghi căn cứ cho riêng hai con số 30 s và hệ số 4. Phần dưới là căn cứ dựng lại lúc viết mục này. Ghi rõ như vậy để không trình bày như lý do đã có từ lúc đặt.
- **Tính theo mẫu thực thay cho biên min/max.** Quy tắc biên cũ (`nguon_khong_phu_tron`, như `m1_ft.doi_moc._phu`) chỉ xét mẫu đầu và mẫu cuối, nên không bắt được lỗ ở giữa. Phép thử tổng hợp ở lượt 7 cho thấy điều này: bỏ 8 mẫu giữa của chuỗi 15 s thì lỗ là 135 s, quy tắc biên không báo (LOG T-073 lượt 7, mục 22:03Z kiểm).
- **Metric 4 × bước.** Ngưỡng này cho phép tối đa 3 lần lấy mẫu liên tiếp bị hụt trước khi gọi là thiếu, nhằm không báo thiếu vì một vài lần scrape trễ. Cùng quy ước "4 bước" như ngưỡng 60 s = 4 bước dò 15 s của H5 trong V082. Quan sát nền: ở các nguồn không bị can thiệp của E5 và lượt dưới tải E3 (`t073-dev-008`), lỗ lớn nhất là 15 s với nguồn bước 15 s và 20,001–20,088 s với nguồn bước 10 s (E3: `results/T-073/kiem/dev/t073-dev-008/su-co/b08d6da4d1.json` `#/…/phu/nguon`, 32 nguồn 15 s, 29 nguồn 10 s). Cả hai đều dưới ngưỡng với khoảng cách lớn.
- **Trace 30 s.** Dưới tải ×1, span đến liên tục. Lỗ lớn nhất quan sát được là 0,35–0,395 s ở dev, E3 và E5. Lỗ 30 s là quy ước, lớn hơn khoảng 75 lần lỗ lớn nhất quan sát được ở dev, E3 và E5. Vượt ngưỡng cho biết cửa sổ thiếu span, không tự cho biết do mất thu hay do không phát sinh span. Ngưỡng tính trên trace gộp toàn hệ thống, không theo từng dịch vụ.
- **Log không bắt buộc.** Dịch vụ có thể không ghi log trong khoảng khỏe, nên thiếu log không có nghĩa là mất dữ liệu.

**Phương án đã xét.**
- (1) Quy tắc biên min/max: bỏ, vì không bắt được lỗ giữa (vẫn ghi để đối chiếu).
- (2) Tỷ lệ số mẫu so với số kỳ vọng: không chọn, vì một lỗ liền lớn có thể bị che bởi tỷ lệ mẫu còn cao.
- (3) Ngưỡng chặt hơn, ví dụ 2 × bước: chưa xét bằng dữ liệu; sẽ dễ báo thiếu vì scrape trễ.
- (4) Ngưỡng theo từng dịch vụ cho trace: không làm ở W5.

**Điều kiện thất bại.**
- (a) Lỗ dưới ngưỡng vẫn có thể rơi đúng đoạn khởi phát lỗi và đổi kết quả. Ngưỡng không đo ảnh hưởng lên xếp hạng.
- (b) Nguồn dẫn xuất (`rate[1m]`, phân vị) làm mịn mất mẫu thô khoảng 1 phút. Vì vậy ngưỡng 60 s của nhóm HTTP có thể không thấy một lỗ thô ngắn hơn khoảng 2 phút.
- (c) Trace gộp có thể đủ trong khi một dịch vụ mất hết span. Đó là trường hợp Payment ở E5, chỉ có span ở N.
- (d) `check_core_input.py` bản E5 chỉ áp quy tắc lên 61 nguồn metric cơ sở của đầu vào P7. Hai kênh `live-down` và `live-ms` mà V082 thêm sau đó không nằm trong phép kiểm tự động (CX-21 điểm 1). Với ca E5, 16 nguồn `live-*` đã được kiểm tay sau Q1 và đủ phủ (`results/T-073/dap-cx21/dinh-chinh-e5-2.md` §1). Các lượt sau vẫn cần thêm phép kiểm cho hai kênh này.
- (e) Đổi bước scrape thì ngưỡng metric đổi theo.

**Bằng chứng.**
- `campaigns/online/check_core_input.py` (bản E5 `81a9273`), docstring và hàm `lo_lon_nhat`.
- LOG T-073 lượt 7 (mục 22:03Z) và lượt 10 (E3, `t073-dev-008`).
- `results/T-073/khai-truoc-e5.json` `#/tieu_chi/ket_qua_phu_cua_so`.
- `results/T-073/e5/su-co/bbc0a6d44f.json` `#/du_lieu_loi/phu`.

**Kết luận phụ thuộc.**
- Chỉ phụ thuộc: câu "lõi nhận đủ cửa sổ" hoặc "đã hiển thị nhưng thiếu phủ" trong kết quả W5 (E5, và các lượt sau nếu dùng lại quy tắc).
- Không phụ thuộc: kết quả chức năng E5 (đạt), độ chính xác hay đối chứng của W6–W7.
- Nếu W6–W7 cần biết thiếu phủ có làm đổi hạng hay không, đó là phép đo riêng, không suy ra từ ngưỡng này.

*Minh duyệt chữ ngày 23/11/2026 ("Approve WHY-111"). Nguồn nháp: `results/T-073/dap-cx21/nhap-why-nguong-phu.md` (sha256 `91fb63f2…`), ghi bởi điều phối T-070.*
*Sửa 23/11/2026 (Minh duyệt "Approve update"): điều kiện (d) thay theo nháp T-073 đã cập nhật sau Q1 (16 nguồn `live-*` kiểm tay, đủ phủ; `results/T-073/dap-cx21/dinh-chinh-e5-2.md`).*
*Sửa 24/11/2026 (Minh "Duyệt cả 6", mục 4): câu về ngưỡng trace 30 s thay theo `results/T-073/dap-cx21/dinh-chinh-e5-3.md` §4.*
