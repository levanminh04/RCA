# Hướng dẫn đọc phần RCA của FlashTicket

## Đọc từ mục tiêu đến quyết định

1. **Đề tài yêu cầu gì?** Đồ thị biểu diễn các dịch vụ và quan hệ phụ thuộc. Nhật ký, vết truy vết và số đo giúp khoanh vùng ảnh hưởng, phát hiện bất thường và xếp hạng nguyên nhân gốc (RCA). [Đề tài DT18](reference/sources/DT18-de-tai-va-nhiem-vu.md)
2. **Nghiên cứu trả lời thế nào?** Đọc phần tóm tắt và câu hỏi nghiên cứu. Nhóm kiểm các phương pháp trên dữ liệu công khai, phân tích ca sai, rồi thiết kế phương pháp đồ thị và thử trên FlashTicket. [Kế hoạch nghiên cứu MRP](MRP.md)
3. **Giai đoạn 2 làm gì trên FlashTicket?** Đọc §8.2 cho nhánh trình diễn, §8.3 cho nhánh đánh giá và §8.4 để thấy việc nào phụ thuộc việc nào. [Kế hoạch giai đoạn 2](techstack/KE-HOACH-GIAI-DOAN-2.md)
4. **Đã làm tới đâu?** Tra mã công việc (task), tình trạng nghiệm thu và việc đang chờ. Nhật ký từng task ghi các mốc chi tiết. [Trạng thái dự án](STATE.md)
5. **Minh đã duyệt gì?** Tìm theo mã task hoặc ngày để đọc phạm vi và ngoại lệ của quyết định. [Sổ quyết định](DECISIONS.md)
6. **Vì sao chọn cách đó?** Tra lý do, phương án đã cân nhắc và kết luận phụ thuộc vào lựa chọn. [Sổ lý do](WHY.md)

## Lần theo một task

Ví dụ với T-069, đọc **SPEC** để biết điều kiện nào được tính là tụt hạng. Sang **LOG**, tìm mốc Minh nghiệm thu và ngoại lệ đi kèm. Mở **results** để xem trường hợp cụ thể và đọc bản đính chính trước khi trích kết luận. [SPEC](../tasks/T-069-v082-ban-ghim/SPEC.md) · [LOG](../tasks/T-069-v082-ban-ghim/LOG.md) · [Kết quả và đính chính](../results/T-069/dinh-chinh-1.md)

| Task | Việc đã làm và kết quả chính | File nên mở |
|---|---|---|
| T-066 | Dựng lại môi trường quan sát và tải từ repo lab. Ca `e2e-001` chạy trọn từ phát tải đến xuất kết quả RCA. | [Hồ sơ ca chạy](../results/T-066/e2e-001/README.md) |
| T-067 | Ghim phiên bản FlashTicket trên máy ứng dụng và kiểm tín hiệu của luồng mua vé. Minh đã nghiệm thu bản ghim. | [Kiểm tín hiệu](../results/T-067/kiem-tin-hieu.md) · [LOG nghiệm thu](../tasks/T-067-ban-flashticket-ghim/LOG.md) |
| T-068 | Tổ chức lại các trang Grafana. Từ một ca sự cố, người xem có thể mở đồ thị dịch vụ dựng từ vết truy vết gốc. | [Nhật ký dựng và kiểm đồ thị](../tasks/T-068-don-grafana/LOG.md) |
| T-069 | Kiểm lại phương pháp V082 trên bản ghim. Ở ca `CPU-BOOK-1`, dịch vụ gốc tụt hạng cả ở lần thu chính và lần lặp. Minh nghiệm thu với ngoại lệ này. | [Đính chính kết quả](../results/T-069/dinh-chinh-1.md) · [LOG nghiệm thu](../tasks/T-069-v082-ban-ghim/LOG.md) |
| T-070 | Điều phối lịch máy cho các nhóm dùng chung. Sau lượt thử trực tuyến E5, khung máy S4 đã đóng và máy quan sát đã về cấu hình sau thử nghiệm. | [Sổ trạng thái điều phối](../tasks/T-070-dieu-phoi-giai-doan-2/TRANG-THAI.json) |
| T-071 | Chạy tải nền, phân loại từng phút để có mẫu chấm báo động giả. E4 có 383 phút hệ thống khỏe ở mức tải chuẩn (×1). | [Tổng hợp E4, `#/khoe_x1_phut`](../results/T-071/e4/phan-loai-tom-tat.txt) |
| T-072 | Đặt ngưỡng cảnh báo bằng đợt nền E2, rồi chấm trên E4. Có 0 sự cố báo giả trong các phút khỏe ở tải chuẩn. Kết quả này chưa cho biết khả năng phát hiện lỗi thật. | [Bảng chấm, `#/ty_le_khoe_x1/su_co`](../results/T-072/bang-bao-dong-gia.json) |
| T-073 | Thử RCA trực tuyến khi tạm dừng Payment. Cảnh báo đã kích hoạt chẩn đoán và Grafana hiện kết quả trong hạn. Một số chuỗi số đo Payment bị khuyết mẫu. | [Kết quả E5](../results/T-073/e5-ket-qua.md) · [Đính chính về Payment](../results/T-073/dap-cx21/dinh-chinh-e5-3.md) |
| T-074 | Thiết kế cách đánh giá trên FlashTicket. Đã tách lượt chuẩn bị E6, còn ở bản nháp, khỏi phần cần chốt trước đợt đánh giá W7. | [Nháp E6](../results/T-074/e6-spec-nhap-3.md) · [Thiết kế W7](../results/T-074/thiet-ke-w6-5.md) |
| T-075 | Soạn khuôn giải thích kết quả bằng mô hình ngôn ngữ lớn (LLM) và kiểm trích dẫn bằng các đầu ra mẫu. Đã thử ngoại tuyến, chưa gọi mô hình. | [Bản thử và kết quả](../results/T-075/ban-2.md) |

## Dữ liệu và phần chạy được

Các gói dữ liệu lớn của chiến dịch FlashTicket nằm ngoài Git tại `D:/RCA-archive/`. Mỗi nhóm có danh sách SHA-256 để đối chiếu bản sao. Với bộ dữ liệu nghiên cứu trong `data/`, tra nguồn, phiên bản và cách dựng lại trong README dữ liệu. [Vị trí lưu trữ, §12](../AGENTS.md) · [README dữ liệu](../data/README.md)

Ở repo lab, bắt đầu từ sơ đồ trong README. Để theo một ca trực tuyến, đọc luật nào phát cảnh báo, rồi xem bộ điều phối nhận cảnh báo và gọi RCA ra sao. Để hiểu tải dùng khi thử, xem bộ chạy chuỗi lượt k6. [README lab](https://github.com/levanminh04/flashticket-rca-lab/blob/main/README.md) · [Luật cảnh báo](https://github.com/levanminh04/flashticket-rca-lab/blob/main/observability/grafana/provisioning/alerting/t072-luat.yaml) · [Bộ điều phối](https://github.com/levanminh04/flashticket-rca-lab/blob/main/campaigns/online/orchestrator.py) · [Bộ chuỗi tải](https://github.com/levanminh04/flashticket-rca-lab/blob/main/load/controller/chuoi_tai.py)
