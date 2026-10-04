# Bài học phải áp dụng

Bản rút gọn để đọc nhanh. Câu chuyện đầy đủ, số liệu và nguồn ở `reference/LESSONS-v1.md`; mã ST, SL, QT, CB dưới đây trỏ về file đó.

## Sự thật đã đo về RE2-TT (dùng nếu P2 chọn RE2-TT; không đo lại trừ khi spec yêu cầu)

- 90 ca = 5 service gốc × 6 loại lỗi × 3 lần lặp. Nhãn chỉ có: service gốc, loại lỗi, thời điểm tiêm lỗi (ST1).
- Trace: 98,45% span cha resolve được. `statusCode` rỗng toàn bộ. Log có ở 89/90 ca (ST2).
- Đồ thị gần như hằng số: 30 ca dev chỉ có 2 đồ thị khác nhau. auth không có cạnh nào (ST3).
- 60 ca chưa ai nhìn từng ca. Bài FSE 2026 báo baseline không dùng đồ thị SimpleRCA đạt top-1 0,80 trên RE2-TT (ST9, ST10).

## Sai lầm không được lặp lại

| Mã | Sai lầm | Điều cần làm thay |
|---|---|---|
| SL1, SL22 | Câu hỏi lệch đề tài; bám khung cũ khi làm bản mới | Bắt đầu từ DT18 và chuỗi của cô (MRP §2) |
| SL2, SL3 | Một lựa chọn riêng (sàn 1e-12) quyết định dấu của kết luận; giá trị vô lý bị ghi là "giới hạn" | Kiểm chịu lực; soi giá trị trung gian |
| SL5, SL12 | Hạ tầng và quy trình lớn hơn khoa học; ngữ cảnh mỗi phiên quá nặng | Quy trình vừa đủ; STATE một trang |
| SL7, SL10 | Đơn giản hóa prior work đúng chỗ tạo giá trị; so với một baseline yếu | Dùng code chính thức; baseline mạnh |
| SL8, SL15 | Đo "giá trị đồ thị" trên dữ liệu không phân xử được | Đếm khả năng phân xử trước khi đặt giả thuyết |
| SL13 | Dùng công cụ nặng cho câu hỏi nhanh | Báo chi phí trước |
| SL14, SL21 | Nêu mẫu hình từ trung bình nhóm (thực ra chỉ một ô); rồi kết luận quá tay theo chiều ngược lại | Tách theo ô; phân biệt "chưa biết" với "không được" |
| SL16, SL18 | Chỉ nhận sai khi người khác chỉ ra; đưa góp ý của reviewer vào tài liệu mà chưa tự kiểm | Tự kiểm; góp ý là đầu vào, không phải lệnh |
| SL17 | Viết số từ trí nhớ | Lấy số từ file kết quả |
| SL20 | Gắn "hoàn thành" với "đồ thị phải thắng" | Kết quả trung thực (Q-04) |
| SL23 | Đề xuất chưa kiểm nhưng nói như sự thật | Ghi "chưa kiểm", giả định, khi nào sai |
| SL24 | Cài và đo thời gian phương pháp mà không kiểm nó chạy đúng; báo "chạy được" khi chỉ biết "không lỗi" (T-005) | Trước khi dùng số của một phương pháp: tái lập số công bố nếu có; luôn chạy phép kiểm không cần nhãn (đầu ra rỗng, trùng thứ tự cột hoặc nhánh dự phòng, chạy lại ra cùng kết quả) |
| SL25 | Chạy lượt có thể dài mà không ghi tiến độ hay thời gian từng bước; bị dừng ở giới hạn thì không biết gì (CIRCA-PC tốn 2 giờ máy cho câu "quá 1 giờ") (T-005) | Ghi tiến độ và thời gian từng bước ngay từ lượt đầu, nhất là khi SPEC đã nêu rủi ro chạy lâu |
| SL26 | Người soạn SPEC loại một phép kiểm cần thiết ("không đọc thứ hạng") mà không nêu hệ quả (T-005) | Khi SPEC bỏ một phép kiểm, ghi rõ kết luận nào yếu đi vì thiếu nó, để Minh quyết |
| SL27 | Đánh giá chi phí theo từng ca, không theo tổng (BOCPD 24 phút/ca tưởng chấp nhận được, thực ra khoảng 36 giờ cho 90 ca) (T-005) | Quy mọi chi phí về tổng ngân sách (Q-40) |
| SL28 | Tra số công bố sau khi đo (Bảng 8 bài TORAI đã có thời gian chạy) (T-005) | Tra số công bố trước khi thiết kế phép đo, dùng làm mốc so |
| SL29 | Dựng môi trường không ghim phiên bản (pandas 3.0.6, causal-learn 0.1.4.8), lệch với lúc tác giả chạy (T-005) | Ghim phiên bản theo lock file hoặc thời điểm công bố; lệch thì ghi và kiểm ảnh hưởng |
| SL30 | Chạy việc khác trong lúc đo (`du` song song); đặt giới hạn chạy nền quá ngắn làm lượt cài bị dừng (T-005) | Không chạy việc nặng khác khi đang đo; đặt giới hạn theo ước lượng có dư |
| SL31 | Người làm thay mục "Bổ sung yêu cầu phản biện" của mẫu bằng danh sách kiểm riêng, kèm kết luận sẵn và câu thu hẹp phạm vi; neo người phản biện (prompt T-001 bản 4, T-005 bản 2) | Chép nguyên văn mẫu; chỉ điền thông tin trung tính (Q-44) |
| SL32 | SPEC xếp các bước theo thứ tự đọc, không theo phụ thuộc thật: SPEC T-006 bắt mọi luồng chờ hết bước 0, làm X1 trễ và EC2 của T-007 ngồi rảnh (T-006, T-007) | Trong SPEC, ghi rõ mỗi bước cần đầu ra nào của bước nào; việc không phụ thuộc thì chạy ngay (Q-43) |
| SL33 | SPEC kiểm đúng đắn (T-006, T-007) chỉ dùng dữ liệu cỡ nhỏ (Online Boutique, Sock Shop), bỏ dữ liệu cỡ Train Ticket công khai (`fse-tt`) dù RE2-TT là ứng viên dataset chính; người soạn SPEC không nêu hệ quả. Minh tưởng Train Ticket đã được kiểm vì T-005 có đo thời gian trên một ca RE2-TT (T-006, T-007) | Phạm vi dữ liệu của task kiểm phải phủ mọi quy mô và dataset ứng viên mà kết quả sẽ dùng; bỏ phần nào thì ghi lý do và hệ quả để Minh quyết. Báo cáo phân biệt rõ "đã đo thời gian" với "đã kiểm đúng sai" |
| SL34 | T017: regex suy pod từ tên làm gộp nhầm database hợp lệ (ts-assurance-mongo→ts) | Kiểm tên bằng dữ liệu/schema, dùng alias tường minh; soi điểm trung gian và giữ/rerun lượt bị ảnh hưởng. Bằng chứng: results/T-017/kiem-dung-dan.md; run-dev-004 |
| SL35 | Viết câu phổ quát ("30 ca đều có `inject_time.txt`") sau khi chỉ nhìn một thư mục (T-018, đã đính chính) | Câu "mọi/đều" phải có lệnh đếm trên đủ đối tượng |
| SL36 | Kết luận "TORAI khớp" chỉ dựa vào điểm cuối khớp số công bố (T-006). Ở đúng cấu hình đó, bước nhân quả không nhận cột metric nào do lỗi giảm mẫu hai lần, và 176/184 cụm rơi nhánh dự phòng về thứ tự mức nghiêm trọng; số vẫn khớp dù bản cài đang kiểm có lỗi; chưa xác minh code hay lượt chạy nào tạo số công bố (T-016) | Trước khi gọi một phương pháp là "kiểm đúng đắn": soi đầu vào thật của từng thành phần (số cột, số dòng), đếm số lần rơi nhánh dự phòng bên trong, và so điểm với một bản bỏ thành phần đó (ví dụ chỉ SeverityScorer) |

## Quy tắc

- **QT1 — Mục đích trước.** Mỗi thành phần, thí nghiệm, tài liệu phải nói được nó phục vụ câu nào của cô, DT18, RQ nào. Không nói được thì không làm.
- **QT2 — Prior work là mặc định.** Lấy đúng quy ước của bài hoặc code gốc, có file và dòng. Lệch thì ghi lý do vào WHY.
- **QT3 — Kiểm chịu lực trước khi khóa.** Thay từng lựa chọn riêng trong khoảng hợp lý trên dev. Kết luận đổi dấu thì phải biện minh lựa chọn đó và báo độ nhạy.
- **QT4 — Tiêu chí chọn không thiên vị giả thuyết.** Mỗi thành phần chọn theo chất lượng của chính nó, không theo mức chênh "có đồ thị trừ không đồ thị". Đã nhìn kết quả nhánh khác lúc chọn thì ghi rõ.
- **QT5 — Soi giá trị trung gian.** Điểm lớn hơn 1e6, toàn hòa, ngưỡng cực lớn, một nhóm kênh chiếm gần hết → dừng tìm nguyên nhân.
- **QT6 — Dev để sửa, test để kiểm.** Khuyết tật thấy trên dev thì sửa, có nguyên lý. Test mở một lần sau G3.
- **QT7 — Nhánh không đồ thị phải mạnh.** Ngang hoặc hơn baseline đơn giản đã công bố trên cùng dữ liệu.
- **QT8 — Khẳng định về đồ thị cần ba thứ:** hơn nhánh không đồ thị; hơn đồ thị ngẫu nhiên giữ bậc; báo theo điều kiện và từng ca.
- **QT12 — Review gọn.** Một reviewer khác model, chỉ nhận spec, diff, kết quả. Minh quyết sửa gì.
- **QT13 — Viết cho người đọc.** Tiếng Việt, câu ngắn, có "tại sao".
- **QT15 — Tách theo ô và theo ca trước khi nêu mẫu hình.** Một ô không phải mẫu hình. Service không có cạnh không tính là bằng chứng cho hay chống đồ thị.
- **QT16 — Hỏi "dữ liệu này phân xử nổi không" trước khi đặt giả thuyết.** Nếu kết cục dễ xảy ra nhất là "không đủ bằng chứng" thì nói ngay với Minh.
- **QT17 — Số trong tài liệu lấy từ file kết quả**, có ghi nguồn.
- **QT18 — Góp ý của subagent hay reviewer là đầu vào, không phải lệnh.**
- **QT19 — Triệt để (Q-41).** Mọi thứ kiểm được với chi phí hợp lý thì kiểm ngay trong task. "Chưa kiểm" chỉ khi không kiểm được trong task, kèm lý do. Kiểm triệt để mà không vừa một phiên thì tách task, không kiểm nhẹ đi.
