# Kế hoạch P6 — bản hợp nhất sau phản biện

Ngày ghi: 18/10/2026. Người lập: Codex. Người phản biện kế hoạch: Claude.

## 1. Trạng thái, quyền hạn và cách đọc

Minh yêu cầu **ghi lại đầy đủ kế hoạch P6 đã chốt qua các lượt phản biện và các quyết định liên quan**, dựng từ nguyên văn để tiếp tục trên phiên/agent/máy khác. Quyền ghi nhận này được lưu ở [DECISIONS](DECISIONS.md), Q-177–Q-178. Bản hiện hành gồm **13 phần việc chính M1–M13 và 15 nhánh có điều kiện C1–C15**; không phải 28 task mặc định đều triển khai.

- **USER_CONFIRMED / DECIDED về tổ chức:** lưu bản hợp nhất lần 3 cùng phần sửa cuối đã được phản biện chấp nhận; chia theo đầu ra/phép kiểm, dùng lại P1–P5; giữ đính chính của Minh về thời gian, phiên, nén ngữ cảnh và bàn giao.
- **FACT về phản biện:** Claude xác nhận phần sửa đạt, không còn bất đồng ảnh hưởng cấu trúc và đề xuất dừng (S15). Không biến đồng thuận của hai agent thành bằng chứng phương pháp hiệu quả.
- **CANDIDATE:** cơ chế, mức graph, nguồn cạnh, baseline bổ sung, dữ liệu nền và cấu hình cụ thể. C15 hiện **chưa kích hoạt**; không đồng nghĩa đã chứng minh mọi GNN bất khả thi.
- **OPEN:** dữ liệu có đủ phân xử không, hiệu chỉnh detector, hiệu quả ứng viên, khả năng dùng trong vận hành và các phụ thuộc nghiệm thu nguồn.
- **Chưa được cấp quyền:** tạo/triển khai SPEC, chạy thử nghiệm mới, kích hoạt toàn bộ nhánh C, tải dữ liệu, mở test/giữ ngoài, chọn thiết kế cuối, đóng G3/RQ hoặc commit/push. M/C là mã kế hoạch; chưa cấp mã T mới. Vai trò từng task chốt khi trình SPEC, không tự kế thừa phân công kế hoạch.

Nguồn quyết định chính thức vẫn là DECISIONS; MRP/WHY không bị thay thế. Tài liệu này ghi tổ chức công việc và trạng thái lựa chọn, không phải một “SPEC P6” khổng lồ.

**Đọc để tiếp tục:** §2–§7 là bản hiện hành. §8 là prompt bàn giao. §9 lưu nguyên văn các nguồn S01–S16 ngay trong repo. Các đường dẫn attachment/session trong phụ lục chỉ là xuất xứ; không cần các file trên máy cũ để đọc nguồn. Trong phụ lục có đề xuất/ước lượng/quyền ghi lịch sử đã hết hiệu lực; không dùng chúng thay phần hợp nhất. Không suy từ nguồn mới hơn rằng mọi ứng viên trong nguồn đó đều đã được chọn.

## 2. Đính chính của Minh và lịch sử hợp nhất

Áp dụng nguyên văn đính chính S05; Q-178 dẫn lại nguồn này. Không dùng giờ máy, số file hoặc số đầu việc để suy ra lượng context; chưa đo thì ghi chưa biết. Task, cuộc trò chuyện và vòng đời làm–phản biện–sửa–nghiệm thu là các đơn vị khác nhau. Sau nén, khôi phục mục tiêu, quyền hạn, trạng thái, bằng chứng và bước tiếp theo; chỉ đề nghị chuyển phiên vì lý do cụ thể. Checkpoint và quyền ghi vẫn giữ nguyên. Không giảm câu hỏi khoa học để vừa phiên.

AGENTS §5/§5a chưa được sửa trong lượt này. Đính chính trực tiếp của Minh là cách áp dụng được lưu cho P6, không coi nén ngữ cảnh tự nó là lệnh dừng. Chưa lập lịch theo giờ/tuần của Minh; không dùng câu trả lời 16 giờ/tuần để định hình task.

| Nguồn | Nội dung được tiếp nhận / thay thế |
|---|---|
| S01–S04 | Yêu cầu đủ khoa học và bàn giao giữ nguyên; phân rã 34 + 15 và dự toán giờ cứng không còn là kế hoạch thực hiện. |
| S05–S06 | Gộp theo quan hệ công việc; dùng lại P1–P5; bỏ quy đổi runtime thành giới hạn phiên. Bản 12 + 11 là bước trung gian. |
| S07–S11 | Phát hiện có câu hỏi, baseline và phép kiểm riêng; phân biệt raw flag/sự kiện/thông báo; xử lý biên file, tiền xử lý và phạm vi ranker. |
| S12 | Bản hợp nhất 13 + 15; thêm M6 cài/kiểm baseline, C12–C15; đối chiếu đủ 49 mã cũ. |
| S13–S14 | M1 thêm nguồn nền/hiệu chỉnh và bằng chứng GDN; ưu tiên C8/C12/C13/C15; sửa cách diễn giải số và chi phí. |
| S15 | Phản biện chấp nhận sửa; không còn bất đồng về cấu trúc. Các câu khoa học vẫn OPEN. |
| S16 | Minh giao ghi lại bản chốt và các quyết định vào repo, không viết từ trí nhớ. |

### Các đính chính khoa học đã được tiếp nhận

- UV-1 không chỉ đổi nơi gán cùng một điểm: còn gộp tỷ lệ lời gọi đi vào vượt nền. Không kết luận mọi cách cài đều giữ nguyên điểm hệ thống.
- G2-H22 xác nhận phép OR và độ dài lịch sử có ảnh hưởng; chưa xác định đầy đủ nguyên nhân N-Sigma báo dày.
- Sắp điểm là một lựa chọn xếp hạng phải có căn cứ và đánh giá MRR; không bắt buộc thêm PageRank. Không chọn thiết kế chỉ để làm tăng chênh lệch có–không đồ thị.
- Thứ hạng cải thiện không tự chứng minh detector tốt hơn. Đếm cờ, đợt, thông báo và thời gian ở trạng thái báo động; ít thông báo do thời gian trơ không đồng nghĩa phân biệt tốt hơn.
- Chưa tìm được cơ chế để thử không được coi là đã làm xong nghĩa vụ thiết kế; kết quả âm của phép thử hợp lệ được giữ và diễn giải trung thực.

## 3. Kế hoạch thực hiện hợp nhất

Mục tiêu P6 là tạo ra phương pháp có thể chạy và kiểm được trên dev: phát hiện, vùng nghi ngờ và xếp hạng; có baseline đủ sức so sánh; có đối chứng để phân biệt tác dụng của tín hiệu với tác dụng của quan hệ; có giao diện dùng lại trên FlashTicket.

P6 kết thúc bằng hồ sơ trình G3. Kết luận trên dữ liệu chưa dùng để thiết kế thuộc P7; giải thích bằng LLM thuộc P8; triển khai quan sát và tích hợp thuộc P9; bằng chứng vận hành FlashTicket thuộc P10. Không chuyển nghĩa vụ đánh giá phát hiện công khai sang P10.

Các mã M/C dưới đây là mã kế hoạch. Thư mục task hiện kết thúc ở T-040; chưa cấp mã task chính thức mới.

### Căn cứ thiết kế và phần chưa biết

| Thành phần | Căn cứ hiện có | Việc P6 phải phân xử |
|---|---|---|
| RCA dùng chứng cứ phía gọi, tính cho bên được gọi | UV-1 và phân tích vị trí tín hiệu trong G2 | Cải thiện thứ hạng ở điều kiện nào; có làm hỏng ca đúng, ca không có cạnh hoặc lỗi trả về nhanh không |
| Phát hiện có dùng quan hệ | Yêu cầu DT18/MRP; P3 cho thấy bộ phát hiện hiện tại chưa đáp ứng mục tiêu vận hành | Quan hệ bổ sung thông tin gì để đổi quyết định cảnh báo; lợi ích có còn khi giữ cùng tín hiệu và chính sách cảnh báo không |
| Vùng nghi ngờ | DT18 yêu cầu đầu ra vùng; đồ thị P5 cung cấp quan hệ | Vùng được tạo bằng phép tính nào; có chứa root và rộng tới đâu; chưa gọi là vùng ảnh hưởng thật nếu thiếu nhãn |
| Metric/log và lỗi return | UV-6; giới hạn của tín hiệu độ trễ | Tín hiệu nào thực sự phân biệt được lỗi, thay vì chỉ thêm nhiều cờ |
| Đồ thị tĩnh và các loại cạnh khác | Bàn giao P5; yêu cầu DT18 | Cạnh nào có dữ liệu và thực sự tham gia tính toán; phần nào chỉ kiểm được trên FlashTicket |

Nguồn đầu vào chính là [G2](../results/T-034/goi-g2.md) và [bàn giao P6 của T-040](../results/T-040/ban-giao-p6.md). Các tài liệu này đã được kiểm lại hash trong lượt lưu kế hoạch (§7). Bàn giao P5 cũng nêu rõ: cạnh trace dev chưa được xác nhận kiểu; không được tự coi chúng là cạnh gọi đồng bộ hoặc dùng kiểu tĩnh để lấp chỗ thiếu.

Đối với phát hiện, M1 sẽ xét các hướng sau, **chưa giao cài mặc định**:

| Hướng ứng viên | Quan hệ tham gia ở đâu? | Điều kiện có thể làm hướng này thất bại |
|---|---|---|
| Thống kê quét trên đồ thị con | Quan hệ xác định những vùng được xét; điểm và ngưỡng quyết định cho cả vùng | Tải bình thường cũng gây lệch đồng thời; lỗi đơn lẻ bị bỏ sót; quét nhiều vùng làm ngưỡng sai nếu không hiệu chỉnh |
| Phần dư có điều kiện | Dự báo hoặc giải thích tín hiệu một nút bằng tín hiệu ở các nút liên quan | Mô hình học cả sự cố; quan hệ không phù hợp; thiếu nền; trừ mất chính chứng cứ cần phát hiện |
| Phân rã chứng cứ theo cây lời gọi | Quan hệ cha–con thay đổi đại lượng được chấm, không chỉ tên nơi nhận điểm | Thiếu span, bất đồng bộ, chồng lấn; lỗi không làm tăng thời lượng |

Thống kê quét có cơ sở nghiên cứu, nhưng **không thể suy “xét vùng liên thông sẽ chữa được báo động dày”**. Công trình CNSS chỉ ra chính việc tối đa hóa trên nhiều đồ thị con có thể làm phép chấm hiệu chỉnh sai. Đây là căn cứ phải xét cách hiệu chỉnh, chưa phải bằng chứng phù hợp với RCAEval. [Bài CNSS, AAAI 2022](https://ojs.aaai.org/index.php/AAAI/article/view/20339).

### Bộ baseline được tổ chức theo câu hỏi so sánh

| Nhóm | Trạng thái và mục đích | Nơi chịu trách nhiệm |
|---|---|---|
| N-Sigma đã chạy ở P3 | Giữ làm mốc lịch sử; dùng lại kết quả đúng giao thức cũ | M1 xác định phép so; M6 chỉ chạy phần cần cho giao thức mới |
| BOCPD lịch sử | Giữ số hồi cứu và giới hạn tiền xử lý; không gọi thành detector trực tuyến | M1/M12 |
| Baseline thống kê nhân quả bổ sung | Xét một cách có khả năng cạnh tranh, thay vì chỉ so với N-Sigma nguyên trạng; ứng viên gồm ngưỡng hiệu chỉnh hoặc phương pháp tích lũy | M1 lựa chọn để thử; **M6 cài và kiểm** |
| Baseline dùng trace | So tác dụng của thêm trace; lựa chọn giữa luật span có nền nhân quả và biến thể MicroRank phù hợp đầu vào | M1 xác định biến thể; **M6 cài và kiểm** |
| BOCPD nhân quả | Một biến thể cần kiểm riêng tiền xử lý và số học | C8 |
| GDN làm baseline | Đối chiếu với detector học quan hệ giữa các chuỗi metric; không đồng nhất đồ thị học được với đồ thị gọi dịch vụ | C12 |
| Đối chứng cùng tín hiệu nhưng bỏ phần quan hệ đang xét | Phân biệt lợi ích do quan hệ với lợi ích do tín hiệu, cửa sổ hoặc ngưỡng | M7 |
| Baseline RCA chế độ (a) | Dùng lại bộ P3 theo từng dataset và trạng thái hỗ trợ | M12 |
| Baseline RCA chế độ (b) | Hiện hành: BARO, CIRCA kiến trúc, TORAI; mọi bổ sung phải ghi riêng | M1/M12; C5/C7 nếu mở rộng |

Ví dụ, CUSUM có mục đích tích lũy bằng chứng để phát hiện dịch chuyển nhỏ kéo dài, khác với chỉ xét một điểm vượt ngưỡng. Điều đó đủ để đưa vào thẩm định, **không đủ để chọn trước hoặc hứa giảm báo sai trên dữ liệu này**. [Tài liệu NIST](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm).

GDN cũng là một đối thủ có cơ chế khác: học quan hệ giữa các biến để dự báo hành vi. Khả năng sử dụng ở đây còn phụ thuộc dữ liệu học, hiệu chỉnh và chi phí. [Bài GDN](https://arxiv.org/abs/2106.06947).

M1 phải chốt **danh sách hữu hạn để thử**, phiên bản, dữ liệu học/hiệu chỉnh, ngân sách chọn cấu hình và lý do loại các phương án còn lại. M6 không nhận một yêu cầu mở kiểu “cài thêm baseline cho đủ mạnh”.

### Bổ sung bắt buộc cho đầu ra M1: nguồn nền và hiệu chỉnh

Đầu vào thêm T-005, T-018 §8–9 và WHY-18. Đầu ra phải có một bảng giao thức cho từng detector, trả lời được:

1. **Nền lấy từ đâu?** Bản ghi bình thường riêng, đoạn dev khác được chọn bằng nhãn phục vụ học, hay đoạn khởi động của chính luồng?
2. **Dữ liệu nào dùng để học, chọn cấu hình, hiệu chỉnh ngưỡng và đánh giá?** Có dùng lại cùng dữ liệu cho nhiều vai trò không; nếu có thì kết luận bị giới hạn thế nào?
3. **Tại thời điểm báo động, hệ thống thực sự đã có thông tin nào?** Gồm cả điền thiếu, chuẩn hóa, chọn cột, chọn ngưỡng và cập nhật nền.
4. **Khoảng nào chưa thể chấm?** Khởi động, thiếu nền, thiếu tín hiệu phải được báo rõ; không tính mặc nhiên là bình thường.
5. **Cách chọn ngưỡng cân bằng báo động và bỏ sót ra sao?** Không chọn bằng việc giảm số thông báo sau khi đã thấy kết quả.

Phương án ưu tiên **để M1 xem xét**, chưa chốt, là học/hiệu chỉnh từ các nhóm dev khác rồi đánh giá trên nhóm không tham gia các bước ấy. Các lần lặp cùng ô phải đi cùng phía, phù hợp MRP; không chỉ chia ngẫu nhiên từng ca. Phải phân biệt tập chọn mô hình với tập hiệu chỉnh ngưỡng, đồng thời tránh cửa sổ chồng qua ranh giới.

Dùng mốc tiêm của **ca dev khác** để lấy đoạn học là sử dụng nhãn cho việc học. T-018 đã khai điều này cho phép chẩn đoán của nó; không vì thế mà tự động có một giao thức P6 hoàn chỉnh đã được duyệt.

Phương án dùng đoạn khởi động của chính luồng vẫn có thể xét, nhưng **rút ngắn đoạn đó không chứng minh nó bình thường**. Nó chỉ cho phép kết luận trong điều kiện vận hành có một giai đoạn khởi động phù hợp. Nếu dữ liệu không kiểm được giả định này thì phải giữ giới hạn, không dùng điểm đẹp để thay bằng chứng.

### Các nhánh phát hiện được ưu tiên và phân trách nhiệm lại như sau.

| Phần việc | Mục đích và điều kiện thực hiện |
|---|---|
| **M1 → M3/M5/M6** | Ưu tiên trước: xác định nền hợp lệ; xây điểm và quyết định báo động; cài baseline thống kê và baseline trace có câu hỏi so sánh rõ. M6 tiếp nhận kết quả nhánh bổ sung, không cài lại. |
| **C8 — BOCPD theo luồng** | Chỉ kích hoạt khi cần phân xử ảnh hưởng của tiền xử lý nhìn trước trong BOCPD lịch sử, hoặc cần đối chứng phát hiện điểm đổi mà baseline M6 chưa cung cấp. Nếu BOCPD chính là baseline được chọn ở M6, gộp phần thực hiện vào M6; không tạo thêm một lần chạy tương đương. |
| **C13 — xét dữ liệu bổ sung** | Có thể cần ngay từ M1 nếu dữ liệu hiện tại không phân xử được câu hỏi về nền, tải thay đổi hoặc báo động vận hành. Không đợi chạy hết các phương pháp rồi mới nhận ra thiếu dữ liệu. Dùng lại hồ sơ P2; chỉ kiểm khoảng trống cụ thể. |
| **C14 — tích hợp dữ liệu bổ sung** | Chỉ sau khi C13 xác định được bộ dữ liệu phù hợp và Minh duyệt. |
| **C12 — baseline GDN** | Chỉ kích hoạt khi có câu hỏi khoa học và thay đổi cụ thể so với cấu hình T-018: chẳng hạn xử lý lệch mức giữa các lượt chạy, hoặc so quan hệ metric học được với quan hệ dịch vụ. Phải có phép thử có thể bác bỏ kỳ vọng ấy. **Không kích hoạt chỉ để có tên GNN trong bảng.** |
| **C15 — phương pháp GNN của đề tài** | Hiện **chưa kích hoạt**. Chưa có chuỗi bằng chứng được trình đủ để đáp ứng WHY-10. Đây là trạng thái thiếu căn cứ hiện tại, không phải chứng minh mọi GNN thất bại. |

Việc tìm không thấy từ “ngữ cảnh” hoặc “GNN” trong báo cáo G2 không đủ để chứng minh tuyệt đối rằng không có hiện tượng liên quan. Nhưng trách nhiệm vẫn thuộc bên đề xuất C15: phải chỉ ra hiện tượng, thông tin quan hệ cần dùng và phép thử phân xử. Hiện chưa có lý do để cam kết cài.

### 13 task chính

Đề xuất chung cho các task: Codex làm, Claude phản biện; Minh quyết phân công khi duyệt SPEC. Mỗi task đều bao gồm tự kiểm, đọc trung gian, phân tích kết quả trong phạm vi của nó, lưu lượt hỏng, tài liệu và bàn giao. Những việc đó không được dồn sang task cuối.

| Task và loại việc | Công việc, đầu ra cụ thể | Phụ thuộc và phép kiểm kết thúc |
|---|---|---|
| **M1 — Thiết kế phương pháp và giao thức** — thiết kế | Viết giả thuyết riêng cho phát hiện/RCA; chọn ứng viên để thử, mức graph, nguồn cạnh, tập ứng viên; lập bảng baseline; quy định nền, hiệu chỉnh, cảnh báo, chấm điểm, biên file và nhánh rẽ. Chốt giao diện sớm cho P8/P9. | Đọc trực tiếp MRP, G2, T-040 và hồ sơ phương pháp liên quan. Xong khi mỗi lựa chọn có phương án khác, phép bác bỏ, đầu vào cần và task thực hiện; không đòi đã có kết quả dev mới. |
| **M2 — Chứng cứ trace và quan hệ theo thời gian** — cài đặt, kiểm chứng | Dùng lại adapter/cửa sổ P3 và builder P5; bổ sung chỉ mục request/span, thời điểm chứng cứ khả dụng, ánh xạ owner–caller–callee và đại lượng trace cần cho ứng viên. Không dựng lại graph đã hợp lệ. | Sau giao diện M1. Kiểm trên dữ liệu giả có đáp án tính tay: mất cha, nhiều root, span chồng lấn, đến muộn; đối chiếu mẫu thật của cả TT và OB. Chỉ dùng chứng cứ đã khả dụng tại thời điểm quyết định. |
| **M3 — Metric, log, nền và chuẩn hóa** — cài đặt, phân tích | Dùng lại adapter TT/OB; giữ scope service/thao tác/tài nguyên chung; tạo nền nhân quả và trạng thái thiếu dữ liệu; bổ sung chứng cứ cần cho lỗi return. Không nhân một metric chung thành nhiều bằng chứng độc lập. | Sau M1; làm song song M2 được. Kiểm tính tay các phép chuẩn hóa, nền hằng/thưa, tín hiệu tăng/giảm, log trùng và alias. Đối chiếu ca đúng/sai có cùng điều kiện; tín hiệu không phân xử được phải ghi rõ. |
| **M4 — Điểm và xếp hạng RCA ứng viên** — cài đặt, thực nghiệm sớm | Cài cơ chế được M1 giao thử, nối điểm thành thứ hạng và giữ chứng cứ giải thích. Dùng bản ghi/bộ chấm P3 ngay từ đầu. Thử cặp có/bỏ quan hệ trước khi mở nhiều cấu hình. | Cần đầu ra M2/M3 mà công thức sử dụng. Kiểm đường đầu vào → điểm → thứ hạng, hòa điểm, root thiếu tín hiệu/cạnh và ca đúng bị hỏng. Chọn cách xếp hạng theo chất lượng của chính nó, gồm MRR; không chọn theo độ chênh có–không graph. |
| **M5 — Phát hiện và vùng nghi ngờ** — cài đặt, thực nghiệm sớm | Cài điểm hệ thống thực sự dùng quan hệ, nền/ngưỡng, mở–duy trì–đóng cảnh báo và vùng nghi ngờ. Tách điểm thô, sự kiện và thông báo. Thực hiện kiểm tương lai/biên file và lượt thử ghép cặp trên TT. | Cần M1, phần cần thiết của M2/M3; không bắt buộc chờ RCA “thắng”. Kiểm cảnh báo trên tín hiệu giả, thay đổi cạnh, thời điểm khả dụng và phục hồi. Xong về kỹ thuật không đồng nghĩa đã chứng minh dùng được trong vận hành. |
| **M6 — Cài và kiểm baseline phát hiện** — cài đặt, kiểm chứng, thực nghiệm | Cài baseline thống kê và trace đã được chọn để thử trong M1. Ghi đúng bản gốc/biến thể; dùng chung giao diện điểm–cảnh báo–trạng thái. Tái sử dụng N-Sigma và hồ sơ T-015; không gọi luật span hiện có là detector hoàn chỉnh. | Bắt đầu sau M1 và khi đầu vào cần thiết của M2/M3 có sẵn; có thể song song M4/M5. Kiểm oracle, tính nhân quả, trạng thái thiếu nền, tiền xử lý và phép chấm; chạy dev theo cấu hình đã khai. BOCPD/GDN nếu chọn nhận từ C8/C12, không cài trùng. |
| **M7 — Đối chứng cấu trúc** — cài đặt, kiểm chứng | Cài bỏ quan hệ, graph ngẫu nhiên giữ bậc và graph tĩnh có điều kiện. Khai chính xác thông tin cấu trúc còn giữ trong từng nhánh. Giữ cùng tín hiệu, coverage và ngân sách ở phần không chủ ý thay. | Sau khi giao diện tính của M4/M5 đủ rõ; không phải chờ chúng thắng. Kiểm đồ thị sinh ra, tập nút, hướng/bậc và đường tính sử dụng cạnh. Nhánh giữ self-time vẫn dùng cây span, không được gọi là hoàn toàn không cấu trúc. |
| **M8 — Điều phối ma trận và dùng lại trung gian** — kỹ thuật | Mở rộng runner/cache từ P3 cho cấu hình P6. Khóa khóa cache theo dữ liệu, phép biến đổi, cấu hình và revision thực sự ảnh hưởng kết quả. Đo bộ nhớ, đĩa, thời gian từng giai đoạn; xử lý đúng nút thắt nếu đã đo thấy. | Giao diện M2–M7 ổn định ở phần cần chạy. Kiểm chạy tiếp sau ngắt, không mất lượt hỏng, cache không lấy nhầm kết quả và đầu ra tương đương đường chạy sớm. Không dựng bộ chấm thứ hai. |
| **M9 — Ma trận dev RE2-TT** — thực nghiệm | Chạy chế độ (a), (b), các cấu hình/đối chứng đã khai; dùng lại bản ghi sớm nếu phép tính và đầu vào tương ứng không đổi. Báo theo ca/ô, tình trạng không cảnh báo, thiếu nền và lỗi. | Sau những thành phần được dùng của M4–M8 và nhánh baseline liên quan. Đủ ma trận, không bỏ ca khó; tách chất lượng detector, RCA tại cùng mốc và thành công toàn chuỗi. |
| **M10 — Ma trận dev Nezha-OB** — thực nghiệm | Chạy chế độ (a), với giới hạn cửa sổ/kênh đã có. Đối chiếu lỗi return, mạng, node thiếu trace và graph tĩnh. | Sau các thành phần tương ứng; có thể độc lập M9. Không dựng chế độ (b) từ trace/log đã cắt quanh mốc tiêm. Báo đầy đủ ca không hỗ trợ và yếu tố thay cùng. |
| **M11 — Độ nhạy, cơ chế và lựa chọn** — phân tích, thực nghiệm phân xử | Phân tích ca thắng/hòa/thua, nguồn tín hiệu, cửa sổ/nền, cách gộp, chính sách cảnh báo và cấu trúc. Chạy phần độ nhạy cần để phân biệt các giải thích dẫn tới lựa chọn khác nhau. Chọn detector và ranker bằng tiêu chí riêng. | Cần kết quả liên quan của M9/M10 và các nhánh được kích hoạt. Xong khi có lựa chọn được hỗ trợ, hoặc có bác bỏ/OPEN với bằng chứng thiếu cụ thể; không chỉ hoàn thành bảng số. |
| **M12 — So sánh cuối trên dev và kiểm toàn chuỗi** — thực nghiệm, kiểm chứng | Hoàn thành các cặp so sánh còn thiếu theo thiết kế được chọn; chạy baseline tại báo động mới khi cần. Kiểm điểm nối detector → cửa sổ RCA → thứ hạng → gói bằng chứng. Dùng lại P3 ở phần không đổi. | Không nhận thiết kế/cài phương pháp mới. Phải có baseline và đối chứng hợp lệ trước khi chạy phần so sánh phụ thuộc. Nếu cần thay thiết kế, quay đúng task sở hữu và chạy lại phần bị ảnh hưởng. |
| **M13 — Hồ sơ G3 và bàn giao** — tài liệu, bàn giao | Tổng hợp đặc tả, code/config, bảng kết quả, phạm vi kết luận, lỗi/nhánh dự phòng, giao thức P7 và giao diện P8/P9/P10. Ghi những phần còn thiếu để Minh quyết. | Chỉ tổng hợp bằng chứng đã có; không giấu cài đặt hoặc thực nghiệm mới. Không tự duyệt G3, mở test, commit hay coi kết quả âm là lỗi phải sửa cho thắng. |

**Vì sao gộp như vậy:** M2 gộp các bước cùng đi qua span/request; M3 gộp các phép cần thống nhất scope và nền; M4 giữ điểm và xếp hạng trong cùng chuỗi kiểm chứng; M5 giữ điểm hệ thống, trạng thái cảnh báo và vùng được xuất ra cùng thời điểm. M6 được tách vì baseline có nguồn, giả định và phép kiểm độc lập với phương pháp mới. M9/M10 tách vì hai dataset có giao thức và khả năng quan sát khác nhau.

Đây là lý do theo quan hệ công việc. Tôi chưa có căn cứ khẳng định mỗi task tương ứng đúng một cuộc trò chuyện hoặc một số giờ cố định.

### 15 task có điều kiện

Mỗi nhánh chỉ được kích hoạt khi có quyết định thiết kế hoặc câu hỏi phụ thuộc rõ ràng. “Có điều kiện” không có nghĩa được bỏ nghĩa vụ nghiên cứu bằng cách không kích hoạt.

| Nhánh | Điều kiện kích hoạt | Đầu ra và nơi sử dụng |
|---|---|---|
| **C1 — Phần thời gian span chưa được con phủ** | Công thức cần UV-2; giả định thời gian đủ kiểm được | Phép hợp khoảng có oracle chồng lấn/thiếu con/bất đồng bộ; đưa vào M2, M4/M5 |
| **C2 — Phần dư bằng hồi quy có điều kiện** | M1 chỉ ra thay đổi cụ thể so với nhánh đã có bằng chứng bất lợi | Mô hình, đối chứng bỏ quan hệ, kiểm nền và phần dư; M4/M5/M11. Không là phương án cứu mặc định |
| **C3 — Phân xử bước chọn tập của TraceRCA** | Lựa chọn phương pháp hoặc baseline phụ thuộc câu còn mở về singleton/frontend | Dùng trung gian đã có trước; bổ sung đúng cặp so sánh cần thiết; đầu ra phân biệt nguyên nhân hoặc giữ OPEN |
| **C4 — Ứng viên chấm theo tập** | C3/G2 cung cấp dự đoán cần thử cho cách chấm này | Cài điểm tập, oracle và đối chứng; đưa vào M4/M11 |
| **C5 — Nhánh tác giả TraceRCA thành baseline bổ sung** | M1 xác định phép so mà baseline hiện hành chưa trả lời | Adapter, quy ước biến thể, kiểm đúng và kết quả dev; đưa vào M12 |
| **C6 — Phần cơ chế MicroRank còn chưa phân xử** | Việc chọn cơ chế hoặc baseline phụ thuộc phần còn mở sau đổi bộ chia/đếm | Phân tích trung gian và ca đối chiếu; không tự mở lại toàn bộ task cũ |
| **C7 — Biến thể MicroRank làm baseline RCA** | C6/M1 chỉ ra mục đích và phạm vi hợp lệ | Adapter/biến thể được kiểm cùng kết quả dev; không mặc nhiên được dùng ở chế độ (b) |
| **C8 — BOCPD nhân quả** | Có câu hỏi riêng về tiền xử lý nhìn trước hoặc đối chứng điểm đổi chưa được M6 cung cấp; nếu là baseline được chọn ở M6 thì gộp thực hiện, không đếm hai lần | Một task gồm biến thể, kiểm số học, chạy toàn dev được duyệt và đo chi phí; không tách thành ba task chỉ theo batch |
| **C9 — Underflow của tiền xử lý lịch sử** | Kết luận cơ chế hoặc việc sử dụng số lịch sử phụ thuộc phần chưa kiểm | Phân xử trên phần còn lại, giữ lịch sử; không đồng nhất với C8 |
| **C10 — Nhãn/nhóm lan truyền** | Muốn đưa ra kết luận theo lan/không lan hoặc dùng giả thuyết tự sinh/kế thừa | Kiểm nguồn nhãn độc lập và khả năng phân xử. Nếu dữ liệu không đủ, báo giới hạn; không lấy cờ của phương pháp làm nhãn |
| **C11 — OM-07** | Một kết luận P6 thực sự phụ thuộc vấn đề này | Thu đúng bằng chứng còn thiếu theo phạm vi Minh duyệt; không mở lại toàn P5 |
| **C12 — GDN làm baseline** | Có câu hỏi khoa học, thay đổi cụ thể so với T-018 và dự đoán có thể bác bỏ; dữ liệu học/hiệu chỉnh hợp lệ, chi phí khả thi. Không kích hoạt chỉ để có tên GNN | Adapter, chuẩn hóa/ngưỡng hợp lệ, kiểm dự báo–điểm–cảnh báo, seed và kết quả dev; cung cấp cho M6/M12 |
| **C13 — Thẩm định nguồn dữ liệu phát hiện bổ sung** | M1 xác định khoảng trống công khai không thể phân xử bằng nguồn hiện có; có thể kích hoạt sớm từ M1, dùng lại hồ sơ P2 | So hồ sơ nguồn, giấy phép, schema, nền/onset, clock, dung lượng và cách chia. GAIA/MicroSS/Eadro là ứng viên, không mặc nhiên được nhận |
| **C14 — Adapter và thực nghiệm trên nguồn dev bổ sung** | C13 đạt và Minh duyệt nguồn, phạm vi truy cập/tải, cách chia | Cài adapter, kiểm thời gian/nhãn/đầu vào rồi chạy ma trận detector trên phần dev được phép. Kết quả vào M11/M12; dữ liệu giữ ngoài vẫn khóa |
| **C15 — GNN của phương pháp đề xuất** | Hiện chưa kích hoạt; chỉ xét khi đủ điều kiện WHY-10 và có giả thuyết riêng về quan hệ phụ thuộc. Chưa đủ căn cứ không đồng nghĩa bất khả thi | Cài biến thể dùng quan hệ được chọn, đối chứng và kiểm huấn luyện. Tách khỏi C12 vì “GDN làm đối thủ” không đồng nghĩa “chọn GNN làm phương pháp của mình” |

C13 và C14 tách vì **chấp nhận một nguồn dữ liệu** và **tích hợp, thực nghiệm trên nguồn đã chấp nhận** có đầu ra và quyền truy cập khác nhau. Không coi “đã khảo sát dataset” là đã tính xong phần sử dụng nó.

C12/C15 có thể dùng chung môi trường và thành phần đã kiểm nếu phù hợp; không huấn luyện hay dựng adapter trùng chỉ vì chúng có hai mục đích nghiên cứu.

### Quy tắc rẽ hướng tách riêng cho phát hiện và RCA

| Quan sát sau lượt thử hợp lệ | Phát hiện — M5/M6/M11 | RCA — M4/M11 |
|---|---|---|
| Cài đặt/trung gian sai | Sửa đúng bước; chưa đánh giá giả thuyết | Tương tự |
| Quan hệ đổi phép tính nhưng không giúp chất lượng | Báo đánh đổi cảnh báo sai–bỏ sót–độ trễ; xét bác bỏ ứng viên | Báo ca thắng/thua, MRR và nhóm điều kiện; xét bác bỏ ứng viên |
| Chỉ giảm số thông báo nhờ thời gian trơ | Không nhận là detector phân biệt tốt hơn | Không suy chất lượng RCA tăng từ ít lượt gọi hơn |
| Thứ hạng tốt hơn nhưng cảnh báo không đổi | Chưa có bằng chứng cải thiện phát hiện | Có thể là bằng chứng dev cho RCA, với giới hạn tương ứng |
| Thiếu tín hiệu hoặc nhãn cần thiết | Giao phần thiếu cho C13/P9/P10 hoặc giữ kết luận OPEN | Giữ ca trong mẫu số; phân biệt thiếu quan sát với tính điểm sai |
| Dự đoán được hỗ trợ ở nhóm phù hợp | Mở rộng kiểm dev và độ nhạy | Tương tự; chưa khẳng định tổng quát trước P7 |

Một kết quả âm sau phép thử hợp lệ có giá trị nghiên cứu. Nhưng **chưa tìm được cơ chế để thử** không đồng nghĩa đã hoàn thành nghĩa vụ thiết kế P6. Khi đó phải trình rõ phần thiếu và hướng xử lý; không tự thay mục tiêu bằng một detector không dùng quan hệ.

### Giao thức phát hiện phải có ngay trong M1

- Giữ riêng kết quả P3 theo giao thức cũ và kết quả P6 theo giao thức mới; không trộn độ đo khác nghĩa.
- Nền, hiệu chỉnh, thời gian khởi động và cập nhật chỉ dùng thông tin hợp lệ; không cắt theo mốc tiêm rồi gọi là tự phát hiện.
- Kiểm bất biến với phần tương lai khi lịch sử được phép nhìn thấy giữ nguyên.
- Phép đổi điểm bắt đầu không chứng minh đoạn khởi động sạch; nền còn phụ thuộc nguồn, cách chia và giả định đã khai trong M1.
- Kiểm độ nhạy với thời điểm bắt đầu quan sát: độ lệch khác nhau giữa các ca, sinh theo quy tắc/seed khai trước, không chọn theo nhãn; giữ toàn bộ lượt. Phân biệt thiếu lịch sử với bám vị trí sự cố.
- Đếm riêng cờ, sự kiện và thông báo. Đo precision/recall/F1, độ trễ theo loại mốc thật sự có, cảnh báo trước tiêm theo proxy, thời gian duy trì cảnh báo và khả năng phục hồi.
- Chỉ gọi là tỷ lệ cảnh báo sai trong vận hành khi có nền phù hợp đã được xác minh. Không tự đặt một ngưỡng “chấp nhận được” bằng con số chưa có căn cứ.
- Với RCA, báo cả chế độ biết mốc, RCA tại cùng báo động, và thành công toàn chuỗi. Thời điểm trả được thứ hạng phải tính cả cửa sổ dữ liệu cần chờ.
- Vùng trên dữ liệu công khai được gọi đúng là vùng nghi ngờ; không chấm như vùng ảnh hưởng thật khi thiếu nhãn.

### Khối lượng thực nghiệm và cách dùng lại kết quả

Phạm vi nền vẫn là **30 ca TT cho hai chế độ và 22 ca OB cho chế độ (a)**. Một cấu hình có đủ ba nhánh đó tương ứng:

\[
30+30+22=82\ \text{đơn vị ca–chế độ}.
\]

Nhưng không lấy 82 nhân một số cấu hình đặt trước để coi là đã biết toàn bộ chi phí. M1 phải xác định các tập hữu hạn:

- Cấu hình RCA và detector được thử.
- Các cấu hình đối chứng tương ứng.
- Seed của phương pháp ngẫu nhiên.
- Lượt thay thời điểm bắt đầu quan sát.
- Biến thể độ nhạy có câu hỏi cần phân xử.

Ví dụ, số lượt đánh giá RCA biết mốc là \(52K_a\); số lượt phát lại detector TT là \(30K_d\). Các lượt đổi điểm bắt đầu được tính riêng theo số lịch phát lại đã khai. Nhiều detector có thể dùng chung một lần trích đặc trưng nếu dữ liệu và phép trích giống nhau.

Tại **một bộ báo động mới**, phạm vi ranker chế độ (b) hiện hành có trần đếm theo cách cũ là:

\[
30(1_{\text{BARO}}+1_{\text{CIRCA}}+3_{\text{seed TORAI}})=150.
\]

Đây không phải tổng P6, cũng không phải cam kết mọi ca đều có báo động hợp lệ. Mọi bổ sung SimpleRCA, TraceRCA hoặc MicroRank phải cộng từ phạm vi đã xác định, không giữ số 240 mặc định.

**Không cộng lại** lượt M4–M6 vào M9–M12 nếu chúng đã có đúng đầu vào, phép tính và cấu hình cần dùng. Không chạy lại toàn bộ P3 chỉ vì có phương pháp mới.

Thời gian máy, RAM, đĩa của những phép tính mới hiện **chưa đo**. Chi phí agent đọc/sửa/phân tích và thời gian chờ phản biện cũng **chưa có ước lượng đáng tin**. Các task cài đặt phải đo ngay từ lượt đầu; M8 tổng hợp theo toàn ma trận. Tôi bỏ các khoảng giờ và tỷ lệ dự phòng không có căn cứ của bản đầu.

### Phụ thuộc và song song

```text
M1
 ├─ M2 ─┐
 ├─ M3 ─┼─ M4: RCA ─────────┐
 │      ├─ M5: phát hiện ────┼─ M7: đối chứng
 │      └─ M6: baseline ─────┘
 └─ Các nhánh được kích hoạt ──┐
                               ↓
                    M8: chạy ma trận
                       ├─ M9: TT
                       └─ M10: OB
                               ↓
                    M11: phân xử/chọn
                               ↓
                    M12: so sánh còn thiếu
                               ↓
                    M13: hồ sơ G3
```

M8 có thể được chuẩn bị từ khi giao diện ổn định, không cần chờ mọi phân tích khoa học kết thúc. M2/M3 và các phần độc lập của M4/M5/M6 có thể làm song song. M9/M10 độc lập về dữ liệu, nhưng chỉ chạy đồng thời nếu bộ nhớ cho phép; không chạy việc nặng khác trong lúc đo chi phí.

Phản biện nằm trong vòng đời từng task. Phát hiện cần sửa quay về đúng nơi sở hữu; không tạo task mới chỉ vì có thêm một lượt phản biện, và không cam kết “chỉ một lượt cuối rồi dừng”.

### Đối chiếu toàn bộ 34 + 15 task của bản đầu

Các mã T bên trái dưới đây là **mã dự kiến trong bản kế hoạch cũ**, không phải task đã được tạo.

| Phần cũ | Xử lý trong bản này |
|---|---|
| 041, 043, 060 | M1; phần cài hợp đồng đi cùng M2/M3/M6 |
| 042 | Đo tại module tương ứng, tổng hợp ở M8; bỏ task kiểm khả thi chung chung |
| 044–047 | Gộp M2; dùng lại adapter/builder hợp lệ |
| 048–050, 066 | Gộp M3 |
| 051, 054 | M4; phần điểm phục vụ cảnh báo thuộc M5 |
| 052–053 | M5 |
| 055–056 | M8; bản ghi/bộ chấm dùng ngay từ M4–M6 |
| 057–059 | M7 |
| 061–062, 080–082 | C8; một phần việc BOCPD nhân quả, không chia theo ba batch |
| 063–064 | M12 với phạm vi ranker đã sửa |
| 065 | C10; M11 theo dõi kết luận nào phụ thuộc |
| 067 / 068 | M9 / M10 |
| 069–071 | M11 |
| 072 | Kiểm tại M4–M8 khi cài; đối chiếu toàn chuỗi ở M12 |
| 073–074 | Giao diện sớm ở M1, bàn giao hoàn chỉnh ở M13 |
| 075 | C2 |
| 076–077 | Gộp C3 |
| 078 / 079 | C4 / C6 |
| 083 | Nhánh xử lý nút thắt đã đo trong M8 |
| 084 / 085 / 086 | C5 / C7 / C11 |
| 087–089 | Gộp C9 |

Như vậy, không bỏ sót mã nào trong 49 đề xuất cũ. So với bản 12 + 11:

- Thêm **M6** vì cài/kiểm baseline phát hiện là công việc bắt buộc phải có người nhận.
- Giữ M1–M5; M6–M12 cũ chuyển thành M7–M13.
- Thêm **C12–C15** để tách rõ GDN baseline, thẩm định dữ liệu, sử dụng dữ liệu đã nhận và GNN của phương pháp. Đây là những việc có điều kiện khác nhau, không được ngầm dồn vào M11/M12.

### Phạm vi file cho các task tương lai, chưa được phép triển khai

Kế hoạch được lưu tại `docs/PLAN-P6.md` theo yêu cầu mới của Minh. File này chứa tổ chức công việc và trạng thái ứng viên; không thay MRP, WHY hoặc DECISIONS.

Khi từng SPEC được duyệt, mã mới dự kiến nằm dưới `D:/RCA-flashticket/src/p6/`:

| Chủ sở hữu | Module dự kiến |
|---|---|
| M1 | Hợp đồng/API và đặc tả phương pháp trong đầu ra task |
| M2 | `trace_evidence.py` |
| M3 | `signals.py`, `normal_reference.py` |
| M4 | `ranking.py` |
| M5 | `detection.py`, `regions.py` |
| M6 | `baselines/` cho các bộ được chọn |
| M7 | `controls.py` |
| M8 | `runner.py`, phần mở rộng đánh giá cần thiết |
| M9–M13 | Kết quả, phân tích và tài liệu; không mặc nhiên có quyền sửa lõi |
| Các nhánh C | Module và đầu ra đúng biến thể được duyệt; không sửa bản P3 lịch sử |

Đầu ra mỗi task nằm trong `D:/RCA-flashticket/results/<mã-task>/`; SPEC/LOG/REVIEW theo cấu trúc hiện hành. Các thay đổi mã dùng chung hoặc WHY chỉ được ghi khi SPEC/phạm vi tương ứng được Minh duyệt. Quyền lưu kế hoạch hiện tại gồm ghi quyết định và con trỏ STATE; không cấp quyền sửa AGENTS hoặc thực hiện các module trên.

## 4. Bằng chứng GDN và giới hạn đã đính chính

**Về bằng chứng GDN: có một chỗ trộn hai cách tính khác nhau.**

Tôi đã đối chiếu kết quả gốc và kiểm hash của 10 file liên quan; đều khớp manifest lưu ở T-020.

| Kết quả trên các đoạn dev tách khỏi tập học | Chuẩn hóa theo toàn đoạn đang chấm | Chuẩn hóa bằng thống kê kiểm định cố định |
|---|---:|---:|
| Học 1 ca: tỷ lệ tick báo động | 23,62% | 99,58% |
| Học 5 ca: tỷ lệ tick báo động | 10,82% | 99,58% |
| Học 10 ca: tỷ lệ tick báo động | 4,95% | 45,15% |
| Học 10 ca: số tick báo động trên ca R-ca | **0** | **702** |

Nguồn: [kết quả phân tích T-018](../results/T-018/runs/b6b7-phan-tich.json), các nhánh `luot/<tên lượt>/giu_ngoai_code`, `giu_ngoai_b` và `ca_rca`; lượt 10 ca là `l7-lstar-n10-seed5`.

Cột thứ nhất dùng thống kê của cả đoạn được chấm, gồm dữ liệu tương lai. Tôi đã đối chiếu lại đúng [revision code GDN đã dùng](https://github.com/d-ailin/GDN/blob/9853899da860682669a134e4af315d036aab4eca/evaluate.py#L44-L62). Vì vậy:

- Không thể dùng **4,95%** làm bằng chứng về khả năng phát hiện trực tuyến của biến thể chuẩn hóa cố định.
- Câu “mô hình 10 ca không báo động ở R-ca” chỉ đúng với cách tính thứ nhất. Biến thể thứ hai báo **702 tick**; chưa phân tích vị trí các tick thì cũng chưa được gọi đó là phát hiện đúng.
- Đây là báo động trên các đoạn **được giả định bình thường vì nằm trước mốc tiêm**. Chưa có xác nhận sức khỏe độc lập để gọi toàn bộ chúng là báo sai vận hành.

Kết quả vẫn cho thấy vấn đề nghiêm trọng: **cấu hình GDN chuẩn hóa cố định đã thử chưa tạo được nền đủ yên trên những đoạn này.** Chính [WHY-18](WHY.md) đã ghi trạng thái “chưa đạt”, không phải cấu hình P3 được chọn.

Hai nhận định khác cũng cần giới hạn:

- Mất 23/25 cột `_error` là mất phần lớn **nhóm cột error**, không chứng minh gần như mất mọi tín hiệu sự cố. Latency, CPU, memory, socket… vẫn có thể chứa triệu chứng.
- “Có ít service gốc nên mô hình có giám sát **sẽ học thuộc**, do đó **không khả thi**” mạnh hơn bằng chứng. [WHY-10](WHY.md) nêu nguy cơ học thiên lệch về tập service và yêu cầu đánh giá phù hợp; chưa có phép thử chứng minh kết luận bất khả thi. Cách nói đúng là **chưa đủ căn cứ ưu tiên hướng này với dữ liệu và giao thức hiện tại**.


Nguồn ghi chi phí: results/T-005/runs/ket-qua-do.jsonl, bản ghi muc=gdn_hoc: method_s=1028.822, tong_s=1035.18; results/T-018/runs/b6b7-phan-tich.json#/luot/l7-lstar-n10-seed5/s_hoc=1928.69. Đây là thời gian máy của những lượt đã đo, không phải giờ công agent hoặc dự toán đầy đủ C12. Ngoại suy khoảng 20 giờ chưa kiểm không được dùng làm lý do chia task hay kết luận bất khả thi.


## 5. Bao phủ yêu cầu, dùng lại và các phụ thuộc còn mở

Bảng này chỉ lập chỉ mục tới phần việc đã có trong bản hợp nhất, không thêm nhiệm vụ hay cổng mới.

| Yêu cầu / nguồn | Dùng lại và phần còn thiếu | Chủ sở hữu / giới hạn kết luận |
|---|---|---|
| DT18-NV2, MRP §2–3: phép tính dùng cạnh | Builder và hợp đồng P5; công thức cụ thể chưa chọn | M1, M2–M5; M7/M11 phân xử quan hệ, P7 kiểm lợi ích sau khóa |
| Ánh xạ log/trace/metric và scope | Adapter P3, mapping P5; cần chứng cứ và thời điểm khả dụng cho phép tính mới | M2/M3; không nhân metric chung thành phiếu độc lập |
| Phát hiện và cảnh báo có tính áp dụng | Dùng kết quả/hồ sơ P3; nguồn nền và hiệu chỉnh mới chưa chốt | M1/M5/M6/M9/M11/M12; C13/C14 khi dữ liệu không đủ |
| Xếp hạng và vùng | Bộ chấm/bản ghi P3; chưa có nhãn vùng thật trên nguồn công khai | M4/M5/M7/M11; không gọi vùng nghi ngờ là vùng ảnh hưởng đã xác nhận |
| Đối chứng, baseline đủ mục đích | Giữ bộ P3 trong miền tương đương; bổ sung phải có câu hỏi | M1/M6/M7/M12, C5/C7/C8/C12 khi kích hoạt |
| Câu OPEN P4/P5 | Đọc code/trung gian trước; ca sai và ca đúng tương ứng | C1–C11 và M11 theo đúng quyết định phụ thuộc; không mặc nhiên mở lại P5 |
| Tính nhân quả theo thời gian, chống rò nhãn | Giao thức P3 và các đường rò đã biết ở T-018/T-033 | M1–M3/M5–M8; không dùng test chọn thiết kế |
| Lỗi, thiếu tín hiệu/nền, UNSUPPORTED, hòa điểm | Giữ mẫu số và trạng thái P3 phù hợp | M1/M4–M12; không bỏ ca khó hoặc đổi nghĩa độ đo |
| Tái lập, tài nguyên, lượt hỏng và phản biện | Runner/cache và môi trường hiện có | Tự kiểm tại task sở hữu; M8 tổng hợp; M13 chỉ bàn giao |
| G3/P7 | Khóa mã, cấu hình, giả thuyết, phép chấm và bảng diễn giải | M11–M13; Minh quyết G3 và quyền mở test riêng |
| P8/P9/P10 | T-040 bàn giao đầu vào, yêu cầu quan sát P9; cùng định dạng nội bộ | M1 giao diện sớm, M13 hoàn chỉnh; LLM không đổi hạng; vận hành thật chưa được chứng minh |

### Phụ thuộc nghiệm thu và dữ liệu

P5 đã đóng theo Q-176, không tự đóng từng task: T-034/T-038/T-040 chờ nghiệm thu; T-035 và gói SMTP V2 T-036 còn phản biện chính thức/nghiệm thu theo STATE. T-037/T-039 đã đóng. Không biến việc kiểm kỹ thuật đạt thành phản biện chính thức đã xong. Phần dùng graph tĩnh TT phải giữ điều kiện tiếp nhận/nghiệm thu T-038 theo bàn giao T-040.

Đọc nguồn thật trước phần phụ thuộc:

- [G2](../results/T-034/goi-g2.md), manifest hiện hành tại [manifest-cuoi-007](../results/T-034/runs/manifest-cuoi-007/manifest.json).
- [Bàn giao P6](../results/T-040/ban-giao-p6.md), [các mục còn mở](../results/T-040/con-mo.json), [yêu cầu P9](../results/T-040/yeu-cau-quan-sat-p9.md), [manifest T-040](../results/T-040/manifest.json).
- [WHY-10/WHY-18 và các giao thức đã duyệt](WHY.md), [MRP](MRP.md), [DECISIONS](DECISIONS.md); SPEC/LOG nguồn theo STATE.

Cạnh trace dev chưa xác nhận kiểu; không lấy kiểu tĩnh lấp vào trace. Không coi mô hình tĩnh là runtime đã xác minh. OM-07 chỉ mở theo C11 khi có phụ thuộc thật; OM-11/R-01…R-10 đã chuyển P9a theo Q-175, bộ yêu cầu được bổ sung sau và chưa gửi nhóm hệ thống. Không mở repo RCA lưu trữ.

Nguồn nền, số gập, số seed, độ dài warmup, ngưỡng chấp nhận và danh sách ứng viên cuối **chưa chốt**. “24 đoạn mỗi gập”, “20 giờ” và “khả năng cao cần C13” trong phản biện là giả định/ngoại suy, không phải cấu hình hoặc kết quả đã xác nhận. Chia theo ô là yêu cầu tránh các lần lặp ở hai phía; tổng quát sang service gốc chưa thấy cần giao thức chia phù hợp, không suy từ phép chia theo ô.

## 6. Bước tiếp theo và phạm vi ghi

Bước tiếp theo là **soạn và trình SPEC cho M1 trong chat**, dùng tasks/_MAU/SPEC.md, chưa tạo hay chạy task khi chưa có quyền cụ thể. Đọc AGENTS → STATE → Q-177/Q-178 → tài liệu này §1–§7, nguyên văn S05 và các nguồn khoa học trực tiếp chi phối. Kiểm danh sách tasks trước khi đề xuất mã T; không lấy các mã 041–089 lịch sử làm task đã tồn tại.

SPEC M1 cần nhận đủ đầu ra đã nêu trong bảng M1 và phần bổ sung nguồn nền/hiệu chỉnh: câu hỏi riêng cho detector/RCA, giả thuyết và phép bác bỏ, danh sách baseline hữu hạn, dữ liệu/nhãn/cách chia, mức/nguồn graph, hợp đồng thời gian–scope–trạng thái, ma trận thử và điều kiện kích hoạt nhánh. Phần chưa biết giữ OPEN có bằng chứng cần bổ sung và quyết định phụ thuộc. Các lựa chọn cần WHY được trình theo quyền, không ghi trước như đã chọn.

Lượt lưu kế hoạch chỉ ghi PLAN-P6.md, nối DECISIONS.md và sửa các câu trạng thái P6 trong STATE.md. Không sửa AGENTS/MRP/WHY, task cũ, kết quả, code hoặc dữ liệu. Chưa commit/push.

## 7. Nhật ký dựng lại và kiểm bản ghi

- Dựng từ nguyên văn S01–S16; bản 3 S12 là nền, sửa cuối S14 và kiểm lại S15 quyết định nội dung hợp nhất; S05 là đính chính trực tiếp của Minh. Không lấy bản tóm tắt sau nén làm nguồn.
- Mọi nội dung nguyên văn nguồn được giữ ở §9; các hạn chế ghi file của lượt PLAN cũ chỉ là lịch sử. Nguồn nguyên văn được chuẩn hóa xuống dòng LF, không viết lại câu.
- Kiểm danh mục M1–M13, C1–C15 và đối chiếu 041–089; kiểm các sửa về nền/hiệu chỉnh, baseline, GDN, nhánh dữ liệu, quyền hạn và thời gian.
- Kiểm hash 10 file T-005/T-018 theo input_manifest_frozen.inputs của results/T-020/manifest.json: khớp. Kiểm goi-g2.md theo manifest-cuoi-007 và ba file T-040 được dẫn ở §5 theo manifest gốc: khớp.
- Chỉ đọc nguồn/JSON/code và kiểm tài liệu; không chạy lại GDN hoặc thực nghiệm mới, không mở data/locked.
- Sau ghi: 16/16 nguồn nhúng khớp nguyên văn nguồn gốc; đủ M1–M13/C1–C15 và 49/49 mã cũ; liên kết nội bộ phần hiện hành tồn tại; prompt giữ nguyên khối chung/công đoạn/G3. Nội dung DECISIONS cũ (gồm Q-176 có sẵn) và mọi dòng task cũ của STATE được giữ; chỉ nối Q-177/Q-178 và đổi bốn câu trạng thái P6. Kiểm diff không có lỗi khoảng trắng; xuống dòng DECISIONS được chuẩn hóa. Ba file trong phạm vi; chưa commit/push.
- Bước khoa học tiếp theo chưa thực hiện: SPEC M1; chưa khóa giao thức detector, chưa lựa chọn thuật toán, chưa G3/test.

## 8. Prompt bàn giao để Minh chuyển khi cần

Lượt kiểm này nhằm đối chiếu bản ghi với nguồn và quyền được duyệt. Bước làm việc tiếp theo vẫn là trình SPEC M1; không tự gửi prompt hoặc khởi động phản biện.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: bản ghi kế hoạch P6 tại docs/PLAN-P6.md, docs/DECISIONS.md và các câu P6 trong docs/STATE.md.
- Công đoạn: soát kết quả.
- Gói/cổng: ghi lại kế hoạch P6 sau phản biện, trước G3.
- Người làm và người phản biện chính thức: Codex lập và ghi kế hoạch; Claude phản biện kế hoạch. Lượt này chỉ kiểm bản ghi, không tự mở lại phản biện toàn diện.
- Tài liệu gốc: docs/PLAN-P6.md §9 S01–S16; AGENTS.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/STATE.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md.
- Phản biện và phản hồi trước: nguyên văn S01–S16 theo thứ tự trong docs/PLAN-P6.md §9.
- Code và kết quả liên quan: results/T-005/; results/T-018/; results/T-020/manifest.json; results/T-034/runs/manifest-cuoi-007/manifest.json; results/T-040/manifest.json và các nguồn được kế hoạch dẫn. Chỉ đọc.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat; không sửa file, chạy thực nghiệm, mở dữ liệu khóa, tải dữ liệu, commit/push hoặc tự gửi prompt.

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

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.

Tài liệu đầu vào — nguyên văn đính chính của Minh (S05; giới hạn chỉ đọc trong lượt cũ là lịch sử, quyền lượt này ghi ở trên):

không ghi vào desision, không quan tâm đến số giờ của tôi vội, tôi cần bạn lập plan chia task trước.&#x20;

Tôi cần đính chính cách hiểu về “task vừa một phiên”, thời gian thực hiện và ngữ cảnh của agent trước khi tiếp tục chia kế hoạch P6.

Sau khi làm đến T-040, tôi nhận thấy cách agent ước lượng và chia task chưa sát thực tế. Tôi yêu cầu rà lại kế hoạch theo các điểm sau. Đây là yêu cầu phân tích và đề xuất trong chat, chưa cho phép sửa file.

**1. Phải phân biệt thời gian máy chạy với công việc của agent.**

Một task mất 4–5 giờ có thể chủ yếu là thời gian chạy script Python. Trong các task đã thực hiện, tôi quan sát thấy thời gian chạy script chiếm phần lớn. Khoảng thời gian này chủ yếu phụ thuộc CPU, RAM, dữ liệu và cách cài đặt; không thể quy đổi trực tiếp thành lượng ngữ cảnh agent sử dụng.

Agent vẫn cần đọc kết quả, kiểm tra trung gian, xử lý lỗi và diễn giải. Đó là phần việc cần đánh giá riêng. Một script chạy nhiều giờ nhưng chỉ cần kiểm tra vài đầu ra khác với nhiều giờ agent liên tục đọc tài liệu, sửa code và xử lý kết quả.

Vì vậy, tôi không chấp nhận lấy con số ước lượng kiểu “task này mất 4–5 giờ” làm căn cứ để kết luận vừa hoặc không vừa một phiên, rồi tách task. Nếu viện dẫn thời gian, phải nói rõ đó là thời gian máy chạy, thời gian agent xử lý hay thời gian chờ phản biện; có bằng chứng đo nào và phần nào chưa biết. Không gán những khoảng giờ có vẻ chính xác khi chưa có căn cứ.

**2. “Vừa một phiên” không phải một giới hạn giờ cứng.**

Không được trình bày đây là quy định của OpenAI. Cũng không được khẳng định đã ước lượng được lượng context của một task chỉ từ số file, số đầu việc hoặc số giờ chạy script.

Nếu chưa đo hoặc chưa có dữ liệu từ các task tương tự, hãy ghi chưa biết. Cần đánh giá khả năng giữ mạch công việc qua phạm vi tài liệu, số quyết định liên quan, lượng đầu ra cần đọc và độ phức tạp khi kiểm chứng.

Một task có thể có lượt chạy dài và nhiều lượt phản biện. Không đồng nhất task, một phiên trò chuyện và toàn bộ vòng đời làm–phản biện–sửa–nghiệm thu.

**3. Ngữ cảnh bị nén không tự động bắt buộc dừng phiên.**

Tôi đính chính cách áp dụng yêu cầu này: sau khi nén ngữ cảnh, agent cần kiểm tra khả năng tiếp tục đúng công việc, đối chiếu nguồn và khôi phục những thông tin cần thiết. Có thể tiếp tục nếu vẫn xác định được mục tiêu, quyền hạn, trạng thái, bằng chứng và bước tiếp theo.

Chỉ đề nghị chuyển phiên khi có lý do cụ thể như mất mạch, lặp việc, không phục hồi được thông tin cần thiết hoặc nguy cơ sai tăng rõ rệt. Không coi sự kiện nén ngữ cảnh tự nó là bằng chứng phải dừng hay phải chia nhỏ task.

Đính chính này không cho phép bỏ qua checkpoint, nguồn sự thật trong repo hoặc quyền ghi file.

**4. Chia task theo phần việc có đầu ra và phép kiểm rõ ràng; tránh chia nhỏ quá mức.**

Có thể chia theo module. Những phần liên hệ chặt, dùng chung đầu vào, trung gian, lượt xử lý hoặc tài nguyên có thể được gộp nếu giúp thực hiện và kiểm chứng hiệu quả hơn.

Không mặc định mỗi bước nhỏ, mỗi loại file hay mỗi thao tác kiểm tra phải thành một task riêng. Cũng không gộp chỉ vì cùng dùng CPU/RAM: phải chỉ ra lợi ích cụ thể và việc gộp có làm khó kiểm chứng, sửa lỗi hoặc nghiệm thu hay không.

Ưu tiên cao nhất vẫn là tính đúng đắn. Không cắt nhóm khó, giảm phép phân xử cần thiết hoặc thu hẹp câu hỏi nghiên cứu để làm cho task “vừa phiên”.

**5. Rà lại P6 trên cơ sở công việc đã có.**

P1–P5 đã tạo code, hạ tầng, giao thức và kết quả. P3 đã đánh giá các baseline trong phạm vi được duyệt. Phải xác định phần nào dùng lại được và phần nào P6 thực sự thay đổi trước khi đề xuất kiểm lại.

Không đặt một task “kiểm hạ tầng” hoặc “kiểm baseline” chung chung. Mỗi phần kiểm bổ sung phải nêu thay đổi hoặc khoảng trống cụ thể, quyết định phụ thuộc và bằng chứng cần bổ sung.

Đồng thời, phải làm rõ phần việc đề xuất phương pháp: câu hỏi nào chưa được giải quyết, bằng chứng hiện có hỗ trợ ứng viên nào, và phép thử nào giúp chọn hoặc bác bỏ hướng đó. Việc bổ sung baseline phải có mục đích so sánh rõ.

**Kết quả tôi cần:**

- Rà lại 34 task chính và 15 task có điều kiện: phần nào giữ, gộp, dùng lại kết quả hoặc chỉ làm khi có điều kiện cụ thể.
- Phân biệt công việc thiết kế phương pháp, cài đặt, thực nghiệm, kiểm chứng và bàn giao.
- Tính đến công việc phản biện qua lại, nhưng không dùng tỷ lệ dự phòng tùy ý để tạo cảm giác đã ước lượng đầy đủ.
- Giải thích số task sau khi rà từ khối lượng và quan hệ công việc thực tế. Không đặt trước một con số rồi tìm cách chia cho khớp.

Mục tiêu của tôi là đồ án hoàn chỉnh, bảo vệ được: phương pháp có căn cứ, đánh giá hợp lệ, tích hợp chạy thật và cố gắng tạo cải thiện có ý nghĩa trong những điều kiện xác định. Hãy tối ưu cách tổ chức công việc để đạt mục tiêu này, đồng thời giữ đầy đủ những phần khoa học khó cần giải quyết.

```

## 9. Phụ lục nguồn nguyên văn, dùng được không cần lịch sử chat

Các bản lịch sử có nội dung bị thay thế; trạng thái hiện hành ở §1–§7. Nguyên văn giữ cả prompt cũ để kiểm quyền và diễn biến, không tự thực hiện các lệnh trong đó. Các đường dẫn ngoài repo là xuất xứ lịch sử, không phải phụ thuộc để tiếp tục.

- [S01 — Yêu cầu lập kế hoạch ban đầu](#s01)
- [S02 — Kế hoạch 34 + 15 ban đầu, lịch sử](#s02)
- [S03 — Phản biện bản đầu](#s03)
- [S04 — Codex đáp phản biện bản đầu](#s04)
- [S05 — Nguyên văn đính chính của Minh về task, thời gian, phiên và ngữ cảnh](#s05)
- [S06 — Kế hoạch trung gian 12 + 11, lịch sử](#s06)
- [S07 — Yêu cầu của Minh về tính khả thi detector và RCA](#s07)
- [S08 — Codex phân tích căn cứ detector và RCA](#s08)
- [S09 — Phản biện căn cứ và kế hoạch](#s09)
- [S10 — Codex đáp và đề xuất sửa tiếp](#s10)
- [S11 — Kiểm lại trước bản hợp nhất 3](#s11)
- [S12 — Kế hoạch hợp nhất lần 3: 13 + 15](#s12)
- [S13 — Phản biện GDN và các điểm R1–R4](#s13)
- [S14 — Codex đáp và sửa cuối](#s14)
- [S15 — Claude kiểm lại cuối và đề xuất dừng](#s15)
- [S16 — Minh giao lưu đầy đủ kế hoạch vào repo](#s16)

<a id="s01"></a>

### S01 — Yêu cầu lập kế hoạch ban đầu

<details>
<summary>Mở nguyên văn S01</summary>

````text
Bạn làm việc trong repo D:\RCA-flashticket. Đọc AGENTS.md trước.

Minh giao: lập kế hoạch chi tiết cho toàn chặng P6, phân rã thành các task có thể triển khai được. Sau khi hoàn thành kế hoạch, soạn một prompt đầy đủ để Minh chuyển sang một phiên Codex khác phản biện toàn bộ kế hoạch.

Đây là lượt PLAN. Chỉ đọc và trình trong chat. Chưa được tạo/sửa file, tạo task chính thức, chạy thực nghiệm mới, mở test hoặc dataset giữ ngoài, tải dữ liệu, commit/push. Không tự mở phiên hay gửi sang agent khác.

## 1. Bối cảnh và mục tiêu

P5 và P6 là các chặng nghiên cứu; SPEC thuộc từng task cụ thể. Không tạo một task khổng lồ hoặc một “SPEC P6” thay cho việc phân rã toàn chặng.

Đọc quyết định hiện hành trong docs/DECISIONS.md, gồm ghi nhận đóng P5 ngày 18/10/2026. Phân biệt đóng chặng, nghiệm thu riêng từng task, kết luận khoa học và quyền G3/test. Không tự mở lại P5 hoặc biến các OPEN thành đã được giải quyết.

Mục tiêu lượt này là kế hoạch đủ sâu để người triển khai không tới lúc bắt tay làm mới phát hiện khối lượng vốn đã có thể biết và lại yêu cầu chia task. Phải khảo sát khối lượng trước khi chốt phân rã. Không giảm phép kiểm hoặc thu hẹp mục tiêu nghiên cứu để làm task trông vừa một phiên.

Không hứa nghiên cứu sẽ không có phát hiện mới. Phân biệt rõ:
- Công việc và rủi ro đã có thể nhận diện từ nguồn hiện có: phải được tính và chia ngay trong kế hoạch.
- Công việc phụ thuộc kết quả chưa có: phải có nhánh xử lý, task phụ thuộc dự kiến và tác động chi phí.
- Phát sinh thật sự chưa thể biết: nêu điều kiện phải trình Minh; không dùng nó làm lý do để bỏ khảo sát ban đầu.

## 2. Đọc nguồn trực tiếp

Không chỉ dựa vào STATE hoặc các bản tóm tắt. Đọc theo phụ thuộc, tối thiểu:

- AGENTS.md.
- docs/MRP.md: mục tiêu, RQ, P4–P7, giao diện với P8–P10, nguyên tắc thực nghiệm và G3.
- docs/reference/sources/DT18-de-tai-va-nhiem-vu.md.
- docs/reference/sources/advisor-2026-09-23.md.
- docs/LESSONS.md; phần WHY và DECISIONS trực tiếp chi phối.
- docs/review-prompt.md.
- tasks/_MAU/SPEC.md.
- SPEC, mục LOG liên quan và đầu ra gốc của T-034–T-040.
- results/T-034/goi-g2.md và các nguồn kết quả mà lập luận P6 phụ thuộc.
- results/T-040/ban-giao-p6.md, bao-cao-p5b.md, con-mo.json, yeu-cau-quan-sat-p9.md, dau-vao.json và manifest hiện hành.
- Đặc tả, hợp đồng, graph, ánh xạ, trung gian và mã thật của T-035–T-039 khi cần xác định đầu vào và khối lượng.
- src/do_thi/, src/do_thi_tinh/, các adapter và mã baseline sẽ tái sử dụng.
- Nguồn P4 trong T-032/T-033 theo con trỏ của G2 khi một lựa chọn cần bằng chứng cơ chế.

Đọc yêu cầu và đầu ra gốc trước kết luận review cũ. Trước khi dùng kết quả cũ làm căn cứ, kiểm manifest phù hợp. Tách lệch pin lịch sử đã được giải thích khỏi lệch chưa được xử lý. Không sửa hoặc tự lập manifest để hợp thức hóa lệch.

Repo hệ thống FlashTicket ở D:/Project/flash-ticket-platform chỉ đọc, chỉ đọc nguồn cần thiết. Không đọc repo RCA lưu trữ D:/Project/flash-ticket-rca-research.

Các câu “SPEC P6” trong tài liệu cũ cần được hiểu theo đúng nội dung: đặc tả phương pháp và các SPEC task thuộc chặng P6; không mặc nhiên coi là yêu cầu tạo một task duy nhất.

## 3. Khảo sát trước khi chia task

Lập danh mục công việc thực tế, rồi mới quyết số lượng task. Không chốt trước một con số task cho đẹp.

Với từng nhóm việc:
- Chỉ ra module/API, schema, đầu vào và kết quả sẵn có; phần nào tái sử dụng được, phần nào phải viết hoặc kiểm lại.
- Xác định đơn vị xử lý: span, request, cửa sổ, graph, service/thao tác, cấu hình, seed, dataset và chế độ đánh giá.
- Tính số tổ hợp phải thực hiện từ phạm vi đề xuất. Tách số đã kiểm với dự toán.
- Tính cả đọc nguồn, thiết kế, cài đặt, fixture/oracle, kiểm trung gian, chạy dev, phân tích theo ca/ô, tài liệu, manifest, LOG và bàn giao.
- Ước lượng giờ công, thời gian máy, RAM, dung lượng, số lượt chạy và dự phòng sửa lỗi/hồi quy; nêu căn cứ hoặc khoảng bất định.
- Phân biệt thời gian máy có thể chạy độc lập với công việc cần agent theo dõi. Không mặc định chia một lượt chạy dài thành nhiều phiên sẽ tự giải quyết được mọi vấn đề.
- Kiểm phụ thuộc thật và giao diện giữa các phần; chỉ rõ phần có thể làm song song, phần bắt buộc tuần tự và xung đột ghi mã chung.

Không chạy benchmark/pilot mới trong lượt PLAN. Nếu thiếu phép đo khiến chưa thể ước lượng hoặc chốt phạm vi, nêu rõ và đặt một task khảo sát khả thi có đầu ra, ngân sách, tiêu chí quyết định và các nhánh kế tiếp đã được dự kiến. Không đánh tráo một kế hoạch chưa hoàn chỉnh thành kế hoạch triển khai toàn chặng đã chốt.

## 4. Nội dung nghiên cứu phải được phân công đầy đủ

Lập ma trận yêu cầu nguồn → bằng chứng hiện có → việc còn thiếu → task chịu trách nhiệm → quyết định được phép rút ra.

Kế hoạch phải xử lý đầy đủ phần P6 trực tiếp chi phối, gồm:
- Chọn mức đồ thị, nguồn cạnh và tín hiệu bằng căn cứ phù hợp.
- Ánh xạ log/trace/metric, giữ scope và tránh nhân tín hiệu dùng chung thành bằng chứng độc lập.
- Phép tính bất thường thực sự dùng quan hệ đồ thị.
- Phát hiện ở mức hệ thống, vùng nghi ngờ và xếp hạng nguyên nhân.
- Tách yêu cầu DT18, nhu cầu kỹ thuật, thành phần nhằm sửa hạn chế P4 và ứng viên chưa được kiểm.
- Các câu còn OPEN ảnh hưởng lựa chọn P6: cần kiểm gì, kiểm ở task nào, hay dữ liệu hiện tại không phân xử được.
- Đối chứng, baseline, ngân sách chọn cấu hình và kiểm hành vi trên dev trước G3.
- Chính sách thiếu tín hiệu/cạnh/nền, nút cô lập, ca lỗi, UNSUPPORTED, nhánh dự phòng, tập ứng viên, mẫu số và hòa điểm.
- Tiền xử lý chỉ dùng thông tin được phép ở thời điểm dự đoán; nhãn và mốc tiêm không lọt vào phương pháp.
- Phân tích độ nhạy, tính đúng giá trị trung gian và lưu bằng chứng cần để giải thích kết quả.
- Tích hợp các thành phần, kiểm toàn chuỗi và gói khóa thiết kế trình G3.
- Giao diện và nghĩa vụ chuyển sang P7/P9/P10.

Không mặc định khung bốn tầng hoặc bất kỳ ứng viên trong G2/bàn giao đã được chọn. Không yêu cầu cài mọi ứng viên chỉ vì chúng được liệt kê. Đề xuất cách thu hẹp có căn cứ, phép phân xử và nhánh xử lý nếu ứng viên bị bác bỏ.

Tách rõ công việc cài/kiểm đối chứng trên dev trước G3 với đánh giá lợi ích trên test ở P7. Không mở test để giải quyết lựa chọn thiết kế.

Không bỏ một nghĩa vụ nguồn bằng cách ghi “ngoài task”. Mọi phần chưa làm phải có nơi xử lý, lý do, bằng chứng thiếu và quyết định phụ thuộc.

## 5. Hồ sơ chi tiết cho từng task dự kiến

Kiểm thư mục tasks và mã đã dùng trước khi đề xuất mã mới. Các mã chỉ là dự kiến cho tới khi Minh duyệt.

Với MỖI task, trình đủ:
1. Mã/tên, loại task và câu hỏi nguồn.
2. Mục tiêu cụ thể; phần mục tiêu nghiên cứu được bao phủ.
3. Điều kiện bắt đầu và phụ thuộc tới đầu ra cụ thể của task trước.
4. Đầu vào: file, schema/API, revision/manifest, miền dữ liệu và quyền cần có.
5. Công việc theo bước; module/hàm dự kiến tái sử dụng hoặc bổ sung; không mô tả bằng câu chung như “cài phương pháp và kiểm”.
6. Ma trận cấu hình/phép kiểm/ca cần chạy, số tổ hợp dự kiến, thứ tự và cách dùng lại trung gian.
7. Đầu ra và phạm vi ghi dự kiến tới đường dẫn; quyền ghi mã chung hoặc tài liệu quyết định phải được tính trước.
8. Kiểm đúng đắn độc lập: đầu vào → xử lý → trung gian → đầu ra, oracle/fixture, kiểm không nhãn và hồi quy cần thiết.
9. Tiêu chí xong kiểm được; kết quả nào hỗ trợ, bác bỏ hoặc chưa phân xử; kết luận nào chưa được phép.
10. Giờ công, thời gian máy, RAM/disk và độ tin cậy dự toán; tính cả tự kiểm, ghi kết quả và bàn giao.
11. Rủi ro, phần chưa biết, nhánh xử lý đã dự kiến và ảnh hưởng tới task sau.
12. Vai trò dự kiến và điểm cần Minh quyết; không tự đổi phân công chính thức hoặc cấp ngoại lệ.
13. Vì sao task này vừa một phiên theo quy định repo.

Nếu một task vẫn chứa nhiều câu hỏi độc lập, nhiều thành phần mới hoặc tổ hợp chạy/kiểm quá lớn, chia ngay trong kế hoạch. Tránh những task cuối chặng mang tên “tổng hợp”, “tích hợp” hoặc “kiểm đầy đủ” nhưng thực tế còn giấu phần thiết kế/cài đặt lớn.

Không cần chép lặp toàn bộ boilerplate SPEC cho mọi task. Tuy nhiên mức chi tiết phải đủ để sau này viết SPEC không phải khám phá lại khối lượng và cấu trúc phân rã.

## 6. Đầu ra toàn kế hoạch

Trình:
- Mục tiêu P6 và ranh giới với các chặng khác.
- Bản đồ căn cứ/OPEN/quyết định.
- Danh mục module, dữ liệu và công việc thực tế đã khảo sát.
- Ma trận bao phủ yêu cầu.
- Danh sách task cùng hồ sơ chi tiết ở mục 5.
- Sơ đồ phụ thuộc và thứ tự triển khai; đường găng, phần song song có lợi và chi phí tổng.
- Các nhánh kế hoạch phụ thuộc kết quả; phân biệt task chắc chắn với task có điều kiện.
- Bảng kiểm khối lượng: phần nào từng dễ bị bỏ sót, đã được tính vào task nào; chứng minh không dồn việc chưa phân rã sang task cuối.
- Danh sách quyết định Minh cần duyệt, gom một lượt; khuyến nghị có lý do.
- File đề xuất để lưu kế hoạch và danh sách file cần tạo/sửa sau khi được duyệt. Lượt này vẫn chỉ trình trong chat.
- Tự soát toàn kế hoạch: tính đúng khoa học, đủ yêu cầu nguồn, tính khả thi từng phiên, ngân sách, phụ thuộc, quyền ghi và khả năng bàn giao sang máy/agent khác.

Không coi kế hoạch được duyệt là đã chọn thuật toán, xác nhận giả thuyết hoặc cấp quyền thực hiện mọi task.

## 7. Prompt cho phiên Codex khác phản biện toàn bộ

Sau khi kế hoạch hoàn chỉnh, soạn một prompt độc lập để Minh copy sang một phiên Codex mới khác phiên lập kế hoạch.

Prompt phải:
- Chứa hoặc kèm nguyên văn toàn bộ kế hoạch cần phản biện. Nếu kế hoạch chưa được phép lưu file, chỉ dẫn rõ Minh gửi kèm nguyên văn kế hoạch; không dùng đường dẫn tới file chưa tồn tại.
- Ghi vai trò: Codex phiên này là người lập kế hoạch; Codex phiên khác là người phản biện độc lập kế hoạch theo yêu cầu Minh. Phân công này chỉ áp dụng lượt kế hoạch, không tự áp sang phản biện kết quả các task sau.
- Chép nguyên văn Prompt chung + Khối “Soát SPEC” + Khối G3 hiện hành từ docs/review-prompt.md; chỉ điền thông tin trung tính.
- Đưa nguyên văn yêu cầu của Minh về độ chi tiết và việc khảo sát khối lượng trước khi chia task vào phần tài liệu đầu vào.
- Yêu cầu đánh giá TOÀN BỘ kế hoạch và các giao diện giữa task, không chỉ soát từng dòng riêng: độ khớp mục tiêu nguồn, căn cứ thiết kế, khả năng phân xử, phần bỏ sót/chồng lặp, khối lượng mỗi phiên, dự toán tổng, phụ thuộc, task có điều kiện, tích hợp và G3.
- Không kèm kết luận tự soát, số liệu lựa chọn để neo reviewer, gợi ý finding hoặc lời khẳng định kế hoạch đã an toàn.
- Chỉ cho phép đọc và trả lời trong chat; không sửa kế hoạch, chạy thực nghiệm mới, mở dữ liệu khóa, tạo phiên hoặc tự gửi prompt.
- Phản biện phải phân biệt lỗi kế hoạch thật với bất định nghiên cứu hợp lệ; không đòi kết quả của thực nghiệm chưa được duyệt và không thu hẹp mục tiêu cho vừa task.

Kết thúc lượt bằng báo cáo bốn mục theo AGENTS.md và prompt phản biện đầy đủ. Dừng ở trình kế hoạch; Minh quyết chuyển phản biện, sửa và duyệt.
````

</details>

<a id="s02"></a>

### S02 — Kế hoạch 34 + 15 ban đầu, lịch sử

<details>
<summary>Mở nguyên văn S02</summary>

````text
Tôi đề xuất **34 task trên đường triển khai chính và 15 task có điều kiện**. Số lượng này xuất phát từ phần việc đã khảo sát, gồm cả xử lý dữ liệu theo thời gian, kiểm trung gian, đối chứng và các nhánh nghiên cứu còn mở.

Đây là **kế hoạch đề xuất**, chưa phải quyền triển khai. Dự toán hiện tại vẫn cần task khảo sát khả thi để thay các khoảng ước lượng bằng số đo.

:::writing{variant="document" id="61427"}
KẾ HOẠCH TOÀN CHẶNG P6 — ĐỀ XUẤT ĐỂ PHẢN BIỆN

**1. Mục tiêu, trạng thái và ranh giới**

P6 phải tạo được một phương pháp nhận log, trace, metric và quan hệ đồ thị để:

- Tính điểm bất thường có sử dụng quan hệ.
- Phát hiện sự cố ở mức hệ thống.
- Trả vùng nghi ngờ có định nghĩa rõ.
- Xếp hạng nguyên nhân, giữ đúng tập ứng viên và giới hạn quan sát.
- Có đối chứng đã cài và kiểm trên dev.
- Có gói thiết kế đủ cụ thể để Minh xem xét tại G3.

P6 chưa trả lời được phương pháp có khắc phục hạn chế trên dữ liệu ngoài thiết kế hay không. Phần đó thuộc P7. Khả năng giữ kết quả trên FlashTicket thuộc P10.

Khung bốn tầng trong MRP là **CANDIDATE**, không phải kiến trúc đã chọn. Việc phân chia module dưới đây phục vụ triển khai và kiểm riêng từng phép tính; không mặc nhiên xác nhận khung đó.

| Phân loại | Nội dung |
|---|---|
| USER_CONFIRMED / DECIDED | Minh đã đóng P5 ngày 18/10/2026. Không tự mở lại P5. |
| FACT | Đóng P5 không đồng nghĩa nghiệm thu riêng mọi task, giải quyết mọi OPEN, chọn phương pháp P6 hoặc cấp quyền G3/test. |
| FACT | Đã có bộ dựng đồ thị quan sát, hợp đồng đồ thị tĩnh, mô hình ba hệ và đối chiếu nguồn. |
| FACT | Chưa có phương pháp P6 được chọn, cài hoàn chỉnh và kiểm toàn chuỗi. |
| CANDIDATE | Phân rã task, cơ chế ưu tiên thử, ma trận cấu hình, ngân sách và vai trò trong kế hoạch này. |
| OPEN | Cơ chế cuối cùng, mức đồ thị, tham số, chính sách nền, mức khả dụng của đối chứng tĩnh và ngân sách máy thực tế. |

Nguồn trực tiếp: [MRP](/D:/RCA-flashticket/docs/MRP.md), [DT18](/D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md), [hướng dẫn của cô](/D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md), [DECISIONS](/D:/RCA-flashticket/docs/DECISIONS.md), [gói G2](/D:/RCA-flashticket/results/T-034/goi-g2.md), [bàn giao P6](/D:/RCA-flashticket/results/T-040/ban-giao-p6.md).

**2. Khảo sát đã thực hiện và độ tin cậy của đầu vào**

Đã đọc nguồn yêu cầu, SPEC/LOG và đầu ra liên quan của T-034–T-040; đọc mã dùng chung và trung gian P4 cần để xác định khối lượng. Không chạy lại thực nghiệm.

Các manifest hiện hành của T-034, T-035, T-037, T-038, T-039, T-040 và gói SMTP V2 đã được kiểm hash. Manifest kết quả P4 dùng chung của T-032/T-033 cũng đã được kiểm.

Hai trường hợp cần giữ đúng ý nghĩa:

- Manifest T-036 lịch sử lệch ba file mã/tài liệu sau thay đổi SMTP V2 đã được duyệt. Pin V2 và mã đang dùng khớp. Không coi đây là kết quả cũ bị hỏng, cũng không dùng manifest cũ để xác nhận mã mới.
- Một manifest phản biện P4 lưu phiên bản WHY/LOG cũ. Hai file hiện hành dài hơn; tiền tố byte được pin vẫn khớp. Phần kết quả được sử dụng phải đi theo manifest kết quả tương ứng.

B16 hiện tại khớp nguồn được T-040 ghi nhận. Repo FlashTicket chỉ được đọc; không đọc repo RCA lưu trữ.

**Khối lượng đã kiểm từ đầu ra có manifest**

| Đại lượng | RE2-TT dev | Nezha-OB dev |
|---|---:|---:|
| Ca | 30 | 22 |
| Ô đánh giá | 10 | 13 |
| Span trong miền T-035 đã xử lý | 22.834.238 | 1.421.887 |
| Quan hệ cha–con khác chủ quản được đếm | 3.957.045 | 338.829 |
| Graph canonical đã lưu | 1.069 | 132 |
| Chế độ được dùng trong kế hoạch | (a), (b) | (a) |

Nguồn số span và quan hệ: [thống kê T-035](/D:/RCA-flashticket/results/T-035/thong-ke-do-thi.json), các con trỏ `/datasets/RE2-TT`, `/datasets/Nezha-OB`; danh sách graph ở `/canonical_graph_files`. Số ca/ô và phạm vi chế độ đối chiếu với gói G2 và giao thức P3.

Tổng miền trace đã được T-035 xử lý là **24.256.125 span**. Đây không phải số span đã đọc lại trong lượt PLAN.

Lượt dựng graph đầy đủ trước đây mất khoảng **18,14 phút**, RAM đỉnh khoảng **2,25 GiB**; nguồn `/cost/full_run_seconds` và `/cost/peak_rss_bytes`. Không dùng thời gian này làm dự báo trực tiếp cho trích request, tính thời lượng hoặc chạy P6.

Ổ D còn khoảng **35 GiB** khi khảo sát. Con số 65 GB trong mô tả thiết bị là mốc lịch sử, không dùng để cấp ngân sách hiện tại.

**Những gì graph hiện có chưa cung cấp**

- Graph gộp chỉ giữ số đếm và lượng chứng cứ hạn chế trên cạnh; không thay thế cây span đầy đủ.
- Không thể suy thời gian không bị span con phủ, quan hệ từng invocation hay chuỗi online từ graph gộp.
- Graph full/N/A được dựng bằng cửa sổ đã biết. Không mặc nhiên dùng chúng tại thời điểm báo động của chế độ (b).
- Trace công khai chưa xác nhận đầy đủ kiểu cạnh gọi đồng bộ, messaging và database.
- Đồ thị thao tác quan sát được vẫn dùng được để nghiên cứu. Thiếu ánh xạ thao tác tĩnh không có nghĩa “không dựng được đồ thị thao tác”.
- Nezha chỉ có miền cửa sổ đã được adapter chấp nhận. Không coi đó là chuỗi cả ngày hoặc tự mở chế độ phát hiện liên tục.

**3. Danh mục module và phần việc thực tế**

| Nguồn hiện có | Tái sử dụng | Phải bổ sung hoặc kiểm lại |
|---|---|---|
| [builder.py](/D:/RCA-flashticket/src/do_thi/builder.py): `from_p3`, `Prepared`, `graph`, `project`, `build` | Chuẩn hóa span, danh tính, cạnh, phép chiếu, coverage | Chỉ đưa dữ liệu đã khả dụng vào phép tính online; không lấy graph full làm graph tại quá khứ |
| [bộ dựng đồ thị tĩnh](/D:/RCA-flashticket/src/do_thi_tinh/build.py) và [compare.py](/D:/RCA-flashticket/src/do_thi_tinh/compare.py) | Schema, nguồn cạnh, mapping, đối chiếu | Adapter cho phương pháp; tách cạnh thiết kế và quan sát; không biến binding thành lời gọi |
| [selector.py](/D:/RCA-flashticket/src/p3/selector.py) | Allowlist, mã mờ, kiểm đường dẫn/hash | Tách hoàn toàn runner có metadata chấm khỏi payload phương pháp |
| [nezha.py](/D:/RCA-flashticket/src/p3/nezha.py) | Miền được phép, timestamp và provenance từng kênh | Chính sách cửa sổ, nền ít mẫu, thời gian không đồng bộ; không nội suy tạo mẫu |
| [cua_so.py](/D:/RCA-flashticket/src/p3/cua_so.py) | Phép cắt dữ liệu có thể kiểm riêng | Không tái sử dụng nguyên tiền xử lý nhìn toàn bản ghi cho chế độ online |
| [ban_ghi.py](/D:/RCA-flashticket/src/p3/ban_ghi.py) | Trạng thái, khóa xếp hạng, hòa điểm, tập trả về | Bản ghi điểm đồ thị, báo động, vùng nghi ngờ, lý do thiếu và fallback |
| [danh_gia.py](/D:/RCA-flashticket/src/p3/danh_gia.py) | Độ đo, chấm hòa, bootstrap theo ô | Kiểm mẫu số, lỗi, coverage và ghép đầu ra P6 bằng oracle độc lập |
| [runner.py](/D:/RCA-flashticket/src/p3/runner.py) | Tiến trình riêng, timeout, ghi chi phí | Runner P6 và cache có khóa đầy đủ; giữ mọi lượt lỗi |
| Mã MicroRank, SimpleRCA, CIRCA, TORAI hiện có | Baseline đã pin; một số phép tính tham khảo | Kiểm đúng biến thể, đầu vào, seed và ý nghĩa phép so trước khi dùng |
| Trung gian P4 | Chuỗi chứng cứ và phép đối chiếu đã có | Những câu chưa phân xử được giao riêng; không chạy lại toàn P4 |

Schema P6 dự kiến phải biểu diễn tối thiểu:

`sample_time`, `available_at`, đơn vị thời gian, thực thể/thao tác, nguồn tín hiệu, scope, `evidence_id`, chất lượng/thiếu dữ liệu, nguồn cạnh, thời hạn hiệu lực cạnh và provenance.

Đầu ra mỗi lần dự đoán phải nối được:

`input → đặc trưng → chuẩn hóa/nền → quan hệ được dùng → điểm → ngưỡng → báo động/vùng/xếp hạng`.

Nhãn, tên ca và mốc tiêm thuộc runner/evaluator, không nằm trong payload phương pháp.

**4. Bản đồ căn cứ, OPEN và cách thu hẹp ứng viên**

| Vấn đề | Bằng chứng hiện có | Phần phải phân xử | Nơi nhận |
|---|---|---|---|
| Thời lượng phía gọi bị quy cho phía gọi | P4 đã có chuỗi chứng cứ ở nhóm liên quan | Gán chứng cứ theo quan hệ có cải thiện phân biệt trên dev không; điều kiện sai | T-041, 047, 051, 067–069 |
| Thời gian không bị span con phủ | Có thể tính hình học từ interval | Có thể diễn giải tới đâu khi song song, bất đồng bộ, thiếu span | T-047; không mặc định là self-time vật lý |
| Lỗi return hoặc lỗi nhanh | Có quan sát và câu hỏi chưa đo đủ theo thao tác | Duration giảm, lỗi log, outcome có giữ thông tin phân biệt không | T-049, 066 |
| Nhãn “lan” | Có nháp và bảng lời gọi | Độ nhạy ngưỡng, nhóm không đo được, giá trị phân nhóm | T-065 |
| TraceRCA chọn tập, cờ frontend | Còn phép kiểm sau E1 | Chỉ cần nếu dùng chấm theo tập hoặc nâng nhánh tác giả thành baseline | T-076–078, 084 |
| MicroRank sau đổi bộ chia/đếm | Còn hai ca chưa phân xử | Cần trước khi chọn cơ chế xếp hạng tương ứng | T-079, 085 |
| BOCPD số học và nhìn tương lai | Có bằng chứng cho hai vấn đề khác nhau | Tách sửa số học, sửa tiền xử lý và ảnh hưởng toàn dev | T-061–062, 080–082, 087–089 |
| Đồ thị tĩnh khác quan sát | Có đối chiếu P5, còn lineage/workload | Phép so nào tương đương; phần nào chỉ là độ nhạy theo nguồn graph | T-059, 070–071 |
| OB checkout→currency | Chưa mở nghiên cứu sâu trong P5 | Chỉ điều tra nếu kết luận P6 phụ thuộc cạnh này | T-086 |
| Host, span kind, queue/DB identity, onset/recovery | Thiếu quan sát độc lập | Không phục hồi bằng thuật toán trên dữ liệu hiện có | T-073 chuyển P9/P10 |
| Hiệu quả trên test/FlashTicket | Chưa đánh giá | P7/P10 sau quyền riêng | T-074 bàn giao |

**Khuyến nghị thu hẹp ban đầu — vẫn là CANDIDATE**

Ưu tiên thử một họ nhỏ: giữ điểm tín hiệu tại chủ quản, đồng thời kiểm cách đưa chứng cứ thời lượng theo quan hệ cha–con tới đích liên quan. Hai cách gộp đơn giản có thể làm ứng viên là cực đại và trung bình có kiểm soát trọng số. Chưa gọi điểm đó là “nguyên nhân tự sinh”.

Lý do đủ để **đề xuất thử**: P4 đã chỉ ra một số trường hợp vị trí ghi thời lượng và nơi cần quy chứng cứ khác nhau. Bằng chứng đó chưa đủ để chọn công thức, mức graph hay khẳng định lợi ích.

Trước khi chọn họ này để triển khai, T-041 phải viết rõ:

- Đại lượng nào nằm trên span, cạnh và nút.
- Điều kiện tạo cặp cha–con và điều kiện không thể gán.
- Công thức, trọng số và cách xử lý nhiều đích.
- Khi nào phép tính khác nhánh không quan hệ.
- Phản ví dụ: nhiều con, span thiếu, cạnh sai, lỗi nhanh, tín hiệu tài nguyên không có độ trễ.
- Điều gì sẽ bác bỏ khả năng dùng ứng viên.

Hồi quy có điều kiện là nhánh dự phòng T-075 nếu họ trên không qua kiểm khả dụng hoặc không đáp ứng đầu ra cần có. Không mặc định chạy cả hai họ.

GNN không nằm trong triển khai mặc định: chưa có căn cứ cho nhu cầu mô hình đó, ngân sách và nền huấn luyện phù hợp. T-041 phải ghi lý do giữ hoặc loại khỏi vòng này. Nếu cần thử GNN, phải trình phạm vi và ngân sách mới; không giấu việc huấn luyện trong task tích hợp.

PageRank, spectrum, khai phá tập và quy tắc “sâu nhất” cũng không tự trở thành thành phần bắt buộc. Xếp trực tiếp theo điểm đã dùng quan hệ là một phương án cần xét.

**5. Ma trận bao phủ yêu cầu nguồn**

| Yêu cầu | Bằng chứng hiện có | Việc còn thiếu | Task | Kết luận được phép |
|---|---|---|---|---|
| Nút/cạnh và ba loại quan hệ DT18 | Hợp đồng P5; dữ liệu công khai thiếu một số kiểu | Quy tắc tính theo kiểu và kiểm fixture; bàn giao runtime | 041, 043, 051, 059, 073 | Hỗ trợ hợp đồng; chưa xác nhận runtime FlashTicket |
| Log/trace/metric trên graph | Mapping và provenance P5 | Đặc trưng theo thời gian, scope và chống đếm lặp | 044–050 | Ánh xạ đúng trong miền được kiểm |
| Điểm bất thường dùng cạnh | Ứng viên và probe P4 | Công thức, trung gian, phản ví dụ, dev | 051, 057–059, 067–071 | Tính đúng và hành vi dev; chưa phải lợi ích test |
| Phát hiện hệ thống | Detector P3 và hạn chế đã biết | Bộ phát hiện P6, nền/ngưỡng nhân quả | 050, 052, 061–062 | Phát hiện trong giao thức đã khai |
| Vùng nghi ngờ | Yêu cầu MRP | Định nghĩa vùng, tính ổn định và coverage | 053, 056 | Vùng nghi ngờ; không tự gọi vùng ảnh hưởng thật |
| Xếp hạng | Giao thức P3 | Điểm, tập trả về, hòa, thiếu tín hiệu | 054, 056, 063–064 | Xếp hạng theo giao thức |
| Chọn thiết kế có căn cứ | G2 và OPEN | So ứng viên, trường hợp đúng/sai, điều kiện thất bại | 041, 065–069 | Chọn trên dev sau Minh duyệt |
| Đối chứng công bằng | MRP/WHY | Cài, kiểm thông tin còn lại và ngân sách | 057–060, 067–071 | Phạm vi tác dụng cấu trúc tương ứng phép so |
| Không rò nhãn/tương lai | Selector, các cấm đầu vào | Kiểm prefix, cache, cửa sổ, cập nhật nền | 043–045, 050, 055, 072 | Không thấy rò trong các đường đã kiểm |
| Khóa G3 | Quy định hiện hành | Gói code/cấu hình/diễn giải/độ đo | 074 | Đủ hồ sơ trình Minh; chưa cấp quyền test |
| P7/P8/P9/P10 | MRP, B16, R-01…R-10 | Hợp đồng sử dụng và nghĩa vụ còn thiếu | 073–074 | Bàn giao có owner và giới hạn |

**6. Giao thức và số tổ hợp dự kiến**

Các con số dưới đây là **dự toán**, chưa phải cấu hình được chọn.

**Đơn vị đánh giá**

- Một cấu hình có tối đa `30 × 2 + 22 = 82` đơn vị ca–chế độ.
- Không dùng `52 × 2`: Nezha chưa được cấp miền tự phát hiện liên tục.
- Hai mức graph ứng viên: thực thể và thao tác.
- Hai độ rộng cửa sổ ứng viên của TT: 60 và 300 giây.
- OB chỉ dùng cửa sổ nằm trong hợp đồng hiện hành. Nếu hai lựa chọn sau cắt là cùng dữ liệu thì gộp, không tính thành hai cấu hình độc lập.
- Hai cách gộp trong một họ nhỏ: tối đa `2 × 2 × 2 = 8` cấu hình có nghĩa.

T-041 phải ghi danh sách cấu hình cụ thể. T-042 kiểm khả thi. Không bổ sung tham số âm thầm sau khi xem điểm.

**Đối chứng trên dev**

Bốn họ: graph quan sát; không quan hệ; graph tĩnh; graph ngẫu nhiên giữ bậc.

Dự toán trên mức tối đa tám cấu hình:

- Ba họ không ngẫu nhiên: `3 × 8 × 82 = 1.968` đơn vị.
- Graph ngẫu nhiên: `20 seed × 8 × 82 = 13.120` đơn vị.
- Tổng trần: **15.088 đơn vị chấm từ trung gian dùng lại**.

Đây không phải 15.088 lần đọc lại trace. Cấu hình trùng hoặc UNSUPPORTED được ghi rõ; không giả là có đủ số phép so hữu hiệu.

Hai giới hạn diễn giải phải được giữ:

1. Bỏ quan hệ khỏi phương pháp có thể làm mất cả đặc trưng được tạo bằng quan hệ. Khi đó phép so đo tác dụng của toàn phần thông tin quan hệ đó.
2. Nếu chỉ xáo lại đích ở graph gộp nhưng vẫn giữ cặp span gốc, phép so chỉ đo phần cấu trúc đã xáo. Không gọi đó là loại bỏ mọi cấu trúc trace.

Đối chứng tĩnh phải báo phần tín hiệu, mapping và coverage thay cùng. Không tạo dữ liệu cạnh không có để làm phép so trông tương đương.

**Độ nhạy sau lựa chọn dev**

Dự kiến tối đa 16 biến thể bổ sung cho cấu hình được chọn:

- Bỏ từng nguồn metric, log, trace: 3.
- Giảm nền; đổi cách giữ dấu; đổi mức bảo vệ số học: 3.
- Bỏ 25% và 50% cạnh, mỗi mức 5 seed: 10.

Tổng tối đa `16 × 82 = 1.312` đơn vị. Chỉ giữ phép thay có ý nghĩa với thiết kế được chọn; lý do bỏ phải được ghi. Không dùng kết quả này để chọn lại tùy ý một cấu hình ngoài ngân sách đã khai.

**Baseline**

Giữ sáu baseline P3 ở TT và bốn baseline được hỗ trợ ở OB. Baseline chuẩn đã khóa là một nhóm tham chiếu; các biến thể sửa là nhóm riêng.

- TT chế độ (a): năm phương pháp một seed và TORAI ba seed → 240 lượt vật lý đã có thể đối chiếu.
- OB: bốn phương pháp × 22 ca → 88 lượt.
- Tái sử dụng chỉ khi hash, đầu vào, cửa sổ, phiên bản và quy tắc chấm khớp.
- Tại báo động P6 được chọn: tối đa 150 lượt của năm baseline một seed và 90 lượt TORAI. Đây là phép so xếp hạng cùng thời điểm, không phải phép so các pipeline phát hiện độc lập.
- Các pipeline detector P3 được báo riêng theo đúng tiền xử lý và giới hạn lịch sử.

Không nhận “ngân sách tuning bằng nhau” giữa phương pháp mới và baseline P3 cố định. Ngân sách bằng nhau được áp cho các nhánh đối chứng của phương pháp mới. T-060 phải trình Minh việc giữ baseline chuẩn hay bổ sung tuning cho baseline mạnh; nếu bổ sung, phải có task và ngân sách riêng trước khi chạy.

**7. Quy ước áp dụng cho mọi hồ sơ task**

Các mã dưới đây mới là dự kiến. Thư mục hiện tại đã được kiểm; mã cao nhất đang dùng là T-040. Không tạo cả danh sách task ngay khi duyệt kế hoạch.

Để tránh lặp boilerplate, mỗi hồ sơ dùng các quy ước sau:

- `W(n)` là phạm vi dự kiến:
  - `D:/RCA-flashticket/results/T-n/`;
  - `D:/RCA-flashticket/tasks/T-n-p6/SPEC.md` khi Minh duyệt tạo;
  - `D:/RCA-flashticket/tasks/T-n-p6/LOG.md`;
  - đúng dòng task trong `D:/RCA-flashticket/docs/STATE.md`;
  - cộng chính xác file mã ghi ở hồ sơ.
- Mỗi thư mục kết quả có đầu vào/pin, cấu hình, fixture hoặc oracle, kết quả kiểm, báo cáo, manifest và các lượt được giữ nguyên. Không sao chép dữ liệu lớn vào mọi lượt.
- Đầu vào từ task trước chỉ dùng khi đầu ra hợp lệ, manifest khớp và quyền triển khai task sau đã có.
- Đầu vào P4/P5 dùng các phiên bản hiện hành đã nêu ở mục 2; không tự suy pin từ HEAD.
- Mọi task đọc dev mới phải có allowlist và quyền dữ liệu cụ thể trong SPEC.
- Vai trò đề xuất cho **từng task**: Codex làm, Claude phản biện chính thức. Minh quyết khi duyệt từng SPEC. Ngoại lệ hai phiên Codex của lượt kế hoạch này không chuyển sang các task.
- Mọi thay đổi WHY/DECISIONS cần đề xuất nguyên nội dung và được Minh duyệt trước. `W(n)` không tự cấp quyền ghi hai file đó.
- Giờ công gồm đọc nguồn liên quan, thiết kế trong phạm vi, cài, fixture, kiểm trung gian, phân tích, tài liệu, manifest, LOG và prompt. Phản biện chính thức và thời gian chờ Minh tính riêng.
- “Vừa một phiên” là dự toán cho một đầu ra hẹp với đầu vào đã sẵn sàng; không dùng nó để giảm kiểm nếu phát hiện lỗi.

**8. Hồ sơ task trên đường triển khai chính**

**T-041 — Căn cứ và hợp đồng khoa học P6. Loại: thiết kế.**

1–4. Trả lời cần dùng quan hệ ở đâu và vì sao. Đọc MRP, DT18, G2, bàn giao P5 và chuỗi P4 gốc; không cần đọc telemetry mới. Đầu ra phải phân biệt yêu cầu đề tài, nhu cầu kỹ thuật và giả thuyết sửa hạn chế.

5–7. Lập danh sách ứng viên; viết công thức của họ ưu tiên và phương án đối lập; chỉ rõ nút/cạnh/tín hiệu; định nghĩa phép bác bỏ; lập tám cấu hình tối đa và bảng diễn giải. Ghi `W(041)`, với `hop-dong-khoa-hoc.md`, `ung-vien.json`, `ma-tran-dev.json`. Không ghi lựa chọn vào WHY khi chưa duyệt.

8–9. Lần từng biến trong công thức tới đầu vào; dựng phản ví dụ bằng tay cho thiếu cạnh, nhiều con, lỗi nhanh và tín hiệu chung. Xong khi mỗi thành phần có căn cứ, điều kiện thất bại và phép phân xử. Không kết luận ứng viên tốt.

10–13. 3–4 giờ công, máy 0,1–0,2 giờ; RAM dưới 1 GiB, đĩa mới dưới 0,2 GiB; tin cậy vừa. Rủi ro là thiếu cơ sở cho họ ưu tiên: chuyển đề xuất T-075 hoặc giữ OPEN. Minh duyệt họ được thử và ma trận. Vừa phiên vì chỉ đặc tả quyết định thử, không cài phương pháp.

**T-042 — Khảo sát khả thi có đo. Loại: kỹ thuật, thực nghiệm được duyệt sau.**

1–4. Xác định chi phí I/O, cây span, đặc trưng và cache. Cần T-041 và quyền đọc dev. Dùng selector, adapter và số kích thước đã có để chọn ba ca TT, ba ca OB theo kích thước/coverage, không chọn theo điểm RCA.

5–7. Đọc một lần mỗi ca; đo từng bước đọc/hash, chuẩn hóa, nhóm request, chuẩn bị cửa sổ; thử tối đa bốn tổ hợp mức/cửa sổ trên mỗi ca, tức 24 bản đo. Ghi `W(042)` và script khảo sát trong đó; chưa tạo bộ chạy sản xuất.

8–9. Kiểm số bản ghi trước/sau, checksum, đỉnh RAM, byte mỗi trung gian; ngoại suy theo span/request/cửa sổ và nêu sai số. Đầu ra phải xác định lịch chạy, cache, số worker và trường hợp cần T-083. Không lấy thời gian P5 nhân một hệ số tùy ý.

10–13. 3–5 giờ công, máy 0,25–1 giờ; RAM dự kiến 3–6 GiB, đĩa mới tối đa 2 GiB; tin cậy thấp trước đo. Nếu vượt tài nguyên, trình đổi cách lưu hoặc máy, không giảm ca. Vừa phiên vì sáu ca và bộ đo hẹp; Minh duyệt quyền chạy và ngân sách trước.

**T-043 — Schema và API xuyên suốt. Loại: cài hợp đồng.**

1–4. Cần T-041 và kết quả khả thi T-042. Chốt ranh giới runner/phương pháp/evaluator, không chốt thuật toán.

5–7. Tạo kiểu dữ liệu cho `Evidence`, `GraphView`, `FeatureWindow`, `Score`, `Alarm`, `Region`, `Ranking`, `RunRecord`; trường availability/scope/missing/status/provenance. Ghi `W(043)` và `D:/RCA-flashticket/src/p6/contracts.py`, `D:/RCA-flashticket/src/p6/__init__.py`.

8–9. Ít nhất 12 fixture hợp lệ/không hợp lệ bao phủ ba tín hiệu, kiểu cạnh, timestamp, khóa nhãn, tín hiệu chung và trạng thái lỗi. Round-trip không mất nghĩa; khóa cấm bị từ chối. Chưa có bằng chứng hiệu quả.

10–13. 3–4 giờ, máy 0,1–0,3 giờ; RAM 1 GiB, đĩa 0,2 GiB; tin cậy vừa. Nếu schema mâu thuẫn nguồn, dừng phần phụ thuộc. Minh duyệt schema/phạm vi mã. Một phiên vì một hợp đồng, không chứa xử lý dữ liệu.

**T-044 — Adapter TT chỉ dùng thông tin đã khả dụng. Loại: cài dữ liệu.**

1–4. Cần T-043; dùng selector P3, schema TT và quy tắc thời gian đã kiểm. Hai chế độ có API riêng: cửa sổ được runner cung cấp ở (a), luồng theo cutoff ở (b).

5–7. Viết `read_allowed`, `iter_prefix`, `slice_available`; thống nhất giây/µs/ns; không truyền tên ca, root, mốc tiêm vào lõi. Ghi `W(044)` và `D:/RCA-flashticket/src/p6/input_tt.py`.

8–9. Mười fixture biên thời gian; sáu ca khảo sát hoặc phần TT trong đó; kiểm prefix bất biến khi thêm tương lai, span kết thúc sau cutoff và đường dẫn bị cấm. Xong khi dữ liệu đầu ra khớp oracle và không có trường nhãn.

10–13. 4–5 giờ, máy 0,2–0,8 giờ; RAM 4 GiB, đĩa 1 GiB; tin cậy vừa. Sai đơn vị chặn toàn online. Minh duyệt chính sách availability. Vừa phiên vì chỉ một adapter, không tạo đặc trưng.

**T-045 — Adapter OB và giới hạn hỗ trợ. Loại: cài dữ liệu.**

1–4. Cần T-043; dùng hợp đồng Nezha hiện hành, dữ liệu từng kênh và cửa sổ cho phép.

5–7. Giữ timestamp bản địa, số mẫu thật, scope metric/service; ghi rõ cửa sổ trace/log khả dụng; trả UNSUPPORTED cho chế độ (b). Ghi `W(045)` và `D:/RCA-flashticket/src/p6/input_ob.py`.

8–9. Tám fixture cho kênh lệch thời gian, ít mẫu, thiếu kênh và cửa sổ trùng sau cắt; đối chiếu ba ca khảo sát. Không nội suy tăng số quan sát, không gọi dữ liệu adapter là cả ngày.

10–13. 3–4 giờ, máy 0,2–0,5 giờ; RAM 3 GiB, đĩa 1 GiB; tin cậy vừa. Nền không đủ chuyển trạng thái chất lượng tới T-050, không giả có nền dài. Minh duyệt chính sách hỗ trợ. Một phiên vì không thiết kế detector OB.

**T-046 — Cây request và chỉ mục span. Loại: cài trung gian.**

1–4. Cần T-044/045 và quy tắc danh tính T-035. Đơn vị là span và request, không phải graph gộp.

5–7. Tạo chỉ mục cha–con, request root, orphan, xung đột ID, chu trình và biên cửa sổ; lưu danh tính thao tác riêng chủ quản. Ghi `W(046)` và `D:/RCA-flashticket/src/p6/trace_tree.py`.

8–9. Mười hai cây nhỏ có đáp án tay; đảo thứ tự bản ghi không đổi kết quả; fixture duplicate/conflict không bị gộp âm thầm. Đối chiếu số cạnh với bộ dựng trên miền tương ứng. Không gọi mọi parent là lời gọi đồng bộ.

10–13. 4–5 giờ, máy 0,2–0,6 giờ; RAM 4 GiB; đĩa cache dự kiến tối đa 4 GiB, phải thay bằng đo T-042. Minh duyệt cách giữ cây thiếu. Một phiên vì chỉ tạo trung gian cấu trúc.

**T-047 — Đặc trưng trace và chứng cứ trên cạnh. Loại: cài phép đo.**

1–4. Cần cây T-046. Dùng chuỗi P4 liên quan duration và chủ quản để xác định đại lượng cần giữ.

5–7. Tính duration, số invocation, lỗi nếu có trường nguồn, phân phối theo thao tác/cạnh; tính hợp interval con được cắt trong cha và phần không bị phủ. Lưu cả đầu vào phép gộp. Ghi `W(047)` và `D:/RCA-flashticket/src/p6/trace_features.py`.

8–9. Mười hai fixture gồm con lồng, song song, vượt cha, thiếu con và async không rõ; oracle interval độc lập. Không dùng phép trừ tổng duration con. Tách “đo được phần không bị phủ” khỏi “đã đo self-time vật lý”.

10–13. 4–5 giờ, máy 0,2–0,8 giờ; RAM 4 GiB, đĩa tăng tối đa 2 GiB ngoài cache cây. Minh duyệt tập đặc trưng thử. Một phiên vì không chọn trọng số hay chấm RCA.

**T-048 — Đặc trưng metric và scope. Loại: cài phép đo.**

1–4. Cần T-043–045; dùng mapping P3/P5, không suy host từ trường chưa xác minh.

5–7. Giữ kênh gốc, chủ quản, loại phép gộp, thiếu mẫu và timestamp; chỉ resample theo quy tắc được duyệt; tạo giá trị cửa sổ mà chưa chuẩn hóa bằng tương lai. Ghi `W(048)` và `D:/RCA-flashticket/src/p6/metric_features.py`.

8–9. Tám fixture: counter/gauge, reset nếu liên quan, thiếu điểm, trùng điểm, metric dùng chung, đổi đơn vị, prefix và nền hằng. Đối chiếu vài kênh thật bằng tính tay. Không biến metric service thành nhiều chứng cứ operation độc lập.

10–13. 3–4 giờ, máy 0,1–0,4 giờ; RAM 3 GiB, đĩa 1 GiB; tin cậy vừa. Kênh không có semantics được giữ riêng/không dùng theo quyết định, không đoán. Một phiên vì chỉ một nguồn tín hiệu.

**T-049 — Đặc trưng log và kiểm đếm chứng cứ. Loại: cài phép đo.**

1–4. Cần T-043–045; dùng schema log thật và kết luận P4 về dòng log, request, outcome.

5–7. Nối span chỉ khi có khóa hợp lệ; nếu không, giữ service–time. Tạo count/rate/outcome theo trường có thật; nếu dùng template, quy định fit chỉ trên dữ liệu được phép. Giữ `evidence_id` để chống nhân bản. Ghi `W(049)` và `D:/RCA-flashticket/src/p6/log_features.py`.

8–9. Mười fixture cho nhiều dòng một request, duplicate, không có trace ID, shared scope, template mới và prefix. Kiểm tổng count đối chiếu nguồn. Không gọi số dòng lỗi là số request lỗi.

10–13. 4–5 giờ, máy 0,2–0,7 giờ; RAM 4 GiB, đĩa 1 GiB; tin cậy vừa. Nếu cần parser mới ngoài phạm vi, trình nhánh riêng. Một phiên vì không nghiên cứu mô hình ngôn ngữ log.

**T-050 — Nền, chuẩn hóa và thiếu tín hiệu. Loại: cài phép tính.**

1–4. Cần đặc trưng T-047–049 và hợp đồng T-041. Nền phải có nguồn và thời điểm khả dụng; “trước mốc tiêm” không tự là nền khỏe độc lập.

5–7. Cài `fit/update/transform`, số mẫu tối thiểu, scale floor, dấu tăng/giảm, missing mask, cold start và quy tắc cập nhật nền. Giữ thống kê dùng để chuẩn hóa. Ghi `W(050)` và `D:/RCA-flashticket/src/p6/normalization.py`.

8–9. Mười hai chuỗi nhỏ: hằng, gần hằng, outlier, thiếu, đổi đơn vị, thêm tương lai, đổi thứ tự và nền ít mẫu. Oracle số tay; kiểm không có NaN/Inf lọt vào điểm. Không coi floor là chứng cứ sinh học/hệ thống.

10–13. 3–4 giờ, máy 0,1–0,4 giờ; RAM 3 GiB, đĩa 0,5 GiB. Minh duyệt các chính sách kỹ thuật trước dev. Vừa phiên vì chỉ một bộ chuẩn hóa, không tuning cả pipeline.

**T-051 — Bộ tính điểm dùng quan hệ, họ được phép thử. Loại: cài ứng viên.**

1–4. Cần T-041, T-047–050. Chỉ bắt đầu khi công thức và miền áp dụng đã được duyệt để thử.

5–7. Cài `score_local`, `score_relation`, `aggregate`; tách điểm tại chủ quản và điểm do quan hệ mang tới; giữ contribution từng cạnh. Tối đa hai cách gộp đã khai. Định nghĩa riêng hành vi với call/data/message và cạnh không có tín hiệu. Ghi `W(051)` và `D:/RCA-flashticket/src/p6/scoring.py`.

8–9. Mười hai graph nhỏ và các chuỗi chứng cứ P4 được phép: đổi một cạnh phải gây thay đổi dự đoán được; cạnh không liên quan không tự cộng chứng cứ; node cô lập còn điểm local. Không nhận “tự sinh/kế thừa” khi chưa có phép phân xử.

10–13. 4–5 giờ, máy 0,2–0,8 giờ; RAM 4 GiB, đĩa 1 GiB. Không qua tính đúng/khả dụng thì xét T-075 trước ma trận lớn. Một phiên vì một họ công thức hẹp; Minh chưa chọn thuật toán cuối.

**T-052 — Báo động hệ thống. Loại: cài detector P6.**

1–4. Cần T-050–051. Đầu vào là chuỗi điểm đã có `available_at`, không có mốc tiêm.

5–7. Định nghĩa điểm hệ thống, học ngưỡng từ nền được phép, warm-up, persistence/cooldown nếu được chọn, và thời điểm phát báo động. Ghi `W(052)` và `D:/RCA-flashticket/src/p6/detection.py`.

8–9. Mười chuỗi có đáp án báo động tay; kiểm thêm tương lai không đổi báo động quá khứ; kiểm no-alarm, cold-start và tất cả điểm thiếu. Ghi rõ latency nếu cần đợi cửa sổ sau báo động.

10–13. 3–4 giờ, máy 0,1–0,4 giờ; RAM 3 GiB, đĩa 0,5 GiB. Thiếu nhãn onset chỉ giới hạn cách gọi độ trễ, không sửa mốc. Một phiên vì không cài lại baseline detector.

**T-053 — Vùng nghi ngờ. Loại: cài đầu ra.**

1–4. Cần T-051–052. Câu hỏi là cách biểu diễn nhóm triệu chứng và quan hệ được quan sát.

5–7. Xác định phần tử vượt điều kiện, hướng/kiểu cạnh dùng nối vùng, xử lý isolate và nhiều vùng; xuất thành viên, chứng cứ và kích thước. Ghi `W(053)` và `D:/RCA-flashticket/src/p6/regions.py`.

8–9. Tám graph tay: chuỗi, nhánh, vòng, isolate, thiếu cạnh, hai bất thường độc lập, nhiều vùng và vùng rỗng. Nếu chỉ tìm thành phần liên thông thì gọi đúng là vùng nghi ngờ; không tự gọi subgraph anomaly detection.

10–13. 2–3 giờ, máy 0,1–0,2 giờ; RAM 1 GiB, đĩa 0,2 GiB. Minh duyệt định nghĩa đầu ra. Vừa phiên vì không thiết kế mô hình chấm graph con mới.

**T-054 — Xếp hạng và tập ứng viên. Loại: cài đầu ra.**

1–4. Cần T-051, giao thức P3 và universe đã duyệt. Tập chấm không đồng nhất với tập quan sát hoặc tập trả về.

5–7. Ánh xạ điểm operation lên thực thể theo quy tắc đã khai; giữ khóa điểm thật, hòa chính xác, trạng thái không có bằng chứng; không lọc ứng viên chỉ vì dưới ngưỡng bất thường. Ghi `W(054)` và `D:/RCA-flashticket/src/p6/ranking.py`.

8–9. Mười fixture: hòa, root vắng, isolate có metric, nhiều operation chung chứng cứ, ngoài universe, điểm không hữu hạn. Không điền ngẫu nhiên hoặc tự thêm hạng cho thực thể không có bằng chứng.

10–13. 3–4 giờ, máy 0,1–0,3 giờ; RAM 1 GiB, đĩa 0,2 GiB. Nếu muốn PageRank/spectrum, phải kích hoạt nhánh tương ứng. Một phiên vì chỉ một quy tắc xếp hạng chính.

**T-055 — Runner, cache và sổ lượt chạy. Loại: hạ tầng thực nghiệm.**

1–4. Cần T-043–054. Tái sử dụng cách cách ly tiến trình và timeout của P3.

5–7. Cài driver theo manifest công việc; khóa cache bằng input hash, code, miền thời gian, mức graph, config; ghi trạng thái từng bước, thời gian/RAM và lỗi. Resume không ghi đè. Ghi `W(055)` và `D:/RCA-flashticket/src/p6/runner.py`.

8–9. Tám tình huống: ngắt, timeout, cache sai pin, cache sai cửa sổ, lỗi dữ liệu, lỗi phương pháp, chạy lại cùng seed, thiếu artifact. Không cho cache của toàn bản ghi lọt vào prefix.

10–13. 3–4 giờ, máy 0,2–0,5 giờ; RAM 3 GiB, đĩa 0,5 GiB. Minh duyệt concurrency sau T-042. Một phiên vì không chứa logic khoa học mới.

**T-056 — Evaluator và mẫu số. Loại: cài/kiểm giao thức.**

1–4. Cần T-043, 052–055; tái sử dụng hàm chấm P3 với bản ghi chuyển đổi rõ.

5–7. Tính Hit@k, MRR, NDCG, các bảng tương thích; detection theo cửa sổ, báo động sai/giờ và độ trễ theo loại nhãn; vùng chứa root/kích thước khi thiếu nhãn vùng. Giữ mẫu số toàn ca và bảng có điều kiện song song.

8–9. Mười hai bản ghi oracle, gồm hòa theo khối, root vắng, ERROR, UNSUPPORTED, no-alarm, fallback và ô nhiều ca. Bootstrap theo ô, không coi seed là ca độc lập. Ghi `W(056)` và `D:/RCA-flashticket/src/p6/evaluation.py`.

10–13. 3–4 giờ, máy 0,1–0,4 giờ; RAM 1 GiB, đĩa 0,5 GiB. Không âm thầm đổi quy tắc chấm baseline. Một phiên vì dùng giao thức đã có và kiểm phần nối mới.

**T-057 — Đối chứng không quan hệ. Loại: cài đối chứng.**

1–4. Cần T-041 và T-047–056. Phải xác định mọi đường quan hệ đi vào đặc trưng, điểm, vùng và hạng.

5–7. Tạo nhánh không nhận parent ID, adjacency hoặc đặc trưng đã suy từ quan hệ; giữ raw signal, thời gian, chuẩn hóa, universe và ngân sách như phần có thể giữ chung. Ghi `W(057)` và `D:/RCA-flashticket/src/p6/control_no_relations.py`.

8–9. Tám cặp fixture, đổi/xóa topology không làm nhánh này đổi kết quả; lập bảng trường bị loại và yếu tố thay cùng. Nếu chỉ bỏ một tầng thì đặt tên đúng tầng, không gọi toàn bộ là không đồ thị.

10–13. 4–5 giờ, máy 0,2–0,6 giờ; RAM 3 GiB, đĩa 1 GiB. Đây là kiểm đường thông tin, không đòi graph thắng. Một phiên vì chỉ một đối chứng.

**T-058 — Graph ngẫu nhiên giữ bậc. Loại: cài đối chứng.**

1–4. Cần hợp đồng graph và bộ điểm; dùng phép xáo có kiểm soát, tham khảo mã probe P4 sau khi kiểm pin.

5–7. Xác định cạnh nào xáo, bậc vào/ra, kiểu cạnh, payload được giữ, self-loop/multiedge và graph không xáo được. Lưu 20 seed cố định và số swap thành công. Ghi `W(058)` và `D:/RCA-flashticket/src/p6/control_random_graph.py`.

8–9. Sáu graph tay × 20 seed; kiểm bảo toàn bất biến, graph không đổi, tính tái lập và giới hạn không gian xáo. Không coi 20 bản giống nhau là 20 đối chứng hữu hiệu.

10–13. 3–4 giờ, máy 0,2–0,5 giờ; RAM 1 GiB, đĩa 0,5 GiB. Một phiên vì không chạy full matrix; Minh duyệt ý nghĩa đối chứng và seed trước.

**T-059 — Adapter graph tĩnh và phép so có điều kiện. Loại: cài đối chứng.**

1–4. Cần T-036 V2, mô hình/mapping T-038–039, T-040 và scorer P6.

5–7. Chuyển graph tĩnh vào API P6; tách source revision, kiểu cạnh và support; không lấy mapping thiếu làm mapping đúng. Tạo bảng graph-source × level × dataset, kể cả UNSUPPORTED.

8–9. Tám fixture mapping/kiểu cạnh và một số graph đại diện từ mỗi hệ; kiểm cùng tín hiệu/candidate/normalization ở phần có thể giữ chung. Ghi `W(059)` và `D:/RCA-flashticket/src/p6/control_static_graph.py`. Không quy mọi chênh điểm cho topology nếu coverage thay.

10–13. 3–4 giờ, máy 0,2–0,5 giờ; RAM 3 GiB, đĩa 0,5 GiB. Nếu phụ thuộc OM-07 thì trình T-086. Một phiên vì không truy lại toàn bộ kiến trúc P5.

**T-060 — Audit baseline và ngân sách so sánh. Loại: thiết kế giao thức.**

1–4. Dùng code, cấu hình, kết quả P3/G2 và manifest tương ứng; không chạy lại toàn baseline.

5–7. Lập từng dòng phương pháp: biến thể, tín hiệu, cửa sổ, seed, candidate, tie, preprocessing, reproductions, lỗi và quyền dùng. Phân loại kết quả nào tái sử dụng, cần chạy ở báo động mới, chỉ dùng lịch sử hoặc cần bản sửa. Ghi `W(060)` với `baseline-contract.json`, `comparison-plan.md`.

8–9. Tái tính một mẫu bản ghi và trace đường xử lý cho từng phương pháp; kiểm cả baseline mạnh TT. Không lấy BARO làm đối thủ duy nhất. Chính sách tuning và hạn chế tương đương phải được Minh duyệt.

10–13. 3–4 giờ, máy 0,1–0,4 giờ; RAM 1 GiB, đĩa 0,5 GiB. Vừa phiên vì audit và kế hoạch chạy; các lượt mới thuộc task riêng.

**T-061 — Detector tham chiếu: tiền xử lý nhân quả và số học. Loại: cài biến thể kỹ thuật.**

1–4. Cần T-050, T-060; đọc code NSigma/BOCPD và phép E2 gốc. Không đồng nhất sửa tiền xử lý với sửa underflow.

5–7. Giữ bản lịch sử; tạo adapter nhân quả và nhánh BOCPD miền log từ phép đã kiểm; ghi tên biến thể, khác biệt và nguồn. Ghi `W(061)` và `D:/RCA-flashticket/src/p6/reference_detection.py`.

8–9. Tám chuỗi nhỏ; so xác suất/posterior/MAP với phép tính trực tiếp ở miền an toàn; kiểm prefix; kiểm chuỗi dài gây underflow bằng fixture. Xong về số học/hành vi, chưa chứng minh ảnh hưởng toàn dev.

10–13. 4–5 giờ, máy 0,2–1 giờ; RAM 3 GiB, đĩa 0,5 GiB. Minh quyết có đưa biến thể vào so sánh chính. Một phiên vì chưa chạy full BOCPD trên toàn dev.

**T-062 — Kiểm detector tham chiếu trên dev và đo chi phí. Loại: thực nghiệm.**

1–4. Cần T-061, runner/evaluator và quyền dev. NSigma theo phạm vi hỗ trợ; BOCPD chỉ pilot được duyệt.

5–7. Tối đa 30 ca NSigma và ba ca BOCPD đại diện kích thước; kiểm ngưỡng, warm-up, báo động và chi phí theo độ dài. Dùng kết quả để trình phạm vi T-080–082, không tự chạy phần còn lại.

8–9. Đối chiếu báo động với trace điểm/ngưỡng; báo từng ca/ô và loại nhãn thời gian. Ghi `W(062)`. Nếu còn lookahead hoặc số không hữu hạn thì chặn sử dụng biến thể.

10–13. 3–4 giờ, máy 0,5–3 giờ; RAM 4–6 GiB, đĩa 1 GiB; tin cậy thấp về BOCPD. Lượt vượt một giờ cần Minh duyệt trước. Một phiên có theo dõi máy; không coi chia batch là miễn ngân sách.

**T-063 — Baseline một seed tại báo động P6. Loại: thực nghiệm so sánh.**

1–4. Cần cấu hình/báo động được chọn ở T-069, hợp đồng T-060 và runner đã kiểm. Dùng năm baseline một seed của TT.

5–7. Tối đa `5 × 30 = 150` lượt; ca không có báo động vẫn có bản ghi trạng thái. Dùng cùng cửa sổ được phép tại thời điểm báo cáo hạng; giữ mọi lỗi và chi phí. Ghi `W(063)`; không sửa mã baseline.

8–9. Kiểm đầu vào từng phương pháp, các hạng/khóa hòa và những ca đổi so với P3. Không so trực tiếp như thể đây là detector độc lập của baseline.

10–13. 3–4 giờ, máy 0,5–3 giờ; RAM 4 GiB, đĩa 1 GiB. Nếu pilot báo vượt thì trình ngân sách/đợt chạy cụ thể, không giảm phương pháp khó. Một phiên vì chỉ chạy mã đã pin, không sửa thuật toán.

**T-064 — TORAI tại báo động P6. Loại: thực nghiệm có seed.**

1–4. Cùng điều kiện T-063, dùng biến thể TORAI_B và quy tắc seed đã duyệt.

5–7. Tối đa `30 × 3 = 90` lượt; ghi cụm, khóa hạng, fallback và severity khi cần đối chiếu. Tái sử dụng môi trường riêng đã xác minh; không tự nâng thư viện. Ghi `W(064)`.

8–9. Kiểm tái lập một số lượt, hạng theo mọi seed, tỷ lệ fallback và mẫu số; không lấy seed tốt nhất. Nếu cần chuyển môi trường, đó là thay đổi phạm vi phải trình.

10–13. 3–4 giờ, máy 1–3 giờ; RAM 4–6 GiB, đĩa 1 GiB; tin cậy thấp đến vừa. Một phiên tách riêng vì seed và môi trường khác; Minh duyệt thời gian dài trước chạy.

**T-065 — Phân xử nhãn lan trên dev. Loại: phân tích nghiên cứu.**

1–4. Dùng bảng lời gọi P4 đã lưu và câu hỏi MRP; không dùng nhãn này làm đầu vào phương pháp.

5–7. Khai trước ba phân vị nền × ba mức θ: chín cấu hình mô tả × 52 ca, tối đa 468 bản phân loại. Giữ nhóm “không đo được”; đối chiếu ca đúng/sai tương ứng, kiểm tính vòng lặp của định nghĩa. Ghi `W(065)`.

8–9. Bảng chuyển nhóm theo ngưỡng, chứng cứ invocation → cờ → nhóm, và đánh giá có cần phân tầng này ở G3 không. Không cộng cờ chồng lấn thành tỷ lệ nguyên nhân.

10–13. 3–4 giờ, máy 0,1–0,5 giờ; RAM 3 GiB, đĩa 0,5 GiB. Minh quyết khóa định nghĩa, không dùng hoặc giữ OPEN; không tự gán nhãn chỉ để đủ bảng. Một phiên vì dùng trung gian đã có.

**T-066 — Tín hiệu theo thao tác ở lỗi return. Loại: phân tích cơ chế.**

1–4. Dùng span/log dev được phép, bảng nhóm P4 và T-047/049; đọc code/trung gian trước chạy thêm.

5–7. Lập đầy đủ nhóm ca liên quan và nhóm đối chiếu; so hai cửa sổ đối xứng hợp lệ, duration/count/outcome theo thao tác; giữ hướng tăng/giảm. Số ca lấy từ bảng nhóm có pin trước khi chạy, không chọn riêng ca thuận lợi. Ghi `W(066)`.

8–9. Chuỗi input → thao tác → đặc trưng → điểm và cặp đúng/sai tương ứng. Phân biệt phản ứng duration, lỗi nhanh và thiếu quan sát. Không suy log rate là tỷ lệ request thất bại nếu không nối được request.

10–13. 3–4 giờ, máy 0,2–0,7 giờ; RAM 4 GiB, đĩa 1 GiB. Kết quả quyết định giữ đặc trưng nào trong ngân sách đã khai; thay thiết kế vượt phạm vi phải trình. Một phiên vì một nhóm câu hỏi.

**T-067 — Ma trận dev TT. Loại: thực nghiệm.**

1–4. Cần T-041–060, 065–066 và mọi nhánh ứng viên được duyệt trước đó. Các module phải qua fixture trước full run.

5–7. Tối đa `60 × 8 × 23 = 11.040` đơn vị score/control, từ cache dùng chung; thực hiện smoke, chạy tuần tự theo dataset/config rồi phân tích theo 10 ô và từng ca. Ghi `W(067)`.

8–9. Kiểm tổng job, trạng thái, candidate, trung gian của ca đổi hạng/báo động và ca đúng tương ứng; tái tính bảng từ bản ghi. Không chỉ kiểm tổng trung bình. Nếu graph không thắng, vẫn báo đúng.

10–13. 4–5 giờ công, máy 1–4 giờ; RAM 4 GiB, đĩa kết quả tối đa 3 GiB sau đo cache; tin cậy thấp trước pilot. Vừa phiên nếu đo T-042/051 xác nhận; nếu không, T-083 phải xử lý trước, không chia khi đã chạy dở.

**T-068 — Ma trận dev OB. Loại: thực nghiệm.**

1–4. Cần cùng bộ mã với T-067, adapter OB và miền hỗ trợ đã khóa để thử.

5–7. Tối đa `22 × 8 × 23 = 4.048` đơn vị; loại tổ hợp cửa sổ trùng theo quy tắc đã khai; báo 13 ô, ít mẫu và coverage của từng tín hiệu. Ghi `W(068)`.

8–9. Kiểm timestamp từng kênh, mẫu thực dùng, graph operation/static unsupported và mọi trạng thái fallback. Không diễn giải thành phát hiện liên tục hoặc bằng chứng đồng bộ chính xác giữa các kênh.

10–13. 3–4 giờ, máy 0,5–2 giờ; RAM 3 GiB, đĩa 1 GiB; tin cậy thấp đến vừa. Một phiên riêng để không gộp hai giao thức khác nhau.

**T-069 — Chọn thiết kế trên dev. Loại: phân tích và đề xuất quyết định.**

1–4. Cần T-067/068, baseline audit và các phân tích cơ chế liên quan; chỉ đọc đầu ra đã kiểm.

5–7. So tám cấu hình tối đa theo tiêu chí khai trước: tính đúng/coverage trước, chất lượng đầu ra và chi phí sau; xếp hạng theo độ đo phù hợp, không chọn theo chênh graph–không graph. Lập bảng thành phần → mục đích → bằng chứng → điều kiện sai → lựa chọn đề nghị.

8–9. Giải thích cả ca hỗ trợ và phản bác, tách khác biệt dataset và phụ thuộc nhãn. Ghi `W(069)` với đặc tả phương pháp đề nghị và nội dung WHY/DECISIONS cần xin duyệt. Không tự ghi DECIDED.

10–13. 3–4 giờ, máy 0,1–0,3 giờ; RAM 1 GiB, đĩa 0,2 GiB. Kết quả yếu không tự buộc thêm thuật toán. Nếu chưa phân xử được lựa chọn cần thiết, G3 còn chặn. Một phiên vì không cài/rerun.

**T-070 — Độ nhạy và cơ chế trên TT. Loại: thực nghiệm phân tích.**

1–4. Cần lựa chọn thử cuối của T-069 và ma trận độ nhạy đã duyệt.

5–7. Tối đa `60 × 16 = 960` đơn vị thêm, tái dùng cache; phân tích theo ô và các nhóm cơ chế, trong đó có thiếu cạnh/tín hiệu và nền. Ghi `W(070)`.

8–9. Kiểm biến nào thật sự thay; giữ các phần khác cố định; đối chiếu mất/chuyển contribution với đổi hạng/báo động. Không gọi mọi sụt điểm là cùng một nguyên nhân.

10–13. 3–4 giờ, máy 0,5–2 giờ; RAM 4 GiB, đĩa 1 GiB. Nếu phát hiện lỗi tính đúng, quay về đúng module và xin phạm vi sửa; không tuning ngầm. Một phiên vì cấu hình đã cố định.

**T-071 — Độ nhạy và giới hạn trên OB. Loại: thực nghiệm phân tích.**

1–4. Cần T-069; cùng phép thay có ý nghĩa với OB, không ép đủ 16 nếu không hỗ trợ.

5–7. Tối đa `22 × 16 = 352` đơn vị; tập trung ít mẫu, shared metric, timestamp và mapping operation. Ghi `W(071)`.

8–9. Báo từng phép khả dụng/không khả dụng, root coverage và điểm thay vì chỉ điểm tổng. Không diễn giải thiếu dữ liệu là lỗi thuật toán đã xác nhận.

10–13. 3–4 giờ, máy 0,25–1 giờ; RAM 3 GiB, đĩa 0,5 GiB. Một phiên vì chỉ một miền dữ liệu và cấu hình đã chọn.

**T-072 — Kiểm toàn chuỗi và rò thông tin. Loại: kiểm tích hợp.**

1–4. Cần mọi module và cấu hình cuối; không còn chức năng mới được dự kiến.

5–7. Chạy 12 kịch bản fixture xuyên suốt và sáu ca dev đại diện: thêm tương lai, đổi tên ca, đổi đường dẫn, đảo nhãn ở evaluator, cache khác cutoff, missing, isolate, no-alarm, lỗi, unsupported, resume và lặp môi trường. Ghi `W(072)`; script kiểm nằm trong kết quả task.

8–9. So input → feature → score → alarm → region → rank → metric với oracle đã có. Method output không đổi khi chỉ thay metadata chấm. Nếu dùng dữ liệu sau alarm để xếp hạng, thời điểm trả kết quả phải phản ánh việc đó.

10–13. 3–4 giờ, máy 0,2–1 giờ; RAM 4 GiB, đĩa 1 GiB. Không sửa nhiều module ngay trong task kiểm: lập đề xuất sửa đúng nơi. Vừa phiên vì đây là kiểm đường nối đã có, không chứa thiết kế/cài lớn.

**T-073 — Hợp đồng bàn giao P7/P8/P9/P10. Loại: tài liệu và kiểm giao diện.**

1–4. Cần schema, thiết kế cuối, OPEN P5/P6 và B16. Repo hệ thống vẫn chỉ đọc.

5–7. Viết hợp đồng input/output cho cùng lõi offline/online; bảng evidence cho P8, không cho LLM đổi hạng; P7 nhận config/độ đo/đối chứng; P9a nhận R-01…R-10 cộng thiếu mới có chứng cứ; P10 nhận yêu cầu onset/recovery/workload/nhãn vùng và tiêu chí thu.

8–9. Kiểm bằng các payload đã có; mỗi OPEN có input thiếu, owner và quyết định bị chặn. Ghi `W(073)`, không sửa B16 hoặc gửi nhóm hệ thống. Không coi collector có thể khôi phục thông tin chưa từng ghi.

10–13. 3–4 giờ, máy 0,1–0,2 giờ; RAM 1 GiB, đĩa 0,2 GiB. Minh quyết nội dung chuyển và quyền gửi sau. Một phiên vì chỉ đóng gói giao diện đã cài.

**T-074 — Gói khóa thiết kế trình G3. Loại: tổng hợp quyết định.**

1–4. Cần T-063/064, 069–073 và các nhánh bắt buộc theo quyết định Minh. Không mở test.

5–7. Tập hợp code/revision, môi trường, cấu hình, hypothesis, độ đo, universe, seed, lỗi/unsupported/fallback, bảng diễn giải, đối chứng và danh sách quyền chưa có; kiểm manifest và hướng dẫn dựng trên máy khác. Ghi `W(074)`.

8–9. Kiểm mỗi kết luận nối tới đầu ra; không còn thiết kế/cài/kiểm dev bắt buộc bị giấu trong mục “sau G3”. Nếu còn thiếu thì ghi đúng nội dung chặn. Không đòi graph thắng.

10–13. 3–4 giờ, máy 0,1–0,2 giờ; RAM 1 GiB, đĩa 0,5 GiB. Minh quyết G3, commit và quyền mở test riêng. Một phiên vì chỉ đóng gói artifact đã hoàn tất; không tự nghiệm thu.

**9. Task có điều kiện**

Các task dưới đây **không được tự kích hoạt**. Điều kiện là phụ thuộc khoa học hoặc kỹ thuật, không phải kết quả “chưa đẹp”.

**T-075 — Ứng viên điểm phần dư có điều kiện.**

- Câu hỏi: một phép dự đoán từ lân cận có khả dụng và ổn định hơn họ ưu tiên trong điều kiện đầu vào hiện có không?
- Bắt đầu khi T-041/051 chỉ ra lý do phải xét; dùng đặc trưng/nền/graph đã kiểm. Đọc code CIRCA liên quan, không kế thừa mặc định mô hình hay bước cộng điểm.
- Cài một mô hình đơn giản có regularization và tối đa hai cấu hình; lưu dự đoán, phần dư, scale, condition/degeneracy và contribution. Ghi `W(075)` và `D:/RCA-flashticket/src/p6/scoring_residual.py`.
- Tám fixture có đáp án, cộng sáu ca khảo sát; kiểm nền phẳng, ít mẫu, cô lập và quan hệ sai. Thiếu nền thì trả đúng trạng thái, không tạo điểm cực lớn.
- Xong về khả dụng/tính đúng trước ma trận T-067/068. Không tự thay họ chính sau khi xem test. Nếu dùng, phải thay ma trận đã trình bằng phạm vi mới được Minh duyệt.
- 4–5 giờ công, máy 0,2–1 giờ; RAM 4 GiB, đĩa 1 GiB; tin cậy thấp đến vừa. Một phiên vì một mô hình hẹp, không gồm tìm kiến trúc.

**T-076 — TraceRCA: bước chọn tập sau E1.**

- Chỉ kích hoạt nếu định dùng chấm theo tập hoặc kết luận phụ thuộc cơ chế này.
- Dùng trung gian E1 có pin; giữ mọi thứ, chỉ đổi việc giữ tập singleton đã khai phá. Hai nhánh trên đúng tập ca E1; số ca được chép từ manifest trước chạy.
- Lưu tập trước/sau, support/confidence và đường tới hạng; oracle tập nhỏ độc lập. Ghi `W(076)`, không sửa baseline gốc.
- Hỗ trợ hoặc bác bỏ đúng vai trò bước chọn tập; kết quả chưa chọn phương pháp P6.
- 3–4 giờ, máy dự kiến dưới 0,5 giờ; RAM 3 GiB, đĩa 0,5 GiB; tin cậy vừa. Minh duyệt phép đổi duy nhất. Vừa phiên vì không chạy lại mọi biến thể TraceRCA.

**T-077 — TraceRCA: đối chiếu cờ frontend theo invocation.**

- Chỉ kích hoạt nếu dùng nhánh tác giả hoặc lập luận về cờ frontend.
- Dùng bảy cặp đã chỉ trong G2 và bảng invocation đã lưu; so nhánh lời văn với nhánh tác giả, giữ đầu vào chung.
- Nối từng invocation → cờ → tập → contribution → hạng, kiểm cả cặp không khác. Ghi `W(077)`.
- Xong khi phân biệt được do định nghĩa invocation, cờ hay bước sau; thiếu trung gian thì nêu chính xác phép thu thêm, không đoán.
- 3–4 giờ, máy dưới 0,5 giờ; RAM 3 GiB, đĩa 0,5 GiB. Một phiên vì bảy cặp đã xác định. Minh quyết phép bổ sung nếu dữ kiện chưa đủ.

**T-078 — Cài ứng viên chấm theo tập.**

- Chỉ sau T-076/077 và quyết định cho thử; không mặc định mọi kết quả của chúng dẫn tới cài.
- Cài miner/scorer hẹp theo định nghĩa được duyệt, ràng buộc support và finite value; giữ tập và chứng cứ dùng để xếp hạng. Ghi `W(078)` và `D:/RCA-flashticket/src/p6/scoring_patterns.py`.
- Sáu tập giả có đáp án và sáu ca khảo sát; kiểm singleton, tập trùng, mẫu mới, tập rỗng, thứ tự và số không hữu hạn.
- Không gọi đây là graph-based detection nếu phép tính vẫn chưa dùng quan hệ; không thay nghĩa vụ T-051.
- 4–5 giờ, máy 0,2–1 giờ; RAM 4 GiB, đĩa 1 GiB. Nếu đưa vào full matrix, phải trình lại số tổ hợp trước T-067/068. Vừa phiên vì chỉ cài một cơ chế đã có định nghĩa.

**T-079 — MicroRank: phần còn lại sau bộ chia và cách đếm.**

- Chỉ cần trước khi chọn cơ chế xếp hạng tương ứng hoặc nâng biến thể thành baseline.
- Đọc trung gian hai ca chưa rõ cùng ca đúng có điều kiện tương ứng; tách cohort, count, PageRank weight và spectrum.
- Tối đa bốn phép thay một yếu tố trên tập chẩn đoán được duyệt; ghi `W(079)`.
- Oracle graph/trace nhỏ và kiểm từng hạng. Không cộng tác dụng các phép đổi chạy trên cohort khác nhau.
- 3–4 giờ, máy 0,2–1 giờ; RAM 4 GiB, đĩa 1 GiB. Một phiên vì câu hỏi cơ chế giới hạn; chưa cài biến thể sản xuất.

**T-080, T-081, T-082 — BOCPD nhân quả, ba batch toàn dev.**

Đây là ba task riêng, cùng hợp đồng nhưng đầu vào không trùng:

| Task | Phạm vi |
|---|---|
| T-080 | 10 mã mờ đầu theo danh sách được khóa |
| T-081 | 10 mã mờ tiếp |
| T-082 | 10 mã mờ cuối |

- Chỉ kích hoạt nếu Minh chọn đưa BOCPD nhân quả vào so sánh cần bao phủ toàn dev và duyệt chi phí.
- Cần T-061/062, pin code, cấu hình duy nhất và danh sách 30 ca. Không đổi tham số giữa batch.
- Mỗi task chạy tối đa 10 chuỗi full; lưu posterior/MAP hoặc trung gian đủ tái dựng, điểm, báo động, chi phí và lỗi; dùng `W(080)`, `W(081)`, `W(082)` tương ứng, không sửa mã.
- Kiểm prefix/finite từ T-061 vẫn phải khớp; đối chiếu mọi ca đổi báo động với bản lịch sử nhưng tách tác động tiền xử lý và số học.
- Mỗi task 2–3 giờ công, máy tạm tính 2–3,5 giờ; RAM dự kiến tối đa 6 GiB, đĩa 1 GiB; độ tin cậy thấp, phải thay bằng đo T-062.
- Vừa một phiên có theo dõi và ghi kết quả nếu pilot xác nhận. Tổng ba batch vẫn là một ngân sách phương pháp. Chia batch không miễn lời duyệt lượt trên một giờ hoặc ngoại lệ ngân sách Q-40.
- Nếu thời gian vượt phạm vi phiên, phải sửa cách thực hiện trong đề xuất trước khi chạy; không tự bật máy tính phí.

**T-083 — Xử lý đúng nút thắt hiệu năng đã đo.**

- Chỉ kích hoạt khi T-042 hoặc smoke của module cho thấy ma trận không vừa RAM/thời gian/đĩa.
- Chọn đúng một nút thắt có profile: chỉ mục span, sao chép mảng hoặc cache; không làm tối ưu tổng quát.
- Ghi `W(083)` và đúng file mã đã trình Minh trong đề xuất sửa; giữ đường triển khai trước để so.
- Sáu ca khảo sát × trước/sau; đầu ra khoa học phải bằng nhau, đo peak RAM/byte/thời gian. Không nén mất trung gian cần phân xử.
- 4–5 giờ, máy 0,5–2 giờ; RAM tối đa 6 GiB, đĩa 2 GiB. Nếu cần thay schema hoặc thuật toán, dừng và trình. Một phiên vì một bottleneck đã biết.

**T-084 — TraceRCA nhánh tác giả thành baseline bổ sung.**

- Chỉ khi T-060 và, nếu liên quan, T-076/077 cho phép định nghĩa biến thể rõ.
- Dùng revision và đầu vào đã kiểm; giữ tên latency-only hoặc phạm vi thật, không gọi là toàn phương pháp bài gốc.
- Cài wrapper riêng, kiểm sáu fixture và pilot; full dev theo phạm vi được duyệt, tối đa 52 ca hỗ trợ. Ghi `W(084)` và `D:/RCA-flashticket/src/p6/baseline_tracerca_author.py`.
- Kiểm intermediary/finite/tie/coverage; báo tách baseline hiện hành. 3–4 giờ công, máy 0,5–2 giờ; RAM 4 GiB, đĩa 1 GiB; tin cậy thấp đến vừa.
- Vừa phiên chỉ khi pilot xác nhận và không còn sửa thuật toán. Minh quyết tư cách baseline và ngân sách.

**T-085 — MicroRank biến thể được duyệt thành baseline bổ sung.**

- Chỉ sau T-079 và quyết định về bộ chia/count/weight cụ thể.
- Tạo wrapper bất biến, kiểm fixture cohort/PageRank/spectrum; tối đa 52 ca hỗ trợ, giữ các trung gian quyết định hạng.
- Ghi `W(085)` và `D:/RCA-flashticket/src/p6/baseline_microrank_variant.py`.
- Kiểm tương đương với phép chẩn đoán nguồn và cách khác bài gốc; không thay baseline P3 âm thầm.
- 3–4 giờ công, máy 0,5–3 giờ; RAM 4–6 GiB, đĩa 1 GiB; phải pilot trước full. Một phiên vì triển khai biến thể đã xác định, không còn tìm cơ chế.

**T-086 — OM-07 phục vụ kết luận P6 có phụ thuộc.**

- Chỉ kích hoạt nếu static comparison hoặc lựa chọn graph thực sự phụ thuộc checkout→currency.
- Đọc lại code nguồn và trung gian đã lưu; chỉ đếm/đối chiếu span mồ côi hoặc đường gọi trong dev được phép khi cần.
- Lập chuỗi source → mapping → quan sát; so với các cạnh đúng có điều kiện tương ứng. Ghi `W(086)`, không sửa kết quả P5.
- Không có runtime lineage thì kết luận vẫn có điều kiện; không dùng không thấy cạnh để xác nhận không có lời gọi.
- 3–4 giờ, máy 0,2–1 giờ; RAM 4 GiB, đĩa 1 GiB. Minh duyệt phạm vi mới ngoài P5. Một phiên vì chỉ một câu hỏi đã xác định.

**T-087, T-088, T-089 — Kiểm underflow trên tiền xử lý lịch sử còn lại.**

Ba task này khác T-080–082: giữ **đầu vào full lịch sử** để trả lời câu hỏi còn lại sau E2, không dùng chúng để chứng minh online nhân quả.

| Task | Phạm vi dự kiến trong 28 ca còn lại |
|---|---:|
| T-087 | 10 ca |
| T-088 | 9 ca |
| T-089 | 9 ca |

- Chỉ kích hoạt nếu kết luận về BOCPD lịch sử hoặc việc dùng số P3 phụ thuộc kết quả này.
- Dùng NPZ nguồn và bản miền log đã kiểm, sau xác minh manifest và khả dụng máy; không lấy dữ liệu qua repo lưu trữ.
- Mỗi task so posterior/MAP/change point của hai phép tính số học trên cùng đầu vào; lưu đầy đủ sai khác. Dùng `W(n)` tương ứng; không đổi preprocessing.
- Hai ca E2 đã có được dùng lại sau hash, không chạy lại để đủ số.
- Mỗi task 2–3 giờ công, máy khoảng 2–3,5 giờ; RAM/đĩa phải đo, dự kiến trần 6 GiB/1 GiB mỗi batch. Căn cứ thời gian cũ khoảng 909 giây/chuỗi trên máy cũ; không coi đó là tốc độ laptop.
- Tổng phần còn lại đã có dự báo khoảng bảy giờ máy trên điều kiện cũ. Cần Minh duyệt chi phí và xử lý ngân sách trước. Một phiên mỗi batch chỉ khả thi sau kiểm máy; không suy quyền EC2 từ quyền task lịch sử.
- Kết quả chỉ giải quyết underflow trong giao thức lịch sử; câu hỏi nền khỏe, onset và nhìn tương lai vẫn riêng.

**10. Phụ thuộc, đường găng và song song**

Chuỗi chính:

```text
041 → 042 → 043
             ├→ 044 ─┐
             └→ 045 ─┴→ 046 → 047 ─┐
                     ├→ 048 ───────┤
                     └→ 049 ───────┴→ 050 → 051 → 052/053/054
                                                └→ 057/058/059
043 + các đầu ra trên → 055/056
060 → 061 → 062
P4 + 047/049 → 065/066
tất cả phần cần thiết → 067/068 → 069
069 → 063/064 + 070/071
cấu hình cuối + các kết quả → 072 → 073 → 074 → Minh xem G3
```

T-075–079, 084–086 phải được quyết định trước ma trận hoặc kết luận phụ thuộc. T-080–082 và T-087–089 chỉ chặn đúng kết luận/so sánh BOCPD tương ứng; không tự chặn mọi công việc độc lập.

**Đường găng dự kiến:** hợp đồng → đầu vào → cây/đặc trưng → chuẩn hóa → điểm/đầu ra → đối chứng → ma trận dev → lựa chọn → độ nhạy/kiểm toàn chuỗi → G3.

Khả năng song song có lợi, chỉ thực hiện khi Minh duyệt phân công:

- T-044 và T-045: hai adapter, không chung file.
- T-048 và T-049 sau hợp đồng; T-047 sau cây span.
- T-053 và T-054 sau điểm.
- T-057, 058, 059 sau API đã ổn định.
- T-060 và các phân tích P4 độc lập với việc cài.
- TT và OB có thể phân tích song song; không mặc định chạy nặng đồng thời trên laptop.

Xung đột ghi cần tránh:

- Mỗi module có một task sở hữu.
- `contracts.py` do T-043 sở hữu; thay đổi sau phải đề xuất, không để các task tự mở rộng khác nhau.
- Không cho hai task cùng sửa WHY/DECISIONS.
- Mỗi task chỉ cập nhật dòng STATE của mình; không ghi lại toàn STATE.
- Mã P3/P5 và kết quả cũ giữ nguyên, trừ khi có đề xuất sửa riêng được duyệt.

**11. Ngân sách tổng và điều kiện khả thi**

Tổng 34 task đường chính dự kiến:

| Khoản | Dự toán |
|---|---:|
| Giờ công người làm, đã gồm tự kiểm/tài liệu/bàn giao | 109–144 giờ |
| Phản biện chính thức, khoảng 1–2 giờ/task | 34–68 giờ |
| Dự phòng sửa/hồi quy thông thường 20% | Khoảng 29–43 giờ |
| Tổng công đường chính | **Khoảng 172–255 giờ** |
| Máy đường chính, trước dự phòng | Khoảng 8–32 giờ |
| Máy có dự phòng | **Khoảng 10–39 giờ** |

Đây là cộng khối lượng, không phải lịch hứa hoàn thành. Thời gian chờ Minh, chờ phản biện và chờ nguồn bên ngoài chưa nằm trong số giờ công.

Nếu mọi nhánh có điều kiện đều được kích hoạt, cộng khoảng **42–57 giờ người làm**, phản biện và sửa khiến phần cộng có thể khoảng **68–105 giờ công**. Không khuyến nghị chạy tất cả. Một số nhánh là lựa chọn thay thế.

**RAM và đĩa**

- Chạy nặng mặc định một worker; chỉ nâng khi có số đo.
- Dự kiến giới hạn làm việc 4–6 GiB mỗi tiến trình để còn chỗ cho hệ điều hành và ứng dụng.
- Dự trù cache cấu trúc/đặc trưng dùng chung 6–8 GiB; kết quả và trung gian phép chạy 4–6 GiB; lượt lỗi, hồi quy và bản giữ thêm 4–6 GiB.
- Tổng tăng dự kiến **14–20 GiB**, còn phải đo ở T-042. Không lấy tổng các trần từng task làm dự báo disk vì nhiều task đọc cùng cache.
- Nếu cần hơn dung lượng khả dụng, trình nơi lưu hoặc tài nguyên mới. Không xóa lượt cũ, không bỏ trung gian khoa học để vừa đĩa.
- Không tải dữ liệu hoặc tạo máy tính phí trong ngân sách mặc định.

Phần máy dài có thể chạy độc lập sau khi đầu vào/config đã khóa, nhưng vẫn cần theo dõi lỗi, tài nguyên và lưu tiến độ. Giờ máy không được cộng máy móc vào giờ công, cũng không được coi là không cần người giám sát.

Q-40 và luật báo trước lượt trên một giờ vẫn áp dụng. Ngoại lệ của task lịch sử không chuyển sang P6.

**12. Bảng kiểm khối lượng dễ bị bỏ sót**

| Phần dễ bị bỏ | Đã giao |
|---|---|
| Đọc lại trace vì graph gộp không đủ invocation/duration | 042, 046–047 |
| Thời điểm khả dụng của span và graph online | 044, 046, 052, 072 |
| OB ít mẫu và timestamp từng kênh | 045, 048, 050, 068, 071 |
| Shared signal bị nhân thành nhiều bằng chứng | 043, 048–049, 054 |
| Thực thể không có cạnh nhưng có tín hiệu | 050–054, 056 |
| Thiếu cả tín hiệu, root vắng và mẫu số toàn ca | 054, 056 |
| Ca lỗi, timeout, unsupported, no-alarm, fallback | 055–056 |
| Cửa sổ sau alarm làm tăng thời điểm trả hạng | 044, 052, 063–064, 072 |
| Thông tin quan hệ còn lại trong “không đồ thị” | 057 |
| Graph ngẫu nhiên không đổi hoặc không xáo được | 058 |
| Mapping/coverage thay cùng graph tĩnh | 059 |
| Seed TORAI và môi trường riêng | 060, 064 |
| BOCPD số học khác BOCPD nhân quả | 061–062, 080–082, 087–089 |
| Nhãn lan, return theo operation | 065–066 |
| Ca đúng để đối chiếu ca sai | 065–071 |
| Lượt hỏng, cache, hash, phục hồi trên máy khác | 042, 055, 074 |
| Yêu cầu typed edge chưa có runtime công khai | 041, 043, 051, 073 |
| P8 không được tự đổi hạng | 073 |
| Quyền commit/test tách quyền khóa thiết kế | 074 |

T-072 chỉ kiểm giao diện đã cài. T-073 chỉ bàn giao hợp đồng đã có. T-074 chỉ đóng gói để Minh quyết. Không task cuối nào được dùng làm chỗ chứa thuật toán, adapter hoặc đối chứng chưa phân rã.

**13. Quyết định Minh cần xem xét, gom một lượt**

Đề nghị Minh quyết sau phản biện kế hoạch:

1. **Phân rã và thứ tự:** chấp nhận đường chính, các nhánh có điều kiện và cách mở từng SPEC; chưa cấp quyền chạy toàn chặng.
2. **Họ ứng viên ưu tiên thử:** chấp nhận hướng đưa chứng cứ theo quan hệ để T-041 đặc tả; hoặc yêu cầu phương án khác. Đây không phải chọn thuật toán cuối.
3. **Ngân sách:** chấp nhận khoảng công sức và cho phép T-042 đo khả thi; chưa duyệt mọi lượt dài.
4. **Baseline:** giữ baseline P3 cố định làm tham chiếu, các đối chứng phương pháp mới có cùng ngân sách; hoặc bổ sung tuning baseline mạnh bằng phạm vi riêng.
5. **BOCPD:** quyết việc nào cần cho kết luận P6: bản nhân quả toàn dev, kiểm underflow lịch sử còn lại, cả hai hoặc giữ giới hạn. Nếu chưa làm phần cần thiết, kết luận phụ thuộc không được trình như đã đủ.
6. **Vai trò:** dự kiến Codex làm, Claude phản biện từng task; không áp ngoại lệ lượt kế hoạch cho kết quả task.
7. **Song song:** ưu tiên các module không chung file; chưa dùng subagent hoặc mở phiên tự động.
8. **Lưu kế hoạch:** sau khi sửa theo phản biện và được duyệt, đề xuất tạo `D:/RCA-flashticket/docs/PLAN-P6.md`.

Không cần Minh quyết ngay công thức cuối, ngưỡng cuối hoặc mức graph cuối. Các quyết định ấy phải dựa trên đầu ra dev đã được giao.

**14. Phạm vi file cần tạo/sửa sau khi được duyệt**

Đề xuất lưu kế hoạch trước bằng gói cụ thể:

| File | Nội dung | Ảnh hưởng |
|---|---|---|
| `D:/RCA-flashticket/docs/PLAN-P6.md` | Toàn kế hoạch đã được duyệt, trạng thái nhánh và dự toán | Nguồn điều phối P6, không thay MRP hoặc SPEC |
| `D:/RCA-flashticket/docs/DECISIONS.md` | Chỉ nguyên lời quyết định Minh về kế hoạch, sau khi trình dòng ghi | Ghi quyền và lựa chọn thật sự được duyệt |
| `D:/RCA-flashticket/docs/STATE.md` | Con trỏ kế hoạch và bước tiếp theo được duyệt | Không đổi trạng thái nghiệm thu task cũ |

Sau đó mỗi task mới trình riêng `SPEC.md`, `LOG.md`, dòng STATE, thư mục kết quả và các file mã đã nêu trong hồ sơ. Không tạo đồng loạt 49 thư mục.

Các thay đổi quan trọng về phương pháp được trình nội dung WHY/DECISIONS tương ứng trước khi dùng làm quyết định. Không tự sửa MRP, AGENTS, P3/P5, B16 hoặc repo hệ thống từ quyền duyệt kế hoạch.

Nội dung cần đưa vào tài liệu nghiên cứu chính thức về sau: phạm vi dataset/chế độ, nguồn cạnh, scope tín hiệu, khác biệt thiết kế–runtime, định nghĩa điểm/vùng/hạng, tính nhân quả theo thời gian, đối chứng và những kết luận chưa phân xử được.
:::

Tự soát của người lập kế hoạch:

- Đã tách bằng chứng đủ để thử, chọn trên dev và khẳng định lợi ích trên test.
- Đã phân công đầu vào, trung gian, đối chứng, lỗi/mẫu số và giao diện chặng sau.
- Dự toán máy, đĩa và thời lượng phiên vẫn có độ tin cậy thấp ở phần trích trung gian và BOCPD. T-042/T-062 phải xác nhận trước các lượt phụ thuộc; chưa thể coi toàn chặng đã sẵn sàng triển khai.
- Các lựa chọn khoa học và quyền ghi/chạy còn chờ Minh. Chưa có quyết định mới được ghi chính thức.

Báo cáo bốn mục:

1. **Đã làm:** khảo sát nguồn, mã, hợp đồng, đầu ra và khối lượng; lập kế hoạch cùng các nhánh xử lý.
2. **File thay đổi:** không sửa file nào. Trạng thái Git cuối lượt giống đầu lượt.
3. **Kiểm đã chạy:** đọc nguồn, kiểm hash các manifest liên quan, đối chiếu pin V2 và B16, kiểm danh sách task và tính số tổ hợp. Không chạy thực nghiệm mới hoặc mở dữ liệu khóa.
4. **Còn cần Minh quyết:** chuyển phản biện, sửa kế hoạch và duyệt phạm vi tiếp theo. Kế hoạch chưa chọn thuật toán, chưa xác nhận giả thuyết, chưa cấp quyền G3/test.

Minh copy prompt dưới đây và **gửi kèm nguyên văn khối kế hoạch phía trên**. Phần tự soát của người lập không cần đưa vào tài liệu phản biện.

:::writing{variant="standard" id="61428"}
Bạn phản biện độc lập TOÀN BỘ kế hoạch P6 trong repo D:\RCA-flashticket.

Minh gửi kèm nguyên văn khối “KẾ HOẠCH TOÀN CHẶNG P6 — ĐỀ XUẤT ĐỂ PHẢN BIỆN”. Kế hoạch đang nằm trong chat, chưa được lưu thành file. Nếu chưa nhận đủ khối kế hoạch, đề nghị Minh gửi đủ; không dùng đường dẫn tới file kế hoạch dự kiến như thể file đã tồn tại.

Codex phiên lập kế hoạch là người lập. Codex phiên mới này là người phản biện độc lập kế hoạch theo yêu cầu Minh. Phân công này chỉ áp dụng lượt kế hoạch; không tự áp sang phản biện kết quả các task sau.

Chỉ đọc và trả lời trong chat. Không sửa kế hoạch hoặc file khác, không tạo task chính thức, không chạy thực nghiệm mới, không mở test/dataset giữ ngoài, không tải dữ liệu, không commit/push, không mở phiên, không dùng subagent và không tự gửi prompt.

Tài liệu đầu vào bổ sung — nguyên văn yêu cầu của Minh về độ chi tiết và khảo sát khối lượng:

“Mục tiêu lượt này là kế hoạch đủ sâu để người triển khai không tới lúc bắt tay làm mới phát hiện khối lượng vốn đã có thể biết và lại yêu cầu chia task. Phải khảo sát khối lượng trước khi chốt phân rã. Không giảm phép kiểm hoặc thu hẹp mục tiêu nghiên cứu để làm task trông vừa một phiên.

Không hứa nghiên cứu sẽ không có phát hiện mới. Phân biệt rõ:
- Công việc và rủi ro đã có thể nhận diện từ nguồn hiện có: phải được tính và chia ngay trong kế hoạch.
- Công việc phụ thuộc kết quả chưa có: phải có nhánh xử lý, task phụ thuộc dự kiến và tác động chi phí.
- Phát sinh thật sự chưa thể biết: nêu điều kiện phải trình Minh; không dùng nó làm lý do để bỏ khảo sát ban đầu.”

“## 3. Khảo sát trước khi chia task

Lập danh mục công việc thực tế, rồi mới quyết số lượng task. Không chốt trước một con số task cho đẹp.

Với từng nhóm việc:
- Chỉ ra module/API, schema, đầu vào và kết quả sẵn có; phần nào tái sử dụng được, phần nào phải viết hoặc kiểm lại.
- Xác định đơn vị xử lý: span, request, cửa sổ, graph, service/thao tác, cấu hình, seed, dataset và chế độ đánh giá.
- Tính số tổ hợp phải thực hiện từ phạm vi đề xuất. Tách số đã kiểm với dự toán.
- Tính cả đọc nguồn, thiết kế, cài đặt, fixture/oracle, kiểm trung gian, chạy dev, phân tích theo ca/ô, tài liệu, manifest, LOG và bàn giao.
- Ước lượng giờ công, thời gian máy, RAM, dung lượng, số lượt chạy và dự phòng sửa lỗi/hồi quy; nêu căn cứ hoặc khoảng bất định.
- Phân biệt thời gian máy có thể chạy độc lập với công việc cần agent theo dõi. Không mặc định chia một lượt chạy dài thành nhiều phiên sẽ tự giải quyết được mọi vấn đề.
- Kiểm phụ thuộc thật và giao diện giữa các phần; chỉ rõ phần có thể làm song song, phần bắt buộc tuần tự và xung đột ghi mã chung.

Không chạy benchmark/pilot mới trong lượt PLAN. Nếu thiếu phép đo khiến chưa thể ước lượng hoặc chốt phạm vi, nêu rõ và đặt một task khảo sát khả thi có đầu ra, ngân sách, tiêu chí quyết định và các nhánh kế tiếp đã được dự kiến. Không đánh tráo một kế hoạch chưa hoàn chỉnh thành kế hoạch triển khai toàn chặng đã chốt.”

“## 5. Hồ sơ chi tiết cho từng task dự kiến

Kiểm thư mục tasks và mã đã dùng trước khi đề xuất mã mới. Các mã chỉ là dự kiến cho tới khi Minh duyệt.

Với MỖI task, trình đủ:
1. Mã/tên, loại task và câu hỏi nguồn.
2. Mục tiêu cụ thể; phần mục tiêu nghiên cứu được bao phủ.
3. Điều kiện bắt đầu và phụ thuộc tới đầu ra cụ thể của task trước.
4. Đầu vào: file, schema/API, revision/manifest, miền dữ liệu và quyền cần có.
5. Công việc theo bước; module/hàm dự kiến tái sử dụng hoặc bổ sung; không mô tả bằng câu chung như “cài phương pháp và kiểm”.
6. Ma trận cấu hình/phép kiểm/ca cần chạy, số tổ hợp dự kiến, thứ tự và cách dùng lại trung gian.
7. Đầu ra và phạm vi ghi dự kiến tới đường dẫn; quyền ghi mã chung hoặc tài liệu quyết định phải được tính trước.
8. Kiểm đúng đắn độc lập: đầu vào → xử lý → trung gian → đầu ra, oracle/fixture, kiểm không nhãn và hồi quy cần thiết.
9. Tiêu chí xong kiểm được; kết quả nào hỗ trợ, bác bỏ hoặc chưa phân xử; kết luận nào chưa được phép.
10. Giờ công, thời gian máy, RAM/disk và độ tin cậy dự toán; tính cả tự kiểm, ghi kết quả và bàn giao.
11. Rủi ro, phần chưa biết, nhánh xử lý đã dự kiến và ảnh hưởng tới task sau.
12. Vai trò dự kiến và điểm cần Minh quyết; không tự đổi phân công chính thức hoặc cấp ngoại lệ.
13. Vì sao task này vừa một phiên theo quy định repo.

Nếu một task vẫn chứa nhiều câu hỏi độc lập, nhiều thành phần mới hoặc tổ hợp chạy/kiểm quá lớn, chia ngay trong kế hoạch. Tránh những task cuối chặng mang tên “tổng hợp”, “tích hợp” hoặc “kiểm đầy đủ” nhưng thực tế còn giấu phần thiết kế/cài đặt lớn.

Không cần chép lặp toàn bộ boilerplate SPEC cho mọi task. Tuy nhiên mức chi tiết phải đủ để sau này viết SPEC không phải khám phá lại khối lượng và cấu trúc phân rã.”

Đánh giá toàn bộ kế hoạch và các giao diện giữa task: độ khớp mục tiêu nguồn, căn cứ thiết kế, khả năng phân xử, phần bỏ sót/chồng lặp, khối lượng từng phiên, dự toán tổng, phụ thuộc, task có điều kiện, tích hợp và G3. Phân biệt lỗi kế hoạch thật với bất định nghiên cứu hợp lệ. Không đòi kết quả thực nghiệm chưa được duyệt và không thu hẹp mục tiêu để làm task vừa phiên.

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch toàn chặng P6, nguyên văn được Minh gửi kèm trong chat; chưa có task chính thức hoặc file kế hoạch.
- Công đoạn: soát SPEC.
- Gói/cổng: đề xuất phân rã P6, chuẩn bị công việc trước G3.
- Người làm và người phản biện chính thức: Codex phiên lập kế hoạch là người lập; Codex phiên mới này phản biện độc lập kế hoạch theo yêu cầu Minh; phân công chỉ áp dụng lượt kế hoạch.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/docs/STATE.md; D:/RCA-flashticket/docs/MRP.md; D:/RCA-flashticket/docs/WHY.md; D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/LESSONS.md; D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md; D:/RCA-flashticket/docs/review-prompt.md; D:/RCA-flashticket/tasks/_MAU/SPEC.md; SPEC và LOG của T-034–T-040; nguyên văn kế hoạch và yêu cầu Minh gửi trong chat.
- Phản biện và phản hồi trước: chưa có bản phản biện của kế hoạch này được cung cấp.
- Code và kết quả liên quan: D:/RCA-flashticket/src/do_thi/; D:/RCA-flashticket/src/do_thi_tinh/; D:/RCA-flashticket/src/p3/; mã baseline liên quan trong D:/RCA-flashticket/src/; D:/RCA-flashticket/results/T-034/goi-g2.md; D:/RCA-flashticket/results/T-035/ đến D:/RCA-flashticket/results/T-040/; nguồn T-032/T-033 theo con trỏ gốc; manifest hiện hành và pin lịch sử tương ứng trên các file thật. Đọc D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md khi cần, theo luật trực tiếp chi phối repo đó; repo hệ thống chỉ đọc. Không đọc D:/Project/flash-ticket-rca-research.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; không ghi file.

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
:::
````

</details>

<a id="s03"></a>

### S03 — Phản biện bản đầu

<details>
<summary>Mở nguyên văn S03</summary>

````text
**Tôi chưa khuyến nghị duyệt nguyên trạng kế hoạch P6 này.** Lo ngại của Minh có cơ sở: kế hoạch khảo sát khá kỹ các phần phải làm, nhưng chưa tổ chức tốt theo ưu tiên **giảm rủi ro thất bại của toàn đồ án**.

Cần chỉnh một điểm về số lượng: [STATE](D:/RCA-flashticket/docs/STATE.md) có **38 mã task lịch sử thuộc P1–P5**, gồm cả T-020 được thay bằng T-021. P6 đề xuất **34 task chính, tối đa 49 nếu kích hoạt mọi nhánh**. Vì vậy, đường chính chưa nhiều hơn toàn bộ P1–P5, nhưng đã gần bằng. Số task tự nó chưa chứng minh kế hoạch quá lớn; điều đáng hỏi là công sức ấy có đưa đồ án tới kết quả cần thiết đủ sớm không.

Tôi lấy ưu tiên Minh vừa xác nhận làm căn cứ: **đồ án hoàn chỉnh, bảo vệ được; phương pháp có căn cứ, đánh giá hợp lệ, tích hợp chạy thật; cố gắng tạo cải thiện có ý nghĩa trong nhóm điều kiện xác định.** Đây chưa phải thay đổi các yêu cầu đã duyệt.

**Ba điểm phản biện chính**

**1. CHẶN việc duyệt nguyên đường triển khai: kiểm khả năng thành công của phương pháp còn quá muộn.**

Trong đề xuất, ma trận dev T-067 cần T-041–060 và T-065–066; kiểm xuyên suốt nằm ở T-072. T-042 đo khả thi tài nguyên, còn các task trước chủ yếu kiểm từng module.

Kế hoạch **có fixture, kiểm trung gian và smoke test**, nên không thể nói nó bỏ kiểm sớm. Nhưng những việc đó chưa thay được câu hỏi quan trọng nhất:

> Trên dữ liệu thật, phép tính dùng quan hệ có giữ hoặc bổ sung được thông tin cần để phân biệt nguyên nhân với triệu chứng không?

Nếu tới khi đủ adapter, đặc trưng, cache, evaluator và các đối chứng mới phát hiện cơ chế chính không có thông tin hữu ích, chi phí đổi hướng sẽ lớn.

**Sửa tối thiểu:** đưa một lượt thử trọn chuỗi trên dev lên sớm, sau phần đầu vào và phép tính cần thiết. Lượt này phải có ca hỗ trợ, ca phản bác và nhóm khó liên quan đến giả thuyết; đối chiếu với nhánh không quan hệ và baseline phù hợp. Nó kiểm khả năng phân xử và tính đúng, **không buộc đồ thị thắng mới được tiếp tục**, cũng không thay đánh giá đầy đủ trước G3.

Đây là cách ưu tiên việc khó: kiểm sớm giả thuyết khoa học có thể làm cả phương án thất bại.

**2. CHẶN việc duyệt toàn bộ phạm vi mặc định: một số việc còn phụ thuộc lựa chọn thiết kế nhưng đã được đặt vào đường chính.**

Ví dụ cụ thể trong [kế hoạch được gửi](<C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt:229>):

| Phần | Vấn đề cần sửa |
|---|---|
| T-046–047: cây request và phần thời gian không bị span con phủ | Phải xác định phần nào công thức được chọn thật sự cần. Họ gán chứng cứ thời lượng theo cạnh chưa tự đòi toàn bộ phép phân rã thời gian. |
| T-061–062: biến thể detector tham chiếu, gồm BOCPD | Kế hoạch còn để Minh quyết việc dùng biến thể, nhưng công việc chuẩn bị nó đã thuộc đường chính. Cần tách phần bắt buộc để có đối chứng hợp lệ với phần nghiên cứu thêm về BOCPD. |
| T-065: phân xử nhãn “lan” | [MRP](D:/RCA-flashticket/docs/MRP.md:192) đặt điều kiện cho việc phân tầng này. Cần giải thích vì sao nó chặn thiết kế đang thử, thay vì mặc định chặn toàn ma trận dev. |
| Tám cấu hình × mọi họ đối chứng × 20 seed ngẫu nhiên | Phép nhân ra **15.088 đơn vị chấm** là đúng. Nhưng con số đó chưa có nghĩa mọi tổ hợp đều cần để quyết định thiết kế. |

Kế hoạch đã ghi đây là dự toán, dùng lại cache và loại tổ hợp không có nghĩa. Đó là điểm tốt. Tuy vậy, **một trần công việc chưa phải phạm vi tối thiểu cần thiết**.

**Sửa tối thiểu:** nối từng việc với lựa chọn hoặc kết luận mà nó bảo vệ. Giữ các đối chứng bắt buộc và kiểm độ nhạy theo MRP; xác định ma trận phù hợp với thiết kế thực sự được thử. Không tự bỏ mức thao tác, BOCPD hay nhóm khó chỉ vì tốn công; cũng không mặc định triển khai hết khi chưa có phụ thuộc rõ.

**3. CHẶN việc coi kế hoạch đã khả thi cho toàn đồ án: ngân sách P6 chưa gắn với phần việc còn lại.**

Tổng **109–144 giờ người làm** cộng đúng từ 34 task. Sau phản biện và dự phòng, đề xuất thành **172–255 giờ công**, chưa gồm thời gian chờ và các nhánh có điều kiện.

Trong khi đó, [MRP](D:/RCA-flashticket/docs/MRP.md:357) đặt mốc G4 cuối tháng 11 và nộp quyển ngày 30/12. Sau P6 vẫn còn đánh giá test, lớp giải thích, tích hợp, thực nghiệm FlashTicket và báo cáo.

Chưa có lịch và năng lực thực hiện thì **chưa thể kết luận chắc chắn trễ**, nhưng cũng chưa đủ căn cứ duyệt rằng phạm vi này bảo vệ được khả năng hoàn thành toàn đồ án. Nguồn yêu cầu hiện hành còn nói rõ nghiên cứu RCA không được làm giảm nhẹ phần xây dựng FlashTicket. [Xác nhận phạm vi](D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md:30)

**Sửa tối thiểu:** đặt P6 vào lịch còn lại, dành rõ thời gian cho P7–P10 và viết báo cáo. P9a tiếp tục từ bộ yêu cầu đã bàn giao; không chờ T-073 mới bắt đầu chuẩn bị quan sát.

**Tôi đề nghị ưu tiên như sau**

- **Giữ phần cốt lõi:** đồ thị thật sự tham gia tính điểm; có phát hiện, vùng nghi ngờ và xếp hạng; log/trace/metric được dùng đúng phạm vi; kiểm rò thông tin; baseline mạnh; đối chứng cấu trúc; ca sai và ca đúng; đánh giá ngoài thiết kế; tích hợp cùng lõi vào FlashTicket.
- **Làm sớm phần dễ khiến phương án thất bại:** khả năng phân xử của dữ liệu, phép tính dùng cạnh, nhóm lỗi khó liên quan và hành vi trọn chuỗi trên dev.
- **Chỉ mở rộng khi có lý do cụ thể:** thêm họ thuật toán, sửa sâu baseline, mở thêm biến thể hoặc xử lý câu hỏi lịch sử không ảnh hưởng kết luận đang cần.
- **Chia task theo đầu ra kiểm được và sức chứa một phiên.** Không ép xuống một con số đẹp. Gộp hai task có tổng khối lượng quá lớn chỉ chuyển vấn đề sang lúc triển khai.

**“Không bỏ khó làm dễ” ở đây nghĩa là giữ các câu hỏi quyết định giá trị đồ án và đối diện chúng sớm.** Nó không có nghĩa mọi câu hỏi còn mở đều phải được giải quyết trong P6. Câu hỏi quan trọng nhưng chưa giải quyết phải có bằng chứng thiếu, nơi tiếp nhận và kết luận bị giới hạn.

Mức thành công Minh chọn cũng không đồng nghĩa chỉ cần chương trình chạy. Cần giải thích được vì sao phương pháp hợp lý, nó giúp hoặc không giúp trong điều kiện nào, và sản phẩm dùng đúng phương pháp đã đánh giá. Kết quả không thắng tổng thể vẫn có thể đáp ứng tiêu chí nghiên cứu đã duyệt; “không thắng” không miễn nghĩa vụ tìm nguyên nhân và kiểm thiết kế. [MRP về tiêu chí hoàn thành](D:/RCA-flashticket/docs/MRP.md:84)

**Đề nghị hiện tại:** người lập kế hoạch chỉnh thứ tự, phạm vi mặc định và ngân sách toàn đồ án trước khi trình duyệt lại. Chưa có căn cứ để tôi thay “34 task” bằng một số task khác, hoặc hứa giảm được một tỷ lệ thời gian cụ thể.

Báo cáo lượt này:

1. **Đã làm:** phản biện phạm vi, thứ tự và khả năng đáp ứng ưu tiên Minh chọn.
2. **File thay đổi:** không sửa file nào.
3. **Kiểm tra:** đếm task; cộng lại giờ công và ma trận; đối chiếu MRP, DT18, hướng dẫn, quyết định và bàn giao P5; hash hai tài liệu bàn giao P6/P9 khớp manifest. Không chạy thực nghiệm.
4. **Còn mở:** hiệu quả ứng viên và chi phí thực tế chưa được đo. Các phản đối trên cần người lập đáp trước khi duyệt nguyên kế hoạch; chưa cần mở thêm nghiên cứu chỉ để trả lời lượt phản biện này.

Đề xuất nối vào [DECISIONS.md](D:/RCA-flashticket/docs/DECISIONS.md) nguyên lời Minh: “Đồ án hoàn chỉnh, bảo vệ được: phương pháp có căn cứ, đánh giá hợp lệ, tích hợp chạy thật; cố gắng tạo cải thiện có ý nghĩa ở nhóm điều kiện xác định.” Dòng này lưu ưu tiên cho việc sửa kế hoạch; chưa ghi vì Luật 0 yêu cầu Minh duyệt đúng nội dung thay đổi.

Prompt dưới đây để Minh chuyển lại người lập kế hoạch, kèm bản phản biện này:

Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch toàn chặng P6 tại C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt, cùng nguyên văn yêu cầu và câu trả lời bổ sung của Minh được gửi kèm.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: đề xuất kế hoạch P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex phiên lập kế hoạch là người lập; Codex phiên đánh giá kế hoạch là người phản biện theo yêu cầu Minh. Phân công áp dụng cho lượt kế hoạch.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/docs/STATE.md; D:/RCA-flashticket/docs/MRP.md; D:/RCA-flashticket/docs/WHY.md; D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/LESSONS.md; D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md; D:/RCA-flashticket/docs/review-prompt.md; kế hoạch và yêu cầu Minh nêu trên.
- Phản biện và phản hồi trước: bản phản biện kế hoạch trong chat do Minh gửi kèm; chưa có phản hồi của người lập cho bản này.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; D:/RCA-flashticket/src/do_thi/; D:/RCA-flashticket/src/do_thi_tinh/; D:/RCA-flashticket/results/T-034/; D:/RCA-flashticket/results/T-040/ban-giao-p6.md; D:/RCA-flashticket/results/T-040/yeu-cau-quan-sat-p9.md; manifest và nguồn được các tài liệu này dẫn.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; chưa có quyền sửa kế hoạch hoặc file.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
````

</details>

<a id="s04"></a>

### S04 — Codex đáp phản biện bản đầu

<details>
<summary>Mở nguyên văn S04</summary>

````text
**Tôi nhận cả ba điểm phản biện là đúng và chặn việc duyệt nguyên trạng kế hoạch.** Vấn đề chính là tôi đã phân rã theo thành phần kỹ thuật trước khi tổ chức công việc quanh những câu hỏi có thể làm phương án nghiên cứu thất bại.

Tôi cũng sửa lại câu trả lời trước: **P1–P5 có 38 task lịch sử; P6 đề xuất 34 task chính, tối đa 49.** Không thể chỉ nhìn số task để kết luận P6 quá lớn. Điều phải chứng minh là từng phần việc cần thiết, được làm đúng lúc và còn đủ nguồn lực hoàn thành phần sau.

**Phản hồi từng điểm**

| Điểm | Kết luận của người lập | Bằng chứng và phạm vi tiếp nhận |
|---|---|---|
| **1. Kiểm khả năng phân xử của phương pháp quá muộn** | **Đúng — CHẶN thứ tự triển khai hiện tại.** | T-067 đợi T-041–060 và T-065–066; T-072 mới kiểm xuyên suốt. Fixture, smoke test và đo tài nguyên đã có, nhưng chưa thay cho thử sớm cơ chế trên dữ liệu thật. Tôi nhận sửa thứ tự này. |
| **2. Công việc có điều kiện bị đưa vào đường chính** | **Đúng — CHẶN phạm vi mặc định.** | Chỉ mục cha–con có thể cần ngay, nhưng toàn bộ cây request và phép tính thời gian không bị con phủ chỉ cần khi công thức dùng chúng. Tương tự, sửa sâu BOCPD và khóa nhãn “lan” phải có phụ thuộc cụ thể. [MRP đặt điều kiện cho nhãn lan](/D:/RCA-flashticket/docs/MRP.md:192). |
| **3. Ngân sách chưa bảo vệ khả năng hoàn thành toàn đồ án** | **Đúng — CHẶN kết luận khả thi.** | Tổng 109–144 giờ người làm cộng đúng, nhưng các ước lượng thành phần chưa đủ chắc và chưa đặt vào lịch P7–P10, báo cáo, công việc của Minh. [MRP yêu cầu P9 làm song song](/D:/RCA-flashticket/docs/MRP.md:282), G4 cuối tháng 11 và nộp quyển 30/12. |

Với điểm 3, cần giữ một giới hạn: kế hoạch cũ **không cấm** P9a bắt đầu sớm, nhưng lịch chưa thể hiện việc đó. Đặt bàn giao ở T-073 cuối chặng là chưa đủ. Bộ yêu cầu P9a đã tồn tại và đã được chuyển theo quyết định hiện hành; không phải đợi thiết kế P6 hoàn tất mới chuẩn bị quan sát.

**Thông tin 16 giờ/tuần làm thay đổi cách lập ngân sách**

Minh vừa xác nhận đây là thời gian dành cho RCA, gồm triển khai, xem kết quả và duyệt công việc.

Nếu tính từ 18/10, lấy 30/11 làm mốc cuối tháng:

- Tới G4: khoảng **98 giờ của Minh**.
- Tới 30/12: khoảng **167 giờ của Minh**, cho toàn bộ phần RCA còn lại, tích hợp liên quan và báo cáo.

Đây là quỹ thời gian của Minh, **không đồng nhất với giờ agent hoặc giờ máy**. Vì vậy, tôi chưa thể lấy 172–255 giờ trong bản cũ so trực tiếp với 98 giờ rồi kết luận chắc chắn trễ. Nhưng bản sửa phải tách được bốn khoản: Minh trực tiếp làm/duyệt, agent làm, máy chạy và thời gian chờ.

**Phạm vi sửa tôi đề xuất**

Đây là đề xuất sửa bản kế hoạch trong chat, chưa phải bản kế hoạch mới đã áp dụng.

| Phần | Cũ → nội dung cần sửa | Ảnh hưởng |
|---|---|---|
| Thứ tự nghiên cứu | Hoàn thiện nhiều module rồi mới thử rộng → đưa một lượt thử trọn chuỗi lên sớm, dùng phần đầu vào và phép tính thật sự cần | Phát hiện sớm ứng viên thiếu thông tin hoặc sai giả định |
| Phạm vi lượt thử sớm | Đo chủ yếu tài nguyên → kiểm cả khả năng phân xử, trung gian, đầu ra và chi phí | Có ca hỗ trợ, phản bác và nhóm khó; so với nhánh không quan hệ và baseline phù hợp |
| Đường chính | Xếp sẵn nhiều thành phần vào mặc định → mỗi việc phải chỉ rõ lựa chọn/kết luận nào cần nó | Giữ kiểm bắt buộc; chuyển đúng phần phụ thuộc thiết kế sang nhánh có điều kiện |
| Ma trận thực nghiệm | Dùng tích tám cấu hình × mọi đối chứng × 20 seed làm trần mặc định → xây ma trận theo câu hỏi và thiết kế thực sự được thử | Giữ đối chứng cấu trúc, độ nhạy và ngân sách so sánh hợp lệ; chưa chốt số tổ hợp mới |
| Cách chia task | Một module thường thành một task → task gắn với đầu ra nghiên cứu kiểm được; module và fixture là bước con khi vừa phiên | Giảm bàn giao không cần thiết, không gộp quá sức |
| Lịch toàn đồ án | Cộng giờ riêng P6 → lập lịch P6–P10 và báo cáo theo 16 giờ/tuần của Minh; P9a có nhánh sớm | Bảo vệ thời gian đánh giá ngoài thiết kế và tích hợp thật |

Lượt thử sớm phải phân biệt được bốn kết quả: ứng viên có căn cứ để tiếp tục; giả định bị bác bỏ; dữ liệu chưa phân xử được; hoặc bản cài/giao thức có lỗi. **Không đặt điều kiện “đồ thị phải thắng”**, không thay đánh giá đầy đủ trước G3 và không lấy vài ca thuận lợi làm căn cứ chọn phương pháp.

Tôi chưa đề xuất số task mới hoặc tỷ lệ tiết kiệm. Làm vậy lúc này sẽ lặp lại lỗi chốt con số trước khi phân rã theo phụ thuộc.

**Trạng thái sau lượt đáp**

Tôi không còn bất đồng với ba finding. Tuy nhiên, chúng **chưa được xử lý trong kế hoạch**. Tôi đề nghị chuyển sang sửa sau khi Minh duyệt phạm vi trên; chưa đề nghị duyệt triển khai hoặc đóng phản biện toàn kế hoạch.

Đề xuất riêng cho [DECISIONS.md](/D:/RCA-flashticket/docs/DECISIONS.md), chưa ghi:

> Minh xác nhận thời gian dành cho phần RCA, gồm triển khai, xem kết quả và duyệt công việc: “16 giờ mỗi tuần”.

Báo cáo bốn mục:

1. **Đã làm:** kiểm từng finding, sửa nhận định trước về số task và xác định phạm vi chỉnh kế hoạch.
2. **File thay đổi:** không sửa file nào; trạng thái Git giữ nguyên.
3. **Kiểm đã chạy:** đếm được 38 task P1–P5; cộng lại 34 dòng chi phí thành 109–144 giờ; kiểm phép nhân 15.088; đối chiếu MRP, DT18, hướng dẫn, WHY/LESSONS và quyết định; hash hai tài liệu bàn giao P6/P9 khớp manifest. Không chạy thực nghiệm. Lượt này tôi đã đọc phản biện trước khi tái đối chiếu nguồn, nên không gọi là tự soát mù trước phản biện.
4. **Còn mở:** thiết kế và chi phí thực tế; lịch mới theo 16 giờ/tuần; quyền sửa kế hoạch và ghi dòng quyết định trên.

Prompt để Minh chuyển lại người phản biện, nếu muốn kiểm lượt đáp trước khi cho sửa:

:::writing{variant="standard" id="72846"}
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch toàn chặng P6 tại C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt, cùng phản hồi và đề xuất sửa của người lập được Minh gửi kèm nguyên văn trong chat. Chưa có bản kế hoạch sửa được áp dụng.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: đề xuất kế hoạch P6, chuẩn bị G3.
- Người làm và người phản biện chính thức: Codex phiên lập kế hoạch là người lập; Codex phiên phản biện kế hoạch là người phản biện theo yêu cầu Minh. Phân công chỉ áp dụng lượt kế hoạch.
- Tài liệu gốc: D:/RCA-flashticket/AGENTS.md; D:/RCA-flashticket/docs/STATE.md; D:/RCA-flashticket/docs/MRP.md; D:/RCA-flashticket/docs/WHY.md; D:/RCA-flashticket/docs/DECISIONS.md; D:/RCA-flashticket/docs/LESSONS.md; D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; D:/RCA-flashticket/docs/reference/sources/advisor-2026-09-23.md; D:/RCA-flashticket/docs/review-prompt.md; yêu cầu lập kế hoạch tại C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; kế hoạch, phản hồi và câu trả lời bổ sung của Minh trong chat.
- Phản biện và phản hồi trước: bản phản biện tại C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt; tiếp theo là phản hồi người lập do Minh gửi kèm nguyên văn. Minh trả lời câu hỏi về thời gian dành cho RCA, gồm triển khai, xem kết quả và duyệt công việc: “16 giờ mỗi tuần”.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; D:/RCA-flashticket/src/do_thi/; D:/RCA-flashticket/src/do_thi_tinh/; D:/RCA-flashticket/results/T-034/; D:/RCA-flashticket/results/T-040/ban-giao-p6.md; D:/RCA-flashticket/results/T-040/yeu-cau-quan-sat-p9.md; manifest và nguồn trực tiếp được các tài liệu này dẫn.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat; không sửa kế hoạch hoặc file, không chạy thực nghiệm mới, không mở dữ liệu khóa, không tải dữ liệu, không mở phiên, không dùng subagent và không tự gửi prompt.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
:::

**Minh có duyệt chỉnh kế hoạch trong chat theo sáu thay đổi trên và ghi đúng dòng xác nhận “16 giờ mỗi tuần” vào DECISIONS không?**

Tôi cần lời duyệt vì prompt Minh chuyển ghi “chưa có quyền sửa kế hoạch hoặc file”; [AGENTS.md, Luật 0](/D:/RCA-flashticket/AGENTS.md:26) cũng quy định: “Duyệt chỉ có hiệu lực trong đúng phạm vi đã đề xuất.”
````

</details>

<a id="s05"></a>

### S05 — Nguyên văn đính chính của Minh về task, thời gian, phiên và ngữ cảnh

<details>
<summary>Mở nguyên văn S05</summary>

````text
không ghi vào desision, không quan tâm đến số giờ của tôi vội, tôi cần bạn lập plan chia task trước.&#x20;

Tôi cần đính chính cách hiểu về “task vừa một phiên”, thời gian thực hiện và ngữ cảnh của agent trước khi tiếp tục chia kế hoạch P6.

Sau khi làm đến T-040, tôi nhận thấy cách agent ước lượng và chia task chưa sát thực tế. Tôi yêu cầu rà lại kế hoạch theo các điểm sau. Đây là yêu cầu phân tích và đề xuất trong chat, chưa cho phép sửa file.

**1. Phải phân biệt thời gian máy chạy với công việc của agent.**

Một task mất 4–5 giờ có thể chủ yếu là thời gian chạy script Python. Trong các task đã thực hiện, tôi quan sát thấy thời gian chạy script chiếm phần lớn. Khoảng thời gian này chủ yếu phụ thuộc CPU, RAM, dữ liệu và cách cài đặt; không thể quy đổi trực tiếp thành lượng ngữ cảnh agent sử dụng.

Agent vẫn cần đọc kết quả, kiểm tra trung gian, xử lý lỗi và diễn giải. Đó là phần việc cần đánh giá riêng. Một script chạy nhiều giờ nhưng chỉ cần kiểm tra vài đầu ra khác với nhiều giờ agent liên tục đọc tài liệu, sửa code và xử lý kết quả.

Vì vậy, tôi không chấp nhận lấy con số ước lượng kiểu “task này mất 4–5 giờ” làm căn cứ để kết luận vừa hoặc không vừa một phiên, rồi tách task. Nếu viện dẫn thời gian, phải nói rõ đó là thời gian máy chạy, thời gian agent xử lý hay thời gian chờ phản biện; có bằng chứng đo nào và phần nào chưa biết. Không gán những khoảng giờ có vẻ chính xác khi chưa có căn cứ.

**2. “Vừa một phiên” không phải một giới hạn giờ cứng.**

Không được trình bày đây là quy định của OpenAI. Cũng không được khẳng định đã ước lượng được lượng context của một task chỉ từ số file, số đầu việc hoặc số giờ chạy script.

Nếu chưa đo hoặc chưa có dữ liệu từ các task tương tự, hãy ghi chưa biết. Cần đánh giá khả năng giữ mạch công việc qua phạm vi tài liệu, số quyết định liên quan, lượng đầu ra cần đọc và độ phức tạp khi kiểm chứng.

Một task có thể có lượt chạy dài và nhiều lượt phản biện. Không đồng nhất task, một phiên trò chuyện và toàn bộ vòng đời làm–phản biện–sửa–nghiệm thu.

**3. Ngữ cảnh bị nén không tự động bắt buộc dừng phiên.**

Tôi đính chính cách áp dụng yêu cầu này: sau khi nén ngữ cảnh, agent cần kiểm tra khả năng tiếp tục đúng công việc, đối chiếu nguồn và khôi phục những thông tin cần thiết. Có thể tiếp tục nếu vẫn xác định được mục tiêu, quyền hạn, trạng thái, bằng chứng và bước tiếp theo.

Chỉ đề nghị chuyển phiên khi có lý do cụ thể như mất mạch, lặp việc, không phục hồi được thông tin cần thiết hoặc nguy cơ sai tăng rõ rệt. Không coi sự kiện nén ngữ cảnh tự nó là bằng chứng phải dừng hay phải chia nhỏ task.

Đính chính này không cho phép bỏ qua checkpoint, nguồn sự thật trong repo hoặc quyền ghi file.

**4. Chia task theo phần việc có đầu ra và phép kiểm rõ ràng; tránh chia nhỏ quá mức.**

Có thể chia theo module. Những phần liên hệ chặt, dùng chung đầu vào, trung gian, lượt xử lý hoặc tài nguyên có thể được gộp nếu giúp thực hiện và kiểm chứng hiệu quả hơn.

Không mặc định mỗi bước nhỏ, mỗi loại file hay mỗi thao tác kiểm tra phải thành một task riêng. Cũng không gộp chỉ vì cùng dùng CPU/RAM: phải chỉ ra lợi ích cụ thể và việc gộp có làm khó kiểm chứng, sửa lỗi hoặc nghiệm thu hay không.

Ưu tiên cao nhất vẫn là tính đúng đắn. Không cắt nhóm khó, giảm phép phân xử cần thiết hoặc thu hẹp câu hỏi nghiên cứu để làm cho task “vừa phiên”.

**5. Rà lại P6 trên cơ sở công việc đã có.**

P1–P5 đã tạo code, hạ tầng, giao thức và kết quả. P3 đã đánh giá các baseline trong phạm vi được duyệt. Phải xác định phần nào dùng lại được và phần nào P6 thực sự thay đổi trước khi đề xuất kiểm lại.

Không đặt một task “kiểm hạ tầng” hoặc “kiểm baseline” chung chung. Mỗi phần kiểm bổ sung phải nêu thay đổi hoặc khoảng trống cụ thể, quyết định phụ thuộc và bằng chứng cần bổ sung.

Đồng thời, phải làm rõ phần việc đề xuất phương pháp: câu hỏi nào chưa được giải quyết, bằng chứng hiện có hỗ trợ ứng viên nào, và phép thử nào giúp chọn hoặc bác bỏ hướng đó. Việc bổ sung baseline phải có mục đích so sánh rõ.

**Kết quả tôi cần:**

- Rà lại 34 task chính và 15 task có điều kiện: phần nào giữ, gộp, dùng lại kết quả hoặc chỉ làm khi có điều kiện cụ thể.
- Phân biệt công việc thiết kế phương pháp, cài đặt, thực nghiệm, kiểm chứng và bàn giao.
- Tính đến công việc phản biện qua lại, nhưng không dùng tỷ lệ dự phòng tùy ý để tạo cảm giác đã ước lượng đầy đủ.
- Giải thích số task sau khi rà từ khối lượng và quan hệ công việc thực tế. Không đặt trước một con số rồi tìm cách chia cho khớp.

Mục tiêu của tôi là đồ án hoàn chỉnh, bảo vệ được: phương pháp có căn cứ, đánh giá hợp lệ, tích hợp chạy thật và cố gắng tạo cải thiện có ý nghĩa trong những điều kiện xác định. Hãy tối ưu cách tổ chức công việc để đạt mục tiêu này, đồng thời giữ đầy đủ những phần khoa học khó cần giải quyết.

````

</details>

<a id="s06"></a>

### S06 — Kế hoạch trung gian 12 + 11, lịch sử

<details>
<summary>Mở nguyên văn S06</summary>

````text
**Tôi đề xuất tổ chức lại thành 12 task chính và 11 task có điều kiện. Đây là số phần việc có đầu ra riêng, không phải cam kết hoàn thành trong 12 hoặc 23 phiên.** Không phải làm tất cả các nhánh có điều kiện.

Bản cũ chia quá nhiều theo từng thành phần kỹ thuật, chưa thể hiện đúng phần đã có từ P3–P5, và đưa phép thử phương pháp hoàn chỉnh xuống quá muộn. Tôi rút lại các khoảng giờ công và cách kết luận “vừa phiên” dựa vào những khoảng giờ đó.

Dưới đây là kế hoạch sửa trong chat. **Không ghi DECISIONS, không dùng mức 16 giờ/tuần để lập lịch, không sửa file.**

**1. Cách chia task áp dụng cho bản này**

Một task có một đầu ra đủ rõ để kiểm và bàn giao. Nó có thể gồm thiết kế chi tiết, cài đặt, chạy script, đọc trung gian, phân tích, tự kiểm và tài liệu nếu những việc đó cùng phục vụ đầu ra ấy.

Tách task khi có một trong các ranh giới thực sự:

- Đầu ra trước cần được đánh giá để quyết định có làm phần sau hay không.
- Hai phần trả lời các câu hỏi khác nhau, cần bằng chứng và tiêu chí nghiệm thu khác nhau.
- Hai module có thể được kiểm độc lập và bàn giao qua giao diện ổn định.
- Việc gộp làm khó xác định lỗi nằm ở dữ liệu, công thức hay cách đánh giá.

Không tách chỉ vì script chạy lâu, có nhiều file hoặc có nhiều lượt phản biện. Các đợt chạy, lần sửa và lượt phản biện vẫn thuộc task tương ứng.

Sau nén ngữ cảnh, agent khôi phục mục tiêu, quyền hạn, trạng thái, nguồn bằng chứng và bước tiếp theo. Tiếp tục được thì tiếp tục. **Hiện chưa có số đo đủ để khẳng định task nào chắc chắn vừa một cửa sổ ngữ cảnh.** Tôi chỉ đánh giá được mức độ liền mạch của công việc và những chỗ dễ mất mạch.

**2. P6 thực sự kế thừa gì**

Tôi đối chiếu với mã hiện có, không coi P6 là bắt đầu lại từ đầu.

| Phần đã có | Cách dùng lại | Phần P6 thực sự phải bổ sung |
|---|---|---|
| Adapter, lựa chọn ca và cắt cửa sổ P3 | Dùng lại miền dev, quy tắc thời gian và bộ đọc Nezha | Đường xử lý theo thời điểm dữ liệu đã khả dụng; dữ liệu cho đặc trưng mới |
| Bộ dựng đồ thị P5 | Dùng lại định danh, quan hệ, phép chiếu thực thể/thao tác và hợp đồng nguồn tĩnh | Tín hiệu theo thời gian trên nút/cạnh; kiểm graph được phép xuất hiện ở thời điểm dự đoán |
| Trung gian P4 | Đọc lại bảng lời gọi, điểm và phép đổi đã có | Chỉ thu thêm trung gian mà công thức hoặc kết luận mới thực sự cần |
| Bộ chạy P3 | Dùng lại cách cách ly tiến trình, timeout và đo tài nguyên | Bộ gọi phương pháp P6, cấu hình/cache và bản ghi mới |
| Bộ chấm P3 | Dùng lại xếp hạng, hòa điểm, tổng hợp theo nhóm, bootstrap, chấm phát hiện | Chuyển đầu ra P6 về bản ghi chuẩn; chấm vùng nghi ngờ và thời điểm kết quả sẵn sàng |
| Baseline P3 | Dùng lại kết quả khi đầu vào, cửa sổ, mã, cấu hình và cách chấm khớp | Chạy mới khi đổi đầu vào, điển hình là xếp hạng tại báo động mới của P6 |
| N-Sigma | Dùng lại bản hiện có với tiền xử lý dùng quá khứ | Chỉ kiểm phần nối vào giao thức P6 nếu phần nối thay đổi |
| BOCPD | Giữ kết quả lịch sử cùng giới hạn đã khai | Biến thể nhân quả và phần underflow còn lại là hai nhánh nghiên cứu khác nhau |
| Bàn giao P9 | Dùng ngay bộ yêu cầu quan sát đã có | Bổ sung yêu cầu phát sinh từ phương pháp; kiểm thực tế ở P9/P10 |

Các điểm cụ thể từ mã:

- [cua_so.py](D:/RCA-flashticket/src/p3/cua_so.py) và [nezha.py](D:/RCA-flashticket/src/p3/nezha.py) đã giải quyết một phần đáng kể công việc mà bản cũ gọi thành hai task adapter mới.
- [danh_gia.py](D:/RCA-flashticket/src/p3/danh_gia.py) đã có phần lớn bộ chấm. Không cần viết lại một evaluator hoàn chỉnh.
- [phat_hien.py](D:/RCA-flashticket/src/p3/adapters/phat_hien.py:68) đã có N-Sigma dùng điền giá trị từ quá khứ. Không có căn cứ đặt một task mặc định để “sửa nhân quả cho N-Sigma”.
- [builder.py](D:/RCA-flashticket/src/do_thi/builder.py) cung cấp cấu trúc graph. Tuy nhiên, graph tổng hợp không thay thế toàn bộ lời gọi và khoảng thời gian span mà một đặc trưng mới có thể cần.

Vì vậy, tôi **bỏ hai task độc lập kiểu “kiểm hạ tầng” và “kiểm baseline”**. Các kiểm bổ sung được gắn vào đúng thay đổi bên dưới.

**3. Phần khoa học cần giải quyết trước**

Nguồn chính là [MRP](D:/RCA-flashticket/docs/MRP.md:218), [gói G2](D:/RCA-flashticket/results/T-034/goi-g2.md) và [bàn giao P6](D:/RCA-flashticket/results/T-040/ban-giao-p6.md).

Hướng ưu tiên thử vẫn là **ứng viên**: giữ chứng cứ tại nơi đo, đồng thời dùng quan hệ lời gọi để kiểm cách quy chứng cứ thời lượng cho thành phần được gọi. Chưa gọi kết quả đó là điểm “nguyên nhân tự sinh”.

Căn cứ đủ để thử là P4 đã xác lập một số chuỗi trong đó thời lượng ở phía gọi bị tính thành bất thường của phía gọi. Nhưng có bằng chứng hạn chế hướng này: hiện tượng chờ cũng xuất hiện ở ca đúng; nhiều ca sai của các phương pháp khác không thuộc quan hệ phía gọi–root; lỗi return và root thiếu cạnh có thể không được lợi.

Do đó, kế hoạch phải phân xử ít nhất những câu sau:

| Câu hỏi | Phép phân xử cần có | Nơi xử lý |
|---|---|---|
| Quan hệ giúp quy chứng cứ đúng hơn hay chỉ chuyển điểm sang một nút khác? | Cùng dữ liệu gốc, so cách dùng quan hệ với nhánh không dùng quan hệ; đọc chuỗi trung gian ở cả ca đúng và sai | M1, M4, M6, M11 |
| Mức thực thể hay thao tác giữ được thông tin hữu ích hơn? | So trên cùng phạm vi ca, giữ rõ khác biệt scope và tín hiệu dùng chung | M2–M4, M8–M10 |
| Gộp tín hiệu có làm một cạnh lớn hoặc nhiều tín hiệu trùng lặp lấn át? | Đối chiếu các cách gộp đã định nghĩa; fixture lặp tín hiệu, nhiều cạnh, cạnh thưa | M1, M3, M4 |
| Lỗi nhanh/return hoặc lỗi tài nguyên không tăng duration được xử lý thế nào? | Đọc theo thao tác, giữ cả dấu giảm và thông tin log/metric hợp lệ; so với ca đối chiếu | M2–M4, M9, M10 |
| Phát hiện có hoạt động khi chỉ dùng dữ liệu đã đến? | Phát lại theo tiền tố; kiểm nền, ngưỡng, thời điểm span hoàn tất và thời điểm có kết quả RCA | M2, M3, M5, M7 |
| Đồ thị thật có đóng góp vượt quá tín hiệu đầu vào? | Nhánh không quan hệ, graph ngẫu nhiên giữ bậc; phân tích theo ca/ô và điều kiện | M6, M11; kết luận kiểm ngoài dev ở P7 |
| Graph tĩnh và graph quan sát khác nhau do cấu trúc hay do coverage/mapping? | Tách phần tương đương và phần thay đồng thời | M6, M11 |
| Những gì dữ liệu công khai không phân xử được? | Giữ OPEN; xác định quan sát/nhãn cần thu trên FlashTicket | M1, M12 → P9/P10 |

**Không mặc định phải làm cây request đầy đủ, tính self-time, sửa BOCPD, dùng PageRank, hồi quy hay GNN.** Mỗi thành phần chỉ được đưa vào khi có câu hỏi, căn cứ và phép phân xử tương ứng.

**4. Danh sách 12 task chính**

Tôi dùng mã kế hoạch **M1–M12** để tránh nhầm với mã T-041…T-089 của bản cũ. Repo hiện dùng tới T-040. Mã T chính thức sẽ được cấp theo thứ tự tạo task sau khi được duyệt.

Các đường dẫn mới dưới đây là **phạm vi ghi dự kiến**, chưa phải quyền ghi. Mỗi task còn có SPEC, LOG, kết quả, manifest và prompt bàn giao của chính task. Mặc định đề xuất Codex làm, Claude phản biện; phân công cuối thuộc từng SPEC. Ngoại lệ Codex phản biện kế hoạch này không tự áp sang các task kết quả.

**M1 — Thiết kế ứng viên, phép phân xử và phạm vi so sánh**

- **Loại:** thiết kế phương pháp và giao thức.
- **Đầu vào:** yêu cầu DT18/cô, MRP, G2, bàn giao P5, mã P3/P5 và các câu OPEN trực tiếp liên quan.
- **Việc làm:** định nghĩa nút/cạnh, chứng cứ trên từng phần tử, công thức ứng viên, cách gộp, nền/ngưỡng, tập ứng viên và xử lý thiếu dữ liệu. Lập bảng mỗi lựa chọn nhằm sửa hạn chế P4, đáp ứng DT18 hay phục vụ kỹ thuật.
- **Phần so sánh:** xác định kết quả P3 nào dùng nguyên trạng; đầu vào nào đổi; baseline nào phải chạy mới và để trả lời câu hỏi gì. Giữ baseline mạnh, không chỉ BARO.
- **Đầu ra:** đặc tả để thử, ma trận cấu hình, nhóm ca cần đọc sâu, bảng phạm vi khẳng định, hợp đồng đầu vào/đầu ra ban đầu. Chuyển ngay yêu cầu phương pháp tới giao diện P9a đang có.
- **Kiểm:** công thức có thực sự dùng cạnh; có phản ví dụ và khả năng bác bỏ; có dùng nhãn hoặc tương lai không; mọi OPEN có nơi xử lý.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/results/T-xxx/` của task. Các mục WHY cần thiết được trình riêng theo quyền ghi; lượt này không đề xuất ghi DECISIONS.
- **Ranh giới:** chưa cài, chưa chọn thuật toán cuối. Task hoàn thành khi đủ rõ để cài và kiểm một ứng viên, không phải khi hứa được lợi ích.

Đây là một task vì các quyết định phải khớp nhau trước khi cài. Tách schema, baseline và công thức thành ba task tài liệu độc lập sẽ tạo nhiều lượt đồng bộ mà chưa thêm bằng chứng.

**M2 — Chứng cứ trace và graph theo thời gian**

- **Loại:** cài đặt và kiểm dữ liệu.
- **Phụ thuộc:** hợp đồng và đại lượng trace được phép thử ở M1.
- **Dùng lại:** adapter P3, `from_p3`, định danh và bộ dựng graph P5; bảng lời gọi P4 nếu đúng đại lượng cần dùng.
- **Việc mới:** trích các lời gọi/đặc trưng trace cần cho công thức; giữ chủ thể đo, đích quan hệ, scope, nguồn và thời điểm khả dụng. Chỉ tạo chỉ mục cha–con cần thiết, chưa xây toàn bộ cây request nếu không dùng đến.
- **Miền xử lý:** 30 ca TT và 22 ca OB dev; chuẩn bị cả mức thực thể và thao tác. Lượt đọc trace được dùng chung cho các cấu hình.
- **Kiểm độc lập:** đối chiếu thủ công các lời gọi chọn từ dữ liệu được phép; span mồ côi, trùng định danh, nằm sát biên, kết thúc sau cutoff, song song và thiếu phía ghép. So graph sinh ra với P5 trong phạm vi đầu vào tương đương.
- **Đầu ra:** bảng chứng cứ trace có nguồn truy lại được, thống kê trường hợp không đo được, cache có phiên bản.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/src/p6/trace.py`, phần hợp đồng liên quan và kết quả của task.
- **Nhánh:** nếu công thức cần khoảng thời gian không bị span con phủ, kích hoạt C1. Không tự coi trường chưa tính là bằng không.

Gộp TT/OB ở đây vì phần mới dùng cùng hợp đồng chứng cứ; bộ đọc từng dataset đã có. Không gộp chỉ vì cả hai cùng đọc trace.

**M3 — Tín hiệu metric/log, nền và chuẩn hóa chung**

- **Loại:** cài đặt và kiểm phép đo.
- **Phụ thuộc:** M1; tiếp nhận schema chứng cứ thống nhất với M2.
- **Dùng lại:** bộ đọc P3, ánh xạ/scope P5, quy tắc tên thực thể đã có.
- **Việc mới:** tạo tín hiệu metric/log, nối log vào phạm vi thực sự biết được, chống đếm lặp tín hiệu dùng chung; định nghĩa nền, thiếu nền, giá trị không hữu hạn và dấu thay đổi.
- **Phần return:** đọc đáp ứng theo thao tác từ chứng cứ M2; xác định duration, log hoặc metric nào thực sự có thông tin. Việc này nằm trong phát triển tín hiệu và phân tích OB, không thành một task khảo sát tách rời mặc định.
- **Kiểm:** cùng một tín hiệu dùng chung không biến thành nhiều phiếu độc lập; số dòng log không được gọi là số request; thêm dữ liệu tương lai không đổi đặc trưng đã phát ra; nền ngắn/không đủ phải tạo đúng trạng thái.
- **Đầu ra:** khối đặc trưng thống nhất cho ba nguồn, kèm scope, thời gian và trạng thái chất lượng.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/src/p6/signals.py`, `D:/RCA-flashticket/src/p6/normalization.py` và kết quả của task.
- **Ranh giới:** chưa kết luận tín hiệu nào cải thiện RCA. Không gọi đoạn trước mốc tiêm là nền khỏe đã được xác nhận độc lập.

Lý do gộp là lỗi scope, chuẩn hóa và nhân bản tín hiệu phải được kiểm cùng nhau.

**M4 — Điểm dùng quan hệ, xếp hạng và thử nghiệm sớm chế độ (a)**

- **Loại:** cài phương pháp và thực nghiệm phân xử ban đầu.
- **Phụ thuộc:** M1–M3.
- **Việc mới:** cài công thức đã được duyệt để thử; nối điểm thành xếp hạng; xử lý nút cô lập, thiếu tín hiệu, hòa điểm và tập ứng viên. Cài đồng thời nhánh không quan hệ cần cho phép thử ban đầu.
- **Thử sớm:** một cấu hình tham chiếu được khai trước, trên toàn bộ 52 ca dev chế độ (a), cho phương pháp và nhánh đối chứng: **104 đơn vị ca–nhánh**. Dùng lại baseline P3 nếu điều kiện so khớp.
- **Đọc sâu:** nhóm thuận lợi cho giả thuyết, nhóm phản bác, root thiếu cạnh, cạnh thưa, lỗi return và ca đúng có điều kiện tương ứng. Không chỉ đọc ca phương pháp mới thắng.
- **Kiểm:** oracle đồ thị nhỏ; đổi nhãn evaluator không đổi dự đoán; đổi quan hệ có làm đổi đúng trung gian dự kiến; kiểm số hữu hạn và truy nguyên điểm.
- **Đầu ra:** ứng viên chạy được, bằng chứng hỗ trợ/bác bỏ/chưa phân xử, các lỗi triển khai đã tách khỏi giới hạn phương pháp.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/src/p6/scoring.py`, `D:/RCA-flashticket/src/p6/ranking.py`, phần đối chứng tối thiểu và kết quả.
- **Nhánh:** ứng viên không hợp lệ thì sửa đúng lỗi hoặc trình hướng khác, như C2. Không chạy tiếp ma trận lớn chỉ vì đã cài xong.

Đây là lần kiểm giá trị của phương pháp đầu tiên, không phải đợi đến task thứ 27 như bản cũ.

**M5 — Phát hiện, vùng nghi ngờ và chuỗi xử lý chế độ (b)**

- **Loại:** cài đặt và thực nghiệm toàn chuỗi sớm.
- **Phụ thuộc:** M4; nền và thời gian khả dụng của M2–M3.
- **Việc mới:** điểm hệ thống, cập nhật nền/ngưỡng, báo động, mở lượt RCA, tạo vùng nghi ngờ và trả kết quả. Phân biệt thời điểm báo động với thời điểm đã đủ dữ liệu để xếp hạng.
- **Thử sớm:** 30 ca TT, phương pháp và nhánh không quan hệ: **60 đơn vị ca–nhánh**. N-Sigma hiện có là đối chiếu phát hiện trong phạm vi giao thức tương ứng.
- **So RCA:** khi chạy baseline tại báo động P6 mới, đó là đầu vào mới. Thử sớm với baseline mạnh phù hợp; SimpleRCA và TORAI_B là các đối chiếu phải xét, không chỉ chọn baseline dễ thắng. Giữ số seed đúng giao thức.
- **Kiểm:** phát lại tiền tố, dữ liệu đến muộn, khởi động thiếu nền, không có báo động, nhiều báo động, vùng rỗng, root ngoài vùng; không bỏ root khỏi tập xếp hạng chỉ vì chưa vượt ngưỡng.
- **Đầu ra:** chuỗi dữ liệu → điểm → báo động → vùng → hạng, cùng bằng chứng và chi phí đo thật.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/src/p6/online.py`, `D:/RCA-flashticket/src/p6/regions.py`, bộ gọi thử và kết quả.
- **Giới hạn:** chưa gọi vùng nghi ngờ là vùng ảnh hưởng thật; chưa suy báo động trước mốc tiêm thành báo giả vận hành.

Nếu cửa sổ RCA còn cần dữ liệu sau báo động, thời gian chờ đó phải hiện trong kết quả. Không trình như xếp hạng tức thời.

**M6 — Đối chứng cấu trúc và nguồn graph**

- **Loại:** cài đặt và kiểm đối chứng.
- **Phụ thuộc:** công thức và các đường thông tin của M4–M5.
- **Việc làm:** hoàn thiện đối chứng không quan hệ; graph ngẫu nhiên giữ bậc; graph tĩnh so với graph quan sát. Dùng lại mã hoán đổi cạnh P4 khi phù hợp, hợp đồng và ánh xạ graph tĩnh P5.
- **Kiểm trọng tâm:** quan hệ còn ẩn trong đặc trưng nào; giữ hay chuyển chứng cứ khi đổi cạnh; kiểu cạnh và hướng; số graph ngẫu nhiên thực sự khác nhau; coverage/mapping thay cùng với nguồn graph.
- **Đầu ra:** các đối chứng chạy được, bảng yếu tố giữ–đổi, giới hạn kết luận của từng phép so.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/src/p6/controls.py` và kết quả.
- **Tiêu chí xong:** không chỉ “chạy không lỗi”; phải chứng minh đã loại/đổi đúng thông tin muốn thử.
- **Nhánh:** OM-07 chỉ mở C11 nếu một phép so hoặc kết luận thực sự phụ thuộc nó.

Ba đối chứng được gộp vì cùng cần lần theo đường đi thông tin của một scorer. Đây không phải ba nghiên cứu triển khai lại phương pháp.

**M7 — Đưa P6 vào bộ chạy và bộ chấm hiện có**

- **Loại:** tích hợp kỹ thuật và kiểm giao thức.
- **Phụ thuộc:** đầu ra thật của M4–M6.
- **Dùng lại:** `chay_tien_trinh`, bản ghi và các hàm chấm P3.
- **Việc mới:** bộ gọi P6, cache theo mã/cấu hình/đầu vào/thời gian; ánh xạ bản ghi; trạng thái lỗi; cách ghi thời điểm khả dụng; chấm vùng nghi ngờ; cấu hình môi trường tái lập trên máy khác.
- **Kiểm bổ sung có lý do:** đầu ra mới có mẫu số mới hoặc trạng thái mới; cache tiền tố không được lấy dữ liệu tương lai; pipeline có thể chờ thêm dữ liệu sau báo động; đường dẫn môi trường cũ có phần phụ thuộc thiết bị.
- **Kiểm độc lập:** bản ghi giả với kết quả tính tay; chuyển bản ghi P3 qua lớp tương thích phải giữ điểm; lượt bị ngắt giữ đầu ra và phát lại không trộn cấu hình.
- **Đầu ra:** lệnh thực nghiệm đầy đủ và có thể phát lại, cùng bộ chấm đã kiểm các phần thay đổi.
- **Phạm vi dự kiến:** `D:/RCA-flashticket/src/p6/runner.py`, `D:/RCA-flashticket/src/p6/evaluation.py` và kết quả.
- **Ranh giới:** không mở một cuộc kiểm tra chung lại toàn bộ P3.

M4–M5 dùng đường gọi tối thiểu để thử khoa học sớm. M7 hoàn thiện đường chạy ma trận và tái lập; không để việc xây bộ chạy trì hoãn phép thử đầu tiên.

**M8 — Thực nghiệm thiết kế trên TT dev**

- **Loại:** thực nghiệm và phân tích theo ca/ô.
- **Phụ thuộc:** ứng viên hợp lệ từ M4–M5, đối chứng đã kiểm ở M6 và bộ chạy M7.
- **Miền:** 30 ca, cả chế độ (a) và (b).
- **Ma trận:** các cấu hình đã khai ở M1; nếu giữ hai mức graph và hai cách gộp thì có **4 × 30 × 2 = 240 đơn vị cho nhánh phương pháp**. Đây là dự toán của phương án bốn cấu hình, chưa phải cấu hình đã được duyệt.
- **Việc làm:** dùng chung đặc trưng, lưu điểm trước/sau phép gộp, đọc các ô quan trọng và các cặp thắng–hòa–thua; tách phát hiện, RCA tại mốc cho trước và thành công toàn chuỗi.
- **Kiểm:** tính đủ bản ghi, lỗi và mẫu số; đối chiếu kết quả với trung gian; kiểm lại đúng trường hợp có kết quả bất thường.
- **Đầu ra:** bằng chứng lựa chọn trên TT, điều kiện thất bại và câu chưa phân xử.
- **Phạm vi dự kiến:** kết quả và script phân tích của task; không tự đổi mã lõi trong khi chạy.
- **Ranh giới:** không chọn thiết kế theo mức chênh với nhánh không đồ thị; chưa kết luận tổng quát hóa.

**M9 — Thực nghiệm thiết kế trên OB dev**

- **Loại:** thực nghiệm và phân tích theo ca/ô.
- **Phụ thuộc:** như M8; có thể dùng cùng phiên bản mã đã khóa cho lượt chạy.
- **Miền:** 22 ca, chế độ (a); không tự thêm chế độ tự phát hiện cho OB.
- **Ma trận:** cùng bốn cấu hình đề xuất có **4 × 22 = 88 đơn vị cho nhánh phương pháp**, trừ những cấu hình trùng dữ liệu hoặc không có nghĩa; phải ghi lý do, không lặng lẽ loại.
- **Việc làm:** tập trung lỗi mã nguồn/return, nền ngắn, cạnh thưa, thiếu trường và thông tin theo thao tác. So bốn baseline P3 được hỗ trợ.
- **Kiểm:** UNSUPPORTED khác ERROR; tín hiệu thiếu khác tín hiệu bình thường; không dùng thông tin tên ca để chọn kênh đặc trưng.
- **Đầu ra:** bằng chứng bổ sung hoặc phản bác khả năng chuyển sang hệ khác, với giới hạn cụ thể.
- **Phạm vi dự kiến:** kết quả và script phân tích của task.
- **Ranh giới:** không biến việc phương pháp chạy trên OB thành bằng chứng đã giải quyết dữ liệu thiếu.

Tách M8/M9 vì giao thức, chế độ hỗ trợ và câu hỏi dữ liệu khác nhau. Không tách vì thời gian máy của hai dataset cộng lại dài.

**M10 — Độ nhạy, cơ chế và đề xuất chọn thiết kế**

- **Loại:** thực nghiệm phân xử và tổng hợp khoa học.
- **Phụ thuộc:** M8–M9.
- **Việc làm:** đọc trước trung gian đã lưu; chỉ chạy thêm những thay đổi cần phân biệt giải thích. So ca đúng và sai tương ứng, không chỉ xem điểm trung bình.
- **Ma trận đề xuất:** bỏ từng nguồn tín hiệu; thay cửa sổ TT; giảm lượng nền; thay ngưỡng phát hiện. Những phép liên quan dấu, sàn số học hay mất cạnh chỉ thêm khi thiết kế hoặc kết luận thực sự phụ thuộc chúng.
- **Tiêu chí:** chỉ rõ điều kiện X, bước Y và thông tin Z bị giữ/mất/đánh giá sai. Nếu chưa chỉ được Y thì giữ OPEN, không gọi đặc tính chung là nguyên nhân.
- **Lựa chọn:** đề xuất cấu hình trên hiệu quả và độ ổn định của nhiệm vụ tương ứng; nêu cấu hình đối lập và bằng chứng chống lại lựa chọn.
- **Đầu ra:** đề xuất thiết kế cuối, điều kiện sử dụng, giới hạn, phần cần chuyển P9/P10.
- **Phạm vi dự kiến:** kết quả phân tích và đề xuất nội dung tài liệu phương pháp/WHY.
- **Nhánh:** C10 nếu dùng nhãn lan hoặc đưa ra kết luận phụ thuộc nhãn đó. Không tự thêm nhãn lan để làm bảng đẹp.

Nếu phép độ nhạy dẫn tới muốn đổi thiết kế ngoài tập đã khai, phải trình thay đổi và cập nhật các phép so phụ thuộc. Không âm thầm xem đó là “chỉ thử thêm”.

**M11 — So sánh cuối trên dev với baseline và đối chứng**

- **Loại:** thực nghiệm kiểm chứng trước G3.
- **Phụ thuộc:** đề xuất từ M10, phạm vi so sánh M1 và đối chứng M6.
- **Việc làm:** dùng lại mọi kết quả còn khớp; chạy phần thiếu cho cấu hình và các đối chứng được trình khóa. Kiểm ngân sách chọn cấu hình và độ tương đương ở những yếu tố không chủ ý thay.
- **Baseline:** giữ nhóm P3 chuẩn; chạy tại báo động P6 khi cần trả lời câu hỏi “xếp hạng tại cùng thời điểm”. Báo riêng so sánh pipeline phát hiện nguyên bản.
- **Ma trận:** phụ thuộc số cấu hình có nghĩa và số seed ngẫu nhiên được chọn có lý do; công thức khối lượng ở mục 7 dưới đây.
- **Kiểm:** ca lỗi, không báo động, thiếu tín hiệu, coverage, hòa điểm và mẫu số; kiểm hồi quy toàn chuỗi ở đúng đường đã thay sau thử sớm.
- **Đầu ra:** bảng dev cuối có thể truy về bản ghi, đủ phân biệt hiệu quả phương pháp, tác dụng của quan hệ và giới hạn phép so.
- **Phạm vi dự kiến:** kết quả/script phân tích của task.
- **Ranh giới:** không bắt đồ thị phải thắng mới hoàn thành; nếu bằng chứng không phân xử được thì khóa phạm vi kết luận tương ứng hoặc trình phần thiếu.

Task này có lý do cụ thể: cấu hình và thời điểm báo động cuối có thể khác bản thử sớm. Nó không phải một task “kiểm lại mọi thứ cho chắc”.

**M12 — Hồ sơ G3 và bàn giao P7–P10**

- **Loại:** tài liệu, khóa phạm vi đề xuất và bàn giao.
- **Phụ thuộc:** M10–M11 và các nhánh thực sự chặn thiết kế.
- **Việc làm:** tổng hợp mã/revision, cấu hình, giả thuyết, độ đo, tập ứng viên, trạng thái lỗi, bảng diễn giải và giới hạn. Liệt kê chính xác phần chưa có bằng chứng.
- **Bàn giao:** P7 nhận giao thức đánh giá; P8 nhận gói bằng chứng, không được đổi thứ hạng; P9 nhận định dạng nội bộ/API và yêu cầu quan sát; P10 nhận điều kiện cần kiểm trên hệ chạy thật.
- **Kiểm:** từ một kết luận đi ngược được tới bảng, bản ghi, cấu hình và nguồn; hướng dẫn trên máy khác không phụ thuộc trí nhớ của agent.
- **Đầu ra:** hồ sơ trình G3 và các giao diện đã được kiểm bằng dữ liệu/fixture thích hợp.
- **Phạm vi dự kiến:** tài liệu và kết quả của task; cập nhật nguồn chính thức theo đúng phạm vi Minh duyệt.
- **Ranh giới:** không chứa cài thuật toán, adapter hay đối chứng còn thiếu. Không mở test, không tự commit.

**5. Mười một task có điều kiện**

Đây là danh sách nghĩa vụ đã nhận diện, không phải danh sách mặc định phải thực hiện.

| Mã | Công việc và điều kiện kích hoạt | Đầu ra/phép kiểm | Quyết định phụ thuộc |
|---|---|---|---|
| **C1** | Khoảng thời gian không bị span con phủ, khi công thức thực sự dùng đại lượng này | Tính hợp các khoảng; kiểm chồng lấn, bất đồng bộ, span thiếu; không mặc định là self-time vật lý | Có dùng đặc trưng phân rã thời gian không |
| **C2** | Ứng viên phần dư có điều kiện, khi có lý do khoa học phải xét phương án này | Công thức, điều kiện nền, kiểm số học và so trung gian với phương án đang xét | Có thay/bổ sung họ chấm điểm không |
| **C3** | Hai câu còn lại của TraceRCA sau E1: chọn tập singleton và cờ frontend | Dùng trung gian E1 và bảy cặp đã có; đổi đúng bước cần phân xử | Có dùng cơ chế chấm tập hoặc cách diễn giải nhánh tác giả không |
| **C4** | Cài ứng viên chấm theo tập, chỉ sau C3 và khi hướng đó được phép thử | Cài một cơ chế xác định; oracle tập, điểm và thông tin quan hệ | Có đưa ứng viên này vào ma trận P6 không |
| **C5** | Bổ sung baseline TraceRCA nhánh tác giả, khi cần một đối chiếu mà baseline hiện tại chưa trả lời | Pin phiên bản, đặc tả khác biệt, chạy đúng miền so sánh | Kết luận so với nhánh tác giả |
| **C6** | Phân xử hai ca MicroRank còn lại, khi cơ chế dự định dùng hoặc nhận định về MicroRank phụ thuộc chúng | Lần theo bộ chia → đếm → trọng số → điểm, đối chiếu ca đúng | Có cơ sở dùng/sửa cơ chế tương ứng không |
| **C7** | Baseline MicroRank biến thể, sau C6 và khi có mục đích so sánh rõ | Cấu hình biến thể, phép kiểm và kết quả riêng với baseline chuẩn | Kết luận so với MicroRank biến thể |
| **C8** | BOCPD nhân quả, khi cần bộ phát hiện tham chiếu đã sửa hoặc phương pháp phụ thuộc nó | Tái sử dụng phần miền log đã kiểm; tách tác động tiền xử lý và số học; kiểm tiền tố và toàn dev được duyệt | So sánh với BOCPD nhân quả |
| **C9** | Underflow BOCPD trên 28 ca lịch sử còn lại, khi kết luận về kết quả lịch sử cần mở rộng sau E2 | Giữ đầu vào/tiền xử lý lịch sử; đối chiếu MAP và điểm đổi | Phạm vi diễn giải số BOCPD lịch sử; không chứng minh tính nhân quả online |
| **C10** | Hoàn thiện nhãn lan, khi báo cáo theo nhóm lan hoặc kết luận cơ chế cần nhãn đó | Quét ngưỡng/phân vị từ bảng lời gọi đã có; giữ nhóm không đo được; xét nền ngắn và nhiều tầng | Có khóa nhãn và dùng để phân nhóm không |
| **C11** | OM-07, khi kết luận P6 phụ thuộc quan hệ checkout–currency | Đối chiếu đúng nguồn, mapping và lời gọi liên quan | Phép so hoặc kết luận đang phụ thuộc cạnh này |

Mỗi nhánh có SPEC và kết quả riêng khi được kích hoạt. Phạm vi mã dự kiến:

- C1 bổ sung module trace.
- C2/C4 bổ sung module phương pháp tương ứng.
- C5/C7/C8 bổ sung adapter hoặc biến thể riêng, giữ baseline chuẩn.
- C3/C6/C9/C10/C11 chủ yếu nằm trong kết quả và script phân tích của task.

**C8 là một task khoa học, không phải ba task vì chia 30 ca thành ba đợt chạy. C9 cũng vậy.** Các đợt chạy vẫn cần ghi tiến độ, tài nguyên và giữ lượt hỏng.

Nếu có nút thắt hiệu năng, trước hết sửa trong task sở hữu module, với phép kiểm kết quả trước/sau. Chỉ đề xuất task tối ưu riêng khi đã đo được nút thắt và phạm vi thay đổi đủ độc lập. Không giữ sẵn một task tối ưu chung chung.

Các câu còn OPEN không được kích hoạt vẫn giữ nguyên trạng thái. Không dùng việc “chưa cần cho ứng viên này” để tuyên bố đã giải quyết chúng.

**6. Đối chiếu đủ 34 task chính và 15 task có điều kiện của bản cũ**

| Mã cũ | Xử lý trong kế hoạch mới |
|---|---|
| T-041 | Giữ phần thiết kế → **M1** |
| T-042 | Bỏ task đo tài nguyên độc lập; đo cùng xử lý thật ở **M2–M5**, dùng kết quả để quyết lịch chạy |
| T-043 | Hợp đồng được xác định ở **M1**, cài cùng module và hoàn thiện ở **M7** |
| T-044, T-045 | Dùng lại adapter; phần mới chia theo chứng cứ trace **M2**, tín hiệu/nền **M3**, thời gian khả dụng **M5** |
| T-046 | Chỉ mục tối thiểu → **M2**; cây/phân rã đầy đủ chỉ khi **C1** cần |
| T-047 | Đặc trưng trace cần thiết → **M2**; phần chưa phủ → **C1** |
| T-048, T-049, T-050 | Gộp thành **M3**, vì dùng chung scope, nền, chuẩn hóa và chống đếm lặp |
| T-051, T-054 | Gộp lõi điểm và hạng → **M4** |
| T-052, T-053 | Gộp phát hiện, vùng và kiểm toàn chuỗi → **M5** |
| T-055, T-056 | Dùng lại P3, chỉ cài phần thay đổi → **M7** |
| T-057 | Bản tối thiểu ở **M4**; kiểm đầy đủ đường quan hệ ở **M6** |
| T-058, T-059 | Gộp đối chứng cấu trúc/nguồn graph → **M6** |
| T-060 | Bỏ task audit chung; thiết kế phép so ở **M1**, kiểm phần nối ở **M7**, kết quả so ở **M11** |
| T-061, T-062 | N-Sigma dùng lại ở **M5/M11**; BOCPD mới chỉ theo **C8** |
| T-063, T-064 | Gộp chiến dịch so baseline tại báo động cuối → **M11**; một phần thử sớm ở **M5** |
| T-065 | Chuyển thành **C10** |
| T-066 | Gộp vào phát triển chứng cứ/tín hiệu và phân tích return → **M2–M3, M9–M10** |
| T-067 | Giữ chiến dịch TT, sửa ma trận và phụ thuộc → **M8** |
| T-068 | Giữ chiến dịch OB, sửa ma trận và phụ thuộc → **M9** |
| T-069, T-070, T-071 | Gộp lựa chọn với bằng chứng độ nhạy/cơ chế → **M10** |
| T-072 | Kiểm từ sớm ở **M4–M5**, phần giao thức ở **M7**, hồi quy đúng phần thay ở **M11** |
| T-073 | Giao diện ban đầu ở **M1**, bàn giao hoàn chỉnh ở **M12** |
| T-074 | Giữ hồ sơ G3, không chứa triển khai mới → **M12** |
| T-075 | → **C2** |
| T-076, T-077 | Gộp điều tra TraceRCA dùng chung trung gian → **C3** |
| T-078 | → **C4** |
| T-079 | → **C6** |
| T-080, T-081, T-082 | Gộp ba đợt chạy vào **C8** |
| T-083 | Không giữ task mặc định; xử lý nút thắt đã đo trong task sở hữu, hoặc trình phạm vi riêng |
| T-084 | → **C5** |
| T-085 | → **C7** |
| T-086 | → **C11** |
| T-087, T-088, T-089 | Gộp ba đợt chạy vào **C9** |

Số 12 task chính hình thành từ các ranh giới:

- 1 task thiết kế.
- 2 task tạo chứng cứ/đặc trưng.
- 2 task phát triển và thử sớm phương pháp.
- 2 task đối chứng và tích hợp bộ thực nghiệm.
- 2 chiến dịch dev có giao thức khác nhau.
- 1 task phân xử và lựa chọn.
- 1 task so sánh cuối.
- 1 task hồ sơ G3/bàn giao.

Không có task nào chỉ để tạo một loại file, chạy một batch hoặc viết một prompt.

**7. Khối lượng thực nghiệm: phần tính được và phần chưa được phép coi là đã biết**

Một cấu hình có:

- TT: `30 × 2 = 60` đơn vị ca–chế độ.
- OB: `22 × 1 = 22`.
- Tổng: **82**, không phải 104.

Phương án ban đầu để M1 xét là hai mức graph và hai cách gộp. Nếu cả bốn đều có nghĩa, phần lựa chọn của nhánh phương pháp có **328 đơn vị**. Không tự nhân thêm mọi cửa sổ, mọi chuẩn hóa và mọi đối chứng thành một tích Descartes.

Ma trận độ nhạy cơ sở đề xuất cho một thiết kế được xét:

| Phép thay | Khối lượng tối đa theo miền hiện có |
|---|---:|
| Bỏ lần lượt metric, log, trace | `3 × 82 = 246` |
| Một cửa sổ TT khác đã có căn cứ | `1 × 60 = 60` |
| Một mức giảm nền có nghĩa | `1 × 82 = 82` |
| Hai ngưỡng phát hiện quanh cấu hình tham chiếu | `2 × 30 = 60` |
| **Tổng** | **448 đơn vị** |

Đây là **ma trận đề xuất**, không phải số lượt đã duyệt. Phép thay không có nghĩa trên miền nào phải ghi rõ, không tạo một cấu hình giả để đủ bảng. Các giá trị cụ thể phải được xác định trước khi chạy; không chọn sau khi thấy điểm.

Với đối chứng, gọi:

- \(C\): số cấu hình thực sự được phép chọn;
- \(S\): số seed graph ngẫu nhiên có lý do sử dụng.

Nếu cả ba loại đối chứng đều hợp lệ trên toàn miền, khối lượng đối chứng là:

\[
82 \times C \times (2 + S)
\]

Trong đó hai nhánh không ngẫu nhiên là không quan hệ và graph tĩnh. Đây là trần tổ hợp logic; miền không hỗ trợ và kết quả đã có phải được thể hiện riêng.

**Không mặc định chạy mọi seed cho mọi phép độ nhạy.** Nhưng cũng không giảm ngân sách của đối chứng rồi vẫn tuyên bố đã so công bằng giữa những phương pháp được chọn cấu hình khác nhau. M1 phải phân biệt phép bỏ thành phần của một thiết kế cố định với phép so các nhánh được tối ưu riêng.

Đối với baseline:

- Kết quả chế độ (a) cũ dùng lại khi điều kiện khớp.
- Nếu chạy đủ sáu baseline TT tại báo động mới: tối đa `5 × 30 + 3 × 30 = 240` lượt vật lý, với TORAI ba seed theo giao thức.
- Không có báo động hợp lệ thì ghi đúng trạng thái và mẫu số; không bịa một lượt RCA.
- Baseline mới, tuning mới hoặc BOCPD mới không nằm ngầm trong 240 lượt này.

Các lượt thử M4–M5 được dùng lại trong ma trận sau nếu mã, đầu vào và cấu hình không đổi. Không chạy lại chỉ để chuyển kết quả sang task khác.

**8. Thời gian, ngữ cảnh và phản biện**

Hiện có một ví dụ đo thực tế: [thống kê T-035](D:/RCA-flashticket/results/T-035/thong-ke-do-thi.json), tại `#/cost`, ghi lượt dựng graph khoảng **18,1 phút máy**, RSS đỉnh khoảng **2,25 GiB**.

Số đó cho biết chi phí của lượt dựng graph đã thực hiện. Nó **không** cho biết thời gian trích đặc trưng mới, thời gian agent phân tích, dung lượng cache mới hoặc task P6 có vừa ngữ cảnh hay không.

| Thành phần | Cách đưa vào kế hoạch này |
|---|---|
| Thời gian máy | Đo trên đường xử lý thật ở M2–M5; ghi riêng đọc dữ liệu, tạo đặc trưng, chấm và lưu |
| RAM/đĩa | Đo theo trung gian thực tế; không lấy các trần RAM/đĩa cũ làm dự báo |
| Công việc agent | Tính đủ đọc nguồn, cài, oracle, đọc trung gian, phân tích ca/ô, tài liệu và bàn giao; **chưa có căn cứ quy thành tổng giờ đáng tin cậy** |
| Context | Đánh giá khả năng giữ mạch qua nguồn, quyết định và lượng bằng chứng cần đọc; chưa có phép quy đổi từ giờ máy |
| Phản biện | Là một phần vòng đời mỗi task; số lượt và thời gian chờ chưa biết |
| Sửa sau phản biện | Xác định theo ảnh hưởng: sửa lời diễn giải, sửa module, hay đổi giao thức phải phát lại các kết quả phụ thuộc |

Tôi không cộng một tỷ lệ dự phòng như 30% hoặc 50%. Thay vào đó, kế hoạch chỉ rõ hậu quả của từng loại phát hiện:

- Sai diễn giải: sửa tài liệu, đối chiếu lại nguồn.
- Sai một đặc trưng: sửa module, chạy lại các cấu hình dùng đặc trưng ấy.
- Sai giao thức thời gian hoặc mẫu số: dừng kết luận liên quan, phát lại toàn bộ phạm vi bị ảnh hưởng.
- Ứng viên bị bác bỏ: trình nhánh phương pháp khác và ngân sách mới; không coi đó là lỗi kỹ thuật cần sửa cho đến khi thắng.

Các lượt dài vẫn phải xin quyền chạy theo quy định hiện hành. Chia batch không làm mất nghĩa vụ đó.

**9. Thứ tự triển khai và mục tiêu đồ án hoàn chỉnh**

Chuỗi chính:

```text
M1
 ├─ M2 ─┐
 └─ M3 ─┴─ M4 → M5
                  ├─ M6 ─┐
                  └──────┴─ M7
                             ├─ M8 ─┐
                             └─ M9 ─┴─ M10 → M11 → M12
```

M2/M3 có thể phát triển độc lập sau khi thống nhất hợp đồng. M8/M9 có thể xử lý song song về công việc, nhưng không mặc định chạy hai tác vụ nặng đồng thời trên laptop. M6 có thể chuẩn bị sau M4; phải kiểm cả đường phát hiện khi M5 đã có.

**P9a không đợi M12.** Bộ yêu cầu ban đầu đã có tại [yeu-cau-quan-sat-p9.md](D:/RCA-flashticket/results/T-040/yeu-cau-quan-sat-p9.md). M1 bổ sung nhu cầu thiết kế, M5 cung cấp giao diện chạy được, M12 bàn giao bản cuối. Việc triển khai hoặc gửi sang nhóm hệ thống cần phạm vi giao việc riêng; lượt này không thực hiện.

Các phần sau P6 vẫn cần thiết để đạt mục tiêu Minh nêu:

| Chặng | Nghĩa vụ giữ nguyên |
|---|---|
| P7 | Đánh giá sau khóa trên test/dataset giữ ngoài; chỉ mở khi được phép |
| P8 | Giải thích trung thành với bằng chứng; không dùng LLM sửa thứ hạng |
| P9 | Đọc dữ liệu thật từ hệ quan sát, đổi về cùng định dạng nội bộ và chạy cùng lõi RCA |
| P10 | Lỗi tự tiêm, tải thay đổi, nhãn độc lập phù hợp, kiểm các cạnh/quan sát công khai còn thiếu và demo |
| Báo cáo | Viết dần căn cứ phương pháp, giao thức, kết quả dev và giới hạn từ M1/M8–M12; bổ sung kết quả cuối từ P7/P10 |

Cải thiện có ý nghĩa phải gắn với điều kiện và bằng chứng. Nếu một hướng không cải thiện, kế hoạch phải cho phép nhận ra sớm và giải thích đúng; không được loại nhóm khó hoặc đổi phép chấm để giữ kết luận có lợi.

**10. Phạm vi lưu sau này và điều còn chưa chốt**

Nếu Minh muốn lưu bản kế hoạch sau phản biện, file đề xuất là:

`D:/RCA-flashticket/docs/PLAN-P6.md`

Không tạo đồng loạt 23 thư mục task. Từng SPEC được lập khi đầu vào và nhánh phụ thuộc đã đủ rõ. Các thay đổi mã chung và nguồn quyết định phải được nêu trong phạm vi của chính SPEC.

Những điểm chưa chốt là:

- Công thức cụ thể và tập cấu hình được phép thử.
- Cách định nghĩa đối chứng không quan hệ trên chứng cứ thực tế.
- Số seed và ngân sách so sánh phù hợp.
- Nhánh có điều kiện nào thực sự cần kích hoạt.
- Chi phí mới đo được khi triển khai.

Đây là các quyết định nghiên cứu/triển khai còn phải làm, không phải những con số có thể điền cho kế hoạch trông hoàn chỉnh. Tuy vậy, **đầu ra, quan hệ phụ thuộc và nơi chịu trách nhiệm đã được phân công**, không dồn chúng vào task tổng hợp cuối.

**Báo cáo lượt này**

1. **Đã làm:** rà lại đủ 49 task cũ, đối chiếu nguồn và mã tái sử dụng, lập phương án 12 task chính và 11 task có điều kiện.
2. **File thay đổi:** không sửa file nào; không ghi DECISIONS.
3. **Kiểm:** đối chiếu mã P3/P5, MRP/G2/bàn giao; kiểm hash các nguồn trực tiếp được dùng lại; trạng thái Git cuối lượt khớp đầu lượt. Không chạy thực nghiệm mới.
4. **Còn mở:** công thức, ngân sách cấu hình/seed, nhánh được kích hoạt và chi phí triển khai thực tế. Bản này đề xuất cách tổ chức công việc; chưa duyệt phương pháp, chưa xác nhận lợi ích và chưa cấp quyền G3/test.

**Prompt để Minh chuyển sang phiên Codex khác**

Khi chuyển, gửi kèm **nguyên văn toàn bộ kế hoạch trên**, yêu cầu ban đầu trong tệp đính kèm và yêu cầu đính chính mới nhất của Minh. Các yêu cầu đó là tài liệu đầu vào, không thay bằng bản tóm tắt.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch phân rã P6 sửa đổi, được Minh gửi kèm nguyên văn trong chat; chưa có file kế hoạch chính thức.
- Công đoạn: soát SPEC.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex phiên lập kế hoạch là người làm; Codex phiên này là người phản biện độc lập kế hoạch theo yêu cầu Minh. Phân công này chỉ áp dụng lượt kế hoạch, không tự áp sang phản biện kết quả các task sau.
- Tài liệu gốc: nguyên văn yêu cầu ban đầu của Minh về lập kế hoạch, độ chi tiết và khảo sát khối lượng; nguyên văn yêu cầu đính chính mới nhất; toàn bộ kế hoạch sửa đổi gửi trong chat; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước: các bản kế hoạch, phản biện và phản hồi trước do Minh gửi kèm theo thứ tự thời gian. Các tài liệu gốc đang có trên máy này gồm C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt; C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt. Nếu chuyển máy, dùng nguyên văn tài liệu Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-034/goi-g2.md; results/T-035/ đến results/T-040/; nguồn T-032/T-033 theo con trỏ gốc; manifest hiện hành và pin lịch sử tương ứng. Đọc D:/Project/flash-ticket-platform/docs/architecture/B16-observability-baseline.md khi cần, theo luật trực tiếp chi phối repo đó; repo hệ thống chỉ đọc. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Yêu cầu của Minh cho lượt phản biện kế hoạch:
Đánh giá TOÀN BỘ kế hoạch và các giao diện giữa task, không chỉ từng dòng riêng: mục tiêu nguồn, căn cứ thiết kế, khả năng phân xử, phần bỏ sót/chồng lặp, khối lượng công việc, dự toán, phụ thuộc, nhánh có điều kiện, tích hợp và G3.
Áp dụng nguyên văn yêu cầu đính chính mới nhất Minh gửi kèm về thời gian máy, công việc agent, “vừa một phiên”, nén ngữ cảnh và cách chia task.
Phân biệt lỗi kế hoạch thật với bất định nghiên cứu hợp lệ. Không đòi kết quả thực nghiệm chưa được duyệt, không thu hẹp mục tiêu để làm task vừa phiên và không coi số task ít hơn là bằng chứng kế hoạch tốt hơn.
```
````

</details>

<a id="s07"></a>

### S07 — Yêu cầu của Minh về tính khả thi detector và RCA

<details>
<summary>Mở nguyên văn S07</summary>

````text
bộ phát hiện và RCA dự định dựng dựa trên tiêu chí nào, base line nào, căn cứ và khoa học nào , đặc biệt là baseline của bộ phát hiện còn ít thông tin , chưa đa dạng và kết quả cũng kém trong P3, tôi khá bi quan về mức độ khả thi , 1 bộ phát hiện báo cảnh báo liên tục là không thực tế và không có tính áp dụng, cho phép dùng 1 subagent , tôi cần một cái nhìn rõ ràng

````

</details>

<a id="s08"></a>

### S08 — Codex phân tích căn cứ detector và RCA

<details>
<summary>Mở nguyên văn S08</summary>

````text
**Lo ngại của Minh có căn cứ. Hiện chúng ta có nền tảng để tiếp tục nghiên cứu RCA, nhưng chưa có đủ bằng chứng để nói bộ phát hiện P6 sẽ dùng được trong vận hành.** Kế hoạch tôi vừa trình đã làm rõ phần tổ chức công việc hơn phần căn cứ thiết kế bộ phát hiện. Đây là thiếu sót cần sửa.

Tôi đã dùng đúng một subagent kiểm độc lập nguồn trong repo, đối chiếu lại số P3 và đọc thêm nguồn khoa học gốc. Có ba điểm cần nói rõ ngay:

- **N-Sigma và BOCPD hiện tại chưa đủ làm bộ đối chiếu cho tính thực dụng.**
- **Thêm đồ thị không tự giải quyết cảnh báo liên tục.**
- **Một detector có F1 khá hơn nhưng vẫn gần như luôn báo là không đạt mục tiêu áp dụng.**

**1. P3 thực sự cho thấy vấn đề nghiêm trọng đến đâu?**

Các số dưới đây lấy từ [phat-hien.json](D:/RCA-flashticket/results/T-025/phat-hien.json), đã kiểm chuỗi hash qua bản tổng hợp G2.

| Cấu hình P3 | F1 theo cửa sổ | Cờ thô trước tiêm, quy đổi/giờ | Thông báo trước tiêm sau cooldown 300 giây, quy đổi/giờ | Báo động đầu tại/sau tiêm |
|---|---:|---:|---:|---:|
| BOCPD | 0,555 | 23,87 | 6,34 | 3/30 ca |
| N-Sigma, bộ cột chính | 0,671 | 1.167,68 | 13,35 | 0/30 ca |
| N-Sigma, mọi cột | **0,706** | **3.563,03** | **17,42** | 0/30 ca |

Con trỏ nguồn: `#/bo_phat_hien/{bocpd,nsigma,nsigma_doi_chung}/tong_hop`, phần `co_dieu_kien_tren_ca_OK` và `theo_ca_tren_30`.

Đáng chú ý nhất: **N-Sigma mọi cột có F1 cao nhất, nhưng bật cờ ở 18.409 trên 18.600 giây trước tiêm được đánh giá — khoảng 99%.** Đây là bằng chứng trực tiếp rằng chọn theo F1 trong giao thức này có thể chọn một detector gần như luôn báo.

Cần giữ đúng giới hạn: “trước tiêm” ở đây là **nhãn thay thế của giao thức**, chưa phải đoạn vận hành khỏe đã được xác nhận độc lập. Vì vậy, bảng không phải tỷ lệ báo giả ngoài thực tế. Nhưng giới hạn đó **không biến kết quả thành chấp nhận được**. Nó cho thấy cả hành vi detector lẫn khả năng đánh giá đều cần được xử lý.

Từ mã và P4, chúng ta biết thêm:

- N-Sigma dùng trung bình/độ lệch chuẩn của toàn bộ quá khứ rồi gộp cờ từ các cột bằng phép OR: một cột báo là cả hệ báo. Thêm cột không thể làm giảm số cờ theo cách gộp này.
- N-Sigma đã dùng tiền xử lý theo quá khứ. Không thể hứa “sửa nhìn trước” sẽ cứu nó.
- BOCPD P3 có tiền xử lý nhìn toàn bản ghi. Sửa thành xử lý nhân quả là điều kiện hợp lệ, **chưa phải bằng chứng sẽ giảm báo nhầm**.
- Cooldown chỉ giảm số thông báo được phát ra. Nó không sửa việc hệ thống bị đánh dấu bất thường liên tục.

Các phân biệt này đã nằm trong [WHY-34/35](D:/RCA-flashticket/docs/WHY.md:333) và [phân tích T-033](D:/RCA-flashticket/results/T-033/runs/phan-hoi-review-001/bo-sung-bao-cao.md).

**2. Bộ phát hiện phải được dựng theo tiêu chí nào?**

Trước khi chọn thuật toán, phải xác định **sự kiện cần phát hiện**.

Ví dụ trong FlashTicket:

- Tải tăng, CPU tăng nhưng giao dịch vẫn đạt yêu cầu: chưa đủ để gọi là sự cố.
- Người dùng không đặt được vé, thời gian xử lý tăng kéo dài, thanh toán hoặc phát hành vé thất bại: là những mục tiêu cần xét.
- “Hết vé” đúng nghiệp vụ không tự được tính là lỗi hệ thống.
- Tải tăng làm cạn tài nguyên và gây giao dịch thất bại: vẫn là sự cố thật; không được loại đi chỉ vì nguyên nhân khởi đầu là tải.

Đây là các ví dụ để định nghĩa phạm vi, **chưa phải tiêu chí FlashTicket đã được chốt**.

Tôi đề xuất đánh giá ở ba mức khác nhau:

| Mức | Cần trả lời |
|---|---|
| **Điểm bất thường** | Tín hiệu có lệch khỏi hành vi phù hợp với điều kiện hiện tại không? |
| **Cảnh báo sự cố** | Sự lệch đó có đủ đáng kể, kéo dài hoặc có tác động để yêu cầu xử lý không? |
| **RCA** | Với sự cố và bằng chứng hiện có, thành phần nào đáng nghi nhất? |

Các tiêu chí chọn detector cần gồm:

- **Số đợt cảnh báo nhầm trên thời gian vận hành khỏe đã xác minh.**
- **Tỷ lệ sự cố phát hiện được**, tách theo loại và mức độ.
- **Độ trễ phát hiện**, tính từ mốc tác động phù hợp; không đánh tráo mốc tiêm với onset thật.
- **Thời gian còn giữ cảnh báo sau khi sự cố đã hết.**
- **Tỷ lệ thời gian hệ thống ở trạng thái cảnh báo**, cùng số thông báo lặp.
- Chi phí xử lý và thời điểm kết quả thực sự có thể phát ra.

Google SRE cũng đánh giá chiến lược cảnh báo bằng precision, recall, thời gian phát hiện và thời gian trở về trạng thái bình thường; cảnh báo được gắn với sự kiện có ý nghĩa đối với chất lượng dịch vụ. Đây là căn cứ vận hành, không phải bằng chứng rằng một thuật toán cụ thể sẽ thắng trên FlashTicket. [Nguồn Google SRE](https://sre.google/workbook/alerting-on-slos/).

**Tiêu chí lựa chọn nên là “phát hiện được bao nhiêu sự cố trong một mức báo nhầm và độ trễ chấp nhận được”, không chỉ “F1 lớn nhất”.**

Các mức chấp nhận cụ thể hiện **chưa được chốt**. Tôi không nên tự điền một con số như “một cảnh báo/ngày” rồi coi đó là yêu cầu khoa học đã có.

**3. Baseline phát hiện cần bổ sung những gì?**

Tôi đề xuất bộ đối chiếu theo **cơ chế và câu hỏi**, không theo số lượng tên thuật toán.

| Nhóm | Đại diện đề xuất | Mục đích so sánh | Điều kiện và giới hạn |
|---|---|---|---|
| **Mốc lịch sử P3** | N-Sigma, BOCPD hiện hành | Biết cải thiện so với những cấu hình đã phân tích | Giữ đúng giới hạn; BOCPD hồi cứu không được trình như cảnh báo online |
| **Cảnh báo theo chất lượng dịch vụ** | Quy tắc trên SLI/SLO: tỷ lệ lỗi, tỷ lệ request chậm, giao dịch thất bại | Đối chiếu với một cách cảnh báo có ý nghĩa sử dụng trực tiếp | Cần định nghĩa nghiệp vụ và tín hiệu tương ứng; không chọn SLI theo root của từng ca |
| **Ngưỡng thống kê bền vững hơn** | Phân vị hoặc median–MAD, xử lý theo quá khứ | Kiểm xem thay cách ước lượng nền/ngưỡng đã đủ cải thiện chưa, trước khi cần graph | Đây là cấu hình cần đặc tả và thử; vẫn có thể sai khi tải đổi hoặc nền bị nhiễm |
| **Phát hiện thay đổi tích lũy** | CUSUM | Bắt thay đổi nhỏ nhưng kéo dài, khác việc báo từng điểm vượt ngưỡng | Cần xác định nền và độ thay đổi quan tâm; phải kiểm ảnh hưởng tự tương quan và đổi tải |
| **Học quan hệ đa biến** | GDN, khi điều kiện dữ liệu đáp ứng | So với một phương pháp phát hiện có sử dụng quan hệ giữa các tín hiệu | Cần dữ liệu học/hiệu chỉnh hợp lệ và bộ cột ổn định; graph học được không đồng nghĩa graph phụ thuộc dịch vụ |

CUSUM có cơ sở thống kê về tích lũy sai lệch và thiết kế đánh đổi giữa báo nhầm, bỏ sót và mức thay đổi cần phát hiện. Tuy nhiên, kết quả lý thuyết không tự chuyển thành bảo đảm trên telemetry microservice. [NIST: CUSUM](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm).

GDN đã có [hồ sơ trong repo](D:/RCA-flashticket/results/T-018/ho-so-gdn.md), nên không cần khảo sát lại từ đầu. Bài gốc học dự báo từ dữ liệu bình thường, dùng quan hệ giữa các cảm biến và đặt ngưỡng trên tập validation. Điều kiện đó phải được kiểm với dữ liệu của chúng ta; không thể thêm GDN vào bảng để tạo cảm giác đa dạng rồi bỏ qua nền học không phù hợp. [Bài GDN](https://bhooi.github.io/papers/gdn_aaai2021.pdf).

**SPOT cũng đáng xét, nhưng phải đặt đúng vai trò:** nó dùng lý thuyết giá trị cực trị để hiệu chỉnh ngưỡng. Nếu chỉ thay ngưỡng trên cùng một chuỗi điểm, đó là đối chiếu cách hiệu chỉnh, không phải một phương pháp phát hiện độc lập hoàn toàn. SPOT có giả định về phân bố ổn định; DSPOT xử lý một dạng trôi nền. Tham số rủi ro của nó không tự là số cảnh báo sự cố nhầm mỗi giờ. [Bài SPOT/DSPOT](https://www.amossys.fr/wp-content/uploads/anomaly-detection-with-evt-1.pdf).

Khuyến nghị của tôi là **ưu tiên đối chiếu vận hành, ngưỡng thống kê hợp lý và CUSUM trước**. GDN và SPOT được xét theo khoảng trống còn lại và điều kiện dữ liệu. Không mặc định cài tất cả.

**4. Căn cứ của phương pháp đồ thị hiện mạnh ở RCA hơn ở phát hiện**

Đây là điểm quan trọng nhất cần sửa trong lập luận trước của tôi.

Ứng viên “quy chứng cứ thời lượng từ phía gọi sang phía được gọi” có căn cứ P4 cho **một số vấn đề xếp hạng**. Nhưng điều đó chưa trả lời:

> Khi hệ thống vẫn hoạt động bình thường nhưng tải thay đổi, điểm toàn hệ có giữ thấp không?

Một ví dụ toán học đơn giản: nếu graph chỉ chuyển cùng các điểm sang những nút khác, thì điểm lớn nhất có thể vẫn giữ nguyên:

\[
s'=\text{hoán vị của }s
\quad\Rightarrow\quad
\max(s')=\max(s)
\]

Khi ấy, thứ hạng root có thể thay đổi, nhưng detector lấy điểm lớn nhất **không được cải thiện chút nào**. Đây là phản ví dụ với lập luận “RCA dùng cạnh tốt hơn nên cảnh báo sẽ tốt hơn”, không phải kết luận rằng mọi cách gộp điểm của ứng viên đều chỉ là hoán vị.

Vì vậy, phần phát hiện cần một giả thuyết riêng, chẳng hạn:

> Quan hệ giữa các thành phần giúp dự báo hoặc mô tả hành vi bình thường theo ngữ cảnh, từ đó phân biệt biến động hợp lệ với sai lệch bất thường tốt hơn cách xét từng tín hiệu riêng.

Đó là **ứng viên chưa kiểm**. Để thử, phải so:

- Cùng tín hiệu và lịch sử của chính thành phần.
- Thêm thông tin từ thành phần có quan hệ.
- Thay bằng quan hệ ngẫu nhiên.
- Giữ cùng cách hiệu chỉnh cảnh báo và ngân sách chọn cấu hình.

Giả thuyết có thể sai khi quan hệ không cung cấp thông tin thêm, nền thiếu, graph sai hoặc thay đổi tải chưa được quan sát. Không được coi “cô yêu cầu graph-based detection” là bằng chứng giả thuyết đúng.

Còn phần RCA có thể tiếp tục trên căn cứ hiện có:

| Tiêu chí RCA | Đối chiếu |
|---|---|
| Xếp đúng root trên cùng bằng chứng/cửa sổ | Các baseline P3 được hỗ trợ; giữ SimpleRCA và TORAI_B ở TT |
| Thông tin quan hệ thực sự có đóng góp | Nhánh không quan hệ và graph ngẫu nhiên giữ bậc |
| Không chỉ thắng ở một ô | Theo dataset, loại lỗi, vị trí root và từng cặp ca |
| Xử lý được trường hợp khó | Root thiếu cạnh/tín hiệu, return, nhiều triệu chứng, thiếu log/trace |
| Dùng được trong chuỗi chạy thật | RCA tại thời điểm cảnh báo thực sự có thể phát ra; tính cả thời gian chờ dữ liệu |

Không gọi một thành phần là nguyên nhân nhân quả đã xác nhận chỉ vì điểm của nó cao nhất.

**5. Làm gì với tình trạng “cảnh báo liên tục”?**

Một hệ cảnh báo cần quản lý **một đợt sự cố**: lúc nghi ngờ, lúc mở cảnh báo, lúc cập nhật và lúc xác nhận phục hồi. Persistence, gộp cảnh báo và điều kiện phục hồi là các thành phần kỹ thuật hợp lý. Prometheus và Alertmanager có các cơ chế chờ điều kiện tồn tại, giữ trạng thái, loại trùng và nhóm thông báo. [Alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/), [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/).

Nhưng phải kiểm hai việc riêng:

1. **Detector có phân biệt đúng không?**
2. **Chính sách thông báo có trình bày sự cố hợp lý không?**

Một detector luôn bật, được giới hạn gửi một tin mỗi giờ, vẫn là detector không dùng được. Ngược lại, một sự cố kéo dài có thể hợp lý khi duy trì một cảnh báo đang mở; không cần phát tin mới ở mỗi tick.

Vì vậy phải đo cả điểm/cờ thô, trạng thái sự cố và thông báo. Đồng thời đo sự cố bị bỏ lỡ hoặc phát hiện chậm do bộ lọc cảnh báo. Không dùng cooldown để che chất lượng kém.

**6. Mức khả thi hiện tại: có thể tin tới đâu?**

| Mục tiêu | Đánh giá từ bằng chứng hiện có |
|---|---|
| Xây và kiểm một phương pháp RCA dùng graph | **Có cơ sở để triển khai nghiên cứu**, nhờ P3–P5 |
| Chứng minh RCA cải thiện trong một số điều kiện | **Có giả thuyết đáng thử, chưa có kết quả phương pháp mới** |
| Xây detector tốt hơn hai cấu hình P3 | **Có hướng thử, chưa có bằng chứng thành công** |
| Chứng minh detector ít báo nhầm khi chạy liên tục | **Thiếu bằng chứng đánh giá thiết yếu** |
| Đưa cảnh báo vào FlashTicket để sử dụng thực tế | **Chưa thể khẳng định đạt** |

Khoảng thiếu lớn nhất không chỉ là thuật toán. Chúng ta cần dữ liệu có:

- Những đoạn không tiêm lỗi **và có kiểm chứng chất lượng giao dịch**, ở nhiều mức tải.
- Tải tăng hợp lệ, tải gây quá tải thật và các lỗi tự tiêm.
- Mốc bật lỗi, mốc có tác động và mốc phục hồi được phân biệt.
- Bằng chứng đánh giá độc lập phù hợp, không lấy chính cờ detector làm nhãn.
- Phần học/hiệu chỉnh tách khỏi phần đánh giá; không ghép các snapshot sự cố thành một dòng vận hành giả.

Các nhu cầu này đã được nêu trong [T-033, phần chuẩn nền và thời điểm tác động](D:/RCA-flashticket/results/T-033/runs/phan-hoi-review-001/bo-sung-bao-cao.md:238). Dataset hiện tại vẫn hữu ích cho phát triển và phân tích cơ chế. Nhưng nếu thiếu những quan sát trên, **không có cách diễn giải F1 hay chọn thêm mô hình nào thay thế được bằng chứng về tính áp dụng**.

**Đề xuất của tôi cho bước tiếp theo**

Trước khi coi kế hoạch P6 là sẵn sàng triển khai, cần làm rõ phần thiết kế bộ phát hiện trong M1/M5:

1. Xác định sự cố cần báo và tiêu chí chấp nhận.
2. Chốt bộ baseline theo các cơ chế khác nhau và khả năng dữ liệu hỗ trợ.
3. Tách giả thuyết graph giúp phát hiện khỏi giả thuyết graph giúp RCA.
4. Đưa việc chuẩn bị bằng chứng vận hành ở P9 lên sớm; vẫn giữ đánh giá công khai và các giới hạn của nó.

Đây là đề xuất nội dung cần bổ sung, chưa phải quyết định đổi phương pháp hoặc thêm task.

**Tôi chưa có cơ sở để trấn an Minh rằng “chắc chắn khả thi”. Nhưng cũng chưa có cơ sở kết luận hướng nghiên cứu thất bại.** Điều có thể kết luận chắc hiện nay là: lấy hai detector P3 làm chuẩn, thêm điểm graph và cooldown, rồi coi đó là một bộ phát hiện thực dụng thì **chưa đủ căn cứ**.

- **Đã làm:** kiểm nguồn repo, số P3, mã detector và nguồn khoa học; dùng đúng một subagent.
- **File thay đổi:** không có.
- **Kiểm:** chuỗi hash nguồn số P3 khớp; trạng thái Git không đổi; không chạy thực nghiệm.
- **Còn mở:** tiêu chí vận hành, baseline bổ sung, giả thuyết phát hiện và dữ liệu để xác nhận khả thi.
````

</details>

<a id="s09"></a>

### S09 — Phản biện căn cứ và kế hoạch

<details>
<summary>Mở nguyên văn S09</summary>

````text
Tôi đang đọc gói G2 và các nguồn gốc để soát kế hoạch của Codex. Chưa sửa file nào.

Tôi đang kiểm các khẳng định về mã và số trong kế hoạch của Codex (bộ phát hiện, bộ chấm, chi phí T-035).

Tôi đã đọc xong nguồn và kiểm các con số. Giờ đọc mẫu prompt để soạn phần bàn giao.

## Kết luận

**Chưa nên duyệt nguyên trạng kế hoạch 12 + 11.** Cách chia mới tốt hơn bản 34 + 15 ở ba điểm: thử phương pháp sớm (M4–M5), dùng lại đúng phần đã có của P3–P5, và mỗi nhánh có điều kiện có lý do kích hoạt.

Chỗ yếu nhất là **bộ phát hiện**, đúng chỗ Minh lo. Kế hoạch có hai lỗi chặn ở phần này (P1 và P2 bên dưới). Phần RCA đi đúng hướng nhưng còn thiếu quy tắc rẽ hướng sau lượt thử đầu.

---

## 1. Hết P6, Minh có gì trong tay

| Có | Không có (thuộc chặng sau) |
|---|---|
| Mã `src/p6/`: trích chứng cứ trace, tín hiệu metric/log, chấm điểm, xếp hạng, phát hiện trực tuyến, vùng nghi ngờ, đối chứng, bộ chạy và bộ chấm | Kết quả trên tập test và dataset giữ ngoài (P7) |
| Đặc tả phương pháp cùng các mục WHY: mỗi thành phần ghi rõ sửa hạn chế nào, đáp ứng DT18 hay phục vụ nhu cầu kỹ thuật | Bằng chứng đồ thị giúp thật; chỉ P7 trả lời được |
| Kết quả dev: TT chế độ (a) và (b), OB chế độ (a); độ nhạy; ba đối chứng (bỏ quan hệ, đồ thị ngẫu nhiên giữ bậc, đồ thị tĩnh so với quan sát); so với baseline | Lớp LLM giải thích (P8) |
| Hồ sơ G3: cấu hình khóa, giả thuyết, bảng diễn giải, giao thức P7 | Chạy trên FlashTicket và demo (P9b, P10) |
| Giao diện bàn giao cho P8 (gói bằng chứng), P9 (định dạng nội bộ, yêu cầu quan sát), P10 | Đánh giá phát hiện có nền sạch và onset thật |

Với quyển đồ án: hết P6 viết được chương thiết kế phương pháp và thực nghiệm trên dev. Chương so sánh cuối phải chờ P7.

## 2. Bộ phát hiện và RCA đang đi theo hướng nào

**RCA (M4).**
- Ứng viên chính là UV-1: thời lượng đo ở span phía gọi được tính cho dịch vụ **được gọi**, dựa vào cạnh gọi.
- Căn cứ ở mức ĐC: root đứng đầu theo vị trí này ở 19/20 ca TT và 13/20 ca OB (`goi-g2.md` §5, UV-1).
- Hướng này có ba giới hạn đã biết:
  - Ở TT gần như không còn chỗ để tăng. TORAI B đã đúng 26/30 ca, SimpleRCA không dùng quan hệ vẫn đạt 0,833 (`goi-g2.md` §0).
  - UV-1 không giúp được 8 ca root không được dịch vụ nào gọi, ví dụ auth.
  - Hiện tượng "chờ" có cả ở ca đúng (83/96).
- Chỗ có thể cải thiện có ý nghĩa là **Nezha-OB**, nơi mọi baseline yếu (cao nhất BARO 0,364), nhất là lỗi return và lỗi trễ mạng. Ở đó cần UV-1 đi cùng tín hiệu riêng của nút và log (UV-6). Kế hoạch có nhắc phần return trong M3, nhưng chưa coi OB là nơi chính để chứng minh cải thiện.

**Phát hiện (M5).**
- Điểm hệ thống gộp từ điểm của từng phần tử (cạnh, nút), cộng nền và ngưỡng cập nhật trực tuyến, chỉ dùng dữ liệu đã đến.
- Chỉ chạy trên 30 ca TT. OB không có chế độ (b), và lý do đúng: trace/log Nezha chỉ có quanh mốc tiêm (Q-64).
- Đối chiếu chỉ có N-Sigma. BOCPD nằm ở nhánh có điều kiện C8.

## 3. Phản biện

### P1 — CHẶN: baseline phát hiện vẫn mỏng như P3, và kế hoạch không có chỗ nào xử lý việc này

- **Chặn:** mọi kết luận RQ3a ở M5, M11, G3.
- **Bằng chứng:**
  - N-Sigma báo 1.168 lần mỗi giờ bình thường và 0/30 ca có báo động đầu đúng. BOCPD đúng 3/30 ca (`goi-g2.md` §2.5). Đối chiếu với hai bộ này gần như chắc thắng, nên thắng không chứng minh gì (MRP §6 mục 2, "baseline phải mạnh").
  - Q-62 đưa GDN vào tầng 2 và Q-69 ghi "phần chấm phát hiện trên dữ liệu công khai mỏng; xem lại sau G2". Kế hoạch không nhắc tới cả hai.
  - T-015 đã lập hồ sơ bộ phát hiện trace của MicroRank (μ+1,5σ, hơn 8 trace) và của TraceRCA, nhưng kế hoạch không dùng.
  - Bộ phát hiện P6 dùng trace, còn hai baseline chỉ dùng metric (`phat_hien.py:9`, cột latency-50 và `_error`). Thắng hai bộ này có thể chỉ do khác nguồn tín hiệu, không do đồ thị.
- **Hậu quả:** câu "bộ phát hiện đồ thị tốt hơn baseline" sẽ không bảo vệ được trước cô.
- **Sửa tối thiểu:**
  - M1 chốt bộ baseline phát hiện kèm lý do, gồm ít nhất một bộ dùng trace có hồ sơ sẵn từ P1.
  - Quyết rõ BOCPD: chạy bản nhân quả (C8) hay chỉ giữ số lịch sử kèm giới hạn.
  - Ghi đánh giá GDN theo tiêu chí WHY-10, kể cả khi kết quả là không làm.
  - Trình Q-69 cho Minh quyết lại.

### P2 — CHẶN: rò mốc tiêm qua biên file RE2-TT chưa được xử lý

- **Chặn:** kết luận phát hiện trên dev và trên test.
- **Bằng chứng:**
  - Mọi file RE2-TT có đúng 720 điểm trước mốc tiêm và 720 điểm sau. Điểm giữa file cho lại mốc tiêm (`results/T-002/the-rcaeval.md:123`).
  - T-002 ghi rõ giao thức tự phát hiện của P3/P7 phải xử lý nguy cơ này trước khi chấm.
  - M5 chỉ kiểm phát lại theo tiền tố, tức chống dùng dữ liệu tương lai. M10 lại chỉnh ngưỡng và lượng nền trên dev.
- **Hậu quả:**
  - Thời gian khởi động hoặc ngưỡng chỉnh trên dev có thể khớp với cấu trúc 720/720 mà không ai cố ý.
  - 60 ca test có cùng cấu trúc, nên tách dev/test **không bắt được** lỗi này.
  - RE2-TT không có file nào không có lỗi, nên không làm được phép thử giả của MRP §6 mục 7.
- **Sửa tối thiểu (rẻ):**
  - M1 khai trước phép cắt tiền tố file với độ lệch cố định, chọn trước, không dựa vào nhãn. Kết quả phát hiện phải không đổi đáng kể khi đổi độ lệch.
  - Báo cáo ghi rõ báo động trên đoạn trước mốc **không** phải tỷ lệ báo sai khi vận hành.
  - Đánh giá phát hiện chính đặt ở P10. R-07 của P9a đã có yêu cầu lượt nền và onset.

### P3 — KHÔNG CHẶN: chưa gắn với WHY-02, và đánh giá GNN chưa có task nào nhận

- WHY-02 đã quyết (Q-36): đồ thị tham gia chấm điểm, **và** khoanh vùng, xếp hạng cũng chạy trên đồ thị.
- Kế hoạch ghi "không mặc định PageRank", còn M4 chỉ ghi "nối điểm thành xếp hạng". Nếu bước xếp hạng chỉ là sắp điểm thì phần "xếp hạng trên đồ thị" của WHY-02 không còn.
- **Sửa:** M1 chỉ rõ phép tính dùng cạnh ở mỗi đầu ra của DT18. Một cách rẻ (chưa kiểm): so "sắp theo điểm UV-1" với "PageRank cá nhân hóa khởi từ điểm UV-1". Phép so này cho ví dụ PageRank của cô một chỗ có phân xử. Nếu không làm thì trình Minh sửa WHY-02.

### P4 — KHÔNG CHẶN: M4 chưa có quy tắc rẽ hướng khai trước

- Kế hoạch ghi "ứng viên không hợp lệ thì sửa hoặc trình hướng khác như C2". C2 là hồi quy kiểu CIRCA, mà G2 đã thấy bất lợi trên dev (UV-8: 12 so với 12 trên 19 ca).
- Luật cứng 14 đòi tiêu chí xong phải nói kết quả nào dẫn tới lựa chọn nào.
- **Sửa:** M4 khai trước các nhánh, ví dụ:
  - Trung gian cho thấy điểm chuyển sang dịch vụ được gọi ở nhóm ca hỗ trợ và không làm hỏng ca đúng tương ứng: đi tiếp M5.
  - Có chuyển điểm nhưng hỏng ca đúng: xét cách gộp.
  - Không chuyển: trình hướng khác.
  - Không đòi phải thắng baseline ở bất kỳ nhánh nào.

### P5 — KHÔNG CHẶN cho nội dung, nhưng cần Minh quyết trước khi duyệt: cỡ task và lịch

- AGENTS §5 đang ghi "một task … làm xong trong **một phiên**", và §5a.4 bắt tách ngay khi viết SPEC. Yêu cầu gốc của Minh cũng đòi mỗi task có giờ công và lý do "vừa một phiên".
- Bản sửa bỏ cả hai, viện dẫn "đính chính mới nhất của Minh". Tôi không thấy nguyên văn đính chính đó, và DECISIONS chưa có dòng nào ghi lại.
- M4, M5, M11 có cỡ khó vừa một phiên.
- Điểm 3 của lượt phản biện trước (đặt P6 vào lịch còn lại tới G4 cuối tháng 11 và nộp ngày 30/12) chưa được đáp.

### P6 — KHÔNG CHẶN: M7 đặt sau M4–M5 tạo ra hai đường chạy

- M4 và M5 chạy qua "đường gọi tối thiểu". M7 mới dựng bộ chạy thật, rồi M8 muốn dùng lại kết quả M4–M5 "nếu mã không đổi". Nhưng chính M7 làm mã đổi.
- **Sửa:** dùng định dạng bản ghi P3 (`ban_ghi.py`, `danh_gia.py`) ngay từ M4. M7 chỉ còn phần cache và chạy ma trận.

### P7 — KHÔNG CHẶN: bộ baseline RCA tại báo động mới

- Phép tính "6 baseline, 240 lượt" có gồm MicroRank và TraceRCA, nhưng WHY-35 đã loại hai phương pháp này khỏi chế độ (b).
- Mục 8 của G2 còn ba điểm Minh chưa quyết, đều đổi bộ baseline P7: điểm 2 (nhánh tác giả TraceRCA), điểm 5 (TORAI bỏ log), điểm 6 (biến thể MicroRank).
- **Sửa:** đưa các điểm này vào danh sách quyết định của M1.

### Phần tôi đã kiểm và thấy đúng

- Chi phí T-035 khớp file: `thong-ke-do-thi.json#/cost` ghi 1.088,5 s (18,1 phút) và đỉnh RSS 2.412.781.568 byte (2,25 GiB).
- Các phép tính 104, 82, 448 và 240 đều đúng số học.
- N-Sigma đúng là chỉ điền giá trị từ quá khứ (`phat_hien.py:68–72`).
- Các file `cua_so.py`, `nezha.py`, `danh_gia.py`, `builder.py` có thật và đúng vai trò kế hoạch nêu.

## 4. Đề xuất cho bộ phát hiện (chưa kiểm)

| Phương án | Được | Mất |
|---|---|---|
| **A. Khuyến nghị:** giữ dữ liệu như hiện có; thêm phép cắt tiền tố (P2); thêm một baseline trace từ hồ sơ T-015; quyết rõ BOCPD; coi P10 là nơi đánh giá phát hiện chính | Rẻ, đúng giao thức, câu trả lời trung thực trước cô | Kết luận phát hiện trên dữ liệu công khai vẫn hẹp |
| B. Thêm một task kiểm GAIA/MicroSS (lựa chọn mà G1 từng đề xuất) | Có thể có dữ liệu bình thường liên tục, một hệ thứ ba, một bộ dữ liệu độc lập | Thêm ít nhất một task; dung lượng tải và giấy phép chưa biết, phải trình trước (luật cứng 8) |
| C. Xem lại phiên no-fault của Eadro | Dữ liệu đã có sẵn trên máy | T-023 còn mở các vấn đề đồng hồ và cách ghép (Q-83) |

Về thiết kế, bộ phát hiện P6 nên tránh đúng lỗi của N-Sigma: gộp nhiều cột bằng phép OR làm báo động dày đặc. Ứng viên cho M1: gộp điểm có kiểm soát số phép thử, kèm luật "kéo dài k cửa sổ" (chưa kiểm).

## 5. Khả thi

Đây là ước lượng từ nhịp các chặng trước, chưa kiểm:
- Đường găng có khoảng 10 bước nối tiếp: M1 → M2/M3 → M4 → M5 → M6 → M7 → M8/M9 → M10 → M11 → M12.
- P3–P4 mất khoảng 10 ngày (05–14/10), P5 khoảng 5 ngày (14–18/10).
- Nếu mỗi bước cần 1–2 ngày kể cả phản biện, G3 rơi vào khoảng đầu đến giữa tháng 11. G4 cuối tháng 11 chỉ giữ được khi không phải đổi hướng lớn sau M4 và kích hoạt không quá 2–3 nhánh có điều kiện.
- Có thể rút ngắn bằng cách chia Claude/Codex làm song song M2 ‖ M3, M6 ‖ M5 (sau M4) và M8 ‖ M9.

## 6. Cần Minh quyết

1. **Phát hiện trên dữ liệu công khai:** A, B hay C ở mục 4? Tôi khuyến nghị A.
2. **Bộ baseline phát hiện:** có thêm bộ dùng trace không? BOCPD chạy bản nhân quả (tốn EC2) hay chỉ giữ số lịch sử?
3. **Cỡ task:** giữ quy tắc "một task một phiên" của AGENTS §5, hay đổi? Nếu đổi thì phải ghi vào AGENTS và DECISIONS theo Luật 0.
4. **Lịch:** có giữ mốc G4 cuối tháng 11 (Q-70) để kế hoạch tự xếp vào không?

## Báo cáo lượt

1. **Đã làm:**
   - Đọc MRP, DT18, hướng dẫn của cô, WHY-02/07/10/35, DECISIONS Q-61–Q-89 và Q-149–Q-176.
   - Đọc `goi-g2.md` (§0, §2.5–2.9, G2-H20–H26, §5–§8), `ban-giao-p6.md`, `yeu-cau-quan-sat-p9.md`, `the-rcaeval.md`, `goi-g1.md`.
   - Đọc yêu cầu gốc của Minh, kế hoạch bản 1 và phản biện bản 1 trong thư mục attachments.
   - Đọc mã `phat_hien.py`, `danh_gia.py`.
2. **File thay đổi:** không sửa file nào.
3. **Kiểm đã chạy:**
   - Kiểm chi phí T-035 bằng con trỏ JSON: khớp.
   - Tính lại số học các ma trận: đúng.
   - Grep DECISIONS và AGENTS: không có dòng nào đổi quy tắc "một phiên" hay nhắc 16 giờ/tuần.
   - Không chạy thực nghiệm, không mở dữ liệu khóa.
4. **Còn mở:**
   - Tôi chưa thấy nguyên văn "đính chính mới nhất" mà Codex viện dẫn, nên P5 có thể đổi khi thấy văn bản đó.
   - Đề xuất ở mục 4 và quy tắc rẽ hướng ở P4 đều chưa kiểm.
   - **Đề xuất:** tiếp tục phản biện, vì còn hai điểm CHẶN chưa được người lập đáp.

---

## Prompt cho Codex (người lập kế hoạch) đáp phản biện

Khi gửi, Minh đính kèm nguyên văn kế hoạch sửa đổi và nguyên văn toàn bộ câu trả lời phản biện này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch phân rã P6 sửa đổi (12 task chính, 11 task có điều kiện), Minh gửi kèm nguyên văn trong chat; chưa có file kế hoạch chính thức.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex phiên lập kế hoạch là người làm; Claude là người phản biện lượt kế hoạch sửa đổi này theo yêu cầu Minh. Phân công chỉ áp dụng lượt kế hoạch, không tự áp sang các task sau.
- Tài liệu gốc: nguyên văn yêu cầu ban đầu của Minh (C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt); nguyên văn yêu cầu đính chính mới nhất của Minh; toàn bộ kế hoạch sửa đổi gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước, theo thời gian: kế hoạch bản 1 (C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt); phản biện bản 1 (C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt); kế hoạch sửa đổi; bản phản biện của Claude cho kế hoạch sửa đổi, Minh gửi kèm nguyên văn. Nếu chuyển máy, dùng nguyên văn Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-034/goi-g2.md; results/T-035/ đến results/T-040/; các nguồn kết quả mà kế hoạch và bản phản biện dẫn; manifest hiện hành tương ứng. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s10"></a>

### S10 — Codex đáp và đề xuất sửa tiếp

<details>
<summary>Mở nguyên văn S10</summary>

````text
**Tôi đồng ý chưa nên duyệt nguyên trạng kế hoạch 12 + 11.** Kế hoạch của tôi còn thiếu căn cứ ở phần phát hiện, chưa xử lý đầy đủ nguy cơ từ biên file, và đã tính phạm vi baseline chế độ (b) rộng hơn phần được duyệt.

Tuy nhiên, tôi không đồng ý tiếp nhận nguyên trạng mọi cách sửa của reviewer. Đặc biệt: chưa đủ căn cứ để bắt buộc PageRank, chuyển đánh giá phát hiện chính sang P10, hoặc yêu cầu Minh quyết lại cách hiểu “một phiên”.

Đây là phản hồi của **người lập kế hoạch**, chỉ trong chat. Những điểm về thiếu tiêu chí vận hành và thiếu giả thuyết riêng cho bộ phát hiện đã được tôi nhận ra ở lượt trước. Các điểm mới dưới đây được kiểm sau khi đọc bản phản biện; tôi không gọi đó là một lượt tự soát độc lập trước phản biện.

**Kết quả đối chiếu từng điểm**

| Điểm | Phản hồi của tôi | Phần cần sửa hoặc giữ lại |
|---|---|---|
| **P1 — Baseline phát hiện mỏng** | **Đúng về cốt lõi; CHẶN việc duyệt bộ so sánh và kết luận bộ phát hiện có ưu thế.** Nhưng “gần như chắc thắng” và “thắng không chứng minh gì” đều quá mạnh. | M1 phải xác định từng phép so nhằm kiểm điều gì, lựa chọn baseline cạnh tranh và đối chứng cùng tín hiệu. Thêm một tên phương pháp chưa giải quyết đủ vấn đề. |
| **P2 — Biên file tiết lộ mốc tiêm** | **Đúng về nguy cơ và khoảng trống giao thức; chưa phải bằng chứng P6 đã khai thác rò nhãn.** CHẶN việc coi giao thức hiện tại đã đủ cho kết luận tự phát hiện. | Bổ sung phép kiểm phụ thuộc biên file và thời gian từ lúc khởi động. Điều chỉnh đề xuất cắt tiền tố; không đòi kết quả bất biến khi đã thay lượng lịch sử đầu vào. |
| **P3 — Xếp điểm chưa đáp ứng WHY-02** | **Đúng một phần.** Cần chỉ rõ quan hệ tham gia mỗi đầu ra. **Không đồng ý** rằng sắp điểm đã tính từ đồ thị thì mặc nhiên không còn là xếp hạng dựa trên đồ thị. | M1/M4 phải làm rõ đường tính và phép đối chứng. Không bắt buộc thêm PageRank hoặc sửa WHY-02 chỉ vì bước cuối là sắp điểm. |
| **P4 — Thiếu quy tắc rẽ hướng** | **Đúng.** Đây là thiếu sót trong tiêu chí kết thúc lượt thử phương pháp. | Phân biệt lỗi cài đặt, thiếu thông tin quan sát, giả thuyết bị bác bỏ và kết quả chưa phân xử. Không tự chuyển sang C2 hoặc tiếp tục chỉnh để cứu ứng viên. |
| **P5 — Cỡ task và lịch** | **Không còn đúng ở phần yêu cầu Minh quyết lại.** Reviewer chưa có nguyên văn chỉ dẫn mới nhất của Minh. | Áp dụng đính chính đã có trong chat. Không ghi DECISIONS, không yêu cầu sửa AGENTS, chưa lập lịch theo giờ/tuần. Độ phức tạp của M4/M5/M11 vẫn phải được đánh giá, nhưng hiện chưa đo được lượng công việc của agent. |
| **P6 — Hai đường chạy** | **Đúng một phần.** Cách viết của tôi chưa bảo đảm đường thử ban đầu và đường chạy ma trận dùng chung phần tính toán, bản ghi và bộ chấm. | Dùng các thành phần P3 phù hợp ngay từ M4/M5. M7 mở rộng điều phối và cache. Chỉ chạy lại kết quả bị ảnh hưởng bởi thay đổi tính toán hoặc giao thức. |
| **P7 — 240 lượt RCA tại báo động mới** | **Đúng về việc mở rộng phạm vi chưa được giải thích. Tôi coi đây là điểm CHẶN việc duyệt ma trận M11.** | Lập rõ bảng baseline hiện hành và từng mở rộng được đề xuất. Không coi MicroRank/TraceRCA đã được duyệt cho chế độ (b). |

Có bốn vấn đề cần giải thích kỹ hơn để tránh sửa kế hoạch theo một cách vẫn thiếu căn cứ.

**1. Bộ phát hiện cần được thiết kế và đánh giá như một câu hỏi nghiên cứu riêng.**

Lo ngại của Minh vẫn có cơ sở. Nhưng phải diễn đạt đúng số liệu: mức khoảng **1.168 cờ/giờ** của N-Sigma là cờ thô trên đoạn trước tiêm được giao thức coi là bình thường. Sau thời gian trơ, mức thông báo tương ứng là khoảng **13,35 thông báo/giờ**. Cả hai đều đáng lo, nhưng khác đơn vị và **chưa phải tỷ lệ báo sai trên vận hành bình thường đã được xác minh**.

Nguồn: [phat-hien.json](/D:/RCA-flashticket/results/T-025/phat-hien.json), con trỏ `#/bo_phat_hien/nsigma/tong_hop/co_dieu_kien_tren_ca_OK`, các trường `bao_dong_sai_moi_gio` và `thong_bao_sai_moi_gio`. Tôi đã kiểm hash qua nguồn ghim trong gói G2.

M1 cần phân biệt ba mục đích so sánh:

| Mục đích | So sánh cần có |
|---|---|
| Bộ mới có hơn cách phát hiện thực dụng, đủ cạnh tranh không? | Baseline nhân quả được lựa chọn và hiệu chỉnh hợp lệ, với tiêu chí cảnh báo phù hợp. N-Sigma và BOCPD lịch sử vẫn có giá trị tham chiếu, nhưng chưa đủ cho toàn bộ kết luận này. |
| Lợi ích đến từ thêm trace hay từ dùng quan hệ? | Đối chứng giữ cùng tín hiệu, lịch sử và chính sách cảnh báo, chỉ thay phần sử dụng quan hệ cần kiểm. |
| Bộ mới có dùng được trong hệ thống thật không? | Đo cảnh báo sai theo sự kiện, khả năng phát hiện, độ trễ, thời gian duy trì cảnh báo, khả năng trở về trạng thái bình thường và chi phí trên dữ liệu có nền được xác minh. |

Tôi đồng ý đưa **baseline dùng trace vào phần thẩm định của M1**. Nhưng hồ sơ T-015 không có nghĩa đã có sẵn một bộ tự phát hiện hoàn chỉnh để cắm vào:

- Luật theo span của TraceRCA/RCAEval cần một mốc chia dữ liệu tham chiếu và hiện tại. Chuyển sang tự phát hiện phải định nghĩa cách tạo nền nhân quả và cách gộp thành cảnh báo hệ thống. Đó là công việc thiết kế cần khai rõ. Xem [hồ sơ detector trace](/D:/RCA-flashticket/results/T-015/ho-so-phat-hien-trace.md:11).
- MicroRank gốc dùng điều kiện `frontend` cùng `span.kind=server` để tính độ trễ request. Schema RE2 đã khảo sát không cung cấp đầy đủ trường này. Thay bằng quy tắc khác phải gọi đúng là biến thể. Tôi đã đối chiếu lại [code tiền xử lý chính thức tại revision đã ghim](https://raw.githubusercontent.com/IntelligentDDS/MicroRank/efd85e8e6f0fad30f6f8aaf0555e3324d8f5f982/preprocess_data.py).
- Luật cảnh báo và luật phân nhóm trace cho RCA trong MicroRank cũng khác nhau. Không thể coi chúng là một giao diện thống nhất chỉ vì cùng dùng mean/std. [Code detector chính thức](https://raw.githubusercontent.com/IntelligentDDS/MicroRank/efd85e8e6f0fad30f6f8aaf0555e3324d8f5f982/anormaly_detector.py).

Với GDN, tôi nhận thiếu sót chưa giao việc đánh giá rõ ràng cho M1. Tuy nhiên, cần tách **xét GDN làm baseline** khỏi **tự xây biến thể GNN của phương pháp**. [WHY-10](/D:/RCA-flashticket/docs/WHY.md:99) quy định điều kiện cho việc thứ hai; không nên dùng máy móc để loại một baseline đối lập đáng xét.

Quan trọng hơn, **UV-1 hiện chủ yếu cung cấp căn cứ cho giả thuyết RCA**: quan hệ gọi có thể giúp đặt chứng cứ vào đúng dịch vụ. Nó chưa tự chứng minh bộ phát hiện sẽ bớt báo sai. Ví dụ, nếu chỉ chuyển cùng các giá trị điểm sang tên dịch vụ khác, giá trị lớn nhất toàn hệ thống vẫn không đổi. Khi đó thứ hạng RCA có thể đổi, còn quyết định cảnh báo không đổi.

Vì vậy, kế hoạch sửa phải yêu cầu **một giả thuyết riêng về cách quan hệ cải thiện việc phân biệt bất thường với biến động bình thường**, cùng phép thử có thể bác bỏ nó. Thêm luật “kéo dài k cửa sổ” chỉ là ứng viên xử lý cảnh báo; phải đo cả cái giá về bỏ sót và chậm phát hiện.

**2. Cách xử lý biên file của reviewer chưa đủ để kết luận đã hết nguy cơ.**

Tôi tính lại từ [bảng khảo sát gốc T-002](/D:/RCA-flashticket/results/T-002/local-inspection/run-002/case-summary.csv), sau khi kiểm hash: **30/30 ca RE2-TT trong bảng có biên metric ở ±720 giây quanh mốc tiêm**. Đây là bằng chứng về các ca đã khảo sát; lượt này không đọc tập khóa để xác nhận thêm.

Nếu cắt cùng một lượng đầu file cho mọi ca, sự cố vẫn xuất hiện tại một vị trí cố định mới. Cách đó chưa loại được nguy cơ học theo thời gian từ lúc khởi động.

Tôi đề xuất tách hai phép kiểm, đều **chưa thực hiện**:

- **Giữ nguyên lịch sử được phép nhìn thấy:** thay phần tương lai hoặc thông tin đóng gói file; đầu ra tại thời điểm đang xét phải không phụ thuộc những phần đó.
- **Thay thời điểm bắt đầu quan sát theo quy tắc khai trước, không chọn bằng nhãn:** đo độ nhạy trên phần thời gian có thể đối chiếu, sau thời gian khởi động hợp lệ. Vì lượng lịch sử đã đổi, kết quả có thể thay đổi hợp lý; phải phân biệt thay đổi đó với việc bám theo vị trí sự cố trong file.

Các phép này kiểm nguy cơ cụ thể. **Chúng không tạo ra dữ liệu bình thường liên tục hoặc nhãn bắt đầu biểu hiện sự cố vốn đang thiếu.**

Tôi chưa tiếp nhận đề xuất “đánh giá phát hiện chính đặt ở P10” như một quyết định. P10 cần cung cấp bằng chứng vận hành thật, nhưng không vì thế mà tự giảm nghĩa vụ đánh giá công khai ở P7. Ba hướng A/B/C của reviewer có thể bổ sung cho nhau; cần chọn theo khoảng trống bằng chứng, không nhất thiết chọn đúng một phương án.

**3. Vai trò đồ thị phải được chứng minh bằng đường tính, không bằng tên thuật toán.**

Nếu điểm được tính bằng \(s=f(X,E)\), trong đó \(E\) là quan hệ, thì thứ hạng \(\operatorname{argsort}(s)\) có thể phụ thuộc vào quan hệ. Bước sắp xếp cuối không cần thêm một thuật toán đồ thị nữa mới có sự phụ thuộc đó.

Điều cần kiểm là:

- Quan hệ đã làm thay đổi thông tin hay phép tính nào?
- Thay quan hệ trong khi giữ phần còn lại tương đương có làm thay đổi điểm và thứ hạng theo giả thuyết không?
- Thay đổi ấy giúp ở điều kiện nào và làm hại ở điều kiện nào?

Đây phù hợp với nội dung [WHY-02](/D:/RCA-flashticket/docs/WHY.md:25). PageRank vẫn có thể là ứng viên nếu giải quyết một câu hỏi cụ thể; **chưa có căn cứ để bắt buộc thêm nó chỉ nhằm khớp cách diễn đạt “xếp hạng trên đồ thị”.**

Tôi cũng không tiếp nhận kết luận rằng TT gần hết khả năng cải thiện, nên OB phải là nơi chính để chứng minh thành công. Điểm top-1 cao trên TT chỉ nói về độ đo và phạm vi đã chạy. Baseline yếu trên OB không bảo đảm UV-1 hữu ích, nhất là với lỗi không tạo ra biểu hiện chậm như giả thuyết dự kiến.

Các số vị trí tín hiệu trong UV-1 là **bằng chứng chẩn đoán để đề xuất thử**, không phải chất lượng của bộ RCA mới. Dev có thể cung cấp bằng chứng thăm dò để chọn thiết kế; P7 mới kiểm khả năng giữ được kết quả sau khi khóa thiết kế.

**4. Tôi sửa đề xuất tổ chức công việc như sau, chưa ghi thành file.**

| Phần kế hoạch | Nội dung cần bổ sung hoặc sửa |
|---|---|
| **M1 — Thiết kế và giao thức** | Tách giả thuyết phát hiện/RCA; giao rõ việc chọn baseline, đánh giá GDN, xử lý biên file, xác định độ đo vận hành và khoảng trống dữ liệu. Phân biệt baseline hiện hành, biến thể và đối chứng. |
| **M4/M5 — Cài đặt và thử phương pháp sớm** | Dùng phần tính toán, bản ghi và bộ chấm thống nhất ngay từ đầu. Có quy tắc rẽ hướng theo bằng chứng, gồm cả kết quả bác bỏ ứng viên. |
| **M7 — Chạy ma trận** | Mở rộng điều phối, cache và khả năng tái lập từ đường chạy đã dùng. Thay đổi điều phối không mặc nhiên làm mất giá trị mọi kết quả cũ. |
| **M10 — Phân xử và lựa chọn** | Tách lợi ích do tín hiệu, quan hệ và chính sách cảnh báo. Không chọn cấu hình chỉ vì tăng chênh lệch đồ thị trừ không đồ thị. |
| **M11 — So sánh cuối trên dev** | Tính lại ma trận sau khi phạm vi baseline được xác định. Không giữ 240 lượt như khối lượng mặc định. |
| **M12 — Bàn giao G3** | Nêu rõ kết luận nào được dev hỗ trợ, kết luận nào chờ P7/P10 và dữ liệu nào còn thiếu. |

Quy tắc rẽ hướng ở M4/M5 nên phân biệt ít nhất các tình huống sau:

- **Cài đặt hoặc phép kiểm trung gian sai:** sửa phần đó; chưa kết luận giả thuyết sai.
- **Đầu vào đủ, cài đặt đúng nhưng dự đoán không xuất hiện:** bác bỏ hoặc thu hẹp giả thuyết theo bằng chứng.
- **Có lợi ở nhóm hỗ trợ nhưng làm hỏng nhóm đối chiếu:** phân xử nguyên nhân và đánh đổi; không tự mặc định “chỉnh cách gộp là được”.
- **Thiếu chứng cứ quan sát cần thiết:** giữ nhóm ca trong báo cáo, nêu giới hạn và yêu cầu quan sát; không loại nhóm khó.
- **Bằng chứng bước đầu phù hợp:** tiếp tục đánh giá dev đầy đủ, chưa coi là thành công cuối.

C2 không phải nhánh cứu mặc định. Muốn thử hồi quy có điều kiện sau kết quả bất lợi đã có, phải nêu **điều gì thực sự thay đổi và phép thử nào phân xử được giải thích mới**.

Về M11, [WHY-35](/D:/RCA-flashticket/docs/WHY.md:343) hiện chọn BARO, CIRCA kiến trúc và TORAI cho chế độ (b). Với cách đếm cũ của tôi, riêng ba phương pháp này tương ứng tối đa:

\[
30\times(1+1+3)=150\text{ lượt}
\]

cho **một cấu hình detector**, nếu các ca đều tạo được mốc cần chạy. Thêm SimpleRCA sẽ là một mở rộng cần nêu rõ; thêm MicroRank/TraceRCA còn cần làm rõ giao thức và biến thể. Không được suy “adapter nhận được mốc thời gian” thành “đã được duyệt và kiểm hợp lệ”.

Reviewer cũng nói rộng hơn nguồn ở một chỗ: điểm TORAI bỏ log trong [G2 §8](/D:/RCA-flashticket/results/T-034/goi-g2.md:897) đề xuất **dòng độ nhạy, ghi rõ không đổi baseline**. Nó không cùng trạng thái với việc chọn nhánh tác giả TraceRCA hoặc biến thể MicroRank làm baseline mới.

Những thay đổi trên **không tự sinh thêm một task cho mỗi finding**. Chúng sửa nội dung và phụ thuộc của các module. Số task chỉ được chốt lại khi biết baseline nào thực sự phải cài, phần nào dùng lại và nhánh nào được kích hoạt; tôi không bảo vệ con số 12 + 11 bằng mọi giá.

Riêng P5, Minh đã nói rõ:

> “không ghi vào desision, không quan tâm đến số giờ của tôi vội, tôi cần bạn lập plan chia task trước.”

Cùng với đính chính về thời gian máy chạy, phiên làm việc và nén ngữ cảnh, chỉ dẫn này đủ để áp dụng trong lượt hiện tại. **Không cần Minh duyệt lại chính điều Minh vừa yêu cầu.** Tôi cũng không nhận ước lượng “1–2 ngày mỗi bước” của reviewer làm lịch khả thi đã có căn cứ.

**Báo cáo lượt**

1. **Đã làm:** đối chiếu bảy điểm phản biện với nguồn, code và kết quả; nêu phần nhận, phần phản bác và đề xuất sửa kế hoạch.
2. **File thay đổi:** không sửa file nào; không ghi DECISIONS, không chạy thực nghiệm, không mở dữ liệu khóa.
3. **Kiểm tra:** hồ sơ T-015, gói G2, nguồn số phát hiện và bảng khảo sát biên file khớp hash tương ứng. Thẻ T-002 lệch snapshot bàn giao cũ do có đợt sửa được ghi trong LOG; tôi dùng bảng gốc khớp hash để kiểm số. Trạng thái Git cuối lượt giống đầu lượt.
4. **Còn mở:** bộ baseline cuối, giả thuyết phát hiện và phạm vi bằng chứng vận hành. Các đề xuất sửa chưa phải kết quả đã kiểm. Tôi đề xuất **tiếp tục phản biện phần đáp này**, vì những vấn đề chặn duyệt kế hoạch chưa được giải quyết bằng một thiết kế cụ thể đã thống nhất.

Prompt để Minh chuyển cho Claude, kèm nguyên văn đính chính của Minh, kế hoạch 12 + 11 và phản hồi trên:

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch phân rã P6 sửa đổi và phản hồi của người lập kế hoạch, Minh gửi kèm nguyên văn trong chat; chưa có file kế hoạch chính thức.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex là người lập kế hoạch; Claude là người phản biện lượt kế hoạch này. Phân công chỉ áp dụng đề xuất kế hoạch.
- Tài liệu gốc: nguyên văn yêu cầu ban đầu tại C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; nguyên văn yêu cầu đính chính và yêu cầu về bộ phát hiện của Minh gửi kèm; toàn bộ kế hoạch sửa đổi gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước: kế hoạch bản 1 tại C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt; phản biện bản 1 tại C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt; kế hoạch sửa đổi gửi kèm; phản biện kế hoạch sửa đổi tại C:/Users/84583/.codex/attachments/ca11a615-a65e-4a57-bb7b-1489b6adf748/Pasted text.txt; phản hồi mới nhất của Codex gửi kèm nguyên văn. Nếu chuyển máy, dùng nguyên văn Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-002/; results/T-015/; results/T-025/; results/T-034/ đến results/T-040/; các nguồn kết quả được kế hoạch, phản biện và phản hồi dẫn; manifest tương ứng và lịch sử bàn giao trong LOG. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s11"></a>

### S11 — Kiểm lại trước bản hợp nhất 3

<details>
<summary>Mở nguyên văn S11</summary>

````text
Tôi đã kiểm xong các số Codex dẫn (đều khớp). Giờ đọc phần detector MicroRank gốc rồi lập bản kiểm lại.

## Kết luận

Phản hồi của Codex **đúng ở phần lớn các điểm**. Tôi nhận năm chỗ lượt trước của tôi nói quá hoặc sai. Hai bên đã thống nhất hướng sửa cho hai điểm CHẶN cũ (P1, P2). Nhưng hiện chưa có một bản kế hoạch hợp nhất ghi các hướng sửa đó. Ngoài ra còn **một điểm CHẶN mới**: việc cài baseline phát hiện chưa có task nào nhận.

## 1. Số và nguồn Codex dẫn: đều khớp file

| Khẳng định của Codex | Kết quả kiểm |
|---|---|
| N-Sigma: 1.167,7 cờ thô/giờ, 13,35 thông báo/giờ | Khớp `results/T-025/phat-hien.json#/bo_phat_hien/nsigma/tong_hop/co_dieu_kien_tren_ca_OK`. BOCPD ở cùng chỗ: 23,87 cờ thô và 6,34 thông báo/giờ |
| 30/30 ca RE2-TT có biên metric đúng ±720 s quanh mốc tiêm | Khớp: tính từ `results/T-002/local-inspection/run-002/case-summary.csv` ra một nhóm duy nhất (720, 720), gồm 30 ca |
| Luật span của RCAEval cần mốc chia nền/hiện tại, không tự phát hiện được | Khớp `results/T-015/ho-so-phat-hien-trace.md` §A.1 |
| Bộ phát hiện MicroRank gốc cần span `frontend` có `span.kind=server`; RE2 thiếu tag này | Khớp cùng file §B.1 |
| Chế độ (b) chỉ gồm BARO, CIRCA, TORAI; TORAI ít nhất 3 seed, nên 30×(1+1+3)=150 lượt | Khớp WHY-35 (`docs/WHY.md:344`) và WHY-19/20 |
| Điểm 5 ở mục 8 G2 chỉ là dòng độ nhạy, "không đổi baseline" | Khớp `goi-g2.md` §8 điểm 5 |

## 2. Từng điểm cũ: kết luận

| Điểm | Kết luận | Lý do |
|---|---|---|
| **P1** baseline phát hiện | Codex **đúng**. Tôi sai ở hai chỗ | (a) Tôi viết "1.168 lần mỗi giờ bình thường" mà không nói đó là cờ thô trên đoạn mà nhãn proxy coi là bình thường. (b) "Gần như chắc thắng, thắng không chứng minh gì" là nói quá. (c) Tôi gộp sai việc xét GDN làm baseline (Q-62) với việc tự làm biến thể GNN (WHY-10). **Vẫn CHẶN** cho tới khi bản kế hoạch có ba mục đích so sánh mà Codex nêu |
| **P2** biên file | Codex **đúng**, và hai phép kiểm Codex đề xuất tốt hơn đề xuất của tôi | Đổi độ lệch thì lượng lịch sử cũng đổi, nên không thể đòi kết quả bất biến. Chỉ thêm một chi tiết: độ lệch nên **khác nhau giữa các ca trong cùng một lượt**, khai trước bằng seed và không dùng nhãn. Nếu mọi ca cùng một độ lệch, sự cố lại nằm ở một vị trí cố định mới. **Vẫn CHẶN** cho tới khi M1 ghi phép này |
| **P2b** "P10 là nơi đánh giá phát hiện chính" | Codex **đúng** | P7 vẫn phải trả lời RQ3a trên dữ liệu công khai, kèm giới hạn. P10 bổ sung bằng chứng vận hành. Ba hướng A, B, C có thể dùng cùng nhau |
| **P3** WHY-02 / PageRank | **Đúng một phần, cho cả hai bên** | Tôi không bắt buộc PageRank: lượt trước ghi "một cách rẻ… nếu không làm thì trình Minh sửa WHY-02". Lập luận `argsort(f(X,E))` của Codex hợp lý. Phần còn lại nằm ở MRP P6 tầng 4: phải chọn cách xếp hạng "theo MRR của chính tầng này", và mỗi lựa chọn phải ghi "đã xét phương án nào". **Sửa tối thiểu:** M1 ghi bước sắp điểm là một lựa chọn của tầng 4, kèm phương án đã xét và lý do; báo cáo cho cô nói thẳng đồ thị vào thứ hạng qua bước chấm điểm. KHÔNG CHẶN, nên đóng điểm này |
| **P4** quy tắc rẽ hướng | Codex **đúng**; năm tình huống Codex nêu là đủ | Thêm một chi tiết: phát hiện và RCA cần **hai bộ quy tắc riêng** (xem N2 bên dưới) |
| **P5** cỡ task và lịch | Codex **đúng cho lượt lập kế hoạch** | Lời Minh "không quan tâm đến số giờ… lập plan chia task trước" đã đủ cho lượt này. Tôi không thấy nguyên văn đính chính về "phiên và nén ngữ cảnh" trong các file đính kèm, nên không kiểm được phần đó. Khi viết SPEC từng task, AGENTS §5 và §5a vẫn áp dụng. Rút điểm này |
| **P6** hai đường chạy | Codex **đúng một phần**; hướng sửa đạt | — |
| **P7** 240 lượt | Codex **đúng**. Tôi nói quá về điểm 5 ở mục 8 G2 | — |

**Tôi tự đính chính thêm một câu của lượt trước.** Tôi viết "ở TT gần như không còn chỗ để tăng". Câu này chỉ đúng với Hit@1 ở chế độ (a). Ở chế độ (b) trên chính TT, thành công chung cao nhất chỉ 0,067 (`goi-g2.md` §2.6). Vậy **chỗ cải thiện lớn nhất trên TT là cả chuỗi phát hiện rồi xếp hạng**. Codex cũng đúng khi bác ý "OB là nơi chính": baseline yếu không bảo đảm UV-1 giúp được.

## 3. Điểm mới

### N1 — CHẶN việc duyệt kế hoạch như đã phân rã đủ: chưa có task nào cài baseline phát hiện

- **Ở đâu:** bảng sửa M1–M12 trong phản hồi. M1 "thẩm định" baseline, M11 "chạy phần thiếu". Không task chính hay nhánh có điều kiện nào nhận việc **cài và kiểm** các bộ phát hiện mà M1 chọn. Chỉ có C8 nhận BOCPD.
- **Bằng chứng:** chính Codex xác nhận cả hai bộ phát hiện trace đều cần thiết kế thêm:
  - Luật span cần mốc chia.
  - MicroRank cần một biến thể cho phần chọn span đầu.
  - GDN cần đoạn nền học được mà không dựa vào mốc tiêm.
  - Kiểm tập dữ liệu phát hiện bổ sung (Q-69, hướng B) cần tải và lập thẻ.
  
  Yêu cầu gốc của Minh ghi: "Công việc phụ thuộc kết quả chưa có: phải có nhánh xử lý, task phụ thuộc dự kiến và tác động chi phí", và cấm dồn phần cài đặt vào task cuối.
- **Hậu quả:** phần cài này sẽ âm thầm dồn vào M11. Đó đúng là lỗi bản 1 bị phản biện.
- **Sửa tối thiểu:** thêm nhánh có điều kiện, mỗi nhánh có điều kiện kích hoạt từ M1 và đặt trước M11, chạy được song song với M4–M6:
  - cài baseline phát hiện dùng trace;
  - GDN làm baseline;
  - kiểm dataset phát hiện bổ sung (Q-69).

### N2 — KHÔNG CHẶN: phát hiện chưa có cơ chế ứng viên nào dùng quan hệ để đổi quyết định báo động

- Nhận xét của Codex đúng và quan trọng. UV-1 chỉ chuyển điểm giữa các nút, nên mọi phép gộp đối xứng (max, tổng) ở mức hệ thống không đổi.
- Hệ quả: hiện tầng phát hiện có dùng đồ thị ở điểm của từng phần tử, nhưng **không có ứng viên nào để đồ thị đổi quyết định báo động**. Nếu M1 không tìm được ứng viên, kết quả hợp lệ là "đồ thị không đổi quyết định phát hiện". Kế hoạch phải cho phép kết luận này và báo trung thực.
- Ứng viên để M1 xét, **chưa kiểm**:
  - **(a) Thống kê quét trên đồ thị con liên thông.** Báo động khi một vùng liên thông các phần tử lệch vượt ngưỡng, thay cho phép OR độc lập từng cột. Phép OR này chính là chỗ N-Sigma hỏng (G2-H22). Đây cũng là chỗ đặt ví dụ "subgraph anomaly detection" của cô vào phần phát hiện.
  - **(b) Giảm phần bất thường kế thừa dọc chuỗi gọi trước khi gộp.**
  - Cả hai đều làm đổi được giá trị gộp. Cả hai đều phải đo cái giá: bỏ sót và chậm phát hiện.
- Bộ phát hiện MicroRank gốc dùng quan hệ cha–con để tính thời gian tự xử lý (`ho-so-phat-hien-trace.md` §B.2). Vì vậy nó là đối thủ đúng loại cho câu "phát hiện có dùng cấu trúc". Muốn dùng nó trên RE2 phải làm bản biến thể ở phần chọn span đầu (N1).

## 4. Đề xuất

**Tiếp tục, nhưng đổi cách làm.** Bất đồng thật còn lại nhỏ: chỉ còn cách hiểu WHY-02 ở P3, và tôi đề xuất đóng. Việc còn thiếu là một văn bản. Codex nên viết **bản kế hoạch hợp nhất (bản 3)** chứa:
- các sửa đã thống nhất cho P1, P2, P4, P6, P7;
- N1 và N2;
- bảng baseline phát hiện và RCA hiện hành tách khỏi các phần mở rộng đề xuất.

Sau đó soát một lượt cuối rồi dừng. Tranh luận thêm từng điểm trong chat không thêm bằng chứng.

**Minh cần quyết** (Codex đã đề nghị nêu trong M1): có mở hướng B, tức kiểm GAIA/MicroSS theo Q-69, không. Hướng này tốn ít nhất một task, và dung lượng tải phải trình trước theo luật cứng 8.

## Báo cáo lượt

1. **Đã làm:**
   - Kiểm sáu khẳng định của Codex trên file thật.
   - Kết luận từng điểm P1–P7, tự đính chính năm chỗ của lượt trước.
   - Nêu hai điểm mới N1, N2.
2. **File thay đổi:** không sửa file nào.
3. **Kiểm đã chạy:**
   - Đọc con trỏ JSON trong `phat-hien.json`.
   - Tính biên file từ `case-summary.csv`.
   - Đọc T-015 §A và §B, WHY-19/20/35.
   - Tìm trong `pasted-text-attachments.json`: không thấy nguyên văn đính chính về phiên và nén ngữ cảnh.
   - Không chạy thực nghiệm, không mở dữ liệu khóa.
4. **Còn mở:**
   - N1 (CHẶN) chưa xử lý.
   - Cơ chế phát hiện dùng đồ thị (N2) mới là ứng viên.
   - Quyết định Q-69 thuộc về Minh.
   - Mọi đề xuất ở đây đều chưa kiểm.

---

## Prompt cho Codex đáp phản biện

Khi gửi, Minh đính kèm nguyên văn kế hoạch 12 + 11, phản hồi mới nhất của Codex và toàn bộ câu trả lời này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch phân rã P6 sửa đổi và phản hồi của người lập kế hoạch, Minh gửi kèm nguyên văn trong chat; chưa có file kế hoạch chính thức.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex là người lập kế hoạch; Claude là người phản biện lượt kế hoạch này. Phân công chỉ áp dụng đề xuất kế hoạch.
- Tài liệu gốc: nguyên văn yêu cầu ban đầu tại C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; nguyên văn yêu cầu đính chính và yêu cầu về bộ phát hiện của Minh gửi kèm; toàn bộ kế hoạch sửa đổi gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước, theo thời gian: kế hoạch bản 1 tại C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt; phản biện bản 1 tại C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt; kế hoạch sửa đổi gửi kèm; phản biện kế hoạch sửa đổi tại C:/Users/84583/.codex/attachments/ca11a615-a65e-4a57-bb7b-1489b6adf748/Pasted text.txt; phản hồi của Codex gửi kèm nguyên văn; bản kiểm lại phản hồi của Claude gửi kèm nguyên văn. Nếu chuyển máy, dùng nguyên văn Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-002/; results/T-015/; results/T-018/; results/T-021/; results/T-025/; results/T-034/ đến results/T-040/; các nguồn kết quả được kế hoạch, phản biện và phản hồi dẫn; manifest tương ứng và lịch sử bàn giao trong LOG. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s12"></a>

### S12 — Kế hoạch hợp nhất lần 3: 13 + 15

<details>
<summary>Mở nguyên văn S12</summary>

````text
**Tôi nhận N1: kế hoạch trước thiếu nơi cài và kiểm baseline phát hiện. Tôi hợp nhất kế hoạch ngay dưới đây, thay vì tiếp tục chỉ liệt kê những chỗ cần sửa.**

Bản này có **13 task chính và 15 task có điều kiện**. Đây là đề xuất phân công công việc, chưa phải 28 task đều phải thực hiện, chưa chọn thuật toán và chưa cấp quyền sửa file.

**Về phản biện mới, có ba điểm cần chốt cách hiểu.**

- **N1 đúng, chặn việc coi bản trước đã phân rã đủ.** Bản này bổ sung M6 cho baseline phát hiện; C12 cho GDN; C13–C14 cho khảo sát và sử dụng dữ liệu bổ sung.
- **N2 đúng về yêu cầu có giả thuyết phát hiện riêng, nhưng có hai câu nói quá.** Ví dụ tôi nêu trước là *nếu chỉ đổi nơi gán cùng các điểm* thì phép gộp đối xứng không đổi. UV-1 trong G2 còn có bước gộp tỷ lệ theo các cạnh đi vào, nên chưa thể khẳng định mọi cách cài UV-1 đều giữ nguyên điểm hệ thống. Đồng thời, G2-H22 xác nhận phép OR và độ dài lịch sử ảnh hưởng kết quả, **chưa xác định đầy đủ nguyên nhân N-Sigma báo dày**. [Nguồn G2](/D:/RCA-flashticket/results/T-034/goi-g2.md:575).
- **P3 có thể kết thúc bất đồng về PageRank.** Sắp điểm là một lựa chọn xếp hạng cần có lý do, phương án đối lập và đánh giá MRR. Không bắt buộc thêm PageRank. Đính chính của Minh về phiên và nén ngữ cảnh tiếp tục áp dụng khi soạn SPEC; quyền ghi, checkpoint và việc đối chiếu nguồn vẫn giữ nguyên.

---

**Bản kế hoạch hợp nhất P6 — đề xuất lần 3**

Mục tiêu P6 là tạo ra phương pháp có thể chạy và kiểm được trên dev: phát hiện, vùng nghi ngờ và xếp hạng; có baseline đủ sức so sánh; có đối chứng để phân biệt tác dụng của tín hiệu với tác dụng của quan hệ; có giao diện dùng lại trên FlashTicket.

P6 kết thúc bằng hồ sơ trình G3. Kết luận trên dữ liệu chưa dùng để thiết kế thuộc P7; giải thích bằng LLM thuộc P8; triển khai quan sát và tích hợp thuộc P9; bằng chứng vận hành FlashTicket thuộc P10. Không chuyển nghĩa vụ đánh giá phát hiện công khai sang P10.

Các mã M/C dưới đây là mã kế hoạch. Thư mục task hiện kết thúc ở T-040; chưa cấp mã task chính thức mới.

**Căn cứ thiết kế và phần chưa biết**

| Thành phần | Căn cứ hiện có | Việc P6 phải phân xử |
|---|---|---|
| RCA dùng chứng cứ phía gọi, tính cho bên được gọi | UV-1 và phân tích vị trí tín hiệu trong G2 | Cải thiện thứ hạng ở điều kiện nào; có làm hỏng ca đúng, ca không có cạnh hoặc lỗi trả về nhanh không |
| Phát hiện có dùng quan hệ | Yêu cầu DT18/MRP; P3 cho thấy bộ phát hiện hiện tại chưa đáp ứng mục tiêu vận hành | Quan hệ bổ sung thông tin gì để đổi quyết định cảnh báo; lợi ích có còn khi giữ cùng tín hiệu và chính sách cảnh báo không |
| Vùng nghi ngờ | DT18 yêu cầu đầu ra vùng; đồ thị P5 cung cấp quan hệ | Vùng được tạo bằng phép tính nào; có chứa root và rộng tới đâu; chưa gọi là vùng ảnh hưởng thật nếu thiếu nhãn |
| Metric/log và lỗi return | UV-6; giới hạn của tín hiệu độ trễ | Tín hiệu nào thực sự phân biệt được lỗi, thay vì chỉ thêm nhiều cờ |
| Đồ thị tĩnh và các loại cạnh khác | Bàn giao P5; yêu cầu DT18 | Cạnh nào có dữ liệu và thực sự tham gia tính toán; phần nào chỉ kiểm được trên FlashTicket |

Nguồn đầu vào chính là [G2](/D:/RCA-flashticket/results/T-034/goi-g2.md) và [bàn giao P6 của T-040](/D:/RCA-flashticket/results/T-040/ban-giao-p6.md). Tôi đã kiểm hash các tài liệu này. Bàn giao P5 cũng nêu rõ: cạnh trace dev chưa được xác nhận kiểu; không được tự coi chúng là cạnh gọi đồng bộ hoặc dùng kiểu tĩnh để lấp chỗ thiếu.

Đối với phát hiện, M1 sẽ xét các hướng sau, **chưa giao cài mặc định**:

| Hướng ứng viên | Quan hệ tham gia ở đâu? | Điều kiện có thể làm hướng này thất bại |
|---|---|---|
| Thống kê quét trên đồ thị con | Quan hệ xác định những vùng được xét; điểm và ngưỡng quyết định cho cả vùng | Tải bình thường cũng gây lệch đồng thời; lỗi đơn lẻ bị bỏ sót; quét nhiều vùng làm ngưỡng sai nếu không hiệu chỉnh |
| Phần dư có điều kiện | Dự báo hoặc giải thích tín hiệu một nút bằng tín hiệu ở các nút liên quan | Mô hình học cả sự cố; quan hệ không phù hợp; thiếu nền; trừ mất chính chứng cứ cần phát hiện |
| Phân rã chứng cứ theo cây lời gọi | Quan hệ cha–con thay đổi đại lượng được chấm, không chỉ tên nơi nhận điểm | Thiếu span, bất đồng bộ, chồng lấn; lỗi không làm tăng thời lượng |

Thống kê quét có cơ sở nghiên cứu, nhưng **không thể suy “xét vùng liên thông sẽ chữa được báo động dày”**. Công trình CNSS chỉ ra chính việc tối đa hóa trên nhiều đồ thị con có thể làm phép chấm hiệu chỉnh sai. Đây là căn cứ phải xét cách hiệu chỉnh, chưa phải bằng chứng phù hợp với RCAEval. [Bài CNSS, AAAI 2022](https://ojs.aaai.org/index.php/AAAI/article/view/20339).

**Bộ baseline được tổ chức theo câu hỏi so sánh**

| Nhóm | Trạng thái và mục đích | Nơi chịu trách nhiệm |
|---|---|---|
| N-Sigma đã chạy ở P3 | Giữ làm mốc lịch sử; dùng lại kết quả đúng giao thức cũ | M1 xác định phép so; M6 chỉ chạy phần cần cho giao thức mới |
| BOCPD lịch sử | Giữ số hồi cứu và giới hạn tiền xử lý; không gọi thành detector trực tuyến | M1/M12 |
| Baseline thống kê nhân quả bổ sung | Xét một cách có khả năng cạnh tranh, thay vì chỉ so với N-Sigma nguyên trạng; ứng viên gồm ngưỡng hiệu chỉnh hoặc phương pháp tích lũy | M1 lựa chọn để thử; **M6 cài và kiểm** |
| Baseline dùng trace | So tác dụng của thêm trace; lựa chọn giữa luật span có nền nhân quả và biến thể MicroRank phù hợp đầu vào | M1 xác định biến thể; **M6 cài và kiểm** |
| BOCPD nhân quả | Một biến thể cần kiểm riêng tiền xử lý và số học | C8 |
| GDN làm baseline | Đối chiếu với detector học quan hệ giữa các chuỗi metric; không đồng nhất đồ thị học được với đồ thị gọi dịch vụ | C12 |
| Đối chứng cùng tín hiệu nhưng bỏ phần quan hệ đang xét | Phân biệt lợi ích do quan hệ với lợi ích do tín hiệu, cửa sổ hoặc ngưỡng | M7 |
| Baseline RCA chế độ (a) | Dùng lại bộ P3 theo từng dataset và trạng thái hỗ trợ | M12 |
| Baseline RCA chế độ (b) | Hiện hành: BARO, CIRCA kiến trúc, TORAI; mọi bổ sung phải ghi riêng | M1/M12; C5/C7 nếu mở rộng |

Ví dụ, CUSUM có mục đích tích lũy bằng chứng để phát hiện dịch chuyển nhỏ kéo dài, khác với chỉ xét một điểm vượt ngưỡng. Điều đó đủ để đưa vào thẩm định, **không đủ để chọn trước hoặc hứa giảm báo sai trên dữ liệu này**. [Tài liệu NIST](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm).

GDN cũng là một đối thủ có cơ chế khác: học quan hệ giữa các biến để dự báo hành vi. Khả năng sử dụng ở đây còn phụ thuộc dữ liệu học, hiệu chỉnh và chi phí. [Bài GDN](https://arxiv.org/abs/2106.06947).

M1 phải chốt **danh sách hữu hạn để thử**, phiên bản, dữ liệu học/hiệu chỉnh, ngân sách chọn cấu hình và lý do loại các phương án còn lại. M6 không nhận một yêu cầu mở kiểu “cài thêm baseline cho đủ mạnh”.

**13 task chính**

Đề xuất chung cho các task: Codex làm, Claude phản biện; Minh quyết phân công khi duyệt SPEC. Mỗi task đều bao gồm tự kiểm, đọc trung gian, phân tích kết quả trong phạm vi của nó, lưu lượt hỏng, tài liệu và bàn giao. Những việc đó không được dồn sang task cuối.

| Task và loại việc | Công việc, đầu ra cụ thể | Phụ thuộc và phép kiểm kết thúc |
|---|---|---|
| **M1 — Thiết kế phương pháp và giao thức** — thiết kế | Viết giả thuyết riêng cho phát hiện/RCA; chọn ứng viên để thử, mức graph, nguồn cạnh, tập ứng viên; lập bảng baseline; quy định nền, hiệu chỉnh, cảnh báo, chấm điểm, biên file và nhánh rẽ. Chốt giao diện sớm cho P8/P9. | Đọc trực tiếp MRP, G2, T-040 và hồ sơ phương pháp liên quan. Xong khi mỗi lựa chọn có phương án khác, phép bác bỏ, đầu vào cần và task thực hiện; không đòi đã có kết quả dev mới. |
| **M2 — Chứng cứ trace và quan hệ theo thời gian** — cài đặt, kiểm chứng | Dùng lại adapter/cửa sổ P3 và builder P5; bổ sung chỉ mục request/span, thời điểm chứng cứ khả dụng, ánh xạ owner–caller–callee và đại lượng trace cần cho ứng viên. Không dựng lại graph đã hợp lệ. | Sau giao diện M1. Kiểm trên dữ liệu giả có đáp án tính tay: mất cha, nhiều root, span chồng lấn, đến muộn; đối chiếu mẫu thật của cả TT và OB. Chỉ dùng chứng cứ đã khả dụng tại thời điểm quyết định. |
| **M3 — Metric, log, nền và chuẩn hóa** — cài đặt, phân tích | Dùng lại adapter TT/OB; giữ scope service/thao tác/tài nguyên chung; tạo nền nhân quả và trạng thái thiếu dữ liệu; bổ sung chứng cứ cần cho lỗi return. Không nhân một metric chung thành nhiều bằng chứng độc lập. | Sau M1; làm song song M2 được. Kiểm tính tay các phép chuẩn hóa, nền hằng/thưa, tín hiệu tăng/giảm, log trùng và alias. Đối chiếu ca đúng/sai có cùng điều kiện; tín hiệu không phân xử được phải ghi rõ. |
| **M4 — Điểm và xếp hạng RCA ứng viên** — cài đặt, thực nghiệm sớm | Cài cơ chế được M1 giao thử, nối điểm thành thứ hạng và giữ chứng cứ giải thích. Dùng bản ghi/bộ chấm P3 ngay từ đầu. Thử cặp có/bỏ quan hệ trước khi mở nhiều cấu hình. | Cần đầu ra M2/M3 mà công thức sử dụng. Kiểm đường đầu vào → điểm → thứ hạng, hòa điểm, root thiếu tín hiệu/cạnh và ca đúng bị hỏng. Chọn cách xếp hạng theo chất lượng của chính nó, gồm MRR; không chọn theo độ chênh có–không graph. |
| **M5 — Phát hiện và vùng nghi ngờ** — cài đặt, thực nghiệm sớm | Cài điểm hệ thống thực sự dùng quan hệ, nền/ngưỡng, mở–duy trì–đóng cảnh báo và vùng nghi ngờ. Tách điểm thô, sự kiện và thông báo. Thực hiện kiểm tương lai/biên file và lượt thử ghép cặp trên TT. | Cần M1, phần cần thiết của M2/M3; không bắt buộc chờ RCA “thắng”. Kiểm cảnh báo trên tín hiệu giả, thay đổi cạnh, thời điểm khả dụng và phục hồi. Xong về kỹ thuật không đồng nghĩa đã chứng minh dùng được trong vận hành. |
| **M6 — Cài và kiểm baseline phát hiện** — cài đặt, kiểm chứng, thực nghiệm | Cài baseline thống kê và trace đã được chọn để thử trong M1. Ghi đúng bản gốc/biến thể; dùng chung giao diện điểm–cảnh báo–trạng thái. Tái sử dụng N-Sigma và hồ sơ T-015; không gọi luật span hiện có là detector hoàn chỉnh. | Bắt đầu sau M1 và khi đầu vào cần thiết của M2/M3 có sẵn; có thể song song M4/M5. Kiểm oracle, tính nhân quả, trạng thái thiếu nền, tiền xử lý và phép chấm; chạy dev theo cấu hình đã khai. BOCPD/GDN nếu chọn nhận từ C8/C12, không cài trùng. |
| **M7 — Đối chứng cấu trúc** — cài đặt, kiểm chứng | Cài bỏ quan hệ, graph ngẫu nhiên giữ bậc và graph tĩnh có điều kiện. Khai chính xác thông tin cấu trúc còn giữ trong từng nhánh. Giữ cùng tín hiệu, coverage và ngân sách ở phần không chủ ý thay. | Sau khi giao diện tính của M4/M5 đủ rõ; không phải chờ chúng thắng. Kiểm đồ thị sinh ra, tập nút, hướng/bậc và đường tính sử dụng cạnh. Nhánh giữ self-time vẫn dùng cây span, không được gọi là hoàn toàn không cấu trúc. |
| **M8 — Điều phối ma trận và dùng lại trung gian** — kỹ thuật | Mở rộng runner/cache từ P3 cho cấu hình P6. Khóa khóa cache theo dữ liệu, phép biến đổi, cấu hình và revision thực sự ảnh hưởng kết quả. Đo bộ nhớ, đĩa, thời gian từng giai đoạn; xử lý đúng nút thắt nếu đã đo thấy. | Giao diện M2–M7 ổn định ở phần cần chạy. Kiểm chạy tiếp sau ngắt, không mất lượt hỏng, cache không lấy nhầm kết quả và đầu ra tương đương đường chạy sớm. Không dựng bộ chấm thứ hai. |
| **M9 — Ma trận dev RE2-TT** — thực nghiệm | Chạy chế độ (a), (b), các cấu hình/đối chứng đã khai; dùng lại bản ghi sớm nếu phép tính và đầu vào tương ứng không đổi. Báo theo ca/ô, tình trạng không cảnh báo, thiếu nền và lỗi. | Sau những thành phần được dùng của M4–M8 và nhánh baseline liên quan. Đủ ma trận, không bỏ ca khó; tách chất lượng detector, RCA tại cùng mốc và thành công toàn chuỗi. |
| **M10 — Ma trận dev Nezha-OB** — thực nghiệm | Chạy chế độ (a), với giới hạn cửa sổ/kênh đã có. Đối chiếu lỗi return, mạng, node thiếu trace và graph tĩnh. | Sau các thành phần tương ứng; có thể độc lập M9. Không dựng chế độ (b) từ trace/log đã cắt quanh mốc tiêm. Báo đầy đủ ca không hỗ trợ và yếu tố thay cùng. |
| **M11 — Độ nhạy, cơ chế và lựa chọn** — phân tích, thực nghiệm phân xử | Phân tích ca thắng/hòa/thua, nguồn tín hiệu, cửa sổ/nền, cách gộp, chính sách cảnh báo và cấu trúc. Chạy phần độ nhạy cần để phân biệt các giải thích dẫn tới lựa chọn khác nhau. Chọn detector và ranker bằng tiêu chí riêng. | Cần kết quả liên quan của M9/M10 và các nhánh được kích hoạt. Xong khi có lựa chọn được hỗ trợ, hoặc có bác bỏ/OPEN với bằng chứng thiếu cụ thể; không chỉ hoàn thành bảng số. |
| **M12 — So sánh cuối trên dev và kiểm toàn chuỗi** — thực nghiệm, kiểm chứng | Hoàn thành các cặp so sánh còn thiếu theo thiết kế được chọn; chạy baseline tại báo động mới khi cần. Kiểm điểm nối detector → cửa sổ RCA → thứ hạng → gói bằng chứng. Dùng lại P3 ở phần không đổi. | Không nhận thiết kế/cài phương pháp mới. Phải có baseline và đối chứng hợp lệ trước khi chạy phần so sánh phụ thuộc. Nếu cần thay thiết kế, quay đúng task sở hữu và chạy lại phần bị ảnh hưởng. |
| **M13 — Hồ sơ G3 và bàn giao** — tài liệu, bàn giao | Tổng hợp đặc tả, code/config, bảng kết quả, phạm vi kết luận, lỗi/nhánh dự phòng, giao thức P7 và giao diện P8/P9/P10. Ghi những phần còn thiếu để Minh quyết. | Chỉ tổng hợp bằng chứng đã có; không giấu cài đặt hoặc thực nghiệm mới. Không tự duyệt G3, mở test, commit hay coi kết quả âm là lỗi phải sửa cho thắng. |

**Vì sao gộp như vậy:** M2 gộp các bước cùng đi qua span/request; M3 gộp các phép cần thống nhất scope và nền; M4 giữ điểm và xếp hạng trong cùng chuỗi kiểm chứng; M5 giữ điểm hệ thống, trạng thái cảnh báo và vùng được xuất ra cùng thời điểm. M6 được tách vì baseline có nguồn, giả định và phép kiểm độc lập với phương pháp mới. M9/M10 tách vì hai dataset có giao thức và khả năng quan sát khác nhau.

Đây là lý do theo quan hệ công việc. Tôi chưa có căn cứ khẳng định mỗi task tương ứng đúng một cuộc trò chuyện hoặc một số giờ cố định.

**15 task có điều kiện**

Mỗi nhánh chỉ được kích hoạt khi có quyết định thiết kế hoặc câu hỏi phụ thuộc rõ ràng. “Có điều kiện” không có nghĩa được bỏ nghĩa vụ nghiên cứu bằng cách không kích hoạt.

| Nhánh | Điều kiện kích hoạt | Đầu ra và nơi sử dụng |
|---|---|---|
| **C1 — Phần thời gian span chưa được con phủ** | Công thức cần UV-2; giả định thời gian đủ kiểm được | Phép hợp khoảng có oracle chồng lấn/thiếu con/bất đồng bộ; đưa vào M2, M4/M5 |
| **C2 — Phần dư bằng hồi quy có điều kiện** | M1 chỉ ra thay đổi cụ thể so với nhánh đã có bằng chứng bất lợi | Mô hình, đối chứng bỏ quan hệ, kiểm nền và phần dư; M4/M5/M11. Không là phương án cứu mặc định |
| **C3 — Phân xử bước chọn tập của TraceRCA** | Lựa chọn phương pháp hoặc baseline phụ thuộc câu còn mở về singleton/frontend | Dùng trung gian đã có trước; bổ sung đúng cặp so sánh cần thiết; đầu ra phân biệt nguyên nhân hoặc giữ OPEN |
| **C4 — Ứng viên chấm theo tập** | C3/G2 cung cấp dự đoán cần thử cho cách chấm này | Cài điểm tập, oracle và đối chứng; đưa vào M4/M11 |
| **C5 — Nhánh tác giả TraceRCA thành baseline bổ sung** | M1 xác định phép so mà baseline hiện hành chưa trả lời | Adapter, quy ước biến thể, kiểm đúng và kết quả dev; đưa vào M12 |
| **C6 — Phần cơ chế MicroRank còn chưa phân xử** | Việc chọn cơ chế hoặc baseline phụ thuộc phần còn mở sau đổi bộ chia/đếm | Phân tích trung gian và ca đối chiếu; không tự mở lại toàn bộ task cũ |
| **C7 — Biến thể MicroRank làm baseline RCA** | C6/M1 chỉ ra mục đích và phạm vi hợp lệ | Adapter/biến thể được kiểm cùng kết quả dev; không mặc nhiên được dùng ở chế độ (b) |
| **C8 — BOCPD nhân quả** | M1 chọn làm đối chiếu trực tuyến hoặc cần phân xử tác động tiền xử lý | Một task gồm biến thể, kiểm số học, chạy toàn dev được duyệt và đo chi phí; không tách thành ba task chỉ theo batch |
| **C9 — Underflow của tiền xử lý lịch sử** | Kết luận cơ chế hoặc việc sử dụng số lịch sử phụ thuộc phần chưa kiểm | Phân xử trên phần còn lại, giữ lịch sử; không đồng nhất với C8 |
| **C10 — Nhãn/nhóm lan truyền** | Muốn đưa ra kết luận theo lan/không lan hoặc dùng giả thuyết tự sinh/kế thừa | Kiểm nguồn nhãn độc lập và khả năng phân xử. Nếu dữ liệu không đủ, báo giới hạn; không lấy cờ của phương pháp làm nhãn |
| **C11 — OM-07** | Một kết luận P6 thực sự phụ thuộc vấn đề này | Thu đúng bằng chứng còn thiếu theo phạm vi Minh duyệt; không mở lại toàn P5 |
| **C12 — GDN làm baseline** | Có dữ liệu học/hiệu chỉnh hợp lệ, câu hỏi so sánh rõ và chi phí khả thi | Adapter, chuẩn hóa/ngưỡng hợp lệ, kiểm dự báo–điểm–cảnh báo, seed và kết quả dev; cung cấp cho M6/M12 |
| **C13 — Thẩm định nguồn dữ liệu phát hiện bổ sung** | M1 xác định khoảng trống công khai không thể phân xử bằng nguồn hiện có | So hồ sơ nguồn, giấy phép, schema, nền/onset, clock, dung lượng và cách chia. GAIA/MicroSS/Eadro là ứng viên, không mặc nhiên được nhận |
| **C14 — Adapter và thực nghiệm trên nguồn dev bổ sung** | C13 đạt và Minh duyệt nguồn, phạm vi truy cập/tải, cách chia | Cài adapter, kiểm thời gian/nhãn/đầu vào rồi chạy ma trận detector trên phần dev được phép. Kết quả vào M11/M12; dữ liệu giữ ngoài vẫn khóa |
| **C15 — GNN của phương pháp đề xuất** | Đủ điều kiện WHY-10 và có giả thuyết riêng về quan hệ phụ thuộc | Cài biến thể dùng quan hệ được chọn, đối chứng và kiểm huấn luyện. Tách khỏi C12 vì “GDN làm đối thủ” không đồng nghĩa “chọn GNN làm phương pháp của mình” |

C13 và C14 tách vì **chấp nhận một nguồn dữ liệu** và **tích hợp, thực nghiệm trên nguồn đã chấp nhận** có đầu ra và quyền truy cập khác nhau. Không coi “đã khảo sát dataset” là đã tính xong phần sử dụng nó.

C12/C15 có thể dùng chung môi trường và thành phần đã kiểm nếu phù hợp; không huấn luyện hay dựng adapter trùng chỉ vì chúng có hai mục đích nghiên cứu.

**Quy tắc rẽ hướng tách riêng cho phát hiện và RCA**

| Quan sát sau lượt thử hợp lệ | Phát hiện — M5/M6/M11 | RCA — M4/M11 |
|---|---|---|
| Cài đặt/trung gian sai | Sửa đúng bước; chưa đánh giá giả thuyết | Tương tự |
| Quan hệ đổi phép tính nhưng không giúp chất lượng | Báo đánh đổi cảnh báo sai–bỏ sót–độ trễ; xét bác bỏ ứng viên | Báo ca thắng/thua, MRR và nhóm điều kiện; xét bác bỏ ứng viên |
| Chỉ giảm số thông báo nhờ thời gian trơ | Không nhận là detector phân biệt tốt hơn | Không suy chất lượng RCA tăng từ ít lượt gọi hơn |
| Thứ hạng tốt hơn nhưng cảnh báo không đổi | Chưa có bằng chứng cải thiện phát hiện | Có thể là bằng chứng dev cho RCA, với giới hạn tương ứng |
| Thiếu tín hiệu hoặc nhãn cần thiết | Giao phần thiếu cho C13/P9/P10 hoặc giữ kết luận OPEN | Giữ ca trong mẫu số; phân biệt thiếu quan sát với tính điểm sai |
| Dự đoán được hỗ trợ ở nhóm phù hợp | Mở rộng kiểm dev và độ nhạy | Tương tự; chưa khẳng định tổng quát trước P7 |

Một kết quả âm sau phép thử hợp lệ có giá trị nghiên cứu. Nhưng **chưa tìm được cơ chế để thử** không đồng nghĩa đã hoàn thành nghĩa vụ thiết kế P6. Khi đó phải trình rõ phần thiếu và hướng xử lý; không tự thay mục tiêu bằng một detector không dùng quan hệ.

**Giao thức phát hiện phải có ngay trong M1**

- Giữ riêng kết quả P3 theo giao thức cũ và kết quả P6 theo giao thức mới; không trộn độ đo khác nghĩa.
- Nền, hiệu chỉnh, thời gian khởi động và cập nhật chỉ dùng thông tin hợp lệ; không cắt theo mốc tiêm rồi gọi là tự phát hiện.
- Kiểm bất biến với phần tương lai khi lịch sử được phép nhìn thấy giữ nguyên.
- Kiểm độ nhạy với thời điểm bắt đầu quan sát: độ lệch khác nhau giữa các ca, sinh theo quy tắc/seed khai trước, không chọn theo nhãn; giữ toàn bộ lượt. Phân biệt thiếu lịch sử với bám vị trí sự cố.
- Đếm riêng cờ, sự kiện và thông báo. Đo precision/recall/F1, độ trễ theo loại mốc thật sự có, cảnh báo trước tiêm theo proxy, thời gian duy trì cảnh báo và khả năng phục hồi.
- Chỉ gọi là tỷ lệ cảnh báo sai trong vận hành khi có nền phù hợp đã được xác minh. Không tự đặt một ngưỡng “chấp nhận được” bằng con số chưa có căn cứ.
- Với RCA, báo cả chế độ biết mốc, RCA tại cùng báo động, và thành công toàn chuỗi. Thời điểm trả được thứ hạng phải tính cả cửa sổ dữ liệu cần chờ.
- Vùng trên dữ liệu công khai được gọi đúng là vùng nghi ngờ; không chấm như vùng ảnh hưởng thật khi thiếu nhãn.

**Khối lượng thực nghiệm và cách dùng lại kết quả**

Phạm vi nền vẫn là **30 ca TT cho hai chế độ và 22 ca OB cho chế độ (a)**. Một cấu hình có đủ ba nhánh đó tương ứng:

\[
30+30+22=82\ \text{đơn vị ca–chế độ}.
\]

Nhưng không lấy 82 nhân một số cấu hình đặt trước để coi là đã biết toàn bộ chi phí. M1 phải xác định các tập hữu hạn:

- Cấu hình RCA và detector được thử.
- Các cấu hình đối chứng tương ứng.
- Seed của phương pháp ngẫu nhiên.
- Lượt thay thời điểm bắt đầu quan sát.
- Biến thể độ nhạy có câu hỏi cần phân xử.

Ví dụ, số lượt đánh giá RCA biết mốc là \(52K_a\); số lượt phát lại detector TT là \(30K_d\). Các lượt đổi điểm bắt đầu được tính riêng theo số lịch phát lại đã khai. Nhiều detector có thể dùng chung một lần trích đặc trưng nếu dữ liệu và phép trích giống nhau.

Tại **một bộ báo động mới**, phạm vi ranker chế độ (b) hiện hành có trần đếm theo cách cũ là:

\[
30(1_{\text{BARO}}+1_{\text{CIRCA}}+3_{\text{seed TORAI}})=150.
\]

Đây không phải tổng P6, cũng không phải cam kết mọi ca đều có báo động hợp lệ. Mọi bổ sung SimpleRCA, TraceRCA hoặc MicroRank phải cộng từ phạm vi đã xác định, không giữ số 240 mặc định.

**Không cộng lại** lượt M4–M6 vào M9–M12 nếu chúng đã có đúng đầu vào, phép tính và cấu hình cần dùng. Không chạy lại toàn bộ P3 chỉ vì có phương pháp mới.

Thời gian máy, RAM, đĩa của những phép tính mới hiện **chưa đo**. Chi phí agent đọc/sửa/phân tích và thời gian chờ phản biện cũng **chưa có ước lượng đáng tin**. Các task cài đặt phải đo ngay từ lượt đầu; M8 tổng hợp theo toàn ma trận. Tôi bỏ các khoảng giờ và tỷ lệ dự phòng không có căn cứ của bản đầu.

**Phụ thuộc và song song**

```text
M1
 ├─ M2 ─┐
 ├─ M3 ─┼─ M4: RCA ─────────┐
 │      ├─ M5: phát hiện ────┼─ M7: đối chứng
 │      └─ M6: baseline ─────┘
 └─ Các nhánh được kích hoạt ──┐
                               ↓
                    M8: chạy ma trận
                       ├─ M9: TT
                       └─ M10: OB
                               ↓
                    M11: phân xử/chọn
                               ↓
                    M12: so sánh còn thiếu
                               ↓
                    M13: hồ sơ G3
```

M8 có thể được chuẩn bị từ khi giao diện ổn định, không cần chờ mọi phân tích khoa học kết thúc. M2/M3 và các phần độc lập của M4/M5/M6 có thể làm song song. M9/M10 độc lập về dữ liệu, nhưng chỉ chạy đồng thời nếu bộ nhớ cho phép; không chạy việc nặng khác trong lúc đo chi phí.

Phản biện nằm trong vòng đời từng task. Phát hiện cần sửa quay về đúng nơi sở hữu; không tạo task mới chỉ vì có thêm một lượt phản biện, và không cam kết “chỉ một lượt cuối rồi dừng”.

**Đối chiếu toàn bộ 34 + 15 task của bản đầu**

Các mã T bên trái dưới đây là **mã dự kiến trong bản kế hoạch cũ**, không phải task đã được tạo.

| Phần cũ | Xử lý trong bản này |
|---|---|
| 041, 043, 060 | M1; phần cài hợp đồng đi cùng M2/M3/M6 |
| 042 | Đo tại module tương ứng, tổng hợp ở M8; bỏ task kiểm khả thi chung chung |
| 044–047 | Gộp M2; dùng lại adapter/builder hợp lệ |
| 048–050, 066 | Gộp M3 |
| 051, 054 | M4; phần điểm phục vụ cảnh báo thuộc M5 |
| 052–053 | M5 |
| 055–056 | M8; bản ghi/bộ chấm dùng ngay từ M4–M6 |
| 057–059 | M7 |
| 061–062, 080–082 | C8; một phần việc BOCPD nhân quả, không chia theo ba batch |
| 063–064 | M12 với phạm vi ranker đã sửa |
| 065 | C10; M11 theo dõi kết luận nào phụ thuộc |
| 067 / 068 | M9 / M10 |
| 069–071 | M11 |
| 072 | Kiểm tại M4–M8 khi cài; đối chiếu toàn chuỗi ở M12 |
| 073–074 | Giao diện sớm ở M1, bàn giao hoàn chỉnh ở M13 |
| 075 | C2 |
| 076–077 | Gộp C3 |
| 078 / 079 | C4 / C6 |
| 083 | Nhánh xử lý nút thắt đã đo trong M8 |
| 084 / 085 / 086 | C5 / C7 / C11 |
| 087–089 | Gộp C9 |

Như vậy, không bỏ sót mã nào trong 49 đề xuất cũ. So với bản 12 + 11:

- Thêm **M6** vì cài/kiểm baseline phát hiện là công việc bắt buộc phải có người nhận.
- Giữ M1–M5; M6–M12 cũ chuyển thành M7–M13.
- Thêm **C12–C15** để tách rõ GDN baseline, thẩm định dữ liệu, sử dụng dữ liệu đã nhận và GNN của phương pháp. Đây là những việc có điều kiện khác nhau, không được ngầm dồn vào M11/M12.

**Phạm vi file dự kiến, chưa được phép ghi**

Nếu lưu bản kế hoạch, đề xuất một file mới: `D:/RCA-flashticket/docs/PLAN-P6.md`. File này chứa kế hoạch và trạng thái ứng viên; không thay MRP, WHY hoặc DECISIONS.

Khi từng SPEC được duyệt, mã mới dự kiến nằm dưới `D:/RCA-flashticket/src/p6/`:

| Chủ sở hữu | Module dự kiến |
|---|---|
| M1 | Hợp đồng/API và đặc tả phương pháp trong đầu ra task |
| M2 | `trace_evidence.py` |
| M3 | `signals.py`, `normal_reference.py` |
| M4 | `ranking.py` |
| M5 | `detection.py`, `regions.py` |
| M6 | `baselines/` cho các bộ được chọn |
| M7 | `controls.py` |
| M8 | `runner.py`, phần mở rộng đánh giá cần thiết |
| M9–M13 | Kết quả, phân tích và tài liệu; không mặc nhiên có quyền sửa lõi |
| Các nhánh C | Module và đầu ra đúng biến thể được duyệt; không sửa bản P3 lịch sử |

Đầu ra mỗi task nằm trong `D:/RCA-flashticket/results/<mã-task>/`; SPEC/LOG/REVIEW theo cấu trúc hiện hành. Các thay đổi mã dùng chung hoặc WHY chỉ được ghi khi SPEC/phạm vi tương ứng được Minh duyệt. Lượt này không đề xuất ghi DECISIONS hay sửa AGENTS.

**Báo cáo lượt**

1. **Đã làm:** đáp N1/N2 và hợp nhất kế hoạch; giao rõ cài baseline, phép thử phát hiện, các nhánh dữ liệu và toàn bộ phần việc cũ.
2. **File thay đổi:** không sửa file nào; không tạo task, chạy thực nghiệm, mở dữ liệu khóa hoặc tải dataset.
3. **Kiểm tra:** đối chiếu MRP, nguồn đề tài, G2, bàn giao T-040, mã P3/P5 và tài liệu khoa học liên quan. Các đầu ra G2/T-040 được dùng khớp manifest. Kiểm bảng ánh xạ đủ 49 mã cũ; trạng thái Git không đổi.
4. **Còn mở:** danh sách ứng viên được phép thử, cấu hình/ngân sách cụ thể, dữ liệu nền và khả năng cải thiện thực tế. Bản này xử lý thiếu phân công ở N1, chưa chứng minh phương pháp khả thi về chất lượng. **Đề xuất phản biện bản hợp nhất này**, rồi dừng khi không còn phản đối có căn cứ ảnh hưởng việc duyệt kế hoạch; không đặt trước số lượt.

Không cần Minh quyết tải GAIA/MicroSS ngay để hoàn thiện bản kế hoạch. Nếu M1 đề xuất kích hoạt C13, đề xuất đó phải nêu rõ khoảng trống cần lấp, nguồn cần đọc/tải và chi phí cụ thể.

Prompt bàn giao dưới đây dùng cùng nguyên văn bản kế hoạch này và các đính chính của Minh:

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: bản kế hoạch hợp nhất P6 lần 3 và phản hồi của người lập kế hoạch, Minh gửi kèm nguyên văn trong chat; chưa có file kế hoạch chính thức.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex là người lập kế hoạch; Claude là người phản biện lượt kế hoạch này. Phân công chỉ áp dụng đề xuất kế hoạch.
- Tài liệu gốc: yêu cầu ban đầu tại C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; nguyên văn các đính chính của Minh về thời gian máy, công việc agent, phiên, nén ngữ cảnh, quyền ghi và việc chia task; yêu cầu của Minh về bộ phát hiện và RCA; toàn bộ bản kế hoạch hợp nhất gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước: kế hoạch bản 1 tại C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt; phản biện bản 1 tại C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt; kế hoạch sửa đổi và phản hồi của Codex gửi kèm; phản biện tại C:/Users/84583/.codex/attachments/ca11a615-a65e-4a57-bb7b-1489b6adf748/Pasted text.txt; bản kiểm lại tại C:/Users/84583/.codex/attachments/e427eb03-eb51-4627-ae4c-53c6aab92e3f/Pasted text.txt; phản hồi và kế hoạch hợp nhất mới nhất gửi kèm nguyên văn. Nếu chuyển máy, dùng nguyên văn Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-002/; results/T-015/; results/T-018/; results/T-021/; results/T-025/; results/T-034/ đến results/T-040/; các nguồn và manifest tương ứng được kế hoạch dẫn. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s13"></a>

### S13 — Phản biện GDN và các điểm R1–R4

<details>
<summary>Mở nguyên văn S13</summary>

````text
## 1. Câu hỏi về GNN: đã tính trên dữ liệu thật hay chỉ trên giấy?

**Đã đo trên dữ liệu thật, nhưng ở P1 (T-005, T-018), không phải trong kế hoạch.** Bản 3 không dẫn các số đó. Hai điều kiện kích hoạt C12 ("có dữ liệu học hợp lệ") và C15 ("đủ điều kiện WHY-10") vì vậy mới chỉ ở mức giấy, dù bằng chứng để quyết đã có sẵn trong repo.

**Những gì đã đo** (`results/T-018/ho-so-gdn.md` §9, `results/T-005/do-kha-thi.md:51–54`):

| Câu hỏi | Đã biết |
|---|---|
| GDN cần nhãn không? | Không cần nhãn lỗi để học. GDN học dự báo hành vi bình thường. Nhưng cần **đoạn bình thường không thuộc ca được chấm** |
| Dữ liệu bình thường có bao nhiêu? | RE2-TT: 12 phút trước mốc tiêm mỗi ca, tức tối đa 6 giờ khi gộp 30 ca dev. Đây là 30 lượt chạy rời nhau, và chưa ai xác nhận độc lập rằng các đoạn này sạch |
| Lấy đoạn bình thường thế nào? | Cắt bằng mốc tiêm của **các ca dev khác**. Đây là "nhãn dev dùng để học": hợp lệ nếu khai rõ (MRP §4; T-018 §8.1 dòng G8). Không bao giờ dùng mốc của ca đang được chấm |
| Bộ cột | Giao 30 ca còn 317 cột. Bộ này mất 23/25 cột `_error`, nên GDN gần như không thấy tín hiệu lỗi |
| Kết quả trên đoạn bình thường giữ ngoài | Học 1 ca: báo sai 23,6 % số tick. Học 5 ca: 10,8 %. Học 10 ca: 4,95 %, khoảng 5 đợt/giờ. Với cách chuẩn hóa hợp lệ ở chế độ (b), 10 ca vẫn báo 45 % số tick. Mô hình 10 ca **không báo tick nào** ở ca R-ca, kể cả sau mốc tiêm |
| Độ ổn định | Học trên 1 ca: đổi seed thì tập tick báo động gần như đổi hẳn (Jaccard 0,18–0,58) |
| Chi phí | 5 ca, 30 epoch: 17 phút trên CPU laptop, RAM dưới 1 GB |

Ước lượng chi phí của tôi, **chưa kiểm**: ngoại suy tuyến tính, mỗi lượt học trên 24 ca mất khoảng 80 phút. Kiểm chéo 5 phần × 3 seed là khoảng 20 giờ máy, nên phải xin Minh duyệt theo luật cứng 8.

**GNN có giám sát:** không khả thi trên dữ liệu này.
- Dev chỉ có 30 ca và 5 service gốc. Mô hình sẽ học thuộc 5 service đó (WHY-10 tiêu chí 2).
- Không có nhãn bất thường theo từng thời điểm ngoài nhãn proxy, và không có nhãn vùng.
- Dữ liệu công khai duy nhất trong repo có nhãn theo từng trace là DeepTraLog. Bộ này không được chọn ở G1 và không có metric tài nguyên (`ho-so-gdn.md` §9.5).

**C15 (GNN làm phương pháp):** tiêu chí 1 của WHY-10 hiện **chưa đạt**. Tiêu chí này đòi P4 chỉ ra loại bất thường phụ thuộc ngữ cảnh mà cách chấm theo từng phần tử bỏ sót. Gói G2 không có dòng hạn chế nào như vậy; tìm "ngữ cảnh", "GNN" trong `goi-g2.md` không ra kết quả nào liên quan.

**Hệ quả cho Minh:**
- Câu trả lời cho cô "vì sao chưa dùng GNN" phần lớn **đã có bằng chứng** ở T-018. MRP §2.3 yêu cầu đúng điều này.
- C12 chỉ đáng làm nếu Minh muốn có một dòng "GNN-based detection" trong bảng so sánh. Khi đó nó là đối chứng cho ví dụ của cô, **không** phải baseline mạnh.

## 2. Kết luận về bản 3

**Không còn điểm nào chặn việc duyệt cấu trúc kế hoạch.**
- N1 đã được xử lý bằng M6 và C12–C14.
- P1, P2 đã có giao thức trong M1.
- Quy tắc rẽ hướng đã tách riêng cho phát hiện và RCA.
- Tôi đếm lại bảng đối chiếu 49 mã cũ: đủ 49.

Còn ba điểm cần sửa trong nội dung M1 và các nhánh C, cùng một lưu ý quy trình.

## 3. Kiểm phản hồi của Codex về N2 và P3

- **N2:** Codex **đúng**, tôi nói quá hai chỗ.
  - UV-1 có bước "gộp tỷ lệ lời gọi đi vào vượt nền" (`ban-giao-p6.md` §3), nên không phải chỉ chuyển nguyên điểm sang nút khác.
  - G2-H22 chỉ xác lập phép OR và độ dài lịch sử *có đi vào* kết quả, chưa xác định nguyên nhân N-Sigma báo dày.
- **P3:** đồng ý đóng như Codex nêu.

## 4. Điểm mới

### R1 — KHÔNG CHẶN duyệt kế hoạch; cần ghi vào tiêu chí xong của M1: C12 và C15 chưa dùng bằng chứng đã có

- **Ở đâu:** bảng nhánh có điều kiện, dòng C12 và C15.
- **Sai gì:** điều kiện kích hoạt viết như thể chưa biết gì, trong khi T-005 và T-018 đã đo dữ liệu, bộ cột, mức báo sai, độ nhạy seed và chi phí.
- **Hậu quả:** M1 có thể kích hoạt C12 với kỳ vọng sai. Hoặc ngược lại, bỏ GNN mà không viện dẫn bằng chứng, trong khi cô đã nêu tên ví dụ này.
- **Sửa tối thiểu:**
  - Đưa T-018 §8–9 và T-005 vào đầu vào của M1.
  - M1 quyết C12 dựa trên các số trên. Nếu kích hoạt, kế thừa cách chạy hợp lệ ở T-018 §8.2.
  - Ghi rõ C15 không kích hoạt cho tới khi có dòng hạn chế đạt tiêu chí 1 của WHY-10.

### R2 — KHÔNG CHẶN duyệt kế hoạch; CHẶN việc khóa giao thức phát hiện ở M1: chưa nói dữ liệu nền và dữ liệu hiệu chỉnh lấy từ đâu

- **Ở đâu:** mục "Giao thức phát hiện phải có ngay trong M1". Điều này áp dụng cho M5, M6, C8, C12, C14.
- **Sai gì:**
  - Bản 3 chỉ ghi "chỉ dùng thông tin hợp lệ", chưa nêu **nguồn** của dữ liệu nền.
  - T-018 §9.2 đã chỉ ra một rủi ro cụ thể. Nếu lấy đoạn đầu file của chính ca đó làm nền, giả định "đoạn đầu là bình thường" đúng chỉ **nhờ cách cắt file** 720/720 (đã kiểm lại: 30/30 ca).
- **Tôi tự đính chính:** phép đổi thời điểm bắt đầu quan sát mà tôi và Codex đã thống nhất **không phát hiện được rủi ro này**. Mọi độ lệch nhỏ hơn 720 s vẫn để lại một đoạn đầu nằm trước mốc tiêm.
- **Hậu quả:** độ đo phát hiện trên dev và trên test có thể đẹp hơn thực tế vận hành. Test có cùng cấu trúc file nên không bắt được.
- **Sửa tối thiểu:** M1 chọn và khai một trong hai nguồn nền:
  1. Kho đoạn bình thường của các ca dev khác (nhãn dev dùng để học, đánh giá chéo theo ca).
  2. Đoạn khởi động của chính ca, độ dài chốt trước và ngắn hơn hẳn 12 phút, ghi rõ giả định.
  
  Báo cáo phải nêu giới hạn tương ứng.

### R3 — KHÔNG CHẶN: nhánh phát hiện có 7 phần việc nhưng chưa xếp ưu tiên

- **Bằng chứng:** M5, M6, C8, C12, C13, C14, C15 cùng phục vụ phát hiện trên một miền 30 ca TT có giới hạn cấu trúc đã biết.
- **Sai gì:**
  - C8 (BOCPD nhân quả) chồng mục đích với "baseline thống kê nhân quả" của M6. Bản 3 chưa nói C8 trả lời câu gì mà M6 không trả lời.
  - C12 tốn khoảng chục giờ máy (ước lượng ở mục 1, chưa kiểm).
- **Sửa tối thiểu:** M1 ghi mục đích riêng của C8 so với M6. Nếu không có mục đích riêng thì giữ số BOCPD lịch sử kèm giới hạn và không kích hoạt C8. C12 và C15 quyết theo R1.

### R4 — KHÔNG CHẶN, quy trình: phạm vi áp dụng đính chính của Minh

- Bản 3 ghi đính chính về phiên và nén ngữ cảnh "tiếp tục áp dụng khi soạn SPEC". Nguyên văn tôi thấy chỉ nói về lượt lập kế hoạch.
- Nếu Minh muốn áp cho SPEC và các phiên làm task, nên ghi ở chỗ phiên sau đọc được. Nếu không, agent khác ở phiên khác hoặc máy khác sẽ áp nguyên văn AGENTS §5/§5a.
- Đây là việc Minh quyết. Tôi không đề xuất sửa AGENTS.

## 5. Đề xuất

**Dừng phản biện toàn diện** sau khi Codex đáp R1–R3. Các điểm đó là nội dung cần ghi vào M1 và C8/C12/C15, không làm đổi cấu trúc 13 + 15. Minh có thể duyệt cấu trúc kế hoạch khi Codex đã tiếp nhận ba điểm này. Kết luận về hiệu quả của phương pháp vẫn OPEN cho tới P7.

**Minh cần quyết:**
1. Có giữ GNN trong P6 không? Tôi khuyến nghị: không kích hoạt C15. Chỉ kích hoạt C12 nếu Minh muốn có dòng GNN-based trong bảng so sánh, chấp nhận chi phí khoảng chục giờ máy (chưa kiểm).
2. Đính chính về phiên có áp cho các phiên làm task sau không (R4)?

## Báo cáo lượt

1. **Đã làm:**
   - Đọc hồ sơ GDN T-018 (§0, §8, §9) và số đo GDN trong T-005.
   - Tìm trong G2 xem có căn cứ cho tiêu chí 1 của WHY-10 không.
   - Kiểm phản hồi của Codex về N2 và P3, đếm bảng 49 mã cũ.
   - Phản biện toàn bộ bản 3.
2. **File thay đổi:** không sửa file nào.
3. **Kiểm đã chạy:** đọc file và grep; tính lại tổng 49 mã. Không chạy thực nghiệm, không mở dữ liệu khóa. Chi phí C12 là ngoại suy, chưa kiểm.
4. **Còn mở:**
   - R2 phải xong trước khi khóa giao thức phát hiện.
   - Tôi không kiểm được bài CNSS mà Codex dẫn (không truy cập web trong lượt này).
   - Hai quyết định ở mục 5 thuộc về Minh.

---

## Prompt cho Codex đáp phản biện

Khi gửi, Minh đính kèm nguyên văn bản kế hoạch 3 và toàn bộ câu trả lời này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: bản kế hoạch hợp nhất P6 lần 3 (13 task chính, 15 task có điều kiện), Minh gửi kèm nguyên văn trong chat; chưa có file kế hoạch chính thức.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex là người lập kế hoạch; Claude là người phản biện lượt kế hoạch này. Phân công chỉ áp dụng đề xuất kế hoạch.
- Tài liệu gốc: yêu cầu ban đầu tại C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; nguyên văn các đính chính của Minh về thời gian máy, công việc agent, phiên, nén ngữ cảnh, quyền ghi và việc chia task; yêu cầu của Minh về bộ phát hiện, RCA và GNN; bản kế hoạch hợp nhất lần 3 gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước, theo thời gian: kế hoạch bản 1 tại C:/Users/84583/.codex/attachments/a4c9b59c-1dbb-42ca-a689-6f48105e86eb/Pasted text.txt; phản biện bản 1 tại C:/Users/84583/.codex/attachments/4130c51d-3d9c-44b1-a44c-770d317e9a1a/Pasted text.txt; kế hoạch sửa đổi và phản hồi của Codex; phản biện tại C:/Users/84583/.codex/attachments/ca11a615-a65e-4a57-bb7b-1489b6adf748/Pasted text.txt; bản kiểm lại tại C:/Users/84583/.codex/attachments/e427eb03-eb51-4627-ae4c-53c6aab92e3f/Pasted text.txt; bản kế hoạch hợp nhất lần 3; phản biện của Claude cho bản lần 3, Minh gửi kèm nguyên văn. Nếu chuyển máy, dùng nguyên văn Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-002/; results/T-005/; results/T-013/; results/T-015/; results/T-018/; results/T-021/; results/T-025/; results/T-034/ đến results/T-040/; các nguồn và manifest tương ứng được kế hoạch và phản biện dẫn. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s14"></a>

### S14 — Codex đáp và sửa cuối

<details>
<summary>Mở nguyên văn S14</summary>

````text
**Tôi tiếp nhận R1–R3 và giữ cấu trúc đề xuất 13 task chính + 15 nhánh có điều kiện. Tuy nhiên, phần kết luận về GNN trong phản biện cần đính chính trước khi dùng để quyết định.** GDN đã có thực nghiệm thật; kết quả hiện tại đáng lo, nhưng chưa chứng minh mọi hướng GNN đều không khả thi.

Tất cả nội dung dưới đây là phân tích và sửa đề xuất **trong chat**, chưa phải quyết định đã duyệt.

**Về bằng chứng GDN: có một chỗ trộn hai cách tính khác nhau.**

Tôi đã đối chiếu kết quả gốc và kiểm hash của 10 file liên quan; đều khớp manifest lưu ở T-020.

| Kết quả trên các đoạn dev tách khỏi tập học | Chuẩn hóa theo toàn đoạn đang chấm | Chuẩn hóa bằng thống kê kiểm định cố định |
|---|---:|---:|
| Học 1 ca: tỷ lệ tick báo động | 23,62% | 99,58% |
| Học 5 ca: tỷ lệ tick báo động | 10,82% | 99,58% |
| Học 10 ca: tỷ lệ tick báo động | 4,95% | 45,15% |
| Học 10 ca: số tick báo động trên ca R-ca | **0** | **702** |

Nguồn: [kết quả phân tích T-018](/D:/RCA-flashticket/results/T-018/runs/b6b7-phan-tich.json), các nhánh `luot/<tên lượt>/giu_ngoai_code`, `giu_ngoai_b` và `ca_rca`; lượt 10 ca là `l7-lstar-n10-seed5`.

Cột thứ nhất dùng thống kê của cả đoạn được chấm, gồm dữ liệu tương lai. Tôi đã đối chiếu lại đúng [revision code GDN đã dùng](https://github.com/d-ailin/GDN/blob/9853899da860682669a134e4af315d036aab4eca/evaluate.py#L44-L62). Vì vậy:

- Không thể dùng **4,95%** làm bằng chứng về khả năng phát hiện trực tuyến của biến thể chuẩn hóa cố định.
- Câu “mô hình 10 ca không báo động ở R-ca” chỉ đúng với cách tính thứ nhất. Biến thể thứ hai báo **702 tick**; chưa phân tích vị trí các tick thì cũng chưa được gọi đó là phát hiện đúng.
- Đây là báo động trên các đoạn **được giả định bình thường vì nằm trước mốc tiêm**. Chưa có xác nhận sức khỏe độc lập để gọi toàn bộ chúng là báo sai vận hành.

Kết quả vẫn cho thấy vấn đề nghiêm trọng: **cấu hình GDN chuẩn hóa cố định đã thử chưa tạo được nền đủ yên trên những đoạn này.** Chính [WHY-18](/D:/RCA-flashticket/docs/WHY.md:178) đã ghi trạng thái “chưa đạt”, không phải cấu hình P3 được chọn.

Hai nhận định khác cũng cần giới hạn:

- Mất 23/25 cột `_error` là mất phần lớn **nhóm cột error**, không chứng minh gần như mất mọi tín hiệu sự cố. Latency, CPU, memory, socket… vẫn có thể chứa triệu chứng.
- “Có ít service gốc nên mô hình có giám sát **sẽ học thuộc**, do đó **không khả thi**” mạnh hơn bằng chứng. [WHY-10](/D:/RCA-flashticket/docs/WHY.md:97) nêu nguy cơ học thiên lệch về tập service và yêu cầu đánh giá phù hợp; chưa có phép thử chứng minh kết luận bất khả thi. Cách nói đúng là **chưa đủ căn cứ ưu tiên hướng này với dữ liệu và giao thức hiện tại**.

**Tôi trả lời từng điểm phản biện như sau.**

| Điểm | Kết luận | Thay đổi trong đề xuất |
|---|---|---|
| **R1 — chưa tận dụng T-005/T-018** | **Đúng.** Đây là thiếu sót của bản 3. | M1 phải dùng kết quả và các đường rò thông tin đã biết để xét C12/C15. Không khởi động lại từ câu hỏi chung “GDN chạy được không?”. |
| **R2 — chưa chỉ rõ nguồn nền và hiệu chỉnh** | **Đúng; chặn khóa giao thức detector.** | M1 phải chỉ rõ nguồn, cách chia, quyền dùng nhãn, cách chuẩn hóa và ngưỡng. Việc đổi thời điểm bắt đầu quan sát không đủ chứng minh đoạn khởi động sạch. |
| **R3 — chưa ưu tiên, C8 có thể trùng M6** | **Đúng.** | M6 sở hữu việc cài và kiểm baseline. C8 chỉ kích hoạt nếu có câu hỏi riêng; không tính hai lần cùng một phần cài đặt/thực nghiệm. |
| **R4 — đính chính có thể không đến phiên sau** | **Đúng về rủi ro bàn giao; không cần hỏi lại Minh nội dung đã nói rõ.** | Khi bàn giao phải kèm nguyên văn đính chính của Minh. Lượt này không ghi DECISIONS, không sửa AGENTS và không coi văn bản repo đã được cập nhật. |

**Phần M1 được bổ sung cụ thể như sau.**

Đầu vào thêm T-005, T-018 §8–9 và WHY-18. Đầu ra phải có một bảng giao thức cho từng detector, trả lời được:

1. **Nền lấy từ đâu?** Bản ghi bình thường riêng, đoạn dev khác được chọn bằng nhãn phục vụ học, hay đoạn khởi động của chính luồng?
2. **Dữ liệu nào dùng để học, chọn cấu hình, hiệu chỉnh ngưỡng và đánh giá?** Có dùng lại cùng dữ liệu cho nhiều vai trò không; nếu có thì kết luận bị giới hạn thế nào?
3. **Tại thời điểm báo động, hệ thống thực sự đã có thông tin nào?** Gồm cả điền thiếu, chuẩn hóa, chọn cột, chọn ngưỡng và cập nhật nền.
4. **Khoảng nào chưa thể chấm?** Khởi động, thiếu nền, thiếu tín hiệu phải được báo rõ; không tính mặc nhiên là bình thường.
5. **Cách chọn ngưỡng cân bằng báo động và bỏ sót ra sao?** Không chọn bằng việc giảm số thông báo sau khi đã thấy kết quả.

Phương án tôi ưu tiên **để M1 xem xét**, chưa chốt, là học/hiệu chỉnh từ các nhóm dev khác rồi đánh giá trên nhóm không tham gia các bước ấy. Các lần lặp cùng ô phải đi cùng phía, phù hợp MRP; không chỉ chia ngẫu nhiên từng ca. Phải phân biệt tập chọn mô hình với tập hiệu chỉnh ngưỡng, đồng thời tránh cửa sổ chồng qua ranh giới.

Dùng mốc tiêm của **ca dev khác** để lấy đoạn học là sử dụng nhãn cho việc học. T-018 đã khai điều này cho phép chẩn đoán của nó; không vì thế mà tự động có một giao thức P6 hoàn chỉnh đã được duyệt.

Phương án dùng đoạn khởi động của chính luồng vẫn có thể xét, nhưng **rút ngắn đoạn đó không chứng minh nó bình thường**. Nó chỉ cho phép kết luận trong điều kiện vận hành có một giai đoạn khởi động phù hợp. Nếu dữ liệu không kiểm được giả định này thì phải giữ giới hạn, không dùng điểm đẹp để thay bằng chứng.

**Các nhánh phát hiện được ưu tiên và phân trách nhiệm lại như sau.**

| Phần việc | Mục đích và điều kiện thực hiện |
|---|---|
| **M1 → M3/M5/M6** | Ưu tiên trước: xác định nền hợp lệ; xây điểm và quyết định báo động; cài baseline thống kê và baseline trace có câu hỏi so sánh rõ. M6 tiếp nhận kết quả nhánh bổ sung, không cài lại. |
| **C8 — BOCPD theo luồng** | Chỉ kích hoạt khi cần phân xử ảnh hưởng của tiền xử lý nhìn trước trong BOCPD lịch sử, hoặc cần đối chứng phát hiện điểm đổi mà baseline M6 chưa cung cấp. Nếu BOCPD chính là baseline được chọn ở M6, gộp phần thực hiện vào M6; không tạo thêm một lần chạy tương đương. |
| **C13 — xét dữ liệu bổ sung** | Có thể cần ngay từ M1 nếu dữ liệu hiện tại không phân xử được câu hỏi về nền, tải thay đổi hoặc báo động vận hành. Không đợi chạy hết các phương pháp rồi mới nhận ra thiếu dữ liệu. Dùng lại hồ sơ P2; chỉ kiểm khoảng trống cụ thể. |
| **C14 — tích hợp dữ liệu bổ sung** | Chỉ sau khi C13 xác định được bộ dữ liệu phù hợp và Minh duyệt. |
| **C12 — baseline GDN** | Chỉ kích hoạt khi có câu hỏi khoa học và thay đổi cụ thể so với cấu hình T-018: chẳng hạn xử lý lệch mức giữa các lượt chạy, hoặc so quan hệ metric học được với quan hệ dịch vụ. Phải có phép thử có thể bác bỏ kỳ vọng ấy. **Không kích hoạt chỉ để có tên GNN trong bảng.** |
| **C15 — phương pháp GNN của đề tài** | Hiện tôi **khuyến nghị chưa kích hoạt**. Chưa có chuỗi bằng chứng được trình đủ để đáp ứng WHY-10. Đây là trạng thái thiếu căn cứ hiện tại, không phải chứng minh mọi GNN thất bại. |

Việc tìm không thấy từ “ngữ cảnh” hoặc “GNN” trong báo cáo G2 không đủ để chứng minh tuyệt đối rằng không có hiện tượng liên quan. Nhưng trách nhiệm vẫn thuộc bên đề xuất C15: phải chỉ ra hiện tượng, thông tin quan hệ cần dùng và phép thử phân xử. Hiện chưa có lý do để cam kết cài.

Về chi phí, T-005 đo một lượt học 5 ca khoảng **17 phút**; T-018 còn có lượt 10 ca đo được khoảng **32 phút học**. “Khoảng 20 giờ” là ngoại suy cho một thiết kế kiểm chéo giả định, không phải chi phí C12 đã xác nhận. Không dùng con số đó để kết luận task quá lớn hoặc GNN bất khả thi. Nguồn: [số đo T-005](/D:/RCA-flashticket/results/T-005/runs/ket-qua-do.jsonl), bản ghi `muc=gdn_hoc`; và `luot/l7-lstar-n10-seed5/s_hoc` trong kết quả T-018.

**Về tính khả thi mà Minh đang lo: hiện chưa đủ bằng chứng để hứa sẽ có detector dùng được trong vận hành.** P6 phải giải quyết điều đó bằng thực nghiệm, không bằng cách bổ sung tên thuật toán.

Tôi vẫn đề xuất giữ hướng đồ thị, nhưng phân biệt rõ hai mức căn cứ:

- **RCA:** đã có căn cứ để thử các ứng viên như tính thời gian lời gọi cho phía được gọi, tổng hợp theo cạnh đi vào và tách thời gian tự xử lý. [Bàn giao P5](/D:/RCA-flashticket/results/T-040/ban-giao-p6.md:38) nêu đầu vào, phép tính và điều kiện thất bại. Chưa có bằng chứng chúng tạo cải thiện ổn định.
- **Detector:** cần chứng minh điểm có dùng quan hệ giúp phân biệt điều kiện bình thường và sự cố tốt hơn đối chứng tương ứng. Chỉ gom các nút đã báo động thành vùng chưa chứng minh đồ thị giúp phát hiện.

Tiêu chí vận hành phải xem đồng thời **thời gian ở trạng thái báo động, số đợt, số thông báo, sự cố bỏ sót và độ trễ**. Một cảnh báo kéo dài hàng giờ không trở nên hữu ích chỉ vì được gộp thành một thông báo. Ngược lại, giảm báo động bằng cách làm detector im lặng cũng không đạt mục tiêu.

Các sửa đổi trên **không sinh thêm task chính**: chúng làm rõ đầu ra của M1, trách nhiệm của M6 và điều kiện của các nhánh đã có. Vì vậy tôi giữ **13 task chính và danh mục 15 nhánh có điều kiện**, không coi đó là 28 task bắt buộc.

Tôi đề xuất **dừng phản biện toàn diện về cấu trúc**, và nếu tiếp tục thì chỉ kiểm các sửa đổi cùng bất đồng có bằng chứng nêu trên. Chưa nên dùng phản biện hiện tại làm căn cứ kết luận GNN bất khả thi hoặc kích hoạt GDN vì tên gọi. Giao thức nền/hiệu chỉnh vẫn phải được giải quyết trong M1 trước khi khóa.

Báo cáo lượt:

- **Đã làm:** đối chiếu phản biện với kết quả GDN gốc, code nguồn, MRP/WHY; cụ thể hóa sửa M1 và các nhánh.
- **File thay đổi:** không sửa file nào; không ghi DECISIONS.
- **Kiểm tra:** 10 file bằng chứng khớp hash; trạng thái Git không đổi so với đầu lượt. Không chạy thực nghiệm mới, không mở dữ liệu khóa.
- **Còn mở:** nguồn nền đủ tin cậy, khả năng hiệu chỉnh detector và hiệu quả các ứng viên. Các đề xuất trong chat chưa được chuyển thành quyết định hay quyền thực hiện.

Prompt dưới đây để Minh chuyển cho Claude nếu muốn kiểm tiếp; kèm bản kế hoạch 3, phản biện vừa gửi và toàn bộ phản hồi này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch hợp nhất P6 lần 3 và phần sửa đề xuất trong phản hồi mới nhất của Codex; Minh gửi kèm nguyên văn. Chưa có file kế hoạch chính thức.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: đề xuất kế hoạch P6, trước G3.
- Người làm và người phản biện chính thức: Codex lập kế hoạch; Claude phản biện đề xuất kế hoạch.
- Tài liệu gốc: yêu cầu và các đính chính của Minh gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan.
- Phản biện và phản hồi trước: bản kế hoạch 3; phản biện của Claude tại C:/Users/84583/.codex/attachments/407bb5c5-df38-4acd-9f0e-1b5441bd5711/Pasted text.txt; phản hồi mới nhất của Codex. Minh gửi kèm nguyên văn, cùng các lượt trước khi cần.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-005/; results/T-018/; results/T-020/manifest.json; results/T-021/; results/T-025/; results/T-034/ đến results/T-040/ và các nguồn được dẫn; code GDN revision 9853899da860682669a134e4af315d036aab4eca. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần; không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s15"></a>

### S15 — Claude kiểm lại cuối và đề xuất dừng

<details>
<summary>Mở nguyên văn S15</summary>

````text
## Kết luận

**Codex đúng ở phần đính chính GNN. Lượt trước tôi đã trộn hai cách chuẩn hóa điểm của GDN.** Sau khi sửa, kết luận "GDN theo cấu hình đã thử chưa dùng được" vẫn giữ, thậm chí bất lợi hơn. Hai bên không còn bất đồng nào ảnh hưởng tới cấu trúc kế hoạch. **Tôi đề xuất dừng phản biện kế hoạch.**

## 1. Kiểm số GDN trên file gốc

Nguồn: `results/T-018/runs/b6b7-phan-tich.json`, nhánh `luot/<lượt>/…`.

| Học trên | Tỷ lệ tick báo động trên đoạn trước mốc của ca khác: cách của code (dùng thống kê của cả đoạn đang chấm, gồm dữ liệu tương lai) | Cùng chỉ số: chuẩn hóa cố định, **hợp lệ khi chạy trực tuyến** | Ca R-ca: tick báo động theo cách code / cách cố định |
|---|---|---|---|
| 1 ca | 23,62 % | 99,58 % | 301 / 1433 |
| 5 ca | 10,82 % | 99,58 % | 97 / 1433 |
| 10 ca | 4,95 % | **45,15 %** (7,15 đợt/giờ) | **0 / 702** |

- Lượt trước tôi đưa các số 23,6 %, 10,8 %, 4,95 % và câu "10 ca không báo tick nào ở R-ca" mà **không ghi** đó là cách chuẩn hóa nhìn trước. Cách này không hợp lệ ở chế độ tự phát hiện. Đây là lỗi của tôi.
- Với cách hợp lệ, 1 và 5 ca học báo động gần như liên tục. 10 ca học báo 45 % số tick trên đoạn được giả định bình thường.
- 702 tick ở R-ca chưa được phân tích vị trí, nên chưa gọi được là phát hiện đúng.
- Codex cũng đúng ở hai chỗ khác:
  - Đây là báo động trên đoạn **giả định** bình thường, chưa xác nhận độc lập là sạch.
  - Thời gian học 10 ca là 1.928,69 s, khoảng 32 phút (`l7-lstar-n10-seed5/s_hoc`).

## 2. Các điểm còn lại

| Điểm | Kết luận của tôi |
|---|---|
| "Mất 23/25 cột `_error` nên gần như không thấy tín hiệu lỗi" | Codex **đúng một phần**. Câu này lấy từ T-018 §9.1, nhưng chỉ nói về nhóm cột đếm lỗi. Latency, CPU, bộ nhớ, socket vẫn có thể mang triệu chứng |
| "GNN có giám sát không khả thi" | Codex **đúng**: tôi nói quá. Cách nói đúng: chưa đủ căn cứ để ưu tiên. Lý do cụ thể: dev chỉ có 30 ca và 5 service gốc. Muốn kiểm khả năng tổng quát sang service gốc chưa thấy thì phải chia theo service gốc (WHY-10), khi đó tập học còn ít hơn nữa |
| Tìm "ngữ cảnh" trong G2 không ra | **Đúng một phần, cho cả hai bên.** Không tìm thấy từ không chứng minh tuyệt đối. Nhưng trong 26 dòng hạn chế G2-H01 đến H26 không có dòng nào về bất thường phụ thuộc ngữ cảnh. Codex cũng đồng ý trách nhiệm chứng minh thuộc bên đề xuất C15 |
| Chi phí khoảng 20 giờ | **Đồng ý** đây chỉ là ngoại suy cho một thiết kế giả định, không dùng để kết luận GNN bất khả thi. Lượt trước tôi cũng đã ghi "chưa kiểm" |
| R1–R3 | Codex tiếp nhận; phần sửa M1 và các nhánh C8, C12, C13, C15 **đạt**. Bảng 5 câu về nguồn nền và hiệu chỉnh cho từng detector trả lời đúng R2. Chia gập theo ô (các lần lặp cùng ô ở cùng một phía) đúng MRP §4 |
| R4 | **Chấp nhận** cách xử lý: mọi prompt bàn giao kèm nguyên văn đính chính của Minh |

**Tự soát phần sửa mới:** tôi không thấy lỗi đáng kể. Có một lưu ý, chưa kiểm: chia gập theo ô thì mỗi gập chỉ còn khoảng 24 đoạn 12 phút để học và hiệu chỉnh. T-018 cho thấy mức metric lệch mạnh giữa các lượt chạy. Vì vậy khả năng cao M1 sẽ phải kích hoạt C13 sớm. Bản kế hoạch đã cho phép làm vậy, nên đây không phải lỗi.

## 3. Trả lời Minh về GNN, sau khi đã sửa

- **Đã làm thật, không chỉ trên giấy.** GDN đã chạy trên RE2-TT ở P1 (T-005, T-018).
  - Dữ liệu học: đoạn trước mốc tiêm của các ca dev khác, tức dùng nhãn dev để học và có khai báo.
  - Bộ cột cố định 317 cột; thử với 1, 5 và 10 ca học.
- **Kết quả:** với cách chạy hợp lệ khi chạy trực tuyến, cấu hình đã thử chưa tạo được nền yên. Học 10 ca vẫn báo 45 % số tick trên đoạn giả định bình thường. Đây là bằng chứng đã có để trả lời cô vì sao GNN chưa là hướng chính.
- **Nhãn:** GDN không cần nhãn lỗi, chỉ cần dữ liệu bình thường đủ nhiều lượt chạy. RE2-TT chỉ có 30 đoạn × 12 phút. GNN có giám sát cần ca có nhãn; dev có 30 ca với 5 service gốc, nên chưa đủ căn cứ để ưu tiên.
- **Hai agent thống nhất:**
  - C15 (GNN làm phương pháp): chưa kích hoạt.
  - C12 (GDN làm baseline): chỉ kích hoạt khi có một thay đổi cụ thể so với T-018, ví dụ xử lý lệch mức giữa các lượt chạy, kèm dự đoán có thể bác bỏ. Không kích hoạt chỉ để có tên GNN trong bảng.

## 4. Đề xuất

**Dừng phản biện kế hoạch.** Lý do:
- Không còn phản đối nào chưa xử lý ảnh hưởng tới cấu trúc 13 + 15.
- Các câu còn mở (nguồn nền đủ tin cậy, hiệu chỉnh detector, hiệu quả ứng viên, có cần C13 không) là việc của M1 và các thực nghiệm sau, không phải lỗi kế hoạch.
- Dừng phản biện không tự duyệt kế hoạch và không xác nhận phương pháp sẽ hiệu quả.

**Minh quyết:**
1. Duyệt kế hoạch 13 + 15, gồm phần sửa M1 và các nhánh trong phản hồi mới nhất của Codex?
2. Nếu duyệt, có lưu vào `docs/PLAN-P6.md` như Codex đề xuất không? Việc này cần Minh duyệt đúng nội dung file theo Luật 0. Bước kế tiếp là soạn SPEC cho M1.

## Báo cáo lượt

1. **Đã làm:**
   - Đọc số GDN của mọi lượt trong `b6b7-phan-tich.json`.
   - Đối chiếu đính chính của Codex với lượt trước của tôi, nhận lỗi trộn hai cách chuẩn hóa.
   - Kiểm phần sửa M1 và các nhánh C.
2. **File thay đổi:** không sửa file nào.
3. **Kiểm đã chạy:** đọc JSON. Số Codex dẫn khớp file: 23,62 / 10,82 / 4,95 %; 99,58 / 99,58 / 45,15 %; R-ca 0 và 702 tick; thời gian học 1.928,69 s. Tôi không kiểm lại hash manifest T-020 và không đọc code GDN trên GitHub. Không chạy thực nghiệm, không mở dữ liệu khóa.
4. **Còn mở:** không còn bất đồng có bằng chứng. Các câu khoa học vẫn OPEN như nêu ở mục 4.

---

## Prompt cho Codex

Prompt này để Minh dùng nếu muốn Codex xác nhận việc dừng. Khi gửi, Minh đính kèm nguyên văn câu trả lời này.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: kế hoạch hợp nhất P6 lần 3 cùng phần sửa trong phản hồi mới nhất của Codex; Minh gửi kèm nguyên văn. Chưa có file kế hoạch chính thức.
- Công đoạn: người làm đáp phản biện.
- Gói/cổng: đề xuất kế hoạch toàn chặng P6, trước G3.
- Người làm và người phản biện chính thức: Codex là người lập kế hoạch; Claude là người phản biện lượt kế hoạch này. Phân công chỉ áp dụng đề xuất kế hoạch.
- Tài liệu gốc: yêu cầu ban đầu tại C:/Users/84583/.codex/attachments/f47519fa-33b6-45df-893a-550d48bc5834/Pasted text.txt; nguyên văn các đính chính của Minh gửi kèm; yêu cầu của Minh về bộ phát hiện, RCA và GNN; bản kế hoạch lần 3 và phản hồi mới nhất của Codex gửi kèm; D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; docs/review-prompt.md; tasks/_MAU/SPEC.md; SPEC và LOG liên quan của T-034–T-040.
- Phản biện và phản hồi trước, theo thời gian: các lượt kế hoạch, phản biện và phản hồi trước Minh gửi kèm; phản biện bản 3 của Claude tại C:/Users/84583/.codex/attachments/407bb5c5-df38-4acd-9f0e-1b5441bd5711/Pasted text.txt; phản hồi mới nhất của Codex; bản kiểm lại mới nhất của Claude gửi kèm nguyên văn. Nếu chuyển máy, dùng nguyên văn Minh gửi kèm.
- Code và kết quả liên quan: D:/RCA-flashticket/src/p3/; src/do_thi/; src/do_thi_tinh/; results/T-005/; results/T-018/; results/T-020/manifest.json; results/T-021/; results/T-025/; results/T-034/ đến results/T-040/ và các nguồn được dẫn; code GDN revision 9853899da860682669a134e4af315d036aab4eca. Repo hệ thống D:/Project/flash-ticket-platform chỉ đọc khi cần. Không đọc repo RCA lưu trữ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ đọc và trả lời trong chat. Không ghi DECISIONS hoặc file khác; không chạy thực nghiệm mới, mở dữ liệu khóa, tải dữ liệu, tạo phiên hay tự gửi prompt.

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

Công đoạn: người làm đáp phản biện. Giữ vai trò người làm, không là người phản biện chính thức của chính task.
Tự soát yêu cầu và mọi file đầu ra gốc cần để trả lời các câu hỏi như một người chưa từng làm task, TRƯỚC khi mở kết luận các bản phản biện. Ghi danh sách điểm tự tìm được vào LOG trước khi mở các kết luận ấy nếu được phép ghi; phiên chỉ đọc ghi nhận xét trong chat.
Sau đó kiểm từng điểm phản biện trên file/code/dữ liệu thật; chạy lại khi rẻ và được phép. Kết luận đúng / đúng một phần / sai / chưa kiểm được với bằng chứng riêng. Reviewer có thể sai, nói quá hoặc đề xuất sửa có mặt trái.
Nếu được Minh cho phép: điền bảng Phản hồi của người làm ở cuối đúng bản phản biện; thêm N1, N2… cho điểm tự tìm được với CHẶN/KHÔNG CHẶN; để trống cột Minh quyết; nối LOG đủ mục 7 của AGENTS, gồm đề xuất sửa gom theo file; chỉ cập nhật dòng task trong STATE khi được phép. Không sửa nội dung hay prompt của reviewer hoặc tự sửa báo cáo/code.
Nếu chưa có quyền ghi các phần này, trình phản hồi và đề xuất trong chat. Soạn prompt bàn giao cho người phản biện kiểm độc lập.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```
````

</details>

<a id="s16"></a>

### S16 — Minh giao lưu đầy đủ kế hoạch vào repo

<details>
<summary>Mở nguyên văn S16</summary>

````text

# Files pasted by the user:

## "## Kết luận **Codex đúng ở phần đính chính GNN. Lượt trước tôi đã trộn hai cách…": C:\Users\84583\.codex/attachments/7fcf8559-c2c5-4d8b-8485-4f7e0a7a4abb/Pasted text.txt

## My request:
Minh giao: ghi lại đầy đủ kế hoạch P6 đã chốt qua các lượt phản biện và các quyết định liên quan vào repo, để phiên sau, agent khác hoặc máy khác làm tiếp được mà không cần lịch sử chat. Minh lo ngữ cảnh đã bị nén khiến bản ghi thiếu quyết định hoặc thiếu một bước trong kế hoạch. Vì vậy KHÔNG viết từ trí nhớ. Dựng lại từ nguyên văn các tài liệu dưới đây.



````

</details>

### Manifest văn bản nguồn nhúng

Hash áp dụng chuỗi UTF-8 đã chuẩn hóa xuống dòng LF, không gồm hàng rào Markdown. Dùng để đối chiếu bản sao nguyên văn, không thay manifest kết quả khoa học.

```json
{
  "schema": "p6-plan-embedded-sources/v1",
  "session_id": "01a14ca6-8a67-7b63-a430-937a5e867ac8",
  "sources": [
    {
      "id": "S01",
      "origin": "attachment:f47519fa-33b6-45df-893a-550d48bc5834",
      "text_utf8_sha256": "e580fa457e3a0e1f76cee177b20a8f02e7431dd3ce678840cd2a2a0b565da21d",
      "characters": 10653
    },
    {
      "id": "S02",
      "origin": "session:373",
      "text_utf8_sha256": "5fd1313325a38017cc9e07bc39ce935e6fdcf9d88acc134e175478fe89a70531",
      "characters": 73414
    },
    {
      "id": "S03",
      "origin": "attachment:4130c51d-3d9c-44b1-a44c-770d317e9a1a",
      "text_utf8_sha256": "a76012b2507c5212461086864090a897eaa14d8a3c282ec438f6f39bb811a0ef",
      "characters": 16202
    },
    {
      "id": "S04",
      "origin": "session:479",
      "text_utf8_sha256": "783a4528136f1ba1cfa55c944bc86113b984bbb02112effafea4d4e56527e64e",
      "characters": 14811
    },
    {
      "id": "S05",
      "origin": "session:489",
      "text_utf8_sha256": "f1d181ae54dd26447d22e33795fd09e1850b56b0e84c36939716fab8cc48a12c",
      "characters": 4755
    },
    {
      "id": "S06",
      "origin": "session:619",
      "text_utf8_sha256": "b02c35f447f984a6c5f0bbf091fa21038ca6edc1879df5a661242810da0dcfc2",
      "characters": 44320
    },
    {
      "id": "S07",
      "origin": "session:626",
      "text_utf8_sha256": "5299767b186453f902098606f8b98dbf9e50f44ec4cb49cacdb1f6d904c8931a",
      "characters": 368
    },
    {
      "id": "S08",
      "origin": "session:755",
      "text_utf8_sha256": "9573da66283daf938459436d38b4d0fb39144ecbea1413115ef95ea025ef2d91",
      "characters": 13256
    },
    {
      "id": "S09",
      "origin": "attachment:ca11a615-a65e-4a57-bb7b-1489b6adf748",
      "text_utf8_sha256": "36c1fb5f38a9e14a2e6f73658873522d674650c2cb80b45d75492aaad1948b2c",
      "characters": 20481
    },
    {
      "id": "S10",
      "origin": "session:943",
      "text_utf8_sha256": "122be517ab1b5e484e1ebd7e08325d6d5dcd17d7f40add51962c0ad557ffd70e",
      "characters": 22755
    },
    {
      "id": "S11",
      "origin": "attachment:e427eb03-eb51-4627-ae4c-53c6aab92e3f",
      "text_utf8_sha256": "31281ad600d7656d51dbe30df33774d90a86d0269e4294115e086e776971e027",
      "characters": 17438
    },
    {
      "id": "S12",
      "origin": "session:1057",
      "text_utf8_sha256": "2dcf76f3b5adecc90bf2f1d11c155f4a94b05b0fe341509c8d1ce70c163aae47",
      "characters": 34891
    },
    {
      "id": "S13",
      "origin": "attachment:407bb5c5-df38-4acd-9f0e-1b5441bd5711",
      "text_utf8_sha256": "dd82a355755f63e24b7b74323da2290b4b11c231787ec62727e0b61f0adcde7c",
      "characters": 17313
    },
    {
      "id": "S14",
      "origin": "session:1185",
      "text_utf8_sha256": "950aeaf5401a5ec4ed980e3dc883b53188be9e47e99c4771c9e446dc6b7037b7",
      "characters": 18302
    },
    {
      "id": "S15",
      "origin": "attachment:7fcf8559-c2c5-4d8b-8485-4f7e0a7a4abb",
      "text_utf8_sha256": "a0622e7e494358302863b6c17f014e861fb10825318658ac929813ea8b95625e",
      "characters": 14818
    },
    {
      "id": "S16",
      "origin": "session:1196",
      "text_utf8_sha256": "1c1ccbc2187e8648ef1600008944bf14502aeb0c5ccf991cdc8bdd87a789e598",
      "characters": 579
    }
  ]
}
```
