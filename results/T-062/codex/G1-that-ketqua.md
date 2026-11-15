G1-THAT ĐẠT MỘT PHẦN

Đã kiểm Grafana thật bằng Edge headless 157.0.4341.46, Playwright 1.65.0 và API Grafana 13.3.0. Phép đo mất 15,6 phút.

[Báo cáo đầy đủ, URL, thông báo lỗi và danh sách 16 ảnh](D:/RCA-flashticket/results/T-062/codex/g1-that/BAO-CAO.md).

| Ca | Danh sách | Nút/cạnh | Hạng | Bằng chứng #1 | Explore | Phát lại |
|---|---|---|---|---|---|---|
| e8661e0a | Đạt, 9 dòng | 17/14 | Khớp* | 2 | Menu đạt; bảng lỗi 2 link | Khớp** |
| 00eaea92 | Đạt | 17/14 | Khớp* | 4 | Menu đạt; bảng lỗi 4 link | Khớp** |
| bf17acbf | Đạt | 17/14 | Khớp* | 15 | Menu đạt; bảng lỗi 14 link | Khớp** |
| f728fce2 | Đạt | 17/14 | Khớp* | 1 | Menu đạt; bảng không có link | Khớp** |
| 6c1a9fd8 | Đạt | 17/14 | Khớp* | 1 | Menu đạt; bảng lỗi 1 link | Khớp** |
| 2e2a5541 | Đạt | 17/14 | Khớp* | 8 | Menu đạt; bảng lỗi 8 link | Khớp** |
| a89954d1 | Đạt | 17/14 | Khớp* | 4 | Menu đạt; bảng lỗi 3 link | Khớp** |
| 1ad3afeb | Đạt | 17/14 | Khớp* | 13 | Menu đạt; bảng lỗi 13 link | Khớp** |
| a5539fba | Đạt | 17/14 | Khớp* | 2 | Menu đạt; bảng lỗi 2 link | Khớp** |

*Dashboard ẩn số hạng của nhóm “bình thường”, dù JSON có `hang`.

**Phát lại khớp trường `thanh_phan_tiem`. Riêng NET-GW-BOOK hiển thị “api-gateway — bị kéo theo #4”; bảng chấm ghi hạng tốt nhất trong tập chấp nhận là #1. Báo cáo giữ nguyên cả hai thông tin.

Các điểm quan sát chính:

- **47/47 link trong bảng bằng chứng bị mã hóa hai lần.** Mở thử Tempo và Prometheus hiện “Could not parse Explore URL”, truy vấn trống và “No data”.
- Sáu link từ menu nút của hai ca mở thành công: Tempo, Loki và Prometheus đều có dữ liệu.
- Panel 5xx báo “No data” ở 5 ca; panel log có bộ lọc báo “No data” ở 7 ca. API cùng truy vấn/cửa sổ trả rỗng, không báo lỗi.
- Trang chính không thấy giá trị đáp án, nhưng có chữ “đáp án” trong link sang trang phát lại; điều kiện nguyên văn không có chữ này chưa đạt.

Chỉ tạo đầu ra trong thư mục được phép và gói npm tạm. Không sửa Grafana, không đọc các bản phản biện G1. Đã đóng trình duyệt và đường hầm riêng; SSH cũ giữ nguyên.

**Giới hạn:** kết quả áp dụng Grafana version 4 đã đo. Bộ sinh và hai dashboard JSON local thay đổi trong lúc kiểm; phiên này không sửa chúng và chưa kiểm bản mới.