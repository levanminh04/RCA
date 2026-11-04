# C1 — T1 không bất biến theo xáo hàng

Trạng thái: **CHẶN bước 3 trở đi; chưa sửa src, chưa duyệt ứng viên.** Ghi 2026-11-02T14:17:33+07:00.

## Quan sát và chuỗi bằng chứng

T1 đã đủ 238 lượt cấu hình–ca chính. Seed 0/1/2 trùng byte. Xáo hàng lệch đúng hai trường `p_len` trên 52 ca; các trường còn lại, gồm cờ, tầng và thứ hạng, trùng. Nguồn: `t1.json#/bat_bien`; `runs/b2-t1-xao0-001/so-xao-chan-doan-001.json#/ca_lech` và hai tệp `different-*.json`.

Cả hai trường thuộc `metric|ts-admin-travel-service_latency-90`. Các cặp (mốc, giá trị) N/A giữ nguyên, chỉ hoán vị thứ tự. Raw đã kiểm hash qua allowlist; chẩn đoán không đọc nhãn chấm.

| Ca | Độ dài khối b | p gốc → p xáo |
|---|---|---|
| `dev-98bc73c499` | 60 → 43 | 0.00396825396825 → 0.00108225108225 |
| `dev-ba831dbeb8` | 60 → 12 | 0.00396825396825 → 0.000499750124938 |

Nguồn số: `runs/t1-xao-dieu-tra-002/summary.json` và từng ca, `#/versions/original`, `#/versions/shuffled`. N có hai mức 0,235 và 0,23500000000000004. Thứ tự thêm ô vào dict theo thứ tự hàng đi qua `o_1s`; `tu_tuong_quan` dùng `list(o.values())` và cộng các cặp theo thứ tự dict. Sai số trung bình/phương sai trên chuỗi gần hằng khuếch đại khi chuẩn hóa thành rho; rho làm đổi b, số khối, rồi không gian chia khối và p. Sắp lại theo thời gian phục hồi b/p gốc ở cả hai ca. Ca đối chiếu cùng đơn vị `dev-03d4910932` có biến thiên rõ hơn: b và p không đổi giữa hai thứ tự. Xem `#/versions/sorted_shuffled` và ca đối chiếu trong cùng thư mục.

**Phân loại đã xác nhận:** lỗi tất định số học/thứ tự xử lý trong cài đặt G3, tại `src/m1/cong.py` hàm `o_1s`, `tu_tuong_quan`. Không có bằng chứng adapter đổi tập mẫu: chẩn đoán kiểm cùng cặp mẫu và ghép mốc đúng. Không phải đổi ngẫu nhiên seed; ba seed đã trùng đầu ra và G3 khóa seed theo mã đơn vị/hướng. Không nới tiêu chí T1 vì hiện cờ/hạng chưa đổi: p/b đã thay đổi thực sự và SPEC yêu cầu bất biến.

**OPEN riêng:** ý nghĩa thống kê và độ ổn định của G3 trên chuỗi gần hằng ở mức độ chính xác máy. Sửa thứ tự không xác nhận hiệu chuẩn G3, không giải quyết câu hỏi có nên đặt điều kiện gần hằng. Không tự thêm epsilon hoặc sàn phương sai.

## Đề xuất sửa tối thiểu — chưa áp dụng

Patch cụ thể: `runs/de-xuat-c1-003/de-xuat.patch`; bản nguồn dự kiến `cong-proposed.py`. Chỉ hai hàm:

1. `o_1s`: gom mẫu theo ô; tổng `math.fsum` trên dãy giá trị đã sắp; xuất ô theo thời gian tăng (chỉ số ô N giảm).
2. `tu_tuong_quan`: mảng và các cặp rho dùng cùng thứ tự chỉ số ô đã khóa, thay vì thứ tự chèn dict.

Giữ công thức trung bình/phương sai/rho, điều kiện phương sai bằng 0, ngưỡng rho, giới hạn b, số hoán vị, seed, cửa sổ, G3/D1/S1, h, ma trận và luật chọn. Tổng bù tránh mất số hạng nhỏ khi nhiều mẫu chung một ô. Không làm tròn dữ liệu hoặc đặt ngưỡng gần hằng.

Ứng viên riêng đã qua 3 phép kiểm: hoán vị chuỗi gần hằng; nhiều mẫu chung ô với đáp án tổng biết trước; điều kiện ít ô/phương sai bằng 0. Đã kiểm bản patch trong namespace tách rời trên hai đơn vị lỗi và một đơn vị đối chiếu: cùng cặp mẫu, b/p bất biến và khớp bản gốc hiện lưu. Nguồn: `runs/ung-vien-tat-dinh-002/junit.xml`, `runs/de-xuat-c1-003/kiem-ung-vien.json`. **Chưa kiểm tích hợp toàn chuỗi hoặc mọi đơn vị/dev. Không gắn ứng viên vào M1 đang dùng.** `src` vẫn nguyên byte.

## Bản đồ ảnh hưởng xin Minh duyệt

| File/phạm vi | Thay đổi đề nghị | Tác động và lý do |
|---|---|---|
| `src/m1/cong.py` | Áp đúng patch C1 ở trên | Mọi phép G3 có thể chịu ảnh hưởng số học; mặc định G0/D0 không gọi tệp này. Cần hồi quy và chạy lại bằng code có đính chính. |
| `results/T-047/` | Giữ mọi lượt; bổ sung test, metadata hash nguồn thực, lượt mới, T1 và K/hậu xử lý | Không gắn số cũ với code đã sửa; không dùng lại kết quả chỉ vì từng PASS. Phần không phụ thuộc sửa được giữ sau kiểm hash. |
| `tasks/T-047-khoi-k-luot-2/LOG.md` | Chỉ nối lời duyệt thật, phạm vi C1, hash, kiểm và bàn giao | Giữ lịch sử và căn cứ đổi nguồn chạy từ c298188e sang c298188e cộng patch C1. |
| Dòng T-047 trong `docs/STATE.md` | Cập nhật bước làm theo kết quả thật | Không tự nghiệm thu hoặc đóng task. |
| `docs/DECISIONS.md` | Đề nghị một dòng Q-233, nếu mã còn trống, ghi nguyên văn lời duyệt thật và phạm vi C1/ngân sách Minh quyết | Đây là quyền bổ sung cần duyệt riêng; chưa ghi dòng này. Không sửa quyết định cũ. |

Không sửa SPEC đã khóa, WHY hoặc manifest T-043–T-046. Đề nghị duyệt đính chính cài đặt C1 làm ngoại lệ nguồn code: nguồn gốc c298188e cộng patch đã duyệt, không gọi là byte nguyên bản c298188e. Nguồn src của T-046 cũ kiểm bằng `git show c298188e`, kết quả cũ vẫn kiểm theo manifest cũ; nguồn mới và patch ghi hash tại T-047. Metadata mới phải ghi rõ nguồn thực, không chỉ mang revision cũ.

Sau khi được duyệt: kiểm cài đặt mặc định/adapter và ứng viên đã tích hợp; chạy thử đo thời gian/RAM; chạy lại phần T1 bị phụ thuộc vào G3 đã sửa rồi mới K. Đối chiếu T-046 phải giải thích lệch do C1 nếu có, không tự đổi tiêu chí hoặc coi mọi lệch là hợp lệ. Nếu xuất hiện mâu thuẫn SPEC hoặc cần đổi công thức/ma trận/tham số, dừng phần phụ thuộc trình Minh.

Chi phí dự báo CHƯA KIỂM: sửa/hồi quy/đo lại khoảng 15–25 phút; T1 khoảng 60–85 phút; K khoảng 2–3 giờ; cơ chế/độ bền/độ nhạy/bảng/báo cáo khoảng 45–75 phút. Tổng còn lại khoảng 4–5,5 giờ nếu không có lỗi mới; có thể vượt phần còn lại của trần 7 giờ. Đề nghị Minh quyết quyền sửa và, nếu muốn duyệt cùng gói chạy tiếp, **trần tổng 8 giờ**, tính cả mọi lượt đã chạy, không phải thêm 8 giờ mới. Chưa tự nới trần. Nếu chỉ duyệt sửa và giữ 7 giờ, phải đo/dự báo lại trước lượt nặng; dự báo vượt thì dừng.

## Phần nghiên cứu và nghĩa vụ còn lại

Đã có bằng chứng cài đặt về bất biến hash seed và một lỗi theo thứ tự hàng, Đ5 D1, QT5 và đối chiếu R0 thật/C-e với T-046. Chưa có K, D2 mới, lựa chọn khối, bootstrap hay bảng 2×2. Không trả lời xong câu hỏi chọn thành phần, RQ3 hoặc lợi ích RCA. Lỗi cài đặt này không tự chứng minh phương pháp sai về hiệu quả, cũng không được bỏ vì hạng hiện chưa đổi.
