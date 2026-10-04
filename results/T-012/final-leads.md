# Ba đầu mối cuối và phạm vi bằng chứng

Đọc nguồn chính thức ngày 03/10/2026, sau hai truy vấn còn lại S5/S6. Snapshot và hash ở [manifest run-003](runs/run-003/source-manifest.json). Không mở raw, archive kết quả dự đoán hoặc file số đo Bank. Không dùng điểm phương pháp trong hai bài làm căn cứ chọn bảo toàn hoặc chất lượng dataset.

| Đầu mối | Phân loại từ nguồn chính thức | Tác động tới khảo sát |
|---|---|---|
| [How Far Can RCA Go on Real-World Telemetry Data?](https://arxiv.org/html/2607.13548v1) | Bài dùng lại OpenRCA; phần IV-A xác nhận các hệ Market/Bank/Telecom | Không tạo dataset độc lập hoặc thêm thẻ trùng. Phạm vi window/query đã biết và số lỗi cho trước không tự là detector liên tục. Chỉ lấy provenance/protocol; không dùng phân tích hậu nghiệm của bài để khẳng định dữ liệu Bank đã phân xử được. |
| [Why Do AI Agents Systematically Fail at Cloud RCA?](https://arxiv.org/html/2602.09937v1) | Nghiên cứu agent trên benchmark OpenRCA, không công bố corpus telemetry mới trong mô tả đã đọc | Kết quả của agent không biến thành incident mới, nhãn vùng mới hoặc bộ độc lập. Không tải artifact agent. |
| [FAMOS TrainTicket](https://zenodo.org/records/13120167) | Record ngày 29/07/2024; người tạo Chiming Duan; CC-BY-4.0; một `train-ticket.zip`, 287.053.696 byte | Ngoài cửa sổ dataset công bố 2025–2026 của T-012. Giữ nguồn lịch sử, không tự bỏ khỏi cân nhắc G1 hoặc thêm vào tập thí nghiệm. Census/root/time/collector/reuse OPEN vì record không mô tả và archive chưa mở. Số byte không là incident; không suy sang hệ Mall. |

Toàn lượt có 11 hồ sơ chính thức, gồm LO2v2 là hồ sơ riêng sau record v1. Dừng tìm ở giới hạn sáu truy vấn. Lượt này không exhaustive; phần thời gian web trước checkpoint không có phép đo nên không dựng lại thành số thực đo. Có 14 thẻ của các biến thể scoped; hai bài reuse và record năm 2024 ở bảng này không đếm thành dataset mới năm 2025–2026.
