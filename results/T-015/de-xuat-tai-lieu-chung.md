# Nháp đề xuất tài liệu chung — T-015

Không ghi trực tiếp file chung. Trạng thái lựa chọn P3 là **CANDIDATE**; quyền Minh cho thực hiện T-015 không tự chốt P3/G1.

## 1. docs/DECISIONS.md — thêm các xác nhận trong phiên

**Đoạn cũ:** chưa có dòng về ủy quyền T-015/vai trò/biến thể.

**Đoạn mới (mã do Minh cấp khi ghi):**

- 04/10/2026 — Minh ủy quyền tự viết và tự duyệt SPEC T-015 theo prompt Đợt 1, rồi triển khai trong phạm vi được ghi. Đây chỉ là ngoại lệ bước duyệt SPEC cho T-015.
- 04/10/2026 — Minh: "Đồng ý: Codex làm, Claude phản biện" cho T-015.
- 04/10/2026 — Minh: "Đồng ý phương án 1, kèm điều kiện: (a) Đặt tên rõ ràng: \"MicroRank-RCAEval sửa đầu vào\", không gọi là MicroRank gốc. Hồ sơ có bảng: bước nào giữ theo bài, bước nào khác bài, vì sao. (b) Ghi lý do chọn vào SPEC/LOG TRƯỚC khi chạy so với T-007. Lý do chọn dựa trên cơ chế (sửa hai lỗi, đúng ngữ nghĩa code gốc), không dựa trên điểm. Báo cáo nói rõ bản này không có số công bố để tái lập; độ tin cậy dựa trên ví dụ tính tay và phép so từng ca với T-007. (c) Trong giới hạn task, đọc code gốc để đánh giá phương án 3: suy span kind, root và tên pod từ dữ liệu (không dùng nhãn), rồi chạy code gốc kèm bộ phát hiện gốc. Chỉ đánh giá khả thi và chi phí, chưa cần cài. Ghi kết quả vào hồ sơ để G1 quyết. Giữ kết quả bản RCAEval của T-007 làm mốc đối chiếu."

**Vì sao:** lưu quyền và điều kiện để phiên sau không suy từ chat. **Phụ thuộc:** phạm vi kiểm T-015; không chốt baseline P3 hay cửa sổ.

## 2. docs/WHY.md — nháp lựa chọn biến thể MicroRank, đề xuất G1

**Đoạn cũ:** chưa có lý do riêng cho cách sửa MicroRank ở P3.

**Đoạn mới:**

### Vì sao đề xuất MicroRank-RCAEval sửa đầu vào cho giao thức span hiện có — Đề xuất (G1)

- **Chọn đề xuất:** MicroRank-RCAEval sửa đầu vào, giữ detector span μ+3σ RCAEval; chia trace bất thường khi có ít nhất một span vượt ngưỡng, bình thường là phần bù; cùng hai nhóm trace dùng để dựng graph và số đếm; tích lũy cạnh operation-operation. Giữ nguyên PageRank và spectrum MIT gốc. Lý do này đã ghi SPEC/LOG trước chạy so T-007.
- **Vì sao:** sửa hai lỗi đã kiểm trên code và khôi phục tính nhất quán của spectrum: graph không được chứa trace ngoài tập được đếm. Không cần dựng span.kind/pod không có trong dữ liệu. Đây là lựa chọn theo cơ chế và điều kiện đầu vào, không theo bản có điểm cao hơn.
- **Đã xét:** (1) RCAEval nguyên trạng — giữ làm mốc T-007, có lỗi graph/count/NaN không được xem là xác nhận MicroRank gốc; (2) full MicroRank gốc qua adapter — cần kind, root frontend-server, self-time bình thường và pod instance; (3) suy các trường này bằng dữ liệu không nhãn — chỉ đánh giá khả thi/chi phí trong hồ sơ, chưa cài, không tự suy pod thật từ service. (4) Giữ normal graph và số đếm từ baseline trước mốc. Muốn nhất quán cả hai phía còn phải đếm toàn current theo anomaly graph, hoặc lọc anomaly graph chỉ còn trace có span bị cờ rồi đếm cùng tập. Phương án đầu bỏ vai trò3σ trong partition của spectrum; phương án sau là biến thể pre/post, cần quy tắc trace ngang mốc. Chỉ sửa normal_list_len không hết nf âm (RCAEval microrank.py:683–684,697). Các phương án pre/post lệch ngữ nghĩa code gốc chia hai nhóm trong cùng cửa sổ current; vì vậy T-015 chọn phần bù trong current theo cơ chế và quyền Minh, không theo Hit@k. Không chạy các phương án đối lập sau khi nhìn điểm.
- **Bằng chứng:** source đúng revision trong manifest; toy graph so AST gốc; công thức detector gốc so AST; ví dụ độc lập mọi điểm; so từng ca T-007. Biến thể sửa đầu vào **không có số công bố riêng để tái lập**; mốc công bố gốc và số RCAEval không được gán cho biến thể này.
- **Giới hạn:** giữ span3σ có ddof=1/round2/inclusive duration, khác self-time ddof=0/round4 và trace threshold gốc. Hoán vị dòng/seed đã kiểm trong T-015; không bảo đảm detector ít báo giả. Trần ứng viên phụ thuộc trace và cắt top11. Full-score/service mapping là output kiểm, cách dùng cho MRR/NDCG ở P3 chờ G1. Luật ít nhất một span tạo nhiều cơ hội flag ở trace dài; ba ca TT có trung vị normal/anomaly5/179 span. Đây là tương quan đã kiểm, chưa chứng minh nguyên nhân duy nhất hoặc Dstar2 trực tiếp đo độ dài. Control khác độ dài baseline nên không so tỷ lệ để đo hiệu quả. Chẩn đoán cùng snapshotauth25/26/50/100/101 cho thấy nhạy số vòng và chưa hội tụ; giữ25 để khớp code. Nguồn: runs/review-response/trace-length-stats.csv và iteration-probe.json. Không khái quát3/30dev thành cả30.
- **Kết luận phụ thuộc:** tên baseline, input assumptions, khả năng tái lập và giải thích chênh với T-007. Không cho kết luận riêng về lợi ích PageRank hoặc đồ thị, vì hai bên khác grouping/graph/count. Nghĩa nhóm bình thường đã đổi: trace current không có span bị cờ, khác tập baseline trước sự cố. Baseline trước mốc chỉ học μ/σ trong biến thể này. Tương quan độ dài và độ nhạy25vòng hạn chế cách đọc thứ hạng, không làm nó thành bằng chứng causal root.

## 3. docs/WHY.md — nháp sửa sắp xếp TraceRCA RCAEval, đề xuất G1

**Đoạn cũ:** chưa có quy tắc adapter cho NaN/tie.

**Đoạn mới:**

### Vì sao lọc giá trị không hữu hạn trước khi sắp TraceRCA RCAEval — Đề xuất (G1)

- Chọn đề xuất: giữ support/confidence/điểm hữu hạn; tách zero-support/NaN thành trạng thái không có bằng chứng, trước sort; sắp giảm dần theo điểm hữu hạn và phá hòa bằng khóa operation canonical. Không tự gán điểm cho service vắng trace.
- Vì sao: NaN không có quan hệ thứ tự toàn phần; sort rồi lọc không bảo đảm giảm dần và làm thứ hạng phụ thuộc thứ tự span. Thay tie bằng canonical là quy ước bổ sung, phải công khai riêng với sửa NaN.
- Đã xét: giữ raw chỉ để tái dựng số T-007; gán 0 cho zero-support sẽ giữ ứng viên nhiều hơn nhưng là quyết định khác về tập ứng viên; không chọn vì điểm tốt hơn. Trường hợp tổng abnormal=0 trả no-evidence, không coi danh sách tùy ý là nguyên nhân.
- Bằng chứng: runs/tracerca-audit; tái dựng 90 ca raw, kiểm independent span/point/TT/seed/hoán vị. So raw và canonical là tác động kết hợp NaN+tie, không quy tất cả cho một lỗi.
- Phụ thuộc: thứ hạng TraceRCA P3 và service mapping; không thay bộ phát hiện hoặc biến thể thành TraceRCA gốc.

## 4. K1, MRP, WHY-02 — làm rõ quan hệ tham gia detector gốc

**File đích:** `docs/knowledge/K1-phuong-phap-rca.md` §3/§4/§C.3/§D.3; `docs/MRP.md` §2.3; `docs/WHY.md` WHY-02.

**Đoạn cũ:** các câu hiểu rằng đồ thị/quan hệ không tham gia bất kỳ phần phát hiện nào của MicroRank.

**Đoạn mới:** "PageRank trong MicroRank dùng sau khi chia trace và không quyết định nhãn bất thường. Nhưng code MicroRank gốc dùng quan hệ span cha–con để trừ duration con khỏi duration cha khi học SLO tự xử lý. Vì vậy quan hệ có tham gia tiền xử lý thống kê của detector gốc; luật span μ+3σ của RCAEval không có bước đó. Không suy từ việc PageRank chạy sau rằng mọi đặc trưng phát hiện đều không dùng cấu trúc."

**Vì sao:** code `preprocess_data.py:191–192,218–219`, hồ sơ T-015 và PDF; phân biệt graph ranker với thông tin quan hệ dùng trong baseline. **Phụ thuộc:** phân loại vai trò graph, biên đối chứng không đồ thị ở P7; không tự thay kiến trúc P6.

## 5. T-001 — ngưỡng TraceRCA gốc

**File đích:** `results/T-001/danh-sach-phuong-phap.md:88`.

**Đoạn cũ:** "phát hiện 3σ trên các đặc trưng đã chọn".

**Đoạn mới:** "phát hiện độ lệch hai phía theo reference trên các đặc trưng đã chọn; hàm tên `anomaly_detection_3sigma` nhưng multiplier mặc định là 1 (`run_anomaly_detection_invo.py:14,59,72`; `Makefile:23 SIGMA=1`). Không đồng nhất với luật span μ+3σ một phía của RCAEval."

**Vì sao:** đã tái kiểm AST gốc với toy 2σ: bị flag ở default1, không bị flag ở3; `runs/tracerca-audit/toy-extra/toy-checks.json`. **Phụ thuộc:** hồ sơ detector và khác biệt TraceRCA gốc/RCAEval; không đổi kết quả RCAEval T-007.

## 6. STATE — việc dọn EC2 đã làm

**File đích:** dòng T-007 và câu EC2 đã Stop trong `docs/STATE.md`, chỉ khi Minh cho sửa file chung.

**Đoạn cũ:** "Việc dọn còn lại: xóa ~/.sudo_as_admin_successful khi bật lại EC2 của T-007".

**Đoạn mới:** "Đã dọn ~/.sudo_as_admin_successful trong T-015 ngày 04/10/2026; lệnh rm chạy đúng một lần, test xác nhận không còn. EC2 đã kết nối lại với địa chỉ mới theo prompt Đợt 1."

**Vì sao:** tránh phiên khác chạy rm lại từ trạng thái cũ. **Phụ thuộc:** trạng thái vận hành; không ảnh hưởng số khoa học. T-015 chưa sửa các dòng chung này.


## 7. DECISIONS — EC2 thứ hai theo Minh

**Đoạn cũ:** chưa có chỉ đạo trong phiênT015. **Đoạn mới:** 04/10/2026 — Minh: "chuyển sang 3.26.62.217 , file key2.pem, ssh xem được không"; "nếu thiếu ram thì chuyển lê ec2 nhé, 3.26.62.217 là ec2 thứ 2". T015 được dùng máy hai, mọi ghi mới trong~/rca/T-015/. **Vì sao:** lưu chỉ đạo vận hành, không suy quyền chạy nhiều worker. **Phụ thuộc:** môi trường và nguồn dữ liệu, không chốt protocolP3.

## 8. WHY — bản sao span và guard conflict

**Đoạn cũ:** chưa có policy bản sao. **Đoạn mới:** Giữ mỗi row exact-copy trong SLO/detector RCAEval và pr_trace; lookup cha theo(traceID,spanID) giữ một identity. Chỉ chấp nhận ID trùng nếu8measurement columns cùng nội dung; conflicting identity báo lỗi. Vì sao: graph gốc overwrite lookup nhưng append occurrence mỗi row; không dedup để tự thay prior. Đã xét reject mọi duplicate (bỏ hai ca hợp lệ về quan sát), dedup toànrow (thay detector/prior), last-wins conflict (tùy thứ tự); không chọn theo điểm. SLO full-original duyệt dict unique spans, khác SLO RCAEval đang giữ của biến thể. Bằng chứng: diagnosis48/99exactkeys,0conflict, toy AST graph, hai rerun độc lập. Phụ thuộc: giao thức input và2ca so OB; không suy exporter tạo duplicate vì nguyên nhân gì. Đây là đề xuất G1, không quyết định P3.


## 9. Cụ thể hóa nguyên văn đoạn cũ cho đề xuất §4

**File đích:** docs/MRP.md §2.3.

**Đoạn cũ:** "K1 §D.3 ghi một phản ví dụ quan trọng: MicroRCA và MicroRank chỉ dùng PageRank **sau khi** đã phát hiện bất thường cục bộ, nên đồ thị không tham gia việc phát hiện. Nếu chỉ làm theo nghĩa rộng, cô hỏi "đồ thị phát hiện bất thường ở đâu?" sẽ không trả lời được."

**Đoạn mới:** "K1 §D.3 phân biệt PageRank với detector: PageRank của MicroRCA/MicroRank chạy sau khi đã phân loại bất thường. Riêng code MicroRank gốc còn dùng quan hệ span cha–con khi học SLO self-time; vì vậy PageRank không quyết định nhãn, nhưng không thể suy mọi thông tin quan hệ đều vắng khỏi tiền xử lý detector. Luật span của bản RCAEval không có bước self-time này. Phần P6 vẫn cần chỉ rõ loại đồ thị nào tham gia trực tiếp vào điểm bất thường."

**File đích:** docs/WHY.md WHY-02, chỉ thay câu sau trong dòng Vì sao.

**Đoạn cũ:** "Trong MicroRCA và MicroRank, PageRank chỉ chạy sau khi đã phát hiện bất thường cục bộ, tức đồ thị không tham gia việc phát hiện (K1 §D.3)."

**Đoạn mới:** "Trong MicroRCA và MicroRank, PageRank chạy sau detector. Riêng code MicroRank gốc dùng quan hệ cha–con khi học SLO self-time; do đó câu kết luận không có quan hệ tham gia phát hiện chỉ đúng khi nói riêng đồ thị PageRank, không đúng cho mọi tiền xử lý có cấu trúc."

**File đích:** docs/knowledge/K1-phuong-phap-rca.md §C.3, dòng Detector.

**Đoạn cũ:** "- **Detector.** Từ normal window, paper ước lượng `μ_o, σ_o`, đặt operation SLO `μ_o+1.5σ_o`, rồi cộng SLO theo số operation trong trace để tạo expected trace latency. Trace thực vượt expected bị xem là abnormal. Cửa sổ online 30 giây; khi trigger, thu thêm khoảng 5 phút trace."

**Đoạn mới:** "- **Detector.** Bài dùng normal history của handling time để học μ_o,σ_o và dự báo latency theo số operation. Code gốc tính handling time bằng duration cha trừ duration con quan sát được; quan hệ cha–con tham gia bước học SLO. System alarm dùng μ+1.5σ và hơn8trace; partition RCA dùng μ+σ+50ms. Bài dùng cửa sổ30s; code detector60s và RCA−5/+55s. PageRank chạy sau partition và không tự quyết định nhãn bất thường."

**Vì sao/phụ thuộc cho ba sửa:** đã kiểm nguồn cha–con và hai luật gốc trong T015; sửa phạm vi lập luận về graph, không tự quyết thiết kế P6. Các câu K1 chỉ nói riêng PageRank có phạm vi đúng, nên không đề xuất đổi chúng thành lời khẳng định PageRank phát hiện bất thường.

**Không đính chính thành lỗi:** K1 ghi Ochiai mặc định và R@2≈66% là đúng cho thực nghiệm bài MicroRank. Code revision T015 gọi Dstar2, có R@2=54% trong dòng khác của bảng bài. Hồ sơ T015 đã tách hai nguồn; không sửa số66 thành54 một cách máy móc.


## 10. docs/DECISIONS.md — Minh duyệt sửa sau REVIEW T-015

**Đoạn cũ:** chưa có quyết định sửa sau phản biện T-015.

**Đoạn mới (mã do Minh cấp khi ghi):** 04/10/2026 — Minh: “duyệt sửa theo đề xuất”, áp dụng danh sách “Đề xuất sửa gom theo file” trong LOG phiên2 cho R1–R3/N1–N7. Sửa hồ sơ/bảng đầu vào, guard thời gian hữu hạn và kiểm/bàn giao; giữ luật3σ, code PageRank/spectrum gốc,25vòng/top11. Không có chỉ đạo mở rộng thêm27TT hoặc chốtP3; phạm vi thực nghiệm vẫn3/30dev.

**Vì sao:** lưu quyền đúng phạm vi; không suy quyền mới từ góp ý reviewer. **Phụ thuộc:** phiên3 sửa đã duyệt, không chốt baseline P3 hoặc chuyển task thành xong. T-015 chỉ viết nháp, không ghi DECISIONS thật.


## 11. docs/DECISIONS.md — Minh chốt T-015 sau sửa phản biện

**Đoạn cũ:** chưa có quyết định đóng T-015 sau sửa phản biện.

**Đoạn mới (mã do Minh cấp khi ghi):** 04/10/2026 — Minh: “chốt”. Minh duyệt kết quả T-015 sau sửa R1–R3/N1–N7 và đóng task. Phạm vi kiểm Train Ticket là3/30dev với phần27ca chưa kiểm đã nêu. Các đề xuất baseline, cửa sổ, tập ứng viên và adapter choG1/P3 vẫn chờ quyết định riêng. Không có chỉ đạo commit/push hoặc ghi các nháp vào tài liệu chung.

**Vì sao:** lưu quyết định kết thúc task, giữ đúng phạm vi lời Minh. **Phụ thuộc:** trạng thái Xong của T-015; không tự chốt giao thức G1/P3. T-015 chỉ viết nháp, không ghi DECISIONS thật.
