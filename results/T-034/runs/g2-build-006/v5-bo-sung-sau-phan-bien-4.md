# V5 bổ sung sau lượt phản biện thứ tư (14/10/2026)

Phép đọc, không phải phép máy. Bản trước: `results/T-034/runs/phat-hanh-004/`. Lượt dựng dùng để phát hành: `g2-build-006`. Lượt `g2-build-005` hỏng V4 vì một chữ số ngày tháng viết sai dạng ở dòng mở đầu; giữ làm lượt lỗi, không dùng.

## Điều V5 lượt trước đã bỏ sót

- Lượt 004 sửa UV-7 thành "chưa có dự đoán" nhưng để nguyên câu mở đầu mục 5 nói mọi ứng viên đã đủ căn cứ để thử. Hai chỗ mâu thuẫn nhau.
- G2-H23 ghi "không tách theo ô" trong khi nguồn có số theo ca, ghép được với ô.
- Câu 16 mục 7 chỉ kể danh sách đã chốt; bỏ sót việc tầng hai chưa chạy và việc họ "học có đồ thị" chưa có đại diện xếp hạng.

## Nhận định đã đổi và căn cứ

| Chỗ | Nhận định mới | Căn cứ |
|---|---|---|
| Mở đầu mục 5; UV-7 | Phần (ii) của UV-7 là câu hỏi thiết kế, chưa là ứng viên. UV-10 là yêu cầu DT18, chưa có dự đoán kiểm được trên dev; vẫn phải thiết kế và kiểm khi có đầu vào phù hợp | MRP §3 (bậc "đề xuất để thử" đòi dự đoán có thể bác bỏ); thẻ dataset T-002, T-008 |
| G2-H23; Phụ lục C | Thêm bảng 10 ô cho hai nhánh nén. Tổng điểm đổi giảm ở chín ô, tăng ở ô route/mem | `results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/engine-final-summary-001.json#/slots`, ghép ô bằng `results/T-029/nhan-proxy-va-schema.json#/P1/cases`; tổng theo ô ghi ở `runs/g2-build-006/t033-dan-xuat.json#/by_cell`, bước dựng tự kiểm tổng 10 ô bằng tổng 30 ca |
| G2-H24 | Lý do không tách theo ô: giới hạn chung của dữ liệu; không dựng tỷ lệ khi không có nhãn thời điểm sự cố bắt đầu | G2-H24, trường "Vì sao" |
| Câu 16 mục 7 | Nêu ba tiêu chí chọn, các họ có đại diện, tầng hai chưa chạy, họ "học có đồ thị" chưa có đại diện xếp hạng | MRP mục P1; `results/T-001/danh-sach-phuong-phap.md` (bảng phủ các họ); Q-37, Q-38, Q-62; `docs/PLAN-P3-G2.md` |

## Giải thích khác và giới hạn

- Bảng G2-H23: mỗi ô ba ca; số điểm đổi không phải thước đo chất lượng; phép nén đổi cùng lúc nhiều yếu tố. Ô route/mem tăng là một quan sát, chưa có giải thích.
- Phụ lục A và B: người phản biện đã đối chiếu số ở lượt kiểm bản 004. Người làm chưa tự đọc từng dòng; căn cứ của người làm là bước dựng tự so tổng theo ô với T-028 và V4 đạt.
- Dòng B16 ở mục 6.2: người phản biện đã đọc toàn văn chuẩn quan sát và xác nhận; người làm chỉ tìm theo từ khóa.

## Điều không đổi

Số của bảng baseline, `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json`. Các câu còn mở: lan có đáng kể; đóng góp của chờ ở CIRCA; bước gây chênh giữa hai bản TraceRCA; underflow ngoài hai ca; thời điểm sự cố bắt đầu; lựa chọn P6; lợi ích đồ thị.
