# T-034 V5 — Bổ sung sau phản biện (lượt dựng `g2-build-002`)

Ngày 13/10/2026. Nối tiếp `runs/g2-build-001/v5-kiem-lap-luan.md`; bản đó giữ nguyên. Nguồn: hai lượt phản biện của Codex và hai lượt đáp của Claude, đều trong chat; Minh duyệt sửa bằng lời “duyệt sửa”.

## 1. Chỗ bản V5 đầu bỏ sót

Bản V5 đầu ghi kết luận E1 là “Giữ”. Điều đó sai: câu “quy tắc chấm qua tập nhiều dịch vụ không phải bước đưa dịch vụ gọi lên trên root” trái với chính kết quả (một cặp đảo chiều, cả hai bên còn bằng chứng) và trái dòng đầu của bảng diễn giải tôi khai trước. Tự kiểm của người viết đã không bắt được lỗi này; phản biện bắt được.

## 2. Đã sửa gì

| Điểm | Sửa | Ở đâu |
|---|---|---|
| E1, cờ một lần | Báo theo ba loại cặp: đảo chiều; điểm dịch vụ gọi giảm nhưng chưa đảo chiều; giữ nguyên điểm và quan hệ vì root không có tập được chấm. Kết luận: quy tắc có đóng góp, không đủ | `hai-phep-kiem.md` mục 0, 1.4, 1.5, 1.6; `goi-g2.md` dòng G2-H05, UV-4, câu 11 mục 7; thiết kế, Mục nối 6 |
| Cặp đảo chiều là ca đã nhìn | Ghi giới hạn khái quát; giữ mức CT | `hai-phep-kiem.md` mục 1.4; G2-H05; UV-4 |
| PF của E2 | “chuỗi tiền tố, mặt nạ tiền tố, thang toàn bản ghi; vẫn nhìn trước qua thang” | `hai-phep-kiem.md` mục 2.1 và bảng 2.3 |
| D5 thiếu nội dung | Thêm hiện tượng mất span cha, mẫu số, trạng thái cổng kiểm; thêm điều kiện thất bại cho UV-3 | G2-H19; UV-3 |
| D7 lẫn với D3 | Tách: Nezha-OB thiếu trường trạng thái; RE2-TT không có span mang mã lỗi | G2-H19 |
| M6 gắn sai điều kiện | Chuyển từ dòng lỗi return sang dòng trễ mạng; ghi nghĩa đúng của cờ | G2-H06, G2-H07 |
| HP-5, HP-9 | Thêm câu diễn giải | G2-H21 |
| TORAI: câu “lỗi giảm mẫu hai lần” | Bỏ; ghi cụm một dịch vụ, nhánh dự phòng, RCD; ghi bản đang dùng là bản đã sửa | G2-H15 |
| TORAI: “không dựa vào quan hệ gọi” | Bỏ câu toàn pipeline; giữ kết luận hẹp về RCD; ghi khâu dựng trace nguồn B có dùng quan hệ cha–con | `goi-g2.md` mục 0, câu 3 mục 1, câu 4 và 14 mục 7 |

Không số nào đã phát hành bị đổi. Hai văn bản dùng thêm bảy số (từ 2.427 lên 2.434), đều có con trỏ nguồn. `bang-baseline.json` và `hai-phep-kiem.json` không đổi.

## 3. Kiểm sau sửa

- V3: đạt (M6 nay thuộc G2-H06; mọi mã gốc vẫn có chỗ).
- V4: đạt trên lượt `g2-build-002` (`v4.json` cùng thư mục).
- Quét lại các câu phủ định tuyệt đối về E1 và câu “không dựa vào quan hệ gọi” trong hai văn bản: không còn.

## 4. Bài học cho phép tự kiểm

V3 chỉ đếm mã có mặt, không kiểm nội dung của mã có được mang sang không. Ba chỗ thiếu (D5, D7, M6) đều qua V3. Tôi không đề xuất thêm phép kiểm; chỉ ghi giới hạn này để người đọc V3 không hiểu “đủ mã” là “đủ nội dung”.
