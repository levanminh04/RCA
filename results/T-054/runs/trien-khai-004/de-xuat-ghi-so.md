# Đề nghị ghi sổ — chưa sửa DECISIONS/WHY

Phạm vi xin duyệt: chỉ nối cuối docs/DECISIONS.md và docs/WHY.md, không sửa lịch sử. Nguồn quyết định đã có trong LOG phiên5 và quyet-dinh-minh.json. Ảnh hưởng: thay các OPEN tương ứng của P7, không thay phương pháp/cohort/G3 hoặc quyền dữ liệu. Mã đề nghị dựa trên sổ hiện có; nếu sổ đổi trước khi duyệt phải kiểm lại mã, không ghi đè.

## Nối DECISIONS.md

### T-054 — gói chuẩn bị thu gọn và quyết định trước G3, 05/11/2026

| Mã | Ngày | Lời Minh/nguồn | Nội dung được ghi |
|---|---|---|---|
| Q-251 | 05/11/2026 | “DUYỆT TRIỂN KHAI TOÀN BỘ CÁC BƯỚC NÀY ... KHI NÀO SẴN SÀNG CHẠY CHÍNH THÌ DỪNG BÁO TÔI” | Dừng baseline dev diện rộng; chỉ bổ sung cho lỗi/phép đối chiếu cụ thể. Hoàn thiện vận hành driver, kiểm phần đổi, chỉ đo thêm 2 worker để chọn ổn định; không săn 3/4 worker. Chốt số học/lỗi/hết giờ/C-e/quyền nguồn trước test. Đủ điều kiện trình G3 rồi dừng báo; không tự chạy main/test/RE3/SSH hoặc commit. |
| Q-252 | 05/11/2026 | “Chấp nhận đúng ba sai khác; giữ 1 luồng” | Chấp nhận riêng ba sai khác so nguồn khác máy trong results/T-054/runs/trien-khai-003/numeric-parity-analysis.json: MicroRank OB một ca 1 ULP; M1/T12 một ca OB tối đa 2 ULP, trường rời rạc đã đối chiếu không đổi. Giữ 1 luồng; không dung sai chung, không làm tròn hoặc sửa kết quả. Sai khác mới vẫn cần phân xử. Không kết luận thread lịch sử là 16. |
| Q-253 | 05/11/2026 | “Duyệt cả hai công thức độ nhạy” | Bản loại lỗi bỏ nguyên cặp nếu M1 hoặc bất kỳ seed baseline có ERROR/TIMEOUT phương pháp đủ điều kiện, giữ NO_EVIDENCE/UNSUPPORTED, không bình quân seed sống; báo n/ô và CI trên cặp còn lại, rỗng N/A. TT hoán vị ca hai phía10.000 mẫu, seed20261005,+1 tử/mẫu; so thống kê chính xác. Cả hai chỉ độ nhạy, không điều khiển E-04/chuyển mức OB. |
| Q-254 | 05/11/2026 | “trừ khi chạy hàng chục tiếng chưa xong hoặc chạy lỗi. vòng lặp vô tận thì dừng, không thì cứ cho chạy, không tạo trần cố định” | Riêng P7: bỏ trần thời gian cộng dồn toàn đợt/method×dataset; chạy đủ cohort, giữ timeout từng lượt để xử lý treo. Khi lỗi, không tiến triển/lặp vô tận hoặc hàng chục giờ chưa xong thì dừng/báo Minh; không thay bằng một trần cố định. Lượt chưa chạy không là method TIMEOUT; giữ PENDING/BLOCKED và chặn bảng cần đủ cohort. Ngoại lệ Q-40/P3 chỉ áp P7, giữ lịch sử cũ. Không là quyền main/G3/test hoặc cho một lượt >1giờ. |

## Nối WHY.md

### WHY-79. Chuẩn bị P7 vừa đủ và các lựa chọn trước test — theo Q-251–Q-254

- Chọn: tái dùng G2/native và checkpoint003 đã kiểm pin; chỉ thêm phép kiểm cho nhánh công cụ thay đổi. Chỉ thử 2 worker. Giữ các slot độc lập; chưa dựng cache liên vế vì chưa có lợi ích đủ căn cứ so công cài/kiểm. Phương án thử mọi mức2/3/4 hoặc chạy lại diện rộng tăng công mà chưa giải một bất đồng khoa học cụ thể.
- Số học: giữ môi trường một luồng thống nhất, chấp nhận đúng ba sai khác nguồn đã nêu và giữ mọi kết quả. Lệch số liên tục cuối không đổi các trường rời rạc trong miền đã so; đây không là bảo đảm mọi ca hoặc dung sai chung. Phương án giữ exact và điều tra thêm đã trình; Minh chọn ngoại lệ hữu hạn, không sửa số để khớp.
- Thống kê: hai bảng nhạy đã chốt giúp thấy ảnh hưởng của phương pháp lỗi và giả định đơn vị hoán đổi; chúng không cấp thêm ngưỡng hoặc quyết định chính. Bản loại lỗi vẫn có chọn lọc theo lỗi, hoán vị ca vẫn có phụ thuộc cùng ô; không coi là chữa undercoverage.
- Thời gian: tổng thời gian chờ không phải lỗi thuật toán. Chạy đủ rồi đánh giá, giữ timeout cho phương pháp thực sự đã chạy; không gán lỗi cho ca chưa chạy để đóng mẫu số. Phương án trần P3 cố định giữ là lịch sử, riêng P7 dùng chỉ đạo mới của Minh. Nếu chạy lỗi hoặc không tiến triển/hàng chục giờ chưa xong, dừng báo thay vì tự nới hoặc phát thêm lô.
- Bằng chứng: manifest003, quyet-dinh-minh.json, operational/final-branch/sensitivity/C-e checks và pilot-2-worker-001/summary.json tại runs/trien-khai-004. Lô nhỏ chứng minh overlap/parity và phạm vi vận hành đã kiểm, chưa chứng minh lợi ích tốc độ toàn matrix hoặc hiệu quả độc lập.
- Kết luận phụ thuộc: tính hợp lệ/khả năng tái dựng bản P7 được trình khóa; chưa G3 hoặc grant nguồn/test/A/RE3, chưa nghiệm thu task/RQ3. RE3 vẫn có H1 schema/H2 adapter riêng trước lần đánh giá bản cuối, không bỏ khỏi nghiên cứu.
