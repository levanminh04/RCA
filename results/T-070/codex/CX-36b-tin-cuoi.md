**CHƯA ĐẠT để dùng v2c chốt tử số khi lưới ngoại tuyến bị đứt.** Bản sửa đạt cả hai ca gốc của CX-33 và CX-33b, nhưng hai ca giả bổ sung cho thấy bộ chấm vẫn có thể kết luận sai.

| Điểm kiểm | Kết quả |
|---|---|
| Phạm vi ghi | **ĐẠT.** Trong `results/T-072`, chỉ ba tệp được phép có mtime thuộc lượt CX-36. SHA-256 của cả ba khớp báo cáo. Nhật ký lệnh không ghi nhận sửa quy tắc, sửa diễn giải p95 hay chấm lại E4. |
| A · Đầu khoảng ở giây 70 | **ĐẠT.** Alerting ở giây 80 vẫn được liệt kê, tỷ lệ đổi từ **1/1** thành **0/1**. Đối chứng Alerting ở giây 120 vẫn là **1/1**. |
| D · Ca gốc thiếu bước 30–110 | **ĐẠT.** Hai lịch sử đầy đủ cho **0/2** và **1/2**. Với lưới khuyết, v2c trả `chua-phan-xu`. |
| Hồi quy và tái lập | **ĐẠT.** Cả 9 ca cũ đạt trên hai bản. Số khoảng cháy khớp `[0,1,2,2,2,2,2,2]`. Hai biên bản chạy lại khớp từng byte với bản lưu, cả sáu hash mã thực chạy đều khớp. |

**Hai lỗi còn lại**

1. **CHƯA ĐẠT · Chốt 0 khi tử số có thể là 1.** Bắt đầu chấm ở giây 60. Tín hiệu đúng từ giây 20 đến 70, thiếu bước 80, sai ở giây 90. Nếu bước 80 đúng, cảnh báo vừa đủ 60 giây và kết quả là **1/2**. Nếu sai, kết quả là **0/2**. V2c trả **0/2** vì chỉ xét lỗ khi bước đầu sau lỗ đúng. Sửa tối thiểu là xét cả trường hợp Pending có thể chuyển sang Alerting ngay trong lỗ rồi kết thúc ở mẫu kế tiếp. [Nhánh bỏ sót](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2c.py:134)
2. **CHƯA ĐẠT · Báo chưa phân xử khi tử số chắc chắn là 1.** Chỉ thiếu bước 110. Điền đúng hoặc sai cho hai mốc Alerting là 110 hoặc 180, đều thuộc phút khỏe. Cả hai lần chạy đủ đều đếm **1**. V2c trả `chua-phan-xu` vì xét cả phút flash ở giữa, dù cảnh báo không thể bắt đầu ở phút đó. Sửa tối thiểu là chỉ so lớp của các mốc Alerting thực sự có thể xảy ra. [Phép xét lớp phút](D:/RCA-flashticket/results/T-072/v2/cham_offline_v2c.py:265)

Đề nghị giữ hai ca này làm hồi quy khi Minh duyệt sửa. Phiên kiểm chỉ đọc, không sửa tệp nào.