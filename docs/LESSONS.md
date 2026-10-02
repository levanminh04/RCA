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
