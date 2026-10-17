# T-032 — Thiết kế phép đổi tất định, bản 005: K-2 theo loại cạnh (CIRCA, chỉ RE2-TT)

Viết ngày 11/10/2026 (khoảng 04:05 +07), trước khi chạy hai nhánh dưới đây. Người viết: Claude. Minh duyệt chạy trong chat ngày 11/10 ("duyệt" cho đề xuất 2 của lượt trả lời trước). Các bản 001–003 giữ nguyên; quy tắc chung ở mục 3 của bản 001 áp dụng y nguyên.

## 1. Điều tôi đã thấy trước khi viết

Toàn bộ kết quả K-2 và nhánh quan sát của lượt `runs/circa-laptop-k2-001` (`ket-qua-phien-10.md` mục 1): bỏ mọi cạnh thì 0/11 nút còn cực lớn; hồi quy theo cha làm tăng điểm ở 3.285/4.526 nút; tỷ số điểm tăng theo số cha; nút cực lớn `ts-admin-travel-service_latency` có 7 cha, gồm 5 metric của chính dịch vụ đó và 2 metric latency của dịch vụ nó gọi (xem một ca, `dev-a5cabe5fa7`). Trong 30 đồ thị có 7.220 cạnh cùng dịch vụ và 3.709 cạnh giữa hai dịch vụ. Vì vậy hai nhánh này là câu hỏi đặt ra sau khi xem dữ liệu dev; kết quả chỉ là bằng chứng trên dev.

## 2. Câu hỏi

K-2 bỏ mọi cạnh cùng lúc. Chưa biết phần tăng điểm và giá trị cực lớn đến từ cạnh nối hai metric của **cùng một dịch vụ** hay cạnh nối metric của **hai dịch vụ khác nhau**. Hai loại cạnh này ứng với hai loại thông tin khác nhau: loại đầu không dùng quan hệ gọi giữa các dịch vụ, loại sau có dùng. Câu trả lời liên quan tới việc một phương pháp đồ thị nên lan thông tin theo loại quan hệ nào.

## 3. Hai nhánh

Dịch vụ của một nút lấy bằng đúng hàm `circa_kien_truc.builder.metric_mapping` mà phương pháp dùng.

| Nhánh | Cạnh bị bỏ (bước duy nhất bị đổi) | Cạnh giữ lại |
|---|---|---|
| `k2x` | mọi cạnh nối hai nút thuộc hai dịch vụ khác nhau | cạnh cùng dịch vụ |
| `k2s` | mọi cạnh nối hai nút thuộc cùng một dịch vụ | cạnh giữa hai dịch vụ |

Giữ: tập nút, frame, cửa sổ train/test, `current`, hồi quy OLS, chuẩn hóa phần dư, bước DA, cách xếp. Thực hiện như nhánh `k2` của bản 003: bọc `p3.adapters.circa.do_thi` trong tiến trình con, không sửa file mã nguồn.

**Sham:** chạy lại nhánh sham trong chính lượt mới; hai bản ghi phải trùng bản đóng băng từng bit ở 30/30 ca, nếu không thì dừng. Nhánh `k2` (không cạnh) dùng lại từ lượt `circa-laptop-k2-001`, không chạy lại.

## 4. Đại lượng (khai trước)

Với mỗi ca và mỗi nhánh trong bốn nhánh native, `k2x`, `k2s`, `k2`: số nút có điểm RHT vượt 1e10; với từng nút, điểm RHT; hạng root (rank_min, rank_max) ở bảng RHT; Hit@1, Hit@5 bi quan theo hòa. Với mỗi nút có hồi quy ở native: điểm ở từng nhánh so với điểm không cạnh. Báo riêng 11 ca có nút cực lớn và 19 ca còn lại (Q-82). Bảng có DA của hai nhánh mới được lưu nhưng không dùng để kết luận về DA.

## 5. Dự đoán đối lập

- **H-nội-bộ:** phần tăng điểm đến từ cạnh cùng dịch vụ. Khi đó `k2x` (còn cạnh cùng dịch vụ) cho điểm gần native, `k2s` cho điểm gần không cạnh; số nút "điểm cao hơn không cạnh" ở `k2x` gần 3.285, ở `k2s` nhỏ.
- **H-liên-dịch-vụ:** ngược lại.
- **Cả hai:** mỗi loại cạnh đóng một phần; hai con số đều lớn.
- **Giá trị cực lớn:** nút cực lớn có cha ở cả hai loại. Nếu chỉ cần có bất kỳ cha nào là đủ sinh giá trị cực lớn thì nó còn ở cả `k2x` lẫn `k2s` (11/11 mỗi nhánh). Nếu chỉ một loại cha gây ra thì nó mất ở nhánh bỏ loại đó.

## 6. Giới hạn

Hai nhánh không tách được tác dụng của từng cạnh riêng lẻ, và không đánh giá chất lượng của đồ thị gọi. Kết quả không phải thành tích của một phương pháp và không thay số P3. Không dùng kết quả để chọn cấu hình CIRCA.

## 7. Nơi chạy và chi phí

Laptop, 90 tiến trình con (sham, `k2x`, `k2s` cho 30 ca), canh RAM như bản 003 mục 4. Ước lượng từ lượt 001 (597,5 s cho 90 tiến trình con): khoảng 10 phút, không kể thời gian chờ RAM.
