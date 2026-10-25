# Kế hoạch giai đoạn tới: P6–P10 và quyển đồ án

- **Tạo ngày:** 22/10/2026. **Người soạn:** Claude.
- **Quyền tạo file:** lời Minh ngày 22/10/2026: "tôi duyệt tạo file, nhưng file này phải ghi lại những quyết định mới nhất, để không bị mất thông khi chuyển phiên"; "tạo file đề đề xuất luôn trong lượt này để các lần sau sửa trực tiếp và theo dõi các thay đổi sau khi đã đào sâu nghiên cứu".
- **Trạng thái:** Phần A là lời Minh, chép nguyên văn từ chat. Mọi phần khác là **ĐỀ XUẤT**, chưa duyệt.
- **Quan hệ với tài liệu khác:** file này không thay MRP, PLAN-P6, DE-XUAT-HUONG-GRAFANA-RCA, WHY, DECISIONS, AGENTS. Đề xuất sửa các file đó nằm ở Phần C.
- **Cách sửa:** khi Minh duyệt thì sửa trực tiếp file này; mỗi lần sửa thêm một dòng vào Phần Z.
- **Nhãn:**
  - [TL] tài liệu chính thức;
  - [REPO] file trong repo này hoặc repo FlashTicket;
  - [TÍNH] tự tính, có giả định;
  - [ĐX] đề xuất, chưa kiểm;
  - [ĐO] chỉ biết khi chạy.

**Phiên mới đọc theo thứ tự:** Phần A (quyết định) → Phần E (câu hỏi đang chờ) → Phần F (việc tiếp theo) → phần cần cho việc đang làm.

---

## Phần A. Quyết định và mong muốn của Minh

Chép nguyên văn từ chat ngày 22/10/2026. Mã M-xx chỉ dùng trong file này. Các mục này **chưa được chép vào `docs/DECISIONS.md`** (xem Phần F.3).

| Mã | Lời Minh (nguyên văn) | Áp vào kế hoạch |
|---|---|---|
| M-01 | "RCA không được chỉ dựa vào các phát hiện từ việc chạy baseline của nhóm. Phải tham khảo cả cơ chế của các phương pháp đã khảo sát … và các công trình, nền tảng khác" (yêu cầu phiên lập kế hoạch) | D.2, D.7 |
| M-02 | "Phần phân tích trước đây tập trung gần như chỉ vào Hit@1. Đề xuất bộ độ đo … Lựa chọn cuối do Minh quyết." | D.6 |
| M-03 | "Nhóm có thể tạo 4 tài khoản. AWS có khoảng 200 USD tín dụng miễn phí; nhóm đang dùng EC2 trong một số task cũ. Google Cloud có khoảng 300 USD tín dụng miễn phí, dự kiến dùng cho máy mạnh hơn." "Mốc "26 giờ nền" trong các trao đổi trước thuộc một số phép phát hiện của Grafana Cloud. Bản Grafana tự cài đặt không có yêu cầu này; thời gian chạy nền để chọn ngưỡng cảnh báo là lựa chọn thiết kế của nhóm." | Phần B, D.8 |
| M-04 | "tôi đã bỏ 5.5 thay vào đó trình bày trong email luôn" (nguyên văn email ở Phụ lục P1) | Phần B, D.4, E |
| M-05 | "4 tài khoản khác nhau, đều là free, aws hiện instance mạnh nhất có thể sử dụng từ aws là m7i-flex.large" | D.8 |
| M-06 | "flash ticket hiện chưa chạy được luồng chính, các thành viên khác vẫn đang phát triển, nhưng đảm bảo sẽ sẵn sàng sau khi test thành công trên dataset công khai" | D.9, D.12 |
| M-07 | "phải chọn 1 cái hả ? tưởng có kêt quả thì đo được hết các độ đo ?" | D.6: mọi độ đo đều tính và báo; "độ đo chính" chỉ dùng khi phải quyết |
| M-08 | "nếu laptop chạy được trơn tru thì cho phép, không thì chạy trên cloud, tiền không phải vấn đề" | D.8.3 (cần SPEC T-042) |
| M-09 | "t41 là do codex đề xuất nên tôi không rõ nó có thực sự cần thiết không" | E-10 |
| M-10 | "mở rộng và nghiên cứu sâu hơn, vì tôi không chuyên môn nên có nhiều khía cạnh tôi không tính đến … tôi cần có 1 plan cho tương lai thật chắc chắn, về khả năng triên khai hạ tầng tôi chưa có kinh nghiệm, phát triển phương pháp RCA tôi cũng không nghĩ có thể cho ra 1 phương pháp mang lại kết quả đo cao" | Toàn file |
| M-11 | "tôi duyệt tạo file, nhưng file này phải ghi lại những quyết định mới nhất, để không bị mất thông khi chuyển phiên" | File này |
| M-12 | "nếu cả MRP cần thay đổi hay các decision Q-123 nào đó mà bạn thấy nên thay đổi thì cứ đề xuất, tôi không muốn agent bị gò bó trong các luật 1 cách quá mức, phần MRP P6: phát hiện có dùng đồ thị là bắt buộc cũng có thể đổi để phù hợp với tình hình hiện tại là sử dụng grafana cho bước báo động." | Phần C, D.4 |
| M-13 | "cái tôi cần là được bạn đề xuất 1 cách độc lập ,đa chiều, đề xuất ra những hướng mà tôi chưa nghĩ đến, thay vì chỉ tập trung vào những thứ đang có, hoặc việc hiện tại đang cố định LLM là ở khâu cuối, nhưng nếu LLM có thể hữu ích trong các khâu trung gian thì bạn vẫn có thể đề xuất" | D.3, Phần C |
| M-14 | "việc kết hợp các phương pháp lại thành 1 phương pháp tổng, thay vì mỗi bài học lại là 1 phương pháp riêng lẻ, tất nhiên là nếu kết hợp khả thi, phần này có thể note rõ để sau này khi triển khai task cụ thể, agent sẽ phân tích." | D.2 |
| M-15 | "về thời gian thi tôi cũng cần agent không nên ưu tiên thời gian quá nhiều … thời gian không phải vấn đề, vấn đề là 1 plan hợp lý, trước đó G2 agent dự đoán 20/10 là không thể hoàn thành nhưng cuối cùng đã hoàn thành trước mốc, không thể hoàn thành là quá mạnh." | D.12, D.13: không dùng thời gian làm lý do cắt phạm vi |
| M-16 | "dùng grafana tự host thì có kết hợp được với grafana cloud hay không nếu có thì có thể tận dụng tối đa không, thay vì chỉ gói gọn những gì đã có, miễn sai demo thật suôn sẻ." | D.8.1, D.8.2 |
| M-17 | "aws-runtime-baseline.md là ban đầu, hiện tại sau này có thể có thêm nhiều tài khoản , ngoài ra còn có thể tạo nhiều instance trên cùng 1 account aws, chỉ là đốt tiền sẽ nhanh, nhưng chấp nhận được cho giai đoạn test tải nặng hoặc gần cuối dự án." | D.8.4 |
| M-18 | "chạy trên RE2 TÔI không bắt buộc phải vượt baseline nhưng nếu thua thì cũng không được quá cách biệt, còn trên flash ticket thì tôi hi vọng là phải vượt vì đây là hệ thống tự thiết kế cho phương pháp nên nếu không vượt thì rất dễ bị hội đồng bảo vệ đánh giá kém." | D.1, E-01, E-04 |
| M-19 | "tôi thấy so sánh với việc bỏ đồ thị là đủ, so với các quy tắc đơn giản như chọn sâu nhất, sớm nhất thì tôi đồng ý, chỉ là xáo trộn các nút ngẫu nhiên thì tôi thấy không hợp lý (c-a, c-d, c-e,c-f tôi đồng ý, c-c thì tôi chưa chắc lợi ích của nó là gi), nếu tôi nhận định sai hoặc việc so sánh với đồ thị ngẫu nhiên là có giá trị cao thì bạn cứ đề xuất" | D.5, E-02, E-03 |
| M-20 | "về việc dùng đồ thị để tham giá quyết định báo động thì tôi chưa rõ, là 1 hướng nghiên cứu phương pháp khác dự phòng cho luật của grafana ? nếu là vậy thì tôi cần để hướng này xem xét sau khi có quyết định từ giảng viên" | D.4: nhánh này hoãn tới khi có ý kiến cô |
| M-21 | "nếu quan điểm của tôi có phần nào mâu thuẫn thì hãy hỏi lại tôi" | Phần E |
| M-22 | "soạn prompt cho codex phản biện cũng cần ưu cầu codex tuân theo nhưng mong muốn này của tôi và đề xuất sâu hơn những thứ tôi không nghĩ đến" | Phụ lục P2 (ngoại lệ AGENTS §9, xem C-10) |
| M-23 | "tạo file đề đề xuất luôn trong lượt này để các lần sau sửa trực tiếp và theo dõi các thay đổi sau khi đã đào sâu nghiên cứu" | Cách sửa file; Phần Z |
| M-24 | "E-01: "phải vượt" trên FlashTicket là mục tiêu thiết kế, kèm năm luật chống thiên lệch ở D.9; nếu không vượt thì báo trung thực theo Q-04." | D.1, D.9, C-03; E-01 đã trả lời |
| M-25 | "E-02: bỏ đối chứng đồ thị ngẫu nhiên; kết luận ghi là lợi ích của bước lan, không phải của cấu trúc phụ thuộc thật." | D.5, C-02, D.14; E-02 đã trả lời |
| M-26 | "C-c giữ." | D.5; E-03 đã trả lời |
| M-27 | "bạn đề xuất E-04" | D.1, E-04: Claude đề xuất biên Δ, chờ Minh duyệt |
| M-28 | "E-05 tôi chưa hiểu rõ, việc nghiên cứu phương pháp dùng đồ thị cho cảnh báo này sẽ tách biệt với phương pháp RCA nhóm sẽ nghiên cứu hay sao ?" | D.4.1 giải thích; C-01 chờ Minh |
| M-29 | "E-06: chỉ lượt này , nhưng prompt vẫn phải tuân theo prompt mẫu." | Phụ lục P2; C-10 |
| M-30 | "E-07: C01 liên quan đến E-05 tôi chờ bạn trả lời rồi mới quyết, duyệt C02 03 04 05 06 07 08 09 12 13 c-10 không duyệt" | Phần C, bảng trạng thái C.1 |
| M-31 | "c-11 trươc giờ spec luôn có ngân sách mà, sao phải thêm luật làm gì ?" | C-11 rút lại |
| M-32 | "c-14 tôi không chắc, tôi không tuyên bố mạnh là phương pháp hợp nhất từ các bài học đã rút ra" | C-14 sửa lời; D.2 đổi tên |
| M-33 | "E-08 có thẻ nâng lên gói paid khi cần nhưng hiện aws đã đủ dùng rồi trong khi gg cloud cung cấp server trong gói free còn mạnh hơn instance mạnh nhất mà gói free aws cung cấp, khi nào cần tải nặng thì mở, linh hoạt được" | D.8.4 |
| M-34 | "E-09 chưa có thông tin cụ thể về ngày bảo vệ, trước hết cần lên plan đúng đã." | D.12 |
| M-35 | "E-10 phản biện đầy đủ , tôi sẽ tự tạo phiên mới yêu cầu claude phản biện, nhưng mà task 41 là codex đề xuất nhanh nên tôi không rõ là task này có quan trọng không" | Phần F, A1 |
| M-36 | "E-11 có, không đăn đo vấn đề này"; "E-12 tôi chưa hiểu mục đích, giải thích lại"; "E-13 không gửi cô" | D.8.2; Phần E (E-12 giải thích); D.4.1 |
| M-37 | "E-04 vậy nếu không vượt thì sao ? hay chỉ đặt ngưỡng cho có mà không có backup ? chưa sửa hay duyệt E-04 nhé." | E-04 giữ nguyên, chưa duyệt; Claude trả lời câu hỏi trong chat 22/10 |
| M-38 | "duyệt E-05" | C-01 duyệt hướng (bảng C.1) |
| M-39 | "các phần còn lại duyệt." | C-14 duyệt hướng; chính sách phản biện ở D.13 duyệt; C-02 duyệt nhưng còn chọn cách xử lý RQ3d (Phần E) |
| M-40 | "E-12 tạo prompt cho phiên claude mới tôi sẽ cho phép dùng subagent." | Phụ lục P3; Phần F, A10 |
| M-41 | "tôi thấy agent hay nói về việc là sửa sau khi xem test là mất giá trị, mất cái gì ? xem biết lỗi nằm ở đâu để điều chỉnh phương pháp thì có gì sai ? … cả việc chia ra dữ liệu dev test rồi nói là không được lộ test, tôi thấy không hợp lý, ngay cả những bài học rút ra từ G2 cũng là sửa theo các lỗi tìm được, sau test phát hiện thêm lỗi thì không được sửa nữa à ?" | Câu hỏi, chưa phải quyết định. Claude trả lời trong chat 22/10; đề xuất C-15; E-14 chờ Minh |
| M-42 | "phương án B duyệt thì có sửa lại luật 1 ở agent không ?" | Câu hỏi. Claude trả lời: luật cứng 1 giữ nguyên; các chỗ phải sửa ghi ở C-15. Câu này có thể đọc là đã duyệt B hoặc là câu điều kiện, nên chờ Minh xác nhận (E-14) |
| M-43 | "duyệt B, sau khi sửa xong, xem phản hồi của codex dưới đây, sau đó phản biện lại codex và nêu các phần mới cập nhật yêu cầu codex xem xét" | C-15 phương án B duyệt hướng, gồm điểm (5); E-14 đã trả lời. Phản biện của Codex ngày 22/10 nằm trong chat, Claude đáp trong chat |
| M-44 | Ngày 23/10/2026: "duyệt E-04". Khi Claude hỏi duyệt bản nào, Minh chọn: "E-04 sửa theo KS-07 (Recommended)" | D.1 (E-04 đã duyệt), Phần E, C-08 ở bảng C.1. Nội dung KS-07 ở `docs/KHAO-SAT-SAU-K1-K6.md` mục 3 và Phụ lục A.5 |
| M-45 | Ngày 23/10/2026: "Duyệt P-A (đoạn mới cho D.1 E-04, thêm M-45 ở Phần A và một dòng Phần Z của KE-HOACH) và P-B (sửa đúng các vị trí đã liệt kê trong docs/KHAO-SAT-SAU-K1-K6.md, thêm Phụ lục C và dòng lịch sử). Giữ hai câu N3. Không sửa file khác, không commit." | D.1 (cách đọc E-04: hai câu hỏi; sức phân biệt kèm giả định; ghi chú M1). "Hai câu N3" là dòng "Đã áp vào file" ở Phần A và dòng "Câu hỏi còn chờ Minh" ở Phần E, sửa cùng lượt M-44 |
| M-46 | Ngày 23/10/2026: "041 đóng rồi , cập nhật ngay để lần sau đừng nhắc lại nữa" | T-041 đã nghiệm thu và đóng ngày 23/10/2026 (Q-186, ghi ở DECISIONS và STATE từ phiên đóng task). Phần B, E-10, A1 ở Phần F sửa theo |
| M-47 | Ngày 23/10/2026: "duyệt sửa RQ3d" | C-02: chọn sửa câu RQ3d theo đề xuất ở Phần E (E-07). Bước tiếp: soạn đoạn sửa MRP, WHY-07, LESSONS QT8 và trình trước khi ghi (bảng C.1) |
| M-48 | Ngày 23/10/2026: "Duyệt đề xuất 2: đưa bốn nhóm gợi ý của bản khảo sát vào bản thiết kế đầu tiên làm món để thử. Mỗi món ghi trước cần dữ liệu gì, làm gì khi thiếu, và ba kết cục: giúp thì giữ, hại thì bỏ, không đủ ca để phân xử thì giữ lại và kiểm trên FlashTicket. Không sửa kế hoạch trước." | Khi soạn SPEC M1: KS-10 (thay đổi thành phần, D.2) và KS-11 (đối chứng, D.5) của `docs/KHAO-SAT-SAU-K1-K6.md` là ứng viên để thử; KS-14 là danh sách đọc ở bước đầu; KS-16 là phép đếm chỉ đọc trên dev, chạy đầu tiên. Mỗi ứng viên ghi trước dữ liệu cần, cách xử lý khi thiếu và ba kết cục nêu trên. D.2, D.5, D.7 chưa sửa; chi tiết duyệt cùng SPEC M1 |

**Đã áp vào file:**
- Không coi thời gian là lý do cắt phạm vi (M-15).
- Đề xuất cả thay đổi tài liệu điều hành (M-12).
- Mặc định mở sự cố bằng luật cảnh báo Grafana; nhánh "đồ thị tham gia quyết định báo động" hoãn tới khi có ý kiến cô (M-12, M-20).
- Thiết kế một phương pháp hợp nhất nhiều mô-đun (M-14).
- Xét dùng LLM ở cả các khâu trung gian (M-13).
- Kết hợp Grafana tự cài với Grafana Cloud (M-16).
- Đối chứng: giữ C-a, C-d, C-e, C-f (M-19) và C-c (M-26). Bỏ C-b, đồ thị ngẫu nhiên; kết luận ghi là "lợi ích của bước lan", không phải "lợi ích của cấu trúc phụ thuộc thật" (M-25).
- Đề xuất C-02 đến C-09, C-12, C-13 được duyệt hướng; C-10 không duyệt; C-11 rút lại; C-01 và C-14 chờ Minh (M-30, M-31, M-32). Xem bảng C.1.
- Không gửi câu hỏi cho cô (M-36). AWS hiện đủ dùng; mở Google Cloud khi cần tải nặng; nâng AWS lên Paid khi cần (M-33). Dùng Grafana Cloud (M-36). Chưa có ngày bảo vệ (M-34). T-041 phản biện đầy đủ (M-35).
- C-01 và C-14 duyệt hướng; chính sách phản biện ở D.13 duyệt (M-38, M-39). E-04 chưa duyệt (M-37); ngày 23/10/2026 duyệt theo bản sửa KS-07 (M-44). Phiên Claude mới làm khảo sát sâu, được dùng subagent (M-40, Phụ lục P3).
- Vượt baseline trên FlashTicket là mục tiêu thiết kế, không phải điều kiện bắt buộc; năm luật chống thiên lệch ở D.9 là bắt buộc; nếu không vượt thì báo trung thực theo Q-04 (M-24).
- T-041 đã đóng (Q-186); không còn việc phản biện T-041 (M-46). RQ3d: chọn sửa câu hỏi (M-47).

---

## Phần B. Trạng thái và dữ kiện đã kiểm (22/10/2026)

| Mục | Dữ kiện | Nguồn |
|---|---|---|
| Lịch cố định | Nộp quyển 30/12/2026 (Q-23). Mốc G4 "cuối tháng 11" (Q-70; đề xuất đặt lại ở C-04). Ngày bảo vệ: repo chưa có | [REPO] |
| Báo cáo gửi cô | Gửi 21/10. Chương 5 đã bỏ mục 5.5, nhưng 5.1.2 và Bảng 5.9 còn dẫn tới "mục 5.5" và "Bảng 5.5". Email chỉ xin góp ý chung, không hỏi năm câu cụ thể | M-04; Phụ lục P1 |
| Mâu thuẫn định hướng | Chương 5 §5.3.2: đồ thị chưa tham gia quyết định báo động. MRP P6: phát hiện có dùng đồ thị là bắt buộc. Minh cho phép đổi MRP (M-12) | [REPO]; M-12 |
| Kết quả nền | RE2-TT dev30, Hit@1: TORAI B 0,867 (26/30), SimpleRCA 0,833 (25/30), BARO 0,700. Hit@3 của TORAI B = 1,000; MRR 0,917. Nezha-OB: Hit@1 tốt nhất 0,364 (BARO); MRR tốt nhất 0,538 (SimpleRCA) | `results/T-034/bang-baseline.json` (hash khớp `runs/manifest-cuoi-007`) |
| FlashTicket | Chưa chạy được luồng chính (M-06). Bản clone ở `D:/Project/flash-ticket-platform`: Spring Boot **4.1.1**, Java **21**; năm service mới là khung (một lớp Application), gateway đã có code | M-06; [REPO FT] `services/*/pom.xml` |
| Thiết kế đích FlashTicket | Hai máy 8 GiB, mỗi máy khoảng 6 GiB cho tiến trình. Bộ quan sát đặt ở EC2 #2, chung với MongoDB, Keycloak, event, user, Config, Eureka, chatbot. Minh coi đây là bản ban đầu (M-17) | [REPO FT] `aws-runtime-baseline.md` §4–5 |
| AWS | 4 tài khoản của 4 người, đều gói Free; máy mạnh nhất m7i-flex.large (2 vCPU, 8 GiB) (M-05). Tín dụng 100 USD khi mở, thêm tối đa 100 USD qua hoạt động. Gói Free hết sau 6 tháng hoặc khi hết tín dụng; khi đó **tài khoản bị đóng**, có 90 ngày để nâng cấp, sau đó xóa dữ liệu. Tín dụng hết hạn sau 12 tháng. Một khách hàng không nhận tín dụng Free Tier cho hơn một tài khoản. Tham gia AWS Organizations thì tài khoản tự lên gói Paid | [TL] AWS billing, EC2 Free Tier, điều khoản |
| AWS quota | **Quota mặc định "Running On-Demand Standard instances" là 5 vCPU mỗi vùng.** Mỗi máy m7i-flex.large dùng 2 vCPU, nên mỗi tài khoản ở một vùng chạy được tối đa 2 máy loại này. Có thể xin tăng; có người dùng báo tài khoản mới bị từ chối (chưa kiểm). Quota thật của từng tài khoản: chưa kiểm | [TL] EC2 instance quotas; diễn đàn re:Post |
| Google Cloud | 300 USD trong 90 ngày tính từ lúc đăng ký. Không GPU, không xin tăng quota, không VM Windows. Hết tiền hoặc hết hạn thì tài nguyên bị dừng; 30 ngày ân hạn. Tín dụng không trả được Gemini API trên AI Studio. Quota vCPU khi dùng thử: chưa kiểm | [TL] |
| Grafana Cloud Free | 10.000 chuỗi metric; 50 GB log, 50 GB trace, 50 GB profile mỗi tháng; lưu 14 ngày; Application Observability 2.232 host-giờ; Assistant cho 3 người dùng AI (mỗi người 40 triệu token) cộng 25 triệu token cho lượt tự động; Synthetics 100.000 lượt API và 10.000 lượt trình duyệt; k6 500 VU-giờ; IRM 3 người dùng; ghi "không bao giờ tính tiền". Knowledge Graph có sẵn trong mọi stack, cần Application Observability và metric service graph. ML (forecast, outlier, Sift) miễn phí; Sift thiên về Kubernetes | [TL] grafana.com/pricing, tài liệu Knowledge Graph, Sift |
| "26 giờ nền" | Chỉ là yêu cầu của hai insight trên Grafana Cloud. Luật cảnh báo của bản tự cài không có yêu cầu lịch sử tối thiểu | [TL]; M-03 |
| Laptop | RAM 15,7 GiB. Ổ C còn 61 GB, ổ D còn 35 GB. Docker 28.3.2 (chưa bật lúc kiểm). WSL2 mặc định cấp 50% RAM (khoảng 7,8 GiB) và swap bằng 25% RAM | kiểm 22/10; [TL] Microsoft |
| OpenTelemetry Demo | Cần 6 GB RAM (khoảng 3 GB ở chế độ tối giản, chế độ này bỏ Kafka) và 14 GB ổ. Có 19 cờ bật lỗi. Đi kèm Jaeger, Grafana, Prometheus, OpenSearch | [TL] |
| Công cụ | Tempo bản mới nhất là 3.x (3.0 bỏ ingester, compactor, mã hóa v2). Collector tự báo mất dữ liệu ở cổng 8888 (`otelcol_receiver_refused_*`, `otelcol_exporter_send_failed_*`, `otelcol_exporter_enqueue_failed_*`, `otelcol_exporter_queue_size/capacity`). Grafana khuyên dùng Alloy, một bản phân phối của OTel Collector có chế độ chạy cấu hình YAML của Collector. Tài liệu OTel không đưa con số overhead của Java agent, khuyên tự đo | [TL] |
| Java agent với Spring Boot 4 | Tài liệu ghi agent hỗ trợ Spring Web MVC từ 3.1 trở lên. Bài viết của Spring lưu ý agent sửa bytecode nên phải khớp đúng phiên bản thư viện. Spring Boot 4 có thêm `spring-boot-starter-opentelemetry`. **Chưa kiểm trên FlashTicket** | [TL] |
| Chaos Monkey for Spring Boot | Không tìm thấy xác nhận hỗ trợ Spring Boot 4 | tra web 22/10 |
| Chi phí test cũ | BOCPD 30 ca RE2-TT trên EC2 mất 8.419 s | [REPO] `tasks/T-025-che-do-b/LOG.md:131` |
| Bộ giữ ngoài RE3-OB | 30 ca lỗi mã nguồn f1–f5 (ad 9, cart 3, currency 3, email 15). Chưa tải; dung lượng chưa kiểm | [REPO] `results/T-002/public-sources.md:32` |
| License | License của Nezha còn để mở | [REPO] STATE, dòng T-026 |
| T-041 | **Đã nghiệm thu và đóng ngày 23/10/2026** (Q-186, M-46). Không còn việc phản biện T-041 | [REPO] STATE, DECISIONS Q-186 |
| Quyết định cũ liên quan | Q-04: báo kết quả trung thực, kể cả khi đồ thị không hơn baseline. Q-22: bỏ điều kiện "phải có ít nhất một điều kiện đồ thị hỗ trợ tốt". Q-62: "Mốc phải vượt ở P7 là baseline tốt nhất của P3" | [REPO] DECISIONS |

---

## Phần C. Đề xuất thay đổi tài liệu điều hành

Mỗi mục cần Minh duyệt riêng (Luật 0). Ghi "duyệt C-xx" là đủ để agent soạn đúng đoạn sửa, rồi trình lại trước khi ghi.

| Mã | Tài liệu, mục | Hiện ghi | Đề xuất | Vì sao | Ảnh hưởng |
|---|---|---|---|---|---|
| C-01 | MRP §2.3, P6 tầng 2; WHY-02 | Phát hiện bất thường có dùng đồ thị là bắt buộc; đồ thị tham gia điểm bất thường ở tầng 2 | Tách hai mức. **Mức hệ thống:** mở sự cố bằng luật cảnh báo Grafana. **Mức thành phần:** lúc chẩn đoán, dùng đồ thị để phát hiện thành phần bất thường và tách bất thường tự sinh khỏi bất thường kế thừa (Mô-đun B ở D.2). Nhánh đồ thị tham gia quyết định báo động ghi là **hoãn**, kích hoạt nếu cô yêu cầu | M-12, M-20. Chương 5 đã báo cô theo hướng này. DT18 viết "phát hiện dấu hiệu bất thường", không bắt buộc đồ thị phải quyết định báo động | M5, M6 thu nhỏ; C8, C12, C15 hoãn; RQ3a đo trên bộ luật. Rủi ro: cô hiểu bước 2 theo nghĩa hẹp; khi đó kích hoạt nhánh hoãn |
| C-02 | MRP §3 RQ3d; MRP §6 mục 3; MRP P7 (nhánh đồ thị ngẫu nhiên); LESSONS QT8; WHY-07 | Muốn khẳng định lợi ích do cấu trúc thì phải hơn cả nhánh bỏ quan hệ và đồ thị ngẫu nhiên giữ bậc | **Đã có quyết định của Minh (M-25): bỏ đối chứng đồ thị ngẫu nhiên.** Sửa các mục trên cho khớp: chỉ còn nhánh bỏ quan hệ (C-a) và quy tắc đơn giản (C-d); kết luận về quan hệ chỉ ở mức "lợi ích của bước lan, của phép dùng quan hệ"; không khẳng định "lợi ích do cấu trúc phụ thuộc thật". Bản đề xuất trước (giữ hẹp) xem D.5 | M-19, M-25 | Bớt phép chạy. RQ3d ("phần thay đổi có đến từ cấu trúc đồ thị thật không") không còn được trả lời trực tiếp; cần sửa RQ3d, hoặc ghi là ngoài phạm vi kèm giới hạn |
| C-03 | DECISIONS Q-62 | "Mốc phải vượt ở P7 là baseline tốt nhất của P3" | Đổi "phải vượt" thành "mốc so sánh". RE2-TT: không thua quá biên Δ khai trước. Nezha-OB: mục tiêu cải thiện. FlashTicket: mục tiêu vượt (là mục tiêu thiết kế, không phải điều kiện; M-24), theo luật chống thiên lệch ở D.9 | M-18; sức phân biệt thống kê ở D.6 | Tiêu chí P7 và cách viết kết luận |
| C-04 | DECISIONS Q-70; MRP §7 | G4 cuối tháng 11/2026 | Minh đặt lại G3, G4 theo thứ tự phụ thuộc ở D.12. Không dùng mốc ngày làm lý do cắt phạm vi | M-15 | Lịch báo cáo cô |
| C-05 | MRP P8 | LLM chỉ ở khâu cuối, không đổi thứ hạng | Cho phép LLM ở khâu trung gian (D.3), với năm điều kiện: không thấy nhãn; ghim model và phiên bản; lưu cache mọi đầu ra; có nhánh bỏ LLM; trong phương pháp chính LLM không quyết thứ hạng (chỉ được thử như một nhánh riêng) | M-13 | Thêm hai thành phần có thể đánh giá được (L1, L2) |
| C-06 | MRP P10 | FlashTicket dùng để demo và làm bộ có tiêm lỗi | Thêm: chạy các baseline trên dữ liệu FlashTicket qua cùng định dạng nội bộ (WHY-08); danh mục kịch bản khai trước; nhãn vùng lấy từ tín hiệu độc lập với RCA (k6, Synthetics) | M-18: muốn vượt trên FlashTicket thì phải có baseline chạy trên đó | Thêm việc viết adapter xuất dữ liệu |
| C-07 | MRP §4 | Không nhắc OpenTelemetry Demo | Ghi OTel Demo là sân thử hạ tầng và chuỗi online, không phải bộ đánh giá chính | FlashTicket sẵn sàng muộn (M-06) | Thêm vai trò rõ ràng, tránh dùng nhầm Demo làm dataset |
| C-08 | WHY-06 | Danh sách độ đo, trạng thái "Đề xuất (G3)" | Ghi: độ đo chính của xếp hạng là MRR; báo đủ các độ đo khác; báo mức ngẫu nhiên; nêu phép thống kê (D.6) | M-02, M-07 | Khóa cách chọn trên dev |
| C-09 | PLAN-P6 | 13 phần việc chính + 15 nhánh | Sau phản biện, thay bằng D.14 và D.12; giữ PLAN-P6 làm lịch sử | Hướng đã đổi | Ít task hơn, ít vòng phản biện hơn |
| C-10 | AGENTS §9; DECISIONS Q-44; LESSONS SL31 | Prompt bàn giao chỉ được điền thông tin trung tính | Khi Minh yêu cầu, cho phép thêm "Khối yêu cầu của Minh" (lời Minh, nêu phạm vi và mong muốn), đặt sau các khối mẫu | M-22 | Lượt này đã dùng (Phụ lục P2). Cần Minh quyết chỉ áp cho lượt này hay thành luật |
| C-11 | AGENTS luật cứng 8 | Báo trước và chờ Minh với thao tác tốn kém | Nếu SPEC đã duyệt có ngân sách (giờ máy, USD, GB tải, số subagent) thì chạy trong ngân sách không phải hỏi lại; vượt ngân sách mới hỏi | M-08, M-15. Minh là người duyệt duy nhất nên dễ thành nút thắt | Nhanh hơn; vẫn giữ trần |
| C-12 | MRP P9 | Kho quan sát tự cài | Thêm bản sao trên Grafana Cloud để demo và làm đối chứng định tính (D.8.2) | M-16 | Thêm cấu hình; dữ liệu demo đi ra ngoài |
| C-13 | Repo FlashTicket `aws-runtime-baseline.md` (repo khác; Minh phụ trách observability baseline) | Hai máy 8 GiB, bộ quan sát ở EC2 #2 | Cho phép giai đoạn 3 dùng thêm máy, ví dụ một máy riêng cho bộ quan sát, theo quota vCPU (D.8.4) | M-17; RAM EC2 #2 có thể không đủ | Phải trao đổi với nhóm hệ thống |
| C-14 | MRP §5 P6 | Không có mô tả cấu trúc tổng của phương pháp | **Lời đã sửa theo M-32:** MRP P6 mô tả phương pháp là một chuỗi chẩn đoán gồm các thành phần thay được. Mỗi thành phần ghi nguồn (hạn chế P4, công trình khác, DT18 hoặc nhu cầu kỹ thuật) và có nhánh bỏ để đo tác dụng. **Không** tuyên bố đây là phương pháp mới hay "hợp nhất từ các bài học" | M-14, M-32 | Định hướng cho SPEC M1; không thêm khẳng định mạnh |
| C-15 | MRP §6 mục 1, P7, §9 (dòng "Thiết kế theo test"); LESSONS QT6 | Test chỉ mở một lần sau G3; không sửa sau khi xem test | **Phương án B, cho phép sửa sau test nhưng tách cách báo cáo.** (1) Giữ test khóa tới G3; lần chạy đầu sau khi khóa là **kết quả chính**, báo nguyên. (2) Sau đó được xem lỗi trên test và sửa phương pháp. Kết quả sau sửa ghi rõ "đã dùng test để thiết kế", không gọi là kiểm độc lập. (3) Bản sau sửa được kiểm độc lập trên dữ liệu chưa dùng: các lượt FlashTicket mới chạy sau khi khóa bản sửa; RE3-OB nếu chưa mở. (4) Tách sửa lỗi cài đặt (chạy lại mọi phương pháp, ghi rõ) với sửa thiết kế. Hai phương án khác Minh có thể chọn thay: A, giữ nguyên luật hiện hành; C, bỏ chia dev/test trên RE2-TT và Nezha-OB, chỉ giữ RE3-OB và FlashTicket làm phần kiểm độc lập. **(5) Bổ sung cho B (M-42):** RE3-OB chỉ mở một lần, cho bản cuối cùng sau mọi lần sửa, để còn một phép kiểm sạch trên dữ liệu công khai. **Các chỗ phải sửa nếu chọn B:** AGENTS §11, dòng "Đang sửa thiết kế sau khi đã nhìn kết quả test" (đổi thành: sửa mà không ghi rõ, hoặc báo kết quả sau sửa như một phép kiểm độc lập); MRP §6 mục 1; MRP P7 ("chạy một lần"); MRP §7, câu cuối của "Cách dùng G3"; MRP §9, dòng "Thiết kế theo test"; LESSONS QT6; WHY-04 (thêm cách dùng test sau G3). **Luật cứng 1 của AGENTS giữ nguyên**, vì nó chỉ cấm mở test trước G3 | M-41, M-42; lý do ở câu trả lời trong chat 22/10 | Đổi cách viết kết luận P7. Luật cứng 1 (không mở test trước G3) giữ nguyên ở phương án A, B |

**Không đề xuất đổi:** DT18 (tên và nhiệm vụ chính thức); luật cứng 1 về tập test khóa; luật cứng 6 về không đưa nhãn vào phương pháp. Lý do: bỏ ba thứ này thì kết quả mất giá trị trước hội đồng.

### C.1 Trạng thái các đề xuất (cập nhật 22/10/2026)

"Duyệt" ở đây là duyệt hướng. Theo quy ước ở đầu Phần C, agent soạn đúng đoạn sửa cho từng tài liệu rồi trình Minh trước khi ghi. Dòng cũ của DECISIONS không bị sửa; đổi nghĩa thì nối dòng Q mới.

| Mã | Trạng thái | Bước tiếp theo |
|---|---|---|
| C-01 | Duyệt hướng (M-38) | Soạn đoạn sửa MRP §2.3, P6 tầng 2 và WHY-02 → trình |
| C-02 | Duyệt hướng (M-30, M-39). Đã chọn sửa câu RQ3d (M-47). **Đã sửa ngày 23/10/2026** theo lời Minh "duyệt đề xuất 1 3" | Xong: MRP RQ3d, dòng đối chứng ở P4 và P7, §6 mục 3; WHY-07; LESSONS QT8; AGENTS luật cứng 18 |
| C-03 | Duyệt hướng (M-30) | Soạn dòng DECISIONS mới, đổi nghĩa Q-62 → trình |
| C-04 | Duyệt hướng (M-30). Ngày mới chưa có (M-34) | Soạn dòng DECISIONS mới: bỏ mốc G4 cũ, mốc mới chờ Minh → trình |
| C-05 | Duyệt hướng (M-30) | Soạn đoạn sửa MRP P8 và §5 (LLM ở khâu trung gian, năm điều kiện) → trình |
| C-06 | Duyệt hướng (M-30) | Soạn đoạn sửa MRP P10 → trình |
| C-07 | Duyệt hướng (M-30) | Soạn đoạn thêm vào MRP §4 → trình |
| C-08 | Duyệt hướng (M-30). E-04 đã duyệt theo bản sửa KS-07 (M-44) | Soạn đoạn sửa WHY-06, gộp biên Δ và cách đọc của E-04 ở D.1 → trình |
| C-09 | Duyệt hướng (M-30) | Soạn ghi chú đầu PLAN-P6 trỏ tới file này; giữ nội dung cũ làm lịch sử → trình |
| C-10 | **Không duyệt** (M-30). Khối yêu cầu của Minh chỉ dùng cho lượt phản biện ở Phụ lục P2; prompt vẫn theo mẫu (M-29) | — |
| C-11 | **Rút lại** (M-31). Minh đúng: SPEC đã duyệt luôn có ngân sách, và việc duyệt SPEC đó đã là sự đồng ý theo luật cứng 8 | — |
| C-12 | Duyệt hướng (M-30) | Soạn đoạn sửa MRP P9 → trình |
| C-13 | Duyệt hướng (M-30) | Soạn đoạn sửa `aws-runtime-baseline.md` ở repo FlashTicket (repo khác) → trình; báo nhóm hệ thống |
| C-14 | Duyệt hướng với lời đã sửa theo M-32 (M-39) | Soạn đoạn sửa MRP §5 P6 → trình |
| C-15 | **Phương án B duyệt hướng** (M-43), gồm điểm (5): RE3-OB chỉ mở cho bản cuối. Luật cứng 1 giữ nguyên | Soạn đoạn sửa AGENTS §11, MRP §6 mục 1, P7, §7, §9, LESSONS QT6, WHY-04 → trình |

---

## Phần D. Kế hoạch

### D.1 Đích đến và mức thành công

- **Tầng 1, tối thiểu. Phải đạt dù phương pháp không thắng.**
  - (a) Phương pháp hợp nhất được cài, kiểm giá trị trung gian, chạy hết dev và chạy test một lần.
  - (b) So với 6 baseline và các đối chứng.
  - (c) Phân tích từng ca: đồ thị giúp ở đâu, hại ở đâu, vì sao.
  - (d) Chuỗi thu thập → cảnh báo → chẩn đoán → giao diện chạy được trên FlashTicket.
  - (e) LLM giải thích.
  - Đây là đóng góp hợp lệ (MRP §3, Q-04, DT18-NV3).
- **Tầng 2, mục tiêu.**
  - **RE2-TT:** không thua baseline đối chứng khai trước (TORAI B) quá biên Δ (M-18). Cách đọc theo E-04 ở cuối mục này (đã duyệt, M-44).
  - **Nezha-OB:** cải thiện, ở mức có ý nghĩa thống kê nếu được.
  - **FlashTicket:** vượt baseline là **mục tiêu thiết kế**, không phải điều kiện bắt buộc (M-18, M-24). Áp đủ năm luật chống thiên lệch ở D.9. Nếu không vượt thì báo trung thực (Q-04).
  - **Ablation:** bỏ mô-đun đồ thị thì kết quả giảm.
- **Tầng 3, mở rộng:** nhánh đồ thị tham gia quyết định báo động (nếu cô yêu cầu); LLM ở khâu trung gian có lợi đo được; nhiều kịch bản Saga.

**Vì sao trên FlashTicket có khả năng vượt (lập luận, chưa kiểm):**
- Trên FlashTicket, phương pháp có thông tin mà baseline không dùng: kind của span, cạnh DB và hàng đợi, máy chạy từng service.
- Dữ liệu công khai thiếu đúng các thông tin đó (Chương 5, Bảng 5.3).
- Đây là "lợi thế thông tin". Phải trình bày đúng như vậy và kèm ablation bỏ cạnh có kiểu, để hội đồng thấy lợi ích đến từ đâu.

**E-04: biên Δ trên RE2-TT** [Đã duyệt ngày 23/10/2026 (M-44), theo bản sửa KS-07 ở `docs/KHAO-SAT-SAU-K1-K6.md`. Bản đề xuất ban đầu (M-27) đọc theo điểm ước lượng ở cả MRR và Hit@1, so với baseline tốt nhất theo từng độ đo; bản này thay thế. Cách đọc làm rõ ngày 23/10/2026 sau phản biện Codex (M-45)]
- **So với ai:** baseline đối chứng khai trước là TORAI B. Không chọn lại baseline theo từng độ đo sau khi xem kết quả. Trên dev30, TORAI B có Hit@1 0,867 và MRR 0,917 [REPO `bang-baseline.json`].
- **Biên:**
  - MRR: Δ = 0,05. Đây là độ đo dùng để kết luận.
  - Hit@1: Δ = 2 ca trên 30 ca dev (0,067); theo cùng tỷ lệ là 4 ca trên 60 ca test. Hit@1 chỉ để mô tả, không thuộc điều kiện kết luận.
- **Vì sao chọn mức này:** đặt giữa hai khoảng cách đã thấy giữa chính các baseline.
  - **Mức "ngang nhau":** TORAI B và SimpleRCA cách nhau 1 ca Hit@1 và 0,026 MRR. G2 ghi khoảng bootstrap của bốn phương pháp đứng đầu chồng nhau [REPO `goi-g2.md` §0].
  - **Mức "rõ ràng kém":** BARO kém TORAI B 5 ca Hit@1 và 0,149 MRR.
- **Cách đọc:** dùng khoảng tin cậy 95% (CI) của chênh MRR (phương pháp mới trừ TORAI B). Báo đồng thời hai kết luận; hai kết luận có thể cùng đúng.
  - **(1) Không thua quá Δ?** Cận dưới của CI lớn hơn −Δ: **đạt E-04** (không thua quá Δ). Ngược lại: **chưa chứng minh được** không thua quá Δ.
  - **(2) Khác 0?** CI nằm trọn trên 0: **hơn** TORAI B. CI nằm trọn dưới 0: **kém** TORAI B. CI chứa 0: **chưa phân biệt được**.
  - Ví dụ: Δ = 0,05, CI = [−0,04; −0,01]. Kết quả: đạt E-04 và kém có ý nghĩa thống kê. Ghi cả hai.
  - E-04 chỉ xét câu (1). Cách tính CI theo D.6; hiện là bootstrap theo ô. KS-08 đề xuất đổi phép kiểm, chưa duyệt.
- **Tiêu chí thực dụng, chỉ báo kèm:** điểm ước lượng chênh không vượt Δ. Không gọi tiêu chí này là phép kiểm không thua.
- **Sức phân biệt** [TÍNH, công thức ở Phụ lục C của `docs/KHAO-SAT-SAU-K1-K6.md`]:
  - Giả định: 60 ca độc lập; SD của chênh RR bằng SD của cặp TORAI B − SimpleRCA trên dev30 (0,363).
  - Nửa độ rộng CI ≈ 0,092. Khi chênh thật bằng 0: xác suất điểm ước lượng dưới −Δ ≈ 0,14; power của câu (1) ≈ 0,19.
  - Gom theo ô làm khoảng rộng hơn trên dev30 (0,151 so với 0,130 khi n = 30). SD của phương pháp mới chưa biết, có thể lớn hơn hoặc nhỏ hơn.
  - Vì vậy kết quả "chưa chứng minh được" là khả năng lớn và phải được báo đúng như vậy.
- **Khi không đạt "không thua":** các phương án có trong tài liệu (K4):
  - (a) báo P(chênh > −Δ) trên trung bình MRR, tính theo ô;
  - (b) đặt Δ trước khi có dữ liệu theo kiểu M1/M2 của FDA, kiểm trên dữ liệu gộp có phân tầng. Phải định nghĩa M1 tương ứng cho RCA trước khi dùng; hiện chưa có;
  - (c) chuyển trọng tâm sang ước lượng cỡ hiệu ứng kèm CI.
  - Chọn phương án nào: Minh quyết khi soạn giao thức (A4).
- **Khi nào khóa:** trước khi chạy dev P6; ghi vào WHY-06 cùng C-08.
- **Nezha-OB:** không đặt Δ, vì đây là bộ có chỗ để cải thiện.

### D.2 Chuỗi chẩn đoán gồm nhiều mô-đun (M-14) [ĐX]

Cách gọi theo M-32: đây là một chuỗi chẩn đoán gồm các thành phần thay được, mỗi thành phần có nguồn và có nhánh bỏ. Không tuyên bố là phương pháp mới hay "hợp nhất từ các bài học". Chữ "phương pháp hợp nhất" ở các mục khác trong file hiểu theo nghĩa này.

```
Dữ liệu (trace, log, metric; FlashTicket có thêm kind, DB, hàng đợi, máy)
 → A. Ánh xạ và chuẩn hóa bằng chứng   (E1, E2, E3, E4)
 → B. Giải thích theo phụ thuộc         (E5; có E8 ở FlashTicket)
 → C. Điểm nguồn và xếp hạng            (E6)
 → D. Vùng nghi ngờ                     (E7)
 → E. Gói bằng chứng cho giao diện và LLM
```

| Mô-đun | Thành phần | Làm gì | Căn cứ | Dữ liệu dùng được |
|---|---|---|---|---|
| A | E1 | Thời gian độc quyền theo đường găng của trace, xử lý lời gọi con chạy song song | Bài học 1; UV-2; CRISP | RE2-TT, Nezha, FT |
| A | E2 | Gắn bằng chứng lên cạnh; nền tính riêng cho từng cạnh; tính cho bên được gọi | Bài học 1; UV-1; MicroHECL | Cả ba; FT có kind |
| A | E3 | Tín hiệu lỗi hai chiều (tăng và giảm); log gom theo mẫu trước khi đếm (có thể dùng L1) | Bài học 2; UV-6; Nezha, Eadro | Cả ba |
| A | E4 | Đưa điểm về cùng thang; chặn điểm vô lý (mẫu số gần 0); giới hạn đóng góp của một nguồn; metric chung không nhân lên theo số thao tác | Bài học 3; UV-7; P5 §46 | Cả ba |
| B | E5 | Một thành phần bất thường được coi là "kế thừa" nếu thành phần nó phụ thuộc giải thích được bất thường đó. Hướng lan theo loại tín hiệu: độ trễ và lỗi lan ngược lên phía gọi | Bài học 1, 6; MRP P6 tầng 2; MicroHECL; Budhathoki; Sage; CIRCA | Cả ba |
| B | E8 | Cạnh dữ liệu, thông điệp, triển khai. Ví dụ: CPU của máy cao thì các service cùng máy nhận bằng chứng "nguyên nhân chung" | Bài học 6; DT18; MonitorRank; Murphy | FT, OTel Demo |
| C | E6 | (a) quy tắc; (b) PageRank cá nhân hóa trên đồ thị con bất thường; (c) xếp lại top-k của một bộ chấm cục bộ mạnh | Bài học 4; MicroRCA; MicroRank | Cả ba |
| D | E7 | Vùng nghi ngờ: chuỗi lan hoặc thành phần liên thông quanh ứng viên đầu | DT18; MicroHECL | Cả ba |
| (tùy chọn) | E9 | Thứ tự xuất hiện bất thường, có dung sai thời gian. Mốc bất thường phải lấy từ bộ phát hiện không nhìn trước | Bài học 7; PAL, FChain, LagRCA | FT tốt hơn; Nezha chỉ 1 điểm/phút |

**Ghi chú khả thi để agent phân tích khi triển khai:**
1. **Tránh đếm hai lần:** E2 (tính cho bên được gọi) và E5 (giải thích theo phụ thuộc) cùng chuyển điểm từ phía gọi xuống phía được gọi. Chỉ giữ một cơ chế, hoặc khai thứ tự rõ và kiểm bằng ablation.
2. **Thứ tự:** E4 phải chạy trước mọi phép lan (Bài học 3, CIRCA: điểm vô lý bị lan sang dịch vụ khác).
3. **Kênh log (E3) không cần cạnh.** Nhánh "bỏ quan hệ" vẫn giữ E3, nên lợi ích của E3 không được tính là lợi ích của đồ thị.
4. **E1 trên RE2-TT, Nezha** chỉ là thời gian chưa được con quan sát phủ, chưa phải thời gian CPU (T-041 §7). Chỉ FlashTicket có kind để gọi đúng là "chờ phía gọi".
5. **Phương án E6(c) (xếp lại top-k)** giữ được điểm cao của bộ chấm mạnh, nhưng tác dụng của đồ thị chỉ ở ít ca. Nếu dùng điểm baseline làm đầu vào thì đối chứng C-c là bắt buộc (D.5).
6. **Thành phần không có dữ liệu:** báo riêng là "thiếu dữ liệu", không điền điểm mặc định (WHY-26, Bài học 5).
7. **Một mô-đun bị bác bỏ** (dự đoán không xảy ra) thì bỏ mô-đun đó. Chuỗi vẫn chạy với các mô-đun còn lại.

**Thứ tự thử, rẻ trước:**

| Lượt | Thành phần | Bác bỏ khi nào (khai trước) |
|---|---|---|
| 1 | E1 | Ở Nezha-OB không hơn phép trừ hợp khoảng con (đang 10/22), hoặc ở RE2-TT kém 26/26 |
| 2 | E4 | Còn ca do một điểm cực lớn quyết định |
| 3 | E3 | Số ca đang đúng bị hỏng vượt số ca lỗi trả về được sửa |
| 4 | E2 | Theo dự đoán UV-1 ở G2 §5 |
| 5 | E5 | Không giảm số ca dịch vụ phía gọi đứng trên root, hoặc tăng ở mốc giả |
| 6 | E6, E7 | E6 chọn theo MRR; E7 báo vùng chứa root và kích thước |

- Lượt 1–3 chạy trên span và log đã lưu, không cần thực nghiệm mới nặng.
- Số cấu hình được thử khai trước trong SPEC M1.

### D.3 LLM ở các khâu (M-13) [ĐX]

**Nghiên cứu đã có:**
- Trên OpenRCA (ICLR 2025), một tập lỗi thật kèm telemetry thô, cấu hình tốt nhất (Claude 3.5 cùng agent riêng) chỉ giải đúng 11,34% ca [TL]. Một phân tích sau cho rằng một số nhãn không suy ra được từ dữ liệu.
- RCACopilot (EuroSys 2024): LLM nhận thông tin đã được thu thập sẵn theo từng loại sự cố, rồi đoán loại nguyên nhân, đạt Micro-F1 0,766 [TL, bản arXiv].
- LILAC (FSE 2024): dùng LLM để tách mẫu log (log template), có bộ nhớ đệm, tăng mạnh độ đúng so với các bộ tách mẫu trước [TL].
- **Hệ quả:** LLM làm tốt khi nhận bằng chứng đã có cấu trúc; làm kém khi phải tự đào telemetry thô. Vì vậy nên dùng LLM để **chuẩn bị** và **diễn giải** bằng chứng, không để LLM tự xếp hạng trên dữ liệu thô.

| Mã | Khâu | Dùng LLM làm gì | Lợi ích | Rủi ro và cách kiểm |
|---|---|---|---|---|
| L1 | Ánh xạ log | Tách và gom mẫu log offline theo kiểu LILAC, lưu cache thành từ điển mẫu | Sửa đúng Bài học 2: log cùng loại ở TORAI bị tách thành nhiều mẫu hiếm | So với Drain trên một mẫu log; kiểm tác dụng lên E3 bằng ablation; LLM không được thấy nhãn hay tên ca |
| L2 | Dựng đồ thị tĩnh | Đọc code và cấu hình FlashTicket (RabbitMQ binding, repository, HTTP client) để đề xuất cạnh | Bổ sung hợp đồng tĩnh P5; tăng cạnh dữ liệu và thông điệp | Mọi cạnh phải được trace xác nhận hoặc gắn nhãn "tĩnh, chưa quan sát"; so với P5 |
| L3 | Cảnh báo | Soạn nháp luật cảnh báo và SLO từ hợp đồng API B13 | Đỡ công viết luật | Người duyệt; không tính là đóng góp phương pháp |
| L4 | Thực nghiệm | Soạn nháp kịch bản tiêm lỗi và sổ chạy | Đỡ công | Người duyệt; không được để nhãn lọt vào RCA |
| L5 | Xếp hạng (nhánh riêng) | Đưa gói bằng chứng có cấu trúc cho LLM, xin top-3 kèm lý do | Trả lời câu "LLM có thay được phương pháp không"; so với Grafana Assistant Investigations | Một nhánh riêng, không trộn vào phương pháp chính; ghim model; nhiệt độ 0; lặp vài lần để đo độ ổn định |
| L6 | Đánh giá P8 | LLM chấm chất lượng lời giải thích, có người chấm hiệu chỉnh trên một mẫu | Đỡ công chấm | Báo mức đồng thuận giữa LLM và người |

**Điều kiện chung:**
- không đưa nhãn, tên ca hay đường dẫn ca vào prompt (luật cứng 6);
- ghim model và phiên bản; lưu cache mọi đầu ra;
- tính chi phí;
- tín dụng Google Cloud không trả được Gemini API trên AI Studio;
- chỉ gửi dữ liệu đã lọc theo B16 §6.

**Ưu tiên:** L1 và L2 trước, vì chúng sửa đúng hạn chế đã thấy và đánh giá được. L5 là thí nghiệm phụ có giá trị trình bày trước hội đồng.

### D.4 Khâu phát hiện (M-12, M-20) [ĐX]

- **Mặc định:** mở sự cố bằng luật cảnh báo Grafana. Phát hiện thành phần bất thường có dùng đồ thị nằm ở bước chẩn đoán (Mô-đun B).
- **Phần nghiên cứu của khâu phát hiện:**
  - chọn ngưỡng từ đoạn bình thường, không dùng nhãn;
  - đo tỷ lệ phát hiện trong hạn D, số báo động giả mỗi giờ trên đoạn bình thường, độ trễ;
  - báo loại lỗi nào bắt được, loại nào không;
  - gom cảnh báo thành sự cố.
- **Trả lời M-20:** đúng vậy. "Đồ thị tham gia quyết định báo động" là một hướng phương pháp khác, dự phòng hoặc mở rộng cho bộ luật Grafana. Có hai biến thể:
  - **G:** điểm hệ thống tính từ điểm thành phần trên đồ thị.
  - **H:** luật mở sự cố như mặc định; đồ thị gộp hoặc nén các cảnh báo cùng được giải thích bởi một nguyên nhân phía dưới. Dynatrace cũng gộp các sự kiện thuộc cùng một đồ thị nhân quả thành một sự cố [TL].
  - Cả hai **hoãn tới khi có ý kiến cô** (M-20).
- **RE2-TT chế độ (b):** chỉ phát lại những luật có tín hiệu tương ứng. BOCPD và N-Sigma chỉ còn là baseline lịch sử của P3.

#### D.4.1 Phát hiện dùng đồ thị có tách biệt với phương pháp RCA không? (trả lời M-28)

- Chuỗi giám sát trả lời hai câu hỏi:
  1. **Khi nào có sự cố:** quyết định báo động.
  2. **Cái gì gây ra:** chẩn đoán và xếp hạng.
- Phương pháp RCA (D.2) dùng đồ thị cho câu hỏi 2. Trong đó, Mô-đun B đã là một phép **phát hiện bất thường trên đồ thị ở mức thành phần**: thành phần nào bất thường, và bất thường đó tự sinh hay kế thừa từ thành phần phía dưới.
- "Đồ thị tham gia quyết định báo động" (nhánh G, H) là dùng chính các điểm của Mô-đun A, B cho thêm câu hỏi 1:
  - **G:** tính điểm liên tục theo chu kỳ; điểm vượt ngưỡng thì báo động.
  - **H:** luật Grafana vẫn mở sự cố; đồ thị gộp các cảnh báo cùng được giải thích bởi một nguyên nhân phía dưới.
- **Vì vậy nhánh này không tách biệt.** Nó dùng chung Mô-đun A, B với phương pháp RCA. Phần phải làm thêm:
  - chạy liên tục (online);
  - chọn ngưỡng trên đoạn bình thường;
  - đo chất lượng báo động (báo giả mỗi giờ, độ trễ, bỏ sót);
  - so với bộ luật Grafana.
- **C-01 đề xuất:**
  - Câu hỏi 1 mặc định do luật Grafana trả lời.
  - Đồ thị dùng cho câu hỏi 2, gồm cả phát hiện bất thường ở mức thành phần.
  - Nhánh G, H để sau.
- **Vì không gửi câu hỏi cho cô (M-36),** nhánh G, H sẽ chỉ được kích hoạt nếu cô tự nhận xét, hoặc Minh tự quyết. Đề xuất: ghi G, H là việc tầng 3, Minh quyết làm hay không sau khi phương pháp RCA đã chạy trên dev. H rẻ hơn G vì dùng lại Mô-đun B.
- **Rủi ro khi bảo vệ:** hội đồng có thể hỏi "đồ thị phát hiện bất thường ở đâu". Trả lời bằng Mô-đun B (mức thành phần). Nếu làm H thì có thêm phần đồ thị gộp cảnh báo.

### D.5 Đối chứng (M-19): ý kiến độc lập

| Mã | Đối chứng | Đề xuất | Lý do |
|---|---|---|---|
| C-a | Cùng tín hiệu, gán cho service sở hữu span, không dùng quan hệ | Giữ (Minh đồng ý) | Tách lợi ích của tín hiệu khỏi lợi ích của quan hệ |
| C-d | Quy tắc đơn giản trên cùng đồ thị (sâu nhất, sớm nhất) | Giữ (Minh đồng ý) | Cách phức tạp có hơn quy tắc đơn giản không |
| C-e | Chạy ở mốc giả không có lỗi | Giữ (Minh đồng ý) | Phương pháp có tự "nghi" một dịch vụ cố định không |
| C-f | Service Graph, Knowledge Graph, Assistant của Grafana | Giữ (Minh đồng ý); mở rộng sang Grafana Cloud (D.8.2) | Tham chiếu công nghiệp, so định tính |
| C-b | Đồ thị ngẫu nhiên giữ bậc | **Bỏ** (Minh quyết, M-25). Kết luận ghi là "lợi ích của bước lan", không phải "lợi ích của cấu trúc phụ thuộc thật" | Đề xuất trước đó (giữ hẹp) và lý do giữ lại dưới đây làm lịch sử |
| C-c | Gộp hạng của các baseline không dùng đồ thị (ví dụ reciprocal rank fusion) | **Giữ** (Minh quyết, M-26) | Lý do ở dưới |

**C-b (lịch sử; Minh đã quyết bỏ theo M-25):** đề xuất của Claude trước khi Minh quyết. Giữ lại để phiên sau biết lý do và giới hạn kết luận đi kèm.

**C-b: Minh đúng một phần.**
- Với các mô-đun chỉ dùng quan hệ cha–con của span (E1, E2), xáo trộn không có nghĩa, vì nó chỉ gán thời gian cho sai bên. Ở đây C-a là đủ.
- Với các mô-đun lan điểm trên đồ thị dịch vụ (E5, E6b, E7), C-b trả lời được một câu mà C-a không trả lời được: cấu trúc phụ thuộc cụ thể có giúp không, hay đồ thị nào có cùng bậc cũng cho kết quả như vậy?
- Repo đã có tiền lệ: ở v1, đồ thị ngẫu nhiên gây đúng thiệt hại như đồ thị thật ở các ca xấu nhất (WHY-07, LESSONS ST5). Phép này từng phát hiện ra rằng thiệt hại đến từ cách lan, không đến từ cấu trúc.
- Chi phí thấp: một phép biến đổi đồ thị và chạy lại mô-đun rẻ.
- Trên RE2-TT, đồ thị nhỏ và gần như không đổi (30 ca dev chỉ có 2 đồ thị khác nhau; auth không có cạnh — LESSONS ST3), nên phép này ít thông tin ở đó. Chỉ làm trên Nezha-OB và FlashTicket.
- Nếu Minh vẫn muốn bỏ: viết kết luận là "lợi ích của bước lan", không phải "lợi ích của cấu trúc phụ thuộc thật".

**C-c có lợi gì:**
- Phương pháp hợp nhất gộp nhiều nguồn: metric, log, trace. Hội đồng có thể hỏi: chỉ gộp kết quả của các phương pháp có sẵn thì có được như vậy không? C-c trả lời câu đó.
- Chi phí gần như bằng 0: tính từ thứ hạng P3 đã lưu, không chạy lại.
- Nếu dùng E6(c) hoặc dùng điểm baseline làm đầu vào thì C-c là bắt buộc. Nếu không, C-c là tùy chọn.

### D.6 Độ đo và thống kê

- **Mọi độ đo đều được tính và báo** (M-07). "Độ đo chính" dùng ở ba chỗ:
  - chọn giữa các biến thể trên dev;
  - câu kết luận chính;
  - phép kiểm thống kê chính.
- **Ví dụ các độ đo cho kết quả ngược nhau** ([REPO] `bang-baseline.json`):
  - Nezha-OB: BARO hơn SimpleRCA theo Hit@1 (0,364 so với 0,318), nhưng thua theo Hit@3 (0,545 so với 0,682) và MRR (0,527 so với 0,538).
  - RE2-TT: CIRCA thua BARO theo Hit@1 (0,533 so với 0,700), nhưng hơn theo Hit@5 (0,900 so với 0,867).
- **Xếp hạng:**
  - Độ đo chính đề xuất là MRR (C-08): có trong danh sách của cô; MRP P6 đã khai từ trước; dùng toàn bộ thứ hạng.
  - Báo kèm: Hit@1, Hit@3, Hit@5, NDCG@5, AC@k, Avg@5, hạng của root ở từng ca, số ca thắng/hòa/thua theo cặp, mức ngẫu nhiên.
  - Hit@3 chạm trần ở RE2-TT (TORAI B = 1,0) và che đúng lỗi "root ở hạng 2" mà thiết kế muốn sửa. Không dùng làm độ đo chính, nhưng vẫn báo vì hợp với cách người vận hành đọc kết quả (top-3).
- **Mức ngẫu nhiên** [TÍNH]:

  | Số ứng viên N | MRR ngẫu nhiên | Hit@3 ngẫu nhiên |
  |---|---|---|
  | 10 | 0,293 | 0,300 |
  | 20 | 0,180 | 0,150 |
  | 68 | 0,071 | 0,044 |

- **Sức phân biệt thống kê** [TÍNH, McNemar chính xác hai phía, chỉ đếm các ca hai phương pháp cho kết quả khác nhau]:

  | Thắng | Thua | p |
  |---|---|---|
  | 4 | 0 | 0,125 |
  | 6 | 0 | 0,031 |
  | 8 | 1 | 0,039 |
  | 8 | 2 | 0,109 |
  | 10 | 3 | 0,092 |

  TORAI B chỉ trượt 4/30 ca RE2-TT dev. Vì vậy trên RE2-TT dev **không thể** chứng minh "hơn" có ý nghĩa thống kê. Đây là lý do của biên Δ (D.1).
- **Phép thống kê:**
  - McNemar cho Hit@1;
  - kiểm định hoán vị hoặc Wilcoxon trên nghịch đảo hạng;
  - khoảng tin cậy bootstrap theo ô (Q-74 Q10);
  - khoảng tin cậy chứa 0 thì ghi "chưa phân biệt được";
  - có gộp các bộ dữ liệu theo tầng hay không: khai trong giao thức.
- **Phát hiện:**
  - Cặp số chính: tỷ lệ phát hiện trong hạn D (tách theo loại lỗi) và số báo động giả mỗi giờ trên đoạn bình thường. Kèm độ trễ.
  - Precision, Recall, F1 theo cửa sổ: báo vì cô yêu cầu.
  - Quy tắc ba: không có báo động nào trong T giờ thì cận trên 95% ≈ 3/T mỗi giờ. Chạy nền 10 giờ cho 0,3/giờ; 30 giờ cho 0,1/giờ [TÍNH]. Độ dài chạy nền chọn theo khẳng định nhóm muốn đưa ra.
- **Khoanh vùng:**
  - Dữ liệu công khai: vùng có chứa root không, vùng rộng bao nhiêu.
  - FlashTicket: Precision, Recall, F1 so với nhãn vùng độc lập.
- **Cả chuỗi:**
  - Thành công ở k: phát hiện trong hạn D và root nằm trong top-k ở đúng lần RCA đó.
  - Thời gian từ lúc lỗi tới lúc có kết quả.
  - Số lần RCA chạy cho mỗi sự cố.
- **Cỡ mẫu FlashTicket** [TÍNH, với p ≈ 0,7 và các ca độc lập]: sai số ±0,10 cần khoảng 81 sự cố; ±0,15 cần khoảng 36.

### D.7 Nguồn cần đọc trước khi thiết kế

Mỗi bài một thẻ một trang: cơ chế; đầu vào; dữ liệu nhóm có hay thiếu; điều kiện thất bại theo bảy bài học; ý tưởng lấy được.

Đọc theo thứ tự:
1. CRISP.
2. MicroHECL.
3. PAL và FChain, bản gốc.
4. Budhathoki và cộng sự (ICML 2022); Sage.
5. MonitorRank; Murphy (SIGCOMM 2023).
6. Phương pháp Nezha và Eadro.
7. Groot; tài liệu Dynatrace Davis.
8. LILAC; RCACopilot; OpenRCA (cho D.3).
9. Tài liệu Grafana Knowledge Graph và RCA Workbench.
10. LagRCA: chỉ khi giữ hướng E9.
11. ART và thống kê quét CNSS: chỉ khi kích hoạt nhánh G hoặc H.
12. Bài RCAEval và bài SimpleRCA FSE 2026: để thống nhất cách tính độ đo.

### D.8 Hạ tầng

#### D.8.1 Kiến trúc lai: Grafana tự cài làm chính, Grafana Cloud làm bản sao (M-16) [ĐX]

```
Ứng dụng: FlashTicket (hoặc OTel Demo) + Java agent
  Toxiproxy đặt trước DB, Redis, RabbitMQ, mock VNPay; Pumba
        │ OTLP
        ▼
OTel Collector (B16; có thể dùng Alloy ở chế độ chạy YAML của Collector)
  trace: spanmetrics + servicegraph (trước khi lấy mẫu) → tail sampling
          → Tempo tự cài + file cho RCA + Grafana Cloud (đã lọc)
  metric → Prometheus tự cài + Grafana Cloud (dưới 10.000 chuỗi)
  log    → Loki tự cài + Grafana Cloud (chỉ log lỗi)
        │
        ├─ Tự cài: Tempo, Loki, Prometheus, Grafana   → thực nghiệm, chấm điểm, demo chính
        └─ Grafana Cloud                              → Knowledge Graph, Assistant, Synthetics, k6, IRM
Dịch vụ RCA đọc kho tự cài → JSON, annotation lên Grafana tự cài
```

- Collector gửi được cùng lúc tới hai đích: một exporter `otlphttp` có xác thực `basicauth` cho Grafana Cloud, cộng exporter cho kho tự cài, liệt kê cả hai trong từng pipeline [TL Grafana].
- Kho tự cài là nguồn chấm điểm, vì nhóm kiểm soát toàn bộ dữ liệu.
- Grafana Cloud chỉ làm bản sao, để demo và để so định tính.

#### D.8.2 Tận dụng Grafana Cloud

| Tính năng | Dùng để | Hạn mức gói Free [TL] | Lưu ý |
|---|---|---|---|
| Knowledge Graph, RCA Workbench | Đối chứng công nghiệp trên cùng sự cố FlashTicket: Workbench có chỉ tới root không | Có trong mọi stack. Cần Application Observability và metric service graph. Metric phát sinh thêm 5–10% | Tài liệu không nói rõ cho host Docker không chạy Kubernetes (chưa kiểm). So định tính, vì đầu ra khác dạng |
| Assistant Investigations | Đối chứng LLM công nghiệp cho P8 và L5 | 3 người dùng AI, mỗi người 40 triệu token; 25 triệu token cho lượt tự động | Kết quả không ổn định giữa các lần chạy (DE-XUAT §2.2); lặp nhiều lần |
| Synthetic Monitoring | Đo phía người dùng, độc lập với RCA, làm nhãn vùng và SLO; dùng trong demo | 100.000 lượt API, 10.000 lượt trình duyệt mỗi tháng | Cần endpoint công khai; bảo mật |
| k6 Cloud | Tạo tải đột biến từ bên ngoài cho demo flash sale | 500 VU-giờ | Phí truyền dữ liệu của EC2: chưa kiểm |
| Sift, forecast, outlier | Thử ML có sẵn | Miễn phí | Sift thiên về Kubernetes, nhiều kiểm tra sẽ không chạy trên Docker/EC2 |
| IRM, OnCall | Demo định tuyến cảnh báo | 3 người dùng | — |

**Giới hạn và cách xử lý:**
- 10.000 chuỗi metric là ít, vì ước tính ở D.8.5 là khoảng 15.000 → chỉ gửi RED và vài metric chính.
- 50 GB trace mỗi tháng → gửi trace đã lấy mẫu.
- Lưu 14 ngày.
- Gói Free ghi "không tính tiền"; khi vượt hạn mức thì xử lý thế nào chưa kiểm.
- Demo phụ thuộc mạng và bên thứ ba → luôn có bản tự cài và bản phát lại offline.

#### D.8.3 Lộ trình từng bước, cho người chưa có kinh nghiệm

| Bước | Làm gì | Trả lời câu hỏi nào | Ở đâu | Qua khi | Nếu không qua |
|---|---|---|---|---|---|
| H0 | Ghim phiên bản (Tempo 3.x). Kiểm kích thước image. Giới hạn RAM WSL (sửa `.wslconfig`, file ngoài repo, cần duyệt). Tắt chế độ ngủ | Chuẩn bị | Laptop | Có danh sách phiên bản và dung lượng | — |
| H1 | `otel-lgtm` cùng gateway và một service khung FlashTicket có Java agent | Agent có chạy với Spring Boot 4.1.1 không; span có kind và route không; log có trace_id không; Micrometer có lên Prometheus không | Laptop | Đủ bốn điều | Thử `spring-boot-starter-opentelemetry` (đổi B16, cần nhóm hệ thống đồng ý) |
| H2 | OTel Demo với Collector theo DE-XUAT §4 | RAM, CPU; số byte mỗi giờ ở 2–3 mức tải; chỉ số mất dữ liệu ở cổng 8888 | Laptop nếu trơn tru (M-08) | Chạy 1 giờ: không container nào bị dừng vì hết bộ nhớ hay tự khởi động lại; RAM trống ≥ 20%; Collector không báo bỏ span; CPU trung bình < 80%; đạt tải đặt | Lên cloud |
| H3 | Luật cảnh báo, dịch vụ nhận webhook, gom đợt sự cố; bật cờ `paymentFailure`, `intlShippingSlowdown`, `kafkaQueueProblems` | Độ trễ cảnh báo; số thông báo mỗi sự cố | Laptop hoặc cloud | Đo được | Chỉnh luật |
| H4 | Adapter OTLP→P5; Node graph qua Infinity | Giao diện có làm được không | Như trên | Hiện được đồ thị | Sửa adapter, đổi panel |
| H5 | Lên EC2 theo D.8.4; chrony với Amazon Time Sync [TL]; security group chỉ mở cho IP của Minh; dung lượng ổ theo D.8.5 | Máy 8 GiB có đủ không | AWS | Chạy ổn 1 giờ | Thêm máy riêng cho bộ quan sát |
| H6 | Bộ chạy chiến dịch: lịch tiêm lỗi, sổ thực nghiệm, xuất gói chấm lại, checksum; chạy qua đêm | Tự động hóa | Cloud | Chạy thử một đêm đạt | Sửa script |
| H7 | Gửi song song lên Grafana Cloud; bật Knowledge Graph và Synthetics | Tận dụng Cloud | Cloud | Thấy entity graph | Chỉ dùng kho tự cài |

- **Các bước dài chạy trên cloud.** Lý do: laptop có thể ngủ, tự cập nhật và khởi động lại, đồng hồ có thể lệch.
- **Hạ tầng cũng là phần việc của Minh bên hệ thống.** `roles.md` ghi Minh phụ trách observability baseline và hạ tầng local, nên kết quả H0–H7 dùng được cho báo cáo hệ thống (NV1).

#### D.8.4 Tài khoản, quota, bố trí (M-17) [ĐX]

- **Quota mặc định 5 vCPU mỗi vùng** → mỗi tài khoản chạy tối đa 2 máy m7i-flex.large trong một vùng [TL].
  - Việc đầu tiên: xem trang Service Quotas của từng tài khoản (chỉ đọc).
  - Xin tăng nếu cần. Có người báo tài khoản mới bị từ chối (chưa kiểm).
- **Bố trí đề xuất:**
  - **Tài khoản A:** 2 máy FlashTicket theo thiết kế đích.
  - **Tài khoản B:** máy bộ quan sát và RCA nếu EC2 #2 thiếu RAM; máy chạy batch P7 (BOCPD khoảng 4,7 giờ cho 60 ca test [TÍNH]).
  - **Tài khoản C:** máy sinh tải.
  - **Tài khoản D:** dự phòng, và thay thế nếu một tài khoản hết tín dụng.
- **Nối mạng giữa hai tài khoản:**
  - VPC peering giữa hai tài khoản có trong gói Free không: chưa kiểm.
  - Nếu không có, dùng IP công khai, bắt buộc TLS và xác thực cho OTLP.
  - Lượt chạy chính thức của FlashTicket vẫn nên đặt trong một tài khoản (`aws-runtime-baseline.md` §3).
- **Google Cloud (M-33):**
  - AWS hiện đủ dùng.
  - Mở Google Cloud khi cần tải nặng.
  - Nâng AWS lên gói Paid khi cần.
  - **Lưu ý:** máy mạnh hơn m7i-flex.large trên Google Cloud đến từ **tín dụng dùng thử 300 USD** (90 ngày tính từ lúc đăng ký, trong quota dùng thử; quota chưa kiểm). Gói luôn miễn phí của Google Cloud chỉ có một máy e2-micro rất yếu. Vì vậy chỉ đăng ký khi sắp cần dùng.
  - Không đặt một nửa thực nghiệm ở cloud khác.
- **Gói Free:** không tiêu vượt tín dụng được. Hết tín dụng là đóng tài khoản. Phải xem ngày mở và số dư của từng tài khoản (E-08).

#### D.8.5 Dung lượng [TÍNH]

Giả định: mỗi request 10 span; mỗi span 450 B (suy từ tài liệu Tempo); mỗi request 3 dòng log × 400 B; 15.000 chuỗi metric, mỗi mẫu 1–2 B.

| Tải | Trace giữ 100% | Trace giữ khoảng 12% | Log thô | Metric |
|---|---|---|---|---|
| 20 rps | 0,32 GB/giờ | 0,04 | 0,09 | 4–7 MB/giờ |
| 100 rps | 1,6 | 0,19 | 0,43 | như trên |
| 500 rps | 8,1 | 0,97 | 2,2 | như trên |

- Khi đã lấy mẫu trace, log chiếm nhiều chỗ nhất.
- Cách giới hạn:
  - tail sampling, với spanmetrics chạy trước bước lấy mẫu;
  - lọc trace health check;
  - giảm thời hạn lưu của Tempo; bật retention cho Loki; đặt `retention.size` cho Prometheus;
  - mỗi lượt chỉ xuất gói đủ để chấm lại.
- Bộ ghi file cho RCA xoay vòng tối đa khoảng 10 GB, nên ở tải cao chỉ giữ được chưa tới khoảng 1 giờ.

#### D.8.6 Chi phí [TÍNH]

- Một máy 0,1197 USD/giờ (`tasks/T-005-do-kha-thi/LOG.md:168`), chạy liên tục khoảng 86 USD/tháng.
- Hai máy cộng 150 GB ổ khoảng 184 USD/tháng, tức gần hết tín dụng của một tài khoản trong một tháng.
- Tắt máy khi không chạy. Chiến dịch chạy theo đợt.
- Phí IPv4 công khai và phí truyền dữ liệu: chưa kiểm.

#### D.8.7 Những chỗ dễ vỡ

1. **Spring Boot 4 và agent:** xử lý ở H1.
2. **Overhead của agent:** tài liệu không đưa số. Kết quả kiểm thử tải NV1 phải ghi rõ có bật agent không, hoặc chạy cả hai trường hợp.
3. **Lấy mẫu mâu thuẫn với kiểm thử tải:** chiến dịch RCA chạy ở tải vừa, giữ 100% trace; lượt NV1 tải cao có lấy mẫu.
4. **Đồng hồ:** chrony cho các EC2.
5. **Giám sát chính bộ giám sát:** các chỉ số ở cổng 8888, chuỗi `up`, ổ đĩa.
6. **Bảo mật:** Grafana và các cổng khác không mở ra internet, truy cập qua SSH tunnel; khóa để ngoài repo; log tuân theo B16 §6.
7. **Tempo 3.x khác 2.9:** đối chiếu lại các khẳng định của DE-XUAT theo bản đã ghim.
8. **Dữ liệu Docker trên laptop nằm ở ổ C.**
9. **Sao lưu trước khi tài khoản hết hạn.**

### D.9 FlashTicket (P10)

**Yêu cầu gửi nhóm hệ thống ngay** (Minh gửi; bổ sung cho R-01…R-10 của P9a):
- (a) B16 từ lát cắt đầu: gắn Java agent; log JSON có trace_id; Micrometer; `hostId`.
- (b) Cờ bật lỗi trong code, chỉ ở môi trường dev, cần quyền quản trị mới bật: ném lỗi hoặc thêm trễ ở một số thao tác đã chọn. Lý do: Chaos Monkey for Spring Boot chưa xác nhận chạy được với Boot 4.
- (c) Chuỗi kết nối cấu hình được để đi qua Toxiproxy.
- (d) Mock VNPay.
- (e) Docker compose cho từng máy, tên container cố định.
- (f) Dùng chung kịch bản k6 với NV1.
- (g) Có endpoint health.

**Ba chặng và hai đợt FlashTicket** [ĐX; Q-197; chi tiết hợp đồng ở B1.9 của `tasks/T-043-thiet-ke-rca-m1/SPEC.md`]:
1. **Lõi trên dữ liệu công khai:** thử và chọn trên dev; khóa bản dùng cho P7.
2. **Phát triển chuyển giao** trên OTel Demo và FlashTicket dev: phần dùng thông tin phong phú (kiểu span, DB/cache/pool, thông điệp, máy, nối log–span, siêu dữ liệu thu), hiệu chỉnh tham số theo tải, ứng viên LLM ở khâu giữa.
3. **Đánh giá** trên phần FlashTicket dành riêng, bằng các lượt mới sau khi khóa.
- Có hai bản được ghi rõ: bản P7 và bản FlashTicket. Kết quả P7 chỉ nói về bản P7.
- **Chia đợt theo ô** (thành phần gốc × loại lỗi), như MRP §4 và WHY-04. Với mỗi họ lỗi, liệt kê các vị trí hợp lệ; đợt phát triển dùng một vị trí, đợt đánh giá dùng vị trí khác.
- Họ lỗi chỉ có một vị trí hợp lệ (ví dụ một số lỗi Saga) thì khai trước: chỉ đánh giá, tức chưa thấy khi thiết kế; hoặc ghi riêng giới hạn. **Phương án đặt các lần lặp của cùng một ô ở cả hai phía trái MRP §4 và WHY-04. Phương án này để OPEN; chỉ dùng khi Minh duyệt ngoại lệ, hoặc duyệt đoạn sửa hai nguồn đó.**
- Báo riêng ba câu hỏi: chuyển sang vị trí lỗi mới; chịu được điều kiện khác đã khai trước (tải, cường độ, cách triển khai); lặp lại được trên tình huống đã phát triển.
- **Đợt phát triển phải có:** tải tăng mà hệ khỏe; lỗi khi tải giữ nguyên; cùng lỗi đó dưới tải khác; các lượt chạy nền để kiểm ngưỡng và trạng thái quan sát.
- **Trước các lượt dùng để kết luận:** kiểm chất lượng telemetry xuyên suốt ứng dụng → exporter → collector → kho → dữ liệu RCA đọc được, ở tải thấp và tải dự kiến, nối với R-01–R-10 và B16.
- **LLM ở khâu giữa:** đánh giá ở chặng 2 (gom mẫu log; đề xuất cạnh tĩnh); so với Drain và quy tắc trên cùng dữ liệu; có nhánh bỏ LLM, cache, ngân sách riêng; quyết giữ hay bỏ trước khi khóa bản FlashTicket. Cần đoạn sửa MRP P8 theo C-05 (chưa soạn).
- **Chi phí đợt phát triển:** OPEN, vì chưa có số ô, số lượt và thời lượng. Duyệt văn bản không cấp quyền chạy chiến dịch.

**Danh mục kịch bản (khai trước, gồm cả kịch bản đồ thị không có lợi thế):**

| Kịch bản | Cách tạo | Đáp án | Kiểm điều gì |
|---|---|---|---|
| Đường truy cập DB của Booking chậm | Toxiproxy | Cạnh Booking→DB | Bài học 1; cạnh dữ liệu |
| Cạn pool kết nối hoặc mất DB | Toxiproxy | Cạnh Booking→DB | Bài học 2 |
| Redis chậm | Toxiproxy | Cạnh tới Redis | Cạnh dữ liệu |
| Consumer phát vé dừng | Pumba pause | ticket-service | Cạnh thông điệp; Bài học 5 |
| Thao tác trả lỗi 5xx | Cờ trong code | Service đó | Bài học 2 |
| Thao tác chậm bên trong | Cờ trong code | Service đó | Đối chứng với dòng đầu |
| Trễ mạng giữa hai service | Pumba netem | Cạnh A→B | Bài học 1 |
| Cạn CPU | Pumba stress | Service đó | Bài học 6 (các service cùng máy) |
| VNPay chậm | Toxiproxy | Cạnh Payment→VNPay | Phụ thuộc ngoài |
| Saga phải bù trừ | Cờ lỗi khi phát vé | ticket-service | Luồng bất đồng bộ |
| Flash sale, không có lỗi | k6 tăng tải đột biến | Không có root | Báo động giả; câu phụ của RQ5 |

- Cột "Đáp án" ở bảng trên là vị trí tiêm. SPEC P10 tách ba trường: vị trí tiêm; cơ chế; đáp án mà telemetry phân biệt được, kèm số đo xác nhận can thiệp. Ví dụ "đường DB chậm" và "cạn pool hoặc mất DB" phải là các can thiệp tách riêng vào pool, DB và đường mạng. Thiếu quan sát thì ghi giới hạn; không đổi nhãn thật.

**Luật chống thiên lệch "hệ thống tự thiết kế"** (bắt buộc theo M-24; để mục tiêu M-18 bảo vệ được trước hội đồng):
1. Khai danh mục kịch bản và quy tắc nhãn trước khi chạy.
2. Các baseline chạy trên cùng dữ liệu, qua adapter xuất sang định dạng của chúng (C-06). Baseline không chạy được thì ghi UNSUPPORTED.
3. Áp cho đợt đánh giá: không đổi phương pháp sau khi xem kết quả của đợt này; lần lặp đầu chỉ để sửa lỗi cài đặt. Code, cấu hình, phiên bản và LLM (nếu có) khóa trước đợt đánh giá. Sửa sau đánh giá theo hướng B (C-15) phải ghi rõ đã dùng dữ liệu đánh giá để thiết kế, và cần lượt mới để kiểm. Đợt phát triển được phép chỉnh.
4. Báo kết quả theo từng kịch bản, kể cả kịch bản thua.
5. Có ablation "phương pháp bỏ cạnh có kiểu" để thấy phần lợi ích đến từ lợi thế thông tin.

**Nhãn:**
- Root theo quy tắc khai trước. Mốc tiêm lấy từ log của công cụ tiêm lỗi, ghi vào sổ thực nghiệm. RCA không đọc sổ này (luật cứng 6).
- Đoạn bình thường theo DE-XUAT §5.6.
- Vùng ảnh hưởng lấy từ số đo phía người dùng của k6 hoặc Synthetics, tức tín hiệu RCA không dùng. Số đo này chỉ ở mức endpoint. Vì vậy: hoặc đo độc lập ở từng thành phần, hoặc đưa cả dự đoán lẫn nhãn về mức endpoint và gọi đúng là "ảnh hưởng endpoint".
- Nhãn là cạnh: khai trước tập đáp án chấp nhận cho mọi phương pháp, cộng một bảng định vị cạnh riêng. Báo riêng điểm xác định đúng nguyên nhân theo nhãn thật và điểm định vị theo tập đáp án chấp nhận; không gọi điểm thứ hai là xác định đúng nguyên nhân.

**Cỡ chiến dịch** [TÍNH]:
- Khoảng 20 ô × 3 lần lặp ≈ 60 sự cố; mỗi chu kỳ khoảng 30 phút.
- Cộng 10–30 giờ chạy nền, tổng 40–60 giờ máy, tức 3–4 đêm.
- Dự toán này là cho đợt đánh giá, chưa gồm đợt phát triển (chi phí OPEN).

### D.10 OpenTelemetry Demo

| | RE2-TT, Nezha-OB | OTel Demo |
|---|---|---|
| Bản chất | Dữ liệu đã ghi sẵn, tác giả công bố nhãn | Hệ thống chạy được; nhóm tự sinh và tự ghi dữ liệu |
| Trace | Không có kind, không có thuộc tính DB/thông điệp | Dự kiến có kind, DB, Kafka (phải kiểm) |
| Lỗi | Tài nguyên, mạng; lỗi trả về ở Nezha | 19 cờ, mỗi cờ gắn sẵn với một service |

- **Dùng cho:** chạy thử hạ tầng; kiểm những gì dữ liệu công khai không có; viết adapter và dịch vụ RCA online trước khi có FlashTicket.
- **Giới hạn:**
  - không độc lập với nhóm;
  - có thể quá dễ, vì lỗi được viết vào code để minh họa;
  - đáp án của vài cờ không rõ;
  - ít service Java;
  - không đi kèm Tempo, Loki.
- **Không đưa vào bảng so sánh chính** (C-07).

### D.11 P7, P8, demo, quyển, bảo vệ

- **P7:**
  - Chạy test một lần sau G3: 60 ca RE2-TT, phần test của Nezha-OB, RE3-OB.
  - Kiểm dung lượng RE3-OB qua metadata (chỉ đọc) rồi tải khi Minh duyệt.
  - RE3-OB là lỗi mã nguồn; hai root ad và cart có thể thiếu nút trong trace (T-002:498).
- **P8:** LLM giải thích dựa trên gói bằng chứng; kiểm tự động mức trung thành với bằng chứng; so với Grafana Assistant. Thêm L1, L2 nếu Minh duyệt C-05.
- **Demo:**
  - phần phát hiện được demo ngang với phần RCA (Q-28);
  - kịch bản có script;
  - video dự phòng;
  - chế độ phát lại offline: RCA đọc gói dữ liệu đã lưu;
  - Grafana Cloud làm bản sao.
- **Quyển:**
  - mục "mối đe dọa đến tính hợp lệ": nội tại, ngoại tại, cách đo;
  - một mục chuẩn bị câu hỏi hội đồng, ví dụ "SimpleRCA đã 83% thì cần đồ thị làm gì", "hệ tự thiết kế có thiên vị không", "LLM có bịa không";
  - Minh tự biên tập, vì cô từng nhận xét bản trước có vẻ do AI viết và còn mơ hồ;
  - gộp báo cáo hệ thống và báo cáo RCA;
  - kiểm license của dữ liệu và công cụ.

### D.12 Thứ tự công việc theo phụ thuộc

Không lấy giờ làm lý do cắt phạm vi (M-15). Ngày cố định duy nhất là nộp quyển 30/12. Chưa có ngày bảo vệ; ưu tiên làm đúng kế hoạch trước (M-34). Mốc G3, G4 mới Minh đặt sau (C-04).

| Giai đoạn | Việc | Vào khi | Ra khi |
|---|---|---|---|
| S0 | Nhóm việc A ở Phần F; SPEC T-042; H0–H2; gửi yêu cầu cho nhóm hệ thống; thẻ đọc | Ngay | Có số đo hạ tầng; Minh quyết C-xx và D1–D12 |
| S1 | SPEC M1: thiết kế hợp nhất và giao thức | Thiết kế RCA: không chờ thư cô (Q-187). Phần phát hiện G/H: thư cô hoặc Minh tự quyết | SPEC được duyệt |
| S2 | Lượt thử E1–E4 trên dev; H3–H4 | S1 | Giữ hoặc bỏ từng thành phần |
| S3 | E5–E7, đối chứng; L1, L2 nếu duyệt; H5–H7 | S2 | Thiết kế ứng viên chạy được |
| S4 | Ma trận dev đầy đủ, phân tích, chọn; hồ sơ G3 | S3 | Minh duyệt G3 |
| S5 | P7: chạy test một lần; G4 | S4 | Bảng kết quả |
| S6a | Phát triển chuyển giao: OTel Demo và FlashTicket dev; phần thông tin phong phú, hiệu chỉnh theo tải, ứng viên LLM ở khâu giữa; kiểm chất lượng telemetry | S4 xong; OTel Demo từ S2; FlashTicket dev khi chạy được luồng chính (M-06) | Bản FlashTicket khóa |
| S6b | P10: đợt đánh giá FlashTicket, lượt mới sau khóa; P8 | S6a | Kết quả và demo |
| S7 | Quyển, slide, video | Song song từ S4 | Nộp 30/12 |

**Song song:** nhánh hạ tầng (H) chạy cùng S1–S5; S6a chuẩn bị trên OTel Demo từ S2.

### D.13 Cách làm việc

- **Song song giữa các agent:** nhánh R (phương pháp) và nhánh H (hạ tầng) độc lập, giao cho hai agent khác nhau.
- **Nút thắt thật là việc duyệt của Minh và thời gian máy, không phải tốc độ agent.** Mua thêm tài khoản agent giúp phần agent nhanh hơn, nhưng không giúp hai thứ này. Đề xuất C-11 (duyệt theo ngân sách trong SPEC) và gom các quyết định vào một lượt.
- **Phản biện:** chính thức ở G3 và ở các SPEC chính (M1, T-042); các task nhỏ phản biện gọn. Minh quyết (E-07).

### D.14 PLAN-P6: giữ, gộp, hoãn

- **Giữ:** M1 (tách thành giao thức, thiết kế, phát hiện) và M13.
- **Gộp:** M2 với C1; M3 thu hẹp; M4 với phần vùng của M5 và M7 (M7 bỏ đồ thị ngẫu nhiên, chỉ còn nhánh bỏ quan hệ và đồ thị tĩnh có điều kiện; M-25); M8 vào task chạy; M9 với M10; M11 với M12.
- **Hoãn theo cô (M-20):** phần phát hiện của M5, M6, C8, C9, C12, C15, C13, C14.
- **Hoãn có điều kiện:** C2–C7, C10, C11.
- **Thêm:** D.2 (phương pháp hợp nhất), D.3 (L1, L2, L5), D.8 (H0–H7), D.9 (FlashTicket), C-c.

### D.15 Rủi ro

| Rủi ro | Dấu hiệu sớm | Phương án dự phòng |
|---|---|---|
| FlashTicket trễ | Đã xong S4 mà luồng đặt vé chưa chạy với agent | P10 trên phần đã chạy được, cộng OTel Demo; thu nhỏ danh mục kịch bản |
| Phương pháp không hơn baseline | E1–E6 bị bác bỏ | Trình bày theo tầng 1; phân tích "khi nào đồ thị giúp" |
| Thua trên FlashTicket | Kết quả S6 | Báo trung thực (Q-04); phân tích kịch bản thua; ablation |
| Cô yêu cầu đồ thị trong phát hiện | Thư trả lời | Kích hoạt nhánh G hoặc H, dùng lại Mô-đun B |
| Agent không chạy với Boot 4 | H1 thất bại | Dùng starter của Spring (cần nhóm hệ thống đồng ý) |
| Quota vCPU chặn | Service Quotas | Xin tăng; chia tài khoản; dùng Google Cloud |
| Hết tín dụng, tài khoản bị đóng | Số dư dưới 20% | Tắt máy; chuyển tài khoản |
| EC2 #2 thiếu RAM | H5 | Máy riêng cho bộ quan sát |
| Rò nhãn trên FlashTicket | Sổ thực nghiệm lọt vào đầu vào RCA | Tách thư mục và quyền đọc |
| Thử quá nhiều cấu hình trên dev | Vượt số cấu hình đã khai | Khóa ở G3 |
| Demo hỏng khi bảo vệ | — | Video, phát lại offline, bản sao trên Cloud |
| Minh duyệt không kịp | Việc chờ duyệt dồn lại | C-11; gom quyết định |

---

## Phần E. Câu hỏi đang chờ Minh

Gồm cả những chỗ có thể mâu thuẫn (M-21).

| Mã | Câu hỏi | Vì sao hỏi |
|---|---|---|
| E-01 | ~~Trên FlashTicket, "phải vượt" là mục tiêu thiết kế hay điều kiện bắt buộc?~~ **Đã trả lời ngày 22/10/2026 (M-24): mục tiêu thiết kế**, kèm năm luật ở D.9; nếu không vượt thì báo trung thực theo Q-04 | Câu hỏi được đặt vì "điều kiện bắt buộc" sẽ trái Q-04, Q-22 và LESSONS SL20 |
| E-02 | ~~Đồ thị ngẫu nhiên: bỏ hẳn, hay giữ hẹp như D.5?~~ **Đã trả lời ngày 22/10/2026 (M-25): bỏ**; kết luận ghi là lợi ích của bước lan | Hệ quả: RQ3d cần sửa (C-02) |
| E-03 | ~~C-c: giữ hay bỏ?~~ **Đã trả lời (M-26): giữ** | — |
| E-04 | ~~Biên Δ trên RE2-TT: Δ_MRR = 0,05; Δ_Hit@1 = 2/30 ca dev, 4/60 ca test (M-27, M-37).~~ **Đã trả lời ngày 23/10/2026 (M-44): duyệt E-04 theo bản sửa KS-07.** Baseline đối chứng TORAI B; kết luận theo vị trí CI; quy tắc điểm ước lượng chỉ báo kèm; Hit@1 chỉ để mô tả; thêm phương án khi không đạt. Xem D.1 | Để định nghĩa "không quá cách biệt" (M-18) |
| E-05 | ~~Đổi MRP P6 ngay hay chờ thư cô?~~ **Đã trả lời (M-38): duyệt C-01** | Nhánh G, H không tách biệt với RCA: dùng chung Mô-đun A, B |
| E-06 | ~~Ngoại lệ AGENTS §9: chỉ lượt này hay thành luật?~~ **Đã trả lời (M-29): chỉ lượt này; prompt vẫn theo mẫu.** C-10 không duyệt | — |
| E-07 | ~~Duyệt các mục C nào?~~ **Đã trả lời (M-30, M-31, M-32, M-38, M-39):** xem bảng C.1. Chính sách phản biện ở D.13 duyệt (M-39). RQ3d của C-02: **sửa câu (M-47)** | Claude đề xuất **sửa câu RQ3d** thành: "Phần thay đổi có đến từ việc dùng quan hệ không, so với nhánh cùng tín hiệu bỏ quan hệ (C-a); và có hơn quy tắc đơn giản trên cùng đồ thị không (C-d)?". Lý do: câu hỏi trả lời được bằng các đối chứng đang giữ, và không để lại một câu hỏi nghiên cứu bỏ trống trong quyển |
| E-08 | ~~Tài khoản, quota, Paid?~~ **Đã trả lời (M-33):** AWS đủ dùng; nâng Paid khi cần; mở Google Cloud khi cần tải nặng. Còn nên làm: xem trang Service Quotas và ngày mở của từng tài khoản (chỉ đọc) | D.8.4 |
| E-09 | ~~Ngày bảo vệ?~~ **Đã trả lời (M-34): chưa có; làm đúng kế hoạch trước.** Mốc FlashTicket chạy được luồng chính: theo M-06 | D.12 |
| E-10 | ~~Cách xử lý T-041?~~ **Đã trả lời (M-35): phản biện đầy đủ; Minh tự mở phiên Claude mới.** Sau đó T-041 đã nghiệm thu và đóng ngày 23/10/2026 (Q-186, M-46); không còn việc phản biện | — |
| E-11 | ~~Grafana Cloud?~~ **Đã trả lời (M-36): dùng, không đắn đo** | D.8.2 |
| E-12 | Minh hỏi lại mục đích (M-36); giải thích ở dưới. **Đã quyết (M-40): Minh mở phiên Claude mới, cho phép dùng subagent; prompt ở Phụ lục P3** | — |
| E-13 | ~~Gửi cô câu hỏi?~~ **Đã trả lời (M-36): không gửi** | D.4.1 |
| E-14 | ~~Cách dùng test (C-15): A, B hay C?~~ **Đã trả lời (M-43): duyệt B** | M-41, M-42 |

**Giải thích E-12 (deep research):**
- **Là gì:** một chế độ làm việc trong đó nhiều agent con cùng tìm và đọc tài liệu song song, thường rất nhiều nguồn, rồi tổng hợp thành một báo cáo có trích nguồn.
- **Mục đích ở đây:** rà rộng các công trình 2024–2026 về RCA dùng đồ thị, RCA dùng LLM, cách kết hợp hai hướng này, và các công cụ công nghiệp, để biết có hướng nào tốt hơn D.2–D.3 mà file chưa có.
- **Khác A2:** deep research tìm rộng; A2 đọc sâu 10–12 bài đã chọn ở D.7.
- **Chi phí:** dùng hơn 2 agent con nên phải báo trước theo luật cứng 8; tốn nhiều token hơn một phiên thường; thời gian chưa ước lượng được.
- **Đề xuất:** làm A2 trước. Chỉ chạy deep research cho một câu hỏi hẹp nếu A2 thấy còn thiếu, ví dụ "các phương pháp RCA dùng đồ thị 2024–2026 có đánh giá trên RCAEval hoặc Nezha".

**Câu hỏi còn chờ Minh:** không còn ở Phần E. RQ3d đã quyết (M-47).

---

## Phần F. Việc tiếp theo và đề xuất ghi sổ chưa duyệt

### F.1 Làm dù cô trả lời thế nào

| Mã | Việc | Đầu ra | Chi phí |
|---|---|---|---|
| A1 | ~~T-041 phản biện đầy đủ (M-35).~~ **Xong: T-041 đã nghiệm thu và đóng ngày 23/10/2026 (Q-186, M-46). Không làm việc này nữa** | — | — |
| A0 | Soạn đúng đoạn sửa cho các đề xuất C đã duyệt hướng (bảng C.1), trình Minh một lượt trước khi ghi | Các đoạn sửa MRP, WHY, DECISIONS, PLAN-P6, LESSONS và tài liệu FlashTicket | 1 phiên |
| A10 | Khảo sát sâu: Minh mở phiên Claude mới, dán prompt ở Phụ lục P3; được dùng subagent (M-40) | Báo cáo khảo sát K1–K6 và danh sách đề xuất sửa kế hoạch | Theo ngân sách subagent ghi trong prompt; không dùng máy thực nghiệm |
| A2 | Thẻ đọc D.7 | Thẻ phương pháp | 1–2 phiên; không dùng máy |
| A3 | Bảng đủ độ đo, mức ngẫu nhiên, hạng từng ca cho baseline P3 | Bảng (cần quyền ghi) | Vài phút máy, chỉ đọc kết quả cũ |
| A4 | Dự thảo giao thức đánh giá | Văn bản | Agent |
| A5 | SPEC T-042 và H0–H2 | Số đo hạ tầng | Laptop, 0 USD; tải khoảng 14 GB (cần duyệt) |
| A6 | Gửi yêu cầu D.9 cho nhóm hệ thống | Bản yêu cầu | 1 phiên; Minh gửi |
| A7 | Kiểm dung lượng RE3-OB; xem Service Quotas các tài khoản | Số liệu | Chỉ đọc |
| A8 | Minh trả lời Phần E | Quyết định | — |

### F.2 Chờ cô

Nhánh G hoặc H của khâu phát hiện (M-20); phạm vi lỗi; tiêu chí lan truyền; cách trình bày đóng góp.

### F.3 Đề xuất ghi sổ chưa duyệt

- **Q-185** (thông tin hạ tầng) và **Q-186** (quyền chạy thử hạ tầng): soạn trong chat ngày 22/10; nội dung tương ứng là M-03, M-05, M-06, M-08.
- **Chép M-01…M-22 vào `docs/DECISIONS.md`:** chưa làm.
- **Một dòng trong `docs/STATE.md` trỏ tới file này:** chưa làm.

---

## Phần G. Nguồn

- **AWS:**
  - Gói Free: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-plans.html
  - EC2 Free Tier: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-free-tier-usage.html
  - Điều khoản: https://aws.amazon.com/free/terms/
  - Quota loại máy: https://docs.aws.amazon.com/ec2/latest/instancetypes/ec2-instance-quotas.html
  - Đồng bộ giờ: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html
  - Giá EBS: https://aws.amazon.com/ebs/pricing/
- **Google Cloud:** https://docs.cloud.google.com/free/docs/free-cloud-features
- **Grafana:**
  - Bảng giá: https://grafana.com/pricing/
  - Gói Free: https://grafana.com/products/cloud/free-tier/
  - Gửi OTLP lên Cloud: https://grafana.com/docs/grafana-cloud/send-data/otlp/send-data-otlp/
  - Điều kiện bật Knowledge Graph: https://grafana.com/docs/grafana-cloud/platform/knowledge-graph/get-started/prerequisites/
  - Sift: https://grafana.com/docs/grafana-cloud/machine-learning/sift/sift/
  - Base insights: https://grafana.com/docs/grafana-cloud/platform/knowledge-graph/reference/about-base-insights/
  - Đánh giá luật cảnh báo: https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rule-evaluation/
  - Nâng cấp Tempo: https://grafana.com/docs/tempo/latest/set-up-for-tracing/setup-tempo/upgrade/
  - Alloy và OTel: https://grafana.com/docs/alloy/latest/introduction/otel_alloy/
- **OpenTelemetry:**
  - Cờ lỗi của Demo: https://opentelemetry.io/docs/demo/feature-flags/
  - Kiến trúc Demo: https://opentelemetry.io/docs/demo/architecture/
  - Cài Demo bằng Docker: https://opentelemetry.io/docs/demo/docker-deployment/
  - Hiệu năng Java agent: https://opentelemetry.io/docs/zero-code/java/agent/performance/
  - Chỉ số tự báo của Collector: https://opentelemetry.io/docs/collector/internal-telemetry/
  - Thư viện được hỗ trợ: https://github.com/open-telemetry/opentelemetry-java-instrumentation/blob/main/docs/supported-libraries.md
- **Spring:** https://spring.io/blog/2025/11/18/opentelemetry-with-spring-boot/
- **Microsoft WSL:** https://learn.microsoft.com/en-us/windows/wsl/wsl-config
- **Prometheus:** https://prometheus.io/docs/prometheus/latest/storage/
- **Dynatrace:** https://docs.dynatrace.com/docs/platform/davis-ai/problem-and-root-cause/root-cause-analysis
- **Nghiên cứu:**
  - OpenRCA: https://proceedings.iclr.cc/paper_files/paper/2025/file/d29b8d53678015079e1d245c023e49d2-Paper-Conference.pdf
  - RCACopilot: https://arxiv.org/pdf/2305.15778
  - LILAC: https://arxiv.org/pdf/2310.01796
  - Murphy: https://sachin.cs.illinois.edu/papers/murphy-harsh-sigcomm23.pdf
  - Budhathoki: https://proceedings.mlr.press/v162/budhathoki22a.html
  - Các bài khác đã có trong `docs/knowledge/K4-ho-thuat-toan.md` và DE-XUAT §17.
- **Repo:**
  - `results/T-034/bang-baseline.json`
  - `results/T-002/public-sources.md`
  - `tasks/T-005-do-kha-thi/LOG.md`, `tasks/T-025-che-do-b/LOG.md`
  - `docs/MRP.md`, `docs/DECISIONS.md` (Q-04, Q-22, Q-62, Q-70), `docs/WHY.md` (WHY-02, WHY-06, WHY-07), `docs/LESSONS.md` (ST3, ST5, SL20, SL31)
  - Repo FlashTicket: `docs/architecture/aws-runtime-baseline.md`, `B16-observability-baseline.md`, `services/*/pom.xml`

---

## Phụ lục P1. Email gửi cô ngày 21/10/2026 (nguyên văn, Minh dán ngày 22/10/2026)

```text
Em chào cô ạ,
Em xin phép đại diện nhóm gửi cô hai báo cáo tiến độ, tên đồ án "Xây dựng hệ thống bán vé theo kiến trúc phân tán có ứng dụng đồ thị phụ thuộc để giám sát và chẩn đoán sự cố", báo cáo tiến độ gồm:
Báo cáo tiến độ xây dựng hệ thống bán vé theo kiến trúc phân tán.
Báo cáo tiến độ nghiên cứu đồ thị phụ thuộc vào chẩn đoán sự cố.
Do cả hai tài liệu đều tương đối dài, chúng em xin phép trình bày trước một số nội dung chính về những công việc nhóm đã thực hiện, những vấn đề còn đang nghiên cứu và một số điểm nhóm mong nhận được ý kiến định hướng từ cô.
1. Về phần xây dựng hệ thống bán vé theo kiến trúc phân tán
Đối với phần xây dựng hệ thống FlashTicket, hiện tại nhóm đang tiếp tục triển khai theo kế hoạch và chưa gặp khó khăn lớn về mặt kỹ thuật cần xin cô hỗ trợ giải quyết.
Trong báo cáo  nhóm tập trung trình bày phương pháp tiếp cận bài toán, phân tích nghiệp vụ và cơ sở lựa chọn kiến trúc.
Cụ thể, nhóm sử dụng phương pháp thiết kế hướng miền (Domain-Driven Design – DDD). Từ đó, nhóm lập luận cách phân chia trách nhiệm giữa các dịch vụ, phạm vi quản lý dữ liệu và cách các dịch vụ phối hợp với nhau.
Nhóm cũng đã vẽ các diagram để thể hiện yêu cầu nghiệp vụ, các luồng xử lý chính và phương án thiết kế hệ thống. Nhóm chú trọng những vấn đề đặc thù của hệ thống bán vé phân tán như xử lý nhiều yêu cầu đồng thời, tránh oversell, , tính nhất quán dữ liệu và khả năng xử lý khi một thành phần gặp lỗi, phục vụ cho các kịch bản kiểm thử tải sau này.
Tuy nhiên, có một vấn đề chúng em còn băn khoăn và rất mong được cô tư vấn.
Về định hướng báo cáo và bảo vệ, với tên đề tài như trên, chúng em mong được cô góp ý thêm về những nội dung cô và hội đồng kỳ vọng nhóm cần thể hiện được, ngoài việc trình diễn các chức năng của website. Chẳng hạn, khi bảo vệ, nhóm nên demo trực tiếp những tình huống đặc trưng của hệ thống phân tán hay tập trung trình bày kết quả kiểm thử, số liệu đo đạc? Nội dung quyển báo cáo nên chú trọng phân tích tính đúng đắn của nghiệp vụ bán vé, các nguyên tắc thiết kế hệ thống phân tán, hay kết hợp cả hai ở mức độ phù hợp? 
Chúng em muốn xác định rõ những yêu cầu quan trọng để phân bổ thời gian hợp lý, chuẩn bị đầy đủ cả phần triển khai, kiểm chứng và trình bày.
2. Về phần nghiên cứu ứng dụng đồ thị phụ thuộc vào chẩn đoán sự cố
Vì phần này khá mới với nhóm và phải tìm hiểu cơ chế của nhiều phương pháp hiện có và hiểu sâu nên tiến độ có thể chưa đáp ứng được kì vọng của cô.
Bám theo định hương trước đó của cô, nhóm đã tập trung tìm hiểu sâu hơn về cơ chế của các phương pháp RCA hiện có, mở rộng thực nghiệm trên dữ liệu công khai và phân tích các trường hợp chẩn đoán sai để xác định những hạn chế còn tồn tại. Trên cơ sở đó, nhóm đã xây dựng bước đầu mô hình đồng thời nghiên cứu cách ánh xạ log, trace và metric lên đồ thị.
Báo cáo phần này tương đối dài vì ngoài việc trình bày tiến độ, do nhiều nội dung chúng em mới tiếp cận lần đầu, nhóm cố gắng ghi lại tương đối chi tiết cách hiểu và các bước phân tích, để có cơ sở đối chiếu khi phát triển phương pháp tiếp theo.. Trong đó, Chương 1–2 trình bày cơ sở nghiên cứu và các phương pháp hiện có; Chương 3 là kết quả thực nghiệm; Chương 4 phân tích sâu những hạn chế và nguyên nhân dẫn đến kết quả chưa phù hợp; Chương 5 tổng hợp các phát hiện chính, mô hình đồ thị đã xây dựng và định hướng cho giai đoạn sau.
Chúng em hiểu thời gian của cô có hạn, nên nếu chưa thuận tiện xem xét toàn bộ tài liệu, nhóm xin phép lưu ý rằng các nội dung chúng em mong được cô góp ý nhất hiện tập trung ở Chương 5. Những chương trước chủ yếu cung cấp cơ sở thuật toán, số liệu và phần phân tích chi tiết để đối chiếu cho các đề xuất ở chương 5. 
3. Mong cô góp ý và định hướng chung
Nếu định hướng hiện tại còn điểm nào chưa phù hợp, chúng em rất mong cô góp ý về phạm vi, phương pháp và thứ tự ưu tiên để nhóm rà soát, điều chỉnh.
Cuối cùng, chúng em mong cô thông cảm vì hai tài liệu đính kèm còn khá dài và một số phần có thể chưa thật sự cô đọng. Nhóm rất mong cô góp ý thêm về cách tổ chức và trình bày báo cáo để những lần sau rõ trọng tâm, phù hợp hơn với yêu cầu của cô.
Bên cạnh đó, chúng em cũng mong được cô lưu ý thêm những yêu cầu quan trọng và các vấn đề nhóm cần chuẩn bị cho buổi bảo vệ đồ án cuối cùng, để có thể chủ động hoàn thiện từ sớm.
Em cảm ơn cô đã dành thời gian xem xét và hướng dẫn nhóm ạ!
Đại diện nhóm
Lê Văn Minh
```

---

## Phụ lục P2. Prompt cho Codex phản biện file này

- Gồm: Prompt chung, khối "Soát SPEC" và khối G3 của `docs/review-prompt.md`, chép nguyên văn.
- Thêm "Khối yêu cầu của Minh" theo M-22. Khối này là ngoại lệ đối với AGENTS §9 và Q-44, **chỉ dùng cho lượt phản biện này** (M-29). Prompt vẫn theo mẫu. C-10 không duyệt, nên các prompt sau không tự thêm khối này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: docs/KE-HOACH-GIAI-DOAN-TOI.md (kế hoạch giai đoạn P6–P10 và quyển đồ án, Claude tạo ngày 22/10/2026 theo lời duyệt của Minh; xem Phần Z của file để biết bản hiện hành). Ngoài task, chưa có mã T.
- Công đoạn: soát SPEC.
- Gói/cổng: P6–P10, trước SPEC M1; G2 đã duyệt (Q-149), G3 chưa mở. Loại đề xuất: kế hoạch công việc, đề xuất thay đổi tài liệu điều hành (Phần C của file), đề xuất ghi sổ.
- Người làm và người phản biện chính thức: ngoài task; vai trò dự kiến: Claude soạn, Codex phản biện.
- Tài liệu gốc: docs/KE-HOACH-GIAI-DOAN-TOI.md (Phần A là lời Minh nguyên văn; Phụ lục P1 là email gửi cô); báo cáo tiến độ gửi cô 21/10/2026, chương 5 (C:\Users\84583\Downloads\Định hướng chức năng AI cho đồ án tốt nghiệp.docx; Minh đính kèm nếu không đọc được); docs/DE-XUAT-HUONG-GRAFANA-RCA.md; docs/PLAN-P6.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/review-prompt.md; results/T-034/goi-g2.md và bang-baseline.json; results/T-040/ban-giao-p6.md; results/T-041/; results/T-002/; tasks/T-005-do-kha-thi/LOG.md; tasks/T-025-che-do-b/LOG.md; docs/knowledge/; docs/reference/sources/; D:/Project/flash-ticket-platform (chỉ đọc: services/*/pom.xml, docs/architecture/aws-runtime-baseline.md, B16-observability-baseline.md, B13-api-and-event-contracts.md). docs/DECISIONS.md và docs/STATE.md có thay đổi chưa commit từ trước (git diff).
- Phản biện và phản hồi trước: chưa có phản biện cho file này. Lịch sử phản biện PLAN-P6 ở docs/PLAN-P6.md §9; phản biện định hướng Grafana dừng theo Q-179.
- Code và kết quả liên quan: không có code mới; manifest results/T-034/runs/manifest-cuoi-007/manifest.json. Được đọc tài liệu chính thức, bài và mã gốc trên web; được chạy lệnh chỉ đọc và phép tính nhỏ không ghi file trong repo.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: soát SPEC.
Kiểm câu hỏi nguồn, phần mục tiêu được bao phủ, giả thuyết khác, khả năng phân xử của dữ liệu, phép kiểm dự kiến, phụ thuộc bước, chi phí, phạm vi và tiêu chí xong. Phần không làm phải có lý do, hệ quả và quyết định phụ thuộc.
Đánh giá kế hoạch và bằng chứng đã có; không đòi có kết quả của thực nghiệm chưa được duyệt. Phân biệt ứng viên để thử với lựa chọn đã chốt.
Chỉ ghi bản phản biện được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat nếu chưa có quyền ghi. Không tự sửa SPEC.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.

Khối yêu cầu của Minh cho lượt này (Minh yêu cầu ngày 22/10/2026; nguyên văn ở Phần A của file, mã M-10, M-12 đến M-22). Khối này là ngoại lệ Minh cho phép đối với AGENTS §9 và Q-44. Khi khối này khác với câu trong Prompt chung về phạm vi đề xuất, làm theo khối này:
1. Phản biện độc lập và đa chiều. Ngoài việc tìm lỗi, chủ động đề xuất những hướng, khía cạnh và rủi ro mà file và Minh chưa nghĩ tới. Minh không chuyên về hạ tầng, chưa có kinh nghiệm triển khai, và không kỳ vọng phương pháp RCA có điểm đo cao; đề xuất cần cụ thể, làm được, không chung chung.
2. Được đề xuất thay đổi MRP, WHY, DECISIONS, AGENTS, PLAN-P6 nếu có lý do, kể cả các mục Claude không nêu trong Phần C. Không bị gò bó quá mức bởi luật hiện hành. Mỗi đề xuất ghi: thay gì, vì sao, ảnh hưởng.
3. Được đề xuất về nội dung nghiên cứu: phương pháp, cách kết hợp các thành phần thành một phương pháp tổng, cách dùng LLM ở các khâu trung gian, cách dùng Grafana Cloud cùng bản tự cài, bố trí hạ tầng nhiều tài khoản và instance, cách đánh giá và trình bày trước hội đồng. Đây là đề xuất nội dung, không bị câu "không đề xuất thêm quy trình" chặn.
4. Không dùng thời gian làm lý do chính để cắt phạm vi. Nêu chi phí thật nếu có: máy, tiền, dung lượng, công duyệt của Minh.
5. Được phản bác cả đề xuất của Claude lẫn quan điểm của Minh ghi ở Phần A, khi có bằng chứng. Nêu rõ chỗ mâu thuẫn để Minh quyết; không tự chọn thay Minh.
6. Mỗi đề xuất ghi đã kiểm hay chưa kiểm, nguồn, giả định và khi nào nó sai.
```

---

## Phụ lục P3. Prompt cho phiên Claude khảo sát sâu (M-40)

- Phiên mới, do Minh mở. Minh cho phép dùng subagent (M-40).
- Đây là phiên khảo sát, không phải phản biện, nên không dùng mẫu `docs/review-prompt.md`.
- Số subagent tối đa trong prompt là đề xuất; Minh sửa trước khi dán nếu muốn.

```text
Bạn là phiên Claude mới làm khảo sát sâu (deep research) trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Minh cho phép phiên này dùng subagent và skill deep-research (lời Minh ngày 22/10/2026, mã M-40 trong docs/KE-HOACH-GIAI-DOAN-TOI.md). Ngân sách: tối đa 6 subagent. Cần nhiều hơn thì dừng và hỏi Minh.

Mục đích: tìm những hướng, bằng chứng và rủi ro mà kế hoạch docs/KE-HOACH-GIAI-DOAN-TOI.md chưa có, để Minh quyết sửa kế hoạch. Đây là khảo sát. Không thiết kế chi tiết, không cài đặt, không chạy thực nghiệm.

Đọc trực tiếp trước khi giao việc cho subagent (không dựa tóm tắt):
- docs/KE-HOACH-GIAI-DOAN-TOI.md: Phần A (lời Minh), Phần B (dữ kiện), Phần D (kế hoạch; D.7 là danh sách đọc đã có), Phần E (câu hỏi đang chờ).
- docs/MRP.md §2–3 và P6–P10; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md.
- docs/knowledge/K1-phuong-phap-rca.md và K4-ho-thuat-toan.md, để không lặp lại phần repo đã có.
- results/T-034/goi-g2.md mục 0 và mục 5.
- docs/DE-XUAT-HUONG-GRAFANA-RCA.md §2 và §17.

Câu hỏi khảo sát. Trả lời riêng từng câu:
K1. Phương pháp RCA dùng đồ thị công bố 2023–2026, ưu tiên có đánh giá trên RCAEval (RE1, RE2, RE3), Nezha, Train Ticket, Online Boutique hoặc sự cố thật. Với mỗi phương pháp: cơ chế; đầu vào; dùng quan hệ ở bước nào; kết quả công bố và có so với baseline đơn giản (SimpleRCA FSE 2026, BARO) không; điều kiện thất bại; liên quan tới mô-đun nào ở D.2. Có thành phần nào nên thêm vào hoặc thay cho E1–E9 không?
K2. LLM ở các khâu trung gian của RCA: tách mẫu log, trích quan hệ phụ thuộc từ code và cấu hình, tóm tắt bằng chứng, agent điều tra, xếp hạng. Kết quả, chi phí, độ ổn định giữa các lần chạy, cách đánh giá, rủi ro rò nhãn và bịa. Đối chiếu với L1–L6 ở D.3.
K3. Đồ thị trong quyết định báo động và gom cảnh báo: nghiên cứu (ví dụ ART, CNSS, các phương pháp alert correlation, alert aggregation) và công cụ công nghiệp (Dynatrace, Grafana Cloud Knowledge Graph, Datadog, Coroot và các nền tảng AIOps khác). Đối chiếu với nhánh G, H ở D.4.1.
K4. Cách đánh giá: độ đo RCA chuẩn (AC@k, Avg@k, MRR, NDCG); phép thống kê khi mẫu nhỏ; cách đặt biên không thua (non-inferiority); cách các bài báo tránh thiên lệch khi đánh giá trên hệ thống tự dựng. Đối chiếu với D.6, D.9 và đề xuất E-04 ở D.1.
K5. Hạ tầng:
  - tình trạng hỗ trợ của OpenTelemetry Java agent với Spring Boot 4.x và Java 21;
  - công cụ tiêm lỗi cho Spring Boot 4 và Docker trên EC2, không dùng Kubernetes;
  - cách kết hợp Grafana tự cài với Grafana Cloud;
  - testbed và dataset công khai dựng trên OpenTelemetry Demo.
  Đối chiếu với D.8, D.9, D.10.
K6. Những khía cạnh kế hoạch chưa xét. Tự đề xuất, đa chiều, cụ thể: phương pháp, đánh giá, hạ tầng, demo, bảo vệ trước hội đồng.

Yêu cầu của Minh cho phiên này (nguyên văn ở Phần A, các mã M-10, M-12 đến M-22):
- Đề xuất độc lập, đa chiều; ưu tiên hướng Minh chưa nghĩ tới.
- Được đề xuất đổi MRP, WHY, DECISIONS, AGENTS, PLAN-P6 và chính file kế hoạch.
- Không dùng thời gian làm lý do chính để cắt phạm vi.
- Được phản bác cả kế hoạch lẫn quan điểm của Minh khi có bằng chứng. Chỗ mâu thuẫn thì nêu để Minh quyết; không tự chọn thay Minh.

Chất lượng nguồn:
- Ưu tiên bài báo gốc, tài liệu và mã chính thức. Ghi đường dẫn cho mọi khẳng định.
- Tách rõ ba loại: đã đọc nguồn gốc; chỉ đọc tóm tắt hoặc nguồn bên thứ ba; suy luận.
- Số liệu ghi rõ lấy từ đâu (bảng, mục).
- Không chép dài. Mỗi nguồn trích nguyên văn tối đa một câu ngắn.

Giới hạn:
- Không tạo, sửa, xóa file nào trong repo hay ngoài repo (AGENTS Luật 0). Không commit. Chỉ trả lời trong chat, trừ khi Minh cho phép ghi một file cụ thể trong phiên.
- Không mở data/locked. Không chạy thực nghiệm. Không tải dữ liệu.
- Subagent cũng tuân theo các giới hạn trên.

Đầu ra (tiếng Việt, câu ngắn):
1. Tóm tắt một trang: những gì nên thay đổi trong kế hoạch, xếp theo mức ảnh hưởng.
2. Với từng câu K1–K6: phát hiện; nguồn; mức tin cậy; liên quan tới mục nào của file kế hoạch; đề xuất cụ thể (thêm, bỏ, đổi) kèm lý do và ảnh hưởng.
3. Danh sách đề xuất sửa file theo mẫu Luật 0 mục 3 (file nào, sửa gì, vì sao, ảnh hưởng), để Minh duyệt.
4. Những điều chưa kiểm được và vì sao.
5. Số subagent đã dùng và thời gian đã chạy.
6. Báo cáo bốn mục theo AGENTS §7.
```

---

## Phần Z. Lịch sử sửa

| Ngày | Người sửa | Nội dung | Căn cứ |
|---|---|---|---|
| 22/10/2026 | Claude | Tạo bản đầu: gộp kế hoạch lượt 1–3 trong chat ngày 22/10, các đính chính và quyết định M-01…M-22, phần mở rộng (Grafana Cloud, quota vCPU, Spring Boot 4, LLM khâu trung gian, phương pháp hợp nhất, đối chứng) và prompt Codex | M-11, M-23 (lời duyệt trong chat 22/10/2026) |
| 22/10/2026 | Claude | Ghi câu trả lời E-01 của Minh: thêm M-24; sửa D.1, D.9, C-03, Phần E (E-01 đã trả lời), danh sách "Đã áp vào file" ở Phần A | M-24; M-11 (file ghi quyết định mới nhất) |
| 22/10/2026 | Claude | Ghi câu trả lời E-02 của Minh: thêm M-25; bỏ C-b ở D.5 (giữ lập luận cũ làm lịch sử); sửa C-02 (thêm hệ quả cho RQ3d), D.14 (M7), Phần E, danh sách "Đã áp vào file" | M-25; M-11 |
| 22/10/2026 | Claude | Ghi các câu trả lời M-26…M-36. Thêm bảng trạng thái C.1 (duyệt hướng C-02…C-09, C-12, C-13; C-10 không duyệt; C-11 rút lại; C-01, C-14 chờ). Sửa lời C-14 và đổi tên D.2 theo M-32. Thêm đề xuất E-04 vào D.1. Thêm D.4.1 (trả lời M-28). Sửa D.5 (C-c giữ), D.8.4 (M-33), D.12 (M-34). Cập nhật Phần E (thêm giải thích E-12), Phần F (A0, A1) và ghi chú ở Phụ lục P2 (M-29) | M-26…M-36; M-11 |
| 22/10/2026 | Claude | Ghi M-37…M-40. Bảng C.1: C-01, C-14 duyệt hướng. Phần E: E-05, E-07, E-12 cập nhật; thêm đề xuất cách xử lý RQ3d; E-04 giữ nguyên, chưa duyệt. Thêm A10 ở Phần F và Phụ lục P3 (prompt khảo sát sâu) | M-37…M-40; M-11 |
| 22/10/2026 | Claude | Ghi câu hỏi M-41 về việc sửa sau khi xem test; thêm đề xuất C-15 (Phần C, bảng C.1) và câu E-14 (Phần E) | M-41; M-11 |
| 22/10/2026 | Claude | Ghi câu hỏi M-42. Bổ sung C-15: thời điểm mở RE3-OB, danh sách chỗ phải sửa nếu chọn B (luật cứng 1 giữ nguyên, sửa AGENTS §11) | M-42; M-11 |
| 22/10/2026 | Claude | Ghi M-43: C-15 phương án B duyệt hướng (bảng C.1); E-14 đã trả lời | M-43; M-11 |
| 23/10/2026 | Claude | Ghi M-44: E-04 duyệt theo bản sửa KS-07. Sửa D.1 (dòng RE2-TT ở Tầng 2, mục E-04), Phần A (dòng M-44; dòng "Đã áp vào file" về E-04), bảng C.1 (C-08), Phần E (dòng E-04; dòng câu hỏi còn chờ) | M-44; Minh chọn "Ghi vào kế hoạch" ngày 23/10/2026 |
| 23/10/2026 | Claude | Ghi M-45 (P-A sau phản biện Codex): D.1 mục E-04 đổi "Cách đọc" thành hai câu hỏi báo đồng thời; "Tiêu chí thực dụng" bỏ số chưa kiểm; "Sức phân biệt" ghi số kèm giả định; phương án (b) thêm ghi chú về M1; tiêu đề E-04 ghi M-45. Giữ Δ, TORAI B, vai trò Hit@1 | M-45 |
| 23/10/2026 | Claude | Ghi M-46: T-041 đã đóng (Q-186); sửa Phần B (dòng T-041), Phần E (E-10), Phần F (A1), danh sách "Đã áp vào file". Ghi M-47: RQ3d chọn sửa câu; sửa bảng C.1 (C-02), Phần E (E-07, dòng câu hỏi còn chờ). Chưa sửa MRP, WHY, LESSONS | M-46, M-47; M-11 |
| 23/10/2026 | Claude | Thiết kế RCA không chờ thư cô: sửa D.12 (dòng S1, cột "Vào khi"); ghi Q-187 ở DECISIONS, sửa STATE. Áp đoạn sửa RQ3d vào MRP, WHY-07, LESSONS QT8, AGENTS luật cứng 18; cập nhật bảng C.1 (C-02) | Q-187; lời Minh "duyệt đề xuất 1 3" ngày 23/10/2026 |
| 23/10/2026 | Claude | Ghi M-48 ở Phần A: bốn nhóm gợi ý của bản khảo sát vào SPEC M1 làm ứng viên để thử, kèm ba kết cục. Không sửa D.2, D.5, D.7 | M-48 |
| 25/10/2026 | Claude | D.9: thêm "Ba chặng và hai đợt FlashTicket" (chia theo ô; ngoại lệ chia theo lần lặp để OPEN; ba câu hỏi báo riêng; điều kiện tải trong đợt phát triển; kiểm chất lượng telemetry; LLM ở khâu giữa; chi phí đợt phát triển OPEN); ghi chú tách vị trí tiêm, cơ chế, đáp án dưới bảng kịch bản; luật chống thiên lệch 3 chỉ áp cho đợt đánh giá; nhãn vùng ở mức endpoint và chấm nhãn cạnh; dự toán chiến dịch chỉ cho đợt đánh giá. D.12: tách S6 thành S6a (phát triển chuyển giao) và S6b (đánh giá) | Q-197; phản biện Codex R17–R24 ngày 25/10/2026 |
