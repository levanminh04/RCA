# T-051 — Hoàn tất phần người làm sau kiểm bổ sung

## Phần việc đã hoàn tất

Minh yêu cầu làm nốt phần còn thiếu ngày 04/11/2026. Phần thiếu có thể thực hiện ngay là lưu kiểm native ở nhánh có tác động. Kiểm gồm E9 tắt/bật cửa sổ 55 và T12 bật cửa sổ 43, trên đúng đầu vào và cấu hình đã ghim. Hồ sơ kiểm đặt ở native-co-tac-dong-001, gồm bản ghi native, trung gian, cấu hình, hash đầu vào, đối chiếu, thời gian và RAM.

Ba cấu hình native đều khớp đầu vào chuẩn hóa, F_I, m, khóa và nhóm hòa, V0, vùng và kế thừa với bản phát lại đã ghim. Cấu hình T12 cũng khớp các đối chứng áp dụng. Ca 55 có hai kênh đổi F_I giữa hai vế, ca 43 có bốn kênh đổi F_I. Không có mismatch ở ba thế giới.

| Cửa sổ | Cấu hình native | Thời gian của phép kiểm | Kết quả |
|---|---|---:|---|
| 55 | E9 tắt | 68,703 giây | 0 sai khác |
| 55 | E9 bật | 6,924 giây | 0 sai khác |
| 43 | T12 bật | 186,528 giây | 0 sai khác |

Tổng lượt kiểm là 262,740 giây, khoảng 4,38 phút. Hai vế E9 dùng lại cache đúng runner hiện hành nên vế bật ngắn hơn. Ca 43 dài hơn pilot, đã cập nhật ETA trong lúc chạy. Bản ghi native và trung gian được giữ đầy đủ trong từng thư mục con, biên nhận tổng tại native-co-tac-dong-001/summary.json.

Báo cáo gốc, đính chính lượt 1 và hai manifest trước giữ mốc lịch sử. Trạng thái hiện hành đọc cùng hồ sơ kiểm bổ sung và manifest-dap-phan-bien-002.json. Theo tự kiểm của người làm, các bước kỹ thuật và đầu ra có thể thực hiện trong phạm vi T11/T12/KB đã đủ. Hai sai lệch lịch sử được nêu ở cuối tài liệu để Minh xem khi nghiệm thu.

## Các câu hỏi đã có hướng xử lý cụ thể

Các mục dưới không còn là một danh sách OPEN chung. Cột kết luận ghi điều đã có bằng chứng hoặc quyết định. Cột xử lý ghi rõ việc cần thực hiện ở bước tiếp theo. Chỉ những khẳng định còn thiếu bằng chứng mới giữ trạng thái chưa xác nhận.

| Nội dung | Kết luận và lựa chọn hiện tại | Xử lý cụ thể, phụ thuộc và người chịu trách nhiệm |
|---|---|---|
| E9, cạnh tĩnh, thành phần K | E9 tắt, T12 tắt. Nền E1-U, E2-C, E5, z+S1, E6a. E3(a), E3b, E6b tắt. Giữ cờ đánh đổi E2. T11/T12 và bốn kết cục KB đã có. | Codex hoàn tất kiểm native bổ sung và bàn giao. Claude kiểm phần sửa nếu Minh chuyển. Minh nghiệm thu. Đây là lựa chọn của T-051 trên dev. |
| PageRank đảo chiều | Nền dùng E6a theo Q-241. Kết cục HẠI của T9 áp cho chiều đã thử. Hiệu quả biến thể đảo chưa được đo. | Đề xuất giữ E6a cho T-052. Nếu mở lượt thăm dò mới, phép thử chỉ đổi chiều trên cùng đầu vào, nút, điểm, trọng số và khóa. Đặt riêng theo đính chính T-050. |
| Tương tác VC với E5 | K-b chọn C trên nền E5 bật. KB giữ cả C và E5 nên không phát sinh việc phải chọn lại. Chưa có căn cứ khẳng định C/VC độc lập với E5. | Người làm T-052 giữ giới hạn trong hồ sơ G3. Phép 2×2 chỉ cần khi muốn khẳng định tương tác hoặc thay E5, theo kế hoạch hiện hành và WHY-72/73. |
| Cạnh thông điệp và dữ liệu | Dev hiện tại không có đủ hai đầu quan sát để các cạnh này tham gia điểm/hạng/vùng. T12 chỉ cho bằng chứng tác động của cạnh gọi đồng bộ đủ điều kiện. | P9/P10 cần ánh xạ hai đầu quan hệ và tín hiệu trên thực thể để kiểm vai trò chẩn đoán. Người làm T-052 mang yêu cầu quan sát này sang bàn giao FlashTicket. Lặp lại cùng dev sẽ không bổ sung thông tin về nhóm thiếu quan sát. |
| Revision nguồn tĩnh | Hai snapshot và hash đã ghim. Chưa nối chắc với revision ứng dụng sinh benchmark. | Người làm T-052 trình kết luận T12 có điều kiện theo snapshot. Việc đối chiếu revision phải có nguồn provenance phù hợp, không suy từ số cạnh khớp. Nền T12 tắt không phụ thuộc chứng minh ích lợi của snapshot. |
| Verdict | WHY-68 đã ghi chưa chọn được verdict hợp lệ cho P7 từ dev hiện tại. V0 giữ trong mã và không phân biệt được cửa sổ lỗi ở phép C-e đã xem. | Người làm T-052 trình đầu ra/G3 dựa trên quyết định này. Đề xuất giữ V0 như trạng thái chẩn đoán có giới hạn, dùng cảnh báo hệ thống theo hướng MRP đã quyết. Hiệu chuẩn phải có dữ liệu bình thường cùng cỡ cửa sổ ở FlashTicket. |
| Nhãn vùng ảnh hưởng | Dataset công khai hiện chỉ hỗ trợ độ chứa root và độ rộng vùng. Độ đúng vùng ảnh hưởng chưa đo được. | T-052 mô tả vùng trên cấu hình cuối. P10 tạo nhãn độc lập với đầu vào RCA theo Q-210/WHY-06. Chỉ sau đó mới chấm độ đúng vùng. |
| Baseline, đối chứng và lợi ích quan hệ | C-d2 có MRR gộp cao hơn nền 3/624 trên cùng dev, chưa đủ để tuyên bố nền hơn quy tắc sớm nhất. Chưa có kiểm tổng quát hóa trên dữ liệu độc lập. | T-052 thực hiện T13, bảng baseline và đủ đối chứng đã duyệt, giữ C-d2. Hồ sơ G3 khóa thiết kế và giao thức trước P7. Người làm T-052 trình gói đầy đủ, Minh quyết quyền test. |
| Chế độ tự phát hiện (b) | Q-211/Q-212 đã hoãn quyết ở P7. T-051 chỉ triển khai (a). | Người làm T-052 phải trình phương án chế độ (b), miền dữ liệu có chuỗi thời gian hợp lệ và chi phí trong gói G3. Minh quyết phạm vi. Hướng này không được suy thành quyền mở dữ liệu khóa. |
| RE3-OB giữ ngoài | Q-211/Q-212 hoãn quyết. Quyền dữ liệu giữ ngoài còn khóa. | Người làm T-052 trình nguồn, cách dùng, phép đánh giá và dung lượng trước khi tải/mở. Minh quyết quyền dữ liệu trong gói G3. |
| Áp dụng FlashTicket | MRP đã đặt P9/P10 sau nghiên cứu phương pháp, gồm quan sát, tiêm lỗi/tải và đánh giá trên hệ bán vé. | Người làm P9/P10 nhận các yêu cầu về ánh xạ, dữ liệu bình thường, nhãn độc lập và các nhóm quan hệ thiếu trong dev. Triển khai phụ thuộc hệ thống và dữ liệu thực, theo task riêng được Minh duyệt. |

Nguồn trực tiếp gồm SPEC T-051 mục Tiêu chí xong, docs/KE-HOACH-SAU-T047.md mục T-052 và cập nhật hiện hành, WHY-06/68/72–75, Q-210–212, Q-241, MRP P6–P10 và đính chính T-050. Bảng này ghi hướng xử lý và phụ thuộc, không tự thay các quyết định đã hoãn.

## Những sai lệch của lượt đầu được giữ trong lịch sử

Pilot trước ghép nhãn đã không phủ ca mà cơ chế đổi phân loại. Kiểm native hồi cứu mới bù bằng chứng đúng đắn của nhánh có tác động. Thứ tự pilot lịch sử không thể thực hiện lại vào thời điểm trước chấm.

Phân rã thời gian và RAM lượt chính đầu đã không được lưu đủ. Đính chính lượt 1 đã đo bổ sung trên cùng đầu vào, đối chiếu kết quả và phân biệt số mới với lịch sử. Không có phép chạy nào khôi phục được mốc thời gian chưa từng ghi.

Hai sai lệch được công khai khi nghiệm thu. Phần kỹ thuật có thể kiểm và lưu hiện nay được hoàn tất trong lượt này, thay vì tiếp tục coi là đang chờ phương án.
