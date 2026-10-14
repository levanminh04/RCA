# V5 bổ sung, lượt sửa thứ sáu (14/10/2026)

Phép đọc, không phải phép máy. Bản trước: `results/T-034/runs/phat-hanh-006/`. Lượt dựng dùng để phát hành: `g2-build-008`.

## Điều đã đổi

| Chỗ | Nội dung | Căn cứ |
|---|---|---|
| Mở đầu mục 5; UV-7; mục 6.1; câu 12 mục 7 | Câu hỏi "cách gộp điểm từ nút con lên nút cha" rời khỏi mục ứng viên, thành một dòng ở mục 6.1. UV-7 chỉ còn yêu cầu kỹ thuật "xử lý giá trị không hợp lệ trước khi lan", có dự đoán bác bỏ được | Đây là câu hỏi thiết kế phải giải quyết trên dev trước khi khóa thiết kế, nên thuộc mục 6.1, không thuộc mục 6.3 (sau khóa). Người phản biện và người làm cùng đề xuất; Minh duyệt |

Không số nào đổi. `ban-do-g2.json` chỉ khác ở trường thời điểm dựng và đường dẫn file dẫn xuất của lượt.

## Đính chính một giới hạn ghi ở bản V5 bổ sung thứ năm

Bản V5 của lượt `g2-build-007` ghi bảng G2-H24 "khớp ở mức tổng và một ca, chưa đối chiếu từng ca với file gốc". Điều đó đúng với phép kiểm của người làm ở lượt ấy. Sau đó người phản biện báo đã đối chiếu từng ca: tìm đầu ra BOCPD gốc của cả 30 ca trong `results/T-033/runs/checkpoint-handoff-001/artifacts/runs/` (dẫn ở `results/T-033/runs/session9-report-002/source-catalog.json`), kiểm mã băm, tính lại điểm đổi, và thấy khớp bảng. Người làm đã xác nhận các file đó có trên máy; người làm **không** tự lặp lại phép đối chiếu từng ca.

## Trạng thái tiêu chí xong của SPEC, theo người làm

- Mọi dòng G2-Hn có số hoặc bảng theo ô (Phụ lục A, B, C), giải thích khác, lời tác giả hoặc "chưa thấy".
- UV-1 đến UV-9 có mục đích, căn cứ, mức, giải thích khác và dự đoán bác bỏ được trên dev. Các thành phần DT18 yêu cầu và câu hỏi cách gộp điểm đứng ngoài danh sách ứng viên, có ghi lý do.
- K7 có 16 câu.
- Đây là tự đánh giá của người làm; việc nghiệm thu do Minh quyết.

## Điều không đổi

Số của bảng baseline, `hai-phep-kiem.md`, `hai-phep-kiem.json`, `bang-baseline.json`. Các câu còn mở: lan có đáng kể; đóng góp của chờ ở CIRCA; bước gây chênh giữa hai bản TraceRCA; underflow ngoài hai ca; thời điểm sự cố bắt đầu; lựa chọn P6; lợi ích đồ thị.
